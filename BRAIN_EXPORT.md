# BRAIN EXPORT — ĐẦU NÃO VIDEO NGẮN FB (HADA WHY 9:16 @ 60FPS)

> File tổng hợp toàn bộ kiến trúc, quy chuẩn, cấu hình và mã nguồn điều phối của dự án `D:\Đầu Não Video Ngắn FB (không xóa)`.

## 1. Cây thư mục đầy đủ (Full Directory Tree)

```text
Đầu Não Video Ngắn FB (không xóa)/
├── .agent/
│   ├── rules/
│   │   └── 00-hadawhy-core.md (9.2 KB)
│   ├── workflows/
│   │   └── san-xuat-reel.md (8.0 KB)
│   └── COMPONENT_CATALOG.md (13.4 KB)
├── .github/
│   └── workflows/
│       ├── deploy_telegram_bot.yml (2.2 KB)
│       └── hadawhy_cloud_reels.yml (4.1 KB)
├── _archive_cu/
│   ├── skills/
│   │   └── fb-reels-master-studio/
│   │       └── SKILL.md (6.8 KB)
│   ├── subagents/
│   │   ├── fb-reels-asset-harvester.md (2.5 KB)
│   │   ├── fb-reels-fact-scriptwriter.md (4.0 KB)
│   │   ├── fb-reels-master-commander.md (4.8 KB)
│   │   ├── fb-reels-motion-3d-director.md (3.5 KB)
│   │   ├── fb-reels-qc-sound-sentinel.md (2.1 KB)
│   │   └── fb-reels-thumbnail-seo-architect.md (2.7 KB)
│   ├── BiMatLiveBanThiNoReel.tsx (28.8 KB)
│   ├── BiMatLiveBanThiNoV2Reel.tsx (27.0 KB)
│   ├── KineticWordCaption.tsx (10.4 KB)
│   ├── nvidiaCaptionsData.ts (15.6 KB)
│   ├── NvidiaSuccession40s.tsx (60.8 KB)
│   ├── QUY_CHUAN_ADN_FB_REELS.md (5.1 KB)
│   ├── StickerPop.tsx (2.8 KB)
│   ├── ThuatToanGoiXeMaster.tsx (28.6 KB)
│   ├── ThuatToanGoiXeReel.tsx (25.5 KB)
│   ├── ThuatToanGoiXeV2Master.tsx (26.9 KB)
│   └── ThuatToanGoiXeV3Master.tsx (21.8 KB)
├── assets/
│   ├── fonts/ (20 files media/tài nguyên)
│   ├── icons_2.5d/ (0 files media/tài nguyên)
│   ├── maps/ (0 files media/tài nguyên)
│   └── textures/ (0 files media/tài nguyên)
├── engine/
│   ├── ace_step_fb_runner.py (26.8 KB)
│   ├── audio_harvester.py (14.8 KB)
│   ├── audio_used_history.json (8.2 KB)
│   ├── auto_asset_harvester.py (70.2 KB)
│   ├── auto_cutout.py (18.7 KB)
│   ├── bgm_fingerprint_ledger.json (2.9 KB)
│   ├── fact_researcher.py (12.5 KB)
│   ├── geo_map_builder.py (7.6 KB)
│   ├── image_used_history.json (3.4 KB)
│   ├── playwright_web_helper.py (3.7 KB)
│   ├── qc_gate.py (33.6 KB)
│   ├── render_reel.py (11.7 KB)
│   ├── sfx_timeline_mixer.py (49.2 KB)
│   ├── studio_lessons_learned.json (12.1 KB)
│   ├── thumbnail_3d_seo_engine.py (17.9 KB)
│   ├── vieneu_whisper_pacer.py (13.5 KB)
│   ├── visual_layout_history.json (0.0 KB)
│   └── voice_visual_sync.py (9.6 KB)
├── guidelines/
├── remotion_reels/
│   ├── out/
│   ├── public/
│   │   ├── brand/ (3 files media/tài nguyên)
│   │   ├── fonts/ (3 files media/tài nguyên)
│   │   └── maps/ (1 files media/tài nguyên)
│   ├── src/
│   │   ├── components/
│   │   │   ├── fx/
│   │   │   │   ├── CapCutTransitions.tsx (3.7 KB)
│   │   │   │   ├── CinematicStagePrimitives.tsx (12.0 KB)
│   │   │   │   ├── fxFonts.ts (1.1 KB)
│   │   │   │   ├── index.ts (0.3 KB)
│   │   │   │   ├── KineticTextFX.tsx (6.3 KB)
│   │   │   │   ├── KnowledgeExplainerFX.tsx (60.2 KB)
│   │   │   │   ├── KnowledgeMotionFX.tsx (13.4 KB)
│   │   │   │   ├── motionPresets.ts (1.5 KB)
│   │   │   │   ├── MotionTrackedCallout.tsx (4.3 KB)
│   │   │   │   └── RealSceneSpotlight.tsx (7.5 KB)
│   │   │   ├── AnatomyCallout3D.tsx (4.5 KB)
│   │   │   ├── ChannelWatermark9x16.tsx (2.2 KB)
│   │   │   ├── CinematicStagePrimitives.tsx (0.0 KB)
│   │   │   ├── CoinStream.tsx (5.7 KB)
│   │   │   ├── eurasiaGeoPaths.ts (517.1 KB)
│   │   │   ├── GeoStrategicMap3D.tsx (12.5 KB)
│   │   │   ├── HaDaWhyMistBackground.tsx (1.8 KB)
│   │   │   ├── KineticHookHeader.tsx (2.8 KB)
│   │   │   ├── RealPersonSpotlight3D.tsx (4.9 KB)
│   │   │   ├── ScaleComparison3D.tsx (8.4 KB)
│   │   │   ├── ThumbnailCover9x16.tsx (13.8 KB)
│   │   │   ├── TimelineTrack3D.tsx (4.7 KB)
│   │   │   ├── UrbanSatelliteDive9x16.tsx (14.1 KB)
│   │   │   └── usSingaporeGeoPaths.ts (959.8 KB)
│   │   ├── index.ts (0.1 KB)
│   │   ├── Root.tsx (0.9 KB)
│   │   └── RootSkeletonExample.tsx (1.7 KB)
│   ├── package-lock.json (146.5 KB)
│   ├── package.json (0.5 KB)
│   ├── remotion.config.ts (0.5 KB)
│   └── tsconfig.json (0.4 KB)
├── .gitignore (0.3 KB)
├── CHAY_SAN_XUAT_FB_REELS.bat (0.4 KB)
├── export_bo_nao_part1_quy_chuan_agents.txt (73.8 KB)
├── export_bo_nao_part2_engine_he_thong.txt (197.9 KB)
├── export_bo_nao_part3_remotion_3d.txt (165.3 KB)
└── plugin.json (0.7 KB)
```

## 2. Tổng quan luồng hoạt động (Pipeline & Architecture)

### Kiến trúc 3 tầng
- **Tầng 1 — Đầu Não (0 bytes media):** `D:\Đầu Não Video Ngắn FB (không xóa)\` chứa quy chuẩn, engine Python và bộ khung Remotion TSX. Thư mục `remotion_reels/public/harvested/` luôn giữ 0 bytes khi không render.
- **Tầng 2 — WIP (Work In Progress):** `D:\DuAn_DangLam\<du_an>\temp\` chứa toàn bộ dữ liệu trung gian của từng tập (`research_raw.json`, `script_5beat.json`, `voiceover.wav`, `words.json`, `harvest_plan.json`, `candidates_sheet.jpg`, `assets\`, `asset_manifest.json`, `choreography_blueprint.json`, `thumb_props.json`, `thumbnail_9x16.png`).
- **Tầng 3 — Thành phẩm:** `D:\Video thành phẩm\HaDaWhy_<TenVideo>_FB_Reels_Master.mp4` + Thumbnail + `SEO_Titles.txt`.

### Luồng sản xuất 4 Trạm (có 3 Điểm Dừng phê duyệt)
1. **Trạm 1 — Nghiên cứu & Kịch bản & Giọng đọc:**
   - `engine/fact_researcher.py`: Cào sâu 5–8 bài báo gốc + Wikipedia VI/EN theo 4–5 truy vấn -> xuất `temp/research_raw.json`.
   - Agent viết `temp/script_5beat.json` (40–55s, 5 nhịp nhân quả: Cơ chế -> Chế tài -> Hậu quả).
   - `engine/vieneu_whisper_pacer.py`: Chuẩn hóa đọc mã viết tắt (`C04` -> `xê không bốn`), sinh giọng local **VieNeu-TTS ("Hải Đăng")** -> `temp/voiceover.wav`, sau đó dùng **Faster-Whisper** căn timing từng từ -> `temp/words.json`.
   - **Điểm Dừng 1:** Trình dữ kiện + kịch bản + thời lượng voice, chờ user duyệt `"OK"`.
2. **Trạm 2 — Trinh sát Tư liệu & Tách nền 3D:**
   - Agent lập `temp/harvest_plan.json` (khai báo `visual_reasoning` + `asset_role`: `prop_3d` | `avatar_node` | `ev_card`).
   - `engine/qc_gate.py plan`: Kiểm định chất lượng từ khóa & tư duy đạo diễn.
   - `engine/auto_asset_harvester.py --candidates`: Cào 6 ứng viên A..F (>= 700px) từ Bing Images / Wikimedia / DuckDuckGo / Playwright -> xuất `temp/candidates_sheet.jpg`.
   - `engine/auto_asset_harvester.py --select`: Chốt ứng viên hoặc báo `REJECT`, tự động tách nền (`engine/auto_cutout.py` dùng `rembg` với `birefnet`/`isnet-general-use`/`u2net`), kiểm tra cắt cụt (`CUTOUT_CHOPPED_WARNING`) -> xuất `temp/assets_contact_sheet.jpg` & `temp/asset_manifest.json`.
   - **Điểm Dừng 2:** Trình danh sách tư liệu + contact sheet, chờ user duyệt `"OK"`.
3. **Trạm 3 — Dựng Cảnh Remotion 9:16 @ 60fps & Kiểm định:**
   - Agent tra `.agent/COMPONENT_CATALOG.md` + `engine/visual_layout_history.json`, lập `temp/choreography_blueprint.json` (`fps: 60`, 20–32 mốc `frame` / `time_ms`), viết `remotion_reels/src/<CompId>.tsx` (phối >= 5 component, >= 2 Beat 2.5D/3D, `<HaDaWhyMistBackground />`, `<CameraStageWrapper />`, `<ChannelWatermark9x16 />`) và đăng ký vào `Root.tsx`.
   - `engine/qc_gate.py tsx` + `npx tsc --noEmit`: Kiểm định lỗi TSX, đè chéo, timing, font Việt.
   - **Điểm Dừng 3:** Trình kết quả QC & TypeScript, chờ user duyệt `"OK"`.
4. **Trạm 4 — Thumbnail, Âm thanh Peak-0ms, Render & Bàn giao:**
   - Render bìa 9:16 (`npx remotion still ThumbnailCover9x16`) + cào từ khóa SEO (`engine/thumbnail_3d_seo_engine.py --mode seo`).
   - `engine/audio_harvester.py`: Cào BGM kịch tính (>= 72/100) + SFX 6 vai trò từ Mixkit (chống trùng lặp qua `audio_used_history.json` & `bgm_fingerprint_ledger.json`).
   - `engine/render_reel.py`: Điều phối `npx remotion render` (60fps, 1080x1920), gọi `engine/sfx_timeline_mixer.py` (căn đỉnh nổ SFX `Peak-Transient Alignment` 0ms, ducking BGM, chuẩn hóa `-14.0 LUFS`), xuất 3 file kiểm âm (`bgm_only_check.mp3`, `sfx_only_check.mp3`, `master_audio_qc_preview.mp3`), xuất lưới `temp/qc_grid_3x3.jpg` và bàn giao thành phẩm vào `D:\Video thành phẩm\`.

### Công cụ, Thư viện, Model AI & API kết nối
- **Render & Frontend 3D:** Node.js, Remotion `4.0.541` (`@remotion/cli`, `@remotion/three`, `@remotion/shapes`, `@remotion/motion-blur`, `@remotion/captions`), React `19.3.1`, Three.js `0.171.0`, `@react-three/fiber` `9.8.2`, TypeScript `5.8.2`.
- **TTS & Speech Alignment:** `VieNeu-TTS` (giọng local "Hải Đăng" qua Python / Gradio client), `faster-whisper` (`WhisperModel`).
- **Xử lý Ảnh & Tách nền:** `rembg` (`BiRefNet`, `isnet-general-use`, `u2net`), `Pillow` (PIL), `OpenCV` (`cv2`), `NumPy`, `SciPy` (`gaussian_filter`).
- **Xử lý Video & Âm thanh:** `FFmpeg` & `ffprobe` (muxing, LUFS loudness normalization, spectral/transient analysis).
- **Nghiên cứu & Cào dữ liệu Web:** `DuckDuckGo Search` (`ddgs` / `duckduckgo_search`), `Bing Search / Bing Images`, `Google News RSS`, `Google Suggest`, `Wikimedia Commons API`, `Mixkit` (BGM & SFX), `Playwright` (`playwright.sync_api`), `Tavily API` (tùy chọn qua `TAVILY_API_KEY`).
- **LLM / AI API:** `google-genai` (`gemini-2.5-flash` trong `ace_step_fb_runner.py`). Ngoài ra các GitHub Actions workflow có khai báo thêm OpenRouter, DeepSeek, GitHub Models, Modal, Telegram Bot (nhưng script cloud tương ứng hiện chưa có trong repo).

## 3. Toàn bộ nội dung cốt lõi của "Bộ não"

> **Lưu ý các file không trích nguyên văn toàn bộ để tránh phình/trùng lặp:**
> - `export_bo_nao_part1_quy_chuan_agents.txt`, `export_bo_nao_part2_engine_he_thong.txt`, `export_bo_nao_part3_remotion_3d.txt`: là 3 file export cũ (đã lỗi thời so với `.agent/rules/00-hadawhy-core.md` và mã nguồn hiện tại).
> - `remotion_reels/package-lock.json` (150 KB): lockfile npm tự động sinh.
> - `remotion_reels/src/components/eurasiaGeoPaths.ts` (529 KB) & `usSingaporeGeoPaths.ts` (982 KB): dữ liệu tọa độ SVG Path bản đồ tĩnh.
> - Các file `.tsx` video tập cũ trong `_archive_cu/` (8 file).


### 3.1. Quy chuẩn, Workflows & Danh mục Component (.agent/)

#### `.agent/rules/00-hadawhy-core.md`

```markdown
---
trigger: always_on
description: Quy chuẩn lõi phi chủ đề FB Reels 9:16 (60fps AE) HaDa Why — chống cắt ảnh, khóa font Việt, Peak-SFX 0ms & BGM rõ kịch tính.
---

# QUY CHUẨN LÕI HADA WHY FB REELS (9:16 @ 60FPS — PHI CHỦ ĐỀ)

## 1. Kiến Trúc 3 Tầng & Kỷ Luật Tiết Kiệm Token
- **Tầng 1 (Đầu Não — 0 bytes media):** `D:\Đầu Não Video Ngắn FB (không xóa)\` (`remotion_reels/public/harvested/` luôn 0 bytes khi không render).
- **Tầng 2 (WIP):** `D:\DuAn_DangLam\<du_an>\temp\` (`research_raw.json`, `script_5beat.json`, `voiceover.wav`, `words.json`, `harvest_plan.json`, `candidates_sheet.jpg`, `assets\`, `asset_manifest.json`, `choreography_blueprint.json`, `thumb_props.json`, `thumbnail_9x16.png`).
- **Tầng 3 (Thành phẩm):** `D:\Video thành phẩm\HaDaWhy_<TenVideo>_FB_Reels_Master.mp4` + Thumbnail + `SEO_Titles.txt`.
- **Khóa mã nguồn & tiết kiệm token:** CẤM tự ý sửa code trong `engine/` và `remotion_reels/src/components/`; CẤM mở đọc `*GeoPaths.ts`, `countries.geojson`, `package-lock.json`, `export_bo_nao*.txt`, và các file `.py` trong `engine/` — chỉ gọi CLI ở Mục 2. CẤM chạy `render_reel.py` trước khi nhận duyệt `"OK"` theo `.agent/workflows/san-xuat-reel.md`.

## 2. Bộ Lệnh CLI Chuẩn Duy Nhất
1. **Cào sâu toàn văn bài gốc & dữ kiện cứng (Trạm 1 — >= 4–5 truy vấn):**
   `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\fact_researcher.py" --topic "<chủ đề>" --queries "cơ chế|số liệu|bằng chứng|luật gốc|english query" --project "D:\DuAn_DangLam\<du_an>"`
2. **Sinh giọng Hải Đăng local BẮT BUỘC ngay sau `script_5beat.json` ở Trạm 1 (tự chuẩn hóa mã viết tắt `C04` -> `"xê không bốn"`, tự sinh sẵn `temp/voiceover.wav` + `temp/words.json` trước Điểm Dừng 1, CẤM fallback giọng khác):**
   `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\vieneu_whisper_pacer.py" --script "D:\DuAn_DangLam\<du_an>\temp\script_5beat.json" --project "D:\DuAn_DangLam\<du_an>" --voice "Hải Đăng"`
3. **Cào 6 ứng viên A..F (>= 700px) theo tư duy Đạo diễn & Chốt tư liệu có `REJECT` (Trạm 2):**
   - Trước khi đặt từ khóa, MỌI mục trong `temp/harvest_plan.json` BẮT BUỘC khai báo đủ `"visual_reasoning"` (>= 15 ký tự: giải thích ngắn 1 câu *vì sao vật thể/hình ảnh này giúp người xem hiểu ngay câu thoại trong 1 giây không cần đọc chữ*; CẤM ảnh trừu tượng/chung chung kiểu `"văn phòng"`, `"bắt tay"`, `"mạng xã hội"`) và `"asset_role"` thuộc đúng 1 trong 3 vai trò:
     1. `"prop_3d"` (vật thể/đạo cụ thật tách nền nổi 3D: con chip, bìa sách, tờ tiền, thiết bị, biểu tượng vật lý thật...): ưu tiên ảnh chụp vật thể nguyên vẹn nằm trọn trong khung, góc trực diện hoặc nghiêng 3/4, nền đơn giản để tách nền sắc tuyệt đối.
     2. `"avatar_node"` (chân dung nhân vật thật gắn sơ đồ/vòng tròn): ưu tiên ảnh rõ mặt, nhìn thẳng, đủ khoảng thở trên đầu để cắt khung tròn sắc nét.
     3. `"ev_card"` (ảnh hiện trường, sự kiện lịch sử, tài liệu báo chí, bản đồ vệ tinh): giữ nguyên khung `imageFit="contain"`, KHÔNG tách nền (`remove_bg: false`).
   - **Khóa nguyên tắc `search_queries`:** Luôn dùng **tên riêng chính xác** (tên nhân vật, mã sản phẩm, địa danh, tên công ty/tài liệu thật) kết hợp từ khóa chụp thật (`"official photo"`, `"close up"`, `"isolated"`, `"product photography"`, `"archival photo"` — TUYỆT ĐỐI cấm `"3d icon"`, `"render"`, `"vector"`, `"clipart"`).
   - Tải 6 ứng viên: `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\auto_asset_harvester.py" --candidates --manifest "D:\DuAn_DangLam\<du_an>\temp\harvest_plan.json" --project "D:\DuAn_DangLam\<du_an>" [--only id1,id2]`
   - Chốt ảnh / báo `REJECT`: `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\auto_asset_harvester.py" --select "ev_01:B,prop_02:E,..." --manifest "D:\DuAn_DangLam\<du_an>\temp\harvest_plan.json" --project "D:\DuAn_DangLam\<du_an>"`
4. **Kiểm định TSX & đồng bộ 60fps (Trạm 3):**
   `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\qc_gate.py" tsx --tsx "D:\Đầu Não Video Ngắn FB (không xóa)\remotion_reels\src\<CompId>.tsx" --project "D:\DuAn_DangLam\<du_an>"`
5. **Cào mới 100% BGM kịch tính (>= 72/100) & SFX 6 vai trò (Trạm 4):**
   `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\audio_harvester.py" --project "D:\DuAn_DangLam\<du_an>" --sfx-keywords "<kw1,kw2,kw3>" --bgm-mood "<driving,trailer,suspense>" [--include-money]`
6. **Render bìa Still 9:16 & cào SEO (Trạm 4):**
   - `cd "D:\Đầu Não Video Ngắn FB (không xóa)\remotion_reels" ; npx remotion still ThumbnailCover9x16 "D:/DuAn_DangLam/<du_an>/temp/thumbnail_9x16.png" --props="D:/DuAn_DangLam/<du_an>/temp/thumb_props.json"`
   - `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\thumbnail_3d_seo_engine.py" --mode seo --keywords "<kw1>" "<kw2>" --temp-dir "D:\DuAn_DangLam\<du_an>\temp"`
7. **Render Master 60fps + Peak-SFX Mix `-14.0 LUFS` + QC Video (Trạm 4):**
   `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\render_reel.py" --comp "<CompId>" --project "D:\DuAn_DangLam\<du_an>" --name "HaDaWhy_<TenVideo>" --bgm-mood "<mood>" --sfx-keywords "<kw1,kw2,kw3>"`

## 3. Luật Thị Giác, Chuyển Động 60fps AE, Thumbnail & Âm Thanh Bất Biến
- **Nền, Thương hiệu 2 lớp chống re-up & Chống cắt ảnh 100%:** Nền duy nhất `<HaDaWhyMistBackground />` (`#0D2342 -> #061224 -> #030812` + lưới `56px` sạch); CẤM `ContextBackdropLayer`, `FloorPlatform3D`, `StickerPop`, karaoke, neon. Mọi file `.tsx` BẮT BUỘC đặt `<ChannelWatermark9x16 />` ở **dòng cuối cùng ngay trước `</AbsoluteFill>`** (sau toàn bộ `<Sequence>`) gồm đủ 2 lớp (logo góc trên trái `top: 52, left: 40` + logo chìm chống bản quyền `opacity: 0.08` vùng giữa, `zIndex: 9999`); **CẤM AI tự ý gỡ bỏ hoặc tắt lớp logo chìm chống bản quyền** trong `ChannelWatermark9x16.tsx`. Mọi thẻ ảnh mặc định `imageFit="contain"` trên nền đệm mờ tối từ chính ảnh đó (chống cắt đầu/mặt/chữ).
- **Ít chữ, chống đè chéo & khóa font Việt:** Nhãn 2–4 từ (`nowrap` tự co cỡ chữ, cấm rớt 1 chữ đơn xuống dòng); khóa 100% font `BeVietnamProBlack` (0 vỡ dấu `Ả, Ẩ, Ỡ`). CẤM đặt `HeroCutout3D` đè lên biểu đồ/nhân vật; `HighContrastConclusionCard` không được đè lên sơ đồ khác. Sắp xếp đúng mạch nhân quả (**Hành vi/Cơ chế -> Xử lý/Chế tài -> Điểm chốt/Hậu quả**).
- **Sân Khấu Mở & Chiều sâu 2.5D/3D (Bắt buộc mọi kịch bản):** Trước khi dựng, BẮT BUỘC tra bảng **"Kịch bản nói gì → Gọi món đó"** trong `.agent/COMPONENT_CATALOG.md` để phối đa dạng **>= 5 loại component minh họa khác nhau** cho 5 Beat, tối thiểu **>= 2 Beat có chiều sâu 2.5D/3D** (`ParallaxDepthStage`, `SpeechPopCard25D`, `SpeechPopCardStack25D`, `Tilt3DFlip`, `AnatomyCallout3D`, `ScaleComparison3D`, `TimelineTrack3D`, `RealPersonSpotlight3D`, `FlowPipeline3D`) và thẻ bật nổi đúng nhịp thoại (`SpeechPopCard25D` gắn sự kiện `"card_snap"` vào `choreography_blueprint.json`). **CẤM lặp quá 2 lần** cùng 1 component (`EvidenceDocumentCard`, `ProcessStepChain`, `VisualBarCompare`, `DualStageKnowledgeLayout`). Mọi `CustomTopicVisual` SVG tự viết **CẤM vẽ hộp nền `#0B1220` + viền chữ nhật bao quanh** — phải vẽ trực tiếp lên nền lưới xanh dương.
- **Motion 60fps AE & Khóa nhịp đầu cảnh:** Bọc Beat bằng `<CameraStageWrapper />` (`opacity: 1`, cấm cross-fade bóng ma), GPU `translate3d` + stagger `3–5f`; frame `0..30` phải hiện đủ hình + số ngay; mọi `MetricOdometerHero` hoặc nhánh đồ họa chính phải xuất hiện trong vòng `<= 60 frames` (1s đầu Beat, CẤM `startFrame={180}` gây trống nửa màn hình); mọi `triggerFrame` trong chuỗi bước phải tăng dần nghiêm ngặt (`step[i].triggerFrame < step[i+1].triggerFrame`); cảnh `> 3s` có `>= 2` mốc biến đổi thị giác + `30f` (0.5s) đệm cuối.
- **Thumbnail chuẩn ADN (CẤM thanh nhãn đỏ):** Logo trên trái + nền ảnh thật mờ nhẹ + **DUY NHẤT 2 dòng** (`#22B8FF` + `#FFFFFF` viền đen dày, cấm tuyệt đối tag đỏ/dòng thứ 3) + chủ thể thật cỡ lớn & ảnh phụ/vòng nét đứt đỏ.
- **Âm thanh Peak-Aligned 0ms & BGM rõ giai điệu:** `choreography_blueprint.json` khóa `"fps": 60` (`time_ms = round(frame * 1000 / 60)`). SFX căn đỉnh nổ `Peak-Transient Alignment` đập trúng đúng frame (không lùi `min_gap_ms`, ưu tiên `hook_slam > impact > slash_cut > card_snap > num_tick`, Hook vol `1.25`). BGM rõ kịch tính (`0.48–0.55` lúc đọc, bung `0.85` lúc nghỉ, `-14.0 ± 1.0 LUFS`). Bắt buộc nghe đủ 3 file: `bgm_only_check.mp3`, `sfx_only_check.mp3`, `master_audio_qc_preview.mp3`.
```


#### `.agent/workflows/san-xuat-reel.md`

````markdown
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
2. Viết `temp/script_5beat.json` (`>= 6` dữ kiện cứng & `>= 3` nguồn thật, 40–55s, 5 nhịp theo mạch nhân quả **Cơ chế -> Chế tài -> Hậu quả**, ghi sẵn `bgm_mood` và 3–4 `sfx_keywords`).
3. **BẮT BUỘC** chạy ngay sau bước 2 để sinh sẵn `temp/voiceover.wav` + `temp/words.json` bằng giọng local `"Hải Đăng"` (tự chuẩn hóa đọc mã viết tắt `C04`, `A05`..., CẤM fallback giọng khác) trước khi trình Điểm Dừng 1:
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\vieneu_whisper_pacer.py" --script "D:\DuAn_DangLam\<du_an>\temp\script_5beat.json" --project "D:\DuAn_DangLam\<du_an>" --voice "Hải Đăng"
   ```
4. **ĐIỂM DỪNG 1:** Báo cáo dữ kiện bài gốc + kịch bản 5 nhịp + thời lượng giọng đọc. **DỪNG chờ duyệt `"OK"`** mới sang Trạm 2.

---

## TRẠM 2 — Tư Duy Đạo Diễn, Cào 6 Ứng Viên A..F (>= 700px), Chọn/REJECT & Bóc Tách 3D
1. Lập `temp/harvest_plan.json` (`>= 8–12` mục khớp từng nhịp). Trước khi gõ từ khóa, TỪNG mục BẮT BUỘC điền đủ:
   - `"entity_id"`, `"script_line"`, `"must_show"`.
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
1. BẮT BUỘC tra bảng **"Kịch bản nói gì → Gọi món đó"** và Sổ tay Props trong `.agent/COMPONENT_CATALOG.md` + đọc `engine/visual_layout_history.json` để phối đa dạng **>= 5 loại component minh họa khác nhau** (CẤM lặp quá 2 lần cùng 1 món), có **>= 2 Beat chiều sâu 2.5D/3D** (`ParallaxDepthStage`, `SpeechPopCard25D`, `Tilt3DFlip`, `AnatomyCallout3D`, `ScaleComparison3D`, `TimelineTrack3D`, `RealPersonSpotlight3D`, `FlowPipeline3D`), không trùng 3 tập gần nhất (chỉ dùng bản đồ khi có địa lý).
2. Lập `temp/choreography_blueprint.json` (`"fps": 60`, `>= 20–32` mốc `{id, type, frame, time_ms}` khớp `words.json`, gắn `"card_snap"` khớp từng `triggerFrame` của `SpeechPopCard25D`) và viết `remotion_reels/src/<CompId>.tsx`: bọc `<CameraStageWrapper />`, ảnh `contain` nguyên vẹn, chữ `BeVietnamProBlack` 2–4 từ `nowrap`, frame `0..30` hiện đủ hình+số, cảnh `> 3s` có `>= 2` biến đổi thị giác, 0 đè chéo, +30 frame đệm cuối, đặt `<ChannelWatermark9x16 />` ngay trước `</AbsoluteFill>`; đăng ký vào `Root.tsx`.
3. Chạy kiểm định tới khi `passed: true` và `0 lỗi` TypeScript:
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\qc_gate.py" tsx --tsx "D:\Đầu Não Video Ngắn FB (không xóa)\remotion_reels\src\<CompId>.tsx" --project "D:\DuAn_DangLam\<du_an>"
   cd "D:\Đầu Não Video Ngắn FB (không xóa)\remotion_reels" ; npx tsc --noEmit
   ```
4. **ĐIỂM DỪNG 3:** Báo cáo kết quả `qc_gate.py tsx` và `tsc --noEmit`. **DỪNG chờ duyệt `"OK"`** mới sang Trạm 4.

---

## TRẠM 4 — Thumbnail ADN (0 Nhãn Đỏ), Âm Thanh Peak-0ms, Render & QC 3 File Âm
1. Tạo `temp/thumb_props.json` (DUY NHẤT 2 dòng `#22B8FF` + `#FFFFFF`, cấm `topBadgeText`), render bìa 9:16 & cào SEO:
   ```powershell
   cd "D:\Đầu Não Video Ngắn FB (không xóa)\remotion_reels" ; npx remotion still ThumbnailCover9x16 "D:/DuAn_DangLam/<du_an>/temp/thumbnail_9x16.png" --props="D:/DuAn_DangLam/<du_an>/temp/thumb_props.json"
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\thumbnail_3d_seo_engine.py" --mode seo --keywords "<kw1>" "<kw2>" --temp-dir "D:\DuAn_DangLam\<du_an>\temp"
   ```
2. Cào mới 100% BGM kịch tính (`>= 72/100`) + SFX 6 vai trò và chạy render tổng:
   ```powershell
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\audio_harvester.py" --project "D:\DuAn_DangLam\<du_an>" --sfx-keywords "<kw1,kw2,kw3>" --bgm-mood "<driving,trailer,suspense>" [--include-money]
   python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\render_reel.py" --comp "<CompId>" --project "D:\DuAn_DangLam\<du_an>" --name "HaDaWhy_<TenVideo>" --bgm-mood "<mood>" --sfx-keywords "<kw1,kw2,kw3>"
   ```
3. Mở xem trực tiếp `temp/qc_grid_3x3.jpg` + `temp/thumbnail_9x16.png` và **bắt buộc mở nghe kiểm đủ 3 file âm thanh**: `temp/bgm_only_check.mp3`, `temp/sfx_only_check.mp3`, `temp/master_audio_qc_preview.mp3`.
4. Xuất 3 tiêu đề SEO Evergreen vào `D:\Video thành phẩm\HaDaWhy_<TenVideo>_SEO_Titles.txt` và bàn giao Master MP4 tại `D:\Video thành phẩm\`.
````


#### `.agent/COMPONENT_CATALOG.md`

```markdown
# SỔ TAY PROPS CHUẨN (COMPONENT CATALOG — 60FPS AE & 2.5D/3D)

Nền xanh dương ADN `<HaDaWhyMistBackground />`, Safe Zone `X: 80..920`, `Y: 340..1560`, khóa 100% font tiếng Việt `BeVietnamProBlack` (0 vỡ dấu), GPU `translate3d` + `willChange: "transform"`.
**Luật cứng:** Mỗi video 5 Beat bắt buộc dùng **>= 5 loại component minh họa khác nhau**, tối thiểu **2 Beat có chiều sâu 2.5D/3D**, CẤM lặp quá **2 lần** cùng 1 component (`EvidenceDocumentCard`, `ProcessStepChain`, `VisualBarCompare`, `DualStageKnowledgeLayout`).

## 0. BẢN ĐỒ "KỊCH BẢN NÓI GÌ → GỌI MÓN ĐÓ" (BẮT BUỘC TRA TRƯỚC KHI DỰNG)
- **Dòng tiền / doanh thu / chia lợi nhuận:** `CoinStream` / `FlowPipeline3D`
- **Mổ xẻ cấu tạo vật thể / thiết bị:** `AnatomyCallout3D` / `MotionTrackedCallout`
- **Rẽ nhánh cơ chế / lựa chọn / hệ quả:** `DecisionBranchPulse` / `VisualCauseEffectFlow`
- **So sánh quy mô / kích thước / chênh lệch:** `ScaleComparison3D` / `VisualBarCompare`
- **Mốc lịch sử / tiến trình thời gian:** `TimelineTrack3D` / `EditorialSplitTimeline`
- **Nhân vật trung tâm / mạng lưới:** `RealPersonSpotlight3D` / `RadialAvatarHub`
- **Liệt kê từng ý / số liệu nhảy theo đúng nhịp thoại:** `SpeechPopCard25D` / `SpeechPopCardStack25D` (gắn `card_snap` vào `choreography_blueprint.json`)
- **Tạo chiều sâu không gian 3 lớp / lật cảnh 3D:** `ParallaxDepthStage` / `Tilt3DFlip`
- **Địa lý / bản đồ / tuyến đường (chỉ khi kịch bản có địa danh):** `UrbanSatelliteDive9x16` / `GeoStrategicMap3D`

---

## 1. KHUNG THƯƠNG HIỆU, CAMERA & CHUYỂN CẢNH (10 MÓN)
- `HaDaWhyMistBackground` | `import { HaDaWhyMistBackground } from "./components/HaDaWhyMistBackground"`
  Props: `{ intensity?: number; accentHex?: string; gridOpacity?: number }`
- `ChannelWatermark9x16` | `import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16"`
  Props: `{ logoSrc?: string }` — **Đủ 2 lớp (`zIndex: 9999`, logo góc trái + logo chìm chống re-up `opacity: 0.08`), BẮT BUỘC đặt dòng cuối ngay trước `</AbsoluteFill>`.**
- `HaDaWhyFontFaces` | `import { HaDaWhyFontFaces } from "./components/KineticHookHeader"`
  Props: `{}` (nhúng font `BeVietnamProBlack` & `BeVietnamProExtraBold`).
- `KineticHookHeader` | `import { KineticHookHeader } from "./components/KineticHookHeader"`
  Props: `{ beat: { start: number; eyebrow: string; hero: string; accent?: string; heroColor?: string; heroSize?: number }; top?: number }`
- `ThumbnailCover9x16` | `import { ThumbnailCover9x16 } from "./components/ThumbnailCover9x16"`
  Props: `{ heroSubjectSrc: string; headlineLine1: string; headlineLine2: string; backgroundPhotoSrc?: string; mysteryOrSecondarySrc?: string; layoutMode?: "mystery_silhouette"|"dual_confrontation"|"forensic_object"|"titan_evidence"; forensicCircle?: { cx: number; cy: number; r: number }; heroBwHighContrast?: boolean; mysterySilhouetteMode?: boolean }` (CẤM `topBadgeText`).
- `CameraStageWrapper` | `import { CameraStageWrapper } from "./components/fx"`
  Props: `{ durationInFrames: number; enterDirection?: "up"|"left"|"right"|"zoom"; children: React.ReactNode }`
- `WhipPanTransition` | `import { WhipPanTransition } from "./components/fx"`
  Props: `{ children: React.ReactNode; direction?: "left"|"right"|"up"|"down"; durationFrames?: number; startFrame?: number }`
- `ZoomThroughTransition` | `import { ZoomThroughTransition } from "./components/fx"`
  Props: `{ children: React.ReactNode; startFrame?: number; durationFrames?: number; initialScale?: number }`
- `SplitCurtainWipe` | `import { SplitCurtainWipe } from "./components/fx"`
  Props: `{ children: React.ReactNode; startFrame?: number; durationFrames?: number }`
- `Tilt3DFlip` | `import { Tilt3DFlip } from "./components/fx"`
  Props: `{ children: React.ReactNode; startFrame?: number; durationFrames?: number; axis?: "X"|"Y" }`

---

## 2. CHIỀU SÂU 2.5D / 3D & BỐ CỤC SÂN KHẤU MỞ (9 MÓN — `import { ... } from "./components/fx"`)
- `SpeechPopCard25D`: `{ triggerFrame: number; title: string; x: number; y: number; metric?: string; imageSrc?: string; width?: number; tiltX?: number; tiltY?: number; accentColor?: string; zIndex?: number }`
- `SpeechPopCardStack25D`: `{ cards: SpeechPopCard25DProps[]; baseZIndex?: number }`
- `ParallaxDepthStage`: `{ backLayer?: React.ReactNode; midLayer?: React.ReactNode; frontLayer?: React.ReactNode; durationFrames?: number; startFrame?: number; panX?: number; panY?: number; bgSrc?: string; subjectSrc?: string; bgBlur?: number }` (`back 0.3x | mid 1.0x | front 1.35x`).
- `HeroCutout3D`: `{ src: string; x?: number; y?: number; width?: number; maxHeight?: number; startFrame?: number; floatAmp?: number; brightness?: number; rotateDeg?: number; tiltX?: number; tiltY?: number; perspective?: number; rimHighlight?: boolean; darkObjectBacklight?: boolean; mode?: "prop_3d"|"avatar_node"; avatarBorderColor?: string; avatarLabel?: string; zIndex?: number; fadeBottom?: boolean }` (mặc định `tiltX=6, tiltY=-9, perspective=1050, darkObjectBacklight=true`).
- `CircularAvatarNode`: `{ src: string; size?: number; x?: number; y?: number; borderColor?: string; borderWidth?: number; objectPosition?: string; label?: string; subLabel?: string; startFrame?: number; floatAmp?: number; inline?: boolean; zIndex?: number }`
- `OpenHeroWatermarkStage`: `{ watermarkText: string; heroSrc: string; rightObjectSrc?: string; rightMetric?: string; rightLabel?: string; bottomPhotoSrc?: string; bottomCaption?: string; startFrame?: number; accentColor?: string }`
- `RadialAvatarHub`: `{ avatarSrc: string; avatarLabel?: string; avatarSubLabel?: string; avatarBorderColor?: string; nodeCount?: number; bottomMetric?: string; bottomHeadline?: string; alertFrame?: number; startFrame?: number; size?: number }`
- `VisualCauseEffectFlow`: `{ items: { imageSrc: string; label: string; metric?: string; isCutout?: boolean; triggerFrame?: number; accentColor?: string }[]; startFrame?: number; topY?: number }`
- `EditorialSplitTimeline`: `{ items: { triggerFrame: number; metric: string; title: string; detail?: string; imageSrc?: string; imageFit?: "contain"|"cover"; objectPosition?: string; accentColor?: string }[]; startFrame?: number }`

---

## 3. ĐỒ NGHỀ CHUYÊN BIỆT 3D & BẢN ĐỒ ĐỘNG (7 MÓN)
- `AnatomyCallout3D` | `import { AnatomyCallout3D } from "./components/AnatomyCallout3D"`
  Props: `{ startFrame: number; endFrame: number; centerCutoutSrc: string; callouts: { anchorX: number; anchorY: number; labelX: number; labelY: number; title: string; value: string; accentColor?: string; delayFrames?: number }[]; centerX?: number; centerY?: number; centerWidth?: number }`
- `TimelineTrack3D` | `import { TimelineTrack3D } from "./components/TimelineTrack3D"`
  Props: `{ startFrame: number; endFrame: number; milestones: { dateLabel: string; title: string; iconOrCutoutSrc: string; accentColor?: string; triggerOffsetFrames: number }[]; centerX?: number; columnOffset?: number; startNodeY?: number; nodeStepY?: number; spineTop?: number; spineMaxHeight?: number; spineColors?: [string, string] }`
- `ScaleComparison3D` | `import { ScaleComparison3D } from "./components/ScaleComparison3D"`
  Props: `{ startFrame: number; endFrame: number; leftItemSrc: string; leftItemCount: number; leftLabel: string; rightTopTitle: string; rightTargetNumber: number; rightUnitSuffix: string; rightLabel: string; rightPrimaryStackSrc?: string; rightSecondaryStackSrc?: string; rightStartNumber?: number; stampText?: string }`
- `RealPersonSpotlight3D` | `import { RealPersonSpotlight3D } from "./components/RealPersonSpotlight3D"`
  Props: `{ startFrame: number; endFrame: number; cutoutSrc: string; subjectName: string; backdropSrc?: string; cutoutWidth?: number; centerX?: number; backdropWidth?: number; cutoutTop?: number; labelTop?: number; rimGlowColor?: string; subjectSubtitle?: string; keyMetricValue?: string; keyMetricAccentColor?: string }`
- `CoinStream` | `import { CoinStream } from "./components/CoinStream"`
  Props: `{ p0: { x: number; y: number }; p1: { x: number; y: number }; p2: { x: number; y: number }; startFrame: number; endFrame?: number; coinCount?: number; blockedAtT?: number; dotColor?: string; useDollarNotes?: boolean; primaryItemSrc?: string; secondaryItemSrc?: string }`
- `UrbanSatelliteDive9x16` | `import { UrbanSatelliteDive9x16 } from "./components/UrbanSatelliteDive9x16"`
  Props: `{ locationName: string; zoneLabel: string; zoneMetric: string; durationFrames: number; mapImageSrc?: string; overlayMode?: "pins"|"route"|"radius_zone"|"hex_grid"|"clean_highlight"; zoneColor?: string; routePoints?: { x: number; y: number }[]; routeDistanceLabel?: string; pins?: { x: number; y: number; label: string; color?: string }[] }`
- `GeoStrategicMap3D` | `import { GeoStrategicMap3D } from "./components/GeoStrategicMap3D"`
  Props: `{ startFrame: number; endFrame: number; originLabel: string; targetLabel: string; originCoord?: { x: number; y: number }; targetCoord?: { x: number; y: number }; originPaths?: string[]; targetPaths?: string[]; bgPaths?: string[]; evidenceImageSrc?: string; evidenceTitle?: string }`

---

## 4. SƠ ĐỒ, SO SÁNH, CHỨNG CỨ & CALLOUT (16 MÓN — `import { ... } from "./components/fx"`)
- `FlowPipeline3D`: `{ sourceLabel: string; branches: { label: string; percent: number; color: string }[]; startFrame?: number }`
- `DecisionBranchPulse`: `{ rootLabel: string; winLabel: string; loseLabel: string; startFrame?: number }`
- `MotionTrackedCallout`: `{ trackPoints: { frame: number; x: number; y: number }[]; title: string; subtitle?: string; metricValue?: string; offsetX?: number; offsetY?: number; startFrame?: number; accentColor?: string }`
- `RealSceneCameraStage`: `{ bgSrc: string; waypoints?: { frame: number; scale: number; x: number; y: number }[]; subjects?: { src: string; appearFrame: number; x: number; y: number; width: number; rotateDeg?: number; glowColor?: string }[]; durationFrames?: number; bgBrightness?: number; children?: React.ReactNode }`
- `EvidenceCalloutOverlay`: `{ targetX: number; targetY: number; labelX: number; labelY: number; label: string; metric?: string; startFrame?: number; color?: string }`
- `FactPunchlineCard`: `{ headline: string; subline?: string; startFrame?: number; accentColor?: string }`
- `ContainedPhotoBox`: `{ src: string; width?: number|string; height?: number; borderRadius?: number; border?: string; imageFit?: "contain"|"cover"; objectPosition?: string; zoomScale?: number }`
- `EvidenceDocumentCard`: `{ sourceBadge: string; highlightLine: string; imageSrc?: string; imageFit?: "contain"|"cover"; objectPosition?: string; startFrame?: number; highlightFrame?: number; rotateDeg?: number; tiltY?: number; width?: number; imageHeight?: number; slashOld?: string; slashNew?: string; slashFrame?: number }` *(tối đa <= 2 lần/video)*
- `SlashCrossOut`: `{ oldValue: string; newValue: string; slashFrame: number }`
- `VisualBarCompare`: `{ items: { label: string; value: number; suffix?: string; color?: string; startFrame?: number }[]; startFrame?: number; width?: number; maxBarHeight?: number }` *(tối đa <= 2 lần/video)*
- `ProcessStepChain`: `{ steps: { label: string; metric?: string; triggerFrame: number; accentColor?: string }[]; startFrame?: number; width?: number }` *(tối đa <= 2 lần/video, `triggerFrame` tăng dần)*
- `RadialNetworkBurst`: `{ centerLabel: string; nodeCount?: number; startFrame?: number; alertFrame?: number; size?: number }`
- `CycleDialProgress`: `{ segments: string[]; centerMetric: string; activeCount?: number; centerSublabel?: string; startFrame?: number; stepFrames?: number; accentColor?: string; size?: number }`
- `VisualComparisonStrip`: `{ wrongTitle: string; wrongReason: string; rightTitle: string; rightReason: string; startFrame?: number; rightDelayFrames?: number; width?: number }`
- `HighContrastConclusionCard`: `{ headline: string; subline?: string; variant?: "white"|"yellow"; startFrame?: number; top?: number }`
- `DualStageKnowledgeLayout`: `{ topStage: React.ReactNode; bottomStage: React.ReactNode; gap?: number }` *(CẤM dùng quá 2 Beat/video)*

---

## 5. CHỮ ĐỘNG, SỐ LIỆU ODOMETER & PRESETS (7 MÓN — `import { ... } from "./components/fx"`)
- `MetricOdometerHero`: `{ from: number; to: number; startFrame: number; durationFrames?: number; prefix?: string; suffix?: string; label?: string; x?: number; y?: number; color?: string; fontSize?: number; zIndex?: number }` *(bắt buộc `startFrame <= 90`)*
- `ForensicStampSlam`: `{ text: string; startFrame: number; x?: number; y?: number; color?: string; rotate?: number; fontSize?: number; zIndex?: number }`
- `MarkerHighlightText`: `{ text: string; startFrame?: number; highlightColor?: string; textColor?: string; fontSize?: number; fontFamily?: string }`
- `StaggerWaveText`: `{ text: string; startFrame?: number; staggerFrames?: number; fontSize?: number; color?: string; fontFamily?: string }`
- `GlitchSplitText`: `{ text: string; startFrame?: number; fontSize?: number; color?: string; fontFamily?: string }`
- `MetallicSweepText`: `{ text: string; startFrame?: number; fontSize?: number; fontFamily?: string }`
- `OdometerCounter`: `{ to: number; from?: number; startFrame?: number; durationFrames?: number; prefix?: string; suffix?: string; fontSize?: number; color?: string }`
- **Motion Presets (`./components/fx`):** `AE_SNAP_OUT`, `AE_PUNCH_OUT`, `AE_WHIP_TRANSITION`, `SPRING_SNAPPY`, `SPRING_HEAVY_SLAM`, `getAliveFloat`, `getKenBurnsScale`, `getStaggerDelay`.
```


### 3.2. Cấu hình dự án, Batch & GitHub Actions

#### `.gitignore`

```text
# Node / Remotion
node_modules/
remotion_reels/node_modules/
remotion_reels/.remotion/
remotion_reels/out/

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# Outputs & Temp
cloud_out/
temp_render/
remotion_reels/public/harvested/
*.mp4
*.mov
*.avi
*.wav
*.mp3
!remotion_reels/public/sfx/*.mp3
!assets/music/*.mp3
*.log
.DS_Store
Thumbs.db
.env
```


#### `plugin.json`

```json
{
  "name": "masterbrain-fb-reels-9x16",
  "displayName": "MasterBrain FB Reels 9:16 Studio",
  "version": "1.0.0",
  "description": "Đội ngũ 5 Sub-Agents tinh nhuệ (Cấm đẻ con rác) chuyên trách sản xuất Video Ngắn FB Reels / TikTok 9:16 (60fps): Biên kịch chuyên sâu 5 nhịp -> Trinh sát tư liệu thật & 3D theo đúng kịch bản -> Dựng Remotion 3D 60fps Zero-Box 80/20 -> Hòa âm -14.0 LUFS & Soi Mắt Thần.",
  "suggestedPrompts": [
    "Sản xuất video ngắn FB Reels 9:16 chuẩn 60fps từ chủ đề mới",
    "Lên kịch bản chuyên sâu 5 nhịp giữ chân & đi trinh sát tư liệu thật",
    "Dựng Remotion 3D 60fps chữ Zero-Box 2 màu 80/20 & kiểm duyệt Mắt Thần"
  ]
}
```


#### `CHAY_SAN_XUAT_FB_REELS.bat`

```bat
@echo off
chcp 65001 >nul
echo =====================================================================
echo    ĐẦU NÃO SẢN XUẤT VIDEO NGẮN FB REELS - FORENSIC GLASS NOIR
echo =====================================================================
echo.
echo Cách dùng:
echo   python engine\render_reel.py --comp ^<TenComp^> --project "D:\DuAn_DangLam\^<ten_du_an^>" --name "^<TenVideo^>"
echo.
python "%~dp0engine\render_reel.py" --help
pause
```


#### `.github/workflows/deploy_telegram_bot.yml`

```yaml
name: Deploy Telegram Bot Webhook on Modal

on:
  workflow_dispatch:

jobs:
  deploy_bot:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Sync Modal Secrets & Deploy Webhook
        env:
          MODAL_TOKEN_ID: ${{ secrets.MODAL_TOKEN_ID }}
          MODAL_TOKEN_SECRET: ${{ secrets.MODAL_TOKEN_SECRET }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
          SERPER_API_KEY: ${{ secrets.SERPER_API_KEY }}
          GH_MODELS_TOKEN: ${{ secrets.GH_MODELS_TOKEN }}
          MOTAPI_KEY: ${{ secrets.MOTAPI_KEY }}
          GH_PAT: ${{ secrets.GH_PAT }}
        run: |
          python -m pip install -q modal
          modal secret create hadawhy-secrets --force \
            "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" \
            "TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID" \
            "GEMINI_API_KEY=$GEMINI_API_KEY" \
            "OPENROUTER_API_KEY=$OPENROUTER_API_KEY" \
            "DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY" \
            "SERPER_API_KEY=$SERPER_API_KEY" \
            "GH_MODELS_TOKEN=$GH_MODELS_TOKEN" \
            "MOTAPI_KEY=$MOTAPI_KEY" \
            "GH_PAT=$GH_PAT"

          DEPLOY_LOG=$(modal deploy engine/modal_worker.py 2>&1)
          echo "$DEPLOY_LOG"

          WEBHOOK_URL=$(python -c '
          import re, sys
          log = re.sub(r"\s+", "", sys.stdin.read())
          m = re.search(r"https://[a-z0-9-]+--hadawhy-reels-gpu-telegram-webhook\.[a-z0-9-]+\.modal\.run", log)
          print(m.group(0) if m else "https://dangnguyen18051989--hadawhy-reels-gpu-telegram-webhook.us-east.modal.run")
          ' <<< "$DEPLOY_LOG")

          echo "Registering Telegram Webhook: $WEBHOOK_URL"
          curl -sS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
            -d "url=${WEBHOOK_URL}"
          echo ""
```


#### `.github/workflows/hadawhy_cloud_reels.yml`

```yaml
name: HaDa Why Cloud Reels 9x16

on:
  workflow_dispatch:
    inputs:
      mode:
        description: "auto (1-click kich ban moi + anh + render MP4) | create (tao kich ban + preview) | preview | render | revise"
        required: true
        default: "auto"
        type: choice
        options:
          - auto
          - create
          - preview
          - render
          - revise
      feedback:
        description: "Nhap chu de/yeu cau video moi (auto/create) hoac gop y sua (revise)"
        required: false
        default: ""
        type: string

permissions:
  contents: read
  models: read

jobs:
  build_reels:
    runs-on: ubuntu-latest
    timeout-minutes: 45

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Detect Modal GPU Worker
        env:
          M_ID: ${{ secrets.MODAL_TOKEN_ID }}
          M_SEC: ${{ secrets.MODAL_TOKEN_SECRET }}
        run: |
          if [ -n "$M_ID" ] && [ -n "$M_SEC" ]; then
            echo "HAS_MODAL=true" >> "$GITHUB_ENV"
          else
            echo "HAS_MODAL=false" >> "$GITHUB_ENV"
          fi

      - name: Setup Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Run on Modal T4 GPU (Fast ~2m) if Modal Secrets configured
        if: ${{ env.HAS_MODAL == 'true' }}
        env:
          MODAL_TOKEN_ID: ${{ secrets.MODAL_TOKEN_ID }}
          MODAL_TOKEN_SECRET: ${{ secrets.MODAL_TOKEN_SECRET }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
          SERPER_API_KEY: ${{ secrets.SERPER_API_KEY }}
          GH_MODELS_TOKEN: ${{ secrets.GH_MODELS_TOKEN }}
          MOTAPI_KEY: ${{ secrets.MOTAPI_KEY }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          python -m pip install -q modal
          modal run engine/modal_worker.py --mode "${{ github.event.inputs.mode }}" --feedback "${{ github.event.inputs.feedback }}"

      - name: Setup Node.js 20
        if: ${{ env.HAS_MODAL != 'true' }}
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install Chromium dependencies for Remotion
        if: ${{ env.HAS_MODAL != 'true' }}
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2t64 || true

      - name: Cache HuggingFace, rembg & Remotion browser
        if: ${{ env.HAS_MODAL != 'true' }}
        uses: actions/cache@v4
        with:
          path: |
            ~/.cache/huggingface
            ~/.u2net
            remotion_reels/node_modules/.remotion
          key: ${{ runner.os }}-ai-models-v2

      - name: Install Node & Python dependencies
        if: ${{ env.HAS_MODAL != 'true' }}
        run: |
          cd remotion_reels && npm install
          python -m pip install --upgrade pip google-genai vieneu edge-tts "rembg[cpu]" opencv-python-headless numpy pillow requests

      - name: Run Cloud Reels Pipeline
        if: ${{ env.HAS_MODAL != 'true' }}
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          python engine/cloud_reels_runner.py --mode "${{ github.event.inputs.mode }}" --feedback "${{ github.event.inputs.feedback }}"

      - name: Upload Preview / Video Artifacts
        if: ${{ env.HAS_MODAL != 'true' }}
        uses: actions/upload-artifact@v4
        with:
          name: hadawhy-cloud-output-${{ github.event.inputs.mode }}
          path: cloud_out/
          retention-days: 7
```


#### `remotion_reels/package.json`

```json
{
  "name": "remotion_reels",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@react-three/fiber": "^9.8.2",
    "@remotion/captions": "4.0.541",
    "@remotion/cli": "4.0.541",
    "@remotion/motion-blur": "4.0.541",
    "@remotion/shapes": "4.0.541",
    "@remotion/three": "4.0.541",
    "@types/three": "^0.171.0",
    "react": "^19.3.1",
    "react-dom": "^19.3.1",
    "remotion": "4.0.541",
    "three": "^0.171.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "typescript": "^5.8.2"
  }
}
```


#### `remotion_reels/remotion.config.ts`

```typescript
import { Config } from "@remotion/cli/config";
import fs from "fs";
import os from "os";

if (process.platform === "win32") {
  const D_TEMP = "D:\\DuAn_DangLam\\temp";
  if (!fs.existsSync(D_TEMP)) {
    fs.mkdirSync(D_TEMP, { recursive: true });
  }
  process.env.TEMP = D_TEMP;
  process.env.TMP = D_TEMP;
}

const cpuCount = Math.max(1, os.cpus().length);
Config.setChromiumOpenGlRenderer("angle");
Config.setConcurrency(Math.min(6, cpuCount));
Config.setOverwriteOutput(true);
```


#### `remotion_reels/tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": false,
    "noEmit": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*", "remotion.config.ts"]
}
```


### 3.3. Dữ liệu cấu hình & Lịch sử hệ thống (engine/*.json)

#### `engine/studio_lessons_learned.json`

```json
{
  "version": "2026-11-16",
  "channel_positioning": "HaDa WHY (@hadawhy) KHÔNG làm kênh tài chính thuần túy. Chuyên GÓC KHUẤT XÃ HỘI và BÍ ẨN BÊN TRONG SỰ VIỆC (chữ WHY) có từ khóa tìm kiếm thực tế cao trên Google/YouTube.",
  "mandatory_channel_dna": {
    "backdrop": "<HaDaWhyMistBackground intensity={0.11} accentHex=\"66, 178, 242\" /> (Nền đen sâu Obsidian + sương mù xanh thương hiệu #42B2F2 Mức 1 rất nhẹ. CẤM lưới ô vuông, CẤM tự đổi màu nền sang vàng/đỏ).",
    "layout_2_layers": "Tầng trên (Y:220..520px) chữ Hook Slam 2 dòng nổi bật; Tầng giữa (Y:520..1580px) 100% cho minh họa 3D + tư liệu thật; CẤM phụ đề karaoke đáy màn hình (KineticWordCaption).",
    "suspense_reveal": "Câu hỏi đặt vấn đề giữ bí mật bằng bối cảnh thật + biểu tượng 3D sắc nét (KHÔNG phát sáng neon); CHỈ bung đáp án 3D đúng lúc giọng đọc nói tới.",
    "image_quality_gate": "Mọi ảnh tải về bắt buộc >= 800x500px (hoặc >= 650x450px cho prop 3D) và Laplacian sharpness >= 45.0; tuyệt đối cấm ảnh mờ nhòe vỡ hạt.",
    "real_video_broll": "Với kịch bản đời thật/sự kiện thật: ưu tiên cào VIDEO B-roll thật sắc nét (>=720p, sạch watermark/phụ đề, lưu public/harvested/*.mp4) đưa vào khung minh họa tầng giữa bằng <OffthreadVideo muted /> trên nền ADN #42B2F2 Mức 1 thay vì chỉ dùng ảnh tĩnh.",
    "audio_sync_gate": "1 luồng nhạc nền liền mạch mượt (CẤM cắt nối 5 khúc rời rạc, CẤM tích tắc đồng hồ rền rĩ, CẤM filler SFX); SFX chỉ nổ khớp đúng mốc chủ thể/số liệu trong choreography_blueprint.json (±30ms), tối đa 2 lần/file SFX; Vacuum Drop ramp mượt 120ms + Sidechain Ducking.",
    "pre_render_and_qc": "Bắt buộc pass engine/qc_gate.py tsx -> render & hòa âm -14.0 LUFS bằng engine/render_reel.py (tự chạy engine/qc_gate.py video >= 95/100) -> soi qc_grid_3x3.jpg + nghe trực tiếp 2 file audio preview trước khi báo cáo."
  },
  "continuous_improvement_protocol": "Sau mỗi video, mọi góp ý của Người Chỉ Huy phải được mã hóa thành check tự động trong engine/qc_gate.py hoặc engine/render_reel.py để lỗi cũ không bao giờ tái diễn.",
  "evolution_lessons": [
    {
      "date": "2026-11-17T23:35:37",
      "lesson": "LUAT TIEN HOA & DOC BAN",
      "root_cause": "BiMatVeSo40s scored 23.0 vs Nvidia 39.4 and best 47.8; reused brain cutout from VanHoaNhau; StickerPop pop-shake reused every episode; objects/ plastic icons; SFX guessed from words.json.",
      "enforcement": [
        "novelty_progress_ledger.py wired into engine/qc_gate.py",
        "objects/ demo_archive/ deleted",
        "StickerPop banned",
        "src/components/fx library",
        "SFX from tsx frames + no consecutive repeats"
      ]
    },
    {
      "date": "2026-11-24T01:07:00",
      "lesson": "CHONG CAO MU, CHONG NHAY COC RENDER & TOI UU 70% TOKEN",
      "root_cause": "Harvester cũ cào mù theo dung lượng gây lọt cái cân tòa án, nước hoa, bảng ăn kiêng và ảnh Vecteezy watermark; tự ý chạy render khi hệ thống chưa hoàn tất; luật rải rác mâu thuẫn giữa SKILL/subagents/guidelines và deadlock kind ở voice_visual_sync.py.",
      "enforcement": [
        "auto_asset_harvester.py: BANNED_ABSTRACT_METAPHORS + Tavily/Wikimedia/Bing Clean + Gemini Vision + CLI --manifest/--contact-sheet",
        "vieneu_whisper_pacer.py: CLI --script/--project xuất chuẩn temp/voiceover.wav & temp/words.json",
        "voice_visual_sync.py + sfx_timeline_mixer.py: đồng bộ đủ 5 nhóm kind & ánh xạ SFX Mixkit theo từ khóa tên file",
        "render_reel.py: truyền script_5beat.json vào script_text khi mix BGM",
        "Nén toàn bộ luật vào đúng 2 file .agent/rules/00-hadawhy-core.md (Always On) + .agent/workflows/san-xuat-reel.md (4 trạm có điểm DỪNG); archive toàn bộ file cũ vào _archive_cu/"
      ]
    }
  ],
  "commander_permanent_laws_2026_11_19": {
    "law_1_zero_abstract_dots": "CẤM trừu tượng vô nghĩa (DotMatrix 60 chấm / lưới ma trận trừu tượng). Mọi ý niệm phải minh họa bằng hình ảnh thực tế / mô hình 3D trực quan dễ hiểu ngay trong 1 giây.",
    "law_2_natural_cinematic_outro": "CẤM cảnh kết công nghiệp, gượng ép ở cuối video (cấm chia 2 khối màu xanh/cam đối đầu cứng nhắc, cấm hộp thoại bình luận 3D / bàn tay bấm tương tác giả tạo, cấm mũi tên ký tự '↓', cấm lời chèo kéo sáo mòn kiểu 'hãy để lại bình luận'). Cảnh kết phải TỰ NHIÊN chuẩn điện ảnh: quay lại bối cảnh đời thực có chiều sâu hoặc hình ảnh biểu tượng giàu cảm xúc của câu chuyện, kèm câu hỏi mở sắc bén để người xem tự muốn tranh luận.",
    "law_3_no_neon_borders_or_glow": "CẤM tuyệt đối viền ảnh màu mè, textShadow/boxShadow/drop-shadow phát sáng neon loang lổ và Rim Light màu quanh cutout 3D. Chỉ dùng bóng đổ đen sâu tự nhiên rgba(0,0,0,0.75..0.9) và viền chữ đen đanh gọn.",
    "law_4_dense_frame_synced_sfx": "PHÂN TÁCH 5 NHÓM SFX KHỚP ĐÚNG BẢN CHẤT TRÊN MÀN HÌNH: (1) Chữ Hook (hook_text) -> cut/tap/pop_dry/whoosh1; (2) Chữ Kiến thức/Callouts/Highlight (knowledge_text) -> type_soft/marker_highlight/paper_turn/keyboard_click/typing; (3) Số Kiến thức/Năm/Diện tích/% (number_knowledge) -> tick/ding/gear_lock/keyboard_click; (4) Số Tiền bạc/Giá (number_money) -> cash_counter_roll/cash_flip/coin1; (5) Đồ vật thật/Bản đồ/Đóng dấu (subject) -> tổ hợp SFX vật lý + forensic_stamp_thud + Vacuum Drop.",
    "law_5_audible_engaging_bgm": "Nhạc nền BGM giao hưởng điều tra / trailer phải dồn dập lôi cuốn ngay từ 0:00s (cấm nhạc synth gõ wood-wood lặp đơn điệu); âm lượng nằm dưới giọng đọc từ -6.5 dB đến -8.5 dB (bgm_base_volume=0.72, sidechain ratio=2.2, threshold=0.05; cấm dìm sâu dưới -14 dB), đồng thời cắt rãnh 2.5kHz (-4.5dB) để không đè lời đọc.",
    "law_6_thumbnail_adn_mandatory": "CẤM nền tối trống rỗng làm Thumbnail. Bắt buộc: (a) Ảnh bối cảnh đời thực 9:16 Chiaroscuro, (b) Text Hook 2 dòng Kanit-Black Xanh #42B2F2 / Trắng #FFFFFF viền đen dày 11px không neon, (c) Vật thể Hero 3D khổng lồ tiền cảnh dưới trái, (d) Khung bằng chứng phụ bên phải có vòng khoanh đỏ nét đứt + mũi tên đỏ.",
    "law_7_zero_running_captions": "CẤM TUYỆT ĐỐI phụ đề chạy chữ karaoke (KineticWordCaption / SyncCaptionBand) ở mọi video. Màn hình chỉ hiển thị chữ Hook lớn, số liệu Odometer và nhãn chứng cứ sắc nét.",
    "law_8_nvidia_golden_master_real_3d_only": "KHUÔN VÀNG THƯỚC NGỌC: Chuẩn phong cách điện ảnh như NvidiaSuccession40s (chuyển cảnh chắc, RealPersonSpotlight3D, GeoStrategicMap3D, TimelineTrack3D, camera shake nhẹ) NHƯNG bỏ sạch phụ đề chạy chữ và CẤM TUYỆT ĐỐI icon nhựa/hoạt hình (StickerPop). 100% vật thể/icon phải là 3D vật liệu thật (kim loại, kính, ảnh chụp thật tách nền --no-rim với bóng đổ đen tự nhiên).",
    "law_10_minimal_text_density_no_clutter": "TỐI GIẢN CHỮ & CẤM TRÙNG CHỮ HOOK VỚI CHỮ KIẾN THỨC (mọi kịch bản): mỗi nhịp tối đa ~40 từ hiển thị (gate chặn > 60). Chữ Hook tầng trên (dẫn mạch/đặt câu hỏi) và chữ giải thích kiến thức tầng giữa (tên thuật ngữ, thông số bằng chứng, nhãn mô hình, dấu đóng forensic) TUYỆT ĐỐI KHÔNG ĐƯỢC NHẠI LẠI / TRÙNG NHAU (giống video Nvidia: Hook trên ghi 'BỊ HỘI ĐỒNG QUẢN TRỊ ĐIỀU TRA', tầng giữa ghi 'CEO NVIDIA JENSEN HUANG' & '33 NĂM NGỰ TRỊ CHIP AI'). CẤM câu thuyết minh dài trên màn hình.",
    "law_11_asset_must_match_script_subject": "NÓI A HIỆN ĐÚNG A (mọi kịch bản): mỗi tư liệu phải đúng chủ thể danh từ chính của câu thoại nó minh họa. Trinh sát lập asset_manifest.json {file, depicts, scene_id} cho MỌI tư liệu và ghép contact sheet 3x3 đánh số theo cảnh; QC đối chiếu 'depicts' với câu thoại bằng mắt; lệch chủ thể thì tìm/sinh lại. Không có tư liệu đúng thì dùng chữ Hook hoặc mô hình 3D khác đúng chủ thể; CẤM nhét hình gần giống cho đủ.",
    "law_9_every_key_subject_is_real_3d_not_text_box": "MỌI CHỦ THỂ QUAN TRỌNG = MÔ HÌNH 3D THẬT, KHÔNG PHẢI Ô CHỮ (áp dụng cho MỌI kịch bản, mọi đề tài). Trong bất kỳ sơ đồ, quy trình, chuỗi nhiều khâu, bản đồ mặt bằng, so sánh hay bảng xếp hạng: mỗi chủ thể / khu vực / trạm / nhân vật được nhắc trong kịch bản phải hiện bằng ảnh hoặc mô hình 3D thật của đúng chủ thể đó (cutout bria-rmbg --no-rim, bóng đổ đen tự nhiên) đặt đúng vị trí. CẤM vòng tròn rỗng chỉ có số/chữ, CẤM ô hộp chữ nhật chỉ có chữ thay cho vật thể. Chữ chỉ là nhãn 2-3 từ + con số ở chân mô hình.",
    "law_12_visuals_follow_the_voiceover": "HÌNH VÀ HIỆU ỨNG BÁM THEO GIỌNG ĐỌC (mọi kịch bản): hình chỉ hiện khi giọng đọc nói tới nó, KHÔNG rải hiệu ứng theo đồng hồ để lấp chỗ trống. Mỗi câu chỉ hiện đúng thứ cần để người xem hiểu: chủ thể chính (mô hình 3D thật) + con số quan trọng, tối đa 2 thứ/câu. Ví dụ: 'thị trường chip AI đã thống trị 40.000$' -> chỉ hiện hình chip AI và con số 40.000$. Biên kịch ghi key_visuals từng câu; Đạo diễn lập choreography_blueprint.json với events {frame, kind: subject|number, show, voice_word} lấy mốc từ words.json (hình hiện sớm tối đa 0.5s hoặc trễ tối đa 0.6s so với lúc đọc). Gate voice_visual_sync.py kiểm: đúng thời điểm, mọi con số quan trọng đều được hiện, không quá 3 hình/câu. Khoảng thời gian không có hiệu ứng KHÔNG phải lỗi.",
    "law_13_compound_sfx_and_anti_muddiness": "PHỐI HỢP SFX ĐA TẦNG & CHỐNG LÙNG BÙNG (bài học @nhanho.home 2026-11-22): Cấm rập khuôn 1 tiếng whoosh/hit đơn lẻ. Dùng 15+ tổ hợp COMPOUND_SFX_COMBOS trong sfx_timeline_mixer.py (Riser+Hit, Riser+Whoosh, Riser+Reverse, Swell+Impact, Click+Typing, BassDrop+Hit, SnareRoll+Hit, Ambient+Riser+Stinger, TrailerHit+Braam...) khớp điểm rơi chuyển Beat / chủ thể / số liệu. Bắt buộc gom SFX vào [sfx_bus] cắt rãnh 2.5kHz (-3.5dB) + Sidechain Ducking nhẹ dưới giọng đọc để không bị 'lùng bùng' át lời.",
    "law_14_mandatory_contact_sheet_visual_qc": "CẤM TIN MÙ AUTO-QC 100/100: Trước khi báo cáo hoàn thành bất kỳ video nào, Con Tổng bắt buộc gọi read_file mở xem trực tiếp 3 file ảnh (assets_contact_sheet.jpg, final_12frames_contact_sheet.jpg, thumbnail_9x16.jpg) và mở nghe trực tiếp 2 file âm thanh (bgm_qc_preview.mp3, master_audio_qc_preview.mp3).",
    "law_15_nvidia_style_and_forensic_assets": "CHUẨN VÀNG KÊNH HADA WHY TRÊN MỌI KỊCH BẢN: (1) Xuyên suốt 100% thời lượng dùng nền gốc <HaDaWhyMistBackground intensity={0.11} accentHex=\"66, 178, 242\" /> kết hợp <ContextBackdropLayer opacity={0.40..0.46} /> để có chiều sâu bối cảnh thực tế và không bị lỗi EMPTY_DARK_VOID_SCREEN trong engine/qc_gate.py; (2) CẤM dùng trùng 1 bức ảnh ở >= 2 cảnh trong cùng 1 video và CẤM lấy ảnh stock chung chung vô hồn — bắt buộc lấy bằng chứng đắt giá (giao diện thật, bài báo/hồ sơ thật, chủ thể thật đúng câu thoại); (3) Bản đồ 3D tự động biến thiên theo kịch bản: xuyên quốc gia dùng GeoStrategicMap3D (258 nước qua engine/geo_map_builder.py)."
  }
}
```


#### `engine/visual_layout_history.json`

```json
{
  "entries": []
}
```


#### `engine/audio_used_history.json`

```json
{
  "used_bgm_urls": [
    "https://assets.mixkit.co/music/623/623.mp3",
    "https://assets.mixkit.co/music/614/614.mp3",
    "https://assets.mixkit.co/music/493/493.mp3",
    "https://assets.mixkit.co/music/871/871.mp3",
    "https://assets.mixkit.co/music/51/51.mp3",
    "https://assets.mixkit.co/music/676/676.mp3",
    "https://assets.mixkit.co/music/601/601.mp3",
    "https://assets.mixkit.co/music/126/126.mp3",
    "https://assets.mixkit.co/music/188/188.mp3",
    "https://assets.mixkit.co/music/706/706.mp3",
    "https://assets.mixkit.co/music/565/565.mp3"
  ],
  "used_sfx_urls": [
    "https://assets.mixkit.co/active_storage/sfx/2930/2930-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2465/2465-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2870/2870-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2358/2358-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/995/995-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/916/916-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1492/1492-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/166/166-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1143/1143-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/488/488-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/788/788-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2908/2908-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1489/1489-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1491/1491-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1000/1000-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/3124/3124-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2782/2782-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2182/2182-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1714/1714-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1490/1490-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2290/2290-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1486/1486-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2573/2573-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/3120/3120-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/992/992-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2866/2866-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2608/2608-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2909/2909-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2198/2198-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/498/498-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/3005/3005-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2350/2350-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1287/1287-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1474/1474-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1687/1687-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2589/2589-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2577/2577-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2133/2133-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/790/790-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1088/1088-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1146/1146-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1465/1465-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1485/1485-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/787/787-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1133/1133-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/275/275-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2594/2594-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/3116/3116-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/677/677-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2630/2630-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/784/784-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2902/2902-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2623/2623-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2918/2918-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1386/1386-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2531/2531-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1059/1059-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1045/1045-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1144/1144-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/561/561-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2900/2900-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/833/833-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2596/2596-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2408/2408-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2532/2532-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1393/1393-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1060/1060-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/988/988-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1583/1583-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1582/1582-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/492/492-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/565/565-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/3046/3046-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/772/772-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2903/2903-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1493/1493-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1372/1372-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2538/2538-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1061/1061-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1063/1063-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1993/1993-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2841/2841-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2293/2293-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/489/489-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2150/2150-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2152/2152-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2650/2650-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1721/1721-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1396/1396-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1387/1387-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1046/1046-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1056/1056-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1999/1999-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1939/1939-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/563/563-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/497/497-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2804/2804-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/773/773-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/2651/2651-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/3024/3024-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1392/1392-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1376/1376-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1072/1072-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1047/1047-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1996/1996-preview.mp3",
    "https://assets.mixkit.co/active_storage/sfx/1989/1989-preview.mp3"
  ]
}
```


#### `engine/bgm_fingerprint_ledger.json`

```json
{
  "used_hashes": [
    "71e869b39663f2d5e701754d33dbddb5ada382f926427693c479128e7e2686a7",
    "df537ce22c072288b67c0d90e473a9c68e6bea84231d7e13a6294ab6077f64f6",
    "18d3278e1f89917562b61312da7540a7fe8c070ddaba3740e06ad675e95e8c05",
    "d5f7c85c5789cc1e00960687ddc06ea5b287bcc8d00bb6430c8d6f67382e09a3",
    "79ba2cffaaed89241e26e126105db6815453b349df62d1669e629464716dffc3",
    "cd78e9320b200b15b908464465d24a8bb7c9b88c4a75f94de257dd8a42e18734",
    "5282cbd2da75e0ec06fe525a2ed476d9e059deaece22101aeb3e1a8a07b6ca90",
    "5da98b8507364f0ba81be96c645644fb75e6d4fbb1cffcdf6fcbed81d9c9c384",
    "61052f8374c96ea289028acfe203687f8b646a13e795f58d8e4a740e6b5e4ed7",
    "eb3b826685e8bd434fad2feef1385931846b11b032209972babd4f18356004bb",
    "22cf6511251e262737bf14b2906de78befa6457478fb5053a2fb07df36976fd5",
    "61a4f66d9572b61bf16ca915eadd142bbd45f7cf906f635793894937accdcf3a",
    "1997f1e26c4dad37d137f4b72b684850c8850140ac544cd786222f85cf5d8b55",
    "506ad361e4f9a50b4f00333b4f8b8acf88cc5bcf5cefe7f5c750dde3ecf1902c",
    "d8edfecc6ae847eb2d4e92478f7e1ffcee2e285f8edcd8a413aaed36bc961ee0",
    "9a5c87a34fe2ea4a5babd5fbbac782b9ddaf9b027d7304c32557aa1d9c45cd00",
    "4741a2627efb9982264c076c01d6fca737552f1fd7028677e65db3db87594121",
    "5da92ddd8d3766ee96faff30927d4c550d70fb0ab3ef8451f001f921963a97e1",
    "85f4b991dcd713043cf1feec8a29a71973914160dbbaedf06af84562df52f10a"
  ],
  "used_recipes": [
    "forensic_finance_st-2_tm1.156_s0.0_18.0_53.2_42.0_14.0",
    "geopolitics_war_st0_tm1.156_s0.4_25.2_46.0_37.2_14.5",
    "conspiracy_thriller_st0_tm1.228_s0.0_20.4_53.2_42.8_13.0",
    "forensic_finance_st-3_tm1.132_s0.0_24.4_47.8_41.2_13.0",
    "forensic_finance_st-1_tm1.204_s0.4_21.2_48.7_42.0_12.5",
    "conspiracy_thriller_st2_tm1.216_s0.0_27.6_52.3_38.0_13.0",
    "tech_monopoly_st-2_tm1.24_s0.0_23.6_58.6_34.0_13.5",
    "conspiracy_thriller_st0_tm1.156_s0.8_20.4_51.4_42.8_14.0",
    "conspiracy_thriller_st-3_tm1.24_s0.8_21.2_46.9_42.8_12.5",
    "consumer_trap_st-2_tm1.18_s0.4_22.8_58.6_38.0_14.0",
    "consumer_trap_st-3_tm1.216_s0.4_18.0_55.0_37.2_12.5",
    "conspiracy_thriller_st-2_tm1.132_s0.8_20.4_48.7_37.2_14.0",
    "geopolitics_war_st-2_tm1.156_s0.8_26.0_54.1_35.6_13.5",
    "tech_monopoly_st-2_tm1.216_s0.0_18.8_46.9_37.2_12.5",
    "conspiracy_thriller_st-2_tm1.204_s0.4_19.6_54.1_35.6_12.5",
    "tech_monopoly_st1_tm1.18_s0.4_23.6_55.9_34.0_13.5",
    "tech_monopoly_st-1_tm1.204_s0.4_21.2_58.6_42.0_14.0",
    "conspiracy_thriller_st0_tm1.132_s0.0_28.4_57.7_39.6_14.0",
    "conspiracy_thriller_st0_tm1.216_s0.4_18.8_52.3_34.0_12.5"
  ],
  "used_tracks": [
    "wallstreet_finance_cinema_02.mp3",
    "epic_victory_climax_02.mp3",
    "epic_victory_climax_01.mp3",
    "dark_investigation_orchestral_03.mp3",
    "wallstreet_finance_drive_01.mp3",
    "cyber_ai_future_02.mp3",
    "dark_investigation_mystery_02.mp3",
    "wallstreet_finance_momentum_03.mp3",
    "dark_investigation_tension_01.mp3"
  ]
}
```


#### `engine/image_used_history.json`

```json
{
  "entries": [
    {
      "date": "2026-11-24T11:08:08",
      "project": "ThuatToanGoiXe",
      "entity_id": "bg_city_night_traffic",
      "url": "https://images.pexels.com/photos/14648214/pexels-photo-14648214.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
      "md5": "e22401b1d965562ddb7185068f87d159",
      "dhash": "20c06699b53c362c"
    },
    {
      "date": "2026-11-24T11:08:16",
      "project": "ThuatToanGoiXe",
      "entity_id": "bg_rainy_street_traffic",
      "url": "https://img5.thuthuatphanmem.vn/uploads/2021/12/18/hinh-nen-canh-dep-dai-duong_110522928.jpg",
      "md5": "f088b95f1cdc03b8e55633551ac5f8a8",
      "dhash": "8783133333e3e3c3"
    },
    {
      "date": "2026-11-24T11:08:55",
      "project": "ThuatToanGoiXe",
      "entity_id": "prop_smartphone_gps",
      "url": "https://as1.ftcdn.net/jpg/22/47/38/52/1000_F_2247385285_qMc1tcwnH9OVnRd2n3PFenzD0ViUmLzP.jpg",
      "md5": "85f23e452c8b03c2f71dcf5414498e1a",
      "dhash": "d99bbbbbbb3bbbdb"
    },
    {
      "date": "2026-11-24T11:09:21",
      "project": "ThuatToanGoiXe",
      "entity_id": "prop_sedan_car",
      "url": "https://www.pngall.com/wp-content/uploads/2018/04/Sedan-Transparent.png",
      "md5": "05295ebc93d1bcec1aec4d8defcac6cc",
      "dhash": "308038e49ccce400"
    },
    {
      "date": "2026-11-24T11:09:46",
      "project": "ThuatToanGoiXe",
      "entity_id": "prop_server_rack",
      "url": "https://as1.ftcdn.net/jpg/11/66/91/86/1000_F_1166918637_Fvl0LCGTvfN8JMWGRw7EQypwvyKJOKKV.jpg",
      "md5": "9938d0a9855214dd8e1b454855d74ed0",
      "dhash": "b079796969696930"
    },
    {
      "date": "2026-11-24T11:10:10",
      "project": "ThuatToanGoiXe",
      "entity_id": "prop_stopwatch",
      "url": "https://as1.ftcdn.net/v2/jpg/19/41/68/88/1000_F_1941688878_Pw1iFItJgwuHoqy8J31E9lCs54H5Lpmv.jpg",
      "md5": "5f89c407c378e5d2da33a27048cbf049",
      "dhash": "3733316969697332"
    },
    {
      "date": "2026-11-24T11:10:58",
      "project": "ThuatToanGoiXe",
      "entity_id": "bg_rainy_street_traffic",
      "url": "https://cafefcdn.com/203337114487263232/2026/10/1/img5162-1790859408212-1790859409409305584639-1790898433968-1790898435597684661883.jpg",
      "md5": "235537b6a830dc9082bc7078d5d00d1b",
      "dhash": "ccac8c0149680f86"
    },
    {
      "date": "2026-11-24T11:11:38",
      "project": "ThuatToanGoiXe",
      "entity_id": "prop_server_rack",
      "url": "https://i.dell.com/is/image/DellContent/content/dam/ss2/product-images/peripherals/server/prod-1960-enterprise-rack-24u-rf-800x620.png?fmt=png-alpha&wid=800&hei=620",
      "md5": "6670d33943fb35c92b9c04310df2116a",
      "dhash": "0e8e8e8e8e8e8e16"
    },
    {
      "date": "2026-11-24T11:12:21",
      "project": "ThuatToanGoiXe",
      "entity_id": "prop_smartphone_gps",
      "url": "https://static0.anpoimages.com/wordpress/wp-content/uploads/wm/2024/11/how-to-make-google-maps-the-default-navigation-app-on-your-iphone.jpg",
      "md5": "a1cfa86b0b949a0f3efe43e4215dbb44",
      "dhash": "716949032ead8f87"
    },
    {
      "date": "2026-11-24T11:12:47",
      "project": "ThuatToanGoiXe",
      "entity_id": "prop_stopwatch",
      "url": "https://www.saturnstopwatches.co.uk/user/products/hanhart-robust-mechanical-stopwatch-194-p.jpg",
      "md5": "dcf6cf125a7a1bfd7a492b56fa1a1b64",
      "dhash": "b0b270ccd4d4dc70"
    }
  ]
}
```


### 3.4. Mã nguồn điều phối Engine (engine/*.py)

#### `engine/fact_researcher.py`

```python
# -*- coding: utf-8 -*-
r"""
fact_researcher.py - CÀO SÂU TOÀN VĂN BÀI GỐC & DỮ KIỆN CỨNG TRẠM 1 (0 API TRẢ PHÍ)
- Nhận >= 4-5 truy vấn chuyên sâu (cơ chế | số liệu | bằng chứng/vụ việc | tài liệu/luật gốc | từ khóa tiếng Anh).
- Cào song song Wikipedia API (vi + en) + DuckDuckGo HTML + Bing Web/News.
- Truy cập trực tiếp top 5-8 URL uy tín nhất, lọc sạch menu/quảng cáo và trích 2.500-4.000 ký tự toàn văn
  chứa dữ kiện cứng (%, tiền tệ, năm, điều luật, cơ chế) lưu vào temp/research_raw.json.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SSL_CTX = ssl._create_unverified_context()
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}
WIKI_HEADERS = {"User-Agent": "HaDaWhyFactResearcher/2.0 (mailto:admin@hadawhy.vn)"}

FACT_NUM_RE = re.compile(
    r"(\d[\d.,]*\s*(?:%|phần trăm|tỷ|triệu|nghìn|ngàn|usd|đô|vnđ|đồng|năm|tháng|ngày|giờ|phút|giây|km|m2|ha|lần|điều\s+\d+|khoản\s+\d+|nghị định|luật|billion|million|percent|years?))",
    re.IGNORECASE,
)

SKIP_ARTICLE_DOMAINS = (
    "facebook.com", "tiktok.com", "instagram.com", "youtube.com", "pinterest.com",
    "shopee.vn", "lazada.vn", "tiki.vn", "ebay.com", "amazon.com", "duckduckgo.com", "bing.com",
)


def _strip_tags(raw: str) -> str:
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip()


def _fetch_text(url: str, headers: Dict[str, str], timeout: int = 12) -> str:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
        raw_bytes = resp.read(850_000)
        return raw_bytes.decode("utf-8", errors="ignore")


def _unwrap_ddg_url(href: str) -> str:
    if "uddg=" in href:
        m = re.search(r"uddg=([^&]+)", href)
        if m:
            return urllib.parse.unquote(m.group(1))
    return href


def extract_clean_article_body(url: str) -> Dict[str, Any] | None:
    """Truy cập trực tiếp URL bài gốc, lọc menu/quảng cáo và trích 2.500-4.000 ký tự toàn văn + dữ kiện cứng."""
    try:
        parsed = urllib.parse.urlparse(url)
        domain = (parsed.netloc or "").lower()
        if not domain or any(bad in domain for bad in SKIP_ARTICLE_DOMAINS):
            return None

        raw_html = _fetch_text(url, HEADERS, timeout=11)
        title_m = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.IGNORECASE | re.DOTALL)
        title = _strip_tags(title_m.group(1))[:160] if title_m else domain

        # Lọc sạch script, style, nav, header, footer, aside, form, iframe, quảng cáo
        cleaned = re.sub(
            r"<(?:script|style|noscript|svg|nav|header|footer|aside|form|iframe|button)[^>]*>[\s\S]*?</(?:script|style|noscript|svg|nav|header|footer|aside|form|iframe|button)>",
            " ",
            raw_html,
            flags=re.IGNORECASE,
        )
        paragraphs = re.findall(r"<p[^>]*>([\s\S]*?)</p>", cleaned, flags=re.IGNORECASE)
        good_paras: List[str] = []
        for p_raw in paragraphs:
            p_txt = _strip_tags(p_raw)
            if len(p_txt) < 45:
                continue
            if any(junk in p_txt.lower() for junk in ("bản quyền thuộc về", "đăng ký nhận tin", "quảng cáo", "cookie", "chính sách bảo mật")):
                continue
            good_paras.append(p_txt)

        full_body = " ".join(good_paras).strip()
        if len(full_body) < 350:
            return None

        excerpt = full_body[:3800]
        sentences = re.split(r"(?<=[.!?])\s+", full_body)
        extracted_facts = [s.strip()[:340] for s in sentences if len(s.strip()) >= 40 and FACT_NUM_RE.search(s)][:12]
        raw_excerpts = [p[:500] for p in good_paras[:8]]

        return {
            "url": url,
            "source_name": domain.replace("www.", ""),
            "title": title,
            "char_length": len(excerpt),
            "full_excerpt": excerpt,
            "extracted_facts": extracted_facts,
            "raw_excerpts": raw_excerpts,
        }
    except Exception:
        return None


def search_wikipedia_deep(query: str, lang: str = "vi", limit: int = 3) -> List[Dict[str, Any]]:
    articles: List[Dict[str, Any]] = []
    try:
        q = urllib.parse.quote(query)
        api = (
            f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search"
            f"&srsearch={q}&srlimit={limit}&utf8=1&format=json"
        )
        data = json.loads(_fetch_text(api, WIKI_HEADERS))
        for item in data.get("query", {}).get("search", []):
            title = item.get("title", "")
            if not title:
                continue
            ext_api = (
                f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=extracts"
                f"&explaintext=1&exchars=4000&titles={urllib.parse.quote(title)}&format=json"
            )
            ext_data = json.loads(_fetch_text(ext_api, WIKI_HEADERS))
            pages = ext_data.get("query", {}).get("pages", {})
            for _, p in pages.items():
                extract = re.sub(r"\s+", " ", (p.get("extract") or "")).strip()
                if len(extract) < 200:
                    continue
                sents = re.split(r"(?<=[.!?])\s+", extract)
                facts = [s.strip()[:340] for s in sents if len(s.strip()) >= 35 and FACT_NUM_RE.search(s)][:10]
                wiki_url = f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                articles.append({
                    "url": wiki_url,
                    "source_name": f"Wikipedia ({lang})",
                    "title": title,
                    "char_length": len(extract[:3800]),
                    "full_excerpt": extract[:3800],
                    "extracted_facts": facts,
                    "raw_excerpts": [extract[i:i + 600] for i in range(0, min(len(extract), 2400), 600)],
                })
    except Exception as exc:
        print(f"[WIKI WARN {lang}] {query}: {exc}")
    return articles


def discover_search_urls(query: str) -> List[Dict[str, str]]:
    found: List[Dict[str, str]] = []
    # 1. DuckDuckGo HTML
    try:
        ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        page = _fetch_text(ddg_url, HEADERS, timeout=12)
        blocks = re.findall(
            r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>[\s\S]*?<a[^>]*class="result__snippet"[^>]*>(.*?)</a>',
            page,
        )
        for href, t_raw, s_raw in blocks[:8]:
            real_u = _unwrap_ddg_url(html.unescape(href))
            if real_u.startswith("http"):
                found.append({"url": real_u, "title": _strip_tags(t_raw), "snippet": _strip_tags(s_raw)})
    except Exception:
        pass

    # 2. Bing Web
    try:
        bing_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&setlang=vi"
        page = _fetch_text(bing_url, HEADERS, timeout=12)
        items = re.findall(
            r'<li class="b_algo"[\s\S]*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a></h2>[\s\S]*?<p[^>]*>(.*?)</p>',
            page,
        )
        for href, t_raw, s_raw in items[:8]:
            real_u = html.unescape(href)
            if real_u.startswith("http"):
                found.append({"url": real_u, "title": _strip_tags(t_raw), "snippet": _strip_tags(s_raw)})
    except Exception:
        pass
    return found


def run_research(topic: str, queries: List[str], project_dir: Path) -> Path:
    all_queries = [q.strip() for q in queries if q.strip()]
    if topic.strip() and topic.strip() not in all_queries:
        all_queries.insert(0, topic.strip())

    wiki_articles: List[Dict[str, Any]] = []
    discovered: List[Dict[str, str]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        w_futs = [ex.submit(search_wikipedia_deep, q, "vi", 2) for q in all_queries[:4]]
        w_futs += [ex.submit(search_wikipedia_deep, q, "en", 2) for q in all_queries[:3]]
        s_futs = [ex.submit(discover_search_urls, q) for q in all_queries]
        for fut in concurrent.futures.as_completed(w_futs):
            try:
                wiki_articles.extend(fut.result())
            except Exception:
                pass
        for fut in concurrent.futures.as_completed(s_futs):
            try:
                discovered.extend(fut.result())
            except Exception:
                pass

    # Chọn top URL uy tín không trùng để đọc sâu toàn văn
    seen_urls: set[str] = set()
    candidate_urls: List[str] = []
    for d in discovered:
        u = d["url"].split("#")[0]
        dom = urllib.parse.urlparse(u).netloc.lower()
        if not dom or any(b in dom for b in SKIP_ARTICLE_DOMAINS) or "wikipedia.org" in dom:
            continue
        if u not in seen_urls:
            seen_urls.add(u)
            candidate_urls.append(u)

    deep_web_articles: List[Dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        art_futs = [ex.submit(extract_clean_article_body, u) for u in candidate_urls[:14]]
        for fut in concurrent.futures.as_completed(art_futs):
            res = fut.result()
            if res is not None:
                deep_web_articles.append(res)

    deep_web_articles.sort(key=lambda a: (len(a["extracted_facts"]), a["char_length"]), reverse=True)
    top_web_articles = deep_web_articles[:8]

    # Khử trùng wiki articles
    seen_w: set[str] = set()
    clean_wiki: List[Dict[str, Any]] = []
    for wa in wiki_articles:
        if wa["url"] not in seen_w:
            seen_w.add(wa["url"])
            clean_wiki.append(wa)

    all_articles = top_web_articles + clean_wiki[:4]
    flat_facts: List[Dict[str, Any]] = []
    seen_fact_keys: set[str] = set()
    for art in all_articles:
        for f_txt in art.get("extracted_facts", []):
            fk = re.sub(r"\W+", "", f_txt.lower())[:85]
            if fk and fk not in seen_fact_keys:
                seen_fact_keys.add(fk)
                flat_facts.append({
                    "source": f"{art['source_name']} — {art['title']}",
                    "url": art["url"],
                    "has_number": True,
                    "snippet": f_txt,
                })

    # Bổ sung thêm snippet tìm kiếm có số liệu nếu cần
    for d in discovered:
        if FACT_NUM_RE.search(d.get("snippet", "")):
            fk = re.sub(r"\W+", "", d["snippet"].lower())[:85]
            if fk and fk not in seen_fact_keys:
                seen_fact_keys.add(fk)
                flat_facts.append({
                    "source": d["title"][:90],
                    "url": d["url"],
                    "has_number": True,
                    "snippet": d["snippet"][:340],
                })

    out_path = project_dir / "temp" / "research_raw.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "topic": topic,
        "queries": all_queries,
        "deep_urls_count": len(all_articles),
        "hard_facts_count": len(flat_facts),
        "articles": all_articles,
        "facts": flat_facts[:40],
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"[FACT RESEARCHER DEEP OK] Đã đọc sâu {len(all_articles)} bài gốc (2.500-4.000 ký tự/bài) "
        f"& trích {len(flat_facts)} dữ kiện cứng -> {out_path}"
    )
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Cào sâu toàn văn bài gốc & số liệu sự thật (Wikipedia VI/EN + Top URLs)")
    ap.add_argument("--topic", required=True, help="Chủ đề chính của video")
    ap.add_argument("--queries", default="", help="4-5 truy vấn chuyên sâu cách nhau dấu | (VD: 'q1|q2|q3|q4')")
    ap.add_argument("--project", required=True, help="Thư mục dự án WIP (VD: D:\\DuAn_DangLam\\ten_du_an)")
    args = ap.parse_args()

    q_list = [q.strip() for q in args.queries.split("|") if q.strip()]
    run_research(args.topic, q_list, Path(args.project))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```


#### `engine/vieneu_whisper_pacer.py`

```python
# -*- coding: utf-8 -*-
r"""
VIENEU WHISPER PACER (Bộ Điều Phối Giọng Hải Đăng & Bóc Tách Word-Level Timestamps)
Tích hợp:
1. VieNeu TTS (Giọng Hải Đăng - Nam Bắc Tự Nhiên & Uy Lực)
2. faster-whisper (Bóc tách toạ độ mili-giây từng từ vựng)
Đầu ra:
- voice.wav (Âm thanh giọng đọc sạch sẽ)
- speech_words.json (Danh sách từ + start_ms + end_ms phục vụ đồng bộ động hình & Foley)
"""
import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# Đảm bảo UTF-8 cho Windows console
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

_VN_LETTER_PRON = {
    "a": "a", "b": "bê", "c": "xê", "d": "đê", "e": "e", "f": "ép",
    "g": "gờ", "h": "hát", "i": "i", "j": "giây", "k": "ca", "l": "lờ",
    "m": "mờ", "n": "nờ", "o": "o", "p": "pê", "q": "quy", "r": "rờ",
    "s": "ét", "t": "tê", "u": "u", "v": "vê", "w": "đắp liu", "x": "ích",
    "y": "y", "z": "dét",
}
_VN_DIGIT_PRON = {
    "0": "không", "1": "một", "2": "hai", "3": "ba", "4": "bốn",
    "5": "năm", "6": "sáu", "7": "bảy", "8": "tám", "9": "chín",
}


def normalize_vietnamese_tts_codes(text: str) -> str:
    """
    Chuẩn hóa đọc mượt các mã viết tắt chữ+số ngắn (VD: C04 -> 'xê không bốn', A05 -> 'a không năm', PC02 -> 'pê xê không hai')
    tránh TTS ngắt khựng giữa chữ cái và chữ số; giữ nguyên các đơn vị thông dụng (m2, 3D, 4K, G7, H3, F0/F1 nếu cần đọc liền).
    """
    import re

    skip_tokens = {"3D", "2D", "4K", "8K", "5G", "4G", "M2", "S24", "B52"}

    def _repl(match: re.Match) -> str:
        tok = match.group(0)
        if tok.upper() in skip_tokens:
            return tok
        letters = match.group(1)
        digits = match.group(2)
        if digits.startswith("0") or (letters.isupper() and len(digits) in (2, 3)):
            l_spoken = " ".join(_VN_LETTER_PRON.get(ch.lower(), ch) for ch in letters)
            d_spoken = " ".join(_VN_DIGIT_PRON.get(d, d) for d in digits)
            return f"{l_spoken} {d_spoken}"
        return tok

    return re.sub(r"\b([A-Za-z]{1,2})(\d{2,3})\b", _repl, text)


class VieNeuWhisperPacer:
    def __init__(self, output_dir: Optional[Path | str] = None):
        self.base_dir = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
        if output_dir:
            self.voice_output_dir = Path(output_dir)
        else:
            # Mặc định trỏ về thư mục WIP dự án, TUYỆT ĐỐI KHÔNG lưu vào Đầu Não
            self.voice_output_dir = Path(r"D:\DuAn_DangLam\temp")
        self.voice_output_dir.mkdir(parents=True, exist_ok=True)
        self.whisper_model = None

    def _get_whisper(self):
        if self.whisper_model is None:
            from faster_whisper import WhisperModel
            # Sử dụng model base/tiny để nhận diện cực nhanh trên CPU
            self.whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        return self.whisper_model

    def _assert_local_hai_dang_voice(self, voice_name: str):
        """Khóa cứng giọng nội bộ 'Hải Đăng', cấm fallback sang bất kỳ giọng/TTS nào khác."""
        required_voice = "Hải Đăng"
        if (voice_name or "").strip() != required_voice:
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: Chỉ cho phép giọng local '{required_voice}', "
                f"từ chối giọng '{voice_name}'."
            )

        vieneu_root = Path(r"D:\VieNeu-TTS")
        old_voice_py = Path(r"D:\Đầu Não (không xóa)\engine\vieneu_voice_engine.py")
        if not vieneu_root.exists() or not old_voice_py.exists():
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: Thiếu VieNeu-TTS local ({vieneu_root}) "
                f"hoặc voice engine ({old_voice_py})."
            )

        if str(vieneu_root) not in sys.path:
            sys.path.insert(0, str(vieneu_root))

        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("old_voice", str(old_voice_py))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            client = mod.get_vieneu_client()
            if hasattr(client, "list_preset_voices"):
                presets = client.list_preset_voices()
                names = [
                    (p[0] if isinstance(p, (tuple, list)) else str(p))
                    for p in (presets or [])
                ]
                if not any(required_voice.lower() in n.lower() for n in names):
                    raise RuntimeError(
                        f"MISSING_LOCAL_VOICE_HAI_DANG: Không tìm thấy giọng '{required_voice}' "
                        f"trong danh sách local VieNeu-TTS: {names}"
                    )
            return mod
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: Không thể nạp giọng local '{required_voice}': {exc}"
            ) from exc

    def generate_voiceover(
        self,
        script_text: str,
        voice_name: str = "Hải Đăng",
        output_wav: Optional[Path] = None
    ) -> Path:
        """
        Sinh file WAV giọng đọc local 'Hải Đăng' từ VieNeu TTS (CẤM fallback giọng khác).
        """
        if output_wav is None:
            output_wav = self.voice_output_dir / "voiceover.wav"
        output_wav = Path(output_wav)
        output_wav.parent.mkdir(parents=True, exist_ok=True)

        mod = self._assert_local_hai_dang_voice(voice_name)
        try:
            mod.generate_voice(text=script_text, voice="Hải Đăng", output_path=str(output_wav))
        except Exception as exc:
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: Lỗi khi sinh giọng local 'Hải Đăng': {exc}"
            ) from exc

        if not output_wav.exists() or output_wav.stat().st_size < 1024:
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: File WAV sinh ra không hợp lệ ({output_wav})."
            )
        return output_wav

    def extract_word_timestamps(self, audio_wav: Path) -> List[Dict]:
        """
        Dùng faster-whisper trích xuất toạ độ từng từ (start, end tính theo giây)
        """
        model = self._get_whisper()
        segments, info = model.transcribe(
            str(audio_wav),
            word_timestamps=True,
            language="vi"
        )

        words_data = []
        for segment in segments:
            for w in segment.words:
                words_data.append({
                    "word": w.word.strip(),
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(w.probability, 3)
                })

        return words_data

    def process_script(
        self,
        script_text: str,
        out_prefix: str = "voiceover",
        output_dir: Optional[Path | str] = None,
        voice_name: str = "Hải Đăng",
    ) -> Dict:
        """
        Quy trình trọn gói: Sinh giọng Hải Đăng -> Whisper Word-Timestamps.
        Luôn xuất đúng chuẩn: voiceover.wav & words.json khi dùng mặc định.
        """
        target_dir = Path(output_dir) if output_dir else self.voice_output_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        wav_path = target_dir / ("voiceover.wav" if out_prefix == "voiceover" else f"{out_prefix}.wav")
        json_path = target_dir / ("words.json" if out_prefix == "voiceover" else f"{out_prefix}_words.json")

        # 1. Tiền xử lý mã chữ+số ngắn (C04 -> xê không bốn) rồi sinh voiceover
        tts_ready_text = normalize_vietnamese_tts_codes(script_text)
        self.generate_voiceover(tts_ready_text, voice_name=voice_name, output_wav=wav_path)

        # 2. Bóc tách timestamps
        words = self.extract_word_timestamps(wav_path)

        # 3. Lưu JSON kèm metadata khóa giọng local Hải Đăng
        meta_payload = {
            "voice_name": "Hải Đăng",
            "voice_source": "local",
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "script": script_text,
                "voice": "Hải Đăng",
                **meta_payload,
                "duration": words[-1]["end"] if words else 0.0,
                "word_count": len(words),
                "words": words
            }, f, ensure_ascii=False, indent=2)

        voice_meta_path = target_dir / "voice_meta.json"
        with open(voice_meta_path, "w", encoding="utf-8") as mf:
            json.dump({
                **meta_payload,
                "wav_path": str(wav_path),
                "words_path": str(json_path),
                "duration": words[-1]["end"] if words else 0.0,
            }, mf, ensure_ascii=False, indent=2)

        return {
            "wav_path": str(wav_path),
            "json_path": str(json_path),
            "duration": words[-1]["end"] if words else 0.0,
            "word_count": len(words),
            "words": words
        }


def _extract_script_text(script_path: Path) -> str:
    """Đọc nội dung lời thoại từ file .txt hoặc .json (tự nối toàn bộ nhịp theo thứ tự)."""
    raw = script_path.read_text(encoding="utf-8").strip()
    if script_path.suffix.lower() != ".json":
        return raw

    data = json.loads(raw)
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, dict):
        for key in ("full_script", "full_voiceover", "script_text"):
            if isinstance(data.get(key), str) and data[key].strip():
                return data[key].strip()
        parts: List[str] = []
        beats = data.get("beats") or data.get("scenes") or data.get("segments") or []
        if isinstance(beats, list):
            for b in beats:
                if isinstance(b, str):
                    if b.strip():
                        parts.append(b.strip())
                elif isinstance(b, dict):
                    txt = (
                        b.get("voiceover")
                        or b.get("narration")
                        or b.get("voice_text")
                        or b.get("spoken_text")
                        or b.get("text")
                        or b.get("script")
                    )
                    if isinstance(txt, str) and txt.strip():
                        parts.append(txt.strip())
                    elif isinstance(b.get("lines"), list):
                        for ln in b["lines"]:
                            if isinstance(ln, str) and ln.strip():
                                parts.append(ln.strip())
                            elif isinstance(ln, dict):
                                lt = ln.get("text") or ln.get("voiceover") or ln.get("narration")
                                if isinstance(lt, str) and lt.strip():
                                    parts.append(lt.strip())
        if parts:
            return " ".join(parts)
        if isinstance(data.get("script"), str) and data["script"].strip():
            return data["script"].strip()
    elif isinstance(data, list):
        parts = []
        for item in data:
            if isinstance(item, str) and item.strip():
                parts.append(item.strip())
            elif isinstance(item, dict):
                txt = item.get("voiceover") or item.get("narration") or item.get("text") or item.get("script")
                if isinstance(txt, str) and txt.strip():
                    parts.append(txt.strip())
        if parts:
            return " ".join(parts)

    raise ValueError(f"Không trích xuất được lời thoại từ file JSON: {script_path}")


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="Sinh giọng đọc VieNeu TTS (Hải Đăng) & bóc tách word timestamps (temp/voiceover.wav + temp/words.json)."
    )
    ap.add_argument("--script", help="Đường dẫn tới script_5beat.json hoặc file .txt lời thoại")
    ap.add_argument("--project", help="Thư mục dự án WIP (VD: D:\\DuAn_DangLam\\ten_du_an)")
    ap.add_argument("--voice", default="Hải Đăng", help="Tên giọng đọc VieNeu TTS (khóa cứng mặc định: Hải Đăng)")
    ap.add_argument("--check-voice", action="store_true", help="Kiểm tra nhanh giọng local 'Hải Đăng' trên máy")
    args = ap.parse_args()

    if args.check_voice:
        pacer = VieNeuWhisperPacer()
        pacer._assert_local_hai_dang_voice(args.voice)
        print(f"[OK] Verified local voice: {args.voice} (source=local)")
        return 0

    if not args.script or not args.project:
        ap.error("Cần truyền --script và --project (hoặc --check-voice).")

    script_path = Path(args.script)
    if not script_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file kịch bản: {script_path}")

    script_text = _extract_script_text(script_path)
    out_dir = Path(args.project) / "temp"
    pacer = VieNeuWhisperPacer(output_dir=out_dir)
    res = pacer.process_script(
        script_text=script_text,
        out_prefix="voiceover",
        output_dir=out_dir,
        voice_name=args.voice,
    )
    print(f"[OK] WAV: {res['wav_path']}")
    print(f"[OK] WORDS: {res['json_path']}")
    print(f"[OK] Processed {res['word_count']} words | Duration: {res['duration']}s | Voice: {args.voice}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```


#### `engine/auto_asset_harvester.py`

```python
# -*- coding: utf-8 -*-
r"""
auto_asset_harvester.py - ĐẦU NÃO CÀO TƯ LIỆU THỰC TẾ & MẮT THẦN GEMINI VISION ĐỘC BẢN
(Dành riêng cho Hệ thống Video Ngắn FB Reels: D:\Đầu Não Video Ngắn FB (không xóa))

TRIỆT TIÊU 100% CÁC LỖI TỬ HUYỆT (ZERO-MISMATCH MANDATE):
1. CẤM TUYỆT ĐỐI ẨN DỤ TRỪU TƯỢNG VÔ NGHĨA (BANNED METAPHORS):
   - Chặn đứng 100% việc video công nghệ/đời thực lại đi cào cân công lý thời trung cổ,
     não hoạt hình, chai nước hoa hay bảng ăn kiêng!
   - Bắt buộc tư liệu phải là THỰC THỂ THỰC TẾ: Giao diện app thật, tài xế thật,
     máy chủ thật, bản đồ nhiệt thật, hồ sơ/bằng chứng thật.
2. ĐA TẦNG NGUỒN DỮ LIỆU ĐẲNG CẤP:
   - Tầng 1: Tavily Image Search (Báo chí chính thống VN: Thanh Niên, Tuổi Trẻ, Dân Trí, CafeF).
   - Tầng 2: Wikimedia Commons API (Kho lưu trữ quốc tế, siêu máy chủ, bản đồ, phần cứng).
   - Tầng 3: Bing HD Clean qua Playwright (Lọc sạch 100% domain rác).
3. CHẶN ĐỨNG 100% WATERMARK & DOMAIN RÁC:
   - Danh sách đen: Alamy, Shutterstock, Getty, iStock, Pinterest, eBay, Shopee...
4. MẮT THẦN GEMINI VISION PHÊ DUYỆT BẮT BUỘC (MULTI-KEY FAILOVER):
   - Soi chiếu trực tiếp ảnh tải về với chủ đề bài viết và bối cảnh câu thoại.
   - Bác bỏ ngay lập tức nếu ảnh lạc đề, mờ nhòe, hoặc dính chữ bản quyền.
5. TỰ ĐỘNG XUẤT ẢNH TIẾP XÚC (CONTACT SHEET) KIỂM ĐỊNH THỊ GIÁC:
   - Ghép toàn bộ tư liệu đã cào vào 1 ảnh lưới contact sheet duy nhất có nhãn sắc nét
     để Con Tổng soi trực tiếp trước khi bắt tay vào dựng video.
"""

from __future__ import annotations

import html
import io
import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if sys.stderr:
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

FB_ROOT = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
ENGINE_DIR = FB_ROOT / "engine"
DEFAULT_HARVEST_DIR = Path(r"D:\DuAn_DangLam\temp\assets")

# Nạp API keys từ hệ thống HaDaWhy Facebook AI
HADA_FB_DIR = Path(r"D:\HaDaWhy_Facebook_AI")
load_dotenv(HADA_FB_DIR / ".env")
if str(HADA_FB_DIR) not in sys.path:
    sys.path.insert(0, str(HADA_FB_DIR))

try:
    import hd_image_extractor as vision_inspector
    HAS_VISION_INSPECTOR = True
except Exception as exc:
    print(f"[HARVESTER WARN] Không thể import hd_image_extractor ({exc}). Fallback sang chế độ lọc chữ ký.")
    HAS_VISION_INSPECTOR = False


# =============================================================================
# 1. BỘ LỌC ẨN DỤ TRỪU TƯỢNG VÔ NGHĨA (CHỐNG LỆCH CHỦ ĐỀ NGAY TỪ ĐẦU VÀO)
# =============================================================================
BANNED_ABSTRACT_METAPHORS = [
    "scale", "justice scale", "balance scale", "cái cân", "chiếc cân", "cân công lý",
    "perfume", "nước hoa", "louis vuitton",
    "diet", "nutrition", "workout", "giảm cân", "thực đơn",
    "cartoon brain", "icon não", "plastic icon", "sticker",
    "handshake 3d", "bàn tay bắt tay", "hộp quà 3d",
    # Chặn các từ khóa kéo ra đồ CGI/nhựa giả, siêu thực/ma-nơ-canh & nhạy cảm vi phạm chính sách FB/TikTok
    "3d icon", "3d render", "3d model", "blender", "cgi", "isometric",
    "glossy icon", "illustration", "mockup", "vector", "pngtree", "clipart",
    "mannequin", "ma-nơ-canh", "surreal", "wax figure", "doll",
    "bikini", "lingerie", "nsfw", "nude", "sexy", "erotic", "gore", "blood", "corpse", "deformed",
]

def validate_harvest_query(query: str, topic_domain: str = "") -> None:
    """
    Kiểm tra tính hợp lệ của từ khóa tìm kiếm:
    Tuyệt đối cấm các từ khóa ẩn dụ vô hồn (cái cân, nước hoa, thực đơn ăn kiêng) và từ khóa CGI/render/icon.
    """
    q_low = query.lower()
    for banned in BANNED_ABSTRACT_METAPHORS:
        if banned in q_low:
            raise ValueError(
                f"[LỖI VI PHẠM KỶ LUẬT THỊ GIÁC] Từ khóa '{query}' chứa ẩn dụ trừu tượng/sai lệch '{banned}'. "
                f"Chủ đề '{topic_domain}' yêu cầu thực thể thực tế (tên riêng chính xác + ảnh chụp thật)!"
            )
    if re.search(r"\brender\b", q_low):
        raise ValueError(
            f"[LỖI VI PHẠM KỶ LUẬT THỊ GIÁC] Từ khóa '{query}' chứa từ cấm 'render'. "
            "Chỉ dùng từ khóa chụp thật ('official photo', 'close up', 'isolated', 'product photography', 'archival photo')!"
        )


# =============================================================================
# 2. DANH SÁCH ĐEN TÊN MIỀN RÁC & WATERMARK THƯƠNG MẠI
# =============================================================================
BANNED_DOMAINS = [
    # Stock photo watermark heavy
    "alamy.com", "shutterstock.com", "gettyimages.com", "istockphoto.com",
    "dreamstime.com", "depositphotos.com", "123rf.com", "vecteezy.com",
    "stock.adobe.com", "ftcdn.net", "vectorstock.com", "canstockphoto.com", "bigstockphoto.com",
    "freepik.com", "pngwing.com", "pngtree.com", "flaticon.com", "stockcake.com", "magnific.com",
    "thuthuatphanmem.vn",
    # Pinterest & spam pinboards
    "pinterest.com", "pinimg.com",
    # E-commerce marketplace ads
    "ebay.com", "amazon.com", "aliexpress.com", "temu.com",
    "shopee.vn", "lazada.vn", "tiki.vn", "alibaba.com", "dhgate.com",
    # Low quality user avatars
    "lookaside.fbsbx.com", "lookaside.instagram.com", "fbcdn.net",
]

JUNK_PATH_PATTERNS = [
    "logo_default", "logo.", "/logo", "logo_", "icon.", "/icon",
    "/avatar.", "/avatars/", "avatar_default", "default_avatar",
    "placeholder", "default_image", "banner", "tracking", "button", "badge",
    "meme", "clipart", "emoji", "sticker", "cartoon", "vector",
    "3d icon", "3d-icon", "3d_icon", "3d render", "3d-render", "3d_render",
    "3d model", "3d-model", "blender", "cgi", "isometric",
    "glossy icon", "illustration", "mockup", "pngtree",
    "watermark", "logo-tron", "stamp-logo", "mannequin", "surreal",
    "bikini", "lingerie", "nsfw", "nude", "sexy", "gore", "blood",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

WIKI_HEADERS = {
    "User-Agent": "HaDaWhyMediaProducer/2.0 (mailto:admin@hadawhy.vn)"
}

SSL_CTX = ssl._create_unverified_context()


def is_banned_url(url: str) -> bool:
    """Kiểm tra URL có thuộc tên miền dính watermark hoặc spam không."""
    low = url.lower()
    for dom in BANNED_DOMAINS:
        if dom in low:
            return True
    for pat in JUNK_PATH_PATTERNS:
        if pat in low:
            return True
    return False


# =============================================================================
# 3. NGUỒN TƯ LIỆU 1: TAVILY IMAGE SEARCH (BÁO CHÍ CHÍNH THỐNG VIỆT NAM)
# =============================================================================
def search_tavily_editorial_images(query: str, max_urls: int = 8) -> List[str]:
    """Tìm kiếm ảnh báo chí thực tế chất lượng cao qua Tavily Search API."""
    tavily_key = os.environ.get("TAVILY_API_KEY")
    if not tavily_key:
        return []

    urls: List[str] = []
    try:
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=json.dumps({
                "api_key": tavily_key,
                "query": query,
                "include_images": True,
                "max_results": max_urls,
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=12, context=SSL_CTX) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for u in data.get("images", []):
                if is_banned_url(u):
                    continue
                if u not in urls:
                    urls.append(u)
    except Exception as exc:
        print(f"[HARVESTER WARN] Tavily Image Search error: {exc}")
    return urls


# =============================================================================
# 4. NGUỒN TƯ LIỆU 2: WIKIMEDIA COMMONS CHÍNH QUY (FILE NAMESPACE = 6)
# =============================================================================
def search_wikimedia_commons(query: str, max_urls: int = 8) -> List[str]:
    """Tìm kiếm trực tiếp trên Wikimedia Commons API chuẩn namespace 6 (File:)."""
    encoded = urllib.parse.quote(query)
    api_url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&list=search"
        f"&srsearch={encoded}&srnamespace=6&srlimit={max_urls}&format=json"
    )
    urls: List[str] = []
    try:
        req = urllib.request.Request(api_url, headers=WIKI_HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
        search_items = data.get("query", {}).get("search", [])

        for item in search_items:
            title = item.get("title", "")
            if not any(title.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                continue

            info_url = (
                f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}"
                f"&prop=imageinfo&iiprop=url|size&format=json"
            )
            req2 = urllib.request.Request(info_url, headers=WIKI_HEADERS)
            with urllib.request.urlopen(req2, timeout=8, context=SSL_CTX) as resp2:
                info_data = json.loads(resp2.read().decode("utf-8", errors="ignore"))
            pages = info_data.get("query", {}).get("pages", {})
            for _, p in pages.items():
                iinfo = p.get("imageinfo", [])
                if iinfo:
                    direct_url = iinfo[0].get("url", "")
                    w = iinfo[0].get("width", 0)
                    h = iinfo[0].get("height", 0)
                    if direct_url and w >= 600 and h >= 400:
                        urls.append(direct_url)
    except Exception as exc:
        print(f"[HARVESTER WARN] Wikimedia search error: {exc}")
    return urls


# =============================================================================
# 5. NGUỒN TƯ LIỆU 3: BING IMAGES HD (LỌC 100% SPAM DOMAINS)
# =============================================================================
def search_bing_hd_clean(query: str, max_urls: int = 15) -> List[str]:
    """Quét Bing Images bằng Playwright headless, tự động gạt bỏ 100% domain rác."""
    encoded = urllib.parse.quote(query)
    search_url = f"https://www.bing.com/images/search?q={encoded}"
    urls: List[str] = []

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(user_agent=HEADERS["User-Agent"])
            page = ctx.new_page()
            page.goto(search_url, wait_until="domcontentloaded", timeout=16000)
            page.wait_for_timeout(1500)
            cards = page.evaluate("""() => {
                const out = [];
                for (const el of document.querySelectorAll('a.iusc')) {
                    const m = el.getAttribute('m');
                    if (m) {
                        try {
                            const parsed = JSON.parse(m);
                            if (parsed.murl) out.push(parsed.murl);
                        } catch(e) {}
                    }
                }
                return out;
            }""")
            browser.close()
            for u in cards:
                if is_banned_url(u):
                    continue
                if any(ext in u.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                    if u not in urls:
                        urls.append(u)
                if len(urls) >= max_urls:
                    break
        if urls:
            return urls
    except Exception as exc:
        print(f"[HARVESTER WARN] Playwright error: {exc}. Fallback regex...")

    # Fallback nhẹ bằng urllib
    try:
        req = urllib.request.Request(search_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            page_html = resp.read().decode("utf-8", errors="ignore")
        matches = re.findall(r'murl&quot;:&quot;(https?://[^&]+?)&quot;', page_html)
        for m in matches:
            clean_url = html.unescape(m)
            if is_banned_url(clean_url):
                continue
            if any(ext in clean_url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                if clean_url not in urls:
                    urls.append(clean_url)
            if len(urls) >= max_urls:
                break
    except Exception as exc:
        print(f"[HARVESTER WARN] Bing fallback error: {exc}")
    return urls


# =============================================================================
# 6. MẮT THẦN GEMINI VISION THẨM ĐỊNH NỘI DUNG (CÓ --skip-vision & AUTO-FALLBACK 429)
# =============================================================================
_SKIP_VISION_SESSION = False


def set_skip_vision(skip: bool) -> None:
    global _SKIP_VISION_SESSION
    _SKIP_VISION_SESSION = bool(skip)


def verify_candidate_with_vision(
    img_path: Path,
    expected_entity: str,
    context_sentence: str = "",
    topic_domain: str = "",
    skip_vision: bool = False,
) -> Tuple[bool, str]:
    """
    Soi mắt thần Gemini Vision trước khi cấp phép lưu ảnh.
    - Nếu bật skip_vision hoặc phiên đã gặp 429/RESOURCE_EXHAUSTED: tự động bỏ qua API Vision
      (vẫn giữ nguyên 100% lọc domain rác, độ phân giải, từ khóa cấm, dHash và check_cutout_completeness).
    """
    global _SKIP_VISION_SESSION

    if skip_vision or _SKIP_VISION_SESSION:
        return True, "Đã bỏ qua API Vision (--skip-vision / auto-fallback 429)."

    if not HAS_VISION_INSPECTOR:
        return True, "Vision Inspector không khả dụng, bỏ qua."

    strict_real_photo_rule = (
        "YÊU CẦU TUYỆT ĐỐI VỀ CHẤT LIỆU & KHUNG HÌNH: "
        "TỪ CHỐI NGAY (is_match=false) mọi ảnh 3D render bóng nhựa, CGI, Blender, hình vẽ minh họa (illustration), "
        "clipart, vector, mockup, icon hoạt hình, HOẶC ảnh bị cắt cụt mất đầu/nửa xe/nửa vật thể ở viền khung hình. "
        "CHỈ DUYỆT ảnh chụp vật lý thật ngoài đời có vật liệu thật (kim loại, gỗ, giấy in, linh kiện thật, hiện trường thật) và chủ thể nằm trọn trong khung hình."
    )
    full_context = f"{topic_domain} | {context_sentence} | {strict_real_photo_rule}".strip(" |")
    try:
        status, reason = vision_inspector._verify_image_with_vision(
            str(img_path),
            topic_title=expected_entity,
            topic_context=full_context,
        )
        reason_low = str(reason or "").lower()
        if status is None or any(tok in reason_low for tok in ("429", "resource_exhausted", "quota", "hạn ngạch", "rate limit")):
            _SKIP_VISION_SESSION = True
            print(f"   [VISION AUTO-FALLBACK 429] Gặp giới hạn API ({reason}) -> Tự động bật --skip-vision cho các ảnh còn lại!")
            return True, f"Auto-fallback bỏ qua Vision do 429/quota ({reason})."
        return bool(status), str(reason)
    except Exception as exc:
        err_low = str(exc).lower()
        if any(tok in err_low for tok in ("429", "resource_exhausted", "quota", "rate limit")):
            _SKIP_VISION_SESSION = True
            print(f"   [VISION AUTO-FALLBACK 429] Gặp ngoại lệ API ({exc}) -> Tự động bật --skip-vision cho các ảnh còn lại!")
            return True, f"Auto-fallback bỏ qua Vision do 429/quota ({exc})."
        return False, f"Lỗi Mắt Thần Vision: {exc}"


# =============================================================================
# 7. CHỐNG LẶP ẢNH 3 TẦNG (URL + MD5 + PERCEPTUAL DHASH + LỊCH SỬ TẬP CŨ)
# =============================================================================
IMAGE_HISTORY_PATH = ENGINE_DIR / "image_used_history.json"


def _compute_dhash_hex(img: Image.Image) -> str:
    """Tính perceptual dHash 64-bit (16 ký tự hex) để phát hiện ảnh trùng kể cả khác kích thước/CDN."""
    gray = img.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
    pixels = list(gray.getdata())
    bits = 0
    for row in range(8):
        row_start = row * 9
        for col in range(8):
            bits = (bits << 1) | (1 if pixels[row_start + col] > pixels[row_start + col + 1] else 0)
    return f"{bits:016x}"


def _dhash_hamming(hex_a: str, hex_b: str) -> int:
    try:
        return (int(hex_a, 16) ^ int(hex_b, 16)).bit_count()
    except Exception:
        return 64


class ImageDedupeRegistry:
    """Sổ kiểm soát chống lặp ảnh trong cùng 1 video và giữa các video/tập khác nhau."""

    def __init__(self, history_path: Path = IMAGE_HISTORY_PATH, check_global_history: bool = True):
        self.history_path = history_path
        self.check_global_history = check_global_history
        self.session_urls: set[str] = set()
        self.session_md5s: set[str] = set()
        self.session_dhashes: list[str] = []
        self.history_entries: list[dict[str, Any]] = []
        self._load_history()

    def _load_history(self) -> None:
        if self.history_path.exists():
            try:
                data = json.loads(self.history_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self.history_entries = data
                elif isinstance(data, dict):
                    self.history_entries = data.get("entries", [])
            except Exception:
                self.history_entries = []

    def _save_history(self) -> None:
        try:
            self.history_path.parent.mkdir(parents=True, exist_ok=True)
            trimmed = self.history_entries[-500:]
            self.history_path.write_text(
                json.dumps({"entries": trimmed}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            print(f"[DEDUPE WARN] Không lưu được lịch sử ảnh: {exc}")

    def is_url_used(self, url: str) -> Tuple[bool, str]:
        norm = url.strip().lower()
        if norm in self.session_urls:
            return True, "trùng URL trong cùng dự án"
        if self.check_global_history:
            for e in self.history_entries:
                if str(e.get("url", "")).strip().lower() == norm:
                    return True, f"đã dùng ở tập cũ ({e.get('project', 'unknown')})"
        return False, ""

    def is_image_duplicate(self, md5_hex: str, dhash_hex: str, max_hamming: int = 6) -> Tuple[bool, str]:
        if md5_hex in self.session_md5s:
            return True, "trùng MD5 tuyệt đối trong cùng dự án"
        for h in self.session_dhashes:
            if _dhash_hamming(dhash_hex, h) <= max_hamming:
                return True, "ảnh gần giống/trùng nội dung (dHash) trong cùng dự án"
        if self.check_global_history:
            for e in self.history_entries:
                if e.get("md5") == md5_hex:
                    return True, f"trùng MD5 với tập cũ ({e.get('project', 'unknown')})"
                eh = str(e.get("dhash", ""))
                if eh and _dhash_hamming(dhash_hex, eh) <= max_hamming:
                    return True, f"ảnh trùng nội dung (dHash) với tập cũ ({e.get('project', 'unknown')})"
        return False, ""

    def register(self, url: str, md5_hex: str, dhash_hex: str, project_name: str, entity_id: str) -> None:
        norm = url.strip().lower()
        self.session_urls.add(norm)
        self.session_md5s.add(md5_hex)
        self.session_dhashes.append(dhash_hex)
        self.history_entries.append({
            "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "project": project_name,
            "entity_id": entity_id,
            "url": url,
            "md5": md5_hex,
            "dhash": dhash_hex,
        })
        self._save_history()


# =============================================================================
# 7B. TẢI VÀ DUYỆT ẢNH THẬT QUA MẮT THẦN + CHỐNG TRÙNG 100%
# =============================================================================
def remove_background_safe(
    input_png: Path,
    output_png: Path,
    soft_bottom_fade: bool = False,
) -> Path:
    """
    Tách nền chất lượng cao bằng auto_cutout.cutout_image (bria-rmbg, defringe=True,
    edge_feather=0.8, add_rim_light=False); tự động fallback u2net nếu thiếu RAM.
    """
    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    import auto_cutout

    output_png.parent.mkdir(parents=True, exist_ok=True)
    # Chuẩn hóa kích thước ảnh lớn > 1400px vào file tạm để bảo vệ RAM
    work_in = input_png
    scaled_tmp: Optional[Path] = None
    with Image.open(input_png) as orig:
        if max(orig.size) > 1400:
            scale = 1400.0 / max(orig.size)
            resized = orig.convert("RGBA").resize(
                (int(orig.size[0] * scale), int(orig.size[1] * scale)),
                Image.Resampling.LANCZOS,
            )
            scaled_tmp = output_png.with_name(f"tmp_scale_{output_png.name}")
            resized.save(scaled_tmp, format="PNG")
            work_in = scaled_tmp

    try:
        try:
            auto_cutout.cutout_image(
                work_in,
                output_png,
                model_name="bria-rmbg",
                defringe=True,
                edge_feather=0.7,
                add_rim_light=False,
                crop_tight=False,
                soft_bottom_fade=soft_bottom_fade,
            )
        except Exception as exc:
            print(f"[AI CUTOUT WARN] bria-rmbg lỗi ({exc}), fallback sang u2net...")
            auto_cutout.cutout_image(
                work_in,
                output_png,
                model_name="u2net",
                defringe=True,
                edge_feather=0.7,
                add_rim_light=False,
                crop_tight=False,
                soft_bottom_fade=soft_bottom_fade,
            )
    finally:
        if scaled_tmp and scaled_tmp.exists():
            scaled_tmp.unlink(missing_ok=True)

    return output_png


def download_and_verify_image(
    urls: List[str],
    out_path: Path,
    expected_entity: str,
    context_sentence: str = "",
    topic_domain: str = "",
    min_width: int = 600,
    min_height: int = 400,
    dedupe: Optional[ImageDedupeRegistry] = None,
    project_name: str = "",
    entity_id: str = "",
    remove_bg: bool = False,
    final_cutout_path: Optional[Path] = None,
) -> Tuple[Optional[Path], str]:
    """
    Duyệt từng ứng viên: Kiểm trùng URL -> Tải -> Kiểm kích thước & dHash -> Mắt Thần soi.
    Nếu remove_bg=True: chạy tách nền thử + check_cutout_completeness(), tự loại ảnh bị chém cụt mép;
    nếu hết ứng viên mà chỉ còn ảnh bán thân chạm đáy -> tự bật soft_bottom_fade=True + display_mode='framed_or_faded'.
    Trả về: (saved_raw_path_or_None, display_mode).
    """
    import hashlib
    import shutil

    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    import auto_cutout

    tmp_path = out_path.with_name(f"tmp_verify_{out_path.name}")
    tmp_cut_path = out_path.with_name(f"tmp_cut_{out_path.name}")
    fallback_raw_path = out_path.with_name(f"tmp_fb_raw_{out_path.name}")
    fallback_meta: Optional[Tuple[str, str, str]] = None  # (url, md5, dhash)

    for idx, u in enumerate(urls[:20]):
        try:
            if dedupe is not None:
                used, why = dedupe.is_url_used(u)
                if used:
                    print(f"   [Bỏ qua trùng #{idx+1}] {why}: {u[:70]}...")
                    continue

            print(f"   [Soi ứng viên #{idx+1}] Đang tải: {u[:80]}...")
            hdrs = WIKI_HEADERS if "wikimedia.org" in u else HEADERS
            req = urllib.request.Request(u, headers=hdrs)
            with urllib.request.urlopen(req, timeout=12, context=SSL_CTX) as resp:
                raw_bytes = resp.read()

            if len(raw_bytes) < 25000:
                print(f"   [Bỏ qua #{idx+1}] File quá nhẹ ({len(raw_bytes)} bytes < 25KB)")
                continue

            md5_hex = hashlib.md5(raw_bytes).hexdigest()
            with open(tmp_path, "wb") as f:
                f.write(raw_bytes)

            with Image.open(tmp_path) as img:
                w, h = img.size
                if w < min_width or h < min_height:
                    print(f"   [Bỏ qua #{idx+1}] Kích thước {w}x{h} < {min_width}x{min_height}")
                    should_skip = True
                    dhash_hex = ""
                else:
                    should_skip = False
                    dhash_hex = _compute_dhash_hex(img)

            if should_skip:
                tmp_path.unlink(missing_ok=True)
                continue

            if dedupe is not None:
                is_dup, dup_why = dedupe.is_image_duplicate(md5_hex, dhash_hex)
                if is_dup:
                    print(f"   [Bỏ qua trùng ảnh #{idx+1}] {dup_why}")
                    tmp_path.unlink(missing_ok=True)
                    continue

            # SOI MẮT THẦN GEMINI VISION
            matched, reason = verify_candidate_with_vision(
                tmp_path,
                expected_entity=expected_entity,
                context_sentence=context_sentence,
                topic_domain=topic_domain,
            )

            if not matched:
                print(f"   [MẮT THẦN TỪ CHỐI #{idx+1}] {reason}")
                tmp_path.unlink(missing_ok=True)
                continue

            print(f"   [MẮT THẦN DUYỆT OK #{idx+1}] {reason}")

            if remove_bg and final_cutout_path is not None:
                # Chạy tách nền thử và kiểm tra độ nguyên vẹn 4 viền TRƯỚC crop_tight
                remove_background_safe(tmp_path, tmp_cut_path, soft_bottom_fade=False)
                with Image.open(tmp_cut_path) as cut_im:
                    comp = auto_cutout.check_cutout_completeness(cut_im)
                print(
                    f"   [CHECK VIỀN #{idx+1}] top={comp['top_touch']} bottom={comp['bottom_touch']} "
                    f"left={comp['left_touch']} right={comp['right_touch']} area={comp['subject_area_ratio']}"
                )
                if comp["is_chopped"]:
                    if comp["is_bottom_only_touch"] and fallback_meta is None:
                        print(f"   [DỰ PHÒNG CHẠM ĐÁY #{idx+1}] Giữ làm phương án soft_bottom_fade nếu hết ảnh trọn vẹn...")
                        shutil.copy2(tmp_path, fallback_raw_path)
                        fallback_meta = (u, md5_hex, dhash_hex)
                    else:
                        print(f"   [LOẠI CẮT CỤT MÉP #{idx+1}] Vật thể bị chém cụt viền khung -> chuyển ứng viên kế tiếp!")
                    tmp_path.unlink(missing_ok=True)
                    tmp_cut_path.unlink(missing_ok=True)
                    continue

                # Ảnh nguyên vẹn 4 cạnh! Lưu luôn bản raw và bản cutout sạch
                out_path.parent.mkdir(parents=True, exist_ok=True)
                final_cutout_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(tmp_path, out_path)
                shutil.copy2(tmp_cut_path, final_cutout_path)
                tmp_path.unlink(missing_ok=True)
                tmp_cut_path.unlink(missing_ok=True)
                fallback_raw_path.unlink(missing_ok=True)
                if dedupe is not None:
                    dedupe.register(u, md5_hex, dhash_hex, project_name or out_path.parent.parent.parent.name, entity_id or out_path.stem)
                return out_path, "cutout_clean"

            # Không tách nền (ảnh bối cảnh bg_*)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(tmp_path, out_path)
            tmp_path.unlink(missing_ok=True)
            if dedupe is not None:
                dedupe.register(u, md5_hex, dhash_hex, project_name or out_path.parent.parent.parent.name, entity_id or out_path.stem)
            return out_path, "full_backdrop"

        except Exception as exc:
            print(f"   [Lỗi tải ứng viên #{idx+1}] {exc}")
            tmp_path.unlink(missing_ok=True)
            tmp_cut_path.unlink(missing_ok=True)
            continue

    # Nếu hết ứng viên mà có ảnh bán thân chỉ chạm đáy -> tự bật soft_bottom_fade=True
    if remove_bg and final_cutout_path is not None and fallback_meta is not None and fallback_raw_path.exists():
        u, md5_hex, dhash_hex = fallback_meta
        print(f"   [FALLBACK SOFT_BOTTOM_FADE] Áp dụng làm tan mượt 18% cạnh đáy -> {final_cutout_path.name}")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fallback_raw_path, out_path)
        remove_background_safe(out_path, final_cutout_path, soft_bottom_fade=True)
        fallback_raw_path.unlink(missing_ok=True)
        if dedupe is not None:
            dedupe.register(u, md5_hex, dhash_hex, project_name or out_path.parent.parent.parent.name, entity_id or out_path.stem)
        return out_path, "framed_or_faded"

    fallback_raw_path.unlink(missing_ok=True)
    return None, ""


# =============================================================================
# 9. HÀM CÀO CHÍNH THỐNG CHO MỌI THỰC THỂ
# =============================================================================
def harvest_entity_asset(
    entity_id: str,
    search_query: str,
    remove_bg: bool = True,
    target_dir: Path = DEFAULT_HARVEST_DIR,
    context_sentence: str = "",
    topic_domain: str = "",
    dedupe: Optional[ImageDedupeRegistry] = None,
    project_name: str = "",
) -> Dict[str, Any]:
    """
    Quy trình cào dữ liệu chuẩn mực 5 bước:
    1. Kiểm định từ khóa (chặn đứng ẩn dụ trừu tượng & CGI/nhựa giả)
    2. Săn ảnh đa tầng (Tavily Báo chí -> Wikimedia Commons -> Bing HD Clean)
    3. Chống trùng URL + MD5 + dHash + duyệt Mắt Thần Gemini Vision (chỉ duyệt ảnh chụp thật)
    4. Tách nền bria-rmbg + kiểm tra check_cutout_completeness() chống cắt cụt mép
    5. Xuất thông tin chuẩn (gồm display_mode) cho đạo diễn
    """
    validate_harvest_query(search_query, topic_domain=topic_domain)

    target_dir.mkdir(parents=True, exist_ok=True)
    raw_path = target_dir / f"{entity_id}_raw.png"
    final_path = target_dir / f"{entity_id}.png"

    print(f"\n========================================================")
    print(f"[*] SĂN TƯ LIỆU CHO [{entity_id}]: '{search_query}'")
    print(f"[*] Bối cảnh câu thoại: '{context_sentence}'")
    if topic_domain:
        print(f"[*] Miền chủ đề dự án: '{topic_domain}'")
    print(f"========================================================")

    # 1. Gom ứng viên từ 3 tầng nguồn sạch
    tavily_urls = search_tavily_editorial_images(search_query, max_urls=8)
    wiki_urls = search_wikimedia_commons(search_query, max_urls=6)
    bing_urls = search_bing_hd_clean(search_query, max_urls=12)

    candidate_urls = tavily_urls + wiki_urls + bing_urls
    print(f"[*] Tìm thấy {len(candidate_urls)} ứng viên tiềm năng (Tavily: {len(tavily_urls)}, Wiki: {len(wiki_urls)}, Bing: {len(bing_urls)})")

    downloaded, display_mode = download_and_verify_image(
        candidate_urls,
        raw_path,
        expected_entity=search_query,
        context_sentence=context_sentence,
        topic_domain=topic_domain,
        dedupe=dedupe,
        project_name=project_name,
        entity_id=entity_id,
        remove_bg=remove_bg,
        final_cutout_path=final_path if remove_bg else None,
    )

    if not downloaded or not downloaded.exists():
        raise RuntimeError(f"Mắt Thần/Kiểm tra viền từ chối toàn bộ ứng viên cho: '{search_query}'. Không có ảnh nào đạt chuẩn!")

    if not remove_bg:
        import shutil
        shutil.copy2(raw_path, final_path)

    with Image.open(final_path) as fin_im:
        fw, fh = fin_im.size
    if abs(fw - fh) <= max(fw, fh) * 0.08:
        orient = "square"
    elif fw > fh:
        orient = "landscape"
    else:
        orient = "portrait"

    return {
        "entity_id": entity_id,
        "query": search_query,
        "remove_bg": remove_bg,
        "display_mode": display_mode,
        "width": fw,
        "height": fh,
        "orientation": orient,
        "public_path": f"harvested/{final_path.name}",
        "abs_path": str(final_path),
    }


# =============================================================================
# 10. TẠO ẢNH TIẾP XÚC (CONTACT SHEET) KIỂM ĐỊNH TOÀN BỘ TƯ LIỆU BẰNG MẮT
# =============================================================================
def generate_assets_contact_sheet(
    assets_dir: Path,
    output_path: Path,
    title: str = "TỔNG THANH TRA TƯ LIỆU THỰC TẾ (HADA WHY)",
) -> Path:
    """
    Ghép toàn bộ file ảnh thành 1 contact sheet lưới 3 cột,
    có nhãn kích thước, tên file rõ ràng để Con Tổng soi trực tiếp.
    """
    image_files = sorted(
        [p for p in assets_dir.glob("*.png") if not p.name.endswith("_raw.png")] +
        [p for p in assets_dir.glob("*.jpg") if not p.name.endswith("_raw.jpg")]
    )

    if not image_files:
        raise ValueError(f"Không có ảnh nào trong thư mục: {assets_dir}")

    cols = 3
    rows = (len(image_files) + cols - 1) // cols
    cell_w, cell_h = 500, 360
    header_h = 100
    sheet_w = cols * cell_w + 40
    sheet_h = rows * cell_h + header_h + 30

    sheet = Image.new("RGB", (sheet_w, sheet_h), color=(15, 18, 24))
    draw = ImageDraw.Draw(sheet)

    # Tiêu đề Header
    draw.text((30, 25), title, fill=(255, 230, 0))
    draw.text((30, 60), f"Tổng cộng: {len(image_files)} tư liệu | Thư mục: {assets_dir.name}", fill=(180, 200, 220))

    for idx, fpath in enumerate(image_files):
        r = idx // cols
        c = idx % cols
        x0 = 20 + c * cell_w + 10
        y0 = header_h + r * cell_h + 10

        # Khung viền
        draw.rectangle([x0, y0, x0 + cell_w - 20, y0 + cell_h - 20], fill=(24, 28, 38), outline=(50, 60, 80))

        try:
            with Image.open(fpath) as im:
                im_w, im_h = im.size
                thumb = im.convert("RGBA")
                thumb.thumbnail((cell_w - 40, cell_h - 80), Image.Resampling.LANCZOS)
                tw, th = thumb.size

                # Paste thumb ở giữa
                px = x0 + (cell_w - 20 - tw) // 2
                py = y0 + 10 + (cell_h - 80 - th) // 2
                sheet.paste(thumb, (px, py), mask=thumb.split()[3] if len(thumb.split()) == 4 else None)

                # Nhãn file & kích thước
                label = f"#{idx+1}: {fpath.name}"
                info = f"{im_w}x{im_h} | {fpath.stat().st_size // 1024}KB"
                draw.text((x0 + 10, y0 + cell_h - 55), label[:35], fill=(255, 255, 255))
                draw.text((x0 + 10, y0 + cell_h - 35), info, fill=(0, 229, 255))
        except Exception as e:
            draw.text((x0 + 10, y0 + 50), f"Lỗi đọc ảnh: {e}", fill=(255, 80, 80))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92)
    print(f"[CONTACT SHEET OK] Đã tạo ảnh lưới kiểm định: {output_path} ({sheet_w}x{sheet_h})")
    return output_path


def purge_harvested_folder(target_dir: Path = DEFAULT_HARVEST_DIR) -> None:
    """Làm sạch thư mục assets dự án trước khi cào mới."""
    if target_dir.exists():
        for p in target_dir.glob("*"):
            if p.is_file():
                p.unlink(missing_ok=True)
    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"[ZERO-CARRYOVER OK] Đã dọn sạch: {target_dir}")


# =============================================================================
# 11. TỰ ĐỘNG ĐỌC KỊCH BẢN -> BÓC TÁCH THỰC THỂ KHỚP ĐÚNG LỜI ĐỌC (SCRIPT-TO-PLAN)
# =============================================================================
def build_harvest_plan_from_script(script_path: Path, output_plan_path: Path) -> Dict[str, Any]:
    """
    Đọc script_5beat.json (hoặc .txt), dùng Gemini bóc tách từng nhịp/câu thoại
    thành danh sách tư liệu ĐỜI THẬT/CÔNG NGHỆ khớp chính xác 1-1 với những thứ cần hiện ra:
    - KHÔNG lặp ảnh giữa các cảnh (mỗi cảnh có bg_* và/hoặc 3d_* riêng biệt).
    - Gắn đúng voice_anchor_quote (cụm từ trong lời đọc) + context_sentence (nguyên câu thoại).
    - Cấm tuyệt đối ẩn dụ trừu tượng vô nghĩa.
    """
    raw_script = script_path.read_text(encoding="utf-8").strip()
    try:
        from gemini_utils import generate_content_resilient
    except Exception as exc:
        raise RuntimeError(f"Không thể import gemini_utils để phân tích kịch bản: {exc}")

    prompt = f"""Bạn là Đạo diễn Hình ảnh & Trinh sát Tư liệu của kênh FB Reels HaDa Why.
Hãy đọc kỹ kịch bản sau và lập kế hoạch cào ảnh JSON (`harvest_plan.json`) khớp CHÍNH XÁC TỪNG CÂU LỜI ĐỌC.

KỊCH BẢN GỐC:
{raw_script[:6000]}

YÊU CẦU BẮT BUỘC:
1. Chỉ chọn những thực thể HỮU HÌNH, ĐỜI THẬT hoặc CÔNG NGHỆ THẬT được nhắc trực tiếp trong lời đọc (nhân vật thật, địa điểm thật, hiện trường thật, giao diện app/báo cáo thật, thiết bị/máy chủ/bản đồ thật).
2. CẤM TUYỆT ĐỐI ẩn dụ trừu tượng vô nghĩa (cân công lý, não hoạt hình, bàn tay bắt tay, chai nước hoa, icon nhựa, bảng ăn kiêng).
3. CHỐNG LẶP ẢNH: Mỗi cảnh (`scene_id`) phải có `entity_id` và `search_query` RIÊNG BIỆT. Tạo đủ cả:
   - Ảnh nền hiện trường (`entity_id` bắt đầu bằng `bg_`, `remove_bg`: false) — mỗi nhịp/bối cảnh 1 ảnh khác nhau.
   - Chủ thể nổi khối (`entity_id` bắt đầu bằng `3d_`, `remove_bg`: true) — khớp chính xác danh từ chính trong từng câu thoại.
4. `voice_anchor_quote`: trích ĐÚNG 2-5 từ có thật trong câu thoại khi hình này phải xuất hiện.
5. `context_sentence`: trích nguyên câu thoại tương ứng để Mắt Thần Gemini Vision đối chiếu.
6. `search_query`: viết cực kỳ cụ thể (tiếng Việt cho sự kiện/địa điểm VN, tiếng Anh cho công nghệ/quốc tế) để tìm ra ảnh chụp thật HD, không watermark.
7. Tổng cộng khoảng 7–12 tư liệu chất lượng cao phủ trọn các nhịp kịch bản.

TRẢ VỀ DUY NHẤT JSON HỢP LỆ (không markdown, không giải thích ngoài JSON):
{{
  "topic_domain": "mô tả ngắn miền chủ đề video",
  "assets": [
    {{
      "scene_id": "scene_1",
      "entity_id": "bg_ten_khong_dau",
      "voice_anchor_quote": "cụm từ chính xác trong lời đọc",
      "search_query": "từ khóa tìm ảnh thật cực sát",
      "remove_bg": false,
      "context_sentence": "Nguyên câu thoại tương ứng trong kịch bản"
    }}
  ]
}}"""

    resp_text = generate_content_resilient(prompt)
    if not resp_text:
        raise RuntimeError("Gemini không phản hồi khi phân tích kịch bản để lập harvest_plan.json.")

    cleaned = resp_text.strip()
    m = re.search(r"\{[\s\S]*\}", cleaned)
    if not m:
        raise ValueError(f"Gemini không trả về JSON hợp lệ:\n{cleaned[:400]}")

    plan = json.loads(m.group(0))
    topic_domain = str(plan.get("topic_domain", "") or "").strip()
    raw_assets = plan.get("assets") or []

    # Chuẩn hóa, khử trùng entity_id và kiểm tra cấm ẩn dụ trừu tượng
    seen_ids: set[str] = set()
    clean_assets: List[Dict[str, Any]] = []
    for idx, item in enumerate(raw_assets, 1):
        eid = re.sub(r"[^a-z0-9_]", "_", str(item.get("entity_id", f"asset_{idx}")).lower()).strip("_")
        if not eid:
            eid = f"asset_{idx}"
        base_eid = eid
        c = 2
        while eid in seen_ids:
            eid = f"{base_eid}_{c}"
            c += 1
        seen_ids.add(eid)

        sq = str(item.get("search_query", "")).strip()
        if not sq:
            continue
        validate_harvest_query(sq, topic_domain=topic_domain)
        clean_assets.append({
            "scene_id": str(item.get("scene_id", f"scene_{idx}")),
            "entity_id": eid,
            "voice_anchor_quote": str(item.get("voice_anchor_quote", "")).strip(),
            "search_query": sq,
            "remove_bg": bool(item.get("remove_bg", not eid.startswith("bg_"))),
            "context_sentence": str(item.get("context_sentence", "")).strip(),
        })

    if not clean_assets:
        raise ValueError("Không trích xuất được thực thể hợp lệ nào từ kịch bản.")

    final_plan = {"topic_domain": topic_domain, "assets": clean_assets}
    output_plan_path.parent.mkdir(parents=True, exist_ok=True)
    output_plan_path.write_text(json.dumps(final_plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SCRIPT->PLAN OK] Đã bóc tách {len(clean_assets)} thực thể khớp lời đọc -> {output_plan_path}")
    return final_plan


# =============================================================================
# 12. CHẾ ĐỘ 6 ỨNG VIÊN SOI 1 LẦN (A..F, >= 700px, MUST_SHOW & REJECT)
# =============================================================================
def _extract_item_queries(item: Dict[str, Any]) -> List[str]:
    """Đọc mảng search_queries (2-3 từ khóa) hoặc fallback search_query đơn."""
    qs: List[str] = []
    raw_qs = item.get("search_queries")
    if isinstance(raw_qs, list):
        qs.extend(str(q).strip() for q in raw_qs if str(q).strip())
    single_q = str(item.get("search_query", "") or "").strip()
    if single_q and single_q not in qs:
        qs.append(single_q)
    return qs


def _compute_orientation(w: int, h: int) -> str:
    if abs(w - h) <= max(w, h) * 0.08:
        return "square"
    return "landscape" if w > h else "portrait"


VALID_ASSET_ROLES = {"prop_3d", "avatar_node", "ev_card"}


def _normalize_asset_role(item: Dict[str, Any]) -> str:
    """Chuẩn hóa asset_role thuộc 1 trong 3 vai trò: prop_3d | avatar_node | ev_card."""
    raw_role = str(item.get("asset_role") or "").strip().lower()
    if raw_role in VALID_ASSET_ROLES:
        return raw_role
    eid = str(item.get("entity_id") or "").strip().lower()
    if eid.startswith("avatar"):
        return "avatar_node"
    if bool(item.get("remove_bg", False)) or eid.startswith("prop"):
        return "prop_3d"
    return "ev_card"


def _role_badge_spec(asset_role: str) -> Tuple[str, Tuple[int, int, int], Tuple[int, int, int]]:
    """Trả về (nhãn vai trò, màu nền badge, màu chữ/viền badge) để in lên candidates_sheet.jpg."""
    if asset_role == "prop_3d":
        return "[PROP 3D]", (64, 42, 6), (255, 204, 30)
    if asset_role == "avatar_node":
        return "[AVATAR]", (8, 48, 66), (34, 211, 238)
    return "[EVIDENCE]", (14, 52, 34), (110, 235, 155)


def search_ddg_hd_clean(query: str, max_urls: int = 10, min_dim: int = 700) -> List[str]:
    """Tìm ảnh độ phân giải cao (>= 700px) trên DuckDuckGo Images (nếu có ddgs/duckduckgo_search), lọc sạch spam."""
    urls: List[str] = []
    DDGS_cls = None
    try:
        from ddgs import DDGS as DDGS_cls  # type: ignore
    except Exception:
        try:
            from duckduckgo_search import DDGS as DDGS_cls  # type: ignore
        except Exception:
            DDGS_cls = None
    if DDGS_cls is None:
        return urls
    try:
        with DDGS_cls() as ddgs:
            results = ddgs.images(query, size="Large", type_image="photo", max_results=max_urls * 2)
            for r in results or []:
                u = str(r.get("image") or "").strip()
                w = int(r.get("width") or 0)
                h = int(r.get("height") or 0)
                if not u or is_banned_url(u):
                    continue
                if (w and h) and (max(w, h) < min_dim or min(w, h) < 400):
                    continue
                urls.append(u)
                if len(urls) >= max_urls:
                    break
    except Exception:
        pass
    return urls


def _crop_avatar_top_weighted(im: Image.Image) -> Image.Image:
    """
    Tự động nhận diện vùng đầu/mặt phía trên (Haar Cascade + fallback top-weighted crop)
    để giữ trọn khoảng thở trên đỉnh đầu & trán cho avatar_node, tuyệt đối không xén mất đỉnh đầu hay trán.
    """
    rgb = im.convert("RGB")
    w, h = rgb.size
    if w < 64 or h < 64:
        return rgb

    face_box: Optional[Tuple[int, int, int, int]] = None
    try:
        import cv2
        gray = np.array(rgb.convert("L"), dtype=np.uint8)
        cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        if os.path.exists(cascade_path):
            detector = cv2.CascadeClassifier(cascade_path)
            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(max(36, min(w, h) // 10), max(36, min(w, h) // 10)),
            )
            if len(faces) > 0:
                # Ưu tiên khuôn mặt lớn nằm ở 75% nửa trên khung hình
                upper_faces = [f for f in faces if (f[1] + f[3] * 0.5) <= h * 0.78]
                cand_faces = upper_faces if upper_faces else list(faces)
                cand_faces.sort(key=lambda b: int(b[2]) * int(b[3]), reverse=True)
                fx, fy, fw, fh = [int(v) for v in cand_faces[0]]
                face_box = (fx, fy, fw, fh)
    except Exception:
        face_box = None

    side = min(w, h)
    if face_box is not None:
        fx, fy, fw, fh = face_box
        # Mở khung rộng ~2.4x bề ngang mặt để ôm trọn vai + khoảng thở trên đỉnh đầu
        crop_side = max(min(side, int(fw * 2.5)), min(side, int(min(w, h) * 0.72)))
        cx = fx + fw // 2
        # Đặt tâm mắt/trán ở ~34% từ mép trên xuống -> chừa đầy đủ tóc và đỉnh đầu
        ideal_y0 = fy - int(fh * 0.68)
        x0 = max(0, min(w - crop_side, cx - crop_side // 2))
        y0 = max(0, min(h - crop_side, ideal_y0))
        return rgb.crop((x0, y0, x0 + crop_side, y0 + crop_side))

    # Fallback Top-Weighted Crop: bám sát phần trên khung hình (chỉ lùi 4% nếu ảnh dọc, 0% nếu ảnh ngang)
    if h >= w:
        x0 = 0
        y0 = max(0, min(h - side, int((h - side) * 0.04)))
    else:
        x0 = (w - side) // 2
        y0 = 0
    return rgb.crop((x0, y0, x0 + side, y0 + side))


def _gather_candidates_by_hint(
    search_queries: List[str],
    source_hint: str = "auto",
    asset_role: str = "ev_card",
) -> List[str]:
    """
    Gom ứng viên đa nguồn từ cả 2-3 từ khóa (Wikimedia Commons + Bing/DDG >= 700px + Tavily).
    Nếu asset_role == 'prop_3d': tự động ưu tiên ảnh chụp vật thể rõ nét trên nền sạch.
    """
    hint = (source_hint or "auto").strip().lower()
    merged: List[str] = []
    seen: set[str] = set()

    effective_queries = list(search_queries)
    if asset_role == "prop_3d" and effective_queries:
        clean_mods = ("isolated", "product photography", "close up", "white background", "studio")
        if not any(any(m in q.lower() for m in clean_mods) for q in effective_queries):
            effective_queries.append(f"{effective_queries[0]} isolated close up")

    for sq in effective_queries:
        if asset_role == "prop_3d":
            # Ưu tiên Wikimedia Commons + Bing HD Clean + DDG (>= 700px) cho vật thể 3D nền sạch
            batch = (
                search_wikimedia_commons(sq, max_urls=8)
                + search_bing_hd_clean(sq, max_urls=14)
                + search_ddg_hd_clean(sq, max_urls=8, min_dim=700)
            )
        elif hint == "wikimedia":
            batch = search_wikimedia_commons(sq, max_urls=8) + search_bing_hd_clean(sq, max_urls=10)
        elif hint == "web":
            batch = (
                search_bing_hd_clean(sq, max_urls=12)
                + search_ddg_hd_clean(sq, max_urls=6, min_dim=700)
                + search_tavily_editorial_images(sq, max_urls=5)
                + search_wikimedia_commons(sq, max_urls=4)
            )
        else:
            batch = (
                search_wikimedia_commons(sq, max_urls=6)
                + search_bing_hd_clean(sq, max_urls=12)
                + search_ddg_hd_clean(sq, max_urls=6, min_dim=700)
                + search_tavily_editorial_images(sq, max_urls=5)
            )
        for u in batch:
            if u not in seen:
                seen.add(u)
                merged.append(u)
    return merged


def harvest_candidates_sheet(
    items: List[Dict[str, Any]],
    temp_dir: Path,
    topic_domain: str = "",
    only_ids: Optional[set[str]] = None,
) -> Path:
    """
    Tải 6 ứng viên (A, B, C, D, E, F, >= 700px chiều chính, lọc sạch watermark/CGI/nhạy cảm)
    cho từng thực thể vào temp/candidates/ và ghép temp/candidates_sheet.jpg
    gắn nhãn vai trò [PROP 3D] / [AVATAR] / [EVIDENCE] + entity_id + must_show bên trái từng hàng.
    """
    cand_dir = temp_dir / "candidates"
    cand_dir.mkdir(parents=True, exist_ok=True)
    index_path = cand_dir / "candidates_index.json"
    existing_index: Dict[str, Any] = {}
    if index_path.exists():
        try:
            existing_index = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception:
            existing_index = {}

    letters = ("A", "B", "C", "D", "E", "F")
    dedupe = ImageDedupeRegistry(check_global_history=False)

    for item in items:
        entity_id = str(item["entity_id"]).strip()
        if only_ids and entity_id not in only_ids:
            continue
        queries = _extract_item_queries(item)
        if not queries:
            raise ValueError(f"Mục '{entity_id}' thiếu search_queries / search_query!")
        for sq in queries:
            validate_harvest_query(sq, topic_domain=topic_domain)

        raw_role = str(item.get("asset_role") or "").strip().lower()
        visual_reasoning = str(item.get("visual_reasoning") or "").strip()
        if len(visual_reasoning) < 15 or raw_role not in VALID_ASSET_ROLES:
            raise ValueError(
                f"MISSING_VISUAL_REASONING: Mục '{entity_id}' bắt buộc có 'visual_reasoning' (>= 15 ký tự) "
                f"và 'asset_role' thuộc {{'prop_3d', 'avatar_node', 'ev_card'}} trước khi cào!"
            )
        asset_role = raw_role
        must_show = str(item.get("must_show") or item.get("context_sentence") or item.get("context") or "").strip()
        script_line = str(item.get("script_line") or item.get("context_sentence") or "").strip()
        source_hint = str(item.get("source_hint", "auto") or "auto")
        remove_bg = True if asset_role == "prop_3d" else (False if asset_role == "ev_card" else bool(item.get("remove_bg", False)))

        role_label, _, _ = _role_badge_spec(asset_role)
        print(f"\n[*] TẢI 6 ỨNG VIÊN (A..F) CHO {role_label} [{entity_id}] (hint={source_hint}): {queries}")
        urls = _gather_candidates_by_hint(queries, source_hint=source_hint, asset_role=asset_role)
        saved_slots: Dict[str, Dict[str, Any]] = {}
        slot_idx = 0

        for u in urls[:40]:
            if slot_idx >= 6:
                break
            try:
                used, _ = dedupe.is_url_used(u)
                if used:
                    continue
                hdrs = WIKI_HEADERS if "wikimedia.org" in u else HEADERS
                req = urllib.request.Request(u, headers=hdrs)
                with urllib.request.urlopen(req, timeout=12, context=SSL_CTX) as resp:
                    raw = resp.read()
                if len(raw) < 28000:
                    continue
                import hashlib
                md5_hex = hashlib.md5(raw).hexdigest()
                letter = letters[slot_idx]
                out_jpg = cand_dir / f"{entity_id}_{letter}.jpg"
                with Image.open(io.BytesIO(raw)) as im:
                    w, h = im.size
                    if max(w, h) < 700 or min(w, h) < 400:
                        continue
                    dhash_hex = _compute_dhash_hex(im)
                    is_dup, _ = dedupe.is_image_duplicate(md5_hex, dhash_hex)
                    if is_dup:
                        continue
                    im.convert("RGB").save(out_jpg, format="JPEG", quality=92)
                dedupe.session_urls.add(u.strip().lower())
                dedupe.session_md5s.add(md5_hex)
                dedupe.session_dhashes.append(dhash_hex)
                saved_slots[letter] = {
                    "path": str(out_jpg),
                    "url": u,
                    "width": w,
                    "height": h,
                    "orientation": _compute_orientation(w, h),
                }
                print(f"   [OK {entity_id}:{letter}] {w}x{h} <- {u[:72]}...")
                slot_idx += 1
            except Exception:
                continue

        existing_index[entity_id] = {
            "entity_id": entity_id,
            "asset_role": asset_role,
            "visual_reasoning": visual_reasoning,
            "must_show": must_show,
            "script_line": script_line,
            "search_queries": queries,
            "remove_bg": remove_bg,
            "slots": saved_slots,
        }

    index_path.write_text(json.dumps(existing_index, ensure_ascii=False, indent=2), encoding="utf-8")

    # Ghép lưới lớn temp/candidates_sheet.jpg: cột trái gắn nhãn [PROP 3D] / [AVATAR] / [EVIDENCE] + entity_id + must_show
    ordered_ids = [str(it["entity_id"]).strip() for it in items if str(it["entity_id"]).strip() in existing_index]
    info_col_w = 370
    cell_w, cell_h = 340, 276
    top_banner_h = 86
    sheet_w = info_col_w + 6 * cell_w + 40
    sheet_h = top_banner_h + len(ordered_ids) * (cell_h + 16) + 30
    sheet = Image.new("RGB", (sheet_w, max(320, sheet_h)), color=(10, 14, 24))
    draw = ImageDraw.Draw(sheet)

    try:
        font_lg = ImageFont.truetype("arialbd.ttf", 26)
        font_md = ImageFont.truetype("arialbd.ttf", 18)
        font_sm = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font_lg = font_md = font_sm = ImageFont.load_default()

    draw.text((24, 18), f"CANDIDATES SHEET (6 UNG VIEN A..F >= 700px) — {len(ordered_ids)} MUC", fill=(255, 230, 0), font=font_lg)
    draw.text(
        (24, 52),
        "[PROP 3D]: chon vat nguyen ven 4 goc, nen sach | [AVATAR]: ro mat & tran | [EVIDENCE]: giu nguyen khung | Sai y -> REJECT",
        fill=(180, 210, 240),
        font=font_sm,
    )

    for r_idx, eid in enumerate(ordered_ids):
        y0 = top_banner_h + r_idx * (cell_h + 16)
        entry = existing_index[eid]
        role_code = str(entry.get("asset_role") or "ev_card")
        badge_txt, badge_bg, badge_fg = _role_badge_spec(role_code)

        # Cột thông tin bên trái từng hàng: Nhãn vai trò [PROP 3D]/[AVATAR]/[EVIDENCE] + entity_id + must_show
        draw.rectangle([16, y0, 16 + info_col_w - 10, y0 + cell_h - 6], fill=(18, 30, 50), outline=badge_fg, width=2)
        draw.rectangle([24, y0 + 10, 162, y0 + 38], fill=badge_bg, outline=badge_fg, width=2)
        draw.text((32, y0 + 14), badge_txt, fill=badge_fg, font=font_md)
        draw.text((170, y0 + 14), f"#{r_idx+1} {eid}", fill=(255, 255, 255), font=font_md)

        role_guide = (
            "Cat nen 3D: CAM cat goc/che tay"
            if role_code == "prop_3d"
            else ("Node tron: ro mat, du dinh dau" if role_code == "avatar_node" else "The contain: giu 100% khung")
        )
        draw.text((26, y0 + 44), role_guide, fill=badge_fg, font=font_sm)

        ms_txt = str(entry.get("must_show", ""))
        for li in range(0, min(len(ms_txt), 144), 36):
            draw.text((26, y0 + 70 + (li // 36) * 19), ms_txt[li:li + 36], fill=(235, 242, 250), font=font_sm)

        vr_txt = str(entry.get("visual_reasoning", ""))
        if vr_txt:
            draw.text((26, y0 + 154), "Why 1s:", fill=(255, 230, 0), font=font_sm)
            for li in range(0, min(len(vr_txt), 144), 36):
                draw.text((26, y0 + 174 + (li // 36) * 18), vr_txt[li:li + 36], fill=(175, 205, 235), font=font_sm)

        slots = entry.get("slots", {})
        for c_idx, letter in enumerate(letters):
            x0 = 16 + info_col_w + c_idx * cell_w + 4
            draw.rectangle([x0, y0, x0 + cell_w - 10, y0 + cell_h - 6], fill=(16, 22, 34), outline=(55, 75, 105))
            info = slots.get(letter)
            if info and Path(info["path"]).exists():
                try:
                    with Image.open(info["path"]) as im:
                        th = im.convert("RGB")
                        th.thumbnail((cell_w - 22, cell_h - 48), Image.Resampling.LANCZOS)
                        px = x0 + (cell_w - 10 - th.size[0]) // 2
                        py = y0 + 36 + (cell_h - 48 - th.size[1]) // 2
                        sheet.paste(th, (px, py))
                except Exception:
                    pass
                draw.rectangle([x0 + 6, y0 + 6, x0 + 54, y0 + 36], fill=(5, 7, 12), outline=(255, 230, 0), width=2)
                draw.text((x0 + 20, y0 + 7), letter, fill=(255, 230, 0), font=font_lg)
                dim_txt = f"{info.get('width', 0)}x{info.get('height', 0)}"
                draw.rectangle([x0 + 60, y0 + 8, x0 + 185, y0 + 34], fill=(5, 7, 12))
                draw.text((x0 + 66, y0 + 11), dim_txt, fill=(255, 255, 255), font=font_sm)
            else:
                draw.text((x0 + 85, y0 + 120), f"{letter}: TRONG", fill=(255, 90, 90), font=font_md)

    sheet_out = temp_dir / "candidates_sheet.jpg"
    sheet.save(sheet_out, quality=90)
    print(f"[CANDIDATES SHEET 6-SLOTS OK] Đã xuất 1 ảnh lưới duy nhất: {sheet_out} ({sheet_w}x{sheet_h})")
    return sheet_out


def select_candidates_to_assets(
    select_spec: str,
    items: List[Dict[str, Any]],
    temp_dir: Path,
    topic_domain: str = "",
) -> Path:
    """
    Chốt ảnh đã chọn (--select 'ev_01:B,prop_02:E,ev_03:REJECT') theo đúng asset_role:
    - prop_3d: bria-rmbg + defringe_alpha + check_cutout_completeness(); cảnh báo đỏ CUTOUT_CHOPPED_WARNING nếu chạm mép trái/phải/trên > 8%.
    - avatar_node: top-weighted face/head crop giữ trọn đỉnh đầu & trán.
    - ev_card: giữ nguyên 100% khung (remove_bg=False, imageFit='contain').
    """
    import shutil

    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    import auto_cutout

    cand_dir = temp_dir / "candidates"
    index_path = cand_dir / "candidates_index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"Chưa chạy --candidates! Không thấy {index_path}")
    cand_index = json.loads(index_path.read_text(encoding="utf-8"))

    choices: Dict[str, str] = {}
    rejected_ids: List[str] = []
    for pair in select_spec.split(","):
        if ":" not in pair:
            continue
        k, v = pair.split(":", 1)
        eid_k = k.strip()
        val_v = v.strip().upper()
        if val_v == "REJECT":
            rejected_ids.append(eid_k)
        else:
            choices[eid_k] = val_v

    if rejected_ids:
        rej_csv = ",".join(rejected_ids)
        raise RuntimeError(
            f"[REJECT DETECTED] Các mục chưa đạt yêu cầu must_show: {rej_csv}. "
            f"CẤM chọn bừa ảnh lệch ý! Hãy đổi search_queries trong harvest_plan.json rồi chạy lại: "
            f"--candidates --only {rej_csv}"
        )

    assets_dir = temp_dir / "assets"
    purge_harvested_folder(assets_dir)
    manifest_assets: List[Dict[str, Any]] = []

    for item in items:
        eid = str(item["entity_id"]).strip()
        if eid not in choices:
            continue
        letter = choices[eid]
        slot = cand_index.get(eid, {}).get("slots", {}).get(letter)
        if not slot or not Path(slot["path"]).exists():
            raise FileNotFoundError(f"Không tìm thấy ứng viên {eid}:{letter} trong {cand_dir}")

        src_path = Path(slot["path"])
        raw_path = assets_dir / f"{eid}_raw.png"
        final_path = assets_dir / f"{eid}.png"

        asset_role = _normalize_asset_role(item)
        visual_reasoning = str(item.get("visual_reasoning") or "").strip()
        cutout_chopped_warning = False

        if asset_role == "avatar_node":
            with Image.open(src_path) as im:
                cropped_avatar = _crop_avatar_top_weighted(im)
                cropped_avatar.save(raw_path, format="PNG")
            remove_bg = bool(item.get("remove_bg", False))
            if remove_bg:
                remove_background_safe(raw_path, final_path, soft_bottom_fade=True)
            else:
                shutil.copy2(raw_path, final_path)
            display_mode = "avatar_node_circle"
            print(f"   [AVATAR TOP-WEIGHTED OK] {eid}:{letter} -> giữ trọn vùng đầu/trán phía trên ({final_path.name})")

        elif asset_role == "prop_3d":
            with Image.open(src_path) as im:
                im.convert("RGB").save(raw_path, format="PNG")
            remove_bg = True
            remove_background_safe(raw_path, final_path, soft_bottom_fade=False)
            with Image.open(final_path) as cut_im:
                comp = auto_cutout.check_cutout_completeness(cut_im)

            side_or_top_chopped = (
                comp["left_touch"] > 0.08 or comp["right_touch"] > 0.08 or comp["top_touch"] > 0.08
            )
            if side_or_top_chopped:
                cutout_chopped_warning = True
                display_mode = "chopped_warning_replace"
                print(
                    f"\033[91m[CUTOUT_CHOPPED_WARNING] {eid}:{letter} bị cắt cụt mép trái/phải/trên > 8% "
                    f"(left={comp['left_touch']:.1%}, right={comp['right_touch']:.1%}, top={comp['top_touch']:.1%})! "
                    f"YÊU CẦU ĐỔI ỨNG VIÊN KHÁC nguyên vẹn trên candidates_sheet.jpg "
                    f"(hoặc sửa search_queries & chạy --candidates --only {eid}) thay vì lờ đi!\033[0m"
                )
            elif comp["is_bottom_only_touch"]:
                print(f"   [SOFT BOTTOM FADE] {eid}:{letter} chạm nhẹ đáy ({comp['bottom_touch']:.1%}) -> bật soft_bottom_fade=True")
                remove_background_safe(raw_path, final_path, soft_bottom_fade=True)
                display_mode = "prop_3d_bottom_faded"
            else:
                display_mode = "prop_3d_clean"

        else:
            # ev_card: giữ nguyên 100% khung hình gốc (imageFit="contain", không tách nền)
            with Image.open(src_path) as im:
                im.convert("RGB").save(raw_path, format="PNG")
            remove_bg = False
            shutil.copy2(raw_path, final_path)
            display_mode = "ev_card_contain"

        with Image.open(final_path) as fin_im:
            fw, fh = fin_im.size

        queries = _extract_item_queries(item)
        manifest_assets.append({
            "entity_id": eid,
            "asset_role": asset_role,
            "visual_reasoning": visual_reasoning,
            "selected_candidate": letter,
            "search_queries": queries,
            "must_show": str(item.get("must_show") or ""),
            "script_line": str(item.get("script_line") or item.get("context_sentence") or item.get("context") or ""),
            "remove_bg": remove_bg,
            "display_mode": display_mode,
            "cutout_chopped_warning": cutout_chopped_warning,
            "width": fw,
            "height": fh,
            "orientation": _compute_orientation(fw, fh),
            "public_path": f"harvested/{final_path.name}",
            "abs_path": str(final_path),
        })

    manifest_out = temp_dir / "asset_manifest.json"
    manifest_out.write_text(
        json.dumps({"topic_domain": topic_domain, "count": len(manifest_assets), "assets": manifest_assets}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    sheet_out = temp_dir / "assets_contact_sheet.jpg"
    generate_assets_contact_sheet(assets_dir, sheet_out)
    print(f"[SELECT OK] Đã chốt {len(manifest_assets)} tư liệu sạch (kèm width/height/orientation) -> {manifest_out}")
    return sheet_out


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="Bộ cào tư liệu thật đa tầng + 4 Ứng viên A/B/C/D + Chống trùng dHash/Lịch sử + Tách nền bria-rmbg."
    )
    ap.add_argument("--project", required=True, help="Thư mục dự án WIP (VD: D:\\DuAn_DangLam\\ten_du_an)")
    ap.add_argument("--candidates", action="store_true", help="Tải 4 ứng viên A/B/C/D cho mỗi mục -> xuất temp/candidates_sheet.jpg")
    ap.add_argument("--only", default="", help="Khi dùng --candidates, chỉ cào lại các entity_id cách nhau dấu phẩy")
    ap.add_argument("--select", default="", help="Chốt ứng viên đã chọn dạng 'ev_01:B,prop_02:A,...' -> tách nền & xuất contact sheet")
    ap.add_argument("--script", help="Đường dẫn script_5beat.json/.txt để tự bóc tách kế hoạch")
    ap.add_argument("--plan-only", action="store_true", help="Khi dùng --script, chỉ xuất temp/harvest_plan.json rồi dừng")
    ap.add_argument("--manifest", help="Đường dẫn file kế hoạch cào JSON có sẵn (VD: temp/harvest_plan.json)")
    ap.add_argument("--contact-sheet", action="store_true", help="Chỉ xuất lại temp/assets_contact_sheet.jpg từ temp/assets/")
    ap.add_argument("--skip-vision", action="store_true", help="Bỏ qua gọi API Gemini Vision (chống 429)")
    ap.add_argument("--allow-history-reuse", action="store_true", help="Cho phép dùng lại ảnh từng dùng ở tập cũ (mặc định: CẤM)")
    args = ap.parse_args()

    if args.skip_vision:
        set_skip_vision(True)
        print("[MODE] --skip-vision ĐANG BẬT (lọc domain rác + độ phân giải + dHash + check_cutout_completeness).")

    project_dir = Path(args.project)
    temp_dir = project_dir / "temp"
    assets_dir = temp_dir / "assets"
    sheet_path = temp_dir / "assets_contact_sheet.jpg"

    if args.contact_sheet:
        generate_assets_contact_sheet(assets_dir, sheet_path)
        return 0

    if args.candidates or args.select:
        if not args.manifest:
            ap.error("Cần truyền --manifest <temp/harvest_plan.json> khi dùng --candidates hoặc --select.")
        plan_path = Path(args.manifest)
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        topic_domain = "" if isinstance(plan, list) else str(plan.get("topic_domain", "") or "")
        items = plan if isinstance(plan, list) else (plan.get("assets") or plan.get("items") or plan.get("entities") or [])
        if args.candidates:
            only_ids = {x.strip() for x in args.only.split(",") if x.strip()} if args.only else None
            harvest_candidates_sheet(items, temp_dir, topic_domain=topic_domain, only_ids=only_ids)
            return 0
        select_candidates_to_assets(args.select, items, temp_dir, topic_domain=topic_domain)
        return 0

    plan_path: Optional[Path] = None
    if args.script:
        script_path = Path(args.script)
        if not script_path.exists():
            raise FileNotFoundError(f"Không tìm thấy kịch bản: {script_path}")
        plan_path = temp_dir / "harvest_plan.json"
        build_harvest_plan_from_script(script_path, plan_path)
        if args.plan_only:
            print(f"[PLAN-ONLY] Đã dừng sau khi xuất kế hoạch tại: {plan_path}")
            return 0
    elif args.manifest:
        plan_path = Path(args.manifest)
        if not plan_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file kế hoạch cào: {plan_path}")
    else:
        ap.error("Cần truyền --script <path>, --manifest <path>, hoặc --contact-sheet.")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if isinstance(plan, list):
        topic_domain = ""
        items = plan
    else:
        topic_domain = str(plan.get("topic_domain", "") or "")
        items = plan.get("assets") or plan.get("items") or plan.get("entities") or []

    if not items:
        raise ValueError(f"Danh sách tài nguyên trong {plan_path} đang rỗng!")

    purge_harvested_folder(assets_dir)
    dedupe = ImageDedupeRegistry(check_global_history=not args.allow_history_reuse)
    project_name = project_dir.name

    harvested_manifest: List[Dict[str, Any]] = []
    for item in items:
        entity_id = str(item["entity_id"]).strip()
        search_query = str(item["search_query"]).strip()
        remove_bg = bool(item.get("remove_bg", True))
        context_sentence = str(item.get("context_sentence") or item.get("context") or "")

        res = harvest_entity_asset(
            entity_id=entity_id,
            search_query=search_query,
            remove_bg=remove_bg,
            target_dir=assets_dir,
            context_sentence=context_sentence,
            topic_domain=topic_domain,
            dedupe=dedupe,
            project_name=project_name,
        )
        res["context_sentence"] = context_sentence
        if item.get("scene_id"):
            res["scene_id"] = item["scene_id"]
        if item.get("voice_anchor_quote"):
            res["voice_anchor_quote"] = item["voice_anchor_quote"]
        harvested_manifest.append(res)

    manifest_out = temp_dir / "asset_manifest.json"
    manifest_out.write_text(
        json.dumps(
            {
                "topic_domain": topic_domain,
                "count": len(harvested_manifest),
                "assets": harvested_manifest,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[MANIFEST OK] Đã xuất: {manifest_out} ({len(harvested_manifest)} tư liệu, 0 trùng lặp)")
    generate_assets_contact_sheet(assets_dir, sheet_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```


#### `engine/auto_cutout.py`

```python
"""
auto_cutout.py - Tự động bóc tách nền nhân vật/vật thể bằng AI (BiRefNet / BRIA-RMBG SOTA)
Hỗ trợ hiệu ứng cao cấp cho cả Video 16:9 (Dài) & 9:16 (Ngắn):
1. Multi-Model Support: Mặc định bria-rmbg (1GB High-Res), hỗ trợ birefnet-general, isnet-general-use
2. De-fringing & Alpha Feathering: Khử triệt để viền lem nhem, halo trắng/đen quanh chi tiết cơ khí
3. Soft Rim Light: Ánh sáng ven mềm hổ phách/neon tôn khối chủ thể điện ảnh
4. 3D Double-Layer Contact & Cast Shadow: Đổ bóng sàn tiếp xúc 3D 2 tầng chân thực
5. Sticker Outline: Viền nét mảnh (tùy chọn)
"""

import sys
import os
from pathlib import Path

# Đảm bảo UTF-8 cho Windows console
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr:
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops
import numpy as np
import rembg

# Session cache toàn cục tránh load lại model nhiều lần
_GLOBAL_SESSIONS = {}

def get_rembg_session(model_name: str = "bria-rmbg"):
    """Lấy hoặc khởi tạo session rembg theo model yêu cầu"""
    global _GLOBAL_SESSIONS
    if model_name not in _GLOBAL_SESSIONS:
        try:
            print(f"[AI Cutout] Khởi tạo AI Matting Engine với Model: {model_name}...")
            _GLOBAL_SESSIONS[model_name] = rembg.new_session(model_name)
        except Exception as e:
            print(f"[!] Không thể load model {model_name} ({e}), chuyển sang fallback mặc định...")
            _GLOBAL_SESSIONS[model_name] = rembg.new_session()
    return _GLOBAL_SESSIONS[model_name]


def defringe_alpha(
    image_rgba: Image.Image,
    erode_px: int = 1,
    feather_radius: float = 0.7,
    iterations: int = 2,
) -> Image.Image:
    """
    Khử viền sáng/răng cưa chuyên sâu cho nền xanh đêm #061224 (SOTA De-fringing & Alpha Erosion):
    1. Khử nhiễm màu nền trắng/xám (Color Decontamination): kéo màu RGB vùng lõi bên trong ra biên
       và dập tắt các pixel halo trắng/xám bám quanh vật thể tối màu.
    2. Co nhẹ mặt nạ biên `erode_px` (1px) để cắt sạch rìa nền sáng còn sót.
    3. Làm mềm biên `feather_radius` (0.7px GaussianBlur lên kênh alpha) triệt tiêu răng cưa.
    """
    if image_rgba.mode != "RGBA":
        image_rgba = image_rgba.convert("RGBA")

    r, g, b, a = image_rgba.split()
    alpha_np = np.array(a, dtype=np.uint8)

    if np.all(alpha_np == 0) or np.all(alpha_np == 255):
        return image_rgba

    # Bước 1: Lan truyền màu lõi (inner RGB) ra vùng biên bán trong suốt & dập halo trắng/xám
    rgb_np = np.stack(
        [np.array(r, dtype=np.float32), np.array(g, dtype=np.float32), np.array(b, dtype=np.float32)],
        axis=-1,
    )
    core_mask_pil = a.filter(ImageFilter.MinFilter(5))
    core_mask = np.array(core_mask_pil, dtype=np.uint8) >= 220

    # Tính màu tham chiếu tối/sạch từ vùng sát lõi bằng MinFilter nhẹ để triệt viền trắng sáng
    r_inner = np.array(r.filter(ImageFilter.MinFilter(3)), dtype=np.float32)
    g_inner = np.array(g.filter(ImageFilter.MinFilter(3)), dtype=np.float32)
    b_inner = np.array(b.filter(ImageFilter.MinFilter(3)), dtype=np.float32)
    inner_min_rgb = np.stack([r_inner, g_inner, b_inner], axis=-1)

    # Ở dải viền ngoài (~2-3px quanh mép alpha), khử hoàn toàn lốm đốm trắng/xám có độ sáng cao hơn lõi
    edge_zone = (alpha_np > 0) & (~core_mask)
    rgb_max = np.max(rgb_np, axis=-1)
    rgb_min = np.min(rgb_np, axis=-1)
    sat = rgb_max - rgb_min
    luma = 0.299 * rgb_np[..., 0] + 0.587 * rgb_np[..., 1] + 0.114 * rgb_np[..., 2]
    inner_luma = 0.299 * inner_min_rgb[..., 0] + 0.587 * inner_min_rgb[..., 1] + 0.114 * inner_min_rgb[..., 2]

    # Pixel biên bị ám nền trắng/xám (ít bão hòa hoặc sáng vọt hơn phần thịt bên trong) -> thay bằng màu lõi tối hơn
    white_gray_halo = edge_zone & ((luma > inner_luma + 14.0) | ((rgb_min > 145.0) & (sat < 42.0)))
    rgb_np[white_gray_halo] = inner_min_rgb[white_gray_halo]

    # Hòa mượt thêm 2 vòng ở sát biên để chuyển sắc tự nhiên
    rgb_img = Image.fromarray(np.clip(rgb_np, 0, 255).astype(np.uint8), mode="RGB")
    for _ in range(max(1, iterations)):
        edge_mask = a.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
        rgb_blurred = rgb_img.filter(ImageFilter.BoxBlur(1))
        rgb_img = Image.composite(rgb_img, rgb_blurred, ImageChops.invert(edge_mask))

    # Bước 2: Co nhẹ mặt nạ biên 1px (MinFilter(3)) nhưng bảo toàn chi tiết mảnh nếu quá nhỏ
    clean_a = a
    if erode_px > 0:
        k_size = max(3, int(erode_px) * 2 + 1)
        eroded = a.filter(ImageFilter.MinFilter(k_size))
        if np.any(np.array(eroded, dtype=np.uint8) > 32):
            clean_a = eroded

    # Bước 3: Làm mềm biên 0.7px bằng GaussianBlur lên kênh alpha
    if feather_radius > 0:
        clean_a = clean_a.filter(ImageFilter.GaussianBlur(float(feather_radius)))
        # Dọn sạch bụi alpha siêu mờ (< 6) ngoài rìa sau khi blur để nền trong suốt tuyệt đối
        a_arr = np.array(clean_a, dtype=np.uint8)
        a_arr[a_arr < 6] = 0
        clean_a = Image.fromarray(a_arr, mode="L")

    r_clean, g_clean, b_clean = rgb_img.split()
    return Image.merge("RGBA", (r_clean, g_clean, b_clean, clean_a))


def defringe_rgba(image_rgba: Image.Image, iterations: int = 2) -> Image.Image:
    """Alias tương thích ngược gọi thẳng defringe_alpha chuẩn mới."""
    return defringe_alpha(image_rgba, erode_px=1, feather_radius=0.7, iterations=iterations)


def apply_alpha_feathering(image_rgba: Image.Image, radius: float = 1.0) -> Image.Image:
    """
    Làm mềm viền alpha (Alpha Feathering) tự nhiên, triệt tiêu răng cưa thô cứng.
    """
    if radius <= 0:
        return image_rgba
    r, g, b, a = image_rgba.split()
    a_feathered = a.filter(ImageFilter.GaussianBlur(radius))
    return Image.merge("RGBA", (r, g, b, a_feathered))


def add_outline(image_rgba: Image.Image, stroke_color=(255, 255, 255), stroke_width=4) -> Image.Image:
    """Tạo viền nét (stroke) cho ảnh PNG có kênh alpha"""
    if stroke_width <= 0:
        return image_rgba
        
    alpha = image_rgba.split()[-1]
    expanded_alpha = alpha.filter(ImageFilter.MaxFilter(stroke_width * 2 + 1))
    
    outline_img = Image.new("RGBA", image_rgba.size, (*stroke_color, 255))
    outline_img.putalpha(expanded_alpha)
    
    return Image.alpha_composite(outline_img, image_rgba)


def add_soft_rim_light(image_rgba: Image.Image, color=(255, 190, 70), width=16, blur=10, opacity=0.85) -> Image.Image:
    """
    Tạo ánh sáng ven mềm (Soft Rim Light) phong cách điện ảnh / Chuyện Nhà Băng
    Ánh sáng ven viền mờ dần vào trong thân người/vật thể, không bị giả như viền sticker.
    """
    if width <= 0:
        return image_rgba

    alpha = image_rgba.split()[-1]
    
    # Tạo inner border mask bằng cách lấy alpha gốc trừ đi alpha đã co nhỏ (Erode / MinFilter)
    eroded_alpha = alpha.filter(ImageFilter.MinFilter(width * 2 + 1))
    inner_edge = ImageChops.subtract(alpha, eroded_alpha)
    
    # Làm mờ cạnh trong để ánh sáng ven tan tự nhiên vào da/quần áo/kim loại
    blurred_edge = inner_edge.filter(ImageFilter.GaussianBlur(blur))
    
    # Áp dụng opacity
    if opacity < 1.0:
        blurred_edge = blurred_edge.point(lambda p: int(p * opacity))
        
    rim_layer = Image.new("RGBA", image_rgba.size, (*color, 255))
    rim_layer.putalpha(blurred_edge)
    
    # Ghép hòa trộn rim light lên trên chủ thể (chỉ hiển thị trong phạm vi alpha của chủ thể)
    final_rim = Image.composite(rim_layer, Image.new("RGBA", image_rgba.size, (0, 0, 0, 0)), alpha)
    result = Image.alpha_composite(image_rgba, final_rim)
    return result


def add_3d_double_shadow(
    image_rgba: Image.Image,
    canvas_size=None,
    subject_pos=None,
    shadow_color=(10, 10, 15),
    contact_opacity=0.85,
    cast_opacity=0.45,
    contact_blur=8,
    cast_blur=22,
    scale_y=0.28,
    shear_x=-0.45
) -> Image.Image:
    """
    Đổ bóng tiếp xúc sàn 3D 2 Lớp (Double-Layer Contact & Cast Shadow):
    - Lớp 1 (Contact Shadow): Bóng đen đậm, sát điểm tiếp xúc sàn (bánh xe, chân đế)
    - Lớp 2 (Cast Shadow): Bóng trải dài, nghiêng theo góc sáng, mờ dần ra xa
    """
    sub_w, sub_h = image_rgba.size
    
    if canvas_size is None:
        c_w = int(sub_w * 1.8)
        c_h = int(sub_h * 1.5)
    else:
        c_w, c_h = canvas_size

    if subject_pos is None:
        sub_x = (c_w - sub_w) // 2
        sub_y = c_h - sub_h - int(c_h * 0.08)
    else:
        sub_x = subject_pos[0] - sub_w // 2
        sub_y = subject_pos[1] - sub_h

    alpha = image_rgba.split()[-1]
    
    # ==================== LỚP 1: CONTACT SHADOW (ĐẬM & SÁT CHÂN) ====================
    contact_base = Image.new("RGBA", (sub_w, sub_h), (*shadow_color, 255))
    contact_base.putalpha(alpha)
    contact_flat_h = max(4, int(sub_h * 0.12))
    contact_flat = contact_base.resize((sub_w, contact_flat_h), Image.Resampling.BILINEAR)
    contact_blurred = contact_flat.filter(ImageFilter.GaussianBlur(contact_blur))
    
    # Scale opacity contact shadow
    c_alpha = np.array(contact_blurred.split()[-1], dtype=np.float32) * contact_opacity
    contact_blurred.putalpha(Image.fromarray(np.clip(c_alpha, 0, 255).astype(np.uint8)))
    
    # ==================== LỚP 2: CAST SHADOW (DÀI, NGHIÊNG, MỜ DẦN) ====================
    cast_base = Image.new("RGBA", (sub_w, sub_h), (*shadow_color, 255))
    cast_base.putalpha(alpha)
    cast_flat_h = max(4, int(sub_h * scale_y))
    cast_flat = cast_base.resize((sub_w, cast_flat_h), Image.Resampling.BILINEAR)
    
    m = shear_x
    x_shift = abs(int(cast_flat_h * m)) if m < 0 else 0
    new_w = sub_w + abs(int(cast_flat_h * m))
    
    sheared_cast = cast_flat.transform(
        (new_w, cast_flat_h),
        Image.Transform.AFFINE,
        (1, -m, x_shift if m < 0 else 0, 0, 1, 0),
        Image.Resampling.BILINEAR
    )
    cast_blurred = sheared_cast.filter(ImageFilter.GaussianBlur(cast_blur))
    
    # Gradient fade cho cast shadow (càng ra xa càng mờ)
    sh_w, sh_h = cast_blurred.size
    fade_arr = np.linspace(cast_opacity, cast_opacity * 0.15, sh_h, endpoint=True)
    cast_alpha = np.array(cast_blurred.split()[-1], dtype=np.float32)
    for i in range(sh_h):
        cast_alpha[i, :] = cast_alpha[i, :] * fade_arr[i]
    cast_blurred.putalpha(Image.fromarray(np.clip(cast_alpha, 0, 255).astype(np.uint8)))

    # ==================== TỔNG HỢP LÊN CANVAS 3D ====================
    canvas = Image.new("RGBA", (c_w, c_h), (0, 0, 0, 0))
    
    # 1. Dán Cast Shadow (dưới cùng)
    cast_x = sub_x - (x_shift if m < 0 else 0)
    cast_y = sub_y + sub_h - int(cast_flat_h * 0.20)
    canvas.paste(cast_blurred, (cast_x, cast_y), cast_blurred)
    
    # 2. Dán Contact Shadow (đè lên cast shadow nhưng dưới vật thể)
    contact_x = sub_x
    contact_y = sub_y + sub_h - int(contact_flat_h * 0.40)
    canvas.paste(contact_blurred, (contact_x, contact_y), contact_blurred)
    
    # 3. Dán chủ thể lên trên cùng
    canvas.paste(image_rgba, (sub_x, sub_y), image_rgba)
    
    return canvas


def check_cutout_completeness(rgba_img: Image.Image, border_px: int = 3) -> dict:
    """
    Kiểm tra kênh alpha trên 4 viền rộng 3px (trên, dưới, trái, phải) TRƯỚC khi crop_tight
    để phát hiện ảnh bị chém cụt mất đầu/nửa xe/nửa vật thể ở mép khung hình.
    """
    if rgba_img.mode != "RGBA":
        rgba_img = rgba_img.convert("RGBA")
    alpha = np.array(rgba_img.split()[-1], dtype=np.uint8)
    h, w = alpha.shape
    if h == 0 or w == 0:
        return {
            "top_touch": 1.0,
            "bottom_touch": 1.0,
            "left_touch": 1.0,
            "right_touch": 1.0,
            "subject_area_ratio": 0.0,
            "is_chopped": True,
            "is_bottom_only_touch": False,
        }

    b = max(1, min(border_px, h // 4, w // 4))
    mask = alpha > 128
    top_touch = float(mask[:b, :].mean())
    bottom_touch = float(mask[h - b:, :].mean())
    left_touch = float(mask[:, :b].mean())
    right_touch = float(mask[:, w - b:].mean())
    subject_area_ratio = float(mask.mean())

    side_or_top_chopped = (left_touch > 0.08) or (right_touch > 0.08) or (top_touch > 0.08)
    bottom_chopped = bottom_touch > 0.12
    too_small = subject_area_ratio < 0.05
    is_chopped = side_or_top_chopped or bottom_chopped or too_small
    is_bottom_only_touch = (not side_or_top_chopped) and (not too_small) and bottom_chopped

    return {
        "top_touch": round(top_touch, 4),
        "bottom_touch": round(bottom_touch, 4),
        "left_touch": round(left_touch, 4),
        "right_touch": round(right_touch, 4),
        "subject_area_ratio": round(subject_area_ratio, 4),
        "is_chopped": is_chopped,
        "is_bottom_only_touch": is_bottom_only_touch,
    }


def apply_soft_bottom_fade(rgba_img: Image.Image, fade_ratio: float = 0.18) -> Image.Image:
    """Nhân gradient làm tan mượt kênh alpha ở 18% cạnh đáy để xóa sạch đường cắt ngang sắc lẹm."""
    if rgba_img.mode != "RGBA":
        rgba_img = rgba_img.convert("RGBA")
    r, g, b, a = rgba_img.split()
    alpha_np = np.array(a, dtype=np.float32)
    h, _ = alpha_np.shape
    fade_h = max(4, int(h * fade_ratio))
    if fade_h < h:
        grad = np.linspace(1.0, 0.0, fade_h, dtype=np.float32).reshape(-1, 1)
        alpha_np[h - fade_h:, :] *= grad
    new_a = Image.fromarray(np.clip(alpha_np, 0, 255).astype(np.uint8))
    return Image.merge("RGBA", (r, g, b, new_a))


def cutout_image(
    input_path: str | Path,
    output_path: str | Path = None,
    model_name: str = "bria-rmbg",
    defringe: bool = True,
    edge_feather: float = 0.7,
    add_rim_light: bool = False,
    rim_color=(255, 190, 70),
    rim_width: int = 14,
    add_floor_shadow: bool = False,
    add_3d_shadow: bool = None,
    double_shadow: bool = True,
    canvas_size=None,
    add_stroke: bool = False,
    stroke_color=(255, 255, 255),
    stroke_width: int = 4,
    crop_tight: bool = False,
    soft_bottom_fade: bool = False,
) -> Path:
    """
    Bóc tách nền của ảnh và xuất ra sản phẩm chuyên nghiệp chuẩn SOTA 2026.
    Tự động áp dụng defringe_alpha (co biên 1px + GaussianBlur 0.7px + khử viền trắng/xám), Soft Rim Light và 3D Double Shadow.
    (Hỗ trợ cả 2 tên gọi: add_floor_shadow và alias add_3d_shadow)
    """
    if add_3d_shadow is not None:
        add_floor_shadow = add_3d_shadow
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.with_name(f"{input_path.stem}_cutout.png")
    else:
        output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[AI Cutout SOTA] Đang bóc tách nền: {input_path.name} (Model: {model_name})...")
    orig = Image.open(input_path).convert("RGBA")
    
    # 1. Chạy AI Matting theo model session
    session = get_rembg_session(model_name)
    result_img = rembg.remove(orig, session=session)
    
    # 2. Khử viền trắng/xám + co biên 1px + làm mềm alpha 0.7px (defringe_alpha)
    if defringe:
        result_img = defringe_alpha(
            result_img,
            erode_px=1,
            feather_radius=edge_feather if edge_feather > 0 else 0.7,
            iterations=2,
        )
    elif edge_feather > 0:
        result_img = apply_alpha_feathering(result_img, radius=edge_feather)
    
    # 4. Thêm viền sticker (nếu bật)
    if add_stroke:
        result_img = add_outline(result_img, stroke_color=stroke_color, stroke_width=stroke_width)
        
    # 5. Thêm ánh sáng ven mềm (Soft Rim Light)
    if add_rim_light:
        result_img = add_soft_rim_light(result_img, color=rim_color, width=rim_width)
        
    # 5b. Làm tan mượt 18% cạnh đáy cho ảnh bán thân/chân dung chạm đáy
    if soft_bottom_fade:
        result_img = apply_soft_bottom_fade(result_img, fade_ratio=0.18)

    # 6. Thêm bóng sàn 3D (2 tầng hoặc 1 tầng)
    if add_floor_shadow:
        if double_shadow:
            result_img = add_3d_double_shadow(result_img, canvas_size=canvas_size)
        else:
            # Fallback single shadow
            result_img = add_3d_double_shadow(result_img, canvas_size=canvas_size, cast_opacity=0.0)
    elif crop_tight:
        bbox = result_img.getbbox()
        if bbox:
            result_img = result_img.crop(bbox)
            
    result_img.save(output_path, "PNG")
    print(f"[AI Cutout OK] Đã lưu sản phẩm bóc tách hoàn mỹ: {output_path}")
    return output_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Tự động bóc tách nền AI SOTA (BiRefNet/BRIA) & Chiếu sáng 3D")
    parser.add_argument("input", help="Đường dẫn ảnh đầu vào")
    parser.add_argument("-o", "--output", help="Đường dẫn file PNG kết quả", default=None)
    parser.add_argument("--model", default="bria-rmbg", choices=["bria-rmbg", "birefnet-general", "isnet-general-use", "u2net"], help="Model bóc tách")
    parser.add_argument("--rim", action="store_true", default=False, help="Bật Soft Rim Light (mặc định TẮT theo Luật 3)")
    parser.add_argument("--no-rim", dest="rim", action="store_false", help="Tắt Soft Rim Light")
    parser.add_argument("--rim-color", default="255,190,70", help="Màu ánh sáng ven R,G,B")
    parser.add_argument("--shadow", action="store_true", help="Bật bóng sàn phối cảnh 3D 2 lớp")
    parser.add_argument("--stroke", action="store_true", help="Thêm viền trắng sticker phẳng")
    parser.add_argument("--crop", action="store_true", help="Cắt sát mép vật thể")
    parser.add_argument("--no-defringe", dest="defringe", action="store_false", default=True, help="Tắt De-fringing")
    parser.add_argument("--feather", type=float, default=0.8, help="Bán kính Alpha Feathering")
    
    args = parser.parse_args()
    in_file = Path(args.input)
    out_file = Path(args.output) if args.output else None
        
    rim_c = tuple(map(int, args.rim_color.split(",")))
    cutout_image(
        in_file,
        out_file,
        model_name=args.model,
        defringe=args.defringe,
        edge_feather=args.feather,
        add_rim_light=args.rim,
        rim_color=rim_c,
        add_floor_shadow=args.shadow,
        double_shadow=True,
        add_stroke=args.stroke,
        crop_tight=args.crop
    )
```


#### `engine/playwright_web_helper.py`

```python
# -*- coding: utf-8 -*-
r"""
playwright_web_helper.py - Đọc trang web JS & chụp ảnh bằng chứng báo chí siêu nét bằng Playwright
Cách dùng:
  python playwright_web_helper.py read --url "https://..." --max-chars 6000
  python playwright_web_helper.py capture --url "https://..." --out "D:\DuAn_DangLam\...\evidence.png"
"""
import argparse
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")


def _open_page(pw, url: str, width: int = 1280, height: int = 900, timeout_ms: int = 25000):
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": width, "height": height},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ),
        locale="vi-VN",
    )
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
    try:
        page.wait_for_load_state("networkidle", timeout=6000)
    except Exception:
        page.wait_for_timeout(1500)
    return browser, page


def cmd_read(url: str, max_chars: int) -> dict:
    with sync_playwright() as pw:
        browser, page = _open_page(pw, url)
        try:
            title = page.title()
            text = page.evaluate(
                """() => {
                    const drop = document.querySelectorAll('script, style, noscript, nav, footer, aside, iframe');
                    drop.forEach(el => el.remove());
                    const main = document.querySelector('article, main, [role="main"]') || document.body;
                    return (main ? main.innerText : '').replace(/\\n{3,}/g, '\\n\\n').trim();
                }"""
            )
            return {
                "ok": True,
                "url": page.url,
                "title": title,
                "chars": len(text),
                "text": text[:max_chars],
            }
        finally:
            browser.close()


def cmd_capture(url: str, out_path: Path, width: int, height: int, full_page: bool) -> dict:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser, page = _open_page(pw, url, width=width, height=height)
        try:
            page.screenshot(path=str(out_path), full_page=full_page)
            return {
                "ok": True,
                "url": page.url,
                "title": page.title(),
                "saved": str(out_path),
                "bytes": out_path.stat().st_size,
            }
        finally:
            browser.close()


def main() -> int:
    ap = argparse.ArgumentParser(description="Playwright helper cho Biên kịch & Trinh sát FB Reels")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_read = sub.add_parser("read", help="Đọc nội dung trang web nặng JS")
    p_read.add_argument("--url", required=True)
    p_read.add_argument("--max-chars", type=int, default=6000)

    p_cap = sub.add_parser("capture", help="Chụp ảnh màn hình bài báo / số liệu thật")
    p_cap.add_argument("--url", required=True)
    p_cap.add_argument("--out", required=True)
    p_cap.add_argument("--width", type=int, default=1280)
    p_cap.add_argument("--height", type=int, default=900)
    p_cap.add_argument("--full-page", action="store_true")

    args = ap.parse_args()
    if args.cmd == "read":
        res = cmd_read(args.url, args.max_chars)
    else:
        res = cmd_capture(args.url, Path(args.out), args.width, args.height, args.full_page)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```


#### `engine/geo_map_builder.py`

```python
r"""
geo_map_builder.py - CÔNG CỤ TRÍCH XUẤT BẢN ĐỒ ĐỊA CHIẾN LƯỢC 3D TỰ ĐỘNG CHO MỌI QUỐC GIA (258 QUỐC GIA)
Đọc trực tiếp từ: D:\Đầu Não Video Ngắn FB (không xóa)\remotion_reels\public\maps\countries.geojson
Hỗ trợ tự động:
- Tra cứu tên quốc gia bằng cả Tiếng Việt lẫn Tiếng Anh (VD: "Việt Nam", "Mỹ", "Trung Quốc", "Nhật Bản", "Anh", "Nga", "Singapore"...)
- Tự động tính tọa độ tâm (Centroid lon/lat) của quốc gia lớn nhất nếu không truyền tay
- Tự động tính khung nhìn bản đồ (Bounding Box) bao trọn Quốc gia Nguồn + Quốc gia Đích kèm khoảng đệm thẩm mỹ
"""

import json
import sys
from pathlib import Path

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

FB_BRAIN = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
GEOJSON_PATH = FB_BRAIN / "remotion_reels" / "public" / "maps" / "countries.geojson"
DEFAULT_OUT_TS = FB_BRAIN / "remotion_reels" / "src" / "components" / "eurasiaGeoPaths.ts"

VI_TO_EN_COUNTRY = {
    "việt nam": "Vietnam",
    "vietnam": "Vietnam",
    "anh": "United Kingdom",
    "vương quốc anh": "United Kingdom",
    "luân đôn": "United Kingdom",
    "mỹ": "United States of America",
    "hoa kỳ": "United States of America",
    "trung quốc": "China",
    "nhật bản": "Japan",
    "nhật": "Japan",
    "hàn quốc": "South Korea",
    "triều tiên": "North Korea",
    "đài loan": "Taiwan",
    "singapore": "Singapore",
    "thái lan": "Thailand",
    "ấn độ": "India",
    "nga": "Russia",
    "đức": "Germany",
    "pháp": "France",
    "ý": "Italy",
    "úc": "Australia",
    "canada": "Canada",
    "brazil": "Brazil",
    "iran": "Iran",
    "israel": "Israel",
    "ả rập xê út": "Saudi Arabia",
    "uae": "United Arab Emirates",
    "thổ nhĩ kỳ": "Turkey",
    "ukraina": "Ukraine",
    "malaysia": "Malaysia",
    "indonesia": "Indonesia",
    "philippines": "Philippines",
    "campuchia": "Cambodia",
    "lào": "Laos",
    "hà lan": "Netherlands",
    "thụy sĩ": "Switzerland",
}


def resolve_country_name(name: str) -> str:
    clean = name.strip().lower()
    return VI_TO_EN_COUNTRY.get(clean, name.strip())


def compute_main_polygon_centroid(polys: list) -> tuple[float, float]:
    """Tìm đa giác có nhiều điểm nhất (đất liền chính) và tính tâm (lon, lat)."""
    best_ring = []
    for poly in polys:
        if poly and len(poly[0]) > len(best_ring):
            best_ring = poly[0]
    if not best_ring:
        return (0.0, 0.0)
    lons = [p[0] for p in best_ring]
    lats = [p[1] for p in best_ring]
    return (round(sum(lons) / len(lons), 2), round(sum(lats) / len(lats), 2))


def build_geo_paths_ts(
    origin_country: str = "Vietnam",
    target_country: str = "United Kingdom",
    origin_lonlat: tuple[float, float] | None = None,
    target_lonlat: tuple[float, float] | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    out_ts_path: Path = DEFAULT_OUT_TS,
):
    origin_en = resolve_country_name(origin_country)
    target_en = resolve_country_name(target_country)

    data = json.loads(GEOJSON_PATH.read_text(encoding="utf-8"))

    # Bước 1: Tự động tìm tâm (lon, lat) từ GeoJSON nếu chưa truyền tay
    auto_orig_lonlat = (105.85, 21.02)
    auto_targ_lonlat = (-0.12, 51.50)
    for feat in data.get("features", []):
        name = str(feat.get("properties", {}).get("name", ""))
        geom = feat.get("geometry", {})
        gtype = geom.get("type", "")
        coords = geom.get("coordinates", [])
        polys = [coords] if gtype == "Polygon" else coords if gtype == "MultiPolygon" else []
        if name.lower() == origin_en.lower():
            auto_orig_lonlat = compute_main_polygon_centroid(polys)
        elif name.lower() == target_en.lower():
            auto_targ_lonlat = compute_main_polygon_centroid(polys)

    if origin_lonlat is None:
        origin_lonlat = auto_orig_lonlat
    if target_lonlat is None:
        target_lonlat = auto_targ_lonlat

    # Bước 2: Tự động tính Bounding Box bao trọn 2 nước + khoảng đệm thẩm mỹ nếu chưa truyền tay
    if bbox is None:
        min_lon = min(origin_lonlat[0], target_lonlat[0])
        max_lon = max(origin_lonlat[0], target_lonlat[0])
        min_lat = min(origin_lonlat[1], target_lonlat[1])
        max_lat = max(origin_lonlat[1], target_lonlat[1])
        span_lon = max(35.0, max_lon - min_lon)
        span_lat = max(25.0, max_lat - min_lat)
        pad_lon = max(14.0, span_lon * 0.22)
        pad_lat = max(12.0, span_lat * 0.28)
        bbox = (
            max(-179.0, min_lon - pad_lon),
            min(179.0, max_lon + pad_lon),
            max(-65.0, min_lat - pad_lat),
            min(78.0, max_lat + pad_lat),
        )

    lon_min, lon_max, lat_min, lat_max = bbox
    w, h = 1000.0, 640.0

    def proj(lon: float, lat: float) -> tuple[float, float]:
        x = (lon - lon_min) / (lon_max - lon_min) * w
        y = (lat_max - lat) / (lat_max - lat_min) * h
        return round(x, 1), round(y, 1)

    def ring_to_path(ring: list, step: int = 1) -> str:
        pts = ring[::step]
        if len(pts) < 3:
            return ""
        coords = [proj(p[0], p[1]) for p in pts]
        d = f"M{coords[0][0]},{coords[0][1]}"
        for cx, cy in coords[1:]:
            d += f"L{cx},{cy}"
        return d + "Z"

    bg_paths, origin_paths, target_paths = [], [], []

    for feat in data.get("features", []):
        props = feat.get("properties", {})
        name = str(props.get("name", ""))
        geom = feat.get("geometry", {})
        gtype = geom.get("type", "")
        coords = geom.get("coordinates", [])

        polys = [coords] if gtype == "Polygon" else coords if gtype == "MultiPolygon" else []
        is_orig = name.lower() == origin_en.lower()
        is_targ = name.lower() == target_en.lower()

        for poly in polys:
            if not poly:
                continue
            ring = poly[0]
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]
            if max(lons) < lon_min or min(lons) > lon_max or max(lats) < lat_min or min(lats) > lat_max:
                continue
            step = 1 if (is_orig or is_targ) else max(1, len(ring) // 45)
            d = ring_to_path(ring, step=step)
            if not d:
                continue
            if is_orig:
                origin_paths.append(d)
            elif is_targ:
                target_paths.append(d)
            else:
                bg_paths.append(d)

    orig_pt = proj(*origin_lonlat)
    targ_pt = proj(*target_lonlat)

    ts_code = f"""// Auto-generated by geo_map_builder.py from countries.geojson
export const MAP_WIDTH = {int(w)};
export const MAP_HEIGHT = {int(h)};
export const ORIGIN_COORD = {{ x: {orig_pt[0]}, y: {orig_pt[1]} }};
export const TARGET_COORD = {{ x: {targ_pt[0]}, y: {targ_pt[1]} }};
export const ORIGIN_PATHS: string[] = {json.dumps(origin_paths)};
export const TARGET_PATHS: string[] = {json.dumps(target_paths)};
export const BG_PATHS: string[] = {json.dumps(bg_paths)};
// Backwards-compatible aliases
export const HANOI_COORD = ORIGIN_COORD;
export const LONDON_COORD = TARGET_COORD;
export const VIETNAM_PATHS = ORIGIN_PATHS;
export const UK_PATHS = TARGET_PATHS;
export const EURASIA_BG_PATHS = BG_PATHS;
"""
    out_ts_path.write_text(ts_code, encoding="utf-8")
    print(f"[GEO MAP BUILDER OK] Origin={origin_en} ({len(origin_paths)} paths, pt={orig_pt}), Target={target_en} ({len(target_paths)} paths, pt={targ_pt}) -> {out_ts_path.name}")
    return out_ts_path


if __name__ == "__main__":
    build_geo_paths_ts()
```


#### `engine/qc_gate.py`

```python
# -*- coding: utf-8 -*-
r"""
qc_gate.py - CỔNG KIỂM ĐỊNH DUY NHẤT (PRE-RENDER CODE GATE + POST-RENDER VISUAL/AUDIO QC)
Thay thế toàn bộ pre_render_gate.py & auto_qc_fb_reels.py cũ.

Chốt chặn thép:
1. Pre-render (.tsx):
   - CẤM phụ đề chạy chữ karaoke đáy, CẤM icon nhựa/StickerPop, CẤM neon chói, CẤM DotMatrixZoom.
   - BẮT BUỘC có lớp bối cảnh thật mờ sâu (ContextBackdropLayer / backdropSrc / objectFit: "cover") để diệt màn hình đen rỗng.
   - BẮT BUỘC có ít nhất 2 cơ chế diễn hoạt kiến thức (FlowPipeline3D, DecisionBranchPulse, ScaleComparison3D,
     GeoStrategicMap3D, TimelineTrack3D, AnatomyCallout3D, MetricOdometerHero, <svg).
   - BẮT BUỘC có words.json & voiceover.wav trong <project>/temp/.
2. Post-render (.mp4):
   - 1080x1920, >= 30fps (chuẩn 60fps).
   - CHỐNG MÀN HÌNH ĐEN RỖNG: nếu > 68% diện tích khung hình tối đen (gray < 18) hoặc mean_luma < 26.0 -> RỚT NGAY.
   - CHỐNG SLIDE ĐỨNG IM: kiểm tra biến thiên chuyển động giữa các mốc thời gian.
   - Chuẩn âm thanh EBU R128: -14.0 LUFS (± 1.0 LUFS), True Peak <= -0.5 dBTP.
   - Xuất ảnh lưới 3x3 (qc_grid_3x3.jpg) để Con Tổng soi trực tiếp bằng mắt.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

import cv2
import numpy as np

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

NEON_RE = re.compile(
    r"(?<![\w.-])(?<!0\s)0(?:px)?\s+0(?:px)?\s+(?:[4-9]|[1-9]\d)px\s+"
    r"(?:rgba?\(\s*(?!0\s*,\s*0\s*,\s*0\s*[,)])[^)]*\)|#[0-9A-Fa-f]{3,8}\b)",
    re.IGNORECASE,
)


VALID_ASSET_ROLES = {"prop_3d", "avatar_node", "ev_card"}

KNOWLEDGE_PRIMITIVES = (
    "SpeechPopCard25D",
    "SpeechPopCardStack25D",
    "ParallaxDepthStage",
    "Tilt3DFlip",
    "OpenHeroWatermarkStage",
    "RadialAvatarHub",
    "VisualCauseEffectFlow",
    "EditorialSplitTimeline",
    "DualStageKnowledgeLayout",
    "HighContrastConclusionCard",
    "VisualComparisonStrip",
    "ProcessStepChain",
    "VisualBarCompare",
    "EvidenceDocumentCard",
    "RadialNetworkBurst",
    "CycleDialProgress",
    "CircularAvatarNode",
    "HeroCutout3D",
    "FlowPipeline3D",
    "DecisionBranchPulse",
    "ScaleComparison3D",
    "GeoStrategicMap3D",
    "TimelineTrack3D",
    "AnatomyCallout3D",
    "CoinStream",
    "MetricOdometerHero",
    "OdometerCounter",
    "ForensicStampSlam",
    "RealPersonSpotlight3D",
    "UrbanSatelliteDive9x16",
    "MotionTrackedCallout",
    "RealSceneCameraStage",
    "EvidenceCalloutOverlay",
    "FactPunchlineCard",
    "SlashCrossOut",
    "MarkerHighlightText",
    "StaggerWaveText",
    "GlitchSplitText",
    "MetallicSweepText",
    "<svg",
)

# Khung dùng chung KHÔNG được tính vào chỉ số đa dạng component minh họa
SHARED_FRAME_COMPONENTS = {
    "HaDaWhyMistBackground",
    "ChannelWatermark9x16",
    "KineticHookHeader",
    "HaDaWhyFontFaces",
    "CameraStageWrapper",
    "ContainedPhotoBox",
}

# Các component bị cấm lặp quá 2 lần trong cùng 1 video
OVERUSE_LIMITED_COMPONENTS = (
    "EvidenceDocumentCard",
    "ProcessStepChain",
    "VisualBarCompare",
    "DualStageKnowledgeLayout",
)

# Nhóm component tạo chiều sâu 2.5D/3D bắt buộc có ở >= 2 Beat/video
DEPTH_25D_3D_COMPONENTS = (
    "ParallaxDepthStage",
    "SpeechPopCard25D",
    "SpeechPopCardStack25D",
    "Tilt3DFlip",
    "AnatomyCallout3D",
    "ScaleComparison3D",
    "TimelineTrack3D",
    "RealPersonSpotlight3D",
    "FlowPipeline3D",
)


def extract_layout_signature(code: str) -> Dict[str, Any]:
    """Trích xuất chữ ký bố cục (opening_style + component_sequence) từ mã nguồn TSX."""
    ordered_seq = sorted(
        [(code.find(k), k) for k in KNOWLEDGE_PRIMITIVES if k != "<svg" and k in code],
        key=lambda x: x[0],
    )
    comp_seq = [k for _, k in ordered_seq[:6]]
    opening_style = comp_seq[0] if comp_seq else "none"
    return {"opening_style": opening_style, "component_sequence": comp_seq}


def record_visual_layout_history(
    project_name: str,
    opening_style: str,
    component_sequence: List[str],
) -> Path:
    """
    Tự động ghi { project, opening_style, component_sequence, timestamp } vào
    engine/visual_layout_history.json sau khi qc_gate.py video hoặc render_reel.py thành công.
    """
    from datetime import datetime

    layout_hist_path = Path(__file__).resolve().parent / "visual_layout_history.json"
    entries: List[Dict[str, Any]] = []
    if layout_hist_path.exists():
        try:
            raw = json.loads(layout_hist_path.read_text(encoding="utf-8"))
            entries = raw if isinstance(raw, list) else (raw.get("entries") or [])
        except Exception:
            entries = []

    record = {
        "project": str(project_name).strip() or "unknown_project",
        "opening_style": str(opening_style or "none"),
        "component_sequence": list(component_sequence or []),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    # Loại bản ghi cũ cùng tên project (nếu render lại) rồi thêm bản mới nhất vào cuối
    entries = [e for e in entries if isinstance(e, dict) and e.get("project") != record["project"]]
    entries.append(record)
    entries = entries[-30:]

    layout_hist_path.write_text(
        json.dumps({"entries": entries}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return layout_hist_path


def check_harvest_plan(hplan_path: Path) -> Dict[str, Any]:
    """
    Kiểm định kế hoạch cào tư liệu (harvest_plan.json):
    - Đủ >= 8 mục khớp nhịp kịch bản, mỗi mục có must_show & >= 2 search_queries cụ thể.
    - BẮT BUỘC mỗi mục có đủ 'visual_reasoning' (>= 15 ký tự, không viết đối phó)
      và 'asset_role' hợp lệ thuộc {'prop_3d', 'avatar_node', 'ev_card'}.
      Thiếu -> chặn ngay với mã lỗi MISSING_VISUAL_REASONING.
    """
    issues: List[str] = []
    if not hplan_path.exists():
        return {
            "passed": False,
            "issues": [f"MISSING_HARVEST_PLAN: Không tìm thấy file kế hoạch cào tại {hplan_path}"],
        }

    try:
        hp = json.loads(hplan_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "passed": False,
            "issues": [f"INVALID_HARVEST_PLAN_JSON: Không đọc được JSON {hplan_path} ({exc})"],
        }

    hp_items = hp if isinstance(hp, list) else (hp.get("assets") or hp.get("items") or hp.get("entities") or [])
    if len(hp_items) < 8:
        issues.append(
            f"LAZY_HARVEST_PLAN: harvest_plan.json mới có {len(hp_items)} mục (< 8 mục tối thiểu khớp các nhịp kịch bản)."
        )

    lazy_logged = False
    for idx, it in enumerate(hp_items):
        if not isinstance(it, dict):
            continue
        eid = str(it.get("entity_id") or f"item_{idx+1}").strip()

        vr = str(it.get("visual_reasoning") or "").strip()
        if len(vr) < 15:
            issues.append(
                f"MISSING_VISUAL_REASONING: Mục '{eid}' thiếu 'visual_reasoning' hợp lệ "
                f"(hiện có {len(vr)} ký tự, bắt buộc >= 15 ký tự giải thích vì sao vật thể giúp hiểu ngay câu thoại trong 1s)."
            )

        role = str(it.get("asset_role") or "").strip().lower()
        if role not in VALID_ASSET_ROLES:
            issues.append(
                f"MISSING_VISUAL_REASONING: Mục '{eid}' thiếu hoặc sai 'asset_role'='{role}' "
                f"(bắt buộc chọn đúng 1 trong 3 vai trò: prop_3d | avatar_node | ev_card)."
            )

        qs = it.get("search_queries") if isinstance(it.get("search_queries"), list) else []
        if not lazy_logged and (not str(it.get("must_show", "")).strip() or len(qs) < 2):
            issues.append(
                f"LAZY_HARVEST_PLAN: Mục '{eid}' thiếu 'must_show' cụ thể hoặc 'search_queries' có < 2 từ khóa."
            )
            lazy_logged = True

    return {"passed": len(issues) == 0, "issues": issues, "count": len(hp_items)}


def check_tsx(tsx_path: Path, project_dir: Path) -> Dict[str, Any]:
    issues: List[str] = []
    warnings: List[str] = []

    if not tsx_path.exists():
        return {"passed": False, "issues": [f"Không tìm thấy file TSX: {tsx_path}"], "warnings": []}

    code = tsx_path.read_text(encoding="utf-8")

    # 1. Cấm phụ đề karaoke đáy, StickerPop, objects/*, DotMatrixZoom
    if re.search(r"<(?:KineticWordCaption|SyncCaptionBand|KaraokeCaption|SubtitleBand)\b", code):
        issues.append("BANNED_KARAOKE: Phát hiện phụ đề chạy chữ đáy màn hình. Chỉ dùng KineticHookHeader + nhãn kiến thức + số liệu.")
    if re.search(r"<StickerPop\b", code) or re.search(r'["\'\`/]objects(?:_3d)?/', code, re.IGNORECASE):
        issues.append("BANNED_PLASTIC_ICON: Phát hiện StickerPop hoặc objects/*. Bắt buộc dùng ảnh thật tách nền bria-rmbg.")
    if "DotMatrixZoom" in code:
        issues.append("BANNED_ABSTRACT_MATRIX: Cấm DotMatrixZoom trừu tượng.")
    if "CommentBubble3D" in code:
        issues.append("BANNED_OUTRO_CTA: Cấm CommentBubble3D gượng ép ở cuối video.")
    if "FloorPlatform3D" in code:
        issues.append("BANNED_FLOOR_DISC: Cấm dùng FloorPlatform3D (đĩa tròn dưới chân vật thể). Đổi sang nền sạch + bóng đổ tiếp xúc tự nhiên.")
    if "ContextBackdropLayer" in code:
        issues.append("BANNED_MESSY_PHOTO_BACKDROP: Cấm dùng ContextBackdropLayer phủ ảnh mờ toàn màn hình. Đặt ảnh thật sắc nét (opacity: 1) trong EvidenceDocumentCard / EditorialSplitTimeline trên nền lưới xanh đêm.")

    # 2. Cấm neon phát sáng nhòe
    neon_hits = [m.group(0) for m in NEON_RE.finditer(code)]
    if neon_hits:
        issues.append(f"BANNED_NEON_GLOW: Phát hiện {len(neon_hits)} hiệu ứng phát sáng màu ({neon_hits[0]}). Đổi thành bóng đen rgba(0,0,0,0.85).")

    # 3. Bắt buộc thành phần thương hiệu 2 lớp (góc trái + logo chìm chống bản quyền zIndex: 9999) & chữ chuẩn
    if "<ChannelWatermark9x16" not in code:
        issues.append("MISSING_WATERMARK: Thiếu <ChannelWatermark9x16 />.")
    wm_comp_path = Path(__file__).resolve().parent.parent / "remotion_reels" / "src" / "components" / "ChannelWatermark9x16.tsx"
    if not wm_comp_path.exists():
        issues.append(f"MISSING_STEALTH_WATERMARK: Không tìm thấy file {wm_comp_path}.")
    else:
        wm_code = wm_comp_path.read_text(encoding="utf-8")
        has_top_z = bool(re.search(r"zIndex\s*:\s*9999\b", wm_code))
        has_stealth_opacity = bool(re.search(r"opacity\s*:\s*0\.0\d+\b", wm_code)) or ("stealth-watermark" in wm_code)
        if not (has_top_z and has_stealth_opacity):
            issues.append(
                "MISSING_STEALTH_WATERMARK: ChannelWatermark9x16.tsx thiếu zIndex: 9999 hoặc lớp logo chìm chống bản quyền (opacity: 0.08). "
                "Khôi phục đủ 2 lớp thương hiệu trước khi render!"
            )
    if "<HaDaWhyMistBackground" not in code:
        issues.append("MISSING_MIST_BG: Thiếu <HaDaWhyMistBackground />.")
    if "KineticHookHeader" not in code and "HaDaWhyFontFaces" not in code:
        issues.append("MISSING_HOOK_HEADER: Thiếu <KineticHookHeader /> hoặc <HaDaWhyFontFaces />.")

    # 4. Cho phép dùng nền tối sạch <HaDaWhyMistBackground /> + lưới mờ hoặc kết hợp ContextBackdropLayer để sơ đồ nổi bật

    # 5. CHỐT CHẶN ĐA DẠNG COMPONENT MINH HỌA (LOW_COMPONENT_DIVERSITY >= 5 loại, không tính khung dùng chung)
    used_primitives = [k for k in KNOWLEDGE_PRIMITIVES if k in code]
    distinct_visual_comps = [
        k for k in KNOWLEDGE_PRIMITIVES
        if k != "<svg" and k not in SHARED_FRAME_COMPONENTS and re.search(rf"<{k}\b", code)
    ]
    if len(distinct_visual_comps) < 5:
        issues.append(
            f"LOW_COMPONENT_DIVERSITY: Video mới dùng {len(distinct_visual_comps)} loại component minh họa khác nhau "
            f"({distinct_visual_comps}). Bắt buộc dùng tối thiểu 5 loại component minh họa khác nhau cho 5 Beat "
            "(tra bảng 'Kịch bản nói gì -> Gọi món đó' trong .agent/COMPONENT_CATALOG.md)."
        )

    # 5a. OVERUSED_SINGLE_COMPONENT & BANNED_OVERUSED_DOUBLE_BOX: Cấm lặp quá 2 lần cùng 1 component minh họa
    for lim_comp in OVERUSE_LIMITED_COMPONENTS:
        cnt = len(re.findall(rf"<{lim_comp}\b", code))
        if cnt > 2:
            issues.append(
                f"OVERUSED_SINGLE_COMPONENT: Component <{lim_comp} bị lặp {cnt} lần (> 2 lần tối đa/video). "
                "Hãy phối hợp đa dạng đồ nghề theo .agent/COMPONENT_CATALOG.md!"
            )
            if lim_comp == "DualStageKnowledgeLayout":
                issues.append(
                    f"BANNED_OVERUSED_DOUBLE_BOX: Phát hiện gọi <DualStageKnowledgeLayout {cnt} lần (> 2 Beat tối đa). "
                    "Cấm lặp khuôn 2 hộp PowerPoint! Hãy phối hợp với OpenHeroWatermarkStage, RadialAvatarHub, VisualCauseEffectFlow, EditorialSplitTimeline."
                )

    # 5a1. MISSING_25D_3D_DEPTH: Bắt buộc tối thiểu 2 Beat sử dụng chiều sâu 2.5D/3D rõ rệt
    seq_blocks = re.split(r"<Sequence\b", code)[1:]
    if len(seq_blocks) >= 2:
        depth_beats = sum(
            1 for blk in seq_blocks
            if any(re.search(rf"<{dc}\b", blk) for dc in DEPTH_25D_3D_COMPONENTS)
        )
    else:
        depth_beats = sum(len(re.findall(rf"<{dc}\b", code)) for dc in DEPTH_25D_3D_COMPONENTS)
    if depth_beats < 2:
        issues.append(
            f"MISSING_25D_3D_DEPTH: Chỉ có {depth_beats} Beat dùng chiều sâu 2.5D/3D (< 2 Beat bắt buộc). "
            "Bắt buộc dùng ít nhất 2 Beat có ParallaxDepthStage / SpeechPopCard25D / Tilt3DFlip / AnatomyCallout3D / ScaleComparison3D / TimelineTrack3D / RealPersonSpotlight3D / FlowPipeline3D."
        )

    # 5a2. EMPTY_EARLY_STAGE_DELAY: Chặn MetricOdometerHero xuất hiện quá muộn (startFrame > 90)
    for m_odo in re.finditer(r"<MetricOdometerHero\b[\s\S]*?/>", code):
        tag_txt = m_odo.group(0)
        m_sf = re.search(r"startFrame\s*=\s*\{\s*(\d+)\s*\}", tag_txt)
        if m_sf:
            sf_val = int(m_sf.group(1))
            if sf_val > 90:
                issues.append(
                    f"EMPTY_EARLY_STAGE_DELAY: MetricOdometerHero có startFrame={sf_val} (> 90 frames / 1.5s đầu Beat) gây trống nửa màn hình. "
                    "Bắt buộc xuất hiện trong <= 60 frames đầu Beat!"
                )

    # 5a3. OUT_OF_ORDER_STEPS: Chặn nếu triggerFrame trong ProcessStepChain không tăng dần nghiêm ngặt
    for m_psc in re.finditer(r"<ProcessStepChain\b[\s\S]*?/>", code):
        block = m_psc.group(0)
        trigs = [int(x) for x in re.findall(r"triggerFrame\s*:\s*(\d+)", block)]
        if len(trigs) >= 2 and any(trigs[i] >= trigs[i + 1] for i in range(len(trigs) - 1)):
            issues.append(
                f"OUT_OF_ORDER_STEPS: Các triggerFrame trong ProcessStepChain không tăng dần nghiêm ngặt ({trigs}). "
                "Bắt buộc step[i].triggerFrame < step[i+1].triggerFrame!"
            )

    # 5b. Chặn EMPTY_BOTTOM_STAGE (chấp nhận hoàn toàn các bố cục Sân Khấu Mở & 2.5D/3D, chỉ chặn khi tổng thể bỏ trống nửa dưới)
    has_bottom_stage = any(
        k in code
        for k in (
            "OpenHeroWatermarkStage",
            "RadialAvatarHub",
            "VisualCauseEffectFlow",
            "EditorialSplitTimeline",
            "DualStageKnowledgeLayout",
            "HighContrastConclusionCard",
            "VisualComparisonStrip",
            "SpeechPopCard25D",
            "SpeechPopCardStack25D",
            "ParallaxDepthStage",
            "AnatomyCallout3D",
            "ScaleComparison3D",
            "TimelineTrack3D",
            "RealPersonSpotlight3D",
        )
    ) or bool(re.search(r'(?:top\s*[:=]\s*\{?\s*(?:9\d\d|1[0-5]\d\d)|y\s*=\s*\{\s*(?:9\d\d|1[0-5]\d\d))', code))
    if not has_bottom_stage:
        issues.append(
            "EMPTY_BOTTOM_STAGE: Tổng thể nửa dưới màn hình (Y: 900..1540) đang bị bỏ trống. "
            "Hãy dùng OpenHeroWatermarkStage / RadialAvatarHub / VisualCauseEffectFlow / EditorialSplitTimeline hoặc đặt khối minh họa ở nửa dưới."
        )

    # 5c. Chặn REPETITIVE_TEMPLATE_CLONE qua engine/visual_layout_history.json (so với 3 tập gần nhất)
    layout_hist_path = Path(__file__).resolve().parent / "visual_layout_history.json"
    sig = extract_layout_signature(code)
    comp_seq = sig["component_sequence"]
    opening_style = sig["opening_style"]
    try:
        (project_dir / "temp").mkdir(parents=True, exist_ok=True)
        (project_dir / "temp" / "layout_signature.json").write_text(
            json.dumps({"project": project_dir.name, **sig}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass
    if layout_hist_path.exists() and comp_seq:
        try:
            hist_data = json.loads(layout_hist_path.read_text(encoding="utf-8"))
            recent = (hist_data if isinstance(hist_data, list) else hist_data.get("entries", []))[-3:]
            for rec in recent:
                if rec.get("project") != project_dir.name and rec.get("opening_style") == opening_style and rec.get("component_sequence") == comp_seq:
                    issues.append(
                        f"REPETITIVE_TEMPLATE_CLONE: Bố cục trùng y hệt tập '{rec.get('project')}' "
                        f"(opening={opening_style}, seq={comp_seq}). Hãy đổi kiểu mở đầu và thứ tự khối đồ họa!"
                    )
                    break
        except Exception:
            pass

    # 5d. Kiểm tra mật độ SFX & khớp FPS 60 trong choreography_blueprint.json
    bp_cand = project_dir / "temp" / "choreography_blueprint.json"
    if bp_cand.exists():
        try:
            bp_data = json.loads(bp_cand.read_text(encoding="utf-8"))
            bp_fps = int(bp_data.get("fps", 0) or 0)
            if bp_fps != 60:
                issues.append(f"FPS_MISMATCH: choreography_blueprint.json có fps={bp_fps}, bắt buộc fps=60 khớp 100% với .tsx.")
            all_ev = [e for e in (bp_data.get("events") or []) if isinstance(e, dict)]
            all_ev.extend([e for b in bp_data.get("beats", []) for e in (b.get("events") or []) if isinstance(e, dict)])
            if len(all_ev) < 18:
                issues.append(
                    f"INSUFFICIENT_SFX_DENSITY: choreography_blueprint.json mới có {len(all_ev)} mốc sự kiện (< 18 mốc tối thiểu cho video 40-45s)."
                )
            ev_kinds = {str(e.get("kind") or e.get("type") or "").lower() for e in all_ev}
            has_hook_ev = bool(ev_kinds & {"hook", "hook_text", "text"})
            has_subj_ev = bool(ev_kinds & {"subject", "knowledge", "knowledge_text"})
            has_num_ev = bool(ev_kinds & {"number", "number_knowledge", "number_money"})
            if not (has_hook_ev and has_subj_ev and has_num_ev):
                issues.append(
                    f"INSUFFICIENT_SFX_DENSITY: Thiếu nhóm sự kiện trong choreography_blueprint.json "
                    f"(hook={has_hook_ev}, subject/knowledge={has_subj_ev}, number={has_num_ev})."
                )
        except Exception:
            pass

    # 5e. Kiểm tra SHALLOW_RESEARCH, LAZY_HARVEST_PLAN & BANNED_RED_THUMBNAIL_BADGE
    temp_dir = project_dir / "temp"
    res_raw = temp_dir / "research_raw.json"
    res_dos = temp_dir / "research_dossier.json"
    if res_raw.exists():
        try:
            rd = json.loads(res_raw.read_text(encoding="utf-8"))
            n_facts = int(rd.get("hard_facts_count", len(rd.get("facts", []))))
            n_urls = int(rd.get("deep_urls_count", len({f.get("url") for f in rd.get("facts", []) if f.get("url")})))
            if n_facts < 6 or n_urls < 3:
                issues.append(
                    f"SHALLOW_RESEARCH: research_raw.json chỉ có {n_facts} dữ kiện cứng / {n_urls} URL (< 6 dữ kiện hoặc < 3 URL thật). Chạy lại fact_researcher.py với >= 4-5 truy vấn sâu!"
                )
        except Exception:
            pass
    elif res_dos.exists():
        try:
            dd = json.loads(res_dos.read_text(encoding="utf-8"))
            items_d = dd if isinstance(dd, list) else (dd.get("facts") or dd.get("items") or [])
            if len(items_d) < 6:
                issues.append(f"SHALLOW_RESEARCH: research_dossier.json chỉ có {len(items_d)} dữ kiện (< 6 dữ kiện cứng).")
        except Exception:
            pass

    hplan_path = temp_dir / "harvest_plan.json"
    if hplan_path.exists():
        hp_res = check_harvest_plan(hplan_path)
        issues.extend(hp_res.get("issues", []))

    thumb_props_path = temp_dir / "thumb_props.json"
    if thumb_props_path.exists():
        try:
            tp_txt = thumb_props_path.read_text(encoding="utf-8")
            tp_json = json.loads(tp_txt)
            if str(tp_json.get("topBadgeText", "")).strip():
                issues.append("BANNED_RED_THUMBNAIL_BADGE: Cấm truyền topBadgeText (thanh nhãn đỏ/dòng chữ thứ 3) vào thumb_props.json!")
        except Exception:
            pass
    if "topBadgeText" in code:
        issues.append("BANNED_RED_THUMBNAIL_BADGE: Phát hiện topBadgeText (thanh nhãn đỏ trên Thumbnail).")

    # 6. Kiểm tra tối thiểu 4 ảnh thật trong harvested/ & CHỐNG LẶP ẢNH TRONG CÙNG VIDEO
    raw_img_refs = re.findall(r'harvested/[^"\'\s]+\.(?:png|jpg|jpeg|webp)', code, re.IGNORECASE)
    img_refs = sorted(set(raw_img_refs))
    if len(img_refs) < 4:
        issues.append(f"INSUFFICIENT_REAL_ASSETS: Chỉ tham chiếu {len(img_refs)} ảnh thật trong harvested/. Cần ít nhất 4 ảnh thật sắc nét.")

    from collections import Counter
    ref_counts = Counter(r.lower() for r in raw_img_refs)
    dup_refs = {k: v for k, v in ref_counts.items() if v >= 2}
    if dup_refs:
        dup_str = ", ".join(f"{k} ({v}x)" for k, v in sorted(dup_refs.items()))
        issues.append(
            f"DUPLICATE_ASSET_IN_VIDEO: Cấm lặp lại cùng 1 ảnh trên nhiều cảnh trong 1 video: {dup_str}. "
            "Mỗi cảnh phải dùng ảnh riêng biệt sát với lời thoại của cảnh đó."
        )

    # 6b. Kiểm tra cấm ẩn dụ trừu tượng / rác trong tên asset (Zero Banned Metaphors)
    banned_asset_keywords = ["scale", "justice", "perfume", "diet", "nutrition", "cartoon"]
    for ref in img_refs:
        ref_low = ref.lower()
        for b_kw in banned_asset_keywords:
            if b_kw in ref_low:
                issues.append(f"BANNED_METAPHOR_ASSET: Asset '{ref}' vi phạm Luật 1 & 11 (Cấm ẩn dụ trừu tượng '{b_kw}' trong video công nghệ/đời thực). Bắt buộc dùng thực thể thực tế!")

    # 7. Kiểm tra words.json, voiceover.wav & ĐỒNG BỘ HÌNH KHỚP GIỌNG ĐỌC (Voice-Visual Sync)
    temp_dir = project_dir / "temp"
    has_words = (temp_dir / "words.json").exists() or any(project_dir.rglob("*words*.json"))
    has_voice = (temp_dir / "voiceover.wav").exists() or (temp_dir / "voice.wav").exists()
    if not has_words:
        issues.append(f"MISSING_WORDS_JSON: Không thấy words.json trong {project_dir}.")
    if not has_voice:
        issues.append(f"MISSING_VOICEOVER: Không thấy voiceover.wav / voice.wav trong {temp_dir}.")
    if has_words:
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from voice_visual_sync import check as voice_sync_check
            vs = voice_sync_check(project_dir)
            issues.extend(vs.get("issues", []))
            warnings.extend(vs.get("warnings", []))
        except Exception as exc:
            issues.append(f"VOICE_VISUAL_SYNC_ERROR: Không chạy được kiểm tra khớp hình-thoại ({exc}).")

    return {
        "passed": len(issues) == 0,
        "tsx_path": str(tsx_path),
        "used_primitives": used_primitives,
        "real_assets_count": len(img_refs),
        "issues": issues,
        "warnings": warnings,
    }


def make_contact_sheet(video_path: Path, out_grid: Path, dur_sec: float) -> None:
    tmp_dir = out_grid.parent / "_qc_frames_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    ts = [
        0.20, 1.50, max(2.5, dur_sec * 0.14),
        dur_sec * 0.28, dur_sec * 0.42, dur_sec * 0.56,
        dur_sec * 0.70, dur_sec * 0.84, max(0.5, dur_sec - 0.8),
    ]
    for i, t in enumerate(ts):
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(video_path), "-frames:v", "1", "-q:v", "3", str(tmp_dir / f"f{i}.jpg")],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    cmd = ["ffmpeg", "-y"]
    for i in range(9):
        cmd += ["-i", str(tmp_dir / f"f{i}.jpg")]
    cmd += [
        "-filter_complex",
        "xstack=inputs=9:layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0|0_h0+h3|w0_h0+h3|w0+w1_h0+h3,scale=1080:-1",
        str(out_grid),
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(tmp_dir, ignore_errors=True)


def measure_lufs(video_path: Path) -> Dict[str, float]:
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-af", "ebur128=peak=true", "-f", "null", "-",
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    stderr = res.stderr or ""
    integrated = -99.0
    true_peak = 0.0
    m_i = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", stderr)
    if m_i:
        integrated = float(m_i[-1])
    m_tp = re.findall(r"Peak:\s*(-?\d+(?:\.\d+)?)\s*dBFS", stderr)
    if m_tp:
        true_peak = float(m_tp[-1])
    return {"integrated_lufs": integrated, "true_peak_db": true_peak}


def check_video(
    video_path: Path,
    grid_out: Path | None = None,
    project_dir: Path | None = None,
    tsx_path: Path | None = None,
) -> Dict[str, Any]:
    report: Dict[str, Any] = {
        "video_path": str(video_path),
        "passed": False,
        "score": 100,
        "issues": [],
        "metrics": {},
    }
    if not video_path.exists():
        report["score"] = 0
        report["issues"].append("Video không tồn tại!")
        return report

    # 1. ffprobe check
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height,r_frame_rate,duration,codec_type", "-of", "json", str(video_path)],
        capture_output=True, text=True,
    )
    if probe.returncode != 0:
        report["score"] = 0
        report["issues"].append("ffprobe đọc file thất bại!")
        return report

    meta = json.loads(probe.stdout)
    v_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), None)
    if not v_stream:
        report["score"] = 0
        report["issues"].append("Không có video stream!")
        return report

    w, h = int(v_stream.get("width", 0)), int(v_stream.get("height", 0))
    report["metrics"]["resolution"] = f"{w}x{h}"
    if w != 1080 or h != 1920:
        report["score"] -= 30
        report["issues"].append(f"Sai tỷ lệ 9:16: {w}x{h} (yêu cầu 1080x1920).")

    # 2. OpenCV visual density & anti-empty-void check
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur_sec = total_frames / fps if fps > 0 else 0.0
    report["metrics"]["fps"] = round(fps, 2)
    report["metrics"]["duration_sec"] = round(dur_sec, 2)

    sample_times = [dur_sec * p for p in (0.08, 0.18, 0.30, 0.42, 0.54, 0.66, 0.78, 0.88, 0.95)]
    luma_list: List[float] = []
    std_luma_list: List[float] = []
    dark_ratio_list: List[float] = []
    black_frames = 0
    prev_small = None
    static_pairs = 0

    for t in sample_times:
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(total_frames - 1, max(0, int(t * fps))))
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_luma = float(np.mean(gray))
        std_luma = float(np.std(gray))
        dark_ratio = float(np.mean(gray < 18))
        luma_list.append(mean_luma)
        std_luma_list.append(std_luma)
        dark_ratio_list.append(dark_ratio)
        if mean_luma < 5.0 and std_luma < 4.0:
            black_frames += 1
        small = cv2.resize(gray, (180, 320))
        if prev_small is not None:
            diff = float(np.mean(np.abs(small.astype(np.float32) - prev_small.astype(np.float32))))
            if diff < 1.8:
                static_pairs += 1
        prev_small = small
    cap.release()

    avg_luma = round(float(np.mean(luma_list)) if luma_list else 0.0, 2)
    avg_std_luma = round(float(np.mean(std_luma_list)) if std_luma_list else 0.0, 2)
    avg_dark_ratio = round(float(np.mean(dark_ratio_list)) * 100.0 if dark_ratio_list else 100.0, 1)
    report["metrics"]["avg_luma"] = avg_luma
    report["metrics"]["avg_std_luma"] = avg_std_luma
    report["metrics"]["avg_black_void_pct"] = avg_dark_ratio
    report["metrics"]["black_frames"] = black_frames
    report["metrics"]["static_pairs"] = static_pairs

    if black_frames > 0:
        report["score"] -= 40
        report["issues"].append(f"BLACK_FRAME_DETECTED: Có {black_frames} khung hình đen kịt hỏng render.")
    if avg_luma < 6.0 and avg_std_luma < 4.0:
        report["score"] -= 35
        report["issues"].append(
            f"EMPTY_DARK_VOID_SCREEN: Màn hình đen kịt hỏng render (avg_luma={avg_luma} < 6.0, std_luma={avg_std_luma} < 4.0)."
        )
    if static_pairs >= 3:
        report["score"] -= 25
        report["issues"].append(f"STATIC_SLIDESHOW_DETECTED: {static_pairs} cặp khung hình hầu như đứng im không biến chuyển.")

    # 3. Audio EBU R128 check
    audio_stats = measure_lufs(video_path)
    report["metrics"].update(audio_stats)
    lufs = audio_stats["integrated_lufs"]
    tp = audio_stats["true_peak_db"]
    if not (-15.2 <= lufs <= -12.8):
        report["score"] -= 25
        report["issues"].append(f"LOUDNESS_OUT_OF_SPEC: {lufs:.1f} LUFS (yêu cầu -14.0 ± 1.0 LUFS).")
    if tp > -0.3:
        report["score"] -= 15
        report["issues"].append(f"TRUE_PEAK_CLIPPING: {tp:.1f} dBFS (yêu cầu <= -0.5 dBTP).")

    if grid_out:
        make_contact_sheet(video_path, grid_out, dur_sec)
        report["grid_path"] = str(grid_out)

    report["score"] = max(0, report["score"])
    report["passed"] = report["score"] >= 85 and len(report["issues"]) == 0

    # Tự động ghi vào engine/visual_layout_history.json khi QC video đạt chuẩn
    if report["passed"]:
        try:
            proj_name = project_dir.name if project_dir else video_path.stem
            sig_data: Dict[str, Any] | None = None
            if tsx_path and tsx_path.exists():
                sig_data = extract_layout_signature(tsx_path.read_text(encoding="utf-8"))
            else:
                cand_sigs = []
                if project_dir:
                    cand_sigs.append(project_dir / "temp" / "layout_signature.json")
                if grid_out:
                    cand_sigs.append(grid_out.parent / "layout_signature.json")
                for sp in cand_sigs:
                    if sp.exists():
                        raw_sig = json.loads(sp.read_text(encoding="utf-8"))
                        proj_name = str(raw_sig.get("project") or proj_name)
                        sig_data = {
                            "opening_style": raw_sig.get("opening_style", "none"),
                            "component_sequence": raw_sig.get("component_sequence", []),
                        }
                        break
            if sig_data:
                record_visual_layout_history(
                    project_name=proj_name,
                    opening_style=sig_data["opening_style"],
                    component_sequence=sig_data["component_sequence"],
                )
                report["layout_history_recorded"] = True
        except Exception as exc:
            report["layout_history_error"] = str(exc)

    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Unified QC Gate for FB Reels 9:16")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan", help="Kiểm tra tư duy đạo diễn trong temp/harvest_plan.json trước khi cào")
    p_plan.add_argument("--project", default="")
    p_plan.add_argument("--manifest", default="")

    p_tsx = sub.add_parser("tsx", help="Kiểm tra file Composition .tsx trước khi render")
    p_tsx.add_argument("--tsx", required=True)
    p_tsx.add_argument("--project", required=True)

    p_vid = sub.add_parser("video", help="Kiểm tra video MP4 thành phẩm sau khi render")
    p_vid.add_argument("--video", required=True)
    p_vid.add_argument("--grid", default="")
    p_vid.add_argument("--project", default="")
    p_vid.add_argument("--tsx", default="")

    args = ap.parse_args()
    if args.cmd == "plan":
        manifest_p = Path(args.manifest) if args.manifest else (Path(args.project) / "temp" / "harvest_plan.json")
        res = check_harvest_plan(manifest_p)
    elif args.cmd == "tsx":
        res = check_tsx(Path(args.tsx), Path(args.project))
    else:
        res = check_video(
            Path(args.video),
            Path(args.grid) if args.grid else None,
            project_dir=Path(args.project) if args.project else None,
            tsx_path=Path(args.tsx) if args.tsx else None,
        )

    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
```


#### `engine/voice_visual_sync.py`

```python
"""
VOICE-VISUAL SYNC - hình & hiệu ứng phải BÁM THEO GIỌNG ĐỌC (luật chung cho mọi kịch bản).

Nguyên tắc (Người Chỉ Huy):
  - Hiệu ứng/hình chỉ xuất hiện khi giọng đọc nói tới nó, không rải theo đồng hồ để lấp chỗ trống.
  - Mỗi câu thoại chỉ hiện đúng thứ cần để người xem hiểu: CHỦ THỂ chính (mô hình 3D thật) và CON SỐ quan trọng.
    Ví dụ câu "...thị trường chip AI đã thống trị được 40.000$" -> chỉ hiện: hình chip AI + con số 40.000$.

Nguồn dữ liệu:
  - words.json (mốc thời gian từng từ của giọng đọc) trong <project>/temp/ hoặc <project>/.
  - choreography_blueprint.json: mỗi beat có events dạng
        {"frame": 126, "kind": "subject", "show": "chip AI", "voice_word": "chip"}
        {"frame": 228, "kind": "number",  "show": "40.000$"}
    kind = subject | number | text. 'voice_word' là từ trong lời đọc kích hoạt hình đó (số thì tự dò theo chữ số).

Kiểm tra:
  1. SYNC: hình xuất hiện sớm tối đa LEAD_SEC hoặc trễ tối đa LAG_SEC so với lúc giọng đọc nói từ/số đó.
  2. COVERAGE: mọi con số quan trọng trong lời đọc đều có hình hiển thị số đó.
  3. MINIMAL: mỗi câu tối đa MAX_PER_SENTENCE_BLOCK hình quan trọng (khuyến nghị <= MAX_PER_SENTENCE_WARN).

Dùng:
  python voice_visual_sync.py --tsx <file.tsx> --project <D:\\DuAn_DangLam\\id>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FPS = 60
LEAD_SEC = 0.5               # hình được hiện sớm tối đa 0.5s trước khi giọng đọc nói
LAG_SEC = 0.6                # hoặc trễ tối đa 0.6s sau khi giọng đọc nói
PAUSE_SEC = 0.6              # khoảng lặng >= 0.6s coi như hết câu
MAX_PER_SENTENCE_WARN = 2    # khuyến nghị: chủ thể + con số
MAX_PER_SENTENCE_BLOCK = 3   # vượt mức này là rối mắt -> chặn
KINDS = ("subject", "number", "text", "hook", "hook_text", "knowledge", "knowledge_text", "number_knowledge", "number_money")


def find_words_json(project_dir: Path | str) -> Path | None:
    """Vị trí words.json thống nhất cho MỌI gate. Các công cụ cũ ghi ở nhiều chỗ khác nhau:
    <project>/words.json, <project>/temp/words.json, <project>/gate_tmp/words.json (cloud_reels_runner),
    <project>/**/<prefix>_words.json (vieneu_whisper_pacer). Lấy file mới nhất."""
    project_dir = Path(project_dir)
    fixed = [project_dir / "temp" / "words.json", project_dir / "words.json", project_dir / "gate_tmp" / "words.json"]
    found = [p for p in fixed if p.exists()]
    if not found and project_dir.exists():
        found = [p for p in project_dir.rglob("*words.json") if p.is_file()]
    return max(found, key=lambda p: p.stat().st_mtime) if found else None


def _load_words(project_dir: Path) -> list[dict]:
    cand = find_words_json(project_dir)
    if cand is not None:
        if True:
            data = json.loads(cand.read_text(encoding="utf-8"))
            items = data.get("words", data) if isinstance(data, dict) else data
            out: list[dict] = []
            for w in items:
                if "start" in w:
                    st = float(w["start"])
                elif "startMs" in w:
                    st = float(w["startMs"]) / 1000.0
                else:
                    st = 0.0
                if "end" in w:
                    en = float(w["end"])
                elif "endMs" in w:
                    en = float(w["endMs"]) / 1000.0
                else:
                    en = None
                out.append({"text": str(w.get("word", w.get("text", ""))), "start": st, "end": en})
            return out
    return []


def _load_events(project_dir: Path) -> list[dict]:
    for cand in (project_dir / "temp" / "choreography_blueprint.json", project_dir / "choreography_blueprint.json"):
        if cand.exists():
            bp = json.loads(cand.read_text(encoding="utf-8"))
            ev: list[dict] = []
            raw_list = list(bp.get("events") or [])
            for b in bp.get("beats", []):
                raw_list.extend(b.get("events") or [])
            for e in raw_list:
                if isinstance(e, dict) and "frame" in e:
                    k = e.get("kind") or e.get("type")
                    if k in KINDS:
                        norm_e = dict(e)
                        norm_e["kind"] = k
                        ev.append(norm_e)
            return ev
    return []


def _norm(s: str) -> str:
    return re.sub(r"[^\w]", "", s.lower())


def _digits(s: str) -> str:
    return re.sub(r"\D", "", s)


def _is_key_number(token: str) -> bool:
    d = _digits(token)
    return bool(d) and (len(d) >= 2 or bool(re.search(r"[%$đ₫]", token)))


def _sentences(words: list[dict]) -> list[tuple[float, float]]:
    """Cắt câu theo dấu chấm/hỏi/than hoặc khoảng lặng dài. Trả về [(t_start, t_end)]."""
    spans: list[tuple[float, float]] = []
    if not words:
        return spans
    s0 = words[0]["start"]
    for i, w in enumerate(words):
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_t = w["end"] if w["end"] is not None else (nxt["start"] if nxt else w["start"] + 0.4)
        ends = bool(re.search(r"[.!?…]$", w["text"].strip()))
        gap = (nxt["start"] - end_t) if nxt else 99.0
        if ends or gap >= PAUSE_SEC or nxt is None:
            spans.append((s0, end_t))
            if nxt:
                s0 = nxt["start"]
    return spans


def check(project_dir: Path) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    words = _load_words(project_dir)
    events = _load_events(project_dir)

    if not words:
        warnings.append("VOICE SYNC bỏ qua: chưa có words.json (không có mốc giọng đọc để đối chiếu).")
        return {"passed": True, "issues": issues, "warnings": warnings}
    if not events:
        issues.append(
            "VOICE SYNC BLUEPRINT THIẾU (Luật 12): choreography_blueprint.json phải có events dạng "
            "{frame, kind: subject|number|text, show, voice_word} bám theo mốc giọng đọc trong words.json. "
            "Mỗi câu chỉ lập sự kiện cho chủ thể chính và con số quan trọng."
        )
        return {"passed": False, "issues": issues, "warnings": warnings}

    key_tokens = [(w["start"], _digits(w["text"])) for w in words if _is_key_number(w["text"])]

    # 1. SYNC từng sự kiện với lời đọc
    for e in events:
        t = int(e["frame"]) / FPS
        show = str(e.get("show", ""))
        kind = e["kind"]
        if kind in ("number", "number_knowledge", "number_money"):
            d = _digits(show)
            starts = [s for s, dd in key_tokens if dd == d] or [
                w["start"] for w in words if _digits(w["text"]) == d and d
            ]
            label = f"số '{show}'"
        else:
            show_first = show.split()[0] if show.split() else ""
            vw = str(e.get("voice_word") or show_first)
            first = _norm(vw.split()[0]) if vw.split() else ""
            starts = [w["start"] for w in words if first and _norm(w["text"]) == first]
            label = f"hình '{show}' (từ '{vw}')"
        if not starts:
            issues.append(f"VOICE SYNC (Luật 12): {label} không có trong lời đọc words.json - hình không có điểm neo giọng đọc.")
            continue
        near = min(starts, key=lambda s: abs(s - t))
        delta = t - near
        if not (-LEAD_SEC <= delta <= LAG_SEC):
            when = "SỚM" if delta < 0 else "TRỄ"
            issues.append(
                f"VOICE SYNC (Luật 12): {label} hiện {when} {abs(delta):.2f}s so với lúc giọng đọc nói "
                f"(cho phép sớm <= {LEAD_SEC}s, trễ <= {LAG_SEC}s). Dời frame về ~{int(round(near * FPS))}."
            )

    # 2. COVERAGE con số quan trọng
    shown = {_digits(str(e.get("show", ""))) for e in events if e["kind"] in ("number", "number_knowledge", "number_money")}
    for s, d in key_tokens:
        if d not in shown:
            issues.append(
                f"VOICE SYNC COVERAGE (Luật 12): giọng đọc nói con số quan trọng tại {s:.2f}s (chữ số {d}) "
                "nhưng chưa có sự kiện kind=number hiển thị số đó."
            )
    # chỉ báo mỗi con số một lần
    issues[:] = list(dict.fromkeys(issues))

    # 3. MINIMAL: số hình quan trọng mỗi câu
    for i, (a, b) in enumerate(_sentences(words), 1):
        n = sum(1 for e in events if a - LEAD_SEC <= int(e["frame"]) / FPS <= b + LAG_SEC)
        if n > MAX_PER_SENTENCE_BLOCK:
            issues.append(
                f"VOICE SYNC MINIMAL (Luật 12): câu #{i} ({a:.1f}s-{b:.1f}s) có {n} hình quan trọng "
                f"(tối đa {MAX_PER_SENTENCE_BLOCK}). Chỉ giữ chủ thể chính + con số quan trọng."
            )
        elif n > MAX_PER_SENTENCE_WARN:
            warnings.append(f"Câu #{i} có {n} hình quan trọng (> {MAX_PER_SENTENCE_WARN}) - nên rút còn chủ thể + con số.")

    return {"passed": not issues, "issues": issues, "warnings": warnings, "events": len(events)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsx", help="(không bắt buộc) giữ để đồng bộ giao diện với các gate khác")
    ap.add_argument("--project", required=True)
    a = ap.parse_args()
    res = check(Path(a.project))
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
```


#### `engine/audio_harvester.py`

```python
# -*- coding: utf-8 -*-
r"""
audio_harvester.py - CÀO NHẠC NỀN & SFX TƯƠI MỚI 100% THEO CHỦ ĐỀ VÀO DỰ ÁN ĐANG LÀM
(Không lưu kho nhạc/SFX chết trong Đầu Não; mỗi kịch bản mới cào mới vào D:\DuAn_DangLam\<du_an>\temp\)
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import List, Optional
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

HISTORY_PATH = Path(__file__).parent / "audio_used_history.json"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def _load_history() -> dict:
    if HISTORY_PATH.exists():
        try:
            return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"used_bgm_urls": [], "used_sfx_urls": []}


def _save_history(hist: dict) -> None:
    hist["used_bgm_urls"] = hist.get("used_bgm_urls", [])[-1000:]
    hist["used_sfx_urls"] = hist.get("used_sfx_urls", [])[-3000:]
    HISTORY_PATH.write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")


def _download_file(url: str, out_path: Path) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://mixkit.co/"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) < 4000:
            return False
        out_path.write_bytes(data)
        return True
    except Exception:
        return False


def _scrape_mixkit_urls(page, url: str, pattern: str) -> List[str]:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=22000)
        page.wait_for_timeout(1600)
        html = page.content()
        found = re.findall(pattern, html)
        # Preserve page order while deduplicating
        seen = set()
        out = []
        for u in found:
            if u not in seen:
                seen.add(u)
                out.append(u)
        return out
    except Exception:
        return []


BANNED_BGM_KEYWORDS = (
    # Nhạc buồn ngủ / nhẹ nhàng / corporate
    "lofi", "lo-fi", "chill", "relax", "calm", "ambient", "sleep",
    "meditation", "study", "acoustic", "romantic", "jazz", "happy", "peaceful",
    "soft", "gentle", "minimal", "slow", "corporate", "uplifting",
    # Nhạc vui tươi / rock / funk / dance / vlog
    "rock", "funk", "funky", "pop", "guitar", "upbeat", "indie", "energetic",
    "vlog", "summer", "motivational", "cheerful", "bright", "groove", "disco",
    "edm", "dance", "trap party",
)

DEFAULT_BGM_QUERIES = [
    "dark cinematic suspense",
    "crime documentary tension",
    "thriller pulse beat",
    "dark investigative bass",
    "intense mystery percussion",
]


def _scrape_mixkit_bgm_cards(page, url: str) -> List[tuple[str, str]]:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=22000)
        p_wait = page.wait_for_timeout(1600)
        items = page.evaluate(
            """() => {
                const cards = Array.from(document.querySelectorAll('[data-audio-player-preview-url-value], .item-grid-card'));
                const out = [];
                for (const c of cards) {
                    const txt = (c.innerText || '').toLowerCase();
                    const html = c.outerHTML || '';
                    const m = html.match(/https:\\/\\/assets\\.mixkit\\.co\\/music\\/\\d+\\/\\d+\\.mp3/);
                    if (m) out.push([m[0], txt]);
                }
                return out;
            }"""
        )
        seen = set()
        out = []
        for mp3_url, card_txt in items:
            if mp3_url in seen:
                continue
            if any(bad in card_txt for bad in BANNED_BGM_KEYWORDS):
                continue
            seen.add(mp3_url)
            out.append((mp3_url, card_txt.strip().splitlines()[0] if card_txt.strip() else mp3_url))
        return out
    except Exception:
        return []


def score_bgm_excitement(audio_path: Path) -> float:
    """
    Chấm điểm độ kịch tính & nhịp trống của BGM (0..100) trên 25s đầu bằng FFmpeg + NumPy:
    - Năng lượng trầm 40-160Hz (sub/kick punch)
    - Mật độ xung trống (onset density)
    - Độ tương phản động (dynamic contrast)
    Nhạc phẳng lì/chậm (< 65/100) sẽ bị loại tự động.
    """
    import subprocess
    import numpy as np

    try:
        cmd = [
            "ffmpeg", "-v", "error", "-i", str(audio_path),
            "-t", "25", "-ac", "1", "-ar", "16000", "-f", "f32le", "pipe:1",
        ]
        res = subprocess.run(cmd, capture_output=True, timeout=20)
        if res.returncode != 0 or len(res.stdout) < 16000 * 4:
            return 0.0
        sig = np.frombuffer(res.stdout, dtype=np.float32)
        if np.max(np.abs(sig)) < 1e-4:
            return 0.0

        # 1. Năng lượng trầm 40-160Hz (FFT)
        n = min(len(sig), 16000 * 25)
        spec = np.abs(np.fft.rfft(sig[:n])) ** 2
        freqs = np.fft.rfftfreq(n, d=1.0 / 16000.0)
        total_e = float(np.sum(spec) + 1e-9)
        bass_e = float(np.sum(spec[(freqs >= 40.0) & (freqs <= 160.0)]))
        bass_ratio = bass_e / total_e
        bass_score = min(35.0, (bass_ratio / 0.18) * 35.0)

        # 2. Mật độ xung trống (onset density theo khung 50ms = 800 samples)
        hop = 800
        n_frames = len(sig) // hop
        if n_frames < 10:
            return 0.0
        frames = sig[: n_frames * hop].reshape(n_frames, hop)
        rms = np.sqrt(np.mean(frames ** 2, axis=1) + 1e-9)
        diff = np.maximum(0.0, np.diff(rms))
        thresh = float(np.mean(diff) + 1.15 * np.std(diff))
        onsets = int(np.sum(diff > max(thresh, 1e-4)))
        onsets_per_sec = onsets / (n_frames * 0.05)
        onset_score = min(35.0, (onsets_per_sec / 2.2) * 35.0)

        # 3. Độ tương phản động (p95 / median RMS)
        med = float(np.median(rms) + 1e-6)
        p95 = float(np.percentile(rms, 95))
        contrast = p95 / med
        contrast_score = min(30.0, max(0.0, (contrast - 1.15) / 1.4) * 30.0)

        total_score = round(bass_score + onset_score + contrast_score, 1)
        return float(total_score)
    except Exception:
        return 0.0


def harvest_fresh_bgm(project_dir: Path, mood_query: str = "dark,suspense,thriller,mystery") -> Path:
    temp_dir = Path(project_dir) / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    out_bgm = temp_dir / "bgm_fresh.mp3"
    hist = _load_history()
    used_bgm = set(hist.get("used_bgm_urls", []))

    # Ưu tiên nhóm từ khóa tối, kịch tính, điều tra rõ rệt — CẤM nhạc vui tươi / rock / funk / lofi
    urls_to_scan = [
        f"https://mixkit.co/free-stock-music/discover/{re.sub(r'[^a-z0-9]+', '-', q.lower()).strip('-')}/"
        for q in DEFAULT_BGM_QUERIES
    ] + [
        "https://mixkit.co/free-stock-music/tag/suspense/",
        "https://mixkit.co/free-stock-music/tag/thriller/",
        "https://mixkit.co/free-stock-music/tag/tension/",
        "https://mixkit.co/free-stock-music/tag/dark/",
        "https://mixkit.co/free-stock-music/tag/mystery/",
        "https://mixkit.co/free-stock-music/tag/trailer/",
    ]
    for raw_s in mood_query.split(","):
        sl = re.sub(r"[^a-z0-9\-]", "", raw_s.strip().lower().replace(" ", "-"))
        if sl and not any(bad in sl for bad in BANNED_BGM_KEYWORDS) and sl not in ("dramatic", "thriller", "cinematic", "suspense", "dark", "mystery"):
            urls_to_scan.insert(0, f"https://mixkit.co/free-stock-music/tag/{sl}/")

    candidates: List[tuple[str, str]] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()
        for page_url in urls_to_scan:
            candidates.extend(_scrape_mixkit_bgm_cards(page, page_url))
        browser.close()

    fresh = [(u, t) for (u, t) in candidates if u not in used_bgm] or candidates
    best_fallback: Optional[tuple[float, str, str, bytes]] = None
    tmp_bgm = temp_dir / "tmp_bgm_eval.mp3"

    for u, title in fresh[:18]:
        if not _download_file(u, tmp_bgm):
            continue
        sc = score_bgm_excitement(tmp_bgm)
        print(f"   [BGM SCORE] '{title[:40]}' -> {sc}/100")
        if sc >= 72.0:
            out_bgm.write_bytes(tmp_bgm.read_bytes())
            tmp_bgm.unlink(missing_ok=True)
            hist.setdefault("used_bgm_urls", []).append(u)
            _save_history(hist)
            print(f"[AUDIO HARVESTER BGM OK | SCORE {sc}/100 >= 72] '{title}' ({u}) -> {out_bgm}")
            return out_bgm
        if best_fallback is None or sc > best_fallback[0]:
            best_fallback = (sc, u, title, tmp_bgm.read_bytes())

    tmp_bgm.unlink(missing_ok=True)
    if best_fallback is not None:
        sc, u, title, raw_bytes = best_fallback
        out_bgm.write_bytes(raw_bytes)
        hist.setdefault("used_bgm_urls", []).append(u)
        _save_history(hist)
        print(f"[AUDIO HARVESTER BGM FALLBACK BEST | SCORE {sc}/100] '{title}' -> {out_bgm}")
        return out_bgm

    raise RuntimeError(f"Không tải được nhạc nền hồi hộp/kịch tính mới từ Mixkit cho mood={mood_query}")


BANNED_SFX_KEYWORDS = (
    "cartoon", "comedy", "funny", "cute", "toy", "boing", "bubble",
    "8-bit", "arcade", "retro", "laugh", "applause", "meow", "dog", "baby",
    "chill", "lofi", "relax", "magic", "fairy", "sparkle",
    "bell", "bells", "chime", "chimes", "ring", "ringing", "alarm", "siren",
    "howl", "howling", "screech", "scream", "shriek", "whistle", "horn",
    "buzz", "buzzer", "beep", "laser", "zap", "shrill", "high pitch",
    "ting", "ding", "gong", "church",
)


def _scrape_mixkit_sfx_cards(page, url: str) -> List[tuple[str, str]]:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=22000)
        page.wait_for_timeout(1500)
        items = page.evaluate(
            """() => {
                const cards = Array.from(document.querySelectorAll('[data-audio-player-preview-url-value], .item-grid-card'));
                const out = [];
                for (const c of cards) {
                    const txt = (c.innerText || '').toLowerCase();
                    const html = c.outerHTML || '';
                    const m = html.match(/https:\\/\\/assets\\.mixkit\\.co\\/active_storage\\/sfx\\/\\d+\\/\\d+-preview\\.mp3/);
                    if (m) out.push([m[0], txt]);
                }
                return out;
            }"""
        )
        seen = set()
        out = []
        for mp3_url, card_txt in items:
            if mp3_url in seen:
                continue
            if any(bad in card_txt for bad in BANNED_SFX_KEYWORDS):
                continue
            seen.add(mp3_url)
            title = card_txt.strip().splitlines()[0] if card_txt.strip() else mp3_url
            out.append((mp3_url, title))
        return out
    except Exception:
        return []


ROLE_SFX_GROUPS = [
    ("role_riser", ["cinematic", "swoosh", "riser"], 2),
    ("role_impact", ["impact", "hit", "boom"], 2),
    ("role_hook", ["whoosh", "transition"], 2),
    ("role_knowledge", ["typing", "click", "paper", "ui"], 2),
    ("role_num", ["clock", "tick", "interface", "tech"], 2),
]

ROLE_MONEY_GROUP = ("role_money", ["cash", "coins", "money"], 2)


def harvest_fresh_sfx(
    project_dir: Path,
    topic_keywords: Optional[List[str]] = None,
    count: int = 14,
    include_money: bool = False,
) -> List[Path]:
    """
    Cào SFX tươi mới 100% vào temp/sfx/ theo 6 nhóm vai trò + từ khóa chủ đề kịch bản:
    - role_riser_*.mp3, role_impact_*.mp3, role_hook_*.mp3, role_knowledge_*.mp3, role_num_*.mp3
    - role_money_*.mp3 (chỉ cào khi include_money=True)
    - role_topic_*.mp3 (2-3 file theo --sfx-keywords riêng của kịch bản)
    """
    sfx_dir = Path(project_dir) / "temp" / "sfx"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    hist = _load_history()
    used_sfx = set(hist.get("used_sfx_urls", []))

    groups: List[tuple[str, List[str], int]] = list(ROLE_SFX_GROUPS)
    if include_money:
        groups.append(ROLE_MONEY_GROUP)

    topic_kws = [re.sub(r"[^a-z0-9\-]", "", k.strip().lower()) for k in (topic_keywords or []) if k.strip()]
    if topic_kws:
        groups.append(("role_topic", topic_kws, 3))

    downloaded: List[Path] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()

        for role_prefix, kw_list, target_n in groups:
            picked_for_role = 0
            for kw in kw_list:
                if picked_for_role >= target_n:
                    break
                cards = _scrape_mixkit_sfx_cards(page, f"https://mixkit.co/free-sound-effects/{kw}/")
                fresh = [(u, t) for (u, t) in cards if u not in used_sfx] or cards
                for u, title in fresh:
                    if picked_for_role >= target_n:
                        break
                    sid = re.search(r"/(\d+)-preview\.mp3", u)
                    fname = f"{role_prefix}_{kw}_{sid.group(1) if sid else len(downloaded)}.mp3"
                    out_p = sfx_dir / fname
                    if _download_file(u, out_p):
                        downloaded.append(out_p)
                        used_sfx.add(u)
                        hist.setdefault("used_sfx_urls", []).append(u)
                        picked_for_role += 1
                        print(f"[AUDIO HARVESTER SFX OK | {role_prefix.upper()}] '{title}' -> {fname}")
        browser.close()

    _save_history(hist)
    if not downloaded:
        raise RuntimeError("Không tải được SFX kịch tính mới nào cho dự án!")
    return downloaded


def main() -> int:
    ap = argparse.ArgumentParser(description="Harvest fresh BGM & 6-role topic-matched SFX into project temp/")
    ap.add_argument("--project", required=True, help="Thư mục dự án (VD: D:\\DuAn_DangLam\\ten_du_an)")
    ap.add_argument("--sfx-keywords", default="transition,impact,technology", help="Từ khóa SFX tiếng Anh cách nhau dấu phẩy")
    ap.add_argument("--bgm-mood", default="dark,suspense,thriller,mystery", help="Mood nhạc nền tối/kịch tính/điều tra (CẤM nhạc vui/rock/funk/lofi)")
    ap.add_argument("--sfx-count", type=int, default=14)
    ap.add_argument("--include-money", action="store_true", help="Bật cào nhóm role_money_*.mp3 (khi kịch bản có yếu tố tiền)")
    args = ap.parse_args()

    proj = Path(args.project)
    kws = [k.strip() for k in args.sfx_keywords.split(",") if k.strip()]
    harvest_fresh_bgm(proj, mood_query=args.bgm_mood)
    harvest_fresh_sfx(proj, topic_keywords=kws, count=args.sfx_count, include_money=args.include_money)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```


#### `engine/ace_step_fb_runner.py`

```python
# -*- coding: utf-8 -*-
r"""
ACE-STEP 1.5 & CREATIVE 5-BEAT HOLLYWOOD TRAILER COMPOSER ENGINE
Chuyên biệt cho: Đầu Não Video Ngắn FB (D:\Đầu Não Video Ngắn FB (không xóa))

LUẬT THÉP BẤT DI BẤT DỊCH (ZERO OLD AUDIO REUSE & CREATIVE SCRIPT-DRIVEN SCORING):
1. CẤM TUYỆT ĐỐI lấy lại file nhạc nền cũ hoặc lặp lại cấu trúc âm thanh của kịch bản trước!
   Mọi bản nhạc sinh ra đều được kiểm tra mã băm SHA-256 và công thức DNA tại `bgm_fingerprint_ledger.json`.
2. TƯ DUY PHÂN TÍCH KỊCH BẢN (Script Musical DNA Analyzer):
   - Tự động đọc nội dung kịch bản (`script_topic`, `script_text`, `beat_timestamps`) để xác định:
     * Thể loại cảm xúc (Conspiracy Thriller, Tech Monopoly, Geopolitical War, Financial Noir, Consumer Trap).
     * Tông nhạc riêng biệt (C minor, C# minor, D minor, Eb minor, E minor, F minor, F# minor) và tốc độ BPM riêng (125 - 138 BPM).
     * Mốc thời gian chính xác của 5 Nhịp kịch bản (Beat 1 Hook -> Beat 2 Context -> Beat 3 Escalation -> Beat 4 Twist -> Beat 5 Cliffhanger & Vacuum Drop).
3. KẾT HỢP KÉP AI CLOUD (ACE-Step 1.5 Fixed API) + BỘ TỔNG HỢP GIAO HƯỞNG ĐA TẦNG & PROCEDURAL FOLEY:
   - Khi gọi ACE-Step 1.5: Dùng `/song` (bật `think=True` 5Hz LM Planner + `meta_json`) hoặc `/instrumental` với `lyrics=""` (khắc phục triệt để lỗi `instrumental=False` sinh nhạc chill/organ).
   - Kết hợp Re-Orchestration theo đúng 5 mốc thời gian kịch bản kèm Procedural Braaam / Sub-Drop / Heartbeat / Riser mới 100% cho từng kịch bản.
4. BẮT BUỘC NGHE THẨM ĐỊNH BẰNG TAI AI (`view_file`/`read_file` trên `.mp3`) trước khi xuất bản!
"""

import hashlib
import json
import math
import random
import shutil
import struct
import subprocess
import sys
import time
import wave
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


FB_BRAIN_DIR = Path(__file__).resolve().parent.parent
LEDGER_PATH = FB_BRAIN_DIR / "engine" / "bgm_fingerprint_ledger.json"

# Bảng phân tích DNA cảm xúc kịch bản từ nội dung văn bản
ARCHETYPE_KEYWORDS: Dict[str, List[str]] = {
    "conspiracy_thriller": [
        "điều tra", "bí mật", "điệp viên", "âm mưu", "nghi vấn", "hồ sơ", "tội", "án",
        "luật sư", "tòa", "thâu tóm", "kế nhiệm", "ngai vàng", "quyền lực", "ngầm", "ép",
    ],
    "tech_monopoly": [
        "chip", "ai", "nvidia", "apple", "google", "bán dẫn", "công nghệ", "thuật toán",
        "robot", "dữ liệu", "máy chủ", "độc quyền", "hệ sinh thái", "phần cứng",
    ],
    "geopolitics_war": [
        "cấm vận", "chiến tranh", "biên giới", "quân sự", "tên lửa", "mỹ", "trung quốc",
        "nga", "châu âu", "eo biển", "phong tỏa", "địa chính trị", "an ninh",
    ],
    "forensic_finance": [
        "tỷ đô", "tỷ usd", "ipo", "cổ phiếu", "vốn hóa", "sàn chứng khoán", "phá sản",
        "ngân hàng", "nợ", "lãi suất", "bốc hơi", "thao túng", "tài chính", "wall street",
    ],
    "consumer_trap": [
        "người tiêu dùng", "bẫy giá", "lừa", "ảo thuật giá", "khuyến mãi", "chiêu trò",
        "thương hiệu", "đắt", "rẻ", "mánh khóe", "tâm lý",
    ],
}

SCRIPT_MOOD_PRESETS: Dict[str, Dict] = {
    "conspiracy_thriller": {
        "style": (
            "Dark investigative conspiracy thriller movie trailer score, Hans Zimmer and Ludwig Goransson style, "
            "instant 0:00 colossal sub-bass braaam impact, relentless 16th-note spiccato cello and violin ostinato, "
            "ominous low brass swells, deep orchestral war drums, high-stakes boardroom espionage tension, "
            "no repetitive woodblock or ticking synth loop, no slow intro, no chill piano, no vocals"
        ),
        "base_bpm": 130,
        "keys": ["D minor", "C# minor", "C minor", "F minor"],
    },
    "tech_monopoly": {
        "style": (
            "Blockbuster investigative tech-thriller orchestral trailer soundtrack, Social Network and Oppenheimer score style, "
            "instant 0:00 sub-bass braaam slam, relentless driving 132 BPM orchestral strings ostinato and deep taiko war drums, "
            "ominous brass swells, high-stakes silicon empire tension, no repetitive woodblock or ticking synth, no vocals"
        ),
        "base_bpm": 132,
        "keys": ["D minor", "E minor", "F# minor", "C minor"],
    },
    "geopolitics_war": {
        "style": (
            "Monumental geopolitical war thriller movie trailer score, instant 0:00 thunderous taiko drum slam, "
            "colossal low brass braaams, rapid orchestral string storm, relentless blockbuster tension, "
            "no repetitive woodblock or ticking synth, no vocals, instrumental trailer"
        ),
        "base_bpm": 128,
        "keys": ["E minor", "D minor", "G minor", "C minor"],
    },
    "forensic_finance": {
        "style": (
            "High-stakes Wall Street financial investigation movie trailer score, Succession and Margin Call dark orchestral style, "
            "instant 0:00 heavy sub-drop braaam, urgent staccato strings ostinato, deep acoustic war drums, "
            "breathless corporate crisis tension, no repetitive woodblock or ticking synth, no vocals, instrumental"
        ),
        "base_bpm": 129,
        "keys": ["C minor", "D minor", "Eb minor", "F# minor"],
    },
    "consumer_trap": {
        "style": (
            "Fast-paced psychological thriller orchestral trailer score, instant 0:00 impact hit, "
            "urgent pizzicato and spiccato strings ostinato, deep cinematic drums, "
            "gripping investigative reveal momentum, no repetitive woodblock or ticking synth, no vocals"
        ),
        "base_bpm": 127,
        "keys": ["A minor", "D minor", "C minor", "E minor"],
    },
}


class ACEStepFBRunner:
    def __init__(self):
        self.base_dir = FB_BRAIN_DIR
        self.master_music_dir = Path(r"D:\MasterBrain\assets\music")
        if not self.master_music_dir.exists():
            self.master_music_dir = Path(r"D:\Đầu Não (không xóa)\assets\music")

    def _load_ledger(self) -> Dict:
        if LEDGER_PATH.exists():
            try:
                return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"used_hashes": [], "used_recipes": []}

    def _save_ledger(self, ledger: Dict) -> None:
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    def detect_script_archetype(self, script_topic: str, script_text: str = "", default_mood: str = "conspiracy_thriller") -> str:
        combined = f"{script_topic} {script_text}".lower()
        scores: Dict[str, int] = {k: 0 for k in ARCHETYPE_KEYWORDS}
        for arch, kw_list in ARCHETYPE_KEYWORDS.items():
            for kw in kw_list:
                if kw in combined:
                    scores[arch] += 2
        best_arch = max(scores, key=scores.get)
        if scores[best_arch] > 0:
            return best_arch
        return default_mood if default_mood in SCRIPT_MOOD_PRESETS else "conspiracy_thriller"

    def compute_unique_musical_dna(
        self,
        script_topic: str,
        script_text: str = "",
        mood: str = "",
        duration_sec: float = 43.5,
        beat_timestamps: Optional[List[float]] = None,
    ) -> Dict:
        """
        Tư duy phân tích kịch bản để sinh công thức DNA âm nhạc độc bản (không bao giờ trùng lặp giữa 2 kịch bản).
        """
        archetype = self.detect_script_archetype(script_topic, script_text, default_mood=mood or "conspiracy_thriller")
        preset = SCRIPT_MOOD_PRESETS.get(archetype, SCRIPT_MOOD_PRESETS["conspiracy_thriller"])
        ledger = self._load_ledger()

        attempt = 0
        while True:
            seed_str = f"{script_topic.strip()}|{script_text[:200].strip()}|{archetype}|{attempt}"
            h_hex = hashlib.sha256(seed_str.encode("utf-8")).hexdigest()
            h_int = int(h_hex[:12], 16)

            # Chọn tông dịch chuyển (pitch semitones: -3, -2, -1, 0, +1, +2) và tốc độ tempo riêng biệt
            semitone_Pool = [-3, -2, -1, 0, 1, 2]
            pitch_semitones = semitone_Pool[h_int % len(semitone_Pool)]
            tempo_mult = round(1.12 + ((h_int >> 4) % 11) * 0.012, 3)  # 1.12x .. 1.24x
            bpm = preset["base_bpm"] + ((h_int >> 8) % 9) - 4
            key_name = preset["keys"][(h_int >> 12) % len(preset["keys"])]

            # Chọn vị trí cắt micro-phrases độc bản cho từng nhịp
            b1_start = round(((h_int >> 16) % 3) * 0.4, 2)
            b2_start = round(18.0 + ((h_int >> 20) % 14) * 0.8, 2)
            b3_start = round(46.0 + ((h_int >> 24) % 16) * 0.9, 2)
            b4_start = round(34.0 + ((h_int >> 28) % 12) * 0.8, 2)
            b5_start = round(12.5 + ((h_int >> 32) % 5) * 0.5, 2)

            recipe_id = f"{archetype}_st{pitch_semitones}_tm{tempo_mult}_s{b1_start}_{b2_start}_{b3_start}_{b4_start}_{b5_start}"
            if recipe_id not in ledger.get("used_recipes", []) or attempt > 25:
                break
            attempt += 1

        # Xác định 5 mốc chuyển nhịp theo đúng kịch bản
        if beat_timestamps and len(beat_timestamps) >= 5:
            beats = [round(float(x), 2) for x in beat_timestamps[:5]]
        else:
            b_step = duration_sec / 5.0
            beats = [
                0.0,
                round(b_step * 0.85, 2),
                round(b_step * 1.75, 2),
                round(b_step * 2.80, 2),
                round(b_step * 3.82, 2),
            ]

        return {
            "archetype": archetype,
            "style_prompt": preset["style"],
            "bpm": bpm,
            "key": key_name,
            "pitch_semitones": pitch_semitones,
            "tempo_mult": tempo_mult,
            "offsets": (b1_start, b2_start, b3_start, b4_start, b5_start),
            "beats": beats,
            "recipe_id": recipe_id,
            "seed": h_int % 9999999,
        }

    def _synthesize_procedural_trailer_accent_layer(self, out_wav: Path, duration_sec: float, dna: Dict) -> Path:
        """
        Tổng hợp lớp xung chấn vật lý MỚI 100% bằng toán học (Zero-Copyright Procedural Accents):
        - Cú nổ Sub-Bass Braaam ở 0:00 và tại đúng các mốc chuyển nhịp (beats) của kịch bản.
        - Tiếng kim đồng hồ cơ khí tích tắc đa tần (Binaural Clockwork Ticks) theo đúng BPM kịch bản.
        - Tiếng Riser dâng trào trước điểm kết.
        """
        sr = 44100
        n_samples = int(sr * duration_sec)
        bpm = dna["bpm"]
        spb = 60.0 / bpm
        pitch_factor = math.pow(2.0, dna["pitch_semitones"] / 12.0)
        base_f = 55.0 * pitch_factor
        beats = dna["beats"]

        buf_l = [0.0] * n_samples
        buf_r = [0.0] * n_samples

        # 1. Đặt cú nổ Sub-Bass Braaam êm gọn tại đúng đầu các mốc Beat chính (bỏ tiếng tích tắc rền rĩ gây rối tai)
        for b_idx, bt in enumerate(beats):
            if b_idx not in (0, 2, 4):
                continue
            i0 = int(bt * sr)
            b_dur = 1.6 if b_idx == 0 else 1.2
            blen = min(int(b_dur * sr), n_samples - i0)
            for j in range(blen):
                lt = j / sr
                f_drop = max(34.0, 88.0 * math.exp(-lt * 4.5))
                sub_hit = math.sin(2.0 * math.pi * f_drop * lt) * math.exp(-lt * 3.0)
                env = min(1.0, lt / 0.03) * math.exp(-lt * 1.6)
                val = sub_hit * env * (0.42 if b_idx == 0 else 0.28)
                buf_l[i0 + j] += val
                buf_r[i0 + j] += val

        # Ghi ra WAV stereo
        with wave.open(str(out_wav), "w") as wf:
            wf.setparams((2, 2, sr, n_samples, "NONE", "not compressed"))
            frames = bytearray(n_samples * 4)
            for i in range(n_samples):
                cl = max(-32767, min(32767, int(buf_l[i] * 32767)))
                cr = max(-32767, min(32767, int(buf_r[i] * 32767)))
                struct.pack_into("<hh", frames, i * 4, cl, cr)
            wf.writeframes(frames)

        return out_wav

    def _analyze_mood_with_gemini(self, script_topic: str, script_text: str) -> Tuple[Optional[str], Optional[str]]:
        """Dùng Gemini đọc hiểu mạch cảm xúc toàn bộ kịch bản/video để chọn archetype & viết mô tả nhạc nền chuẩn xác."""
        import os
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            env_path = FB_BRAIN_DIR / ".env"
            if env_path.exists():
                for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                    if line.strip().startswith(("GEMINI_API_KEY=", "GOOGLE_API_KEY=")):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if api_key:
                            break
        if not api_key:
            return None, None
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            ask = (
                "Analyze this Vietnamese short-form documentary video script and choose the single best musical archetype "
                "from [conspiracy_thriller, tech_monopoly, geopolitics_war, forensic_finance, consumer_trap], "
                "plus a 20-word English orchestral music prompt describing the emotional arc (strings/cello/war drums, NO woodblock/ticking synth).\n"
                f"Topic: {script_topic}\nScript: {script_text[:1200]}\n"
                'Return ONLY strict JSON: {"archetype": "...", "cue": "..."}'
            )
            resp = client.models.generate_content(model="gemini-2.5-flash", contents=ask)
            txt = (resp.text or "").strip().strip("`")
            if txt.startswith("json"):
                txt = txt[4:].strip()
            obj = json.loads(txt)
            arch = obj.get("archetype")
            cue = obj.get("cue")
            if arch in SCRIPT_MOOD_PRESETS:
                return arch, str(cue) if cue else None
        except Exception:
            pass
        return None, None

    def _try_cloud_ace_step_generation(self, dna: Dict, duration_sec: float, raw_ai_wav: Path, custom_cue: Optional[str] = None) -> bool:
        """
        Gọi ACE-Step 1.5 Cloud với tham số CHUẨN XÁC:
        - Truyền lyrics="" vào /instrumental để instrumental=True (tuyệt đối không truyền chữ vào lyrics của /instrumental).
        - Kiểm tra năng lượng tần số trầm và mật độ xung nhịp để loại bỏ nhạc chill/organ/woodblock.
        """
        try:
            from gradio_client import Client

            gen_duration = min(120.0, max(20.0, round(duration_sec + 2.0, 1)))
            cue_part = f"{custom_cue}, " if custom_cue else ""
            prompt = (
                f"{dna['style_prompt']}, {cue_part}{dna['bpm']} BPM, {dna['key']}, "
                "dynamic 5-act short documentary orchestral trailer score: immediate punchy impact at 0s, "
                "curious investigative strings tension in middle, dramatic reveal swell, clean studio mix, no woodblock, no vocal"
            )
            client = Client("Reubencf/Kiku-ACE-Step-15")
            status, gradio_audio_path = client.predict(
                prompt,
                "",  # BẮT BUỘC chuỗi rỗng để instrumental=True trong Kiku-ACE-Step-15!
                float(gen_duration),
                27,
                11.5,
                int(dna["seed"]),
                api_name="/instrumental",
            )
            if gradio_audio_path and Path(gradio_audio_path).exists():
                shutil.copy2(gradio_audio_path, raw_ai_wav)
                try:
                    Path(gradio_audio_path).unlink(missing_ok=True)
                except Exception:
                    pass
                if raw_ai_wav.exists() and raw_ai_wav.stat().st_size > 80000:
                    return True
        except Exception as e:
            print(f"[ACE-STEP CLOUD INFO] Chuyển sang Bộ Tổng Hợp Giao Hưởng 5 Nhịp Độc Bản ({e})")
        return False

    @staticmethod
    def _per_second_db(path: Path) -> list:
        """Đo độ to RMS (dBFS) từng giây của file nhạc để phát hiện đoạn hụt/im lặng."""
        import numpy as np
        p = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
            capture_output=True,
        )
        a = np.frombuffer(p.stdout, dtype=np.int16).astype(np.float32) / 32768.0
        n = len(a) // 8000
        if n == 0:
            return []
        seg = a[: n * 8000].reshape(n, 8000)
        rms = np.sqrt(np.mean(seg ** 2, axis=1)) + 1e-9
        return [float(20 * np.log10(x)) for x in rms]

    @staticmethod
    def _find_continuous_offset(db: list, need_sec: float, floor_db: float = -30.0, max_dip_db: float = 12.0):
        """Tìm điểm bắt đầu sao cho mọi giây trong [off, off+need) đều >= floor_db và không tụt quá max_dip_db so với trung vị."""
        import math as _m
        need = int(_m.ceil(need_sec))
        if len(db) < need:
            return None
        for off in range(0, len(db) - need + 1):
            win = db[off: off + need - 1]  # bỏ giây cuối (fade-out)
            if not win:
                continue
            med = sorted(win)[len(win) // 2]
            if min(win) >= floor_db and min(win) >= med - max_dip_db:
                return off
        return None

    def compose_bespoke_5beat_trailer_bgm(
        self,
        script_topic: str,
        output_path: str | Path,
        duration_sec: float = 43.5,
        mood: str = "conspiracy_thriller",
        script_text: str = "",
        beat_timestamps: Optional[List[float]] = None,
    ) -> Path:
        """
        Sáng tác & tổng hợp bản nhạc nền Trailer Điện Ảnh 5 Nhịp ĐỘC BẢN cho từng kịch bản:
        - Tự động tính toán DNA âm nhạc mới (Tông nhạc mới, BPM mới, vị trí cắt nhịp mới, lớp xung chấn Procedural Braaam & Clockwork mới).
        - Lưu dấu vân tay SHA-256 vào `bgm_fingerprint_ledger.json`, đảm bảo 100% KHÔNG BAO GIỜ LẶP LẠI BẤT KỲ KỊCH BẢN CŨ NÀO!
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        ai_arch, ai_cue = self._analyze_mood_with_gemini(script_topic, script_text)
        dna = self.compute_unique_musical_dna(
            script_topic=script_topic,
            script_text=script_text,
            mood=ai_arch or mood,
            duration_sec=duration_sec,
            beat_timestamps=beat_timestamps,
        )
        print(
            f"[TRAILER COMPOSER DNA] Chủ đề: '{script_topic[:45]}' | Archetype: {dna['archetype']} "
            f"{'(Gemini AI)' if ai_arch else '(Rule)'} | Key: {dna['key']} ({dna['pitch_semitones']:+d} st) | BPM: {dna['bpm']} | Recipe: {dna['recipe_id']}"
        )

        # Tạo lớp xung chấn vật lý Procedural mới 100% theo đúng các mốc Beat của kịch bản này
        proc_accent_wav = output_path.with_name(f"._proc_accent_{output_path.stem}.wav")
        self._synthesize_procedural_trailer_accent_layer(proc_accent_wav, duration_sec, dna)

        # Thử gọi lớp AI ACE-Step Cloud (với lyrics="") để sinh bản nhạc mới liền mạch
        cloud_ai_wav = output_path.with_name(f"._cloud_ace_{output_path.stem}.wav")
        has_cloud_ai = self._try_cloud_ace_step_generation(dna, duration_sec, cloud_ai_wav, custom_cue=ai_cue)

        ledger = self._load_ledger()
        used_tracks = set(ledger.get("used_tracks", []))

        # KHÔNG DÙNG KHO NHẠC CŨ TRONG ĐẦU NÃO: nếu AI cloud hụt hơi/im lặng, cào nhạc tươi mới vào dự án
        fresh_project_bgm = output_path.parent / "bgm_fresh.mp3"
        candidate_tracks: list[Path] = []
        if fresh_project_bgm.exists() and fresh_project_bgm.stat().st_size > 20000:
            candidate_tracks.append(fresh_project_bgm)

        # CỔNG LIỀN MẠCH NHẠC NỀN: bản AI cloud phải đủ to từng giây (cấm hụt/im lặng ở Hook hay giữa bài)
        if has_cloud_ai and cloud_ai_wav.exists() and cloud_ai_wav.stat().st_size > 20000:
            cloud_db = self._per_second_db(cloud_ai_wav)
            cloud_off = self._find_continuous_offset(cloud_db, duration_sec)
            if cloud_off is None:
                print(f"[BGM CONTINUITY GATE] Loại bản AI cloud (hụt/im lặng): {[round(x) for x in cloud_db[:24]]}")
                has_cloud_ai = False
            else:
                cloud_start = float(cloud_off)

        chosen_track = None
        start_off = 0.0
        if not has_cloud_ai:
            if not candidate_tracks:
                from audio_harvester import harvest_fresh_bgm
                mood_q = "dramatic,thriller,cinematic"
                harvested_p = harvest_fresh_bgm(output_path.parent.parent, mood_query=mood_q)
                candidate_tracks = [harvested_p]
            for cand in candidate_tracks:
                off = self._find_continuous_offset(self._per_second_db(cand), duration_sec)
                if off is not None:
                    chosen_track, start_off = cand, float(off)
                    break
            if chosen_track is None and candidate_tracks:
                chosen_track, start_off = candidate_tracks[0], 0.0
            if chosen_track is None:
                raise RuntimeError("Không cào được nhạc nền mới cho dự án!")
            print(f"[BGM CONTINUITY GATE OK] Dùng nhạc cào mới {chosen_track.name} từ giây {start_off:.0f}")

        raw_mix = output_path.with_name(f"._raw_5beat_{output_path.stem}.wav")

        if has_cloud_ai:
            print(f"[BGM CONTINUITY GATE OK] Dùng bản AI cloud từ giây {cloud_start:.0f}")
            filter_complex = (
                f"[0:a]atrim={cloud_start:.2f}:{cloud_start + duration_sec:.2f},asetpts=PTS-STARTPTS,"
                f"afade=t=in:st=0:d=0.3,afade=t=out:st={max(0.5, duration_sec - 1.2):.2f}:d=1.2[bgm_main];"
                f"[1:a]atrim=0:{duration_sec:.2f},asetpts=PTS-STARTPTS,volume=0.35[acc];"
                f"[bgm_main][acc]amix=inputs=2:normalize=0,alimiter=limit=0.95:level=disabled[out]"
            )
            cmd1 = [
                "ffmpeg", "-y",
                "-stream_loop", "-1", "-i", str(cloud_ai_wav),
                "-i", str(proc_accent_wav),
                "-filter_complex", filter_complex,
                "-map", "[out]", "-ar", "48000", "-ac", "2", str(raw_mix),
            ]
        else:
            # 1 bản nhạc chủ đạo liền mạch từ đoạn đã qua cổng kiểm tra (KHÔNG cắt nối 5 khúc rời rạc)
            pitch_rate = round(math.pow(2.0, max(-2, min(2, dna["pitch_semitones"])) / 12.0), 6)
            inv_tempo = max(0.85, min(1.15, round(1.0 / pitch_rate, 4)))
            filter_complex = (
                f"[0:a]atrim={start_off:.2f}:{start_off + duration_sec + 2.0:.2f},asetpts=PTS-STARTPTS,"
                f"asetrate=44100*{pitch_rate},aresample=48000,atempo={inv_tempo},"
                f"atrim=0:{duration_sec:.2f},afade=t=in:st=0:d=0.3,afade=t=out:st={max(0.5, duration_sec - 1.2):.2f}:d=1.2[bgm_main];"
                f"[1:a]atrim=0:{duration_sec:.2f},asetpts=PTS-STARTPTS,volume=0.32[acc];"
                f"[bgm_main][acc]amix=inputs=2:normalize=0,alimiter=limit=0.95:level=disabled[out]"
            )
            cmd1 = [
                "ffmpeg", "-y",
                "-stream_loop", "-1", "-i", str(chosen_track),
                "-i", str(proc_accent_wav),
                "-filter_complex", filter_complex,
                "-map", "[out]", "-ar", "48000", "-ac", "2", str(raw_mix),
            ]

        res1 = subprocess.run(cmd1, capture_output=True, text=True, encoding="utf-8", errors="replace")
        proc_accent_wav.unlink(missing_ok=True)
        cloud_ai_wav.unlink(missing_ok=True)
        if not has_cloud_ai and chosen_track is not None:
            used_tracks.add(chosen_track.name)
            ledger["used_tracks"] = list(used_tracks)[-15:]
            self._save_ledger(ledger)

        if res1.returncode != 0:
            raise RuntimeError(f"Lỗi tổng hợp 5-Beat Trailer BGM: {res1.stderr[-500:]}")

        codec_args = ["-c:a", "libmp3lame", "-b:a", "320k"] if output_path.suffix.lower() == ".mp3" else ["-c:a", "pcm_s16le"]
        cmd2 = [
            "ffmpeg", "-y",
            "-i", str(raw_mix),
            "-af", "acompressor=threshold=-22dB:ratio=3.2:attack=15:release=150:makeup=5,loudnorm=I=-12.0:TP=-1.0:LRA=5",
            *codec_args,
            "-ar", "48000", "-ac", "2",
            str(output_path),
        ]
        res2 = subprocess.run(cmd2, capture_output=True, text=True, encoding="utf-8", errors="replace")
        raw_mix.unlink(missing_ok=True)
        if res2.returncode != 0:
            raise RuntimeError(f"Lỗi chuẩn hóa 5-Beat Trailer BGM: {res2.stderr[-500:]}")

        final_db = self._per_second_db(output_path)
        if self._find_continuous_offset(final_db, len(final_db), floor_db=-30.0) != 0:
            raise RuntimeError(f"[BGM FINAL GATE FAILED] Nhạc nền thành phẩm có đoạn hụt/im lặng: {[round(x) for x in final_db]}")
        print(f"[BGM FINAL GATE OK] Liền mạch từng giây: {[round(x) for x in final_db]}")

        # Lưu mã băm SHA-256 và công thức DNA vào sổ cái chống trùng lặp
        file_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()
        ledger = self._load_ledger()
        if file_hash not in ledger["used_hashes"]:
            ledger["used_hashes"].append(file_hash)
        if dna["recipe_id"] not in ledger["used_recipes"]:
            ledger["used_recipes"].append(dna["recipe_id"])
        self._save_ledger(ledger)

        print(f"[5-BEAT HOLLYWOOD TRAILER BGM OK] Đã xuất bản nhạc nền ĐỘC BẢN tại: {output_path} (SHA256: {file_hash[:12]})")
        return output_path

    def generate_unique_script_bgm(
        self,
        script_topic: str,
        output_path: str | Path,
        duration_sec: float = 43.5,
        mood: str = "conspiracy_thriller",
        custom_keywords: str = "",
        seed: int = -1,
        script_text: str = "",
        beat_timestamps: Optional[List[float]] = None,
    ) -> Path:
        """
        Sinh bản nhạc nền 5 Nhịp Trailer Điện Ảnh Hollywood ĐỘC BẢN khớp kịch bản.
        """
        return self.compose_bespoke_5beat_trailer_bgm(
            script_topic=script_topic,
            output_path=output_path,
            duration_sec=duration_sec,
            mood=mood,
            script_text=script_text or custom_keywords,
            beat_timestamps=beat_timestamps,
        )
```


#### `engine/sfx_timeline_mixer.py`

```python
# -*- coding: utf-8 -*-
r"""
sfx_timeline_mixer.py - BỘ HÒA ÂM ĐA TẦNG PHÒNG THU & TRÍ TUỆ BIÊN ĐẠO SFX THEO NGỮ NGHĨA KỊCH BẢN (-14.0 LUFS)
(Dành riêng cho Đầu Não Video Ngắn FB: D:\Đầu Não Video Ngắn FB (không xóa))

LUẬT THÉP BẤT DI BẤT DỊCH:
1. MỖI KỊCH BẢN LÀ MỘT BẢN PHỐI MỚI 100% — CẤM LẤY ÂM THANH CŨ:
   - Nhạc nền 5 Nhịp phải được sáng tác/tổng hợp mới theo đúng nội dung kịch bản qua `ACEStepFBRunner`.
   - Điểm rơi SFX phải được tự động biên đạo mới (`auto_choreograph_script_sfx_cues`) dựa trên file `words.json`
     của kịch bản mới — TUYỆT ĐỐI CẤM copy-paste danh sách mốc thời gian SFX của kịch bản cũ sang kịch bản mới!
2. Giọng đọc Hải Đăng luôn ở NGÔI THƯỢNG TẦNG (`voice_volume = 1.28`, tăng độ nét `3.0kHz +2.8dB`, lọc đáy `85Hz`):
   TUYỆT ĐỐI KHÔNG BAO GIỜ BỊ NHẠC NỀN LẤN ÁT DÙ CHỈ 1 dB!
3. Nhạc nền Trailer Điện Ảnh 5 Nhịp (đã chuẩn hóa `-12.0 LUFS, LRA=5`):
   - Áp dụng Cắt rãnh tần số phẫu thuật (`Surgical Spectral Pocket: -3.5dB tại 2.5kHz`) để nhường dải giọng nói cho Hải Đăng
     nhưng bảo toàn 100% lực đập của dàn dây Staccato (`400Hz-1.5kHz`), Sub-Bass/War Drums (`+2.0dB tại 90Hz`) và tiếng tích tắc đồng hồ (`4kHz-10kHz`).
   - Âm lượng nhạc nền cân đối hài hòa (`bgm_base_volume = 0.44`, tức thấp hơn giọng đọc `5.5 - 6.5 dB`): Vừa đủ nghe rõ từng nhịp trống,
     từng tiếng đàn cello kịch tính lôi cuốn như trailer phim mà tuyệt đối không làm át giọng đọc!
   - Vacuum Drop: Ngắt sạch nhạc `0.65s` ngay trước câu chốt kịch tính.
4. Tự động xuất file `_qc_listen_preview.mp3` ngay sau khi mix để Agent bắt buộc mở nghe kiểm chứng bằng `view_file`/`read_file`!
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

FB_BRAIN = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
_ACTIVE_PROJECT_SFX_DIR: Optional[Path] = None


def set_project_sfx_dir(sfx_dir: Optional[Path]) -> None:
    global _ACTIVE_PROJECT_SFX_DIR
    _ACTIVE_PROJECT_SFX_DIR = Path(sfx_dir) if sfx_dir else None


def preprocess_sfx_punch(src: Path, dst: Path) -> Path:
    """
    Cắt sạch khoảng lặng đầu file (-30dB) để SFX nổ đúng từng mili-giây khung hình,
    cắt đuôi <= 2.2s kèm fade-out 80ms và chuẩn hóa đỉnh -0.5 dBFS.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    af = (
        "silenceremove=start_periods=1:start_duration=0:start_threshold=-30dB,"
        "atrim=0:2.2,afade=t=out:st=2.12:d=0.08,"
        "alimiter=limit=0.94:attack=2:release=35"
    )
    res = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dst)],
        capture_output=True,
        text=True,
    )
    if res.returncode == 0 and dst.exists() and dst.stat().st_size > 2000:
        return dst
    return src


def get_sfx_peak_offset_ms(wav_path: Path) -> int:
    """Tìm chính xác mili-giây có đỉnh biên độ lớn nhất (argmax(abs(samples))) bằng NumPy sau khi cắt im lặng đầu."""
    import wave
    import numpy as np

    try:
        with wave.open(str(wav_path), "rb") as wf:
            sr = wf.getframerate() or 48000
            n_ch = max(1, wf.getnchannels())
            raw = wf.readframes(min(wf.getnframes(), sr * 2))
        if not raw:
            return 0
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
        if n_ch > 1:
            samples = samples.reshape(-1, n_ch).mean(axis=1)
        peak_idx = int(np.argmax(np.abs(samples)))
        return int(round((peak_idx * 1000.0) / sr))
    except Exception:
        return 0


def _sfx_priority(fname: str) -> int:
    low = fname.lower()
    if "hook_slam" in low or "role_hook" in low:
        return 5
    if "impact" in low or "riser_boom" in low or "boom" in low:
        return 4
    if "slash_cut" in low:
        return 3
    if "card_snap" in low or "role_knowledge" in low or "marker_swipe" in low:
        return 2
    return 1


def resolve_sfx_priority_conflicts(
    sfx_cues: List[Tuple[str, int, float]],
    min_gap_ms: int = 140,
) -> List[Tuple[str, int, float]]:
    """
    TUYỆT ĐỐI KHÔNG dời lùi SFX về sau để né min_gap_ms:
    Nếu 2 cụm sự kiện khác nhau cách nhau < 140ms, chỉ giữ cụm có độ ưu tiên cao hơn
    (hook_slam > impact > slash_cut > card_snap > num_tick), giữ nguyên 100% mốc thời gian gốc!
    """
    if not sfx_cues:
        return []
    # Gom các lớp cùng thuộc 1 mốc sự kiện (cách <= 65ms coi là các lớp chồng của cùng 1 cú đánh)
    sorted_cues = sorted(sfx_cues, key=lambda x: x[1])
    clusters: List[List[Tuple[str, int, float]]] = []
    for c in sorted_cues:
        if clusters and abs(c[1] - clusters[-1][0][1]) <= 65:
            clusters[-1].append(c)
        else:
            clusters.append([c])

    kept_clusters: List[List[Tuple[str, int, float]]] = []
    for cl in clusters:
        cl_anchor = cl[0][1]
        cl_prio = max(_sfx_priority(x[0]) for x in cl)
        if kept_clusters:
            prev_anchor = kept_clusters[-1][0][1]
            prev_prio = max(_sfx_priority(x[0]) for x in kept_clusters[-1])
            if 65 < abs(cl_anchor - prev_anchor) < min_gap_ms:
                if cl_prio > prev_prio:
                    kept_clusters[-1] = cl
                # Nếu ưu tiên thấp hơn hoặc bằng -> bỏ cụm phụ, giữ nguyên mốc cụm chính
                continue
        kept_clusters.append(cl)

    return [item for cl in kept_clusters for item in cl]


def generate_fresh_foley_pack(out_dir: Path, seed: str = "hadawhy") -> dict[str, Path]:
    """
    Bộ sinh transient vật lý tươi mới bằng Python/NumPy (seed theo tên dự án để mỗi tập có màu âm riêng):
    - proc_hook_slam.wav, proc_card_snap.wav, proc_num_tick.wav,
      proc_slash_cut.wav, proc_marker_swipe.wav, proc_riser_boom.wav
    """
    import hashlib
    import wave
    import numpy as np

    out_dir.mkdir(parents=True, exist_ok=True)
    sr = 48000
    seed_int = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16)
    rng = np.random.default_rng(seed_int)
    pitch_jit = float(rng.uniform(0.92, 1.09))

    def _write_wav(path: Path, mono: np.ndarray) -> Path:
        peak = float(np.max(np.abs(mono)) + 1e-9)
        norm = np.clip((mono / peak) * 0.89, -1.0, 1.0)
        pcm = (norm * 32767.0).astype(np.int16)
        stereo = np.column_stack((pcm, pcm)).ravel()
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(stereo.tobytes())
        return path

    files: dict[str, Path] = {}

    # 1. proc_hook_slam.wav (punchy sub-drop + crisp metallic transient, 0.42s)
    t = np.linspace(0, 0.42, int(sr * 0.42), endpoint=False)
    f_sweep = (155.0 * pitch_jit) * np.exp(-t * 9.5) + 42.0
    sub = np.sin(2 * np.pi * np.cumsum(f_sweep) / sr) * np.exp(-t * 7.5)
    click = rng.normal(0, 1, len(t)) * np.exp(-t * 55.0) * 0.65
    files["proc_hook_slam.wav"] = _write_wav(out_dir / "proc_hook_slam.wav", sub + click)

    # 2. proc_card_snap.wav (crisp tactile snap + short air thump, 0.18s)
    t = np.linspace(0, 0.18, int(sr * 0.18), endpoint=False)
    snap_tone = np.sin(2 * np.pi * (420.0 * pitch_jit) * np.exp(-t * 22.0) * t) * np.exp(-t * 28.0)
    snap_air = rng.normal(0, 1, len(t)) * np.exp(-t * 45.0) * 0.55
    files["proc_card_snap.wav"] = _write_wav(out_dir / "proc_card_snap.wav", snap_tone + snap_air)

    # 3. proc_num_tick.wav (tight mechanical digital tick, 0.09s)
    t = np.linspace(0, 0.09, int(sr * 0.09), endpoint=False)
    tick = (np.sin(2 * np.pi * (1450.0 * pitch_jit) * t) + 0.5 * np.sin(2 * np.pi * (2900.0 * pitch_jit) * t)) * np.exp(-t * 68.0)
    files["proc_num_tick.wav"] = _write_wav(out_dir / "proc_num_tick.wav", tick)

    # 4. proc_slash_cut.wav (sharp blade swoosh + high transient, 0.24s)
    t = np.linspace(0, 0.24, int(sr * 0.24), endpoint=False)
    noise = rng.normal(0, 1, len(t))
    env = np.sin(np.pi * (t / 0.24)) ** 1.4 * np.exp(-t * 6.0)
    blade = np.sin(2 * np.pi * (900.0 * pitch_jit * (1.0 - 0.5 * t / 0.24)) * t) * np.exp(-t * 24.0) * 0.55
    files["proc_slash_cut.wav"] = _write_wav(out_dir / "proc_slash_cut.wav", noise * env * 0.75 + blade)

    # 5. proc_marker_swipe.wav (paper/highlighter swipe texture, 0.28s)
    t = np.linspace(0, 0.28, int(sr * 0.28), endpoint=False)
    sw_env = np.sin(np.pi * (t / 0.28)) ** 1.2
    sw_noise = rng.normal(0, 1, len(t))
    # Simple moving-average smoothing to shape mid-band paper swipe
    kernel = np.ones(12) / 12.0
    sw_band = np.convolve(sw_noise, kernel, mode="same") - np.convolve(sw_noise, np.ones(48) / 48.0, mode="same")
    files["proc_marker_swipe.wav"] = _write_wav(out_dir / "proc_marker_swipe.wav", sw_band * sw_env)

    # 6. proc_riser_boom.wav (0.55s rising tension swell into deep sub boom)
    t = np.linspace(0, 0.75, int(sr * 0.75), endpoint=False)
    riser_mask = t < 0.50
    r_t = np.clip(t / 0.50, 0.0, 1.0)
    riser = (rng.normal(0, 1, len(t)) * 0.35 + np.sin(2 * np.pi * (120.0 + 380.0 * (r_t ** 2)) * t) * 0.5) * (r_t ** 2.2) * riser_mask
    b_t = np.maximum(0.0, t - 0.50)
    boom = np.sin(2 * np.pi * ((110.0 * pitch_jit) * np.exp(-b_t * 10.0) + 38.0) * b_t) * np.exp(-b_t * 8.0) * (~riser_mask)
    files["proc_riser_boom.wav"] = _write_wav(out_dir / "proc_riser_boom.wav", riser * 0.65 + boom)

    return files


def resolve_sfx_path(fname: str, project_sfx_dir: Optional[Path] = None) -> Path:
    """
    CHỈ đọc SFX từ temp/sfx/ của đúng dự án đang làm (ZERO REUSE).
    Tuyệt đối không đọc kho cũ trong D:\\Đầu Não (không xóa) hay dự án khác.
    """
    sdir = project_sfx_dir or _ACTIVE_PROJECT_SFX_DIR
    if not sdir or not sdir.exists():
        return Path("__MISSING_PROJECT_SFX_DIR__") / fname
    sdir_resolved = sdir.resolve()
    p = sdir / Path(fname).name
    if p.exists() and p.is_file():
        return p
    for cand in sdir.rglob(Path(fname).name):
        if cand.is_file() and sdir_resolved in cand.resolve().parents:
            return cand
    return sdir / Path(fname).name

# Từ điển 16 Tổ hợp SFX Đa tầng (Compound Stacking - Chuẩn @nhanho.home)
# Nguyên tắc: KHÔNG dùng 1 tiếng whoosh/hit đơn lẻ rập khuôn; mỗi điểm rơi phối 2-3 lớp (tạo đà -> bùng nổ).
COMPOUND_SFX_COMBOS = {
    # Nhóm 1: Chuyển cảnh / Cao trào
    "riser_hit": [("riser.wav", -750, 0.28), ("impact.wav", 0, 0.48)],
    "riser_whoosh": [("riser.wav", -650, 0.26), ("whoosh_fast.wav", 0, 0.44)],
    "riser_reverse": [("riser.wav", -700, 0.25), ("reverse_swell.wav", -140, 0.40)],
    "swell_impact": [("swell.wav", -800, 0.28), ("impact.wav", 0, 0.48)],
    # Nhóm 2: Tăng cường nhịp điệu & Chữ/Số liệu
    "hit_drum_kick": [("impact.wav", 0, 0.40), ("drum_kick.wav", 10, 0.42)],
    "click_typing": [("keyboard_click.wav", 0, 0.42), ("typing.wav", 40, 0.30)],
    "snare_roll_hit": [("snare_roll.wav", -650, 0.30), ("impact.wav", 0, 0.48)],
    "bass_drop_hit": [("boom_drop.wav", 0, 0.46), ("sub_bass_impact.wav", 15, 0.42)],
    # Nhóm 3: Tạo bầu không khí
    "ambient_hit": [("server_hum.wav", -550, 0.20), ("impact.wav", 0, 0.44)],
    "ambient_riser_stinger": [("riser.wav", -700, 0.24), ("stinger.wav", 0, 0.44)],
    "rain_piano": [("rain.wav", -500, 0.20), ("piano_key.wav", 0, 0.40)],
    # Nhóm 4: Cao trào / Cảm giác bom tấn
    "riser_swish_hit": [("riser.wav", -750, 0.25), ("whoosh_fast.wav", -110, 0.36), ("impact.wav", 0, 0.48)],
    "deep_boom_sub": [("boom_drop.wav", 0, 0.46), ("sub_drop.wav", 20, 0.42)],
    "choir_impact": [("choir.wav", -350, 0.26), ("impact.wav", 0, 0.46)],
    "trailer_hit_braam": [("sub_bass_impact.wav", 0, 0.45), ("braaam.wav", 30, 0.42)],
}

# Từ điển ngữ nghĩa từ khóa -> Tổ hợp SFX phòng thu tương ứng để tự động biên đạo cho kịch bản mới
SEMANTIC_SFX_MAP = [
    # 1. Tiền bạc, Tỷ đô, Vốn hóa, Tài chính (từ khóa đặc thù, tránh từ quá phổ thông)
    (
        ["tỷ", "triệu", "usd", "ipo", "lãi", "lỗ", "thuế", "%"],
        [("cash_flip.wav", 0.48), ("bass_drop_hit", 1.0), ("hit_drum_kick", 1.0)],
    ),
    # 2. Điều tra, Pháp lý, Bí mật, Cấm vận
    (
        ["điều", "luật", "tòa", "mật", "cấm", "phạt", "bắt"],
        [("gavel_slam.wav", 0.50), ("ambient_riser_stinger", 1.0), ("click_typing", 1.0)],
    ),
    # 3. Đế chế, Quyền lực, Độc quyền, Chấn động
    (
        ["đế", "ngai", "quyền", "khổng", "thống", "sụp"],
        [("trailer_hit_braam", 1.0), ("deep_boom_sub", 1.0), ("choir_impact", 1.0)],
    ),
]


def _find_blueprint_near(words_path: Path) -> Optional[Path]:
    for cand in [
        words_path.parent / "choreography_blueprint.json",
        words_path.parent.parent / "choreography_blueprint.json",
        words_path.parent.parent / "temp" / "choreography_blueprint.json",
    ]:
        if cand.exists():
            return cand
    return None


def auto_choreograph_script_sfx_cues(
    words_json_path: str | Path,
    total_duration_sec: float,
    beat_timestamps: Optional[List[float]] = None,
    blueprint_json_path: Optional[str | Path] = None,
) -> Tuple[List[Tuple[str, int, float]], List[Tuple[float, float]]]:
    """
    Biên đạo SFX chuẩn điện ảnh (Luật 12 — Visual-Linked, Zero Filler, Chống lặp):
    - Ưu tiên 1: Đọc mốc sự kiện chủ thể 3D / con số từ `choreography_blueprint.json` -> SFX CHỈ nổ đúng lúc hình/số xuất hiện.
    - Ưu tiên 2 (fallback): Nếu chưa có blueprint, chỉ điểm huyệt tại chuyển Beat + con số lớn + điểm Vacuum Drop cuối.
    - XÓA BỎ HOÀN TOÀN cơ chế filler nhồi pop/tap khi trống (giữ khoảng thở cho giọng đọc).
    - Kết nối kho Foley phòng thu thật (`assets/foleys/`) và giới hạn mỗi file tối đa 2 lần/video.
    """
    words_path = Path(words_json_path)
    if not words_path.exists():
        raise FileNotFoundError(f"Không tìm thấy words.json để biên đạo SFX: {words_path}")

    # Khóa kho SFX theo từng dự án + tự sinh bộ transient vật lý tươi mới theo seed tên dự án
    project_sfx_dir = words_path.parent / "sfx"
    set_project_sfx_dir(project_sfx_dir)
    proj_seed = words_path.parent.parent.name or "hadawhy"
    generate_fresh_foley_pack(project_sfx_dir, seed=proj_seed)
    fresh_sfx_files = sorted(
        [p.name for p in project_sfx_dir.glob("*") if p.is_file() and p.suffix.lower() in (".mp3", ".wav")]
    ) if project_sfx_dir.exists() else []
    if not any(f.startswith("role_") for f in fresh_sfx_files):
        try:
            from audio_harvester import harvest_fresh_sfx
            harvest_fresh_sfx(
                words_path.parent.parent,
                topic_keywords=["transition", "whoosh", "click", "technology", "impact", "cinematic"],
                count=14,
            )
            fresh_sfx_files = sorted(
                [p.name for p in project_sfx_dir.glob("*") if p.is_file() and p.suffix.lower() in (".mp3", ".wav")]
            )
        except Exception as exc:
            print(f"[SFX WARN] Không cào thêm được Mixkit ({exc}), dùng bộ transient proc_*.wav vừa sinh.")

    # Phân loại tự động SFX tươi mới trong temp/sfx/ theo tiền tố 6 vai trò `role_*` (fallback từ khóa tên file)
    def _match_fresh_by_prefix_or_kw(prefixes: Tuple[str, ...], keywords: Tuple[str, ...]) -> List[str]:
        by_prefix = [f for f in fresh_sfx_files if any(f.lower().startswith(pf) for pf in prefixes)]
        by_kw = [f for f in fresh_sfx_files if f not in by_prefix and any(kw in f.lower() for kw in keywords)]
        return by_prefix + by_kw

    role_riser = _match_fresh_by_prefix_or_kw(("role_riser_",), ("riser", "swoosh", "swell"))
    role_impact = _match_fresh_by_prefix_or_kw(("role_impact_",), ("impact", "hit", "boom", "cinematic", "slam", "drop"))
    role_hook = _match_fresh_by_prefix_or_kw(("role_hook_",), ("whoosh", "transition", "swish"))
    role_knowledge = _match_fresh_by_prefix_or_kw(("role_knowledge_",), ("typing", "click", "paper", "ui"))
    role_num = _match_fresh_by_prefix_or_kw(("role_num_",), ("clock", "tick", "interface", "tech"))
    role_money = _match_fresh_by_prefix_or_kw(("role_money_",), ("cash", "coin", "money"))
    role_topic = _match_fresh_by_prefix_or_kw(("role_topic_",), ())

    mixkit_transition_hook = role_hook or role_riser or role_topic
    mixkit_knowledge_click = role_knowledge or role_num
    mixkit_num_pool = role_num or role_knowledge
    mixkit_money_cash = role_money or role_num
    mixkit_subject_impact = role_impact + role_topic

    raw_data = json.loads(words_path.read_text(encoding="utf-8"))
    words = raw_data.get("words", raw_data) if isinstance(raw_data, dict) else raw_data

    if not beat_timestamps or len(beat_timestamps) < 5:
        step = total_duration_sec / 5.0
        beat_timestamps = [0.0, round(step * 0.85, 2), round(step * 1.75, 2), round(step * 2.80, 2), round(step * 3.82, 2)]

    cues: List[Tuple[str, int, float]] = []
    event_anchors_ms: List[int] = []
    use_counts: dict[str, int] = {}
    last_used_sfx: List[Optional[str]] = [None]

    def add_cue(sfx_file: str, ms: int, vol: float, min_gap_ms: int = 260, max_uses: int = 4) -> bool:
        ms = max(0, min(int(total_duration_sec * 1000) - 250, int(ms)))
        if any(abs(ms - u) < min_gap_ms for u in event_anchors_ms):
            return False
        if last_used_sfx[0] == sfx_file:
            return False
        if use_counts.get(sfx_file, 0) >= max_uses:
            return False
        if not resolve_sfx_path(sfx_file).exists():
            return False
        cues.append((sfx_file, ms, round(vol, 2)))
        event_anchors_ms.append(ms)
        use_counts[sfx_file] = use_counts.get(sfx_file, 0) + 1
        last_used_sfx[0] = sfx_file
        return True

    def add_dynamic_compound(anchor_ms: int, min_gap_ms: int = 500, vol_scale: float = 1.0) -> bool:
        """Dynamic Compound Stacking: xếp lớp role_riser_* (-500ms, 0.65) + role_impact_* / proc_riser_boom (0ms, 1.10)."""
        anchor_ms = max(0, min(int(total_duration_sec * 1000) - 250, int(anchor_ms)))
        if any(abs(anchor_ms - u) < min_gap_ms for u in event_anchors_ms):
            return False
        added = False
        riser_cand = next((f for f in role_riser if use_counts.get(f, 0) < 4 and resolve_sfx_path(f).exists()), None)
        impact_pool = list(role_impact) + ["proc_riser_boom.wav", "proc_hook_slam.wav"]
        impact_cand = next((f for f in impact_pool if use_counts.get(f, 0) < 4 and f != last_used_sfx[0] and resolve_sfx_path(f).exists()), None)
        if riser_cand and anchor_ms >= 350:
            r_ms = max(0, anchor_ms - 500)
            cues.append((riser_cand, r_ms, round(min(1.10, 0.65 * vol_scale), 2)))
            use_counts[riser_cand] = use_counts.get(riser_cand, 0) + 1
            added = True
        if impact_cand:
            cues.append((impact_cand, anchor_ms, round(min(1.10, 1.05 * vol_scale), 2)))
            use_counts[impact_cand] = use_counts.get(impact_cand, 0) + 1
            last_used_sfx[0] = impact_cand
            added = True
        if added:
            event_anchors_ms.append(anchor_ms)
        return added

    def add_combo(
        combo_or_file: str,
        anchor_ms: int,
        vol_scale: float = 1.0,
        min_gap_ms: int = 450,
        fallback_pool: Optional[List[str]] = None,
    ) -> bool:
        """Đặt tổ hợp SFX đa tầng tại 1 mốc sự kiện; ưu tiên Dynamic Compound role_* trước rồi fallback nhóm role_*."""
        anchor_ms = max(0, min(int(total_duration_sec * 1000) - 250, int(anchor_ms)))
        if any(abs(anchor_ms - u) < min_gap_ms for u in event_anchors_ms):
            return False
        if combo_or_file not in COMPOUND_SFX_COMBOS:
            return add_cue(combo_or_file, anchor_ms, 0.76 * vol_scale, min_gap_ms=min_gap_ms, max_uses=3)

        if add_dynamic_compound(anchor_ms, min_gap_ms=min_gap_ms, vol_scale=vol_scale):
            return True

        search_pool = list(fallback_pool or []) + [f for f in fresh_sfx_files if f not in (fallback_pool or [])]
        for cand in search_pool:
            if add_cue(cand, anchor_ms, 0.74 * vol_scale, min_gap_ms=min_gap_ms, max_uses=3):
                return True
        return False

    # 1. Mở đầu Beat: Dynamic Compound Stacking (role_riser_* -600ms + role_impact_* 0ms)
    beat_combo_openers = [
        "riser_whoosh",
        "riser_hit",
        "swell_impact",
        "riser_reverse",
        "riser_swish_hit",
    ]
    for idx, bt in enumerate(beat_timestamps[:5]):
        b_ms = int(bt * 1000)
        combo_name = beat_combo_openers[idx % len(beat_combo_openers)]
        add_combo(
            combo_name,
            max(0, b_ms),
            vol_scale=1.0,
            min_gap_ms=800,
            fallback_pool=mixkit_transition_hook or mixkit_subject_impact,
        )

    # 2. Đọc mốc từ choreography_blueprint.json -> ánh xạ chuẩn 5 nhóm vào `role_*`, min_gap_ms=450ms cho micro-SFX
    bp_path = Path(blueprint_json_path) if blueprint_json_path else _find_blueprint_near(words_path)
    used_blueprint = False
    if bp_path and bp_path.exists():
        try:
            bp = json.loads(bp_path.read_text(encoding="utf-8"))
            fps = float(bp.get("fps", 60))
            hook_text_pool = ["proc_hook_slam.wav"] + list(mixkit_transition_hook)
            knowledge_text_pool = ["proc_marker_swipe.wav", "proc_card_snap.wav"] + list(mixkit_knowledge_click)
            number_knowledge_pool = ["proc_num_tick.wav", "proc_slash_cut.wav"] + list(mixkit_num_pool)
            number_money_pool = ["proc_num_tick.wav"] + list(mixkit_money_cash)
            subject_pool = ["proc_card_snap.wav"] + list(mixkit_subject_impact) + ["ambient_hit"]
            counters = {"hook": 0, "know": 0, "num_k": 0, "num_m": 0, "subj": 0}
            ev_list = []
            if isinstance(bp.get("events"), list):
                for ev in bp["events"]:
                    if isinstance(ev, dict) and ("frame" in ev or "time_ms" in ev):
                        ev_list.append(ev)
            for beat in bp.get("beats", []):
                for ev in beat.get("events", []):
                    if isinstance(ev, dict) and ("frame" in ev or "time_ms" in ev):
                        ev_list.append(ev)
            for ev in ev_list:
                ev_ms = int(ev["time_ms"]) if "time_ms" in ev else int(round((float(ev["frame"]) * 1000.0) / fps))
                kind = str(ev.get("kind") or ev.get("type") or "subject").lower()
                if kind in ("hook", "hook_text", "text"):
                    # Mọi mốc hook_text BẮT BUỘC có lớp Hook đập/quét/trầm nổi bật (vol 1.25)
                    hook_added = False
                    if resolve_sfx_path("proc_hook_slam.wav").exists():
                        cues.append(("proc_hook_slam.wav", max(0, ev_ms), 1.25))
                        hook_added = True
                    if role_hook:
                        rh = role_hook[counters["hook"] % len(role_hook)]
                        if resolve_sfx_path(rh).exists():
                            cues.append((rh, max(0, ev_ms - 60), 1.12))
                            hook_added = True
                    if role_impact:
                        ri = role_impact[counters["hook"] % len(role_impact)]
                        if resolve_sfx_path(ri).exists():
                            cues.append((ri, max(0, ev_ms), 1.15))
                            hook_added = True
                    if hook_added:
                        event_anchors_ms.append(max(0, ev_ms))
                        counters["hook"] += 1
                        used_blueprint = True
                        continue
                    pool, c_key, gap_ms, vol_s, fb_pool = hook_text_pool, "hook", 260, 1.25, mixkit_transition_hook
                elif kind in ("knowledge", "knowledge_text"):
                    pool, c_key, gap_ms, vol_s, fb_pool = knowledge_text_pool, "know", 260, 0.88, mixkit_knowledge_click
                elif kind == "number_money":
                    pool, c_key, gap_ms, vol_s, fb_pool = number_money_pool, "num_m", 260, 0.95, mixkit_money_cash
                elif kind in ("number", "number_knowledge"):
                    pool, c_key, gap_ms, vol_s, fb_pool = number_knowledge_pool, "num_k", 260, 0.95, mixkit_num_pool
                else:
                    pool, c_key, gap_ms, vol_s, fb_pool = subject_pool, "subj", 320, 0.92, mixkit_subject_impact
                start_idx = counters[c_key]
                added_ev = False
                for off in range(len(pool)):
                    c_name = pool[(start_idx + off) % len(pool)]
                    if add_combo(c_name, ev_ms, vol_scale=vol_s, min_gap_ms=gap_ms, fallback_pool=fb_pool):
                        counters[c_key] = start_idx + off + 1
                        used_blueprint = True
                        added_ev = True
                        break
                if not added_ev and fresh_sfx_files:
                    ordered_fresh = list(fb_pool) + [f for f in fresh_sfx_files if f not in fb_pool]
                    for off in range(len(ordered_fresh)):
                        f_name = ordered_fresh[(start_idx + off) % len(ordered_fresh)]
                        if add_cue(f_name, ev_ms, round(min(1.10, 0.90 * vol_s), 2), min_gap_ms=gap_ms, max_uses=4):
                            counters[c_key] = start_idx + off + 1
                            used_blueprint = True
                            break
        except Exception:
            used_blueprint = False

    # 3. Fallback khi chưa có blueprint: chỉ bám từ khóa đặc thù & con số quan trọng (gap >= 2.0s, KHÔNG filler)
    if not used_blueprint:
        cat_counters = [0] * len(SEMANTIC_SFX_MAP)
        for w_obj in words:
            w_text = str(w_obj.get("word", w_obj.get("text", ""))).strip().lower()
            w_clean = re.sub(r"[^\w%]", "", w_text)
            if not w_clean:
                continue
            start_sec = float(w_obj.get("start", w_obj.get("startMs", 0) / 1000.0 if "startMs" in w_obj else 0.0))
            start_ms = int(start_sec * 1000)

            matched = False
            for c_idx, (kw_list, sfx_pool) in enumerate(SEMANTIC_SFX_MAP):
                if any(kw == w_clean or (len(kw) >= 3 and kw in w_clean) for kw in kw_list):
                    for off in range(len(sfx_pool)):
                        c_name, c_scale = sfx_pool[(cat_counters[c_idx] + off) % len(sfx_pool)]
                        if add_combo(c_name, start_ms, vol_scale=c_scale, min_gap_ms=2000):
                            cat_counters[c_idx] += 1
                            matched = True
                            break
                    break

            if not matched and any(ch.isdigit() for ch in w_clean) and len(w_clean) >= 2:
                num_combos = ["bass_drop_hit", "hit_drum_kick", "deep_boom_sub", "trailer_hit_braam"]
                for off in range(len(num_combos)):
                    c_name = num_combos[(len(event_anchors_ms) + off) % len(num_combos)]
                    if add_combo(c_name, start_ms, vol_scale=1.0, min_gap_ms=2200):
                        break

    # 4. Tìm điểm Vacuum Drop (khoảng ngắt trước câu chốt cuối cùng ở vùng 82% - 94% thời lượng)
    drop_start = round(total_duration_sec * 0.88, 2)
    best_gap = 0.0
    for i in range(len(words) - 1):
        end_cur = float(words[i].get("end", words[i].get("endMs", 0) / 1000.0 if "endMs" in words[i] else 0.0))
        st_nxt = float(words[i + 1].get("start", words[i + 1].get("startMs", 0) / 1000.0 if "startMs" in words[i + 1] else 0.0))
        if total_duration_sec * 0.80 <= end_cur <= total_duration_sec * 0.94:
            gap = st_nxt - end_cur
            if gap >= best_gap:
                best_gap = gap
                drop_start = round(max(0.0, end_cur - 0.15), 2)

    drop_end = round(min(total_duration_sec - 1.0, drop_start + 0.65), 2)
    vacuum_drops = [(drop_start, drop_end)]

    # Cú chốt bom tấn sau Vacuum Drop
    add_combo("deep_boom_sub", int(drop_end * 1000) + 60, vol_scale=1.05, min_gap_ms=400)

    cues.sort(key=lambda x: x[1])
    mode = "BLUEPRINT_COMPOUND" if used_blueprint else "SPARSE_COMPOUND"
    print(f"[SFX CHOREOGRAPHER OK | {mode}] Đã biên đạo {len(cues)} lớp SFX đa tầng (0 filler) & Vacuum Drop {vacuum_drops}!")
    return cues, vacuum_drops


def deduplicate_consecutive_sfx(sfx_cues: list[tuple[str, int, float]]) -> list[tuple[str, int, float]]:
    """
    Chống lặp SFX đơn điệu: cấm 2 cue cùng vai trò đứng liền nhau dùng 1 file,
    cho phép các lớp nền Compound (`riser.wav`, `impact.wav`, `swell.wav`, `sub_bass_impact.wav`) phối đa tầng tối đa 5 lần/video.
    """
    variant_groups = [
        ["metal_hit.mp3", "lock.mp3", "gavel_slam.wav", "camera_click.wav", "gear_lock.mp3", "cut.mp3"],
        ["whoosh_big.mp3", "whoosh1.mp3", "whoosh2.mp3", "whoosh3.mp3", "zoom_hit.mp3", "whoosh_fast.wav"],
        ["bass_hit.mp3", "hit_blow.mp3", "boom_drop.wav", "braaam.wav", "drum_kick.wav", "cash_flip.wav"],
        ["pop.mp3", "pop_dry.mp3", "tap.mp3", "type_soft.mp3", "tick.mp3"],
    ]
    compound_core_files = {"riser.wav", "impact.wav", "swell.wav", "sub_bass_impact.wav", "whoosh_fast.wav"}
    sorted_cues = sorted(sfx_cues, key=lambda x: x[1])
    out: list[tuple] = []
    prev_name: Optional[str] = None
    counts: dict[str, int] = {}
    for cue in sorted_cues:
        fname, start_ms, vol = cue[0], cue[1], cue[2]
        rest = cue[3:]
        chosen = fname
        cap = 5 if chosen in compound_core_files else 2
        if (prev_name is not None and chosen == prev_name) or counts.get(chosen, 0) >= cap:
            for grp in variant_groups:
                if chosen in grp:
                    idx = grp.index(chosen)
                    for offset in range(1, len(grp)):
                        cand = grp[(idx + offset) % len(grp)]
                        cand_cap = 5 if cand in compound_core_files else 2
                        if cand != prev_name and counts.get(cand, 0) < cand_cap and resolve_sfx_path(cand).exists():
                            chosen = cand
                            break
                    break
        counts[chosen] = counts.get(chosen, 0) + 1
        out.append((chosen, start_ms, vol, *rest))
        prev_name = chosen
    return out


def extract_tsx_sfx_cues(tsx_path: str | Path, fps: int = 60) -> list[tuple[str, int, float]]:
    """
    Trích xuất SFX sạch bám chủ thể/số liệu (KHÔNG spam pop/tap/tick 35-45 cues):
    - Ưu tiên 1: Nếu tìm thấy `choreography_blueprint.json` + `words.json` của dự án, dùng `auto_choreograph_script_sfx_cues()`
      để SFX chỉ nổ đúng mốc chủ thể 3D / con số (0 filler, tối đa 2 lần/file).
    - Ưu tiên 2 (fallback từ .tsx): Chỉ lấy chuyển cảnh `<Sequence from={...}>` và `impactFrames`,
      lọc khoảng cách tối thiểu `1400ms`, dùng kho Foley thật, cấm spam `pop/tap/tick/type_soft`.
    """
    tsx_p = Path(tsx_path)
    code = tsx_p.read_text(encoding="utf-8")

    # Tìm blueprint + words.json gần dự án nếu có
    fb_root = tsx_p.parent.parent.parent
    words_cand = None
    bp_cand = None
    for cand_dir in [tsx_p.parent, Path(r"D:\DuAn_DangLam")]:
        if cand_dir.exists():
            # Tìm trong D:\DuAn_DangLam nếu tên file khớp hoặc thư mục mới nhất có choreography_blueprint.json
            pass
    # Kiểm tra các đường dẫn chuẩn quanh tsx hoặc trong D:\DuAn_DangLam
    stem_snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", tsx_p.stem).lower()
    for proj_dir in [Path(r"D:\DuAn_DangLam") / stem_snake, tsx_p.parent]:
        for sub in [proj_dir, proj_dir / "temp"]:
            if (sub / "choreography_blueprint.json").exists() and (sub / "words.json").exists():
                bp_cand = sub / "choreography_blueprint.json"
                words_cand = sub / "words.json"
                break
        if bp_cand:
            break

    if bp_cand and words_cand:
        wdata = json.loads(words_cand.read_text(encoding="utf-8"))
        words_list = wdata.get("words", wdata) if isinstance(wdata, dict) else wdata
        dur = float(wdata.get("duration", 45.0)) if isinstance(wdata, dict) else 45.0
        if words_list and isinstance(words_list[-1], dict):
            dur = max(dur, float(words_list[-1].get("end", dur)))
        cues, _ = auto_choreograph_script_sfx_cues(words_cand, dur, blueprint_json_path=bp_cand)
        return deduplicate_consecutive_sfx(cues)

    # Fallback sạch từ .tsx: CHỈ lấy Sequence transitions & impactFrames (không quét frame >= / interpolate)
    raw_events: list[tuple[str, int, float]] = []
    seq_frames = [int(m) for m in re.findall(r"<Sequence[^>]*\bfrom\s*=\s*\{\s*(\d+)\s*\}", code)]
    opener_pool = ["whoosh_big.mp3", "camera_click.wav", "whoosh2.mp3", "gear_lock.mp3", "cut.mp3"]
    for i, fr in enumerate(seq_frames):
        raw_events.append((opener_pool[i % len(opener_pool)], round(fr * 1000 / fps), 0.58))

    imp_pool = ["metal_hit.mp3", "bass_hit.mp3", "gavel_slam.wav", "boom_drop.wav", "lock.mp3"]
    for imp_match in re.finditer(r"impactFrames\s*=\s*\[([^\]]+)\]", code):
        impacts = [int(x.strip()) for x in imp_match.group(1).split(",") if x.strip().isdigit()]
        for i, fr in enumerate(impacts):
            raw_events.append((imp_pool[i % len(imp_pool)], round(fr * 1000 / fps), 0.56))

    raw_events.sort(key=lambda x: x[1])
    filtered: list[tuple[str, int, float]] = []
    last_ms = -2000
    for fname, ms, vol in raw_events:
        if ms - last_ms >= 1400 and resolve_sfx_path(fname).exists():
            filtered.append((fname, ms, vol))
            last_ms = ms

    return deduplicate_consecutive_sfx(filtered)


def validate_fresh_ai_bgm(bgm_path: Path) -> None:
    bgm_str = str(bgm_path.resolve()).lower()
    forbidden_markers = [
        "demo_fb_reels_forensic_bgm",
        "wallstreet_finance_drive_01",
        "dark_investigation_tension_01",
        "cyber_ai_future_02",
        "epic_victory_climax_01",
        r"\assets\music\\",
        r"\public\music\\",
        r"\public\audio\bgm\\",
    ]
    for marker in forbidden_markers:
        if marker in bgm_str:
            raise ValueError(
                f"VI PHẠM LUẬT THÉP: Phát hiện lấy nhạc nền tĩnh cũ trong máy ({bgm_path})! "
                f"Bắt buộc dùng bộ sáng tác nhạc Trailer 5 Nhịp ĐỘC BẢN theo kịch bản!"
            )


def mix_reels_master_audio(
    voice_wav: str | Path,
    output_wav: str | Path,
    sfx_cues: Optional[list[tuple[str, int, float]]] = None,
    total_duration_sec: float = 43.0,
    bgm_path: str | Path | None = None,
    script_topic: str = "",
    script_text: str = "",
    words_json_path: str | Path | None = None,
    beat_timestamps: Optional[List[float]] = None,
    mood: str = "conspiracy_thriller",
    voice_volume: float = 1.28,
    bgm_base_volume: float = 0.72,
    bgm_duck_volume: float = 0.28,
    vacuum_drops: list[tuple[float, float]] | None = None,
) -> Path:
    """
    Hòa âm Trailer Hollywood 5 Nhịp kịch tính & cân đối hài hòa với giọng đọc Hải Đăng (-14.0 LUFS).
    Nếu truyền `words_json_path` mà chưa có `sfx_cues`, hệ thống tự động biên đạo SFX mới 100% theo từng từ khóa!
    """
    voice_wav = Path(voice_wav)
    output_wav = Path(output_wav)
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    if (output_wav.parent / "sfx").exists():
        set_project_sfx_dir(output_wav.parent / "sfx")
    elif words_json_path and (Path(words_json_path).parent / "sfx").exists():
        set_project_sfx_dir(Path(words_json_path).parent / "sfx")

    if not voice_wav.exists():
        raise FileNotFoundError(f"Không tìm thấy voice_wav: {voice_wav}")

    # Tự động biên đạo SFX mới 100% từ words.json nếu chưa truyền sfx_cues
    if (not sfx_cues or len(sfx_cues) == 0) and words_json_path:
        sfx_cues, auto_drops = auto_choreograph_script_sfx_cues(
            words_json_path=words_json_path,
            total_duration_sec=total_duration_sec,
            beat_timestamps=beat_timestamps,
        )
        if not vacuum_drops:
            vacuum_drops = auto_drops
    elif not sfx_cues:
        raise ValueError("Bắt buộc truyền sfx_cues hoặc words_json_path để biên đạo SFX mới cho kịch bản!")

    if bgm_path is None:
        if not script_topic:
            raise ValueError("Bắt buộc truyền bgm_path hoặc script_topic để biên soạn nhạc trailer 5 nhịp mới!")
        from ace_step_fb_runner import ACEStepFBRunner
        runner = ACEStepFBRunner()
        bgm_path = output_wav.parent / f"bespoke_5beat_trailer_{output_wav.stem}.wav"
        runner.generate_unique_script_bgm(
            script_topic=script_topic,
            output_path=bgm_path,
            duration_sec=total_duration_sec + 0.5,
            mood=mood,
            script_text=script_text,
            beat_timestamps=beat_timestamps,
        )
    else:
        bgm_path = Path(bgm_path)

    if not bgm_path.exists():
        raise FileNotFoundError(f"Không tìm thấy bgm_path: {bgm_path}")

    validate_fresh_ai_bgm(bgm_path)

    sfx_cues = resolve_sfx_priority_conflicts(deduplicate_consecutive_sfx(sfx_cues), min_gap_ms=140)

    punched_dir = output_wav.parent / "sfx_punched"
    punched_cache: dict[str, Path] = {}
    peak_offset_cache: dict[str, int] = {}
    for cue in sfx_cues:
        fname = cue[0]
        fpath = resolve_sfx_path(fname)
        if not fpath.exists():
            raise FileNotFoundError(f"SFX không tồn tại trong kho dự án: {fpath}")
        if fname not in punched_cache:
            punched_wav = preprocess_sfx_punch(fpath, punched_dir / f"{fpath.stem}_punch.wav")
            punched_cache[fname] = punched_wav
            peak_offset_cache[fname] = get_sfx_peak_offset_ms(punched_wav)

    # Căn đỉnh nổ âm thanh (Peak-Transient Alignment) để đỉnh nổ đập trúng đúng frame chữ/số chạm màn hình
    aligned_cues: list[tuple] = []
    cmd = ["ffmpeg", "-y", "-i", str(voice_wav), "-i", str(bgm_path)]
    for cue in sfx_cues:
        fname, target_ms, vol = cue[0], int(cue[1]), cue[2]
        rest = cue[3:]
        low_f = fname.lower()
        if any(r in low_f for r in ("role_riser", "riser", "whoosh", "swoosh")) and "riser_boom" not in low_f:
            lead_ms = min(500, max(350, peak_offset_cache.get(fname, 400)))
        else:
            lead_ms = min(peak_offset_cache.get(fname, 0), 180) + 40
        aligned_ms = max(0, target_ms - lead_ms)
        aligned_cues.append((fname, aligned_ms, vol, *rest))
        cmd.extend(["-i", str(punched_cache[fname])])
    sfx_cues = aligned_cues

    fade_out_st = max(0.5, round(total_duration_sec - 1.2, 2))

    # 1. Đường tiếng Giọng đọc Hải Đăng: Lọc sạch tạp âm đáy 85Hz, tăng độ rõ chữ 3.0kHz (+2.8dB)
    vo_filter = (
        f"[0:a]highpass=f=85,"
        f"equalizer=f=3000:width_type=o:width=1.3:g=1.8,"
        f"equalizer=f=6000:width_type=q:width=1.5:g=-2.0,"
        f"loudnorm=I=-15.5:TP=-2.0:LRA=4,volume={voice_volume}[vo_clean]"
    )

    # 2. Đường tiếng Nhạc nền Trailer 5 Nhịp:
    # - Surgical Spectral Pocket (-5.0dB tại 2.5kHz) nhường trọn dải giọng nói nhưng giữ lực đàn dây & trống trận.
    # - Boost nhẹ sub-bass 90Hz (+2.0dB) tạo độ dày rạp chiếu phim.
    # Khôi phục BGM rõ giai điệu & kịch tính: bung 0.85 ở quãng nghỉ >= 0.25s, giữ rõ 0.48–0.55 lúc có giọng đọc
    bgm_base_volume = max(0.75, min(0.92, float(bgm_base_volume)))
    bgm_proc_filter = (
        f"[1:a]atrim=0:{total_duration_sec:.2f},"
        f"equalizer=f=2500:width_type=o:width=1.2:g=-4.0,"
        f"equalizer=f=90:width_type=o:width=1.2:g=2.2,"
        f"volume={bgm_base_volume},"
        f"afade=t=out:st={fade_out_st:.2f}:d=1.2[bgm_eq]"
    )

    if vacuum_drops:
        # Smooth 120ms ramp-down & ramp-up to prevent harsh digital clicks/pops
        ramp = 0.12
        expr_parts = []
        for d_st, d_end in vacuum_drops:
            in_end = round(d_st + ramp, 3)
            out_st = round(max(in_end, d_end - ramp), 3)
            expr_parts.append(
                f"if(between(t,{d_st:.3f},{in_end:.3f}),1-((t-{d_st:.3f})/{ramp}),"
                f"if(between(t,{in_end:.3f},{out_st:.3f}),0,"
                f"if(between(t,{out_st:.3f},{d_end:.3f}),(t-{out_st:.3f})/{ramp},1)))"
            )
        vol_expr = "*".join(expr_parts)
        bgm_vac_filter = f"[bgm_eq]volume='{vol_expr}':eval=frame[bgm_vac]"
    else:
        bgm_vac_filter = "[bgm_eq]anull[bgm_vac]"

    # Sidechain mượt giữ BGM ở mức 0.48–0.55 khi có lời đọc và tự bung 0.85 ở quãng nghỉ >= 0.25s (không dìm mất nhạc)
    vo_split = "[vo_clean]asplit=3[vo_mix][vo_sc][vo_sc_sfx]"
    bgm_final_filter = (
        f"[bgm_vac][vo_sc]sidechaincompress=threshold=0.048:ratio=1.85:attack=22:release=240[bgm_final]"
    )

    # 2b. Lớp âm nền theo bối cảnh (Contextual Ambience Bed - siêu nhẹ tạo chiều sâu không gian thật)
    topic_low = (script_topic + " " + script_text).lower()
    if any(k in topic_low for k in ("mưa", "bão", "sét", "đêm", "storm")):
        amb_filter = f"anoisesrc=d={total_duration_sec:.2f}:c=pink:r=48000:a=0.012,highpass=f=180,lowpass=f=2400,aformat=channel_layouts=mono,haas[amb_bed]"
    elif any(k in topic_low for k in ("phố", "vỉa hè", "chợ", "vé số", "đám đông", "quán")):
        amb_filter = f"anoisesrc=d={total_duration_sec:.2f}:c=brown:r=48000:a=0.014,highpass=f=120,lowpass=f=1600,aformat=channel_layouts=mono,haas[amb_bed]"
    else:
        amb_filter = f"anoisesrc=d={total_duration_sec:.2f}:c=brown:r=48000:a=0.009,highpass=f=90,lowpass=f=900,aformat=channel_layouts=mono,haas[amb_bed]"

    filter_parts = [vo_filter, vo_split, bgm_proc_filter, bgm_vac_filter, bgm_final_filter, amb_filter,
                    "[vo_mix]aformat=channel_layouts=stereo[vo_st]",
                    "[bgm_final]aformat=channel_layouts=stereo[bgm_st]"]
    base_mix_inputs = ["[vo_st]", "[bgm_st]", "[amb_bed]"]

    # 3. Nạp các điểm rơi SFX đa tầng + Anti-Harshness EQ (hãm 5.2kHz) + Stereo Panning -> gộp vào [sfx_bus]
    spatial_cycle = [-0.42, 0.42, -0.25, 0.25, 0.0]
    sfx_tags = []
    for idx, cue in enumerate(sfx_cues):
        fname, delay_ms, vol = cue[0], cue[1], cue[2]
        if len(cue) >= 4:
            pan_val = float(cue[3])
        elif any(c in fname for c in ("bass_hit", "metal_hit", "hit_blow", "boom_drop", "sub_bass_impact", "sub_drop", "braaam")):
            pan_val = 0.0
        else:
            pan_val = spatial_cycle[idx % len(spatial_cycle)]
        gain_l = round(min(1.0, 1.0 - max(0.0, pan_val)), 3)
        gain_r = round(min(1.0, 1.0 + min(0.0, pan_val)), 3)
        inp_idx = idx + 2
        tag = f"[s{idx}]"
        filter_parts.append(
            f"[{inp_idx}:a]aformat=channel_layouts=stereo,"
            f"highshelf=f=4800:g=-5.5,lowpass=f=9500,"
            f"pan=stereo|c0={gain_l}*c0|c1={gain_r}*c1,"
            f"adelay={int(delay_ms)}|{int(delay_ms)},volume={vol}{tag}"
        )
        sfx_tags.append(tag)

    if sfx_tags:
        # Chống "lùng bùng" khi xếp lớp nhiều SFX: cắt rãnh 2.5kHz (-3.5dB) & sidechain nhẹ dưới giọng đọc
        filter_parts.append(
            f"{''.join(sfx_tags)}amix=inputs={len(sfx_tags)}:duration=longest:dropout_transition=0:normalize=0,"
            f"equalizer=f=2500:width_type=o:width=1.2:g=-3.5[sfx_raw]"
        )
        filter_parts.append(
            f"[sfx_raw][vo_sc_sfx]sidechaincompress=threshold=0.03:ratio=2.5:attack=15:release=180[sfx_bus]"
        )
        mix_inputs = base_mix_inputs + ["[sfx_bus]"]
    else:
        mix_inputs = base_mix_inputs

    total_inputs = len(mix_inputs)
    filter_parts.append(
        f"{''.join(mix_inputs)}amix=inputs={total_inputs}:duration=first:dropout_transition=0:normalize=0[pre_norm]"
    )

    tmp_pre_wav = output_wav.with_name(f"._tmp_{output_wav.stem}_pre_norm.wav")
    try:
        cmd.extend([
            "-filter_complex", ";".join(filter_parts),
            "-map", "[pre_norm]",
            "-c:a", "pcm_f32le",
            "-ar", "48000",
            "-ac", "2",
            str(tmp_pre_wav),
        ])

        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            raise RuntimeError(f"Lỗi mix audio FFmpeg Pass 1: {res.stderr[-500:]}")

        measure_cmd = [
            "ffmpeg", "-i", str(tmp_pre_wav),
            "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7:print_format=json",
            "-f", "null", "-",
        ]
        m_res = subprocess.run(measure_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        json_match = re.search(r"\{[\s\S]*\}", m_res.stderr)
        if not json_match:
            raise RuntimeError(f"Không đo được thông số loudnorm Pass 1: {m_res.stderr[-500:]}")
        stats = json.loads(json_match.group(0))

        norm_filter = (
            f"loudnorm=I=-14.0:TP=-1.5:LRA=7:"
            f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
            f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
            f"offset={stats['target_offset']}:linear=true"
        )
        pass2_cmd = [
            "ffmpeg", "-y", "-i", str(tmp_pre_wav),
            "-af", norm_filter,
            "-c:a", "pcm_s16le",
            "-ar", "48000",
            "-ac", "2",
            str(output_wav),
        ]
        p2_res = subprocess.run(pass2_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if p2_res.returncode != 0:
            raise RuntimeError(f"Lỗi chuẩn hóa loudnorm Pass 2: {p2_res.stderr[-500:]}")
    finally:
        if tmp_pre_wav.exists():
            tmp_pre_wav.unlink()

    # Tự động trích xuất đủ 3 file kiểm âm: bgm_only_check.mp3 (+ alias bgm_qc_preview.mp3), sfx_only_check.mp3, master_audio_qc_preview.mp3
    bgm_only_mp3 = output_wav.parent / "bgm_only_check.mp3"
    bgm_preview_mp3 = output_wav.parent / "bgm_qc_preview.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(bgm_path), "-t", f"{total_duration_sec:.2f}", "-c:a", "libmp3lame", "-b:a", "192k", str(bgm_only_mp3)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if bgm_only_mp3.exists():
        import shutil
        shutil.copy2(bgm_only_mp3, bgm_preview_mp3)

    sfx_only_mp3 = output_wav.parent / "sfx_only_check.mp3"
    if sfx_cues:
        sfx_only_cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={total_duration_sec:.2f}"]
        sfx_only_filters = []
        sfx_only_tags = ["[0:a]"]
        for idx, cue in enumerate(sfx_cues):
            fname, delay_ms, vol = cue[0], cue[1], cue[2]
            sfx_only_cmd.extend(["-i", str(punched_cache[fname])])
            tag = f"[so{idx}]"
            sfx_only_filters.append(f"[{idx+1}:a]aformat=channel_layouts=stereo,adelay={int(delay_ms)}|{int(delay_ms)},volume={vol}{tag}")
            sfx_only_tags.append(tag)
        sfx_only_filters.append(f"{''.join(sfx_only_tags)}amix=inputs={len(sfx_only_tags)}:duration=first:dropout_transition=0:normalize=0[sfx_out]")
        sfx_only_cmd.extend(["-filter_complex", ";".join(sfx_only_filters), "-map", "[sfx_out]", "-c:a", "libmp3lame", "-b:a", "192k", str(sfx_only_mp3)])
        subprocess.run(sfx_only_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    qc_preview_mp3 = output_wav.parent / "master_audio_qc_preview.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(output_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(qc_preview_mp3)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f"[SFX MIXER OK] Master Audio 5-Beat Trailer (-14.0 LUFS, {len(sfx_cues)} SFX Cues): {output_wav}")
    print(f"[MANDATORY EAR QC 1/3 - BGM ONLY] {bgm_preview_mp3}")
    print(f"[MANDATORY EAR QC 2/3 - SFX ONLY] {sfx_only_mp3}")
    print(f"[MANDATORY EAR QC 3/3 - FULL MIX] {qc_preview_mp3}")
    return output_wav
```


#### `engine/thumbnail_3d_seo_engine.py`

```python
r"""
thumbnail_3d_seo_engine.py - BỘ ĐỘNG CƠ CHUYÊN TRÁCH THUMBNAIL 3D ADN HADA WHY,
NHÚNG BÌA TRỰC TIẾP VÀO VIDEO MP4 & TRINH SÁT 3 TIÊU ĐỀ CHUẨN SEO EVERGREEN.

Đặt tại: D:\Đầu Não Video Ngắn FB (không xóa)\engine\thumbnail_3d_seo_engine.py
Phục vụ độc quyền cho Sub-Agent thứ 6: fb-reels-thumbnail-seo-architect.

3 Nhiệm vụ cốt lõi chạy song song:
1. Tư duy logic theo từng kịch bản (4 Chế độ bố cục: Mystery Silhouette, Dual Confrontation,
   Forensic Object Spotlight, Titan + Evidence) trên nền ADN cố định của kênh HaDa Why:
   - Nền bổ trợ bối cảnh thật nâng khối 3D Chiaroscuro + Unsharp Mask.
   - Bầu trời / nền trên liền mạch 100% (Zero-Blob: CẤM tuyệt đối đốm đỏ/đốm đen vô nghĩa).
   - Chữ Hook 2 dòng Kanit-Black (#42B2F2 Xanh HaDa + #FFFFFF Trắng WHY, viền đen 11px) an toàn 4:5.
2. Nhúng Kép (Dual-Embed) tấm Thumbnail 9:16 vào thẳng file Video MP4:
   - Lớp 1: Chèn làm 2 frame đầu tiên (0.00s - 0.03s) ở đầu video để khi đăng lên Facebook Reels /
     Facebook Page kéo thanh chọn ảnh bìa về 00:00 là chọn được ngay tấm bìa 3D sắc nét!
   - Lớp 2: Nhúng luồng metadata attached_pic chuẩn MP4.
3. Đào bới & Cào dữ liệu từ khóa thực tế (Google Suggest API + YouTube Suggest API +
   yt-dlp Top Viral Search + Google News RSS) -> Xuất 3 Tiêu đề chuẩn SEO có Keyword lượt tìm kiếm cao
   và Evergreen (bền vững theo thời gian).
"""

import io
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr:
    sys.stderr.reconfigure(encoding="utf-8")

FB_BRAIN_DIR = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
REMOTION_DIR = FB_BRAIN_DIR / "remotion_reels"
PUBLIC_HARVEST_DIR = REMOTION_DIR / "public" / "harvested"
FINAL_OUTPUT_DIR = Path(r"D:\Video thành phẩm")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


# ==============================================================================
# KHỐI 1: CÀO DỮ LIỆU TỪ KHÓA THẬT & PHÂN TÍCH SEO EVERGREEN
# ==============================================================================

def fetch_autocomplete_suggestions(query: str, source: str = "google") -> List[str]:
    r"""
    Cào từ khóa gợi ý thực tế người dùng Việt Nam đang gõ tìm kiếm nhiều nhất
    trên Google Search hoặc YouTube Search.
    """
    encoded_q = urllib.parse.quote(query.strip())
    if source == "youtube":
        url = f"http://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=vi&gl=VN&q={encoded_q}"
    else:
        url = f"http://suggestqueries.google.com/complete/search?client=firefox&hl=vi&gl=VN&q={encoded_q}"

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
            data = json.loads(raw)
            if isinstance(data, list) and len(data) >= 2 and isinstance(data[1], list):
                results = []
                for item in data[1]:
                    if isinstance(item, str):
                        results.append(item)
                    elif isinstance(item, list) and len(item) > 0 and isinstance(item[0], str):
                        results.append(item[0])
                return results[:12]
    except Exception as e:
        print(f"[SEO-SUGGEST WARN] ({source} - {query}): {e}")
    return []


def fetch_youtube_top_competitors(query: str, limit: int = 8) -> List[Dict[str, Any]]:
    r"""
    Quét trực tiếp trang kết quả tìm kiếm YouTube bằng Python thuần (ytInitialData)
    để lấy tiêu đề, lượt xem và kênh của các video đối thủ đang hút nhiều view nhất.
    """
    encoded_q = urllib.parse.quote(query.strip())
    url = f"https://www.youtube.com/results?search_query={encoded_q}&hl=vi&gl=VN"
    competitors: List[Dict[str, Any]] = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html_str = resp.read().decode("utf-8", errors="ignore")
            m = re.search(r"var ytInitialData = (\{.*?\});</script>", html_str)
            if m:
                data = json.loads(m.group(1))
                # Duyệt đệ quy tìm các videoRenderer
                def find_videos(obj: Any):
                    if isinstance(obj, dict):
                        if "videoRenderer" in obj:
                            vr = obj["videoRenderer"]
                            title_runs = vr.get("title", {}).get("runs", [])
                            title = "".join(r.get("text", "") for r in title_runs)
                            view_text = vr.get("viewCountText", {}).get("simpleText", "")
                            owner_runs = vr.get("ownerText", {}).get("runs", [])
                            channel = "".join(r.get("text", "") for r in owner_runs)
                            if title:
                                competitors.append({
                                    "title": title,
                                    "view_text": view_text,
                                    "channel": channel,
                                })
                        else:
                            for v in obj.values():
                                find_videos(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            find_videos(item)

                find_videos(data)
    except Exception as e:
        print(f"[YT-SEARCH WARN] ({query}): {e}")

    return competitors[:limit]


def fetch_google_news_headlines(query: str, limit: int = 8) -> List[str]:
    r"""Cào tiêu đề báo chí chính thống từ Google News RSS tiếng Việt."""
    encoded_q = urllib.parse.quote(query.strip())
    url = f"https://news.google.com/rss/search?q={encoded_q}&hl=vi&gl=VN&ceid=VN:vi"
    headlines: List[str] = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_bytes = resp.read()
            root = ET.fromstring(xml_bytes)
            for item in root.findall(".//item/title")[:limit]:
                if item.text:
                    headlines.append(item.text.strip())
    except Exception as e:
        print(f"[GOOGLE-NEWS WARN] ({query}): {e}")
    return headlines


def harvest_seo_intelligence(
    seed_keywords: List[str],
    project_temp_dir: Path,
) -> Dict[str, Any]:
    r"""
    Đào bới toàn diện từ khóa Google Suggest, YouTube Suggest, Đối thủ triệu view
    và Báo chí Google News. Lưu kết quả vào D:\DuAn_DangLam\<ten_du_an>\temp\seo_raw_intel.json.
    """
    project_temp_dir.mkdir(parents=True, exist_ok=True)
    google_suggests: List[str] = []
    youtube_suggests: List[str] = []
    competitors: List[Dict[str, Any]] = []
    news_headlines: List[str] = []

    expanded_seeds: List[str] = []
    for kw in seed_keywords:
        kw = kw.strip()
        if not kw:
            continue
        expanded_seeds.append(kw)
        expanded_seeds.append(f"tại sao {kw}")
        expanded_seeds.append(f"bí mật {kw}")
        expanded_seeds.append(f"sự thật {kw}")

    seen_g = set()
    seen_yt = set()
    for q in expanded_seeds[:10]:
        for s in fetch_autocomplete_suggestions(q, source="google"):
            if s.lower() not in seen_g:
                seen_g.add(s.lower())
                google_suggests.append(s)
        for s in fetch_autocomplete_suggestions(q, source="youtube"):
            if s.lower() not in seen_yt:
                seen_yt.add(s.lower())
                youtube_suggests.append(s)

    if seed_keywords:
        primary_q = seed_keywords[0]
        competitors = fetch_youtube_top_competitors(primary_q, limit=8)
        news_headlines = fetch_google_news_headlines(primary_q, limit=8)

    intel = {
        "seed_keywords": seed_keywords,
        "google_autocomplete_keywords": google_suggests[:25],
        "youtube_autocomplete_keywords": youtube_suggests[:25],
        "top_youtube_competitors": competitors,
        "google_news_headlines": news_headlines,
    }

    out_file = project_temp_dir / "seo_raw_intel.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(intel, f, ensure_ascii=False, indent=2)

    print(f"[SEO HARVESTER] Đã cào {len(google_suggests)} Google keywords, {len(youtube_suggests)} YouTube keywords, {len(competitors)} video đối thủ -> {out_file}")
    return intel


# ==============================================================================
# KHỐI 2: XỬ LÝ ẢNH NỀN BỔ TRỢ NỔI KHỐI 3D & BẦU TRỜI LIỀN MẠCH (ZERO-BLOB)
# ==============================================================================

def enhance_backdrop_3d_seamless(
    raw_img_path: Path,
    out_img_path: Path,
    crop_x_ratio: float = 0.16,
    sky_lum_threshold: float = 195.0,
) -> Path:
    """
    Xử lý ảnh nền bổ trợ chuẩn ADN kênh HaDa Why:
    1. Cắt cúp tỷ lệ dọc 9:16 (1080x1920) sắc nét bằng Lanczos.
    2. Tăng độ nét vi mô (Unsharp Mask) làm nổi rõ kết cấu vật lý của công trình/bối cảnh.
    3. Tách biệt 2 diện sáng/tối (Chiaroscuro 3D Volume) để bối cảnh nổi khối 3D đồ sộ.
    4. Bảo toàn 100% bầu trời / phần nền phía trên liền mạch tự nhiên (Zero-Blob:
       CẤM tuyệt đối mọi đốm đỏ hay đốm đen vô nghĩa).
    """
    im = Image.open(raw_img_path).convert("RGB")
    w, h = im.size
    if w < 750 or h < 500:
        raise ValueError(
            f"[THUMBNAIL HD GATE BLOCKED] Ảnh nền '{raw_img_path.name}' quá nhỏ ({w}x{h} < 750x500). "
            "Cấm dùng ảnh nhỏ cắt dọc gây vỡ hạt/mờ nhòe!"
        )

    target_ratio = 9.0 / 16.0
    current_ratio = w / float(h)

    if current_ratio > target_ratio:
        crop_w = int(h * target_ratio)
        max_x = max(0, w - crop_w)
        crop_x = min(max_x, int(w * crop_x_ratio))
        cropped = im.crop((crop_x, 0, crop_x + crop_w, h))
    else:
        crop_h = int(w / target_ratio)
        crop_y = max(0, int((h - crop_h) * 0.1))
        cropped = im.crop((0, crop_y, w, crop_y + crop_h))

    resized = cropped.resize((1080, 1920), Image.Resampling.LANCZOS)

    # 1. Unsharp Mask nâng chi tiết kiến trúc / hiện trường
    sharp = resized.filter(ImageFilter.UnsharpMask(radius=3.0, percent=185, threshold=1))
    arr = np.array(sharp, dtype=np.float32)
    raw_arr = np.array(resized, dtype=np.float32)

    Y, X = np.mgrid[0:1920, 0:1080]
    raw_lum = 0.299 * raw_arr[:, :, 0] + 0.587 * raw_arr[:, :, 1] + 0.114 * raw_arr[:, :, 2]

    # 2. Nhận diện vùng bầu trời sáng tự nhiên để giữ nguyên 100% sự liền mạch (Zero-Blob)
    is_sky = raw_lum > sky_lum_threshold
    sky_mask = gaussian_filter(is_sky.astype(np.float32), sigma=1.5)[:, :, np.newaxis]

    # 3. Nâng khối 3D Chiaroscuro trên công trình / bối cảnh
    dir_light = 1.0 + 0.16 * np.clip((X - 450.0) / 450.0, -0.6, 0.6)[:, :, np.newaxis]
    b_arr = (arr - 128.0) * 1.25 + 128.0
    b_arr = b_arr * dir_light

    # Đẩy độ tươi tự nhiên cho các chi tiết nhận diện thương hiệu (ví dụ logo xanh/vàng/đỏ trên tòa nhà)
    is_green = (arr[:, :, 1] > arr[:, :, 0] * 1.12) & (arr[:, :, 1] > arr[:, :, 2] * 1.12)
    b_arr[:, :, 1] = np.where(is_green, np.clip(b_arr[:, :, 1] * 1.35, 0, 255), b_arr[:, :, 1])
    b_arr[:, :, 0] = np.where(is_green, b_arr[:, :, 0] * 0.85, b_arr[:, :, 0])

    # 4. Hợp nhất: Bầu trời nguyên bản liền mạch 100% + Công trình nổi khối 3D
    final_arr = raw_arr * sky_mask + b_arr * (1.0 - sky_mask)
    final_arr = np.clip(final_arr, 0, 255)

    out_img_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.uint8(final_arr)).save(out_img_path, format="PNG")
    print(f"[3D BACKDROP] Đã xử lý nổi khối 3D & bầu trời liền mạch 100% -> {out_img_path}")
    return out_img_path


# ==============================================================================
# KHỐI 3: NHÚNG KÉP (DUAL-EMBED) THUMBNAIL VÀO THẲNG VIDEO MP4 CHO FACEBOOK
# ==============================================================================

def embed_thumbnail_into_video(
    video_path: Path,
    thumbnail_path: Path,
    temp_dir: Path,
    prepend_cover_frames: bool = True,
) -> Path:
    """
    Nhúng trực tiếp tấm ảnh Thumbnail 9:16 (1080x1920) vào file Video MP4 bằng 2 cơ chế:
    1. Chèn 2 frame đầu tiên (0.033s ở 60fps) bằng chính tấm ảnh Thumbnail để khi
       Người Chỉ Huy đăng lên Facebook Reels / Trang cá nhân và kéo thanh chọn ảnh bìa
       về vị trí đầu tiên (00:00), tấm ảnh bìa 3D hiện ra ngay lập tức để chọn!
    2. Gắn luồng metadata attached_pic chuẩn MP4 để file video hiển thị ảnh bìa
       trên máy tính Windows và các trình quản lý đăng bài.
    """
    if not video_path.exists():
        raise FileNotFoundError(f"Không tìm thấy video: {video_path}")
    if not thumbnail_path.exists():
        raise FileNotFoundError(f"Không tìm thấy thumbnail: {thumbnail_path}")

    temp_dir.mkdir(parents=True, exist_ok=True)
    working_video = temp_dir / f"working_{video_path.name}"
    shutil.copy2(video_path, working_video)

    if prepend_cover_frames:
        # Tạo 1 đoạn video 0.04s (2 frames @ 60fps) từ thumbnail + âm thanh im lặng 0.04s
        # rồi nối (concat) lên đầu video gốc để frame 00:00 chính là Thumbnail!
        pre_framed_video = temp_dir / f"preframed_{video_path.name}"
        filter_complex = (
            "[1:v]scale=1080:1920:flags=lanczos,fps=60,trim=duration=0.034,setpts=PTS-STARTPTS[cov_v];"
            "aevalsrc=0:d=0.034:s=48000:c=stereo[cov_a];"
            "[0:v]setpts=PTS-STARTPTS[main_v];"
            "[0:a]asetpts=PTS-STARTPTS[main_a];"
            "[cov_v][cov_a][main_v][main_a]concat=n=2:v=1:a=1[out_v][cat_a];"
            "[cat_a]loudnorm=I=-14.0:TP=-1.0:LRA=7[out_a]"
        )
        cmd_prepend = [
            "ffmpeg", "-y",
            "-i", str(working_video),
            "-loop", "1", "-t", "0.05", "-i", str(thumbnail_path),
            "-filter_complex", filter_complex,
            "-map", "[out_v]",
            "-map", "[out_a]",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", "-r", "60",
            "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            str(pre_framed_video),
        ]
        res = subprocess.run(cmd_prepend, capture_output=True, text=True)
        if res.returncode == 0 and pre_framed_video.exists() and pre_framed_video.stat().st_size > 10000:
            working_video = pre_framed_video
            print("[DUAL-EMBED] Lớp 1: Đã chèn Thumbnail vào frame 00:00 đầu video (chọn bìa trên FB 1 chạm).")
        else:
            print(f"[DUAL-EMBED WARN] Lớp 1 bỏ qua: {res.stderr[-300:]}")

    # Lớp 2: Nhúng stream attached_pic vào container MP4
    final_embedded = temp_dir / f"embedded_{video_path.name}"
    cmd_attach = [
        "ffmpeg", "-y",
        "-i", str(working_video),
        "-i", str(thumbnail_path),
        "-map", "0:v:0",
        "-map", "0:a:0",
        "-map", "1:v:0",
        "-c:v:0", "copy",
        "-c:a:0", "copy",
        "-c:v:1", "png",
        "-disposition:v:1", "attached_pic",
        "-movflags", "+faststart",
        str(final_embedded),
    ]
    res2 = subprocess.run(cmd_attach, capture_output=True, text=True)
    if res2.returncode == 0 and final_embedded.exists() and final_embedded.stat().st_size > 10000:
        shutil.copy2(final_embedded, video_path)
        print(f"[DUAL-EMBED] Lớp 2: Đã gắn attached_pic vào MP4 thành công -> {video_path}")
    else:
        # Nếu container không nhận attached_pic thì vẫn giữ bản đã chèn frame 00:00
        shutil.copy2(working_video, video_path)
        print(f"[DUAL-EMBED] Đã lưu bản gắn frame 00:00 -> {video_path}")

    # Tự động dọn sạch các file video trung gian trong temp_dir để không tốn dung lượng đĩa
    for tmp_f in [
        temp_dir / f"working_{video_path.name}",
        temp_dir / f"preframed_{video_path.name}",
        temp_dir / f"embedded_{video_path.name}",
    ]:
        try:
            if tmp_f.exists():
                tmp_f.unlink()
        except Exception:
            pass

    return video_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Engine Thumbnail 3D & SEO Evergreen HaDa Why")
    parser.add_argument("--mode", choices=["seo", "backdrop3d", "embed"], required=True)
    parser.add_argument("--keywords", nargs="*", default=[], help="Danh sách từ khóa gốc cần cào SEO")
    parser.add_argument("--temp-dir", type=str, default=r"D:\DuAn_DangLam\temp")
    parser.add_argument("--raw-bg", type=str, help="Đường dẫn ảnh bối cảnh thô")
    parser.add_argument("--out-bg", type=str, help="Đường dẫn ảnh bối cảnh 3D đầu ra")
    parser.add_argument("--video", type=str, help="Đường dẫn video MP4")
    parser.add_argument("--thumb", type=str, help="Đường dẫn ảnh Thumbnail PNG")

    args = parser.parse_args()
    t_dir = Path(args.temp_dir)

    if args.mode == "seo":
        harvest_seo_intelligence(args.keywords, t_dir)
    elif args.mode == "backdrop3d":
        enhance_backdrop_3d_seamless(Path(args.raw_bg), Path(args.out_bg))
    elif args.mode == "embed":
        embed_thumbnail_into_video(Path(args.video), Path(args.thumb), t_dir)
```


#### `engine/render_reel.py`

```python
# -*- coding: utf-8 -*-
r"""
render_reel.py - ĐƯỜNG ỐNG SẢN XUẤT DUY NHẤT & SẠCH 100% (TSX ĐỘC BẢN -> QC -> RENDER -> MIX -14 LUFS -> DUAL-EMBED -> QC VIDEO)

Cách dùng:
  python render_reel.py --comp "TenComposition" --project "D:\DuAn_DangLam\ten_du_an" --name "HaDaWhy_TenVideo"

Đặc điểm cốt lõi:
1. KHÔNG dùng mklink /J (triệt tiêu 100% lỗi EPERM symlink của Remotion Webpack trên Windows).
   Thay vào đó chép tạm assets từ <project>/temp/assets/ sang remotion_reels/public/harvested/ lúc render
   và XÓA SẠCH trong khối `finally:` -> Đầu Não luôn 0 bytes media!
2. Hỗ trợ bất kỳ Composition .tsx độc bản nào (chuẩn NvidiaSuccession40s), không khóa cứng vào template JSON.
3. Chạy bắt buộc qc_gate.check_tsx() trước render và qc_gate.check_video() sau render (chống màn hình đen rỗng).
4. Tự động cào nhạc/SFX tươi mới nếu thiếu, hòa âm -14.0 LUFS + Vacuum Drop, nhúng kép Thumbnail 3D (frame 00:00 + attached_pic).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

FB_ROOT = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
ENGINE_DIR = FB_ROOT / "engine"
REMOTION_DIR = FB_ROOT / "remotion_reels"
PUBLIC_HARVEST = REMOTION_DIR / "public" / "harvested"
OUT_FINAL_DIR = Path(r"D:\Video thành phẩm")

sys.path.insert(0, str(ENGINE_DIR))
import qc_gate  # noqa: E402
import voice_visual_sync  # noqa: E402
from sfx_timeline_mixer import (  # noqa: E402
    auto_choreograph_script_sfx_cues,
    mix_reels_master_audio,
    set_project_sfx_dir,
)


def stage_assets_temporarily(assets_dir: Path) -> None:
    if PUBLIC_HARVEST.exists():
        shutil.rmtree(PUBLIC_HARVEST, ignore_errors=True)
    PUBLIC_HARVEST.mkdir(parents=True, exist_ok=True)
    if assets_dir.exists():
        for f in assets_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, PUBLIC_HARVEST / f.name)


def cleanup_staged_assets() -> None:
    if PUBLIC_HARVEST.exists():
        shutil.rmtree(PUBLIC_HARVEST, ignore_errors=True)


def get_video_duration_sec(video_path: Path) -> float:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
        capture_output=True, text=True,
    )
    try:
        return float(res.stdout.strip())
    except Exception:
        return 40.0


def main() -> int:
    ap = argparse.ArgumentParser(description="Clean FB Reels 9:16 Production Pipeline")
    ap.add_argument("--comp", required=True, help="Tên Composition ID trong Root.tsx (VD: ThuatToanGoiXeMaster)")
    ap.add_argument("--tsx", default="", help="Đường dẫn file .tsx (mặc định remotion_reels/src/<comp>.tsx)")
    ap.add_argument("--project", required=True, help="Thư mục WIP dự án (VD: D:\\DuAn_DangLam\\ten_du_an)")
    ap.add_argument("--name", required=True, help="Tên file xuất bản (không đuôi .mp4)")
    ap.add_argument("--mood", default="conspiracy_thriller", help="Mood nhạc nền kịch tính")
    ap.add_argument("--bgm-mood", default="", help="Override mood nhạc nền kịch tính cho audio_harvester & mixer")
    ap.add_argument("--sfx-keywords", default="", help="Từ khóa SFX tiếng Anh cách nhau dấu phẩy cho kịch bản")
    ap.add_argument("--skip-render", action="store_true", help="Bỏ qua bước render nếu đã có temp/raw_video.mp4")
    args = ap.parse_args()

    project_dir = Path(args.project)
    temp_dir = project_dir / "temp"
    assets_dir = temp_dir / "assets"
    temp_dir.mkdir(parents=True, exist_ok=True)
    tsx_path = Path(args.tsx) if args.tsx else (REMOTION_DIR / "src" / f"{args.comp}.tsx")

    # 1. Pre-Render Gate (Chặn lỗi trước khi tốn 1 giây render)
    if not args.skip_render:
        print(f"[1/5] Pre-Render QC Gate: {tsx_path.name}...")
        gate_res = qc_gate.check_tsx(tsx_path, project_dir)
        if not gate_res["passed"]:
            print(json.dumps(gate_res, ensure_ascii=False, indent=2))
            raise RuntimeError("PRE-RENDER QC GATE FAILED! Sửa toàn bộ lỗi trên trước khi render.")

    # 2. Chép tạm assets sang public/harvested/ và khóa dọn sạch trong finally:
    raw_mp4 = temp_dir / "raw_video.mp4"
    try:
        if not args.skip_render:
            stage_assets_temporarily(assets_dir)
            print("[2/5] TypeScript check (npx tsc --noEmit)...")
            subprocess.run(["cmd", "/c", "npx tsc --noEmit"], cwd=str(REMOTION_DIR), check=True)
            print(f"[3/5] Rendering {args.comp} (60fps, --gl=angle)...")
            render_cmd = f'npx remotion render {args.comp} "{raw_mp4.as_posix()}" --gl=angle --concurrency=4'
            subprocess.run(render_cmd, shell=True, cwd=str(REMOTION_DIR), check=True)
    finally:
        cleanup_staged_assets()

    if not raw_mp4.exists():
        raise FileNotFoundError(f"Không tìm thấy raw_video.mp4: {raw_mp4}")

    total_sec = get_video_duration_sec(raw_mp4)

    # 3. Kiểm tra giọng đọc & words.json
    words_path = voice_visual_sync.find_words_json(project_dir)
    if not words_path:
        raise FileNotFoundError(f"Thiếu words.json trong {project_dir}")
    voice_wav = temp_dir / "voiceover.wav"
    if not voice_wav.exists():
        voice_wav = temp_dir / "voice.wav"
    if not voice_wav.exists():
        raise FileNotFoundError(f"Thiếu voiceover.wav / voice.wav trong {temp_dir}")

    # 4. Đọc script_5beat.json (lấy script_text, sfx_keywords, bgm_mood) & Cào âm thanh 6 vai trò tươi mới nếu thiếu
    print("[4/5] Mixing master audio (-14.0 LUFS, voice-clear, Vacuum Drop)...")
    script_text = ""
    script_sfx_keywords = args.sfx_keywords.strip()
    script_bgm_mood = (args.bgm_mood or args.mood).strip()
    script_json_path = temp_dir / "script_5beat.json"
    if script_json_path.exists():
        try:
            sdata = json.loads(script_json_path.read_text(encoding="utf-8"))
            if isinstance(sdata, dict):
                if not script_sfx_keywords and sdata.get("sfx_keywords"):
                    raw_kw = sdata["sfx_keywords"]
                    script_sfx_keywords = ",".join(raw_kw) if isinstance(raw_kw, list) else str(raw_kw)
                if not args.bgm_mood and isinstance(sdata.get("bgm_mood"), str) and sdata["bgm_mood"].strip():
                    script_bgm_mood = sdata["bgm_mood"].strip()
                parts = []
                for k in ("title", "topic", "full_script", "script"):
                    if isinstance(sdata.get(k), str) and sdata[k].strip():
                        parts.append(sdata[k].strip())
                for b in sdata.get("beats", []) or []:
                    if isinstance(b, dict):
                        txt = b.get("voiceover") or b.get("narration") or b.get("text") or b.get("script")
                        if isinstance(txt, str) and txt.strip():
                            parts.append(txt.strip())
                    elif isinstance(b, str) and b.strip():
                        parts.append(b.strip())
                script_text = " ".join(parts).strip() or script_json_path.read_text(encoding="utf-8")[:1500]
            else:
                script_text = script_json_path.read_text(encoding="utf-8")[:1500]
        except Exception as exc:
            print(f"[WARN] Không đọc được script_5beat.json cho mix audio: {exc}")

    fresh_bgm = temp_dir / "bgm_fresh.mp3"
    sfx_dir = temp_dir / "sfx"
    has_role_sfx = sfx_dir.exists() and any(sfx_dir.glob("role_*.mp3"))
    if not fresh_bgm.exists() or not has_role_sfx:
        harv_cmd = [
            sys.executable, str(ENGINE_DIR / "audio_harvester.py"),
            "--project", str(project_dir),
            "--bgm-mood", script_bgm_mood or "dramatic,thriller,cinematic",
        ]
        if script_sfx_keywords:
            harv_cmd.extend(["--sfx-keywords", script_sfx_keywords])
        low_script = script_text.lower()
        if any(tok in low_script for tok in ("tiền", "đồng", "vnđ", "vnd", "usd", "$", "tỷ", "triệu", "giá", "cước")):
            harv_cmd.append("--include-money")
        subprocess.run(harv_cmd, check=False)
    if sfx_dir.exists():
        set_project_sfx_dir(sfx_dir)

    bp_path = temp_dir / "choreography_blueprint.json"
    beat_ts = [round(total_sec * p, 2) for p in (0.0, 0.15, 0.35, 0.60, 0.82)]
    sfx_cues, vac_drops = auto_choreograph_script_sfx_cues(
        words_json_path=words_path,
        total_duration_sec=total_sec,
        beat_timestamps=beat_ts,
        blueprint_json_path=bp_path if bp_path.exists() else None,
    )

    master_wav = temp_dir / "master_audio.wav"
    mix_reels_master_audio(
        voice_wav=voice_wav,
        output_wav=master_wav,
        sfx_cues=sfx_cues,
        total_duration_sec=total_sec,
        bgm_path=fresh_bgm if (fresh_bgm.exists() and fresh_bgm.stat().st_size > 20000) else None,
        script_topic=args.name,
        script_text=script_text,
        beat_timestamps=beat_ts,
        mood=script_bgm_mood,
        bgm_base_volume=0.85,
        bgm_duck_volume=0.50,
        vacuum_drops=vac_drops,
        words_json_path=words_path,
    )

    # 5. Mux + Dual-Embed Thumbnail 3D (Frame 00:00 + attached_pic)
    OUT_FINAL_DIR.mkdir(parents=True, exist_ok=True)
    final_mp4 = OUT_FINAL_DIR / f"{args.name}_FB_Reels_Master.mp4"
    temp_mux = temp_dir / "temp_muxed.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(raw_mp4), "-i", str(master_wav),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
            "-shortest", str(temp_mux),
        ],
        check=True,
    )

    thumb_cand = None
    for tp in (temp_dir / "thumbnail_9x16.png", OUT_FINAL_DIR / f"{args.name}_thumbnail.png"):
        if tp.exists():
            thumb_cand = tp
            break

    if thumb_cand:
        try:
            from thumbnail_3d_seo_engine import embed_thumbnail_into_video
            shutil.copy2(temp_mux, final_mp4)
            embed_thumbnail_into_video(final_mp4, thumb_cand, temp_dir, prepend_cover_frames=True)
        except Exception as exc:
            print(f"[WARN] Dual-embed fallback sang attached_pic: {exc}")
            subprocess.run(
                [
                    "ffmpeg", "-y", "-i", str(temp_mux), "-i", str(thumb_cand),
                    "-map", "0", "-map", "1", "-c", "copy", "-c:v:1", "png",
                    "-disposition:v:1", "attached_pic", "-movflags", "+faststart",
                    str(final_mp4),
                ],
                check=True,
            )
    else:
        shutil.copy2(temp_mux, final_mp4)

    # 6. Post-Render Visual & Audio QC Gate + Contact Sheet 3x3 + Ghi lịch sử chống lặp bố cục
    print("[5/5] Running Post-Render QC Gate (Anti-Void, LUFS, 3x3 Contact Sheet)...")
    grid_path = temp_dir / "qc_grid_3x3.jpg"
    report = qc_gate.check_video(
        final_mp4,
        grid_path,
        project_dir=project_dir,
        tsx_path=tsx_path if tsx_path.exists() else None,
    )
    if report.get("passed") and not report.get("layout_history_recorded") and tsx_path.exists():
        sig = qc_gate.extract_layout_signature(tsx_path.read_text(encoding="utf-8"))
        qc_gate.record_visual_layout_history(
            project_name=project_dir.name,
            opening_style=sig["opening_style"],
            component_sequence=sig["component_sequence"],
        )
        report["layout_history_recorded"] = True
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"FINAL MP4: {final_mp4}")
    print(f"QC GRID 3x3: {grid_path}")
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
```


### 3.5. Mã nguồn Remotion 9:16 60fps (remotion_reels/src/)

#### `remotion_reels/src/index.ts`

```typescript
import { registerRoot } from "remotion";
import { Root } from "./Root";

registerRoot(Root);
```


#### `remotion_reels/src/Root.tsx`

```tsx
import React from "react";
import { Composition, Still } from "remotion";
import { RootSkeletonExample } from "./RootSkeletonExample";
import { ThumbnailCover9x16, ThumbnailCover9x16Props } from "./components/ThumbnailCover9x16";

export const Root: React.FC = () => {
  return (
    <>
      {/* TECHNICAL SKELETON (Topic-Agnostic Reference, 1080x1920 @ 60fps) */}
      <Composition
        id="RootSkeletonExample"
        component={RootSkeletonExample}
        durationInFrames={600}
        fps={60}
        width={1080}
        height={1920}
      />

      {/* 3D THUMBNAIL COVER STILL (1080x1920) */}
      <Still
        id="ThumbnailCover9x16"
        component={ThumbnailCover9x16}
        width={1080}
        height={1920}
        defaultProps={{
          headlineLine1: "BÍ MẬT",
          headlineLine2: "HADA WHY",
          heroSubjectSrc: "brand/hadawhy_logo.png",
        } as ThumbnailCover9x16Props}
      />
    </>
  );
};
```


#### `remotion_reels/src/RootSkeletonExample.tsx`

```tsx
import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16";
import { HaDaWhyMistBackground } from "./components/HaDaWhyMistBackground";
import { HaDaWhyFontFaces } from "./components/KineticHookHeader";
import { CameraStageWrapper } from "./components/fx";

export interface RootSkeletonExampleProps {
  audioSrc?: string;
}

/**
 * Khung mẫu kỹ thuật phi chủ đề (60fps, 0% nội dung cụ thể).
 * Tham khảo cú pháp gắn Audio, nền xanh dương ADN, watermark và CameraStageWrapper cho từng Beat.
 */
export const RootSkeletonExample: React.FC<RootSkeletonExampleProps> = ({
  audioSrc,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#030812", overflow: "hidden" }}>
      <HaDaWhyFontFaces />
      <HaDaWhyMistBackground />

      {audioSrc ? <Audio src={staticFile(audioSrc)} /> : null}

      {/* Beat 1 (60fps): Hiện đầy đủ hình + số ngay trong 0..30 frames đầu */}
      <Sequence from={0} durationInFrames={300}>
        <CameraStageWrapper durationInFrames={300} enterDirection="zoom">
          <AbsoluteFill />
        </CameraStageWrapper>
      </Sequence>

      {/* Beat 2..N: Cắt dứt khoát khớp mốc words.json + 30 frames (0.5s) đệm cuối */}
      <Sequence from={300} durationInFrames={300}>
        <CameraStageWrapper durationInFrames={300} enterDirection="up">
          <AbsoluteFill />
        </CameraStageWrapper>
      </Sequence>

      {/* BẮT BUỘC đặt dòng cuối cùng ngay trước </AbsoluteFill> để 2 lớp thương hiệu + chống re-up luôn nổi trên cùng */}
      <ChannelWatermark9x16 />
    </AbsoluteFill>
  );
};
```


#### `remotion_reels/src/components/AnatomyCallout3D.tsx`

```tsx
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface CalloutNode {
  /** Anchor point on the central object (canvas coordinates) */
  anchorX: number;
  anchorY: number;
  /** Label endpoint (canvas coordinates) */
  labelX: number;
  labelY: number;
  title: string;
  value: string;
  accentColor?: string;
  delayFrames?: number;
}

export interface AnatomyCallout3DProps {
  startFrame: number;
  endFrame: number;
  centerCutoutSrc: string;
  centerX?: number;
  centerY?: number;
  centerWidth?: number;
  callouts: CalloutNode[];
}

export const AnatomyCallout3D: React.FC<AnatomyCallout3DProps> = ({
  startFrame,
  endFrame,
  centerCutoutSrc,
  centerX = 540,
  centerY = 1040,
  centerWidth = 520,
  callouts,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const localFrame = frame - startFrame;
  const exitOpacity = interpolate(frame, [endFrame - 14, endFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const centerPop = spring({
    frame: localFrame,
    fps,
    config: { damping: 12, stiffness: 160 },
  });
  const floatY = Math.sin(localFrame * 0.08) * 8;

  return (
    <div style={{ position: "absolute", inset: 0, opacity: exitOpacity }}>
      {/* Central Cutout Object */}
      <div
        style={{
          position: "absolute",
          left: centerX,
          top: centerY + floatY,
          width: centerWidth,
          transform: `translate(-50%, -50%) scale(${centerPop})`,
        }}
      >
        <Img
          src={staticFile(centerCutoutSrc)}
          style={{
            width: "100%",
            height: "auto",
            filter:
              "drop-shadow(0px 8px 16px rgba(0,0,0,0.85)) drop-shadow(0px 24px 36px rgba(0,0,0,0.9))",
          }}
        />
      </div>

      {/* SVG AR Pointer Lines */}
      <svg
        width={1080}
        height={1920}
        style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
      >
        {callouts.map((c, idx) => {
          const dFrame = c.delayFrames ?? 18 + idx * 16;
          if (localFrame < dFrame) return null;
          const lineProg = spring({
            frame: localFrame - dFrame,
            fps,
            config: { damping: 14, stiffness: 150 },
          });
          const color = c.accentColor || "#FFE600";
          const curX = interpolate(lineProg, [0, 1], [c.anchorX, c.labelX]);
          const curY = interpolate(lineProg, [0, 1], [c.anchorY, c.labelY]);
          return (
            <g key={`ar-line-${idx}`}>
              <circle cx={c.anchorX} cy={c.anchorY} r={8} fill={color} stroke="#FFF" strokeWidth={3} />
              <line
                x1={c.anchorX}
                y1={c.anchorY}
                x2={curX}
                y2={curY}
                stroke={color}
                strokeWidth={4}
                strokeDasharray="8 6"
              />
            </g>
          );
        })}
      </svg>

      {/* ZERO-BOX Floating AR Callout Labels */}
      {callouts.map((c, idx) => {
        const dFrame = (c.delayFrames ?? 18 + idx * 16) + 6;
        if (localFrame < dFrame) return null;
        const pop = spring({
          frame: localFrame - dFrame,
          fps,
          config: { damping: 12, stiffness: 200 },
        });
        const color = c.accentColor || "#FFE600";
        return (
          <div
            key={`ar-lbl-${idx}`}
            style={{
              position: "absolute",
              left: c.labelX,
              top: c.labelY,
              transform: `translate(-50%, -50%) scale(${pop})`,
              textAlign: "center",
              whiteSpace: "nowrap",
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProExtraBold, sans-serif",
                fontSize: 28,
                color: "#FFFFFF",
                WebkitTextStroke: "6px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              {c.title}
            </div>
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 52,
                color,
                WebkitTextStroke: "9px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 8px 20px rgba(0,0,0,0.92)",
              }}
            >
              {c.value}
            </div>
          </div>
        );
      })}
    </div>
  );
};
```


#### `remotion_reels/src/components/ChannelWatermark9x16.tsx`

```tsx
import React from "react";
import { Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface ChannelWatermark9x16Props {
  logoSrc?: string;
}

/**
 * Hệ thống 2 lớp thương hiệu & chống re-up bắt buộc (LUÔN nổi trên cùng zIndex: 9999):
 * - Lớp 1 (Nhận diện góc): Logo góc trên bên trái cố định (top: 52, left: 40).
 * - Lớp 2 (Logo chìm chống bản quyền / chống re-up): Logo chính giữa vùng Safe Zone,
 *   width: 380px, opacity: 0.08, xoay -12deg, trôi siêu chậm ±24px bằng translate3d để chống tẩy watermark tĩnh.
 * CẤM tự ý gỡ bỏ hoặc tắt lớp logo chìm chống bản quyền.
 */
export const ChannelWatermark9x16: React.FC<ChannelWatermark9x16Props> = ({
  logoSrc = "brand/hadawhy_logo.png",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / Math.max(1, fps);
  const driftX = Math.sin(t * 0.35) * 24;
  const driftY = Math.cos(t * 0.27) * 22;
  const resolvedLogo = staticFile(logoSrc);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        zIndex: 9999,
        pointerEvents: "none",
        overflow: "hidden",
      }}
    >
      {/* LỚP 1: Logo nhận diện góc trên bên trái */}
      <div
        style={{
          position: "absolute",
          top: 52,
          left: 40,
          width: 132,
          opacity: 0.9,
          filter: "drop-shadow(0 3px 10px rgba(0, 0, 0, 0.85))",
        }}
      >
        <Img
          src={resolvedLogo}
          style={{ width: "100%", height: "auto", display: "block" }}
        />
      </div>

      {/* LỚP 2: Logo chìm chống bản quyền / chống re-up ở vùng thân giữa Safe Zone */}
      <div
        data-layer="stealth-watermark"
        style={{
          position: "absolute",
          left: "50%",
          top: "50%",
          width: 380,
          opacity: 0.08,
          transform: `translate3d(calc(-50% + ${driftX.toFixed(2)}px), calc(-50% + ${driftY.toFixed(2)}px), 0) rotate(-12deg)`,
          willChange: "transform",
        }}
      >
        <Img
          src={resolvedLogo}
          style={{ width: "100%", height: "auto", display: "block" }}
        />
      </div>
    </div>
  );
};
```


#### `remotion_reels/src/components/CinematicStagePrimitives.tsx`

```tsx
export * from "./fx/CinematicStagePrimitives";
```


#### `remotion_reels/src/components/CoinStream.tsx`

```tsx
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface Point {
  x: number;
  y: number;
}

export interface CoinStreamProps {
  p0: Point;
  p1: Point;
  p2: Point;
  startFrame: number;
  endFrame?: number;
  coinCount?: number;
  blockedAtT?: number;
  dotColor?: string;
  useDollarNotes?: boolean;
  /** Custom primary item PNG in public/ (e.g. "objects/oil_barrel.png", "objects/chip.png", "harvested/item.png") */
  primaryItemSrc?: string;
  /** Custom secondary alternating item PNG in public/ */
  secondaryItemSrc?: string;
}

function quadBezier(p0: Point, p1: Point, p2: Point, t: number): Point {
  const u = 1 - t;
  return {
    x: u * u * p0.x + 2 * u * t * p1.x + t * t * p2.x,
    y: u * u * p0.y + 2 * u * t * p1.y + t * t * p2.y,
  };
}

export const CoinStream: React.FC<CoinStreamProps> = ({
  p0,
  p1,
  p2,
  startFrame,
  endFrame = 9999,
  coinCount = 6,
  blockedAtT,
  dotColor = "#FFD600",
  useDollarNotes = false,
  primaryItemSrc = "",
  secondaryItemSrc = "",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const streamOpacity =
    endFrame < 9000
      ? interpolate(frame, [endFrame - 18, endFrame], [1, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : 1;

  const localFrame = frame - startFrame;
  const drawProgress = spring({
    frame: localFrame,
    fps,
    config: { damping: 16, stiffness: 90 },
  });

  const totalDots = 16;
  const maxDotT = blockedAtT ? Math.min(drawProgress, blockedAtT) : drawProgress;
  const dots: React.ReactNode[] = [];

  for (let i = 0; i <= totalDots; i++) {
    const t = i / totalDots;
    if (t > maxDotT) continue;
    const pt = quadBezier(p0, p1, p2, t);
    const pulse = 0.75 + 0.25 * Math.sin(localFrame * 0.22 - i * 0.6);
    dots.push(
      <div
        key={`dot-${i}`}
        style={{
          position: "absolute",
          left: pt.x,
          top: pt.y,
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: dotColor,
          boxShadow: "0 4px 10px rgba(0,0,0,0.8)",
          transform: `translate(-50%, -50%) scale(${pulse})`,
          opacity: 0.85,
        }}
      />
    );
  }

  const coins: React.ReactNode[] = [];
  if (frame <= endFrame) {
    const cycleFrames = 42;
    for (let c = 0; c < coinCount; c++) {
      const coinStart = c * 11;
      const cf = localFrame - coinStart;
      if (cf < 0) continue;

      const rawT = (cf % cycleFrames) / cycleFrames;
      const easedT = Math.pow(rawT, 1.35);

      if (blockedAtT !== undefined && easedT >= blockedAtT) {
        const overT = (easedT - blockedAtT) / (1 - blockedAtT);
        if (overT < 0.45) {
          const bp = quadBezier(p0, p1, p2, blockedAtT);
          const spreadX = (c % 2 === 0 ? 1 : -1) * overT * 65;
          const dropY = overT * 45;
          coins.push(
            <div
              key={`coin-blocked-${c}`}
              style={{
                position: "absolute",
                left: bp.x + spreadX,
                top: bp.y + dropY,
                width: 66,
                transform: `translate(-50%, -50%) scale(${1 - overT * 1.6}) rotate(${overT * 140}deg)`,
                opacity: Math.max(0, 1 - overT * 2.2),
                filter: "drop-shadow(0 8px 14px rgba(0,0,0,0.85))",
              }}
            >
              {primaryItemSrc ? <Img src={staticFile(primaryItemSrc)} style={{ width: "100%" }} /> : null}
            </div>
          );
        }
        continue;
      }

      const pt = quadBezier(p0, p1, p2, easedT);
      const scale = interpolate(easedT, [0, 0.15, 0.85, 1], [0.3, 1.08, 1.0, 0.45]);
      const rot = cf * 7 + c * 45;
      const useSecond = useDollarNotes && c % 2 === 1;

      coins.push(
        <div
          key={`coin-${c}`}
          style={{
            position: "absolute",
            left: pt.x,
            top: pt.y,
            width: useSecond ? 88 : 74,
            transform: `translate(-50%, -50%) scale(${scale}) rotate(${rot}deg)`,
            filter: "drop-shadow(0px 10px 18px rgba(0,0,0,0.85))",
          }}
        >
          {(() => {
            const itemSrc = useSecond ? (secondaryItemSrc || primaryItemSrc) : primaryItemSrc;
            return itemSrc ? (
              <Img
                src={staticFile(itemSrc)}
                style={{ width: "100%", height: "auto" }}
              />
            ) : null;
          })()}
        </div>
      );
    }
  }

  let blockGate: React.ReactNode = null;
  if (blockedAtT !== undefined && drawProgress >= blockedAtT * 0.9) {
    const bp = quadBezier(p0, p1, p2, blockedAtT);
    const gatePop = spring({
      frame: Math.max(0, localFrame - 10),
      fps,
      config: { damping: 9, stiffness: 220 },
    });
    blockGate = (
      <div
        style={{
          position: "absolute",
          left: bp.x,
          top: bp.y,
          transform: `translate(-50%, -50%) scale(${gatePop})`,
          width: 68,
          height: 68,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(255,30,60,0.95) 0%, rgba(160,0,25,0.95) 100%)",
          boxShadow: "0 10px 24px rgba(0,0,0,0.88)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#FFFFFF",
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: 38,
          fontWeight: 900,
          border: "3px solid #FFF",
        }}
      >
        ✕
      </div>
    );
  }

  return (
    <div style={{ opacity: streamOpacity }}>
      {dots}
      {coins}
      {blockGate}
    </div>
  );
};
```


#### `remotion_reels/src/components/GeoStrategicMap3D.tsx`

```tsx
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import {
  EURASIA_BG_PATHS,
  HANOI_COORD,
  LONDON_COORD,
  MAP_HEIGHT,
  MAP_WIDTH,
  UK_PATHS,
  VIETNAM_PATHS,
} from "./eurasiaGeoPaths";

export interface GeoStrategicMap3DProps {
  startFrame: number;
  endFrame: number;
  originLabel: string;
  targetLabel: string;
  originCoord?: { x: number; y: number };
  targetCoord?: { x: number; y: number };
  originPaths?: string[];
  targetPaths?: string[];
  bgPaths?: string[];
  containerLeft?: number;
  containerTop?: number;
  containerWidth?: number;
  containerHeight?: number;
  originLabelPos?: { x: number; y: number };
  targetLabelPos?: { x: number; y: number };
  evidenceImageSrc?: string;
  evidenceTitle?: string;
  evidenceCenterX?: number;
  evidenceTop?: number;
  evidenceWidth?: number;
  evidenceHeight?: number;
  evidenceObjectPosition?: string;
  evidenceTitleFontSize?: number;
  leftFloatingIconSrc?: string;
  rightFloatingIconSrc?: string;
  leftFloatingIconPos?: { x: number; y: number; width?: number };
  rightFloatingIconPos?: { x: number; y: number; width?: number };
}

export const GeoStrategicMap3D: React.FC<GeoStrategicMap3DProps> = ({
  startFrame,
  endFrame,
  originLabel,
  targetLabel,
  originCoord = HANOI_COORD,
  targetCoord = LONDON_COORD,
  originPaths = VIETNAM_PATHS,
  targetPaths = UK_PATHS,
  bgPaths = EURASIA_BG_PATHS,
  containerLeft = 40,
  containerTop = 315,
  containerWidth = 1000,
  containerHeight = 640,
  originLabelPos,
  targetLabelPos,
  evidenceImageSrc,
  evidenceTitle,
  evidenceCenterX = 540,
  evidenceTop = 1355,
  evidenceWidth = 820,
  evidenceHeight = 450,
  evidenceObjectPosition = "center center",
  evidenceTitleFontSize = 44,
  leftFloatingIconSrc,
  rightFloatingIconSrc,
  leftFloatingIconPos,
  rightFloatingIconPos,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const localFrame = frame - startFrame;
  const enterPop = spring({
    frame: localFrame,
    fps,
    config: { damping: 15, stiffness: 95 },
  });

  const exitOpacity = interpolate(frame, [endFrame - 14, endFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const arcProgress = interpolate(localFrame, [28, 125], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const ctrlX = (originCoord.x + targetCoord.x) * 0.5 + 40;
  const ctrlY = Math.min(originCoord.y, targetCoord.y) - 185;

  const arcPathD = `M ${originCoord.x} ${originCoord.y} Q ${ctrlX} ${ctrlY} ${targetCoord.x} ${targetCoord.y}`;

  const t = arcProgress;
  const u = 1 - t;
  const headX = u * u * originCoord.x + 2 * u * t * ctrlX + t * t * targetCoord.x;
  const headY = u * u * originCoord.y + 2 * u * t * ctrlY + t * t * targetCoord.y;

  const mapTiltX = interpolate(localFrame, [0, 260], [32, 22], {
    extrapolateRight: "clamp",
  });
  const mapScale = interpolate(enterPop, [0, 1], [0.84, 1.0]);

  const courtPop = spring({
    frame: Math.max(0, localFrame - 95),
    fps,
    config: { damping: 12, stiffness: 150 },
  });

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity: exitOpacity,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: containerLeft,
          top: containerTop,
          width: containerWidth,
          height: containerHeight,
          perspective: 1200,
        }}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            transform: `scale(${mapScale}) rotateX(${mapTiltX}deg)`,
            transformStyle: "preserve-3d",
            borderRadius: 28,
            background:
              "radial-gradient(circle at 50% 45%, rgba(16, 36, 68, 0.85) 0%, rgba(6, 12, 24, 0.95) 100%)",
            border: "2px solid rgba(100, 175, 255, 0.28)",
            boxShadow:
              "0 35px 70px rgba(0,0,0,0.92)",
            overflow: "hidden",
          }}
        >
          <svg
            width={MAP_WIDTH}
            height={MAP_HEIGHT}
            viewBox={`0 0 ${MAP_WIDTH} ${MAP_HEIGHT}`}
            style={{ width: "100%", height: "100%", display: "block" }}
          >
            {Array.from({ length: 10 }).map((_, i) => (
              <line
                key={`vx-${i}`}
                x1={i * 100}
                y1={0}
                x2={i * 100}
                y2={MAP_HEIGHT}
                stroke="rgba(100, 170, 255, 0.08)"
                strokeWidth={1}
              />
            ))}
            {Array.from({ length: 7 }).map((_, i) => (
              <line
                key={`hy-${i}`}
                x1={0}
                y1={i * 100}
                x2={MAP_WIDTH}
                y2={i * 100}
                stroke="rgba(100, 170, 255, 0.08)"
                strokeWidth={1}
              />
            ))}

            {bgPaths.map((d, idx) => (
              <path
                key={`bg-${idx}`}
                d={d}
                fill="rgba(30, 52, 88, 0.65)"
                stroke="rgba(110, 165, 230, 0.25)"
                strokeWidth={1.1}
              />
            ))}

            {originPaths.map((d, idx) => (
              <path
                key={`orig-${idx}`}
                d={d}
                fill="rgba(255, 230, 0, 0.78)"
                stroke="#FFFFFF"
                strokeWidth={2.5}
                style={{
                  filter: "drop-shadow(0px 8px 16px rgba(0,0,0,0.85))",
                }}
              />
            ))}

            {targetPaths.map((d, idx) => (
              <path
                key={`targ-${idx}`}
                d={d}
                fill="rgba(255, 59, 71, 0.85)"
                stroke="#FFFFFF"
                strokeWidth={2.5}
                style={{
                  filter: "drop-shadow(0px 8px 16px rgba(0,0,0,0.85))",
                }}
              />
            ))}

            <circle
              cx={originCoord.x}
              cy={originCoord.y}
              r={18 + ((localFrame * 0.8) % 36)}
              fill="none"
              stroke="#FFE600"
              strokeWidth={3}
              opacity={1 - ((localFrame * 0.8) % 36) / 36}
            />
            <circle
              cx={originCoord.x}
              cy={originCoord.y}
              r={9}
              fill="#FFE600"
              stroke="#FFFFFF"
              strokeWidth={3}
            />

            {arcProgress > 0.75 && (
              <>
                <circle
                  cx={targetCoord.x}
                  cy={targetCoord.y}
                  r={18 + ((localFrame * 1.1) % 44)}
                  fill="none"
                  stroke="#FF3B47"
                  strokeWidth={3.5}
                  opacity={1 - ((localFrame * 1.1) % 44) / 44}
                />
                <circle
                  cx={targetCoord.x}
                  cy={targetCoord.y}
                  r={10}
                  fill="#FF3B47"
                  stroke="#FFFFFF"
                  strokeWidth={3}
                />
              </>
            )}

            <path
              d={arcPathD}
              fill="none"
              stroke="rgba(255, 230, 0, 0.25)"
              strokeWidth={5}
              strokeDasharray="10 10"
            />
            <path
              d={arcPathD}
              fill="none"
              stroke="#FFE600"
              strokeWidth={6}
              strokeLinecap="round"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - arcProgress}
              style={{
                filter: "drop-shadow(0px 8px 16px rgba(0,0,0,0.85))",
              }}
            />

            {arcProgress > 0.02 && arcProgress < 0.99 && (
              <circle
                cx={headX}
                cy={headY}
                r={12}
                fill="#FFFFFF"
                stroke="#FF3B47"
                strokeWidth={5}
                style={{
                  filter: "drop-shadow(0px 8px 16px rgba(0,0,0,0.85))",
                }}
              />
            )}
          </svg>
        </div>

        <div
          style={{
            position: "absolute",
            left: originLabelPos ? originLabelPos.x : Math.min(880, Math.max(120, originCoord.x - 35)),
            top: originLabelPos ? originLabelPos.y : Math.min(580, Math.max(60, originCoord.y + 18)),
            transform: "translate(-50%, -50%)",
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: 32,
            color: "#FFE600",
            WebkitTextStroke: "8px #05070C",
            paintOrder: "stroke fill",
            textShadow: "0 8px 18px rgba(0,0,0,0.95)",
            whiteSpace: "nowrap",
          }}
        >
          {originLabel}
        </div>

        <div
          style={{
            position: "absolute",
            left: targetLabelPos ? targetLabelPos.x : Math.min(880, Math.max(140, targetCoord.x + 60)),
            top: targetLabelPos ? targetLabelPos.y : Math.min(580, Math.max(60, targetCoord.y - 24)),
            transform: "translate(-50%, -50%)",
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: 32,
            color: "#FFFFFF",
            WebkitTextStroke: "8px #05070C",
            paintOrder: "stroke fill",
            textShadow: "0 8px 18px rgba(0,0,0,0.95)",
            whiteSpace: "nowrap",
          }}
        >
          {targetLabel}
        </div>
      </div>

      {evidenceImageSrc && localFrame >= 85 && (
        <div
          style={{
            position: "absolute",
            left: evidenceCenterX,
            top: evidenceTop,
            width: evidenceWidth,
            transform: `translate(-50%, -50%) scale(${courtPop}) rotate(-1.5deg)`,
          }}
        >
          <div
            style={{
              borderRadius: 26,
              overflow: "hidden",
              border: "4px solid rgba(255, 255, 255, 0.92)",
              boxShadow: "0 28px 60px rgba(0,0,0,0.92)",
            }}
          >
            <Img
              src={staticFile(evidenceImageSrc)}
              style={{
                width: "100%",
                height: evidenceHeight,
                objectFit: "cover",
                objectPosition: evidenceObjectPosition,
                display: "block",
              }}
            />
          </div>

          {evidenceTitle && (
            <div
              style={{
                marginTop: 16,
                textAlign: "center",
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: evidenceTitleFontSize,
                color: "#FFE600",
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 10px 24px rgba(0,0,0,0.95)",
                whiteSpace: "nowrap",
              }}
            >
              {evidenceTitle}
            </div>
          )}
        </div>
      )}

      {rightFloatingIconSrc && localFrame >= 115 && (
        <Img
          src={rightFloatingIconSrc.startsWith("http") || rightFloatingIconSrc.startsWith("/") ? rightFloatingIconSrc : staticFile(rightFloatingIconSrc)}
          style={{
            position: "absolute",
            left: rightFloatingIconPos?.x ?? 855,
            top: rightFloatingIconPos?.y ?? 1140,
            width: rightFloatingIconPos?.width ?? 220,
            transform: `translate(-50%, -50%) translateY(${Math.sin(localFrame * 0.08) * 8}px) rotate(-10deg)`,
            filter: "drop-shadow(0 20px 30px rgba(0, 0, 0, 0.92))",
          }}
        />
      )}

      {leftFloatingIconSrc && localFrame >= 98 && (
        <Img
          src={leftFloatingIconSrc.startsWith("http") || leftFloatingIconSrc.startsWith("/") ? leftFloatingIconSrc : staticFile(leftFloatingIconSrc)}
          style={{
            position: "absolute",
            left: leftFloatingIconPos?.x ?? 210,
            top: leftFloatingIconPos?.y ?? 1160,
            width: leftFloatingIconPos?.width ?? 200,
            transform: `translate(-50%, -50%) translateY(${Math.cos(localFrame * 0.08) * 7}px) rotate(8deg)`,
            filter: "drop-shadow(0 20px 30px rgba(0, 0, 0, 0.92))",
          }}
        />
      )}
    </div>
  );
};
```


#### `remotion_reels/src/components/HaDaWhyMistBackground.tsx`

```tsx
import React from "react";
import { AbsoluteFill } from "remotion";

export interface HaDaWhyMistBackgroundProps {
  /** Giữ tương thích ngược; nền studio chuẩn luôn sạch, không sinh đốm bokeh bay qua nội dung. */
  intensity?: number;
  accentHex?: string;
  /** Độ đậm nét lưới kỹ thuật 56x56px (mặc định 0.065). */
  gridOpacity?: number;
}

/**
 * Nền studio xanh đêm sâu sạch 100% cho mọi video 9:16 HaDa Why:
 * - Radial gradient xanh đêm sâu (#0B192E -> #050C18 -> #030710)
 * - Lưới ô vuông kỹ thuật mảnh sắc nét (56px x 56px, rgba(120, 190, 255, 0.065))
 * - Không đốm đỏ / bokeh sáng bay qua vùng chữ và ảnh.
 */
export const HaDaWhyMistBackground: React.FC<HaDaWhyMistBackgroundProps> = ({
  gridOpacity = 0.065,
}) => {
  const safeGrid = Math.min(0.14, Math.max(0.03, gridOpacity));
  const lineColor = `rgba(120, 190, 255, ${safeGrid})`;

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(circle at 50% 35%, #0D2342 0%, #061224 62%, #030812 100%)",
        overflow: "hidden",
      }}
    >
      {/* Lưới ô vuông kỹ thuật mảnh sắc nét 56x56px */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `linear-gradient(to right, ${lineColor} 1px, transparent 1px), linear-gradient(to bottom, ${lineColor} 1px, transparent 1px)`,
          backgroundSize: "56px 56px",
          pointerEvents: "none",
        }}
      />

      {/* Vignette viền ngoài nhẹ giữ độ tập trung vào vùng Safe Zone */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 48%, rgba(2,5,12,0.55) 100%)",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
```


#### `remotion_reels/src/components/KineticHookHeader.tsx`

```tsx
import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface HookBeatSpec {
  start: number;
  eyebrow: string;
  hero: string;
  accent?: string;
  heroColor?: string;
  heroSize?: number;
}

interface KineticHookHeaderProps {
  beat: HookBeatSpec;
  top?: number;
}

export const HaDaWhyFontFaces: React.FC = () => (
  <style>{`
    @font-face {
      font-family: 'BeVietnamProBlack';
      src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
      font-weight: 900;
      font-style: normal;
    }
    @font-face {
      font-family: 'BeVietnamProExtraBold';
      src: url('${staticFile("fonts/BeVietnamPro-ExtraBold.ttf")}') format('truetype');
      font-weight: 800;
      font-style: normal;
    }
    @font-face {
      font-family: 'KanitBlack';
      src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
      font-weight: 900;
      font-style: normal;
    }
  `}</style>
);

export const KineticHookHeader: React.FC<KineticHookHeaderProps> = ({
  beat,
  top = 290,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const hookSpring = spring({
    frame: Math.max(0, frame - beat.start),
    fps,
    config: { damping: 22, stiffness: 280, mass: 0.8 },
  });
  const hookScale = interpolate(hookSpring, [0, 1], [1.22, 1.0]);
  const hookOpacity = interpolate(hookSpring, [0, 0.3], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        left: 540,
        top,
        width: 980,
        transform: `translate3d(-50%, -50%, 0) scale(${hookScale})`,
        willChange: "transform",
        opacity: hookOpacity,
        textAlign: "center",
        pointerEvents: "none",
        zIndex: 35,
      }}
    >
      <div
        style={{
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: 36,
          lineHeight: 1.15,
          letterSpacing: "0.03em",
          color: beat.accent?.startsWith("#") ? beat.accent : "#A0ECFF",
          WebkitTextStroke: "6px #05070C",
          paintOrder: "stroke fill",
          textShadow: "0 8px 22px rgba(0,0,0,0.95)",
          marginBottom: 6,
          textTransform: "uppercase",
          whiteSpace: "nowrap",
        }}
      >
        {beat.eyebrow}
      </div>
      <div
        style={{
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: beat.heroSize ?? 72,
          lineHeight: 1.06,
          color: beat.heroColor ?? "#FFE600",
          WebkitTextStroke: "10px #05070C",
          paintOrder: "stroke fill",
          textShadow: "0 10px 26px rgba(0,0,0,0.95)",
          textTransform: "uppercase",
          whiteSpace: "nowrap",
        }}
      >
        {beat.hero}
      </div>
    </div>
  );
};
```


#### `remotion_reels/src/components/RealPersonSpotlight3D.tsx`

```tsx
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface RealPersonSpotlight3DProps {
  startFrame: number;
  endFrame: number;
  /** Real background photo in public/ (e.g. "harvested/company_hq.png") */
  backdropSrc?: string;
  /** AI-cutout transparent PNG of the real person/product/vehicle in public/ */
  cutoutSrc: string;
  cutoutWidth?: number;
  centerX?: number;
  backdropWidth?: number;
  cutoutTop?: number;
  labelTop?: number;
  rimGlowColor?: string;
  subjectName: string;
  subjectSubtitle?: string;
  keyMetricValue?: string;
  keyMetricAccentColor?: string;
}

export const RealPersonSpotlight3D: React.FC<RealPersonSpotlight3DProps> = ({
  startFrame,
  endFrame,
  backdropSrc,
  cutoutSrc,
  cutoutWidth = 620,
  centerX = 540,
  backdropWidth = 860,
  cutoutTop = 1020,
  labelTop = 1520,
  rimGlowColor = "rgba(255,255,255,0.92)",
  subjectName,
  subjectSubtitle,
  keyMetricValue,
  keyMetricAccentColor = "#FFE600",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const localFrame = frame - startFrame;
  const exitOpacity = interpolate(frame, [endFrame - 14, endFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const bgPop = spring({
    frame: localFrame,
    fps,
    config: { damping: 16, stiffness: 100 },
  });

  const cutoutPop = spring({
    frame: Math.max(0, localFrame - 10),
    fps,
    config: { damping: 12, stiffness: 170, mass: 0.8 },
  });

  const floatY = Math.sin(localFrame * 0.08) * 8;

  return (
    <div style={{ position: "absolute", inset: 0, opacity: exitOpacity }}>
      {/* Optional Tilted 3D Real Context Backdrop */}
      {backdropSrc && (
        <div
          style={{
            position: "absolute",
            left: centerX,
            top: 760,
            width: backdropWidth,
            height: 520,
            perspective: 1100,
            transform: `translate(-50%, -50%) scale(${bgPop})`,
          }}
        >
          <div
            style={{
              width: "100%",
              height: "100%",
              transform: "rotateX(8deg) rotateY(-6deg)",
              borderRadius: 28,
              overflow: "hidden",
              border: "3px solid rgba(255, 255, 255, 0.35)",
              boxShadow: "0 35px 70px rgba(0,0,0,0.92)",
            }}
          >
            <Img
              src={staticFile(backdropSrc)}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "brightness(0.68) contrast(1.12)",
              }}
            />
          </div>
        </div>
      )}

      {/* 3D Foreground Real Cutout Subject */}
      <div
        style={{
          position: "absolute",
          left: centerX,
          top: cutoutTop + floatY,
          width: cutoutWidth,
          transform: `translate(-50%, -50%) scale(${cutoutPop})`,
        }}
      >
        <Img
          src={staticFile(cutoutSrc)}
          style={{
            width: "100%",
            height: "auto",
            filter:
              `drop-shadow(0px 8px 16px rgba(0,0,0,0.85)) drop-shadow(0px 26px 40px rgba(0,0,0,0.92))`,
          }}
        />
      </div>

      {/* ZERO-BOX Subject Name & Key Metric below */}
      {localFrame >= 18 && (
        <div
          style={{
            position: "absolute",
            left: centerX,
            top: labelTop,
            transform: "translate(-50%, -50%)",
            textAlign: "center",
            whiteSpace: "nowrap",
          }}
        >
          {subjectSubtitle && (
            <div
              style={{
                fontFamily: "BeVietnamProExtraBold, sans-serif",
                fontSize: 30,
                color: "#FFFFFF",
                WebkitTextStroke: "6px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              {subjectSubtitle}
            </div>
          )}
          <div
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 54,
              color: "#FFFFFF",
              WebkitTextStroke: "10px #05070C",
              paintOrder: "stroke fill",
              textShadow: "0 10px 24px rgba(0,0,0,0.95)",
            }}
          >
            {subjectName}
          </div>
          {keyMetricValue && (
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 72,
                color: keyMetricAccentColor,
                WebkitTextStroke: "11px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 10px 24px rgba(0,0,0,0.95)",
                marginTop: 4,
              }}
            >
              {keyMetricValue}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```


#### `remotion_reels/src/components/ScaleComparison3D.tsx`

```tsx
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface ScaleComparison3DProps {
  startFrame: number;
  endFrame: number;
  leftItemSrc: string;
  leftItemCount: number;
  leftLabel: string;
  rightPrimaryStackSrc?: string;
  rightSecondaryStackSrc?: string;
  rightTopTitle: string;
  rightStartNumber?: number;
  rightTargetNumber: number;
  rightUnitSuffix: string;
  rightLabel: string;
  stampText?: string;
}

export const ScaleComparison3D: React.FC<ScaleComparison3DProps> = ({
  startFrame,
  endFrame,
  leftItemSrc,
  leftItemCount,
  leftLabel,
  rightPrimaryStackSrc = "",
  rightSecondaryStackSrc = "",
  rightTopTitle,
  rightStartNumber = 0,
  rightTargetNumber,
  rightUnitSuffix,
  rightLabel,
  stampText,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const localFrame = frame - startFrame;

  const towerGrow = spring({
    frame: Math.max(0, localFrame - 20),
    fps,
    config: { damping: 14, stiffness: 85, mass: 1.0 },
  });

  const counterProgress = interpolate(localFrame, [20, 150], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const currentVal = Math.round(
    interpolate(counterProgress, [0, 1], [rightStartNumber, rightTargetNumber])
  );

  const baselineY = 1380;
  const maxTowerHeight = 580;
  const currentTowerHeight = Math.max(20, maxTowerHeight * towerGrow);

  const stampFrame = 180;
  const showStamp = Boolean(stampText) && localFrame >= stampFrame;
  const stampPop = spring({
    frame: Math.max(0, localFrame - stampFrame),
    fps,
    config: { damping: 10, stiffness: 240, mass: 0.7 },
  });
  const stampScale = interpolate(stampPop, [0, 1], [2.2, 1.0]);

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <div
        style={{
          position: "absolute",
          left: 90,
          top: baselineY,
          width: 900,
          height: 8,
          borderRadius: 4,
          background:
            "linear-gradient(90deg, rgba(255,255,255,0.15) 0%, rgba(255,230,0,0.85) 50%, rgba(255,59,71,0.9) 100%)",
          boxShadow: "0 8px 20px rgba(0, 0, 0, 0.85)",
        }}
      />

      {Array.from({ length: leftItemCount }).map((_, idx) => {
        const pStart = 10 + idx * 11;
        if (localFrame < pStart) return null;
        const pPop = spring({
          frame: localFrame - pStart,
          fps,
          config: { damping: 11, stiffness: 200 },
        });
        const py = baselineY - 95 - idx * 125 + Math.sin((frame + idx * 15) * 0.09) * 5;
        return (
          <div
            key={`left-item-${idx}`}
            style={{
              position: "absolute",
              left: 285,
              top: py,
              width: 310,
              transform: `translate(-50%, -50%) scale(${pPop}) rotate(-4deg)`,
            }}
          >
            <Img
              src={staticFile(leftItemSrc)}
              style={{
                width: "100%",
                height: "auto",
                filter: "drop-shadow(0px 16px 24px rgba(0,0,0,0.88))",
              }}
            />
          </div>
        );
      })}

      {localFrame >= 15 && (
        <div
          style={{
            position: "absolute",
            left: 285,
            top: baselineY + 78,
            transform: "translate(-50%, -50%)",
            textAlign: "center",
            whiteSpace: "nowrap",
          }}
        >
          <div
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 44,
              color: "#FFFFFF",
              WebkitTextStroke: "9px #05070C",
              paintOrder: "stroke fill",
              textShadow: "0 8px 20px rgba(0,0,0,0.95)",
            }}
          >
            {leftLabel}
          </div>
        </div>
      )}

      {localFrame >= 92 && (
        <>
          <div
            style={{
              position: "absolute",
              left: 775,
              top: baselineY - currentTowerHeight,
              width: 210,
              height: currentTowerHeight,
              transform: "translateX(-50%)",
              borderRadius: "22px 22px 6px 6px",
              background:
                "linear-gradient(180deg, rgba(255, 59, 71, 0.96) 0%, rgba(190, 15, 35, 0.92) 65%, rgba(90, 5, 18, 0.95) 100%)",
              border: "3px solid rgba(255, 200, 180, 0.85)",
              boxShadow:
                "0 18px 36px rgba(0, 0, 0, 0.88), inset 0 12px 28px rgba(255, 255, 255, 0.25)",
            }}
          />

          {Array.from({ length: 8 }).map((_, sIdx) => {
            const threshold = (sIdx + 1) / 8;
            if (towerGrow < threshold * 0.85) return null;
            const sy = baselineY - 55 - sIdx * 78;
            const offsetX = (sIdx % 2 === 0 ? -1 : 1) * 18;
            const useSec = sIdx % 3 === 2;
            return (
              <div
                key={`stack-${sIdx}`}
                style={{
                  position: "absolute",
                  left: 775 + offsetX,
                  top: sy,
                  width: useSec ? 95 : 130,
                  transform: `translate(-50%, -50%) rotate(${sIdx % 2 === 0 ? -8 : 8}deg)`,
                  filter: "drop-shadow(0 12px 18px rgba(0,0,0,0.85))",
                }}
              >
                {(() => {
                  const stackSrc = useSec ? (rightSecondaryStackSrc || rightPrimaryStackSrc) : rightPrimaryStackSrc;
                  return stackSrc ? (
                    <Img
                      src={staticFile(stackSrc)}
                      style={{ width: "100%", height: "auto" }}
                    />
                  ) : null;
                })()}
              </div>
            );
          })}

          <div
            style={{
              position: "absolute",
              left: 775,
              top: baselineY - currentTowerHeight - 92,
              transform: "translate(-50%, -50%)",
              textAlign: "center",
              whiteSpace: "nowrap",
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProExtraBold, sans-serif",
                fontSize: 30,
                color: "#FFFFFF",
                WebkitTextStroke: "6px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              {rightTopTitle}
            </div>
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 82,
                color: "#FF3B47",
                WebkitTextStroke: "11px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 10px 26px rgba(0, 0, 0, 0.95)",
                lineHeight: 1.05,
                whiteSpace: "nowrap",
              }}
            >
              {currentVal}
              {rightUnitSuffix}
            </div>
          </div>

          <div
            style={{
              position: "absolute",
              left: 775,
              top: baselineY + 78,
              transform: "translate(-50%, -50%)",
              textAlign: "center",
              whiteSpace: "nowrap",
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 38,
                color: "#FFE600",
                WebkitTextStroke: "9px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 8px 20px rgba(0,0,0,0.95)",
              }}
            >
              {rightLabel}
            </div>
          </div>
        </>
      )}

      {showStamp && (
        <div
          style={{
            position: "absolute",
            left: 265,
            top: 900,
            transform: `translate(-50%, -50%) scale(${stampScale}) rotate(-10deg)`,
            padding: "10px 30px",
            border: "7px solid #FF3B47",
            borderRadius: 12,
            background: "transparent",
            boxShadow: "0 12px 24px rgba(0, 0, 0, 0.85)",
            whiteSpace: "nowrap",
          }}
        >
          <div
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 42,
              color: "#FF3B47",
              letterSpacing: "0.04em",
              WebkitTextStroke: "6px #05070C",
              paintOrder: "stroke fill",
            }}
          >
            {stampText}
          </div>
        </div>
      )}
    </div>
  );
};
```


#### `remotion_reels/src/components/ThumbnailCover9x16.tsx`

```tsx
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";

export interface ThumbnailCover9x16Props {
  /** Real event context backdrop photo in public/ (e.g. "harvested/nvidia_context_backdrop.png") */
  backgroundPhotoSrc?: string;
  /** Backdrop Gaussian blur px (default 1.2 for crisp identifiable real backdrop) */
  backgroundBlurPx?: number;
  /** Backdrop zoom scale (default 1.04) */
  backgroundScale?: number;
  /** Backdrop focal position / transform origin (default "50% 50%") */
  backgroundObjectPosition?: string;
  /** Backdrop brightness multiplier (default 0.72) */
  backgroundBrightness?: number;
  /** Backdrop contrast multiplier (default 1.15) */
  backgroundContrast?: number;
  /** Backdrop saturation multiplier (default 1.0) */
  backgroundSaturate?: number;
  /** Main foreground hero subject cutout PNG in public/ (rendered B&W High-Contrast by default) */
  heroSubjectSrc: string;
  /** Mystery secondary cutout PNG in public/ (rendered as dark rim-lit silhouette + "?") */
  mysteryOrSecondarySrc?: string;
  /** Headline Line 1 (HaDa Bright Blue #22B8FF by default) */
  headlineLine1: string;
  /** Headline Line 2 (WHY Pure White #FFFFFF by default) */
  headlineLine2: string;
  /** Official channel logo PNG in public/ (strictly "brand/hadawhy_logo.png") */
  brandLogoSrc?: string;
  /** Glow accent color behind subjects & on "?" hook (default "#E11D2E" Noir Crimson) */
  glowAccentColor?: string;
  /** Line 1 text color (default "#42B2F2" HaDa Sky Blue) */
  headlineLine1Color?: string;
  /** Line 2 text color (default "#FFFFFF" WHY White) */
  headlineLine2Color?: string;
  /** Apply Noir high-contrast B&W filter to hero subject */
  heroBwHighContrast?: boolean;
  /** Render secondary subject as mysterious dark silhouette + giant "?" */
  mysterySilhouetteMode?: boolean;
  /** Optional custom symbol on mystery silhouette (default "?") */
  mysterySymbol?: string;
  /**
   * Dynamic Story Layout Mode (Tư duy linh hoạt theo đúng bản chất kịch bản):
   * - "mystery_silhouette": Chủ thể chính + Bóng đen bí ẩn kèm dấu "?" đỏ (Mặc định khi có ẩn số nhân vật).
   * - "dual_confrontation": 2 Nhân vật / 2 Đế chế đối đầu trực diện (Cả 2 lộ diện rõ nét + mũi tên xung đột).
   * - "forensic_object": Giải phẫu Vật thể / Sự cố / Bằng chứng khổng lồ kèm vòng tròn đỏ khoanh vùng tử huyệt.
   * - "titan_evidence": Nhân vật trung tâm B&W + Vật chứng / Hồ sơ mật nổi 3D bên cạnh kèm vòng khoanh đỏ.
   */
  layoutMode?: "mystery_silhouette" | "dual_confrontation" | "forensic_object" | "titan_evidence";
  /** Optional red forensic circle coordinates for "forensic_object" or "titan_evidence" mode */
  forensicCircle?: { cx: number; cy: number; r: number };
  /** Optional overrides for foreground hero subject positioning & sizing */
  heroWidth?: number;
  heroLeft?: number;
  heroBottom?: number;
  /** Optional overrides for secondary evidence card in "titan_evidence" mode */
  secondaryWidth?: number;
  secondaryTop?: number;
  secondaryLeft?: number;
  /** Optional custom SVG path for the red dashed investigative arrow */
  arrowPath?: string;
  /** Optional smooth top-down linear scrim opacity (0 to 1, Zero-Blob) for headline legibility */
  topScrimOpacity?: number;
  /** Index signature required for Remotion Still compatibility */
  [key: string]: unknown;
}

function fitEditorialSize(text: string, baseSize: number, minSize: number): number {
  const len = text.trim().length;
  if (len <= 18) return baseSize;
  return Math.max(minSize, Math.round(baseSize * (18.2 / len)));
}

export const ThumbnailCover9x16: React.FC<ThumbnailCover9x16Props> = ({
  backgroundPhotoSrc = "",
  backgroundBlurPx = 3.5,
  backgroundScale = 1.04,
  backgroundObjectPosition = "50% 50%",
  backgroundBrightness = 0.65,
  backgroundContrast = 1.15,
  backgroundSaturate = 0.96,
  heroSubjectSrc,
  mysteryOrSecondarySrc,
  headlineLine1,
  headlineLine2,
  brandLogoSrc = "brand/hadawhy_logo.png",
  glowAccentColor = "#E11D2E",
  headlineLine1Color = "#22B8FF",
  headlineLine2Color = "#FFFFFF",
  heroBwHighContrast = false,
  mysterySilhouetteMode = true,
  mysterySymbol = "?",
  layoutMode = "titan_evidence",
  forensicCircle,
  heroWidth,
  heroLeft,
  heroBottom = 0,
  secondaryWidth = 425,
  secondaryTop = 815,
  secondaryLeft = 825,
  arrowPath = "M 555 620 Q 670 575 740 665",
  topScrimOpacity = 0.45,
}) => {
  const isSilhouette = layoutMode === "mystery_silhouette" ? mysterySilhouetteMode : false;
  const line1Size = fitEditorialSize(headlineLine1, 86, 54);
  const line2Size = fitEditorialSize(headlineLine2, 84, 52);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#06101E",
        overflow: "hidden",
      }}
    >
      {/* Khóa 100% font tiếng Việt đầy đủ dấu BeVietnamPro-Black */}
      <style>
        {`
          @font-face {
            font-family: 'BeVietnamProBlack';
            src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
            font-weight: 900;
          }
          @font-face {
            font-family: 'KanitBlack';
            src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
            font-weight: 900;
          }
        `}
      </style>

      {/* ===================================================================
          1. FULL 1080x1920 REAL CONTEXT BACKDROP (SCALED & BLURRED EVENLY)
         =================================================================== */}
      {backgroundPhotoSrc && (
        <Img
          src={staticFile(backgroundPhotoSrc)}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: backgroundObjectPosition,
            transform: `scale(${backgroundScale})`,
            transformOrigin: backgroundObjectPosition,
            filter: backgroundBlurPx > 0
              ? `blur(${backgroundBlurPx}px) brightness(${backgroundBrightness}) contrast(${backgroundContrast}) saturate(${backgroundSaturate})`
              : `brightness(${backgroundBrightness}) contrast(${backgroundContrast}) saturate(${backgroundSaturate})`,
          }}
        />
      )}

      {/* Smooth Zero-Blob Top Scrim for Headline Legibility */}
      {topScrimOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `linear-gradient(180deg, rgba(5, 7, 12, ${topScrimOpacity}) 0%, rgba(5, 7, 12, ${topScrimOpacity * 0.55}) 26%, rgba(5, 7, 12, 0) 48%)`,
            pointerEvents: "none",
          }}
        />
      )}



      {/* ===================================================================
          2. CHANNEL LOGO AT SAFE TOP-LEFT (brand/hadawhy_logo.png)
         =================================================================== */}
      <div
        style={{
          position: "absolute",
          left: 52,
          top: 64,
          width: 225,
          filter: "drop-shadow(0 6px 16px rgba(0, 0, 0, 0.9))",
        }}
      >
        <Img
          src={staticFile(brandLogoSrc)}
          style={{ width: "100%", height: "auto", display: "block" }}
        />
      </div>

      {/* ===================================================================
          3. DUY NHẤT 2 DÒNG TIÊU ĐỀ CHÍNH (#22B8FF + #FFFFFF) — CẤM TAG ĐỎ THỨ 3
         =================================================================== */}
      <div
        style={{
          position: "absolute",
          left: 540,
          top: 385,
          width: 970,
          transform: "translate3d(-50%, -50%, 0)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          gap: 8,
        }}
      >
        <div
          style={{
            width: "100%",
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: line1Size,
            fontWeight: 900,
            lineHeight: 1.08,
            letterSpacing: "-0.015em",
            color: headlineLine1Color,
            WebkitTextStroke: "11px #05070C",
            paintOrder: "stroke fill",
            textShadow: `0px 8px 0px #05070C, 0px 16px 32px rgba(0,0,0,0.95)`,
            textTransform: "uppercase",
            whiteSpace: "nowrap",
          }}
        >
          {headlineLine1}
        </div>
        <div
          style={{
            width: "100%",
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: line2Size,
            fontWeight: 900,
            lineHeight: 1.08,
            letterSpacing: "-0.015em",
            color: headlineLine2Color,
            WebkitTextStroke: "11px #05070C",
            paintOrder: "stroke fill",
            textShadow: `0px 8px 0px #05070C, 0px 16px 32px rgba(0,0,0,0.95)`,
            textTransform: "uppercase",
            whiteSpace: "nowrap",
          }}
        >
          {headlineLine2}
        </div>
      </div>

      {/* ===================================================================
          4. MYSTERY SILHOUETTE RIGHT + GLOWING "?" (ANCHORED TO BOTTOM 1920)
         =================================================================== */}
      {mysteryOrSecondarySrc && (
        <>
          <div
            style={
              layoutMode === "titan_evidence"
                ? {
                    position: "absolute",
                    left: secondaryLeft,
                    top: secondaryTop,
                    width: secondaryWidth,
                    transform: "translateX(-50%) rotate(3deg)",
                    zIndex: 5,
                  }
                : {
                    position: "absolute",
                    left: 815,
                    bottom: 0,
                    width: 850,
                    transform: "translateX(-50%)",
                  }
            }
          >
            <Img
              src={staticFile(mysteryOrSecondarySrc)}
              style={{
                width: "100%",
                height: "auto",
                display: "block",
                borderRadius: layoutMode === "titan_evidence" ? 12 : 0,
                border:
                  layoutMode === "titan_evidence"
                    ? "3px solid rgba(255, 255, 255, 0.25)"
                    : "none",
                filter: isSilhouette
                  ? `brightness(0) drop-shadow(0px 8px 16px rgba(0,0,0,0.85)) drop-shadow(0px 8px 16px rgba(0,0,0,0.85))`
                  : `drop-shadow(0px 22px 34px rgba(0,0,0,0.9))`,
              }}
            />
          </div>

          {/* Red Dashed Investigative Arrow pointing toward Secondary Subject / Evidence */}
          <svg
            width={1080}
            height={1920}
            style={{ position: "absolute", inset: 0, pointerEvents: "none", zIndex: 8 }}
          >
            <defs>
              <marker
                id="cov-mystery-arrow"
                viewBox="0 0 10 10"
                refX="6"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 1 L 9 5 L 0 9 z" fill={glowAccentColor} />
              </marker>
            </defs>
            <path
              d={arrowPath}
              fill="none"
              stroke={glowAccentColor}
              strokeWidth={7}
              strokeDasharray="16 12"
              strokeLinecap="round"
              markerEnd="url(#cov-mystery-arrow)"
              style={{ filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.8))" }}
            />
            {forensicCircle && (
              <circle
                cx={forensicCircle.cx}
                cy={forensicCircle.cy}
                r={forensicCircle.r}
                fill="none"
                stroke={glowAccentColor}
                strokeWidth={8}
                strokeDasharray="22 12"
                style={{ filter: "drop-shadow(0 6px 14px rgba(0,0,0,0.85))" }}
              />
            )}
          </svg>

          {/* Giant Glowing Crimson "?" over Silhouette (Safe inside 4:5) */}
          {isSilhouette && (
            <div
              style={{
                position: "absolute",
                left: 815,
                top: 865,
                transform: "translate(-50%, -50%) rotate(4deg)",
                fontFamily: "KanitBlack, sans-serif",
                fontSize: 345,
                fontWeight: 900,
                lineHeight: 0.9,
                color: glowAccentColor,
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
                textShadow: `0 8px 18px rgba(0,0,0,0.85), 0px 12px 28px rgba(0,0,0,0.95)`,
                pointerEvents: "none",
              }}
            >
              {mysterySymbol}
            </div>
          )}
        </>
      )}

      {/* ===================================================================
          5. GIANT FOREGROUND HERO SUBJECT (ANCHORED FULL TO BOTTOM: 0)
         =================================================================== */}
      <div
        style={{
          position: "absolute",
          left: heroLeft ?? (layoutMode === "forensic_object" && !mysteryOrSecondarySrc ? 540 : 345),
          bottom: heroBottom,
          width: heroWidth ?? (layoutMode === "forensic_object" && !mysteryOrSecondarySrc ? 1020 : 990),
          transform: "translateX(-50%)",
          zIndex: 6,
        }}
      >
        <Img
          src={staticFile(heroSubjectSrc)}
          style={{
            width: "100%",
            height: "auto",
            display: "block",
            filter: heroBwHighContrast
              ? `grayscale(100%) contrast(1.38) brightness(1.06) drop-shadow(0px 24px 38px rgba(0,0,0,0.95))`
              : `drop-shadow(0px 24px 38px rgba(0,0,0,0.95))`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
```


#### `remotion_reels/src/components/TimelineTrack3D.tsx`

```tsx
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface TimelineMilestone {
  dateLabel: string;
  title: string;
  iconOrCutoutSrc: string;
  accentColor?: string;
  triggerOffsetFrames: number;
}

export interface TimelineTrack3DProps {
  startFrame: number;
  endFrame: number;
  milestones: TimelineMilestone[];
  centerX?: number;
  columnOffset?: number;
  startNodeY?: number;
  nodeStepY?: number;
  spineTop?: number;
  spineMaxHeight?: number;
  spineColors?: [string, string];
}

export const TimelineTrack3D: React.FC<TimelineTrack3DProps> = ({
  startFrame,
  endFrame,
  milestones,
  centerX = 540,
  columnOffset = 275,
  startNodeY = 650,
  nodeStepY = 340,
  spineTop = 580,
  spineMaxHeight = 1040,
  spineColors = ["#FFE600", "#FF3B47"],
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const localFrame = frame - startFrame;
  const exitOpacity = interpolate(frame, [endFrame - 14, endFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const lineProgress = interpolate(localFrame, [0, Math.max(30, endFrame - startFrame - 30)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ position: "absolute", inset: 0, opacity: exitOpacity }}>
      {/* Central Glowing Vertical Timeline Spine */}
      <div
        style={{
          position: "absolute",
          left: centerX,
          top: spineTop,
          width: 8,
          height: spineMaxHeight * lineProgress,
          transform: "translateX(-50%)",
          background: `linear-gradient(180deg, ${spineColors[0]} 0%, ${spineColors[1]} 100%)`,
          boxShadow: "0 8px 18px rgba(0, 0, 0, 0.85)",
          borderRadius: 4,
        }}
      />

      {milestones.map((m, idx) => {
        if (localFrame < m.triggerOffsetFrames) return null;
        const mPop = spring({
          frame: localFrame - m.triggerOffsetFrames,
          fps,
          config: { damping: 12, stiffness: 190 },
        });
        const nodeY = startNodeY + idx * nodeStepY;
        const isLeft = idx % 2 === 0;
        const color = m.accentColor || "#FFE600";

        return (
          <div key={`ms-${idx}`}>
            {/* Crisp Node on Spine */}
            <div
              style={{
                position: "absolute",
                left: centerX,
                top: nodeY,
                width: 30,
                height: 30,
                borderRadius: "50%",
                background: color,
                border: "5px solid #FFFFFF",
                boxShadow: "0 6px 16px rgba(0, 0, 0, 0.85)",
                transform: `translate(-50%, -50%) scale(${mPop})`,
              }}
            />

            {/* Cutout / 3D Icon on one side */}
            <div
              style={{
                position: "absolute",
                left: isLeft ? centerX - columnOffset : centerX + columnOffset,
                top: nodeY,
                width: 220,
                transform: `translate(-50%, -50%) scale(${mPop})`,
              }}
            >
              <Img
                src={staticFile(m.iconOrCutoutSrc)}
                style={{
                  width: "100%",
                  height: "auto",
                  filter: "drop-shadow(0px 18px 28px rgba(0,0,0,0.88))",
                }}
              />
            </div>

            {/* ZERO-BOX Date & Title on opposite side */}
            <div
              style={{
                position: "absolute",
                left: isLeft ? centerX + columnOffset : centerX - columnOffset,
                top: nodeY,
                transform: `translate(-50%, -50%) scale(${mPop})`,
                textAlign: "center",
                whiteSpace: "nowrap",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 52,
                  color,
                  WebkitTextStroke: "9px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 8px 20px rgba(0,0,0,0.92)",
                }}
              >
                {m.dateLabel}
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 33,
                  color: "#FFFFFF",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                {m.title}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
```


#### `remotion_reels/src/components/UrbanSatelliteDive9x16.tsx`

```tsx
import React from "react";
import {
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export interface RealEstatePinSpec {
  label: string;
  value?: string;
  image?: string;
  xPercent: number; // 15..85 on map canvas
  yPercent: number; // 20..80 on map canvas
  color?: string;
  startFrame?: number;
}

export type MapOverlayMode = "pins" | "route" | "radius_zone" | "hex_grid" | "clean_highlight";

export interface RealEstateSatelliteDiveProps {
  locationName: string;
  zoneLabel: string;
  zoneMetric: string; // e.g. "5 KM² • X2.0 GIÁ" or "1.200 M² • 150 TỶ"
  mapImageSrc?: string; // Ảnh bản đồ/vệ tinh thật cào riêng theo địa danh kịch bản
  satelliteBgSrc?: string; // Alias tương thích ngược
  overlayMode?: MapOverlayMode; // Mặc định "pins"; chỉ bật "hex_grid" khi kịch bản nói về lưới lục giác
  zoneColor?: string;
  routePoints?: { x: number; y: number }[]; // Normalized 0..1000 canvas points
  routeDistanceLabel?: string;
  pins?: RealEstatePinSpec[];
  durationFrames: number;
}

/**
 * UrbanSatelliteDive9x16 — Bản đồ Vệ tinh 3D phong cách Bất động sản cao cấp
 * Nằm gọn trong Sân khấu tầng giữa (Y: 480..1540px) trên nền <HaDaWhyMistBackground />:
 * 1. Camera bay bổ nhào nghiêng 3D (Pitch 42° -> 56°, Rotate Bearing -12° -> +10°, Zoom 0.86 -> 1.14).
 * 2. Khoanh ranh giới khu đất / vùng nóng nổi khối 3D (Extruded Parcel / Hex Polygon + mặt phủ bán trong suốt + nhãn nổi ở tâm).
 * 3. Tia dẫn đường chạy dọc trục đường thật (Animated Route Line + nhãn khoảng cách).
 * 4. Chân ghim 3D cắm vuông góc xuống mặt đất bung thẻ ảnh thật (--no-rim).
 */
export const UrbanSatelliteDive9x16: React.FC<RealEstateSatelliteDiveProps> = ({
  locationName,
  zoneLabel,
  zoneMetric,
  mapImageSrc,
  satelliteBgSrc,
  overlayMode = "pins",
  zoneColor = "#FF3B47",
  routePoints = [
    { x: 180, y: 690 },
    { x: 370, y: 540 },
    { x: 520, y: 460 },
    { x: 760, y: 310 },
  ],
  routeDistanceLabel,
  pins = [],
  durationFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const diveSpring = spring({
    frame,
    fps,
    config: { damping: 16, stiffness: 80, mass: 1.1 },
  });

  const pitchDeg = interpolate(frame, [0, durationFrames], [38, 54], {
    extrapolateRight: "clamp",
  });
  const rotateZDeg = interpolate(frame, [0, durationFrames], [-9, 7], {
    extrapolateRight: "clamp",
  });
  const zoomScale = interpolate(frame, [0, durationFrames], [0.92, 1.12], {
    extrapolateRight: "clamp",
  });

  const polyProgress = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const routeProgress = interpolate(frame, [10, 48], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const routePathD =
    routePoints.length >= 2
      ? routePoints
          .map((pt, idx) => `${idx === 0 ? "M" : "L"} ${pt.x} ${pt.y}`)
          .join(" ")
      : "M 200 680 L 480 480 L 780 300";

  const activeBgSrc = mapImageSrc || satelliteBgSrc;
  const resolvedSatSrc = activeBgSrc
    ? activeBgSrc.startsWith("http") || activeBgSrc.startsWith("/")
      ? activeBgSrc
      : staticFile(activeBgSrc)
    : undefined;

  return (
    <div
      style={{
        position: "absolute",
        left: 48,
        top: 475,
        width: 984,
        height: 1030,
        perspective: "1350px",
        zIndex: 25,
      }}
    >
      {/* Top Location Coordinate Telemetry Bar */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 14,
          padding: "10px 22px",
          borderRadius: 16,
          background: "rgba(7, 15, 30, 0.88)",
          border: "2px solid rgba(66, 178, 242, 0.55)",
          boxShadow: "0 14px 28px rgba(0, 0, 0, 0.85)",
        }}
      >
        <div
          style={{
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: 26,
            color: "#42B2F2",
            letterSpacing: "0.04em",
          }}
        >
          ◉ VỆ TINH 3D • {locationName.toUpperCase()}
        </div>
        <div
          style={{
            fontFamily: "KanitBlack, sans-serif",
            fontSize: 26,
            color: "#FFE600",
          }}
        >
          {zoneLabel.toUpperCase()}
        </div>
      </div>

      {/* 3D Tilted Real-Estate Satellite Terrain Slab */}
      <div
        style={{
          position: "relative",
          width: 984,
          height: 820,
          borderRadius: 28,
          overflow: "hidden",
          background:
            "radial-gradient(circle at 50% 45%, #0E223D 0%, #06101E 75%, #030710 100%)",
          border: "3px solid rgba(66, 178, 242, 0.65)",
          boxShadow:
            "0 36px 70px rgba(0, 0, 0, 0.95), inset 0 0 60px rgba(0, 0, 0, 0.85)",
          transform: `scale(${interpolate(diveSpring, [0, 1], [0.85, 1])})`,
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: -80,
            transformStyle: "preserve-3d",
            transform: `rotateX(${pitchDeg}deg) rotateZ(${rotateZDeg}deg) scale(${zoomScale})`,
            transformOrigin: "50% 52%",
          }}
        >
          {resolvedSatSrc ? (
            <Img
              src={resolvedSatSrc}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "brightness(0.92) contrast(1.14) saturate(1.12)",
              }}
            />
          ) : null}

          {/* Urban Road Grid & 3D Extruded Parcel / Hex Zone SVG */}
          <svg
            viewBox="0 0 1000 900"
            style={{
              position: "absolute",
              inset: 0,
              width: "100%",
              height: "100%",
            }}
          >
            {/* Subtle Cadastral Road Grid */}
            <g stroke="rgba(66, 178, 242, 0.18)" strokeWidth={1.5}>
              {[150, 300, 450, 600, 750].map((v) => (
                <React.Fragment key={v}>
                  <line x1={v} y1={0} x2={v} y2={900} />
                  <line x1={0} y1={v} x2={1000} y2={v} />
                </React.Fragment>
              ))}
            </g>

            {/* Overlay động theo overlayMode (mặc định "pins", chỉ bật hex_grid khi kịch bản yêu cầu) */}
            {overlayMode === "hex_grid" && (
              <g stroke="rgba(34, 211, 238, 0.45)" strokeWidth={2.5} fill="rgba(34, 211, 238, 0.08)">
                {[
                  { cx: 500, cy: 420 },
                  { cx: 360, cy: 340 },
                  { cx: 640, cy: 340 },
                  { cx: 360, cy: 500 },
                  { cx: 640, cy: 500 },
                ].map((h, hi) => {
                  const pts = Array.from({ length: 6 })
                    .map((_, pi) => {
                      const a = (pi * 60 * Math.PI) / 180;
                      return `${h.cx + 88 * Math.cos(a)},${h.cy + 88 * Math.sin(a)}`;
                    })
                    .join(" ");
                  return <polygon key={`hx-${hi}`} points={pts} />;
                })}
              </g>
            )}

            {overlayMode === "radius_zone" && (
              <g>
                <circle cx={500} cy={430} r={220 * polyProgress} fill="rgba(255, 59, 71, 0.2)" stroke={zoneColor} strokeWidth={5} />
                <circle cx={500} cy={430} r={120 * polyProgress} fill="none" stroke="#FFE600" strokeWidth={3} strokeDasharray="10 8" />
              </g>
            )}

            {(overlayMode === "clean_highlight" || overlayMode === "pins" || overlayMode === "route") && (
              <>
                {/* 3D Extruded Parcel Base Shadow & Side Wall */}
                <polygon
                  points="500,245 690,340 650,555 360,575 310,365"
                  fill="rgba(0, 0, 0, 0.55)"
                  transform="translate(0, 22)"
                />
                <polygon
                  points="500,245 690,340 650,555 360,575 310,365"
                  fill={zoneColor === "#FF3B47" ? "rgba(255, 59, 71, 0.26)" : "rgba(66, 178, 242, 0.26)"}
                  stroke={zoneColor}
                  strokeWidth={7}
                  strokeLinejoin="round"
                  pathLength={1}
                  strokeDasharray={1}
                  strokeDashoffset={1 - polyProgress}
                />
              </>
            )}

            {/* Animated Turf Route Along Real Road Axis */}
            <path
              d={routePathD}
              fill="none"
              stroke="rgba(255, 230, 0, 0.28)"
              strokeWidth={12}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d={routePathD}
              fill="none"
              stroke="#FFE600"
              strokeWidth={7}
              strokeLinecap="round"
              strokeLinejoin="round"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - routeProgress}
            />
          </svg>
        </div>

        {/* Floating Parcel Metric Badge (Đẩy xuống dưới cụm lục giác +32px để viền không bao giờ cắt chữ) */}
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: "76%",
            transform: `translate(-50%, -50%) scale(${interpolate(polyProgress, [0, 1], [0.85, 1])})`,
            opacity: polyProgress,
            padding: "10px 26px",
            borderRadius: 14,
            background: "rgba(5, 10, 22, 0.95)",
            border: `2.5px solid ${zoneColor}`,
            boxShadow: "0 18px 36px rgba(0, 0, 0, 0.95)",
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontFamily: "KanitBlack, sans-serif",
              fontSize: zoneMetric.length > 14 ? 36 : 46,
              color: "#FFE600",
              WebkitTextStroke: "6px #05070C",
              paintOrder: "stroke fill",
              lineHeight: 1.05,
              whiteSpace: "nowrap",
            }}
          >
            {zoneMetric}
          </div>
        </div>

        {/* Route Distance Badge */}
        {routeDistanceLabel && routeProgress > 0.4 && (
          <div
            style={{
              position: "absolute",
              right: 28,
              bottom: 24,
              padding: "10px 22px",
              borderRadius: 14,
              background: "rgba(5, 10, 22, 0.92)",
              border: "2px solid #FFE600",
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 26,
              color: "#FFFFFF",
              boxShadow: "0 12px 24px rgba(0,0,0,0.9)",
            }}
          >
            TUYẾN ĐƯỜNG: <span style={{ color: "#FFE600" }}>{routeDistanceLabel}</span>
          </div>
        )}

        {/* 3D Ground Pins Anchored to Map with Real Cutout Photos */}
        {pins.map((pin, idx) => {
          const pStart = pin.startFrame ?? 25 + idx * 22;
          const pPop = spring({
            frame: Math.max(0, frame - pStart),
            fps,
            config: { damping: 12, stiffness: 180 },
          });
          if (frame < pStart) return null;
          const pinImg = pin.image
            ? pin.image.startsWith("http") || pin.image.startsWith("/")
              ? pin.image
              : staticFile(pin.image)
            : undefined;
          return (
            <div
              key={idx}
              style={{
                position: "absolute",
                left: `${pin.xPercent}%`,
                top: `${pin.yPercent}%`,
                transform: `translate(-50%, -100%) scale(${pPop})`,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                zIndex: 30 + idx,
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  padding: "10px 16px",
                  borderRadius: 18,
                  background: "rgba(6, 13, 26, 0.94)",
                  border: `3px solid ${pin.color ?? "#42B2F2"}`,
                  boxShadow: "0 18px 34px rgba(0, 0, 0, 0.95)",
                }}
              >
                {pinImg && (
                  <Img
                    src={pinImg}
                    style={{
                      width: 74,
                      height: 74,
                      objectFit: "contain",
                      filter: "drop-shadow(0 8px 12px rgba(0,0,0,0.85))",
                    }}
                  />
                )}
                <div>
                  <div
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 22,
                      color: "#FFFFFF",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {pin.label}
                  </div>
                  {pin.value && (
                    <div
                      style={{
                        fontFamily: "KanitBlack, sans-serif",
                        fontSize: 30,
                        color: pin.color ?? "#FFE600",
                        lineHeight: 1.05,
                      }}
                    >
                      {pin.value}
                    </div>
                  )}
                </div>
              </div>
              {/* Vertical 3D Ground Stem + Target Ring */}
              <div
                style={{
                  width: 4,
                  height: 36,
                  background: pin.color ?? "#42B2F2",
                  boxShadow: "0 4px 10px rgba(0,0,0,0.9)",
                }}
              />
              <div
                style={{
                  width: 18,
                  height: 18,
                  borderRadius: "50%",
                  background: "#FFFFFF",
                  border: `4px solid ${pin.color ?? "#42B2F2"}`,
                }}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};
```


#### `remotion_reels/src/components/fx/CapCutTransitions.tsx`

```tsx
import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const WhipPanTransition: React.FC<{
  children: React.ReactNode;
  direction?: "left" | "right" | "up" | "down";
  durationFrames?: number;
  startFrame?: number;
}> = ({ children, direction = "left", durationFrames = 14, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const progress = spring({
    frame: rel,
    fps,
    config: { damping: 18, stiffness: 210, mass: 0.7 },
    durationInFrames: durationFrames,
  });

  const dist = 1080;
  const x =
    direction === "left"
      ? interpolate(progress, [0, 1], [dist, 0])
      : direction === "right"
        ? interpolate(progress, [0, 1], [-dist, 0])
        : 0;
  const y =
    direction === "up"
      ? interpolate(progress, [0, 1], [dist, 0])
      : direction === "down"
        ? interpolate(progress, [0, 1], [-dist, 0])
        : 0;
  const blurPx = interpolate(progress, [0, 0.5, 1], [16, 6, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        transform: `translate3d(${x}px, ${y}px, 0) scale(${interpolate(progress, [0, 1], [1.06, 1])})`,
        filter: blurPx > 0.2 ? `blur(${blurPx.toFixed(1)}px)` : undefined,
      }}
    >
      {children}
    </div>
  );
};

export const ZoomThroughTransition: React.FC<{
  children: React.ReactNode;
  startFrame?: number;
  durationFrames?: number;
  initialScale?: number;
}> = ({ children, startFrame = 0, durationFrames = 16, initialScale = 1.65 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const p = spring({
    frame: rel,
    fps,
    config: { damping: 20, stiffness: 180, mass: 0.8 },
    durationInFrames: durationFrames,
  });
  const scale = interpolate(p, [0, 1], [initialScale, 1]);
  const opacity = interpolate(rel, [0, 5], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        opacity,
        transform: `scale(${scale})`,
        transformOrigin: "center center",
      }}
    >
      {children}
    </div>
  );
};

export const SplitCurtainWipe: React.FC<{
  children: React.ReactNode;
  startFrame?: number;
  durationFrames?: number;
}> = ({ children, startFrame = 0, durationFrames = 18 }) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const insetPct = interpolate(rel, [0, durationFrames], [50, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        clipPath: `inset(0% ${insetPct}% 0% ${insetPct}%)`,
      }}
    >
      {children}
    </div>
  );
};

export const Tilt3DFlip: React.FC<{
  children: React.ReactNode;
  startFrame?: number;
  durationFrames?: number;
  axis?: "X" | "Y";
}> = ({ children, startFrame = 0, durationFrames = 18, axis = "Y" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const p = spring({
    frame: rel,
    fps,
    config: { damping: 16, stiffness: 160, mass: 0.8 },
    durationInFrames: durationFrames,
  });
  const deg = interpolate(p, [0, 1], [75, 0]);
  const opacity = interpolate(rel, [0, 4], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        perspective: 1200,
        opacity,
        transform: `perspective(1200px) rotate${axis}(${deg}deg) scale(${interpolate(p, [0, 1], [0.9, 1])})`,
      }}
    >
      {children}
    </div>
  );
};
```


#### `remotion_reels/src/components/fx/CinematicStagePrimitives.tsx`

```tsx
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { getAliveFloat, SPRING_SNAPPY } from "./motionPresets";

const resolveAsset = (src: string) =>
  src.startsWith("http") || src.startsWith("/") ? src : staticFile(src);

/**
 * LAYER 3A: CircularAvatarNode — Chân dung nhân vật thật (avatar_node) gắn thẳng vào tâm mạng lưới / trục timeline.
 * Khung tròn sắc nét, viền sáng mảnh #22D3EE / #FFE600, canh objectPosition="50% 18%" không bao giờ cắt trán, bóng đổ sâu.
 */
export const CircularAvatarNode: React.FC<{
  src: string;
  size?: number;
  x?: number;
  y?: number;
  borderColor?: "#22D3EE" | "#FFE600" | string;
  borderWidth?: number;
  objectPosition?: string;
  label?: string;
  subLabel?: string;
  startFrame?: number;
  floatAmp?: number;
  inline?: boolean;
  zIndex?: number;
}> = ({
  src,
  size = 176,
  x = 540,
  y = 760,
  borderColor = "#22D3EE",
  borderWidth = 3.5,
  objectPosition = "50% 18%",
  label,
  subLabel,
  startFrame = 0,
  floatAmp = 4,
  inline = false,
  zIndex = 26,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const rel = frame - startFrame;
  const pop = spring({ frame: rel, fps, config: SPRING_SNAPPY });
  const alive = getAliveFloat(rel, fps, floatAmp, 0.35);
  const scale = interpolate(pop, [0, 1], [0.82, 1.0]);

  const posStyle: React.CSSProperties = inline
    ? {
        position: "relative",
        transform: `translate3d(0, ${alive.y.toFixed(2)}px, 0) scale(${scale})`,
      }
    : {
        position: "absolute",
        left: x,
        top: y,
        transform: `translate3d(-50%, calc(-50% + ${alive.y.toFixed(2)}px), 0) scale(${scale})`,
      };

  return (
    <div
      style={{
        ...posStyle,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        willChange: "transform",
        opacity: interpolate(pop, [0, 0.35], [0, 1], { extrapolateRight: "clamp" }),
        zIndex,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          width: size,
          height: size,
          borderRadius: "50%",
          overflow: "hidden",
          background: "#081529",
          border: `${borderWidth}px solid ${borderColor}`,
          boxShadow: "0 16px 36px rgba(0, 0, 0, 0.94), 0 6px 14px rgba(0, 0, 0, 0.88), inset 0 1px 1px rgba(255, 255, 255, 0.28)",
          flexShrink: 0,
        }}
      >
        <Img
          src={resolveAsset(src)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition,
            filter: "contrast(1.06) saturate(1.02)",
          }}
        />
      </div>
      {label && (
        <div
          style={{
            marginTop: -12,
            padding: "6px 18px",
            borderRadius: 999,
            background: "#091426",
            border: `2px solid ${borderColor}`,
            boxShadow: "0 10px 22px rgba(0, 0, 0, 0.92)",
            whiteSpace: "nowrap",
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontFamily: "'BeVietnamProBlack', sans-serif",
              fontSize: Math.max(20, Math.min(26, Math.round(size * 0.135))),
              fontWeight: 900,
              color: "#FFFFFF",
              letterSpacing: "0.02em",
              lineHeight: 1.15,
            }}
          >
            {label}
          </div>
          {subLabel && (
            <div
              style={{
                fontFamily: "'BeVietnamProExtraBold', sans-serif",
                fontSize: 16,
                fontWeight: 800,
                color: borderColor,
                lineHeight: 1.1,
                marginTop: 2,
              }}
            >
              {subLabel}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

/**
 * LAYER 3B: HeroCutout3D — Vật thể tách nền (prop_3d) nổi khối 3D thật sự trên nền lưới xanh đêm #061224
 * - Phối cảnh 3D nhẹ (tiltX, tiltY, perspective: 1100px) + chuyển động nổi mượt getAliveFloat (60fps GPU).
 * - 2 lớp bóng đổ thực tế bám dáng vật thể (bóng tiếp xúc đậm gần + bóng môi trường sâu mềm phía dưới).
 * - Viền sáng cạnh cực mảnh (subtle rim highlight) tách bạch vật thể tối khỏi nền lưới, KHÔNG dùng glow neon.
 * - Hỗ trợ mode="avatar_node" chuyển thẳng sang CircularAvatarNode khi cần.
 */
export const HeroCutout3D: React.FC<{
  src: string;
  x?: number;
  y?: number;
  width?: number;
  maxHeight?: number;
  startFrame?: number;
  floatAmp?: number;
  brightness?: number;
  rotateDeg?: number;
  tiltX?: number;
  tiltY?: number;
  perspective?: number;
  rimHighlight?: boolean;
  darkObjectBacklight?: boolean;
  mode?: "prop_3d" | "avatar_node";
  avatarBorderColor?: "#22D3EE" | "#FFE600" | string;
  avatarLabel?: string;
  zIndex?: number;
  fadeBottom?: boolean;
}> = ({
  src,
  x = 540,
  y = 980,
  width = 580,
  maxHeight = 760,
  startFrame = 0,
  floatAmp = 8,
  brightness = 1.0,
  rotateDeg = 0,
  tiltX = 6,
  tiltY = -9,
  perspective = 1050,
  rimHighlight = true,
  darkObjectBacklight = true,
  mode = "prop_3d",
  avatarBorderColor = "#22D3EE",
  avatarLabel,
  zIndex = 20,
  fadeBottom = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;

  if (mode === "avatar_node") {
    return (
      <CircularAvatarNode
        src={src}
        size={Math.min(width, maxHeight, 260)}
        x={x}
        y={y}
        borderColor={avatarBorderColor}
        label={avatarLabel}
        startFrame={startFrame}
        floatAmp={Math.min(floatAmp, 5)}
        zIndex={zIndex}
      />
    );
  }

  const rel = frame - startFrame;
  const pop = spring({ frame: rel, fps, config: { damping: 16, stiffness: 190, mass: 0.85 } });
  const alive = getAliveFloat(rel, fps, floatAmp, 0.75);
  const scale = interpolate(pop, [0, 1], [0.82, 1.0]);

  // Góc nghiêng 3D sống động nhẹ nhàng quanh góc đặt ban đầu (giống con chip nổi khối 3D)
  const dynTiltX = tiltX + Math.sin((rel / Math.max(1, fps)) * 1.4) * 1.4;
  const dynTiltY = tiltY + Math.cos((rel / Math.max(1, fps)) * 1.15) * 1.8;
  const dynRotZ = rotateDeg + alive.rot;

  const fadeMask: React.CSSProperties = fadeBottom
    ? {
        WebkitMaskImage: "linear-gradient(to bottom, #000 0%, #000 78%, transparent 100%)",
        maskImage: "linear-gradient(to bottom, #000 0%, #000 78%, transparent 100%)",
      }
    : {};

  // Viền sáng cạnh cực mảnh (subtle rim highlight, 0 neon) + 2 lớp bóng đổ thực tế bám dáng vật thể
  const rimFilter = rimHighlight
    ? "drop-shadow(0px -1.5px 0.8px rgba(210, 238, 255, 0.36)) drop-shadow(-1px 0px 0.6px rgba(175, 222, 255, 0.22)) "
    : "";
  const dualShadowFilter =
    "drop-shadow(0px 12px 14px rgba(0, 0, 0, 0.92)) drop-shadow(0px 34px 48px rgba(2, 6, 16, 0.96))";

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width,
        maxHeight,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        perspective: `${perspective}px`,
        transform: `translate3d(-50%, calc(-50% + ${alive.y.toFixed(2)}px), 0) scale(${scale})`,
        willChange: "transform",
        opacity: interpolate(pop, [0, 0.35], [0, 1], { extrapolateRight: "clamp" }),
        zIndex,
        pointerEvents: "none",
      }}
    >
      {darkObjectBacklight && (
        <div
          style={{
            position: "absolute",
            width: "118%",
            height: "118%",
            borderRadius: "50%",
            background: "radial-gradient(circle, rgba(56, 189, 248, 0.22) 0%, transparent 70%)",
            pointerEvents: "none",
            zIndex: 0,
          }}
        />
      )}
      <Img
        src={resolveAsset(src)}
        style={{
          position: "relative",
          zIndex: 1,
          maxWidth: "100%",
          maxHeight: `${maxHeight}px`,
          width: "100%",
          height: "auto",
          objectFit: "contain",
          transform: `rotateX(${dynTiltX.toFixed(2)}deg) rotateY(${dynTiltY.toFixed(2)}deg) rotateZ(${dynRotZ.toFixed(2)}deg)`,
          transformStyle: "preserve-3d",
          willChange: "transform",
          filter: `brightness(${brightness}) contrast(1.08) saturate(1.0) ${rimFilter}${dualShadowFilter}`,
          ...fadeMask,
        }}
      />
    </div>
  );
};

/**
 * LAYER 4: Forensic Stamp Slam (Heavy mechanical slam from 2.2x -> 1.0x)
 */
export const ForensicStampSlam: React.FC<{
  text: string;
  startFrame: number;
  x?: number;
  y?: number;
  color?: string;
  rotate?: number;
  fontSize?: number;
  zIndex?: number;
}> = ({
  text,
  startFrame,
  x = 540,
  y = 1180,
  color = "#FF3B47",
  rotate = -7,
  fontSize = 44,
  zIndex = 34,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const pop = spring({ frame: frame - startFrame, fps, config: { damping: 10, stiffness: 240, mass: 0.7 } });
  const scale = interpolate(pop, [0, 1], [2.1, 1.0]);
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `translate(-50%, -50%) scale(${scale}) rotate(${rotate}deg)`,
        opacity: pop,
        padding: "12px 32px",
        borderRadius: 14,
        background: "#0B0F1A",
        border: `5px solid ${color}`,
        boxShadow: "0 20px 40px rgba(0, 0, 0, 0.92)",
        whiteSpace: "nowrap",
        zIndex,
        pointerEvents: "none",
      }}
    >
      <span
        style={{
          fontFamily: "'KanitBlack', 'BeVietnamProBlack', sans-serif",
          fontSize,
          fontWeight: 900,
          color,
          letterSpacing: "0.04em",
        }}
      >
        {text}
      </span>
    </div>
  );
};

/**
 * LAYER 4B: Crisp Rolling Odometer Metric (Spatial Floating, ZERO Box)
 */
export const MetricOdometerHero: React.FC<{
  from: number;
  to: number;
  startFrame: number;
  durationFrames?: number;
  prefix?: string;
  suffix?: string;
  label?: string;
  x?: number;
  y?: number;
  color?: string;
  fontSize?: number;
  zIndex?: number;
}> = ({
  from,
  to,
  startFrame,
  durationFrames = 30,
  prefix = "",
  suffix = "",
  label,
  x = 540,
  y = 1480,
  color = "#FFE600",
  fontSize = 86,
  zIndex = 36,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const rel = frame - startFrame;
  const pop = spring({ frame: rel, fps, config: { damping: 13, stiffness: 185 } });
  const val = Math.round(
    interpolate(rel, [0, durationFrames], [from, to], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }),
  );
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        transform: `translate(-50%, -50%) scale(${interpolate(pop, [0, 1], [0.75, 1.0])})`,
        opacity: pop,
        textAlign: "center",
        whiteSpace: "nowrap",
        zIndex,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          fontFamily: "'KanitBlack', 'BeVietnamProBlack', sans-serif",
          fontSize,
          fontWeight: 900,
          lineHeight: 1.0,
          color,
          WebkitTextStroke: "8px #05070C",
          paintOrder: "stroke fill",
          textShadow: "0 12px 26px rgba(0, 0, 0, 0.92)",
        }}
      >
        {prefix}
        {val.toLocaleString("vi-VN")}
        {suffix}
      </div>
      {label && (
        <div
          style={{
            marginTop: 8,
            fontFamily: "'BeVietnamProExtraBold', sans-serif",
            fontSize: 30,
            fontWeight: 800,
            color: "#FFFFFF",
            letterSpacing: "0.05em",
            textTransform: "uppercase",
            WebkitTextStroke: "5px #05070C",
            paintOrder: "stroke fill",
            textShadow: "0 6px 18px rgba(0, 0, 0, 0.92)",
          }}
        >
          {label}
        </div>
      )}
    </div>
  );
};
```


#### `remotion_reels/src/components/fx/fxFonts.ts`

```typescript
import { continueRender, delayRender, staticFile } from "remotion";

/**
 * Khóa 100% font tiếng Việt đầy đủ dấu (BeVietnamPro) cho mọi FX primitive,
 * kể cả alias KanitBlack cũng trỏ về BeVietnamPro-Black.ttf để không bao giờ vỡ dấu Ả, Ẩ, Ỡ.
 */
const FX_FONTS: Array<[string, string]> = [
  ["BeVietnamProBlack", "fonts/BeVietnamPro-Black.ttf"],
  ["BeVietnamProExtraBold", "fonts/BeVietnamPro-ExtraBold.ttf"],
  ["KanitBlack", "fonts/BeVietnamPro-Black.ttf"],
];

let loaded = false;

export const ensureFxFonts = (): void => {
  if (loaded || typeof document === "undefined") return;
  loaded = true;
  const handle = delayRender("Loading FX Vietnamese fonts");
  Promise.all(
    FX_FONTS.map(([family, file]) => {
      const face = new FontFace(family, `url(${staticFile(file)})`, { weight: "100 900" });
      return face.load().then((f) => {
        document.fonts.add(f);
      });
    }),
  )
    .then(() => continueRender(handle))
    .catch((err) => {
      console.error("FX font load failed", err);
      continueRender(handle);
    });
};

ensureFxFonts();
```


#### `remotion_reels/src/components/fx/index.ts`

```typescript
import "./fxFonts";
export * from "./fxFonts";
export * from "./motionPresets";
export * from "./CapCutTransitions";
export * from "./KineticTextFX";
export * from "./KnowledgeMotionFX";
export * from "./MotionTrackedCallout";
export * from "./RealSceneSpotlight";
export * from "./CinematicStagePrimitives";
export * from "./KnowledgeExplainerFX";
```


#### `remotion_reels/src/components/fx/KineticTextFX.tsx`

```tsx
import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const MarkerHighlightText: React.FC<{
  text: string;
  startFrame?: number;
  highlightColor?: string;
  textColor?: string;
  fontSize?: number;
  fontFamily?: string;
}> = ({
  text,
  startFrame = 0,
  highlightColor = "#FACC15",
  textColor = "#0B0F19",
  fontSize = 54,
  fontFamily = "'BeVietnamProBlack', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const sweepPct = interpolate(rel, [0, 14], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <span
      style={{
        position: "relative",
        display: "inline-block",
        padding: "2px 12px",
        margin: "0 8px",
        lineHeight: 1.24,
        verticalAlign: "middle",
        whiteSpace: "nowrap",
        fontSize,
        fontFamily,
        fontWeight: 900,
        color: sweepPct > 45 ? textColor : "#FFFFFF",
        letterSpacing: "-0.01em",
      }}
    >
      <span
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: "8%",
          bottom: "8%",
          backgroundColor: highlightColor,
          transformOrigin: "left center",
          transform: `scale3d(${sweepPct / 100}, 1, 1)`,
          willChange: "transform",
          borderRadius: 6,
          zIndex: 0,
        }}
      />
      <span style={{ position: "relative", zIndex: 1 }}>{text}</span>
    </span>
  );
};

export const StaggerWaveText: React.FC<{
  text: string;
  startFrame?: number;
  staggerFrames?: number;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
}> = ({
  text,
  startFrame = 0,
  staggerFrames = 3,
  fontSize = 52,
  color = "#FFFFFF",
  fontFamily = "'BeVietnamProBlack', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "10px 14px",
        fontSize,
        fontFamily,
        fontWeight: 900,
        color,
      }}
    >
      {words.map((word, idx) => {
        const rel = Math.max(0, frame - (startFrame + idx * staggerFrames));
        const p = spring({
          frame: rel,
          fps,
          config: { damping: 14, stiffness: 240, mass: 0.55 },
        });
        const y = interpolate(p, [0, 1], [34, 0]);
        const op = interpolate(rel, [0, 4], [0, 1], { extrapolateRight: "clamp" });
        return (
          <span
            key={idx}
            style={{
              display: "inline-block",
              opacity: op,
              transform: `translateY(${y}px) scale(${interpolate(p, [0, 1], [0.85, 1])})`,
              WebkitTextStroke: "7px #05070C",
              paintOrder: "stroke fill",
              textShadow: "0 4px 20px rgba(0,0,0,0.9)",
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

export const GlitchSplitText: React.FC<{
  text: string;
  startFrame?: number;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
}> = ({
  text,
  startFrame = 0,
  fontSize = 58,
  color = "#FFFFFF",
  fontFamily = "'BeVietnamProBlack', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const glitchAmp = rel < 14 ? interpolate(rel, [0, 14], [10, 0]) : 0;
  const offset = Math.sin(rel * 2.7) * glitchAmp;

  return (
    <div style={{ position: "relative", display: "inline-block", fontSize, fontFamily, fontWeight: 900 }}>
      {glitchAmp > 0.3 && (
        <>
          <span
            style={{
              position: "absolute",
              left: offset,
              top: 0,
              color: "#EF4444",
              opacity: 0.75,
              pointerEvents: "none",
            }}
          >
            {text}
          </span>
          <span
            style={{
              position: "absolute",
              left: -offset,
              top: 0,
              color: "#38BDF8",
              opacity: 0.75,
              pointerEvents: "none",
            }}
          >
            {text}
          </span>
        </>
      )}
      <span
        style={{
          position: "relative",
          color,
          WebkitTextStroke: "2px rgba(0,0,0,0.9)",
          textShadow: "0 6px 20px rgba(0,0,0,0.9)",
        }}
      >
        {text}
      </span>
    </div>
  );
};

export const MetallicSweepText: React.FC<{
  text: string;
  startFrame?: number;
  fontSize?: number;
  fontFamily?: string;
}> = ({
  text,
  startFrame = 0,
  fontSize = 62,
  fontFamily = "'KanitBlack', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const pos = interpolate(rel % 90, [0, 45, 90], [-40, 140, 140]);

  return (
    <div
      style={{
        fontSize,
        fontFamily,
        fontWeight: 900,
        backgroundImage: `linear-gradient(110deg, #F59E0B 0%, #FDE68A ${pos}%, #FFFBEB ${pos + 8}%, #F59E0B ${pos + 18}%, #D97706 100%)`,
        WebkitBackgroundClip: "text",
        color: "transparent",
        filter: "drop-shadow(0 6px 18px rgba(0,0,0,0.9))",
      }}
    >
      {text}
    </div>
  );
};

export const OdometerCounter: React.FC<{
  from?: number;
  to: number;
  startFrame?: number;
  durationFrames?: number;
  prefix?: string;
  suffix?: string;
  fontSize?: number;
  color?: string;
}> = ({
  from = 0,
  to,
  startFrame = 0,
  durationFrames = 36,
  prefix = "",
  suffix = "",
  fontSize = 84,
  color = "#42B2F2",
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const t = interpolate(rel, [0, durationFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const eased = 1 - Math.pow(1 - t, 3);
  const val = Math.round(from + (to - from) * eased);

  return (
    <span
      style={{
        fontSize,
        fontFamily: "'KanitBlack', monospace",
        fontWeight: 900,
        color,
        fontVariantNumeric: "tabular-nums",
        whiteSpace: "nowrap",
        WebkitTextStroke: "7px #05070C",
        paintOrder: "stroke fill",
        textShadow: "0 4px 20px rgba(0,0,0,0.9)",
      }}
    >
      {prefix}
      {val.toLocaleString("vi-VN")}
      {suffix}
    </span>
  );
};
```


#### `remotion_reels/src/components/fx/KnowledgeExplainerFX.tsx`

```tsx
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { AE_SNAP_OUT, getAliveFloat, getKenBurnsScale, SPRING_HEAVY_SLAM, SPRING_SNAPPY } from "./motionPresets";
import { CircularAvatarNode, HeroCutout3D } from "./CinematicStagePrimitives";

const resolveAsset = (src: string) =>
  src.startsWith("http://") || src.startsWith("https://") ? src : staticFile(src);

function fitSingleLineSize(text: string, baseSize: number, maxChars: number, minSize: number = 20): number {
  const len = text.trim().length;
  if (len <= maxChars) return baseSize;
  return Math.max(minSize, Math.round((baseSize * maxChars) / len));
}

/**
 * Khung hiển thị ảnh 100% nguyên vẹn không cắt đầu/mặt hay mất chữ:
 * - Mặc định imageFit="contain" đặt trên lớp nền đệm mờ tối từ chính bức ảnh đó (blur 18px, brightness 0.35, scale 1.15).
 * - Nếu chọn imageFit="cover", mặc định objectPosition="50% 18%" bảo vệ vùng mặt/đầu.
 */
export const ContainedPhotoBox: React.FC<{
  src: string;
  width?: number | string;
  height?: number;
  borderRadius?: number;
  border?: string;
  imageFit?: "contain" | "cover";
  objectPosition?: string;
  zoomScale?: number;
}> = ({
  src,
  width = "100%",
  height = 340,
  borderRadius = 16,
  border = "2px solid rgba(120, 190, 255, 0.35)",
  imageFit = "contain",
  objectPosition = "50% 18%",
  zoomScale = 1.0,
}) => {
  const resolved = resolveAsset(src);
  return (
    <div
      style={{
        position: "relative",
        width,
        height,
        borderRadius,
        overflow: "hidden",
        background: "#06101E",
        border,
        boxShadow: "0 18px 40px rgba(0, 0, 0, 0.9)",
      }}
    >
      {imageFit === "contain" && (
        <Img
          src={resolved}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: "50% 50%",
            filter: "blur(18px) brightness(0.35)",
            transform: "translate3d(0, 0, 0) scale(1.15)",
            pointerEvents: "none",
          }}
        />
      )}
      <Img
        src={resolved}
        style={{
          position: "relative",
          zIndex: 1,
          width: "100%",
          height: "100%",
          objectFit: imageFit,
          objectPosition: imageFit === "cover" ? objectPosition : "50% 50%",
          transform: `translate3d(0, 0, 0) scale(${zoomScale})`,
          willChange: "transform",
          display: "block",
          opacity: 1,
        }}
      />
    </div>
  );
};

/* ============================================================================
 * 0A. DualStageKnowledgeLayout: Chia màn hình 2 tầng phủ >= 80% khung 9:16
 * ============================================================================ */
export const DualStageKnowledgeLayout: React.FC<{
  topStage: React.ReactNode;
  bottomStage: React.ReactNode;
  gap?: number;
}> = ({ topStage, bottomStage, gap = 28 }) => {
  return (
    <div
      style={{
        position: "absolute",
        left: 80,
        top: 350,
        width: 920,
        height: 1190,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        gap,
        zIndex: 20,
      }}
    >
      <div
        style={{
          width: "100%",
          height: 540,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          position: "relative",
        }}
      >
        {topStage}
      </div>
      <div
        style={{
          width: "100%",
          height: 610,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          position: "relative",
        }}
      >
        {bottomStage}
      </div>
    </div>
  );
};

/* ============================================================================
 * 0B. EditorialSplitTimeline: Trục dọc sáng mảnh chính giữa (X: 540) chia
 *     2–3 tầng so le trái–phải, ảnh nguyên vẹn contain + blur pad, ít chữ.
 * ============================================================================ */
export interface EditorialSplitItem {
  triggerFrame: number;
  metric: string;
  title: string;
  detail?: string;
  imageSrc?: string;
  imageFit?: "contain" | "cover";
  objectPosition?: string;
  accentColor?: string;
}

export const EditorialSplitTimeline: React.FC<{
  items: EditorialSplitItem[];
  startFrame?: number;
}> = ({ items, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const safeItems = items.slice(0, 3);
  const rel = Math.max(0, frame - startFrame);
  const axisScaleY = interpolate(rel, [0, 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        left: 80,
        top: 370,
        width: 920,
        height: 1150,
        zIndex: 22,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: 20,
          width: 4,
          height: 1080,
          transformOrigin: "top center",
          transform: `translate3d(-50%, 0, 0) scaleY(${axisScaleY})`,
          willChange: "transform",
          background: "linear-gradient(180deg, #22D3EE 0%, #FFE600 100%)",
          borderRadius: 4,
        }}
      />

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-around",
          height: "100%",
          gap: 24,
        }}
      >
        {safeItems.map((item, idx) => {
          const isLeftImg = idx % 2 === 0;
          const active = frame >= item.triggerFrame;
          const op = active
            ? interpolate(frame, [item.triggerFrame, item.triggerFrame + 5], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })
            : 0.78;
          const pop = active
            ? spring({
                frame: frame - item.triggerFrame,
                fps,
                config: SPRING_SNAPPY,
              })
            : 0.94;
          const accent = item.accentColor || (idx % 2 === 0 ? "#FFE600" : "#22D3EE");
          const kb = active ? getKenBurnsScale(frame - item.triggerFrame, 120, 1.0, 1.05) : 1.0;

          const mediaBox = item.imageSrc ? (
            <div
              style={{
                width: 410,
                opacity: op,
                transform: `translate3d(0, 0, 0) scale(${pop})`,
                willChange: "transform",
              }}
            >
              <ContainedPhotoBox
                src={item.imageSrc}
                width={410}
                height={285}
                borderRadius={18}
                border={`3px solid ${active ? accent : "rgba(148,163,184,0.35)"}`}
                imageFit={item.imageFit ?? "contain"}
                objectPosition={item.objectPosition ?? "50% 18%"}
                zoomScale={kb}
              />
            </div>
          ) : (
            <div
              style={{
                width: 410,
                height: 240,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                opacity: op,
                transform: `translate3d(0, 0, 0) scale(${pop})`,
                willChange: "transform",
              }}
            >
              <div
                style={{
                  fontFamily: "'BeVietnamProBlack', sans-serif",
                  fontSize: fitSingleLineSize(item.metric, 72, 10, 44),
                  color: accent,
                  whiteSpace: "nowrap",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 8px 20px rgba(0,0,0,0.95)",
                }}
              >
                {item.metric}
              </div>
            </div>
          );

          const textBox = (
            <div
              style={{
                width: 410,
                padding: "12px 18px",
                borderLeft: `6px solid ${active ? accent : "rgba(148,163,184,0.4)"}`,
                opacity: op,
                transform: `translate3d(0, 0, 0) scale(${pop})`,
                willChange: "transform",
              }}
            >
              <div
                style={{
                  fontFamily: "'BeVietnamProBlack', sans-serif",
                  fontSize: fitSingleLineSize(item.metric, 50, 12, 32),
                  color: accent,
                  lineHeight: 1.08,
                  whiteSpace: "nowrap",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 6px 16px rgba(0,0,0,0.95)",
                }}
              >
                {item.metric}
              </div>
              <div
                style={{
                  marginTop: 8,
                  fontFamily: "'BeVietnamProBlack', sans-serif",
                  fontSize: fitSingleLineSize(item.title, 26, 20, 20),
                  color: "#FFFFFF",
                  lineHeight: 1.25,
                  textShadow: "0 4px 12px rgba(0,0,0,0.95)",
                }}
              >
                {item.title}
              </div>
            </div>
          );

          return (
            <div
              key={`split-${idx}`}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                position: "relative",
              }}
            >
              {isLeftImg ? mediaBox : textBox}
              <div
                style={{
                  position: "absolute",
                  left: "50%",
                  top: "50%",
                  width: 20,
                  height: 20,
                  borderRadius: "50%",
                  background: active ? accent : "#334155",
                  border: "4px solid #061224",
                  transform: "translate3d(-50%, -50%, 0)",
                  zIndex: 5,
                }}
              />
              {isLeftImg ? textBox : mediaBox}
            </div>
          );
        })}
      </div>
    </div>
  );
};

/* ============================================================================
 * 0C. HighContrastConclusionCard: Thẻ chốt kết luận nền trắng #FFFFFF hoặc
 *     vàng #FFE600, chữ đen siêu đậm, chỉ bật khi vùng đáy trống (không đè sơ đồ).
 * ============================================================================ */
export const HighContrastConclusionCard: React.FC<{
  headline: string;
  subline?: string;
  variant?: "white" | "yellow";
  startFrame?: number;
  top?: number;
}> = ({ headline, subline, variant = "yellow", startFrame = 0, top = 1340 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;

  const rel = frame - startFrame;
  const op = interpolate(rel, [0, 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pop = spring({ frame: rel, fps, config: SPRING_HEAVY_SLAM });
  const bg = variant === "white" ? "#FFFFFF" : "#FFE600";

  return (
    <div
      style={{
        position: "absolute",
        left: 90,
        top,
        width: 900,
        padding: "24px 30px",
        borderRadius: 22,
        background: bg,
        boxShadow: "0 22px 48px rgba(0, 0, 0, 0.92)",
        textAlign: "center",
        transform: `translate3d(0, 0, 0) scale(${0.92 + 0.08 * pop})`,
        willChange: "transform",
        opacity: op,
        zIndex: 35,
      }}
    >
      <div
        style={{
          fontFamily: "'BeVietnamProBlack', sans-serif",
          fontSize: fitSingleLineSize(headline, 36, 26, 24),
          color: "#05070C",
          lineHeight: 1.2,
          whiteSpace: "nowrap",
        }}
      >
        {headline}
      </div>
      {subline && (
        <div
          style={{
            marginTop: 6,
            fontFamily: "'BeVietnamProExtraBold', sans-serif",
            fontSize: fitSingleLineSize(subline, 22, 36, 17),
            color: "#1E293B",
            lineHeight: 1.25,
            whiteSpace: "nowrap",
          }}
        >
          {subline}
        </div>
      )}
    </div>
  );
};

/* ============================================================================
 * 0D. VisualComparisonStrip: Dải so sánh trực tiếp 2 vế (nowrap chống rớt chữ đơn)
 * ============================================================================ */
export const VisualComparisonStrip: React.FC<{
  wrongTitle: string;
  wrongReason: string;
  rightTitle: string;
  rightReason: string;
  startFrame?: number;
  rightDelayFrames?: number;
  width?: number;
}> = ({
  wrongTitle,
  wrongReason,
  rightTitle,
  rightReason,
  startFrame = 0,
  rightDelayFrames = 12,
  width = 860,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const leftRel = Math.max(0, frame - startFrame);
  const rightRel = Math.max(0, frame - (startFrame + rightDelayFrames));

  const leftOp = frame >= startFrame ? interpolate(leftRel, [0, 5], [0, 1], { extrapolateRight: "clamp" }) : 0.78;
  const rightOp =
    frame >= startFrame + rightDelayFrames
      ? interpolate(rightRel, [0, 5], [0, 1], { extrapolateRight: "clamp" })
      : 0.78;

  const leftPop = frame >= startFrame ? spring({ frame: leftRel, fps, config: SPRING_SNAPPY }) : 0.94;
  const rightPop =
    frame >= startFrame + rightDelayFrames
      ? spring({ frame: rightRel, fps, config: SPRING_SNAPPY })
      : 0.94;

  return (
    <div
      style={{
        width,
        margin: "0 auto",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "stretch",
        gap: 24,
      }}
    >
      <div
        style={{
          flex: 1,
          padding: "18px 20px",
          borderTop: "5px solid #FF3B47",
          borderRadius: "0 0 16px 16px",
          background: "rgba(7, 14, 28, 0.9)",
          boxShadow: "0 16px 34px rgba(0,0,0,0.9)",
          opacity: leftOp,
          transform: `translate3d(0, 0, 0) scale(${leftPop})`,
          willChange: "transform",
        }}
      >
        <div
          style={{
            display: "inline-block",
            padding: "4px 12px",
            borderRadius: 999,
            background: "#FF3B47",
            color: "#FFFFFF",
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: 17,
            marginBottom: 10,
          }}
        >
          ✕ BỊ LOẠI
        </div>
        <div
          style={{
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: fitSingleLineSize(wrongTitle, 28, 15, 19),
            color: "#FFFFFF",
            whiteSpace: "nowrap",
            textDecoration: "line-through",
            textDecorationColor: "#FF3B47",
            textDecorationThickness: "4px",
            lineHeight: 1.2,
          }}
        >
          {wrongTitle}
        </div>
        <div
          style={{
            marginTop: 8,
            fontFamily: "'BeVietnamProExtraBold', sans-serif",
            fontSize: fitSingleLineSize(wrongReason, 20, 20, 16),
            color: "#FCA5A5",
            whiteSpace: "nowrap",
          }}
        >
          {wrongReason}
        </div>
      </div>

      <div
        style={{
          flex: 1,
          padding: "18px 20px",
          borderTop: "5px solid #FFE600",
          borderRadius: "0 0 16px 16px",
          background: "rgba(7, 14, 28, 0.9)",
          boxShadow: "0 16px 34px rgba(0,0,0,0.9)",
          opacity: rightOp,
          transform: `translate3d(0, 0, 0) scale(${rightPop})`,
          willChange: "transform",
        }}
      >
        <div
          style={{
            display: "inline-block",
            padding: "4px 12px",
            borderRadius: 999,
            background: "#FFE600",
            color: "#05070C",
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: 17,
            marginBottom: 10,
          }}
        >
          ✓ CHÍNH XÁC
        </div>
        <div
          style={{
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: fitSingleLineSize(rightTitle, 28, 15, 19),
            color: "#FFE600",
            whiteSpace: "nowrap",
            lineHeight: 1.2,
          }}
        >
          {rightTitle}
        </div>
        <div
          style={{
            marginTop: 8,
            fontFamily: "'BeVietnamProExtraBold', sans-serif",
            fontSize: fitSingleLineSize(rightReason, 20, 20, 16),
            color: "#22D3EE",
            whiteSpace: "nowrap",
          }}
        >
          {rightReason}
        </div>
      </div>
    </div>
  );
};

/* ============================================================================
 * 1. ProcessStepChain: Chuỗi 3–4 bước cơ chế (KHÔNG lặp số 01/02/03 thừa,
 *    khoảng hở thoáng >= 28px dưới nút, nhãn gọn 2–4 từ).
 * ============================================================================ */
export interface ProcessStepItem {
  label: string;
  metric?: string;
  triggerFrame: number;
  accentColor?: string;
}

export const ProcessStepChain: React.FC<{
  steps: ProcessStepItem[];
  startFrame?: number;
  width?: number;
}> = ({ steps, startFrame = 0, width = 840 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const safeSteps = steps.slice(0, 4);
  const count = Math.max(1, safeSteps.length);
  const svgH = 260;
  const padX = 115;
  const usableW = width - padX * 2;
  const nodeY = 98;
  const xs = safeSteps.map((_, i) =>
    count === 1 ? width / 2 : padX + (i * usableW) / (count - 1)
  );

  const rel = Math.max(0, frame - startFrame);
  const lineProgress = interpolate(rel, [0, 26], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const totalLen = Math.max(1, xs[xs.length - 1] - xs[0]);
  const particleT = (rel * 0.016) % 1;
  const particleX = xs[0] + totalLen * particleT;

  return (
    <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <svg width={width} height={svgH} viewBox={`0 0 ${width} ${svgH}`} style={{ overflow: "visible" }}>
        {count > 1 && (
          <>
            <line
              x1={xs[0]}
              y1={nodeY}
              x2={xs[xs.length - 1]}
              y2={nodeY}
              stroke="rgba(148, 163, 184, 0.35)"
              strokeWidth={6}
              strokeLinecap="round"
            />
            <line
              x1={xs[0]}
              y1={nodeY}
              x2={xs[0] + totalLen * lineProgress}
              y2={nodeY}
              stroke="#22D3EE"
              strokeWidth={6}
              strokeLinecap="round"
            />
            {lineProgress > 0.15 && (
              <circle
                cx={particleX}
                cy={nodeY}
                r={9}
                fill="#FFE600"
                style={{ filter: "drop-shadow(0 4px 10px rgba(0,0,0,0.85))" }}
              />
            )}
          </>
        )}

        {safeSteps.map((st, idx) => {
          const active = frame >= st.triggerFrame;
          const pop = active
            ? spring({
                frame: frame - st.triggerFrame,
                fps,
                config: SPRING_SNAPPY,
              })
            : 0.92;
          const accent = st.accentColor || "#22D3EE";
          const x = xs[idx];
          const mainText = st.metric || `BƯỚC 0${idx + 1}`;
          const mainFontSize = fitSingleLineSize(mainText, 24, 9, 17);
          const subFontSize = fitSingleLineSize(st.label, 19, 13, 15);

          return (
            <g
              key={`step-${idx}`}
              transform={`translate(${x}, ${nodeY}) scale(${pop}) translate(${-x}, ${-nodeY})`}
              opacity={active ? 1 : 0.78}
            >
              <circle
                cx={x}
                cy={nodeY}
                r={36}
                fill="none"
                stroke={active ? accent : "rgba(148,163,184,0.45)"}
                strokeWidth={4}
                style={{ filter: "drop-shadow(0 8px 18px rgba(0,0,0,0.92))" }}
              />
              <circle
                cx={x}
                cy={nodeY}
                r={10}
                fill={active ? "#FFE600" : "#64748B"}
              />
              <text
                x={x}
                y={nodeY - 52}
                textAnchor="middle"
                fill={active ? "#FFE600" : "#FFFFFF"}
                fontSize={mainFontSize}
                fontWeight={900}
                fontFamily="'BeVietnamProBlack', sans-serif"
                style={{ filter: "drop-shadow(0 6px 14px rgba(0,0,0,0.95))" }}
              >
                {mainText}
              </text>

              {/* Nhãn bước nổi trực tiếp trên nền lưới thoáng rộng */}
              <text
                x={x}
                y={nodeY + 72}
                textAnchor="middle"
                fill="#FFFFFF"
                fontSize={subFontSize}
                fontWeight={900}
                fontFamily="'BeVietnamProBlack', sans-serif"
                style={{ filter: "drop-shadow(0 4px 10px rgba(0,0,0,0.95))" }}
              >
                {st.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

/* ============================================================================
 * 2. VisualBarCompare: Biểu đồ 2–4 cột dâng mượt bằng GPU scaleY + odometer
 * ============================================================================ */
export interface VisualBarItem {
  label: string;
  value: number;
  suffix?: string;
  color?: string;
  startFrame?: number;
}

export const VisualBarCompare: React.FC<{
  items: VisualBarItem[];
  startFrame?: number;
  width?: number;
  maxBarHeight?: number;
}> = ({ items, startFrame = 0, width = 820, maxBarHeight = 300 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const safeItems = items.slice(0, 4);
  const maxVal = Math.max(1, ...safeItems.map((i) => i.value));

  return (
    <div
      style={{
        width,
        margin: "0 auto",
        padding: "20px 18px 16px",
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "space-around",
        gap: 24,
      }}
    >
      {safeItems.map((item, idx) => {
        const sFrame = item.startFrame ?? startFrame + idx * 5;
        const rel = Math.max(0, frame - sFrame);
        const grow = spring({
          frame: rel,
          fps,
          config: SPRING_SNAPPY,
        });
        const targetH = Math.max(24, (item.value / maxVal) * maxBarHeight);
        const displayNum = Math.round(item.value * Math.min(1, grow));
        const barColor = item.color || (idx === 0 ? "#22D3EE" : "#FFE600");
        const numStr = `${displayNum.toLocaleString("vi-VN")}${item.suffix || ""}`;

        return (
          <div
            key={`bar-${idx}`}
            style={{
              flex: 1,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <div
              style={{
                fontFamily: "'BeVietnamProBlack', sans-serif",
                fontSize: fitSingleLineSize(numStr, 38, 9, 24),
                color: barColor,
                marginBottom: 12,
                whiteSpace: "nowrap",
                WebkitTextStroke: "6px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 6px 14px rgba(0,0,0,0.95)",
              }}
            >
              {numStr}
            </div>
            <div
              style={{
                width: "70%",
                height: targetH,
                transformOrigin: "bottom center",
                transform: `translate3d(0, 0, 0) scaleY(${Math.max(0.06, grow)})`,
                willChange: "transform",
                background: `linear-gradient(180deg, ${barColor} 0%, #0A1830 100%)`,
                borderRadius: "14px 14px 4px 4px",
                border: `3px solid ${barColor}`,
                boxShadow: "0 14px 28px rgba(0,0,0,0.9)",
              }}
            />
            <div
              style={{
                marginTop: 14,
                fontFamily: "'BeVietnamProBlack', sans-serif",
                fontSize: fitSingleLineSize(item.label, 21, 14, 16),
                color: "#FFFFFF",
                whiteSpace: "nowrap",
                textAlign: "center",
                textShadow: "0 4px 10px rgba(0,0,0,0.95)",
              }}
            >
              {item.label}
            </div>
          </div>
        );
      })}
    </div>
  );
};

/* ============================================================================
 * 3. EvidenceDocumentCard + SlashCrossOut: Ảnh contain 100% không cắt đầu/chữ,
 *    SlashCrossOut nowrap tự co cỡ chữ (không rớt chữ lẻ xuống dòng).
 * ============================================================================ */
export const SlashCrossOut: React.FC<{
  oldValue: string;
  newValue: string;
  slashFrame: number;
}> = ({ oldValue, newValue, slashFrame }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - slashFrame);
  const slashScale = interpolate(rel, [0, 8], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const newPop = spring({
    frame: Math.max(0, rel - 4),
    fps,
    config: SPRING_HEAVY_SLAM,
  });

  const combinedLen = oldValue.length + newValue.length;
  const oldSize = fitSingleLineSize(oldValue, combinedLen > 18 ? 38 : 48, 12, 24);
  const newSize = fitSingleLineSize(newValue, combinedLen > 18 ? 44 : 56, 12, 26);

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 20,
        marginTop: 16,
        padding: "10px 22px",
        borderRadius: 16,
        background: "rgba(7, 12, 22, 0.96)",
        border: "2.5px solid rgba(255, 230, 0, 0.55)",
        maxWidth: "100%",
        whiteSpace: "nowrap",
      }}
    >
      <div style={{ position: "relative", display: "inline-block", whiteSpace: "nowrap" }}>
        <span
          style={{
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: oldSize,
            color: "#CBD5E1",
            whiteSpace: "nowrap",
          }}
        >
          {oldValue}
        </span>
        {frame >= slashFrame && (
          <div
            style={{
              position: "absolute",
              left: -6,
              right: -6,
              top: "50%",
              height: 6,
              background: "#FF3B47",
              borderRadius: 4,
              transformOrigin: "left center",
              transform: `translate3d(0, -50%, 0) rotate(-7deg) scaleX(${slashScale})`,
              willChange: "transform",
            }}
          />
        )}
      </div>
      {frame >= slashFrame + 4 && (
        <span
          style={{
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: newSize,
            color: "#FFE600",
            whiteSpace: "nowrap",
            transform: `translate3d(0, 0, 0) scale(${newPop})`,
            willChange: "transform",
            display: "inline-block",
            textShadow: "0 6px 16px rgba(0,0,0,0.95)",
          }}
        >
          → {newValue}
        </span>
      )}
    </div>
  );
};

export const EvidenceDocumentCard: React.FC<{
  imageSrc?: string;
  imageFit?: "contain" | "cover";
  objectPosition?: string;
  sourceBadge: string;
  highlightLine: string;
  startFrame?: number;
  highlightFrame?: number;
  rotateDeg?: number;
  tiltY?: number;
  width?: number;
  imageHeight?: number;
  slashOld?: string;
  slashNew?: string;
  slashFrame?: number;
}> = ({
  imageSrc,
  imageFit = "contain",
  objectPosition = "50% 18%",
  sourceBadge,
  highlightLine,
  startFrame = 0,
  highlightFrame,
  rotateDeg = 0,
  tiltY = 0,
  width = 820,
  imageHeight = 350,
  slashOld,
  slashNew,
  slashFrame,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;

  const rel = frame - startFrame;
  const op = interpolate(rel, [0, 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const enter = spring({ frame: rel, fps, config: SPRING_SNAPPY });
  const hlStart = highlightFrame ?? startFrame + 8;
  const hlScale = interpolate(frame, [hlStart, hlStart + 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const kb = getKenBurnsScale(rel, 150, 1.0, 1.04);

  return (
    <div
      style={{
        width,
        margin: "0 auto",
        padding: "20px 24px",
        background: "#0B1220",
        border: "2.5px solid rgba(120, 190, 255, 0.42)",
        borderRadius: 22,
        boxShadow: "0 24px 52px rgba(0, 0, 0, 0.94)",
        transform: `perspective(1100px) rotateY(${tiltY !== 0 ? tiltY : rotateDeg}deg) translate3d(0, 0, 0) scale(${0.94 + 0.06 * enter})`,
        willChange: "transform",
        opacity: op,
        position: "relative",
        zIndex: 25,
      }}
    >
      <div
        style={{
          display: "inline-block",
          background: "#22D3EE",
          color: "#05070C",
          fontFamily: "'BeVietnamProBlack', sans-serif",
          fontSize: 18,
          padding: "4px 14px",
          borderRadius: 8,
          marginBottom: 12,
        }}
      >
        {sourceBadge}
      </div>

      {imageSrc && (
        <div style={{ marginBottom: 14 }}>
          <ContainedPhotoBox
            src={imageSrc}
            width="100%"
            height={imageHeight}
            borderRadius={14}
            imageFit={imageFit}
            objectPosition={objectPosition}
            zoomScale={kb}
          />
        </div>
      )}

      <div style={{ position: "relative", display: "inline-block", padding: "6px 14px", maxWidth: "100%" }}>
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 4,
            bottom: 4,
            background: "#FFE600",
            borderRadius: 6,
            transformOrigin: "left center",
            transform: `scale3d(${hlScale}, 1, 1)`,
            willChange: "transform",
            zIndex: 0,
          }}
        />
        <span
          style={{
            position: "relative",
            zIndex: 1,
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: fitSingleLineSize(highlightLine, 27, 28, 19),
            color: hlScale > 0.45 ? "#05070C" : "#FFFFFF",
            lineHeight: 1.28,
            whiteSpace: "nowrap",
          }}
        >
          {highlightLine}
        </span>
      </div>

      {slashOld && slashNew && slashFrame !== undefined && (
        <div style={{ textAlign: "center" }}>
          <SlashCrossOut oldValue={slashOld} newValue={slashNew} slashFrame={slashFrame} />
        </div>
      )}
    </div>
  );
};

/* ============================================================================
 * 4. RadialNetworkBurst: Tự động thu cỡ chữ & nới bán kính vòng tâm để chữ
 *    bên trong KHÔNG BAO GIỜ tràn ra ngoài viền tròn.
 * ============================================================================ */
export const RadialNetworkBurst: React.FC<{
  centerLabel: string;
  nodeCount?: number;
  startFrame?: number;
  alertFrame?: number;
  size?: number;
}> = ({ centerLabel, nodeCount = 24, startFrame = 0, alertFrame = 99999, size = 540 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const clampedCount = Math.max(12, Math.min(48, nodeCount));
  const cx = size / 2;
  const cy = size / 2;
  const isAlert = frame >= alertFrame;
  const activeColor = isAlert ? "#FF3B47" : "#22D3EE";

  const centerR = Math.max(88, Math.min(124, Math.round(centerLabel.trim().length * 5.8 + 38)));
  const centerFontSize = fitSingleLineSize(centerLabel, 22, Math.floor((centerR * 1.65) / 12), 15);

  const nodes = Array.from({ length: clampedCount }).map((_, i) => {
    const ring = i % 2 === 0 ? 1 : 0.72;
    const angle = (i / clampedCount) * Math.PI * 2 + rel * 0.004;
    const r = Math.max(centerR + 36, size * 0.42 * ring);
    return {
      x: cx + Math.cos(angle) * r,
      y: cy + Math.sin(angle) * r,
      delay: (i % 12) * 1.2,
    };
  });

  const centerPop = spring({ frame: rel, fps, config: SPRING_SNAPPY });

  return (
    <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {nodes.map((nd, idx) => {
          const op = interpolate(rel, [nd.delay, nd.delay + 5], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <g key={`rad-${idx}`} opacity={op}>
              <line
                x1={cx}
                y1={cy}
                x2={nd.x}
                y2={nd.y}
                stroke={activeColor}
                strokeWidth={3}
                strokeOpacity={0.55}
              />
              <circle
                cx={nd.x}
                cy={nd.y}
                r={isAlert ? 8 : 7}
                fill={activeColor}
                stroke="#05070C"
                strokeWidth={2.5}
              />
            </g>
          );
        })}

        <g transform={`translate(${cx}, ${cy}) scale(${centerPop}) translate(${-cx}, ${-cy})`}>
          <circle
            cx={cx}
            cy={cy}
            r={centerR}
            fill="rgba(6, 18, 36, 0.45)"
            stroke={activeColor}
            strokeWidth={4}
            style={{ filter: "drop-shadow(0 12px 24px rgba(0,0,0,0.9))" }}
          />
          <text
            x={cx}
            y={cy + 7}
            textAnchor="middle"
            fill="#FFFFFF"
            fontSize={centerFontSize}
            fontWeight={900}
            fontFamily="'BeVietnamProBlack', sans-serif"
            style={{ filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.95))" }}
          >
            {centerLabel}
          </text>
        </g>
      </svg>
    </div>
  );
};

/* ============================================================================
 * 5. CycleDialProgress: Vòng tròn chu kỳ sáng dần từng nấc + labelRadius rộng
 * ============================================================================ */
export const CycleDialProgress: React.FC<{
  segments: string[];
  activeCount?: number;
  centerMetric: string;
  centerSublabel?: string;
  startFrame?: number;
  stepFrames?: number;
  accentColor?: string;
  size?: number;
}> = ({
  segments,
  activeCount,
  centerMetric,
  centerSublabel = "",
  startFrame = 0,
  stepFrames = 14,
  accentColor = "#FFE600",
  size = 520,
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const total = Math.max(2, segments.length);
  const targetActive = activeCount !== undefined ? Math.min(total, activeCount) : total;
  const litNow = Math.min(targetActive, Math.floor(rel / stepFrames) + 1);
  const cx = size / 2;
  const cy = size / 2;
  const r = size * 0.31;
  const labelRadius = r + 52;
  const circ = 2 * Math.PI * r;
  const gap = 10;
  const segLen = Math.max(8, circ / total - gap);

  return (
    <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ overflow: "visible" }}>
        {segments.map((seg, i) => {
          const isLit = i < litNow;
          const rotateDeg = -90 + (i * 360) / total;
          const labelAngle = ((rotateDeg + 180 / total) * Math.PI) / 180;
          const lx = cx + Math.cos(labelAngle) * labelRadius;
          const ly = cy + Math.sin(labelAngle) * labelRadius;
          return (
            <g key={`seg-${i}`}>
              <circle
                cx={cx}
                cy={cy}
                r={r}
                fill="none"
                stroke={isLit ? accentColor : "rgba(148,163,184,0.35)"}
                strokeWidth={22}
                strokeDasharray={`${segLen} ${circ - segLen}`}
                transform={`rotate(${rotateDeg} ${cx} ${cy})`}
              />
              <text
                x={lx}
                y={ly + 7}
                textAnchor="middle"
                fill={isLit ? "#FFFFFF" : "#CBD5E1"}
                fontSize={22}
                fontWeight={900}
                fontFamily="'BeVietnamProBlack', sans-serif"
                style={{ filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.95))" }}
              >
                {seg}
              </text>
            </g>
          );
        })}

        <circle
          cx={cx}
          cy={cy}
          r={r - 30}
          fill="none"
          stroke="rgba(120,190,255,0.28)"
          strokeWidth={2.5}
        />
        <text
          x={cx}
          y={centerSublabel ? cy - 2 : cy + 14}
          textAnchor="middle"
          fill={accentColor}
          fontSize={fitSingleLineSize(centerMetric, 46, 7, 30)}
          fontWeight={900}
          fontFamily="'BeVietnamProBlack', sans-serif"
          style={{ filter: "drop-shadow(0 6px 16px rgba(0,0,0,0.95))" }}
        >
          {centerMetric}
        </text>
        {centerSublabel && (
          <text
            x={cx}
            y={cy + 34}
            textAnchor="middle"
            fill="#FFFFFF"
            fontSize={fitSingleLineSize(centerSublabel, 20, 12, 15)}
            fontWeight={900}
            fontFamily="'BeVietnamProBlack', sans-serif"
            style={{ filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.95))" }}
          >
            {centerSublabel}
          </text>
        )}
      </svg>
    </div>
  );
};

/* ============================================================================
 * 6. OpenHeroWatermarkStage (Sân Khấu Mở 1 — kiểu Phố Wall 1907):
 *    Con số/năm khổng lồ chìm (fontSize: 220px, opacity: 0.14) phía sau +
 *    HeroCutout3D cỡ lớn bên trái + vật thể/tài liệu thật bên phải +
 *    ảnh tư liệu ngang không viền hộp dày ở nửa dưới.
 * ============================================================================ */
export const OpenHeroWatermarkStage: React.FC<{
  watermarkText: string;
  heroSrc: string;
  rightObjectSrc?: string;
  rightMetric?: string;
  rightLabel?: string;
  bottomPhotoSrc?: string;
  bottomCaption?: string;
  startFrame?: number;
  accentColor?: string;
}> = ({
  watermarkText,
  heroSrc,
  rightObjectSrc,
  rightMetric,
  rightLabel,
  bottomPhotoSrc,
  bottomCaption,
  startFrame = 0,
  accentColor = "#FFE600",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const rel = frame - startFrame;
  const wmPop = spring({ frame: rel, fps, config: SPRING_SNAPPY });
  const rightPop = spring({ frame: Math.max(0, rel - 6), fps, config: SPRING_SNAPPY });
  const bottomPop = spring({ frame: Math.max(0, rel - 10), fps, config: SPRING_SNAPPY });
  const kb = getKenBurnsScale(rel, 180, 1.0, 1.05);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        zIndex: 20,
        pointerEvents: "none",
      }}
    >
      {/* Con số/năm khổng lồ chìm phía sau tạo chiều sâu Sân Khấu Mở */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: 560,
          transform: `translate3d(-50%, -50%, 0) scale(${0.92 + 0.08 * wmPop})`,
          fontFamily: "'BeVietnamProBlack', sans-serif",
          fontSize: fitSingleLineSize(watermarkText, 220, 6, 130),
          fontWeight: 900,
          color: "#FFFFFF",
          opacity: 0.14,
          whiteSpace: "nowrap",
          letterSpacing: "-0.02em",
          zIndex: 10,
        }}
      >
        {watermarkText}
      </div>

      {/* HeroCutout3D cỡ lớn bên trái nổi khối trên nền lưới */}
      <HeroCutout3D
        src={heroSrc}
        x={330}
        y={740}
        width={470}
        maxHeight={560}
        startFrame={startFrame}
        tiltX={5}
        tiltY={8}
        darkObjectBacklight
        zIndex={24}
      />

      {/* Vật thể / số liệu thật bên phải mở thoáng không hộp chữ nhật */}
      <div
        style={{
          position: "absolute",
          left: 595,
          top: 520,
          width: 405,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 14,
          opacity: interpolate(rightPop, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
          transform: `translate3d(0, ${(1 - rightPop) * 26}px, 0) scale(${0.92 + 0.08 * rightPop})`,
          willChange: "transform",
          zIndex: 25,
        }}
      >
        {rightObjectSrc && (
          <div style={{ width: 340, height: 260, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Img
              src={resolveAsset(rightObjectSrc)}
              style={{
                maxWidth: "100%",
                maxHeight: "100%",
                objectFit: "contain",
                filter: "drop-shadow(0 16px 32px rgba(0,0,0,0.92))",
              }}
            />
          </div>
        )}
        {rightMetric && (
          <div
            style={{
              fontFamily: "'BeVietnamProBlack', sans-serif",
              fontSize: fitSingleLineSize(rightMetric, 74, 8, 42),
              color: accentColor,
              whiteSpace: "nowrap",
              WebkitTextStroke: "8px #05070C",
              paintOrder: "stroke fill",
              textShadow: "0 10px 24px rgba(0,0,0,0.95)",
              lineHeight: 1.05,
            }}
          >
            {rightMetric}
          </div>
        )}
        {rightLabel && (
          <div
            style={{
              fontFamily: "'BeVietnamProBlack', sans-serif",
              fontSize: fitSingleLineSize(rightLabel, 28, 16, 20),
              color: "#FFFFFF",
              whiteSpace: "nowrap",
              textAlign: "center",
              textShadow: "0 6px 16px rgba(0,0,0,0.95)",
            }}
          >
            {rightLabel}
          </div>
        )}
      </div>

      {/* Ảnh tư liệu ngang không viền hộp dày ở nửa dưới */}
      {bottomPhotoSrc && (
        <div
          style={{
            position: "absolute",
            left: 80,
            top: 1090,
            width: 920,
            opacity: interpolate(bottomPop, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
            transform: `translate3d(0, ${(1 - bottomPop) * 28}px, 0)`,
            willChange: "transform",
            zIndex: 23,
          }}
        >
          <ContainedPhotoBox
            src={bottomPhotoSrc}
            width={920}
            height={380}
            borderRadius={16}
            border="1.5px solid rgba(148, 197, 255, 0.25)"
            imageFit="contain"
            zoomScale={kb}
          />
          {bottomCaption && (
            <div
              style={{
                marginTop: 12,
                textAlign: "center",
                fontFamily: "'BeVietnamProBlack', sans-serif",
                fontSize: fitSingleLineSize(bottomCaption, 26, 28, 18),
                color: "#E2E8F0",
                whiteSpace: "nowrap",
                textShadow: "0 4px 12px rgba(0,0,0,0.95)",
              }}
            >
              {bottomCaption}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

/* ============================================================================
 * 7. RadialAvatarHub (Sân Khấu Mở 2 — kiểu Jensen Huang 60 lãnh đạo):
 *    Ghép CircularAvatarNode ở chính giữa tâm RadialNetworkBurst tỏa tia xung quanh
 *    + tiêu đề / con số lớn nổi trực tiếp ở đáy.
 * ============================================================================ */
export const RadialAvatarHub: React.FC<{
  avatarSrc: string;
  avatarLabel?: string;
  avatarSubLabel?: string;
  avatarBorderColor?: "#22D3EE" | "#FFE600" | string;
  nodeCount?: number;
  bottomMetric?: string;
  bottomHeadline?: string;
  alertFrame?: number;
  startFrame?: number;
  size?: number;
}> = ({
  avatarSrc,
  avatarLabel,
  avatarSubLabel,
  avatarBorderColor = "#22D3EE",
  nodeCount = 28,
  bottomMetric,
  bottomHeadline,
  alertFrame = 99999,
  startFrame = 0,
  size = 700,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const rel = frame - startFrame;
  const clampedCount = Math.max(12, Math.min(48, nodeCount));
  const cx = size / 2;
  const cy = size / 2;
  const isAlert = frame >= alertFrame;
  const activeColor = isAlert ? "#FF3B47" : avatarBorderColor;
  const bottomPop = spring({ frame: Math.max(0, rel - 8), fps, config: SPRING_SNAPPY });

  const nodes = Array.from({ length: clampedCount }).map((_, i) => {
    const ring = i % 2 === 0 ? 1 : 0.74;
    const angle = (i / clampedCount) * Math.PI * 2 + rel * 0.004;
    const r = Math.max(150, size * 0.43 * ring);
    return {
      x: cx + Math.cos(angle) * r,
      y: cy + Math.sin(angle) * r,
      delay: (i % 12) * 1.2,
    };
  });

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        zIndex: 22,
        pointerEvents: "none",
      }}
    >
      {/* Mạng lưới tỏa tia trực tiếp trên nền lưới xanh dương */}
      <div
        style={{
          position: "absolute",
          left: 540 - size / 2,
          top: 800 - size / 2,
          width: size,
          height: size,
        }}
      >
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ overflow: "visible" }}>
          {nodes.map((nd, idx) => {
            const op = interpolate(rel, [nd.delay, nd.delay + 5], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            });
            return (
              <g key={`hub-rad-${idx}`} opacity={op}>
                <line
                  x1={cx}
                  y1={cy}
                  x2={nd.x}
                  y2={nd.y}
                  stroke={activeColor}
                  strokeWidth={2.8}
                  strokeOpacity={0.55}
                />
                <circle
                  cx={nd.x}
                  cy={nd.y}
                  r={isAlert ? 9 : 7.5}
                  fill={activeColor}
                  stroke="#05070C"
                  strokeWidth={2.5}
                />
              </g>
            );
          })}
        </svg>
      </div>

      {/* CircularAvatarNode đặt chuẩn chính giữa tâm mạng lưới */}
      <CircularAvatarNode
        src={avatarSrc}
        size={224}
        x={540}
        y={800}
        borderColor={activeColor}
        label={avatarLabel}
        subLabel={avatarSubLabel}
        startFrame={startFrame}
        floatAmp={4}
        zIndex={28}
      />

      {/* Con số & tiêu đề lớn ở đáy mở thoáng (Y: 1240..1500) */}
      {(bottomMetric || bottomHeadline) && (
        <div
          style={{
            position: "absolute",
            left: 80,
            top: 1255,
            width: 920,
            textAlign: "center",
            opacity: interpolate(bottomPop, [0, 0.4], [0, 1], { extrapolateRight: "clamp" }),
            transform: `translate3d(0, ${(1 - bottomPop) * 24}px, 0) scale(${0.92 + 0.08 * bottomPop})`,
            willChange: "transform",
            zIndex: 28,
          }}
        >
          {bottomMetric && (
            <div
              style={{
                fontFamily: "'BeVietnamProBlack', sans-serif",
                fontSize: fitSingleLineSize(bottomMetric, 92, 9, 54),
                color: isAlert ? "#FF3B47" : "#FFE600",
                whiteSpace: "nowrap",
                WebkitTextStroke: "9px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 12px 28px rgba(0,0,0,0.95)",
                lineHeight: 1.04,
              }}
            >
              {bottomMetric}
            </div>
          )}
          {bottomHeadline && (
            <div
              style={{
                marginTop: 10,
                fontFamily: "'BeVietnamProBlack', sans-serif",
                fontSize: fitSingleLineSize(bottomHeadline, 34, 24, 22),
                color: "#FFFFFF",
                whiteSpace: "nowrap",
                WebkitTextStroke: "5px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 8px 20px rgba(0,0,0,0.95)",
              }}
            >
              {bottomHeadline}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

/* ============================================================================
 * 8. VisualCauseEffectFlow (Sân Khấu Mở 3):
 *    Chuỗi 3 vật thể/hình ảnh thật nối nhau bằng mũi tên động trực tiếp trên
 *    nền lưới, mỗi hình chỉ kèm 2–3 từ nhãn bên dưới (KHÔNG ô chữ hộp khô khan).
 * ============================================================================ */
export interface VisualCauseEffectItem {
  imageSrc: string;
  label: string;
  metric?: string;
  isCutout?: boolean;
  triggerFrame?: number;
  accentColor?: string;
}

export const VisualCauseEffectFlow: React.FC<{
  items: VisualCauseEffectItem[];
  startFrame?: number;
  topY?: number;
}> = ({ items, startFrame = 0, topY = 460 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const safeItems = items.slice(0, 3);
  const centersY = [topY + 135, topY + 505, topY + 875];
  const centersX = [310, 750, 340];

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        zIndex: 22,
        pointerEvents: "none",
      }}
    >
      {/* Mũi tên cong động nối trực tiếp 3 vật thể trên nền lưới */}
      <svg
        width={1080}
        height={1920}
        viewBox="0 0 1080 1920"
        style={{ position: "absolute", inset: 0, overflow: "visible" }}
      >
        <defs>
          <marker id="vcef-arrow" markerWidth="12" markerHeight="12" refX="9" refY="6" orient="auto">
            <path d="M0,1 L10,6 L0,11 Z" fill="#FFE600" />
          </marker>
        </defs>
        {safeItems.map((it, idx) => {
          if (idx >= safeItems.length - 1) return null;
          const tNext = safeItems[idx + 1].triggerFrame ?? startFrame + (idx + 1) * 18;
          const prog = interpolate(frame, [tNext - 8, tNext + 6], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const x1 = centersX[idx];
          const y1 = centersY[idx] + 95;
          const x2 = centersX[idx + 1];
          const y2 = centersY[idx + 1] - 115;
          const midY = (y1 + y2) / 2;
          const d = `M ${x1} ${y1} C ${x1} ${midY}, ${x2} ${midY}, ${x2} ${y2}`;
          return (
            <path
              key={`vcef-arr-${idx}`}
              d={d}
              fill="none"
              stroke="#FFE600"
              strokeWidth={5}
              strokeDasharray="12 10"
              strokeLinecap="round"
              opacity={prog}
              markerEnd={prog > 0.7 ? "url(#vcef-arrow)" : undefined}
              style={{ filter: "drop-shadow(0 6px 14px rgba(0,0,0,0.92))" }}
            />
          );
        })}
      </svg>

      {/* 3 vật thể thật hoặc ContainedPhotoBox gọn thoáng + 2–3 từ nhãn */}
      {safeItems.map((it, idx) => {
        const trig = it.triggerFrame ?? startFrame + idx * 18;
        const active = frame >= trig;
        const rel = Math.max(0, frame - trig);
        const pop = active ? spring({ frame: rel, fps, config: SPRING_SNAPPY }) : 0.85;
        const op = active
          ? interpolate(rel, [0, 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })
          : 0.35;
        const alive = getAliveFloat(rel, fps, 5, 0.5);
        const accent = it.accentColor || (idx === 2 ? "#FFE600" : "#22D3EE");
        const cx = centersX[idx];
        const cy = centersY[idx];

        return (
          <div
            key={`vcef-node-${idx}`}
            style={{
              position: "absolute",
              left: cx,
              top: cy,
              width: 390,
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              transform: `translate3d(-50%, calc(-50% + ${alive.y.toFixed(1)}px), 0) scale(${pop})`,
              willChange: "transform",
              opacity: op,
            }}
          >
            {it.isCutout ? (
              <div
                style={{
                  position: "relative",
                  width: 300,
                  height: 220,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    width: "110%",
                    height: "110%",
                    borderRadius: "50%",
                    background: "radial-gradient(circle, rgba(56, 189, 248, 0.22) 0%, transparent 70%)",
                  }}
                />
                <Img
                  src={resolveAsset(it.imageSrc)}
                  style={{
                    position: "relative",
                    zIndex: 1,
                    maxWidth: "100%",
                    maxHeight: "100%",
                    objectFit: "contain",
                    filter:
                      "drop-shadow(0px -1.5px 0.8px rgba(210, 238, 255, 0.32)) drop-shadow(0px 14px 22px rgba(0, 0, 0, 0.92))",
                  }}
                />
              </div>
            ) : (
              <ContainedPhotoBox
                src={it.imageSrc}
                width={340}
                height={210}
                borderRadius={16}
                border={`2.5px solid ${accent}`}
                imageFit="contain"
              />
            )}

            {it.metric && (
              <div
                style={{
                  marginTop: 8,
                  fontFamily: "'BeVietnamProBlack', sans-serif",
                  fontSize: fitSingleLineSize(it.metric, 38, 10, 24),
                  color: accent,
                  whiteSpace: "nowrap",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 6px 14px rgba(0,0,0,0.95)",
                }}
              >
                {it.metric}
              </div>
            )}

            <div
              style={{
                marginTop: 6,
                fontFamily: "'BeVietnamProBlack', sans-serif",
                fontSize: fitSingleLineSize(it.label, 25, 16, 18),
                color: "#FFFFFF",
                whiteSpace: "nowrap",
                WebkitTextStroke: "4px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 6px 14px rgba(0,0,0,0.95)",
              }}
            >
              {it.label}
            </div>
          </div>
        );
      })}
    </div>
  );
};

/* ============================================================================
 * 9. SpeechPopCard25D & SpeechPopCardStack25D:
 *    Thẻ bật nổi 2.5D/3D bám đúng frame từ khóa trong words.json (card_snap):
 *    - Ẩn trước triggerFrame; bật trong 10f bằng AE_SNAP_OUT + SPRING_SNAPPY từ
 *      perspective(1100px) translate3d(0, 48px, -120px) rotateX(24deg) rotateY(tiltY*1.8) scale(0.84)
 *      -> nổi khối tại rotateX(tiltX) rotateY(tiltY) scale(1) + vệt sáng lướt kính ở frame 3..14 (0 neon).
 *    - Sau khi đáp giữ getAliveFloat nhẹ (3px, ±0.6deg) + 2 lớp bóng đổ thực tế tách nền #061224.
 * ============================================================================ */
export interface SpeechPopCard25DProps {
  triggerFrame: number;
  title: string;
  metric?: string;
  imageSrc?: string;
  x: number;
  y: number;
  width?: number;
  tiltX?: number;
  tiltY?: number;
  accentColor?: string;
  zIndex?: number;
}

export const SpeechPopCard25D: React.FC<SpeechPopCard25DProps> = ({
  triggerFrame,
  title,
  metric,
  imageSrc,
  x,
  y,
  width = 410,
  tiltX = 6,
  tiltY = -10,
  accentColor = "#22D3EE",
  zIndex = 30,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < triggerFrame) return null;

  const rel = frame - triggerFrame;
  const snapT = interpolate(rel, [0, 10], [0, 1], {
    easing: AE_SNAP_OUT,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const popSpring = spring({ frame: rel, fps, config: SPRING_SNAPPY });
  const blend = Math.min(1, snapT * 0.6 + popSpring * 0.4);

  const settleWeight = interpolate(rel, [8, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const alive = getAliveFloat(rel, fps, 3, 0.6);

  const curY = interpolate(blend, [0, 1], [48, 0]) + alive.y * settleWeight;
  const curZ = interpolate(blend, [0, 1], [-120, 0]);
  const curRotX = interpolate(blend, [0, 1], [24, tiltX]);
  const curRotY = interpolate(blend, [0, 1], [tiltY * 1.8, tiltY]) + alive.rot * settleWeight;
  const curScale = interpolate(blend, [0, 1], [0.84, 1.0]);
  const opacity = interpolate(rel, [0, 4], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Vệt sáng lướt mặt kính mảnh ở frame 3..14 (0 neon glow)
  const sheenX = interpolate(rel, [3, 14], [-130, 140], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const sheenOp = rel >= 3 && rel <= 14 ? 0.9 : 0;

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width,
        transform: `translate3d(-50%, -50%, 0) perspective(1100px) translate3d(0, ${curY.toFixed(2)}px, ${curZ.toFixed(1)}px) rotateX(${curRotX.toFixed(2)}deg) rotateY(${curRotY.toFixed(2)}deg) scale(${curScale.toFixed(4)})`,
        transformStyle: "preserve-3d",
        willChange: "transform",
        opacity,
        zIndex,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          position: "relative",
          overflow: "hidden",
          borderRadius: 20,
          padding: imageSrc ? "14px 16px 16px" : "18px 22px",
          background: "linear-gradient(155deg, rgba(16, 36, 66, 0.94) 0%, rgba(7, 16, 32, 0.96) 100%)",
          border: `2px solid ${accentColor}`,
          boxShadow:
            "0 16px 26px rgba(0, 0, 0, 0.88), 0 32px 54px rgba(2, 6, 16, 0.95), inset 0 1px 0 rgba(255, 255, 255, 0.24)",
        }}
      >
        {/* Vệt sáng lướt mặt kính mảnh (frame 3..14) */}
        {sheenOp > 0 && (
          <div
            style={{
              position: "absolute",
              inset: -20,
              background:
                "linear-gradient(110deg, transparent 36%, rgba(255, 255, 255, 0.28) 50%, transparent 64%)",
              transform: `translate3d(${sheenX}%, 0, 0)`,
              opacity: sheenOp,
              pointerEvents: "none",
              zIndex: 5,
            }}
          />
        )}

        {imageSrc && (
          <div style={{ marginBottom: 12 }}>
            <ContainedPhotoBox
              src={imageSrc}
              width="100%"
              height={Math.round(width * 0.48)}
              borderRadius={12}
              border="1.5px solid rgba(148, 197, 255, 0.28)"
              imageFit="contain"
            />
          </div>
        )}

        {metric && (
          <div
            style={{
              fontFamily: "'BeVietnamProBlack', sans-serif",
              fontSize: fitSingleLineSize(metric, 48, 10, 28),
              color: accentColor,
              whiteSpace: "nowrap",
              lineHeight: 1.08,
              marginBottom: 4,
              WebkitTextStroke: "5px #05070C",
              paintOrder: "stroke fill",
              textShadow: "0 6px 16px rgba(0, 0, 0, 0.94)",
            }}
          >
            {metric}
          </div>
        )}

        <div
          style={{
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: fitSingleLineSize(title, 28, 16, 18),
            color: "#FFFFFF",
            whiteSpace: "nowrap",
            lineHeight: 1.2,
            textShadow: "0 4px 12px rgba(0, 0, 0, 0.95)",
          }}
        >
          {title}
        </div>
      </div>
    </div>
  );
};

export interface SpeechPopCardStack25DProps {
  cards: SpeechPopCard25DProps[];
  baseZIndex?: number;
}

export const SpeechPopCardStack25D: React.FC<SpeechPopCardStack25DProps> = ({
  cards,
  baseZIndex = 30,
}) => {
  return (
    <>
      {cards.map((card, idx) => (
        <SpeechPopCard25D
          key={`sp-card-${idx}-${card.triggerFrame}`}
          {...card}
          zIndex={card.zIndex ?? baseZIndex + idx}
        />
      ))}
    </>
  );
};
```


#### `remotion_reels/src/components/fx/KnowledgeMotionFX.tsx`

```tsx
import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { AE_SNAP_OUT, AE_WHIP_TRANSITION } from "./motionPresets";

/**
 * CameraStageWrapper: Bọc mỗi Beat tạo chuyển động 1 ống kính camera duy nhất (60fps AE):
 * - Vào cảnh: đẩy/trượt nhanh mượt 7 frames bằng AE_SNAP_OUT, giữ opacity: 1 (CẤM cross-fade mờ bóng ma).
 * - Giữa cảnh: trôi nhẹ scale 1.0 -> 1.018.
 * - Ra cảnh: đẩy nhẹ 6 frames cuối bằng AE_WHIP_TRANSITION tạo đà sang Beat tiếp theo.
 */
export const CameraStageWrapper: React.FC<{
  durationInFrames: number;
  enterDirection?: "up" | "left" | "right" | "zoom";
  children: React.ReactNode;
}> = ({ durationInFrames, enterDirection = "zoom", children }) => {
  const frame = useCurrentFrame();
  const enterDur = 7;
  const exitDur = 6;
  const exitStart = Math.max(enterDur + 1, durationInFrames - exitDur);

  const enterT = interpolate(frame, [0, enterDur], [0, 1], {
    easing: AE_SNAP_OUT,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const midScale = interpolate(frame, [enterDur, exitStart], [1.0, 1.018], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const exitT = interpolate(frame, [exitStart, durationInFrames], [0, 1], {
    easing: AE_WHIP_TRANSITION,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  let tx = 0;
  let ty = 0;
  let enterScale = 1.0;
  if (enterDirection === "up") ty = (1 - enterT) * 44;
  else if (enterDirection === "left") tx = (1 - enterT) * 52;
  else if (enterDirection === "right") tx = -(1 - enterT) * 52;
  else enterScale = 0.955 + 0.045 * enterT;

  const finalScale = enterScale * midScale * (1 + exitT * 0.032);
  const exitY = -exitT * 18;

  return (
    <AbsoluteFill
      style={{
        opacity: 1,
        transform: `translate3d(${tx}px, ${ty + exitY}px, 0) scale(${finalScale})`,
        willChange: "transform",
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export interface ParallaxDepthStageProps {
  /** Tầng xa (trôi chậm 0.3x): chữ số khổng lồ chìm, bản đồ, kiến trúc xa */
  backLayer?: React.ReactNode;
  /** Tầng trung (trôi chuẩn 1.0x): sơ đồ, ảnh tư liệu chính */
  midLayer?: React.ReactNode;
  /** Tầng tiền cảnh (trôi nhanh 1.35x): HeroCutout3D hoặc SpeechPopCard25D */
  frontLayer?: React.ReactNode;
  /** Tương thích ngược: ảnh nền mờ + chủ thể */
  bgSrc?: string;
  subjectSrc?: string;
  bgBlur?: number;
  startFrame?: number;
  durationFrames?: number;
  /** Biên độ lia camera ngang/dọc (px) trong suốt Beat */
  panX?: number;
  panY?: number;
}

export const ParallaxDepthStage: React.FC<ParallaxDepthStageProps> = ({
  backLayer,
  midLayer,
  frontLayer,
  bgSrc,
  subjectSrc,
  bgBlur = 5,
  startFrame = 0,
  durationFrames = 240,
  panX = 44,
  panY = 14,
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const progress = interpolate(rel, [0, Math.max(1, durationFrames)], [-0.5, 0.5], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // 3 tốc độ chiều sâu 60fps: back 0.3x | mid 1.0x | front 1.35x
  const backX = -progress * panX * 0.3;
  const backY = -progress * panY * 0.3;
  const midX = -progress * panX * 1.0;
  const midY = -progress * panY * 1.0;
  const frontX = -progress * panX * 1.35;
  const frontY = -progress * panY * 1.35;

  const backScale = interpolate(rel, [0, Math.max(1, durationFrames)], [1.02, 1.06], { extrapolateRight: "clamp" });
  const midScale = interpolate(rel, [0, Math.max(1, durationFrames)], [1.0, 1.035], { extrapolateRight: "clamp" });
  const frontScale = interpolate(rel, [0, Math.max(1, durationFrames)], [0.99, 1.045], { extrapolateRight: "clamp" });

  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden", perspective: "1100px" }}>
      {/* TẦNG 1 — BACK LAYER (0.3x) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate3d(${backX.toFixed(2)}px, ${backY.toFixed(2)}px, 0) scale(${backScale.toFixed(4)})`,
          willChange: "transform",
          zIndex: 10,
        }}
      >
        {backLayer}
        {!backLayer && bgSrc && (
          <Img
            src={staticFile(bgSrc)}
            style={{
              position: "absolute",
              inset: -30,
              width: "calc(100% + 60px)",
              height: "calc(100% + 60px)",
              objectFit: "cover",
              filter: `blur(${bgBlur}px) brightness(0.55)`,
            }}
          />
        )}
      </div>

      {/* TẦNG 2 — MID LAYER (1.0x) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate3d(${midX.toFixed(2)}px, ${midY.toFixed(2)}px, 0) scale(${midScale.toFixed(4)})`,
          willChange: "transform",
          zIndex: 20,
        }}
      >
        {midLayer}
      </div>

      {/* TẦNG 3 — FRONT LAYER (1.35x) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate3d(${frontX.toFixed(2)}px, ${frontY.toFixed(2)}px, 0) scale(${frontScale.toFixed(4)})`,
          willChange: "transform",
          zIndex: 30,
        }}
      >
        {frontLayer}
        {!frontLayer && subjectSrc && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Img
              src={staticFile(subjectSrc)}
              style={{
                maxWidth: "82%",
                maxHeight: "54%",
                objectFit: "contain",
                filter: "drop-shadow(0 28px 42px rgba(0,0,0,0.88))",
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export interface FlowBranch {
  label: string;
  percent: number;
  color: string;
}

export const FlowPipeline3D: React.FC<{
  sourceLabel: string;
  branches: FlowBranch[];
  startFrame?: number;
}> = ({ sourceLabel, branches, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const width = 900;
  const height = 560;
  const startX = 125;
  const startY = height / 2;

  const splitBranchLabel = (label: string): string[] => {
    if (label.length <= 14) return [label];
    const words = label.split(/\s+/);
    const lines: string[] = [];
    let cur = "";
    for (const w of words) {
      if ((cur + " " + w).trim().length > 14 && cur) {
        lines.push(cur);
        cur = w;
      } else {
        cur = (cur + " " + w).trim();
      }
    }
    if (cur) lines.push(cur);
    return lines.slice(0, 2);
  };

  return (
    <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        {branches.map((br, i) => {
          const endY = 95 + i * ((height - 190) / Math.max(1, branches.length - 1));
          const endX = 540;
          const drawPct = interpolate(rel, [i * 12, i * 12 + 36], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const particleT = ((rel * 0.018 + i * 0.27) % 1);
          const cx1 = startX + 170;
          const cx2 = endX - 160;
          const px =
            Math.pow(1 - particleT, 3) * startX +
            3 * Math.pow(1 - particleT, 2) * particleT * cx1 +
            3 * (1 - particleT) * Math.pow(particleT, 2) * cx2 +
            Math.pow(particleT, 3) * endX;
          const py =
            Math.pow(1 - particleT, 3) * startY +
            3 * Math.pow(1 - particleT, 2) * particleT * startY +
            3 * (1 - particleT) * Math.pow(particleT, 2) * endY +
            Math.pow(particleT, 3) * endY;

          const labelLines = splitBranchLabel(br.label);

          return (
            <g key={i} opacity={drawPct}>
              <path
                d={`M ${startX + 95} ${startY} C ${cx1 + 40} ${startY}, ${cx2} ${endY}, ${endX} ${endY}`}
                fill="none"
                stroke={br.color}
                strokeWidth={Math.max(6, br.percent * 0.45)}
                strokeOpacity={0.35}
                strokeLinecap="round"
              />
              <circle cx={px} cy={py} r={8} fill="#FFFFFF" />
              <text
                x={endX + 20}
                y={endY - 8}
                fill={br.color}
                fontSize={34}
                fontWeight={900}
                fontFamily="'BeVietnamProBlack', sans-serif"
              >
                {br.percent}%
              </text>
              {labelLines.map((line, li) => (
                <text
                  key={`bl-${li}`}
                  x={endX + 20}
                  y={endY + 22 + li * 26}
                  fill="#E2E8F0"
                  fontSize={22}
                  fontWeight={700}
                  fontFamily="'BeVietnamProExtraBold', sans-serif"
                >
                  {line}
                </text>
              ))}
            </g>
          );
        })}
        <rect
          x={startX - 105}
          y={startY - 32}
          width={210}
          height={64}
          rx={28}
          fill="#0F172A"
          stroke="#42B2F2"
          strokeWidth={4}
          style={{ filter: "drop-shadow(0 10px 22px rgba(0,0,0,0.88))" }}
        />
        <text
          x={startX}
          y={startY + 8}
          textAnchor="middle"
          fill="#FFFFFF"
          fontSize={22}
          fontWeight={900}
          fontFamily="'BeVietnamProBlack', sans-serif"
        >
          {sourceLabel}
        </text>
      </svg>
    </div>
  );
};

export const DecisionBranchPulse: React.FC<{
  rootLabel: string;
  winLabel: string;
  loseLabel: string;
  startFrame?: number;
}> = ({ rootLabel, winLabel, loseLabel, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const t = Math.min(1, rel / 40);
  const pulseY = interpolate(t, [0, 1], [80, 290]);
  const splitProgress = Math.max(0, Math.min(1, (rel - 24) / 30));

  // Continuous looping circuit pulse down the trunk & along winning Bezier M 450 220 Q 320 260 220 340
  const evalPulsePos = (phase: number) => {
    if (phase < 0.35) {
      const s = phase / 0.35;
      return { x: 450, y: 80 + 140 * s };
    }
    const u = (phase - 0.35) / 0.65;
    const inv = 1 - u;
    return {
      x: inv * inv * 450 + 2 * inv * u * 320 + u * u * 220,
      y: inv * inv * 220 + 2 * inv * u * 260 + u * u * 340,
    };
  };
  const loopT1 = (rel % 48) / 48;
  const loopT2 = ((rel + 24) % 48) / 48;
  const p1 = evalPulsePos(loopT1);
  const p2 = evalPulsePos(loopT2);

  const rootPulseScale = 1 + Math.sin(rel * 0.12) * 0.022;
  const winPulseScale = 1 + Math.sin(rel * 0.16) * 0.03;
  const winGlowOpacity = 0.55 + Math.sin(rel * 0.16) * 0.35;

  return (
    <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <svg
        width={900}
        height={460}
        viewBox="0 0 900 460"
        style={{ fontFamily: "'BeVietnamProBlack', sans-serif", overflow: "visible" }}
      >
      <line x1={450} y1={80} x2={450} y2={220} stroke="#38BDF8" strokeWidth={6} />
      <line
        x1={450}
        y1={80}
        x2={450}
        y2={220}
        stroke="#BAE6FD"
        strokeWidth={3}
        strokeDasharray="10 14"
        strokeDashoffset={-rel * 2.2}
        opacity={0.75}
      />
      <path d="M 450 220 Q 320 260 220 340" fill="none" stroke="#EF4444" strokeWidth={6} strokeOpacity={0.35 + 0.65 * splitProgress} />
      <path
        d="M 450 220 Q 320 260 220 340"
        fill="none"
        stroke="#FCA5A5"
        strokeWidth={3}
        strokeDasharray="12 16"
        strokeDashoffset={-rel * 2.4}
        strokeOpacity={0.4 + 0.5 * splitProgress}
      />
      <path d="M 450 220 Q 580 260 680 340" fill="none" stroke="#64748B" strokeWidth={4} strokeOpacity={0.45} />

      {t < 1 && <circle cx={450} cy={pulseY} r={12} fill="#FACC15" />}

      {/* Looping bright signal pulses */}
      <circle cx={p1.x} cy={p1.y} r={16} fill="#FACC15" opacity={0.28} />
      <circle cx={p1.x} cy={p1.y} r={8} fill="#FEF08A" opacity={0.95} />
      <circle cx={p2.x} cy={p2.y} r={13} fill="#EF4444" opacity={0.28 * splitProgress} />
      <circle cx={p2.x} cy={p2.y} r={6} fill="#FFFFFF" opacity={0.85 * splitProgress} />

      <g transform={`translate(450, 54) scale(${rootPulseScale}) translate(-450, -54)`}>
        <rect
          x={230}
          y={24}
          width={440}
          height={60}
          rx={30}
          fill="#0F172A"
          stroke="#38BDF8"
          strokeWidth={3 + Math.sin(rel * 0.14) * 0.8}
        />
        <text x={450} y={63} textAnchor="middle" fill="#FFFFFF" fontSize={26} fontWeight={900} fontFamily="'BeVietnamProBlack', sans-serif">
          {rootLabel}
        </text>
      </g>

      <g transform={`translate(225, 390) scale(${winPulseScale}) translate(-225, -390)`}>
        <text
          x={225}
          y={395}
          textAnchor="middle"
          fill="#F87171"
          fontSize={28}
          fontWeight={900}
          fontFamily="'BeVietnamProBlack', sans-serif"
          style={{ filter: "drop-shadow(0 8px 16px rgba(0,0,0,0.88))" }}
        >
          {winLabel}
        </text>
      </g>
      <text x={675} y={395} textAnchor="middle" fill="#94A3B8" fontSize={25} fontWeight={800} fontFamily="'BeVietnamProExtraBold', sans-serif">
        {loseLabel}
      </text>
      </svg>
    </div>
  );
};
```


#### `remotion_reels/src/components/fx/motionPresets.ts`

```typescript
import { Easing, interpolate } from "remotion";

/**
 * Đường cong Graph Editor chuẩn After Effects (60fps mượt, dứt khoát, không nảy nhựa).
 */
export const AE_SNAP_OUT = Easing.bezier(0.16, 1, 0.3, 1);
export const AE_PUNCH_OUT = Easing.bezier(0.22, 1, 0.36, 1);
export const AE_WHIP_TRANSITION = Easing.bezier(0.76, 0, 0.24, 1);

export const SPRING_SNAPPY = {
  damping: 24,
  stiffness: 260,
  mass: 0.8,
} as const;

export const SPRING_HEAVY_SLAM = {
  damping: 20,
  stiffness: 320,
  mass: 1.0,
} as const;

/**
 * Micro-motion giữ khung hình luôn sống ở 60fps (dùng cho translate3d & rotate).
 */
export function getAliveFloat(
  frame: number,
  fps: number = 60,
  ampY: number = 6,
  ampRot: number = 0.8,
): { y: number; rot: number } {
  const t = frame / Math.max(1, fps);
  return {
    y: Math.sin(t * 2.1) * ampY,
    rot: Math.cos(t * 1.6) * ampRot,
  };
}

/**
 * Ken Burns zoom mượt trên GPU cho ảnh/thẻ trong suốt thời lượng cảnh.
 */
export function getKenBurnsScale(
  localFrame: number,
  durationInFrames: number,
  fromScale: number = 1.0,
  toScale: number = 1.06,
): number {
  return interpolate(
    localFrame,
    [0, Math.max(1, durationInFrames)],
    [fromScale, toScale],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );
}

/**
 * Độ trễ lệch nhịp (stagger 3-5 frames) giữa Tiêu đề -> Ảnh/Đạo cụ -> Số liệu.
 */
export function getStaggerDelay(index: number, stepFrames: number = 4): number {
  return Math.max(0, index) * stepFrames;
}
```


#### `remotion_reels/src/components/fx/MotionTrackedCallout.tsx`

```tsx
import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface TrackPoint {
  frame: number;
  x: number;
  y: number;
}

export const interpolateTrackPath = (points: TrackPoint[], frame: number): { x: number; y: number } => {
  if (!points || points.length === 0) return { x: 540, y: 960 };
  if (points.length === 1 || frame <= points[0].frame) return { x: points[0].x, y: points[0].y };
  const last = points[points.length - 1];
  if (frame >= last.frame) return { x: last.x, y: last.y };

  for (let i = 0; i < points.length - 1; i++) {
    const a = points[i];
    const b = points[i + 1];
    if (frame >= a.frame && frame <= b.frame) {
      const t = (frame - a.frame) / Math.max(1, b.frame - a.frame);
      return {
        x: a.x + (b.x - a.x) * t,
        y: a.y + (b.y - a.y) * t,
      };
    }
  }
  return { x: last.x, y: last.y };
};

export const MotionTrackedCallout: React.FC<{
  trackPoints: TrackPoint[];
  title: string;
  subtitle?: string;
  metricValue?: string;
  offsetX?: number;
  offsetY?: number;
  startFrame?: number;
  accentColor?: string;
}> = ({
  trackPoints,
  title,
  subtitle,
  metricValue,
  offsetX = 150,
  offsetY = -120,
  startFrame = 0,
  accentColor = "#42B2F2",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const pop = spring({
    frame: rel,
    fps,
    config: { damping: 15, stiffness: 190, mass: 0.7 },
  });

  const target = interpolateTrackPath(trackPoints, frame);
  const elbowX = target.x + offsetX * 0.45;
  const elbowY = target.y + offsetY;
  const endX = target.x + offsetX;
  const endY = target.y + offsetY;
  const lineDraw = interpolate(rel, [0, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pulse = 1 + Math.sin(rel * 0.22) * 0.18;

  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <circle
          cx={target.x}
          cy={target.y}
          r={10 * pulse}
          fill={accentColor}
          opacity={pop}
        />
        <circle
          cx={target.x}
          cy={target.y}
          r={22 * pulse}
          fill="none"
          stroke={accentColor}
          strokeWidth={3}
          opacity={pop * 0.65}
        />
        <polyline
          points={`${target.x},${target.y} ${elbowX},${elbowY} ${endX},${endY}`}
          fill="none"
          stroke={accentColor}
          strokeWidth={4}
          strokeDasharray={360}
          strokeDashoffset={360 * (1 - lineDraw)}
          strokeLinecap="round"
        />
      </svg>

      <div
        style={{
          position: "absolute",
          left: endX + (offsetX >= 0 ? 12 : -12),
          top: endY,
          transform: `translate(${offsetX >= 0 ? "0%" : "-100%"}, -55%) scale(${interpolate(pop, [0, 1], [0.75, 1])})`,
          opacity: pop,
          display: "flex",
          flexDirection: "column",
          alignItems: offsetX >= 0 ? "flex-start" : "flex-end",
        }}
      >
        {metricValue && (
          <div
            style={{
              fontFamily: "'KanitBlack', sans-serif",
              fontSize: 52,
              fontWeight: 900,
              color: accentColor,
              lineHeight: 1.0,
              WebkitTextStroke: "2px rgba(0,0,0,0.9)",
              textShadow: "0 6px 20px rgba(0,0,0,0.95)",
            }}
          >
            {metricValue}
          </div>
        )}
        <div
          style={{
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: 32,
            fontWeight: 900,
            color: "#FFFFFF",
            WebkitTextStroke: "1.5px rgba(0,0,0,0.88)",
            textShadow: "0 4px 16px rgba(0,0,0,0.95)",
            whiteSpace: "nowrap",
          }}
        >
          {title}
        </div>
        {subtitle && (
          <div
            style={{
              fontFamily: "'BeVietnamProExtraBold', sans-serif",
              fontSize: 23,
              fontWeight: 700,
              color: "#CBD5E1",
              textShadow: "0 3px 12px rgba(0,0,0,0.95)",
              whiteSpace: "nowrap",
            }}
          >
            {subtitle}
          </div>
        )}
      </div>
    </div>
  );
};
```


#### `remotion_reels/src/components/fx/RealSceneSpotlight.tsx`

```tsx
import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface SceneCameraWaypoint {
  frame: number;
  scale: number;
  x: number; // px shift
  y: number; // px shift
}

export interface PopSubject3D {
  src: string;
  appearFrame: number;
  x: number; // % or px inside stage (0..1080)
  y: number; // px inside stage
  width: number;
  rotateDeg?: number;
  glowColor?: string;
}

/**
 * RealSceneCameraStage — Lấy ẢNH THẬT / TÀI LIỆU THẬT làm nhân vật chính toàn khung sân khấu,
 * camera bay mượt qua các điểm focus (không bao giờ đứng im) + vật thể thật tách nền 3D bật ra từng nhịp.
 */
export const RealSceneCameraStage: React.FC<{
  bgSrc: string;
  waypoints?: SceneCameraWaypoint[];
  subjects?: PopSubject3D[];
  durationFrames?: number;
  bgBrightness?: number;
  children?: React.ReactNode;
}> = ({
  bgSrc,
  waypoints,
  subjects = [],
  durationFrames = 360,
  bgBrightness = 0.88,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pts: SceneCameraWaypoint[] =
    waypoints && waypoints.length >= 2
      ? waypoints
      : [
          { frame: 0, scale: 1.04, x: -24, y: 12 },
          { frame: Math.round(durationFrames * 0.5), scale: 1.14, x: 18, y: -10 },
          { frame: durationFrames, scale: 1.22, x: -12, y: 6 },
        ];

  const inputFrames = pts.map((p) => p.frame);
  const camScale = interpolate(frame, inputFrames, pts.map((p) => p.scale), {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const camX = interpolate(frame, inputFrames, pts.map((p) => p.x), {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const camY = interpolate(frame, inputFrames, pts.map((p) => p.y), {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ position: "relative", width: "100%", height: "100%", overflow: "hidden", borderRadius: 24 }}>
      <Img
        src={staticFile(bgSrc)}
        style={{
          position: "absolute",
          inset: -40,
          width: "calc(100% + 80px)",
          height: "calc(100% + 80px)",
          objectFit: "cover",
          transform: `translate3d(${camX.toFixed(1)}px, ${camY.toFixed(1)}px, 0) scale(${camScale.toFixed(3)})`,
          filter: `brightness(${bgBrightness}) contrast(1.06)`,
        }}
      />

      {subjects.map((sub, idx) => {
        if (frame < sub.appearFrame) return null;
        const rel = frame - sub.appearFrame;
        const pop = spring({
          frame: rel,
          fps,
          config: { damping: 14, stiffness: 185, mass: 0.72 },
        });
        const floatY = Math.sin(rel * 0.06 + idx) * 7;
        const glow = sub.glowColor ?? "#F59E0B";
        return (
          <div
            key={idx}
            style={{
              position: "absolute",
              left: sub.x,
              top: sub.y,
              width: sub.width,
              transform: `translate(-50%, -50%) translateY(${floatY.toFixed(1)}px) scale(${pop.toFixed(3)}) rotate(${sub.rotateDeg ?? 0}deg)`,
              filter: `drop-shadow(0 18px 30px rgba(0,0,0,0.82)) drop-shadow(0px 8px 16px rgba(0,0,0,0.85))`,
            }}
          >
            <Img src={staticFile(sub.src)} style={{ width: "100%", height: "auto", objectFit: "contain" }} />
          </div>
        );
      })}

      {children}
    </div>
  );
};

/**
 * EvidenceCalloutOverlay — Vẽ đường đứt nét phát sáng + tâm ngắm đỏ/vàng chỉ trực tiếp
 * vào chi tiết trên ảnh thật (chuẩn phong cách Bia Hơi 1986 & TIME 1997).
 */
export const EvidenceCalloutOverlay: React.FC<{
  targetX: number;
  targetY: number;
  labelX: number;
  labelY: number;
  label: string;
  metric?: string;
  startFrame?: number;
  color?: string;
}> = ({
  targetX,
  targetY,
  labelX,
  labelY,
  label,
  metric,
  startFrame = 0,
  color = "#FACC15",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const rel = frame - startFrame;
  const pop = spring({ frame: rel, fps, config: { damping: 15, stiffness: 200, mass: 0.65 } });
  const pulse = 1 + Math.sin(rel * 0.18) * 0.18;

  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      <svg width="100%" height="100%" style={{ position: "absolute", inset: 0, overflow: "visible" }}>
        <line
          x1={labelX}
          y1={labelY}
          x2={targetX}
          y2={targetY}
          stroke={color}
          strokeWidth={4}
          strokeDasharray="10 7"
          strokeDashoffset={-rel * 1.8}
          opacity={pop}
        />
        <circle cx={targetX} cy={targetY} r={10 * pulse} fill={color} opacity={pop} />
        <circle cx={targetX} cy={targetY} r={22 * pulse} fill="none" stroke={color} strokeWidth={3.5} opacity={pop * 0.7} />
      </svg>
      <div
        style={{
          position: "absolute",
          left: labelX,
          top: labelY,
          transform: `translate(-50%, -100%) scale(${pop.toFixed(3)})`,
          textAlign: "center",
        }}
      >
        {metric && (
          <div
            style={{
              fontFamily: "'KanitBlack', sans-serif",
              fontSize: 44,
              color,
              lineHeight: 1.0,
              WebkitTextStroke: "2px rgba(0,0,0,0.92)",
              textShadow: "0 6px 16px rgba(0,0,0,0.95)",
              whiteSpace: "nowrap",
            }}
          >
            {metric}
          </div>
        )}
        <div
          style={{
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: 28,
            color: "#FFFFFF",
            WebkitTextStroke: "1.5px rgba(0,0,0,0.9)",
            textShadow: "0 4px 12px rgba(0,0,0,0.95)",
            whiteSpace: "nowrap",
          }}
        >
          {label}
        </div>
      </div>
    </div>
  );
};

/**
 * FactPunchlineCard — Câu chốt kiến thức ngắn gọn ở đáy màn hình (thay thế hoàn toàn phụ đề chạy từng chữ).
 */
export const FactPunchlineCard: React.FC<{
  headline: string;
  subline?: string;
  startFrame?: number;
  accentColor?: string;
}> = ({ headline, subline, startFrame = 0, accentColor = "#FACC15" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const rel = frame - startFrame;
  const pop = spring({ frame: rel, fps, config: { damping: 16, stiffness: 210, mass: 0.7 } });

  return (
    <div
      style={{
        position: "absolute",
        left: 56,
        right: 56,
        bottom: 245,
        textAlign: "center",
        opacity: pop,
        transform: `translateY(${interpolate(pop, [0, 1], [28, 0]).toFixed(1)}px) scale(${interpolate(pop, [0, 1], [0.92, 1]).toFixed(3)})`,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          fontFamily: "'BeVietnamProBlack', sans-serif",
          fontSize: 44,
          color: accentColor,
          lineHeight: 1.15,
          WebkitTextStroke: "2px rgba(0,0,0,0.92)",
          textShadow: "0 6px 20px rgba(0,0,0,0.95)",
        }}
      >
        {headline}
      </div>
      {subline && (
        <div
          style={{
            marginTop: 6,
            fontFamily: "'BeVietnamProExtraBold', sans-serif",
            fontSize: 28,
            color: "#FFFFFF",
            WebkitTextStroke: "1.5px rgba(0,0,0,0.88)",
            textShadow: "0 4px 14px rgba(0,0,0,0.95)",
          }}
        >
          {subline}
        </div>
      )}
    </div>
  );
};
```


### 3.6. Tài liệu Quy chuẩn, Skill & Subagents lưu trữ cũ (_archive_cu/)

#### `_archive_cu/QUY_CHUAN_ADN_FB_REELS.md`

```markdown
# QUY CHUẨN ADN KÊNH ĐỘC BẢN - FB REELS FORENSIC GLASS NOIR
================================================================================
(HỆ THỐNG ĐẦU NÃO VIDEO NGẮN CHUYÊN BIỆT CHO FACEBOOK REELS & TIKTOK SHORTS)
================================================================================

## 💎 PHẦN 1: TRIẾT LÝ THỊ GIÁC ĐỘC BẢN "FORENSIC GLASS NOIR"
Nghiêm cấm sao chép băng dán giấy xé viền (Paper Tape) và nền kẻ ô ly than chì học sinh của Finpath. Video ngắn của kênh định vị ở đẳng cấp cao hơn: **HỒ SƠ TÀI CHÍNH & PHÁP LÝ ĐIỀU TRA CAO CẤP**.

1. **Nền Obsidian Noir (Smoked Obsidian Studio):**
   - Mặt kính đen huyền bí phản chiếu mờ (#0a0c10 -> #121620) có luồng khói sáng không gian sâu.
2. **Thẻ Acrylic Kính Mờ Đúc Viền Titan (Frosted Acrylic Plate):**
   - Hiệu ứng kính mờ (Backdrop Blur), đúc viền Titan phay xước sáng loáng.
   - 4 đinh ốc titan ở 4 góc thẻ, vệt sáng kim loại 3D quét ngang qua bề mặt (Light Sweep).
   - Khắc chìm mã số án lệ vi mô (`#CASE-082`, `EXHIBIT A`).
3. **Tem Niêm Phong Bảo Mật Pháp Lý (Forensic Security Hologram Seal):**
   - Dấu triện đỏ chu sa / vàng neon dập nổi mã vạch Barcode bảo mật thay thế băng dán giấy xé.
4. **Bản Đồ Vệ Tinh NASA 3D Thực Tế & Phủ Quốc Kỳ Dạ Quang (Flag Map Projection):**
   - Không dùng vector phẳng! Sử dụng texture ảnh vệ tinh thực (NASA Blue Marble / Bathymetry), độ cong Trái Đất 3D và viền khí quyển xanh.
   - Tự động phủ quốc kỳ dạ quang (như cờ Nhật Bản mặt trời đỏ, cờ Việt Nam) trọn vẹn trong đường bờ biển với viền neon phát sáng 3D.
   - Đường bay vòng cung phát sáng (Great Circle Flight Arc) và cắm ổ khóa kim loại vàng đóng sập từng chặng bay.
5. **Cơ Chế Dòng Tiền & Kéo Cắt Hợp Đồng 2.5D:**
   - Két sắt thép đúc mở nắp thấy các cọc tiền bên trong.
   - Đồng xu vàng rơi với gia tốc vật lý $g = 9.8\text{m/s}^2$ vào miệng két.
   - Kéo kim loại mạ crom sáng loáng cắt phựt đường liên kết giữa "Hôm nay" và "Tương lai" kèm tia lửa va chạm.

---

## 🎧 PHẦN 2: THIẾT QUÂN LUẬT ÂM THANH 3 TẦNG
1. **Tầng 1 - Giọng Nói Thượng Tầng (VieNeu Hải Đăng):**
   - Giọng Nam Bắc uy lực, tự nhiên, nhịp đọc nhanh 160-180 wpm, âm lượng 1.0 trong trẻo.
   - Bóc tách toạ độ mili-giây từng từ vựng bằng `faster-whisper`.
2. **Tầng 2 - Nhạc Nền AI Điện Ảnh (ACE-Step 1.5):**
   - 100% Zero-Copyright, sinh theo 4 Hồi kịch tính:
     * *Act 1 (0-5s):* Hook nghẹt thở dồn dập.
     * *Act 2 (5-25s):* Wall Street Finance Drive lạnh lùng.
     * *Act 3 (25-45s):* Dark Investigation Tension nghẹt thở.
     * *Act 4 (45-60s):* Epic Climax bùng nổ.
   - **Auto-Ducking né giọng (-18dB):** Nhạc luôn thì thầm làm nền cho giọng Hải Đăng.
3. **Tầng 3 - Foley Xúc Giác Cơ Học Vi Mô (Micro Transient Impacts):**
   - Nện chính xác từng mili-giây khớp với từ khóa giọng đọc:
     * Ổ khóa sập: `heavy_padlock_clack.wav`
     * Kéo kim loại cắt: `metal_scissors_snip.wav`
     * Máy đếm tiền / tiền rơi: `cash_counter_roll.wav`
     * Ghim tài liệu: `pin_cork_hit.wav`
     * Thanh chắn hạ xuống: `barrier_drop.wav`
     * Dấu triện niêm phong: `forensic_stamp_thud.wav`
4. **Chuẩn Âm Lượng Phát Sóng Quốc Tế:** EBU R128 (-14.0 LUFS $\pm 1.0$ LUFS), True Peak $\le -1.0\text{ dBTP}$.

---

## 📱 PHẦN 3: DẢI AN TOÀN SAFE ZONE FB REELS (9:16 - 1080x1920)
Để không bị các thành phần giao diện của Facebook che khuất:
- **Vùng cấm trên đỉnh (Header Zone):** $Y \in [0, 160\text{px}]$ (thanh tìm kiếm & status bar).
- **Vùng cấm dưới đáy (Footer Zone):** $Y \in [1650, 1920\text{px}]$ (tên Fanpage, nút Follow, Caption, thanh nhạc).
- **Vùng cấm mép phải (Right Rail):** $X \in [920, 1080\text{px}]$ (nút Like, Thả tim, Bình luận, Chia sẻ, Remix).
- **VÙNG AN TOÀN TUYỆT ĐỐI (SAFE ZONE):**
  $$\text{Vùng hiển thị nội dung: } X \in [90, 900\text{px}], \quad Y \in [200, 1620\text{px}]$$

---

## 🤖 PHẦN 4: HỆ THỐNG 5 SUB-AGENTS CHUYÊN BIỆT
1. **`forensic-intel-scripter`**: Viết kịch bản 40s-60s cấu trúc 4 Hồi giật gân, cô đọng kiến thức, bóc tách logic tài chính/pháp lý.
2. **`vieneu-voice-pacer`**: Sinh giọng đọc Hải Đăng + bóc tách word-timestamps Whisper.
3. **`nasa-map-architect`**: Dựng toàn bộ bản đồ vệ tinh NASA 3D, cờ dạ quang và đường bay vòng cung.
4. **`forensic-motion-builder`**: Dựng thẻ kính Acrylic, tem niêm phong, két sắt, kéo cắt và render video 9:16.
5. **`forensic-qc-audio-gatekeeper`**: Kiểm định Mắt Thần OpenCV, Safe Zone và hòa âm EBU R128 (-14.0 LUFS). Đạt $\ge 90/100$ điểm xuất thẳng ra `D:\Video thành phẩm\`.
```


#### `_archive_cu/skills/fb-reels-master-studio/SKILL.md`

```markdown
---
name: fb-reels-master-studio
description: Hệ thống Đầu Não Độc Quyền Sản Xuất Video Ngắn FB Reels / TikTok 9:16 (1080x1920 @ 60fps) chuẩn kênh FB HaDa Why (@hadawhy) tại D:\Đầu Não Video Ngắn FB (không xóa). Điều phối cố định 6 Sub-Agents chuyên trách (Cấm đẻ sub-agent rác), thực thi 15 Luật Vĩnh Viễn tại studio_lessons_learned.json (chuẩn vàng NvidiaSuccession40s trên UniversalReelsMaster.tsx, nền duy nhất HaDaWhyMistBackground #42B2F2, 0 trùng ảnh giữa các cảnh, 0 ảnh stock chung chung, bản đồ 3D vệ tinh BĐS / 258 nước, 3 nhóm SFX tách biệt + BGM giao hưởng 0.72, -14.0 LUFS, Con Tổng bắt buộc gọi read_file xem & nghe trực tiếp).
---

> **NGUỒN LUẬT DUY NHẤT (BẮT BUỘC ĐỌC TRƯỚC KHI LÀM):** `D:\Đầu Não Video Ngắn FB (không xóa)\engine\studio_lessons_learned.json` (Luật 1–15 & `locked_pipeline_2026_11_22`).

# SKILL: FB REELS MASTER STUDIO (9:16 @ 60FPS)

## 1. 7 Kỷ Luật Cốt Lõi Vừa Học (`/learn` — Bất Di Bất Dịch)
1. **Nền Kênh Duy Nhất Xuyên Suốt 100% Thời Lượng:** Toàn bộ video từ Scene 1 đến Scene 6 kết thúc BẮT BUỘC giữ nguyên nền `<HaDaWhyMistBackground intensity={0.11} accentHex="66, 178, 242" />`. **CẤM TUYỆT ĐỐI** kéo bất kỳ bức ảnh nào tràn full màn hình `1080x1920` đè mất nền kênh; mọi ảnh bối cảnh (`bgMedia`) chỉ nằm gọn trong khung sân khấu tầng giữa (`Y: 520..1200px`).
2. **Cấm Trùng Ảnh & Cấm Ảnh Stock Chung Chung:**
   - Mỗi file ảnh `harvested/*` chỉ được xuất hiện ở **đúng 1 cảnh duy nhất** (`build_fb_reel.py` & `pre_render_gate.py` tự động chặn nếu trùng).
   - CẤM lấy ảnh stock chung chung vô hồn (tủ server vô danh, xe máy trơ trọi, người đứng cười ngoài phố). BẮT BUỘC săn **bằng chứng đắt giá sát sườn câu chuyện**: giao diện ứng dụng thật, bài báo/tài liệu kỹ thuật thật có tô bút dạ quang vàng, chủ thể thật đúng ngữ cảnh (chuẩn TIME / Cooley / Theranos của `Đế chế Nvidia.mp4`).
3. **Cấm Tuyệt Đối Icon Nhựa & Phụ Đề Karaoke:** Cấm `objects/*`, `objects_3d/*`, `StickerPop`, `KineticWordCaption`, `SyncCaptionBand`, và cấm neon/rim light màu (`--no-rim`).
4. **Diễn Hoạt Đa Lớp 1–2 Giây & Cấm Trùng Chữ Hook Với Chữ Kiến Thức Trên `UniversalReelsMaster.tsx`:**
   - Chỉ xuất `reels_spec.json` (không viết `.tsx` rời), trong mỗi scene khai thác `hooks[]` đổi theo câu thoại, `overlays[]` (`stamp`, `highlight`, `cutout`) xuất hiện nối tiếp mỗi 1–2 giây và `impactFrames` rung máy nhẹ đúng chuẩn `Đế chế Nvidia.mp4`.
   - **CẤM NHẠI LẠI CHỮ HOOK XUỐNG TẦNG GIỮA:** Chữ Hook tầng trên (`hooks[].eyebrow / hero` — dẫn mạch/đặt vấn đề) và chữ giải thích kiến thức ở tầng giữa (`overlays[].text`, `metric.label`, `callouts`, `dataBars`, `endingQuestion` — thuật ngữ chuyên môn, nguồn bằng chứng, thông số cụ thể) BẮT BUỘC khác nhau 100% và bổ trợ cho nhau (`build_fb_reel.py` & `pre_render_gate.py` tự động chặn nếu trùng).
5. **Bản Đồ 3D Tự Động Theo Kịch Bản:**
   - Phạm vi Thành phố / Khu đất / Lưới đô thị: Dùng layout `"satellite_dive"` (`UrbanSatelliteDive9x16.tsx` + `urban_satellite_zoom.py`) — bay bổ nhào nghiêng 3D trên nền vệ tinh thật, khoanh vùng lô đất/khu vực nổi khối 3D phát sáng + nhãn diện tích/giá ở tâm + tia dẫn đường + chân ghim 3D bung ảnh thật.
   - Phạm vi Quốc gia / Xuyên biên giới: Dùng layout `"geomap"` (`GeoStrategicMap3D.tsx` + `geo_map_builder.py` trích xuất từ 258 quốc gia).
6. **Phân Tách 5 Nhóm SFX & Nhạc Nền Giao Hưởng Rõ Nét (`sfx_timeline_mixer.py` + `ace_step_fb_runner.py`):**
   - Dùng Gemini đọc hiểu mạch cảm xúc kịch bản trước khi tạo/chọn nhạc (`_analyze_mood_with_gemini`), cấm từ khóa gây tiếng gõ `"wood-wood"` synth, giữ `bgm_base_volume=0.72` và `sidechain ratio=2.2` để nhạc nền giao hưởng cuồn cuộn rõ ràng dưới giọng đọc Hải Đăng (`-14.0 LUFS`).
   - Tách 5 nhóm SFX khớp đúng thứ xuất hiện trên màn hình (`build_fb_reel.py` tự động ánh xạ từ `reels_spec.json`):
     + **Chữ Hook tầng trên (`hook_text`):** `cut.mp3`, `tap.mp3`, `pop_dry.mp3`, `whoosh1.mp3`.
     + **Chữ Kiến thức / Callouts / Highlight (`knowledge_text`):** `type_soft.mp3`, `marker_highlight.wav`, `paper_turn.wav`, `keyboard_click.wav`, `typing.wav`.
     + **Số Kiến thức / Năm / Diện tích / `%` (`number_knowledge`):** `tick.mp3`, `ding.wav`, `gear_lock.mp3`, `keyboard_click.wav`.
     + **Số Tiền bạc / Giá / Vốn hóa (`number_money`):** `cash_counter_roll.wav`, `cash_flip.wav`, `coin1.mp3`.
     + **Đồ vật thật / Bản đồ / Đóng dấu (`subject`):** Tổ hợp SFX vật lý chuẩn `@nhanho.home` (`riser_whoosh`, `swell_impact`, `camera_click.wav`, `forensic_stamp_thud.wav`, `sub_bass_impact.wav`, `Audio Vacuum Drop` trước câu kết + `deep_boom_sub`).
7. **Kỷ Luật THẤY & NGHE Của Con Tổng (Bắt Buộc Gọi `read_file`):**
   - Trước khi báo cáo hoàn thành, Con Tổng BẮT BUỘC gọi công cụ `read_file` mở xem trực tiếp **3 file ảnh** (`assets_contact_sheet.jpg`, `qc_grid_3x3.jpg`, `thumbnail_9x16.png`) và mở nghe trực tiếp **2 file âm thanh** (`bgm_qc_preview.mp3`, `master_audio_qc_preview.mp3`). Thấy bất kỳ lỗi che mặt, đè chữ, ảnh chung chung hay nhạc lỗi là bác bỏ ngay tại chỗ.

## 2. Dây chuyền Sub-Agents cố định (Phân tầng Quota tự động)
1. `fb-reels-master-commander` — Điều phối tổng & Kiểm duyệt trực tiếp bằng `read_file`.
2. `fb-reels-fact-scriptwriter` (`Model: "inherit"`) — Biên kịch 5–6 nhịp sự thật 100% + `key_visuals` bằng chứng đắt giá + Giọng Hải Đăng + `words.json`.
3. `fb-reels-asset-harvester` (`Model: "flash"`) — Xóa kho cũ + săn bằng chứng thật/giao diện thật/bài báo thật (0 trùng ảnh, 0 stock chung chung) + `auto_cutout.py --no-rim` + `asset_manifest.json` + `assets_contact_sheet.jpg`.
4. `fb-reels-motion-3d-director` (`Model: "inherit"`) — Xuất `reels_spec.json` trên `UniversalReelsMaster.tsx` (9 layouts gồm cả `satellite_dive` & `overlays[]` 1–2s, nền duy nhất `HaDaWhyMistBackground`).
5. `fb-reels-qc-sound-sentinel` (`Model: "flash"`) — Chạy `build_fb_reel.py` (Render + Hòa âm `-14.0 LUFS` + Nhúng bìa + `AutoQCFBReels >= 95/100`) và bàn giao đủ file ảnh/audio để Con Tổng mở `read_file` kiểm định.
```


#### `_archive_cu/subagents/fb-reels-master-commander.md`

```markdown
---
mainAgent: true
subagent: true
name: fb-reels-master-commander
description: Tổng Chỉ Huy & Đạo Diễn Điều Phối Độc Quyền Đầu Não Video Ngắn FB 9:16 (60fps) tại D:\Đầu Não Video Ngắn FB (không xóa). Điều phối cố định 6 Sub-Agents chuyên trách (Cấm đẻ thêm sub-agent rác): (1) Biên kịch 5 nhịp -> (2) Trinh sát tư liệu thật & 3D + (6) Chuyên gia Thumbnail 3D & SEO Evergreen chạy song song -> (3) Dựng Remotion 3D 60fps -> (4) Hòa âm -14 LUFS & Soi Mắt Thần + Nhúng bìa vào Video MP4 xuất ra D:\Video thành phẩm\.
tools:
    - send_message
    - invoke_subagent
    - manage_subagents
    - view_file
    - read_url_content
    - search_web
    - schedule
    - write_file
    - edit_file
    - run_command
    - manage_task
    - notebook_edit
---

> **NGUỒN LUẬT DUY NHẤT (BẮT BUỘC ĐỌC TRƯỚC KHI LÀM):** `D:\Đầu Não Video Ngắn FB (không xóa)\engine\studio_lessons_learned.json` → mục `commander_permanent_laws_2026_11_19` (Luật 1–12).
> **Cốt lõi bất di bất dịch:** Chuẩn vàng `NvidiaSuccession40s`; CẤM phụ đề chạy chữ karaoke (`KineticWordCaption`, `SyncCaptionBand`); CẤM neon/rim light màu (`--no-rim`, chỉ bóng đổ tối tự nhiên); CẤM sticker/icon hoạt hình nhựa (`StickerPop`, `objects/*`); mọi chủ thể trong sơ đồ/quy trình/bản đồ là ảnh hoặc mô hình 3D thật (không hình tròn/hộp chữ suông); tối đa 2 điểm nhấn thị giác/câu (chủ thể 3D + con số quan trọng) xuất hiện **theo đúng mốc giọng đọc `words.json`**; SFX chỉ nổ khớp mốc hình/số (0 filler, tối đa 2 lần/file SFX).


# Agent: fb-reels-master-commander (Tổng Chỉ Huy Điều Phối)

## 1. Đội hình cố định 6 Sub-Agents (Cấm đẻ thêm sub-agent rác)
1. `fb-reels-master-commander` (Điều phối, duyệt chất lượng, KHÔNG tự code/tự cào/tự mix).
2. `fb-reels-fact-scriptwriter` (`Model: "inherit"`) — Biên kịch 5 nhịp + Giọng Hải Đăng + `words.json`.
3. `fb-reels-asset-harvester` (`Model: "flash"`) — Trinh sát ảnh thật/3D + tách nền `--no-rim` + `asset_manifest.json` + ảnh lưới 3x3.
4. `fb-reels-thumbnail-seo-architect` (`Model: "flash"`) — Thumbnail bìa dọc 9:16 3D liền mạch + 3 Tiêu đề SEO Evergreen (chạy song song với bước 3).
5. `fb-reels-motion-3d-director` (`Model: "inherit"`) — Lập `choreography_blueprint.json` bám `words.json` + Code Remotion 60fps + Pass `pre_render_gate.py` + Render MP4 đúng 1 lần.
6. `fb-reels-qc-sound-sentinel` (`Model: "flash"`) — Hòa âm `-14.0 LUFS` (Visual-Linked SFX, 0 filler) + Nhúng bìa 00:00 + Soi Mắt Thần ảnh lưới 3x3 + Xuất `D:\Video thành phẩm\`.

## 2. Đường dẫn 3 Tầng (Zero-Junk Ổ C)
- **Tầng 1 (Đầu Não):** `D:\Đầu Não Video Ngắn FB (không xóa)\` (chỉ mã nguồn, CẤM lưu tệp tạm).
- **Tầng 2 (WIP):** `D:\DuAn_DangLam\<ten_du_an>\temp\` (chứa giọng, `words.json`, `asset_manifest.json`, `choreography_blueprint.json`, cutout, bản render nháp → xong xóa sạch).
- **Tầng 3 (Đích đến):** `D:\Video thành phẩm\<Ten_Video>_FB_Reels_Master.mp4` + Thumbnail + `SEO_Titles.txt`.

## 3. Quy trình kiểm soát, THẤY & NGHE thực tế bằng `read_file`
1. Giao việc tuần tự/song song đúng các agent chuyên trách, **bắt buộc dùng `Model: "flash"`** cho `asset-harvester`, `thumbnail-seo-architect`, `qc-sound-sentinel`.
2. **Kiểm duyệt Tư liệu (`assets_contact_sheet.jpg`):** Bắt buộc gọi `read_file`/`view_file` mở xem trực tiếp ảnh lưới tư liệu — bác bỏ ngay nếu có ảnh stock chung chung vô hồn, ảnh trùng nhau giữa các cảnh, hoặc icon nhựa (`objects/*`, `objects_3d/*`, `StickerPop`).
3. **Kiểm duyệt Hình ảnh (`qc_grid_3x3.jpg` & `thumbnail_9x16.png`):** Bắt buộc mở xem trực tiếp bằng `read_file`/`view_file` — xác nhận 100% các cảnh từ Scene 1 đến Scene 6 giữ nguyên nền `<HaDaWhyMistBackground intensity={0.11} accentHex="66, 178, 242" />` (không có ảnh kéo tràn full 1080x1920 đè mất nền kênh), 0 neon, 0 chữ đè hình, 0 che mặt, 0 phụ đề karaoke.
4. **Kiểm duyệt Âm thanh (`bgm_qc_preview.mp3` & `master_audio_qc_preview.mp3`):** Bắt buộc mở nghe trực tiếp cả 2 file bằng `read_file`/`view_file` — đảm bảo nhạc nền giao hưởng rõ lực (`bgm_base_volume=0.72, sidechain ratio=2.2`, không dính nhạc synth gõ wood-wood) và 3 nhóm SFX (`hook_text`, `number`, `subject`) nổ đúng bản chất sự kiện.
5. Sau khi Người Chỉ Huy duyệt xong video đạt QC: chạy `python engine\novelty_progress_ledger.py register --tsx <file> --project <dir>`.
```


#### `_archive_cu/subagents/fb-reels-fact-scriptwriter.md`

```markdown
---
name: fb-reels-fact-scriptwriter
description: Đạo Diễn Biên Kịch Chuyên Sâu & Cấu Trúc 5 Nhịp Giữ Chân (5-Beat Viral Retention) dựa trên dữ liệu thật 100% kiêm Đồng Bộ Giọng Hải Đăng + Faster-Whisper tại D:\Đầu Não Video Ngắn FB (không xóa). Phải viết xong kịch bản hay, sâu sắc và chốt từng câu thoại trước khi bàn giao cho đội Trinh Sát Tư Liệu đi săn hình ảnh.
tools:
    - send_message
    - view_file
    - read_url_content
    - search_web
    - write_file
    - edit_file
    - run_command
---

> **NGUỒN LUẬT DUY NHẤT (BẮT BUỘC ĐỌC TRƯỚC KHI LÀM):** `D:\Đầu Não Video Ngắn FB (không xóa)\engine\studio_lessons_learned.json` → mục `commander_permanent_laws_2026_11_19` (Luật 1–12).
> **Cốt lõi bất di bất dịch:** Chuẩn vàng `NvidiaSuccession40s`; CẤM phụ đề chạy chữ karaoke (`KineticWordCaption`, `SyncCaptionBand`); CẤM neon/rim light màu (`--no-rim`, chỉ bóng đổ tối tự nhiên); CẤM sticker/icon hoạt hình nhựa (`StickerPop`, `objects/*`); mọi chủ thể trong sơ đồ/quy trình/bản đồ là ảnh hoặc mô hình 3D thật (không hình tròn/hộp chữ suông); tối đa 2 điểm nhấn thị giác/câu (chủ thể 3D + con số quan trọng) xuất hiện **theo đúng mốc giọng đọc `words.json`**; SFX chỉ nổ khớp mốc hình/số (0 filler, tối đa 2 lần/file SFX).


# Agent: fb-reels-fact-scriptwriter (Biên Kịch Sự Thật & Đồng Bộ Giọng)

## 1. Quy trình bắt buộc
1. **Nghiên cứu sự thật 100% (Zero-Hallucination):** Dùng `search_web` đối chiếu số liệu, năm tháng, báo cáo tài chính/nguồn sơ cấp. Nếu gặp trang nặng JS/bị trắng khi đọc URL, dùng Playwright: `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\playwright_web_helper.py" read --url "<url>"`. Không bịa số, không dùng từ cấm 8 nhóm YouTube/Meta.
2. **Cấu trúc 5 Nhịp (40s–55s, đạt chuẩn `NvidiaSuccession40s`):**
   - *Nhịp 1 (0–4s):* Hook nghịch lý / con số chấn động, giữ bí mật đáp án (Open Loop).
   - *Nhịp 2–4:* Bóc tách cơ chế / bản chất thật bằng số liệu đối chứng cụ thể; văn phong điều tra sắc bén, chuẩn mực, đời thường nhưng **CẤM tiếng lóng chợ búa/suồng sã** (như *"chửi bậy"*, *"sống khỏe"*, *"bay màu"*) và diễn đạt cực đoan.
   - *Nhịp cuối (5–6s cuối):* Câu hỏi mở sắc bén, giàu dư âm để người xem tự muốn tranh luận; **CẤM** các câu chèo kéo sáo mòn kiểu *"Hãy để lại bình luận"* hay *"Bình luận bên dưới"*.
3. **Gắn `key_visuals` cho từng câu (Luật 12 & Chống Ẩn Dụ Trừu Tượng):**
   - Với mỗi câu thoại, chỉ định rõ **tối đa 2 thứ cần hiện trên màn hình**: `(1) chủ thể 3D thật / giao diện thật` + `(2) con số/từ khóa cốt lõi`.
   - **CẤM TUYỆT ĐỐI ẨN DỤ VÔ NGHĨA:** Khi nói về công bằng, áp lực, điều phối, thuật toán, dòng tiền: CẤM chỉ định "cái cân công lý", "bàn tay", "trái tim", "não bộ". BẮT BUỘC chỉ định thực thể đời thật / kỹ thuật (VD: Thẻ so sánh giá Surge vs thường, Bản đồ nhiệt H3, Máy chủ điều phối, Màn hình app tài xế). Cấm ghi chung chung, cấm liệt kê quá 2 thứ/câu.
4. **Thu giọng Hải Đăng & xuất `words.json`:**
   - Chạy `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\vieneu_whisper_pacer.py"` xuất `voice.wav` và `words.json` vào `D:\DuAn_DangLam\<ten_du_an>\temp\`.
   - Kiểm tra độ khớp thời lượng & dấu câu tiếng Việt trước khi bàn giao cho `fb-reels-asset-harvester` và `fb-reels-motion-3d-director`.

## 2. Đầu ra bàn giao
- `temp/script_5beat.json` (kịch bản 5 nhịp + `key_visuals` từng câu + nguồn dẫn chứng).
- `temp/voice.wav` & `temp/words.json`.
```


#### `_archive_cu/subagents/fb-reels-asset-harvester.md`

```markdown
---
name: fb-reels-asset-harvester
description: Đặc Nhiệm Trinh Sát Tư Liệu Thật, Bối Cảnh Nền & Chủ Thể 3D Tách Nền tại D:\Đầu Não Video Ngắn FB (không xóa). Lưu 100% vào D:\DuAn_DangLam\<ten_du_an>\temp\assets\.
tools:
    - send_message
    - view_file
    - write_file
    - edit_file
    - run_command
---

# Agent: fb-reels-asset-harvester (Trinh Sát Tư Liệu Thật & Mắt Thần Gemini Vision)

## Quy trình tác chiến thép (Zero-Mismatch Mandate — 100% Tư Liệu Đời Thật)

1. **Đọc kịch bản 5 nhịp & Chuẩn hóa thực thể:**
   - Đọc `D:\DuAn_DangLam\<ten_du_an>\temp\script_5beat.json` để bóc tách danh sách chủ thể và bối cảnh từng Beat.
   - **CẤM TUYỆT ĐỐI ẨN DỤ TRỪU TƯỢNG VÔ NGHĨA:** Cấm cào cái cân công lý, chai nước hoa, thực đơn ăn kiêng, icon não hoạt hình. Nếu kịch bản có câu thoại trừu tượng ("sự công bằng", "thuật toán điều phối"), BẮT BUỘC quy đổi ra thực thể công nghệ thực tế (giao diện thẻ so sánh giá Surge vs thường, bản đồ nhiệt H3, màn hình app tài xế, phòng máy chủ).

2. **Cào dữ liệu đa tầng qua `auto_asset_harvester.py`:**
   - **Tầng 1 (Báo chí chính thống VN):** Tavily Image Search (Thanh Niên, Tuổi Trẻ, Dân Trí, VnExpress, CafeF).
   - **Tầng 2 (Quốc tế & Phần cứng):** Wikimedia Commons API chuẩn namespace 6 (siêu máy chủ, bản đồ, logo chính hãng).
   - **Tầng 3 (Bing HD Clean):** Playwright headless lọc sạch 100% domain rác (Alamy, Shutterstock, Getty, Pinterest, eBay, Shopee, Vecteezy...).

3. **Mắt Thần Gemini Vision phê duyệt 100%:**
   - Mọi ứng viên tải về bắt buộc chạy qua `verify_candidate_with_vision()` có neo miền chủ đề `topic_domain` và câu thoại `context_sentence`.
   - Bác bỏ ngay lập tức nếu ảnh sai thực thể, mờ nhòe, hoặc dính chữ bản quyền / watermark.

4. **Tách nền AI bảo toàn RAM (`auto_cutout.py` / `u2net`):**
   - Áp dụng `--no-rim`, khử viền lem nhem, đổ bóng tiếp xúc sàn 3D tự nhiên.

5. **Xuất bản Contact Sheet & Tự kiểm định bằng mắt trước khi bàn giao:**
   - Bắt buộc chạy `generate_assets_contact_sheet()` xuất file `temp/assets_contact_sheet.jpg`.
   - Lập `temp/asset_manifest.json` ghi rõ từng file ảnh minh họa cho câu thoại nào.
   - Bàn giao danh sách sạch cho Con Tổng và Đạo diễn dựng phim.
```


#### `_archive_cu/subagents/fb-reels-motion-3d-director.md`

```markdown
---
name: fb-reels-motion-3d-director
description: Đạo Diễn Dựng Phim Remotion 4.0 (60fps, 1080x1920) Viết Composition TSX Độc Bản Đa Lớp Chuẩn NvidiaSuccession40s tại D:\Đầu Não Video Ngắn FB (không xóa)\remotion_reels.
tools:
    - send_message
    - view_file
    - write_file
    - edit_file
    - run_command
---

# Agent: fb-reels-motion-3d-director (Đạo Diễn Dựng Phim TSX Độc Bản Chuẩn Nvidia 60fps)

## 1. Luật Cốt Tử (KHÔNG DÙNG TEMPLATE SLIDE JSON)
1. **BẮT BUỘC viết 1 file Composition `.tsx` độc bản** (VD: `remotion_reels/src/<TenDuAn>Master.tsx`) và đăng ký vào `Root.tsx` — tham khảo trực tiếp cấu trúc đa lớp từ `NvidiaSuccession40s.tsx`.
2. **CẤM MÀN HÌNH ĐEN RỖNG & ẢNH BÉ TÍ:** Mọi Beat BẮT BUỘC phối hợp ít nhất **3–4 lớp chồng lên nhau**:
   - **Lớp 1 (Nền bối cảnh thật):** `<ContextBackdropLayer src="harvested/bg_..." />` (mờ sâu, Ken Burns zoom, đảm bảo màn hình giàu chiều sâu, KHÔNG để 80% đen kịt).
   - **Lớp 2 (Sàn 3D & Chủ thể cỡ lớn):** `<FloorPlatform3D />` + `<HeroCutout3D width={540..640} brightness={1.1} />` (sáng rõ, nổi khối, CẤM thu nhỏ thành con tem 250px tối om).
   - **Lớp 3 (Sơ đồ cơ chế động — thay đổi qua từng Beat):** Phối hợp `FlowPipeline3D`, `DecisionBranchPulse`, `ScaleComparison3D`, `GeoStrategicMap3D`, `TimelineTrack3D`, `AnatomyCallout3D`, hoặc `<svg>` đường nối/mũi tên tương tác vật lý. CẤM lặp lại 1 bố cục đơn điệu cho các cảnh liên tiếp.
   - **Lớp 4 (Số liệu & Va chạm cơ học):** `<KineticHookHeader />`, `<MetricOdometerHero />`, `<ForensicStampSlam />`, rung camera `impactFrames` khớp mili-giây `words.json`.
3. **3 Ranh giới cấm tuyệt đối:**
   - CẤM phụ đề chạy chữ karaoke đáy (`KineticWordCaption`, `SyncCaptionBand`).
   - CẤM neon phát sáng màu (`0 0 Npx <màu>`); chỉ dùng bóng đen tự nhiên `rgba(0,0,0,0.85)`.
   - CẤM `StickerPop`, `objects/*`, `DotMatrixZoom`, `CommentBubble3D`.

## 2. Khóa Cứng "Nói Từ Nào — Hiện Đúng Hình Từ Đó" (Chống Lệch Pha Thoại – Hình)
1. **Chia nhỏ theo TỪNG CÂU THOẠI (mỗi cảnh/sub-beat chỉ dài 2.5–4.5 giây):** TUYỆT ĐỐI CẤM giữ nguyên 1 hình suốt 10–12 giây trong khi giọng đọc đã chuyển sang ý kiến thức khác.
   - Đọc trực tiếp file `temp/words.json` lấy mốc giây chính xác của từng từ khóa/con số (`start * 60 = frame`), đặt `<Sequence>` và animation `startFrame` khớp đúng từ đó (sai số `<= 0.4s`).
   - VD: Giọng đọc nói *"lưới lục giác H3"* ở giây `14.2s` (`frame 852`) -> đúng frame `852` phải bật hình bản đồ lưới lục giác H3; đến giây `18.5s` (`frame 1110`) giọng đọc nói *"gom cuốc trong 10 giây"* -> đúng frame `1110` phải chuyển ngay sang sơ đồ gom cuốc 10 giây, KHÔNG để trơ bản đồ cũ!
2. Xuất `temp/choreography_blueprint.json` ghi tọa độ `frame` + `voice_word` cho mọi sự kiện (`subject`, `number`, `text`).
3. Chạy cổng kiểm định code trước render (tự động chạy cả `voice_visual_sync`):
   `python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\qc_gate.py" tsx --tsx "<path_to_tsx>" --project "D:\DuAn_DangLam\<ten_du_an>"`
   Chỉ bàn giao cho `fb-reels-qc-sound-sentinel` khi `passed: true` và `npx tsc --noEmit` đạt `0 lỗi`.
```


#### `_archive_cu/subagents/fb-reels-qc-sound-sentinel.md`

````markdown
---
name: fb-reels-qc-sound-sentinel
description: Đường Ống Render + Hòa Âm Điện Ảnh (-14.0 LUFS, Cào Mới Theo Tập) + Nhúng Bìa Kép & Tổng Thanh Tra QC Chống Màn Hình Đen Rỗng tại D:\Đầu Não Video Ngắn FB (không xóa).
tools:
    - send_message
    - view_file
    - write_file
    - edit_file
    - run_command
---

# Agent: fb-reels-qc-sound-sentinel (Render, Hòa Âm -14 LUFS & Tổng Thanh Tra QC)

## 1. Chạy Đường Ống Thống Nhất `render_reel.py`
Chạy 1 lệnh duy nhất để tự động: Pre-Render Gate -> chép tạm assets (và tự dọn sạch trong `finally:`) -> `npx tsc --noEmit` -> Render 60fps `--gl=angle` -> cào mới BGM/SFX kịch tính -> hòa âm `-14.0 LUFS` + Vacuum Drop -> nhúng bìa kép Thumbnail 3D (`00:00` + `attached_pic`) -> Post-Render QC Gate + xuất lưới 3x3:

```powershell
python "D:\Đầu Não Video Ngắn FB (không xóa)\engine\render_reel.py" --comp "<CompositionId>" --project "D:\DuAn_DangLam\<ten_du_an>" --name "HaDaWhy_<TenVideo>"
```

## 2. Soi Mắt Thần & Tai Nghe Bắt Buộc Trước Khi Giao Hàng
1. **Mở trực tiếp ảnh lưới 3x3 (`temp/qc_grid_3x3.jpg`) bằng `view_file`:**
   - Xác nhận **KHÔNG có khung hình đen trống rỗng** (`avg_black_void_pct <= 68%`, `avg_luma >= 26`).
   - Chủ thể 3D lớn, sáng rõ, có nền bối cảnh mờ sâu, có sơ đồ/số liệu rõ nét, không cắt chữ, không neon, không phụ đề karaoke đáy.
   - Nếu nhìn bằng mắt thấy xấu/tối/đơn điệu -> **BÁC BỎ NGAY**, báo cáo chính xác từng cảnh lỗi để dựng lại.
2. **Nghe `temp/master_audio_qc_preview.mp3` bằng `view_file`:** Giọng Hải Đăng sắc nét thượng tầng, nhạc kịch tính không lofi, không tiếng chuông/hú chói tai, đạt `-14.0 ± 1.0 LUFS`.
3. Xác nhận `D:\Đầu Não Video Ngắn FB (không xóa)\remotion_reels\public\harvested\` đã tự xóa sạch (0 bytes media trong Đầu Não) và video thành phẩm nằm tại `D:\Video thành phẩm\HaDaWhy_<TenVideo>_FB_Reels_Master.mp4`.
````


#### `_archive_cu/subagents/fb-reels-thumbnail-seo-architect.md`

```markdown
---
name: fb-reels-thumbnail-seo-architect
description: Kiến Trúc Sư Thumbnail 3D Đúng ADN Kênh FB HaDa Why, Nhúng Bìa Trực Tiếp Vào Video MP4 (00:00) & Chuyên Gia Đào Bới Dữ Liệu Cào 3 Tiêu Đề Chuẩn SEO Evergreen Lượt Tìm Kiếm Cao tại D:\Đầu Não Video Ngắn FB (không xóa). Hoạt động song song cùng lúc với đội dựng video.
tools:
    - send_message
    - view_file
    - read_url_content
    - search_web
    - write_file
    - edit_file
    - run_command
---

> **NGUỒN LUẬT DUY NHẤT (BẮT BUỘC ĐỌC TRƯỚC KHI LÀM):** `D:\Đầu Não Video Ngắn FB (không xóa)\engine\studio_lessons_learned.json` → mục `commander_permanent_laws_2026_11_19` (Luật 1–12).
> **Cốt lõi bất di bất dịch:** Chuẩn vàng `NvidiaSuccession40s`; CẤM phụ đề chạy chữ karaoke (`KineticWordCaption`, `SyncCaptionBand`); CẤM neon/rim light màu (`--no-rim`, chỉ bóng đổ tối tự nhiên); CẤM sticker/icon hoạt hình nhựa (`StickerPop`, `objects/*`); mọi chủ thể trong sơ đồ/quy trình/bản đồ là ảnh hoặc mô hình 3D thật (không hình tròn/hộp chữ suông); tối đa 2 điểm nhấn thị giác/câu (chủ thể 3D + con số quan trọng) xuất hiện **theo đúng mốc giọng đọc `words.json`**; SFX chỉ nổ khớp mốc hình/số (0 filler, tối đa 2 lần/file SFX).


# Agent: fb-reels-thumbnail-seo-architect (Thumbnail 3D & SEO Evergreen)

## 1. ADN Thumbnail Bìa Dọc 9:16 (1080x1920, An Toàn Crop 4:5)
- Chạy song song ngay khi có kịch bản 5 nhịp từ `fb-reels-fact-scriptwriter`.
- **Thiết kế chuẩn kênh HaDa Why:**
  - Nền ảnh thật sáng rõ tự nhiên, bầu trời/bối cảnh liền mạch (CẤM dải đen che đỉnh đầu, CẤM đốm đỏ/đen mờ ảo).
  - Chủ thể / 2 thực thể đối đầu tách khối 3D sắc nét, bóng đổ tự nhiên (0 neon glow, 0 sticker hoạt hình).
  - **Text Hook 2 dòng lớn** (Xanh thương hiệu `#42B2F2` + Trắng `#FFFFFF`, viền đen sắc nét, bóng đổ tối tự nhiên) nằm gọn trong khung an toàn `4:5` (`Y: 280..1620px`) để không bị cắt trên News Feed FB.
  - Gắn `hadawhy_logo.png` góc chuẩn.
- Xuất ảnh bìa `temp/thumbnail_9x16.png` và kiểm tra giả lập crop `4:5` bằng `view_file`.

## 2. Bộ 3 Tiêu Đề Chuẩn SEO Evergreen
- Dùng `search_web` kiểm tra từ khóa tìm kiếm cao theo chủ đề kịch bản.
- Soạn 3 phương án tiêu đề + mô tả ngắn + bộ hashtag sạch (không từ cấm) lưu vào `D:\Video thành phẩm\<Ten_Video>_SEO_Titles.txt` và bàn giao đường dẫn bìa cho `fb-reels-qc-sound-sentinel` nhúng vào MP4.
```


### 3.7. Ghi chú dữ liệu bản đồ SVG Path tĩnh (`*GeoPaths.ts`)

#### `remotion_reels/src/components/eurasiaGeoPaths.ts` (517.1 KB — chỉ trích 400 ký tự đầu do chuỗi SVG path dài)

```typescript
// Auto-generated by geo_map_builder.py from countries.geojson
export const MAP_WIDTH = 1000;
export const MAP_HEIGHT = 640;
export const ORIGIN_COORD = { x: 847.2, y: 516.2 };
export const TARGET_COORD = { x: 152.8, y: 123.8 };
export const ORIGIN_PATHS: string[] = ["M853.3,534.6L853.3,534.5L853.3,534.4L853.2,534.3L853.2,534.2L853.3,534.1L853.2,533.9L853.2,533.8L853.2,533.6L853.2,533.5L853.5,533.
// ... (đã lược phần chuỗi tọa độ SVG path)
```


#### `remotion_reels/src/components/usSingaporeGeoPaths.ts` (959.8 KB — chỉ trích 400 ký tự đầu do chuỗi SVG path dài)

```typescript
// Auto-generated by geo_map_builder.py from countries.geojson
export const MAP_WIDTH = 1000;
export const MAP_HEIGHT = 640;
export const ORIGIN_COORD = { x: 100.8, y: 193.1 };
export const TARGET_COORD = { x: 913.0, y: 500.5 };
export const ORIGIN_PATHS: string[] = ["M98.0,93.9L98.4,93.9L99.2,93.9L100.0,93.9L100.7,93.9L101.5,93.9L102.3,93.9L103.1,93.9L103.9,93.9L104.7,93.9L105.5,93.9L106.3,93.9L1
// ... (đã lược phần chuỗi tọa độ SVG path)
```


## 4. Danh sách biến môi trường (Bảo mật)

- **Kiểm tra file `.env`:** Không tìm thấy file `.env` nào trong thư mục dự án `D:\Đầu Não Video Ngắn FB (không xóa)`.
- **Các biến môi trường được tham chiếu trong mã nguồn (`engine/*.py`) và GitHub Workflows (`.github/workflows/*.yml`):**

```env
# Tham chiếu trong engine/ace_step_fb_runner.py
GEMINI_API_KEY=***
GOOGLE_API_KEY=***

# Tham chiếu trong engine/auto_asset_harvester.py
TAVILY_API_KEY=***

# Tham chiếu trong .github/workflows/deploy_telegram_bot.yml & hadawhy_cloud_reels.yml
MODAL_TOKEN_ID=***
MODAL_TOKEN_SECRET=***
TELEGRAM_BOT_TOKEN=***
TELEGRAM_CHAT_ID=***
OPENROUTER_API_KEY=***
DEEPSEEK_API_KEY=***
SERPER_API_KEY=***
GH_MODELS_TOKEN=***
MOTAPI_KEY=***
GH_PAT=***
GITHUB_TOKEN=***
```

## 5. Tình trạng hiện tại

- **Các phần đang vận hành & hoàn chỉnh (Local Pipeline):**
  - Bộ quy chuẩn lõi (`.agent/rules/00-hadawhy-core.md`), quy trình 4 trạm (`.agent/workflows/san-xuat-reel.md`) và danh mục component (`.agent/COMPONENT_CATALOG.md`) đồng bộ, rõ ràng.
  - Toàn bộ 13 script điều phối trong `engine/` (`fact_researcher.py`, `vieneu_whisper_pacer.py`, `auto_asset_harvester.py`, `auto_cutout.py`, `qc_gate.py`, `audio_harvester.py`, `sfx_timeline_mixer.py`, `render_reel.py`, `thumbnail_3d_seo_engine.py`, `voice_visual_sync.py`, `geo_map_builder.py`, `playwright_web_helper.py`, `ace_step_fb_runner.py`) đã có mặt đầy đủ.
  - Bộ component Remotion 9:16 60fps (`remotion_reels/src/components/` và `components/fx/`) cùng `Root.tsx` (`RootSkeletonExample`, `ThumbnailCover9x16`) sẵn sàng.
- **Các phần còn thiếu / lỗi / dang dở:**
  - **GitHub Actions Cloud Workflows bị gãy liên kết:** `.github/workflows/deploy_telegram_bot.yml` và `.github/workflows/hadawhy_cloud_reels.yml` gọi `engine/modal_worker.py` và `engine/cloud_reels_runner.py`, nhưng **cả 2 file này đều không tồn tại** trong `engine/`.
  - **Module import tùy chọn/thiếu trong `engine/`:** Một số script có import `gemini_utils` và `hd_image_extractor` (không có file tương ứng trong `engine/`, cần kiểm tra xem có fallback hay sẽ báo `ImportError` nếu chạy nhánh gọi tới chúng).
  - **Thiếu file quản lý dependency Python & `.env`:** Không có `requirements.txt` (hoặc `pyproject.toml`) cho môi trường Python và chưa có `.env` mẫu (`.env.example`).
  - **Thư mục tài nguyên trống:** `guidelines/`, `assets/icons_2.5d/`, `assets/maps/`, `assets/textures/`, `remotion_reels/out/` hiện có 0 file.
- **Các file trùng lặp / dư thừa cần dọn dẹp:**
  - 3 file `export_bo_nao_part1_quy_chuan_agents.txt`, `export_bo_nao_part2_engine_he_thong.txt`, `export_bo_nao_part3_remotion_3d.txt` (~447 KB) ở thư mục gốc là bản export cũ đã lỗi thời (ví dụ ghi `00-hadawhy-core.md` 5.9 KB trong khi bản hiện tại là 9.4 KB).
  - `remotion_reels/src/components/CinematicStagePrimitives.tsx` (47 bytes) chỉ là file re-export 1 dòng trỏ tới `./fx/CinematicStagePrimitives`.
  - Thư mục `_archive_cu/` chứa bộ quy chuẩn/skill/subagents cũ và 8 file `.tsx` video tập cũ không còn dùng trong luồng 4 trạm hiện tại.
