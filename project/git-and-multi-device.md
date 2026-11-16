# Đưa project lên Git và học trên nhiều máy

Bạn có thể giữ **học liệu, mã bài tập, bằng chứng và tệp tiến độ** trong một repository riêng tư. Trên máy khác, clone repository rồi tiếp tục từ cùng một trạng thái. Git không tự đồng bộ localStorage của trình duyệt; tiến độ trên trang học cần được xuất thành tệp trước khi commit.

Tài liệu này hướng dẫn bạn tạo repository của riêng mình. Nó không có nghĩa project đã được đẩy lên tài khoản GitHub/GitLab của bạn.

## 1. Chuẩn bị bản làm việc trên máy đầu tiên

Tải `workboard-academy.zip` trong trang học, giải nén thành thư mục `workboard-academy`. Đặt nó ngoài các repository khác. Mở terminal ngay trong thư mục chứa `README.md`, `lessons/`, `starter/` và `project/`.

Các lệnh dưới dùng Git CLI. Trên Windows, có thể dùng Git Bash đi kèm Git for Windows. Chạy lần lượt và đọc kết quả; không bỏ qua lỗi để chạy tiếp.

```bash
git --version
git rev-parse --show-toplevel
```

Ở thư mục mới chưa có Git, lệnh thứ hai báo không phải repository là bình thường. Nếu nó in ra một thư mục cha khác, hãy chuyển bộ học liệu ra ngoài repository đó trước. Nếu thư mục này đã là repository do bạn tạo từ trước, giữ nguyên lịch sử và bỏ qua bước `git init`.

```bash
git init -b main
git config --get user.name
git config --get user.email
```

Nếu chưa cấu hình danh tính, thay hai giá trị minh họa sau bằng tên và email của bạn. Cấu hình dưới chỉ áp dụng cho repository này; có thể dùng email riêng tư do GitHub/GitLab cung cấp.

```bash
git config user.name "Ten cua ban"
git config user.email "email-cua-ban@example.com"
```

## 2. Kiểm tra nội dung trước commit đầu tiên

Mở `.gitignore` và kiểm tra các thư mục sinh ra, database thử nghiệm, cấu hình riêng và khóa ký đã được loại trừ. Không commit access token, mật khẩu thật, `.env`, khóa dịch vụ, keystore, private key hoặc dữ liệu cá nhân. SQLite của mock API là dữ liệu thử trên từng máy, không phải nội dung cần chia sẻ bằng Git.

Đưa mã bạn tự viết và nhật ký vào các thư mục có chủ đích, ví dụ `evidence/week-01/`. Nếu tạo ứng dụng Flutter hoàn chỉnh, có thể đặt ở `apps/workboard_app/` trong repository này. Tránh chép một thư mục `.git` của repository khác vào bên trong. Với ứng dụng Flutter, commit `pubspec.lock`; không commit `.dart_tool/` hoặc thư mục `build/`.

```bash
git add .
git status --short
git diff --cached --stat
```

Đọc danh sách file đã stage. Nếu vô tình stage một file không muốn đưa lên, bỏ riêng file đó khỏi index và sửa `.gitignore` trước khi commit. `.gitignore` không tự ngừng theo dõi file đã được commit.

Khi danh sách đúng:

```bash
git commit -m "Add WorkBoard Academy learning project"
```

## 3. Tạo repository riêng tư và đẩy mã lên

Trên GitHub hoặc GitLab, tạo repository tên `workboard-academy`, chọn **Private**. Tạo repository rỗng: chưa thêm README, license hoặc `.gitignore` trên giao diện dịch vụ, vì bản local đã có nội dung và commit đầu tiên.

Sao chép URL clone của repository vừa tạo. URL dưới chỉ là ví dụ; **thay toàn bộ URL bằng URL thật của bạn trước khi chạy**:

```bash
git remote add origin https://github.com/hungkvbn/workboard-academy.git
git push -u origin main
```

Với GitLab, dùng URL clone GitLab tương ứng. Nếu repository đã có remote `origin`, kiểm tra `git remote -v` thay vì thêm trùng. Nếu remote đã có lịch sử, không dùng force push để thay thế; clone remote vào thư mục mới và đưa học liệu vào đó, hoặc hòa giải hai lịch sử một cách có chủ đích.

Đăng nhập theo cơ chế Git của dịch vụ: credential manager, SSH hoặc công cụ chính thức. Không đặt token trực tiếp vào URL remote, lệnh được lưu trong hướng dẫn, hay file trong repository.

Sau khi push thành công, mở repository trên dịch vụ và kiểm tra có README, các bài học và commit vừa tạo. Đây mới là bằng chứng nội dung đã lên remote.

## 4. Chuyển sang máy tính khác

Cài Git rồi clone bằng URL thật. Chọn một thư mục cha dành cho project trước khi chạy:

```bash
git clone https://github.com/hungkvbn/workboard-academy.git
cd workboard-academy
git status
```

