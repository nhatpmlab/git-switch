#!/usr/bin/env python3
"""
Git Profiles - CLI Interface
============================
Command-line interface for Git Profile Manager.
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

from git_profile_manager import GitProfileManager, colors

class GitProfileCLI:
    """CLI interface for Git Profile Manager."""
    
    def __init__(self) -> None:
        """Initialize the CLI."""
        self.manager = GitProfileManager()
    
    def print_ascii_header(self) -> None:
        """Print ASCII art header."""
        header = f"""
{colors.GREEN}   _______ _____ _______     {colors.CYAN}____  ____   ____  ______ _____ __    _____ _____
{colors.GREEN}  / ____(_) __/_  __(_)    {colors.CYAN}/ __ \/ __ \ / __ \/ ____//   _// /   / ___// ___/
{colors.GREEN} / / __/ / /_   / /       {colors.CYAN}/ /_/ / /_/ // / / / /_    / / / /    \__ \ \__ \ 
{colors.GREEN}/ /_/ / / __/  / /       {colors.CYAN}/ ____/ _, _// /_/ / __/  _/ / / /___ ___/ /___/ / 
{colors.GREEN}\____/_/_/    /_/       {colors.CYAN}/_/   /_/ |_|\____/_/    /___//_____//____/  
{colors.ENDC}
{colors.BOLD}{colors.CYAN}                    🚀 Git Profile Manager v2.0 🚀{colors.ENDC}
{colors.YELLOW}              Switch between multiple GitHub accounts seamlessly{colors.ENDC}
"""
        print(header)
    
    def print_status_bar(self) -> None:
        """Print current Git configuration status."""
        current = self.manager.get_current_git_config()
        
        if current:
            self._print_current_profile(current)
        else:
            print(f"\n{colors.YELLOW}⚠️  No Git configuration found!{colors.ENDC}")
    
    def _print_current_profile(self, current: Dict[str, str]) -> None:
        """Print current profile information."""
        print(f"\n{colors.BOLD}Current Profile:{colors.ENDC}")
        print(f"{colors.GREEN}📝 Name: {current['name']}{colors.ENDC}")
        print(f"{colors.BLUE}📧 Email: {current['email']}{colors.ENDC}")
        
        # Find matching profile
        profile_name = self._find_matching_profile(current)
        if profile_name:
            print(f"{colors.CYAN}👤 Profile: {profile_name}{colors.ENDC}")
    
    def _find_matching_profile(self, current: Dict[str, str]) -> Optional[str]:
        """Find the profile name that matches current Git config."""
        profiles = self.manager.load_profiles()
        for username, profile in profiles.items():
            if (profile['name'] == current['name'] and 
                profile['email'] == current['email']):
                return username
        return None
    
    def print_menu(self) -> None:
        """Print the main menu."""
        profiles = self.manager.load_profiles()
        profile_count = len(profiles)
        
        print(f"\n{colors.BOLD}Choose an option:{colors.ENDC}")
        
        menu_items = [
            ("1", "📝 Add new profile", colors.GREEN),
            ("2", "🔄 Switch profile", colors.BLUE, profile_count),
            ("3", "👁️  Show current profile", colors.CYAN),
            ("4", "📋 List all profiles", colors.YELLOW, profile_count),
            ("5", "🗑️  Remove profile", colors.RED),
            ("6", "🔗 Test GitHub connection", colors.BLUE),
            ("7", "🌐 Update repository URL", colors.CYAN),
            ("0", "🚪 Exit", colors.RED),
        ]
        
        for item in menu_items:
            self._print_menu_item(*item)
    
    def _print_menu_item(self, number: str, text: str, color: str, count: Optional[int] = None) -> None:
        """Print a single menu item."""
        count_text = f" {colors.YELLOW}({count} available){colors.ENDC}" if count else ""
        print(f"{color}{number}. {text}{colors.ENDC}{count_text}")
    
    def add_profile(self) -> None:
        """Add a new Git profile."""
        self.manager.print_header("Add New Git Profile")
        
        try:
            username = self._get_valid_username()
            email = self._get_valid_email()
            
            if not self._create_profile(username, email):
                return
            
            self._handle_ssh_setup(username, email)
            
        except KeyboardInterrupt:
            print(f"\n{colors.YELLOW}Profile creation cancelled.{colors.ENDC}")
    
    def _get_valid_username(self) -> str:
        """Get valid username from user input."""
        while True:
            username = input(f"{colors.YELLOW}Enter GitHub username: {colors.ENDC}").strip()
            
            if not username:
                self.manager.print_error("Username cannot be empty!")
                continue
            
            if not self.manager.validate_username(username):
                self.manager.print_error("Invalid username format!")
                continue
            
            if self._username_exists(username):
                self.manager.print_error(f"Profile '{username}' already exists!")
                continue
            
            return username
    
    def _get_valid_email(self) -> str:
        """Get valid email from user input."""
        while True:
            email = input(f"{colors.BLUE}Enter Git email: {colors.ENDC}").strip()
            
            if not email:
                self.manager.print_error("Email cannot be empty!")
                continue
            
            if not self.manager.validate_email(email):
                self.manager.print_error("Invalid email format!")
                continue
            
            return email
    
    def _username_exists(self, username: str) -> bool:
        """Check if username already exists."""
        profiles = self.manager.load_profiles()
        return username in profiles
    
    def _create_profile(self, username: str, email: str) -> bool:
        """Create the profile with SSH key."""
        key_file = self.manager.generate_ssh_key(email, username)
        if not key_file:
            self.manager.print_error("Failed to generate SSH key!")
            return False
        
        # Save profile
        profiles = self.manager.load_profiles()
        profiles[username] = {
            'name': username,
            'email': email,
            'ssh_key': key_file
        }
        
        if not self.manager.save_profiles(profiles):
            self.manager.print_error("Failed to save profile!")
            return False
        
        # Set as current Git config
        if self.manager.set_git_config(username, email):
            self.manager.print_success(f"Profile '{username}' created and activated!")
            return True
        
        return False
    
    def _handle_ssh_setup(self, username: str, email: str) -> None:
        """Handle SSH key setup process."""
        profiles = self.manager.load_profiles()
        key_file = profiles[username]['ssh_key']
        
        if self.manager.show_ssh_instructions(key_file, username):
            self._wait_for_ssh_setup(username)
    
    def _wait_for_ssh_setup(self, username: str) -> None:
        """Wait for user to setup SSH key on GitHub."""
        input(f"\n{colors.YELLOW}Press Enter after adding SSH key to GitHub...{colors.ENDC}")
        
        # Test connection
        if self.manager.test_github_connection(username):
            self.manager.print_success("Setup completed successfully!")
        else:
            self.manager.print_warning("Setup completed but connection test failed.")
            print(f"{colors.CYAN}You can test connection later using option 6.{colors.ENDC}")
    
    def switch_profile(self) -> None:
        """Switch to a different Git profile."""
        profiles = self.manager.load_profiles()
        
        if not profiles:
            self.manager.print_error("No profiles found! Add a profile first.")
            return
        
        self.manager.print_header("Switch Git Profile")
        self._list_available_profiles(profiles)
        
        username = input(f"\n{colors.CYAN}Enter profile name: {colors.ENDC}").strip()
        
        if not self._perform_profile_switch(username, profiles):
            return
        
        self.manager.print_success(f"Switched to profile '{username}'!")
        self._post_switch_actions(username, profiles)
    
    def _list_available_profiles(self, profiles: Dict[str, Any]) -> None:
        """List available profiles."""
        print(f"{colors.YELLOW}Available profiles:{colors.ENDC}")
        for username in profiles:
            print(f"{colors.GREEN}• {username}{colors.ENDC}")
    
    def _perform_profile_switch(self, username: str, profiles: Dict[str, Any]) -> bool:
        """Perform the actual profile switch."""
        if username not in profiles:
            self.manager.print_error(f"Profile '{username}' not found!")
            return False
        
        profile = profiles[username]
        return self.manager.set_git_config(profile['name'], profile['email'])
    
    def _post_switch_actions(self, username: str, profiles: Dict[str, Any]) -> None:
        """Perform actions after successful profile switch."""
        # Update repository URL if in a Git repo
        self.update_repository_url_for_profile(username)
        
        # Test connection
        profile = profiles[username]
        if 'ssh_key' in profile:
            print(f"\n{colors.CYAN}Testing GitHub connection...{colors.ENDC}")
            self.manager.test_github_connection(username)
    
    def show_current(self) -> None:
        """Show current Git configuration."""
        config = self.manager.get_current_git_config()
        
        if not config:
            self.manager.print_error("No Git configuration found!")
            return
        
        self.manager.print_header("Current Git Configuration")
        self._display_current_config(config)
    
    def _display_current_config(self, config: Dict[str, str]) -> None:
        """Display current configuration details."""
        print(f"{colors.GREEN}Name: {config['name']}{colors.ENDC}")
        print(f"{colors.BLUE}Email: {config['email']}{colors.ENDC}")
        
        # Find matching profile
        profiles = self.manager.load_profiles()
        matching_profile = self._find_profile_by_config(config, profiles)
        
        if matching_profile:
            username, profile = matching_profile
            print(f"{colors.YELLOW}Profile: {username}{colors.ENDC}")
            if 'ssh_key' in profile:
                print(f"{colors.CYAN}SSH Key: {profile['ssh_key']}{colors.ENDC}")
    
    def _find_profile_by_config(self, config: Dict[str, str], profiles: Dict[str, Any]) -> Optional[tuple]:
        """Find profile that matches the current config."""
        for username, profile in profiles.items():
            if (profile['name'] == config['name'] and 
                profile['email'] == config['email']):
                return username, profile
        return None
    
    def list_profiles(self) -> None:
        """List all saved profiles."""
        profiles = self.manager.load_profiles()
        
        if not profiles:
            self.manager.print_error("No profiles found!")
            return
        
        self.manager.print_header("All Profiles")
        for username, profile in profiles.items():
            self._display_profile_info(username, profile)
    
    def _display_profile_info(self, username: str, profile: Dict[str, Any]) -> None:
        """Display information for a single profile."""
        print(f"\n{colors.YELLOW}Profile: {username}{colors.ENDC}")
        print(f"{colors.GREEN}  Name: {profile['name']}{colors.ENDC}")
        print(f"{colors.BLUE}  Email: {profile['email']}{colors.ENDC}")
        if 'ssh_key' in profile:
            print(f"{colors.CYAN}  SSH Key: {profile['ssh_key']}{colors.ENDC}")
    
    def remove_profile(self) -> None:
        """Remove a Git profile."""
        profiles = self.manager.load_profiles()
        
        if not profiles:
            self.manager.print_error("No profiles to remove!")
            return
        
        self.manager.print_header("Remove Profile")
        self._list_available_profiles(profiles)
        
        username = input(f"\n{colors.CYAN}Enter profile name to remove: {colors.ENDC}").strip()
        
        if not self._validate_profile_for_removal(username, profiles):
            return
        
        if not self._confirm_removal(username):
            return
        
        profile = profiles[username]
        
        # Handle current profile cleanup
        self._cleanup_current_profile(username, profile)
        
        # Remove SSH keys and config
        self._cleanup_ssh_files(username, profile)
        
        # Remove from profiles and save
        del profiles[username]
        if self.manager.save_profiles(profiles):
            self.manager.print_success(f"Profile '{username}' removed successfully!")
        else:
            self.manager.print_error("Failed to save changes!")
    
    def _validate_profile_for_removal(self, username: str, profiles: Dict[str, Any]) -> bool:
        """Validate profile exists for removal."""
        if username not in profiles:
            self.manager.print_error(f"Profile '{username}' not found!")
            return False
        return True
    
    def _confirm_removal(self, username: str) -> bool:
        """Confirm profile removal with user."""
        confirm = input(f"{colors.RED}Are you sure you want to remove '{username}'? (y/N): {colors.ENDC}").strip().lower()
        if confirm != 'y':
            print(f"{colors.YELLOW}Removal cancelled.{colors.ENDC}")
            return False
        return True
    
    def _cleanup_current_profile(self, username: str, profile: Dict[str, Any]) -> None:
        """Clean up current Git config if it matches the profile being removed."""
        current_config = self.manager.get_current_git_config()
        
        if (current_config and 
            current_config['name'] == profile['name'] and 
            current_config['email'] == profile['email']):
            
            self._clear_git_global_config()
    
    def _clear_git_global_config(self) -> None:
        """Clear Git global configuration."""
        try:
            subprocess.run(['git', 'config', '--global', '--unset', 'user.name'], check=True)
            subprocess.run(['git', 'config', '--global', '--unset', 'user.email'], check=True)
            self.manager.print_success("Cleared Git global configuration")
        except subprocess.CalledProcessError:
            self.manager.print_warning("Could not clear Git configuration")
    
    def _cleanup_ssh_files(self, username: str, profile: Dict[str, Any]) -> None:
        """Clean up SSH keys and configuration."""
        if 'ssh_key' not in profile:
            return
        
        try:
            # Remove SSH keys
            ssh_key_path = Path(profile['ssh_key'])
            ssh_key_path.unlink(missing_ok=True)
            Path(f"{ssh_key_path}.pub").unlink(missing_ok=True)
            
            self.manager.print_success("Removed SSH keys")
            
            # Remove from SSH config
            self.remove_from_ssh_config(username)
            
        except OSError as e:
            self.manager.print_warning(f"Could not remove SSH keys: {e}")
    
    def remove_from_ssh_config(self, username: str) -> None:
        """Remove profile from SSH config."""
        config_file = Path.home() / '.ssh' / 'config'
        if not config_file.exists():
            return
        
        try:
            self._update_ssh_config_file(config_file, username)
        except IOError as e:
            self.manager.print_warning(f"Could not update SSH config: {e}")
    
    def _update_ssh_config_file(self, config_file: Path, username: str) -> None:
        """Update SSH config file by removing profile entry."""
        with open(config_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Filter out the profile's configuration
        new_lines = []
        skip = False
        
        for line in lines:
            if f"Git profile: {username}" in line:
                skip = True
                continue
            if skip and line.strip() == "":
                skip = False
                continue
            if not skip:
                new_lines.append(line)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    
    def test_connection(self) -> None:
        """Test GitHub connection for a profile."""
        profiles = self.manager.load_profiles()
        
        if not profiles:
            self.manager.print_error("No profiles found!")
            return
        
        self.manager.print_header("Test GitHub Connection")
        self._list_available_profiles(profiles)
        
        username_input = input(f"\n{colors.CYAN}Enter profile name (or 'all' for all profiles): {colors.ENDC}").strip()
        
        if username_input.lower() == 'all':
            self._test_all_connections(profiles)
        elif username_input in profiles:
            self.manager.test_github_connection(username_input)
        else:
            self.manager.print_error(f"Profile '{username_input}' not found!")
    
    def _test_all_connections(self, profiles: Dict[str, Any]) -> None:
        """Test connections for all profiles."""
        self.manager.print_header("Testing All Connections")
        for profile_name in profiles:
            print(f"\n{colors.YELLOW}Testing {profile_name}...{colors.ENDC}")
            self.manager.test_github_connection(profile_name)
            print("-" * 50)
    
    def update_repository_url(self) -> None:
        """Update repository URL for current profile."""
        if not self._is_in_git_repository():
            return
        
        current_profile = self._get_current_profile()
        if not current_profile:
            return
        
        username, profile = current_profile
        self.update_repository_url_for_profile(username)
    
    def _is_in_git_repository(self) -> bool:
        """Check if current directory is in a Git repository."""
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            self.manager.print_error("Not in a Git repository!")
            return False
    
    def _get_current_profile(self) -> Optional[Tuple[str, Dict[str, Any]]]:
        """Get current profile information."""
        current = self.manager.get_current_git_config()
        if not current:
            self.manager.print_error("No Git configuration found!")
            return None
        
        profiles = self.manager.load_profiles()
        matching_profile = self._find_profile_by_config(current, profiles)
        
        if not matching_profile:
            self.manager.print_error("Current Git config doesn't match any profile!")
            return None
        
        return matching_profile
    
    def update_repository_url_for_profile(self, username: str) -> bool:
        """Update repository URL for a specific profile."""
        try:
            current_url = self._get_current_remote_url()
            if not current_url:
                return False
            
            new_url = self._convert_url_for_profile(current_url, username)
            if not new_url:
                return False
            
            return self._update_remote_url(new_url)
            
        except subprocess.CalledProcessError:
            return False
    
    def _get_current_remote_url(self) -> Optional[str]:
        """Get current remote URL."""
        try:
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def _convert_url_for_profile(self, current_url: str, username: str) -> Optional[str]:
        """Convert URL format for specific profile."""
        if current_url.startswith('git@github.com'):
            return self._convert_ssh_url(current_url, username)
        elif current_url.startswith('https://github.com/'):
            return self._convert_https_url(current_url, username)
        else:
            self.manager.print_warning("Unsupported repository URL format")
            return None
    
    def _convert_ssh_url(self, current_url: str, username: str) -> str:
        """Convert SSH URL for profile."""
        if f'github.com-' in current_url:
            # Replace existing profile
            parts = current_url.split('github.com-')
            old_profile = parts[1].split(':')[0]
            return current_url.replace(f'github.com-{old_profile}:', f'github.com-{username}:')
        else:
            # Add profile to existing SSH URL
            repo_part = current_url.split('github.com:')[1]
            return f"git@github.com-{username}:{repo_part}"
    
    def _convert_https_url(self, current_url: str, username: str) -> str:
        """Convert HTTPS URL to SSH with profile."""
        repo_part = current_url.replace('https://github.com/', '')
        return f"git@github.com-{username}:{repo_part}"
    
    def _update_remote_url(self, new_url: str) -> bool:
        """Update the remote URL."""
        try:
            subprocess.run(['git', 'remote', 'set-url', 'origin', new_url], check=True)
            self.manager.print_success("Repository URL updated!")
            print(f"{colors.BLUE}New URL: {new_url}{colors.ENDC}")
            return True
        except subprocess.CalledProcessError:
            return False
    
    def handle_choice(self, choice: str) -> bool:
        """Handle menu choice. Returns False to exit."""
        self.manager.clear_screen()
        
        menu_actions = {
            "1": self.add_profile,
            "2": self.switch_profile,
            "3": self.show_current,
            "4": self.list_profiles,
            "5": self.remove_profile,
            "6": self.test_connection,
            "7": self.update_repository_url,
            "0": self._exit_program
        }
        
        action = menu_actions.get(choice)
        if action:
            if choice == "0":
                return action()
            else:
                action()
        else:
            self.manager.print_error("Invalid choice!")
        
        if choice != "0":
            input(f"\n{colors.YELLOW}Press Enter to continue...{colors.ENDC}")
        
        return choice != "0"
    
    def _exit_program(self) -> bool:
        """Exit the program gracefully."""
        print(f"\n{colors.GREEN}Thanks for using Git Profile Manager! 🚀{colors.ENDC}")
        return False
    
    def run(self) -> None:
        """Run the main CLI loop."""
        try:
            while True:
                self.manager.clear_screen()
                self.print_ascii_header()
                self.print_status_bar()
                self.print_menu()
                
                choice = input(f"\n{colors.BOLD}Enter your choice (0-7): {colors.ENDC}").strip()
                
                if not self.handle_choice(choice):
                    break
                    
        except KeyboardInterrupt:
            print(f"\n\n{colors.RED}Goodbye! 👋{colors.ENDC}")
            sys.exit(0)
        except Exception as e:
            self.manager.print_error(f"An unexpected error occurred: {e}")
            sys.exit(1)

def main() -> None:
    """Main entry point."""
    try:
        cli = GitProfileCLI()
        cli.run()
    except KeyboardInterrupt:
        print(f"\n{colors.RED}Goodbye! 👋{colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 