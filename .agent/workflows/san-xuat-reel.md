---
description: Quy trình 4 trạm sản xuất FB Reels 9:16 (60fps AE) phi chủ đề chuẩn HaDa Why có điểm DỪNG phê duyệt.
---

# QUY TRÌNH 4 TRẠM SẢN XUẤT FB REELS (HADA WHY — 60FPS AE)

Tuân thủ `.agent/rules/00-hadawhy-core.md`. Tệp tạm lưu tại `D:\DuAn_DangLam\<du_an>\temp\` (Đầu Não 0 bytes media).

---

## TRẠM 1 — Cào Sâu Bài Gốc, Kịch Bản Nhân Quả 5 Nhịp & Giọng Hải Đăng
1. Chạy CLI đọc sâu 5–8 bài gốc (2.500–4.000 ký tự/bài) + Wikipedia VI/EN với `>= 4–5` truy vấn chuyên sâu:
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\fact_researcher.py" --topic "<chủ đề>" --queries "cơ chế|số liệu|bằng chứng vụ việc|văn bản luật|english keyword" --project "D:\DuAn_DangLam\<du_an>"
   ```
2. Viết `temp/script_5beat.json` (`>= 6` dữ kiện cứng & `>= 3` nguồn thật, 40–55s hoặc video dài, 5 nhịp theo mạch nhân quả **Cơ chế -> Chế tài -> Hậu quả**, ghi sẵn `bgm_mood`, `bgm_segments` nếu là video dài, và 3–4 `sfx_keywords`).
   - **Quy tắc văn phong:** Viết tự nhiên, sắc bén, trung tính; **CẤM** dùng các từ sáo rỗng/kích động như: *bầy đàn, vạch trần, trần trụi, máu me, bạo lực, bòn rút, mổ xẻ, bóc trần...*
3. **BẮT BUỘC** chạy ngay sau bước 2 để sinh sẵn `temp/voiceover.wav` + `temp/words.json` bằng giọng local `"Hải Đăng"` (tự chuẩn hóa đọc mã viết tắt `C04`, `A05`..., CẤM fallback giọng khác) trước khi trình Điểm Dừng 1:
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\vieneu_whisper_pacer.py" --script "D:\DuAn_DangLam\<du_an>\temp\script_5beat.json" --project "D:\DuAn_DangLam\<du_an>" --voice "Hải Đăng"
   ```
4. **ĐIỂM DỪNG 1:** Báo cáo dữ kiện bài gốc + kịch bản 5 nhịp + thời lượng giọng đọc. **DỪNG chờ duyệt `"OK"`** mới sang Trạm 2.

---

## TRẠM 2 — Tư Duy Đạo Diễn, Cào 6 Ứng Viên A..F (>= 700px), Chọn/REJECT & Bóc Tách 3D
1. **Nguyên tắc sắt:** *"Nói gì hiện đúng thứ đó — Cấm tự suy diễn ảnh ẩn dụ. Mọi ảnh cào về phải gắn neo `voice_anchor_quote` có thật trong `words.json`; không tìm thấy ảnh thật khớp 100% câu đọc thì đổi truy vấn cào lại, tuyệt đối không chọn bừa cho đủ số lượng."*
   Lập `temp/harvest_plan.json` (`>= 8–12` mục khớp từng nhịp). Trước khi gõ từ khóa, TỪNG mục BẮT BUỘC điền đủ:
   - `"entity_id"`.
   - `"script_line"`: trích nguyên văn câu thoại có thật trong `script_5beat.json` (sai hoặc tự bịa -> `qc_gate.py plan` chặn ngay với `UNMATCHED_SCRIPT_LINE`).
   - `"voice_anchor_quote"`: cụm 2–5 từ chính xác sẽ vang lên lúc hình này xuất hiện, phải tồn tại trong `script_5beat.json` / `words.json` (không khớp -> chặn `UNMATCHED_VOICE_ANCHOR`).
   - `"must_show"`: mô tả đúng danh từ/thực thể xuất hiện trong `script_line`.
   - `"visual_reasoning"` (`>= 15` ký tự): giải thích ngắn 1 câu *vì sao vật thể/hình ảnh này giúp người xem hiểu ngay câu thoại trong 1 giây không cần đọc chữ* (CẤM ảnh chung chung kiểu `"văn phòng"`, `"bắt tay"`, `"mạng xã hội"`).
   - `"asset_role"` (chọn đúng 1 trong 3 vai trò):
     * `"prop_3d"`: vật thể/đạo cụ thật tách nền nổi 3D (con chip, bìa sách, tờ tiền, thiết bị...) — chọn ảnh chụp nguyên vẹn trọn trong khung, trực diện hoặc nghiêng 3/4, nền sạch (`remove_bg: true`).
     * `"avatar_node"`: chân dung nhân vật thật gắn sơ đồ/vòng tròn — rõ mặt, nhìn thẳng, đủ khoảng thở trên đầu.
     * `"ev_card"`: hiện trường, sự kiện lịch sử, tài liệu báo chí, bản đồ vệ tinh — giữ nguyên `imageFit="contain"`, KHÔNG tách nền (`remove_bg: false`).
   - `"search_queries"` (2–3 truy vấn): luôn ghép **tên riêng chính xác** (nhân vật, mã sản phẩm, địa danh, công ty/hồ sơ thật) + từ khóa chụp thật (`"official photo"`, `"close up"`, `"isolated"`, `"product photography"`, `"archival photo"`; TUYỆT ĐỐI cấm `"3d icon"`, `"render"`, `"vector"`, `"clipart"`, ảnh nhạy cảm/watermark).
2. Kiểm định tư duy đạo diễn `harvest_plan.json`, tải 6 ứng viên `A..F` mỗi mục và xuất `temp/candidates_sheet.jpg` (in nhãn `[PROP 3D]` / `[AVATAR]` / `[EVIDENCE]`, `entity_id` + `must_show`):
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\qc_gate.py" plan --project "D:\DuAn_DangLam\<du_an>"
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\auto_asset_harvester.py" --candidates --manifest "D:\DuAn_DangLam\<du_an>\temp\harvest_plan.json" --project "D:\DuAn_DangLam\<du_an>"
   ```
