#!/bin/bash

# Tạo thư mục cài đặt
INSTALL_DIR="$HOME/.git-profile-manager"
mkdir -p "$INSTALL_DIR"

# Tạo file menu.py
cat > "$INSTALL_DIR/menu.py" << 'EOL'
#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import json

# Cấu hình
CONFIG_FILE = Path.home() / '.git_profiles.json'
SSH_DIR = Path.home() / '.ssh'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print("""
   _______ _____ _______     ____  ____  ____  ______ _____ __    _____
  / ____(_) __//_  __(_)   / __ \/ __ \/ __ \/ ____//   _// /   / ___/
 / / __/ / /_   / /  _    / /_/ / /_/ / / / / /_    / / / /    \__ \ 
/ /_/ / / __/  / /  (_)  / ____/ _, _/ /_/ / __/  _/ / / /___ ___/ / 
\____/_/_/    /_/  (_)  /_/   /_/ |_|\____/_/    /___//_____//____/  
""")

def load_profiles():
    """Load profiles from config file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    """Save profiles to config file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)

def get_current_git_config():
    """Get current Git global configuration."""
    try:
        name = subprocess.check_output(['git', 'config', '--global', 'user.name']).decode().strip()
        email = subprocess.check_output(['git', 'config', '--global', 'user.email']).decode().strip()
        return {'name': name, 'email': email}
    except:
        return None

def set_git_config(name, email):
    """Set Git global configuration."""
    subprocess.run(['git', 'config', '--global', 'user.name', name])
    subprocess.run(['git', 'config', '--global', 'user.email', email])

def generate_ssh_key(email, profile_name):
    """Generate SSH key for the profile."""
    if not SSH_DIR.exists():
        SSH_DIR.mkdir(mode=0o700)
    
    key_file = SSH_DIR / f"id_rsa_{profile_name}"
    if key_file.exists():
        print(f"\nSSH key for profile '{profile_name}' already exists!")
        return str(key_file)
    
    print(f"\nGenerating SSH key for profile '{profile_name}'...")
    subprocess.run([
        'ssh-keygen',
        '-t', 'rsa',
        '-b', '4096',
        '-C', email,
        '-f', str(key_file),
        '-N', ''
    ])
    
    config_file = SSH_DIR / 'config'
    config_content = f"""
# Git profile: {profile_name}
Host github.com-{profile_name}
    HostName github.com
    User git
    IdentityFile {key_file}
"""
    with open(config_file, 'a') as f:
        f.write(config_content)
    
    return str(key_file)

def open_github_ssh_settings():
    """Open GitHub SSH settings page."""
    try:
        if sys.platform == 'darwin':  # macOS
            subprocess.run(['open', 'https://github.com/settings/ssh/new'])
        elif sys.platform == 'win32':  # Windows
            subprocess.run(['start', 'https://github.com/settings/ssh/new'], shell=True)
        else:  # Linux
            subprocess.run(['xdg-open', 'https://github.com/settings/ssh/new'])
    except:
        print("\nPlease visit: https://github.com/settings/ssh/new")

def show_ssh_instructions(key_file, profile_name):
    """Show instructions for setting up SSH key with GitHub."""
    print("\n=== GitHub SSH Key Setup Instructions ===")
    print("1. Your SSH public key:")
    print("-" * 50)
    
    # Read and copy public key
    with open(f"{key_file}.pub", 'r') as f:
        public_key = f.read().strip()
        print(public_key)
    
    print("-" * 50)
    
    # Open GitHub SSH settings
    print("\nOpening GitHub SSH settings page...")
    open_github_ssh_settings()
    
    print("\nInstructions:")
    print(f"1. Title: '{profile_name} - Git Profile Manager'")
    print("2. Paste the public key into 'Key' field")
    print("3. Click 'Add SSH key'")
    
    print(f"\nWhen cloning repositories, use URLs in this format:")
    print(f"git@github.com-{profile_name}:username/repository.git")
    
    # Wait for user confirmation
    input("\nPress Enter after adding the SSH key to GitHub...")
    
    # Test connection
    print("\nTesting GitHub connection...")
    try:
        result = subprocess.run(
            ['ssh', '-T', f'git@github.com-{profile_name}'],
            capture_output=True,
            text=True,
            env={'GIT_SSH_COMMAND': f'ssh -i {key_file}'}
        )
        
        if "successfully authenticated" in result.stderr.lower():
            print("\n✓ Successfully connected to GitHub!")
            return True
        else:
            print("\n✗ Connection failed!")
            print("Error:", result.stderr)
            return False
    except Exception as e:
        print("\n✗ Connection error:", str(e))
        return False

