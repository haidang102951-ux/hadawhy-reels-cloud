import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ensureFxFonts } from "./fxFonts";

ensureFxFonts();

export interface ForensicHighlighterProps {
  /** Đường dẫn ảnh chụp tài liệu/bài báo thật (tùy chọn, nếu có sẽ hiển thị làm nền trang giấy) */
  imageSrc?: string;
  /** Tiêu đề/nguồn tài liệu ngắn (VD: "ĐIỀU 15 — NGHỊ ĐỊNH 168") */
  documentHeader?: string;
  /** Các dòng trích đoạn văn bản thật (3–5 dòng) */
  lines?: string[];
  /** Chỉ số dòng quan trọng cần zoom & quẹt bút dạ quang (0-based) */
  highlightLineIndex?: number;
  /** Chế độ: "highlighter" (quẹt bút dạ quang vàng/đỏ) hoặc "redaction_peel" (bóc vạch đen tài liệu mật) */
  mode?: "highlighter" | "redaction_peel";
  /** Màu bút dạ quang: "yellow" | "red" */
  highlightColor?: "yellow" | "red";
  /** Frame bắt đầu quẹt bút / bóc vạch đen và zoom camera */
  triggerFrame?: number;
  /** Vị trí Y trên khung hình 1080x1920 */
  top?: number;
  /** Bề rộng tờ tài liệu */
  width?: number;
}

const resolveAsset = (src: string): string =>
  /^(https?:|data:|\/)/i.test(src) ? src : staticFile(src);

/**
 * ForensicHighlighter — Hiện trích đoạn văn bản / điều luật / bài báo thật có vân giấy nhẹ;
 * camera zoom mượt vào 1 dòng quan trọng và quẹt nét bút dạ quang vàng/đỏ tự nhiên
 * (hoặc bóc vạch đen tài liệu mật) theo triggerFrame. Không hộp nhựa, không neon.
 */
export const ForensicHighlighter: React.FC<ForensicHighlighterProps> = ({
  imageSrc,
  documentHeader = "TRÍCH LỤC HỒ SƠ",
  lines = [
    "Mọi điều khoản phụ đều có hiệu lực ngay khi ký.",
    "Khoản phí ẩn tự động khấu trừ sau 30 ngày dùng thử.",
    "Người dùng chỉ có 72 giờ để gửi yêu cầu hoàn tiền.",
  ],
  highlightLineIndex = 1,
  mode = "highlighter",
  highlightColor = "yellow",
  triggerFrame = 18,
  top = 420,
  width = 920,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enterP = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 170, mass: 0.7 },
  });
  const enterY = interpolate(enterP, [0, 1], [36, 0]);
  const enterOpacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Camera zoom mượt vào dòng quan trọng khi tới triggerFrame
  const zoomP = spring({
    frame: Math.max(0, frame - triggerFrame),
    fps,
    config: { damping: 20, stiffness: 130, mass: 0.9 },
  });
  const swipeP = interpolate(frame, [triggerFrame + 2, triggerFrame + 24], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const safeIdx = Math.max(0, Math.min(lines.length - 1, highlightLineIndex));
  const zoomScale = 1 + zoomP * 0.085;
  const focusShiftY = -zoomP * ((safeIdx - (lines.length - 1) / 2) * 34);
  const tiltDeg = interpolate(zoomP, [0, 1], [-1.2, -0.3]);

  const markerBg =
    highlightColor === "red"
      ? "rgba(239, 68, 68, 0.38)"
      : "rgba(250, 204, 21, 0.56)";

  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        top,
        width,
        opacity: enterOpacity,
        transform: `translate3d(-50%, ${(enterY + focusShiftY).toFixed(2)}px, 0) scale(${zoomScale.toFixed(4)}) rotate(${tiltDeg.toFixed(2)}deg)`,
        willChange: "transform, opacity",
      }}
    >
      {/* Tờ giấy thật có vân giấy nhẹ và bóng đổ tự nhiên */}
      <div
        style={{
          position: "relative",
          backgroundColor: "#F3EFE6",
          backgroundImage:
            "repeating-linear-gradient(0deg, rgba(15, 23, 42, 0.028) 0px, rgba(15, 23, 42, 0.028) 1px, transparent 1px, transparent 36px)",
          borderRadius: 6,
          padding: "36px 44px 42px 44px",
          boxShadow: "0 24px 55px rgba(0, 0, 0, 0.65), 0 4px 12px rgba(0, 0, 0, 0.35)",
          border: "1px solid rgba(255, 255, 255, 0.35)",
          overflow: "hidden",
        }}
      >
        {imageSrc && (
          <div
            style={{
              position: "relative",
              width: "100%",
              height: 240,
              marginBottom: 24,
              borderRadius: 4,
              overflow: "hidden",
              backgroundColor: "#141A24",
              border: "1px solid rgba(15, 23, 42, 0.16)",
            }}
          >
            <Img
              src={resolveAsset(imageSrc)}
              style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }}
            />
          </div>
        )}

        {/* Tiêu đề hồ sơ */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            borderBottom: "2px solid rgba(15, 23, 42, 0.22)",
            paddingBottom: 14,
            marginBottom: 24,
          }}
        >
          <span
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 24,
              color: "#1E293B",
              letterSpacing: "0.06em",
              textTransform: "uppercase",
            }}
          >
            {documentHeader}
          </span>
          <span
            style={{
              fontFamily: "BeVietnamProExtraBold, sans-serif",
              fontSize: 18,
              color: "#64748B",
            }}
          >
            TRÍCH YẾU
          </span>
        </div>

        {/* Các dòng văn bản */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          {lines.map((line, idx) => {
            const isTarget = idx === safeIdx;
            const dimOpacity = isTarget ? 1 : interpolate(zoomP, [0, 1], [0.85, 0.42]);
            return (
              <div
                key={idx}
                style={{
                  position: "relative",
                  padding: "6px 10px",
                  opacity: dimOpacity,
                }}
              >
                {/* Nét quẹt bút dạ quang tự nhiên */}
                {isTarget && mode === "highlighter" && (
                  <div
                    style={{
                      position: "absolute",
                      left: 0,
                      top: 4,
                      bottom: 4,
                      width: `${(swipeP * 100).toFixed(2)}%`,
                      backgroundColor: markerBg,
                      borderRadius: "4px 8px 3px 6px",
                      transform: "skewX(-6deg)",
                      zIndex: 0,
                    }}
                  />
                )}

                <span
                  style={{
                    position: "relative",
                    zIndex: 1,
                    fontFamily: isTarget
                      ? "BeVietnamProBlack, sans-serif"
                      : "BeVietnamProExtraBold, sans-serif",
                    fontSize: isTarget ? 32 : 26,
                    lineHeight: 1.38,
                    color: "#0F172A",
                    display: "block",
                  }}
                >
                  {line}
                </span>

                {/* Vạch đen tài liệu mật được bóc ra từ trái sang phải */}
                {isTarget && mode === "redaction_peel" && (
                  <div
                    style={{
                      position: "absolute",
                      right: 0,
                      top: 2,
                      bottom: 2,
                      width: `${((1 - swipeP) * 100).toFixed(2)}%`,
                      backgroundColor: "#0B0F19",
                      zIndex: 2,
                      boxShadow: "-4px 0 12px rgba(0,0,0,0.45)",
                    }}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
