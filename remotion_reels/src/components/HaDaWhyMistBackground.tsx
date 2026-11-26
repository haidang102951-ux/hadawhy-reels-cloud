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
