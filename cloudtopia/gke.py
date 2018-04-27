from os import path
from pathlib import Path

SEPARATOR = '\n---------------------------\n'

print('Welcome to Overture for GKE.')
print('This is a interactive program to generate a terraform file to '
    'create a Google Cloud Kubernetes Cluster for machine learning experiments')

while True:
    project = input("What is your project id? (e.g. plexiform-armor-123456): ")
    if project:
        break

while True:
    # TODO: start from here
    print("\nPlease follow this guide: https://www.terraform.io/docs/providers/google/ to obtain authentication json.")
    credential_file_path = input("Please provide path to the authentication json: ")
    if not credential_file_path:
        break
    credential_file_path = path.expanduser(credential_file_path)
    # TODO: local path seems to not be working
    credential_file = Path(credential_file_path)
    if credential_file.exists():
        break
    print('Cannot find file {}'.format(credential_file_path))

while True:
    zone = input("\nWhich zone will your instances be in? (e.g. us-west1-b): ")
    if zone:
        break

while True:
    cluster_name = input("\nGive your kubernetes cluster a name: ")
    if project:
        break

all_templates = []

header_template = \
"""
variable "credential" {{
  default = "{}"
}}

variable "project" {{
  default = "{}"
}}

variable "zone" {{
  default = "{}"
}}

variable "cluster_name" {{
  default = "{}"
}}
""".format(credential_file_path, project, zone, cluster_name)
all_templates.append(header_template)

gke_cluster_template = \
"""
provider "google" {
  credentials = "${file(${var.credential})}"
  project     = "${var.project}"
  region      = "${var.zone}"
}

resource "google_container_cluster" "${var.cluster_name}" {
  name = "${var.cluster_name}"
  zone = "${var.zone}"
  min_master_version = "1.9"

  initial_node_count = 1
  remove_default_node_pool = true
}
"""
all_templates.append(gke_cluster_template)

print("\nSetting up the defalt node pool that will handle all miscellaneous workload")
machine_type = input('The machine type to use for default node pool [n1-standard-1]: ')
if not machine_type:
    machine_type = 'n1-standard-1'

default_pool_template = \
"""
# Default pool for kubernetes system pods and miscellaneous services
resource "google_container_node_pool" "default" {{
  name    = "default"
  zone    = "${{var.zone}}"
  cluster = "${{var.cluster_name}}"
    
  management {{
    auto_update = true
  }}
  autoscaling {{
    min_node_count   = 0
    max_node_count   = 100
  }}
  initial_node_count = 3
  node_config {{
    machine_type = "{0}"
    labels {{
      machine-type = "{0}"
    }}
  }}
}}
""".format(machine_type)
all_templates.append(default_pool_template)

print("")
print("Now we will start creating machines dedicated for computation tasks")
print("They will be tainted so only designated workload will be scheduled on them")

nodes = [{'machine_type': 'n1-standard-8', 'gpu': None, 'gpu-count': None}, 
            {'machine_type': 'n1-standard-8', 'gpu': 'k80', 'gpu-count': 1}
            ]

# def add_pool():

# def remove_pool(n):
#     print('Removing...')

# def describe():
#     print('\tMachine Type\tGPU Type\tGPU Count')
#     for i in range(len(node_types)):
#         spec = nodes[i]
#         print('{}\t{}\t{}').format(spec['machine_type'], node_types[])

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


print('\n'.join(all_templates))
# while True:




ouptut = '\n'.join(all_templates)
