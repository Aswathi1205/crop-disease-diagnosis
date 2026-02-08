# Dependency Inversion Principle (DIP) - Documentation

## Principle Overview
The Dependency Inversion Principle states that:
1. **High-level modules should not depend on low-level modules**. Both should depend on abstractions.
2. **Abstractions should not depend on details**. Details should depend on abstractions.

## Problem Identified
The original code violated DIP by having **tight coupling** between high-level and low-level modules:

1. **UI functions** (`render_sidebar`, `render_login_page`, `render_upload_page`) depended directly on **concrete classes** (`AuthManager`, `InferenceEngine`)
2. **No abstractions**: High-level modules were tightly coupled to implementation details
3. **Hard to test**: Cannot easily mock dependencies for testing
4. **Inflexible**: Changing implementations requires modifying high-level code

**Original Code:**
```python
def render_login_page(auth_manager: AuthManager):  # Depends on concrete class
    # ...
    if auth_manager.authenticate(username, password):
        # ...

def main():
    auth_manager = AuthManager()  # Direct instantiation
    inference_engine = InferenceEngine()  # Direct instantiation
    render_login_page(auth_manager)  # Passes concrete instance
```

## Solution Implemented

### Created: `interfaces.py`
Introduced abstract interfaces that define contracts:

**`IAuthenticator` Interface:**
- Abstract methods: `authenticate()`, `create_session()`, `logout()`
- Defines the contract for authentication operations
- High-level modules depend on this abstraction

**`IPredictor` Interface:**
- Abstract methods: `load_model()`, `predict()`
- Defines the contract for prediction operations
- High-level modules depend on this abstraction

### Modified: `app.py`
Applied dependency inversion throughout the application:

#### 1. Concrete Classes Implement Interfaces

**`AuthManager` implements `IAuthenticator`:**
```python
class AuthManager(IAuthenticator):  # Implements interface
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def authenticate(self, username: str, password: str) -> bool:
        # Implementation
    
    def create_session(self, username: str):
        # Implementation
    
    def logout(self):
        # Implementation
```

**`InferenceEngine` implements `IPredictor`:**
```python
class InferenceEngine(IPredictor):  # Implements interface
    def __init__(self, config_loader: ConfigLoader, ...):
        self.config_loader = config_loader
    
    def load_model(self) -> bool:
        # Implementation
    
    def predict(self, image: Image.Image) -> Optional[DiagnosisResult]:
        # Implementation
```

#### 2. High-Level Modules Depend on Abstractions

**UI Functions Updated:**
```python
# Before: Depended on concrete classes
def render_sidebar(auth_manager: AuthManager):
def render_login_page(auth_manager: AuthManager):
def render_upload_page(inference_engine: InferenceEngine):

# After: Depend on abstractions
def render_sidebar(auth_manager: IAuthenticator):  # Depends on interface
def render_login_page(auth_manager: IAuthenticator):  # Depends on interface
def render_upload_page(inference_engine: IPredictor):  # Depends on interface
```

#### 3. Dependency Injection in Main

**Before:**
```python
def main():
    auth_manager = AuthManager()  # Direct instantiation
    inference_engine = InferenceEngine()  # Direct instantiation
    render_sidebar(auth_manager)
```

**After:**
```python
def main():
    # Initialize dependencies (low-level modules)
    user_repository = UserRepository()
    config_loader = JsonConfigLoader()
    
    # Inject dependencies (dependency injection)
    auth_manager = AuthManager(user_repository)
    inference_engine = InferenceEngine(config_loader)
    
    # Pass abstractions to high-level modules
    render_sidebar(auth_manager)  # auth_manager is IAuthenticator
    render_upload_page(inference_engine)  # inference_engine is IPredictor
```

## Dependency Flow

### Before (Violation):
```
High-Level (UI) → Concrete Classes (AuthManager, InferenceEngine)
                ↓
            Low-Level (File I/O, JSON parsing)
```

### After (DIP Applied):
```
High-Level (UI) → Abstractions (IAuthenticator, IPredictor)
                        ↑
                  Concrete Classes (AuthManager, InferenceEngine)
                        ↓
                  Low-Level (UserRepository, ConfigLoader)
```

## Benefits

1. **Loose Coupling**: High-level modules don't depend on implementation details
2. **Testability**: Easy to create mock implementations of interfaces for testing
3. **Flexibility**: Can swap implementations without changing high-level code
4. **Maintainability**: Changes to concrete classes don't affect high-level modules
5. **Extensibility**: Can add new implementations of interfaces without modifying existing code

## Example: Testing with Mocks

```python
# Create mock authenticator for testing
class MockAuthenticator(IAuthenticator):
    def authenticate(self, username: str, password: str) -> bool:
        return username == "test" and password == "test"
    
    def create_session(self, username: str):
        pass
    
    def logout(self):
        pass

# Test UI function with mock
mock_auth = MockAuthenticator()
render_login_page(mock_auth)  # Works because it depends on IAuthenticator
```

## Files Modified
- ✅ Created: `interfaces.py` (new file)
  - `IAuthenticator` abstract interface
  - `IPredictor` abstract interface
- ✅ Modified: `app.py`
  - Lines 76-162: `AuthManager` implements `IAuthenticator`
  - Lines 169-292: `InferenceEngine` implements `IPredictor`
  - Lines 299, 330, 362: UI functions depend on interfaces
  - Lines 535-542: Dependency injection in `main()`

## Summary
By applying DIP, we've inverted the dependency structure so that both high-level and low-level modules depend on abstractions (interfaces), creating a more flexible, testable, and maintainable architecture.
