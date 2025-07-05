#!/bin/bash

# Tạo thư mục cài đặt
INSTALL_DIR="$HOME/.git-profile-manager"
mkdir -p "$INSTALL_DIR"

# Tải file menu.py từ GitHub
echo "Đang tải Git Profile Manager..."
curl -s https://raw.githubusercontent.com/nhatpm3124/git-switch/main/menu.py -o "$INSTALL_DIR/menu.py"

# Cấp quyền thực thi
chmod +x "$INSTALL_DIR/menu.py"

# Tạo symbolic link
mkdir -p "$HOME/.local/bin"
ln -sf "$INSTALL_DIR/menu.py" "$HOME/.local/bin/git-profile"

# Thêm ~/.local/bin vào PATH nếu chưa có
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
fi

echo "
Git Profile Manager đã được cài đặt thành công!

Sử dụng lệnh 'git-profile' để khởi động chương trình.

Lưu ý: Bạn có thể cần mở terminal mới để lệnh hoạt động.

Đang khởi động Git Profile Manager..."

# Chạy chương trình
"$INSTALL_DIR/menu.py" 