#!/bin/bash

# ASCII art header
echo '
   _______ _____ _______     ____  ____  ____  ______ _____ __    _____
  / ____(_) __//_  __(_)   / __ \/ __ \/ __ \/ ____//   _// /   / ___/
 / / __/ / /_   / /  _    / /_/ / /_/ / / / / /_    / / / /    \__ \ 
/ /_/ / / __/  / /  (_)  / ____/ _, _/ /_/ / __/  _/ / / /___ ___/ / 
\____/_/_/    /_/  (_)  /_/   /_/ |_|\____/_/    /___//_____//____/  
'

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Print step
print_step() {
    echo -e "\n${BLUE}:: $1 ::${NC}"
}

# Print success
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Print error
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Print info
print_info() {
    echo -e "${YELLOW}$1${NC}"
}

# Get latest version from GitHub
get_latest_version() {
    curl -s https://api.github.com/repos/nhatpm3124/git-switch/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'
}

# Create installation directory
print_step "Creating installation directory"
INSTALL_DIR="$HOME/.git-profile-manager"
mkdir -p "$INSTALL_DIR"
print_success "Directory created: $INSTALL_DIR"

# Get latest version
print_step "Checking latest version"
VERSION=$(get_latest_version)
if [ -z "$VERSION" ]; then
    VERSION="main"
    print_info "Using default version: main"
else
    print_success "Latest version: $VERSION"
fi

# Download script
print_step "Downloading Git Profile Manager"
if [ "$VERSION" = "main" ]; then
    DOWNLOAD_URL="https://raw.githubusercontent.com/nhatpm3124/git-switch/main/menu.py"
else
    DOWNLOAD_URL="https://raw.githubusercontent.com/nhatpm3124/git-switch/$VERSION/menu.py"
fi

curl -s "$DOWNLOAD_URL" -o "$INSTALL_DIR/menu.py"
if [ $? -eq 0 ]; then
    print_success "Download completed"
else
    print_error "Download failed"
    exit 1
fi

# Set permissions
print_step "Setting permissions"
chmod +x "$INSTALL_DIR/menu.py"
print_success "Permissions set"

# Create symbolic link
print_step "Creating command link"
mkdir -p "$HOME/.local/bin"
ln -sf "$INSTALL_DIR/menu.py" "$HOME/.local/bin/git-profile"
print_success "Command 'git-profile' created"

# Update PATH
print_step "Updating PATH"
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    if [[ -f "$HOME/.bashrc" ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        print_success "Updated .bashrc"
    fi
    if [[ -f "$HOME/.zshrc" ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
        print_success "Updated .zshrc"
    fi
    print_info "Please restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
else
    print_success "PATH already configured"
fi

# Create update script
print_step "Creating update command"
cat > "$INSTALL_DIR/update.sh" << 'EOL'
#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get latest version
echo -e "\n${BLUE}:: Checking for updates ::${NC}"
VERSION=$(curl -s https://api.github.com/repos/nhatpm3124/git-switch/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

if [ -z "$VERSION" ]; then
    VERSION="main"
    echo -e "${YELLOW}Using default version: main${NC}"
else
    echo -e "${GREEN}Latest version: $VERSION${NC}"
fi

# Download latest version
echo -e "\n${BLUE}:: Downloading latest version ::${NC}"
if [ "$VERSION" = "main" ]; then
    DOWNLOAD_URL="https://raw.githubusercontent.com/nhatpm3124/git-switch/main/menu.py"
else
    DOWNLOAD_URL="https://raw.githubusercontent.com/nhatpm3124/git-switch/$VERSION/menu.py"
fi

curl -s "$DOWNLOAD_URL" -o "$HOME/.git-profile-manager/menu.py"
if [ $? -eq 0 ]; then
    chmod +x "$HOME/.git-profile-manager/menu.py"
    echo -e "${GREEN}✓ Update completed${NC}"
else
    echo -e "${RED}✗ Update failed${NC}"
fi
EOL

chmod +x "$INSTALL_DIR/update.sh"
ln -sf "$INSTALL_DIR/update.sh" "$HOME/.local/bin/git-profile-update"
print_success "Command 'git-profile-update' created"

# Print completion message
echo -e "\n${GREEN}✓ Installation completed successfully!${NC}"
if [ "$VERSION" = "main" ]; then
    print_info "Installed version: main (development)"
else
    print_info "Installed version: $VERSION"
fi

echo -e "\n${YELLOW}Available commands:${NC}"
echo -e "${CYAN}git-profile${NC}         - Launch Git Profile Manager"
echo -e "${CYAN}git-profile-update${NC}  - Update to latest version"

# Start the program
print_step "Starting Git Profile Manager"
"$INSTALL_DIR/menu.py" 