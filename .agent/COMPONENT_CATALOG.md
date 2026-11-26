# SỔ TAY PROPS CHUẨN (COMPONENT CATALOG — 60FPS AE & 2.5D/3D)

Nền xanh dương ADN `<HaDaWhyMistBackground />`, Safe Zone `X: 80..920`, `Y: 340..1560`, khóa 100% font tiếng Việt `BeVietnamProBlack` (0 vỡ dấu), GPU `translate3d` + `willChange: "transform"`.
**Luật cứng:** Mỗi video 5 Beat bắt buộc dùng **>= 5 loại component minh họa khác nhau**, tối thiểu **2 Beat có chiều sâu 2.5D/3D**, CẤM lặp quá **2 lần** cùng 1 component (`EvidenceDocumentCard`, `ProcessStepChain`, `VisualBarCompare`, `DualStageKnowledgeLayout`).

## 0. BẢN ĐỒ "KỊCH BẢN NÓI GÌ → GỌI MÓN ĐÓ" (BẮT BUỘC TRA TRƯỚC KHI DỰNG)
- **Trích điều luật / văn bản / bài báo / tài liệu mật:** `ForensicHighlighter` *(quẹt bút dạ quang vàng/đỏ hoặc bóc vạch đen)*
- **Xâu chuỗi 2–4 bằng chứng / mối liên hệ mắt xích:** `EvidenceStringBoard` *(ảnh rửa nghiêng + ghim dây đỏ)*
- **Lột tả bề nổi bên ngoài vs. bản chất/cấu tạo bên trong:** `XRayPeelReveal` *(đường quét mảnh trượt ngang bóc lớp)*
- **Chi tiết đời thật: hóa đơn / thông báo điện thoại / nút gạt ẩn / chữ nhỏ điều khoản:** `RealLifeArtifact` *(zoom cận cảnh chi tiết đắt giá)*
- **Cơ chế vận hành: phễu lọc / cổ chai / vòng lặp / đòn bẩy:** `BlueprintMechanism` *(bản vẽ nét mảnh SVG trực tiếp lên nền lưới, 0 hộp nền)*
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

## 1. KHUNG THƯƠNG HIỆU, CTA KẾT VIDEO, CAMERA & CHUYỂN CẢNH (11 MÓN)
- `HaDaWhyMistBackground` | `import { HaDaWhyMistBackground } from "./components/HaDaWhyMistBackground"`
  Props: `{ intensity?: number; accentHex?: string; gridOpacity?: number }`
- `HaDaWhyOutroCTA` | `import { HaDaWhyOutroCTA } from "./components/HaDaWhyOutroCTA"`
  Props: `{ durationFrames?: number; logoSrc?: string; channelName?: string; subLabel?: string; shareLabel?: string; top?: number }` — **CTA kết video DUY NHẤT cho toàn kênh (mặc định `210f` = 3.5s cuối, `top: 1210`, Logo 3D + 2 nút 3D chuẩn YouTube ĐĂNG KÝ & CHIA SẺ, khớp 3 mốc SFX tự động `+0ms / +700ms / +1300ms`). BẮT BUỘC đặt ngay trước `<ChannelWatermark9x16 />`, CẤM AI tự chế outro khác.**
- `ChannelWatermark9x16` | `import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16"`
  Props: `{ logoSrc?: string; outroHideFrames?: number }` — **Đủ 2 lớp (`zIndex: 9999`: Logo góc trên trái `top: 105, left: 44` + Logo chìm chống re-up vùng thấp `top: 1360, width: 280, opacity: 0.05`, tự mờ về `0` trong `210f` cuối để không đè `HaDaWhyOutroCTA`), BẮT BUỘC đặt dòng cuối ngay trước `</AbsoluteFill>`.**
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

## 2. ĐỒ CHƠI ĐỜI THẬT, CHIỀU SÂU 2.5D / 3D & BỐ CỤC SÂN KHẤU MỞ (14 MÓN — `import { ... } from "./components/fx"`)
- `ForensicHighlighter`: `{ imageSrc?: string; documentHeader?: string; lines?: string[]; highlightLineIndex?: number; mode?: "highlighter"|"redaction_peel"; highlightColor?: "yellow"|"red"; triggerFrame?: number; top?: number; width?: number }`
- `EvidenceStringBoard`: `{ nodes: { imageSrc: string; label: string; x?: number; y?: number; tiltDeg?: number; triggerFrame: number }[]; top?: number; height?: number }`
- `XRayPeelReveal`: `{ outerImageSrc: string; innerImageSrc: string; outerLabel?: string; innerLabel?: string; revealFrame?: number; sweepDurationFrames?: number; top?: number; width?: number; height?: number }`
- `RealLifeArtifact`: `{ variant: "receipt"|"notification"|"hidden_toggle"|"fine_print"; title: string; rows?: { label: string; value?: string; isFocus?: boolean }[]; bodyText?: string; toggleInitialOn?: boolean; focusFrame?: number; top?: number; width?: number }`
- `BlueprintMechanism`: `{ mode: "funnel"|"bottleneck"|"loop"|"lever"; inputLabel: string; coreLabel: string; outputLabel: string; inputImageSrc?: string; outputImageSrc?: string; triggerFrame?: number; top?: number; width?: number; height?: number }`
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
