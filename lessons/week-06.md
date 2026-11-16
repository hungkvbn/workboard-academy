# Tuần 06 — Điều hướng, responsive và accessibility

**Mục tiêu:** nối các màn hình thành luồng dùng được trên nhiều kích thước và với công cụ hỗ trợ tiếp cận. **Tiên quyết:** form tuần 05 hoạt động và hiểu truyền callback. Tuần này dùng Navigator của Flutter; router khai báo sẽ được học sau.

**Ngân sách 15 giờ:** 3 giờ lý thuyết; 8 giờ lab; 3 giờ kiểm thử thiết bị/kích thước; 1 giờ demo. Lưu sơ đồ luồng, ảnh cỡ chữ lớn và nhật ký thử trình đọc màn hình trong `evidence/week-06/`.

## Bài giảng

### 1. Điều hướng là một phần của trạng thái ứng dụng

Navigator quản lý ngăn xếp route. `push` mở route; `pop` đóng route hiện tại và có thể trả một kết quả. Màn hình tạo/sửa có thể trả bản nháp đã lưu; màn hình danh sách nhận kết quả rồi cập nhật dữ liệu. Hủy thường trả null. Cách này giúp form không phụ thuộc vào toàn bộ cấu trúc màn hình phía sau.

```dart
final editedTitle = await Navigator.of(context).push<String>(
  MaterialPageRoute(builder: (_) => const TitleEditor()),
);
if (!context.mounted || editedTitle == null) return;
// Cập nhật dữ liệu bằng kết quả nhận được.
```

Ví dụ giả định có widget TitleEditor. Khi Lưu, editor gọi `Navigator.pop(context, title)`; khi Hủy, gọi `Navigator.pop(context)`. Kết quả là future vì người dùng có thể ở màn hình mới rất lâu. Không truyền BuildContext xuyên qua tầng dữ liệu.

### 2. Thiết kế theo không gian sẵn có

Responsive không chỉ là chia tất cả số đo cho chiều rộng màn hình. Hãy quyết định bố cục phù hợp với nội dung: màn hình hẹp hiển thị danh sách rồi mở chi tiết; vùng rộng có thể đặt hai phần cạnh nhau. `LayoutBuilder` cung cấp constraints tại vị trí widget, hữu ích khi widget chỉ chiếm một phần màn hình.

```dart
LayoutBuilder(
  builder: (context, constraints) {
    final wide = constraints.maxWidth >= 720;
    return wide ? buildTwoPane() : buildSinglePane();
  },
)
```

720 là điểm bắt đầu để thử nghiệm cho bài, không phải chuẩn chung. Hai hàm trong ví dụ đại diện cho bố cục bạn xây. Thử cả kích thước sát hai phía của ngưỡng để phát hiện nhảy bố cục làm mất selection hoặc bản nháp.

### 3. Accessibility phải tồn tại trong hành vi

Một nút chỉ có biểu tượng cần tên có ý nghĩa. Trạng thái không thể chỉ phân biệt bằng màu. Thứ tự focus nên theo thứ tự thao tác; text tăng kích thước không được che nút Lưu. Dùng các control chuẩn trước khi tự vẽ, vì control chuẩn đã cung cấp nhiều hành vi semantics và bàn phím.

```dart
IconButton(
  tooltip: 'Tạo công việc',
  onPressed: onCreate,
  icon: const Icon(Icons.add),
)
```

Tooltip giúp cung cấp nhãn cho nút biểu tượng này. Không bọc thêm nhiều lớp Semantics với cùng nhãn khiến trình đọc màn hình đọc lặp. Cần bật TalkBack hoặc VoiceOver để nghe trải nghiệm thực tế.

## Thực hành

### W06-L1 — Luồng danh sách, chi tiết, chỉnh sửa

Mở chi tiết theo ID task; từ đó mở form sửa. Lưu trả kết quả cập nhật; Hủy giữ dữ liệu cũ. Thử Back hệ thống, Back trên AppBar và nút Hủy. Nếu task không còn tồn tại, chi tiết hiển thị thông báo và đường trở lại danh sách thay vì ép null.

### W06-L2 — Hai bố cục, một dữ liệu

Xây bố cục một cột ở vùng hẹp và danh sách/chi tiết hai cột ở vùng rộng. Giữ cùng nguồn dữ liệu và selected task ID. Đầu vào là 20 task; đổi kích thước khi đang chọn task thứ 12 phải vẫn thể hiện đúng lựa chọn, không tự chọn task đầu tiên.

### W06-L3 — Kiểm tra tiếp cận

Thử ở chiều rộng 360, 720 và 1024 logical pixels; tăng cỡ chữ của hệ điều hành; mở bàn phím khi nhập description. Dùng trình đọc màn hình đi từ danh sách đến Lưu. Ghi ít nhất ba vấn đề thực sự tìm thấy và sửa; nếu không có, ghi các bước kiểm tra cụ thể cùng bằng chứng thay vì viết “đã test”.

## Nghiệm thu

- [ ] Lưu và Hủy trả kết quả khác nhau đúng thiết kế.
- [ ] Back hệ thống không làm mất task đã lưu.
- [ ] Task ID không tồn tại có UI xử lý riêng.
- [ ] Đổi kích thước không đổi task đang chọn ngoài ý muốn.
- [ ] Cỡ chữ lớn không làm nút quan trọng mất khả năng sử dụng.
- [ ] Nút biểu tượng có tên dễ hiểu; trạng thái có nhãn chữ.
- [ ] Đã thử ít nhất một trình đọc màn hình và ghi kết quả.

## Tự kiểm tra

1. Vì sao `Navigator.push` trả Future?
2. Khi nào LayoutBuilder phù hợp hơn lấy chiều rộng toàn màn hình?
3. Vì sao ảnh chụp giao diện đẹp chưa chứng minh accessibility tốt?

Đọc [Navigation basics](https://docs.flutter.dev/cookbook/navigation/navigation-basics), [Adaptive and responsive design](https://docs.flutter.dev/ui/adaptive-responsive), [Accessibility](https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility). Xem [gợi ý](../solutions/week-06.md).
