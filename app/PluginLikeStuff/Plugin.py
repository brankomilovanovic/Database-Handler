import abc


class Plugin(metaclass=abc.ABCMeta):

    """
    Activates the plugin.

    :return: True if the plugin is successfully activated, False otherwise.
    :rtype: bool
    """
    def activate(self) -> bool:
        raise NotImplementedError

    """
    Deactivates the current plugin.

    :return: A boolean value indicating whether the deactivation was successful or not.
    :rtype: bool
    """
    def deactivate(self) -> bool:
        raise NotImplementedError