3. Mở xem **duy nhất** `temp/candidates_sheet.jpg`: với `[PROP 3D]` phải chọn tấm nguyên vẹn 4 góc, không dính tay/vật lạ che khuất; hàng nào chưa khớp `must_show` phải đánh `REJECT`, sửa `search_queries` và chạy `--candidates --only <id>` (tối đa 2 vòng, cấm chọn bừa). Khi đạt 100% thì chốt (nếu báo `CUTOUT_CHOPPED_WARNING` phải đổi ngay ứng viên nguyên vẹn khác):
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\auto_asset_harvester.py" --select "ev_01:B,prop_02:E,..." --manifest "D:\DuAn_DangLam\<du_an>\temp\harvest_plan.json" --project "D:\DuAn_DangLam\<du_an>"
   ```
4. Mở xem `temp/assets_contact_sheet.jpg` xác nhận sạch 100%, nguyên vẹn, lưu kèm `width/height/orientation`.
5. **ĐIỂM DỪNG 2:** Báo cáo danh sách tư liệu kèm `assets_contact_sheet.jpg`. **DỪNG chờ duyệt `"OK"`** mới sang Trạm 3.

---

## TRẠM 3 — Dựng TSX 60fps AE (Mạch Nhân Quả, 0 Đè Chéo) & Kiểm Định QC
1. BẮT BUỘC tra bảng **"Kịch bản nói gì → Gọi món đó"** và Sổ tay Props trong `.agent/COMPONENT_CATALOG.md` + đọc `engine/visual_layout_history.json` để phối đa dạng **>= 5 loại component minh họa khác nhau** (CẤM lặp quá 2 lần cùng 1 món), ưu tiên các đồ chơi đời thật & chiều sâu 2.5D/3D (`ForensicHighlighter`, `EvidenceStringBoard`, `XRayPeelReveal`, `RealLifeArtifact`, `BlueprintMechanism`, `ParallaxDepthStage`, `SpeechPopCard25D`, `Tilt3DFlip`, `AnatomyCallout3D`, `ScaleComparison3D`, `TimelineTrack3D`, `RealPersonSpotlight3D`, `FlowPipeline3D`), không trùng 3 tập gần nhất (chỉ dùng bản đồ khi có địa lý).
2. Lập `temp/choreography_blueprint.json` (`"fps": 60`, **10–16 điểm rơi SFX đắt giá** `{id, type, frame, time_ms}` khớp `words.json`, gắn `"card_snap"` khớp từng `triggerFrame` của `SpeechPopCard25D`, và khai báo **`bgm_segments`** cho cơ chế Music Spotting: đoạn `"hook"` ở 0:00 + 2–4 đoạn `"tension"`/`"climax"`/`"twist"`, tắt nhạc ở các đoạn giải thích thường cho video dài).
   - **Khóa Zero-Trash Đầu Não & Khóa cứng thời lượng (0 giây im lặng thừa):** Viết code tập mới DUY NHẤT vào `D:\DuAn_DangLam\<du_an>\temp\EpisodeComp.tsx` với `export const ACTIVE_DURATION_FRAMES = Math.ceil(voiceDurationSec * 60);` (CẤM cộng đệm thừa cuối video) và `export const ActiveEpisode: React.FC = ...`. **CẤM tạo `.tsx` trong Đầu Não và CẤM sửa `Root.tsx`**. Phần `<HaDaWhyOutroCTA />` (3.5s cuối) phải **hiển thị lồng lên 3.5 giây cuối cùng khi giọng đọc đang chốt câu kết**, TUYỆT ĐỐI KHÔNG kéo dài thêm thời lượng video sau khi giọng đọc đã hết. Nếu có bản đồ địa lý thì chạy `geo_map_builder.py --project "D:\DuAn_DangLam\<du_an>"` để xuất vào `temp/geoPaths.ts`.
   - **Luật giảm chữ:** Mỗi khung hình tối đa 1 thông điệp chữ; nếu tầng giữa đã có bằng chứng/sơ đồ kèm số lớn thì ẩn `KineticHookHeader`; cấm chép nguyên câu thoại lên màn hình; tối đa 12–15 từ/Beat; hạn chế `subline`/`detail`/`eyebrow` dài.
   - Bọc `<CameraStageWrapper />`, ảnh `contain` nguyên vẹn, chữ `BeVietnamProBlack` 2–4 từ `nowrap`, frame `0..30` hiện đủ hình+số, cảnh `> 3s` có `>= 2` biến đổi thị giác, 0 đè chéo, đặt `<HaDaWhyOutroCTA />` ngay trước `<ChannelWatermark9x16 />`, và `<ChannelWatermark9x16 />` ở dòng cuối trước `</AbsoluteFill>`.
3. Chạy kiểm định tới khi `passed: true` (`qc_gate.py tsx` đọc trực tiếp `temp/EpisodeComp.tsx`):
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\qc_gate.py" tsx --project "D:\DuAn_DangLam\<du_an>"
   ```
