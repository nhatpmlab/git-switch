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
    if [[ -f "$HOME/.bashrc" ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    fi
    if [[ -f "$HOME/.zshrc" ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    fi
fi

# Tạo script cập nhật
cat > "$INSTALL_DIR/update.sh" << 'EOL'
#!/bin/bash

echo "Đang cập nhật Git Profile Manager..."
curl -s https://raw.githubusercontent.com/nhatpm3124/git-switch/main/menu.py -o "$HOME/.git-profile-manager/menu.py"
chmod +x "$HOME/.git-profile-manager/menu.py"
echo "✅ Đã cập nhật thành công!"
EOL

chmod +x "$INSTALL_DIR/update.sh"
ln -sf "$INSTALL_DIR/update.sh" "$HOME/.local/bin/git-profile-update"

echo "
Git Profile Manager đã được cài đặt thành công!

Sử dụng:
  git-profile         : Khởi động chương trình
  git-profile-update : Cập nhật phiên bản mới

Lưu ý: Bạn có thể cần mở terminal mới để các lệnh hoạt động.

Đang khởi động Git Profile Manager..."

# Chạy chương trình
"$INSTALL_DIR/menu.py" 