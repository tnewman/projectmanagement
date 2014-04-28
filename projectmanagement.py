# File: database.py
# Description: Runs the Project Management Application development server.
# Date: 2014/04/27
# Programmer: Thomas Newman

import configparser
import os
import sys

''' Runs the Project Management Application development server. '''

def load_config_file():
    ''' Attempts to load the environmental variables from a configuration 
        file. If the configuration file does not exist, the existing 
        environmental variables are left in-tact. '''
    
    config = configparser.ConfigParser()
    
    if not config.read('configuration.cfg'):
        return
    
    os.environ['SECRET_KEY'] = config['Configuration']['SECRET_KEY']
    os.environ['DATABASE_URL'] = config['Configuration']['DATABASE_URL']
    os.environ['DEBUG'] = config['Configuration']['DEBUG']
    

if __name__ == '__main__':
    load_config_file()
    
    from application.projectmanagement import app, initialize_database
    
    if len(sys.argv) == 1:
        # No command line arguments. Run the server.
        app.run()
        sys.exit(0)
    elif len(sys.argv) == 4:
        if sys.argv[1] == '-initializedatabase':
            # Initialize the database.
            username = sys.argv[2]
            password = sys.argv[3]
            
            initialize_database(username, password)
            sys.exit(0)
    
    print('projectmanagement.py')
    print('Run Server: projectmanagement.py')
    print('Initialize Database: projectmanagement.py -initializedatabase username password')
    sys.exit(1)