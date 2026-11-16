# Release v__

## Người dùng sẽ nhận được gì?

Chức năng, lỗi được sửa, thay đổi dữ liệu hoặc hành vi.

## Trước phát hành

- [ ] Build từ commit xác định, test và phân tích mã đạt.
- [ ] Cấu hình đúng môi trường; không có khóa đặc quyền trong bundle.
- [ ] Cài mới và nâng cấp từ bản cũ được kiểm tra.
- [ ] Quyền, deep link, offline và logout được smoke test.
- [ ] Crash reporting có thông tin phiên bản, không log dữ liệu nhạy cảm.
- [ ] Có người phụ trách theo dõi và điều kiện dừng rollout.

## Phân phối và theo dõi

Kênh beta/store, người dùng mục tiêu, chỉ số và thời gian quan sát. Nếu xảy ra lỗi: dừng rollout, tắt tính năng nếu có cơ chế, hoặc phát hành bản sửa. Ghi rõ giới hạn rollback của mobile và migration.

## Sau phát hành

Kết quả cài đặt/nâng cấp, phản hồi, lỗi mới, quyết định tiếp tục hay dừng.
