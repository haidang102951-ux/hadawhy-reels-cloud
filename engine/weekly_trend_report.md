# Báo Cáo Kỹ Thuật Dựng Phim & Đồ Họa Kiến Thức Mới — HaDa Why (9:16 @ 60fps)
**Cập nhật:** 2026-11-18

1. **Exploded Isometric Tear-Down (Tách Lớp Vật Thể 3D Theo Trục Z):**
   - **Cơ chế:** Tách 1 sản phẩm/cơ cấu (tờ tiền, hóa đơn, thiết bị, hộp sản phẩm) thành 3–4 lớp song song bay tách dọc trục Z trong `ThreeCanvas`, mỗi lớp gắn 1 `MotionTrackedCallout` chỉ rõ phần trăm chi phí/cấu tạo.
   - **Ứng dụng:** Chủ đề bóc tách giá thành, biên lợi nhuận, cấu trúc chi phí ẩn.
2. **Split-Screen Counter-Race (Đua Tốc Độ 2 Thực Thể Trực Quan):**
   - **Cơ chế:** Chia đôi khung hình trên/dưới hoặc trái/phải với thanh tiến độ & đồng hồ `OdometerCounter` chạy thực tế ở 2 tốc độ chênh lệch (ví dụ: tốc độ tăng lương vs tốc độ tăng giá nhà).
   - **Ứng dụng:** Chủ đề nghịch lý kinh tế, so sánh quy mô, chênh lệch giàu nghèo.
3. **Spotlight X-Ray Mask (Ống Kính Quét X-Quang Bóc Trần Sự Thật):**
   - **Cơ chế:** Lớp bề mặt quảng cáo hào nhoáng bị một vòng tròn/thanh quét `clipPath` di chuyển qua, lộ ra lớp sự thật/số liệu thô bên dưới kèm tiếng quét stereo chạy từ trái sang phải.
   - **Ứng dụng:** Chủ đề giải mã chiêu trò marketing, bẫy tiêu dùng, ảo giác tâm lý.
4. **Domino Chain Cascade (Hiệu Ứng Domino Dây Chuyền 3D):**
   - **Cơ chế:** Các khối 3D trong `@remotion/three` đổ nối tiếp nhau theo từng mệnh đề nguyên nhân → hệ quả, camera trượt theo khối đang đổ.
   - **Ứng dụng:** Chủ đề khủng hoảng dây chuyền, lịch sử sụp đổ thương hiệu, hiệu ứng cánh bướm.
5. **Live Receipt Printer Roll (Cuộn Hóa Đơn In Nhiệt Theo Nhịp Giọng Đọc):**
   - **Cơ chế:** Tờ hóa đơn trượt dọc từ dưới lên theo từng từ khóa, mỗi dòng chi phí/thuế in ra được quét `MarkerHighlightText` và cộng dồn tổng tiền ở đáy.
   - **Ứng dụng:** Chủ đề thuế phí, giá bán lẻ, chi tiêu hàng ngày.
