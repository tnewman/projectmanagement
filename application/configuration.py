''' database contains classes to provide interaction with 
	external configuration variables.'''

from abc import ABCMeta, abstractstaticmethod
from configparser import ConfigParser
import os

#: The file name of the configuration file used to inject the configuration 
#: class.
CONFIGURATION_FILE_NAME = 'configuration.cfg'

class ConfigurationFactory:
    ''' The ConfigurationFactory provides a consistent interface 
        to access any implemented configuration that inherits from 
        the :class:`Configuration` class.'''
    configuration_class = None
    
    @staticmethod
    def get_configuration():
        ''' Creates an instance of the configuration based on a configuration 
            class that is loaded based on the class name stored on the disk.
            
            Returns:
                A :class:`Configuration` object used to access external 
                configuration variables.'''
        
        # To minimize disk I/O, the configuration class is only 
        # converted from the class name stored in the configuration 
        # file on disk once.
        if not ConfigurationFactory.configuration_class:
            ConfigurationFactory.configuration_class = ConfigurationFactory._get_configuration_class_from_file()
            
        return ConfigurationFactory.configuration_class
    
    @staticmethod
    def _get_configuration_class_from_file():
        ''' Loads the configuration class name from the disk and converts 
            it to the associated configuration class.
        
            Returns:
                A :class:`Configuration` class used to load 
                configuration.'''
        
        configuration = ConfigParser()
        configuration.read(CONFIGURATION_FILE_NAME)
        
        module_name = 'configuration'
        class_name = configuration['Configuration']['class_name']
        
        # Get the Configuration class based on the module name and 
        # class name read from the disk.
        module = __import__(module_name)
        return getattr(module, class_name)


class Configuration:
    ''' Abstract base class specifying the interfaces that all 
    configuration classes are to provide to allow consistent configuration 
    access, regardless of the underlying configuration storage method.
    
    This class should never be used directly because none of the methods 
    are implemented.'''
    
    __metaclass__ = ABCMeta
    
    @abstractstaticmethod
    def get_database_type():
        ''' Gets the name of the database from the configuration. 
        
            Returns:
                (str): The type of database.'''
        
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_hostname():
        ''' Gets the hostname of the database from the configuration.
        
            Returns:
                (str): The type of database.'''
        
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_port():
        ''' Gets the port to access the database from the configuration.
        
            Returns:
                (str): The type of database.'''
        
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_username():
        ''' Gets the username to access the database from the 
            configuration.
        
            Returns:
                (str): The type of database.'''
        
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_password():
        ''' Gets the password to access the database from the 
            configuration.
        
            Returns:
                (str): The type of database.'''
        
        return NotImplemented
    
    @abstractstaticmethod
    def get_database_name():
        ''' Gets the database name to access the database from the 
            configuration.
        
            Returns:
                (str): The type of database.'''
        
        return NotImplemented


class EnvironmentalVariableConfiguration(Configuration):
    ''' Provides a configuration implementation that uses environmental 
        variables.'''
    
    @staticmethod
    def get_database_type():
        ''' Gets the name of the database from an environmental variable. 
        
            Returns:
                (str): The type of database.'''
        
        return os.environ['DATABASETYPE']
    
    @staticmethod
    def get_database_hostname():
        ''' Gets the hostname of the database from an environmental 
            variable. 
        
            Returns:
                (str): The type of database.'''
        
        return os.environ['DATABASEHOSTNAME']
    
    @staticmethod
    def get_database_port():
        ''' Gets the port to access the database from an environmental 
            variable. 
        
            Returns:
                (str): The type of database.'''
        
        return os.environ['DATABASEPORT']
    
    @staticmethod
    def get_database_username():
        ''' Gets the username to access the database from an environmental 
            variable. 
        
            Returns:
                (str): The type of database.'''
        
        return os.environ['DATABASEUSERNAME']
    
    @staticmethod
    def get_database_password():
        ''' Gets the password to access the database from an environmental 
            variable. 
        
            Returns:
                (str): The type of database.'''
        
        return os.environ['DATABASEPASSWORD']
    
    @staticmethod
    def get_database_name():
        ''' Gets the database name to access the database from an 
            environmental variable. 
        
            Returns:
                (str): The type of database.'''
        
        return os.environ['DATABASENAME']

