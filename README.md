# sshflow SSH Automation Tool

**sshflow** is a Python-based tool that automates the execution of system commands on remote Linux hosts via SSH. The tool detects the host's operating system and executes predefined commands based on the OS type (openSUSE, Debian, Rocky). It supports key-based authentication for SSH and allows you to run both user-level and sudo commands remotely.

## Features
- 🔑 **SSH Key-Based Authentication:** Connects to remote Linux machines via SSH using key-based authentication.
- 🌍 **OS Detection:** Automatically detects the OS type of the remote machine (openSUSE, Debian, Rocky).
- ⚙️ **OS-Specific Commands:** Executes OS-specific commands as listed in a configuration file.
- 🚀 **Supports sudo Commands:** Runs both normal and `sudo` commands with password handling for sudo actions.
- 🌈 **Color-Coded Output:** Command output and errors are displayed in a color-coded format for better readability.

## Requirements

- Python 3.x
- `paramiko` (for SSH connection handling)
- `colorama` (for colored output in the terminal)

To install the required Python libraries, run the following:

```bash
pip install paramiko colorama
```

## File Structure

```
.
├── sshflow.py         # Main script for executing commands on remote hosts
├── commands.txt        # File containing the list of commands for each OS
├── hosts.txt           # File containing the list of hosts and their usernames
└── config.py           # File containing SSH key path and sudo password (to be edited)
```

### 1. `commands.txt`
This file contains the commands to be executed on each OS. It is divided into sections for different OS types: openSUSE, Debian, and Rocky. Commands are listed under the corresponding OS heading.

Example:

```
[opensuse]
ifconfig -a
cat /etc/os-release
cat /etc/resolv.conf

[debian]
netstat -na
sudo apt update 

[rocky]
ps -aux
sudo dnf update -y
```

### 2. `hosts.txt`
This file contains a list of hosts (IP addresses) and usernames for remote machines to connect to. Each line should contain a space-separated `host` and `username`.

Example:

```
192.168.1.9 koosha
```

### 3. `config.py`
This file stores the path to the private SSH key and the sudo password. Edit it to match your setup.

Example:

```python
KEY_PATH = '/path/to/your/private/ssh/key'
SUDO_PASSWORD = 'your_sudo_password'
```

### 4. `sshflow.py`
This is the main script that runs the automation. It reads `commands.txt` to determine what commands to run for each operating system and executes them on the remote hosts specified in `hosts.txt`.

## Usage

### 1. **Edit `config.py`:** 
Provide the path to your private SSH key and your sudo password.

### 2. **Prepare `commands.txt`:**
Add your desired commands for each supported OS (openSUSE, Debian, Rocky).

### 3. **Prepare `hosts.txt`:**
List all hosts and usernames for the systems you want to connect to.

### 4. **Run the script:**

```bash
python sshflow.py commands.txt hosts.txt
```

The script will connect to each host in `hosts.txt`, determine the OS, and execute the appropriate commands from `commands.txt`.

## Output

- **Green**: Successful connection to a host.
- **Yellow**: Command being executed.
- **Cyan**: Command output from the remote host.
- **Red**: Error messages.

If an error occurs (e.g., connection failure, OS detection failure, command execution error), it will be displayed in red.

---

## Create Executable with PyInstaller

To create an installer file using `PyInstaller` from your Python project, follow these steps:

### Step 1: Install PyInstaller in Your Virtual Environment
First, you need to install `PyInstaller` in your virtual environment.

1. **Activate your virtual environment:**

   ```bash
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. **Install PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

### Step 2: Prepare the Project Files
Ensure that all required files are available. You should have the following files:

- `commands.txt`
- `config.py`
- `hosts.txt`
- `sshflow.py`
- `requirements.txt`

Make sure that `sshflow.py` is the main script that you want to package.

### Step 3: Create the PyInstaller Configuration
1. **Navigate to the project directory**:

   Ensure you're in the root directory of your project.

2. **Run PyInstaller on your Python script**:

   The simplest way to use `PyInstaller` is by specifying the main script file (`sshflow.py`):

   ```bash
   git clone https://gitlab.com/KooshaYeganeh/sshflow.git && cd sshflow && pyinstaller --onefile --add-data "commands.txt:." --add-data "hosts.txt:." --add-data "config.py:." sshflow.py && cp dist/sshflow . && rm -rvf dist build && rm sshflow.spec 
   ```

   on Windows, use `;` instead of `:`:

   ```bash
   pyinstaller --onefile --add-data "commands.txt;." --add-data "hosts.txt;." --add-data "config.py;." sshflow.py
   ```

### Step 4: Locate the Executable
Once the process completes, the packaged executable file will be found inside the `dist` folder.

Navigate to the `dist` directory:

```bash
cp dist/sshflow .
```

### Step 5: Test the Executable

Run the executable to make sure it works correctly.

On Linux:

```bash
./sshflow commands.txt hosts.txt
```

on Windows:

```bash
sshflow.exe commands.txt hosts.txt
```

### Step 6: Create an Installer (Optional)
If you want to create an installer for your packaged executable (e.g., `.exe` on Windows), you can use third-party tools like **Inno Setup** or **NSIS** for Windows or `dpkg`/`rpm` for Linux.

### Step 7: Distribute the Executable
Once the installer is created, distribute the packaged installer.

---

## Notes
- Ensure that SSH key-based authentication is set up correctly for all remote hosts.
- The script uses `sudo` for commands that require elevated privileges. You must provide the `SUDO_PASSWORD` in `config.py`.
- The script assumes the remote systems have the necessary commands available. Customize the command list for specific configurations or distributions.

---

For more details and updates, visit the official repository on GitHub:  
[website](https://kooshayeganeh.github.io)

