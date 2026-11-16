# Gợi ý và đáp án — Tuần 04

## Đáp án tự kiểm tra

1. Cha quyết định phạm vi kích thước hợp lệ. Widget con phải chọn kích thước trong phạm vi đó; width là đầu vào cho quá trình layout chứ không vượt qua constraints.
2. Khi Column có chiều cao hữu hạn và danh sách cần nhận phần còn lại sau các thành phần khác. Nếu Column chính nó ở trong vùng cuộn không giới hạn chiều cao, thêm Expanded đơn thuần chưa giải quyết được bài toán.
3. Dữ liệu đầu vào rõ ràng giúp kiểm thử nhiều trường hợp, tái sử dụng, nhìn thấy phụ thuộc và thay nguồn dữ liệu về sau.

## Gợi ý lab

- **W04-L1:** dùng một Row gồm nội dung Expanded và nhãn phụ; đừng để mọi đoạn Text cùng đòi toàn bộ chiều ngang. Luôn kiểm tra tiêu đề dài hơn ví dụ đẹp trong thiết kế.
- **W04-L2:** trong body của Scaffold, Column thường có chiều cao hữu hạn. Đặt thanh lọc ở trên và Expanded(ListView.builder(...)) ở dưới. Dùng dữ liệu rỗng để kiểm tra nhánh empty.
- **W04-L3:** đọc dòng lỗi đầu tiên và cây widget liên quan. Ghi chiều nào là hữu hạn trước khi sửa. Dùng Flutter Inspector để nhìn kích thước thật.

## Sửa lỗi mẫu

Sai trong body của Scaffold:

```dart
Column(children: [
  const Text('Công việc'),
  ListView(children: const [Text('A'), Text('B')]),
])
```

Sửa cho danh sách chiếm phần chiều cao còn lại:

```dart
Column(children: [
  const Text('Công việc'),
  Expanded(
    child: ListView(children: const [Text('A'), Text('B')]),
  ),
])
```

Đây là lời giải theo ngữ cảnh cha có chiều cao hữu hạn, không phải quy tắc áp dụng mọi nơi. Nếu cần toàn trang cuộn chung với nội dung khác, bạn sẽ chọn một cấu trúc cuộn phù hợp thay vì lồng các vùng cuộn vô hạn.
