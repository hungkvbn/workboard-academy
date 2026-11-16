# Tuần 04 — Widget, layout và constraints

**Mục tiêu:** dựng màn hình WorkBoard từ mô hình dữ liệu và tự chẩn đoán lỗi bố cục. **Tiên quyết:** hiểu WorkTask, collections và hàm Dart. Khởi tạo môi trường theo [starter Flutter](../starter/flutter/README.md); phần này dùng dữ liệu mẫu trong bộ nhớ.

**Ngân sách 15 giờ:** 3 giờ bài giảng và ví dụ; 8 giờ ba lab; 3 giờ thử nhiều kích thước và sửa lỗi; 1 giờ demo. Lưu ảnh chụp hai kích thước màn hình và nhật ký debug ở `evidence/week-04/`.

## Bài giảng

### 1. Widget là mô tả giao diện

Widget mô tả cấu hình UI ở một thời điểm. Nó không phải một phần tử màn hình mà bạn sửa trực tiếp như đổi thuộc tính DOM. Hàm `build` trả một cây widget phù hợp với dữ liệu hiện tại. Bắt đầu bằng StatelessWidget khi phần giao diện chỉ phụ thuộc dữ liệu truyền vào.

```dart
class TaskTitle extends StatelessWidget {
  const TaskTitle({super.key, required this.title});
  final String title;

  @override
  Widget build(BuildContext context) {
    return Text(title, maxLines: 2, overflow: TextOverflow.ellipsis);
  }
}
```

Đoạn này cần import `package:flutter/material.dart`. Một widget riêng tạo tên cho ý nghĩa giao diện, giúp tái sử dụng và kiểm thử. Chưa cần tách mỗi `Padding` thành một file; hãy tách theo trách nhiệm và phần có khả năng thay đổi riêng.

### 2. Constraints quyết định kích thước hợp lệ

Widget cha truyền giới hạn xuống; widget con chọn kích thước trong giới hạn; cha quyết định vị trí. Đây là mô hình để suy luận khi một widget không có kích thước như mong đợi. `width: 500` là mong muốn trong giới hạn cha, không phải mệnh lệnh vượt qua mọi giới hạn.

```dart
Row(
  children: [
    const Icon(Icons.task_alt),
    const SizedBox(width: 8),
    Expanded(child: Text(longTitle)),
  ],
)
```

Trong ngữ cảnh có `longTitle`, `Expanded` dành phần chiều ngang còn lại cho văn bản. Nó chỉ dùng trong Flex như Row/Column. Đặt Expanded trong một trục không có giới hạn hữu hạn có thể gây lỗi; chữa bằng hiểu constraints thay vì thêm nhiều lớp widget ngẫu nhiên.

### 3. Bố cục cuộn cần biết phần nào được giới hạn

Một Column chứa thanh lọc và ListView thường cần Expanded quanh danh sách để danh sách nhận chiều cao còn lại. Nếu cho ListView vào Column không giới hạn chiều cao phù hợp, Flutter không biết vùng nhìn của danh sách. `shrinkWrap` có mục đích riêng và thêm chi phí; không dùng nó như thuốc chữa mọi lỗi.

### 4. Theme và khoảng cách tạo tính nhất quán

Lấy kiểu chữ và màu từ Theme giúp giao diện thay đổi đồng bộ. SafeArea bảo vệ nội dung khỏi vùng hệ thống; Padding tạo khoảng cách có chủ đích. Tách dữ liệu mẫu khỏi widget để sau này chuyển sang API mà không viết lại bố cục.

## Thực hành

### W04-L1 — Thẻ công việc

Tạo TaskCard nhận title, status và dueAt. Đầu vào gồm tiêu đề ngắn, dài 200 ký tự để stress layout, hạn null và hạn có giá trị. Hiển thị trạng thái bằng nhãn chữ, không chỉ bằng màu. Đầu ra không overflow; tiêu đề dài được giới hạn hai dòng trong danh sách, chi tiết vẫn đọc được toàn bộ sau này.

### W04-L2 — Màn hình danh sách

Dựng Scaffold, AppBar, thanh lọc giả và danh sách 30 task mẫu. Dùng `ListView.builder` để tạo hàng theo nhu cầu. Khi danh sách rỗng, hiển thị thông điệp và nút thêm; nút có thể chưa điều hướng ở tuần này nhưng callback phải được truyền rõ ràng.

### W04-L3 — Phòng thí nghiệm constraints

Cố ý tạo ba lỗi: Row có tiêu đề dài không Expanded; ListView nằm trong Column không có chiều cao hợp lệ; hộp có chiều rộng lớn hơn cha. Với mỗi lỗi, ghi constraints liên quan, sửa tối thiểu và chụp kết quả. Chạy ở chiều rộng khoảng 360 và 800 logical pixels; không chỉ kiểm tra emulator mặc định.

## Nghiệm thu

- [ ] Có widget riêng cho TaskCard nhận dữ liệu qua constructor.
- [ ] Danh sách 30 mục cuộn được; thanh tiêu đề không trôi ngoài ý định.
- [ ] Tiêu đề dài không gây sọc overflow.
- [ ] Trạng thái vẫn hiểu được khi không phân biệt màu.
- [ ] Trường hợp không có task có UI riêng.
- [ ] Không hardcode chiều cao màn hình để vá lỗi layout.
- [ ] Giải thích bằng lời được ba lỗi constraints đã sửa.

## Tự kiểm tra

1. Vì sao yêu cầu width của widget con không luôn được đáp ứng?
2. Khi nào ListView trong Column cần Expanded?
3. Vì sao nên truyền dữ liệu vào TaskCard thay vì để TaskCard tự đọc danh sách toàn cục?

Đọc [Widget fundamentals](https://docs.flutter.dev/learn/pathway), [Understanding constraints](https://docs.flutter.dev/ui/layout/constraints), [Layout](https://docs.flutter.dev/ui/layout). Xem [gợi ý](../solutions/week-04.md) sau khi tự sửa.