Trên máy mới, cài Flutter/Dart, IDE, Python và thiết bị/emulator theo README. Git đồng bộ mã nguồn và tài liệu, không mang theo SDK, package cache, emulator, phiên đăng nhập hay database local. Chạy lại lệnh cài dependency và test của starter phù hợp. Với API giả lập, đăng nhập lại và tạo dữ liệu thử cần thiết.

Bạn không cần chạy một website local để đọc bài: mở trang WorkBoard Academy bằng cùng tài khoản có quyền truy cập. Khi offline, đọc Markdown trong IDE hoặc `GIAO_TRINH.docx` đã tải về.

## 5. Mang tiến độ trình duyệt theo Git

Trong trang học, mở **Mã nguồn & tài liệu → Xuất tiến độ**. Trình duyệt tải tệp `workboard-progress.json`. Tạo thư mục `tracking/` trong bản local của repository và đặt tệp tại:

```text
workboard-academy/
  tracking/
    workboard-progress.json
```

Nếu thư mục Downloads đã có tệp cùng tên, trình duyệt có thể thêm hậu tố như `(1)`. Hãy chọn đúng bản vừa xuất, rồi lưu vào đường dẫn thống nhất ở trên. Không commit các bản trùng chỉ vì khác hậu tố.

```bash
git add tracking/workboard-progress.json
git commit -m "Update learning progress"
git push
```

Trên máy còn lại, pull repository rồi mở trang học và chọn **Nhập tiến độ**, dùng tệp `tracking/workboard-progress.json` vừa nhận. Kiểm tra số lab và tuần đã hoàn thành.

Nếu chọn gộp, các dấu hoàn thành được kết hợp với tiến độ hiện tại; một tệp cũ có thể đánh dấu lại mục bạn vừa bỏ chọn. Khi cần khôi phục chính xác một bản đã chọn, dùng lựa chọn thay thế nếu giao diện có cung cấp và kiểm tra nội dung trước. Xuất bản hiện tại để sao lưu trước khi thay thế.

`progress.csv` là cách theo dõi thủ công độc lập. Sửa CSV không tự đổi checklist trên trang học, và xuất JSON từ trang học không tự sửa CSV. Chọn một cách theo dõi chính để tránh hai bảng khác nhau.

## 6. Nhịp làm việc mỗi buổi

**Trước buổi học:** bảo đảm thay đổi của buổi trước đã commit, sau đó nhận cập nhật:

```bash
git status
git pull --ff-only
```

Nhập JSON vào trang học nếu chuyển máy. Làm bài, chạy kiểm tra và ghi bằng chứng. **Cuối buổi:** xuất tiến độ về `tracking/workboard-progress.json`, stage các file đã sửa có chủ đích, commit và push. Chờ push thành công trước khi bắt đầu trên máy kia.

Nếu `git pull --ff-only` từ chối vì hai máy đều có commit mới, dừng để đối chiếu lịch sử. Không force push để làm thông báo biến mất. Với tệp tiến độ, giữ bản sao cả hai, chọn bản chính hoặc gộp bằng chức năng của trang học rồi xuất lại. Với mã bài tập, giải quyết từng xung đột, chạy test và commit kết quả hợp nhất. Cách dễ nhất để giảm xung đột là học trên một máy tại một thời điểm và push cuối mỗi buổi.

## Tài liệu Git chính thức

- [Khởi tạo hoặc clone repository](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository).
- [Theo dõi và commit thay đổi](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository).
- [Làm việc với remote](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes).
- [Hành vi của git pull](https://git-scm.com/docs/git-pull).
## Tùy chọn: khởi tạo từ Git bundle

Ngoài ZIP, trang học có bản `workboard-academy.bundle` chứa toàn bộ học liệu và commit khởi đầu. Tải bundle về thư mục Downloads rồi mở terminal tại thư mục đó:

```bash
git clone workboard-academy.bundle workboard-academy
cd workboard-academy
```

Với cách này, project đã có lịch sử Git nên bỏ qua bước `git init` phía trên. Remote `origin` ban đầu trỏ tới tệp bundle trên máy; sau khi tạo repository GitHub riêng tư, thay bằng URL của bạn:

```bash
git remote set-url origin https://github.com/hungkvbn/workboard-academy.git
git push -u origin main
```

URL trên là repository bạn đã chọn; nếu dùng một bản sao khác, thay URL tương ứng. Git dùng thông tin đăng nhập GitHub trên máy của bạn; không đưa token vào URL hoặc commit. Sau khi đẩy lên thành công, máy khác clone URL GitHub như hướng dẫn phía trên. Bạn cũng có thể chuyển bundle bằng ổ đĩa để clone offline; cách đó không tự đồng bộ các thay đổi về sau.

Tiến độ từ trang học dùng chung với [tracking/workboard-progress.json](../tracking/workboard-progress.json). Có thể cập nhật bằng terminal theo [hướng dẫn tracking](../tracking/README.md). Bundle ban đầu có tiến độ trống; xuất tiến độ trình duyệt hiện tại rồi nhập trước khi commit nếu bạn đã học.

