#!/usr/bin/env python3
"""
Git Profile Manager - Enhanced Version
======================================
A powerful tool to manage multiple Git profiles with SSH key automation.
Cross-platform support: Windows, macOS, Linux
"""

import json
import os
import sys
import subprocess
import webbrowser
import getpass
import platform
import shutil
from pathlib import Path
from typing import Dict, Optional, Tuple, Any

# Constants
CONFIG_FILE = Path.home() / '.git_profiles.json'
SSH_DIR = Path.home() / '.ssh'
GITHUB_SSH_URL = 'https://github.com/settings/ssh/new'

class Colors:
    """ANSI color codes for terminal output with Windows support."""
    
    def __init__(self):
        # Enable ANSI colors on Windows
        if platform.system() == "Windows":
            try:
                # Enable ANSI escape sequences on Windows 10+
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                # Fallback for older Windows versions
                self.disable_colors()
                return
        
        self.HEADER = '\033[95m'
        self.BLUE = '\033[94m'
        self.CYAN = '\033[96m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
    
    def disable_colors(self):
        """Disable colors for compatibility."""
        self.HEADER = ''
        self.BLUE = ''
        self.CYAN = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.ENDC = ''
        self.BOLD = ''
        self.UNDERLINE = ''

# Global colors instance
Colors = Colors()

