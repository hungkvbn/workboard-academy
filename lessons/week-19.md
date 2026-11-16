# Tuần 19 — Integration test và ranh giới tài khoản

**Đầu ra:** kiểm thử luồng tạo công việc xuyên UI, state, repository và API; kiểm thử quyền truy cập giữa hai tài khoản. **Tiên quyết:** tuần 18, mock API chạy được, dùng tài khoản học tập trong [hợp đồng API](../project/api-contract.md).

**Lịch 15 giờ:** 3 giờ học, 8 giờ làm lab, 3 giờ điều tra test thất bại, 1 giờ demo. Giữ một môi trường dữ liệu riêng cho integration test; không dùng dữ liệu cá nhân.

## Bài giảng

### Kiểm tra các bộ phận làm việc cùng nhau

Unit test có thể chứng minh parser đúng, widget test chứng minh nút lưu hoạt động, nhưng chúng chưa chứng minh response từ server đi xuyên toàn bộ ứng dụng đúng cách. Integration test kiểm tra luồng giữa các thành phần thật. Ví dụ: đăng nhập, tạo công việc, trở về danh sách, tải lại và thấy dữ liệu vừa tạo.

Test xuyên hệ thống chậm và dễ chịu ảnh hưởng môi trường hơn unit test. Chỉ chọn các hành trình có giá trị cao. Quy tắc lọc với hàng chục trường hợp vẫn nên nằm ở unit test; hành trình đăng nhập và lưu công việc là ứng viên phù hợp cho integration test. Không cần lặp lại mọi biến thể của cùng một quy tắc ở tất cả cấp độ.

### Dữ liệu kiểm thử phải có chủ sở hữu

Một test đáng tin có bước chuẩn bị dữ liệu, hành động và dọn dữ liệu. Dùng ID duy nhất cho mỗi lần chạy để các test không va nhau. Khi chạy một bộ test cần thứ tự, bạn dễ gặp tình huống chạy riêng thất bại nhưng chạy cả bộ lại thành công. Tốt hơn là mỗi test tạo dữ liệu nó cần.

```dart
// Trích đoạn minh họa: adapter API phải được hiện thực trước.
final created = await api.createTask(
  id: testTaskId,
  title: 'Kiểm tra lưu xuyên hệ thống',
);
try {
  final fetched = await api.listTasks();
  expect(fetched.items.any((t) => t.id == created.id), isTrue);
} finally {
  await api.deleteTask(created.id, version: created.version);
}
```

Đừng để lỗi dọn dữ liệu che mất lỗi kiểm tra ban đầu. Trong bộ test thật, ghi nhận lỗi cleanup riêng và giữ dấu vết để điều tra. Với thao tác cập nhật trước khi xóa, dùng version mới nhất thay vì version cũ.

### Authentication khác authorization

Authentication trả lời người gọi là ai. Authorization trả lời người đó được làm gì với tài nguyên này. UI ẩn nút sửa không tạo ra hàng rào bảo vệ API. Người dùng có thể gửi request trực tiếp với ID của công việc người khác; server vẫn phải kiểm tra quyền.

WorkBoard yêu cầu dữ liệu riêng theo `ownerId`. Tài khoản A tạo công việc, B không được đọc, sửa hoặc xóa công việc đó. Hệ thống có thể trả 403 hoặc 404 tùy hợp đồng; hãy kiểm tra đúng lựa chọn được công bố. Kiểm tra thêm đổi tài khoản trong cùng ứng dụng: cache và state của A không được xuất hiện trong phiên B.

## Thực hành

### W19-L1 — Hành trình quan trọng (3 giờ)

Viết integration test đăng nhập tài khoản 1, tạo công việc có tiêu đề duy nhất, thấy nó trên danh sách, mở chi tiết rồi sửa trạng thái. Tải lại dữ liệu và kiểm tra trạng thái được lưu. Đầu ra gồm lệnh chạy, yêu cầu thiết bị/backend, dữ liệu chuẩn bị và bằng chứng một lần chạy thành công từ trạng thái sạch.

### W19-L2 — Kiểm tra quyền bằng API (3 giờ)

Đăng nhập hai tài khoản bằng hai token riêng. A tạo công việc. B thử cập nhật và xóa ID đó; kiểm tra request bị từ chối và dữ liệu của A vẫn nguyên. Kiểm tra `GET /tasks` của B không chứa ID của A. Đăng xuất A trên UI rồi đăng nhập B; màn hình không được lóe dữ liệu A trong lúc đang tải.

### W19-L3 — Phiên hết hạn và lỗi mạng (2 giờ)

Mô phỏng token không hợp lệ hoặc phiên bị từ chối theo khả năng mock API. Xác định ứng dụng sẽ refresh một lần, yêu cầu đăng nhập lại hoặc hiển thị lỗi nào. Sau đó dùng chế độ lỗi local của backend để trả 503. Người dùng phải nhận được đường phục hồi, không mất nội dung đang soạn. Ghi giới hạn của mock so với auth production.

## Nghiệm thu

- [ ] Luồng chính chạy từ môi trường dữ liệu sạch và có hướng dẫn tái hiện.
- [ ] Test không cần một test trước đó tạo sẵn dữ liệu.
- [ ] Tài khoản B không sửa hoặc xóa được công việc của A.
- [ ] Bị từ chối không làm thay đổi dữ liệu của A.
- [ ] Đổi tài khoản không hiển thị dữ liệu phiên cũ.
- [ ] Lỗi phiên và 503 không tạo vòng retry vô hạn.

## Tự kiểm tra

1. Vì sao unit test repository không thay thế integration test?
2. Ẩn nút sửa đã chứng minh authorization chưa?
3. Vì sao dọn dữ liệu cần chú ý version của công việc?

Đọc [integration testing](https://docs.flutter.dev/testing/integration-tests). Xem [gợi ý](../solutions/week-19.md) sau khi đã chạy ít nhất một tình huống bị từ chối quyền.
