import cloudwise.utils as U


_GPU_NAME_MAP = {
    'nvidia-tesla-k80': 'k80',
    'nvidia-tesla-p100': 'p100',
    'nvidia-tesla-v100': 'v100',
}


def _get_machine_summary(cpu, memory_m, gpu_type, gpu_count, preemptible):
    arr = ['np', str(cpu) + 'cpu', str(memory_m) + 'mem']
    if gpu_type is not None:
        arr.append("{}{}".format(gpu_count, _GPU_NAME_MAP[gpu_type]))
    if preemptible:
        arr.append("pr")
    else:
        arr.append("np")
    return "-".join(arr)


def _infer_cpu_memory(machine_type):
    if machine_type.find("n1-standard-") == 0:
        cpu = int(machine_type[len("n1-standard-"):])
        memory = 3.75 * cpu
        return cpu, memory
    elif machine_type.find("n1-highmem-") == 0:
        cpu = int(machine_type[len("n1-highmem-"):])
        memory = 6.5 * cpu
        return cpu, memory
    elif machine_type.find("n1-highcpu-") == 0:
        cpu = int(machine_type[len("n1-highcpu-"):])
        memory = 1.8 * cpu
        return cpu, memory
    else:
        raise ValueError("Unknown machine type {}".format(machine_type))


def _create_node_config(cpu,
                        memory_g,
                        machine_type,
                        gpu_type,
                        gpu_count,
                        preemptible,
                        disk_size_gb,
                        labels,
                        taints,
                        exclusive_workload,
                        name=None,
                        ):

    if cpu is not None and memory_g is not None:
        if machine_type is not None:
            raise ValueError("Either provide cpu and memory or provide machine_type")
        machine_type = "custom-{}-{}".format(int(cpu), int(memory_g * 1024))
    else:
        cpu, memory_g = _infer_cpu_memory(machine_type)
    memory_m = int(1024 * memory_g)
    config = {
        "machine_type": machine_type,
        "preemptible": preemptible,
        "disk_size_gb": disk_size_gb,
        "oauth_scopes": [
            "https://www.googleapis.com/auth/compute",
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/logging.write",
            "https://www.googleapis.com/auth/monitoring",
        ],
    }
    all_labels = {
        "machine_summary": _get_machine_summary(cpu, memory_m, gpu_type, gpu_count, preemptible),
        "machine_type": machine_type,
        "preemptible": preemptible,
        "cpu": cpu,
        "memory_m": memory_m,
    }
    if name is None:
        name = all_labels["machine_summary"]
    all_labels["name"] = name
    all_taints = []
    config["labels"] = all_labels
    config["taint"] = all_taints

    if gpu_type is not None:
        config["guest_accelerator"] = [{
            "type": gpu_type,
            "count": gpu_count,
        }]
        all_labels["gpu_type"] = gpu_type
        all_labels["gpu_count"] = gpu_count

    if labels is not None:
        U.merge_dict(all_labels, labels)

    # Do not create taints for GPU based node pool to avoid blocking google cloud default
    # driver installer daemonset
    if exclusive_workload:
        if gpu_type is None:
            all_taints.append({
                "key": "exclusive_workload",
                "value": "exclusive",
                "effect": "NO_EXECUTE",
            })
    if preemptible:
        if gpu_type is None:
            all_taints.append({
                "key": "preemptible",
                "value": "yes",
                "effect": "NO_EXECUTE",
            })

    if taints is not None:
        for taint in taints:
            all_taints.append(taint)

    return config


def _nodepool(*,
              name=None,
              use_autoscaling=True,
              initial_node_count=None,
              min_node_count=0,
              max_node_count=100,
              cpu=None,
              memory_g=None,
              machine_type=None,
              gpu_type=None,
              gpu_count=0,
              preemptible=False,
              disk_size_gb=100,
              labels=None,
              taints=None,
              exclusive_workload=None):

    node_config = _create_node_config(cpu,
                                      memory_g,
                                      machine_type,
                                      gpu_type,
                                      gpu_count,
                                      preemptible,
                                      disk_size_gb,
                                      labels,
                                      taints,
                                      exclusive_workload,
                                      name=name)
    if name is None:
        name = node_config["labels"]["machine_summary"]
    config = {
        "name": name,
        "cluster": "${var.cluster_name}",
        "management": {
            "auto_repair": True,
            "auto_upgrade": True,
        },
        "node_config": node_config,
        "lifecycle": {
            "ignore_changes": ["node_config.0.taint"],
        }
    }
    if initial_node_count is not None:
        config["initial_node_count"] = initial_node_count

    if use_autoscaling:
        config["autoscaling"] = {
            "min_node_count": min_node_count,
            "max_node_count": max_node_count,
        }
    return config


class GKELauncher:
    def __init__(self,
                 project,
                 zone,
                 cluster_name,
                 credential_file=None):
        self.config = {
            "variable": {
                "cluster_name": {
                    "default": cluster_name,
                }
            },
            "provider": {
                "google": {
                    "project": project,
                    "zone": zone,
                }
            },
            "resource": {
                "google_container_cluster": {
                    cluster_name: {
                        "name": "${var.cluster_name}",
                        "initial_node_count": 1,
                        "remove_default_node_pool": True,
                    },
                },
                "google_container_node_pool": {},
            },
        }
        if credential_file is not None:
            self.config["provider"]["google"]["credentials"] = "${{file(\"{}\")}}".format(credential_file)
        self.node_pools = self.config["resource"]["google_container_node_pool"]

    def add_nodepool(self, **kwargs):
        config = _nodepool(**kwargs)
        if config["name"] in self.node_pools:
            raise ValueError('Nodepool with name {} has already been created'.format(config["name"]))
        self.node_pools[config["name"]] = config
