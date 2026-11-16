# Báo cáo hiệu năng

## Giả thuyết

Hành vi chậm, ảnh hưởng người dùng, nguyên nhân nghi ngờ và dữ kiện ban đầu.

## Điều kiện đo

Thiết bị/OS, Flutter version, commit, profile/release mode, kích thước dữ liệu, tốc độ mạng, kịch bản thao tác, số lượt chạy, điều kiện nóng/lạnh.

| Chỉ số phù hợp | Trước | Sau | Cách lấy số liệu |
|---|---|---|---|
| Thời gian tác vụ/frame | | | |
| Bộ nhớ hoặc số lần rebuild | | | |

## Phân tích

Trace/screenshot, điểm nghẽn, thay đổi, chi phí mới và kết quả qua nhiều lượt. Phân biệt jank UI/raster với độ trễ mạng. Không lấy debug mode làm kết luận hiệu năng sản phẩm.

## Kết luận có giới hạn

Giả thuyết được hỗ trợ hay bác bỏ? Thiết bị hoặc luồng nào chưa đo? Test/budget nào giúp phát hiện hồi quy?
