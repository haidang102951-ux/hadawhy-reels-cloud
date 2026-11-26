import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ensureFxFonts } from "./fxFonts";

ensureFxFonts();

export type RealLifeArtifactVariant = "receipt" | "notification" | "hidden_toggle" | "fine_print";

export interface ArtifactRow {
  label: string;
  value?: string;
  isFocus?: boolean;
}

export interface RealLifeArtifactProps {
  /** Kiểu vật thể đời thật: hóa đơn in nhiệt | thông báo điện thoại | nút gạt ẩn | chữ nhỏ cuối điều khoản */
  variant: RealLifeArtifactVariant;
  /** Tiêu đề trên cùng của vật thể */
  title: string;
  /** Các dòng chi tiết bên trong */
  rows?: ArtifactRow[];
  /** Nội dung dòng chữ nhỏ/nội dung thông báo chính */
  bodyText?: string;
  /** Trạng thái nút gạt (cho hidden_toggle) */
  toggleInitialOn?: boolean;
  /** Frame zoom cận cảnh vào chi tiết đắt giá / gạt nút */
  focusFrame?: number;
  top?: number;
  width?: number;
}

/**
 * RealLifeArtifact — Mô phỏng vật thể/giao diện đời thật (hóa đơn in nhiệt, thông báo điện thoại,
 * nút gạt cài đặt bị ẩn, dòng chữ nhỏ cuối điều khoản) rồi zoom cận cảnh vào đúng chi tiết đắt giá.
 */
