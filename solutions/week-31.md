# Gợi ý và đáp án tuần 31

## Đáp án tự kiểm tra

1. Nhiều thay đổi đồng thời tăng số nguyên nhân có thể, khiến bisect hoặc thay một yếu tố để kiểm tra khó hơn. Nhóm dependency liên quan khi cần, nhưng giữ đơn vị thay đổi có thể giải thích.
2. Test phản ánh hành vi hiện tại, kể cả hành vi sai. Phải so sánh với yêu cầu và đánh dấu rõ phần cố ý thay đổi; regression test cho bug nên kiểm tra kết quả đúng mong muốn.
3. Review có cơ sở về correctness, rủi ro, khả năng bảo trì hoặc quy ước nhóm. Sở thích cá nhân cần được trình bày như gợi ý, không biến thành chặn PR vô lý.

## Gợi ý lab

- **W31-L1:** đọc migration guide trước khi sửa theo lỗi compiler. Với plugin, kiểm tra cả cấu hình Android/iOS được thay đổi, không chỉ API Dart.
- **W31-L2:** chọn một biến đổi nhỏ có thể giải thích trong một câu. Nếu PR vừa đổi state library, DB và UX, hãy chia lại.
- **W31-L3:** đưa người mới README mà không hướng dẫn miệng trước. Những chỗ họ kẹt là dữ liệu cải thiện onboarding.

## Ví dụ sửa lỗi qua review

Vấn đề: request cũ cập nhật state sau logout/login tài khoản khác.

```dart
final generation = session.generation;
final accountId = session.accountId;
final items = await api.fetchTasks();
if (generation != session.generation || accountId != session.accountId) {
  return;
}
cache.replaceForAccount(accountId, items);
```

`generation` tăng khi phiên thay đổi; kiểm tra chỉ user ID không đủ nếu cùng tài khoản đăng xuất rồi đăng nhập lại trong lúc request cũ còn chạy. Cache vẫn cần khóa theo account, và luồng dispose/cancellation phải được xử lý phù hợp. Test điều khiển thứ tự hoàn thành bằng completer, không dựa vào sleep ngẫu nhiên.