def add_profile():
    """Add a new Git profile."""
    profiles = load_profiles()
    
    print("\n=== Add New Git Profile ===")
    username = input("Enter GitHub username: ").strip()
    
    if username in profiles:
        print(f"\nProfile '{username}' already exists!")
        return
    
    email = input("Enter Git email: ").strip()
    
    # Generate SSH key
    key_file = generate_ssh_key(email, username)
    
    profiles[username] = {
        'name': username,
        'email': email,
        'ssh_key': key_file
    }
    
    save_profiles(profiles)
    set_git_config(username, email)
    print(f"\n✓ Profile '{username}' added and activated!")
    
    # Show SSH setup instructions
    show_ssh_instructions(key_file, username)

def switch_profile():
    """Switch to a different Git profile."""
    profiles = load_profiles()
    
    if not profiles:
        print("\nNo profiles found! Please add a profile first.")
        return
    
    print("\n=== Switch Git Profile ===")
    print("Available profiles:")
    for name in profiles:
        print(f"- {name}")
    
    profile_name = input("\nEnter profile name: ").strip()
    
    if profile_name not in profiles:
        print(f"\nProfile '{profile_name}' not found!")
        return
    
    profile = profiles[profile_name]
    set_git_config(profile['name'], profile['email'])
    print(f"\n✓ Switched to profile '{profile_name}'!")
    
    # Update repository URL if in a Git repository
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True)
        current_url = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode().strip()
        
        if current_url.startswith('git@github.com'):
            if 'github.com-' in current_url:
                parts = current_url.split('github.com-')
                old_profile = parts[1].split(':')[0]
                new_url = current_url.replace(f'github.com-{old_profile}:', f'github.com-{profile_name}:')
            else:
                repo_part = current_url.split('github.com:')[1]
                new_url = f"git@github.com-{profile_name}:{repo_part}"
            
            subprocess.run(['git', 'remote', 'set-url', 'origin', new_url])
            print(f"\n✓ Repository URL updated: {new_url}")
    except:
        pass

def list_profiles():
    """List all saved profiles."""
    profiles = load_profiles()
    
    if not profiles:
        print("\nNo profiles found!")
        return
    
    print("\n=== Git Profiles ===")
    for name, profile in profiles.items():
        print(f"\nProfile: {name}")
        print(f"Name: {profile['name']}")
        print(f"Email: {profile['email']}")
        if 'ssh_key' in profile:
            print(f"SSH key: {profile['ssh_key']}")

def remove_profile():
    """Remove a Git profile."""
    profiles = load_profiles()
    
    if not profiles:
        print("\nNo profiles to remove!")
        return
    
    print("\n=== Remove Profile ===")
    print("Available profiles:")
    for name in profiles:
        print(f"- {name}")
    
    profile_name = input("\nEnter profile name to remove: ").strip()
    
    if profile_name not in profiles:
        print(f"\nProfile '{profile_name}' not found!")
        return
    
    # Check if this is the current profile
    current = get_current_git_config()
    profile = profiles[profile_name]
    
    if (current and 
        current['name'] == profile['name'] and 
        current['email'] == profile['email']):
        # Remove Git global config
        subprocess.run(['git', 'config', '--global', '--unset', 'user.name'])
        subprocess.run(['git', 'config', '--global', '--unset', 'user.email'])
    
    # Remove SSH keys
    if 'ssh_key' in profile:
        try:
            os.remove(profile['ssh_key'])
            os.remove(f"{profile['ssh_key']}.pub")
            
            # Remove SSH config
            config_file = SSH_DIR / 'config'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    lines = f.readlines()
                
                new_lines = []
                skip = False
                for line in lines:
                    if f"Git profile: {profile_name}" in line:
                        skip = True
                        continue
                    if skip and line.strip() == "":
                        skip = False
                        continue
                    if not skip:
                        new_lines.append(line)
                
                with open(config_file, 'w') as f:
                    f.writelines(new_lines)
        except:
            pass
    
    del profiles[profile_name]
    save_profiles(profiles)
    print(f"\n✓ Profile '{profile_name}' removed!")

