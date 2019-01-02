from exceptions import DregsContainerException


class DregsContainer(object):
    warning_level = 0.5  # TODO: consider taking from settings
    error_level = 0.9

    def __init__(self, max_volume=500):
        self.max_volume = max_volume
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
