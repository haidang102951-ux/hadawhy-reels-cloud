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
import { KineticWordCaption } from "./components/KineticWordCaption";
import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16";
import { CoinStream } from "./components/CoinStream";
import { AnatomyCallout3D } from "./components/AnatomyCallout3D";
import { ScaleComparison3D } from "./components/ScaleComparison3D";
import { RealPersonSpotlight3D } from "./components/RealPersonSpotlight3D";
import { RAP_PHIM_CAPTIONS } from "./rapPhimCaptionsData";

export const RapPhimBongNgo42s: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Global camera micro-shake on heavy forensic impacts
  const impactFrames = [4, 160, 495, 670, 1300, 1540, 1850, 2334];
  let shakeX = 0;
  let shakeY = 0;
  for (const imp of impactFrames) {
    if (frame >= imp && frame < imp + 14) {
      const dt = frame - imp;
      const decay = Math.exp(-dt * 0.28);
      shakeX += Math.sin(dt * 3.1) * 12 * decay;
      shakeY += Math.cos(dt * 3.5) * 10 * decay;
    }
  }

  // =========================================================================
  // BEAT 1 (0..295 | 0.00s..4.92s): VÉ PHIM 100K VS 0 ĐỒNG LÃI
  // Frame 0 ready: Ticket + Hall already on stage with Slam Zoom 1.35 -> 1.0
  // =========================================================================
  const b1Active = frame <= 300;
  const b1Exit = interpolate(frame, [280, 296], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const slamProgress = spring({
    frame: Math.max(0, frame - 2),
    fps,
    config: { damping: 14, stiffness: 180, mass: 0.9 },
  });
  const slamScale = interpolate(slamProgress, [0, 1], [1.35, 1.0]);

  // First visual turn < 0.80s (frames 14..46)
  const priceOdo = Math.round(
    interpolate(frame, [10, 42], [0, 100], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );
  const zeroProfitPop = spring({
    frame: Math.max(0, frame - 26),
    fps,
    config: { damping: 12, stiffness: 210 },
  });
  // Escalation at ~1.6s (frame 96) + Forensic Stamp at 2.67s (frame 160)
  const escalatePop = spring({
    frame: Math.max(0, frame - 96),
    fps,
    config: { damping: 13, stiffness: 170 },
  });
  const stamp1Pop = spring({
    frame: Math.max(0, frame - 160),
    fps,
    config: { damping: 10, stiffness: 240, mass: 0.7 },
  });

  // =========================================================================
  // BEAT 2 (285..815 | 4.75s..13.58s): HOLLYWOOD HÚT 55%-65% -> 70% TIỀN VÉ
  // =========================================================================
  const b2Active = frame >= 285 && frame <= 820;
  const b2Fade =
    interpolate(frame, [285, 302], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [798, 815], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  const b2Local = Math.max(0, frame - 285);
  const b2Intro = spring({
    frame: b2Local,
    fps,
    config: { damping: 14, stiffness: 140 },
  });
  const pctHollywood =
    frame < 660
      ? Math.round(
          interpolate(frame, [460, 560], [55, 65], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        )
      : Math.round(
          interpolate(frame, [660, 725], [65, 70], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        );
  const isBlockbuster = frame >= 660;
  const blockbusterPulse = spring({
    frame: Math.max(0, frame - 665),
    fps,
    config: { damping: 11, stiffness: 220 },
  });

  // =========================================================================
  // BEAT 4A (1510..1720 | 25.17s..28.67s): 100% BỎNG NƯỚC CHẢY VÀO TÚI RẠP
  // =========================================================================
  const b4aActive = frame >= 1510 && frame <= 1720;
  const b4aFade =
    interpolate(frame, [1510, 1528], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [1700, 1720], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  const b4aPop = spring({
    frame: Math.max(0, frame - 1515),
    fps,
    config: { damping: 14, stiffness: 150 },
  });

  // =========================================================================
  // BEAT 4B (1710..2020 | 28.50s..33.67s): 25% DOANH THU VS 50% LỢI NHUẬN
  // =========================================================================
  const b4bActive = frame >= 1710 && frame <= 2020;
  const b4bFade =
    interpolate(frame, [1710, 1728], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [2000, 2020], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  const revGrow = spring({
    frame: Math.max(0, frame - 1755),
    fps,
    config: { damping: 13, stiffness: 120 },
  });
  const profGrow = spring({
    frame: Math.max(0, frame - 1865),
    fps,
    config: { damping: 12, stiffness: 110 },
  });

  // =========================================================================
  // BEAT 5 (2010..2520 | 33.50s..42.00s): RẠP = TIỆM BỎNG NGÔ, PHIM = CÁI MỒI
  // =========================================================================
  const b5Active = frame >= 2010;
  const b5Fade = interpolate(frame, [2010, 2028], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const baitPop = spring({
    frame: Math.max(0, frame - 2310),
    fps,
    config: { damping: 10, stiffness: 220 },
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#04070D", overflow: "hidden" }}>
      <style>{`
        @font-face {
          font-family: 'BeVietnamProBlack';
          src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
          font-weight: 900;
          font-style: normal;
        }
        @font-face {
          font-family: 'BeVietnamProExtraBold';
          src: url('${staticFile("fonts/BeVietnamPro-ExtraBold.ttf")}') format('truetype');
          font-weight: 800;
          font-style: normal;
        }
        @font-face {
          font-family: 'KanitBlack';
          src: url('${staticFile("fonts/Kanit-Black.ttf")}') format('truetype');
          font-weight: 900;
          font-style: normal;
        }
      `}</style>

      {/* Master Mixed Audio (Voice + Trailer BGM + Foley) */}
      <Audio src={staticFile("audio/master_audio.wav")} />

      {/* Brand Signature ADN Backdrop (Mức 1: Nền đen Obsidian + Sương mù xanh #42B2F2 nhẹ, KHÔNG lưới ô vuông) */}
      <HaDaWhyMistBackground intensity={0.11} accentHex="66, 178, 242" />

      {/* 2-Layer Anti-Reup Watermark */}
      <ChannelWatermark9x16 />

      {/* TẦNG TRÊN (Y: 220..490px): KINETIC IMPACTHOOK 2 TẦNG ZERO-BOX + SPRING SLAM */}
      {(() => {
        const beatInfo =
          frame < 285
            ? {
                start: 0,
                eyebrow: "VÉ XEM PHIM 100.000Đ",
                hero: "RẠP LÃI 0 ĐỒNG?",
                accent: "#FF3B47",
              }
            : frame < 805
            ? {
                start: 285,
                eyebrow: "HOLLYWOOD LẤY THẲNG",
                hero: isBlockbuster ? "70% TIỀN VÉ" : "55% - 65% TIỀN VÉ",
                accent: isBlockbuster ? "#FF3B47" : "#FFE600",
              }
            : frame < 864
            ? {
                start: 785,
                eyebrow: "VẬY RẠP PHIM",
                hero: "SỐNG BẰNG GÌ?",
                accent: "#FF3B47",
              }
            : frame < 972
            ? {
                start: 864,
                eyebrow: "CÂU TRẢ LỜI BẤT NGỜ",
                hero: "HỘP BỎNG NGÔ!",
                accent: "#FFE600",
              }
            : frame < 1150
            ? {
                start: 972,
                eyebrow: "BÓC TÁCH 1 HỘP BỎNG NGÔ",
                hero: "CHI PHÍ RẺ BẤT NGỜ",
                accent: "#FFE600",
              }
            : frame < 1510
            ? {
                start: 1030,
                eyebrow: "VỐN CHỈ 15 - 35 XU",
                hero: "LÃI 85% (GẤP 20 LẦN)",
                accent: "#FFE600",
              }
            : frame < 1710
            ? {
                start: 1510,
                eyebrow: "100% TIỀN BỎNG NƯỚC",
                hero: "CHẢY THẲNG TÚI RẠP",
                accent: "#FFE600",
              }
            : frame < 2010
            ? {
                start: 1710,
                eyebrow: "CHỈ 25% DOANH THU",
                hero: "ĐẺ RA 50% LỢI NHUẬN",
                accent: "#FFE600",
              }
            : {
                start: 2010,
                eyebrow: "RẠP LÀ TIỆM BỎNG NGÔ",
                hero: "PHIM CHỈ LÀ CÁI MỒI",
                accent: "#FF3B47",
              };

        const hookSpring = spring({
          frame: Math.max(0, frame - beatInfo.start),
          fps,
          config: { damping: 12, stiffness: 210, mass: 0.75 },
        });
        const hookScale = interpolate(hookSpring, [0, 1], [1.38, 1.0]);
        const hookOpacity = interpolate(hookSpring, [0, 0.35], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });

        return (
          <div
            style={{
              position: "absolute",
              left: 540,
              top: 345,
              width: 960,
              transform: `translate(-50%, -50%) scale(${hookScale})`,
              opacity: hookOpacity,
              textAlign: "center",
              pointerEvents: "none",
              zIndex: 25,
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 42,
                lineHeight: 1.12,
                letterSpacing: "0.03em",
                color: "#FFFFFF",
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 8px 22px rgba(0,0,0,0.95)",
                marginBottom: 6,
              }}
            >
              {beatInfo.eyebrow}
            </div>
            <div
              style={{
                fontFamily: "KanitBlack, sans-serif",
                fontSize: 82,
                lineHeight: 1.02,
                color: beatInfo.accent,
                WebkitTextStroke: "11px #05070C",
                paintOrder: "stroke fill",
                textShadow: `0 0 36px ${beatInfo.accent}AA, 0 10px 28px rgba(0,0,0,0.96)`,
              }}
            >
              {beatInfo.hero}
            </div>
          </div>
        );
      })()}

      {/* Không chạy phụ đề karaoke đáy - dành 100% không gian cho minh họa kiến thức 3D */}

      {/* Main 3D Stage Container with Camera Shake */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate(${shakeX}px, ${shakeY}px)`,
        }}
      >
        {/* =================================================================
            BEAT 1 (0..295): VÉ XEM PHIM 100K VS 0 ĐỒNG LÃI
            ================================================================= */}
        {b1Active && (
          <div style={{ position: "absolute", inset: 0, opacity: b1Exit }}>
            {/* Real Cinema Hall Tilted 3D Backdrop (Ready at Frame 0) */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 680,
                width: 820,
                height: 440,
                perspective: 1100,
                transform: `translate(-50%, -50%) scale(${slamScale})`,
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  transform: "rotateX(7deg) rotateY(-4deg)",
                  borderRadius: 28,
                  overflow: "hidden",
                  border: "3px solid rgba(255, 230, 0, 0.45)",
                  boxShadow: "0 35px 80px rgba(0,0,0,0.92)",
                }}
              >
                <Img
                  src={staticFile("harvested/cinema_screen_hall.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    filter: "brightness(0.62) contrast(1.15)",
                  }}
                />
              </div>
            </div>

            {/* Hero 3D Cutout Cinema Ticket Ready at Frame 0 */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 920 + Math.sin(frame * 0.08) * 8,
                width: 540,
                transform: `translate(-50%, -50%) scale(${slamScale}) rotate(-6deg)`,
              }}
            >
              <Img
                src={staticFile("harvested/cinema_ticket_cutout.png")}
                style={{
                  width: "100%",
                  height: "auto",
                  filter:
                    "drop-shadow(0px 0px 8px rgba(255,230,0,0.8)) drop-shadow(0px 28px 40px rgba(0,0,0,0.95))",
                }}
              />
            </div>

            {/* Left Odometer: 100.000đ (Pop < 0.8s) */}
            <div
              style={{
                position: "absolute",
                left: 250,
                top: 1280,
                transform: "translate(-50%, -50%)",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 34,
                  color: "#FFFFFF",
                  letterSpacing: 2,
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                GIÁ VÉ
              </div>
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 88,
                  color: "#FFE600",
                  WebkitTextStroke: "10px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 32px rgba(255,230,0,0.65)",
                  lineHeight: 1.0,
                }}
              >
                {priceOdo}K
              </div>
            </div>

            {/* Right Counter-Turn: 0 ĐỒNG LÃI (Pop < 0.8s, Single-Line Locked) */}
            <div
              style={{
                position: "absolute",
                left: 770,
                top: 1280,
                transform: `translate(-50%, -50%) scale(${zeroProfitPop})`,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 34,
                  color: "#FFFFFF",
                  letterSpacing: 2,
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  whiteSpace: "nowrap",
                }}
              >
                LÃI CỦA RẠP
              </div>
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 76,
                  color: "#FF3B47",
                  WebkitTextStroke: "10px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 36px rgba(255,59,71,0.8)",
                  lineHeight: 1.0,
                  whiteSpace: "nowrap",
                }}
              >
                0 ĐỒNG
              </div>
            </div>

            {/* Escalation Baseline Horizon */}
            <div
              style={{
                position: "absolute",
                left: 90,
                top: 1365,
                width: 900 * escalatePop,
                height: 6,
                borderRadius: 3,
                background:
                  "linear-gradient(90deg, #FFE600 0%, rgba(255,255,255,0.4) 50%, #FF3B47 100%)",
                boxShadow: "0 0 22px rgba(255,230,0,0.5)",
              }}
            />

            {/* Transparent Legal Ink Stamp at Frame 160 */}
            {frame >= 160 && (
              <div
                style={{
                  position: "absolute",
                  left: 540,
                  top: 1020,
                  transform: `translate(-50%, -50%) rotate(-14deg) scale(${interpolate(
                    stamp1Pop,
                    [0, 1],
                    [2.4, 1.0]
                  )})`,
                  border: "10px solid #FF3B47",
                  borderRadius: 16,
                  padding: "14px 36px",
                  color: "#FF3B47",
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 64,
                  letterSpacing: 4,
                  textShadow: "0 0 24px rgba(255,59,71,0.8)",
                  boxShadow: "0 0 30px rgba(255,59,71,0.45)",
                  backgroundColor: "transparent",
                }}
              >
                LÃI VÉ = 0%
              </div>
            )}
          </div>
        )}

        {/* =================================================================
            BEAT 2 (285..815): HOLLYWOOD LẤY THẲNG 55% - 70% TIỀN VÉ
            ================================================================= */}
        {b2Active && (
          <div style={{ position: "absolute", inset: 0, opacity: b2Fade }}>
            {/* Left Node: Rạp Chiếu Phim (Large Crisp Auditorium Stage) */}
            <div
              style={{
                position: "absolute",
                left: 270,
                top: 1060,
                width: 440,
                transform: `translate(-50%, -50%) scale(${b2Intro})`,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  width: 440,
                  height: 310,
                  borderRadius: 24,
                  overflow: "hidden",
                  border: "4px solid rgba(255,255,255,0.65)",
                  boxShadow: "0 24px 60px rgba(0,0,0,0.92)",
                }}
              >
                <Img
                  src={staticFile("harvested/cinema_screen_hall.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    filter: "brightness(1.08) contrast(1.08)",
                  }}
                />
              </div>
              <div
                style={{
                  marginTop: 16,
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 38,
                  color: "#FFFFFF",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                RẠP PHIM
              </div>
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 64,
                  color: isBlockbuster ? "#FF3B47" : "#FFE600",
                  WebkitTextStroke: "9px #05070C",
                  paintOrder: "stroke fill",
                  lineHeight: 1.0,
                }}
              >
                {100 - pctHollywood}%
              </div>
            </div>

            {/* Right Node: Hollywood Sign (Iconic Landmark, Large Impact) */}
            <div
              style={{
                position: "absolute",
                left: 785,
                top: 760,
                width: 470,
                transform: `translate(-50%, -50%) scale(${b2Intro})`,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  width: 470,
                  height: 310,
                  borderRadius: 26,
                  overflow: "hidden",
                  border: `4px solid ${isBlockbuster ? "#FF3B47" : "#FFE600"}`,
                  boxShadow: isBlockbuster
                    ? "0 25px 65px rgba(255,59,71,0.6)"
                    : "0 25px 65px rgba(255,230,0,0.45)",
                }}
              >
                <Img
                  src={staticFile("harvested/hollywood_studio_gate.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    filter: "contrast(1.1) saturate(1.15)",
                  }}
                />
              </div>
              <div
                style={{
                  marginTop: 16,
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 40,
                  color: "#FFE600",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                HOLLYWOOD
              </div>
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 102,
                  color: isBlockbuster ? "#FF3B47" : "#FFE600",
                  WebkitTextStroke: "11px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: isBlockbuster
                    ? "0 0 38px rgba(255,59,71,0.9)"
                    : "0 0 32px rgba(255,230,0,0.65)",
                  lineHeight: 0.95,
                  transform: isBlockbuster
                    ? `scale(${interpolate(blockbusterPulse, [0, 1], [1.35, 1.0])})`
                    : "scale(1)",
                }}
              >
                {pctHollywood}%
              </div>
            </div>

            {/* Ticket Cash Flow Streaming Dollars & Coins from Cinema to Hollywood */}
            <CoinStream
              p0={{ x: 350, y: 980 }}
              p1={{ x: 540, y: 580 }}
              p2={{ x: 740, y: 740 }}
              startFrame={315}
              endFrame={810}
              coinCount={11}
              dotColor={isBlockbuster ? "#FF3B47" : "#FFE600"}
              primaryItemSrc="objects/dollar.png"
              secondaryItemSrc="objects/coin.png"
            />

            {/* Floating Contract + Magnifying Glass 3D Evidence */}
            <div
              style={{
                position: "absolute",
                left: 250,
                top: 660 + Math.sin(frame * 0.09) * 8,
                width: 155,
                transform: "translate(-50%, -50%) rotate(-8deg)",
                pointerEvents: "none",
              }}
            >
              <Img
                src={staticFile("objects/contract.png")}
                style={{
                  width: "100%",
                  height: "auto",
                  filter: "drop-shadow(0 16px 26px rgba(0,0,0,0.9))",
                }}
              />
              <Img
                src={staticFile("objects/magnifying_glass.png")}
                style={{
                  position: "absolute",
                  right: -32,
                  bottom: -24,
                  width: 96,
                  height: "auto",
                  transform: `rotate(${Math.sin(frame * 0.08) * 10}deg)`,
                  filter: "drop-shadow(0 10px 18px rgba(0,0,0,0.9))",
                }}
              />
            </div>

            {/* Bottom Zero-Box Callout (Spacious below 37% label) */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 1420,
                transform: "translate(-50%, -50%)",
                textAlign: "center",
                width: 920,
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 48,
                  color: isBlockbuster ? "#FF3B47" : "#FFFFFF",
                  WebkitTextStroke: "9px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                {isBlockbuster ? "BOM TẤN LỚN: THU TỚI 70%" : "TUẦN ĐẦU CÔNG CHIẾU"}
              </div>
            </div>
          </div>
        )}

        {/* =================================================================
            BEAT 3A-1 (785..864): CÂU HỎI "VẬY RẠP SỐNG BẰNG GÌ?" -> BÍ ẨN + DẤU ?
            ================================================================= */}
        {frame >= 785 && frame < 864 && (
          <div style={{ position: "absolute", inset: 0 }}>
            {(() => {
              const qPop = spring({
                frame: Math.max(0, frame - 785),
                fps,
                config: { damping: 12, stiffness: 180 },
              });
              const qScale = interpolate(qPop, [0, 1], [0.75, 1.0]);
              const qPulse = 1 + Math.sin((frame - 785) * 0.22) * 0.06;
              return (
                <>
                  {/* Cinema Hall Backdrop */}
                  <div
                    style={{
                      position: "absolute",
                      left: 540,
                      top: 900,
                      width: 820,
                      height: 480,
                      borderRadius: 28,
                      overflow: "hidden",
                      border: "4px solid rgba(255, 59, 71, 0.7)",
                      boxShadow: "0 30px 80px rgba(0,0,0,0.95)",
                      transform: `translate(-50%, -50%) scale(${qScale})`,
                    }}
                  >
                    <Img
                      src={staticFile("harvested/cinema_screen_hall.png")}
                      style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        filter: "brightness(0.55) contrast(1.2)",
                      }}
                    />
                  </div>
                  {/* Mystery Silhouette + Giant Glowing ? */}
                  <svg
                    width={420}
                    height={520}
                    viewBox="0 0 240 300"
                    style={{
                      position: "absolute",
                      left: 420,
                      top: 1120,
                      transform: `translate(-50%, -50%) scale(${qScale})`,
                      filter: "drop-shadow(0 20px 35px rgba(0,0,0,0.95))",
                    }}
                  >
                    <circle cx="120" cy="78" r="44" fill="#0B111E" stroke="#FF3B47" strokeWidth="5" />
                    <path
                      d="M36 270 C36 185, 204 185, 204 270 Z"
                      fill="#0B111E"
                      stroke="#FF3B47"
                      strokeWidth="5"
                    />
                  </svg>
                  <div
                    style={{
                      position: "absolute",
                      left: 690,
                      top: 1050,
                      transform: `translate(-50%, -50%) scale(${qPulse}) rotate(8deg)`,
                      fontFamily: "KanitBlack, sans-serif",
                      fontSize: 280,
                      lineHeight: 0.9,
                      color: "#FF3B47",
                      WebkitTextStroke: "14px #05070C",
                      paintOrder: "stroke fill",
                      textShadow: "0 0 55px rgba(255,59,71,0.95)",
                    }}
                  >
                    ?
                  </div>
                </>
              );
            })()}
          </div>
        )}

        {/* =================================================================
            BEAT 3A-2 (864..972): ĐÁP ÁN "CHÍNH LÀ HỘP BỎNG NGÔ TRƯỚC CỬA"
            ================================================================= */}
        {frame >= 864 && frame < 972 && (
          <div style={{ position: "absolute", inset: 0 }}>
            {(() => {
              const revPop = spring({
                frame: Math.max(0, frame - 864),
                fps,
                config: { damping: 11, stiffness: 200, mass: 0.85 },
              });
              const boxY = interpolate(revPop, [0, 1], [1500, 1080]);
              const boxScale = interpolate(revPop, [0, 1], [0.55, 1.05]);
              return (
                <>
                  <div
                    style={{
                      position: "absolute",
                      left: 540,
                      top: 760,
                      width: 820,
                      height: 430,
                      borderRadius: 26,
                      overflow: "hidden",
                      border: "4px solid rgba(255, 230, 0, 0.7)",
                      boxShadow: "0 30px 80px rgba(0,0,0,0.95)",
                      transform: "translate(-50%, -50%)",
                    }}
                  >
                    <Img
                      src={staticFile("harvested/cinema_concession_crowd.png")}
                      style={{ width: "100%", height: "100%", objectFit: "cover" }}
                    />
                  </div>
                  <div
                    style={{
                      position: "absolute",
                      left: 540,
                      top: boxY,
                      width: 500,
                      transform: `translate(-50%, -50%) scale(${boxScale})`,
                    }}
                  >
                    <Img
                      src={staticFile("harvested/popcorn_bucket_cutout.png")}
                      style={{
                        width: "100%",
                        height: "auto",
                        filter:
                          "drop-shadow(0 0 18px rgba(255,230,0,0.85)) drop-shadow(0 30px 45px rgba(0,0,0,0.95))",
                      }}
                    />
                  </div>
                </>
              );
            })()}
          </div>
        )}

        {/* =================================================================
            BEAT 3A-3 (972..1150): CHI PHÍ NGÔ, DẦU VÀ HỘP GIẤY
            ================================================================= */}
        <AnatomyCallout3D
          startFrame={972}
          endFrame={1150}
          centerCutoutSrc="harvested/popcorn_bucket_cutout.png"
          centerX={540}
          centerY={1080}
          centerWidth={480}
          callouts={[
            {
              anchorX: 480,
              anchorY: 910,
              labelX: 250,
              labelY: 730,
              title: "NGÔ HẠT",
              value: "~$0.10",
              accentColor: "#FFE600",
              delayFrames: 8,
            },
            {
              anchorX: 610,
              anchorY: 960,
              labelX: 830,
              labelY: 770,
              title: "DẦU & BƠ",
              value: "~$0.08",
              accentColor: "#FFE600",
              delayFrames: 18,
            },
            {
              anchorX: 540,
              anchorY: 1210,
              labelX: 790,
              labelY: 1390,
              title: "HỘP GIẤY",
              value: "~$0.07",
              accentColor: "#FFFFFF",
              delayFrames: 28,
            },
          ]}
        />

        {/* =================================================================
            BEAT 3B (1145..1520): GIÁ VỐN 15-35 XU VS BIÊN LÃI 85% (GẤP 20 LẦN)
            ================================================================= */}
        {frame >= 1145 && frame <= 1520 && (
          <div
            style={{
              position: "absolute",
              left: 265,
              top: 675,
              width: 350,
              transform: "translate(-50%, -50%)",
              textAlign: "center",
              zIndex: 4,
              pointerEvents: "none",
            }}
          >
            <div
              style={{
                width: 350,
                height: 210,
                borderRadius: 20,
                overflow: "hidden",
                border: "3px solid rgba(255, 230, 0, 0.7)",
                boxShadow: "0 20px 50px rgba(0,0,0,0.9)",
              }}
            >
              <Img
                src={staticFile("harvested/cinema_concession_crowd.png")}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </div>
            <Img
              src={staticFile("objects/balance_scale.png")}
              style={{
                position: "absolute",
                right: -36,
                top: -28,
                width: 110,
                height: "auto",
                transform: `rotate(${Math.sin(frame * 0.08) * 6}deg)`,
                filter: "drop-shadow(0 12px 24px rgba(0,0,0,0.9))",
              }}
            />
          </div>
        )}
        <ScaleComparison3D
          startFrame={1145}
          endFrame={1520}
          leftItemSrc="harvested/corn_kernels_cutout.png"
          leftItemCount={1}
          leftLabel="GIÁ VỐN: 15-35 XU"
          rightPrimaryStackSrc="harvested/popcorn_bucket_cutout.png"
          rightSecondaryStackSrc="harvested/cinema_soda_cup_cutout.png"
          rightTopTitle="GẤP >20 LẦN"
          rightStartNumber={0}
          rightTargetNumber={85}
          rightUnitSuffix="%"
          rightLabel="BIÊN LÃI BỎNG NGÔ"
          stampText="LÃI 85%"
        />

        {/* =================================================================
            BEAT 4A (1510..1720): 100% TIỀN BỎNG NƯỚC CHẢY VÀO TÚI RẠP
            ================================================================= */}
        {b4aActive && (
          <div style={{ position: "absolute", inset: 0, opacity: b4aFade }}>
            {/* Left Source: Quầy Bỏng Nước */}
            <div
              style={{
                position: "absolute",
                left: 250,
                top: 900,
                transform: `translate(-50%, -50%) scale(${b4aPop})`,
                textAlign: "center",
              }}
            >
              <Img
                src={staticFile("harvested/popcorn_bucket_cutout.png")}
                style={{
                  width: 310,
                  height: "auto",
                  filter:
                    "drop-shadow(0 0 8px rgba(255,230,0,0.7)) drop-shadow(0 22px 35px rgba(0,0,0,0.9))",
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
                QUẦY BỎNG NƯỚC
              </div>
            </div>

            {/* Right Destination: Túi Rạp Phim */}
            <div
              style={{
                position: "absolute",
                left: 800,
                top: 1050,
                transform: `translate(-50%, -50%) scale(${b4aPop})`,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  width: 380,
                  height: 260,
                  borderRadius: 24,
                  overflow: "hidden",
                  border: "4px solid #FFE600",
                  boxShadow: "0 25px 60px rgba(255,230,0,0.45)",
                }}
              >
                <Img
                  src={staticFile("harvested/cinema_screen_hall.png")}
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
              </div>
              <div
                style={{
                  marginTop: 16,
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 40,
                  color: "#FFE600",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                TÚI RẠP PHIM
              </div>
            </div>

            <CoinStream
              p0={{ x: 350, y: 860 }}
              p1={{ x: 560, y: 660 }}
              p2={{ x: 770, y: 980 }}
              startFrame={1518}
              endFrame={1715}
              coinCount={7}
              dotColor="#FFE600"
              primaryItemSrc="harvested/popcorn_bucket_cutout.png"
              secondaryItemSrc="harvested/cinema_soda_cup_cutout.png"
            />

            <div
              style={{
                position: "absolute",
                left: 540,
                top: 1295,
                transform: "translate(-50%, -50%)",
                textAlign: "center",
                width: 920,
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 92,
                  color: "#FFE600",
                  WebkitTextStroke: "11px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 36px rgba(255,230,0,0.75)",
                  lineHeight: 1.0,
                }}
              >
                100% VÀO TÚI RẠP
              </div>
            </div>
          </div>
        )}

        {/* =================================================================
            BEAT 4B (1710..2020): 25% DOANH THU NHƯNG MANG VỀ 50% LỢI NHUẬN
            ================================================================= */}
        {b4bActive && (
          <div style={{ position: "absolute", inset: 0, opacity: b4bFade }}>
            {/* Horizon Baseline */}
            <div
              style={{
                position: "absolute",
                left: 110,
                top: 1420,
                width: 860,
                height: 8,
                borderRadius: 4,
                background:
                  "linear-gradient(90deg, rgba(255,255,255,0.35) 0%, #FFE600 100%)",
                boxShadow: "0 0 24px rgba(255,230,0,0.5)",
              }}
            />

            {/* Column 1: 25% Doanh Thu */}
            <div
              style={{
                position: "absolute",
                left: 320,
                bottom: 500,
                width: 210,
                height: Math.max(24, 300 * revGrow),
                transform: "translateX(-50%)",
                borderRadius: "20px 20px 0 0",
                background:
                  "linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(160,175,195,0.65) 100%)",
                boxShadow: "0 0 32px rgba(255,255,255,0.28)",
              }}
            />
            <div
              style={{
                position: "absolute",
                left: 320,
                top: 1420 - Math.max(24, 300 * revGrow) - 110,
                transform: "translate(-50%, -50%)",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 88,
                  color: "#FFFFFF",
                  WebkitTextStroke: "10px #05070C",
                  paintOrder: "stroke fill",
                  lineHeight: 0.95,
                }}
              >
                25%
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 32,
                  color: "#FFFFFF",
                  WebkitTextStroke: "7px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                DOANH THU
              </div>
            </div>

            {/* Column 2: 50% Lợi Nhuận */}
            <div
              style={{
                position: "absolute",
                left: 740,
                bottom: 500,
                width: 240,
                height: Math.max(24, 600 * profGrow),
                transform: "translateX(-50%)",
                borderRadius: "22px 22px 0 0",
                background:
                  "linear-gradient(180deg, #FFE600 0%, #FF9900 100%)",
                boxShadow: "0 0 48px rgba(255,230,0,0.65)",
              }}
            />
            <div
              style={{
                position: "absolute",
                left: 740,
                top: 1420 - Math.max(24, 600 * profGrow) - 110,
                transform: "translate(-50%, -50%)",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 96,
                  color: "#FFE600",
                  WebkitTextStroke: "11px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 36px rgba(255,230,0,0.8)",
                  lineHeight: 0.95,
                }}
              >
                50%
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 34,
                  color: "#FFE600",
                  WebkitTextStroke: "7px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                TỔNG LỢI NHUẬN
              </div>
            </div>

            {/* Soda Cup Cutout anchoring beside the profit bar */}
            <div
              style={{
                position: "absolute",
                left: 880,
                top: 1320 + Math.sin(frame * 0.08) * 6,
                width: 190,
                transform: "translate(-50%, -50%) rotate(8deg)",
              }}
            >
              <Img
                src={staticFile("harvested/cinema_soda_cup_cutout.png")}
                style={{
                  width: "100%",
                  height: "auto",
                  filter:
                    "drop-shadow(0 0 6px rgba(255,230,0,0.7)) drop-shadow(0 18px 30px rgba(0,0,0,0.9))",
                }}
              />
            </div>
          </div>
        )}

        {/* =================================================================
            BEAT 5 (2010..2520): RẠP PHIM LÀ TIỆM BÁN BỎNG NGÔ, PHIM LÀ CÁI MỒI
            ================================================================= */}
        {b5Active && (
          <div style={{ position: "absolute", inset: 0, opacity: b5Fade }}>
            <RealPersonSpotlight3D
              startFrame={2010}
              endFrame={2520}
              backdropSrc="harvested/cinema_concession_crowd.png"
              cutoutSrc="harvested/popcorn_bucket_cutout.png"
              cutoutWidth={520}
              centerX={540}
              cutoutTop={960}
              labelTop={1510}
              rimGlowColor="rgba(255, 230, 0, 0.92)"
              subjectName="TIỆM BÁN BỎNG NGÔ"
              subjectSubtitle="SIÊU LỢI NHUẬN"
              keyMetricValue={frame >= 2310 ? "PHIM CHỈ LÀ CÁI MỒI?" : undefined}
              keyMetricAccentColor="#FF3B47"
            />

            {/* Soda Cup Cutout anchoring right side at Beat 5 */}
            <div
              style={{
                position: "absolute",
                left: 840,
                top: 1150 + Math.sin(frame * 0.08) * 6,
                width: 240,
                transform: "translate(-50%, -50%) rotate(10deg)",
              }}
            >
              <Img
                src={staticFile("harvested/cinema_soda_cup_cutout.png")}
                style={{
                  width: "100%",
                  height: "auto",
                  filter:
                    "drop-shadow(0 0 8px rgba(255,230,0,0.8)) drop-shadow(0 18px 30px rgba(0,0,0,0.95))",
                }}
              />
            </div>

            {/* Bait Ticket at bottom-left pulling toward the popcorn counter */}
            {frame >= 2310 && (
              <div
                style={{
                  position: "absolute",
                  left: 220,
                  top: 1210,
                  width: 280,
                  transform: `translate(-50%, -50%) scale(${baitPop}) rotate(-18deg)`,
                }}
              >
                <Img
                  src={staticFile("harvested/cinema_ticket_cutout.png")}
                  style={{
                    width: "100%",
                    height: "auto",
                    filter:
                      "drop-shadow(0 0 8px rgba(255,59,71,0.9)) drop-shadow(0 16px 28px rgba(0,0,0,0.95))",
                  }}
                />
              </div>
            )}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
