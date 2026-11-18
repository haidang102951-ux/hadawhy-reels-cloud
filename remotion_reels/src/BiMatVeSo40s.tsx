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
import { HaDaWhyMistBackground } from "./components/HaDaWhyMistBackground";
import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16";
import {
  HaDaWhyFontFaces,
  HookBeatSpec,
  KineticHookHeader,
} from "./components/KineticHookHeader";
import { CoinStream } from "./components/CoinStream";

const LOTTERY_DIGITS = [
  { target: 8, match: true, lockFrame: 725 },
  { target: 3, match: true, lockFrame: 745 },
  { target: 5, match: true, lockFrame: 765 },
  { target: 1, match: true, lockFrame: 785 },
  { target: 9, match: true, lockFrame: 805 },
  { target: 4, match: false, actual: 7, lockFrame: 835 },
];

export const BiMatVeSo40s: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // =========================================================================
  // CAMERA MICRO-SHAKE ON KEY IMPACTS (Synced to words.json)
  // =========================================================================
  const impactFrames = [2, 197, 263, 686, 835, 1219, 1300, 1756, 2108];
  let shakeX = 0;
  let shakeY = 0;
  for (const imp of impactFrames) {
    if (frame >= imp && frame < imp + 14) {
      const dt = frame - imp;
      const decay = Math.exp(-dt * 0.28);
      const amp = imp === 1300 || imp === 2108 ? 13 : 8;
      shakeX += Math.sin(dt * 3.2) * amp * decay;
      shakeY += Math.cos(dt * 3.6) * (amp - 2) * decay;
    }
  }

  // Global light sweep for continuous motion
  const sweepX = ((frame * 16) % 2400) - 700;

  // =========================================================================
  // 6-BEAT KINETIC HOOK TIMELINE (100% synced to words.json & blueprint)
  // =========================================================================
  const hookInfo: HookBeatSpec = (() => {
    if (frame < 263) {
      return {
        start: 0,
        eyebrow: "VÉ SỐ 10 NGHÌN",
        hero: "KHÓ HƠN SÉT ĐÁNH?",
        accent: "#42B2F2",
        heroSize: 74,
      };
    }
    if (frame < 686) {
      return {
        start: 263,
        eyebrow: "THỨ HỌ THẬT SỰ MUA",
        hero: "GIẤC MƠ ĐỔI ĐỜI 16:30",
        accent: "#FFE600",
        heroSize: 70,
      };
    }
    if (frame < 1219) {
      return {
        start: 686,
        eyebrow: "LỆCH ĐÚNG 1 SỐ CUỐI",
        hero: "NÃO BÙNG DOPAMINE!",
        accent: "#00FF88",
        heroSize: 74,
      };
    }
    if (frame < 1756) {
      return {
        start: 1219,
        eyebrow: "HIỆU ỨNG TÂM LÝ FOMO",
        hero: "LỠ CHIỀU NAY RA ĐÚNG SỐ?",
        accent: "#FF3B47",
        heroSize: 64,
      };
    }
    if (frame < 2096) {
      return {
        start: 1756,
        eyebrow: "NGHỊCH LÝ KINH TẾ",
        hero: "CHẬT VẬT CÀNG ĐẮT HÀNG",
        accent: "#FFE600",
        heroSize: 66,
      };
    }
    return {
      start: 2096,
      eyebrow: "10 NGHÌN MỖI CHIỀU",
      hero: "HY VỌNG HAY TỰ LỪA MÌNH?",
      accent: "#42B2F2",
      heroSize: 64,
    };
  })();

  // =========================================================================
  // BEAT 1: 0..263 (HOOK: Tờ vé số 10k vs Tia sét đánh)
  // =========================================================================
  const b1Active = frame < 275;
  const b1Opacity =
    frame < 250
      ? 1
      : interpolate(frame, [250, 275], [1, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
  const b1Slam = spring({
    frame,
    fps,
    config: { damping: 13, stiffness: 200, mass: 0.75 },
  });
  const b1TicketScale = interpolate(b1Slam, [0, 1], [1.35, 1.0]);
  const b1Float = Math.sin(frame * 0.08) * 10;
  const b1OddsProgress = interpolate(frame, [60, 145], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const b1TicketOdds = Math.round(
    interpolate(b1OddsProgress, [0, 1], [100, 1000000])
  ).toLocaleString("vi-VN");
  const b1LightningOdds = Math.round(
    interpolate(b1OddsProgress, [0, 1], [100, 500000])
  ).toLocaleString("vi-VN");
  const b1LightningFlash =
    (frame >= 188 && frame <= 202) || (frame >= 218 && frame <= 226)
      ? 1.55
      : 1.0;

  // =========================================================================
  // BEAT 2: 263..686 (GÀI TÂM LÝ: Người bán vé số + Đồng hồ 16:30 + CoinStream)
  // =========================================================================
  const b2Active = frame >= 255 && frame < 698;
  const b2Opacity =
    frame < 280
      ? interpolate(frame, [255, 280], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : frame > 670
        ? interpolate(frame, [670, 698], [1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        : 1;
  const b2Enter = spring({
    frame: Math.max(0, frame - 263),
    fps,
    config: { damping: 15, stiffness: 130 },
  });
  const b2PhotoZoom = interpolate(frame, [263, 686], [1.02, 1.11], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const b2SecondsLeft = Math.max(
    0,
    Math.floor(interpolate(frame, [280, 640], [15, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }))
  );
  const b2ClockStr =
    b2SecondsLeft === 0
      ? "16:30:00"
      : `16:29:${String(60 - b2SecondsLeft).padStart(2, "0")}`;

  // =========================================================================
  // BEAT 3: 686..1219 (GIẢI MÃ: 6-Digit Odometer + Não 3D Dopamine)
  // =========================================================================
  const b3Active = frame >= 678 && frame < 1232;
  const b3Opacity =
    frame < 702
      ? interpolate(frame, [678, 702], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : frame > 1200
        ? interpolate(frame, [1200, 1232], [1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        : 1;
  const b3BrainEnter = spring({
    frame: Math.max(0, frame - 690),
    fps,
    config: { damping: 14, stiffness: 120 },
  });
  const b3DopamineLevel = interpolate(frame, [850, 1020], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const b3BrainPulse =
    1 + Math.sin(frame * 0.22) * (0.025 + 0.035 * b3DopamineLevel);
  const b3BeamProgress = interpolate(frame, [845, 920], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // =========================================================================
  // BEAT 4: 1219..1756 (ĐẢO CHIỀU: Sạp vé số + Vé FOMO xoay + Dấu đỏ)
  // =========================================================================
  const b4Active = frame >= 1212 && frame < 1768;
  const b4Opacity =
    frame < 1235
      ? interpolate(frame, [1212, 1235], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : frame > 1735
        ? interpolate(frame, [1735, 1768], [1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        : 1;
  const b4StampSpring = spring({
    frame: Math.max(0, frame - 1300),
    fps,
    config: { damping: 9, stiffness: 250, mass: 0.7 },
  });
  const b4StampScale = interpolate(b4StampSpring, [0, 1], [2.4, 1.0]);
  const b4StampOpacity = frame >= 1300 ? Math.min(1, b4StampSpring * 2.5) : 0;

  // =========================================================================
  // BEAT 5: 1756..2092 (CAO TRÀO: Biểu đồ đối nghịch SVG + Lipstick Effect)
  // =========================================================================
  const b5Active = frame >= 1756 && frame < 2092;
  const b5Opacity =
    frame < 1774
      ? interpolate(frame, [1756, 1774], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : frame >= 2068
        ? interpolate(frame, [2068, 2090], [1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        : 1;
  const b5LineDraw = interpolate(frame, [1766, 1875], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const b5HighlightSweep = interpolate(frame, [1910, 1980], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const b5AreaPulse = 0.16 + 0.08 * Math.sin((frame - 1756) * 0.12);
  const cubicPt = (
    p0: [number, number],
    p1: [number, number],
    p2: [number, number],
    p3: [number, number],
    t: number
  ) => {
    const u = 1 - t;
    return {
      x:
        u * u * u * p0[0] +
        3 * u * u * t * p1[0] +
        3 * u * t * t * p2[0] +
        t * t * t * p3[0],
      y:
        u * u * u * p0[1] +
        3 * u * u * t * p1[1] +
        3 * u * t * t * p2[1] +
        t * t * t * p3[1],
    };
  };
  const b5DotT1 = ((Math.max(0, frame - 1766) % 90) / 90);
  const b5DotT2 = ((Math.max(0, frame - 1766) + 45) % 90) / 90;

  // =========================================================================
  // BEAT 6: 2096..2373 (ĐỐI ĐẦU 2 KHUNG ẢNH THẬT HD + CÂU HỎI 2 CHIỀU)
  // =========================================================================
  const b6Active = frame >= 2096;
  const b6Opacity = interpolate(frame, [2096, 2116], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const b6SplitEnter = spring({
    frame: Math.max(0, frame - 2096),
    fps,
    config: { damping: 14, stiffness: 150 },
  });
  const b6Float = Math.sin((frame - 2096) * 0.08) * 7;

  return (
    <AbsoluteFill style={{ backgroundColor: "#040811", overflow: "hidden" }}>
      {/* 1. MASTER AUDIO */}
      <Audio src={staticFile("audio/master_audio_ve_so.wav")} />

      {/* 2. EMBEDDED BRAND FONTS */}
      <HaDaWhyFontFaces />

      {/* 3. CHANNEL DNA LEVEL-1 MIST BACKDROP (#42B2F2, NO GRID) */}
      <HaDaWhyMistBackground intensity={0.11} accentHex="66, 178, 242" />

      {/* Subtle continuous light sweep */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: sweepX,
          width: 260,
          height: 1920,
          background:
            "linear-gradient(90deg, transparent 0%, rgba(66,178,242,0.06) 50%, transparent 100%)",
          transform: "skewX(-18deg)",
          pointerEvents: "none",
        }}
      />

      {/* 4. MAIN STAGE WITH CAMERA MICRO-SHAKE */}
      <AbsoluteFill
        style={{
          transform: `translate(${shakeX}px, ${shakeY}px)`,
        }}
      >
        {/* TOP KINETIC HOOK HEADER */}
        <KineticHookHeader beat={hookInfo} top={270} />

        {/* =============================================================== */}
        {/* BEAT 1: TỜ VÉ SỐ 10K ĐỐI ĐẦU TIA SÉT THẬT + XÁC SUẤT NHẢY SỐ  */}
        {/* =============================================================== */}
        {b1Active && (
          <AbsoluteFill style={{ opacity: b1Opacity }}>
            {/* Left 3D Lottery Ticket Cutout (Ready at Frame 0!) */}
            <div
              style={{
                position: "absolute",
                left: 55,
                top: 470 + b1Float,
                width: 470,
                transform: `scale(${b1TicketScale}) perspective(900px) rotateY(14deg) rotateZ(-7deg)`,
                filter:
                  "drop-shadow(0 20px 35px rgba(0,0,0,0.9)) drop-shadow(0 0 28px rgba(66,178,242,0.55))",
              }}
            >
              <Img
                src={staticFile("harvested/ve_so_cutout_hd.png")}
                style={{ width: "100%", height: "auto" }}
              />
            </div>

            {/* Right Real Lightning Storm Photo */}
            <div
              style={{
                position: "absolute",
                right: 55,
                top: 465 - b1Float * 0.5,
                width: 470,
                height: 540,
                borderRadius: 22,
                overflow: "hidden",
                border: "3px solid rgba(255, 230, 0, 0.75)",
                boxShadow:
                  "0 24px 48px rgba(0,0,0,0.85), 0 0 36px rgba(255,230,0,0.35)",
                transform: `scale(${b1TicketScale}) perspective(900px) rotateY(-10deg)`,
              }}
            >
              <Img
                src={staticFile("harvested/lightning_storm_real.jpg")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  filter: `brightness(${b1LightningFlash}) contrast(1.18)`,
                }}
              />
            </div>

            {/* Center VS Lightning Bolt SVG */}
            <svg
              width={130}
              height={160}
              viewBox="0 0 130 160"
              style={{
                position: "absolute",
                left: 540 - 65,
                top: 660,
                filter: "drop-shadow(0 0 22px #FFE600)",
                zIndex: 12,
              }}
            >
              <path
                d="M78 6 L22 86 L62 86 L46 154 L108 68 L68 68 Z"
                fill="#FFE600"
                stroke="#05070C"
                strokeWidth="6"
                strokeLinejoin="round"
              />
            </svg>

            {/* Probability Odometer Readouts (Zero-Box Floating Typography) */}
            <div
              style={{
                position: "absolute",
                left: 55,
                top: 1090,
                width: 470,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 30,
                  color: "#42B2F2",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  letterSpacing: "0.04em",
                }}
              >
                TRÚNG ĐỘC ĐẮC
              </div>
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 52,
                  color: "#FF3B47",
                  WebkitTextStroke: "9px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 26px rgba(255,59,71,0.7)",
                }}
              >
                1 / {b1TicketOdds}
              </div>
            </div>

            <div
              style={{
                position: "absolute",
                right: 55,
                top: 1090,
                width: 470,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 30,
                  color: "#FFE600",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  letterSpacing: "0.04em",
                }}
              >
                BỊ SÉT ĐÁNH
              </div>
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 52,
                  color: "#00FF88",
                  WebkitTextStroke: "9px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 26px rgba(0,255,136,0.6)",
                }}
              >
                1 / {b1LightningOdds}
              </div>
            </div>

            {/* Bottom Comparison Tag */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 1320,
                width: 900,
                transform: "translateX(-50%)",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  height: 4,
                  width: "100%",
                  background:
                    "linear-gradient(90deg, #FF3B47 0%, #FFE600 50%, #00FF88 100%)",
                  boxShadow: "0 0 18px rgba(255,230,0,0.65)",
                  marginBottom: 18,
                }}
              />
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 34,
                  color: "#FFFFFF",
                  WebkitTextStroke: "7px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                XÁC SUẤT THẤP HƠN{" "}
                <span style={{ color: "#FFE600" }}>GẤP ĐÔI</span> SÉT ĐÁNH
              </div>
            </div>
          </AbsoluteFill>
        )}

        {/* =============================================================== */}
        {/* BEAT 2: NGƯỜI BÁN VÉ SỐ + ĐỒNG HỒ 16:30 + COINSTREAM 3D         */}
        {/* =============================================================== */}
        {b2Active && (
          <AbsoluteFill style={{ opacity: b2Opacity }}>
            {/* Real Vietnam Lottery Seller Photo */}
            <div
              style={{
                position: "absolute",
                left: 80,
                top: 430,
                width: 920,
                height: 580,
                borderRadius: 24,
                overflow: "hidden",
                border: "3px solid rgba(66,178,242,0.7)",
                boxShadow:
                  "0 28px 60px rgba(0,0,0,0.85), 0 0 38px rgba(66,178,242,0.28)",
                transform: `scale(${interpolate(b2Enter, [0, 1], [0.94, 1])})`,
              }}
            >
              <Img
                src={staticFile("harvested/vn_lottery_seller_real.jpg")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  transform: `scale(${b2PhotoZoom})`,
                }}
              />
            </div>

            {/* Clock Ring 16:30 (SVG + Spatial Floating Text, NO opaque box) */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 1090,
                transform: "translateX(-50%)",
                textAlign: "center",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 28,
                  color: "#42B2F2",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  letterSpacing: "0.08em",
                }}
              >
                KHUNG GIỜ QUAY SỐ
              </div>
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 84,
                  color: "#FFE600",
                  WebkitTextStroke: "10px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 34px rgba(255,230,0,0.75)",
                  lineHeight: 1.05,
                }}
              >
                {b2ClockStr}
              </div>
            </div>

            {/* CoinStream 3D from 10.000đ up to Giấc mơ tiền tỷ */}
            <CoinStream
              p0={{ x: 185, y: 1410 }}
              p1={{ x: 540, y: 1210 }}
              p2={{ x: 895, y: 1380 }}
              startFrame={275}
              endFrame={690}
              coinCount={7}
              useDollarNotes={true}
              dotColor="#FFE600"
            />

            <div
              style={{
                position: "absolute",
                left: 70,
                top: 1435,
                width: 260,
                textAlign: "center",
                fontFamily: "KanitBlack, sans-serif",
                fontSize: 42,
                color: "#FFFFFF",
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              10.000Đ
            </div>
            <div
              style={{
                position: "absolute",
                right: 60,
                top: 1415,
                width: 320,
                textAlign: "center",
                fontFamily: "KanitBlack, sans-serif",
                fontSize: 40,
                color: "#00FF88",
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 0 24px rgba(0,255,136,0.65)",
              }}
            >
              GIẤC MƠ 2 TỶ
            </div>
          </AbsoluteFill>
        )}

        {/* =============================================================== */}
        {/* BEAT 3: DÃY 6 SỐ ODOMETER (5 XANH, 1 ĐỎ) -> BẮN XUNG NÃO 3D    */}
        {/* =============================================================== */}
        {b3Active && (
          <AbsoluteFill style={{ opacity: b3Opacity }}>
            {/* 6-Digit Odometer Strip */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 470,
                transform: "translateX(-50%)",
                display: "flex",
                gap: 18,
                alignItems: "center",
              }}
            >
              {LOTTERY_DIGITS.map((d, idx) => {
                const locked = frame >= d.lockFrame;
                const rollingVal = Math.floor((frame * 0.65 + idx * 3) % 10);
                const displayVal = locked ? d.target : rollingVal;
                const isLastMismatch = locked && !d.match;
                const blink =
                  isLastMismatch && Math.sin(frame * 0.45) > 0 ? 1.1 : 1.0;
                const color = !locked
                  ? "#FFFFFF"
                  : d.match
                    ? "#00FF88"
                    : "#FF3B47";

                return (
                  <div
                    key={idx}
                    style={{
                      width: 126,
                      height: 158,
                      borderRadius: 18,
                      border: `4px solid ${color}`,
                      boxShadow: `0 0 28px ${color}66, inset 0 0 18px ${color}22`,
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "center",
                      justifyContent: "center",
                      transform: `scale(${blink})`,
                    }}
                  >
                    <span
                      style={{
                        fontFamily: "KanitBlack, sans-serif",
                        fontSize: 82,
                        color,
                        WebkitTextStroke: "8px #05070C",
                        paintOrder: "stroke fill",
                        lineHeight: 1,
                      }}
                    >
                      {displayVal}
                    </span>
                    {isLastMismatch && (
                      <span
                        style={{
                          fontFamily: "BeVietnamProBlack, sans-serif",
                          fontSize: 20,
                          color: "#FFE600",
                          WebkitTextStroke: "4px #05070C",
                          paintOrder: "stroke fill",
                        }}
                      >
                        LỆCH 1 SỐ
                      </span>
                    )}
                  </div>
                );
              })}
            </div>

            {/* SVG Neural Energy Impulse Shooting from 6th Digit to Brain */}
            <svg
              width={1080}
              height={1000}
              viewBox="0 0 1080 1000"
              style={{
                position: "absolute",
                left: 0,
                top: 560,
                pointerEvents: "none",
                zIndex: 10,
              }}
            >
              {b3BeamProgress > 0 && (
                <>
                  <path
                    d="M 885 80 Q 870 250 560 400"
                    fill="none"
                    stroke="#FF3B47"
                    strokeWidth="7"
                    strokeDasharray="16 14"
                    strokeDashoffset={-frame * 10}
                    opacity={b3BeamProgress}
                  />
                  <circle
                    cx={560}
                    cy={400}
                    r={28 + b3DopamineLevel * 120}
                    fill="none"
                    stroke="#00FF88"
                    strokeWidth="5"
                    opacity={Math.max(0, 0.85 - b3DopamineLevel * 0.45)}
                  />
                  <circle
                    cx={560}
                    cy={400}
                    r={18 + ((frame * 3) % 90)}
                    fill="none"
                    stroke="#FFE600"
                    strokeWidth="4"
                    opacity={Math.max(0, 0.9 - (((frame * 3) % 90) / 90))}
                  />
                </>
              )}
            </svg>

            {/* 3D Brain Cutout Model */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 730,
                width: 720,
                transform: `translateX(-50%) scale(${b3BrainEnter * b3BrainPulse})`,
                filter: `drop-shadow(0 0 ${24 + b3DopamineLevel * 48}px rgba(0,255,136,0.75)) drop-shadow(0 25px 45px rgba(0,0,0,0.9))`,
              }}
            >
              <Img
                src={staticFile("harvested/brain_neural_cutout_hd.png")}
                style={{ width: "100%", height: "auto" }}
              />
            </div>

            {/* Minimal Dopamine Floating Label */}
            {frame >= 890 && (
              <div
                style={{
                  position: "absolute",
                  left: 540,
                  top: 1410,
                  transform: "translateX(-50%)",
                  textAlign: "center",
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 54,
                  color: "#00FF88",
                  WebkitTextStroke: "9px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 35px rgba(0,255,136,0.9)",
                  letterSpacing: "0.06em",
                }}
              >
                + DOPAMINE HƯNG PHẤN
              </div>
            )}
          </AbsoluteFill>
        )}

        {/* =============================================================== */}
        {/* BEAT 4: SẠP VÉ SỐ CHIỀU + VÉ XOAY FOMO + DẤU ĐỎ BẪY SUÝT TRÚNG  */}
        {/* =============================================================== */}
        {b4Active && (
          <AbsoluteFill style={{ opacity: b4Opacity }}>
            {/* Afternoon Crowd Photo */}
            <div
              style={{
                position: "absolute",
                left: 70,
                top: 430,
                width: 940,
                height: 580,
                borderRadius: 24,
                overflow: "hidden",
                border: "3px solid rgba(255, 59, 71, 0.75)",
                boxShadow: "0 26px 54px rgba(0,0,0,0.85)",
              }}
            >
              <Img
                src={staticFile("harvested/vn_lottery_crowd_afternoon.jpg")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  transform: `scale(${interpolate(frame, [1219, 1756], [1.02, 1.12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})`,
                }}
              />
            </div>

            {/* Orbital FOMO Lottery Copies */}
            {[0, 1, 2, 3].map((i) => {
              const angle = (frame - 1219) * 0.032 + (i * Math.PI) / 2;
              const cx = 540 + Math.cos(angle) * 290;
              const cy = 1215 + Math.sin(angle) * 120;
              const rot = Math.sin(angle) * 16;
              return (
                <div
                  key={i}
                  style={{
                    position: "absolute",
                    left: cx,
                    top: cy,
                    width: 240,
                    transform: `translate(-50%, -50%) rotate(${rot}deg)`,
                    filter:
                      "drop-shadow(0 16px 26px rgba(0,0,0,0.85)) drop-shadow(0 0 18px rgba(255,230,0,0.4))",
                    opacity: 0.92,
                  }}
                >
                  <Img
                    src={staticFile("harvested/ve_so_cutout_hd.png")}
                    style={{ width: "100%", height: "auto" }}
                  />
                </div>
              );
            })}

            {/* Slammed Forensic Transparent Ink Stamp */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 860,
                transform: `translate(-50%, -50%) rotate(-10deg) scale(${b4StampScale})`,
                opacity: b4StampOpacity,
                border: "9px solid #FF2E4C",
                borderRadius: 14,
                padding: "14px 36px",
                backgroundColor: "transparent",
                boxShadow: "0 0 36px rgba(255,46,76,0.65)",
                zIndex: 20,
              }}
            >
              <span
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 64,
                  color: "#FF2E4C",
                  WebkitTextStroke: "4px #05070C",
                  paintOrder: "stroke fill",
                  letterSpacing: "0.05em",
                  whiteSpace: "nowrap",
                }}
              >
                BẪY SUÝT TRÚNG
              </span>
            </div>

            {/* Bottom FOMO Prompt */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 1440,
                width: 900,
                transform: "translateX(-50%)",
                textAlign: "center",
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 38,
                color: "#FFE600",
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              SỢ BỎ LỠ VẬN MAY CHIỀU NAY
            </div>
          </AbsoluteFill>
        )}

        {/* =============================================================== */}
        {/* BEAT 5: BIỂU ĐỒ ĐỐI NGHỊCH ĐỘNG + LIPSTICK EFFECT + 10K HY VỌNG */}
        {/* =============================================================== */}
        {b5Active && (
          <AbsoluteFill style={{ opacity: b5Opacity }}>
            {/* Dual Diverging Trend Chart SVG with Animated Areas & Pulse Dots */}
            <svg
              width={960}
              height={460}
              viewBox="0 0 960 460"
              style={{
                position: "absolute",
                left: 60,
                top: 430,
                overflow: "visible",
              }}
            >
              <defs>
                <linearGradient id="greenAreaGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#00FF88" stopOpacity={b5AreaPulse} />
                  <stop offset="100%" stopColor="#00FF88" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="redAreaGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#FF3B47" stopOpacity={b5AreaPulse * 0.85} />
                  <stop offset="100%" stopColor="#FF3B47" stopOpacity={0} />
                </linearGradient>
              </defs>

              {/* Clean Axis Lines */}
              <line
                x1={70}
                y1={20}
                x2={70}
                y2={420}
                stroke="rgba(255,255,255,0.45)"
                strokeWidth="4"
              />
              <line
                x1={70}
                y1={420}
                x2={910}
                y2={420}
                stroke="rgba(255,255,255,0.45)"
                strokeWidth="4"
              />
              {[120, 220, 320].map((gy) => (
                <line
                  key={gy}
                  x1={70}
                  y1={gy}
                  x2={910}
                  y2={gy}
                  stroke="rgba(255,255,255,0.12)"
                  strokeWidth="2"
                  strokeDasharray="10 10"
                />
              ))}

              {/* Animated Gradient Area Fills */}
              <path
                d="M 90 365 C 310 340, 560 175, 880 65 L 880 420 L 90 420 Z"
                fill="url(#greenAreaGrad)"
                opacity={b5LineDraw}
              />
              <path
                d="M 90 95 C 310 115, 560 275, 880 380 L 880 420 L 90 420 Z"
                fill="url(#redAreaGrad)"
                opacity={b5LineDraw}
              />

              {/* Descending Red Curve: KINH TẾ CHẬT VẬT */}
              <path
                d="M 90 95 C 310 115, 560 275, 880 380"
                fill="none"
                stroke="#FF3B47"
                strokeWidth="11"
                strokeLinecap="round"
                strokeDasharray="950"
                strokeDashoffset={950 * (1 - b5LineDraw)}
                style={{ filter: "drop-shadow(0 0 18px rgba(255,59,71,0.8))" }}
              />

              {/* Ascending Green Curve: NHU CẦU MUA VÉ SỐ */}
              <path
                d="M 90 365 C 310 340, 560 175, 880 65"
                fill="none"
                stroke="#00FF88"
                strokeWidth="11"
                strokeLinecap="round"
                strokeDasharray="950"
                strokeDashoffset={950 * (1 - b5LineDraw)}
                style={{ filter: "drop-shadow(0 0 18px rgba(0,255,136,0.8))" }}
              />

              {/* Continuous Glowing Pulse Dots Traveling Along Curves */}
              {b5LineDraw > 0.35 &&
                [b5DotT1, b5DotT2].map((tVal, idx) => {
                  const ptR = cubicPt([90, 95], [310, 115], [560, 275], [880, 380], tVal);
                  const ptG = cubicPt([90, 365], [310, 340], [560, 175], [880, 65], tVal);
                  return (
                    <g key={idx}>
                      <circle
                        cx={ptR.x}
                        cy={ptR.y}
                        r={12}
                        fill="#FFFFFF"
                        stroke="#FF3B47"
                        strokeWidth="5"
                        style={{ filter: "drop-shadow(0 0 16px #FF3B47)" }}
                      />
                      <circle
                        cx={ptG.x}
                        cy={ptG.y}
                        r={12}
                        fill="#FFFFFF"
                        stroke="#00FF88"
                        strokeWidth="5"
                        style={{ filter: "drop-shadow(0 0 16px #00FF88)" }}
                      />
                    </g>
                  );
                })}
            </svg>

            {/* Chart Floating Labels */}
            <div
              style={{
                position: "absolute",
                right: 90,
                top: 430,
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 30,
                color: "#00FF88",
                WebkitTextStroke: "7px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              MUA VÉ SỐ TĂNG VỌT ↑
            </div>
            <div
              style={{
                position: "absolute",
                right: 90,
                top: 865,
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 30,
                color: "#FF3B47",
                WebkitTextStroke: "7px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              KINH TẾ CHẬT VẬT ↓
            </div>

            {/* Real Economic Knowledge: Lipstick Effect + Real Photo */}
            <div
              style={{
                position: "absolute",
                left: 70,
                top: 945,
                width: 340,
                height: 225,
                borderRadius: 18,
                overflow: "hidden",
                border: "3px solid #FFE600",
                boxShadow: "0 18px 36px rgba(0,0,0,0.85), 0 0 24px rgba(255,230,0,0.3)",
              }}
            >
              <Img
                src={staticFile("harvested/vn_lottery_seller_real.jpg")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  transform: `scale(${interpolate(frame, [1756, 2090], [1.03, 1.12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})`,
                }}
              />
            </div>

            <div
              style={{
                position: "absolute",
                left: 440,
                top: 950,
                width: 575,
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 36,
                  color: "#FFE600",
                  WebkitTextStroke: "7px #05070C",
                  paintOrder: "stroke fill",
                  lineHeight: 1.1,
                }}
              >
                HIỆU ỨNG SON MÔI
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 22,
                  color: "#42B2F2",
                  WebkitTextStroke: "5px #05070C",
                  paintOrder: "stroke fill",
                  marginBottom: 8,
                }}
              >
                (LIPSTICK EFFECT)
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 27,
                  color: "#FFFFFF",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  lineHeight: 1.3,
                }}
              >
                Kinh tế khó → Giảm chi tiêu lớn, tăng mua vé 10k cầu may
              </div>
            </div>

            {/* Highlighted Evidence Note (Yellow Highlighter Sweep) */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 1245,
                width: 900,
                transform: "translateX(-50%)",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 30,
                  color: "#FFFFFF",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  marginBottom: 14,
                }}
              >
                CHẲNG THỨ GÌ RẺ HƠN MÀ CHO TA:
              </div>
              <div
                style={{
                  position: "relative",
                  display: "inline-block",
                  padding: "10px 26px",
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    left: 0,
                    top: 6,
                    bottom: 6,
                    width: `${b5HighlightSweep}%`,
                    backgroundColor: "#FFE600",
                    borderRadius: 10,
                    boxShadow: "0 0 32px rgba(255,230,0,0.7)",
                    zIndex: 0,
                  }}
                />
                <span
                  style={{
                    position: "relative",
                    zIndex: 1,
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 54,
                    color: b5HighlightSweep > 45 ? "#05070C" : "#FFE600",
                    whiteSpace: "nowrap",
                  }}
                >
                  10.000Đ = 1 NGÀY HY VỌNG
                </span>
              </div>
            </div>
          </AbsoluteFill>
        )}

        {/* =============================================================== */}
        {/* BEAT 6: ĐỐI ĐẦU 2 KHUNG ẢNH THẬT HD + CÂU HỎI TRANH LUẬN 2 CHIỀU */}
        {/* =============================================================== */}
        {b6Active && (
          <AbsoluteFill style={{ opacity: b6Opacity }}>
            {/* Left Real Photo Frame: MUA NIỀM VUI HY VỌNG */}
            <div
              style={{
                position: "absolute",
                left: 55,
                top: 465 + b6Float * 0.5,
                width: 455,
                height: 520,
                borderRadius: 22,
                overflow: "hidden",
                border: "4px solid #00FF88",
                boxShadow:
                  "0 24px 48px rgba(0,0,0,0.85), 0 0 32px rgba(0,255,136,0.35)",
                transform: `scale(${b6SplitEnter})`,
              }}
            >
              <Img
                src={staticFile("harvested/vn_lottery_seller_real.jpg")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  transform: `scale(${interpolate(frame, [2096, 2373], [1.04, 1.13], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})`,
                }}
              />
            </div>

            {/* Right Real Photo Frame: GIẤC MƠ KHÓ THÀNH */}
            <div
              style={{
                position: "absolute",
                right: 55,
                top: 465 - b6Float * 0.5,
                width: 455,
                height: 520,
                borderRadius: 22,
                overflow: "hidden",
                border: "4px solid #FF3B47",
                boxShadow:
                  "0 24px 48px rgba(0,0,0,0.85), 0 0 32px rgba(255,59,71,0.35)",
                transform: `scale(${b6SplitEnter})`,
              }}
            >
              <Img
                src={staticFile("harvested/vn_lottery_crowd_afternoon.jpg")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  transform: `scale(${interpolate(frame, [2096, 2373], [1.04, 1.13], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })})`,
                }}
              />
            </div>

            {/* Tilted 3D Ticket Accent Overlapping Right Frame */}
            <div
              style={{
                position: "absolute",
                right: 35,
                top: 865 - b6Float * 0.6,
                width: 245,
                transform: `scale(${b6SplitEnter}) rotate(-12deg)`,
                filter:
                  "drop-shadow(0 14px 26px rgba(0,0,0,0.9)) drop-shadow(0 0 18px rgba(255,59,71,0.55))",
                zIndex: 10,
              }}
            >
              <Img
                src={staticFile("harvested/ve_so_cutout_hd.png")}
                style={{ width: "100%", height: "auto" }}
              />
            </div>

            {/* Center Energy Divider Beam */}
            <div
              style={{
                position: "absolute",
                left: 538,
                top: 465,
                width: 4,
                height: 520,
                background:
                  "linear-gradient(180deg, #42B2F2 0%, #FFE600 50%, #FF3B47 100%)",
                boxShadow: "0 0 22px rgba(255,230,0,0.85)",
                zIndex: 12,
              }}
            />
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 725,
                transform: `translate(-50%, -50%) scale(${b6SplitEnter})`,
                fontFamily: "KanitBlack, sans-serif",
                fontSize: 54,
                color: "#FFE600",
                WebkitTextStroke: "9px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 0 30px rgba(255,230,0,0.9)",
                zIndex: 14,
              }}
            >
              VS
            </div>

            {/* Left Choice Label */}
            <div
              style={{
                position: "absolute",
                left: 55,
                top: 1030,
                width: 455,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 42,
                  color: "#00FF88",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 26px rgba(0,255,136,0.65)",
                  lineHeight: 1.15,
                }}
              >
                MUA NIỀM VUI HY VỌNG
              </div>
            </div>

            {/* Right Choice Label */}
            <div
              style={{
                position: "absolute",
                right: 55,
                top: 1030,
                width: 455,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 42,
                  color: "#FF3B47",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 26px rgba(255,59,71,0.65)",
                  lineHeight: 1.15,
                }}
              >
                GIẤC MƠ KHÓ THÀNH
              </div>
            </div>

            {/* Two-Sided Debate Question */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 1260,
                width: 920,
                transform: "translateX(-50%)",
                textAlign: "center",
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 42,
                color: "#FFE600",
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 0 28px rgba(255,230,0,0.55)",
                lineHeight: 1.25,
              }}
            >
              THEO BẠN, BỎ 10K MỖI CHIỀU LÀ ĐÚNG HAY SAI?
            </div>
          </AbsoluteFill>
        )}
      </AbsoluteFill>

      {/* 5. 2-LAYER COPYRIGHT WATERMARK */}
      <ChannelWatermark9x16 />
    </AbsoluteFill>
  );
};
