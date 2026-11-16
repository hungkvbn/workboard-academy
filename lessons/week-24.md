# Tuần 24 — Bộ nhớ, isolate và chi phí tối ưu

**Đầu ra:** điều tra một vấn đề giữ bộ nhớ; thí nghiệm xử lý dữ liệu trên isolate với kết quả đo. **Tiên quyết:** tuần 23; hiểu lifecycle và async/await.

**Lịch 15 giờ:** 3 giờ học, 8 giờ lab, 3 giờ đo lại/test hồi quy, 1 giờ trình bày. Mục tiêu là hiểu vòng đời tài nguyên và đánh đổi, không thêm isolate vào mọi thao tác.

## Bài giảng

### Có bộ nhớ tăng chưa đủ kết luận leak

Garbage collector thu hồi đối tượng không còn được tham chiếu, nhưng không giải phóng một đối tượng vẫn bị listener hoặc cache giữ. Trong ứng dụng UI, controller, subscription, callback và ảnh là những nơi cần kiểm tra. Mở một màn hình rồi đóng nhiều lần mà số đối tượng sống tiếp tục tăng là tín hiệu đáng điều tra.

Cache chủ động giữ dữ liệu để tránh tải lại, nên mức bộ nhớ không nhất thiết trở về bằng lúc mới mở app. Hãy quan sát xu hướng qua nhiều chu kỳ và đối tượng nào còn được giữ. DevTools Memory view giúp xem heap, allocation và retained objects; số byte tổng cộng một lần chụp không tự giải thích nguyên nhân.

### Quyền sở hữu quyết định nơi giải phóng

Thành phần tạo và sở hữu tài nguyên thường chịu trách nhiệm kết thúc vòng đời của nó. Widget tạo `AnimationController` cần dispose controller khi widget kết thúc. Subscription được tạo trong provider phải gắn với vòng đời provider tương ứng. Tránh dispose một tài nguyên chia sẻ mà thành phần khác vẫn đang dùng.

```dart
@override
void dispose() {
  titleController.dispose();
  animationController.dispose();
  super.dispose();
}
```

Đoạn minh họa giả định hai controller được State này tạo và sở hữu. Thêm kiểm tra `mounted` trước cập nhật UI không thay thế việc hủy subscription: nó tránh một số lỗi sử dụng State đã đóng, nhưng nguồn sự kiện có thể vẫn chạy và giữ tham chiếu.

### Async không biến CPU thành công việc nền

Đánh dấu một hàm `async` không khiến JSON parsing hoặc vòng lặp nặng tự chạy ở isolate khác. Nếu phần tính toán chiếm main isolate quá lâu, UI có thể không xử lý frame đúng hạn. Isolate có bộ nhớ riêng và trao đổi thông điệp; việc tạo isolate và truyền dữ liệu cũng tốn thời gian.

```dart
List<Map<String, dynamic>> decodeRows(String source) {
  final rows = jsonDecode(source) as List<dynamic>;
  return rows
      .map((row) => Map<String, dynamic>.from(row as Map))
      .toList(growable: false);
}

// Cần import dart:convert và package:flutter/foundation.dart.
final rows = await compute(decodeRows, jsonText);
```

Đây là ví dụ với fixture JSON đã biết cấu trúc; parser production vẫn cần kiểm tra dữ liệu không hợp lệ. Trên nền tảng native, `compute` có thể chuyển phép tính sang isolate; trên web, nó chạy trên event loop hiện tại. Thí nghiệm tuần này nhắm mobile. Không truyền controller, database connection hoặc đối tượng nền tảng không gửi được vào isolate.

### Đo cả lợi ích và tổng chi phí

Một phép tính có thể hoàn tất chậm hơn do overhead truyền dữ liệu nhưng UI phản hồi tốt hơn. Hai kết quả đó không mâu thuẫn. Báo cáo cả thời gian hoàn tất và ảnh hưởng tới frame/nhập liệu. Nếu dữ liệu nhỏ, isolate có thể không có lợi; nếu parse chỉ diễn ra hiếm và không gây giật, thêm cơ chế phức tạp chưa chắc đáng giá.

## Thực hành

### W24-L1 — Theo dấu tài nguyên (3 giờ)

Mở và đóng màn hình editor 20 lần với cùng thao tác. Quan sát controller, subscription và đối tượng dữ liệu liên quan bằng DevTools. Chọn một đối tượng đáng nghi, tìm ai giữ tham chiếu sau khi màn hình đóng. Sửa quyền sở hữu hoặc hủy đăng ký rồi lặp lại. Ghi phân biệt giữa cache hợp lệ và leak đã có bằng chứng.

### W24-L2 — Thí nghiệm JSON nặng (3 giờ)

Sinh fixture JSON với 1.000 rồi 50.000 công việc. So sánh parse trực tiếp và `compute` trên cùng thiết bị ở profile mode; giữ kết quả parse giống nhau. Trong lúc parse, thử tương tác một animation hoặc trường nhập. Ghi tổng thời gian, ảnh hưởng frame và kích thước dữ liệu. Không suy rộng kết quả một thiết bị thành quy luật cho mọi app.

### W24-L3 — Chọn giải pháp cuối (2 giờ)

Viết một quyết định kỹ thuật: giữ parse trực tiếp, dùng isolate cho dữ liệu lớn, hoặc thay đổi cách tải dữ liệu để tránh payload lớn. Nêu chi phí code, bộ nhớ và khả năng hủy/bỏ qua kết quả cũ. Kiểm tra đóng màn hình hoặc đổi tài khoản khi đang xử lý: kết quả phiên cũ không được cập nhật phiên mới.

## Nghiệm thu

- [ ] Có chu kỳ tái hiện và bằng chứng đối tượng được giữ hoặc giải phóng.
- [ ] Controller/subscription có chủ sở hữu và vòng đời rõ ràng.
- [ ] Hiểu rằng `mounted` không tự hủy công việc nền.
- [ ] Hai cách parse trả cùng kết quả với fixture đã chọn.
- [ ] Báo cáo cả thời gian tổng và ảnh hưởng UI, ghi rõ nền tảng.
- [ ] Quyết định giữ/bỏ isolate được giải thích bằng dữ liệu.

## Tự kiểm tra

1. Vì sao một mức bộ nhớ cao chưa đủ chứng minh leak?
2. Vì sao `async` không giải quyết JSON parsing làm giật UI?
3. Isolate có thể cải thiện phản hồi nhưng tăng tổng thời gian vì sao?

Đọc [Memory view](https://docs.flutter.dev/tools/devtools/memory) và [isolates](https://docs.flutter.dev/perf/isolates). Xem [gợi ý](../solutions/week-24.md) sau khi lưu báo cáo đo.
