import paramiko
import config
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

def read_file(file_path):
    """Reads a text file and returns its content as a list of lines."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def parse_commands(commands_file):
    """Parses commands from the file based on OS type."""
    commands = {
        'opensuse': [],
        'debian': [],
        'rocky': []
    }
    current_os = None
    with open(commands_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('['):  # New OS section
                current_os = line[1:-1].lower()  # Remove the brackets and convert to lowercase
            elif line and current_os:  # Non-empty command under a section
                commands[current_os].append(line)
    return commands

def get_os_type(ssh_client):
    """Determines the OS type on the remote host."""
    try:
        # Run the command to detect the OS type
        stdin, stdout, stderr = ssh_client.exec_command("cat /etc/os-release")
        os_info = stdout.read().decode().lower()
        if "ubuntu" in os_info or "debian" in os_info:
            return "debian"
        elif "opensuse" in os_info:
            return "opensuse"
        elif "rocky" in os_info or "centos" in os_info or "redhat" or "fedora" in os_info:
            return "rocky"
        else:
            return None  # Unknown OS
    except Exception as e:
        print(Fore.RED + f"Error detecting OS: {e}")
        return None

def execute_commands_on_host(host, username, key_path, commands, sudo_passwords, os_type):
    """Executes a list of commands on a remote host using SSH key-based authentication."""
    try:
        # Setup SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically accept unknown hosts
        
        # Connect to the host using the private key
        print(Fore.GREEN + f"Connecting to {host} as {username}...")
        ssh.connect(host, username=username, key_filename=key_path)
        
        # Get the sudo password for this host from the dictionary
        sudo_password = sudo_passwords.get(host)
        
        if not sudo_password:
            print(Fore.RED + f"No sudo password defined for {host}. Skipping...")
            return
        
        # Get OS-specific commands
        os_commands = commands.get(os_type, [])
        
        # Execute each command
        for command in os_commands:
            if 'sudo' in command:
                # Use echo to pass password to sudo
                command = f"echo {sudo_password} | sudo -S {command}"
            
            print(Fore.YELLOW + f"Executing: {command} on {host}")
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            if output:
                print(Fore.CYAN + f"Output from {host}: {output}")
            
            # Filter out the specific error message
            if error and "[sudo] password for root:" not in error:
                print(Fore.RED + f"Error from {host}: {error}")
        
        # Close the SSH connection
        ssh.close()
    except Exception as e:
        print(Fore.RED + f"Failed to connect or execute commands on {host}: {str(e)}")


def main(commands_file, hosts_file, key_path, sudo_passwords):
    """Main function to process commands on multiple hosts."""
    # Parse the commands from the file
    commands = parse_commands(commands_file)

    # Read hosts and usernames from file
    hosts = read_file(hosts_file)
    
    # Execute commands on each host with the corresponding username
    for entry in hosts:
        # Skip empty lines
        if not entry.strip():
            continue
        
        # Split each entry into host and username
        parts = entry.split()
        if len(parts) != 2:
            print(Fore.YELLOW + f"Skipping invalid line: {entry}")
            continue
        
        host, username = parts
        
        # Get OS type of the remote machine
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, username=username, key_filename=key_path)
            os_type = get_os_type(ssh)
            ssh.close()
        except Exception as e:
            os_type = None
            print(Fore.RED + f"Error detecting OS on {host}: {e}")
        
        # Execute the commands on the host if the OS type is recognized
        if os_type:
            print(Fore.GREEN + f"Detected {os_type} on {host}. Running commands...")
            execute_commands_on_host(host, username, key_path, commands, sudo_passwords, os_type)
        else:
            print(Fore.RED + f"Could not determine OS type for {host}. Skipping...")


if __name__ == "__main__":
    # Specify the paths to your files and SSH credentials
    commands_file = 'commands.txt'  # Path to your commands.txt file
    hosts_file = 'hosts.txt'        # Path to your hosts.txt file
    key_path = config.KEY_PATH  # Path to your private SSH key (e.g., ~/.ssh/id_rsa)
    sudo_password = config.SUDO_PASSWORDS  # Replace with your sudo password

    # Run the main function
    main(commands_file, hosts_file, key_path, sudo_password)
