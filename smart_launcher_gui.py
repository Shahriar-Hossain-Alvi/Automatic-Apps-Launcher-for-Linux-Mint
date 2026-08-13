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
        self.selected_apps = set()

        # UI Elements
        tk.Label(root, text="App Name:").pack()
        self.name_entry = tk.Entry(root, width=50)
        self.name_entry.pack()

        tk.Label(
            root, text="Command (e.g., 'code /path/to/folder' or 'brave'):").pack()
        self.cmd_entry = tk.Entry(root, width=50)
        self.cmd_entry.pack()

        tk.Button(root, text="Add App", command=self.add_app).pack(pady=5)

        self.tree = ttk.Treeview(
            root, 
            columns=(
            "Launch", "Name", "Command"
            ), 
            show='headings')

        self.tree.heading("Launch", text="Launch")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Command", text="Command")

        self.tree.column("Launch", width=60, anchor="center")
        self.tree.column("Name", width=160, anchor="w")

        self.tree.pack(fill="both", expand=True, padx=10)

        self.tree.bind("<Button-1>", self.toggle_launch_selection)

        tk.Button(root, text="Remove Selected",
                  command=self.remove_app).pack(pady=5)
        tk.Button(root, text="🚀 Launch Now", command=self.run_launch_logic,
                  bg="green", fg="white").pack(pady=10)

        self.refresh_list()

    def refresh_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for index, app in enumerate(self.apps):
            checkbox = "☑" if index in self.selected_apps else "☐"

            self.tree.insert(
                "",
                "end",
                values=(checkbox, app['name'], " ".join(app['cmd']))
            )

    def toggle_launch_selection(self, event):
        region = self.tree.identify("region", event.x, event.y)

        # Only toggle when clicking a table cell
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)

        # Only react to clicks in the Launch column
        if column != "#1":
            return

        item = self.tree.identify_row(event.y)

        if not item:
            return

        index = self.tree.index(item)

        if index in self.selected_apps:
            self.selected_apps.remove(index)
        else:
            self.selected_apps.add(index)

        self.refresh_list()

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

    # def run_launch_logic(self):
    #     if not self.selected_apps:
    #         messagebox.showwarning(
    #             "No Apps Selected",
    #             "Please select at least one app to launch."
    #         )
    #         return
        
    #     self.root.destroy()
    #     print("🚀 Starting smart launch sequence...")

    #     for index, app in self.apps:
    #         # Skip apps that were not selected
    #         if index not in self.selected_apps:
    #             print(f"⏭️ Skipping: {app['name']}")
    #             continue

    #         print(f"Checking system health for: {app['name']}")

    #         # Wait until the HDD is NOT saturated
    #         while True:
    #             cpu = psutil.cpu_percent(interval=1)

    #             disk_before = psutil.disk_io_counters()

    #             time.sleep(2)  # Measure over 2 seconds

    #             disk_after = psutil.disk_io_counters()

    #             # Calculate how much data was read/written in those 2 seconds
    #             # If it's more than 5MB, the HDD is likely busy
    #             read_speed = (disk_after.read_bytes -  # type: ignore
    #                           disk_before.read_bytes) / 1024 / 1024  # type: ignore

    #             if cpu < 60 and read_speed < 5.0:
    #                 break  # System is quiet enough
    #             else:
    #                 print(
    #                     f"  [WAITING] CPU: {cpu}% | Disk: {read_speed:.1f} MB/s. HDD is busy...")

    #         # Launch
    #         try:
    #             # Use shell=True to handle the quoted paths correctly
    #             cmd_string = " ".join(app['cmd'])

    #             subprocess.Popen(cmd_string, shell=True)

    #             print(f"✅ Triggered {app['name']}")

    #             # IMPORTANT: Sleep for 30s because your HDD is slow.
    #             # This gives VS Code enough time to actually start
    #             # before the script checks the disk again.
    #             time.sleep(30)
    #         except Exception as e:
    #             print(f"❌ Error: {e}")

    #     print("🎯 Startup complete!")

    def run_launch_logic(self):

        print("\n========================================")
        print("🚀 Launch button pressed")
        print("========================================")

        print(f"Selected indexes: {self.selected_apps}")

        # Check whether anything was selected
        if not self.selected_apps:
            messagebox.showwarning(
                "No Apps Selected",
                "Please select at least one app to launch."
            )
            print("❌ No apps selected.")
            return

        # Build list of selected apps
        selected_apps = [
            self.apps[index]
            for index in sorted(self.selected_apps)
            if index < len(self.apps)
        ]

        print("\nApps selected for launch:")

        for app in selected_apps:
            print(f"  ✅ {app['name']}")
            print(f"     Command: {app['cmd']}")

        print("\n========================================")
        print("Starting launch sequence...")
        print("========================================\n")

        self.root.destroy()

        for app in selected_apps:

            print(f"🔍 Checking system health for: {app['name']}")

            # ---------------------------------------------------------
            # Wait until the HDD and CPU are not heavily loaded
            # ---------------------------------------------------------

            while True:

                cpu = psutil.cpu_percent(interval=1)

                disk_before = psutil.disk_io_counters()

                time.sleep(2)

                disk_after = psutil.disk_io_counters()

                if disk_after is None or disk_before is None:
                    print("⚠️ Could not read disk I/O counters. Retrying...")
                    continue

                read_speed = (
                    (disk_after.read_bytes - disk_before.read_bytes)
                    / 1024
                    / 1024
                )

                print(
                    f"   CPU: {cpu}% | "
                    f"Disk read: {read_speed:.1f} MB/s"
                )

                if cpu < 60 and read_speed < 5.0:
                    break

                print(
                    "   ⏳ System is busy. Waiting..."
                )

            # ---------------------------------------------------------
            # Launch application
            # ---------------------------------------------------------

            try:

                cmd_string = " ".join(app["cmd"])

                print(
                    f"🚀 Launching: {app['name']}"
                )

                print(
                    f"   Command: {cmd_string}"
                )

                process = subprocess.Popen(
                    cmd_string,
                    shell=True
                )

                print(
                    f"✅ Triggered {app['name']} "
                    f"(PID: {process.pid})"
                )

                # Give the slow HDD time to load the application.
                # time.sleep(30) # redundant

            except Exception as e:

                print(
                    f"❌ Error launching "
                    f"{app['name']}: {e}"
                )

        print("\n========================================")
        print("🎯 Startup complete!")
        print("========================================")


if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)

    # This line will automatically trigger the launch after 5 seconds
    # so you have time to cancel or add an app if you need to.
    # root.after(5000, app.run_launch_logic)

    root.mainloop()
