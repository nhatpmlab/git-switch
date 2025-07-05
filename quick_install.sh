#!/bin/bash

# Tạo thư mục cài đặt
INSTALL_DIR="$HOME/.git-profile-manager"
mkdir -p "$INSTALL_DIR"

# Tạo file git_profile_switcher.py
cat > "$INSTALL_DIR/git_profile_switcher.py" << 'EOL'
#!/usr/bin/env python3
import json
import os
import sys
import subprocess
from pathlib import Path

CONFIG_FILE = Path.home() / '.git_profiles.json'
SSH_DIR = Path.home() / '.ssh'

def load_profiles():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)

def get_current_git_config():
    try:
        name = subprocess.check_output(['git', 'config', '--global', 'user.name']).decode().strip()
        email = subprocess.check_output(['git', 'config', '--global', 'user.email']).decode().strip()
        return {'name': name, 'email': email}
    except subprocess.CalledProcessError:
        return None

def set_git_config(name, email):
    subprocess.run(['git', 'config', '--global', 'user.name', name])
    subprocess.run(['git', 'config', '--global', 'user.email', email])

def generate_ssh_key(email, profile_name):
    if not SSH_DIR.exists():
        SSH_DIR.mkdir(mode=0o700)
    
    key_file = SSH_DIR / f"id_rsa_{profile_name}"
    if key_file.exists():
        print(f"\nSSH key cho profile '{profile_name}' đã tồn tại!")
        return str(key_file)
    
    print(f"\nĐang tạo SSH key cho profile '{profile_name}'...")
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

def show_ssh_instructions(key_file, profile_name):
    print("\n=== Hướng dẫn cài đặt SSH key cho GitHub ===")
    print("1. Copy SSH public key sau đây:")
    print("-" * 50)
    with open(f"{key_file}.pub", 'r') as f:
        print(f.read().strip())
    print("-" * 50)
    print("\n2. Truy cập GitHub -> Settings -> SSH and GPG keys -> New SSH key")
    print("3. Paste public key vào và lưu")
    print(f"\n4. Khi clone repository, sử dụng URL dạng:")
    print(f"   git@github.com-{profile_name}:username/repository.git")

def add_profile():
    profiles = load_profiles()
    
    print("\n=== Thêm Profile Git Mới ===")
    profile_name = input("Nhập tên profile: ").strip()
    
    if profile_name in profiles:
        print(f"Profile '{profile_name}' đã tồn tại!")
        return
    
    name = input("Nhập tên người dùng Git: ").strip()
    email = input("Nhập email Git: ").strip()
    
    key_file = generate_ssh_key(email, profile_name)
    
    profiles[profile_name] = {
        'name': name,
        'email': email,
        'ssh_key': key_file
    }
    
    save_profiles(profiles)
    set_git_config(name, email)
    print(f"\nĐã thêm và kích hoạt profile '{profile_name}' thành công!")
    
    show_ssh_instructions(key_file, profile_name)

def switch_profile():
    profiles = load_profiles()
    
    if not profiles:
        print("Không có profile nào! Hãy thêm profile mới trước.")
        return
    
    print("\n=== Chuyển đổi Profile Git ===")
    print("Profiles có sẵn:")
    for name in profiles:
        print(f"- {name}")
    
    profile_name = input("\nNhập tên profile muốn chuyển sang: ").strip()
    
    if profile_name not in profiles:
        print(f"Profile '{profile_name}' không tồn tại!")
        return
    
    profile = profiles[profile_name]
    set_git_config(profile['name'], profile['email'])
    print(f"\nĐã chuyển sang profile '{profile_name}' thành công!")
    
    if 'ssh_key' in profile:
        print(f"\nLưu ý: Khi clone repository mới, sử dụng URL dạng:")
        print(f"git@github.com-{profile_name}:username/repository.git")

def show_current():
    config = get_current_git_config()
    if config:
        print("\n=== Cấu hình Git Hiện tại ===")
        print(f"Tên: {config['name']}")
        print(f"Email: {config['email']}")
        
        profiles = load_profiles()
        for name, profile in profiles.items():
            if profile['name'] == config['name'] and profile['email'] == config['email']:
                print(f"Profile: {name}")
                if 'ssh_key' in profile:
                    print(f"SSH key: {profile['ssh_key']}")
                break
    else:
        print("Chưa cấu hình Git global!")

