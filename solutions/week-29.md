# Gợi ý và đáp án tuần 29

## Đáp án tự kiểm tra

1. Client có thể bị sửa hoặc người dùng gọi API trực tiếp. Server phải xác thực người gọi và kiểm tra quyền trên tài nguyên trong mỗi thao tác liên quan.
2. Spike giới hạn thời gian để giảm một điều chưa biết và kết thúc bằng kết luận/bằng chứng; code thử nghiệm có thể bị bỏ. Tính năng hoàn chỉnh cần nghiệm thu, test, vận hành và bảo trì.
3. Khi rủi ro quan trọng chưa được giải quyết, phụ thuộc ngoài chưa sẵn sàng hoặc thời gian cố định không đủ cho phần bắt buộc. Chia phạm vi giữ nguyên các bất biến như quyền và dữ liệu, không cắt chúng để chạy demo.

## Gợi ý lab

- **W29-L1:** dùng bảng tác nhân × thao tác. “Chỉ chủ nhóm được xóa” cần cả trường hợp owner thành công và member gọi thẳng API bị từ chối.
- **W29-L2:** fake có thể biểu diễn membership thay đổi trong khi client offline. Khi sync, trả một lỗi quyền rõ ràng; UI không tự biến lỗi này thành thành công.
- **W29-L3:** cùng một tiêu chí so sánh hai lựa chọn: độ dễ hiểu cho người dùng, số chỗ kiểm tra quyền, chi phí truy vấn và khả năng thay đổi sau này. Đừng so sánh một phương án được chăm chút với một phương án cố tình yếu.

## Ví dụ sửa yêu cầu

Mơ hồ: “Member không được xóa việc.”

Có thể kiểm chứng:

> Với user B là member của workspace W, khi B gửi yêu cầu xóa task T thuộc W, server trả lỗi forbidden, task T không đổi và client hiển thị thông báo không có quyền. Quy tắc vẫn đúng nếu B gọi API ngoài ứng dụng.

Thêm trường hợp B từng là owner hoặc quyền bị đổi giữa lúc mở màn hình và nhấn xóa. Chọn một nguồn kiểm tra quyền hiện tại phía server; không tin role gửi trong request body. Với bộ học hiện tại, đây là contract/prototype extension, không phải khả năng đã có của mock API.
