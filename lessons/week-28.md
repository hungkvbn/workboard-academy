# Tuần 28 — Quan sát hệ thống, migration và diễn tập sự cố

**Mục tiêu:** tìm được nguyên nhân một lỗi từ bằng chứng, giảm tác động và sửa mà không làm mất dữ liệu. **Tiên quyết:** có bản beta truy được commit và schema cục bộ đã version hóa. **15 giờ:** 3 giờ học, 8 giờ lab, 3 giờ diễn tập và kiểm tra, 1 giờ viết báo cáo.

## Bài giảng

### 1. Crash reporting và log trả lời câu hỏi khác nhau

Crash report giúp biết lỗi, stack trace, phiên bản và môi trường. Log theo luồng giúp hiểu các sự kiện trước lỗi. Cả hai chỉ hữu ích khi gắn đúng version và không chứa dữ liệu nhạy cảm. Một thông báo “request failed” không đủ; ghi mã lỗi, loại thao tác, thời gian và request ID nếu hệ thống có hỗ trợ.

Dùng các trường có cấu trúc thay vì ghép token, email hoặc tiêu đề công việc vào chuỗi log. Ví dụ sự kiện an toàn hơn:

```dart
logger.event('task_sync_failed', {
  'operation': 'update',
  'errorCode': 'version_conflict',
  'attempt': 2,
  'appVersion': buildVersion,
});
```

Đây là giao diện minh họa, không phải API của một package cụ thể. Bạn cần chọn hoặc viết adapter tương ứng. Lỗi đã được xử lý như mất mạng không nhất thiết là crash; tránh ghi mọi retry thành một sự cố nghiêm trọng riêng.

### 2. Từ triệu chứng đến giả thuyết kiểm chứng được

Khi người dùng nói “mất công việc”, có nhiều khả năng: đang xem bộ lọc khác, đăng nhập tài khoản khác, migration lỗi, sync ghi đè hoặc server từ chối. Đầu tiên bảo toàn bằng chứng và xác định phạm vi ảnh hưởng. Sau đó tái hiện trên dữ liệu thử, tìm một giả thuyết có thể bị chứng minh sai, rồi mới thay code.

Một báo cáo lỗi tốt ghi bước thực hiện, kết quả mong đợi, kết quả thực tế, version và điều kiện mạng. Khi chưa tái hiện được, đánh dấu điều chưa biết. Không viết nguyên nhân như sự thật chỉ vì thấy một stack trace có vẻ liên quan.

### 3. Migration là một phép biến đổi dữ liệu

Migration phải được kiểm tra từ schema cũ sang mới với dữ liệu đại diện, gồm giá trị thiếu và dữ liệu chờ đồng bộ. Dùng transaction khi cơ sở dữ liệu hỗ trợ để tránh trạng thái nửa cũ nửa mới. Xác định cách phục hồi khi migration thất bại: giữ dữ liệu gốc, báo lỗi rõ và thử lại phù hợp; không tự xóa database để “hết crash”.

Thêm cột có default phù hợp dễ hơn thay nghĩa một trường. Khi thay cách biểu diễn trạng thái, cần ánh xạ tất cả giá trị cũ và quyết định xử lý giá trị không nhận diện. Version của record phục vụ concurrency không thay thế version schema database.

### 4. Khôi phục dịch vụ trên mobile

Bạn thường không thể ép mọi thiết bị đã cập nhật quay về binary cũ. Các lựa chọn thực tế là dừng rollout, tắt tính năng qua cấu hình đã thiết kế, phục hồi backend khi an toàn hoặc phát hành bản sửa tiến tới. Mỗi lựa chọn có giới hạn; một cờ remote không cứu được app crash trước khi tải cờ.

Postmortem tập trung vào cơ chế gây lỗi và hệ thống phòng ngừa, không tìm người để đổ lỗi. Phân biệt biện pháp giảm tác động ngay với biện pháp ngăn tái diễn lâu dài.

## Ba bài thực hành

### W28-L1 — Theo dấu lỗi

Gắn adapter quan sát vào auth và sync. Cố ý gây lỗi timeout, conflict và một exception trong môi trường test. Đầu ra: có thể phân biệt ba lỗi và truy về version; log không có token, mật khẩu hoặc nội dung công việc.

### W28-L2 — Migration có dữ liệu cũ

Tạo fixture schema trước với ba công việc và một outbox item. Nâng schema bằng một thay đổi nhỏ có ích, như metadata đồng bộ. Kiểm tra count, giá trị nghiệp vụ, owner và pending operation trước/sau; mô phỏng thất bại giữa quy trình.

### W28-L3 — Diễn tập 60 phút

Nhờ người khác hoặc dùng kịch bản tự tạo: bản mới gây duplicate khi retry. Viết timeline, xác định phạm vi, chọn biện pháp giảm tác động, tạo regression test rồi sửa. Ghi rõ đây là diễn tập nếu chưa có sự cố thật.

## Nghiệm thu và bằng chứng

- [ ] Error report gắn đúng version và môi trường.
- [ ] Log được kiểm tra để loại token và dữ liệu riêng tư.
- [ ] Migration test bắt đầu từ schema cũ thực sự.
- [ ] Pending outbox không biến mất hoặc đổi chủ sau nâng cấp.
- [ ] Có regression test tái hiện lỗi của diễn tập.
- [ ] Kế hoạch khôi phục phù hợp hạn chế phân phối mobile.
- [ ] Postmortem tách sự thật, giả thuyết và hành động tiếp theo.

Nộp [báo cáo sự cố](../templates/incident.md) và [checklist release](../templates/release.md) đã bổ sung kiểm tra ngăn lỗi lặp lại.

## Tự kiểm tra

1. Lỗi mất mạng được xử lý có nên ghi như crash không?
2. Vì sao xóa database khi migration lỗi là giải pháp nguy hiểm?
3. “Rollback mobile” có những giới hạn nào?

Đọc [Flutter error handling](https://docs.flutter.dev/testing/errors), [Drift migrations](https://drift.simonbinder.eu/migrations/) và [Firebase Crashlytics for Flutter](https://firebase.google.com/docs/crashlytics/get-started?platform=flutter). [Gợi ý tuần 28](../solutions/week-28.md).
