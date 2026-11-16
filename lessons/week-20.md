# Tuần 20 — CI, review và bảo mật ứng dụng

**Đầu ra:** pipeline kiểm tra mỗi thay đổi; một PR có review và bản rà soát các ranh giới tin cậy. **Tiên quyết:** tuần 19, có bộ test chạy bằng lệnh và repo Git.

**Lịch 15 giờ:** 3 giờ học, 8 giờ lab, 3 giờ sửa pipeline và kiểm tra, 1 giờ trình bày PR. Nếu chưa dùng dịch vụ CI, chạy cùng quy trình bằng script local trước, rồi đưa lên hệ thống CI bạn chọn.

## Bài giảng

### CI là quy trình lặp lại được

Continuous integration chạy các kiểm tra khi có thay đổi, giúp phát hiện lỗi trước khi tích hợp. Một pipeline hữu ích cho WorkBoard cần cài đúng Flutter SDK, lấy dependency, kiểm tra format, phân tích mã và chạy test. Pin phiên bản SDK mà nhóm đã kiểm chứng; không để máy local và CI dùng hai tập công cụ không rõ nguồn gốc.

```sh
flutter pub get
dart format --output=none --set-exit-if-changed lib test
flutter analyze
flutter test
```

Đây là các bước cốt lõi, không phải toàn bộ pipeline phát hành. Integration test cần thiết bị/emulator và backend riêng, vì vậy có thể nằm ở job khác. Khi job thất bại, đọc bước và nguyên nhân; rerun nhiều lần đến khi xanh không sửa được test không ổn định. Cache giúp giảm thời gian, nhưng pipeline vẫn phải chạy đúng khi cache trống.

### Review tập trung vào rủi ro và khả năng hiểu

PR tốt giải thích vấn đề, thay đổi hành vi, kiểm thử và giới hạn còn lại. Reviewer nên có đủ ngữ cảnh để đánh giá mà không phải đọc cuộc trò chuyện trước đó. Tách refactor lớn khỏi thêm tính năng khi có thể; thay đổi quá rộng làm khó tìm lỗi và khó quay lại phiên bản trước.

Review không chỉ là chỉnh tên biến. Hỏi: thao tác nào có thể làm mất dữ liệu; request cũ có ghi đè dữ liệu mới; quyền được kiểm tra ở đâu; test nào chứng minh hành vi. Khi góp ý, nêu hệ quả và ví dụ. Phân biệt vấn đề cần sửa với lựa chọn phong cách để cuộc thảo luận rõ ràng.

### Ứng dụng client không phải nơi giữ bí mật backend

Mã và cấu hình đóng gói trong mobile app có thể được trích xuất. Biến môi trường khi build hoặc obfuscation không biến một khóa đặc quyền thành bí mật an toàn. Chỉ đưa cấu hình public phù hợp vào client; credential đặc quyền thuộc hệ thống server. Token người dùng cần được quản lý theo vòng đời và lưu trữ phù hợp nền tảng.

Log giúp điều tra nhưng cũng có thể lộ dữ liệu. Thay vì ghi toàn bộ header và body, ghi mã lỗi, request ID và thông tin đã lọc. Quyết định rõ dữ liệu nào cần xóa khi logout, dữ liệu offline chưa đồng bộ xử lý ra sao, và ai có quyền xem crash report. Những câu hỏi này gắn trực tiếp với hành vi sản phẩm.

## Thực hành

### W20-L1 — Pipeline từ máy sạch (3 giờ)

Viết script hoặc workflow chạy bốn bước cốt lõi. Ghi phiên bản SDK và dependency lockfile của ứng dụng. Tạo ba thay đổi thử: lỗi format, lỗi analyzer và test thất bại; chứng minh pipeline chặn từng thay đổi. Sau đó khôi phục và chạy từ checkout sạch. Đầu ra là pipeline, README chạy local và bằng chứng ba lỗi được phát hiện.

### W20-L2 — Review có lập luận (3 giờ)

Chọn một thay đổi nhỏ từ tuần 19, viết PR theo [mẫu](../templates/pr.md). Nhờ bạn học review; nếu chưa có người, tự review sau một khoảng nghỉ rồi ghi rõ đó là tự review. Nêu ít nhất một rủi ro dữ liệu, một câu hỏi về error handling và một nhận xét về test. Sửa hoặc giải thích từng ý bằng bằng chứng.

### W20-L3 — Kiểm tra dữ liệu nhạy cảm (2 giờ)

Rà repo, cấu hình build, log HTTP và crash report mẫu. Lập bảng dữ liệu → nơi lưu → người có quyền → thời điểm xóa. Thử logout rồi đăng nhập tài khoản khác. Kiểm tra không có token trong log, khóa đặc quyền trong client hoặc dữ liệu riêng của người trước hiển thị cho người sau.

## Nghiệm thu

- [ ] Pipeline chạy được khi cache trống và dừng khi có kiểm tra thất bại.
- [ ] Phiên bản SDK và cách cài dependency có thể tái tạo.
- [ ] Ba lỗi thử nghiệm bị phát hiện bởi đúng bước.
- [ ] PR giải thích thay đổi hành vi và kiểm thử đã chạy.
- [ ] Không đưa credential đặc quyền vào app hoặc repository.
- [ ] Bảng dữ liệu mô tả chính sách logout và log có lọc.

## Tự kiểm tra

1. Vì sao CI xanh chưa chứng minh ứng dụng không có lỗi?
2. `--dart-define` có bảo vệ được khóa server đặc quyền không?
3. Khi nào nên tách integration test khỏi job unit/widget test?

Đọc [continuous delivery](https://docs.flutter.dev/deployment/cd) và [obfuscation](https://docs.flutter.dev/deployment/obfuscate). Tham khảo [đáp án](../solutions/week-20.md) sau khi hoàn thành rà soát.
