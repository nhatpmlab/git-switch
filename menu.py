#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path
import json
import webbrowser

# Cấu hình
CONFIG_FILE = Path.home() / '.git_profiles.json'
SSH_DIR = Path.home() / '.ssh'

# Màu sắc ANSI
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print(f"{Colors.CYAN}╔═══════════════════════════════════════╗{Colors.ENDC}")
    print(f"{Colors.CYAN}║{Colors.BOLD}        Git Profile Manager            {Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}")
    print(f"{Colors.CYAN}║{Colors.YELLOW}        ------------------            {Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}")
    print(f"{Colors.CYAN}║{Colors.GREEN}  Quản lý nhiều tài khoản Git        {Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}")
    print(f"{Colors.CYAN}╚═══════════════════════════════════════╝{Colors.ENDC}")

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
        print(f"\n{Colors.YELLOW}SSH key cho profile '{profile_name}' đã tồn tại!{Colors.ENDC}")
        return str(key_file)
    
    print(f"\n{Colors.CYAN}Đang tạo SSH key cho profile '{profile_name}'...{Colors.ENDC}")
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
    """Mở trang cài đặt SSH key của GitHub."""
    try:
        # Thử mở bằng webbrowser
        if not webbrowser.open('https://github.com/settings/ssh/new'):
            # Nếu không mở được, thử các lệnh hệ thống
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', 'https://github.com/settings/ssh/new'])
            elif sys.platform == 'win32':  # Windows
                subprocess.run(['start', 'https://github.com/settings/ssh/new'], shell=True)
            else:  # Linux và các hệ điều hành khác
                subprocess.run(['xdg-open', 'https://github.com/settings/ssh/new'])
    except Exception as e:
        print(f"\n{Colors.RED}❌ Không thể mở trình duyệt tự động.{Colors.ENDC}")
        print(f"{Colors.YELLOW}Vui lòng truy cập URL sau:{Colors.ENDC}")
        print("https://github.com/settings/ssh/new")

def copy_to_clipboard(text):
    """Copy text to clipboard using system commands."""
    try:
        if sys.platform == 'darwin':  # macOS
            p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            p.communicate(text.encode())
            return True
        elif sys.platform == 'win32':  # Windows
            p = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
            p.communicate(text.encode())
            return True
        else:  # Linux
            p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            p.communicate(text.encode())
            return True
    except:
        return False

