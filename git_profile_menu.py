#!/usr/bin/env python3
import os
import sys
from git_profile_switcher import (
    add_profile,
    switch_profile,
    show_current,
    list_profiles,
    remove_profile,
    test_github_connection,
    test_all_connections,
    load_profiles
)

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
    print(f"""
{Colors.CYAN}╔═══════════════════════════════════════╗{Colors.ENDC}
{Colors.CYAN}║{Colors.BOLD}        Git Profile Manager            {Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.YELLOW}        ------------------            {Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║{Colors.GREEN}  Quản lý nhiều tài khoản Git        {Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}╚═══════════════════════════════════════╝{Colors.ENDC}
""")

def print_menu():
    """Print the main menu."""
    # Lấy số lượng profiles
    profiles = load_profiles()
    profile_count = len(profiles)
    
    print(f"\n{Colors.BOLD}Chọn một tùy chọn:{Colors.ENDC}")
    print(f"{Colors.GREEN}1. Thêm profile mới{Colors.ENDC}")
    print(f"{Colors.BLUE}2. Chuyển đổi profile{Colors.ENDC}" + (f" {Colors.YELLOW}({profile_count} profiles){Colors.ENDC}" if profile_count > 0 else ""))
    print(f"{Colors.CYAN}3. Xem profile hiện tại{Colors.ENDC}")
    print(f"{Colors.YELLOW}4. Xem danh sách profiles{Colors.ENDC}" + (f" {Colors.GREEN}({profile_count}){Colors.ENDC}" if profile_count > 0 else ""))
    print(f"{Colors.RED}5. Xóa profile{Colors.ENDC}")
    print(f"{Colors.BLUE}6. Kiểm tra kết nối GitHub{Colors.ENDC}")
    print(f"{Colors.CYAN}7. Kiểm tra tất cả kết nối{Colors.ENDC}")
    print(f"{Colors.RED}0. Thoát{Colors.ENDC}")

def print_status_bar():
    """Print status bar with current profile."""
    current = None
    try:
        import subprocess
        name = subprocess.check_output(['git', 'config', '--global', 'user.name']).decode().strip()
        email = subprocess.check_output(['git', 'config', '--global', 'user.email']).decode().strip()
        current = {'name': name, 'email': email}
    except:
        pass
    
    if current:
        print(f"\n{Colors.BOLD}Profile hiện tại:{Colors.ENDC}")
        print(f"{Colors.GREEN}Tên: {current['name']}{Colors.ENDC}")
        print(f"{Colors.BLUE}Email: {current['email']}{Colors.ENDC}")
    else:
        print(f"\n{Colors.YELLOW}Chưa cấu hình Git global!{Colors.ENDC}")

def select_profile():
    """Let user select a profile from the list."""
    profiles = load_profiles()
    if not profiles:
        print(f"\n{Colors.RED}Không có profile nào!{Colors.ENDC}")
        return None
    
    print(f"\n{Colors.BOLD}Profiles có sẵn:{Colors.ENDC}")
    for name in profiles:
        print(f"{Colors.GREEN}- {name}{Colors.ENDC}")
    
    profile_name = input(f"\n{Colors.YELLOW}Nhập tên profile: {Colors.ENDC}").strip()
    if profile_name not in profiles:
        print(f"\n{Colors.RED}Profile '{profile_name}' không tồn tại!{Colors.ENDC}")
        return None
    
    return profile_name

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
        profile_name = select_profile()
        if profile_name:
            test_github_connection(profile_name)
    elif choice == "7":
        test_all_connections()
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