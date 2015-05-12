"""Handle parsing of the 2 different config files."""
import yaml
import pprint
import os
from .model import Rule, CommandSet
from . import DEFAULTS_PATH, USER_PATH


def import_default(path):
    with open(path) as f:
        structure = yaml.load(f)
        defaults = structure.pop("all")
        for k, v in structure.iteritems():
            if isinstance(v, dict):
                copy = defaults.copy()
                copy.update(v)
                structure[k] = copy

        return {k: Rule.from_yaml(**v) for k, v in structure.iteritems()
                if isinstance(v, dict)}


def import_rules(path, defaults):
    with open(path) as f:
        structure = yaml.load(f)
        return {k: CommandSet.from_yaml(defaults, **v)
                for k, v in structure.iteritems()}


def get_rules():
    defaults = import_default(DEFAULTS_PATH)
    ret = import_rules(USER_PATH, defaults)

    return ret
