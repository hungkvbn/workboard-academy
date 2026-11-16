# Gợi ý và đáp án tuần 25

Chỉ mở sau lần thử đầu tiên. Bằng chứng chạy trên thiết bị quan trọng hơn việc chép lại ví dụ.

## Đáp án tự kiểm tra

1. Hệ điều hành có thể kết thúc tiến trình mà không phát đủ callback. Ghi dữ liệu quan trọng trong transaction khi xác nhận thao tác; lifecycle chủ yếu giúp phối hợp tài nguyên và refresh.
2. `MissingPluginException` thường có nghĩa không tìm thấy phần xử lý method/channel trên nền tảng đang chạy. `PlatformException` biểu diễn lỗi được phía nền tảng báo qua channel. Cả hai cần thông tin chẩn đoán phù hợp, nhưng hướng điều tra khác nhau.
3. Chỉ chức năng phụ thuộc quyền bị giới hạn. Ví dụ không được thông báo thì vẫn thêm, sửa, lọc công việc; UI giải thích cách bật nhắc việc nếu người dùng muốn.

## Gợi ý ba lab

- **W25-L1:** giữ một `Future` hoặc cờ đồng bộ đang chạy trong repository; kết thúc bằng `finally`. Dữ liệu cục bộ phải được ghi trước khi UI tuyên bố “đã lưu”. Đừng dùng một cờ trong widget làm cơ chế bền vững.
- **W25-L2:** định nghĩa enum trạng thái ở adapter, ánh xạ kết quả native sang enum. Test các nhánh bằng fake trước, rồi kiểm chứng tên và ý nghĩa trạng thái từ plugin trên OS thực tế.
- **W25-L3:** tên channel và method phải giống hoàn toàn ở hai phía. Method không được hỗ trợ trả `notImplemented`, không giả trả dữ liệu thành công.

## Ví dụ sửa lỗi

Lỗi: tạo listener trong `build` khiến mỗi lần rebuild đăng ký thêm callback.

```dart
@override
void initState() {
  super.initState();
  lifecycle = AppLifecycleListener(onResume: refreshSafely);
}

@override
void dispose() {
  lifecycle.dispose();
  super.dispose();
}
```

`refreshSafely` không được giữ `BuildContext` đã bị hủy; nếu cập nhật UI sau `await`, kiểm tra vòng đời phù hợp. Test chứng minh sau nhiều rebuild, một lần resume chỉ gọi adapter một lần. Chạy lại kịch bản dừng tiến trình để chắc việc sửa listener không che mất lỗi lưu dữ liệu.