def show_ssh_instructions(key_file, profile_name):
    """Show instructions for setting up SSH key with GitHub."""
    print(f"\n{Colors.BOLD}=== Hướng dẫn cài đặt SSH key cho GitHub ==={Colors.ENDC}")
    print(f"{Colors.YELLOW}1. Copy SSH public key sau đây:{Colors.ENDC}")
    print(f"{Colors.CYAN}" + "-" * 50 + Colors.ENDC)
    
    # Đọc và copy public key
    with open(f"{key_file}.pub", 'r') as f:
        public_key = f.read().strip()
        print(f"{Colors.GREEN}{public_key}{Colors.ENDC}")
        
        # Tự động copy vào clipboard
        if copy_to_clipboard(public_key):
            print(f"\n{Colors.GREEN}✅ Đã tự động copy SSH key vào clipboard!{Colors.ENDC}")
            print(f"{Colors.YELLOW}Bạn có thể dùng Ctrl+V (Windows/Linux) hoặc Command+V (macOS) để paste{Colors.ENDC}")
        else:
            print(f"\n{Colors.RED}❌ Không thể copy tự động. Vui lòng copy thủ công.{Colors.ENDC}")
    
    print(f"{Colors.CYAN}" + "-" * 50 + Colors.ENDC)
    
    # Mở trang GitHub SSH settings
    print(f"\n{Colors.BLUE}Đang mở trang cài đặt SSH key của GitHub...{Colors.ENDC}")
    open_github_ssh_settings()
    
    print(f"\n{Colors.BOLD}Hướng dẫn thêm SSH key:{Colors.ENDC}")
    print(f"{Colors.GREEN}1. Đặt tiêu đề: '{profile_name} - Git Profile Manager'{Colors.ENDC}")
    print(f"{Colors.YELLOW}2. Paste SSH key vào ô 'Key' (đã được copy vào clipboard){Colors.ENDC}")
    print(f"{Colors.CYAN}3. Nhấn 'Add SSH key' để lưu{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Sau khi thêm key, khi clone repository, sử dụng URL dạng:{Colors.ENDC}")
    print(f"{Colors.GREEN}   git@github.com-{profile_name}:username/repository.git{Colors.ENDC}")
    
    # Chờ người dùng xác nhận
    input(f"\n{Colors.YELLOW}Sau khi thêm SSH key vào GitHub, nhấn Enter để kiểm tra kết nối...{Colors.ENDC}")
    
    # Kiểm tra kết nối
    print(f"\n{Colors.CYAN}Đang kiểm tra kết nối GitHub...{Colors.ENDC}")
    try:
        result = subprocess.run(
            ['ssh', '-T', f'git@github.com-{profile_name}'],
            capture_output=True,
            text=True,
            env={'GIT_SSH_COMMAND': f'ssh -i {key_file}'}
        )
        
        if "successfully authenticated" in result.stderr.lower():
            print(f"\n{Colors.GREEN}✅ Kết nối thành công với GitHub!{Colors.ENDC}")
            print(f"{Colors.BLUE}Profile: {profile_name}{Colors.ENDC}")
            print(f"{Colors.CYAN}SSH key: {key_file}{Colors.ENDC}")
            return True
        else:
            print(f"\n{Colors.RED}❌ Kết nối thất bại!{Colors.ENDC}")
            print(f"{Colors.YELLOW}Lỗi: {result.stderr}{Colors.ENDC}")
            print(f"\n{Colors.BOLD}Hãy kiểm tra:{Colors.ENDC}")
            print(f"{Colors.CYAN}1. SSH key đã được thêm vào GitHub chưa?{Colors.ENDC}")
            print(f"{Colors.CYAN}2. SSH key có quyền truy cập đúng không? (chmod 600){Colors.ENDC}")
            print(f"{Colors.CYAN}3. Cấu hình SSH config có đúng không?{Colors.ENDC}")
            return False
    except Exception as e:
        print(f"\n{Colors.RED}❌ Lỗi khi kiểm tra kết nối: {str(e)}{Colors.ENDC}")
        return False

def add_profile():
    """Add a new Git profile."""
    profiles = load_profiles()
    
    print(f"\n{Colors.BOLD}=== Thêm Profile Git Mới ==={Colors.ENDC}")
    username = input(f"{Colors.YELLOW}Nhập username GitHub: {Colors.ENDC}").strip()
    
    if username in profiles:
        print(f"\n{Colors.RED}Profile '{username}' đã tồn tại!{Colors.ENDC}")
        return
    
    email = input(f"{Colors.BLUE}Nhập email Git: {Colors.ENDC}").strip()
    
    # Generate SSH key
    key_file = generate_ssh_key(email, username)
    
    profiles[username] = {
        'name': username,
        'email': email,
        'ssh_key': key_file
    }
    
    save_profiles(profiles)
    set_git_config(username, email)
    print(f"\n{Colors.GREEN}✅ Đã thêm và kích hoạt profile '{username}' thành công!{Colors.ENDC}")
    
    # Show SSH setup instructions
    show_ssh_instructions(key_file, username)

