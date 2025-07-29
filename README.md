# Git Profile Manager v2.3

A powerful command-line tool for managing and switching between multiple GitHub accounts on your local machine with an elegant interface and advanced features.

## What's New in v2.3

- **Settings Menu** - Organized configuration options into a dedicated settings menu
- **Update Checker** - Automatic version checking from GitHub repository
- **Cleaner Interface** - Streamlined main menu with 4 core options
- **Enhanced Navigation** - Settings submenu with intuitive back button navigation
- **Integrated Tools** - Connection testing and URL updating within Settings

## Key Features

- **Fast Profile Switching** - Seamlessly switch between multiple GitHub accounts
- **Automatic SSH Key Management** - Generate and manage 4096-bit RSA SSH keys
- **Cross-Platform Clipboard Integration** - Auto-copy SSH keys to clipboard
- **GitHub Integration** - Automatically open GitHub SSH settings page
- **Connection Testing** - Verify GitHub connectivity with troubleshooting guidance
- **Repository URL Auto-Update** - Automatically update repository URLs when switching profiles
- **User-Friendly Interface** - Clean, colorful menu system with intuitive navigation
- **Input Validation** - Ensure data integrity with comprehensive validation

## Installation

### Quick Start (No Installation Required)

#### Linux / macOS
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/nhatpmlab/git-switch/main/run_git_profiles.sh)
```

#### Windows PowerShell
```powershell
iwr -useb https://raw.githubusercontent.com/nhatpmlab/git-switch/main/run_git_profiles.ps1 | iex
```

#### Windows Git Bash
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/nhatpmlab/git-switch/main/run_git_profiles.sh)
```

## Usage

### Direct Run Method
- **Advantages**: No installation required, automatic cleanup, always latest version
- **Considerations**: Requires internet connection for startup, slightly slower initial launch

### Permanent Installation
After installation, use these commands:
- `git-profile` - Launch the application
- `git-profile-update` - Update to the latest version

### Python Direct Execution
```bash
python3 ~/.git-profile-manager/git_profiles.py
```

## Platform Support

### Linux
- Full feature support
- ANSI color support
- Clipboard integration (xclip/xsel/wl-copy)
- Proper SSH key permissions

### macOS
- Complete feature compatibility
- Native clipboard integration (pbcopy)
- Browser integration
- SSH key permission management

### Windows
- **Windows 10+ PowerShell** - Full support
- **Git Bash** - Complete functionality
- **Command Prompt** - Basic support
- ANSI color support (Windows 10+)
- PowerShell clipboard integration
- Native Windows path handling

#### Windows Requirements
- Windows 10 or later (recommended)
- Python 3.6+
- Git for Windows
- OpenSSH Client (Windows 10+) or Git Bash

## Usage Guidelines

### Context-Aware Operation

**Within a Repository**
Switch the Git user for the current project:
```bash
cd my-project
git-profile  # Switch profile and auto-update remote URL
```

**Outside a Repository**
Manage profiles and SSH keys:
```bash
cd ~
git-profile  # Add new profiles, manage SSH keys
```

### Automatic Features

- **Repository URL Auto-Update**: When switching profiles within a Git repository, remote URLs are automatically updated
- **Smart SSH Configuration**: Automatic Host configuration for each profile
- **Connection Verification**: GitHub connectivity testing after setup
- **Clipboard Integration**: Automatic SSH key copying for easy GitHub setup
- **Cross-Platform Path Handling**: Automatic Windows/Unix path resolution

## Interface

```
   _______ _____ _______     ____  ____   ____  ______ _____ __    _____ _____
  / ____(_) __/_  __(_)    / __ \/ __ \ / __ \/ ____//   _// /   / ___// ___/
 / / __/ / /_   / /       / /_/ / /_/ // / / / /_    / / / /    \__ \ \__ \ 
/ /_/ / / __/  / /       / ____/ _, _// /_/ / __/  _/ / / /___ ___/ /___/ / 
\____/_/_/    /_/       /_/   /_/ |_|\____/_/    /___//_____//____/  

                    Git Profile Manager v2.3
              Switch between multiple GitHub accounts seamlessly


No Git configuration found!

Choose an option:
1. Add new profile
2. Switch profile
3. Remove profile
4. Settings
0. Exit

Enter your choice (0-4): 
```

## System Requirements

### Core Requirements
- **Python 3.6+** (uses Python standard library only)
- **Git**
- **Internet connection** (for downloading and GitHub connectivity)

### SSH Features
- **ssh-keygen** (OpenSSH client)
- **Linux**: Usually pre-installed
- **macOS**: Built-in
- **Windows**: OpenSSH Client or Git for Windows

### Clipboard Features
- **Linux**: xclip, xsel, or wl-copy
- **macOS**: pbcopy (built-in)
- **Windows**: PowerShell or clip (built-in)

## Improvements from v1.0

### Code Quality
- Eliminated code duplication (reduced from 3 files to 2)
- Class-based architecture with comprehensive error handling
- Type hints and consistent code style
- Cross-platform compatibility layer

### Security
- SSH key passphrase support
- Proper file permissions (Unix) and Windows compatibility
- Input validation and secure subprocess calls
- Secure temporary file handling

### User Experience
- Clean ASCII art interface with ANSI colors
- Platform-specific troubleshooting guidance
- Enhanced error messages with context
- Progress indicators and confirmation prompts

### Performance & Deployment
- Faster startup time and efficient operations
- No external dependencies (Python standard library only)
- Direct run option without installation
- Automatic cleanup and proper resource management

## Cross-Platform Compatibility

| Feature | Linux | macOS | Windows 10+ | Windows <10 |
|---------|-------|-------|-------------|-------------|
| Core functionality | ✓ | ✓ | ✓ | ✓ |
| ANSI colors | ✓ | ✓ | ✓ | ✗ |
| Clipboard copy | ✓ | ✓ | ✓ | ✓ |
| SSH key generation | ✓ | ✓ | ✓ | Limited |
| Browser integration | ✓ | ✓ | ✓ | ✓ |
| Direct run script | ✓ | ✓ | ✓ | Limited |

## License

MIT License - see LICENSE file for details.

---

**Designed for developers managing multiple GitHub accounts**

**Copyright © NHATPM.SG**
