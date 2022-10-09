from copy import copy


class ConfigurableObject:

    def __init__(self, config=None) -> None:
        config = config or {}
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, copy(val))

    def set_default_config(self):
        pass
