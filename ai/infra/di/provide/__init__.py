from .general import get_providers as get_general_providers
from .other import get_providers as get_other_providers


def get_providers():
    return [
        *get_general_providers(),
        *get_other_providers(),
    ]
