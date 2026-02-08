"""
User Repository for Single Responsibility Principle (SRP)

This module handles all user data persistence operations,
separating data access from business logic.
"""

import json
import bcrypt
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class UserRepository:
    """Handles user data storage and retrieval operations"""
    
    def __init__(self, users_file: str = "data/users.json"):
        """
        Initialize user repository.
        
        Args:
            users_file: Path to users JSON file
        """
        self.users_file = Path(users_file)
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file with demo user if it doesn't exist"""
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.users_file.exists():
            # Create demo user: username=admin, password=admin123
            demo_password = "admin123"
            password_hash = bcrypt.hashpw(demo_password.encode('utf-8'), bcrypt.gensalt())
            
            users = {
                "admin": {
                    "username": "admin",
                    "password_hash": password_hash.decode('utf-8'),
                    "created_at": datetime.now().isoformat(),
                    "last_login": datetime.now().isoformat()
                }
            }
            
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
    
    def load_users(self) -> Dict:
        """
        Load all users from storage.
        
        Returns:
            Dictionary of user data
        """
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise IOError(f"Failed to load users: {str(e)}")
    
    def save_users(self, users: Dict):
        """
        Save users to storage.
        
        Args:
            users: Dictionary of user data to save
        """
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            raise IOError(f"Failed to save users: {str(e)}")
    
    def get_user(self, username: str) -> Optional[Dict]:
        """
        Get user data by username.
        
        Args:
            username: Username to retrieve
            
        Returns:
            User data dictionary or None if not found
        """
        users = self.load_users()
        return users.get(username)
    
    def update_last_login(self, username: str):
        """
        Update user's last login timestamp.
        
        Args:
            username: Username to update
        """
        users = self.load_users()
        if username in users:
            users[username]['last_login'] = datetime.now().isoformat()
            self.save_users(users)
    
    def create_user(self, username: str, password: str) -> tuple[bool, str]:
        """
        Create a new user account.
        
        Args:
            username: Desired username
            password: User's password (will be hashed)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate inputs
        if not username or not password:
            return False, "Username and password are required"
        
        if len(username.strip()) == 0:
            return False, "Username cannot be empty"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        # Check if username already exists
        users = self.load_users()
        if username in users:
            return False, "Username already exists"
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user record
        users[username] = {
            "username": username,
            "password_hash": password_hash.decode('utf-8'),
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }
        
        # Save to file
        try:
            self.save_users(users)
            return True, "Account created successfully!"
        except Exception as e:
            return False, f"Failed to create account: {str(e)}"
