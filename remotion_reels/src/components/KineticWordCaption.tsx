import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface WordToken {
  text: string;
  startSec: number;
  endSec: number;
  color?: string;
}

export interface CaptionPhrase {
  startSec: number;
  endSec: number;
  lines: WordToken[][];
}

// ============================================================================
// QUY TẮC PHỐI MÀU 80/20 (TUYỆT ĐỐI TỐI ĐA 2 MÀU TRÊN MÀN HÌNH Ở MỌI THỜI ĐIỂM):
// - 80% chữ BẮT BUỘC là Trắng tinh (#FFFFFF).
// - Trong mỗi câu (Phrase), CHỈ DUY NHẤT 1 cụm từ khóa đắt giá nhất được tô
//   1 màu nhấn duy nhất (HOẶC Vàng #FFE600, HOẶC Đỏ #FF3B47 - không bao giờ trộn cả 2).
// - Đảm bảo 100% Zero-Box (không có hộp nền chữ).
// ============================================================================
export const MASTER_20S_PHRASES: CaptionPhrase[] = [
  // PHRASE 1 (0.00s - 2.38s): White + Gold (#FFE600)
  {
    startSec: 0.0,
    endSec: 2.38,
    lines: [
      [
        { text: "THỰC", startSec: 0.0, endSec: 0.16, color: "#FFFFFF" },
        { text: "HƯ", startSec: 0.16, endSec: 0.28, color: "#FFFFFF" },
        { text: "VỤ", startSec: 0.28, endSec: 0.44, color: "#FFFFFF" },
        { text: "KIỆN", startSec: 0.44, endSec: 0.66, color: "#FFFFFF" },
      ],
      [
        { text: "250", startSec: 0.66, endSec: 1.1, color: "#FFE600" },
        { text: "TRIỆU", startSec: 1.1, endSec: 1.46, color: "#FFE600" },
        { text: "ĐÔ", startSec: 1.46, endSec: 1.58, color: "#FFE600" },
        { text: "VIETJET", startSec: 1.68, endSec: 2.15, color: "#FFFFFF" },
      ],
    ],
  },
  // PHRASE 2A (2.38s - 4.50s): White + Red (#FF3B47)
  {
    startSec: 2.38,
    endSec: 4.5,
    lines: [
      [
        { text: "KHI", startSec: 2.5, endSec: 2.62, color: "#FFFFFF" },
        { text: "DỊCH", startSec: 2.62, endSec: 2.78, color: "#FFFFFF" },
        { text: "BỆNH", startSec: 2.78, endSec: 2.96, color: "#FFFFFF" },
        { text: "ẬP", startSec: 2.96, endSec: 3.06, color: "#FFFFFF" },
        { text: "TỚI,", startSec: 3.06, endSec: 3.3, color: "#FFFFFF" },
      ],
      [
        { text: "TÀU", startSec: 3.72, endSec: 3.82, color: "#FFFFFF" },
        { text: "BAY", startSec: 3.82, endSec: 3.95, color: "#FFFFFF" },
        { text: "NẰM", startSec: 3.95, endSec: 4.16, color: "#FF3B47" },
        { text: "ĐẤT", startSec: 4.16, endSec: 4.4, color: "#FF3B47" },
      ],
    ],
  },
  // PHRASE 2B (4.50s - 5.88s): White + Gold (#FFE600)
  {
    startSec: 4.5,
    endSec: 5.88,
    lines: [
      [
        { text: "DOANH", startSec: 4.64, endSec: 4.78, color: "#FFFFFF" },
        { text: "THU", startSec: 4.78, endSec: 4.92, color: "#FFFFFF" },
      ],
      [
        { text: "KHÔNG", startSec: 4.92, endSec: 5.1, color: "#FFE600" },
        { text: "VỀ", startSec: 5.1, endSec: 5.24, color: "#FFE600" },
        { text: "KÉT!", startSec: 5.24, endSec: 5.65, color: "#FFE600" },
      ],
    ],
  },
  // PHRASE 3 (5.88s - 7.88s): White + Gold (#FFE600)
  {
    startSec: 5.88,
    endSec: 7.88,
    lines: [
      [
        { text: "MỖI", startSec: 6.04, endSec: 6.2, color: "#FFFFFF" },
        { text: "THÁNG", startSec: 6.2, endSec: 6.38, color: "#FFFFFF" },
        { text: "TIỀN", startSec: 6.38, endSec: 6.6, color: "#FFFFFF" },
        { text: "THUÊ", startSec: 6.6, endSec: 6.82, color: "#FFFFFF" },
      ],
      [
        { text: "VẪN", startSec: 6.82, endSec: 7.0, color: "#FFFFFF" },
        { text: "PHẢI", startSec: 7.0, endSec: 7.18, color: "#FFFFFF" },
        { text: "TRẢ", startSec: 7.18, endSec: 7.38, color: "#FFE600" },
        { text: "ĐỦ", startSec: 7.38, endSec: 7.68, color: "#FFE600" },
      ],
    ],
  },
  // PHRASE 4 (7.88s - 11.10s): White + Red (#FF3B47)
  {
    startSec: 7.88,
    endSec: 11.1,
    lines: [
      [
        { text: "NGÂN", startSec: 8.0, endSec: 8.15, color: "#FFFFFF" },
        { text: "HÀNG", startSec: 8.15, endSec: 8.38, color: "#FFFFFF" },
        { text: "CẮT", startSec: 8.48, endSec: 8.66, color: "#FF3B47" },
        { text: "HỢP", startSec: 8.66, endSec: 8.84, color: "#FF3B47" },
        { text: "ĐỒNG,", startSec: 8.84, endSec: 9.08, color: "#FF3B47" },
      ],
      [
        { text: "BÁN", startSec: 9.15, endSec: 9.5, color: "#FFFFFF" },
        { text: "NỢ", startSec: 9.75, endSec: 10.12, color: "#FFFFFF" },
        { text: "CHO", startSec: 10.12, endSec: 10.26, color: "#FFFFFF" },
        { text: "QUỸ", startSec: 10.26, endSec: 10.44, color: "#FFFFFF" },
        { text: "NGOẠI", startSec: 10.44, endSec: 10.85, color: "#FFFFFF" },
      ],
    ],
  },
  // PHRASE 5 (11.10s - 15.65s): White + Gold (#FFE600)
  {
    startSec: 11.1,
    endSec: 15.65,
    lines: [
      [
        { text: "KIỆN", startSec: 11.95, endSec: 12.36, color: "#FFFFFF" },
        { text: "TỪ", startSec: 12.36, endSec: 12.5, color: "#FFFFFF" },
        { text: "VIỆT", startSec: 12.5, endSec: 12.66, color: "#FFE600" },
        { text: "NAM", startSec: 12.66, endSec: 12.9, color: "#FFE600" },
        { text: "SANG", startSec: 12.9, endSec: 13.2, color: "#FFFFFF" },
      ],
      [
        { text: "TÒA", startSec: 13.3, endSec: 13.66, color: "#FFFFFF" },
        { text: "TỐI", startSec: 13.66, endSec: 13.84, color: "#FFFFFF" },
        { text: "CAO", startSec: 13.84, endSec: 14.08, color: "#FFFFFF" },
        { text: "LUÂN", startSec: 14.08, endSec: 14.28, color: "#FFE600" },
        { text: "ĐÔN!", startSec: 14.28, endSec: 15.3, color: "#FFE600" },
      ],
    ],
  },
  // PHRASE 6 (15.65s - 19.95s): White + Red (#FF3B47)
  {
    startSec: 15.65,
    endSec: 19.95,
    lines: [
      [
        { text: "TỪ", startSec: 15.9, endSec: 16.05, color: "#FFFFFF" },
        { text: "4", startSec: 16.05, endSec: 16.22, color: "#FFFFFF" },
        { text: "TÀU", startSec: 16.4, endSec: 16.54, color: "#FFFFFF" },
        { text: "BAY", startSec: 16.54, endSec: 16.68, color: "#FFFFFF" },
        { text: "THUÊ,", startSec: 16.68, endSec: 16.95, color: "#FFFFFF" },
      ],
      [
        { text: "VỌT", startSec: 18.04, endSec: 18.36, color: "#FFFFFF" },
        { text: "LÊN", startSec: 18.36, endSec: 18.48, color: "#FFFFFF" },
        { text: "250", startSec: 18.48, endSec: 19.02, color: "#FF3B47" },
        { text: "TRIỆU", startSec: 19.02, endSec: 19.44, color: "#FF3B47" },
        { text: "ĐÔ!", startSec: 19.44, endSec: 19.8, color: "#FF3B47" },
      ],
    ],
  },
  // PHRASE 7 (19.95s - 22.40s): White + Gold (#FFE600)
  {
    startSec: 19.95,
    endSec: 22.4,
    lines: [
      [
        { text: "BÀI", startSec: 20.24, endSec: 20.42, color: "#FFFFFF" },
        { text: "HỌC", startSec: 20.42, endSec: 20.56, color: "#FFFFFF" },
        { text: "ĐẮT", startSec: 20.56, endSec: 20.76, color: "#FFE600" },
        { text: "GIÁ", startSec: 20.76, endSec: 21.1, color: "#FFE600" },
      ],
      [
        { text: "SÂN", startSec: 21.35, endSec: 21.52, color: "#FFFFFF" },
        { text: "CHƠI", startSec: 21.52, endSec: 21.65, color: "#FFFFFF" },
        { text: "QUỐC", startSec: 21.65, endSec: 21.82, color: "#FFFFFF" },
        { text: "TẾ!", startSec: 21.82, endSec: 22.25, color: "#FFFFFF" },
      ],
    ],
  },
];

