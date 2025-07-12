# Git Profile Manager v2.3 🚀

Công cụ mạnh mẽ giúp quản lý và chuyển đổi nhanh chóng giữa các tài khoản GitHub khác nhau trên máy local với giao diện đẹp mắt và tính năng nâng cao.

## ✨ Tính năng mới v2.3

- ⚙️ **Settings Menu** - Nhóm các cài đặt vào một menu riêng
- 🔄 **Check for updates** - Kiểm tra phiên bản mới tự động từ GitHub
- 🎯 **Cleaner main menu** - Menu chính gọn gàng hơn với 4 options chính
- 📱 **Better navigation** - Settings submenu với back button
- 🔗 **Integrated tools** - Test connection và update URL trong Settings

## ✨ Tính năng v2.2

- 🎯 **Streamlined menu** - Removed redundant options (Show current, List profiles)
- 🗑️ **Enhanced profile deletion** - Clear warnings, detailed feedback, and verified file removal
- 🔍 **Better SSH key detection** - Accurately finds and removes SSH keys from disk
- ⚠️ **Double confirmation** - Type 'DELETE' + yes/no confirmation for safety
- 📋 **Detailed deletion preview** - Shows exactly what will be removed before deletion
- 🔄 **Step-by-step feedback** - Real-time progress during profile removal

## ✨ Tính năng v2.1

- 🔧 **Code được tối ưu hóa hoàn toàn** - Refactored codebase với improved maintainability
- 🎯 **Type hints đầy đủ** - Enhanced code với comprehensive type annotations
- 🧹 **Clean code structure** - Modular design với single responsibility principle
- ⚡ **Performance improvements** - Reduced complexity và better resource management
- 🔒 **Enhanced security** - Better input validation và file handling
- 📚 **Comprehensive documentation** - Improved docstrings và code comments
- 🧪 **Better testability** - Smaller methods easier to test

## ✨ Tính năng v2.0

- 🎨 **Giao diện ASCII art đẹp mắt** với SpringBoot-style header
- 🔧 **Code được tối ưu hóa** - loại bỏ code duplication
- 🛡️ **Bảo mật nâng cao** - hỗ trợ passphrase cho SSH keys
- ✅ **Error handling tốt hơn** - xử lý lỗi chi tiết và hướng dẫn rõ ràng
- 🌐 **Cross-platform hoàn toàn** - Windows, macOS, Linux
- 📋 **Smart clipboard** - tự động copy SSH key với fallback
- 🔍 **Validation** - kiểm tra định dạng email và username
- ⚡ **Performance** - khởi động nhanh hơn, sử dụng ít tài nguyên
- 🎯 **Direct run** - chạy trực tiếp từ GitHub mà không cần cài đặt

## 🎯 Tính năng chính

- 🔄 **Chuyển đổi profile nhanh chóng** giữa các GitHub accounts
- 🔑 **Tự động tạo và quản lý SSH keys** (4096-bit RSA)
- 📋 **Auto-copy SSH key vào clipboard** với support đa platform
- 🌐 **Tự động mở GitHub SSH settings** 
- 🔍 **Kiểm tra kết nối tự động** với troubleshooting tips
- 🔄 **Tự động cập nhật URL repository** khi switch profile
- 📱 **Giao diện menu thân thiện** với màu sắc đẹp mắt
- 🛡️ **Validation input** - đảm bảo dữ liệu đúng định dạng

## 📦 Cài đặt

### 🚀 Cách 1: Chạy trực tiếp (Không cần cài đặt)

#### **Linux / macOS:**
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/nhatpm3124/git-switch/main/run_git_profiles.sh)
```

#### **Windows PowerShell:**
```powershell
iwr -useb https://raw.githubusercontent.com/nhatpm3124/git-switch/main/run_git_profiles.ps1 | iex
```

#### **Windows Git Bash:**
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/nhatpm3124/git-switch/main/run_git_profiles.sh)
```

### 🏠 Cách 2: Cài đặt vĩnh viễn

#### **One-line install (Khuyến nghị):**
```bash
curl -fsSL https://raw.githubusercontent.com/nhatpm3124/git-switch/main/install.sh | bash
```

#### **Cài đặt thủ công:**
```bash
# Tải installer
curl -o install.sh https://raw.githubusercontent.com/nhatpm3124/git-switch/main/install.sh
chmod +x install.sh
./install.sh
```

## 🎮 Sử dụng

### 💫 Direct Run (Chạy trực tiếp)
- **Ưu điểm**: Không cần cài đặt, tự động cleanup, luôn phiên bản mới nhất
- **Nhược điểm**: Cần internet để khởi động, tốc độ khởi động chậm hơn

### 🏠 Permanent Install (Cài đặt vĩnh viễn)
- `git-profile` - Khởi động chương trình
- `git-profile-update` - Cập nhật phiên bản mới

### 🐍 Chạy trực tiếp bằng Python
```bash
python3 ~/.git-profile-manager/git_profiles.py
```

## 💻 Hỗ trợ đa nền tảng

### 🐧 **Linux**
- ✅ Đầy đủ tính năng
- ✅ ANSI colors
- ✅ Clipboard support (xclip/xsel/wl-copy)
- ✅ SSH key permissions

### 🍎 **macOS** 
- ✅ Đầy đủ tính năng
- ✅ Native clipboard (pbcopy)
- ✅ Browser integration
- ✅ SSH key permissions