export const RealLifeArtifact: React.FC<RealLifeArtifactProps> = ({
  variant,
  title,
  rows = [
    { label: "Dịch vụ cơ bản", value: "0đ" },
    { label: "Phí nền tảng ẩn", value: "29.000đ", isFocus: true },
    { label: "Phí xử lý tự động", value: "12.000đ" },
  ],
  bodyText = "Bằng việc tiếp tục, bạn đồng ý gia hạn tự động theo biểu phí hiện hành.",
  toggleInitialOn = true,
  focusFrame = 24,
  top = 420,
  width = 820,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enterP = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 175, mass: 0.75 },
  });
  const enterY = interpolate(enterP, [0, 1], [36, 0]);
  const enterOpacity = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const zoomP = spring({
    frame: Math.max(0, frame - focusFrame),
    fps,
    config: { damping: 19, stiffness: 135, mass: 0.9 },
  });
  const scale = 1 + zoomP * 0.14;
  const focusShiftY = -zoomP * 24;

  const toggleShift = interpolate(
    frame,
    [focusFrame + 4, focusFrame + 16],
    toggleInitialOn ? [1, 0] : [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        top,
        width,
        opacity: enterOpacity,
        transform: `translate3d(-50%, ${(enterY + focusShiftY).toFixed(2)}px, 0) scale(${scale.toFixed(4)})`,
        willChange: "transform, opacity",
      }}
    >
      {variant === "receipt" && (
        <div
          style={{
            backgroundColor: "#F6F5F0",
            color: "#111827",
            padding: "36px 40px",
            borderRadius: 4,
            boxShadow: "0 24px 55px rgba(0, 0, 0, 0.68)",
            borderTop: "6px dashed #CBD5E1",
            borderBottom: "6px dashed #CBD5E1",
          }}
        >
          <div
            style={{
              textAlign: "center",
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 28,
              letterSpacing: "0.06em",
              paddingBottom: 18,
              borderBottom: "2px dashed #94A3B8",
              marginBottom: 22,
            }}
          >
            {title}
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {rows.map((r, idx) => {
              const highlight = Boolean(r.isFocus);
              return (
                <div
                  key={idx}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: highlight ? "12px 14px" : "4px 6px",
                    borderRadius: 4,
                    backgroundColor: highlight
                      ? `rgba(239, 68, 68, ${(zoomP * 0.18).toFixed(3)})`
                      : "transparent",
                    borderLeft: highlight ? "5px solid #DC2626" : "5px solid transparent",
                  }}
                >
                  <span
                    style={{
                      fontFamily: highlight ? "BeVietnamProBlack, sans-serif" : "BeVietnamProExtraBold, sans-serif",
                      fontSize: highlight ? 28 : 24,
                      color: highlight ? "#991B1B" : "#334155",
                    }}
                  >
                    {r.label}
                  </span>
                  {r.value && (
                    <span
                      style={{
                        fontFamily: "BeVietnamProBlack, sans-serif",
                        fontSize: highlight ? 30 : 24,
                        color: highlight ? "#DC2626" : "#0F172A",
                        whiteSpace: "nowrap",
                      }}
                    >
                      {r.value}
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {variant === "notification" && (
        <div
          style={{
            backgroundColor: "#161C26",
            borderRadius: 24,
            padding: "28px 32px",
            boxShadow: "0 24px 55px rgba(0, 0, 0, 0.72)",
            border: "1px solid rgba(255, 255, 255, 0.16)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
            <span
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 24,
                color: "#22B8FF",
                textTransform: "uppercase",
              }}
            >
              {title}
            </span>
            <span
              style={{
                fontFamily: "BeVietnamProExtraBold, sans-serif",
                fontSize: 18,
                color: "#94A3B8",
              }}
            >
              Vừa xong
            </span>
          </div>
          <div
            style={{
              fontFamily: "BeVietnamProExtraBold, sans-serif",
              fontSize: 28,
              lineHeight: 1.4,
              color: "#F8FAFC",
            }}
          >
            {bodyText}
          </div>
        </div>
      )}

      {variant === "hidden_toggle" && (
        <div
          style={{
            backgroundColor: "#141B29",
            borderRadius: 16,
            padding: "28px 34px",
            boxShadow: "0 24px 55px rgba(0, 0, 0, 0.7)",
            border: "1px solid rgba(255, 255, 255, 0.14)",
          }}
        >
          <div
            style={{
              fontFamily: "BeVietnamProExtraBold, sans-serif",
              fontSize: 20,
              color: "#94A3B8",
              marginBottom: 18,
              textTransform: "uppercase",
              letterSpacing: "0.05em",
            }}
          >
            {title}
          </div>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 24 }}>
            <span
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 28,
                color: "#FFFFFF",
                lineHeight: 1.3,
              }}
            >
              {bodyText}
            </span>
            {/* Nút gạt thực tế kiểu hệ điều hành */}
            <div
              style={{
                width: 96,
                height: 52,
                borderRadius: 999,
                backgroundColor: toggleShift > 0.5 ? "#22C55E" : "#475569",
                padding: 5,
                flexShrink: 0,
                display: "flex",
                alignItems: "center",
              }}
            >
              <div
                style={{
                  width: 42,
                  height: 42,
                  borderRadius: 999,
                  backgroundColor: "#FFFFFF",
                  boxShadow: "0 2px 6px rgba(0,0,0,0.45)",
                  transform: `translate3d(${(toggleShift * 44).toFixed(2)}px, 0, 0)`,
                }}
              />
            </div>
          </div>
        </div>
      )}

      {variant === "fine_print" && (
        <div
          style={{
            backgroundColor: "#F8FAFC",
            color: "#0F172A",
            borderRadius: 8,
            padding: "32px 36px",
            boxShadow: "0 24px 55px rgba(0, 0, 0, 0.68)",
            border: "1px solid rgba(15, 23, 42, 0.15)",
          }}
        >
          <div
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 24,
              color: "#334155",
              marginBottom: 16,
              borderBottom: "1px solid #CBD5E1",
              paddingBottom: 12,
            }}
          >
            {title}
          </div>
          <div
            style={{
              fontFamily: "BeVietnamProExtraBold, sans-serif",
              fontSize: interpolate(zoomP, [0, 1], [17, 26]),
              lineHeight: 1.45,
              color: zoomP > 0.4 ? "#B91C1C" : "#475569",
              backgroundColor: `rgba(254, 240, 138, ${(zoomP * 0.65).toFixed(3)})`,
              padding: "10px 12px",
              borderRadius: 4,
            }}
          >
            {bodyText}
          </div>
        </div>
      )}
    </div>
  );
};
