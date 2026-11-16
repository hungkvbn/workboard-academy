# Tuần 11 — Tìm kiếm, phân trang và cuộc đua giữa các request

**Đích đến:** người dùng gõ nhanh, cuộn nhanh hoặc đổi bộ lọc nhưng WorkBoard vẫn hiển thị đúng truy vấn hiện tại. **Tiên quyết:** state tuần 09, phiên tuần 10 và endpoint `GET /tasks` trong [API contract](../project/api-contract.md).

## 1. Bài giảng

### Debounce giảm request, không bảo đảm thứ tự

Debounce chờ người dùng ngừng gõ trong một khoảng thời gian trước khi gửi truy vấn. Nếu họ gõ `f`, `fl`, `flu` liên tục, có thể chỉ cần gửi `flu`. Nhưng request `f` đã gửi trước đó vẫn có thể về sau `flu`. Vì vậy debounce và chống response lỗi thời là hai trách nhiệm khác nhau. Hủy timer chỉ hủy lần khởi động tiếp theo; nó không tự hủy một HTTP request đang chạy.

Dùng mã thế hệ tăng dần cho truy vấn. Mỗi request chụp giá trị hiện tại, chỉ được cập nhật state nếu nó còn là truy vấn mới nhất. Ví dụ phần lõi, cần tích hợp thêm trạng thái loading/error của bạn:

```dart
int generation = 0;

Future<void> search(String query) async {
  final requestGeneration = ++generation;
  try {
    final page = await repository.search(query: query);
    if (requestGeneration != generation) return;
    applyPage(page);
  } catch (error, stack) {
    if (requestGeneration != generation) return;
    showSearchError(error, stack);
  }
}
```

`repository`, `applyPage` và `showSearchError` thuộc controller. Bỏ qua lỗi cũ cũng quan trọng như bỏ qua dữ liệu cũ. Nếu controller bị hủy, cần vô hiệu hóa hoặc hủy công việc theo cơ chế vòng đời đã chọn.

### Truy vấn là một bộ giá trị

Kết quả phụ thuộc cả từ khóa, trạng thái, tài khoản và cách sắp xếp, không chỉ `q`. Đổi một thành phần làm cursor cũ không còn hợp lệ. Hãy xem truy vấn như một khóa gồm các giá trị đã chuẩn hóa; reset danh sách/cursor theo chính sách rõ ràng khi khóa đổi. Đừng tự lowercase dữ liệu nếu backend có ngữ nghĩa tìm kiếm khác; tuân theo contract.

### Cursor là thông tin server cấp

Với cursor pagination, client nhận `nextCursor` rồi gửi nguyên giá trị đó cho trang kế tiếp. Không tự tăng cursor như số trang và không phân tích định dạng nội bộ. Có ba trạng thái độc lập: đang tải trang đầu, đang tải thêm và đã hết trang. Lỗi tải thêm nên giữ các hàng đã có, hiển thị thử lại ở cuối danh sách.

Chống gọi tải thêm trùng bằng cờ đang tải hoặc cơ chế tương đương. Ghép trang theo ID ổn định; khi task trùng ID, áp dụng quy tắc cập nhật rõ ràng thay vì thêm một hàng nữa. Khử trùng không tự bảo đảm snapshot nhất quán nếu dữ liệu server thay đổi giữa hai lần đọc; giới hạn đó cần được hiểu khi thiết kế API thật.

### Kiểm thử thời gian bằng điều khiển kết quả

Test chờ thật một giây thường chậm và dễ không ổn định. `Completer` cho bạn quyết định request nào kết thúc trước. Với debounce có thể tiêm scheduler hoặc dùng công cụ điều khiển thời gian của môi trường test. Mục tiêu là kiểm tra hành vi, không kiểm tra số lần gọi một hàm nội bộ vô nghĩa.

## 2. Ba bài thực hành

### W11-L1 — Kết quả mới nhất thắng

Tạo fake repository trả hai future A và B. Gọi tìm `dart`, sau đó `flutter`; hoàn thành B trước rồi A. Đầu ra cuối cùng chỉ chứa kết quả `flutter`. Lặp lại với A trả lỗi sau B thành công; lỗi A không được che màn hình B. Thêm debounce khoảng 300 ms, ghi rõ đây là lựa chọn UX của bài.

### W11-L2 — Danh sách nhiều trang

Dùng dữ liệu tối thiểu 25 task, `limit=10`. Tải liên tiếp các trang bằng `nextCursor`; đầu ra có đúng 25 ID duy nhất. Bấm/cuộn kích hoạt tải thêm hai lần liên tiếp nhưng chỉ một request cho cursor đang tải. Trang ba lỗi phải giữ 20 hàng và có nút thử lại.

### W11-L3 — Đổi query giữa lúc tải

Trong lúc tải thêm `todo`, đổi sang `done`. Response trang `todo` đến muộn không được nối vào danh sách `done`. Lặp lại với đổi tài khoản và đóng màn hình. Nộp test bằng fake; dùng debug delay của mock để demo trực quan, không coi demo thay cho test.

## 3. Nghiệm thu và tự kiểm tra

- [ ] Response hoặc lỗi cũ không ghi đè truy vấn mới.
- [ ] Timer debounce được dọn đúng vòng đời.
- [ ] Tải thêm không chạy trùng cho cùng lượt đang xử lý.
- [ ] Đổi query làm vô hiệu cursor và response cũ.
- [ ] Lỗi tải thêm giữ các hàng đã tải.
- [ ] Kết thúc khi `nextCursor` là `null`, không dựa duy nhất vào số hàng.
- [ ] Các test cuộc đua không cần mạng hay sleep thật.

**Ba câu hỏi:** Debounce có ngăn response cũ không? Vì sao cursor cũ không dùng cho bộ lọc mới? Khử trùng ID có giải quyết mọi vấn đề phân trang không?

**15 giờ:** 3 giờ lý thuyết; 8 giờ ba lab; 3 giờ test thứ tự; 1 giờ demo bốn tình huống lỗi. **Nộp:** controller, test và bảng các chuyển trạng thái.

Đọc [Riverpod debounce/cancel](https://riverpod.dev/docs/how_to/cancel), [Dart Completer](https://api.dart.dev/dart-async/Completer-class.html), [gợi ý](../solutions/week-11.md).
