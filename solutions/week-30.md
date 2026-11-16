# Gợi ý và đáp án tuần 30

## Đáp án tự kiểm tra

1. Câu hỏi dễ nhận lời khen xã giao, không chỉ ra hành vi nào gây khó khăn. Nhiệm vụ cụ thể tạo bằng chứng về việc người dùng có đạt mục tiêu hay không.
2. Có thể phát hiện lỗi, hiểu nhầm và giả thuyết cần thử tiếp. Không nên suy rộng tỷ lệ thành thị trường hoặc khẳng định mọi loại người dùng đều gặp cùng vấn đề.
3. Lặp tác vụ tương đương với tiêu chí đã chọn trước; quan sát mức trợ giúp, sai sót hoặc hoàn thành. Kết hợp test kỹ thuật để đảm bảo bản sửa không phá luồng khác.

## Gợi ý lab

- **W30-L1:** pilot một phiên để sửa câu chữ nhiệm vụ. Nếu bạn phải giải thích nhiều, ghi lại lời giải thích thay vì âm thầm giúp rồi tính là hoàn thành độc lập.
- **W30-L2:** gắn mỗi issue với bằng chứng. “Khó dùng” cần chuyển thành hành vi cụ thể như không tìm thấy cách bỏ bộ lọc đang bật.
- **W30-L3:** giữ mục tiêu đo giống trước khi sửa. Nếu đổi cả nhiệm vụ và UI, khó biết yếu tố nào tạo khác biệt.

## Ví dụ sửa tiêu chí đánh giá

Yếu: “Làm offline banner đẹp hơn.”

Cụ thể: “Sau khi tạo task khi mất mạng, người thử xác định được task đang lưu trên máy và chưa sync mà không cần người hướng dẫn giải thích.”

Thay đổi thử nghiệm: hiển thị trạng thái `Đã lưu trên thiết bị · Chờ đồng bộ` gần thao tác vừa hoàn thành, đồng thời dùng trạng thái riêng cho lỗi cần người dùng xử lý. Test widget kiểm tra nội dung theo sync state; phiên usability kiểm tra ý nghĩa người dùng hiểu. Test widget xanh không tự chứng minh người dùng hiểu nhãn.
