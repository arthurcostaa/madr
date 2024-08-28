def sanitize(string):
    cleaned_string = ' '.join(string.split()).lower()
    return ''.join(
        char for char in cleaned_string if char.isalnum() or char.isspace()
    )
