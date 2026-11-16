# Tuần 23 — Đo hiệu năng giao diện bằng DevTools

**Đầu ra:** một báo cáo hiệu năng có baseline, giả thuyết, thay đổi và kết quả đo lại. **Tiên quyết:** tuần 22; ứng dụng có dữ liệu đại diện và chạy được trên thiết bị thật.

**Lịch 15 giờ:** 3 giờ học DevTools, 8 giờ làm lab, 3 giờ đo lại và kiểm tra hồi quy, 1 giờ trình bày kết quả. Nếu chưa có thiết bị thật, vẫn luyện đọc trace nhưng ghi rõ giới hạn của số liệu emulator.

## Bài giảng

### Đo đúng câu hỏi và điều kiện

“Ứng dụng chậm” chưa đủ cụ thể để sửa. Hãy xác định thao tác, thiết bị và loại chậm: cuộn bị giật, phản hồi nhập liệu chậm, truy vấn mất thời gian hay ảnh xuất hiện muộn. Dùng profile mode để đo hiệu năng Flutter trên thiết bị mục tiêu. Debug mode bổ sung kiểm tra và công cụ phục vụ phát triển nên không đại diện cho hành vi bản phát hành.

Ghi model thiết bị, hệ điều hành, tần số quét, phiên bản app, chế độ build, lượng dữ liệu và kịch bản thao tác. Giữ điều kiện tương đương giữa hai lần đo. Thiết bị nóng, tác vụ nền hoặc dữ liệu khác nhau có thể khiến bạn quy nhầm kết quả cho một thay đổi code.

### Frame có thời hạn

Màn hình 60 Hz cập nhật khoảng mỗi 16,7 ms; 120 Hz khoảng mỗi 8,3 ms. Đây là khoảng thời gian để giữ nhịp hiển thị, không phải lời hứa rằng mọi màn hình luôn đạt tốc độ đó. Flutter có công việc xây/layout/paint ở phía UI và rasterization ở phía raster. Đọc trace để tìm giai đoạn kéo dài; các giai đoạn có thể được pipeline, nên không suy diễn mọi trường hợp bằng cách cộng hai con số đơn giản.

Rebuild không đồng nghĩa toàn bộ màn hình bị vẽ lại, và một rebuild nhỏ không tự động là vấn đề. Chi phí phụ thuộc công việc thực hiện. Tìm bằng chứng về widget lớn, tính toán lặp trong `build`, layout tốn kém hoặc hiệu ứng render trước khi quyết định sửa.

### Danh sách chỉ nên dựng phần cần thiết

```dart
ListView.builder(
  itemCount: tasks.length,
  itemBuilder: (context, index) {
    final task = tasks[index];
    return TaskTile(
      key: ValueKey(task.id),
      task: task,
    );
  },
)
```

Builder giúp dựng item theo nhu cầu hiển thị thay vì tạo hàng nghìn widget trước. Key gắn state của item với danh tính công việc khi danh sách thay đổi; key không phải nút tăng tốc chung. Nếu chiều cao item thật sự cố định, bạn có thể thử cung cấp thông tin kích thước phù hợp rồi đo lại. Đừng ép chiều cao khi nội dung nhiều dòng hoặc chữ lớn cần thêm chỗ.

### Thay một yếu tố để kiểm tra giả thuyết

Giả thuyết tốt có dạng: “Bộ lọc đang chạy lại trên 10.000 công việc mỗi lần rebuild; chuyển việc lọc sang lúc input thay đổi sẽ giảm thời gian UI trong thao tác nhập.” Đo trước, sửa, đo lại cùng kịch bản. Nếu số liệu không cải thiện, ghi nhận kết quả và xét lại giả thuyết. Việc học được nguyên nhân đáng giá hơn giữ một tối ưu không có bằng chứng.

## Thực hành

### W23-L1 — Baseline có thể tái hiện (3 giờ)

Tạo fixture 10.000 công việc, tiêu đề dài/ngắn và trạng thái đa dạng. Định nghĩa kịch bản: mở danh sách, cuộn xuống, đổi bộ lọc, tìm kiếm rồi mở chi tiết. Chạy ít nhất ba lượt có điều kiện tương đương; tách lượt khởi động ban đầu khi cần. Lưu trace hoặc ảnh DevTools và số liệu trong [mẫu báo cáo](../templates/performance-report.md).

### W23-L2 — Tìm và sửa một điểm nghẽn (3 giờ)

Chọn một đoạn trace có vấn đề. Ghi giả thuyết trước khi sửa. Thử một thay đổi có cơ sở: builder, giảm tính toán trong build, thu hẹp vùng theo dõi state hoặc giảm công việc layout. Đo lại cùng dữ liệu và thao tác. Không ghép hàng loạt thay đổi khiến không biết cái nào tác động.

### W23-L3 — Hiệu năng không phá tính đúng (2 giờ)

Sau tối ưu, kiểm tra lọc, sắp xếp, trạng thái từng hàng, chữ lớn và thao tác liên tục. Đặc biệt thử đổi thứ tự danh sách khi một item đang có trạng thái cục bộ. Báo cáo cả thay đổi tốt lẫn chi phí mới như cache lớn hơn hoặc code phức tạp hơn.

## Nghiệm thu

- [ ] Báo cáo ghi thiết bị, build mode, dữ liệu và kịch bản.
- [ ] Có baseline và đo lại với điều kiện tương đương.
- [ ] Kết luận dựa trên trace hoặc số liệu, không chỉ cảm giác.
- [ ] Phân biệt thời gian UI, raster và thời gian chờ dữ liệu.
- [ ] Tối ưu không làm mất trạng thái hàng hoặc gây overflow khi tăng chữ.
- [ ] Giải thích được thay đổi nào được giữ, bỏ và vì sao.

## Tự kiểm tra

1. Vì sao số liệu debug mode không phù hợp để kết luận hiệu năng phát hành?
2. Key và builder giải quyết hai vấn đề khác nhau nào?
3. Vì sao ba lượt đo khác nhau mạnh có thể chưa đủ để kết luận?

Đọc [DevTools Performance view](https://docs.flutter.dev/tools/devtools/performance) và [performance best practices](https://docs.flutter.dev/perf/best-practices). Tham khảo [đáp án](../solutions/week-23.md).
