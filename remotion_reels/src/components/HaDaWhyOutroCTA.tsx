import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ensureFxFonts } from "./fx/fxFonts";

ensureFxFonts();

export interface HaDaWhyOutroCTAProps {
  /** Thời lượng xuất hiện ở cuối video (mặc định 210 frames = 3.5s @ 60fps) */
  durationFrames?: number;
  /** Đường dẫn logo kênh trong public/ */
  logoSrc?: string;
  /** Tên kênh hiển thị (chữ WHY tự động tô #22B8FF) */
  channelName?: string;
  /** Nhãn nút Đăng ký */
  subLabel?: string;
  /** Nhãn nút Chia sẻ */
  shareLabel?: string;
  /** Vị trí Y trên khung hình 1080x1920 (mặc định 1210 — gọn nửa dưới Safe Zone) */
  top?: number;
}

/**
 * HaDaWhyOutroCTA — Component CTA kết video DUY NHẤT cho toàn kênh HaDa Why (60fps GPU).
 * - Khớp chuẩn 3 mốc SFX tự động trong engine/sfx_timeline_mixer.py:
 *   1. localFrame = 0  (+0ms): Thẻ CTA & Logo trượt lên
 *   2. localFrame = 42 (+700ms): Nút ĐĂNG KÝ nhún bấm + chuông 3D lắc 2 nhịp
 *   3. localFrame = 78 (+1300ms): Nút CHIA SẺ nhún bấm
 * - Tuyệt đối không dùng neon glow (chỉ dùng bóng đổ đen rgba(0,0,0,0.65..0.85)).
 */
