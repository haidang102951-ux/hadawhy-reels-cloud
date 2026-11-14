import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { KineticWordCaption } from "./components/KineticWordCaption";
import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16";
import { FRIDAY13_CAPTIONS } from "./friday13CaptionsData";
import {
  SAT_UK_PATH,
  SAT_UK_LONDON,
  SAT_FRA_PATH,
  SAT_FRA_PARIS,
  SAT_USA_PATH,
  SAT_USA_NYC,
  SAT_WORLD_HUBS,
} from "./friday13SatMapsData";

// ============================================================================
// HỆ THẨM MỸ ĐỘC BẢN: ARCHIVAL NOIR + 3D SATELLITE TERRAIN (ZERO-BOX 100%)
// ============================================================================
const ACCENT_RED = "#FF3B47";
const ACCENT_GOLD = "#FFE600";
const COLOR_IVORY = "#F7F1E5";
const COLOR_MUTED = "#D8C9B6";

const TEXT_SHADOW_DEEP =
  "0 8px 26px rgba(0,0,0,0.98), 0 3px 8px rgba(0,0,0,0.95)";
const TEXT_SHADOW_GLOW_GOLD =
  "0 8px 28px rgba(0,0,0,0.98), 0 0 28px rgba(255, 230, 0, 0.55)";
const TEXT_SHADOW_GLOW_RED =
  "0 8px 28px rgba(0,0,0,0.98), 0 0 28px rgba(255, 59, 71, 0.65)";

// Font loading block (yêu cầu bởi pre_render_gate.py)
const FONT_CSS = `
@font-face {
  font-family: 'BeVietnamProBlack';
  src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
  font-weight: 900;
}
@font-face {
  font-family: 'BeVietnamProExtraBold';
  src: url('${staticFile("fonts/BeVietnamPro-ExtraBold.ttf")}') format('truetype');
  font-weight: 800;
}
@font-face {
  font-family: 'KanitBlack';
  src: url('${staticFile("fonts/Kanit-Black.ttf")}') format('truetype');
  font-weight: 900;
}
`;

// Style chung cho Text Hook đánh thị giác cực mạnh
const hookStyle = (color: string, glow: string, size = 66): React.CSSProperties => ({
  fontFamily: "'KanitBlack', 'BeVietnamProBlack', sans-serif",
  fontSize: size,
  fontWeight: 900,
  lineHeight: 1.05,
  letterSpacing: "0.01em",
  color,
  WebkitTextStroke: "10px #090507",
  paintOrder: "stroke fill",
  textShadow: glow,
  textAlign: "center",
});

// Component Text Hook 2 tầng kiểu 250M $ (dòng trên Trắng gọn + dòng dưới Khổng lồ Vàng/Đỏ glow)
const ImpactHook: React.FC<{
  eyebrow: string;
  hero: string;
  heroColor?: string;
  heroSize?: number;
  eyebrowSize?: number;
  scale?: number;
}> = ({
  eyebrow,
  hero,
  heroColor = ACCENT_RED,
  heroSize = 92,
  eyebrowSize = 40,
  scale = 1,
}) => {
  const isRed = heroColor === ACCENT_RED;
  const heroGlow = isRed
    ? "0 0 38px rgba(255, 59, 71, 0.78), 0 10px 24px rgba(0,0,0,0.96)"
    : "0 0 38px rgba(255, 230, 0, 0.65), 0 10px 24px rgba(0,0,0,0.96)";
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        transform: `scale(${scale})`,
      }}
    >
      <div
        style={{
          fontFamily: "'BeVietnamProExtraBold', sans-serif",
          fontSize: eyebrowSize,
          fontWeight: 800,
          lineHeight: 1.05,
          letterSpacing: "0.04em",
          color: "#FFFFFF",
          WebkitTextStroke: "8px #08090F",
          paintOrder: "stroke fill",
          textShadow: "0 4px 14px rgba(0,0,0,0.95)",
          textAlign: "center",
          marginBottom: 4,
        }}
      >
        {eyebrow}
      </div>
      <div
        style={{
          fontFamily: "'KanitBlack', 'BeVietnamProBlack', sans-serif",
          fontSize: heroSize,
          fontWeight: 900,
          lineHeight: 0.96,
          letterSpacing: "-0.01em",
          color: heroColor,
          WebkitTextStroke: "14px #120608",
          paintOrder: "stroke fill",
          textShadow: heroGlow,
          textAlign: "center",
          whiteSpace: "nowrap",
        }}
      >
        {hero}
      </div>
    </div>
  );
};

// Component Bản đồ Vệ tinh 3D Thực tế (Esri World Imagery + Viền GeoJSON + Beacon 3D)
interface SatMap3DProps {
  imageSrc: string;
  viewBoxW: number;
  viewBoxH: number;
  borderPath?: string;
  pin?: { x: number; y: number; label: string };
  rotateX?: number;
  rotateY?: number;
  frame: number;
  children?: React.ReactNode;
}

