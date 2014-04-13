from abc import ABCMeta, abstractstaticmethod
from configparser import ConfigParser
import os

CONFIGURATION_FILE_NAME = 'configuration.cfg'

class ConfigurationFactory:
    configuration_class = None
    
    @staticmethod
    def get_configuration():
        # To minimize disk I/O, the configuration class is only 
        # converted from the class name stored in the configuration 
        # file on disk once.
        if not ConfigurationFactory.configuration_class:
            ConfigurationFactory.configuration_class = ConfigurationFactory._get_configuration_class_from_file()
            
        return ConfigurationFactory.configuration_class
    
    @staticmethod
    def _get_configuration_class_from_file():
        configuration = ConfigParser()
        configuration.read(CONFIGURATION_FILE_NAME)
        
        module_name = 'configuration'
        class_name = configuration['Configuration']['class_name']
        
        # Get the Configuration class based on the module name and 
        # class name read from the disk.
        module = __import__(module_name)
        return getattr(module, class_name)


class Configuration:
    __metaclass__ = ABCMeta
    
    @abstractstaticmethod
    def get_database_type():
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_hostname():
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_port():
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_username():
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_password():
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_name():
        return NotImplemented


class EnvironmentalVariableConfiguration(Configuration):
    @staticmethod
    def get_database_type():
        return os.environ['DATABASETYPE']
    
    @staticmethod
    def get_database_hostname():
        return os.environ['DATABASEHOSTNAME']
    
    @staticmethod
    def get_database_port():
        return os.environ['DATABASEPORT']
    
    @staticmethod
    def get_database_username():
        return os.environ['DATABASEUSERNAME']
    
    @staticmethod
    def get_database_password():
        return os.environ['DATABASEPASSWORD']
    
    @staticmethod
    def get_database_name():
        return os.environ['DATABASENAME']

