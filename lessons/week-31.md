# Tuần 31 — Bảo trì, nâng dependency và review

**Mục tiêu:** cải thiện một ứng dụng đang hoạt động mà không đánh mất hành vi quan trọng, đồng thời truyền đạt quyết định để người khác tiếp tục làm được. **Tiên quyết:** đã có ít nhất hai bản beta và backlog thật hoặc pilot. **15 giờ:** 3 giờ học, 8 giờ lab, 3 giờ regression và review, 1 giờ tổng kết.

## Bài giảng

### 1. Bảo trì bắt đầu bằng hiểu hành vi hiện tại

Trước khi sửa một phần code khó đọc, xác định hợp đồng bên ngoài: đầu vào, đầu ra, trạng thái lỗi và tác dụng phụ. Viết characterization test cho hành vi quan trọng chưa có test. Nếu hành vi hiện tại là bug, ghi rõ bạn định thay đổi nó; đừng vô tình khóa bug thành chuẩn chỉ vì test tái hiện được.

Refactor giữ nguyên hành vi quan sát được và thay đổi cấu trúc. Sửa tính năng thay đổi hành vi. Hai việc có thể cùng cần thiết, nhưng chia commit hoặc PR để reviewer hiểu rủi ro. Đặc biệt cẩn thận với auth, migration và đồng bộ vì lỗi có thể không lộ trong happy path.

### 2. Nâng dependency là một thay đổi có kiểm soát

Đọc changelog và migration guide của chính package, kiểm tra phiên bản SDK hỗ trợ, rồi nâng trong nhánh riêng. Nâng một nhóm liên quan đủ nhỏ để khoanh vùng lỗi. Chạy lại analyze, test và smoke test trên các nền tảng bị ảnh hưởng; test unit xanh không kiểm chứng được native plugin.

Giữ lockfile của ứng dụng. Trước và sau thay đổi, lưu phiên bản Flutter, dependency và kết quả kiểm tra. Nếu package bị bỏ bảo trì, quyết định có thể là thay thế, giảm phụ thuộc hoặc duy trì bản fork với chi phí rõ ràng. Không tự động chọn package nhiều lượt thích nhất.

### 3. Review tập trung vào tác động

Một nhận xét tốt gồm vấn đề, tình huống gây lỗi, hệ quả và hướng sửa có thể thảo luận. Ví dụ: “Nếu user đăng xuất khi request đang chờ, response hiện vẫn cập nhật cache chung. Điều này có thể lộ dữ liệu giữa tài khoản; nên ràng buộc response với session hiện tại.”

Phân biệt nhận xét bắt buộc vì correctness/security với đề xuất đọc dễ hơn và câu hỏi để hiểu. Khi đưa sở thích style, dựa vào quy ước đã thống nhất. Review không chỉ tìm lỗi: xác nhận một quyết định tốt giúp người viết biết phần nào nên giữ.

### 4. Hướng dẫn người khác bằng khả năng tự chủ

Một buổi mentoring tốt giúp người học tự chẩn đoán lần sau. Cho họ mô tả triệu chứng, đặt giả thuyết, chọn phép kiểm tra nhỏ và đọc kết quả. Đừng giành bàn phím để sửa tất cả. Trong dự án cá nhân, bạn có thể viết hướng dẫn onboarding và nhờ người khác làm thử; nếu không có người cùng học, ghi đó là bài diễn tập tài liệu, không coi là bằng chứng dẫn dắt đội ngũ thật.

## Ba bài thực hành

### W31-L1 — Một dependency upgrade

Chọn package đang dùng có thay đổi phù hợp để nâng, hoặc diễn tập bằng cách đọc một migration guide và tạo nhánh thử. Ghi phiên bản trước/sau, breaking changes liên quan, test đã chạy và kế hoạch nếu bản nâng có lỗi. Không bắt buộc nâng khi không có lý do.

### W31-L2 — Refactor có bảo vệ

Chọn một phần khó thay đổi trong WorkBoard, chẳng hạn mapping lỗi hoặc xử lý outbox. Viết test còn thiếu, refactor một phạm vi nhỏ và chứng minh hành vi quan trọng không đổi. Nộp PR giải thích vấn đề cụ thể, không chỉ “clean code”.

### W31-L3 — Review và onboarding

Nhờ bạn học review PR hoặc trao đổi review hai chiều. Viết hướng dẫn để người mới chạy app và xử lý một bug nhỏ. Ghi lại câu hỏi họ gặp và sửa tài liệu. Nếu chỉ tự thực hành, tạo checklist và đánh dấu bằng chứng mô phỏng.

## Nghiệm thu và bằng chứng

- [ ] Dependency change có lý do, changelog và phạm vi ảnh hưởng.
- [ ] Lockfile/toolchain được ghi rõ.
- [ ] Native change có smoke test trên nền tảng liên quan hoặc ghi chưa kiểm chứng.
- [ ] Refactor có test hành vi trước và sau.
- [ ] PR phân biệt thay cấu trúc và thay nghiệp vụ.
- [ ] Review có ít nhất một nhận xét gắn với tình huống lỗi cụ thể.
- [ ] Onboarding được kiểm tra bởi người khác hoặc ghi rõ là diễn tập.

Nộp [PR](../templates/pr.md), kết quả upgrade và bản hướng dẫn chạy đã sửa từ phản hồi.

## Tự kiểm tra

1. Vì sao nâng tất cả dependency cùng lúc khó điều tra lỗi?
2. Characterization test có thể vô tình giữ lại bug thế nào?
3. Một nhận xét review khác ý kiến style cá nhân ở điểm nào?

Đọc [Dart dependency management](https://dart.dev/tools/pub/dependencies), [Flutter breaking changes](https://docs.flutter.dev/release/breaking-changes) và changelog của package bạn chọn. [Gợi ý tuần 31](../solutions/week-31.md).
