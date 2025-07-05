#!/bin/bash

# Tạo thư mục cài đặt
INSTALL_DIR="$HOME/.git-profile-manager"
mkdir -p "$INSTALL_DIR"

# Cài đặt các thư viện cần thiết
echo "Đang cài đặt các thư viện cần thiết..."

# Kiểm tra và cài đặt pip nếu cần
if ! command -v pip3 &> /dev/null; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py --user
        rm get-pip.py
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-pip
        fi
    elif [[ "$OSTYPE" == "msys" ]]; then
        # Windows/Git Bash
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py --user
        rm get-pip.py
    fi
fi

# Cài đặt pyperclip
python3 -m pip install --user pyperclip

# Cài đặt xclip trên Linux nếu cần
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! command -v xclip &> /dev/null; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y xclip
        elif command -v yum &> /dev/null; then
            sudo yum install -y xclip
        fi
    fi
fi

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