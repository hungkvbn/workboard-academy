# Tuần 30 — Thử nghiệm beta và ưu tiên từ phản hồi

**Mục tiêu:** quan sát người dùng hoàn thành công việc thật, chuyển phản hồi thành quyết định và kiểm chứng cải tiến. **Tiên quyết:** bản beta ổn định, có hướng dẫn cài và dữ liệu thử. **15 giờ:** 3 giờ học và chuẩn bị, 8 giờ thực hiện ba lab, 3 giờ kiểm tra bản sửa, 1 giờ tổng hợp.

## Bài giảng

### 1. Quan sát hành vi thay vì hỏi người dùng có thích không

Một người có thể khen ứng dụng nhưng không tìm được nút lưu. Cho họ nhiệm vụ cụ thể: “Tạo công việc cho ngày mai, rồi tìm lại nó và đổi sang đã hoàn thành.” Không chỉ từng nút; quan sát họ dừng ở đâu, hiểu sai nhãn gì và có hoàn thành không.

Phân biệt sự kiện quan sát với diễn giải. “Người thử nhấn bộ lọc ba lần và hỏi dữ liệu đâu” là sự kiện. “Bộ lọc khó hiểu” là giả thuyết hợp lý cần kiểm chứng. Ghi môi trường, bản build và tác vụ để có thể tái hiện.

### 2. Dữ liệu định tính và số đo nhỏ

Với 3–5 người thử, bạn tìm được vấn đề hữu ích nhưng không có cơ sở suy rộng thành tỷ lệ của toàn bộ thị trường. Báo cáo “3 trong 4 người thử không tìm thấy cách bỏ bộ lọc” thay vì “75% người dùng không hiểu ứng dụng”.

Chọn số đo gần mục tiêu: hoàn thành tác vụ hay không, số lần cần trợ giúp, lỗi làm mất dữ liệu và thời gian theo cùng một kịch bản. Không thêm analytics khắp nơi chỉ để tạo biểu đồ. Có thể dùng quan sát thủ công trong khóa học. Nếu ghi hình hoặc thu thập thông tin nhận dạng, thống nhất phạm vi với người tham gia và chỉ giữ thứ cần cho bài học.

### 3. Ưu tiên theo ảnh hưởng và độ chắc chắn

Một bug làm mất công việc quan trọng hơn đổi màu icon dù ít người báo hơn. Xem xét mức tác động, số người bị ảnh hưởng trong dữ liệu đang có, khả năng phục hồi, độ chắc chắn của bằng chứng và chi phí sửa.

Ví dụ bảng quyết định:

| Vấn đề | Bằng chứng | Quyết định |
|---|---|---|
| Nhấn lưu hai lần tạo trùng | Tái hiện được, có video | Sửa trước bản beta tiếp theo |
| Không thấy trạng thái offline | 2/4 người hiểu nhầm đã sync | Cải thiện nhãn và kiểm tra lại |
| Muốn thêm chat | Một đề xuất, chưa rõ nhu cầu | Ghi lại, chưa thêm vào phạm vi |

Không dùng một công thức điểm để che một rủi ro dữ liệu nghiêm trọng. Với đề xuất lớn, hỏi người dùng đang cố hoàn thành việc gì trước khi chọn giải pháp.

### 4. Khép vòng phản hồi

Một vòng hoàn chỉnh là quan sát → giả thuyết → thay đổi → kiểm chứng lại. Khi sửa nhãn offline, hãy cho người thử một tác vụ offline tương tự và xem họ còn hiểu sai không. Đừng chỉ hỏi “bây giờ rõ hơn chưa”. Lưu cả kết quả không cải thiện để tránh nhầm công sức đã bỏ ra với tác động thật.

## Ba bài thực hành

### W30-L1 — Năm nhiệm vụ beta

Viết kịch bản gồm tạo, tìm, sửa hạn, làm offline và mở lại app. Mời 3–5 người nếu có thể; mỗi phiên khoảng 20 phút. Dùng dữ liệu giả. Nếu chưa có người thử, chạy pilot với bạn học và ghi rõ hạn chế, không bịa dữ liệu.

### W30-L2 — Backlog dựa trên bằng chứng

Tạo bảng issue với bước tái hiện, ảnh hưởng, độ chắc chắn, bản build và đề xuất. Chọn ba vấn đề ưu tiên; viết lý do trì hoãn ít nhất hai đề xuất khác. Mỗi bug cần tiêu chí xác nhận đã sửa.

### W30-L3 — Một vòng cải tiến

Sửa tối đa hai vấn đề có ảnh hưởng rõ. Chạy regression test, phát hành beta tiếp theo, lặp lại tác vụ liên quan. Đầu ra gồm kết quả trước/sau và những điều vẫn chưa biết; không chỉ ảnh UI mới.

## Nghiệm thu và bằng chứng

- [ ] Kịch bản không hướng dẫn người thử từng nút.
- [ ] Ghi rõ số người, điều kiện thử và hạn chế mẫu nhỏ.
- [ ] Phân biệt quan sát, giả thuyết và đề xuất giải pháp.
- [ ] Bug dữ liệu/độ tin cậy được cân nhắc trước thay đổi trang trí.
- [ ] Có một bản beta cải tiến và test bảo vệ hành vi đã sửa.
- [ ] Kết quả kiểm chứng lại được ghi, kể cả chưa tốt hơn.
- [ ] Không đưa thông tin cá nhân của người thử vào repository công khai.

Nộp kịch bản, bảng quan sát đã ẩn danh, backlog ưu tiên và [ghi chú phát hành](../templates/release.md).

## Tự kiểm tra

1. Vì sao câu hỏi “Bạn thấy app tốt không?” cho ít thông tin hành động?
2. Có thể kết luận gì và chưa thể kết luận gì từ bốn người thử?
3. Làm sao biết một thay đổi UI giải quyết được vấn đề đã quan sát?

Đọc [Flutter accessibility](https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility) và [Android app quality](https://developer.android.com/docs/quality-guidelines/core-app-quality). [Gợi ý tuần 30](../solutions/week-30.md).
