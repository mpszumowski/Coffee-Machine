from coffee_machine.config import get_config, get_params
from coffee_machine.exceptions import DregsContainerException


class DregsContainer(object):

    def __init__(self):
        config = get_config()
        params = get_params()
        self.warning_level = config['DregsContainer']['warning_level']
        self.error_level = params['DregsContainer']['error_level']
        self.max_volume = params['DregsContainer']['size']
        self._level = 0

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if value > self.max_volume:
            raise DregsContainerException("Dregs container is full!")
        self._level = value
        if self._level > self.max_volume * self.error_level:
            # TODO: notify machine to stop serving coffee
            pass
        elif self._level > self.max_volume * self.warning_level:
            # TODO: notify user to empty dregs container
            pass

    def store(self, value):
        self.level += value
