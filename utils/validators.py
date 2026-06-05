def validate_team_name(name: str) -> bool:
    if not (3 <= len(name) <= 50):
        return False
    return all(char.isalnum or char == ' ' for char in name) # to ensure every character is alphanumeric or a space.
