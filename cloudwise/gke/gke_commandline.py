"""
Creates a kubernetes cluster on google cloud
"""
import json
import cloudwise.utils as U
from cloudwise.gke.gke import GKELauncher
import copy


def main():
    print('Welcome to Cloudwork for GKE.')
    print('This is a interactive program to generate a terraform file to '
          'create a Google Cloud Kubernetes Cluster for machine learning experiments')

    project = U.get_input("\nWhat is your project id? (e.g. plexiform-armor-123456): ",
                          input_type=str)

    print("\nPlease follow this guide: https://www.terraform.io/docs/providers/google/ to obtain authentication json.")
    print("\nRun `gcloud auth application-default login` if you skip the authentication JSON")
    credential_file = U.get_file("Please provide path to the authentication json [skip]: ")

    zone = U.get_input("\nWhich zone will your instances be in? [us-west1-b]: ",
                       input_type=str,
                       default='us-west1-b')

    cluster_name = U.get_input("\nGive your kubernetes cluster a name: ",
                               input_type=str)

    launcher = GKELauncher(project=project,
                           credential_file=credential_file,
                           zone=zone,
                           cluster_name=cluster_name)

    print("\nSetting up the defalt node pool that will handle all miscellaneous workload")
    machine_type = U.get_input('The machine type to use for default node pool [n1-standard-2]: ',
                               input_type=str,
                               default='n1-standard-2')
    max_count = U.get_input('The maximum number of nodes for default node pool [1000]: ',
                            input_type=int,
                            default=1000)
    launcher.add_nodepool(machine_type=machine_type,
                          min_node_count=3, 
                          max_node_count=max_count,
                          initial_node_count=3,
                          disk_size_gb=10,
                          name="np-default-{}".format(machine_type))

    print("")
    print("Now we will start creating machines dedicated for computation tasks")
    print("They will be tainted so only designated workload will be scheduled on them")
    configurations = [
        {
            'machine_type': 'n1-standard-2',
            'exclusive_workload': True,
        },
        {
            'machine_type': 'n1-standard-8',
            'exclusive_workload': True,
        },
        {
            'machine_type': 'n1-standard-8',
            'exclusive_workload': True,
            'gpu_type': 'nvidia-tesla-k80',
            'gpu_count': 1,
        },
        # {
        #     'machine_type': 'n1-standard-16',
        #     'exclusive_workload': True,
        #     'gpu_type': 'nvidia-tesla-k80',
        #     'gpu_count': 4,
        #     'max_node_count': 25,
        # },
        {
            'machine_type': 'n1-highmem-8',
            'exclusive_workload': True,
            'gpu_type': 'nvidia-tesla-p100',
            'gpu_count': 1,
        },
        {
            'machine_type': 'n1-highmem-8',
            'exclusive_workload': True,
            'gpu_type': 'nvidia-tesla-v100',
            'gpu_count': 1,
        },
        # {
        #     'machine_type': 'n1-standard-32',
        #     'exclusive_workload': True,
        #     'gpu_type': 'nvidia-tesla-v100',
        #     'gpu_count': 4,
        #     'max_node_count': 25,
        # },

    ]
    descriptions = [
        'machines with 2 cpu each, for small workload',
        'machines with 8 cpu each, for cpu workload',
        'machines with 8 cpu + 1 k80 each, for gpu workload',
        # 'machines with 16 cpu + 4 k80 each, for heavy gpu workload',
        'high memory machines with 8 cpu + 1 p100 each',
        # 'machines with 32 cpu + 4 p100 each',
        'high memory machines with 8 cpu + 1 v100 each',
        # 'machines with 32 cpu + 4 v100 each',

    ]

    confirmed_configurations = []
    for i in range(len(configurations)):
        configuration = configurations[i]
        configuration["max_node_count"] = 100
        configuration["disk_size_gb"] = 10
        description = descriptions[i]
        confirmed = U.get_yn('\nAdd {}?'.format(description), default=True)
        if confirmed:
            launcher.add_nodepool(**configuration)
            confirmed_configurations.append(configuration)
    if len(confirmed_configurations) > 0:
        confirmed = U.get_yn('\nAdd preemptible versions of all added node pools as well?', default=True)
        if confirmed:
            for configuration in confirmed_configurations:
                configuration = copy.copy(configuration)
                configuration['max_node_count'] = 1000
                launcher.add_nodepool(preemptible=True, **configuration)

    output_name = cluster_name + '.tf.json'
    fname = U.get_input('\nPlease provide a filename for the configured tf file [{}]'.format(output_name),
                        input_type=str,
                        default=output_name)

    with open(fname, 'w') as f:
        json.dump(launcher.config, f, sort_keys=True, indent=4)

    U.propose_next_action()

if __name__ == '__main__':
    main()
