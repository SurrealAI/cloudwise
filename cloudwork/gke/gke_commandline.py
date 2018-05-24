import cloudwork.utils as U
from .gke import GoogleCloudKubernetesLauncher


SEPARATOR = '\n---------------------------\n'

print('Welcome to Cloudwork for GKE.')
print('This is a interactive program to generate a terraform file to '
    'create a Google Cloud Kubernetes Cluster for machine learning experiments')

project = U.get_input("\nWhat is your project id? (e.g. plexiform-armor-123456): ")

print("\nPlease follow this guide: https://www.terraform.io/docs/providers/google/ to obtain authentication json.")
credential_file = U.get_file("Please provide path to the authentication json: ")

zone = U.get_input("\nWhich zone will your instances be in? (e.g. us-west1-b): ")

cluster_name = U.get_input("\nGive your kubernetes cluster a name: ")

launcher = GoogleCloudKubernetesLauncher(project=project,
                                         credential_file=credential_file,
                                         zone=zone,
                                         cluster_name=cluster_name)

print("\nSetting up the defalt node pool that will handle all miscellaneous workload")
machine_type = input('The machine type to use for default node pool [n1-standard-2]: ',
                     default='n1-standard-2')

all_templates.append(default_pool_template)

print("")
print("Now we will start creating machines dedicated for computation tasks")
print("They will be tainted so only designated workload will be scheduled on them")

nodes = [{'machine_type': 'n1-standard-8', 'gpu': None, 'gpu-count': None},
         {'machine_type': 'n1-standard-8', 'gpu': 'k80', 'gpu-count': 1}]

# while True:
#     print(SEPARATOR)
#     while True:
#         machine_type = input('\nThe machine type to use (e.g. n1-standard-8): ')
#         if machine_type:
#             break
#     while True:
#         machine_type = input('\nThe machine type to use (e.g. n1-standard-1): ')
#         if machine_type:
#             break
