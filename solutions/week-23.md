# Gợi ý và đáp án — Tuần 23

## Đáp án tự kiểm tra

1. Debug mode có overhead và cách biên dịch phục vụ phát triển. Nó hữu ích để debug nhưng không đại diện cho profile/release trên thiết bị mục tiêu. Vẫn cần đo đúng chế độ và ghi môi trường.
2. Builder tạo item khi cần, giảm việc dựng toàn bộ danh sách. Key giúp framework nhận dạng phần tử khi cập nhật cây, giữ state đúng với danh tính. Key không tự làm việc build tốn kém biến mất.
3. Có thể bị nhiễu bởi nhiệt độ, tác vụ nền, warm-up, cache hoặc thao tác không nhất quán. Cần kiểm tra điều kiện, lặp lại có kiểm soát và công bố độ dao động; đừng chọn riêng lần đẹp nhất.

## Gợi ý lab

- **W23-L1:** ghi cả số lượng item thực tế và độ dài nội dung. Nêu rõ online/offline để tránh so sánh một lượt có chờ mạng với một lượt toàn dữ liệu local.
- **W23-L2:** nếu frame chậm chủ yếu ở raster, chỉ thu hẹp listener state có thể không giải quyết. Xem hiệu ứng, clipping, ảnh hoặc công việc render phù hợp với trace.
- **W23-L3:** thử hoàn thành một công việc rồi đổi sort. Nếu trạng thái của hàng “nhảy” sang công việc khác, kiểm tra identity/key thay vì chỉ nhìn FPS.

## Ví dụ sửa lỗi

Sai khi danh sách lớn:

```dart
SingleChildScrollView(
  child: Column(
    children: tasks.map((t) => TaskTile(task: t)).toList(),
  ),
)
```

Đoạn này dựng toàn bộ item. Nếu màn hình phù hợp một danh sách cuộn, thử `ListView.builder` như bài giảng. Giữ key theo ID và kiểm tra lại layout với chữ lớn. Nếu có header hoặc nhiều phần cuộn, cân nhắc cấu trúc sliver phù hợp; không lồng danh sách scroll tùy tiện rồi bật `shrinkWrap` để che lỗi constraints. Đo trước/sau để xác nhận cải thiện trong ứng dụng của bạn.
