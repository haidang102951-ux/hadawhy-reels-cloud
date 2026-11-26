import React from "react";
import { Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface ChannelWatermark9x16Props {
  logoSrc?: string;
  /** Số frame cuối tự ẩn lớp logo chìm để không đè lên HaDaWhyOutroCTA (mặc định 210 = 3.5s @ 60fps) */
  outroHideFrames?: number;
}

/**
 * Hệ thống 2 lớp thương hiệu & chống re-up bắt buộc (LUÔN nổi trên cùng zIndex: 9999):
 * - Lớp 1 (Nhận diện góc): Logo góc trên bên trái cố định (top: 105, left: 44 — né thanh trạng thái điện thoại).
 * - Lớp 2 (Logo chìm chống bản quyền): Căn giữa ngang, vùng thấp (top: 1360),
 *   width: 280px, opacity: 0.05, blur(0.6px), trôi siêu chậm ngang ±45px, dọc ±10px bằng translate3d;
 *   tự mờ về 0 trong 210 frames cuối để không đè lên <HaDaWhyOutroCTA />.
 * CẤM tự ý gỡ bỏ hoặc tắt lớp logo chìm chống bản quyền.
 */
export const ChannelWatermark9x16: React.FC<ChannelWatermark9x16Props> = ({
  logoSrc = "brand/hadawhy_logo.png",
  outroHideFrames = 210,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / Math.max(1, fps);
  const driftX = Math.sin(t * 0.35) * 45;
  const driftY = Math.cos(t * 0.27) * 10;
  const resolvedLogo = staticFile(logoSrc);

  // Tự mờ về opacity: 0 trong đúng 210 frames cuối khi HaDaWhyOutroCTA xuất hiện
  const ctaStart = Math.max(0, durationInFrames - outroHideFrames);
  const stealthFade =
    durationInFrames > outroHideFrames
      ? interpolate(frame, [Math.max(0, ctaStart - 12), ctaStart], [1, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : 1;
  const baseStealthOpacity = 0.05;
  const currentStealthOpacity = baseStealthOpacity * stealthFade;

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
      {/* LỚP 1: Logo nhận diện góc trên bên trái (né thanh trạng thái điện thoại) */}
      <div
        style={{
          position: "absolute",
          top: 105,
          left: 44,
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

      {/* LỚP 2: Logo chìm chống bản quyền ở vùng thấp (opacity: 0.05, tự mờ về 0 trong 210f cuối) */}
      <div
        data-layer="stealth-watermark"
        style={{
          position: "absolute",
          left: "50%",
          top: 1360,
          width: 280,
          opacity: currentStealthOpacity,
          filter: "blur(0.6px)",
          transform: `translate3d(calc(-50% + ${driftX.toFixed(2)}px), calc(-50% + ${driftY.toFixed(2)}px), 0)`,
          willChange: "transform, opacity",
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
