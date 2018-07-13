import json
# import symphony

_REQUIRED_LABELS = ["name", "cpu", "memory_m"]

class GKESymphonyMachineDispatcher:
    def __init__(self, tf_json):
        """
        json is a dict or a str(in which case it is treated as a json file)
        """
        if not isinstance(tf_json, dict):
            with open(str(tf_json), 'r') as f:
                tf_json = json.load(f)
        self.tf_config = tf_json
        if "resource" not in self.tf_config or \
           "google_container_node_pool" not in self.tf_config["resource"]:
            raise KeyError("resource/google_container_node_pool is required in the json")
        self.node_pools = self.tf_config["resource"]["google_container_node_pool"]
        for k, v in self.node_pools.items():
            self._check_required_labels(k, v)

    def get_nodepools(self):
        return sorted(self.node_pools.keys())

    def get_nodepool(self, name):
        if not name in self.node_pools:
            raise KeyError("Cannot find node pool {}, available:\n"\
                  .format(node_pool_name, ',\n'.join(self.get_nodepools())))
        return self.node_pools[name]

    def assign_to_nodepool(self, process, node_pool_name, exclusive=True):
        """
        exclusive: When true, claim all available resoruces on this node
        """
        if not node_pool_name in self.get_nodepools:
            raise KeyError("Cannot find node pool {}".format(node_pool_name))
        node_pool_di = self.node_pools[node_pool_name]

        np_labels = node_pool_di["node_config"]["labels"]
        name = np_labels["name"]
        cpu = np_labels["cpu"]
        memory_m = np_labels["memory_m"]

        # This selector selects the only nodepool
        process.node_selector("name", name)
        # Tolerations allow the process to be scheduled
        if "taint" in node_pool_di:
            for taint in node_pool_di["taint"]:
                process.add_toleration(**taint)
        if "gpu_type" in np_labels:
            process.add_toleration({
                "effect": "NO_SCHEDULE",
                "key": "nvidia.com/gpu",
                "value": "present"
                })

        if exclusive:
            memory_str = '{}Mi'.format(int(memory_m * 0.8))
            process.resource_request(cpu=cpu - 1, memory=memory_str)
            if "gpu_count" in np_labels:
                process.resource_limit(np_labels["gpu_count"])

        return process

    def _check_required_labels(self, name, di):
        if "node_config" not in di:
            msg = "Missing field 'node_config' in nodepool declaration. "\
                  + "Is this json generated by cloudwise?"
            raise ValueError(msg)
        if "labels" not in di["node_config"]:
            msg = "Missing field 'node_config/labels' in nodepool declaration. "\
                  + "Is this json generated by cloudwise?"
            raise ValueError(msg)
        labels_di = di["node_config"]["labels"]
        for label in _REQUIRED_LABELS:
            if label not in labels_di:
                msg = "Missing field {} in nodepool labels. ".format(label)\
                      + "Is this json generated by cloudwise?"
                raise ValueError(msg)

    def __repr__(self):
        return "<SymphonyMachineDispatcher> instance, available nodepools:\n"\
                + ',\n'.join(self.get_nodepools())