import re


def email(email_str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email_str):
        return email_str
    else:
        raise ValueError(f'{email_str} is not a valid email.')

def password(password_str):
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!-/:-@[-`{-~])[A-Za-z\d!-/:-@[-`{-~]{8,}$'
    if re.fullmatch(regex, password_str):
        return password_str
    else:
        raise ValueError(f'{password_str} must contain one special character, one capital letter, and be at least 8 characters.')