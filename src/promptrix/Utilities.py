import json
import yaml

class Utilities:
    """
    Utility functions.
    """
    @staticmethod
    def to_string(tokenizer, value):
        """
        Converts a value to a string.
        Dates are converted to ISO strings and Objects are converted to JSON or YAML, whichever is shorter.
        :param tokenizer: Tokenizer to use for encoding.
        :param value: Value to convert.
        :returns: Converted value.
        """
        if value is None:
            return ''
        elif isinstance(value, dict):
            if hasattr(value, 'isoformat'):
                return value.isoformat()
            else:
                as_json = json.dumps(value)
                return as_json
        else:
            return str(value)
