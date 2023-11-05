import re


TOTAL_CHARS = 16 # number of a device identifier

def validate_output(value: str or None) -> bool:
    """Validates if value is a chain of numbers and letters
        and counts its len accordingly to use case
        
    Args:
        value (string): output from OCR

    Returns:
        bool
    """
    if value == None:
        return False
    
    countInString = len(value.strip())
    
    if countInString == 0:
        return False
        
    regex = '^[a-zA-Z0-9]*$'
    return re.search(regex, value) and countInString is TOTAL_CHARS
   