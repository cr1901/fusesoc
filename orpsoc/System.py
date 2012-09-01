import sys
if sys.version[0] == '2':
    import ConfigParser as configparser
else:
    import configparser

from orpsoc import Core
from orpsoc.Config import Config
from orpsoc import ProviderLocal
import os

class System:
    def __init__(self, system_file):
        system_root = os.path.dirname(system_file)

        system_config = configparser.SafeConfigParser(allow_no_value=True)
        system_config.readfp(open(system_file))

        self.name = system_config.get('main', 'name')

        self.cores = {}
        self.cores['orpsoc'] = self._create_orpsoc_core(system_config, system_root)
        
        
        cores = self._get_files(system_config, 'cores')

        for core in cores:
            self.cores[core] = Core.Core(os.path.join(Config().cores_root,core,core+'.core'))

        self.simulators = system_config.get('main','simulators').split('\n')

    def setup_cores(self):
        for core in self.cores:
            self.cores[core].setup()
    def _create_orpsoc_core(self, system_config, system_root):
        core = Core.Core()
        
        core.set_rtl_files(self._get_files(system_config, 'rtl_files'))
        core.set_include_dirs(self._get_files(system_config, 'include_dirs'))
        core.set_include_files(self._get_files(system_config, 'include_files'))
        core.set_tb_files(self._get_files(system_config, 'tb_files'))

        core.provider = ProviderLocal.ProviderLocal()
        core.set_root(os.path.join(system_root))
        return core
        
    def _get_files(self, config, identifier):
        files = config.get('main', identifier).split()
        if '' in files:
            files.remove('')
        return files

    def get_cores(self):
        return self.cores

    def get_rtl_files(self):
        return self.rtl_files
            #FIXME: Iterate through core RTL files and append to rtl_files
    def get_tb_files(self):
        return self.tb_files
