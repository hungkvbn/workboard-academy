# Tuần 32 — Bảo vệ dự án và xây kế hoạch phát triển tiếp

**Mục tiêu:** chứng minh năng lực bằng một sản phẩm, giải thích các quyết định và xác định khoảng trống tiếp theo. **Tiên quyết:** hoàn thành các tiêu chí cốt lõi hoặc ghi rõ phần còn thiếu. **15 giờ:** 3 giờ ôn lý thuyết, 8 giờ hoàn thiện hồ sơ/demo, 3 giờ diễn tập đánh giá, 1 giờ lập kế hoạch tiếp theo.

## Bài giảng

### 1. Demo tốt chứng minh một chuỗi hành vi

Một màn hình đẹp không đủ chứng minh ứng dụng đáng tin cậy. Hãy kể một tác vụ xuyên suốt: đăng nhập, tạo công việc, sửa khi offline, đóng ứng dụng, mở lại, khôi phục mạng và kiểm tra trên thiết bị thứ hai. Sau đó cố ý tạo conflict và giải thích cách người dùng xử lý.

Chuẩn bị dữ liệu, tài khoản và phiên bản demo; có kịch bản dự phòng khi mạng không dùng được. Dự phòng giúp thể hiện chức năng đã làm, nhưng phải nói rõ khi đang dùng fake hoặc bản ghi thay vì backend thật. Không dựng video để che một yêu cầu chưa hoạt động.

### 2. Giải thích quyết định bằng bối cảnh

Khi được hỏi “tại sao dùng repository?”, câu trả lời tốt liên hệ với thay đổi cần hỗ trợ: thử dữ liệu fake, đọc cache và remote, kiểm tra lỗi mà không dựng UI. Nêu chi phí: thêm abstraction và cần giữ giao kèo giữa các implementation.

Dùng cấu trúc: vấn đề → lựa chọn → bằng chứng → đánh đổi → khi nào xem xét lại. Với mỗi quyết định chính, chuẩn bị một phương án khác hợp lý. Ví dụ một app rất nhỏ có thể chưa cần nhiều lớp; một hệ thống có nhiều nguồn dữ liệu lại cần ranh giới rõ hơn.

### 3. Phân biệt mức tự chủ với số công cụ đã học

Đánh giá từng năng lực theo bốn mức: làm khi có hướng dẫn; tự làm tình huống thông thường; xử lý lỗi/kiểm thử/phát hành; dẫn dắt lựa chọn và hỗ trợ người khác. Không cộng điểm UI để bù một lỗ hổng làm mất dữ liệu hoặc bỏ qua quyền truy cập.

Hoàn thành chương trình tạo bằng chứng kỹ thuật và thói quen tốt. Năng lực senior còn cần nhiều vòng chịu trách nhiệm với sản phẩm, đồng nghiệp và ràng buộc thực tế. Hồ sơ phải phân biệt sản phẩm có người dùng thật với diễn tập, review thật với tự review và nền tảng đã chạy với nền tảng mới thiết kế.

### 4. Kế hoạch tiếp theo bắt đầu từ khoảng trống

Chọn hai điểm yếu tác động lớn nhất, không mua thêm hàng loạt khóa học. Nếu debug còn dựa vào đoán, luyện điều tra lỗi có trace và regression test. Nếu thiếu làm việc nhóm, tìm dự án chung có review và giao việc thật. Nếu chưa vận hành, tiếp tục beta qua nhiều phiên bản, nhận phản hồi và theo dõi sự cố.

Mỗi mục tiêu tiếp theo cần đầu ra, thời hạn dự kiến và người hoặc bằng chứng đánh giá. “Học kiến trúc” quá rộng; “viết đề xuất cho một thay đổi dữ liệu, nhận review rồi triển khai có migration test” có thể kiểm chứng.

## Ba bài thực hành

### W32-L1 — Hồ sơ hoàn thành

Tập hợp README chạy dự án, sơ đồ luồng dữ liệu, ADR, test report, báo cáo hiệu năng, release notes và một incident report. Thêm bảng yêu cầu đã đạt/chưa đạt, link bằng chứng và giới hạn. Người khác phải tìm được cách chạy mà không hỏi lại bạn.

### W32-L2 — Bảo vệ 45 phút

Demo 15 phút, giải thích kiến trúc 10 phút, xử lý câu hỏi 10 phút, nhận một yêu cầu thay đổi nhỏ và đề xuất cách làm 10 phút. Nhờ một lập trình viên review; nếu chưa có, ghi hình tự bảo vệ rồi tự chấm bằng [rubric](../project/rubric.md), ghi rõ tính chất tự đánh giá.

### W32-L3 — Kế hoạch 90 ngày

Chọn hai khoảng trống từ rubric. Lập ba mốc 30 ngày có deliverable: một thay đổi thật, một vòng review và một lần phát hành/đánh giá. Giữ dự án có người dùng hoặc tham gia codebase nhóm thay vì chỉ bắt đầu demo mới.

## Nghiệm thu cuối

- [ ] App chạy theo hướng dẫn trên nền tảng đã khai báo.
- [ ] Luồng cốt lõi có test và bằng chứng cả tình huống lỗi.
- [ ] Offline/retry không tạo mất dữ liệu hoặc trùng không kiểm soát.
- [ ] Quyền truy cập được thực thi đúng nơi; mock local được ghi rõ giới hạn.
- [ ] Báo cáo hiệu năng có điều kiện đo và số liệu thực tế.
- [ ] Có bằng chứng release, migration và xử lý một sự cố/diễn tập.
- [ ] Hồ sơ phân biệt hoàn thành, chưa làm và chưa kiểm chứng.
- [ ] Kế hoạch tiếp theo dựa trên khoảng trống có bằng chứng.

## Tự kiểm tra

1. Quyết định kỹ thuật nào bạn sẽ thay đổi nếu quy mô hoặc đội ngũ khác đi?
2. Ba bằng chứng mạnh nhất và hai khoảng trống lớn nhất của bạn là gì?
3. Bạn cần trải nghiệm thực tế nào để tiến tới trách nhiệm senior?

Ôn [Flutter architecture](https://docs.flutter.dev/app-architecture), [testing](https://docs.flutter.dev/testing/overview), [performance](https://docs.flutter.dev/perf/best-practices) theo phần còn yếu. [Gợi ý tuần 32](../solutions/week-32.md).
