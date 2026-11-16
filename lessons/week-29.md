# Tuần 29 — Làm rõ yêu cầu, thiết kế và ước lượng

**Mục tiêu:** biến yêu cầu “cho phép làm việc nhóm” thành phạm vi có thể xây dựng, kiểm thử và thảo luận. **Tiên quyết:** WorkBoard cá nhân đã có bản beta. **15 giờ:** 3 giờ học, 8 giờ lab thiết kế/prototype, 3 giờ kiểm tra giả định, 1 giờ review. Đây là tuần thiết kế extension, không bắt buộc xây một backend nhóm hoàn chỉnh.

## Bài giảng

### 1. Yêu cầu nói về kết quả của người dùng

“Thêm nút chia sẻ” chưa cho biết ai được làm gì. Hãy hỏi: chia sẻ một công việc hay một nhóm? Người nhận được xem hay được sửa? Khi thu hồi quyền, dữ liệu offline xử lý thế nào? Một yêu cầu rõ gồm tác nhân, hành động, điều kiện và kết quả có thể quan sát.

Ví dụ: “Chủ nhóm mời một thành viên đã có tài khoản; sau khi lời mời được chấp nhận, người đó xem được công việc của nhóm; người ngoài nhóm không truy cập được bằng API.” Chuyển câu này thành các tiêu chí nghiệm thu trước khi vẽ màn hình.

### 2. Phạm vi nhỏ cần cả những điều chưa làm

MVP tuần này có thể chỉ hỗ trợ hai vai trò owner/member, một nhóm, mời bằng email và thu hồi quyền. Chat, thông báo realtime, lịch sử hoạt động đầy đủ và tổ chức nhiều cấp là phần sau. Viết ngoài phạm vi giúp ước lượng có ý nghĩa và ngăn mọi yêu cầu mới chen vào cùng mốc giao hàng.

Mock API hiện tại chỉ hỗ trợ công việc theo owner; không có groups, invites hoặc memberships. Vì vậy lab dùng tài liệu contract và fake repository để chứng minh luồng UI. Nếu muốn triển khai thật, đó là phần mở rộng riêng và phải thực thi phân quyền phía server. Thay một nút trên UI không tạo được cơ chế bảo mật.

### 3. Thiết kế từ bất biến và ranh giới tin cậy

Bất biến là điều luôn phải đúng. Ví dụ: chỉ owner được thu hồi thành viên; người đã bị thu hồi không gửi được thay đổi mới; mỗi thành viên chỉ có một membership đang hoạt động trong nhóm. Những bất biến này cần được server kiểm tra trong một thao tác nhất quán.

Một contract đề xuất có thể biểu diễn:

```json
{
  "workspaceId": "w-1",
  "userId": "u-2",
  "role": "member",
  "membershipVersion": 3
}
```

Đây là mô hình extension, không phải response của mock hiện có. Số version giúp phát hiện trạng thái quyền đã đổi; nó không thay thế kiểm tra quyền. Với offline, phải quyết định liệu dữ liệu đã cache còn được xem, khi nào xóa và cách báo thao tác bị server từ chối sau thu hồi quyền.

### 4. Ước lượng có giả định

Tách việc thành lát cắt người dùng có thể trải nghiệm: mời → chấp nhận → xem → thu hồi. Mỗi lát cắt gồm UI, API, test và quan sát. Cho khoảng ước lượng cùng giả định, chẳng hạn “luồng mời cần 1–2 ngày nếu dịch vụ email đã có”. Khi chưa biết, làm một spike có thời hạn để trả lời câu hỏi cụ thể, không gọi một con số thiếu căn cứ là cam kết.

Giao tiếp rủi ro bằng tình huống và tác động: “Nếu thu hồi quyền chưa có trên server, không thể phát hành chia sẻ dữ liệu thật.” Đây là thông tin để quyết định phạm vi, không chỉ là ghi chú kỹ thuật.

## Ba bài thực hành

### W29-L1 — Đặc tả MVP

Viết một trang yêu cầu cho nhóm hai vai trò. Có ít nhất sáu tiêu chí Given/When/Then: lời mời hợp lệ, lời mời trùng, người ngoài, member sửa việc, owner thu hồi và thao tác offline sau thu hồi. Đầu ra phải phân biệt điều bắt buộc với phần sau.

### W29-L2 — Contract và prototype

Thiết kế bảng dữ liệu, endpoint đề xuất, mã lỗi và quyền cho từng thao tác. Dùng fake repository để dựng luồng mời/chấp nhận/thu hồi. Không đổi mock API hoặc ghi rằng đã có backend thật khi chỉ dùng fake.

### W29-L3 — Review và ước lượng

So sánh hai lựa chọn: chia sẻ từng task và workspace. Viết [ADR](../templates/adr.md), chia thành ticket có phụ thuộc, ghi khoảng ước lượng và rủi ro. Nhờ người khác review; nếu tự review, ghi rõ đó là diễn tập.

## Nghiệm thu và bằng chứng

- [ ] Mỗi vai trò có bảng quyền cụ thể.
- [ ] Luồng thu hồi quyền gồm cả cache và pending outbox.
- [ ] Contract extension được tách khỏi API đang có.
- [ ] Prototype có trạng thái từ chối, không chỉ thành công.
- [ ] Phạm vi và ngoài phạm vi được viết rõ.
- [ ] Ước lượng có giả định và việc cần khảo sát.
- [ ] ADR ghi ít nhất một đánh đổi đã chấp nhận.

## Tự kiểm tra

1. Vì sao ẩn nút “xóa” không đủ để phân quyền?
2. Một spike khác một tính năng hoàn chỉnh thế nào?
3. Khi nào nên giảm phạm vi thay vì tăng độ chắc chắn giả tạo của ước lượng?

Đọc [Flutter architecture](https://docs.flutter.dev/app-architecture), [Supabase row-level security](https://supabase.com/docs/guides/database/postgres/row-level-security) để hiểu một cách thực thi quyền phía dữ liệu. [Gợi ý tuần 29](../solutions/week-29.md).
