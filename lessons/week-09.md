# Tuần 09 — State có chủ sở hữu, Riverpod và dữ liệu bất đồng bộ

**Đích đến:** từ màn hình gọi API tuần 08, tạo luồng dữ liệu dễ giải thích: repository trả dữ liệu, provider quản lý trạng thái, widget hiển thị. **Tiên quyết:** đã hiểu `setState`, `Future`, loading/error/success và JSON. Đọc [hợp đồng API](../project/api-contract.md) trước khi nối backend.

## 1. Bài giảng

### State thuộc về ai?

State là thông tin có thể thay đổi và ảnh hưởng đến hành vi. Nội dung ô nhập đang gõ chỉ cần tồn tại trong màn hình tạo công việc; danh sách công việc phải được nhiều màn hình quan sát. Đưa mọi thứ vào global state khiến vòng đời khó kiểm soát; giữ mọi thứ trong widget lại gây sao chép dữ liệu. Với mỗi state, hỏi: ai tạo, ai đọc, ai sửa, khi nào nó hết hạn? Quyết định vị trí lưu theo câu trả lời.

Một giá trị có thể tính từ state khác là **derived state**. Số công việc hoàn thành nên tính từ danh sách hiện tại. Lưu riêng cả danh sách và số lượng buộc bạn cập nhật hai nơi sau mỗi thao tác, dễ lệch nhau. Dữ liệu không thay đổi trực tiếp tại chỗ cũng giúp nhận biết thời điểm cần cập nhật.

### Quan sát khác với ra lệnh

Riverpod cung cấp provider làm điểm truy cập state hoặc dependency. `ref.watch` đăng ký quan sát để phần tiêu thụ cập nhật khi giá trị đổi; `ref.read` đọc tại một thời điểm, thường dùng khi xử lý hành động. `ref.listen` phục vụ phản ứng phụ như thông báo, cần dùng đúng vị trí theo tài liệu. Widget dựng giao diện không nên tự gọi API vô điều kiện trong `build()`.

Ví dụ dưới đây dùng API không sinh mã của `flutter_riverpod`:

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

class TaskFilter extends Notifier<String> {
  @override
  String build() => 'all';

  void select(String next) {
    if (!{'all', 'todo', 'doing', 'done'}.contains(next)) {
      throw ArgumentError.value(next, 'next');
    }
    state = next;
  }
}

final taskFilterProvider =
    NotifierProvider<TaskFilter, String>(TaskFilter.new);
```

Trong `ConsumerWidget`, dùng `ref.watch(taskFilterProvider)` để render bộ lọc; callback gọi `ref.read(taskFilterProvider.notifier).select('done')`. Bao ứng dụng trong `ProviderScope`. Việc chọn bộ lọc thuộc controller, còn màu của nút được suy ra trong widget.

### Async state không chỉ là một boolean

Hai biến `isLoading` và `hasError` có thể tạo tổ hợp vô nghĩa: vừa thành công vừa báo lỗi cũ. `AsyncValue<T>` mô tả loading, data hoặc error rõ ràng. `FutureProvider` phù hợp dữ liệu đọc bất đồng bộ; `AsyncNotifier` hữu ích khi cần hành động thay đổi dữ liệu. Chọn kiểu đơn giản đáp ứng bài toán trước.

Refresh còn có quyết định UX: giữ dữ liệu cũ trong lúc tải hay thay toàn bộ bằng spinner? Khi refresh thất bại, người dùng vẫn có thể đọc dữ liệu cũ, nhưng cần biết nó chưa cập nhật. Quyết định này phải hiện trong state và test, không bị giấu trong một `catch` trống.

## 2. Ba bài thực hành

### W09-L1 — Lập bản đồ và chuyển bộ lọc

Liệt kê tám state đang có trong WorkBoard, ghi owner, người đọc và thời điểm hủy. Chuyển bộ lọc trạng thái sang `Notifier`; giữ `TextEditingController` của form trong widget. Đầu vào mẫu gồm ba công việc ở ba trạng thái. Đầu ra khi chọn `done` là đúng một công việc và badge được suy ra từ danh sách.

### W09-L2 — Danh sách bất đồng bộ

Đưa tải công việc vào provider. Thêm thử lại và refresh. Dùng fake repository có ba chế độ: trả danh sách, trả rỗng, ném lỗi. Bản ghi quyết định một đoạn phải nêu rõ refresh giữ hay bỏ dữ liệu cũ. Không để mỗi lần bấm bộ lọc tạo request mới nếu đang lọc dữ liệu cục bộ.

### W09-L3 — Test chủ sở hữu state

Test filter mặc định, đổi filter và dữ liệu rỗng bằng `ProviderContainer` phù hợp phiên bản đã cài; luôn dispose container. Override repository bằng fake thay vì gọi mạng. Ghi một video: mở chi tiết, quay lại, refresh và lỗi; chỉ ra state nào được giữ.

## 3. Nghiệm thu và tự kiểm tra

- [ ] Mỗi state có một nơi chịu trách nhiệm ghi chính.
- [ ] Không lưu riêng một count có thể tính từ danh sách.
- [ ] Gọi API không nằm trực tiếp trong `build()`.
- [ ] Loading, empty, error và retry hiển thị được bằng fake.
- [ ] Refresh không làm mất bộ lọc đang chọn.
- [ ] Test không phụ thuộc mạng hoặc thời gian chờ thật.

**Ba câu hỏi:** Vì sao không thay mọi `watch` bằng `read`? Khi nào state cục bộ nên giữ trong widget? Refresh thất bại khi đã có dữ liệu khác gì lần tải đầu thất bại?

**15 giờ:** 3 giờ đọc và vẽ luồng; 8 giờ làm ba lab; 3 giờ test/debug; 1 giờ demo và ghi quyết định. Nếu còn 5 giờ, xem lại vòng đời provider, chưa thêm thư viện state thứ hai.

**Nộp:** PR, bản đồ state, test và demo. Đọc [Riverpod providers](https://riverpod.dev/docs/concepts2/providers), [testing providers](https://riverpod.dev/docs/how_to/testing), [lời giải và gợi ý](../solutions/week-09.md).
