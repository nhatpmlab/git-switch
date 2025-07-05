#!/usr/bin/env python3
import json
import os
import sys
import subprocess
import webbrowser
import pyperclip  # Thêm thư viện để copy vào clipboard
from pathlib import Path

CONFIG_FILE = Path.home() / '.git_profiles.json'
SSH_DIR = Path.home() / '.ssh'

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
    except subprocess.CalledProcessError:
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
        print(f"\nSSH key cho profile '{profile_name}' đã tồn tại!")
        return str(key_file)
    
    print(f"\nĐang tạo SSH key cho profile '{profile_name}'...")
    subprocess.run([
        'ssh-keygen',
        '-t', 'rsa',
        '-b', '4096',
        '-C', email,
        '-f', str(key_file),
        '-N', ''  # Empty passphrase
    ])
    
    # Add to SSH config
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
    """Mở trang cài đặt SSH key của GitHub."""
    webbrowser.open('https://github.com/settings/ssh/new')

def copy_to_clipboard(text):
    """Copy text vào clipboard."""
    try:
        pyperclip.copy(text)
        return True
    except:
        return False

def show_ssh_instructions(key_file, profile_name):
    """Show instructions for setting up SSH key with GitHub."""
    print("\n=== Hướng dẫn cài đặt SSH key cho GitHub ===")
    print("1. Copy SSH public key sau đây:")
    print("-" * 50)
    
    # Đọc và copy public key
    with open(f"{key_file}.pub", 'r') as f:
        public_key = f.read().strip()
        print(public_key)
        if copy_to_clipboard(public_key):
            print("\n✅ Đã copy public key vào clipboard!")
        else:
            print("\n❌ Không thể copy vào clipboard. Vui lòng copy thủ công.")
    
    print("-" * 50)
    
    # Mở trang GitHub SSH settings
    print("\nĐang mở trang cài đặt SSH key của GitHub...")
    webbrowser.open('https://github.com/settings/ssh/new')
    
    print("\nHướng dẫn thêm SSH key:")
    print(f"1. Đặt tiêu đề: '{profile_name} - Git Profile Manager'")
    print("2. Paste public key vào ô 'Key'")
    print("3. Nhấn 'Add SSH key' để lưu")
    
    print(f"\nSau khi thêm key, khi clone repository, sử dụng URL dạng:")
    print(f"   git@github.com-{profile_name}:username/repository.git")
    print("\nHoặc cập nhật remote URL của repository hiện tại:")
    print(f"   git remote set-url origin git@github.com-{profile_name}:username/repository.git")
    
    # Chờ người dùng xác nhận
    input("\nSau khi thêm SSH key vào GitHub, nhấn Enter để kiểm tra kết nối...")
    
    # Kiểm tra kết nối
    print("\nĐang kiểm tra kết nối GitHub...")
    try:
        result = subprocess.run(
            ['ssh', '-T', f'git@github.com-{profile_name}'],
            capture_output=True,
            text=True,
            env={'GIT_SSH_COMMAND': f'ssh -i {key_file}'}
        )
        
        if "successfully authenticated" in result.stderr.lower():
            print("\n✅ Kết nối thành công với GitHub!")
            print(f"Profile: {profile_name}")
            print(f"SSH key: {key_file}")
            return True
        else:
            print("\n❌ Kết nối thất bại!")
            print("Lỗi:", result.stderr)
            print("\nHãy kiểm tra:")
            print("1. SSH key đã được thêm vào GitHub chưa?")
            print("2. SSH key có quyền truy cập đúng không? (chmod 600)")
            print("3. Cấu hình SSH config có đúng không?")
            return False
    except Exception as e:
        print("\n❌ Lỗi khi kiểm tra kết nối:", str(e))
        return False

def add_profile():
    """Add a new Git profile."""
    profiles = load_profiles()
    
    print("\n=== Thêm Profile Git Mới ===")
    profile_name = input("Nhập tên profile: ").strip()
    
    if profile_name in profiles:
        print(f"Profile '{profile_name}' đã tồn tại!")
        return
    
    name = input("Nhập tên người dùng Git: ").strip()
    email = input("Nhập email Git: ").strip()
    
    # Generate SSH key
    key_file = generate_ssh_key(email, profile_name)
    
    profiles[profile_name] = {
        'name': name,
        'email': email,
        'ssh_key': key_file
    }
    
    save_profiles(profiles)
    set_git_config(name, email)
    print(f"\nĐã thêm và kích hoạt profile '{profile_name}' thành công!")
    
    # Show SSH setup instructions and open browser
    show_ssh_instructions(key_file, profile_name)
    
    # Chờ người dùng xác nhận đã thêm key
    input("\nNhấn Enter sau khi đã thêm SSH key vào GitHub...")
    
    # Kiểm tra kết nối
    print("\nĐang kiểm tra kết nối GitHub...")
    try:
        result = subprocess.run(
            ['ssh', '-T', f'git@github.com-{profile_name}'],
            capture_output=True,
            text=True,
            env={'GIT_SSH_COMMAND': f'ssh -i {key_file}'}
        )
        
        if "successfully authenticated" in result.stderr.lower():
            print("\n✅ Kết nối thành công với GitHub!")
        else:
            print("\n❌ Kết nối thất bại!")
            print("Lỗi:", result.stderr)
    except Exception as e:
        print("\n❌ Lỗi khi kiểm tra kết nối:", str(e))

