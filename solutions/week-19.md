# Gợi ý và đáp án — Tuần 19

## Đáp án tự kiểm tra

1. Unit test có thể dùng fake với cấu trúc dữ liệu khác server thật, hoặc bỏ sót lỗi gắn token, URL, serialization và wiring dependency. Integration test kiểm tra những thành phần đó có phối hợp đúng hay không.
2. Chưa. Authorization phải được thực thi tại API hoặc tầng dữ liệu có thẩm quyền. Kiểm tra bằng request trực tiếp từ token B đến tài nguyên A mới tạo bằng chứng cho ranh giới đó.
3. Sau cập nhật, version tăng. Nếu xóa bằng version cũ, server phải từ chối để tránh xóa dữ liệu đã thay đổi. Cleanup cần theo dõi version mới hoặc tải lại đúng tài nguyên bằng tài khoản sở hữu.

## Gợi ý lab

- **W19-L1:** đặt tên test gắn hành trình. Tạo ID riêng cho mỗi lần chạy và hiển thị ID trong log test; không log token. Dùng nút/semantics ổn định để tương tác UI.
- **W19-L2:** kiểm tra cả response từ chối lẫn việc tài nguyên không bị thay đổi. Một server trả lỗi nhưng đã ghi dữ liệu vẫn là bug nghiêm trọng.
- **W19-L3:** phân biệt 401, 403 và 503. Tự refresh không giải quyết thiếu quyền, còn retry 503 phải giới hạn và giữ thao tác người dùng nhất quán. Mock local không chứng minh cấu hình phân quyền của backend production.

## Ví dụ sửa lỗi

Sai về thiết kế: repository toàn cục giữ danh sách cũ khi token đổi, nên người dùng B thoáng thấy công việc của A.

Hướng sửa:

```text
Phiên A kết thúc
→ dừng request và subscription thuộc A
→ xóa/invalidate state hiển thị của A
→ chọn storage namespace của B hoặc trạng thái chưa đăng nhập
→ tải dữ liệu B
```

Test tạo request A chậm, đăng xuất A rồi đăng nhập B, sau đó cho response A hoàn tất. UI của B phải không thay đổi. Ngoài việc xóa state lúc logout, cần bỏ qua kết quả bất đồng bộ thuộc phiên đã hết hiệu lực.
