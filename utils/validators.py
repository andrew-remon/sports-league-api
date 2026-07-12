# local
import exceptions


def validate_team_name(name: str) -> bool:
    if not (3 <= len(name) <= 50):
        raise exceptions.ValidationError("Invalid Team Name", {"Error Detail": "too many or too large Team Name"})
    return all(char.isalnum or char == " " for char in name)  # to ensure every character is alphanumeric or a space.