4. **ĐIỂM DỪNG 3:** Báo cáo kết quả `qc_gate.py tsx`. **DỪNG chờ duyệt `"OK"`** mới sang Trạm 4.

---

## TRẠM 4 — Thumbnail ADN (0 Nhãn Đỏ), Âm Thanh Peak-0ms, Render & QC 3 File Âm
1. Tạo `temp/thumb_props.json` (DUY NHẤT 2 dòng `#22B8FF` + `#FFFFFF`, cấm `topBadgeText`), render bìa 9:16 qua `render_reel.py --thumb-only` (CẤM chạy tay `remotion still` hay copy ảnh vào `public/harvested/`) & cào SEO:
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\render_reel.py" --thumb-only --project "D:\DuAn_DangLam\<du_an>"
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\thumbnail_3d_seo_engine.py" --mode seo --keywords "<kw1>" "<kw2>" --temp-dir "D:\DuAn_DangLam\<du_an>\temp"
   ```
2. Cào mới 100% SFX 6 vai trò (`--sfx-only`, để `render_reel.py` ưu tiên AI tự sinh BGM riêng + áp dụng `bgm_segments` Music Spotting) và chạy render tổng (tự nạp tạm `temp/EpisodeComp.tsx` -> `ActiveEpisode.tsx`, tự dọn sạch 100% Đầu Não trong `finally:`, bàn giao đủ 3 file sang `D:\Video thành phẩm\`):
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\audio_harvester.py" --project "D:\DuAn_DangLam\<du_an>" --sfx-keywords "<kw1,kw2,kw3>" --sfx-only [--include-money]
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\render_reel.py" --project "D:\DuAn_DangLam\<du_an>" --name "HaDaWhy_<TenVideo>" --bgm-mood "<mood>" --sfx-keywords "<kw1,kw2,kw3>"
   ```
3. Mở xem trực tiếp `temp/qc_grid_3x3.jpg` + `temp/thumbnail_9x16.png` và **bắt buộc mở nghe kiểm đủ 3 file âm thanh**: `temp/bgm_only_check.mp3`, `temp/sfx_only_check.mp3`, `temp/master_audio_qc_preview.mp3`.
4. Xuất 3 tiêu đề SEO Evergreen vào `D:\Video thành phẩm\HaDaWhy_<TenVideo>_SEO_Titles.txt` và bàn giao Master MP4 tại `D:\Video thành phẩm\`.
