# WorkBoard Academy — học Dart & Flutter bằng một dự án

**Dành cho:** người đã biết một ngôn ngữ lập trình, mới học Flutter. **Khối lượng:** 32 tuần × 15–20 giờ, khoảng 480–640 giờ. Đây là chương trình rèn năng lực xây và vận hành ứng dụng; hoàn thành không tự động tương đương chức danh senior.

## Bắt đầu ở đây

1. Đọc [đặc tả sản phẩm](project/brief.md) và [cách đánh giá](project/rubric.md).
2. Mở [bài tuần 01](lessons/week-01.md), học phần giảng rồi làm ba lab.
3. Chạy mã khởi đầu theo [Dart starter](starter/dart/README.md). Đến tuần 04 dùng [Flutter starter](starter/flutter/README.md).
4. Sau mỗi lab, ghi kết quả vào [nhật ký học](templates/learning-log.md). Chỉ đánh dấu hoàn thành khi có bằng chứng nghiệm thu.
5. Từ tuần 08 chạy [API giả lập](mock_api/README.md). Đây là dịch vụ trên máy của bạn để luyện tập, không phải backend production.
6. Khi tự làm xong, xem gợi ý trong `solutions/week-XX.md`. Đối chiếu cách suy nghĩ, không chỉ kết quả.

**Học trên nhiều máy hoặc đưa lên GitHub/GitLab:** đọc [hướng dẫn Git](project/git-and-multi-device.md). Tiến độ có thể lưu ở [tracking/workboard-progress.json](tracking/workboard-progress.json), cập nhật bằng trang học hoặc [công cụ Python](tracking/README.md), rồi commit/push cùng bài làm.

## Bộ tài liệu này gồm gì?

- `lessons/`: 32 bài giảng, mỗi bài có ba lab, ví dụ, tình huống lỗi, câu tự kiểm tra và điều kiện hoàn thành.
- `solutions/`: 32 tài liệu gợi ý và đáp án tự kiểm tra. Mã ví dụ minh họa một khái niệm, không phải bản WorkBoard đã hoàn chỉnh.
- `project/`: đặc tả, hợp đồng API, milestone, bài kiểm tra lỗi và rubric.
- `starter/`: hai project khởi đầu. Phần bài tập chưa làm được ghi rõ; những TODO này là nhiệm vụ của người học.
- `mock_api/`: server Python không cần thư viện ngoài, có tài khoản thử, kiểm tra quyền sở hữu, phiên bản dữ liệu và mô phỏng lỗi.
- `templates/`: mẫu PR, quyết định kiến trúc, test plan, release, báo cáo hiệu năng và sự cố.
- `backlog.csv`: 96 lab để nhập vào bảng công việc. `progress.csv`: 32 tuần để theo dõi thủ công.
- `evidence/`: nơi lưu bằng chứng học tập của bạn. Không đưa token, mật khẩu thật hoặc dữ liệu cá nhân vào đây.

## Cách sử dụng một bài học

**Đọc → giải thích lại → dự đoán kết quả ví dụ → chạy thử → tự làm lab → tạo lỗi → kiểm thử → review.**

Mỗi tuần có 15 giờ cốt lõi: 3 giờ học, 8 giờ làm lab, 3 giờ test/debug, 1 giờ demo và ghi nhật ký. Tối đa 5 giờ bổ sung dành cho phần chưa chắc hoặc bài mở rộng. Không cộng thêm mọi bài nâng cao nếu tuần đó đã đủ tải.

Mỗi lab tạo một nhánh Git nhỏ hoặc một nhóm commit có mục đích rõ. Nộp đường dẫn commit, lệnh kiểm tra, kết quả mong đợi và một ảnh/video ngắn nếu liên quan UI. Bạn có thể tự review trước; từ giai đoạn kiến trúc nên nhờ người khác review định kỳ.

## Công cụ cần có

Flutter stable kèm Dart, Git, IDE, thiết bị Android hoặc emulator. Python 3.10+ dùng cho API giả lập. Flutter web có thể dùng cho một số bài UI và HTTP; bài nền tảng, phát hành và hiệu năng mobile cần thiết bị/emulator phù hợp. iOS build cần macOS và Xcode; nhánh Android là đường học bắt buộc nếu bạn chưa có Mac. Không đánh dấu iOS đã kiểm chứng khi mới đọc lý thuyết.

Chạy `flutter doctor -v` để biết thành phần còn thiếu. Starter dùng Flutter core; chỉ thêm Riverpod, go_router, Drift khi đến bài tương ứng và chọn phiên bản tương thích với Flutter của bạn. Lưu `pubspec.lock` cho ứng dụng. Các API package có thể thay đổi: dùng tài liệu chính thức được liên kết trong bài, đọc migration guide khi cần.

## Nhịp hoàn thành

Các tuần là thứ tự phụ thuộc, không phải hạn chót cứng. Nếu chưa vượt gate của một milestone, dành tuần dự phòng sửa điểm yếu trước khi đi tiếp. Đánh dấu làm được với hướng dẫn, tự làm được, hay đã kiểm chứng trường hợp lỗi theo rubric; đừng chỉ đánh dấu đã đọc.

Ngày đầu: cài công cụ, chạy starter, đọc bài 01 và hoàn thành W01-L1. Cuối tuần đầu: ba lab có commit và test, nhật ký có ít nhất một lỗi bạn tự giải thích được.

## Sau chương trình

Tiếp tục các chu kỳ sản phẩm có người dùng thật, code review và trách nhiệm vận hành. Rèn kỹ năng làm rõ yêu cầu, phối hợp backend/QA/design, bảo trì code cũ và hướng dẫn đồng nghiệp. Bài mô phỏng trong bộ này giúp chuẩn bị; kinh nghiệm đội ngũ cần được tích lũy trong môi trường thật.
