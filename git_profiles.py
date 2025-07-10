#!/usr/bin/env python3
"""
Git Profiles - CLI Interface
============================
Command-line interface for Git Profile Manager.
"""

import sys
import subprocess
from pathlib import Path
from git_profile_manager import GitProfileManager, Colors

class GitProfileCLI:
    """CLI interface for Git Profile Manager."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.manager = GitProfileManager()
    
    def print_ascii_header(self) -> None:
        """Print ASCII art header."""
        print(f"""
{Colors.GREEN}   _______ _____ _______     {Colors.CYAN}____  ____   ____  ______ _____ __    _____ _____
{Colors.GREEN}  / ____(_) __/_  __(_)    {Colors.CYAN}/ __ \/ __ \ / __ \/ ____//   _// /   / ___// ___/
{Colors.GREEN} / / __/ / /_   / /       {Colors.CYAN}/ /_/ / /_/ // / / / /_    / / / /    \__ \ \__ \ 
{Colors.GREEN}/ /_/ / / __/  / /       {Colors.CYAN}/ ____/ _, _// /_/ / __/  _/ / / /___ ___/ /___/ / 
{Colors.GREEN}\____/_/_/    /_/       {Colors.CYAN}/_/   /_/ |_|\____/_/    /___//_____//____/  
{Colors.ENDC}
{Colors.BOLD}{Colors.CYAN}                    🚀 Git Profile Manager v2.0 🚀{Colors.ENDC}
{Colors.YELLOW}              Switch between multiple GitHub accounts seamlessly{Colors.ENDC}
""")
    
    def print_status_bar(self) -> None:
        """Print current Git configuration status."""
        current = self.manager.get_current_git_config()
        if current:
            print(f"\n{Colors.BOLD}Current Profile:{Colors.ENDC}")
            print(f"{Colors.GREEN}📝 Name: {current['name']}{Colors.ENDC}")
            print(f"{Colors.BLUE}📧 Email: {current['email']}{Colors.ENDC}")
            
            # Find matching profile
            profiles = self.manager.load_profiles()
            for username, profile in profiles.items():
                if profile['name'] == current['name'] and profile['email'] == current['email']:
                    print(f"{Colors.CYAN}👤 Profile: {username}{Colors.ENDC}")
                    break
        else:
            print(f"\n{Colors.YELLOW}⚠️  No Git configuration found!{Colors.ENDC}")
    
    def print_menu(self) -> None:
        """Print the main menu."""
        profiles = self.manager.load_profiles()
        profile_count = len(profiles)
        
        print(f"\n{Colors.BOLD}Choose an option:{Colors.ENDC}")
        print(f"{Colors.GREEN}1. 📝 Add new profile{Colors.ENDC}")
        print(f"{Colors.BLUE}2. 🔄 Switch profile{Colors.ENDC}" + 
              (f" {Colors.YELLOW}({profile_count} available){Colors.ENDC}" if profile_count > 0 else ""))
        print(f"{Colors.CYAN}3. 👁️  Show current profile{Colors.ENDC}")
        print(f"{Colors.YELLOW}4. 📋 List all profiles{Colors.ENDC}" + 
              (f" {Colors.GREEN}({profile_count}){Colors.ENDC}" if profile_count > 0 else ""))
        print(f"{Colors.RED}5. 🗑️  Remove profile{Colors.ENDC}")
        print(f"{Colors.BLUE}6. 🔗 Test GitHub connection{Colors.ENDC}")
        print(f"{Colors.CYAN}7. 🌐 Update repository URL{Colors.ENDC}")
        print(f"{Colors.RED}0. 🚪 Exit{Colors.ENDC}")
    
    def add_profile(self) -> None:
        """Add a new Git profile."""
        self.manager.print_header("Add New Git Profile")
        
        # Get username
        while True:
            username = input(f"{Colors.YELLOW}Enter GitHub username: {Colors.ENDC}").strip()
            if not username:
                self.manager.print_error("Username cannot be empty!")
                continue
            if not self.manager.validate_username(username):
                self.manager.print_error("Invalid username format!")
                continue
            
            profiles = self.manager.load_profiles()
            if username in profiles:
                self.manager.print_error(f"Profile '{username}' already exists!")
                continue
            break
        
        # Get email
        while True:
            email = input(f"{Colors.BLUE}Enter Git email: {Colors.ENDC}").strip()
            if not email:
                self.manager.print_error("Email cannot be empty!")
                continue
            if not self.manager.validate_email(email):
                self.manager.print_error("Invalid email format!")
                continue
            break
        
        # Generate SSH key
        key_file = self.manager.generate_ssh_key(email, username)
        if not key_file:
            self.manager.print_error("Failed to generate SSH key!")
            return
        
        # Save profile
        profiles = self.manager.load_profiles()
        profiles[username] = {
            'name': username,
            'email': email,
            'ssh_key': key_file
        }
        
        if not self.manager.save_profiles(profiles):
            self.manager.print_error("Failed to save profile!")
            return
        
        # Set as current Git config
        if self.manager.set_git_config(username, email):
            self.manager.print_success(f"Profile '{username}' created and activated!")
        
        # Show SSH setup instructions
        if self.manager.show_ssh_instructions(key_file, username):
            # Wait for user to add key to GitHub
            input(f"\n{Colors.YELLOW}Press Enter after adding SSH key to GitHub...{Colors.ENDC}")
            
            # Test connection
            if self.manager.test_github_connection(username):
                self.manager.print_success("Setup completed successfully!")
            else:
                self.manager.print_warning("Setup completed but connection test failed.")
                print(f"{Colors.CYAN}You can test connection later using option 6.{Colors.ENDC}")
    
    def switch_profile(self) -> None:
        """Switch to a different Git profile."""
        profiles = self.manager.load_profiles()
        
        if not profiles:
            self.manager.print_error("No profiles found! Add a profile first.")
            return
        
        self.manager.print_header("Switch Git Profile")
        print(f"{Colors.YELLOW}Available profiles:{Colors.ENDC}")
        for username in profiles:
            print(f"{Colors.GREEN}• {username}{Colors.ENDC}")
        
        username = input(f"\n{Colors.CYAN}Enter profile name: {Colors.ENDC}").strip()
        
        if username not in profiles:
            self.manager.print_error(f"Profile '{username}' not found!")
            return
        
        profile = profiles[username]
        if self.manager.set_git_config(profile['name'], profile['email']):
            self.manager.print_success(f"Switched to profile '{username}'!")
            
            # Update repository URL if in a Git repo
            self.update_repository_url_for_profile(username)
            
            # Test connection
            if 'ssh_key' in profile:
                print(f"\n{Colors.CYAN}Testing GitHub connection...{Colors.ENDC}")
                self.manager.test_github_connection(username)
        else:
            self.manager.print_error("Failed to switch profile!")
    
    def show_current(self) -> None:
        """Show current Git configuration."""
        config = self.manager.get_current_git_config()
        if config:
            self.manager.print_header("Current Git Configuration")
            print(f"{Colors.GREEN}Name: {config['name']}{Colors.ENDC}")
            print(f"{Colors.BLUE}Email: {config['email']}{Colors.ENDC}")
            
            # Find matching profile
            profiles = self.manager.load_profiles()
            for username, profile in profiles.items():
                if profile['name'] == config['name'] and profile['email'] == config['email']:
                    print(f"{Colors.YELLOW}Profile: {username}{Colors.ENDC}")
                    if 'ssh_key' in profile:
                        print(f"{Colors.CYAN}SSH Key: {profile['ssh_key']}{Colors.ENDC}")
                    break
        else:
            self.manager.print_error("No Git configuration found!")
    
    def list_profiles(self) -> None:
        """List all saved profiles."""
        profiles = self.manager.load_profiles()
        
        if not profiles:
            self.manager.print_error("No profiles found!")
            return
        
        self.manager.print_header("All Profiles")
        for username, profile in profiles.items():
            print(f"\n{Colors.YELLOW}Profile: {username}{Colors.ENDC}")
            print(f"{Colors.GREEN}  Name: {profile['name']}{Colors.ENDC}")
            print(f"{Colors.BLUE}  Email: {profile['email']}{Colors.ENDC}")
            if 'ssh_key' in profile:
                print(f"{Colors.CYAN}  SSH Key: {profile['ssh_key']}{Colors.ENDC}")
    
    def remove_profile(self) -> None:
        """Remove a Git profile."""
        profiles = self.manager.load_profiles()
        
        if not profiles:
            self.manager.print_error("No profiles to remove!")
            return
        
        self.manager.print_header("Remove Profile")
        print(f"{Colors.YELLOW}Available profiles:{Colors.ENDC}")
        for username in profiles:
            print(f"{Colors.GREEN}• {username}{Colors.ENDC}")
        
        username = input(f"\n{Colors.CYAN}Enter profile name to remove: {Colors.ENDC}").strip()
        
        if username not in profiles:
            self.manager.print_error(f"Profile '{username}' not found!")
            return
        
        # Confirm deletion
        confirm = input(f"{Colors.RED}Are you sure you want to remove '{username}'? (y/N): {Colors.ENDC}").strip().lower()
        if confirm != 'y':
            print(f"{Colors.YELLOW}Removal cancelled.{Colors.ENDC}")
            return
        
        profile = profiles[username]
        
        # Check if it's the current profile
        current_config = self.manager.get_current_git_config()
        if (current_config and 
            current_config['name'] == profile['name'] and 
            current_config['email'] == profile['email']):
            
            # Clear Git global config
            try:
                subprocess.run(['git', 'config', '--global', '--unset', 'user.name'], check=True)
                subprocess.run(['git', 'config', '--global', '--unset', 'user.email'], check=True)
                self.manager.print_success("Cleared Git global configuration")
            except subprocess.CalledProcessError:
                self.manager.print_warning("Could not clear Git configuration")
        
        # Remove SSH keys
        if 'ssh_key' in profile:
            try:
                Path(profile['ssh_key']).unlink(missing_ok=True)
                Path(f"{profile['ssh_key']}.pub").unlink(missing_ok=True)
                self.manager.print_success("Removed SSH keys")
                
                # Remove from SSH config
                self.remove_from_ssh_config(username)
                
            except OSError as e:
                self.manager.print_warning(f"Could not remove SSH keys: {e}")
        
        # Remove from profiles
        del profiles[username]
        if self.manager.save_profiles(profiles):
            self.manager.print_success(f"Profile '{username}' removed successfully!")
        else:
            self.manager.print_error("Failed to save changes!")
    
    def remove_from_ssh_config(self, username: str) -> None:
        """Remove profile from SSH config."""
        config_file = Path.home() / '.ssh' / 'config'
        if not config_file.exists():
            return
        
        try:
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
                
        except IOError as e:
            self.manager.print_warning(f"Could not update SSH config: {e}")
    
    def test_connection(self) -> None:
        """Test GitHub connection for a profile."""
        profiles = self.manager.load_profiles()
        
        if not profiles:
            self.manager.print_error("No profiles found!")
            return
        
        self.manager.print_header("Test GitHub Connection")
        print(f"{Colors.YELLOW}Available profiles:{Colors.ENDC}")
        for username in profiles:
            print(f"{Colors.GREEN}• {username}{Colors.ENDC}")
        
        username = input(f"\n{Colors.CYAN}Enter profile name (or 'all' for all profiles): {Colors.ENDC}").strip()
        
        if username.lower() == 'all':
            self.manager.print_header("Testing All Connections")
            for profile_name in profiles:
                print(f"\n{Colors.YELLOW}Testing {profile_name}...{Colors.ENDC}")
                self.manager.test_github_connection(profile_name)
                print("-" * 50)
        elif username in profiles:
            self.manager.test_github_connection(username)
        else:
            self.manager.print_error(f"Profile '{username}' not found!")
    
    def update_repository_url(self) -> None:
        """Update repository URL for current profile."""
        # Check if we're in a Git repository
        try:
            subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            self.manager.print_error("Not in a Git repository!")
            return
        
        # Get current profile
        current = self.manager.get_current_git_config()
        if not current:
            self.manager.print_error("No Git configuration found!")
            return
        
        # Find profile
        profiles = self.manager.load_profiles()
        current_profile = None
        for username, profile in profiles.items():
            if profile['name'] == current['name'] and profile['email'] == current['email']:
                current_profile = username
                break
        
        if not current_profile:
            self.manager.print_error("Current Git config doesn't match any profile!")
            return
        
        self.update_repository_url_for_profile(current_profile)
    
    def update_repository_url_for_profile(self, username: str) -> bool:
        """Update repository URL for a specific profile."""
        try:
            # Check if in Git repo
            subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True)
            
            # Get current URL
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True, check=True)
            current_url = result.stdout.strip()
            
            # Parse and update URL
            if current_url.startswith('git@github.com'):
                if f'github.com-' in current_url:
                    # Replace existing profile
                    parts = current_url.split('github.com-')
                    old_profile = parts[1].split(':')[0]
                    new_url = current_url.replace(f'github.com-{old_profile}:', f'github.com-{username}:')
                else:
                    # Add profile to existing SSH URL
                    repo_part = current_url.split('github.com:')[1]
                    new_url = f"git@github.com-{username}:{repo_part}"
            elif current_url.startswith('https://github.com/'):
                # Convert HTTPS to SSH with profile
                repo_part = current_url.replace('https://github.com/', '')
                new_url = f"git@github.com-{username}:{repo_part}"
            else:
                self.manager.print_warning("Unsupported repository URL format")
                return False
            
            # Update the URL
            subprocess.run(['git', 'remote', 'set-url', 'origin', new_url], check=True)
            self.manager.print_success("Repository URL updated!")
            print(f"{Colors.BLUE}New URL: {new_url}{Colors.ENDC}")
            return True
            
        except subprocess.CalledProcessError:
            return False
    
    def handle_choice(self, choice: str) -> bool:
        """Handle menu choice. Returns False to exit."""
        self.manager.clear_screen()
        
        if choice == "1":
            self.add_profile()
        elif choice == "2":
            self.switch_profile()
        elif choice == "3":
            self.show_current()
        elif choice == "4":
            self.list_profiles()
        elif choice == "5":
            self.remove_profile()
        elif choice == "6":
            self.test_connection()
        elif choice == "7":
            self.update_repository_url()
        elif choice == "0":
            print(f"\n{Colors.GREEN}Thanks for using Git Profile Manager! 🚀{Colors.ENDC}")
            return False
        else:
            self.manager.print_error("Invalid choice!")
        
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
        return True
    
    def run(self) -> None:
        """Run the main CLI loop."""
        try:
            while True:
                self.manager.clear_screen()
                self.print_ascii_header()
                self.print_status_bar()
                self.print_menu()
                
                choice = input(f"\n{Colors.BOLD}Enter your choice (0-7): {Colors.ENDC}").strip()
                
                if not self.handle_choice(choice):
                    break
                    
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}Goodbye! 👋{Colors.ENDC}")
            sys.exit(0)

def main():
    """Main entry point."""
    cli = GitProfileCLI()
    cli.run()

if __name__ == '__main__':
    main() 