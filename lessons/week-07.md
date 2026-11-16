# Tuần 07 — Danh tính widget, danh sách và rebuild

**Mục tiêu:** sửa các lỗi giữ nhầm state trong danh sách và sử dụng DevTools để kiểm chứng giả thuyết. **Tiên quyết:** danh sách, form và điều hướng tuần 04–06. Chưa cần tối ưu nâng cao hoặc state management bên ngoài Flutter.

**Ngân sách 15 giờ:** 3 giờ bài giảng; 8 giờ lab; 3 giờ debug có ghi chép; 1 giờ demo. Nộp một video ngắn tái hiện lỗi trước/sau và một ghi chú DevTools trong `evidence/week-07/`.

## Bài giảng

### 1. Widget, Element và State có vai trò khác nhau

Widget là cấu hình bất biến. Element là vị trí và liên kết được Flutter duy trì trong cây; State gắn với StatefulElement để giữ dữ liệu qua nhiều lần build. RenderObject tham gia layout và paint khi cần. Không cần viết RenderObject lúc này, nhưng cần biết tạo widget mới không đồng nghĩa tạo lại mọi state hoặc vẽ lại toàn bộ màn hình.

Flutter đối chiếu widget mới với phần đang tồn tại, có xét kiểu widget và key. Khi danh sách đổi thứ tự, identity trở nên quan trọng. Nếu vô tình gắn state vào vị trí thay vì công việc, bản nháp hoặc trạng thái mở rộng có thể chuyển sang hàng khác.

### 2. Key trả lời “đây có còn là cùng một phần tử không?”

```dart
ListView(
  children: [
    for (final task in tasks)
      TaskRow(key: ValueKey(task.id), task: task),
  ],
)
```

Đoạn này giả định TaskRow là widget của bạn. Key ổn định theo ID giúp nhận diện hàng khi danh sách thay đổi. Key cần nằm ở mức con trực tiếp đang được sắp xếp; đặt key sâu trong Row nhưng bên ngoài còn một wrapper không key có thể không giải quyết lỗi mong muốn. Với builder và thao tác reorder, cần xem xét thêm `findChildIndexCallback` để ánh xạ key về index mới.

`UniqueKey()` tạo trong mỗi lần build cho biết mọi lần đều là phần tử khác, có thể làm mất State. Dùng key theo index cũng không thể nhận diện công việc khi index thay đổi. Key không thay thế model: trạng thái nghiệp vụ như done phải thuộc dữ liệu công việc, không chỉ nằm trong checkbox cục bộ.

### 3. Rebuild không luôn là vấn đề hiệu năng

`setState` báo rằng cấu hình UI có thể đổi. Flutter vẫn có các bước đối chiếu và xử lý riêng cho layout, paint. Đếm rebuild chỉ là một tín hiệu, không phải kết luận ứng dụng chậm. Tách widget theo phần thay đổi, dùng constructor const khi hợp lệ và giữ tác dụng phụ khỏi build.

```dart
// Có thể tái sử dụng cấu hình này khi cha rebuild.
const Padding(
  padding: EdgeInsets.all(12),
  child: Text('Công việc hôm nay'),
)
```

`const` không tự chữa ảnh quá lớn, truy vấn chậm hoặc danh sách tải toàn bộ dữ liệu. Đo đúng vấn đề trước khi đổi kiến trúc.

### 4. DevTools biến phỏng đoán thành bằng chứng

Dùng Inspector để tìm widget và constraints; dùng debugger để đặt breakpoint; theo dõi rebuild khi cần kiểm tra phạm vi cập nhật. Số liệu thời gian trong debug mode không đại diện hiệu năng bản phát hành. Tuần hiệu năng sẽ đo ở profile mode; tuần này tập trung tìm quan hệ giữa thao tác và cây widget.

## Thực hành

### W07-L1 — Tái hiện lỗi identity

Tạo danh sách nhỏ ba TaskRow có trạng thái mở rộng hoặc bản nháp cục bộ. Mở task B rồi đảo thứ tự danh sách không key; ghi lại state gắn vào hàng nào. Thêm key theo ID ở đúng cấp và kiểm tra lại. Với danh sách nhỏ có `children` cụ thể, bạn dễ quan sát identity trước khi chuyển sang builder.

### W07-L2 — Danh sách lớn và bộ lọc

Sinh 1.000 task mẫu, hiển thị bằng ListView.builder, thêm bộ lọc trạng thái. Chuyển status của một task không được làm task khác đổi checkbox. Nếu cần giữ local state qua reorder trong builder, bổ sung ánh xạ key/index theo API. Không tạo toàn bộ widget bằng `map(...).toList()` trước khi truyền vào builder.

### W07-L3 — Điều tra một rebuild

Đặt một bộ đếm thao tác tạm thời hoặc dùng công cụ theo dõi rebuild. Thay đổi bộ lọc và mở một hàng; ghi phần nào rebuild và vì sao. Tách một phần tĩnh thành widget riêng, kiểm tra lại. Xóa log debug gây nhiễu khỏi sản phẩm sau khi ghi bằng chứng.

## Nghiệm thu

- [ ] Giải thích được widget khác Element/State ở điểm nào.
- [ ] Lỗi identity được tái hiện trước khi sửa.
- [ ] Key ổn định theo ID, không tạo UniqueKey trong mỗi build.
- [ ] Done là dữ liệu nghiệp vụ của đúng task.
- [ ] Danh sách lớn tạo hàng theo nhu cầu.
- [ ] Không gọi đọc file, request hoặc submit trong build.
- [ ] Kết luận debug ghi rõ quan sát, không suy ra tốc độ release từ debug mode.

## Tự kiểm tra

1. Vì sao key theo index không phù hợp khi đảo thứ tự task?
2. `const` bảo đảm điều gì và không bảo đảm điều gì?
3. Mọi rebuild có dẫn đến paint toàn màn hình không?

Đọc [Key](https://api.flutter.dev/flutter/foundation/Key-class.html), [ListView.builder](https://api.flutter.dev/flutter/widgets/ListView/ListView.builder.html), [Flutter Inspector](https://docs.flutter.dev/tools/devtools/inspector). Xem [gợi ý](../solutions/week-07.md).
