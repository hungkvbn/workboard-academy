# Tuần 17 — Unit test bảo vệ quy tắc nghiệp vụ

**Đầu ra:** một bộ test cho lọc công việc, xác định quá hạn và cập nhật trạng thái; một lỗi được tái hiện rồi sửa. **Tiên quyết:** hoàn thành tuần 16; logic nghiệp vụ không nằm trong widget. Dùng `WorkTask` với các trường trong [hợp đồng API](../project/api-contract.md).

**Lịch 15 giờ:** 3 giờ học và viết ví dụ, 8 giờ cho ba lab, 3 giờ chạy test/debug/refactor, 1 giờ demo. Nếu có thêm thời gian, nhờ người khác thử làm hỏng logic bằng một thay đổi nhỏ.

## Bài giảng

### Test mô tả hành vi có giá trị

Một unit test kiểm tra một quy tắc trong điều kiện xác định. “Hàm chạy không lỗi” là bằng chứng yếu. “Công việc đã hoàn thành không được xem là quá hạn, dù hạn đã qua” là hành vi cụ thể. Hãy viết tên test như một câu mô tả yêu cầu. Chia nội dung thành chuẩn bị dữ liệu, thực hiện hành vi và kiểm tra kết quả. Mỗi test nên có một lý do thất bại rõ ràng; nhiều phép kiểm tra cùng bảo vệ một kết quả vẫn hợp lý.

Quy ước của WorkBoard: công việc quá hạn khi `dueAt < now` và trạng thái khác `done`. Hạn bằng đúng thời điểm hiện tại chưa quá hạn. Không có hạn thì không quá hạn. Thời điểm so sánh là UTC; việc hiển thị theo múi giờ thuộc UI.

```dart
bool isOverdue(WorkTask task, DateTime now) {
  final dueAt = task.dueAt;
  return task.status != TaskStatus.done &&
      dueAt != null &&
      dueAt.isBefore(now);
}
```

Hàm nhận `now` từ bên ngoài để test có thể dùng một thời điểm cố định. Nếu gọi `DateTime.now()` bên trong, test chạy sát thời hạn có thể cho kết quả khác nhau giữa máy bạn và CI. Đây là ví dụ nhỏ của thiết kế để kiểm thử: đưa yếu tố không ổn định ra ngoài quy tắc cần kiểm tra.

### Fake giúp điều khiển tình huống

Fake là một phiên bản đơn giản nhưng có hành vi của dependency, chẳng hạn repository lưu dữ liệu trong bộ nhớ. Nó giúp bạn chủ động tạo thành công, thất bại hoặc trì hoãn. Không cần HTTP thật để kiểm tra bộ điều khiển trạng thái khi repository trả lỗi. Mock thường dùng để kiểm tra tương tác cụ thể; chỉ kiểm tra số lần gọi khi số lần đó thực sự là yêu cầu, như ngăn gửi trùng.

Fake phải tuân theo hợp đồng mà phần được test sử dụng. Fake luôn thành công sẽ che lỗi. Fake trả cùng một danh sách có thể bị sửa từ bên ngoài cũng tạo hành vi không giống repository thật. Trả bản sao khi cần và cung cấp cách cấu hình lỗi rõ ràng.

### Test biên và regression

Danh sách rỗng, hạn đúng bằng hiện tại, chuỗi chỉ có khoảng trắng và ID không tồn tại là dữ liệu biên. Chọn chúng từ quy tắc sản phẩm, không từ mong muốn tăng số lượng test. Khi tìm được bug, viết test thất bại trước khi sửa. Sau khi sửa, test đó trở thành regression test: nó ngăn hành vi cũ quay lại.

## Thực hành

### W17-L1 — Ma trận quá hạn và bộ lọc (3 giờ)

Tạo sáu công việc: không hạn; hạn hôm qua; hạn hôm sau; hạn đúng `now`; đã hoàn thành nhưng hạn hôm qua; tiêu đề chứa khoảng trắng đầu/cuối. Dùng `now` cố định `2026-01-15T10:00:00Z`. Viết bảng kết quả mong đợi trước khi viết test. Kiểm tra lọc theo trạng thái, tìm kiếm không phân biệt chữ hoa/thường và kết hợp hai bộ lọc. Đầu ra là test cùng bảng giải thích từng trường hợp.

### W17-L2 — Repository có lỗi có chủ đích (3 giờ)

Viết fake cho giao diện repository hiện có. Fake hỗ trợ trả danh sách, trả lỗi và chờ một `Completer`. Kiểm tra chuyển trạng thái tải → thành công, tải → lỗi và thử lại → thành công. Không gọi mạng thật; không chờ số giây cố định. Đầu ra là test chạy độc lập và nhanh trên máy không có backend.

### W17-L3 — Sửa một lỗi có bằng chứng (2 giờ)

Cố ý bỏ điều kiện `status != done` trong hàm quá hạn. Chạy test để chứng minh bộ test phát hiện thay đổi. Khôi phục, sau đó tìm hoặc tự tạo một lỗi khác ở bộ lọc. Ghi lại test đỏ, thay đổi sửa lỗi và test xanh trong PR theo [mẫu](../templates/pr.md).

## Nghiệm thu

- [ ] Test không phụ thuộc đồng hồ thật, mạng hoặc thứ tự chạy.
- [ ] Có các ca không hạn, đúng thời điểm và đã hoàn thành.
- [ ] Có đường thất bại và phục hồi sau khi thử lại.
- [ ] Fake không rò rỉ danh sách mutable cho test khác.
- [ ] Một thay đổi sai có chủ đích làm đúng test thất bại.
- [ ] Chạy `flutter test` thành công và giải thích được mỗi test bảo vệ gì.

## Tự kiểm tra

1. Vì sao truyền `now` tốt hơn gọi đồng hồ trực tiếp trong quy tắc này?
2. Khi nào nên kiểm tra số lần gọi repository?
3. Coverage cao có thể bỏ sót lỗi nào trong bài quá hạn?

Đọc [unit testing](https://docs.flutter.dev/cookbook/testing/unit/introduction). Chỉ mở [gợi ý và đáp án](../solutions/week-17.md) sau khi đã thử cả ba lab.
