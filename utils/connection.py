# Module Imports
import mariadb
import sys
import os
from dotenv import load_dotenv

load_dotenv()


def connection():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            database=os.getenv('DB_NAME')
        )

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Return connection
    return conn
