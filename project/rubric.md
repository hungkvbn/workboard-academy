# Rubric và tiêu chí tốt nghiệp

Đánh giá bằng hành vi và bằng chứng. Các mức này là quy ước học tập, không phải chứng nhận chức danh.

| Mức | Mô tả | Bằng chứng |
|---|---|---|
| 0 | Chưa làm hoặc chưa giải thích được | Không có bằng chứng |
| 1 | Làm được với hướng dẫn | Chạy mẫu, giải thích một phần |
| 2 | Tự làm trường hợp thông thường | Tự viết, demo, giải thích quyết định |
| 3 | Làm chủ cả tình huống lỗi | Test, debug, quan sát, phát hành, sửa lỗi |
| 4 | Giúp đội ngũ ra quyết định tốt hơn | Review, hướng dẫn, giải quyết ràng buộc và đo ảnh hưởng |

## Tám nhóm năng lực

1. **Dart:** null safety, models, collections, async, exception, event loop và isolate; giải thích được race condition.
2. **Flutter:** constraints, state, lifecycle, navigation, accessibility, widget/element/rendering ở mức debug.
3. **Dữ liệu:** HTTP, session, ownership, SQL, transaction, migration, offline và conflict.
4. **Thiết kế:** phân chia trách nhiệm, dependency, quyết định có đánh đổi, thay đổi được nguồn dữ liệu.
5. **Kiểm thử:** chọn unit/widget/integration test đúng, tái hiện bug, giữ test ổn định.
6. **Hiệu năng:** thiết kế phép đo, dùng DevTools, xác định nguyên nhân và chứng minh cải thiện.
7. **Phát hành/vận hành:** build, signing, môi trường, monitoring, nâng cấp và ứng phó sự cố.
8. **Hợp tác/sản phẩm:** làm rõ yêu cầu, ước lượng, PR review, nhận phản hồi, hướng dẫn người khác.

## Gate của capstone

Các luồng cốt lõi đạt mức 3 ở Dart/Flutter/dữ liệu/kiểm thử; thiết kế và vận hành ít nhất mức 2 với bằng chứng đã thực hiện. Hợp tác được ghi rõ là review thật hay tự mô phỏng. Không dùng điểm trung bình để bù cho lỗi mất dữ liệu, lộ dữ liệu tài khoản khác hoặc không chạy được từ hướng dẫn.

Người review clone một bản sạch, làm theo README, chạy test và dùng hai tài khoản. Họ chọn ngẫu nhiên ba tình huống từ [failure drills](failure-drills.md). Bạn giải thích một quyết định kiến trúc, một test quan trọng và một số liệu hiệu năng.

## Phiếu chấm mỗi lab

- [ ] Đáp ứng đầu ra yêu cầu và các acceptance checks trong bài.
- [ ] Có đường dẫn commit hoặc PR để kiểm tra.
- [ ] Giải thích được giải pháp và ít nhất một cách làm khác.
- [ ] Tự tạo được một trường hợp lỗi liên quan.
- [ ] Có kiểm chứng phù hợp: test tự động, đo lường hoặc quy trình kiểm tra thủ công ghi rõ.
- [ ] Ghi hạn chế và việc chưa kiểm chứng, không đánh dấu thành công dựa trên phỏng đoán.

Khi chưa đạt: ghi cụ thể điều kiện thất bại, quay lại khái niệm liên quan, sửa một phần nhỏ và chạy lại kiểm tra đó. Nếu bị kẹt quá 45 phút, đọc hint đầu tiên rồi tự tiếp tục. Nếu vẫn không tiến triển, xem worked example và tạo một bài biến thể để tự chứng minh hiểu.

## Hồ sơ hướng tới senior

Lưu những lần bạn dẫn dắt tính năng, sửa sự cố thực tế, giảm chi phí bảo trì và hỗ trợ đồng nghiệp. ADR mô phỏng, mentoring với AI và ứng dụng cá nhân là bài tập chuẩn bị; không ghi thành kinh nghiệm dẫn dắt đội ngũ hoặc vận hành production thật.
