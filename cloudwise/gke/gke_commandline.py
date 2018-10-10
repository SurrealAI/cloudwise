"""
Creates a kubernetes cluster on google cloud
"""
import json
import cloudwise.utils as U
from cloudwise.gke.gke import GKELauncher


def print_state(descriptions, added):
    print('\nAvailable node types:')
    max_length = max([len(x) for x in descriptions])
    for i, description in enumerate(descriptions):
        optional_text = ''
        if added[i]:
            optional_text = '(selected)'
        print('[{index:2}] {description: <{width}}  {optional}'
              .format(index=i,
                      description=description,
                      width=max_length,
                      optional=optional_text))


def print_actions(descriptions, combo_names, combo_node_lists):
    print('\nAvailable actions:')
    print('add <0~{}>'.format(len(descriptions) - 1))
    print('remove <0~{}>'.format(len(descriptions) - 1))
    print('combo <0~{}>'.format(len(combo_names) - 1))
    for i in range(len(combo_names)):
        combo_text = combo_names[i]
        nodes = combo_node_lists[i]
        node_list_str = ', '.join([descriptions[i] for i in nodes])
        print('\t[{}] {}: {}'.format(i, combo_text, node_list_str))
    print('done')
    print('exit')


def add_custom(launcher, preemptible):
    configurations = [
        {
            'machine_type': 'n1-standard-2',
            'exclusive_workload': True,
            'max_node_count': 256,
        },
        {
            'machine_type': 'n1-standard-8',
            'exclusive_workload': True,
            'max_node_count': 128,
        },
        {
            'machine_type': 'n1-standard-32',
            'exclusive_workload': True,
            'max_node_count': 128,
        },
        {
            'machine_type': 'n1-standard-8',
            'exclusive_workload': True,
            'gpu_type': 'nvidia-tesla-k80',
            'gpu_count': 1,
            'max_node_count': 128,
        },
        {
            'machine_type': 'n1-standard-32',
            'exclusive_workload': True,
            'gpu_type': 'nvidia-tesla-k80',
            'gpu_count': 4,
            'max_node_count': 128,
        },
        {
            'machine_type': 'n1-standard-12',
            'exclusive_workload': True,
            'gpu_type': 'nvidia-tesla-p100',
            'gpu_count': 1,
            'max_node_count': 128,
        },
        {
            'machine_type': 'n1-standard-48',
            'exclusive_workload': True,
            'gpu_type': 'nvidia-tesla-p100',
            'gpu_count': 4,
            'max_node_count': 128,
        },
        {
            'machine_type': 'n1-standard-12',
            'exclusive_workload': True,
            'gpu_type': 'nvidia-tesla-v100',
            'gpu_count': 1,
            'max_node_count': 128,
        },
        {
            'machine_type': 'n1-standard-48',
            'exclusive_workload': True,
            'gpu_type': 'nvidia-tesla-v100',
            'gpu_count': 4,
            'max_node_count': 128,
        },
    ]
    for i in range(len(configurations)):
        configurations[i]['disk_size_gb'] = 30
    descriptions = [
        '2 cpu',
        '8 cpu',
        '32 cpu',
        '8 cpu + 1 k80',
        '32 cpu + 4 k80',
        '12 cpu + 1 p100',
        '48 cpu + 4 p100',
        '12 cpu + 1 v100',
        '48 cpu + 4 v100',
    ]
    added = [False for x in descriptions]
    combo_names = [
        'minimal cpu',
        'minimal with k80',
        'for small/medium scale experiments, optimize for cost',
        'for large scale experiments'
    ]
    combo_node_lists = [
        [0, 1],
        [0, 1, 3],
        [1, 3, 5, 7],
        [2, 4, 6, 8],
    ]

    state_changed = True
    while True:
        if state_changed:
            print_state(descriptions, added)
            state_changed = False
        print_actions(descriptions, combo_names, combo_node_lists)
        actions = U.get_input('>', str)
        actions = actions.split(' ')
        if actions[0] not in ['add', 'remove', 'combo', 'done', 'exit']:
            continue
        elif actions[0] in ['add', 'remove', 'combo']:
            if len(actions) > 2:
                print('Too many arguments')
                continue
            if len(actions) < 2:
                print('Too few arguments')
                continue
            try:
                index = int(actions[1])
            except TypeError:
                print('Please provide a valid index')
                continue
            if actions[0] == 'add':
                if index not in range(len(descriptions)):
                    print('Please provide a valid index')
                    continue
                else:
                    added[index] = True
                    state_changed = True
                    continue
            if actions[0] == 'remove':
                if index not in range(len(descriptions)):
                    print('Please provide a valid index')
                    continue
                else:
                    added[index] = False
                    state_changed = True
                    continue
            if actions[0] == 'combo':
                if index not in range(len(combo_names)):
                    print('Please provide a valid index')
                    continue
                else:
                    for i in range(len(added)):
                        added[i] = i in combo_node_lists[index]
                    state_changed = True
                    continue
        elif actions[0] == 'done':
            break
        elif actions[0] == 'exit':
            exit(0)

    for i in range(len(configurations)):
        if added[i]:
            launcher.add_nodepool(preemptible=preemptible, **configurations[i])


def main():
    print('Welcome to Cloudwork for GKE.')
    print('This is a interactive program to generate a terraform file to '
          'create a Google Cloud Kubernetes Cluster for machine learning experiments')

    project = U.get_input("\nWhat is your project id? (e.g. plexiform-armor-123456): ",
                          input_type=str)

    print("\nPlease follow this guide: https://www.terraform.io/docs/providers/google/provider_reference.html to obtain authentication json.")
    credential_file = U.get_file("Provide path to the authentication json [or skip in case it is configured through environment variables]: ")

    zone = U.get_input("\nWhich zone will your instances be in? [us-west1-b]: ",
                       input_type=str, default='us-west1-b')

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
    max_count = U.get_input('The maximum number of nodes for default node pool [20]: ',
                            input_type=int,
                            default=20)
    launcher.add_nodepool(machine_type=machine_type,
                          min_node_count=3,
                          max_node_count=max_count,
                          initial_node_count=3,
                          disk_size_gb=30,
                          name="np-default-{}".format(machine_type))

    print("")
    print("Now we will start creating machines dedicated for computation tasks")
    print("They will be tainted so only designated workload will be scheduled on them")
    preemptible = U.get_yn("Use preemptible nodes?", default=False)
    add_custom(launcher, preemptible)

    output_name = cluster_name + '.tf.json'
    fname = U.get_input('\nPlease provide a filename for the configured tf file [{}]'.format(output_name),
                        input_type=str,
                        default=output_name)

    with open(fname, 'w') as f:
        json.dump(launcher.config, f, sort_keys=True, indent=4)

    U.propose_terraform_actions()
    print('You can use the following command after cluster creation to configure kubectl:')
    print('\n> gcloud container clusters get-credentials {}'.format(cluster_name))

    print('[IMPORTANT] If you have GPUs in your cluster, you need to install GPU drivers (see https://cloud.google.com/kubernetes-engine/docs/how-to/gpus#installing_drivers):')
    print('\n> kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/stable/nvidia-driver-installer/cos/daemonset-preloaded.yaml')

if __name__ == '__main__':
    main()