### 🪟 **Windows**
- ✅ **Windows 10+ PowerShell** - Hỗ trợ đầy đủ
- ✅ **Git Bash** - Hỗ trợ đầy đủ 
- ✅ **Command Prompt** - Cơ bản
- ✅ ANSI colors (Windows 10+)
- ✅ PowerShell clipboard
- ✅ Native Windows paths

#### **Windows Requirements:**
- Windows 10+ (khuyến nghị)
- Python 3.6+
- Git for Windows
- OpenSSH Client (Windows 10+) hoặc Git Bash

## 📋 Lưu ý quan trọng

### 🎯 Khi nào chạy ở đâu:

1. **Trong repository** → Switch người push code trong dự án hiện tại
   ```bash
   cd my-project
   git-profile  # Chuyển đổi và tự động cập nhật remote URL
   ```

2. **Ngoài repository** → Setup SSH key mới hoặc quản lý profiles
   ```bash
   cd ~
   git-profile  # Thêm profile mới, quản lý SSH keys
   ```

### 🔧 Tính năng tự động:

- **Auto-update repository URL**: Khi switch profile trong Git repo, URL sẽ tự động được cập nhật
- **Smart SSH config**: Tự động thêm Host config cho từng profile
- **Connection testing**: Kiểm tra kết nối GitHub sau khi setup
- **Clipboard integration**: Tự động copy SSH key để paste vào GitHub
- **Cross-platform paths**: Tự động xử lý đường dẫn Windows/Unix

## 🖥️ Giao diện mới

```
   _______ _____ _______     ____  ____   ____  ______ _____ __    _____ _____
  / ____(_) __/_  __(_)    / __ \/ __ \ / __ \/ ____//   _// /   / ___// ___/
 / / __/ / /_   / /       / /_/ / /_/ // / / / /_    / / / /    \__ \ \__ \ 
/ /_/ / / __/  / /       / ____/ _, _// /_/ / __/  _/ / / /___ ___/ /___/ / 
\____/_/_/    /_/       /_/   /_/ |_|\____/_/    /___//_____//____//____/  

                    🚀 Git Profile Manager v2.0 🚀
              Switch between multiple GitHub accounts seamlessly

Current Profile:
📝 Name: username
📧 Email: user@example.com
👤 Profile: username

Choose an option:
1. 📝 Add new profile
2. 🔄 Switch profile (2 available)
3. 👁️  Show current profile
4. 📋 List all profiles (2)
5. 🗑️  Remove profile
6. 🔗 Test GitHub connection
7. 🌐 Update repository URL
0. 🚪 Exit
```

## 🛠️ Requirements

### **Cơ bản:**
- **Python 3.6+** (sử dụng Python standard library)
- **Git** 
- **Internet connection** (để tải về và connect GitHub)

### **Cho SSH features:**
- **ssh-keygen** (OpenSSH client)
- **Linux**: Thường có sẵn
- **macOS**: Có sẵn
- **Windows**: OpenSSH Client hoặc Git for Windows

### **Cho clipboard features:**
- **Linux**: xclip, xsel, hoặc wl-copy
- **macOS**: pbcopy (có sẵn)
- **Windows**: PowerShell hoặc clip (có sẵn)

## 🔧 Cải thiện từ v1.0

### 🎯 Code Quality
- ✅ Loại bỏ code duplication (từ 3 files xuống 2 files)
- ✅ Class-based architecture với proper error handling
- ✅ Type hints và consistent code style
- ✅ Cross-platform compatibility layer

### 🛡️ Security
- ✅ Support passphrase cho SSH keys
- ✅ Proper file permissions (Unix) và Windows compatibility
- ✅ Input validation và safe subprocess calls
- ✅ Secure temporary file handling

### 💫 User Experience  
- ✅ Beautiful ASCII art interface với ANSI colors
- ✅ Platform-specific troubleshooting tips
- ✅ Better error messages với context
- ✅ Progress indicators và confirmation prompts

### 🚀 Performance & Deployment
- ✅ Faster startup time và efficient operations
- ✅ No external dependencies (chỉ Python stdlib)
- ✅ Direct run option - không cần install
- ✅ Auto-cleanup và proper resource management

## 🌍 Cross-Platform Testing

| Feature | Linux | macOS | Windows 10+ | Windows <10 |
|---------|-------|-------|-------------|-------------|
| Core functionality | ✅ | ✅ | ✅ | ✅ |
| ANSI colors | ✅ | ✅ | ✅ | ❌ |
| Clipboard copy | ✅ | ✅ | ✅ | ✅ |
| SSH key generation | ✅ | ✅ | ✅ | ⚠️ |
| Browser integration | ✅ | ✅ | ✅ | ✅ |
| Direct run script | ✅ | ✅ | ✅ | ⚠️ |

✅ Hoàn toàn hỗ trợ | ⚠️ Hỗ trợ cơ bản | ❌ Không hỗ trợ

## 🔄 Migration từ v1.0

Git Profile Manager v2.0 hoàn toàn backward compatible với v1.0. Chỉ cần chạy lại installer để cập nhật:

```bash
git-profile-update
```

Tất cả profiles và SSH keys hiện tại sẽ được giữ nguyên.

## 🤝 Contributing

Contributions are welcome! Hãy tạo issue hoặc pull request.

### 🧪 Testing trên các platform:
- **Linux**: Ubuntu, Debian, CentOS, Arch
- **macOS**: macOS 10.15+
- **Windows**: Windows 10+, PowerShell 5.1+

## 📄 License

MIT License - see LICENSE file for details.

---

**Made with ❤️ for developers who work with multiple GitHub accounts**

**ALL COPYRIGHT BELONG TO NHATPM.SG!**

🌟 **Star this repo if it helps you!** 🌟 
