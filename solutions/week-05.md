# Gợi ý và đáp án — Tuần 05

## Đáp án tự kiểm tra

1. Callback `setState` dành cho thay đổi state đồng bộ. Hãy đánh dấu đang lưu trong một lần `setState`, chờ thao tác ở ngoài, rồi cập nhật kết quả trong lần tiếp theo.
2. `mounted` cho biết State còn gắn với cây. Nó ngăn cập nhật UI đã dispose, nhưng không hủy request và không phát hiện response cũ ghi đè response mới.
3. Nếu chỉnh trực tiếp task gốc, Hủy phải khôi phục hàng loạt thay đổi và những nơi khác có thể đã quan sát dữ liệu chưa lưu. Bản nháp tạo ranh giới commit rõ ràng.

## Gợi ý lab

- **W05-L1:** tạo `GlobalKey<FormState>` một lần trong State. Callback Lưu gọi validate trước khi tạo bản dữ liệu gửi đi; chuẩn hóa dữ liệu tại một nơi rõ ràng.
- **W05-L2:** form trả kết quả mới, caller quyết định thay thế task. Nếu có cờ `clearDueAt`, test cả giữ hạn cũ, thay hạn và xóa hạn.
- **W05-L3:** fake save nên do test điều khiển; đừng bắt test chờ nhiều giây thật. Chặn submit bằng `_isSaving` cả ở UI lẫn đầu handler, vì callback còn có thể bị gọi từ nơi khác.

## Sửa lỗi mẫu

Sai: đặt controller trong build hoặc gọi `setState` ngay sau await mà không kiểm tra State còn tồn tại. Trong lớp State có hàm `saveDraft` và trường `_error`, có thể dùng cấu trúc sau:

```dart
Future<void> submit() async {
  if (_isSaving) return;
  setState(() { _isSaving = true; _error = null; });
  try {
    await saveDraft();
  } catch (error) {
    if (mounted) setState(() { _error = 'Lưu thất bại'; });
  } finally {
    if (mounted) setState(() { _isSaving = false; });
  }
}
```

Đây chỉ là phần kiểm soát vòng đời, chưa bao gồm validate, điều hướng hoặc xử lý lỗi nghiệp vụ. Hãy kiểm tra thành công và thất bại đều mở lại khả năng tương tác theo yêu cầu.
