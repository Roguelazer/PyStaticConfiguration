from staticconf import config


class MockConfiguration(object):
    """Convenience object for mocking configuration in tests."""

    def __init__(self, *args, **kwargs):
        name                = kwargs.pop('namespace', config.DEFAULT)
        self.namespace      = config.get_namespace(name)
        self.config_data    = dict(*args, **kwargs)
        self.old_values     = None

    def setup(self):
        self.old_values = dict(self.namespace.get_config_values())
        self.reset_namespace(self.config_data)
        config.reload(name=self.namespace.name)

    def teardown(self):
        self.reset_namespace(self.old_values)
        config.reload(name=self.namespace.name)

    def reset_namespace(self, new_values):
        self.namespace.configuration_values.clear()
        self.namespace.update_values(new_values)

    def __enter__(self):
        return self.setup()

    def __exit__(self, *args):
        self.teardown()