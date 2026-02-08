# Single Responsibility Principle (SRP) - Documentation

## Principle Overview
The Single Responsibility Principle states that a class should have only one reason to change. Each class should have a single, well-defined responsibility.

## Problem Identified
The original `AuthManager` class violated SRP by having **two distinct responsibilities**:

1. **Authentication Logic**: Validating user credentials, managing sessions
2. **Data Persistence**: Reading and writing user data to JSON files

This meant the class had two reasons to change:
- Changes to authentication logic (e.g., adding multi-factor authentication)
- Changes to storage mechanism (e.g., switching from JSON to database)

## Solution Implemented

### Created: `user_repository.py`
Extracted all data persistence operations into a dedicated `UserRepository` class:

**Responsibilities:**
- Loading users from storage
- Saving users to storage
- Retrieving individual user data
- Updating user information (e.g., last login timestamp)

**Key Methods:**
- `load_users()` - Load all users from JSON file
- `save_users(users)` - Save users to JSON file
- `get_user(username)` - Retrieve specific user data
- `update_last_login(username)` - Update user's last login timestamp

### Modified: `app.py` - `AuthManager` class
Refactored `AuthManager` to focus solely on authentication:

**Single Responsibility:**
- User authentication and session management only

**Changes Made:**
1. Removed `_ensure_users_file()` method (moved to `UserRepository`)
2. Removed direct file I/O operations
3. Injected `UserRepository` as a dependency via constructor
4. Delegates all data operations to the repository

**Before:**
```python
class AuthManager:
    def __init__(self, users_file: str = "data/users.json"):
        self.users_file = Path(users_file)
        self._ensure_users_file()  # File I/O responsibility
    
    def authenticate(self, username: str, password: str) -> bool:
        with open(self.users_file, 'r') as f:  # Direct file access
            users = json.load(f)
        # ... authentication logic
        with open(self.users_file, 'w') as f:  # Direct file access
            json.dump(users, f, indent=2)
```

**After:**
```python
class AuthManager(IAuthenticator):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository  # Dependency injection
    
    def authenticate(self, username: str, password: str) -> bool:
        user_data = self.user_repository.get_user(username)  # Delegate to repository
        # ... authentication logic only
        self.user_repository.update_last_login(username)  # Delegate to repository
```

## Benefits

1. **Separation of Concerns**: Authentication logic is separate from data storage
2. **Easier Testing**: Can mock `UserRepository` to test authentication logic in isolation
3. **Flexibility**: Can change storage mechanism (e.g., to database) without touching authentication code
4. **Maintainability**: Each class has a clear, focused purpose
5. **Reusability**: `UserRepository` can be reused by other components that need user data

## Files Modified
- ✅ Created: `user_repository.py` (new file)
- ✅ Modified: `app.py` (lines 76-162)
  - Removed file I/O from `AuthManager`
  - Added dependency injection of `UserRepository`
  - Updated `main()` to instantiate and inject `UserRepository`
