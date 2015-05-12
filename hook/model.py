from . import CURRENT_DIR
import subprocess
import pprint
import copy


class Rule(object):
    """An individual rule for a repository.

    This holds all relevant information in relation to a specific
    trigger i.e. push, pull.
    """
    @classmethod
    def from_yaml(cls, **kwargs):
        """Creates a new instance of a rule in relation to the config file.

        This updates the dictionary of the class with the added details, which
        allows for flexibility in the configuation file.

        Only called when parsing the default configuation file.
        """
        ret = cls()

        for k, v in kwargs.iteritems():
            ret.__dict__[k] = v
        return ret

    def __init__(self):
        self.pull_repo = False
        self.on_error = "Error occurred"
        self.success = "Returned OK"
        self.actions = []

    def merge(self, new_dict):
        """Merges a dictionary into the Rule object."""
        actions = new_dict.pop("actions")
        for action in actions:
            self.add_action(action)

        self.__dict__.update(new_dict)

    def add_action(self, action):
        self.actions.append(action)

    def execute_actions(self, cwd):
        """Iterates over the actions and executes them in order."""
        for action in self.actions:
            print "executing {}".format(action)
            p = subprocess.Popen(action, shell=True, cwd=cwd)
            p.wait()


class CommandSet(object):
    """A set of Rules, as specified by the configuration file."""

    @classmethod
    def from_yaml(cls, defaults, **kwargs):
        """Creates a new instance of a rule by merging two dictionaries.

        This allows for independant configuration files to be merged
        into the defaults."""
        # TODO: I hate myself for this. Fix it later mmkay?
        if "token" not in defaults:
            kwargs["token"] = None

        defaults = copy.deepcopy(defaults)
        return cls(
            defaults=defaults,
            token=kwargs.pop("token"),
            directory=kwargs.pop("directory"),
            **kwargs
        )

    def __init__(self, defaults, token, directory, **kwargs):
        self.token = token
        self.directory = directory
        self.__dict__.update(defaults)

        for k, v in kwargs.iteritems():
            self.__dict__[k].merge(v)

    def __repr__(self):
        return str(self.__dict__)

    def execute_hook(self, hook):
        rule = self.__dict__.get(hook, None)
        try:
            rule.execute_actions(self.directory)
            return rule.success
        except Exception, e:
            print e
