# Gợi ý và đáp án — Tuần 18

## Đáp án tự kiểm tra

1. Spinner lặp liên tục có thể tiếp tục lên lịch frame. `pumpAndSettle()` chờ trạng thái không còn frame được lên lịch nên không kết thúc trước timeout. Hãy điều khiển fake và bơm đúng bước cần quan sát.
2. Key hữu ích khi nhiều phần tử có cùng chữ, văn bản thay đổi theo locale hoặc cần định danh một trường tương tác ổn định. Tìm bằng chữ vẫn tốt khi chính nội dung đó là hành vi cần bảo vệ.
3. Người dùng thật chịu tác động của thứ tự focus, cách hệ điều hành đọc nhãn, bàn phím và cử chỉ. Môi trường test thay thế không mô phỏng đầy đủ tất cả tương tác đó.

## Gợi ý lab

- **W18-L1:** dùng fake chưa hoàn tất, nhấn lưu hai lần, kiểm tra số request đang xử lý là một. Hoàn tất bằng lỗi, kiểm tra title vẫn nguyên; sau đó cấu hình thành công và thử lại.
- **W18-L2:** viết một bảng state → phần tử cần nhìn thấy → hành động được phép. Nó sẽ chỉ ra ngay màn hình nào chưa có đường phục hồi.
- **W18-L3:** đặt giả định rõ: màn hình, cỡ chữ, hệ điều hành và phiên bản app. Những giá trị stress trong đề là tình huống kiểm tra, không thay thế toàn bộ ma trận thiết bị hỗ trợ.

## Ví dụ sửa lỗi

Một icon hành động chỉ chứa `Icon(Icons.delete)` không diễn đạt rõ đối tượng sẽ bị xóa. Có thể dùng:

```dart
IconButton(
  tooltip: 'Xóa công việc ${task.title}',
  onPressed: onDelete,
  icon: const Icon(Icons.delete_outline),
)
```

Kiểm tra nhãn bằng semantics và thử trình đọc màn hình thật. Nếu đã bọc `Semantics` tùy chỉnh, tránh tạo hai nhãn lặp lại. Với hành động phá hủy dữ liệu quan trọng, thiết kế bước xác nhận hoặc khả năng hoàn tác phù hợp yêu cầu sản phẩm, rồi kiểm thử chính hành vi đó.
