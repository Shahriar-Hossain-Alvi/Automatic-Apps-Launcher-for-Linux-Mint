# App Description
If you have a slow and old pc, this script is for you. You can schedule apps to launch after your pc boots and go take a nap!!!

**This program lets you select multiple apps which will be automatically started after your pc boots.**

**It reads your HDD and CPU usage and starts selected apps one by one when HDD and CPU usage is normal.**
> The default normal usage is 60% CPU and 5 MB/s read speed.

# Installation & Setup

### 1. Update the system package list
```
sudo apt update
```

### 2. Install Tkinter (The GUI library)
> This is required for the window and buttons to appear
```
sudo apt install python3-tk
```

### 3. Install Psutil (The system monitoring library)
> This is required for the script to "feel" the HDD usage
```
sudo apt install python3-psutil
```

### 4. Make the Script Executable
Navigate to the folder where you saved smart_launcher_gui.py, open a terminal and run (One time only):
```
chmod +x smart_launcher_gui.py
```

### 5. Add to Linux Mint Menu (Optional but Recommended - One time only)
To find the app in your Start Menu, create a desktop entry:

1. Create the file(Open a terminal & run) : nano ~/.local/share/applications/alvi-launcher.desktop

2. Paste the following (Update the Exec path to your actual path):
```
[Desktop Entry]
Type=Application
Name=Alvi Smart Launcher(Or any name you prefer)
Comment=Launches apps based on HDD health
Exec=python3 "/path/to/your/smart_launcher_gui.py"
Icon=system-run
Terminal=false
Categories=Development;
```

After that press `Ctrl + O` then `Enter` then `Ctrl + X` to save the file.


### 3. Run at Startup: Open Startup Applications from the Mint Menu. (One time only)

1. Click Add -> Custom Command.
2. Name: Smart Launcher(Or any name you prefer)
3. Command: python3 "/path/to/your/smart_launcher_gui.py"
4. Delay: 30 seconds (to allow core OS services to load first).


### 4. How to Add Apps in the Smart Launcher
**When the GUI opens:**

1. *App Name*: Any name you prefer (e.g., Backend Project, Browser, VSCode).

2. *Command*: The terminal command to run.
    > EG: For Apps that are in your menu: Open menu > Find the app > Right Click > Properties > Command (Copy the command) and paste it here
    
    > For VS Code Folders: code "/home/username/path with spaces/project" (Use quotes for paths with spaces!)

**After adding the apps in the GUI you can click the "Launch Now" button to launch the apps every time your pc boots**

# ⚠️ Cautions & Notes
- Path Changes: Remember that if you ever rename or move your project folders, you must update the command in the Launcher GUI, or it will fail to find the directory.

- VS Code Loading: VS Code windows appear before the internal extensions (Python, Docker, etc.) finish loading. The script includes a default 30-second delay between launches to accommodate this.

- Auto Launch: If you want the apps to launch automatically after the **Smart Launcher** starts then look at the line 129 in the code. Then uncomment the line ```root.after(5000, app.run_launch_logic)``` then save the file and restart the *Smart Launcher*. After that the apps that are listed in the **Smart Launcher** will launch automatically after the delayed time eg: 5000 for 5 seconds.

- Do not remove the first line ```#!/usr/bin/env python3`` from the file. This is not a comment and required for the script to run. 