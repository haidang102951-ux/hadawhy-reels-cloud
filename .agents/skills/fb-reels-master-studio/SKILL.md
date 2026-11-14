---
name: fb-reels-master-studio
description: Hệ thống Đầu Não Độc Quyền Sản Xuất Video Ngắn FB Reels / TikTok 9:16 (1080x1920 @ 60fps) chuẩn kênh FB HaDa Why (@hadawhy) tại D:\Đầu Não Video Ngắn FB (không xóa). Bắt buộc kích hoạt khi Người Chỉ Huy yêu cầu làm video ngắn tài chính, kinh tế, thương hiệu, công nghệ, điều tra, giải thích cơ chế hoặc sự kiện thực tế. Thực thi 10 Luật Thép: (1) Kết hợp 2 Bộ Não: Chiều sâu điều tra từ D:\Đầu Não và Thực thi Remotion 3D 60fps từ D:\Đầu Não Video Ngắn FB, (2) Khóa cứng 5 Sub-Agents chuyên trách - Cấm đẻ subagent rác, (3) Kịch bản 5 nhịp giữ chân đạt hoặc vượt chuẩn video 42s Nvidia, (4) Sự thật 100% Zero-Hallucination, (5) Kịch bản nói A minh họa đúng A - Cấm tái sử dụng đồ cũ, (6) Trinh sát Hình Thật + Icon 3D theo kịch bản & tách nền AI bria-rmbg, (7) 6 Khuôn mẫu Remotion 3D 60fps + Chữ Zero-Box 2 màu 80/20 + Hòa âm (-14.0 LUFS) + Soi Mắt Thần, (8) ADN Thumbnail Bìa Dọc 9:16 3D Liền Mạch (Bầu trời tự nhiên liền mạch, CẤM đốm đỏ/đen, Tòa nhà nổi khối 3D, Text Hook 2 dòng Xanh #42B2F2/Trắng #FFFFFF, an toàn 4:5), (9) Logo Chống Ăn Cắp Bản Quyền 2 Lớp (hadawhy_logo.png), (10) Quy chuẩn Đường Dẫn 3 Tầng & Zero-Junk Ổ C (100% tệp tạm tại D:\DuAn_DangLam\<ten_du_an>\temp\, xong dự án xóa sạch).
---

# ĐẦU NÃO VIDEO NGẮN FB REELS 9:16 (60FPS MASTER STUDIO)
**Thư mục gốc:** `D:\Đầu Não Video Ngắn FB (không xóa)`  
**Đích xuất bản duy nhất:** `D:\Video thành phẩm\<Ten_Video>_master.mp4` + `D:\Video thành phẩm\<Ten_Video>_thumbnail.png` (`1080x1920`)

---

## 🎖️ PHẦN 1: DÂY CHUYỀN TÁC CHIẾN 6 SUB-AGENTS CỐ ĐỊNH (CẤM ĐẺ CON RÁC)

Hệ thống vận hành bằng **đúng 6 Sub-Agents chuyên trách cố định**:
* **LUẬT CẤM ĐẺ SUB-AGENT RÁC (`ZERO EXTRA SUBAGENT SPAWN`):**
  - Mọi trao đổi điều phối chỉ diễn ra giữa 6 thành viên cố định này.
  - Nghiêm cấm gọi `invoke_subagent` sinh thêm sub-agent rác ngoài 6 con này.

### TRÌNH TỰ PHỐI HỢP SONG SONG 6 SUB-AGENTS:
1. **Con số 1 — Tổng Chỉ Huy Điều Phối (`fb-reels-master-commander`):**
   - Nhận đề tài từ Người Chỉ Huy $\rightarrow$ Chỉ đạo lên kịch bản chuyên sâu trước $\rightarrow$ Chạy `semantic_scene_planner.py` bóc tách từng câu kịch bản $\rightarrow$ Giao việc song song và giám sát chặt chẽ.
2. **Con số 2 — Đạo Diễn Biên Kịch Sự Thật & 5 Nhịp Giữ Chân (`fb-reels-fact-scriptwriter`):**
   - Lấy chiều sâu điều tra từ `D:\Đầu Não (không xóa)`, nắm chắc sự thật 100% (`fact_sheet.json`).
   - Viết kịch bản mới hoàn toàn theo **Cấu trúc 5 nhịp giữ chân (đạt hoặc vượt chuẩn video 42s Nvidia)**.
   - Sinh giọng đọc Nam Bắc **Hải Đăng** + bóc tách word-timestamps `faster-whisper` (`voice.wav`, `words.json`).
3. **Con số 3 — Đặc Nhiệm Trinh Sát Tư Liệu Thật & 3D (`fb-reels-asset-harvester`):**
   - Chỉ đi trinh sát sau khi kịch bản đã chốt ("Nói A minh họa đúng A").
   - Xóa kho cũ bằng `purge_harvested_folder()` $\rightarrow$ Cào ảnh thật HD, gọi trực tiếp `auto_cutout.py` tách nền AI bria-rmbg có rim light và bóng sàn 3D, nạp icon 3D. 100% tệp tạm gom vào `D:\DuAn_DangLam\<ten_du_an>\temp\`.
4. **Con số 4 — Đạo Diễn Dựng Remotion 3D 60fps (`fb-reels-motion-3d-director`):**
   - Lắp ráp 6 khuôn mẫu Remotion 3D 60fps, chữ Kinetic Zero-Box 2 màu 80/20 nảy từng từ theo giọng đọc, gắn logo chống re-up 2 lớp `<ChannelWatermark9x16 />`.
5. **Con số 5 — Phù Thủy Âm Thanh AI ACE-Step & Tổng Thanh Tra Mắt Thần (`fb-reels-qc-sound-sentinel`):**
   - **Giữ nguyên 100% cách đánh 33+ điểm rơi SFX sắc nét, rõ ràng của bản gốc** (`remotion_reels/public/sfx/` căn chỉnh từng mili-giây theo `words.json` bổ trợ cho Text Hook và chuyển động 3D, tuyệt đối không làm đục hay bóp nhỏ SFX).
   - **Chỉ thay nhạc nền BGM bằng nhạc AI mới 100% sinh từ `ACE-Step 1.5` (`27 steps HD`)** qua `ace_step_fb_runner.py` (cấm tuyệt đối lấy nhạc nền cũ trong máy!), chuẩn hóa EBU R128 (`-14.0 LUFS`).
   - Soi Mắt Thần từng phân cảnh và Thumbnail (giả lập crop 4:5).
6. **Con số 6 — Kiến Trúc Sư Thumbnail 3D, Nhúng Bìa Video & Chuyên Gia SEO Evergreen (`fb-reels-thumbnail-seo-architect` — CHẠY SONG SONG):**
   - Hoạt động cùng lúc với các bộ phận khác ngay khi có kịch bản: đọc hiểu cốt truyện, tư duy chọn 1 trong 4 chế độ bố cục (`mystery_silhouette`, `dual_confrontation`, `forensic_object`, `titan_evidence`) phù hợp nhất với kịch bản mới, giữ vững khung ADN kênh (Logo góc trái, Chữ Hook 2 dòng `#42B2F2` / `#FFFFFF` viền đen 11px an toàn 4:5, Nền bổ trợ bối cảnh thật nổi khối 3D Chiaroscuro, bầu trời/nền trên liền mạch 100% Zero-Blob không đốm đỏ/đen).
   - Khi video hoàn tất, chạy `thumbnail_3d_seo_engine.py --mode embed` **gắn thẳng Thumbnail vào đầu video MP4 (`00:00`) + `attached_pic`** để khi đăng lên Facebook chọn được ngay ảnh bìa trong video.
   - Đồng thời chạy `thumbnail_3d_seo_engine.py --mode seo` cào dữ liệu thật từ Google/YouTube Suggest + `yt-dlp` để trả về **3 Tiêu đề chuẩn SEO có Keyword lượt tìm kiếm cao và Evergreen**.

---

## 🏛️ PHẦN 2: 10 THIẾT QUÂN LUẬT BẤT DI BẤT DỊCH CỦA KÊNH

1. **KẾT HỢP HOÀN HẢO 2 BỘ NÃO:** Chiều sâu điều tra sự thật từ `D:\Đầu Não (không xóa)` $\times$ Cỗ máy dựng Remotion 3D 60fps từ `D:\Đầu Não Video Ngắn FB (không xóa)`. Cấm tự chế lại bánh xe, bắt buộc gọi các engine có sẵn.
2. **"LÀM MỚI HOÀN TOÀN 100% — CẤM TUYỆT ĐỐI DÙNG DỮ LIỆU, ÂM THANH, CHỮ, HÌNH ẢNH CỦA KỊCH BẢN CŨ" (ZERO LEGACY CONTAMINATION):**
   - **Giữ nguyên 100% CÁCH LÀM của ADN kênh:** Cấu trúc 5 nhịp giữ chân, chiều sâu điều tra sự thật, chữ Kinetic Zero-Box 2 màu 80/20, Remotion 3D 60fps, hòa âm -14.0 LUFS, và Thumbnail 3D liền mạch đạt hoặc vượt chuẩn video 42s Nvidia.
   - **CẤM TUYỆT ĐỐI 100% tái sử dụng nội dung bài cũ:** Cấm dùng lại dữ liệu, con số, câu chữ, file caption (`.ts`/`.json`), file giọng đọc (`voice.wav`), bản hòa âm, hay bất kỳ bức ảnh/bối cảnh nào của kịch bản cũ (như Nvidia, Vietjet...).
   - Mỗi kịch bản mới bắt buộc phải làm lại mới hoàn toàn 100% từ con số 0 (xóa sạch `public/harvested/` và audio bài cũ trước khi làm bài mới), hoàn toàn độc lập, không liên quan gì đến kịch bản cũ!
3. **SỰ THẬT BÁO CHÍ & ÁN LỆ 100% (`fact_sheet.json`):** Không bịa số liệu, ngày tháng, tên nhân vật hay pháp nhân.
4. **KỊCH BẢN 5 NHỊP GIỮ CHÂN ĐẠT HOẶC VƯỢT CHUẨN VIDEO 42S NVIDIA:**
   - Nhịp 1 (0–3s): Hook Con Số Thật + Nghịch Lý Gây Sốc đập vỡ kỳ vọng.
   - Nhịp 2 (3–12s): Lộ diện nhân vật / cơ chế ngầm.
   - Nhịp 3 (12–24s): Plot Twist quá khứ kịch tính (hồ sơ án lệ đen tối).
   - Nhịp 4 (24–35s): Quy chiếu giá trị & dòng tiền được bảo vệ.
   - Nhịp 5 (35–42s): Đóng dấu kết luận triết lý sâu sắc, kích thích tranh luận.
5. **ĐỔI NỀN, MÀU NHẤN & BGM THEO 5 BỘ DNA CHỦ ĐỀ (`semantic_scene_planner.py`):**
   - `finance_macro` (Vàng Kim `#FFE600`), `tech_ai_auto` (Xanh Cyber `#00E5FF`), `forensic_crime` (Đỏ Chu Sa `#FF3B47`), `business_consumer` (Xanh Ngọc `#00F59B`), `geopolitics_energy` (Hổ Phách `#FFB800`).
6. **6 KHUÔN MẪU REMOTION 60FPS ĐA NĂNG (`remotion_reels/src/components/`):**
   - `RealPersonSpotlight3D.tsx`, `AnatomyCallout3D.tsx`, `TimelineTrack3D.tsx`, `CoinStream.tsx`, `ScaleComparison3D.tsx`, và `GeoStrategicMap3D.tsx`.
7. **CHỮ ZERO-BOX & QUY TẮC 2 MÀU 80/20 (`KineticWordCaption.tsx`):**
   - Không nền hộp chữ, font `BeVietnamPro-Black.ttf`, viền `9px #06080E`, 80% chữ Trắng `#FFFFFF` + tối đa 1 cụm từ khóa mang màu nhấn DNA nảy từng từ theo giọng nói.
8. **HỆ THỐNG SFX SẮC NÉT NHƯ BẢN GỐC + NHẠC NỀN AI `ACE-STEP 1.5` MỚI 100% (`-14.0 LUFS`) & SOI MẮT THẦN:**
   - Duy nhất 1 giọng `Hải Đăng` mới 100% theo kịch bản (`voice_volume = 1.35`).
   - **Giữ nguyên 100% độ sắc nét & cách đặt 33+ điểm rơi SFX của video gốc (`sfx_timeline_mixer.py`):** Căn chỉnh chuẩn xác từng mili-giây theo `words.json` để bổ trợ rõ ràng cho Text Hook và chuyển động 3D (không cắt `lowpass` làm đục tiếng hay bóp nhỏ SFX).
   - **BGM AI Độc Bản Mới 100% (`ace_step_fb_runner.py`):** Cấm tuyệt đối dùng nhạc nền cũ trong máy (`assets/music/*.mp3`). Mỗi kịch bản bắt buộc gọi `ACE-Step 1.5` (`27 steps HD`) tạo nhạc nền mới kịch tính, tự động Ducking (`bgm_volume = 0.068`) dưới giọng đọc và ngắt chân không (`Vacuum Drop`) trước câu chốt. Chuẩn hóa EBU R128 (`-14.0 LUFS`).
9. **ADN THUMBNAIL 9:16 3D LIỀN MẠCH (`ThumbnailCover9x16.tsx`):**
   - Bầu trời tự nhiên liền mạch 100% từ mép trái sang mép phải (**CẤM tuyệt đối mọi đốm đỏ `#E11D2E` hay đốm đen vô nghĩa trên trời**).
   - Tòa nhà / công trình nổi khối 3D (2 diện chiaroscuro đón sáng/đổ bóng, unsharp mask micro-contrast, logo thương hiệu sắc sảo).
   - Chủ thể B&W High-Contrast bên trái + Đối tượng Silhouette viền đỏ kèm dấu `?` đỏ phát sáng và mũi tên nét đứt bên phải.
   - Text Hook 2 dòng `Kanit-Black.ttf` chiếm ~90% bề ngang, viền đen 11px cực dày tại `top: ~390px`: Dòng 1 Xanh HaDa **`#42B2F2`** + Dòng 2 Trắng WHY **`#FFFFFF`**.
   - Safe Zone 4:5: Mọi chi tiết quan trọng nằm trọn trong `Y: 260..1560`.
10. **QUY CHUẨN ĐƯỜNG DẪN 3 TẦNG & GIAO THỨC CHỐNG RÁC Ổ C:**
   - **Tầng 1 (Hệ thống lõi):** `D:\Đầu Não Video Ngắn FB (không xóa)` chỉ lưu mã nguồn và engine.
   - **Tầng 2 (Dự án đang làm):** `D:\DuAn_DangLam\<ten_du_an>\` chứa 100% tài liệu, kịch bản JSON, âm thanh, video b-roll và thư mục `temp\` chứa tệp tạm. Xong dự án Người Chỉ Huy xóa đúng 1 folder này là giải phóng 100% đĩa.
   - **Tầng 3 (Thành phẩm cuối cùng):** `D:\Video thành phẩm\<Ten_Video>_master.mp4` và `<Ten_Video>_thumbnail.png`.
   - **TUYỆT ĐỐI CẤM:** Không sinh bất kỳ byte rác nào vào ổ C (Bộ Não). Mọi file tạm phải nằm tại `D:\DuAn_DangLam\<ten_du_an>\temp\`.