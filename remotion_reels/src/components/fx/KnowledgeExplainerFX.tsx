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
