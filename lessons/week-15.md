# Tuần 15 — Thay đổi yêu cầu và đặt quy tắc nghiệp vụ đúng chỗ

**Đích đến:** tiếp nhận yêu cầu mới, làm rõ các tình huống biên và thay đổi WorkBoard mà không làm mất hành vi cũ. **Tiên quyết:** kiến trúc tuần 13, clock/fake và mô hình lỗi tuần 14.

## 1. Bài giảng

### Yêu cầu chưa phải đặc tả

“Thêm mục việc quá hạn” nghe đơn giản nhưng còn nhiều câu hỏi: task hoàn thành có bị tính không; chưa đặt hạn thì sao; đúng bằng thời điểm hiện tại thì sao; giờ server hay thiết bị; người dùng đang ở múi giờ nào? Trước khi code, viết ví dụ đầu vào và đầu ra. Ví dụ là cách phát hiện hai người đang hiểu khác nhau một câu ngắn.

Quy tắc dùng trong bài: một task quá hạn khi chưa `done`, có `dueAt`, và `dueAt` trước thời điểm đánh giá UTC. `dueAt` bằng thời điểm đánh giá không tính quá hạn. Màn hình chỉ hiển thị thời gian theo múi giờ người dùng; so sánh các thời điểm tuyệt đối. Nếu sản phẩm sau này dùng “hạn theo ngày” thay vì thời điểm, đó là mô hình nghiệp vụ khác cần quyết định riêng.

### Một quy tắc, nhiều người dùng

Danh sách, badge và báo cáo có thể cùng cần logic quá hạn. Nếu mỗi widget tự viết điều kiện, một nơi dùng `<=`, nơi khác dùng `<` và kết quả lệch nhau. Đặt quy tắc vào hàm hoặc model thuần có test. Không cần một service phức tạp cho một biểu thức, nhưng cần một nơi chịu trách nhiệm.

```dart
bool countsAsOverdue({
  required String status,
  required DateTime? dueAt,
  required DateTime now,
}) => status != 'done' &&
    dueAt != null &&
    dueAt.toUtc().isBefore(now.toUtc());
```

Ví dụ này nhận `now` thay vì đọc đồng hồ ẩn. Khi tính một danh sách, chụp `now` một lần để mọi hàng được đánh giá cùng thời điểm. Không gọi clock cho từng hàng nếu muốn một snapshot nhất quán ở ranh giới giây.

### Chuyển trạng thái và bất biến

Thêm yêu cầu: người dùng có thể đánh dấu hoàn thành và mở lại task. Hãy định nghĩa rõ mở lại chuyển về `todo` hay trạng thái trước đó. Trong bài này chọn `todo`; không tự tạo trường trạng thái cũ nếu contract chưa cần. Server vẫn kiểm tra version khi cập nhật, vì người khác hoặc thiết bị khác có thể sửa cùng task.

Khi network update thất bại, UI phải giữ dữ liệu đủ để phục hồi. Optimistic update là hiển thị kết quả dự kiến trước response, đổi lại cần rollback/reconcile và xử lý thao tác kế tiếp. Bạn có thể chọn chờ server ở tuần này; lựa chọn cần được giải thích theo độ phức tạp và UX, không theo xu hướng.

### Phạm vi hiển thị và phạm vi dữ liệu

Nếu mới tải 10 trong 100 task, đếm quá hạn trong 10 task rồi đặt nhãn “Tổng việc quá hạn” là sai ý nghĩa. Hoặc ghi rõ “trong danh sách đã tải”, hoặc dùng API tổng hợp có contract phù hợp. Chức năng mới có thể buộc thay API; đừng giấu giới hạn bằng một con số có vẻ chính xác.

## 2. Ba bài thực hành

### W15-L1 — Đặc tả bằng ví dụ

Viết bảng ít nhất tám trường hợp cho tính quá hạn: `null`, trước/đúng/sau now, `done`, hai cách biểu diễn cùng thời điểm, task của user khác và dữ liệu trang chưa tải hết. Chọn phạm vi badge. Đầu ra là tiêu chí nghiệm thu được người khác đọc và dự đoán kết quả không cần xem code.

### W15-L2 — Một quy tắc cho ba nơi

Thêm bộ lọc quá hạn, badge và thông tin ở màn hình chi tiết. Dùng cùng hàm nghiệp vụ và clock. Với fixture năm task trong đó hai task quá hạn hợp lệ, cả ba nơi phải thống nhất. Ghi rõ cách UI cập nhật khi thời gian trôi mà người dùng chưa chạm màn hình: refresh thủ công, timer có vòng đời hoặc cơ chế khác bạn chọn.

### W15-L3 — Hoàn thành và mở lại an toàn

Thêm thao tác `todo/doing → done` và `done → todo`. Test success, mạng lỗi và version conflict. Bấm liên tiếp không được làm response cũ ghi đè ý định mới hoặc gửi thao tác không kiểm soát. Chọn khóa nút khi đang lưu hoặc quản lý hàng đợi; ghi lý do trong PR.

## 3. Nghiệm thu và tự kiểm tra

- [ ] Có bảng ví dụ trước khi triển khai.
- [ ] Logic quá hạn chỉ có một định nghĩa dùng chung.
- [ ] Test có mốc đúng bằng giờ và `dueAt=null`.
- [ ] Hai biểu diễn timezone của cùng thời điểm cho cùng kết quả.
- [ ] Badge nói đúng phạm vi dữ liệu đã có.
- [ ] Mở lại task về `todo` theo đặc tả.
- [ ] Lỗi cập nhật không khiến UI báo thành công sai.
- [ ] Không thêm trường request ngoài contract hiện có.

**Ba câu hỏi:** Vì sao tính badge trên một trang có thể sai? Khi nào optimistic update đáng chi phí? Quy tắc theo “ngày” khác quy tắc theo “thời điểm” thế nào?

**15 giờ:** 3 giờ làm rõ yêu cầu; 8 giờ lab; 3 giờ regression; 1 giờ demo và giải thích trade-off. **Nộp:** bảng ví dụ, PR, test và phạm vi dữ liệu.

Đọc [Dart DateTime](https://api.dart.dev/dart-core/DateTime-class.html), [Flutter optimistic state](https://docs.flutter.dev/app-architecture/design-patterns/optimistic-state), [gợi ý](../solutions/week-15.md).
