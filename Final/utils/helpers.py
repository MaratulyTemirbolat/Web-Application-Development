from secrets import SystemRandom
from string import (
    ascii_letters,
    digits,
    punctuation,
)


def generate_secure_random_string(length: int = 12) -> str:
    """Function to generate a secure random string."""
    characters: list[str] = ascii_letters + digits + punctuation
    secure_random: SystemRandom = SystemRandom()
    random_string: str = ''.join(secure_random.choice(characters) for _ in range(length))
    return random_string
