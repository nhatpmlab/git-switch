# Git Profile Manager
Đây là công cụ giúp switch github profile... 
## Cài đặt

Chạy một trong hai lệnh sau để cài đặt:

```bash
# Cách 1 (ngắn gọn):
bash -c "$(curl -fsSL https://raw.githubusercontent.com/nhatpm3124/git-switch/main/install.sh)"

# Cách 2 (đầy đủ):
curl -o install.sh https://raw.githubusercontent.com/nhatpm3124/git-switch/main/install.sh && chmod +x install.sh && ./install.sh
```


Lưu ý: 
1. Chạy project tại terminal trong repo -> nếu bạn muốn switch người push code trong dự án
2. Chạy project tại terminal ngoài repo -> nếu bạn muốn setup ssh key mới


### Thêm profile mới

1. Chọn tùy chọn 1
2. Nhập thông tin:
   - Username GitHub (dùng làm tên profile và tên người dùng Git)
   - Email Git
3. Chương trình sẽ:
   - Tạo SSH key
   - Tự động copy key vào clipboard
   - Mở trang GitHub SSH settings
   - Kiểm tra kết nối

### Chuyển đổi profile

1. Chọn tùy chọn 2
2. Chọn profile muốn chuyển sang
3. Chương trình sẽ:
   - Cập nhật Git config
   - Tự động cập nhật URL repository (nếu có)
   - Kiểm tra kết nối

### Kiểm tra kết nối

1. Chọn tùy chọn 6
2. Chương trình sẽ:
   - Kiểm tra kết nối với GitHub
   - Hiển thị kết quả chi tiết
   - Gợi ý cách khắc phục nếu có lỗi

### Cập nhật URL repository

1. Chọn tùy chọn 7
2. Chương trình sẽ:
   - Phát hiện URL hiện tại
   - Tự động chuyển đổi sang định dạng mới
   - Kiểm tra kết nối

## Cấu trúc URL repository

Khi clone repository mới, sử dụng URL dạng:
```bash
git@github.com-<profile>:username/repository.git
```

Ví dụ:
```bash
# Profile: nhatpm3124
git@github.com-nhatpm3124:nhatpm3124/git-switch.git
```

## Cập nhật

Để cập nhật lên phiên bản mới nhất:
```bash
git-profile-update
```

## Gỡ cài đặt

Để gỡ cài đặt chương trình:
```bash
rm -rf ~/.git-profile-manager ~/.local/bin/git-profile ~/.local/bin/git-profile-update
```

## Lưu ý

1. **SSH key**:
   - Được lưu trong `~/.ssh/id_rsa_<profile>`
   - Cấu hình được thêm vào `~/.ssh/config`

2. **Git config**:
   - Cấu hình được lưu trong Git global config
   - Mỗi profile có user.name và user.email riêng

3. **Repository URL**:
   - Cần sử dụng đúng định dạng URL cho mỗi profile
   - Chương trình sẽ tự động cập nhật khi chuyển profile

4. **Profiles**:
   - Được lưu trong `~/.git_profiles.json`
   - Mỗi profile có tên, email và SSH key riêng

## Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra kết nối: `git-profile` > Tùy chọn 6
2. Cập nhật phiên bản mới: `git-profile-update`
3. Tạo issue trên GitHub: [New Issue](https://github.com/nhatpm3124/git-switch/issues/new) 
