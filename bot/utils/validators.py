import re

def validate_phone(phone: str) -> bool:
    pattern = r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$'
    return bool(re.match(pattern, phone))