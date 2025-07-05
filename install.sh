#!/bin/bash

# Tạo thư mục cài đặt
INSTALL_DIR="$HOME/.git-profile-manager"
mkdir -p "$INSTALL_DIR"

# Tải các file từ GitHub
echo "Đang tải Git Profile Manager..."
curl -s https://raw.githubusercontent.com/nhatpm3124/git-switch/main/git_profile_switcher.py -o "$INSTALL_DIR/git_profile_switcher.py"
curl -s https://raw.githubusercontent.com/nhatpm3124/git-switch/main/git_profile_menu.py -o "$INSTALL_DIR/git_profile_menu.py"

# Cấp quyền thực thi
chmod +x "$INSTALL_DIR/git_profile_switcher.py"
chmod +x "$INSTALL_DIR/git_profile_menu.py"

# Tạo symbolic links trong /usr/local/bin
echo "Tạo shortcuts..."
sudo ln -sf "$INSTALL_DIR/git_profile_menu.py" /usr/local/bin/git-profile
sudo ln -sf "$INSTALL_DIR/git_profile_switcher.py" /usr/local/bin/git-profile-cli

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
" 