export const HaDaWhyOutroCTA: React.FC<HaDaWhyOutroCTAProps> = ({
  durationFrames = 210,
  logoSrc = "brand/hadawhy_logo.png",
  channelName = "HaDa WHY",
  subLabel = "ĐĂNG KÝ",
  shareLabel = "CHIA SẺ",
  top = 1210,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const startFrame = Math.max(0, durationInFrames - durationFrames);
  if (frame < startFrame) return null;

  const localFrame = frame - startFrame;
  const resolvedLogo = /^(https?:|data:|\/)/i.test(logoSrc) ? logoSrc : staticFile(logoSrc);

  // 1. Thẻ tổng & Logo trượt lên mượt bằng spring
  const cardSpring = spring({
    frame: localFrame,
    fps,
    config: { damping: 17, stiffness: 190, mass: 0.78 },
  });
  const cardY = interpolate(cardSpring, [0, 1], [68, 0]);
  const cardOpacity = interpolate(localFrame, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Nghiêng 3D nhẹ cho Logo + vệt sáng kim loại trắng mảnh quét ngang
  const logoTiltX = interpolate(cardSpring, [0, 1], [18, 4]);
  const sheenPos = interpolate(localFrame, [10, 36], [-110, 140], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // 2. Nút ĐĂNG KÝ bật lên (localFrame = 6) & nhún bấm + lắc chuông tại localFrame = 42 (+700ms)
  const subEnter = spring({
    frame: Math.max(0, localFrame - 6),
    fps,
    config: { damping: 15, stiffness: 220, mass: 0.7 },
  });
  const subEnterY = interpolate(subEnter, [0, 1], [24, 0]);
  const subPressScale = interpolate(
    localFrame,
    [40, 44, 50],
    [1, 0.93, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const bellRotate = interpolate(
    localFrame,
    [42, 46, 51, 56, 61, 66],
    [0, -14, 12, -10, 8, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  // 3. Nút CHIA SẺ bật lên trễ 8 frames sau nút Đăng ký (localFrame = 14) & nhún bấm tại localFrame = 78 (+1300ms)
  const shareEnter = spring({
    frame: Math.max(0, localFrame - 14),
    fps,
    config: { damping: 15, stiffness: 220, mass: 0.7 },
  });
  const shareEnterY = interpolate(shareEnter, [0, 1], [24, 0]);
  const sharePressScale = interpolate(
    localFrame,
    [76, 80, 86],
    [1, 0.93, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  // Tách chữ WHY màu #22B8FF nếu tên kênh chứa WHY
  const renderChannelName = () => {
    const match = channelName.match(/^(.*?)(\bWHY\b)(.*)$/i);
    if (!match) {
      return <span style={{ color: "#FFFFFF" }}>{channelName}</span>;
    }
    return (
      <>
        <span style={{ color: "#FFFFFF" }}>{match[1]}</span>
        <span style={{ color: "#22B8FF" }}>{match[2]}</span>
        <span style={{ color: "#FFFFFF" }}>{match[3]}</span>
      </>
    );
  };

  return (
    <div
      data-layer="hadawhy-outro-cta"
      style={{
        position: "absolute",
        left: "50%",
        top,
        width: 680,
        borderRadius: 28,
        padding: "28px 34px 30px 34px",
        background: "linear-gradient(180deg, rgba(13,35,66,0.92) 0%, rgba(6,18,36,0.96) 100%)",
        border: "1.5px solid rgba(66,178,242,0.35)",
        boxShadow: "0 24px 48px rgba(0,0,0,0.75)",
        opacity: cardOpacity,
        transform: `translate3d(-50%, ${cardY.toFixed(2)}px, 0)`,
        willChange: "transform, opacity",
        zIndex: 9990,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 24,
      }}
    >
      {/* HÀNG TRÊN: Logo kênh 3D + vệt sáng kim loại mảnh + tên kênh */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 20,
        }}
      >
        <div
          style={{
            position: "relative",
            width: 72,
            height: 72,
            borderRadius: 18,
            overflow: "hidden",
            transform: `perspective(900px) rotateX(${logoTiltX.toFixed(2)}deg) translate3d(0, 0, 0)`,
            boxShadow: "0 10px 22px rgba(0,0,0,0.7)",
            backgroundColor: "#061224",
            border: "1px solid rgba(255,255,255,0.14)",
            flexShrink: 0,
          }}
        >
          <Img
            src={resolvedLogo}
            style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }}
          />
          {/* Vệt sáng kim loại trắng mảnh quét ngang */}
          <div
            style={{
              position: "absolute",
              top: -12,
              bottom: -12,
              left: 0,
              width: 22,
              background:
                "linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.55) 50%, rgba(255,255,255,0) 100%)",
              transform: `translate3d(${sheenPos.toFixed(1)}px, 0, 0) skewX(-22deg)`,
              pointerEvents: "none",
            }}
          />
        </div>

        <div
          style={{
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: 34,
            letterSpacing: "0.02em",
            lineHeight: 1.05,
            textShadow: "0 4px 12px rgba(0,0,0,0.8)",
            whiteSpace: "nowrap",
          }}
        >
          {renderChannelName()}
        </div>
      </div>

      {/* HÀNG DƯỚI: 2 nút Icon 3D chuẩn YouTube đặt song song */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 28,
          width: "100%",
        }}
      >
        {/* NÚT ĐĂNG KÝ 3D CHUẨN YOUTUBE */}
        <div
          style={{
            flex: 1,
            height: 68,
            borderRadius: 18,
            background: "linear-gradient(180deg, #FF1A1A 0%, #CC0000 100%)",
            borderBottom: "5px solid #7A0000",
            boxShadow: "0 12px 24px rgba(0,0,0,0.65)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 12,
            opacity: interpolate(localFrame, [6, 14], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
            transform: `translate3d(0, ${subEnterY.toFixed(2)}px, 0) scale(${subPressScale.toFixed(4)})`,
            willChange: "transform, opacity",
          }}
        >
          {/* Icon SVG 3D chuông thông báo chuẩn YouTube (lớp vát xám bạc #D4D4D8 + mặt trước #FFFFFF) */}
          <svg
            width={30}
            height={30}
            viewBox="0 0 28 28"
            style={{
              transform: `rotate(${bellRotate.toFixed(2)}deg)`,
              transformOrigin: "14px 4px",
              willChange: "transform",
              flexShrink: 0,
            }}
          >
            {/* Lớp vát chiều dày 3D */}
            <path
              d="M14 4.2c-3.8 0-6.8 3-6.8 6.8v4.3l-1.9 2.3c-.4.5-.1 1.2.6 1.2h16.2c.7 0 1-.7.6-1.2l-1.9-2.3V11c0-3.8-3-6.8-6.8-6.8zm0 19.6c1.5 0 2.7-1.1 2.9-2.5h-5.8c.2 1.4 1.4 2.5 2.9 2.5z"
              fill="#D4D4D8"
              transform="translate(1.8, 1.8)"
            />
            {/* Mặt trước trắng sắc nét */}
            <path
              d="M14 4.2c-3.8 0-6.8 3-6.8 6.8v4.3l-1.9 2.3c-.4.5-.1 1.2.6 1.2h16.2c.7 0 1-.7.6-1.2l-1.9-2.3V11c0-3.8-3-6.8-6.8-6.8zm0 19.6c1.5 0 2.7-1.1 2.9-2.5h-5.8c.2 1.4 1.4 2.5 2.9 2.5z"
              fill="#FFFFFF"
            />
          </svg>
          <span
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 22,
              color: "#FFFFFF",
              letterSpacing: "0.04em",
              whiteSpace: "nowrap",
              textShadow: "0 2px 6px rgba(0,0,0,0.65)",
            }}
          >
            {subLabel}
          </span>
        </div>

        {/* NÚT CHIA SẺ 3D CHUẨN YOUTUBE */}
        <div
          style={{
            flex: 1,
            height: 68,
            borderRadius: 18,
            background: "linear-gradient(180deg, #2B2B2B 0%, #1C1C1C 100%)",
            border: "1px solid rgba(255,255,255,0.18)",
            borderBottom: "5px solid #0A0A0A",
            boxShadow: "0 12px 24px rgba(0,0,0,0.65)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 12,
            opacity: interpolate(localFrame, [14, 22], [0, 1], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
            transform: `translate3d(0, ${shareEnterY.toFixed(2)}px, 0) scale(${sharePressScale.toFixed(4)})`,
            willChange: "transform, opacity",
          }}
        >
          {/* Icon SVG 3D mũi tên cong rẽ phải chuẩn YouTube Share (2 lớp nổi khối lệch 2px) */}
          <svg
            width={30}
            height={30}
            viewBox="0 0 28 28"
            style={{ flexShrink: 0 }}
          >
            <path
              d="M16.5 6.2V10.6C10.2 11.4 6.2 15.2 4.8 21.2C7.8 18.1 11.5 16.8 16.5 16.8V21.2L24.2 13.7L16.5 6.2Z"
              fill="#9CA3AF"
              transform="translate(2, 2)"
            />
            <path
              d="M16.5 6.2V10.6C10.2 11.4 6.2 15.2 4.8 21.2C7.8 18.1 11.5 16.8 16.5 16.8V21.2L24.2 13.7L16.5 6.2Z"
              fill="#FFFFFF"
            />
          </svg>
          <span
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 22,
              color: "#FFFFFF",
              letterSpacing: "0.04em",
              whiteSpace: "nowrap",
              textShadow: "0 2px 6px rgba(0,0,0,0.65)",
            }}
          >
            {shareLabel}
          </span>
        </div>
      </div>
    </div>
  );
};
