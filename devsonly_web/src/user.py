from typing import Any, List, Dict

from src.logger import init_logger
from main.models import User, UserSettings


logger = init_logger(__name__)


def test_generate() -> None:
    # Function to write test users into database
    for i in range(10):
        user = User(
            password='test',
            username=f'test{i}',
            first_name='test',
            last_name='test',
            email='test@test.test',
        )
        user.save()
        userset = UserSettings(
            user=user,
            status='test',
            sex='test/test',
            hard_skills='test',
            work_place='test',
            education='test'
        )
        userset.save()


def get_accesses(user: User) -> Dict[str, int]:
    # Function returns dictionary with accessibility of profile parts
    string: str = UserSettings.objects.get(user=user).parts_access

    accesses: Dict[str, int] = {
        'date_of_birth': int(string[0]),
        'profile_picture': int(string[1]),
        'status': int(string[2]),
        'sex': int(string[3]),
        'hard_skills': int(string[4]),
        'work_place': int(string[5]),
        'education': int(string[6]),
    }

    return accesses


def write_accesses(accesses: Dict[str, int], user: User) -> bool:
    # Function to write accesses into database, returns True if successfully, else returns False
    string: str = ''
    is_valid = lambda s: False not in [c in ['0', '1'] for c in s] and len(s) == 7

    if is_valid(accesses):
        for key, value in accesses.items():
            string += value

        userset = UserSettings.objects.get(user=user)
        userset.parts_access = string
        return True
    else:
        logger.error('Invalid accesses string')
        return False


def user_exists(id: int) -> bool:
    # Function returns True if user with this id exists, else returns False
    return User.objects.filter(id=id).exists()


def userset_exists(id: int) -> bool:
    # Function returns True if user settings with this id exists, else returns False
    if user_exists(id):
        return UserSettings.objects.filter(user=User.objects.get(id=id))
    else:
        return False