def test_connection():
    """Test GitHub connection."""
    current = get_current_git_config()
    if not current:
        print("\nNo Git configuration found!")
        return
    
    profiles = load_profiles()
    current_profile = None
    
    for name, profile in profiles.items():
        if profile['name'] == current['name'] and profile['email'] == current['email']:
            current_profile = profile
            break
    
    if not current_profile:
        print("\nNo matching profile found!")
        return
    
    if 'ssh_key' not in current_profile:
        print("\nNo SSH key found for this profile!")
        return
    
    print("\n=== Testing GitHub Connection ===")
    try:
        result = subprocess.run(
            ['ssh', '-T', f'git@github.com'],
            capture_output=True,
            text=True,
            env={'GIT_SSH_COMMAND': f'ssh -i {current_profile["ssh_key"]}'}
        )
        
        if "successfully authenticated" in result.stderr.lower():
            print("\n✓ Successfully connected to GitHub!")
            username = result.stderr.split("Hi ")[1].split("!")[0]
            print(f"GitHub username: {username}")
        else:
            print("\n✗ Connection failed!")
            print("Error:", result.stderr)
    except Exception as e:
        print("\n✗ Connection error:", str(e))

def print_status():
    """Print current status."""
    current = get_current_git_config()
    if current:
        print("\n=== Current Git Profile ===")
        print(f"Name: {current['name']}")
        print(f"Email: {current['email']}")
        
        # Try to get GitHub username
        try:
            result = subprocess.run(
                ['ssh', '-T', 'git@github.com'],
                capture_output=True,
                text=True
            )
            if "successfully authenticated" in result.stderr.lower():
                username = result.stderr.split("Hi ")[1].split("!")[0]
                print(f"GitHub Account: {username}")
        except:
            pass
    else:
        print("\nNo Git configuration found!")

def print_menu():
    """Print the main menu."""
    profiles = load_profiles()
    profile_count = len(profiles)
    
    print("\n=== Available Commands ===")
    print("1. Add New Profile")
    print("2. Switch Profile" + (f" ({profile_count} profiles)" if profile_count > 0 else ""))
    print("3. List All Profiles" + (f" ({profile_count})" if profile_count > 0 else ""))
    print("4. Remove Profile")
    print("5. Test GitHub Connection")
    print("0. Exit")

def main():
    """Main program loop."""
    while True:
        clear_screen()
        print_header()
        print_status()
        print_menu()
        
        choice = input("\nEnter your choice (0-5): ").strip()
        
        if choice == "1":
            add_profile()
        elif choice == "2":
            switch_profile()
        elif choice == "3":
            list_profiles()
        elif choice == "4":
            remove_profile()
        elif choice == "5":
            test_connection()
        elif choice == "0":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice!")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated.")
        sys.exit(0)
EOL

# Cấp quyền thực thi
chmod +x "$INSTALL_DIR/menu.py"

# Tạo symbolic link
mkdir -p "$HOME/.local/bin"
ln -sf "$INSTALL_DIR/menu.py" "$HOME/.local/bin/git-profile"

# Thêm ~/.local/bin vào PATH nếu chưa có
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    if [[ -f "$HOME/.bashrc" ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    fi
    if [[ -f "$HOME/.zshrc" ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    fi
fi

# Tạo script cập nhật
cat > "$INSTALL_DIR/update.sh" << 'EOL'
#!/bin/bash
echo "Updating Git Profile Manager..."
curl -s https://raw.githubusercontent.com/nhatpm3124/git-switch/main/menu.py -o "$HOME/.git-profile-manager/menu.py"
chmod +x "$HOME/.git-profile-manager/menu.py"
echo "✓ Update completed!"
EOL

chmod +x "$INSTALL_DIR/update.sh"
ln -sf "$INSTALL_DIR/update.sh" "$HOME/.local/bin/git-profile-update"

echo "
Git Profile Manager has been installed successfully!

Available commands:
  git-profile         : Launch Git Profile Manager
  git-profile-update : Update to latest version

Note: You may need to restart your terminal for the commands to work.

Starting Git Profile Manager..."

# Chạy chương trình
"$INSTALL_DIR/menu.py" 