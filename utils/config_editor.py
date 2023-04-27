import os
import glob
import yaml
import webbrowser
import tkinter as tk
from tkinter import messagebox
from collections import OrderedDict


def create_default_config():
    default_config = {
        "matrix": {
            "homeserver": "",
            "bot_user_id": "",
            "access_token": ""
        },
        "matrix_rooms": [],
        "logging": {
            "level": "info"
        },
        "enabled_plugins": []
    }

    with open("config.yaml", "w") as f:
        yaml.dump(default_config, f)
    return default_config

def load_config():
    try:
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return create_default_config()

class Hyperlink(tk.Label):
    def __init__(self, master=None, **kwargs):
        self.default_color = kwargs.pop("fg", "blue")
        self.hover_color = kwargs.pop("hover_color", "darkblue")
        super().__init__(master, fg=self.default_color, cursor="hand2", **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        self.config(fg=self.hover_color)

    def on_leave(self, event):
        self.config(fg=self.default_color)

    def on_click(self, event):
        webbrowser.open(self.cget("text"))

# Functions
def ordered_yaml_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items()
        )

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


def get_plugin_names():
    plugin_files = glob.glob("./plugins/*_plugin.py")
    plugin_files = [p for p in plugin_files if os.path.basename(p) != "base_plugin.py"]
    plugin_names = [os.path.basename(p)[:-10] for p in plugin_files]
    return plugin_names

def create_meshtastic_frame(root):
    frame = tk.LabelFrame(root, text="Meshtastic", padx=5, pady=5)
    frame.pack(fill="x", padx=5, pady=5)

    connection_types = ["serial", "network"]
    connection_type_var = tk.StringVar(value=config["meshtastic"]["connection_type"])

    for i, ctype in enumerate(connection_types):
        radio_button = tk.Radiobutton(frame, text=ctype, variable=connection_type_var, value=ctype)
        radio_button.grid(row=0, column=i, padx=5)

    serial_port_label = tk.Label(frame, text="Serial Port:")
    serial_port_label.grid(row=1, column=0, sticky="w")
    serial_port_var = tk.StringVar(value=config["meshtastic"]["serial_port"])
    serial_port_entry = tk.Entry(frame, textvariable=serial_port_var)
    serial_port_entry.grid(row=1, column=1, sticky="ew")

    host_label = tk.Label(frame, text="Host:")
    host_label.grid(row=2, column=0, sticky="w")
    host_var = tk.StringVar(value=config["meshtastic"]["host"])
    host_entry = tk.Entry(frame, textvariable=host_var)
    host_entry.grid(row=2, column=1, sticky="ew")

    meshnet_name_label = tk.Label(frame, text="Meshnet Name:")
    meshnet_name_label.grid(row=3, column=0, sticky="w")
    meshnet_name_var = tk.StringVar(value=config["meshtastic"]["meshnet_name"])
    meshnet_name_entry = tk.Entry(frame, textvariable=meshnet_name_var)
    meshnet_name_entry.grid(row=3, column=1, sticky="ew")

    broadcast_enabled_label = tk.Label(frame, text="Broadcast Enabled:")
    broadcast_enabled_label.grid(row=4, column=0, sticky="w")
    broadcast_enabled_var = tk.BooleanVar(value=config["meshtastic"]["broadcast_enabled"])
    broadcast_enabled_checkbox = tk.Checkbutton(frame, variable=broadcast_enabled_var)
    broadcast_enabled_checkbox.grid(row=4, column=1, sticky="w")

    return {
        "connection_type": connection_type_var,
        "serial_port": serial_port_var,
        "host": host_var,
        "meshnet_name": meshnet_name_var,
        "broadcast_enabled": broadcast_enabled_var,
    }

def create_logging_frame(root):
    frame = tk.LabelFrame(root, text="Logging", padx=5, pady=5)
    frame.pack(fill="x", padx=5, pady=5)

    logging_options = ["info", "warn", "error", "debug"]
    logging_level_var = tk.StringVar(value=config["logging"]["level"])

    for i, level in enumerate(logging_options):
        radio_button = tk.Radiobutton(frame, text=level, variable=logging_level_var, value=level)
        radio_button.grid(row=0, column=i, padx=5)

    return logging_level_var

def create_plugins_frame(root):
    frame = tk.LabelFrame(root, text="Enabled Plugins", padx=5, pady=5)
    frame.pack(fill="x", padx=5, pady=5)

    plugin_names = get_plugin_names()
    plugin_vars = {}

    for i, plugin in enumerate(plugin_names):
        plugin_frame = tk.Frame(frame)
        plugin_frame.grid(row=i, column=0, padx=5, pady=5, sticky="w")

        active_var = tk.BooleanVar(value=config["plugins"][plugin]["active"])
        checkbox = tk.Checkbutton(plugin_frame, text=plugin, variable=active_var)
        checkbox.grid(row=0, column=0)

        plugin_vars[plugin] = {"active": active_var}

        nested_keys = [k for k in config["plugins"][plugin] if k != "active"]
        for j, nested_key in enumerate(nested_keys):
            label = tk.Label(plugin_frame, text=nested_key)
            label.grid(row=0, column=2 * j + 1, padx=(10, 0))

            nested_var = tk.StringVar(value=config["plugins"][plugin][nested_key])
            entry = tk.Entry(plugin_frame, textvariable=nested_var)
            entry.grid(row=0, column=2 * j + 2)

            plugin_vars[plugin][nested_key] = nested_var

    return plugin_vars


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def save_config(config):
    with open("config.yaml", "w") as f:
        ordered_yaml_dump(config, f)

