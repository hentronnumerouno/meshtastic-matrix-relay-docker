import sys
import importlib
from pathlib import Path
from log_utils import get_logger

logger = get_logger(name="Plugins")

plugins = []


def load_plugins():
    global plugins
    if plugins:
        return plugins

    plugins = []
    plugin_dirs = [Path("plugins"), Path("custom_plugins")]

    for plugin_folder in plugin_dirs:
        sys.path.insert(0, str(plugin_folder.resolve()))

        for plugin_file in plugin_folder.glob("*.py"):
            plugin_name = plugin_file.stem
            if plugin_name == "__init__":
                continue
            plugin_module = importlib.import_module(plugin_name)
            if hasattr(plugin_module, "Plugin"):
                plugin = plugin_module.Plugin()
                if plugin.config["active"]:
                    logger.debug(f"Loaded plugin {plugin_folder/plugin_name}")
                    plugins.append(plugin)

    return plugins