def update_repository_url_for_profile(profile_name):
    """Update repository URL for a specific profile."""
    # Kiểm tra xem có phải là Git repository không
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return
    
    # Lấy URL hiện tại
    try:
        current_url = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode().strip()
    except:
        return
    
    # Phân tích URL hiện tại
    if current_url.startswith('git@github.com'):
        # URL SSH
        if f'github.com-' in current_url:
            # URL đã có profile, thay thế profile
            parts = current_url.split('github.com-')
            old_profile = parts[1].split(':')[0]
            new_url = current_url.replace(f'github.com-{old_profile}:', f'github.com-{profile_name}:')
        else:
            # URL chưa có profile
            repo_part = current_url.split('github.com:')[1]
            new_url = f"git@github.com-{profile_name}:{repo_part}"
    elif current_url.startswith('https://github.com/'):
        # URL HTTPS
        repo_part = current_url.replace('https://github.com/', '')
        new_url = f"git@github.com-{profile_name}:{repo_part}"
    else:
        return
    
    # Cập nhật URL
    try:
        subprocess.run(['git', 'remote', 'set-url', 'origin', new_url], check=True, capture_output=True)
        print(f"\n{Colors.GREEN}✅ Đã cập nhật URL repository:{Colors.ENDC}")
        print(f"{Colors.BLUE}{new_url}{Colors.ENDC}")
    except:
        pass

def switch_profile():
    """Switch to a different Git profile."""
    profiles = load_profiles()
    
    if not profiles:
        print(f"\n{Colors.RED}Không có profile nào! Hãy thêm profile mới trước.{Colors.ENDC}")
        return
    
    print(f"\n{Colors.BOLD}=== Chuyển đổi Profile Git ==={Colors.ENDC}")
    print(f"{Colors.YELLOW}Profiles có sẵn:{Colors.ENDC}")
    for name in profiles:
        print(f"{Colors.GREEN}- {name}{Colors.ENDC}")
    
    profile_name = input(f"\n{Colors.CYAN}Nhập tên profile muốn chuyển sang: {Colors.ENDC}").strip()
    
    if profile_name not in profiles:
        print(f"\n{Colors.RED}Profile '{profile_name}' không tồn tại!{Colors.ENDC}")
        return
    
    profile = profiles[profile_name]
    set_git_config(profile['name'], profile['email'])
    print(f"\n{Colors.GREEN}✅ Đã chuyển sang profile '{profile_name}' thành công!{Colors.ENDC}")
    
    # Cập nhật URL repository nếu đang trong Git repository
    update_repository_url_for_profile(profile_name)
    
    if 'ssh_key' in profile:
        print(f"\n{Colors.YELLOW}Lưu ý: Khi clone repository mới, sử dụng URL dạng:{Colors.ENDC}")
        print(f"{Colors.CYAN}git@github.com-{profile_name}:username/repository.git{Colors.ENDC}")
        
        # Kiểm tra kết nối
        print(f"\n{Colors.CYAN}Đang kiểm tra kết nối GitHub...{Colors.ENDC}")
        try:
            result = subprocess.run(
                ['ssh', '-T', f'git@github.com-{profile_name}'],
                capture_output=True,
                text=True,
                env={'GIT_SSH_COMMAND': f'ssh -i {profile["ssh_key"]}'}
            )
            
            if "successfully authenticated" in result.stderr.lower():
                print(f"{Colors.GREEN}✅ Kết nối thành công!{Colors.ENDC}")
            else:
                print(f"{Colors.RED}❌ Kết nối thất bại!{Colors.ENDC}")
                print(f"{Colors.YELLOW}Lỗi: {result.stderr}{Colors.ENDC}")
                print(f"\n{Colors.BOLD}Hãy kiểm tra:{Colors.ENDC}")
                print(f"{Colors.CYAN}1. SSH key đã được thêm vào GitHub chưa?{Colors.ENDC}")
                print(f"{Colors.CYAN}2. SSH key có quyền truy cập đúng không? (chmod 600){Colors.ENDC}")
                print(f"{Colors.CYAN}3. Cấu hình SSH config có đúng không?{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Lỗi khi kiểm tra kết nối: {str(e)}{Colors.ENDC}")