class GitProfileManager:
    """Main class for managing Git profiles with cross-platform support."""
    
    def __init__(self):
        """Initialize the Git Profile Manager."""
        self.platform = platform.system()
        self.ensure_directories()
        self.check_dependencies()
    
    def check_dependencies(self) -> None:
        """Check if required tools are available."""
        required_tools = ['git', 'ssh-keygen']
        
        for tool in required_tools:
            if not shutil.which(tool):
                self.print_error(f"Required tool '{tool}' not found!")
                if tool == 'git':
                    self.print_info("Please install Git: https://git-scm.com/downloads")
                elif tool == 'ssh-keygen':
                    if self.platform == "Windows":
                        self.print_info("Please install OpenSSH client (Windows 10+) or Git for Windows")
                    else:
                        self.print_info("Please install OpenSSH client")
                sys.exit(1)
    
    def ensure_directories(self) -> None:
        """Ensure required directories exist with proper permissions."""
        if not SSH_DIR.exists():
            SSH_DIR.mkdir(mode=0o700)
        else:
            # Ensure proper permissions
            if self.platform != "Windows":
                SSH_DIR.chmod(0o700)
    
    def load_profiles(self) -> Dict[str, Any]:
        """Load profiles from config file."""
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            self.print_error(f"Error loading profiles: {e}")
        return {}
    
    def save_profiles(self, profiles: Dict[str, Any]) -> bool:
        """Save profiles to config file."""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(profiles, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            self.print_error(f"Error saving profiles: {e}")
            return False
    
    def get_current_git_config(self) -> Optional[Dict[str, str]]:
        """Get current Git global configuration."""
        try:
            name = subprocess.check_output(
                ['git', 'config', '--global', 'user.name'], 
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
            email = subprocess.check_output(
                ['git', 'config', '--global', 'user.email'],
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
            return {'name': name, 'email': email}
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    
    def set_git_config(self, name: str, email: str) -> bool:
        """Set Git global configuration."""
        try:
            subprocess.run(['git', 'config', '--global', 'user.name', name], check=True)
            subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            self.print_error(f"Error setting Git config: {e}")
            return False
    
    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_username(self, username: str) -> bool:
        """Validate username format."""
        if not username or len(username) < 1:
            return False
        # GitHub username rules: alphanumeric and hyphens, cannot start/end with hyphen
        import re
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
        return re.match(pattern, username) is not None and len(username) <= 39
    
    def generate_ssh_key(self, email: str, username: str, use_passphrase: bool = True) -> Optional[str]:
        """Generate SSH key for the profile with Windows support."""
        key_file = SSH_DIR / f"id_rsa_{username}"
        
        if key_file.exists():
            self.print_warning(f"SSH key for profile '{username}' already exists!")
            return str(key_file)
        
        self.print_info(f"Generating SSH key for profile '{username}'...")
        
        # Ask for passphrase if needed
        passphrase = ""
        if use_passphrase:
            self.print_info("For security, we recommend using a passphrase for your SSH key.")
            choice = input(f"{Colors.YELLOW}Use passphrase? (y/N): {Colors.ENDC}").strip().lower()
            if choice == 'y':
                passphrase = getpass.getpass(f"{Colors.CYAN}Enter passphrase (leave empty for no passphrase): {Colors.ENDC}")
        
        try:
            cmd = [
                'ssh-keygen',
                '-t', 'rsa',
                '-b', '4096',
                '-C', email,
                '-f', str(key_file),
                '-N', passphrase
            ]
            
            # Windows compatibility - use shell=True if needed
            shell_needed = self.platform == "Windows"
            result = subprocess.run(cmd, capture_output=True, text=True, shell=shell_needed)
            
            if result.returncode != 0:
                self.print_error(f"Failed to generate SSH key: {result.stderr}")
                return None
            
            # Set proper permissions (skip on Windows as it uses different permission system)
            if self.platform != "Windows":
                os.chmod(key_file, 0o600)
                os.chmod(f"{key_file}.pub", 0o644)
            
            # Add to SSH config
            self.update_ssh_config(username, str(key_file))
            
            self.print_success("SSH key generated successfully!")
            return str(key_file)
            
        except (subprocess.CalledProcessError, OSError) as e:
            self.print_error(f"Error generating SSH key: {e}")
            return None
    
    def update_ssh_config(self, username: str, key_file: str) -> bool:
        """Update SSH config for the profile with Windows path handling."""
        config_file = SSH_DIR / 'config'
        
        # Windows path handling
        if self.platform == "Windows":
            key_file = key_file.replace('\\', '/')
        
        config_content = f"""
# Git profile: {username}
Host github.com-{username}
    HostName github.com
    User git
    IdentityFile {key_file}
    IdentitiesOnly yes

"""
        
        try:
            with open(config_file, 'a', encoding='utf-8') as f:
                f.write(config_content)
            return True
        except IOError as e:
            self.print_error(f"Error updating SSH config: {e}")
            return False
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard with enhanced Windows support."""
        try:
            if self.platform == 'Darwin':  # macOS
                p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                p.communicate(text.encode('utf-8'))
                return True
            elif self.platform == 'Windows':  # Windows
                try:
                    # Try PowerShell first (more reliable)
                    cmd = ['powershell', '-command', f'"{text}" | Set-Clipboard']
                    result = subprocess.run(cmd, capture_output=True, shell=True)
                    if result.returncode == 0:
                        return True
                    
                    # Fallback to clip command
                    p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
                    p.communicate(text.encode('utf-8'))
                    return True
                except:
                    return False
            else:  # Linux
                # Try multiple clipboard tools
                for cmd in [
                    ['xclip', '-selection', 'clipboard'],
                    ['xsel', '--clipboard', '--input'],
                    ['wl-copy']  # Wayland
                ]:
                    try:
                        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                        p.communicate(text.encode('utf-8'))
                        return True
                    except FileNotFoundError:
                        continue
                return False
        except Exception:
            return False
    
    def open_github_ssh_settings(self) -> bool:
        """Open GitHub SSH settings page with enhanced Windows support."""
        try:
            if webbrowser.open(GITHUB_SSH_URL):
                return True
            
            # Fallback to system commands
            if self.platform == 'Darwin':
                subprocess.run(['open', GITHUB_SSH_URL])
                return True
            elif self.platform == 'Windows':
                subprocess.run(['start', GITHUB_SSH_URL], shell=True)
                return True
            else:
                subprocess.run(['xdg-open', GITHUB_SSH_URL])
                return True
        except Exception:
            return False
    
    def show_ssh_instructions(self, key_file: str, username: str) -> bool:
        """Show instructions for setting up SSH key with GitHub."""
        self.print_header("SSH Key Setup Instructions")
        
        # Read and display public key
        try:
            with open(f"{key_file}.pub", 'r', encoding='utf-8') as f:
                public_key = f.read().strip()
            
            print(f"{Colors.YELLOW}1. Your SSH public key:{Colors.ENDC}")
            print(f"{Colors.CYAN}{'-' * 50}{Colors.ENDC}")
            print(f"{Colors.GREEN}{public_key}{Colors.ENDC}")
            print(f"{Colors.CYAN}{'-' * 50}{Colors.ENDC}")
            
            # Copy to clipboard
            if self.copy_to_clipboard(public_key):
                self.print_success("SSH key copied to clipboard!")
                if self.platform == "Windows":
                    print(f"{Colors.YELLOW}You can paste it with Ctrl+V{Colors.ENDC}")
                else:
                    print(f"{Colors.YELLOW}You can paste it with Ctrl+V (Linux) or Cmd+V (macOS){Colors.ENDC}")
            else:
                self.print_warning("Could not copy automatically. Please copy manually.")
            
            # Open GitHub page
            print(f"\n{Colors.BLUE}Opening GitHub SSH settings page...{Colors.ENDC}")
            if self.open_github_ssh_settings():
                self.print_success("GitHub page opened successfully!")
            else:
                self.print_warning("Could not open browser automatically.")
                print(f"Please visit: {GITHUB_SSH_URL}")
            
            # Instructions
            print(f"\n{Colors.BOLD}Setup Instructions:{Colors.ENDC}")
            print(f"{Colors.GREEN}1. Set title: '{username} - Git Profile Manager'{Colors.ENDC}")
            print(f"{Colors.YELLOW}2. Paste the SSH key into the 'Key' field{Colors.ENDC}")
            print(f"{Colors.CYAN}3. Click 'Add SSH key' to save{Colors.ENDC}")
            
            print(f"\n{Colors.BOLD}Repository URL format:{Colors.ENDC}")
            print(f"{Colors.GREEN}git@github.com-{username}:username/repository.git{Colors.ENDC}")
            
            return True
            
        except IOError as e:
            self.print_error(f"Error reading SSH key: {e}")
            return False
    
    def test_github_connection(self, username: str) -> bool:
        """Test SSH connection to GitHub for a specific profile with Windows support."""
        profiles = self.load_profiles()
        
        if username not in profiles:
            self.print_error(f"Profile '{username}' not found!")
            return False
        
        profile = profiles[username]
        if 'ssh_key' not in profile:
            self.print_error(f"Profile '{username}' has no SSH key!")
            return False
        
        self.print_info(f"Testing GitHub connection for profile '{username}'...")
        
        try:
            # Add GitHub to known_hosts if not present
            self.add_github_to_known_hosts()
            
            # Test connection with proper Windows support
            cmd = ['ssh', '-T', f'git@github.com-{username}']
            env = os.environ.copy()
            
            # Windows-specific SSH command setup
            ssh_cmd = f'ssh -i "{profile["ssh_key"]}" -o StrictHostKeyChecking=no'
            if self.platform == "Windows":
                ssh_cmd = ssh_cmd.replace('\\', '/')
            env['GIT_SSH_COMMAND'] = ssh_cmd
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                env=env, 
                timeout=15,
                shell=self.platform == "Windows"
            )
            
            if "successfully authenticated" in result.stderr.lower():
                self.print_success("GitHub connection successful!")
                print(f"{Colors.BLUE}Profile: {username}{Colors.ENDC}")
                print(f"{Colors.GREEN}Name: {profile['name']}{Colors.ENDC}")
                print(f"{Colors.YELLOW}Email: {profile['email']}{Colors.ENDC}")
                return True
            else:
                self.print_error("GitHub connection failed!")
                print(f"{Colors.YELLOW}Error: {result.stderr}{Colors.ENDC}")
                self.print_troubleshooting_tips()
                return False
                
        except subprocess.TimeoutExpired:
            self.print_error("Connection timeout! Check your internet connection.")
            return False
        except Exception as e:
            self.print_error(f"Error testing connection: {e}")
            return False
    
    def add_github_to_known_hosts(self) -> None:
        """Add GitHub to SSH known_hosts with Windows support."""
        known_hosts = SSH_DIR / 'known_hosts'
        try:
            # Check if GitHub is already in known_hosts
            if known_hosts.exists():
                with open(known_hosts, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'github.com' in content:
                    return
            
            # Add GitHub host key
            cmd = ['ssh-keyscan', '-t', 'rsa', 'github.com']
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                shell=self.platform == "Windows"
            )
            
            if result.returncode == 0 and result.stdout:
                with open(known_hosts, 'a', encoding='utf-8') as f:
                    f.write(result.stdout)
                    
        except (IOError, subprocess.CalledProcessError):
            pass
    
    def print_troubleshooting_tips(self) -> None:
        """Print troubleshooting tips with platform-specific advice."""
        print(f"\n{Colors.BOLD}Troubleshooting:{Colors.ENDC}")
        print(f"{Colors.CYAN}1. Ensure SSH key is added to GitHub{Colors.ENDC}")
        
        if self.platform == "Windows":
            print(f"{Colors.CYAN}2. Ensure OpenSSH client is installed (Windows 10+){Colors.ENDC}")
            print(f"{Colors.CYAN}3. Try running from Git Bash if using Git for Windows{Colors.ENDC}")
        else:
            print(f"{Colors.CYAN}2. Check SSH key permissions (chmod 600){Colors.ENDC}")
        
        print(f"{Colors.CYAN}3. Verify SSH config is correct{Colors.ENDC}")
        print(f"{Colors.CYAN}4. Test with: ssh -T git@github.com-{'{username}'}{Colors.ENDC}")
    
    # Utility methods for consistent output
    def clear_screen(self) -> None:
        """Clear the terminal screen with cross-platform support."""
        if self.platform == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def print_header(self, title: str) -> None:
        """Print a formatted header."""
        print(f"\n{Colors.BOLD}=== {title} ==={Colors.ENDC}")
    
    def print_success(self, message: str) -> None:
        """Print success message."""
        print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")
    
    def print_error(self, message: str) -> None:
        """Print error message."""
        print(f"{Colors.RED}❌ {message}{Colors.ENDC}")
    
    def print_warning(self, message: str) -> None:
        """Print warning message."""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")
    
    def print_info(self, message: str) -> None:
        """Print info message."""
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.ENDC}")

# Export the main class
__all__ = ['GitProfileManager', 'Colors'] 