# Git Profile Switcher

Công cụ giúp chuyển đổi nhanh chóng giữa các Git profiles khác nhau trên máy local.

## Tính năng

- Lưu trữ nhiều Git profiles
- Chuyển đổi nhanh chóng giữa các profiles
- Hiển thị profile hiện tại
- Thêm/Xóa profiles

## Cài đặt

1. Đảm bảo bạn đã cài đặt Python 3.6 trở lên
2. Clone repository này về máy
3. Chạy script với lệnh: `python git_profile_switcher.py`

## Sử dụng

- Thêm profile mới: `python git_profile_switcher.py add`
- Chuyển đổi profile: `python git_profile_switcher.py switch`
- Xem profile hiện tại: `python git_profile_switcher.py current`
- Xem danh sách profiles: `python git_profile_switcher.py list`
- Xóa profile: `python git_profile_switcher.py remove`

## Cấu trúc profiles

Mỗi profile sẽ bao gồm:
- Tên profile
- Email
- Tên người dùng 