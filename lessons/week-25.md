# Tuần 25 — Lifecycle, quyền và giao tiếp với nền tảng

**Mục tiêu:** giải thích được chuyện gì xảy ra khi WorkBoard ra nền, xin quyền đúng lúc và gọi một khả năng Android qua platform channel. **Tiên quyết:** hoàn thành tuần 24; có thiết bị Android hoặc emulator. Nhánh iOS cần macOS/Xcode; nếu chưa có, ghi rõ chưa kiểm chứng iOS.

**Phân bổ 15 giờ:** 3 giờ học và chạy ví dụ; 8 giờ thực hiện ba lab; 3 giờ kiểm tra chuyển trạng thái và lỗi; 1 giờ ghi nhận kết quả. Phần thêm 5 giờ dành cho iOS hoặc kiểm tra trên thiết bị Android thứ hai.

## Bài giảng

### 1. Lifecycle của ứng dụng và của widget khác nhau

Một widget bị `dispose` khi rời cây giao diện; cả ứng dụng đi vào nền không đồng nghĩa mọi widget bị hủy. Hệ điều hành có thể dừng tiến trình mà không cho bạn một lần lưu cuối cùng. Vì vậy thao tác người dùng đã được xác nhận phải được ghi bền vững ngay trong luồng xử lý, không chờ `paused`.

Khi ứng dụng trở lại foreground, dữ liệu trên server có thể đã đổi. Gọi một hàm refresh có kiểm soát, tránh tạo nhiều request nếu trạng thái thay đổi liên tiếp. Dùng `AppLifecycleListener` hoặc `WidgetsBindingObserver`, và hủy listener đúng vòng đời. Ví dụ rút gọn:

```dart
late final AppLifecycleListener lifecycle;

void observeLifecycle() {
  lifecycle = AppLifecycleListener(
    onResume: () => repository.refreshIfStale(),
  );
}

void releaseLifecycle() => lifecycle.dispose();
```

Đây là ví dụ về vị trí trách nhiệm: repository quyết định dữ liệu đã cũ hay chưa; callback lifecycle chỉ báo một sự kiện. `observeLifecycle` được gọi khi khởi tạo đối tượng sở hữu, còn `releaseLifecycle` trong quá trình hủy nó. Không khởi tạo listener trong `build`.

### 2. Quyền là một trạng thái sản phẩm

Một tính năng cần quyền có ít nhất các tình huống: chưa hỏi, được cấp, bị từ chối và cần vào Settings để thay đổi. Không coi mọi lời từ chối là lỗi của người dùng. Nếu chưa có quyền thông báo, WorkBoard vẫn phải cho phép quản lý công việc.

Hỏi quyền khi người dùng bật chức năng nhắc việc; giải thích ích lợi trước khi mở hộp thoại hệ thống. Khai báo manifest hoặc thông tin iOS phù hợp không tự cấp quyền runtime. Các yêu cầu thay đổi theo nền tảng và phiên bản hệ điều hành, nên kiểm tra tài liệu đúng môi trường đang dùng. Không yêu cầu tất cả quyền ở lần mở đầu tiên.

### 3. Platform channel là một giao kèo

Dart gửi tên phương thức và dữ liệu được codec hỗ trợ; phía native trả kết quả hoặc lỗi. Hai phía phải thống nhất tên channel, tên method và hình dạng dữ liệu. Ví dụ Dart:

```dart
const channel = MethodChannel('workboard/device_info');
Future<String> readSystemVersion() async {
  return await channel.invokeMethod<String>('systemVersion') ?? 'unknown';
}
```

Bài tập sẽ tự triển khai Android handler trả `Build.VERSION.RELEASE`. Tính năng này không cần quyền nhạy cảm. Nếu thiếu handler, Dart có thể nhận `MissingPluginException`; nếu native chủ động báo lỗi, xử lý `PlatformException`. Bọc channel trong một interface để widget test sử dụng fake, không phụ thuộc máy thật.

### 4. Kiểm chứng từng nền tảng

Một plugin có tên trong `pubspec.yaml` không chứng minh ứng dụng hoạt động trên cả Android và iOS. Ghi rõ thiết bị, OS, phiên bản ứng dụng và kịch bản đã chạy. Với phần chưa có thiết bị, nộp thiết kế và danh sách cần kiểm chứng; không đánh dấu hoàn thành kiểm thử.

## Ba bài thực hành

### W25-L1 — Resume an toàn

Tạo công việc offline, chuyển ứng dụng ra nền rồi mở lại. Thêm log sự kiện không chứa dữ liệu riêng tư. Dữ liệu phải còn; resume chỉ kích hoạt tối đa một refresh đang chạy. Thử tiếp trường hợp dừng hẳn tiến trình rồi mở lại.

### W25-L2 — Luồng quyền

Làm màn hình “Nhắc việc” với trạng thái quyền và nút bật. Dùng fake permission adapter để tái hiện được cấp, từ chối và cần mở Settings. Đầu ra: ba trạng thái UI khác nhau; quản lý công việc luôn dùng được. Đối chiếu một luồng thật trên Android phù hợp phiên bản OS.

### W25-L3 — Channel nhỏ

Viết handler `systemVersion` trên Android và một `DeviceInfoGateway` ở Dart. Màn hình chẩn đoán hiển thị phiên bản hệ thống hoặc thông báo không lấy được dữ liệu. Viết test bằng fake trả thành công và ném lỗi; nếu có Mac, thêm nhánh iOS tương đương.

## Nghiệm thu và bằng chứng

- [ ] Công việc đã lưu còn sau khi tiến trình bị dừng.
- [ ] Resume liên tiếp không tạo các lần đồng bộ chồng nhau.
- [ ] Listener được tạo một lần và hủy đúng lúc.
- [ ] Từ chối quyền không chặn tính năng không liên quan.
- [ ] Channel có handler cho method hợp lệ và lỗi method không tồn tại.
- [ ] Test UI không gọi native thật; có ít nhất một bằng chứng chạy Android thật/emulator.
- [ ] Báo cáo ghi rõ iOS đã kiểm chứng hay mới thiết kế.

Nộp một PR, video hai kịch bản lifecycle, bảng trạng thái quyền và danh sách thiết bị đã thử. Dùng [mẫu PR](../templates/pr.md).

## Tự kiểm tra

1. Vì sao không nên chờ `paused` mới lưu dữ liệu người dùng?
2. Khác biệt giữa `MissingPluginException` và `PlatformException` là gì?
3. Quyền bị từ chối nên ảnh hưởng phần nào của WorkBoard?

Đọc [Flutter lifecycle](https://api.flutter.dev/flutter/dart-ui/AppLifecycleState.html), [platform channels](https://docs.flutter.dev/platform-integration/platform-channels) và [Android runtime permissions](https://developer.android.com/training/permissions/requesting). Sau khi làm, mở [gợi ý tuần 25](../solutions/week-25.md).