def show_current():
    """Show current Git configuration."""
    config = get_current_git_config()
    if config:
        print(f"\n{Colors.BOLD}=== Cấu hình Git Hiện tại ==={Colors.ENDC}")
        print(f"{Colors.GREEN}Tên: {config['name']}{Colors.ENDC}")
        print(f"{Colors.BLUE}Email: {config['email']}{Colors.ENDC}")
        
        profiles = load_profiles()
        for name, profile in profiles.items():
            if profile['name'] == config['name'] and profile['email'] == config['email']:
                print(f"{Colors.YELLOW}Profile: {name}{Colors.ENDC}")
                if 'ssh_key' in profile:
                    print(f"{Colors.CYAN}SSH key: {profile['ssh_key']}{Colors.ENDC}")
                break
    else:
        print(f"\n{Colors.RED}Chưa cấu hình Git global!{Colors.ENDC}")

def list_profiles():
    """List all saved profiles."""
    profiles = load_profiles()
    
    if not profiles:
        print(f"\n{Colors.RED}Không có profile nào!{Colors.ENDC}")
        return
    
    print(f"\n{Colors.BOLD}=== Danh sách Profiles ==={Colors.ENDC}")
    for name, profile in profiles.items():
        print(f"\n{Colors.YELLOW}Profile: {name}{Colors.ENDC}")
        print(f"{Colors.GREEN}Tên: {profile['name']}{Colors.ENDC}")
        print(f"{Colors.BLUE}Email: {profile['email']}{Colors.ENDC}")
        if 'ssh_key' in profile:
            print(f"{Colors.CYAN}SSH key: {profile['ssh_key']}{Colors.ENDC}")

def remove_profile():
    """Remove a Git profile."""
    profiles = load_profiles()
    
    if not profiles:
        print(f"\n{Colors.RED}Không có profile nào để xóa!{Colors.ENDC}")
        return
    
    print(f"\n{Colors.BOLD}=== Xóa Profile ==={Colors.ENDC}")
    print(f"{Colors.YELLOW}Profiles có sẵn:{Colors.ENDC}")
    for name in profiles:
        print(f"{Colors.GREEN}- {name}{Colors.ENDC}")
    
    profile_name = input(f"\n{Colors.CYAN}Nhập tên profile muốn xóa: {Colors.ENDC}").strip()
    
    if profile_name not in profiles:
        print(f"\n{Colors.RED}Profile '{profile_name}' không tồn tại!{Colors.ENDC}")
        return
    
    # Kiểm tra xem profile này có đang được sử dụng không
    current_config = get_current_git_config()
    profile = profiles[profile_name]
    
    if (current_config and 
        current_config['name'] == profile['name'] and 
        current_config['email'] == profile['email']):
        # Xóa cấu hình Git global
        print(f"\n{Colors.YELLOW}Đang xóa cấu hình Git global...{Colors.ENDC}")
        try:
            subprocess.run(['git', 'config', '--global', '--unset', 'user.name'])
            subprocess.run(['git', 'config', '--global', '--unset', 'user.email'])
            print(f"{Colors.GREEN}✅ Đã xóa cấu hình Git global{Colors.ENDC}")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}❌ Lỗi khi xóa cấu hình Git: {str(e)}{Colors.ENDC}")
    
    # Remove SSH keys if they exist
    if 'ssh_key' in profile:
        try:
            os.remove(profile['ssh_key'])
            os.remove(f"{profile['ssh_key']}.pub")
            print(f"{Colors.GREEN}✅ Đã xóa SSH keys của profile '{profile_name}'{Colors.ENDC}")
            
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
                print(f"{Colors.GREEN}✅ Đã xóa cấu hình SSH của profile '{profile_name}'{Colors.ENDC}")
        except OSError:
            pass
    
    del profiles[profile_name]
    save_profiles(profiles)
    print(f"\n{Colors.GREEN}✅ Đã xóa profile '{profile_name}' thành công!{Colors.ENDC}")
    
    # Hiển thị hướng dẫn
    print(f"\n{Colors.BOLD}Lưu ý:{Colors.ENDC}")
    print(f"{Colors.YELLOW}1. Nếu bạn muốn sử dụng Git, hãy chuyển sang một profile khác{Colors.ENDC}")
    print(f"{Colors.YELLOW}2. Hoặc cấu hình Git global mới bằng lệnh:{Colors.ENDC}")
    print(f"{Colors.CYAN}   git config --global user.name \"Tên của bạn\"{Colors.ENDC}")
    print(f"{Colors.CYAN}   git config --global user.email \"email@example.com\"{Colors.ENDC}")
    
    # Hiển thị các profiles còn lại
    if profiles:
        print(f"\n{Colors.BOLD}Các profiles còn lại:{Colors.ENDC}")
        for name in profiles:
            print(f"{Colors.GREEN}- {name}{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}Bạn có thể chuyển sang một trong các profiles trên.{Colors.ENDC}")
    else:
        print(f"\n{Colors.RED}Không còn profile nào. Hãy tạo profile mới để sử dụng.{Colors.ENDC}")