def list_profiles():
    profiles = load_profiles()
    
    if not profiles:
        print("Không có profile nào!")
        return
    
    print("\n=== Danh sách Profiles ===")
    for name, profile in profiles.items():
        print(f"\nProfile: {name}")
        print(f"Tên: {profile['name']}")
        print(f"Email: {profile['email']}")
        if 'ssh_key' in profile:
            print(f"SSH key: {profile['ssh_key']}")

def remove_profile():
    profiles = load_profiles()
    
    if not profiles:
        print("Không có profile nào để xóa!")
        return
    
    print("\n=== Xóa Profile ===")
    print("Profiles có sẵn:")
    for name in profiles:
        print(f"- {name}")
    
    profile_name = input("\nNhập tên profile muốn xóa: ").strip()
    
    if profile_name not in profiles:
        print(f"Profile '{profile_name}' không tồn tại!")
        return
    
    profile = profiles[profile_name]
    if 'ssh_key' in profile:
        try:
            os.remove(profile['ssh_key'])
            os.remove(f"{profile['ssh_key']}.pub")
            print(f"Đã xóa SSH keys của profile '{profile_name}'")
        except OSError:
            pass
    
    del profiles[profile_name]
    save_profiles(profiles)
    print(f"\nĐã xóa profile '{profile_name}' thành công!")

def print_usage():
    print("""
Sử dụng: git-profile-cli <lệnh>

Các lệnh:
  add     - Thêm profile mới (tạo SSH key)
  switch  - Chuyển đổi profile
  current - Xem profile hiện tại
  list    - Xem danh sách profiles
  remove  - Xóa profile (và SSH keys)
""")

def main():
    if len(sys.argv) != 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'add': add_profile,
        'switch': switch_profile,
        'current': show_current,
        'list': list_profiles,
        'remove': remove_profile
    }
    
    if command in commands:
        commands[command]()
    else:
        print_usage()

if __name__ == '__main__':
    main()
EOL

# Tạo file git_profile_menu.py
cat > "$INSTALL_DIR/git_profile_menu.py" << 'EOL'
#!/usr/bin/env python3
import os
import sys
from git_profile_switcher import (
    add_profile,
    switch_profile,
    show_current,
    list_profiles,
    remove_profile
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("""
╔═══════════════════════════════════════╗
║        Git Profile Manager            ║
║        ------------------            ║
║  Quản lý nhiều tài khoản Git        ║
╚═══════════════════════════════════════╝
""")

def print_menu():
    print("\nChọn một tùy chọn:")
    print("1. Thêm profile mới")
    print("2. Chuyển đổi profile")
    print("3. Xem profile hiện tại")
    print("4. Xem danh sách profiles")
    print("5. Xóa profile")
    print("0. Thoát")

def handle_choice(choice):
    clear_screen()
    
    if choice == "1":
        add_profile()
    elif choice == "2":
        switch_profile()
    elif choice == "3":
        show_current()
    elif choice == "4":
        list_profiles()
    elif choice == "5":
        remove_profile()
    elif choice == "0":
        print("\nCảm ơn bạn đã sử dụng Git Profile Manager!")
        sys.exit(0)
    else:
        print("\nLựa chọn không hợp lệ!")
    
    input("\nNhấn Enter để tiếp tục...")

def main():
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("\nNhập lựa chọn của bạn (0-5): ").strip()
        handle_choice(choice)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nĐã thoát chương trình.")
        sys.exit(0)
EOL

# Cấp quyền thực thi
chmod +x "$INSTALL_DIR/git_profile_switcher.py"
chmod +x "$INSTALL_DIR/git_profile_menu.py"

# Tạo symbolic links
ln -sf "$INSTALL_DIR/git_profile_menu.py" "$HOME/.local/bin/git-profile"
ln -sf "$INSTALL_DIR/git_profile_switcher.py" "$HOME/.local/bin/git-profile-cli"

# Thêm ~/.local/bin vào PATH nếu chưa có
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
fi

echo "
Git Profile Manager đã được cài đặt thành công!

Sử dụng:
  git-profile      : Chạy menu tương tác
  git-profile-cli  : Chạy từ command line

Ví dụ:
  git-profile                  # Mở menu
  git-profile-cli add         # Thêm profile mới
  git-profile-cli switch      # Chuyển đổi profile
  git-profile-cli current     # Xem profile hiện tại
  git-profile-cli list        # Xem danh sách profiles
  git-profile-cli remove      # Xóa profile

Lưu ý: Bạn có thể cần mở terminal mới để các lệnh hoạt động.
"

# Tự động chạy menu
echo "Đang khởi động menu..."
sleep 1
"$INSTALL_DIR/git_profile_menu.py" 