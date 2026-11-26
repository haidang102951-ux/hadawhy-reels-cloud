import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ensureFxFonts } from "./fxFonts";

ensureFxFonts();

export interface EvidenceBoardNode {
  imageSrc: string;
  label: string;
  /** Tọa độ tâm X trong khung board (0..960) */
  x?: number;
  /** Tọa độ tâm Y trong khung board (0..960) */
  y?: number;
  /** Góc nghiêng tự nhiên của ảnh rửa (-4..4 độ) */
  tiltDeg?: number;
  /** Frame xuất hiện ảnh và kéo dây đỏ nối từ mắt xích trước */
  triggerFrame: number;
}

export interface EvidenceStringBoardProps {
  nodes: EvidenceBoardNode[];
  top?: number;
  height?: number;
}

const resolveAsset = (src: string): string =>
  /^(https?:|data:|\/)/i.test(src) ? src : staticFile(src);

const DEFAULT_POSITIONS: Record<number, Array<{ x: number; y: number; tilt: number }>> = {
  2: [
    { x: 260, y: 270, tilt: -3.2 },
    { x: 700, y: 610, tilt: 2.8 },
  ],
  3: [
    { x: 250, y: 220, tilt: -3.5 },
    { x: 720, y: 420, tilt: 3.1 },
    { x: 280, y: 710, tilt: -2.4 },
  ],
  4: [
    { x: 245, y: 210, tilt: -3.2 },
    { x: 715, y: 245, tilt: 2.9 },
    { x: 260, y: 690, tilt: 2.5 },
    { x: 705, y: 725, tilt: -3.1 },
  ],
};

/**
 * EvidenceStringBoard — Đặt 2–4 ảnh chụp thật nghiêng nhẹ 2–4 độ như ảnh rửa thật có bóng đổ tự nhiên,
 * căng sợi dây đỏ mảnh nối các mắt xích đúng theo từng triggerFrame. Không hộp kính nhựa, không neon.
 */
export const EvidenceStringBoard: React.FC<EvidenceStringBoardProps> = ({
  nodes,
  top = 340,
  height = 960,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const clampedNodes = nodes.slice(0, 4);
  const preset = DEFAULT_POSITIONS[clampedNodes.length] || DEFAULT_POSITIONS[3];

  const resolvedNodes = clampedNodes.map((n, i) => {
    const p = preset[i] || { x: 480, y: 480, tilt: 0 };
    return {
      ...n,
      x: n.x ?? p.x,
      y: n.y ?? p.y,
      tiltDeg: n.tiltDeg ?? p.tilt,
    };
  });

  const cardW = clampedNodes.length >= 4 ? 360 : 390;
  const cardH = clampedNodes.length >= 4 ? 270 : 295;

  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        top,
        width: 960,
        height,
        transform: "translate3d(-50%, 0, 0)",
        willChange: "transform",
      }}
    >
      {/* Sợi dây đỏ mảnh nối các đinh ghim giữa các ảnh */}
      <svg
        width={960}
        height={height}
        viewBox={`0 0 960 ${height}`}
        style={{ position: "absolute", inset: 0, zIndex: 20, pointerEvents: "none", overflow: "visible" }}
      >
        {resolvedNodes.map((node, idx) => {
          if (idx === 0) return null;
          const prev = resolvedNodes[idx - 1];
          const x1 = prev.x;
          const y1 = prev.y - cardH / 2 + 18;
          const x2 = node.x;
          const y2 = node.y - cardH / 2 + 18;
          const dx = x2 - x1;
          const dy = y2 - y1;
          const length = Math.hypot(dx, dy);
          const progress = interpolate(
            frame,
            [node.triggerFrame, node.triggerFrame + 18],
            [0, 1],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
          );
          if (progress <= 0) return null;
          const dashOffset = length * (1 - progress);
          return (
            <g key={`wire-${idx}`}>
              <line
                x1={x1}
                y1={y1 + 5}
                x2={x2}
                y2={y2 + 5}
                stroke="rgba(0, 0, 0, 0.45)"
                strokeWidth={4}
                strokeDasharray={length}
                strokeDashoffset={dashOffset}
                strokeLinecap="round"
              />
              <line
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke="#DC2626"
                strokeWidth={3.5}
                strokeDasharray={length}
                strokeDashoffset={dashOffset}
                strokeLinecap="round"
              />
            </g>
          );
        })}
      </svg>

      {/* Các tấm ảnh rửa thật có viền giấy trắng mỏng, đinh ghim đỏ và bóng đổ */}
      {resolvedNodes.map((node, idx) => {
        const localF = frame - node.triggerFrame;
        if (localF < 0) return null;

        const popP = spring({
          frame: localF,
          fps,
          config: { damping: 16, stiffness: 210, mass: 0.75 },
        });
        const scale = interpolate(popP, [0, 1], [1.14, 1]);
        const opacity = interpolate(localF, [0, 8], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });

        return (
          <div
            key={`card-${idx}`}
            style={{
              position: "absolute",
              left: node.x - cardW / 2,
              top: node.y - cardH / 2,
              width: cardW,
              backgroundColor: "#F8F6F0",
              padding: "12px 12px 18px 12px",
              borderRadius: 3,
              boxShadow: "0 20px 42px rgba(0, 0, 0, 0.65), 0 4px 10px rgba(0, 0, 0, 0.38)",
              opacity,
              transform: `translate3d(0, 0, 0) scale(${scale.toFixed(4)}) rotate(${node.tiltDeg}deg)`,
              willChange: "transform, opacity",
              zIndex: 10 + idx,
            }}
          >
            {/* Đinh ghim đỏ trên đỉnh ảnh */}
            <div
              style={{
                position: "absolute",
                left: "50%",
                top: 8,
                width: 18,
                height: 18,
                borderRadius: 999,
                backgroundColor: "#B91C1C",
                border: "2px solid #FCA5A5",
                boxShadow: "0 4px 8px rgba(0,0,0,0.6)",
                transform: "translate3d(-50%, 0, 0)",
                zIndex: 30,
              }}
            />

            {/* Ảnh chụp thật giữ nguyên tỉ lệ contain */}
            <div
              style={{
                width: "100%",
                height: cardH - 68,
                backgroundColor: "#0B1220",
                overflow: "hidden",
                borderRadius: 2,
              }}
            >
              <Img
                src={resolveAsset(node.imageSrc)}
                style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }}
              />
            </div>

            {/* Nhãn ngắn 2–4 từ trên mép ảnh rửa */}
            <div
              style={{
                marginTop: 12,
                textAlign: "center",
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 22,
                color: "#0F172A",
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
              }}
            >
              {node.label}
            </div>
          </div>
        );
      })}
    </div>
  );
};
