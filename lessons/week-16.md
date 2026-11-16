# Tuần 16 — Quyết định kỹ thuật, refactor và design review

**Đích đến:** chứng minh vì sao chọn cách làm, thay đổi code trong phạm vi kiểm soát và nhận phản biện có ích. **Tiên quyết:** WorkBoard qua một thay đổi nghiệp vụ, có repository, test và ít nhất một lỗi từng sửa.

## 1. Bài giảng

### ADR ghi quyết định cùng bối cảnh

Architecture Decision Record là bản ghi ngắn về một quyết định có ảnh hưởng lâu dài: vấn đề, ràng buộc, các lựa chọn, lựa chọn được chọn và hệ quả. Nó không phải bài quảng cáo công nghệ. “Riverpod phổ biến” chưa giải thích vì sao phù hợp với nhóm, code hiện có và thời gian dự án. Ghi cả điều kiện khiến bạn phải xem lại quyết định.

Ví dụ bối cảnh: WorkBoard hiện có một developer, cần phát hành beta trong 12 tuần, đã có repository và test. Bạn so sánh refactor toàn bộ sang kiến trúc mới với refactor từng feature khi có nhu cầu. Phương án từng feature có thể giảm rủi ro và cho phép giao sản phẩm liên tục, đổi lại một thời gian tồn tại hai cấu trúc. Đó là trade-off cụ thể, không phải đúng/sai tuyệt đối.

### Refactor giữ hành vi, tính năng đổi hành vi

Refactor thay cách tổ chức code nhưng giữ hành vi quan sát được. Nếu vừa đổi repository vừa sửa cách phân trang vừa đổi thông báo lỗi, người review khó biết regression đến từ đâu. Chia PR theo bước có thể chạy/test được. Chuỗi di chuyển có thể là: thêm interface và test → chuyển một caller → xóa đường cũ sau khi không còn sử dụng.

Ví dụ diff nhỏ giữ hành vi nhưng đặt tên cho ý nghĩa:

```dart
// Trước: cùng biểu thức xuất hiện tại nhiều caller.
final visible = tasks.where((t) => t.ownerId == userId).toList();

// Sau: hàm thuần có tên và test; vẫn giữ thứ tự đầu vào.
List<WorkTask> tasksOwnedBy(List<WorkTask> tasks, String userId) =>
    tasks.where((task) => task.ownerId == userId).toList(growable: false);
```

Đây chỉ là lọc phía client phục vụ state đúng phạm vi; nó không thay thế kiểm tra quyền ở backend. Khi refactor, mô tả cả điều kiện giữ nguyên như thứ tự, nullability và cách báo lỗi.

### Review đánh giá rủi ro và ý định

Một review hữu ích bắt đầu từ vấn đề cần giải quyết, không chỉ tên biến. Người review xem dữ liệu đi đâu, lỗi nào có thể xảy ra, quyền được kiểm tra ở đâu và test bảo vệ hành vi nào. Phân biệt yêu cầu sửa bắt buộc với gợi ý phong cách. Đưa phản ví dụ cụ thể giúp tác giả kiểm chứng thay vì chỉ nói “code chưa clean”.

Người viết PR cần mô tả cách chạy, thay đổi quan sát được, dữ liệu thử và giới hạn. Một video happy path không đủ cho thay đổi phiên hoặc race condition; test tái hiện lỗi cung cấp bằng chứng phù hợp hơn. Không yêu cầu review hàng trăm file format lẫn một thay đổi logic nhỏ.

### Nợ kỹ thuật cần tác động đo được

“Code xấu” khó ưu tiên. “Thêm một bộ lọc phải sửa bốn widget và đã gây hai lỗi count lệch” là vấn đề có ảnh hưởng. Ghi chi phí, tần suất gặp, giải pháp tối thiểu và tiêu chí hoàn thành. Không dùng nợ kỹ thuật như lý do mặc định để viết lại toàn bộ ứng dụng.

## 2. Ba bài thực hành

### W16-L1 — Hai ADR có lựa chọn thật

Dùng [mẫu ADR](../templates/adr.md). Viết một ADR về cấu trúc state/data và một ADR về chính sách cache/refresh. Mỗi bản có ít nhất hai lựa chọn khả thi, ràng buộc cụ thể của WorkBoard và điều kiện xem lại. Không bịa benchmark hoặc phản hồi người dùng chưa đo.

### W16-L2 — Refactor một điểm đau

Chọn một vấn đề đã gặp trong tuần 15. Ghi hành vi cần giữ, tạo test còn thiếu rồi refactor trong một PR nhỏ. Đầu vào/đầu ra của test trước và sau phải giống nhau. Nếu phát hiện bug cần sửa, tách phần sửa hành vi thành commit hoặc PR riêng có mô tả rõ.

### W16-L3 — Design review và phản hồi

Mời một người đọc PR nếu có; nếu chưa có, đóng vai reviewer sau ít nhất một phiên nghỉ và ghi rõ đây là tự review. Chuẩn bị ba câu phản biện: dữ liệu nào có thể mất, lỗi nào chưa test, điều kiện nào khiến quyết định đổi? Trả lời bằng code, test hoặc giới hạn đã ghi; sửa ít nhất một điểm có lý do.

## 3. Nghiệm thu và tự kiểm tra

- [ ] Hai ADR có bối cảnh, lựa chọn, hệ quả và điều kiện xem lại.
- [ ] Không dùng số liệu chưa đo làm bằng chứng.
- [ ] PR refactor có phạm vi và hành vi giữ nguyên rõ ràng.
- [ ] Test trước/sau kiểm tra cùng kỳ vọng nghiệp vụ.
- [ ] Có ít nhất ba nhận xét review và phản hồi có căn cứ.
- [ ] Nếu chưa có người review ngoài, hồ sơ nói đúng là tự review.
- [ ] Backlog nợ kỹ thuật có tác động và tiêu chí kết thúc.

**Ba câu hỏi:** ADR khác hướng dẫn cài đặt thế nào? Vì sao trộn refactor và đổi hành vi làm review khó? Khi nào nên mở lại một quyết định đã có?

**15 giờ:** 3 giờ đọc và phân tích; 8 giờ ADR/refactor/review; 3 giờ regression; 1 giờ trình bày quyết định. **Nộp:** hai ADR, PR, biên bản review và một ticket nợ kỹ thuật có ưu tiên.

Đọc [Flutter architecture recommendations](https://docs.flutter.dev/app-architecture/recommendations), [Google engineering code review guide](https://google.github.io/eng-practices/review/), [gợi ý](../solutions/week-16.md).