def switch_profile():
    """Switch to a different Git profile."""
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
    
    # Show SSH key reminder
    if 'ssh_key' in profile:
        print(f"\nLưu ý: Khi clone repository mới, sử dụng URL dạng:")
        print(f"git@github.com-{profile_name}:username/repository.git")

def show_current():
    """Show current Git configuration."""
    config = get_current_git_config()
    if config:
        print("\n=== Cấu hình Git Hiện tại ===")
        print(f"Tên: {config['name']}")
        print(f"Email: {config['email']}")
        
        # Try to find matching profile
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
    """List all saved profiles."""
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
    """Remove a Git profile."""
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
    
    # Kiểm tra xem profile này có đang được sử dụng không
    current_config = get_current_git_config()
    profile = profiles[profile_name]
    
    if (current_config and 
        current_config['name'] == profile['name'] and 
        current_config['email'] == profile['email']):
        # Xóa cấu hình Git global
        print("\nĐang xóa cấu hình Git global...")
        try:
            subprocess.run(['git', 'config', '--global', '--unset', 'user.name'])
            subprocess.run(['git', 'config', '--global', '--unset', 'user.email'])
            print("✅ Đã xóa cấu hình Git global")
        except subprocess.CalledProcessError as e:
            print("❌ Lỗi khi xóa cấu hình Git:", str(e))
    
    # Remove SSH keys if they exist
    if 'ssh_key' in profile:
        try:
            os.remove(profile['ssh_key'])
            os.remove(f"{profile['ssh_key']}.pub")
            print(f"✅ Đã xóa SSH keys của profile '{profile_name}'")
            
            # Xóa cấu hình SSH
            config_file = SSH_DIR / 'config'
            if config_file.exists():
                with open(config_file, 'r') as f:
                    lines = f.readlines()
                
                # Tìm và xóa phần cấu hình của profile này
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
                
                # Ghi lại file config
                with open(config_file, 'w') as f:
                    f.writelines(new_lines)
                print(f"✅ Đã xóa cấu hình SSH của profile '{profile_name}'")
        except OSError:
            pass
    
    del profiles[profile_name]
    save_profiles(profiles)
    print(f"\n✅ Đã xóa profile '{profile_name}' thành công!")
    
    # Hiển thị hướng dẫn
    print("\nLưu ý:")
    print("1. Nếu bạn muốn sử dụng Git, hãy chuyển sang một profile khác")
    print("2. Hoặc cấu hình Git global mới bằng lệnh:")
    print("   git config --global user.name \"Tên của bạn\"")
    print("   git config --global user.email \"email@example.com\"")
    
    # Hiển thị các profiles còn lại
    if profiles:
        print("\nCác profiles còn lại:")
        for name in profiles:
            print(f"- {name}")
        print("\nBạn có thể chuyển sang một trong các profiles trên.")
    else:
        print("\nKhông còn profile nào. Hãy tạo profile mới để sử dụng.")

def test_github_connection(profile_name):
    """Test SSH connection to GitHub for a specific profile."""
    profiles = load_profiles()
    if profile_name not in profiles:
        print(f"\nProfile '{profile_name}' không tồn tại!")
        return False
    
    profile = profiles[profile_name]
    if 'ssh_key' not in profile:
        print(f"\nProfile '{profile_name}' không có SSH key!")
        return False
    
    print(f"\n=== Kiểm tra kết nối GitHub cho profile '{profile_name}' ===")
    try:
        # Test SSH connection
        result = subprocess.run(
            ['ssh', '-T', f'git@github.com-{profile_name}'],
            capture_output=True,
            text=True,
            env={'GIT_SSH_COMMAND': f'ssh -i {profile["ssh_key"]}'}
        )
        
        # GitHub's success message contains "You've successfully authenticated"
        if "successfully authenticated" in result.stderr.lower():
            print("\n✅ Kết nối thành công với GitHub!")
            print(f"Profile: {profile_name}")
            print(f"User: {profile['name']}")
            print(f"Email: {profile['email']}")
            print(f"SSH key: {profile['ssh_key']}")
            return True
        else:
            print("\n❌ Kết nối thất bại!")
            print("Lỗi:", result.stderr)
            print("\nHãy kiểm tra:")
            print("1. SSH key đã được thêm vào GitHub chưa?")
            print("2. SSH key có quyền truy cập đúng không? (chmod 600)")
            print("3. Cấu hình SSH config có đúng không?")
            return False
            
    except subprocess.CalledProcessError as e:
        print("\n❌ Lỗi khi kiểm tra kết nối:")
        print(e.stderr if e.stderr else str(e))
        return False
    except Exception as e:
        print("\n❌ Lỗi không xác định:", str(e))
        return False

def test_all_connections():
    """Test GitHub connection for all profiles."""
    profiles = load_profiles()
    if not profiles:
        print("\nKhông có profile nào để kiểm tra!")
        return
    
    print("\n=== Kiểm tra kết nối cho tất cả profiles ===")
    for profile_name in profiles:
        test_github_connection(profile_name)
        print("\n" + "-" * 50)

def print_usage():
    """Print usage instructions."""
    print("""
Sử dụng: python git_profile_switcher.py <lệnh>

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