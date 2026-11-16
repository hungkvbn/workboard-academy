# Tuần 03 — Future, Stream và lỗi bất đồng bộ

**Mục tiêu:** đọc/ghi dữ liệu mà không nhầm thứ tự hoàn thành và xử lý lỗi đúng vị trí. **Tiên quyết:** model và kho dữ liệu tuần 02 hoạt động. Tiếp tục dự án Dart; chưa cần Flutter.

**Ngân sách 15 giờ:** 3 giờ đọc và chạy ví dụ; 8 giờ cho ba lab; 3 giờ test/debug; 1 giờ demo. Cuối tuần lưu bản JSON mẫu, kết quả test và ghi chú một lỗi bất đồng bộ tại `evidence/week-03/`.

## Bài giảng

### 1. Future là lời hứa về một kết quả

Một hàm đọc file không có nội dung file ngay lúc được gọi. Nó trả `Future<String>` để đại diện cho một kết quả hoặc lỗi đến sau. `await` tạm dừng phần tiếp theo của hàm bất đồng bộ cho đến khi future hoàn thành; các sự kiện khác vẫn có thể được xử lý.

```dart
Future<String> loadLabel() async {
  final value = await Future<String>.delayed(
    const Duration(milliseconds: 20),
    () => 'WorkBoard',
  );
  return value.toUpperCase();
}
```

Hàm này trả future ngay, không trả chuỗi ngay. Thêm `async` vào một vòng lặp tính toán nặng không tự chuyển vòng lặp sang isolate khác. Công việc CPU dài vẫn có thể chặn isolate hiện tại; tuần hiệu năng mới tập trung vào đo và phân tách tác vụ nặng.

### 2. Tuần tự và đồng thời là quyết định nghiệp vụ

Nếu B cần kết quả A, phải chờ A. Nếu hai lần đọc độc lập, có thể khởi động cả hai trước khi đợi. `Future.wait` thu thập kết quả, nhưng không tự hủy tất cả tác vụ còn lại khi một tác vụ lỗi. Không dùng đồng thời cho hai thao tác ghi cùng file nếu chưa có chiến lược phối hợp.

```dart
Future<List<String>> loadBoth(
  Future<String> Function() readTasks,
  Future<String> Function() readSettings,
) {
  return Future.wait([readTasks(), readSettings()]);
}
```

Truyền các hàm đọc vào ví dụ giúp thay bằng fake trong test. Bạn có thể kiểm soát lần đọc nào kết thúc trước mà không cần mạng hoặc ổ đĩa thật.

### 3. Lỗi đi qua future cần được chờ và bắt

`try` chỉ bao quanh lời gọi không đủ nếu future bị bỏ quên. Đặt `await` trong `try`, phân loại lỗi để phản ứng phù hợp. JSON hỏng khác với file chưa tồn tại: file mới có thể khởi tạo danh sách rỗng, còn file hỏng cần được giữ lại để điều tra hoặc phục hồi. Trả danh sách rỗng cho mọi lỗi có thể khiến lần lưu tiếp theo xóa dữ liệu cũ.

### 4. Stream mô tả nhiều sự kiện theo thời gian

Thông báo thay đổi công việc có thể xảy ra nhiều lần, vì vậy dùng Stream phù hợp hơn Future. Subscription là một tài nguyên có vòng đời: đăng ký lúc cần, hủy khi không còn người sử dụng. Phân biệt sự kiện dữ liệu, sự kiện lỗi và kết thúc stream. Không tạo controller chỉ để thay thế một hàm gọi trực tiếp đơn giản.

## Thực hành

### W03-L1 — Repository JSON bất đồng bộ

Thêm `load` và `save` cho danh sách WorkTask. Ghi ngày bằng ISO UTC; đọc trạng thái bằng quy tắc enum rõ ràng. Đầu vào là hai task, một có hạn và một không hạn; sau lưu rồi tải, dữ liệu nghiệp vụ phải giữ nguyên. Khi file chưa tồn tại, lần tải đầu trả danh sách rỗng. Khi nội dung JSON hỏng, báo lỗi và không ghi đè file tự động.

### W03-L2 — Phòng thí nghiệm thứ tự hoàn thành

Viết fake repository với hai kết quả được điều khiển bằng `Completer`. Khởi động A rồi B, hoàn thành B trước A, ghi lại thứ tự gọi và thứ tự nhận. Sau đó mô phỏng hai lần lưu cần thực hiện tuần tự. Đầu ra là nhật ký sự kiện và test chứng minh thứ tự thực sự, không phải phỏng đoán từ thứ tự dòng code.

### W03-L3 — Theo dõi thay đổi và đóng tài nguyên

Tạo luồng phát số lượng công việc sau mỗi thao tác thêm/xóa. CLI đăng ký và in số lượng mới. Thử thêm hai task, xóa một task, rồi hủy subscription; sự kiện sau khi hủy không được in. Đóng controller ở cuối chương trình và xử lý lỗi phát ra có chủ đích.

## Nghiệm thu

- [ ] Mọi thao tác cần hoàn thành trước khi thoát đều được chờ.
- [ ] Round-trip JSON giữ title, status, ownerId, version và thời điểm.
- [ ] File thiếu và file hỏng có hành vi khác nhau.
- [ ] Lỗi tải không bị biến thành thành công rỗng một cách âm thầm.
- [ ] Có test hoàn thành request theo thứ tự đảo ngược.
- [ ] Test unit dùng fake; test file dùng thư mục tạm riêng và dọn dẹp.
- [ ] Subscription/controller được đóng theo vòng đời.

## Tự kiểm tra

1. Đánh dấu một hàm là `async` có làm tính toán nặng chạy ở nơi khác không?
2. Vì sao `try { save(); }` có thể không bắt được lỗi của `save`?
3. Khi nào Future không diễn tả đủ yêu cầu và cần Stream?

Đọc [Async/await](https://dart.dev/libraries/async/async-await), [Streams](https://dart.dev/libraries/async/using-streams), [Concurrency](https://dart.dev/language/concurrency). Xem [gợi ý](../solutions/week-03.md) sau khi thử.
