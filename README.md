# Environment Variable Parser

A Python utility that converts flat environment variables into nested dictionaries with automatic type conversion.

## Features

- **Nested Dictionary Conversion**: Uses double underscore (`__`) for nesting levels and single underscore (`_`) to split keys
- **Lowercase Keys**: All keys are automatically converted to lowercase
- **Automatic Type Conversion**:
  - Integers: `"5432"` → `5432`
  - Floats: `"3.14"` → `3.14`
  - Booleans: `"true"`, `"1"`, `"yes"`, `"on"` → `True`
  - Booleans: `"false"`, `"0"`, `"no"`, `"off"` → `False`
  - Strings: Kept as-is

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Usage

### Command Line Interface

Run the script with a JSON string containing your environment variables:

```bash
python3 env_parser.py '{"ENV_VAR_NAME": "value"}'
```

### Testing the Script

#### Test 1: Simple Single Variable

```bash
python3 env_parser.py '{"APP_DB__PORT": "5432"}'
```

**Expected Output:**
```json
{
  "app": {
    "db": {
      "port": 5432
    }
  }
}
```

#### Test 2: Multiple Variables with Different Types

```bash
python3 env_parser.py '{"APP_NAME": "MyApp", "APP_DB__HOST": "localhost", "APP_DB__PORT": "5432", "APP_DEBUG": "true"}'
```

**Expected Output:**
```json
{
  "app": {
    "name": "MyApp",
    "db": {
      "host": "localhost",
      "port": 5432
    },
    "debug": true
  }
}
```

#### Test 3: Float and Boolean Conversion

```bash
python3 env_parser.py '{"APP_DB__TIMEOUT": "3.14", "APP_CACHE__ENABLED": "true", "APP_CACHE__TTL": "300", "APP_DEBUG": "false"}'
```

**Expected Output:**
```json
{
  "app": {
    "db": {
      "timeout": 3.14
    },
    "cache": {
      "enabled": true,
      "ttl": 300
    },
    "debug": false
  }
}
```

#### Test 4: Complex Nested Structure

```bash
python3 env_parser.py '{"SERVER_API__V1__ENDPOINT": "https://api.example.com", "SERVER_API__V1__PORT": "8080", "SERVER_API__V1__SECURE": "yes"}'
```

**Expected Output:**
```json
{
  "server": {
    "api": {
      "v1": {
        "endpoint": "https://api.example.com",
        "port": 8080,
        "secure": true
      }
    }
  }
}
```

#### Test 5: Boolean Variations

```bash
python3 env_parser.py '{"FEATURE_A": "1", "FEATURE_B": "yes", "FEATURE_C": "on", "FEATURE_D": "0", "FEATURE_E": "no", "FEATURE_F": "off"}'
```

**Expected Output:**
```json
{
  "feature": {
    "a": true,
    "b": true,
    "c": true,
    "d": false,
    "e": false,
    "f": false
  }
}
```

### Using as a Python Module

You can also import and use the function in your Python code:

```python
from env_parser import parse_env_vars

env_vars = {
    "APP_DB__HOST": "localhost",
    "APP_DB__PORT": "5432",
    "APP_DEBUG": "true"
}

result = parse_env_vars(env_vars)
print(result)
# Output: {'app': {'db': {'host': 'localhost', 'port': 5432}, 'debug': True}}
```

## How It Works

1. **Key Processing**:
   - Converts keys to lowercase
   - Splits by `__` for nesting levels
   - Further splits each part by `_` for individual key components

2. **Type Conversion**:
   - Attempts boolean conversion first
   - Then tries integer conversion
   - Then tries float conversion
   - Falls back to string if all conversions fail

## Example Transformations

| Input | Output |
|-------|--------|
| `APP_NAME` | `app.name` |
| `APP_DB__HOST` | `app.db.host` |
| `APP_DB__PORT` | `app.db.port` |
| `SERVER_API__V1__ENDPOINT` | `server.api.v1.endpoint` |

## Error Handling

If you provide invalid JSON, the script will display an error message:

```bash
python3 env_parser.py 'invalid json'
# Output: Error: Invalid JSON input - ...
```

## License

MIT
