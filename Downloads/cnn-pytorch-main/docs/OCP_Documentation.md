# Open/Closed Principle (OCP) - Documentation

## Principle Overview
The Open/Closed Principle states that software entities should be **open for extension** but **closed for modification**. You should be able to add new functionality without changing existing code.

## Problem Identified
The original `InferenceEngine` class violated OCP by being **closed for extension**:

1. **Hard-coded JSON loading**: Configuration loading was tightly coupled to JSON format
2. **No abstraction**: Adding support for other config formats (YAML, environment variables, etc.) would require modifying the class
3. **Inflexible**: Cannot extend configuration sources without changing existing code

**Original Code:**
```python
def _load_config(self, config_path: str) -> dict:
    with open(config_path, 'r') as f:
        return json.load(f)  # Hard-coded to JSON
```

## Solution Implemented

### Created: `config_loader.py`
Introduced an abstraction layer for configuration loading:

**Abstract Base Class: `ConfigLoader`**
- Defines the contract for all configuration loaders
- Single abstract method: `load(path: str) -> Dict[str, Any]`

**Concrete Implementation: `JsonConfigLoader`**
- Implements `ConfigLoader` for JSON files
- Handles JSON-specific loading and error handling

**Extensibility:**
Future loaders can be added without modifying existing code:
- `YamlConfigLoader` - for YAML configuration files
- `EnvironmentConfigLoader` - for environment variables
- `DatabaseConfigLoader` - for database-stored configuration
- `RemoteConfigLoader` - for remote configuration services

### Modified: `app.py` - `InferenceEngine` class
Refactored to use the `ConfigLoader` abstraction:

**Changes Made:**
1. Injected `ConfigLoader` as a dependency via constructor
2. Removed hard-coded JSON loading logic
3. Delegates all configuration loading to the injected loader
4. Now **open for extension** (new loaders) but **closed for modification** (no code changes needed)

**Before:**
```python
class InferenceEngine:
    def __init__(self, config_path: str = "config/model_config.json"):
        self.config = self._load_config(config_path)
        self.class_names = self._load_class_names()
    
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return json.load(f)  # Tightly coupled to JSON
    
    def _load_class_names(self) -> List[str]:
        with open("config/class_names.json", 'r') as f:
            data = json.load(f)  # Tightly coupled to JSON
            return data['classes']
```

**After:**
```python
class InferenceEngine(IPredictor):
    def __init__(self, config_loader: ConfigLoader, 
                 model_config_path: str = "config/model_config.json",
                 class_names_path: str = "config/class_names.json"):
        self.config_loader = config_loader  # Dependency injection
        self.config = self._load_config(model_config_path)
        self.class_names = self._load_class_names(class_names_path)
    
    def _load_config(self, config_path: str) -> dict:
        return self.config_loader.load(config_path)  # Delegates to abstraction
    
    def _load_class_names(self, class_names_path: str) -> List[str]:
        data = self.config_loader.load(class_names_path)  # Delegates to abstraction
        return data.get('classes', [])
```

## Benefits

1. **Extensibility**: New configuration sources can be added by creating new `ConfigLoader` implementations
2. **No Modification**: Existing code (`InferenceEngine`) doesn't need to change when adding new loaders
3. **Flexibility**: Can switch configuration sources at runtime by injecting different loaders
4. **Testing**: Easy to create mock loaders for testing
5. **Polymorphism**: All loaders share the same interface, making them interchangeable

## Example Extension (Future)
To add YAML support, simply create a new class:

```python
class YamlConfigLoader(ConfigLoader):
    def load(self, path: str) -> Dict[str, Any]:
        import yaml
        with open(path, 'r') as f:
            return yaml.safe_load(f)

# Usage - no changes to InferenceEngine needed!
yaml_loader = YamlConfigLoader()
engine = InferenceEngine(yaml_loader)
```

## Files Modified
- ✅ Created: `config_loader.py` (new file)
  - `ConfigLoader` abstract base class
  - `JsonConfigLoader` concrete implementation
- ✅ Modified: `app.py` (lines 169-196)
  - Refactored `InferenceEngine` to use `ConfigLoader` abstraction
  - Added dependency injection of `ConfigLoader`
  - Updated `main()` to instantiate and inject `JsonConfigLoader`