interface KineticWordCaptionProps {
  phrases?: CaptionPhrase[];
  placement?: "top" | "bottom";
}

export const KineticWordCaption: React.FC<KineticWordCaptionProps> = ({
  phrases = MASTER_20S_PHRASES,
  placement = "top",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentSec = frame / fps;

  const activePhrase = phrases.find(
    (p) => currentSec >= p.startSec && currentSec < p.endSec
  );

  if (!activePhrase) {
    return null;
  }

  return (
    <div
      style={{
        position: "absolute",
        ...(placement === "bottom" ? { bottom: 270 } : { top: 108 }),
        left: 0,
        right: 0,
        width: 1080,
        paddingLeft: 60,
        paddingRight: 60,
        boxSizing: "border-box",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 10,
        zIndex: 50,
        pointerEvents: "none",
      }}
    >
      {activePhrase.lines.map((line, lineIdx) => (
        <div
          key={`line-${lineIdx}`}
          style={{
            display: "flex",
            flexWrap: "nowrap",
            whiteSpace: "nowrap",
            justifyContent: "center",
            gap: 18,
          }}
        >
          {line.map((word, wIdx) => {
            const wordStartFrame = Math.round(word.startSec * fps);
            const hasStarted = frame >= wordStartFrame;
            const isSpeakingNow =
              currentSec >= word.startSec && currentSec <= word.endSec + 0.12;

            if (!hasStarted) {
              return null;
            }

            const pop = spring({
              frame: frame - wordStartFrame,
              fps,
              config: {
                damping: 12,
                stiffness: 260,
                mass: 0.5,
              },
            });

            const scale = interpolate(pop, [0, 1], [0.72, isSpeakingNow ? 1.04 : 1.0]);
            const translateY = interpolate(pop, [0, 1], [16, 0]);
            const opacity = interpolate(frame - wordStartFrame, [0, 4], [0, 1], {
              extrapolateRight: "clamp",
            });

            return (
              <span
                key={`w-${lineIdx}-${wIdx}`}
                style={{
                  display: "inline-block",
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 54,
                  fontWeight: 900,
                  lineHeight: 1.08,
                  letterSpacing: "-0.01em",
                  color: word.color || "#FFFFFF",
                  opacity,
                  transform: `translateY(${translateY}px) scale(${scale})`,
                  // ZERO-BOX: No background rectangle! Pure 3D extruded stroke + deep shadow
                  WebkitTextStroke: "9px #06080E",
                  paintOrder: "stroke fill",
                  textShadow: isSpeakingNow
                    ? `0px 6px 0px #06080E, 0px 14px 28px rgba(0,0,0,0.92), 0px 0px 26px ${word.color || "#FFFFFF"}88`
                    : "0px 6px 0px #06080E, 0px 12px 24px rgba(0,0,0,0.9)",
                }}
              >
                {word.text}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};
