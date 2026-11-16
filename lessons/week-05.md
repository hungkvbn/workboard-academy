# Tuần 05 — State, lifecycle và biểu mẫu

**Mục tiêu:** người dùng tạo và sửa công việc qua giao diện mà không mất dữ liệu nháp hoặc gây lỗi vòng đời. **Tiên quyết:** màn hình danh sách tuần 04 và hàm validation tuần 01. Tiếp tục [starter Flutter](../starter/flutter/README.md).

**Ngân sách 15 giờ:** 3 giờ học và chạy ví dụ; 8 giờ lab; 3 giờ test/debug; 1 giờ demo. Đầu ra gồm form, trạng thái đang lưu và bằng chứng đóng màn hình giữa thao tác bất đồng bộ tại `evidence/week-05/`.

## Bài giảng

### 1. State là dữ liệu có thể làm giao diện khác đi

Tiêu đề người dùng đang nhập, bộ lọc đang chọn và trạng thái đang lưu đều là state. Đặt state ở nơi nhỏ nhất có đủ trách nhiệm quản lý nó. Một form sở hữu dữ liệu nháp; danh sách công việc đã lưu thuộc màn hình hoặc thành phần quản lý cao hơn. Không sửa task gốc mỗi khi gõ nếu nút Hủy phải bỏ thay đổi.

```dart
bool _isSaving = false;

void markSaving() {
  setState(() {
    _isSaving = true;
  });
}
```

Đây là đoạn nằm trong lớp State. Callback của `setState` thực hiện cập nhật đồng bộ; không đặt callback `async` vào đó. Thực hiện thao tác bất đồng bộ ngoài callback, rồi cập nhật state khi có kết quả và màn hình vẫn còn tồn tại.

### 2. Lifecycle quyết định lúc tạo và giải phóng tài nguyên

`initState` chạy khi State được tạo; `build` có thể được gọi nhiều lần; `dispose` là lúc giải phóng tài nguyên State đang sở hữu. Nếu tạo TextEditingController trong `build`, mỗi lần build có thể tạo controller mới và làm mất văn bản hoặc vị trí con trỏ.

```dart
late final TextEditingController _titleController;

@override
void initState() {
  super.initState();
  _titleController = TextEditingController(text: widget.initialTitle);
}

@override
void dispose() {
  _titleController.dispose();
  super.dispose();
}
```

Ví dụ giả định widget có `initialTitle`. Nếu cùng State được dùng lại cho một task khác, cần xử lý thay đổi đầu vào có chủ đích, thường qua `didUpdateWidget` hoặc identity phù hợp. Đừng ghi đè bản nháp sau mỗi lần widget cha rebuild.

### 3. Validation khác với gửi dữ liệu

Form kiểm tra điều kiện tại thiết bị để phản hồi nhanh. Việc lưu vẫn có thể thất bại và về sau backend phải kiểm tra lại. `Form` cùng `GlobalKey<FormState>` cho phép gọi `validate`; validator trả null khi hợp lệ, trả thông báo khi sai. Quy tắc tiêu đề nên dùng chung hàm Dart đã kiểm thử.

### 4. Sau `await`, màn hình có thể đã đóng

Người dùng có thể bấm Back trong khi đang lưu. Khi future hoàn thành, State cũ không còn được cập nhật. Kiểm tra `mounted` trước `setState` hoặc tương tác với context của State sau khoảng bất đồng bộ. Điều này ngăn dùng UI đã hủy; nó không tự hủy tác vụ và không ngăn mọi race condition.

## Thực hành

### W05-L1 — Form tạo công việc

Tạo form gồm title, description, status và hạn tùy chọn. Dùng dữ liệu nháp riêng; title áp dụng quy tắc trim và 1–120. Nhấn Lưu khi rỗng phải hiện lỗi ngay cạnh trường; dữ liệu hợp lệ tạo WorkTask mới. Chưa cần API, có thể gọi callback nhận bản nháp đã hợp lệ.

### W05-L2 — Sửa và hủy

Mở form từ task `t-1`. Đổi tiêu đề rồi Hủy: task gốc phải giữ nguyên. Mở lại, đổi trạng thái và Lưu: bản kết quả phải đổi đúng trường cần sửa. Thêm hành vi xóa hạn; không dùng null vừa có nghĩa giữ nguyên vừa có nghĩa xóa. Nếu người dùng bấm lưu hai lần nhanh, chỉ tạo một thao tác đang chạy.

### W05-L3 — Lưu chậm và thất bại

Tiêm hàm save giả hoàn thành khi bạn điều khiển bằng Completer. Thử thành công, lỗi, và đóng màn hình trước khi hoàn thành. Trong lúc chờ, nút Lưu bị vô hiệu hóa và có nhãn đang lưu. Lỗi giữ nguyên nội dung form và cho thử lại. Ghi lại vì sao `mounted` cần nhưng chưa thay thế việc quản lý vòng đời tác vụ.

## Nghiệm thu

- [ ] Validator dùng lại logic Dart, không có hai quy tắc tiêu đề khác nhau.
- [ ] Controller được tạo và dispose đúng nơi.
- [ ] Parent rebuild không xóa văn bản đang nhập.
- [ ] Hủy không thay đổi task gốc.
- [ ] Lưu thất bại giữ bản nháp và có thể thử lại.
- [ ] Nhấn liên tiếp không phát hai lần lưu đồng thời.
- [ ] Đóng form trong khi lưu không gây `setState after dispose`.

## Tự kiểm tra

1. Vì sao không đặt `await` trong callback `setState`?
2. `mounted` giải quyết vấn đề gì và không giải quyết vấn đề gì?
3. Vì sao cần tách bản nháp khỏi task đang hiển thị trong danh sách?

Đọc [StatefulWidget](https://api.flutter.dev/flutter/widgets/StatefulWidget-class.html), [Form validation](https://docs.flutter.dev/cookbook/forms/validation), [TextEditingController](https://api.flutter.dev/flutter/widgets/TextEditingController-class.html). Xem [gợi ý](../solutions/week-05.md) khi đã thử các tình huống.
