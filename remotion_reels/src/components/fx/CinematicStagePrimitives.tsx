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