def test_connection():
    """Test GitHub connection for current profile."""
    current = get_current_git_config()
    if not current:
        print(f"\n{Colors.RED}Chưa cấu hình Git global!{Colors.ENDC}")
        return
    
    profiles = load_profiles()
    current_profile = None
    
    # Tìm profile hiện tại
    for name, profile in profiles.items():
        if profile['name'] == current['name'] and profile['email'] == current['email']:
            current_profile = name
            break
    
    if not current_profile:
        print(f"\n{Colors.RED}Không tìm thấy profile cho cấu hình Git hiện tại!{Colors.ENDC}")
        return
    
    if 'ssh_key' not in profiles[current_profile]:
        print(f"\n{Colors.RED}Profile '{current_profile}' không có SSH key!{Colors.ENDC}")
        return
    
    # Kiểm tra kết nối
    print(f"\n{Colors.CYAN}Đang kiểm tra kết nối GitHub cho profile '{current_profile}'...{Colors.ENDC}")
    try:
        # Thêm GitHub host key vào known_hosts
        subprocess.run(
            ['ssh-keyscan', '-t', 'rsa', 'github.com'],
            stdout=open(os.path.expanduser('~/.ssh/known_hosts'), 'a'),
            stderr=subprocess.DEVNULL
        )
        
        # Kiểm tra kết nối
        result = subprocess.run(
            ['ssh', '-T', f'git@github.com-{current_profile}'],
            capture_output=True,
            text=True,
            env={'GIT_SSH_COMMAND': f'ssh -i {profiles[current_profile]["ssh_key"]}'}
        )
        
        if "successfully authenticated" in result.stderr.lower():
            print(f"\n{Colors.GREEN}✅ Kết nối thành công với GitHub!{Colors.ENDC}")
            print(f"{Colors.BLUE}Profile: {current_profile}{Colors.ENDC}")
            print(f"{Colors.GREEN}Tên: {current['name']}{Colors.ENDC}")
            print(f"{Colors.BLUE}Email: {current['email']}{Colors.ENDC}")
            print(f"{Colors.CYAN}SSH key: {profiles[current_profile]['ssh_key']}{Colors.ENDC}")
        else:
            print(f"\n{Colors.RED}❌ Kết nối thất bại!{Colors.ENDC}")
            print(f"{Colors.YELLOW}Lỗi: {result.stderr}{Colors.ENDC}")
            print(f"\n{Colors.BOLD}Hãy kiểm tra:{Colors.ENDC}")
            print(f"{Colors.CYAN}1. SSH key đã được thêm vào GitHub chưa?{Colors.ENDC}")
            print(f"{Colors.CYAN}2. SSH key có quyền truy cập đúng không? (chmod 600){Colors.ENDC}")
            print(f"{Colors.CYAN}3. Cấu hình SSH config có đúng không?{Colors.ENDC}")
            
            # Hiển thị public key để thêm vào GitHub
            key_file = profiles[current_profile]['ssh_key']
            print(f"\n{Colors.YELLOW}Public key của profile này:{Colors.ENDC}")
            print(f"{Colors.CYAN}" + "-" * 50 + Colors.ENDC)
            with open(f"{key_file}.pub", 'r') as f:
                public_key = f.read().strip()
                print(f"{Colors.GREEN}{public_key}{Colors.ENDC}")
            print(f"{Colors.CYAN}" + "-" * 50 + Colors.ENDC)
            
            # Hỏi người dùng có muốn mở trang GitHub SSH settings không
            choice = input(f"\n{Colors.YELLOW}Bạn có muốn mở trang GitHub SSH settings để thêm key không? (y/N): {Colors.ENDC}").strip().lower()
            if choice == 'y':
                print(f"\n{Colors.BLUE}Đang mở trang cài đặt SSH key của GitHub...{Colors.ENDC}")
                open_github_ssh_settings()
    
    except Exception as e:
        print(f"\n{Colors.RED}❌ Lỗi khi kiểm tra kết nối: {str(e)}{Colors.ENDC}")

