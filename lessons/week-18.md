# Tuần 18 — Widget test và khả năng tiếp cận

**Đầu ra:** bộ widget test cho biểu mẫu và màn hình danh sách; bản ghi kiểm tra chữ lớn, bàn phím và trình đọc màn hình. **Tiên quyết:** tuần 17, UI có thể nhận dữ liệu giả mà không gọi backend.

**Lịch 15 giờ:** 3 giờ đọc và thử ví dụ, 8 giờ làm ba lab, 3 giờ sửa lỗi và kiểm thử trên thiết bị, 1 giờ demo. Phần thời gian thêm dùng để nhờ người khác thao tác ứng dụng mà không được hướng dẫn.

## Bài giảng

### Test widget quan sát hành vi

Widget test dựng một phần giao diện trong môi trường kiểm thử. Bạn tìm phần tử, nhập dữ liệu, nhấn nút và kiểm tra màn hình thay đổi. Đừng kiểm tra cây widget chi tiết chỉ vì biết cách triển khai. Người dùng quan tâm thông báo lỗi và công việc được lưu; việc nội bộ có bao nhiêu `Container` thường không phải hợp đồng cần giữ.

```dart
await tester.enterText(
  find.byKey(const Key('task-title')),
  '   ',
);
await tester.tap(find.text('Lưu'));
await tester.pump();
expect(find.text('Vui lòng nhập tiêu đề'), findsOneWidget);
expect(fakeRepository.savedTasks, isEmpty);
```

Đoạn minh họa giả định bạn đã dựng màn hình với fake repository. Test xác nhận cả phản hồi nhìn thấy được và việc dữ liệu sai không đi xuống repository. `Key` ổn định hữu ích cho phần tử tương tác; không cần gắn key vào mọi widget.

### Thời gian trong test phải được điều khiển

`pump()` yêu cầu xử lý một frame. `pump(Duration(...))` tiến thời gian kiểm thử, phù hợp khi đang kiểm tra debounce hoặc animation cụ thể. `pumpAndSettle()` tiếp tục bơm frame đến khi không còn frame được lên lịch; nó có thể timeout nếu màn hình có animation lặp liên tục. Khi repository vẫn đang chờ, hãy kiểm tra trạng thái loading rồi chủ động hoàn tất fake, thay vì gọi `pumpAndSettle()` vô điều kiện.

Test rời màn hình trước khi request hoàn tất giúp phát hiện cập nhật state sau dispose. Nên kiểm tra hành vi qua fake có thể điều khiển thời điểm hoàn thành. Chờ một số giây “đủ lâu” làm bộ test chậm và khó tin cậy.

### Khả năng tiếp cận là yêu cầu sử dụng

Một biểu tượng thùng rác không có nhãn có thể khó hiểu với người dùng trình đọc màn hình. Nút bị bàn phím che khiến người dùng không hoàn thành tác vụ. Chữ lớn có thể làm layout cố định bị tràn. Vì thế accessibility gồm ngữ nghĩa, vùng tương tác, thứ tự focus và khả năng thích ứng, không chỉ màu sắc.

Widget test bắt được một phần vấn đề. Kiểm tra semantics và guideline tự động hữu ích, nhưng vẫn cần thử TalkBack hoặc VoiceOver trên thiết bị. Với trạng thái hoàn thành công việc, dùng cả chữ hoặc biểu tượng có nhãn; đừng để màu là tín hiệu duy nhất.

## Thực hành

### W18-L1 — Biểu mẫu đáng tin (3 giờ)

Tạo test cho tiêu đề rỗng, chỉ có khoảng trắng, tiêu đề hợp lệ và nhấn lưu liên tiếp. Fake lưu có thể bị trì hoãn. Trong lúc lưu, hành vi phải ngăn gửi trùng và vẫn truyền đạt trạng thái đang xử lý. Nếu lưu thất bại, nội dung đã nhập phải còn nguyên để người dùng thử lại. Đầu ra gồm test và video ngắn hoặc ghi chú tái hiện.

### W18-L2 — Danh sách qua năm trạng thái (3 giờ)

Dựng màn hình lần lượt với loading, empty, success, error và refreshing khi đã có dữ liệu. Xác định trước liệu refreshing giữ dữ liệu cũ hay thay bằng loading toàn màn hình. Kiểm tra nút thử lại thực sự gọi hành vi tải; lỗi không làm ứng dụng quay về trạng thái trống khó hiểu. Không dùng request thật trong bài này.

### W18-L3 — Đọc và thao tác được (2 giờ)

Thử màn hình rộng 320 logical pixels và text scaling lớn, chẳng hạn 200%, như một tình huống stress. Mở bàn phím, đi qua form, lưu và quay lại. Bật trình đọc màn hình trên thiết bị, kiểm tra nhãn nút xóa, trạng thái hoàn thành và thứ tự đọc. Ghi ít nhất ba quan sát, sửa vấn đề có ảnh hưởng cao nhất.

## Nghiệm thu

- [ ] Validation sai không tạo request và thông báo xuất hiện gần trường liên quan.
- [ ] Lỗi lưu không xóa nội dung người dùng đã nhập.
- [ ] Không dùng chờ thực tế tùy ý để làm test “ổn định”.
- [ ] Có test ngăn gửi trùng và test thử lại sau lỗi.
- [ ] Không overflow trong cấu hình màn hình/chữ đã ghi nhận.
- [ ] Người dùng trình đọc màn hình nhận biết được hành động và trạng thái chính.

## Tự kiểm tra

1. Vì sao `pumpAndSettle()` có thể timeout với loading spinner?
2. Khi nào key hữu ích hơn tìm bằng chữ?
3. Tại sao kiểm tra semantics tự động chưa thay thế kiểm thử trên thiết bị?

Đọc [widget testing](https://docs.flutter.dev/cookbook/testing/widget/introduction) và [accessibility](https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility). Đối chiếu [đáp án](../solutions/week-18.md) sau khi lưu kết quả lab.
