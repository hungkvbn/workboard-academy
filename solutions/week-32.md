# Gợi ý và tiêu chuẩn trả lời tuần 32

Tuần này không có một đáp án sản phẩm duy nhất. Tự đánh giá dựa trên bằng chứng, không chọn câu trả lời nghe cao cấp nhất.

## Tiêu chuẩn cho ba câu tự kiểm tra

1. Nêu bối cảnh hiện tại, quyết định, chi phí và ngưỡng xem xét lại. Ví dụ đồng bộ thủ công phù hợp beta nhỏ nhưng yêu cầu cập nhật nhiều người gần thời gian thực có thể cần một cơ chế khác và cách xử lý conflict rõ hơn.
2. Mỗi bằng chứng phải mở được hoặc tái hiện được: PR, test, artifact, báo cáo đo có điều kiện. Khoảng trống cần cụ thể như chưa thử migration từ bản N−2, chưa từng nhận review ngoài hoặc chưa kiểm chứng iOS.
3. Nêu trách nhiệm chưa trải qua: phối hợp backend/QA, xử lý sự cố thật, duy trì code nhiều phiên bản, ước lượng với ràng buộc và giúp đồng nghiệp tự chủ. Một dự án cá nhân không tự chứng minh tất cả.

## Gợi ý lab

- **W32-L1:** cho một người khác dùng README từ đầu trên môi trường sạch. Link bằng chứng theo yêu cầu, tránh một thư mục ảnh không biết ảnh nào chứng minh điều gì.
- **W32-L2:** chuẩn bị câu hỏi “Nếu bỏ mạng ngay sau khi server ghi nhưng client chưa nhận response thì sao?” và “Nếu quyền đổi trong khi offline thì sao?”. Câu trả lời phải khớp code, không chỉ thiết kế mong muốn.
- **W32-L3:** mỗi mốc 30 ngày có tiêu chí đạt và nơi nhận phản hồi. Nếu mục tiêu là teamwork, cần con người cùng làm thật; đọc thêm tài liệu về teamwork chỉ là bổ trợ.

## Ví dụ sửa một kết luận quá mức

Chưa đúng: “Đã chạy 32 tuần, biết Riverpod, Clean Architecture và CI/CD nên đã là senior.”

Có căn cứ: “Tôi tự xây và phát hành bản Android beta, có test cho luồng chính, giải quyết retry trùng bằng operation ID và đo cải thiện màn danh sách trên thiết bị X. Tôi chưa vận hành sản phẩm nhiều người dùng hoặc dẫn dắt thiết kế trong đội ngũ; 90 ngày tới sẽ nhận một feature trong dự án nhóm và theo nó qua hai lần phát hành.”

Bài học không phải hạ thấp kết quả, mà là trình bày đúng năng lực để người khác tin và giao trách nhiệm phù hợp. Mỗi vòng sản phẩm tiếp theo nên tạo thêm bằng chứng ở những điểm hiện còn thiếu.
