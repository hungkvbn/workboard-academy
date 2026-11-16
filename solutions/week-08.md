# Gợi ý và đáp án tuần 08

## Đáp án tự kiểm tra

1. HTTP 200 chỉ cho biết server báo thành công theo giao thức. Body có thể không đúng JSON hoặc không đúng schema ứng dụng; parser phải kiểm tra kiểu, trường và giá trị hợp lệ.
2. Hai request có thể hoàn thành khi màn hình vẫn mounted. Cần generation/request ID hoặc cơ chế hủy và kiểm tra quyền áp dụng kết quả; tuần 11 thực hành chi tiết.
3. Rỗng nghĩa lần đọc thành công và hiện không có bản ghi phù hợp. Mất kết nối nghĩa chưa biết dữ liệu hiện tại. Hiển thị rỗng khi lỗi sẽ khiến người dùng tưởng dữ liệu đã mất.

## Hint cho ba lab

- **W08-L1:** dùng đúng response `accessToken`; bearer phải đi trên endpoint tasks. Mỗi lần tạo mới cần key mới; retry cùng ý định giữ key và body cũ. Mock bắt đầu với database không có task.
- **W08-L2:** tách một hàm/class chỉ phụ trách HTTP và parsing. Đừng đưa `BuildContext` vào repository. Bắt đầu bằng một state enum và dữ liệu phù hợp, hoặc FutureBuilder với Future được giữ ngoài build. Tuần 09 chuyển phần điều khiển sang Riverpod.
- **W08-L3:** fake trả status và body được định trước; khẳng định loại lỗi và dữ liệu trả về, không kiểm tra chi tiết private implementation. Bổ sung fixture 204 khi bạn viết delete sau này.

## Worked example: parse 204 bị lỗi

Code lỗi:

```dart
final response = await client.delete(uri, headers: headers);
final result = jsonDecode(response.body); // 204 không có JSON
```

Cách xử lý cần theo hợp đồng endpoint:

```dart
final response = await client.delete(uri, headers: headers);
if (response.statusCode == 204) return;
// Các status còn lại được ánh xạ thành lỗi có nghĩa ở repository.
throw Exception('Xóa thất bại: HTTP ${response.statusCode}');
```

Ví dụ rút gọn này minh họa nhánh success; khi triển khai, parse error envelope để phân biệt 401, 404, 409 và transport error. Không hiển thị nguyên exception kỹ thuật cho người dùng.

## Cách tự chứng minh đã hiểu

Tắt server: UI phải báo lỗi kết nối, không báo danh sách rỗng. Sau đó chạy lại, đăng nhập lấy token mới và retry. Giải thích vì sao restart server giữ tasks nhưng làm token cũ mất hiệu lực trong mock này.
