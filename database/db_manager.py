"""
Database Manager module for handling all database operations.
"""

import mysql.connector
import bcrypt
from typing import Dict, List, Optional, Tuple, Union
import re


class DatabaseManager:
    """Manager class for database operations including connection and CRUD operations."""
    
    def __init__(self):
        """Initialize database manager with empty connection."""
        self.connection = None
        self.cursor = None
        self.db_name = None
    
    def connect_to_mysql(self, host: str, user: str, password: str) -> bool:
        """Connect to MySQL server with the provided credentials.
        
        Args:
            host: MySQL server host
            user: MySQL username
            password: MySQL password
            
        Returns:
            bool: True if connection was successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            return True
        except mysql.connector.Error as err:
            return False, str(err)
    
    def get_all_databases(self) -> List[str]:
        """Get a list of all databases on the MySQL server.
        
        Returns:
            List[str]: List of database names
        """
        try:
            self.cursor.execute("SHOW DATABASES")
            # Extract database names from results, excluding system databases
            databases = [db[0] for db in self.cursor if db[0] not in ['information_schema', 'mysql', 'performance_schema', 'sys']]
            return databases
        except mysql.connector.Error:
            return []
    
    def select_database(self, db_name: str) -> bool:
        """Select an existing database.
        
        Args:
            db_name: Database name to select
            
        Returns:
            bool: True if database was selected, False otherwise
        """
        try:
            self.db_name = db_name
            self.cursor.execute(f"USE {self.db_name}")
            return True
        except mysql.connector.Error:
            return False
    
    def create_database(self, db_name: str) -> bool:
        """Create a new database.
        
        Args:
            db_name: Database name to create
            
        Returns:
            bool: True if database was created, False otherwise
        """
        try:
            # Sanitize database name (remove special characters)
            self.db_name = re.sub(r'[^\w]', '', db_name)
            
            # Create database
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            self.cursor.execute(f"USE {self.db_name}")
            return True
        except mysql.connector.Error:
            return False
    
    def create_tables(self) -> bool:
        """Create User and Login tables if they don't exist.
        
        Returns:
            bool: True if tables were created, False otherwise
        """
        try:
            # Create User table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS User (
                userId INT AUTO_INCREMENT PRIMARY KEY,
                firstName VARCHAR(50) NOT NULL,
                lastName VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                accessLevel ENUM('basic', 'admin') DEFAULT 'basic'
            )
            """)
            
            # Create Login table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Login (
                loginId INT AUTO_INCREMENT PRIMARY KEY,
                userId INT UNIQUE,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                FOREIGN KEY (userId) REFERENCES User(userId) ON DELETE CASCADE
            )
            """)
            
            return True
        except mysql.connector.Error:
            return False
    
    def insert_user(self, first_name: str, last_name: str, email: str, access_level: str) -> Optional[int]:
        """Insert a new user and return the user ID.
        
        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            access_level: User's access level ('basic' or 'admin')
            
        Returns:
            int: User ID if insertion was successful, None otherwise
        """
        try:
            query = """
            INSERT INTO User (firstName, lastName, email, accessLevel)
            VALUES (%s, %s, %s, %s)
            """
            values = (first_name, last_name, email, access_level)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            user_id = self.cursor.lastrowid
            return user_id
        except mysql.connector.Error:
            return None
    
    def insert_login(self, user_id: int, username: str, password: str) -> bool:
        """Insert login credentials with encrypted password.
        
        Args:
            user_id: Associated user ID
            username: Login username
            password: Password (will be encrypted)
            
        Returns:
            bool: True if insertion was successful, False otherwise
        """
        try:
            # Hash the password
            hashed_password = self._encrypt_password(password)
            
            query = """
            INSERT INTO Login (userId, username, password)
            VALUES (%s, %s, %s)
            """
            values = (user_id, username, hashed_password)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            return True
        except mysql.connector.Error:
            return False
    
    def _encrypt_password(self, password: str) -> str:
        """Encrypt password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            str: Encrypted password
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')
    
    def verify_password(self, entered_password: str, stored_password: str) -> bool:
        """Verify password against stored hash.
        
        Args:
            entered_password: Password to verify
            stored_password: Stored hashed password
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))
    
    def select_all_users(self) -> List[Dict]:
        """Retrieve all users from the User table.
        
        Returns:
            List[Dict]: List of user dictionaries
        """
        try:
            self.cursor.execute("SELECT userId, firstName, lastName, email, accessLevel FROM User")
            users = []
            for (user_id, first_name, last_name, email, access_level) in self.cursor:
                users.append({
                    'userId': user_id,
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                    'accessLevel': access_level
                })
            return users
        except mysql.connector.Error:
            return []
    
    def select_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Retrieve a specific user by ID.
        
        Args:
            user_id: User ID to search for
            
        Returns:
            Dict: User information if found, None otherwise
        """
        try:
            query = "SELECT userId, firstName, lastName, email, accessLevel FROM User WHERE userId = %s"
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            
            if result:
                user_id, first_name, last_name, email, access_level = result
                return {
                    'userId': user_id,
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                    'accessLevel': access_level
                }
            else:
                return None
        except mysql.connector.Error:
            return None
    
    def select_login_by_username(self, username: str) -> Optional[Dict]:
        """Retrieve login information by username.
        
        Args:
            username: Username to search for
            
        Returns:
            Dict: Login and user information if found, None otherwise
        """
        try:
            query = """
            SELECT l.loginId, l.userId, l.username, l.password, u.firstName, u.lastName, u.email, u.accessLevel
            FROM Login l
            JOIN User u ON l.userId = u.userId
            WHERE l.username = %s
            """
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            
            if result:
                login_id, user_id, username, password, first_name, last_name, email, access_level = result
                return {
                    'loginId': login_id,
                    'userId': user_id,
                    'username': username,
                    'password': password,
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                    'accessLevel': access_level
                }
            else:
                return None
        except mysql.connector.Error:
            return None
    
    def update_user(self, user_id: int, first_name: str = None, last_name: str = None, 
                    email: str = None, access_level: str = None) -> bool:
        """Update user information.
        
        Args:
            user_id: User ID to update
            first_name: New first name or None to keep current
            last_name: New last name or None to keep current
            email: New email or None to keep current
            access_level: New access level or None to keep current
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            # Get current user data
            current_user = self.select_user_by_id(user_id)
            if not current_user:
                return False
            
            # Update with new values or keep current ones
            first_name = first_name if first_name is not None else current_user['firstName']
            last_name = last_name if last_name is not None else current_user['lastName']
            email = email if email is not None else current_user['email']
            access_level = access_level if access_level is not None else current_user['accessLevel']
            
            query = """
            UPDATE User 
            SET firstName = %s, lastName = %s, email = %s, accessLevel = %s
            WHERE userId = %s
            """
            values = (first_name, last_name, email, access_level, user_id)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            return self.cursor.rowcount > 0
        except mysql.connector.Error:
            return False
    
    def update_login(self, user_id: int, username: str = None, password: str = None) -> bool:
        """Update login information.
        
        Args:
            user_id: User ID to update login for
            username: New username or None to keep current
            password: New password or None to keep current
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            # Build the query dynamically based on what's being updated
            query_parts = []
            values = []
            
            if username is not None:
                query_parts.append("username = %s")
                values.append(username)
            
            if password is not None:
                query_parts.append("password = %s")
                hashed_password = self._encrypt_password(password)
                values.append(hashed_password)
            
            if not query_parts:
                return False
            
            # Complete the query
            query = f"UPDATE Login SET {', '.join(query_parts)} WHERE userId = %s"
            values.append(user_id)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            return self.cursor.rowcount > 0
        except mysql.connector.Error:
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user (will cascade delete their login due to constraints).
        
        Args:
            user_id: User ID to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            query = "DELETE FROM User WHERE userId = %s"
            self.cursor.execute(query, (user_id,))
            self.connection.commit()
            
            return self.cursor.rowcount > 0
        except mysql.connector.Error:
            return False
    
    def delete_login(self, login_id: int) -> bool:
        """Delete a login record by login ID.
        
        Args:
            login_id: Login ID to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            query = "DELETE FROM Login WHERE loginId = %s"
            self.cursor.execute(query, (login_id,))
            self.connection.commit()
            
            return self.cursor.rowcount > 0
        except mysql.connector.Error:
            return False
    
    def close_connection(self):
        """Close database connection."""
        if self.connection:
            if self.cursor:
                self.cursor.close()
            self.connection.close()