def update_repository_url():
    """Update repository URL for current profile."""
    current = get_current_git_config()
    if not current:
        print(f"\n{Colors.RED}Chưa cấu hình Git global!{Colors.ENDC}")
        return
    
    profiles = load_profiles()
    current_profile = None
    
    # Tìm profile hiện tại
    for name, profile in profiles.items():
        if profile['name'] == current['name'] and profile['email'] == current['email']:
            current_profile = name
            break
    
    if not current_profile:
        print(f"\n{Colors.RED}Không tìm thấy profile cho cấu hình Git hiện tại!{Colors.ENDC}")
        return
    
    # Kiểm tra xem có phải là Git repository không
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print(f"\n{Colors.RED}Thư mục hiện tại không phải là Git repository!{Colors.ENDC}")
        return
    
    # Lấy URL hiện tại
    try:
        current_url = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode().strip()
        print(f"\n{Colors.BOLD}URL hiện tại:{Colors.ENDC}")
        print(f"{Colors.BLUE}{current_url}{Colors.ENDC}")
    except:
        current_url = None
        print(f"\n{Colors.YELLOW}Chưa có remote origin{Colors.ENDC}")
    
    # Phân tích URL hiện tại
    if current_url:
        if current_url.startswith('git@github.com'):
            # URL SSH
            repo_part = current_url.split('github.com:')[1]
            new_url = f"git@github.com-{current_profile}:{repo_part}"
        elif current_url.startswith('https://github.com/'):
            # URL HTTPS
            repo_part = current_url.replace('https://github.com/', '')
            new_url = f"git@github.com-{current_profile}:{repo_part}"
        else:
            print(f"\n{Colors.RED}Không hỗ trợ định dạng URL này!{Colors.ENDC}")
            return
    else:
        # Tạo remote origin mới
        repo_name = input(f"\n{Colors.YELLOW}Nhập tên repository (username/repo): {Colors.ENDC}").strip()
        new_url = f"git@github.com-{current_profile}:{repo_name}"
    
    # Cập nhật hoặc thêm remote
    try:
        if current_url:
            print(f"\n{Colors.CYAN}Đang cập nhật URL remote...{Colors.ENDC}")
            subprocess.run(['git', 'remote', 'set-url', 'origin', new_url], check=True)
        else:
            print(f"\n{Colors.CYAN}Đang thêm remote origin...{Colors.ENDC}")
            subprocess.run(['git', 'remote', 'add', 'origin', new_url], check=True)
        
        print(f"\n{Colors.GREEN}✅ Đã cập nhật URL thành công:{Colors.ENDC}")
        print(f"{Colors.BLUE}{new_url}{Colors.ENDC}")
        
        # Kiểm tra kết nối
        print(f"\n{Colors.CYAN}Đang kiểm tra kết nối với repository...{Colors.ENDC}")
        try:
            subprocess.run(['git', 'fetch'], check=True, capture_output=True)
            print(f"{Colors.GREEN}✅ Kết nối thành công!{Colors.ENDC}")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}❌ Không thể kết nối với repository!{Colors.ENDC}")
            print(f"{Colors.YELLOW}Lỗi: {e.stderr.decode()}{Colors.ENDC}")
            print(f"\n{Colors.BOLD}Hãy kiểm tra:{Colors.ENDC}")
            print(f"{Colors.CYAN}1. Repository có tồn tại không?{Colors.ENDC}")
            print(f"{Colors.CYAN}2. Bạn có quyền truy cập repository không?{Colors.ENDC}")
            print(f"{Colors.CYAN}3. SSH key đã được thêm vào GitHub chưa?{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"\n{Colors.RED}❌ Lỗi khi cập nhật URL: {e.stderr.decode()}{Colors.ENDC}")

def print_menu():
    """Print the main menu."""
    profiles = load_profiles()
    profile_count = len(profiles)
    
    print(f"\n{Colors.BOLD}Chọn một tùy chọn:{Colors.ENDC}")
    print(f"{Colors.GREEN}1. Thêm profile mới{Colors.ENDC}")
    print(f"{Colors.BLUE}2. Chuyển đổi profile{Colors.ENDC}" + (f" {Colors.YELLOW}({profile_count} profiles){Colors.ENDC}" if profile_count > 0 else ""))
    print(f"{Colors.CYAN}3. Xem profile hiện tại{Colors.ENDC}")
    print(f"{Colors.YELLOW}4. Xem danh sách profiles{Colors.ENDC}" + (f" {Colors.GREEN}({profile_count}){Colors.ENDC}" if profile_count > 0 else ""))
    print(f"{Colors.RED}5. Xóa profile{Colors.ENDC}")
    print(f"{Colors.BLUE}6. Kiểm tra kết nối GitHub{Colors.ENDC}")
    print(f"{Colors.GREEN}7. Cập nhật URL repository{Colors.ENDC}")
    print(f"{Colors.RED}0. Thoát{Colors.ENDC}")

def print_status_bar():
    """Print status bar with current profile."""
    current = get_current_git_config()
    if current:
        print(f"\n{Colors.BOLD}Profile hiện tại:{Colors.ENDC}")
        print(f"{Colors.GREEN}Tên: {current['name']}{Colors.ENDC}")
        print(f"{Colors.BLUE}Email: {current['email']}{Colors.ENDC}")
    else:
        print(f"\n{Colors.YELLOW}Chưa cấu hình Git global!{Colors.ENDC}")

def handle_choice(choice):
    """Handle the user's menu choice."""
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
    elif choice == "6":
        test_connection()
    elif choice == "7":
        update_repository_url()
    elif choice == "0":
        print(f"\n{Colors.GREEN}Cảm ơn bạn đã sử dụng Git Profile Manager!{Colors.ENDC}")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}Lựa chọn không hợp lệ!{Colors.ENDC}")
    
    input(f"\n{Colors.YELLOW}Nhấn Enter để tiếp tục...{Colors.ENDC}")

def main():
    """Main program loop."""
    while True:
        clear_screen()
        print_header()
        print_status_bar()
        print_menu()
        
        choice = input(f"\n{Colors.BOLD}Nhập lựa chọn của bạn (0-7): {Colors.ENDC}").strip()
        handle_choice(choice)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Đã thoát chương trình.{Colors.ENDC}")
        sys.exit(0)
