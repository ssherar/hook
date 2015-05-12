"""Sets defaults and verifies file structure."""
import os

DEFAULTS_PATH = os.path.expanduser("~/.config/hook/default.yml")
USER_PATH = os.path.expanduser("~/.config/hook/rules.yml")
CONFIG_DIR = os.path.expanduser("~/.config/hook")
CURRENT_DIR = os.getcwd()

if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

for file, path in {"default.yml": DEFAULTS_PATH,
                   "rules.yml": USER_PATH}.iteritems():
    import shutil
    if not os.path.exists(path):
        shutil.copy(file, path)
