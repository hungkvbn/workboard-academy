# Gợi ý tuần 16

## Đáp án tự kiểm tra

1. ADR trả lời vì sao một quyết định được chọn trong bối cảnh cụ thể, cùng hệ quả. Hướng dẫn cài đặt giúp chạy hệ thống. Hai loại có thể liên kết nhưng không thay nhau.
2. Khi output đổi, khó biết đó là yêu cầu chủ ý hay regression do di chuyển cấu trúc. Chia bước giúp reviewer kiểm tra giả thuyết và rollback phạm vi phù hợp nếu cần.
3. Khi ràng buộc hoặc bằng chứng thay đổi: số người cùng phát triển tăng, yêu cầu offline xuất hiện, đo thấy bottleneck, dependency không còn đáp ứng. Ghi ADR mới thay thế bản cũ và liên kết lịch sử, không xóa lý do cũ như thể chưa từng tồn tại.

## Gợi ý lab

- **W16-L1:** mỗi lựa chọn phải có cơ hội được chọn thật. “Không xử lý lỗi” không phải đối thủ công bằng của “kiến trúc tốt”. So sánh constructor injection thuần với cấu hình provider trong bối cảnh cụ thể là một ví dụ có ích.
- **W16-L2:** chọn điểm đã làm bạn sửa nhiều nơi hoặc gây bug. Chỉ di chuyển file cho đẹp chưa chứng minh lợi ích. Ghi số caller bị ảnh hưởng trước/sau nếu điều đó phản ánh vấn đề.
- **W16-L3:** review phải có đường dẫn code và phản ví dụ. “Có thể response của A về sau khi login B; test nào bảo vệ?” hữu ích hơn “xử lý async chưa tốt”. Tự review vẫn có giá trị, nhưng không ghi là đã được đồng nghiệp chấp thuận.

## Ví dụ sửa một nhận xét review

**Nhận xét mơ hồ:** “Cách này không clean, dùng use case đi.”

**Nhận xét có thể kiểm chứng:** “Logic quá hạn đang tồn tại trong list và badge với điều kiện biên khác nhau. Khi `dueAt == now`, hai nơi cho kết quả khác. Hãy dùng chung quy tắc đã thống nhất ở W15-L1 và thêm test mốc bằng giờ. Có thể chỉ cần hàm thuần; chưa cần class mới.”

**Đáp án ADR tối thiểu:** bối cảnh một developer, test đã có, thời hạn beta; lựa chọn A giữ logic lặp và thêm test từng nơi, B dùng một hàm thuần, C tạo use-case layer; chọn B vì giải quyết lệch quy tắc với ít cấu trúc; hệ quả là module nghiệp vụ phải được dùng chung; xem lại khi quy tắc cần nhiều dependency hoặc điều phối nhiều repository. Đây là ví dụ về cách lập luận, không phải quyết định bắt buộc cho mọi dự án.
