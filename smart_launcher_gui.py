#!/usr/bin/env python3
import os
import time
import subprocess
import psutil
import json
import tkinter as tk
from tkinter import messagebox, ttk

CONFIG_FILE = os.path.expanduser("~/.smart_launcher_config.json")


def load_apps():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return []


def save_apps(apps):
    with open(CONFIG_FILE, "w") as f:
        json.dump(apps, f)


class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alvi's Smart Launcher")
        self.root.geometry("500x600")

        self.apps = load_apps()

        # UI Elements
        tk.Label(root, text="App Name:").pack()
        self.name_entry = tk.Entry(root, width=50)
        self.name_entry.pack()

        tk.Label(
            root, text="Command (e.g., 'code /path/to/folder' or 'brave'):").pack()
        self.cmd_entry = tk.Entry(root, width=50)
        self.cmd_entry.pack()

        tk.Button(root, text="Add App", command=self.add_app).pack(pady=5)

        self.tree = ttk.Treeview(root, columns=(
            "Name", "Command"), show='headings')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Command", text="Command")
        self.tree.pack(fill="both", expand=True, padx=10)

        tk.Button(root, text="Remove Selected",
                  command=self.remove_app).pack(pady=5)
        tk.Button(root, text="🚀 Launch Now", command=self.run_launch_logic,
                  bg="green", fg="white").pack(pady=10)

        self.refresh_list()

    def refresh_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for app in self.apps:
            self.tree.insert("", "end", values=(app['name'], app['cmd']))

    def add_app(self):
        name, cmd = self.name_entry.get(), self.cmd_entry.get()
        if name and cmd:
            self.apps.append({"name": name, "cmd": cmd.split()})
            save_apps(self.apps)
            self.refresh_list()
        else:
            messagebox.showwarning("Input Error", "Please fill both fields")

    def remove_app(self):
        selected = self.tree.selection()
        if selected:
            idx = self.tree.index(selected[0])
            del self.apps[idx]
            save_apps(self.apps)
            self.refresh_list()

    def run_launch_logic(self):
        self.root.destroy()
        print("🚀 Starting smart launch sequence...")

        for app in self.apps:
            print(f"Checking system health for: {app['name']}")

            # Wait until the HDD is NOT saturated
            while True:
                cpu = psutil.cpu_percent(interval=1)
                disk_before = psutil.disk_io_counters()
                time.sleep(2)  # Measure over 2 seconds
                disk_after = psutil.disk_io_counters()

                # Calculate how much data was read/written in those 2 seconds
                # If it's more than 5MB, the HDD is likely busy
                read_speed = (disk_after.read_bytes -  # type: ignore
                              disk_before.read_bytes) / 1024 / 1024  # type: ignore

                if cpu < 60 and read_speed < 5.0:
                    break  # System is quiet enough
                else:
                    print(
                        f"  [WAITING] CPU: {cpu}% | Disk: {read_speed:.1f} MB/s. HDD is busy...")

            # Launch
            try:
                # Use shell=True to handle the quoted paths correctly
                cmd_string = " ".join(app['cmd'])
                subprocess.Popen(cmd_string, shell=True)
                print(f"✅ Triggered {app['name']}")

                # IMPORTANT: Sleep for 30s because your HDD is slow.
                # This gives VS Code enough time to actually start
                # before the script checks the disk again.
                time.sleep(30)
            except Exception as e:
                print(f"❌ Error: {e}")

        print("🎯 Startup complete!")


if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)

    # This line will automatically trigger the launch after 5 seconds
    # so you have time to cancel or add an app if you need to.
    # root.after(5000, app.run_launch_logic)

    root.mainloop()