const SatelliteMap3D: React.FC<SatMap3DProps> = ({
  imageSrc,
  viewBoxW,
  viewBoxH,
  borderPath,
  pin,
  rotateX = 24,
  rotateY = -6,
  frame,
  children,
}) => {
  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        perspective: 1100,
      }}
    >
      <div
        style={{
          position: "relative",
          width: "100%",
          height: "100%",
          borderRadius: 18,
          overflow: "visible",
          transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`,
          transformStyle: "preserve-3d",
          boxShadow:
            "0 14px 0 #1C130E, 0 28px 54px rgba(0,0,0,0.96), 0 0 36px rgba(255, 230, 0, 0.16)",
          border: "2px solid rgba(255, 230, 0, 0.45)",
        }}
      >
        <Img
          src={staticFile(imageSrc)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            borderRadius: 16,
            filter: "contrast(1.12) saturate(1.18) brightness(0.92)",
          }}
        />

        {/* Lớp SVG viền quốc gia phát sáng + tia bay + sóng radar khớp pixel vệ tinh */}
        <svg
          viewBox={`0 0 ${viewBoxW} ${viewBoxH}`}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            borderRadius: 16,
            pointerEvents: "none",
          }}
        >
          {borderPath && (
            <path
              d={borderPath}
              fill="rgba(255, 59, 71, 0.12)"
              stroke={ACCENT_GOLD}
              strokeWidth="4.5"
              strokeLinejoin="round"
            />
          )}

          {pin && (
            <>
              {[0, 1].map((r) => {
                const p = ((frame + r * 30) % 60) / 60;
                return (
                  <circle
                    key={r}
                    cx={pin.x}
                    cy={pin.y}
                    r={16 + p * 110}
                    fill="none"
                    stroke={ACCENT_RED}
                    strokeWidth="4"
                    opacity={Math.max(0, 1 - p)}
                  />
                );
              })}
              {/* Cột tia laser 3D thẳng đứng */}
              <line
                x1={pin.x}
                y1={pin.y}
                x2={pin.x}
                y2={pin.y - 120}
                stroke={ACCENT_RED}
                strokeWidth="5"
                strokeLinecap="round"
              />
              <circle
                cx={pin.x}
                cy={pin.y - 120}
                r="10"
                fill={ACCENT_GOLD}
                stroke="#FFFFFF"
                strokeWidth="3"
              />
              <circle
                cx={pin.x}
                cy={pin.y}
                r="11"
                fill={ACCENT_RED}
                stroke="#FFFFFF"
                strokeWidth="3"
              />
            </>
          )}

          {children}
        </svg>

        {pin && (
          <div
            style={{
              position: "absolute",
              left: `${(pin.x / viewBoxW) * 100}%`,
              top: `${((pin.y - 150) / viewBoxH) * 100}%`,
              transform: "translate(-50%, -50%) translateZ(36px)",
              fontSize: 28,
              fontWeight: 900,
              color: ACCENT_GOLD,
              WebkitTextStroke: "5px #070403",
              paintOrder: "stroke fill",
              textShadow: TEXT_SHADOW_GLOW_GOLD,
              whiteSpace: "nowrap",
            }}
          >
            {pin.label}
          </div>
        )}
      </div>
    </div>
  );
};

export const Friday13Origins45s: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Global Camera Shake cho các cú va chạm vật lý khớp words.json
  const impactFrames = [24, 134, 460, 692, 1176, 1313, 1631, 1949, 2355];
  let shakeX = 0;
  let shakeY = 0;
  for (const imp of impactFrames) {
    if (frame >= imp && frame < imp + 15) {
      const dt = frame - imp;
      const decay = Math.exp(-dt * 0.28);
      shakeX += Math.sin(dt * 3.14) * 13 * decay;
      shakeY += Math.cos(dt * 3.7) * 10 * decay;
    }
  }

  const spotX = 50 + Math.sin(frame * 0.015) * 12;
  const spotY = 40 + Math.cos(frame * 0.012) * 8;

  // ============================================================================
  // SCENE OPACITIES (100% bám words.json)
  // ============================================================================
  const s1Opacity = interpolate(frame, [0, 162, 178], [1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s2Opacity = interpolate(frame, [166, 180, 536, 554], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s3Opacity = interpolate(frame, [542, 558, 876, 894], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s4Opacity = interpolate(
    frame,
    [882, 898, 1362, 1380],
    [0, 1, 1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );
  const s5Opacity = interpolate(
    frame,
    [1368, 1384, 1772, 1790],
    [0, 1, 1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );
  const s6Opacity = interpolate(
    frame,
    [1778, 1794, 2144, 2162],
    [0, 1, 1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );
  const s7Opacity = interpolate(frame, [2150, 2166, 2505], [0, 1, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // ============================================================================
  // ANIMATION SPRINGS
  // ============================================================================
  // Scene 1
  const s1HookPop = spring({
    frame: Math.max(0, frame - 2),
    fps,
    config: { damping: 11, stiffness: 210, mass: 0.85 },
  });
  const s1PushLeft = spring({
    frame: Math.max(0, frame - 48),
    fps,
    config: { damping: 15, stiffness: 120 },
  });
  const s1WallStIn = spring({
    frame: Math.max(0, frame - 122),
    fps,
    config: { damping: 12, stiffness: 165, mass: 0.9 },
  });
  const s1BarTilt = interpolate(frame, [24, 48, 134, 154], [-6, -5, -5, 6], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s1SlashProgress = interpolate(frame, [50, 74], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Scene 2
  const s2ClockIn = spring({
    frame: Math.max(0, frame - 178),
    fps,
    config: { damping: 14, stiffness: 130 },
  });
  const s2OrbitSpin = (frame - 172) * 0.25;
  const s2MonthsActive = Math.floor(
    interpolate(frame, [265, 354], [0, 12], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );
  const s2OutcastDrop = spring({
    frame: Math.max(0, frame - 460),
    fps,
    config: { damping: 11, stiffness: 190, mass: 1.0 },
  });
  const s2RingLift = interpolate(frame, [458, 480], [0, -70], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s2BarTilt = interpolate(frame, [455, 476], [0, 5.5], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Scene 3
  const s3CrossIn = spring({
    frame: Math.max(0, frame - 556),
    fps,
    config: { damping: 14, stiffness: 130 },
  });
  const s3UkPhase = spring({
    frame: Math.max(0, frame - 686),
    fps,
    config: { damping: 14, stiffness: 125 },
  });
  const s3ArcProgress = interpolate(frame, [715, 765], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Scene 4
  const s4MapIn = spring({
    frame: Math.max(0, frame - 896),
    fps,
    config: { damping: 14, stiffness: 130 },
  });
  const s4KnightIn = spring({
    frame: Math.max(0, frame - 980),
    fps,
    config: { damping: 14, stiffness: 130 },
  });
  const s4KingIn = spring({
    frame: Math.max(0, frame - 1040),
    fps,
    config: { damping: 14, stiffness: 130 },
  });
  const s4DebtFlow = interpolate(frame, [1060, 1165], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s4ChainsSlam = spring({
    frame: Math.max(0, frame - 1176),
    fps,
    config: { damping: 11, stiffness: 210, mass: 0.9 },
  });
  const s4StampSlam = spring({
    frame: Math.max(0, frame - 1313),
    fps,
    config: { damping: 10, stiffness: 240, mass: 0.85 },
  });

  // Scene 5
  const s5LawsonIn = spring({
    frame: Math.max(0, frame - 1380),
    fps,
    config: { damping: 14, stiffness: 130 },
  });
  const s5BookIn = spring({
    frame: Math.max(0, frame - 1480),
    fps,
    config: { damping: 14, stiffness: 135 },
  });
  const s5CrashProgress = interpolate(frame, [1626, 1685], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s5PanicIn = spring({
    frame: Math.max(0, frame - 1635),
    fps,
    config: { damping: 13, stiffness: 150 },
  });

  // Scene 6
  const s6UsaOpacity = interpolate(
    frame,
    [1780, 1796, 1938, 1954],
    [0, 1, 1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );
  const s6WorldOpacity = interpolate(frame, [1942, 1958, 2156], [0, 1, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s6PosterIn = spring({
    frame: Math.max(0, frame - 1949),
    fps,
    config: { damping: 12, stiffness: 165, mass: 0.9 },
  });
  const s6ArcSpread = interpolate(frame, [1970, 2110], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Scene 7
  const s7BeatAOpacity = interpolate(
    frame,
    [2152, 2168, 2345, 2362],
    [0, 1, 1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );
  const s7BeatBOpacity = interpolate(frame, [2348, 2366, 2505], [0, 1, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s7FinaleRise = spring({
    frame: Math.max(0, frame - 2358),
    fps,
    config: { damping: 13, stiffness: 145 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0B0605",
        overflow: "hidden",
        fontFamily: "'BeVietnamProBlack', sans-serif",
      }}
    >
      <style>{FONT_CSS}</style>

      {/* AUDIO CHÍNH: VOICEOVER HẢI ĐĂNG */}
      <Audio src={staticFile("audio/thu_sau_ngay_13_voice.wav")} volume={1.0} />

      {/* NỀN ARCHIVAL NOIR + SPOTLIGHT ĐỘNG */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at ${spotX}% ${spotY}%, rgba(92, 38, 20, 0.48) 0%, rgba(20, 11, 8, 0.96) 65%, #090504 100%)`,
          transform: `translate(${shakeX}px, ${shakeY}px)`,
        }}
      >
        {/* Lưới kinh vĩ tuyến mờ */}
        <svg
          width="1080"
          height="1920"
          style={{ position: "absolute", inset: 0, opacity: 0.07 }}
        >
          {[280, 540, 800, 1060, 1320].map((y) => (
            <line
              key={y}
              x1="0"
              y1={y}
              x2="1080"
              y2={y}
              stroke="#E6D5B8"
              strokeWidth="1"
              strokeDasharray="6 10"
            />
          ))}
          {[220, 540, 860].map((x) => (
            <line
              key={x}
              x1={x}
              y1="140"
              x2={x}
              y2="1440"
              stroke="#E6D5B8"
              strokeWidth="1"
              strokeDasharray="6 10"
            />
          ))}
        </svg>

        {/* ================================================================ */}
        {/* SCENE 1 (f0–f172): TEXT HOOK MẠNH + LỊCH 13 ĐẨY SANG PHỐ WALL    */}
        {/* ================================================================ */}
        {s1Opacity > 0.01 && (
          <AbsoluteFill style={{ opacity: s1Opacity }}>
            <div
              style={{
                position: "absolute",
                top: 230,
                width: "100%",
                textAlign: "center",
                fontSize: 300,
                fontWeight: 900,
                color: "rgba(255, 59, 71, 0.08)",
                letterSpacing: -10,
                lineHeight: 0.9,
              }}
            >
              13
            </div>

            {/* TEXT HOOK SLAM 2 TẦNG KIỂU 250M $ */}
            <div
              style={{
                position: "absolute",
                top: 145,
                left: 40,
                right: 40,
              }}
            >
              <ImpactHook
                eyebrow="THỨ SÁU NGÀY"
                hero="13"
                heroColor={ACCENT_RED}
                heroSize={140}
                eyebrowSize={44}
                scale={interpolate(s1HookPop, [0, 1], [1.32, 1])}
              />
            </div>

            {frame >= 46 && (
              <div
                style={{
                  position: "absolute",
                  top: 325,
                  left: 55,
                  right: 55,
                  ...hookStyle(ACCENT_GOLD, TEXT_SHADOW_GLOW_GOLD, 48),
                  opacity: interpolate(frame, [46, 56, 126, 136], [0, 1, 1, 0.3], {
                    extrapolateLeft: "clamp",
                    extrapolateRight: "clamp",
                  }),
                }}
              >
                KHÔNG PHẢI LỜI NGUYỀN CỔ!
              </div>
            )}

            {/* Thanh chân trời nghiêng kiểu bay.mp4 */}
            <div
              style={{
                position: "absolute",
                top: 1030,
                left: 90,
                right: 90,
                height: 7,
                borderRadius: 4,
                background: `linear-gradient(to right, ${ACCENT_GOLD}, ${ACCENT_RED})`,
                boxShadow: "0 0 26px rgba(255, 59, 71, 0.65)",
                transform: `rotate(${s1BarTilt}deg)`,
              }}
            />

            {/* Lịch 13 rơi xuống bên trái rồi bị đẩy lùi */}
            <div
              style={{
                position: "absolute",
                top: 500,
                left: interpolate(s1PushLeft, [0, 1], [310, 75]),
                width: 440,
                transform: `translateY(${(1 - s1HookPop) * -260}px) scale(${interpolate(
                  s1PushLeft,
                  [0, 1],
                  [1.04, 0.68]
                )}) rotate(${interpolate(s1PushLeft, [0, 1], [-4, -11])}deg)`,
                opacity: interpolate(s1PushLeft, [0, 1], [1, 0.52]),
              }}
            >
              <Img
                src={staticFile("harvested/vintage_calendar_13.png")}
                style={{
                  width: "100%",
                  filter: "drop-shadow(0 24px 36px rgba(0,0,0,0.92))",
                }}
              />
              {s1SlashProgress > 0 && (
                <svg
                  viewBox="0 0 400 400"
                  style={{
                    position: "absolute",
                    inset: 0,
                    width: "100%",
                    height: "100%",
                  }}
                >
                  <line
                    x1="30"
                    y1="360"
                    x2={30 + 340 * s1SlashProgress}
                    y2={360 - 310 * s1SlashProgress}
                    stroke={ACCENT_RED}
                    strokeWidth="24"
                    strokeLinecap="round"
                  />
                </svg>
              )}
            </div>

            {/* NYSE + Ticker Tape lao chéo vào bên phải */}
            {frame >= 120 && (
              <div
                style={{
                  position: "absolute",
                  top: 430,
                  right: 55,
                  width: 600,
                  transform: `translate(${(1 - s1WallStIn) * 320}px, ${
                    (1 - s1WallStIn) * 180
                  }px) scale(${0.86 + 0.14 * s1WallStIn})`,
                  opacity: s1WallStIn,
                }}
              >
                <Img
                  src={staticFile("harvested/wallstreet_nyse_3d.png")}
                  style={{
                    width: "100%",
                    filter:
                      "drop-shadow(0 28px 42px rgba(0,0,0,0.95)) drop-shadow(0 0 28px rgba(255, 230, 0, 0.35))",
                  }}
                />
                <Img
                  src={staticFile("harvested/stock_ticker_tape.png")}
                  style={{
                    position: "absolute",
                    bottom: -20,
                    left: -40,
                    width: 440,
                    transform: "rotate(-6deg)",
                    filter: "drop-shadow(0 18px 28px rgba(0,0,0,0.9))",
                  }}
                />
              </div>
            )}

            {/* Text Hook bùng nổ ở điểm chốt Phố Wall */}
            {frame >= 132 && (
              <div
                style={{
                  position: "absolute",
                  top: 1095,
                  left: 40,
                  right: 40,
                }}
              >
                <ImpactHook
                  eyebrow="SỰ THẬT BẮT NGUỒN"
                  hero="TỪ PHỐ WALL!"
                  heroColor={ACCENT_GOLD}
                  heroSize={92}
                  eyebrowSize={38}
                  scale={interpolate(s1WallStIn, [0, 1], [1.3, 1])}
                />
              </div>
            )}
          </AbsoluteFill>
        )}

        {/* ================================================================ */}
        {/* SCENE 2 (f172–f548): VÒNG TRÒN 12 THÁNG + ĐỒNG HỒ -> SỐ 13 DƯ THỪA*/}
        {/* ================================================================ */}
        {s2Opacity > 0.01 && (
          <AbsoluteFill style={{ opacity: s2Opacity }}>
            <div
              style={{
                position: "absolute",
                top: 150,
                left: 40,
                right: 40,
              }}
            >
              <ImpactHook
                eyebrow="CHU KỲ HOÀN HẢO"
                hero="12 CON SỐ"
                heroColor={ACCENT_GOLD}
                heroSize={92}
                eyebrowSize={38}
              />
            </div>

            <div
              style={{
                position: "absolute",
                top: 370 + s2RingLift,
                left: 160,
                width: 760,
                height: 760,
                transform: `scale(${0.8 + 0.2 * s2ClockIn})`,
                opacity: s2ClockIn,
              }}
            >
              <svg
                viewBox="0 0 760 760"
                style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
              >
                <circle
                  cx="380"
                  cy="380"
                  r="310"
                  fill="none"
                  stroke="rgba(255, 230, 0, 0.25)"
                  strokeWidth="3"
                  strokeDasharray="10 12"
                />
              </svg>

              <div
                style={{
                  position: "absolute",
                  top: 170,
                  left: 170,
                  width: 420,
                  height: 420,
                  transform: `rotate(${Math.sin(frame * 0.04) * 3}deg)`,
                }}
              >
                <Img
                  src={staticFile("harvested/brass_clock_12.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                    filter:
                      "drop-shadow(0 24px 36px rgba(0,0,0,0.95)) drop-shadow(0 0 24px rgba(255,230,0,0.22))",
                  }}
                />
              </div>

              {Array.from({ length: 12 }).map((_, idx) => {
                const angleDeg = idx * 30 - 90 + s2OrbitSpin;
                const rad = (angleDeg * Math.PI) / 180;
                const cx = 380 + Math.cos(rad) * 310;
                const cy = 380 + Math.sin(rad) * 310;
                const isLit = idx < s2MonthsActive || frame >= 354;
                return (
                  <div
                    key={idx}
                    style={{
                      position: "absolute",
                      left: cx - 34,
                      top: cy - 26,
                      width: 68,
                      height: 52,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: 32,
                      fontWeight: 900,
                      color: isLit ? ACCENT_GOLD : "rgba(247,241,229,0.35)",
                      textShadow: isLit
                        ? TEXT_SHADOW_GLOW_GOLD
                        : TEXT_SHADOW_DEEP,
                      transform: `scale(${isLit ? 1.14 : 0.92})`,
                    }}
                  >
                    T{idx + 1}
                  </div>
                );
              })}
            </div>

            {frame >= 445 && (
              <>
                <div
                  style={{
                    position: "absolute",
                    top: 1200,
                    left: 100,
                    right: 100,
                    height: 7,
                    borderRadius: 4,
                    background: `linear-gradient(to right, ${ACCENT_GOLD}, ${ACCENT_RED})`,
                    boxShadow: "0 0 24px rgba(255, 59, 71, 0.6)",
                    transform: `rotate(${s2BarTilt}deg)`,
                  }}
                />

                <div
                  style={{
                    position: "absolute",
                    top: 1100,
                    left: 125,
                    ...hookStyle(ACCENT_GOLD, TEXT_SHADOW_GLOW_GOLD, 62),
                    textAlign: "left",
                  }}
                >
                  12 HOÀN HẢO
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 970,
                    right: 135,
                    fontSize: 175,
                    fontWeight: 900,
                    color: ACCENT_RED,
                    WebkitTextStroke: "8px #080403",
                    paintOrder: "stroke fill",
                    textShadow: TEXT_SHADOW_GLOW_RED,
                    transform: `translateY(${(1 - s2OutcastDrop) * -360}px) rotate(8deg)`,
                    opacity: s2OutcastDrop,
                  }}
                >
                  13
                </div>
                <div
                  style={{
                    position: "absolute",
                    top: 1245,
                    right: 90,
                    ...hookStyle(ACCENT_RED, TEXT_SHADOW_GLOW_RED, 44),
                    opacity: s2OutcastDrop,
                  }}
                >
                  DƯ THỪA — XUI XẺO!
                </div>
              </>
            )}
          </AbsoluteFill>
        )}

        {/* ================================================================ */}
        {/* SCENE 3 (f548–f888): THỨ SÁU + BẢN ĐỒ VỆ TINH 3D ANH + TYBURN    */}
        {/* ================================================================ */}
        {s3Opacity > 0.01 && (
          <AbsoluteFill style={{ opacity: s3Opacity }}>
            {/* Tia sáng vàng thẳng đứng chiếu xuống Thánh giá */}
            <div
              style={{
                position: "absolute",
                top: 120,
                left: interpolate(s3UkPhase, [0, 1], [340, 80]),
                width: 400,
                height: 680,
                background:
                  "linear-gradient(to bottom, rgba(255,230,0,0.22), rgba(255,230,0,0) 85%)",
                clipPath: "polygon(30% 0%, 70% 0%, 100% 100%, 0% 100%)",
                opacity: interpolate(s3UkPhase, [0, 1], [1, 0.35]),
              }}
            />

            {/* Text Hook trên đầu */}
            <div
              style={{
                position: "absolute",
                top: 150,
                left: 40,
                right: 40,
                opacity: interpolate(s3UkPhase, [0, 0.5], [1, 0], {
                  extrapolateRight: "clamp",
                }),
              }}
            >
              <ImpactHook
                eyebrow="THỨ SÁU LÀ NGÀY"
                hero="CHÚA CHỊU NẠN"
                heroColor={ACCENT_GOLD}
                heroSize={82}
                eyebrowSize={38}
              />
            </div>

            {frame >= 680 && (
              <div
                style={{
                  position: "absolute",
                  top: 150,
                  left: 40,
                  right: 40,
                  opacity: s3UkPhase,
                }}
              >
                <ImpactHook
                  eyebrow="TẠI NƯỚC ANH"
                  hero="TREO CỔ TỬ TÙ"
                  heroColor={ACCENT_RED}
                  heroSize={84}
                  eyebrowSize={38}
                />
              </div>
            )}

            {/* Thánh giá gỗ thật */}
            <div
              style={{
                position: "absolute",
                top: interpolate(s3UkPhase, [0, 1], [360, 290]),
                left: interpolate(s3UkPhase, [0, 1], [290, 55]),
                width: 480,
                transform: `scale(${
                  (0.85 + 0.15 * s3CrossIn) * interpolate(s3UkPhase, [0, 1], [1, 0.68])
                })`,
                opacity: s3CrossIn * interpolate(s3UkPhase, [0, 1], [1, 0.72]),
              }}
            >
              <Img
                src={staticFile("harvested/wooden_cross_real.png")}
                style={{
                  width: "100%",
                  filter: "drop-shadow(0 28px 42px rgba(0,0,0,0.95))",
                }}
              />
            </div>

            {/* Bản đồ Vệ tinh 3D Vương quốc Anh + Beacon London */}
            {frame >= 680 && (
              <>
                <div
                  style={{
                    position: "absolute",
                    top: 280,
                    right: 65,
                    width: 440,
                    height: 520,
                    opacity: s3UkPhase,
                    transform: `scale(${0.84 + 0.16 * s3UkPhase})`,
                  }}
                >
                  <SatelliteMap3D
                    imageSrc="harvested/sat_uk.png"
                    viewBoxW={900}
                    viewBoxH={1080}
                    borderPath={SAT_UK_PATH}
                    pin={{ ...SAT_UK_LONDON, label: "LONDON, ANH" }}
                    rotateX={24}
                    rotateY={-8}
                    frame={frame}
                  />
                </div>

                {/* Đường dẫn nhân quả từ London trên bản đồ vệ tinh xuống tranh khắc */}
                <svg
                  viewBox="0 0 1080 1920"
                  style={{
                    position: "absolute",
                    inset: 0,
                    width: "100%",
                    height: "100%",
                    pointerEvents: "none",
                  }}
                >
                  <path
                    d="M 885 690 Q 820 810 540 855"
                    fill="none"
                    stroke={ACCENT_RED}
                    strokeWidth="6"
                    strokeDasharray="12 10"
                    strokeDashoffset={320 * (1 - s3ArcProgress)}
                    opacity={s3ArcProgress}
                  />
                </svg>

                {/* Tranh khắc London Tyburn thật trên thanh chân trời */}
                <div
                  style={{
                    position: "absolute",
                    top: 840,
                    left: 85,
                    right: 85,
                    transform: `translateY(${(1 - s3UkPhase) * 90}px)`,
                    opacity: s3UkPhase,
                  }}
                >
                  <Img
                    src={staticFile("harvested/old_london_engraving.png")}
                    style={{
                      width: "100%",
                      height: 450,
                      objectFit: "cover",
                      borderRadius: 16,
                      filter:
                        "sepia(0.22) contrast(1.14) drop-shadow(0 28px 46px rgba(0,0,0,0.95))",
                    }}
                  />
                  <div
                    style={{
                      marginTop: 18,
                      height: 6,
                      borderRadius: 4,
                      background: `linear-gradient(to right, ${ACCENT_RED}, ${ACCENT_GOLD})`,
                    }}
                  />
                </div>
              </>
            )}
          </AbsoluteFill>
        )}

        {/* ================================================================ */}
        {/* SCENE 4 (f888–f1374): BẢN ĐỒ VỆ TINH 3D PHÁP + 1307 XÙ NỢ       */}
        {/* ================================================================ */}
        {s4Opacity > 0.01 && (
          <AbsoluteFill style={{ opacity: s4Opacity }}>
            <div
              style={{
                position: "absolute",
                top: 230,
                width: "100%",
                textAlign: "center",
                fontSize: 230,
                fontWeight: 900,
                color: "rgba(255, 230, 0, 0.08)",
                letterSpacing: -6,
              }}
            >
              1307
            </div>

            {/* TEXT HOOK TRÊN ĐẦU */}
            <div
              style={{
                position: "absolute",
                top: 145,
                left: 40,
                right: 40,
              }}
            >
              <ImpactHook
                eyebrow="BIẾN CỐ THỨ SÁU"
                hero="13/10/1307"
                heroColor={ACCENT_GOLD}
                heroSize={98}
                eyebrowSize={38}
              />
            </div>

            {/* Bản đồ Vệ tinh 3D Pháp + Paris */}
            <div
              style={{
                position: "absolute",
                top: 265,
                right: 60,
                width: 430,
                height: 420,
                opacity: s4MapIn,
                transform: `scale(${0.86 + 0.14 * s4MapIn})`,
              }}
            >
              <SatelliteMap3D
                imageSrc="harvested/sat_fra.png"
                viewBoxW={1000}
                viewBoxH={980}
                borderPath={SAT_FRA_PATH}
                pin={{ ...SAT_FRA_PARIS, label: "PARIS, PHÁP" }}
                rotateX={26}
                rotateY={-7}
                frame={frame}
              />
            </div>

            {/* Dòng chảy vàng từ Hiệp sĩ (trái dưới) -> Vua Pháp (phải dưới bản đồ) */}
            <svg
              viewBox="0 0 1080 1920"
              style={{
                position: "absolute",
                inset: 0,
                width: "100%",
                height: "100%",
                pointerEvents: "none",
              }}
            >
              <path
                d="M 320 960 Q 520 790 760 880"
                fill="none"
                stroke={frame >= 1176 ? ACCENT_RED : ACCENT_GOLD}
                strokeWidth="7"
                strokeDasharray="16 12"
                strokeDashoffset={600 * (1 - s4DebtFlow) - frame * 2}
                opacity={s4DebtFlow}
              />
            </svg>

            {/* Hiệp sĩ Dòng Đền */}
            <div
              style={{
                position: "absolute",
                top: 650,
                left: 55,
                width: 440,
                transform: `translateX(${(1 - s4KnightIn) * -140}px)`,
                opacity: s4KnightIn,
              }}
            >
              <Img
                src={staticFile("harvested/knights_templar_real.png")}
                style={{
                  width: "100%",
                  height: 610,
                  objectFit: "contain",
                  filter: "drop-shadow(0 24px 36px rgba(0,0,0,0.95))",
                }}
              />
              <div
                style={{
                  marginTop: 8,
                  ...hookStyle(ACCENT_GOLD, TEXT_SHADOW_GLOW_GOLD, 32),
                }}
              >
                HIỆP SĨ DÒNG ĐỀN (CHỦ NỢ)
              </div>
            </div>

            {/* Vua Pháp Philip IV */}
            <div
              style={{
                position: "absolute",
                top: 700,
                right: 60,
                width: 410,
                transform: `translateX(${(1 - s4KingIn) * 140}px)`,
                opacity: s4KingIn,
              }}
            >
              <Img
                src={staticFile("harvested/king_philip_iv.png")}
                style={{
                  width: "100%",
                  filter: "drop-shadow(0 24px 36px rgba(0,0,0,0.95))",
                }}
              />
              <div
                style={{
                  marginTop: 8,
                  ...hookStyle(ACCENT_RED, TEXT_SHADOW_GLOW_RED, 32),
                }}
              >
                VUA PHILIP IV (QUỴT NỢ)
              </div>
            </div>

            {/* Xích sắt chém đứt dòng tiền */}
            {frame >= 1170 && (
              <div
                style={{
                  position: "absolute",
                  top: 760,
                  left: 330,
                  width: 430,
                  transform: `scale(${interpolate(s4ChainsSlam, [0, 1], [1.6, 1])}) rotate(-14deg)`,
                  opacity: s4ChainsSlam,
                }}
              >
                <Img
                  src={staticFile("harvested/iron_chains_real.png")}
                  style={{
                    width: "100%",
                    filter: "drop-shadow(0 22px 34px rgba(0,0,0,0.96))",
                  }}
                />
              </div>
            )}

            {/* Con dấu mực đỏ trong suốt (Zero-Box!) */}
            {frame >= 1310 && (
              <div
                style={{
                  position: "absolute",
                  top: 660,
                  left: 140,
                  right: 140,
                  textAlign: "center",
                  padding: "22px 28px",
                  border: `8px solid ${ACCENT_RED}`,
                  backgroundColor: "transparent",
                  color: ACCENT_RED,
                  fontSize: 60,
                  fontWeight: 900,
                  letterSpacing: 3,
                  WebkitTextStroke: "4px #080403",
                  paintOrder: "stroke fill",
                  textShadow: TEXT_SHADOW_GLOW_RED,
                  boxShadow: "0 0 36px rgba(255, 59, 71, 0.45)",
                  transform: `rotate(-8deg) scale(${interpolate(
                    s4StampSlam,
                    [0, 1],
                    [2.1, 1]
                  )})`,
                  opacity: s4StampSlam,
                }}
              >
                HỒI ĐÓ CHẲNG AI SỢ!
              </div>
            )}
          </AbsoluteFill>
        )}

        {/* ================================================================ */}
        {/* SCENE 5 (f1374–f1784): TÁCH 2 TẦNG RÕ RÀNG — KHÔNG CHỒNG HÌNH!   */}
        {/* Tầng trên (y: 310..790): Lawson + Sách 1907                      */}
        {/* Tầng dưới (y: 860..1360): Đồ thị đỏ + Đám đông Phố Wall          */}
        {/* ================================================================ */}
        {s5Opacity > 0.01 && (
          <AbsoluteFill style={{ opacity: s5Opacity }}>
            <div
              style={{
                position: "absolute",
                top: 230,
                width: "100%",
                textAlign: "center",
                fontSize: 250,
                fontWeight: 900,
                color: "rgba(255, 230, 0, 0.08)",
                letterSpacing: -8,
              }}
            >
              1907
            </div>

            {/* TEXT HOOK MẠNH TRÊN ĐẦU */}
            <div
              style={{
                position: "absolute",
                top: 145,
                left: 40,
                right: 40,
              }}
            >
              <ImpactHook
                eyebrow="TIỂU THUYẾT PHỐ WALL"
                hero="NĂM 1907"
                heroColor={ACCENT_GOLD}
                heroSize={98}
                eyebrowSize={38}
              />
            </div>

            {/* TẦNG TRÊN TRÁI: Thomas Lawson (giới hạn chiều cao 420px để không chạm tầng dưới!) */}
            <div
              style={{
                position: "absolute",
                top: 280,
                left: 70,
                width: 420,
                transform: `translateX(${(1 - s5LawsonIn) * -150}px)`,
                opacity: s5LawsonIn,
              }}
            >
              <Img
                src={staticFile("harvested/thomas_lawson_portrait.png")}
                style={{
                  width: "100%",
                  height: 410,
                  objectFit: "contain",
                  filter: "drop-shadow(0 24px 36px rgba(0,0,0,0.95))",
                }}
              />
              <div
                style={{
                  marginTop: 6,
                  ...hookStyle(COLOR_IVORY, TEXT_SHADOW_DEEP, 30),
                }}
              >
                THOMAS W. LAWSON
              </div>
            </div>

            {/* TẦNG TRÊN PHẢI: Cuốn tiểu thuyết 1907 (giới hạn chiều cao 410px!) */}
            <div
              style={{
                position: "absolute",
                top: 285,
                right: 85,
                width: 380,
                transform: `translateX(${(1 - s5BookIn) * 160}px) rotate(4deg)`,
                opacity: s5BookIn,
              }}
            >
              <Img
                src={staticFile("harvested/lawson_1907_book_evidence.png")}
                style={{
                  width: "100%",
                  height: 410,
                  objectFit: "contain",
                  filter:
                    "drop-shadow(0 26px 40px rgba(0,0,0,0.95)) drop-shadow(0 0 22px rgba(255,230,0,0.28))",
                }}
              />
            </div>

            {/* TẦNG DƯỚI (y: 800..1380): Đồ thị đỏ + Ảnh đám đông Phố Wall TÁCH BẠCH 100% */}
            {frame >= 1618 && (
              <>
                <svg
                  viewBox="0 0 1080 540"
                  style={{
                    position: "absolute",
                    top: 800,
                    left: 0,
                    width: 1080,
                    height: 540,
                    pointerEvents: "none",
                  }}
                >
                  <path
                    d="M 80 60 L 280 110 L 420 80 L 580 260 L 720 210 L 960 440"
                    fill="none"
                    stroke={ACCENT_RED}
                    strokeWidth="12"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeDasharray="1200"
                    strokeDashoffset={1200 * (1 - s5CrashProgress)}
                  />
                </svg>

                <div
                  style={{
                    position: "absolute",
                    top: 870,
                    left: 105,
                    right: 105,
                    transform: `translateY(${(1 - s5PanicIn) * 80}px)`,
                    opacity: s5PanicIn,
                  }}
                >
                  <Img
                    src={staticFile("harvested/wallstreet_crash_newspaper.png")}
                    style={{
                      width: "100%",
                      height: 360,
                      objectFit: "cover",
                      borderRadius: 14,
                      filter: "drop-shadow(0 26px 42px rgba(0,0,0,0.96))",
                    }}
                  />
                  <div
                    style={{
                      marginTop: 16,
                      height: 6,
                      borderRadius: 4,
                      background: `linear-gradient(to right, ${ACCENT_RED}, ${ACCENT_GOLD})`,
                    }}
                  />
                  <div
                    style={{
                      marginTop: 14,
                    }}
                  >
                    <ImpactHook
                      eyebrow="THAO TÚNG SẬP SÀN"
                      hero="THỨ SÁU 13"
                      heroColor={ACCENT_RED}
                      heroSize={84}
                      eyebrowSize={34}
                    />
                  </div>
                </div>
              </>
            )}
          </AbsoluteFill>
        )}

        {/* ================================================================ */}
        {/* SCENE 6 (f1784–f2156): BẢN ĐỒ VỆ TINH 3D MỸ & THẾ GIỚI + POSTER  */}
        {/* ================================================================ */}
        {s6Opacity > 0.01 && (
          <AbsoluteFill style={{ opacity: s6Opacity }}>
            {/* BEAT A: Bản đồ Vệ tinh 3D USA + Sóng xung kích từ NYC */}
            {s6UsaOpacity > 0.01 && (
              <AbsoluteFill style={{ opacity: s6UsaOpacity }}>
                <div
                  style={{
                    position: "absolute",
                    top: 145,
                    left: 40,
                    right: 40,
                  }}
                >
                  <ImpactHook
                    eyebrow="SÁCH BÁN CHẠY KHIẾN"
                    hero="CẢ NƯỚC MỸ ÁM ẢNH"
                    heroColor={ACCENT_GOLD}
                    heroSize={74}
                    eyebrowSize={38}
                  />
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 300,
                    left: 65,
                    width: 950,
                    height: 560,
                  }}
                >
                  <SatelliteMap3D
                    imageSrc="harvested/sat_usa.png"
                    viewBoxW={1120}
                    viewBoxH={660}
                    borderPath={SAT_USA_PATH}
                    pin={{ ...SAT_USA_NYC, label: "PHỐ WALL, NYC" }}
                    rotateX={22}
                    rotateY={-3}
                    frame={frame}
                  />
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 930,
                    left: 360,
                    width: 360,
                  }}
                >
                  <Img
                    src={staticFile("harvested/lawson_1907_book_evidence.png")}
                    style={{
                      width: "100%",
                      height: 360,
                      objectFit: "contain",
                      filter: "drop-shadow(0 24px 38px rgba(0,0,0,0.95))",
                    }}
                  />
                </div>
                <div
                  style={{
                    position: "absolute",
                    top: 1320,
                    left: 110,
                    right: 110,
                    height: 6,
                    borderRadius: 4,
                    background: `linear-gradient(to right, ${ACCENT_GOLD}, ${ACCENT_RED})`,
                  }}
                />
              </AbsoluteFill>
            )}

            {/* BEAT B: Poster Phim 1980 + Bản đồ Vệ tinh 3D Thế giới bắn tia */}
            {s6WorldOpacity > 0.01 && (
              <AbsoluteFill style={{ opacity: s6WorldOpacity }}>
                <div
                  style={{
                    position: "absolute",
                    top: 145,
                    left: 40,
                    right: 40,
                  }}
                >
                  <ImpactHook
                    eyebrow="PHIM KINH DỊ 1980"
                    hero="THỔI BÙNG TOÀN CẦU"
                    heroColor={ACCENT_RED}
                    heroSize={72}
                    eyebrowSize={38}
                  />
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 290,
                    left: 345,
                    width: 390,
                    transform: `scale(${0.78 + 0.22 * s6PosterIn})`,
                    opacity: s6PosterIn,
                  }}
                >
                  <Img
                    src={staticFile("harvested/friday_13th_1980_poster.jpg")}
                    style={{
                      width: "100%",
                      height: 495,
                      objectFit: "cover",
                      borderRadius: 12,
                      filter:
                        "drop-shadow(0 26px 46px rgba(0,0,0,0.96)) drop-shadow(0 0 28px rgba(255,59,71,0.45))",
                    }}
                  />
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 830,
                    left: 55,
                    width: 970,
                    height: 515,
                  }}
                >
                  <SatelliteMap3D
                    imageSrc="harvested/sat_world.png"
                    viewBoxW={1280}
                    viewBoxH={680}
                    rotateX={24}
                    rotateY={0}
                    frame={frame}
                  >
                    {(
                      [
                        SAT_WORLD_HUBS.london,
                        SAT_WORLD_HUBS.paris,
                        SAT_WORLD_HUBS.hanoi,
                        SAT_WORLD_HUBS.tokyo,
                      ] as const
                    ).map((target, idx) => {
                      const midX = (SAT_WORLD_HUBS.nyc.x + target.x) / 2;
                      const midY =
                        Math.min(SAT_WORLD_HUBS.nyc.y, target.y) -
                        (75 + idx * 18);
                      return (
                        <g key={idx}>
                          <path
                            d={`M ${SAT_WORLD_HUBS.nyc.x} ${SAT_WORLD_HUBS.nyc.y} Q ${midX} ${midY} ${target.x} ${target.y}`}
                            fill="none"
                            stroke={ACCENT_RED}
                            strokeWidth="5"
                            strokeDasharray="12 9"
                            strokeDashoffset={620 * (1 - s6ArcSpread) - frame * 2}
                          />
                          <circle
                            cx={target.x}
                            cy={target.y}
                            r="9"
                            fill={ACCENT_GOLD}
                            stroke="#FFF"
                            strokeWidth="2.5"
                          />
                        </g>
                      );
                    })}
                    <circle
                      cx={SAT_WORLD_HUBS.nyc.x}
                      cy={SAT_WORLD_HUBS.nyc.y}
                      r="12"
                      fill={ACCENT_RED}
                      stroke="#FFF"
                      strokeWidth="3"
                    />
                  </SatelliteMap3D>
                </div>
              </AbsoluteFill>
            )}
          </AbsoluteFill>
        )}

        {/* ================================================================ */}
        {/* SCENE 7 (f2156–f2505): KẾT LUẬN KIỂU bay.mp4 (2 VẬT CHỨNG CÂN ĐỐI)*/}
        {/* ================================================================ */}
        {s7Opacity > 0.01 && (
          <AbsoluteFill style={{ opacity: s7Opacity }}>
            {s7BeatAOpacity > 0.01 && (
              <AbsoluteFill style={{ opacity: s7BeatAOpacity }}>
                <div
                  style={{
                    position: "absolute",
                    top: 155,
                    left: 40,
                    right: 40,
                  }}
                >
                  <ImpactHook
                    eyebrow="CHẲNG PHẢI"
                    hero="LỜI NGUYỀN CỔ!"
                    heroColor={ACCENT_GOLD}
                    heroSize={84}
                    eyebrowSize={40}
                  />
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 390,
                    left: 310,
                    width: 460,
                    transform: "rotate(-6deg)",
                    opacity: 0.72,
                  }}
                >
                  <Img
                    src={staticFile("harvested/vintage_calendar_13.png")}
                    style={{
                      width: "100%",
                      filter: "drop-shadow(0 24px 36px rgba(0,0,0,0.95))",
                    }}
                  />
                  <svg
                    viewBox="0 0 400 400"
                    style={{
                      position: "absolute",
                      inset: 0,
                      width: "100%",
                      height: "100%",
                    }}
                  >
                    <line
                      x1="40"
                      y1="40"
                      x2="360"
                      y2="360"
                      stroke={ACCENT_RED}
                      strokeWidth="26"
                      strokeLinecap="round"
                    />
                    <line
                      x1="360"
                      y1="40"
                      x2="40"
                      y2="360"
                      stroke={ACCENT_RED}
                      strokeWidth="26"
                      strokeLinecap="round"
                    />
                  </svg>
                </div>
              </AbsoluteFill>
            )}

            {s7BeatBOpacity > 0.01 && (
              <AbsoluteFill style={{ opacity: s7BeatBOpacity }}>
                <div
                  style={{
                    position: "absolute",
                    top: 150,
                    left: 40,
                    right: 40,
                  }}
                >
                  <ImpactHook
                    eyebrow="DO CON NGƯỜI"
                    hero="TỰ TAY TẠO RA!"
                    heroColor={ACCENT_RED}
                    heroSize={86}
                    eyebrowSize={40}
                    scale={interpolate(s7FinaleRise, [0, 1], [1.18, 1])}
                  />
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 430,
                    left: 85,
                    width: 390,
                    transform: `translateY(${(1 - s7FinaleRise) * 140}px) rotate(-3deg)`,
                  }}
                >
                  <Img
                    src={staticFile("harvested/lawson_1907_book_evidence.png")}
                    style={{
                      width: "100%",
                      height: 490,
                      objectFit: "contain",
                      filter: "drop-shadow(0 26px 40px rgba(0,0,0,0.95))",
                    }}
                  />
                  <div
                    style={{
                      marginTop: 12,
                      ...hookStyle(ACCENT_GOLD, TEXT_SHADOW_GLOW_GOLD, 36),
                    }}
                  >
                    TIỂU THUYẾT 1907
                  </div>
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 630,
                    left: 490,
                    width: 100,
                    textAlign: "center",
                    fontSize: 92,
                    fontWeight: 900,
                    color: COLOR_IVORY,
                    textShadow: TEXT_SHADOW_DEEP,
                    transform: `scale(${s7FinaleRise})`,
                  }}
                >
                  +
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 430,
                    right: 85,
                    width: 390,
                    transform: `translateY(${(1 - s7FinaleRise) * 140}px) rotate(3deg)`,
                  }}
                >
                  <Img
                    src={staticFile("harvested/friday_13th_1980_poster.jpg")}
                    style={{
                      width: "100%",
                      height: 490,
                      objectFit: "cover",
                      borderRadius: 10,
                      filter: "drop-shadow(0 26px 40px rgba(0,0,0,0.95))",
                    }}
                  />
                  <div
                    style={{
                      marginTop: 12,
                      ...hookStyle(ACCENT_RED, TEXT_SHADOW_GLOW_RED, 36),
                    }}
                  >
                    PHIM KINH DỊ 1980
                  </div>
                </div>

                <div
                  style={{
                    position: "absolute",
                    top: 1035,
                    left: 80,
                    right: 80,
                    height: 7,
                    borderRadius: 4,
                    background: `linear-gradient(to right, ${ACCENT_GOLD}, ${ACCENT_RED})`,
                    boxShadow: "0 0 28px rgba(255, 230, 0, 0.55)",
                    transform: `scaleX(${s7FinaleRise})`,
                  }}
                />

                <div
                  style={{
                    position: "absolute",
                    top: 1075,
                    left: 80,
                    right: 80,
                    textAlign: "center",
                    fontSize: 36,
                    fontWeight: 800,
                    color: COLOR_MUTED,
                    textShadow: TEXT_SHADOW_DEEP,
                    opacity: s7FinaleRise,
                  }}
                >
                  CÒN BẠN CÓ SỢ THỨ SÁU NGÀY 13 KHÔNG?
                </div>
              </AbsoluteFill>
            )}
          </AbsoluteFill>
        )}
      </AbsoluteFill>

      {/* LOGO THƯƠNG HIỆU HADA WHY 2 LỚP CHỐNG ĂN CẮP BẢN QUYỀN */}
      <ChannelWatermark9x16 />

      {/* PHỤ ĐỀ KARAOKE ĐỘNG HỌC CHUYỂN XUỐNG KHUNG DƯỚI VIDEO */}
      <KineticWordCaption phrases={FRIDAY13_CAPTIONS} placement="bottom" />
    </AbsoluteFill>
  );
};
