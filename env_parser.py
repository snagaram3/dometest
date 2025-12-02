import sys
import json
from typing import Dict, Any


def parse_env_vars(env_vars: Dict[str, str]) -> Dict[str, Any]:
    """
    Converts flat environment variables to nested dictionaries with automatic type conversion.

    Args:
        env_vars: Dictionary of environment variables with string keys and values

    Returns:
        Nested dictionary with converted types

    Examples:
        >>> env_vars = {"APP_DB__HOST": "localhost", "APP_DB__PORT": "5432"}
        >>> parse_env_vars(env_vars)
        {'app': {'db': {'host': 'localhost', 'port': 5432}}}
    """
    result = {}

    for key, value in env_vars.items():
        # Convert key to lowercase
        key_lower = key.lower()

        # Split by double underscore for nesting levels
        parts = key_lower.split('__')

        # Further split each part by single underscore
        nested_keys = []
        for part in parts:
            nested_keys.extend(part.split('_'))

        # Convert the value to appropriate type
        converted_value = _convert_value(value)

        # Build nested dictionary
        current = result
        for i, nested_key in enumerate(nested_keys[:-1]):
            if nested_key not in current:
                current[nested_key] = {}
            current = current[nested_key]

        # Set the final value
        current[nested_keys[-1]] = converted_value

    return result


def _convert_value(value: str) -> Any:
    """
    Converts string value to appropriate type.

    Args:
        value: String value to convert

    Returns:
        Converted value (int, float, bool, or str)
    """
    # Try to convert to boolean
    if value.lower() in ('true', '1', 'yes', 'on'):
        return True
    if value.lower() in ('false', '0', 'no', 'off'):
        return False

    # Try to convert to integer
    try:
        return int(value)
    except ValueError:
        pass

    # Try to convert to float
    try:
        return float(value)
    except ValueError:
        pass

    # Return as string if no conversion worked
    return value


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python env_parser.py '<JSON_ENV_VARS>'")
        print("Example: python env_parser.py '{\"APP_DB__PORT\": \"5432\"}'")
        sys.exit(1)

    try:
        # Parse JSON input from command line argument
        env_vars = json.loads(sys.argv[1])

        # Parse environment variables
        result = parse_env_vars(env_vars)

        # Print result as formatted JSON
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