def apply_changes():
    # Update matrix config
    for key, var in matrix_vars.items():
        config["matrix"][key] = var.get()
    new_config = OrderedDict()
    new_config["matrix"] = config["matrix"]
    new_config["meshtastic"] = config["meshtastic"]
    new_config["matrix_rooms"] = config["matrix_rooms"]
    new_config["logging"] = config["logging"]
    new_config["enabled_plugins"] = config["enabled_plugins"]

    save_config(new_config)
    messagebox.showinfo("Success", "Configuration changes saved.")

    # Update matrix_rooms config
    config["matrix_rooms"] = []
    for room_frame in matrix_rooms_frames:
        room_id = room_frame.room_id_var.get()
        meshtastic_channel = room_frame.meshtastic_channel_var.get()
        config["matrix_rooms"].append({"id": room_id, "meshtastic_channel": int(meshtastic_channel)})

    # Update logging config
    config["logging"]["level"] = logging_level_var.get()

    # Update enabled_plugins config
    for plugin, vars in plugin_vars.items():
        config["plugins"][plugin] = {k: v.get() for k, v in vars.items()}

    # Update meshtastic config
    for key, var in meshtastic_vars.items():
        if key == "broadcast_enabled":
            config["meshtastic"][key] = var.get()
        else:
            config["meshtastic"][key] = var.get()


def add_matrix_room(room=None, meshtastic_channel=None):
    if len(matrix_rooms_frames) >= 8:
        messagebox.showerror("Error", "There is a maximum of 8 Meshtastic channels.")
        return
    room_frame = tk.Frame(matrix_rooms_frame)
    room_frame.grid(row=len(matrix_rooms_frames), column=0, padx=5, pady=5, sticky="ew")

    room_frame.room_id_var = tk.StringVar(value=room or "")
    room_frame.meshtastic_channel_var = tk.StringVar(value=str(meshtastic_channel) if meshtastic_channel is not None else "")


    room_id_label = tk.Label(room_frame, text="ID:")
    room_id_label.grid(row=0, column=0)

    room_id_entry = tk.Entry(room_frame, textvariable=room_frame.room_id_var, width=40)
    room_id_entry.grid(row=0, column=1, padx=(0, 10))

    meshtastic_channel_label = tk.Label(room_frame, text="Meshtastic Channel:")
    meshtastic_channel_label.grid(row=0, column=2)

    meshtastic_channel_entry = tk.Entry(room_frame, textvariable=room_frame.meshtastic_channel_var, width=5)
    meshtastic_channel_entry.grid(row=0, column=3)

    matrix_rooms_frames.append(room_frame)

def remove_matrix_room():
    if len(matrix_rooms_frames) <= 1:
        messagebox.showerror("Error", "There must be at least one room & channel.")
        return
    if matrix_rooms_frames:
        frame_to_remove = matrix_rooms_frames.pop()
        frame_to_remove.destroy()

# GUI
config = load_config()

root = tk.Tk()
root.title("Config Editor")

# Matrix frame
matrix_frame = tk.LabelFrame(root, text="Matrix", padx=5, pady=5)
matrix_frame.pack(padx=10, pady=10, fill="x", expand="yes")

matrix_keys = ["homeserver", "bot_user_id", "access_token"]
matrix_vars = {}

for i, key in enumerate(matrix_keys):
    label = tk.Label(matrix_frame, text=key)
    label.grid(row=i, column=0, sticky="w")

    var = tk.StringVar(value=config["matrix"][key])
    entry = tk.Entry(matrix_frame, textvariable=var, width=49)
    entry.grid(row=i, column=1, sticky="ew")
    matrix_vars[key] = var

# Add instruction label
instruction_label = tk.Label(matrix_frame, text="For instructions on where to find your access token, visit:")
instruction_label.grid(row=3, column=0, columnspan=2, sticky="ew")

# Add hyperlink label
link_label = Hyperlink(matrix_frame, text="https://t2bot.io/docs/access_tokens/")
link_label.grid(row=4, column=0, columnspan=2, sticky="ew")

#Create meshtastic frame
meshtastic_vars = create_meshtastic_frame(root)

# Matrix rooms frame
matrix_rooms_frame = tk.LabelFrame(root, text="Matrix Rooms", padx=5, pady=5)
matrix_rooms_frame.pack(padx=10, pady=10, fill="both", expand="yes")

matrix_rooms_frames = []

for room in config["matrix_rooms"]:
    add_matrix_room(room["id"], room["meshtastic_channel"])

add_remove_frame = tk.Frame(matrix_rooms_frame)
add_remove_frame.grid(row=1000, column=0, padx=5, pady=5, sticky="ew")

add_button = tk.Button(add_remove_frame, text="+", command=add_matrix_room)
add_button.pack(side="left")

remove_button = tk.Button(add_remove_frame, text="-", command=remove_matrix_room)
remove_button.pack(side="left")

# Create logging frame
logging_level_var = create_logging_frame(root)

# Create plugins frame
plugin_vars = create_plugins_frame(root)

# Apply button
apply_button = tk.Button(root, text="Apply", command=apply_changes)
apply_button.pack(pady=10)

root.mainloop()
