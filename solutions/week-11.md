# Gợi ý tuần 11

## Đáp án tự kiểm tra

1. Debounce giảm tần suất bắt đầu truy vấn. Request đã bắt đầu vẫn có thể hoàn thành muộn. Cần hủy khi lớp mạng hỗ trợ và/hoặc kiểm tra thế hệ trước khi áp dụng kết quả.
2. Cursor gắn với tập kết quả và thứ tự của truy vấn. Trộn cursor `todo` với query `done` có thể trả sai trang hoặc bị server từ chối.
3. Khử trùng chỉ ngăn hiển thị hai hàng cùng ID. Dữ liệu thay đổi giữa các trang vẫn có thể gây thiếu hàng nếu server không bảo đảm snapshot. Cần biết contract và làm refresh khi phù hợp.

## Gợi ý lab

- **W11-L1:** lưu cả dữ liệu thành công và lỗi dưới cùng điều kiện thế hệ. Đừng chỉ kiểm tra request cuối ở nhánh `try`.
- **W11-L2:** lưu cursor mà request thực sự sử dụng; chỉ kết thúc trạng thái đang tải nếu request còn thuộc truy vấn hiện tại. Tạo test response trang sau chứa một ID đã có để kiểm tra cách merge.
- **W11-L3:** tăng generation ngay lúc ý định truy vấn đổi, không chờ debounce kết thúc. Nếu không, response của truy vấn trước có thể được áp dụng trong cửa sổ chờ 300 ms.

## Ví dụ sửa lỗi

```dart
void onQueryChanged(String next) {
  generation++; // Vô hiệu ngay mọi response cũ.
  debounceTimer?.cancel();
  currentQuery = next;
  final intentGeneration = generation;
  debounceTimer = Timer(const Duration(milliseconds: 300), () {
    if (intentGeneration != generation) return;
    loadFirstPage(next, intentGeneration);
  });
}
```

Đoạn này nằm trong controller đã có `Timer? debounceTimer`, query và generation. `loadFirstPage` không tự tạo một generation không khớp với tham số; kiểm tra cùng token trước khi ghi state. Khi dispose, cancel timer và vô hiệu generation. Dùng `Completer` hoàn thành B trước A để kiểm tra, không kỳ vọng mạng thực tế luôn tái hiện đúng thứ tự.
