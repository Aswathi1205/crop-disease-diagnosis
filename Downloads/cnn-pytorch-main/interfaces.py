"""
Abstract Interfaces for Dependency Inversion Principle (DIP)

This module defines abstract base classes that high-level modules depend on,
following the Dependency Inversion Principle.
"""

from abc import ABC, abstractmethod
from typing import Optional
from PIL import Image


class IAuthenticator(ABC):
    """Abstract interface for authentication operations"""
    
    @abstractmethod
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate user credentials.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            True if authentication successful, False otherwise
        """
        pass
    
    @abstractmethod
    def create_session(self, username: str):
        """
        Create a new session for authenticated user.
        
        Args:
            username: Username to create session for
        """
        pass
    
    @abstractmethod
    def logout(self):
        """Invalidate current session"""
        pass


class IPredictor(ABC):
    """Abstract interface for prediction operations"""
    
    @abstractmethod
    def load_model(self) -> bool:
        """
        Load the prediction model.
        
        Returns:
            True if model loaded successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def predict(self, image: Image.Image) -> Optional[object]:
        """
        Make prediction on input image.
        
        Args:
            image: PIL Image to predict on
            
        Returns:
            Prediction result or None if prediction failed
        """
        pass
