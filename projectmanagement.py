import os
import sys
from application.projectmanagement import app, initialize_database

if __name__ == '__main__':
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