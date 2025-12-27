import mysql.connector
import os
import sys

# Adjust the path to include the project's root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.db_config import db_config

def setup_database():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    cursor.execute("CREATE DATABASE IF NOT EXISTS auth_db;")
    cursor.execute("USE auth_db;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL  
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_database()
