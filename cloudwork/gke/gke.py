from os.path import expanduser
from pathlib import Path
from .templates import *

class GoogleCloudKubernetesNodePool:
    def __init__(self, *, 
                 name,
                 machine_type,
                 initial_node_count=0,
                 min_count=0,
                 max_count=100,
                 use_accelerator=False,
                 accelerator_type='nvidia-tesla-k80',
                 accelerator_count=1,
                 use_taint=True,
                 taint_name='exclusive_workload',
                 taint_value='true',#TODO
                 taint_effect='NoExcecute'
                 ):
        self.name = name
        self.machine_type = machine_type
        # autoscaling
        self.initial_node_count = initial_node_count
        self.min_count = min_count
        self.max_count = max_count
        # accelerator
        self.use_accelerator = use_accelerator
        self.accelerator_type = accelerator_type
        self.accelerator_count = accelerator_count
        # taint
        self.use_taint = use_taint
        self.taint_key = taint_key
        self.taint_value = taint_value
        self.taint_effect = taint_effect

    def _accelerator_temp(self):
        if self.use_accelerator:
            return ACCELERATOR_TEMPLATE.format(accelerator_type=self.accelerator_type,
                                               accelerator_count=self.accelerator_count)
        else:
            return ''

    def _taint_temp(self):
        if self.use_taint:
            return SINGLE_TAINT_TEMPLATE.format(taint_key=self.taint_key,
                                                taint_value=self.taint_value,
                                                taint_effect=self.taint_effect)
        else:
            return ''

    def _nodepool_temp(self):
        return NODE_POOL_TEMPLATE_AUTOSCALING \
                .format(name=self.name,
                        min_count=self.min_count,
                        max_count=self.max_count,
                        initial_node_count=self.initial_node_count,
                        machine_type=self.machine_type,
                        taint=self._taint_temp(),
                        accelerator=self._accelerator_temp())


class GoogleCloudKubernetesLauncher:
    def __init__(self, *,
                 project,
                 credential_file,
                 zone,
                 cluster_name,
                 min_master_version='1.9'):
        self.project = str(project)
        if not Path(str(credential_file)).exists:
            raise ValueError('Credential file {} not found'.format(credential_file))
        self.credential_file = credential_file
        self.zone = str(zone)
        self.cluster_name = str(cluster_name)
        self.min_master_version = str(min_master_version)

        self.node_pools = {}

    def add_node_pool(self, node_pool):
        if not isinstance(node_pool, GoogleCloudKubernetesLauncher):
            raise TypeError('node_pool should be of type GoogleCloudKubernetesLauncher'\
                            'Got {} instead'.format(type(node_pool)))
        self.node_pools[node_pool.name] = node_pool

    def _variables_temp(self):
        return VARIABLES_TEMPLATE.format(project=self.project,
                                         zone=self.zone,
                                         credential_file=self.credential_file,
                                         cluster_name=self.cluster_name)

    def _header_temp(self):
        return HEADER_TEMPLATE.format(min_master_version=self.min_master_version)
