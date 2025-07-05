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

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    print("""
╔═══════════════════════════════════════╗
║        Git Profile Manager            ║
║        ------------------            ║
║  Quản lý nhiều tài khoản Git        ║
╚═══════════════════════════════════════╝
""")

def print_menu():
    """Print the main menu."""
    print("\nChọn một tùy chọn:")
    print("1. Thêm profile mới")
    print("2. Chuyển đổi profile")
    print("3. Xem profile hiện tại")
    print("4. Xem danh sách profiles")
    print("5. Xóa profile")
    print("6. Kiểm tra kết nối GitHub")
    print("7. Kiểm tra tất cả kết nối")
    print("0. Thoát")

def select_profile():
    """Let user select a profile from the list."""
    profiles = load_profiles()
    if not profiles:
        print("\nKhông có profile nào!")
        return None
    
    print("\nProfiles có sẵn:")
    for name in profiles:
        print(f"- {name}")
    
    profile_name = input("\nNhập tên profile: ").strip()
    if profile_name not in profiles:
        print(f"\nProfile '{profile_name}' không tồn tại!")
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
        print("\nCảm ơn bạn đã sử dụng Git Profile Manager!")
        sys.exit(0)
    else:
        print("\nLựa chọn không hợp lệ!")
    
    input("\nNhấn Enter để tiếp tục...")

def main():
    """Main program loop."""
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("\nNhập lựa chọn của bạn (0-7): ").strip()
        handle_choice(choice)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nĐã thoát chương trình.")
        sys.exit(0) 