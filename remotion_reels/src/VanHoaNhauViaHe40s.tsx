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

export const VanHoaNhauViaHe40s: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // =========================================================================
  // CAMERA MICRO-SHAKE ON FORENSIC IMPACTS (Synced to continuous 30s audio)
  // =========================================================================
  const impactFrames = [0, 74, 228, 336, 476, 667, 857, 1032, 1207, 1296, 1521];
  let shakeX = 0;
  let shakeY = 0;
  for (const imp of impactFrames) {
    if (frame >= imp && frame < imp + 14) {
      const dt = frame - imp;
      const decay = Math.exp(-dt * 0.28);
      const amp = imp === 1296 || imp === 1521 ? 14 : 9;
      shakeX += Math.sin(dt * 3.1) * amp * decay;
      shakeY += Math.cos(dt * 3.5) * (amp - 2) * decay;
    }
  }

  // Global continuous cinematic light sweep ensuring ZERO frozen frames
  const sweepX = ((frame * 18) % 2600) - 800;

  // =========================================================================
  // 11-BEAT KINETIC HOOK TIMELINE (Synced 100% to voice_continuous_30s.wav)
  // =========================================================================
  const hookInfo: HookBeatSpec = (() => {
    if (frame < 74) {
      return {
        start: 0,
        eyebrow: "NGƯỜI VIỆT MÊ NHẬU?",
        hero: "TOP 2 ĐÔNG NAM Á!",
        accent: "#42B2F2",
        heroSize: 78,
      };
    }
    if (frame < 228) {
      return {
        start: 74,
        eyebrow: "TOP 8 TOÀN CẦU",
        hero: "170 LÍT BIA / NĂM!",
        accent: "#FFE600",
        heroSize: 78,
      };
    }
    if (frame < 336) {
      return {
        start: 228,
        eyebrow: "NHÀ Ở CHẬT CHỘI",
        hero: "ĐẨY DÂN RA ĐƯỜNG!",
        accent: "#FF3B47",
        heroSize: 76,
      };
    }
    if (frame < 476) {
      return {
        start: 336,
        eyebrow: "THỜI KỲ BAO CẤP",
        hero: "BIA HƠI MẬU DỊCH",
        accent: "#FFE600",
        heroSize: 76,
      };
    }
    if (frame < 667) {
      return {
        start: 476,
        eyebrow: "BƯỚC NGOẶT 1986",
        hero: "KINH TẾ VỈA HÈ BÙNG NỔ",
        accent: "#42B2F2",
        heroSize: 64,
      };
    }
    if (frame < 857) {
      return {
        start: 667,
        eyebrow: "NHƯNG ĐIỀU GÌ MỚI THỰC SỰ",
        hero: "GIỮ CHÂN MỌI TẦNG LỚP?",
        accent: "#FF3B47",
        heroSize: 62,
      };
    }
    if (frame < 1032) {
      return {
        start: 857,
        eyebrow: "TÂM LÝ BÌNH DÂN",
        hero: "SAN BẰNG MỌI ĐỊA VỊ!",
        accent: "#42B2F2",
        heroSize: 68,
      };
    }
    if (frame < 1207) {
      return {
        start: 1032,
        eyebrow: "CỒN HẠ PHÒNG VỆ NÃO",
        hero: "KẾT NỐI SIÊU TỐC!",
        accent: "#FFE600",
        heroSize: 74,
      };
    }
    if (frame < 1356) {
      return {
        start: 1207,
        eyebrow: "MẶT TRÁI ĐỘC HẠI",
        hero: "THÓI QUEN ÉP UỐNG!",
        accent: "#FF3B47",
        heroSize: 72,
      };
    }
    if (frame < 1521) {
      return {
        start: 1356,
        eyebrow: "VUI BUỒN ĐỀU NHẬU",
        hero: "TỪ CHỐI SỢ LẠC LÕNG!",
        accent: "#FF3B47",
        heroSize: 66,
      };
    }
    return {
      start: 1521,
      eyebrow: "CÂU HỎI THỨC TỈNH",
      hero: "VUI HAY CHỈ VÌ NỂ?",
      accent: "#FFE600",
      heroSize: 74,
    };
  })();

  // =========================================================================
  // SCENE TRANSITION OPACITIES (1800 Frames = 30.00s)
  // =========================================================================
  // Scene 1 (0..228 | 0.00s..3.80s): Top 2 SEA & 170L + Studio Bia Hoi Glass Cutout + Bar Chart
  const s1Active = frame < 236;
  const s1Opacity = interpolate(frame, [220, 236], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s1Slam = spring({
    frame: Math.max(0, frame - 2),
    fps,
    config: { damping: 14, stiffness: 190, mass: 0.85 },
  });
  const odoLiters = Math.round(
    interpolate(frame, [74, 130], [0, 170], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  // Scene 2A (228..336 | 3.80s..5.60s): Nhà chật đẩy ra đường -> Old Quarter cramped houses
  const s2aActive = frame >= 224 && frame < 344;
  const s2aOpacity =
    interpolate(frame, [224, 236], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [328, 344], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  // Scene 2B (336..476 | 5.60s..7.94s): Bia hơi mậu dịch -> 1970s Monochrome Archival Photo
  const s2bActive = frame >= 332 && frame < 484;
  const s2bOpacity =
    interpolate(frame, [332, 344], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [468, 484], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  // Scene 2C (476..667 | 7.94s..11.12s): Đổi Mới 1986 -> Real Sidewalk Bia Hoi Outlet + Timeline
  const s2cActive = frame >= 472 && frame < 675;
  const s2cOpacity =
    interpolate(frame, [472, 484], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [659, 675], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  const stamp1986 = spring({
    frame: Math.max(0, frame - 476),
    fps,
    config: { damping: 11, stiffness: 220, mass: 0.7 },
  });

  // Scene 3A (667..857 | 11.12s..14.29s): Giữ chân mọi tầng lớp -> Real Sidewalk Drinking Photo
  const s3aActive = frame >= 663 && frame < 865;
  const s3aOpacity =
    interpolate(frame, [663, 675], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [849, 865], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  // Scene 3B (857..1032 | 14.29s..17.21s): Bình dân xóa khoảng cách -> Friends Toast on Plastic Stools
  const s3bActive = frame >= 853 && frame < 1040;
  const s3bOpacity =
    interpolate(frame, [853, 865], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [1024, 1040], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  // Scene 3C (1032..1207 | 17.21s..20.13s): Cồn hạ phòng vệ -> Real Medical Brain MRI + Forensic Highlight Card
  const s3cActive = frame >= 1028 && frame < 1215;
  const s3cOpacity =
    interpolate(frame, [1028, 1040], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [1199, 1215], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  // Scene 4 (1207..1521 | 20.13s..25.35s): Ép uống cả nể & sợ lạc lõng -> Real Peer Pressure Photo + Stamp
  const s4Active = frame >= 1203 && frame < 1529;
  const s4Opacity =
    interpolate(frame, [1203, 1215], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [1513, 1529], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  const stampTrap = spring({
    frame: Math.max(0, frame - 1296),
    fps,
    config: { damping: 10, stiffness: 240, mass: 0.7 },
  });

  // Scene 5 (1521..1800 | 25.35s..30.00s): Vacuum Drop Climax Split Comparison (Vui thật vs Cả nể)
  const s5Active = frame >= 1517;
  const s5Opacity = interpolate(frame, [1517, 1532], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s5Slam = spring({
    frame: Math.max(0, frame - 1521),
    fps,
    config: { damping: 12, stiffness: 180, mass: 0.85 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#04070D",
        color: "#FFFFFF",
        overflow: "hidden",
      }}
    >
      {/* Locked Channel Fonts (BeVietnamProBlack, BeVietnamProExtraBold, KanitBlack) */}
      <HaDaWhyFontFaces />

      {/* 30.00s Continuous Master Audio (-14.0 LUFS EBU R128 + Vacuum Drop + Frame-Synced SFX) */}
      <Audio src={staticFile("audio/master_audio_van_hoa_nhau.wav")} />

      {/* Brand Signature ADN Backdrop (Level 1: Obsidian + Soft #42B2F2 Mist) */}
      <HaDaWhyMistBackground intensity={0.11} accentHex="66, 178, 242" />

      {/* 2-Layer Anti-Reup Watermark */}
      <ChannelWatermark9x16 />

      {/* Ambient Moving Light Sweep (ZERO Frozen Frames Guaranteed) */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: sweepX,
          width: 480,
          height: 1920,
          background:
            "linear-gradient(90deg, transparent 0%, rgba(66, 178, 242, 0.05) 50%, transparent 100%)",
          transform: "skewX(-22deg)",
          pointerEvents: "none",
          zIndex: 10,
        }}
      />

      {/* TOP TIER (Y: 220..440px): KINETIC IMPACTHOOK 2 TẦNG ZERO-BOX + SPRING SLAM */}
      <KineticHookHeader beat={hookInfo} top={320} />

      {/* MAIN 3D VISUAL STAGE WITH CAMERA MICRO-SHAKE */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate(${shakeX}px, ${shakeY}px)`,
        }}
      >
        {/* =================================================================
            SCENE 1 (0..228): HẠNG 2 ĐÔNG NAM Á & 170 LÍT BIA / NĂM
            Real Ta Hien Night Backdrop + Studio HD Bia Hoi Cutout + Comparative Bars
        ================================================================= */}
        {s1Active && (
          <AbsoluteFill style={{ opacity: s1Opacity }}>
            {/* 3D Tilted Real Ta Hien Night Backdrop */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 670,
                width: 860,
                height: 440,
                perspective: 1100,
                transform: `translate(-50%, -50%) scale(${interpolate(s1Slam, [0, 1], [1.25, 1.0])})`,
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  transform: "rotateX(7deg) rotateY(-4deg)",
                  borderRadius: 28,
                  overflow: "hidden",
                  border: "3px solid rgba(66, 178, 242, 0.55)",
                  boxShadow: "0 35px 80px rgba(0,0,0,0.92)",
                }}
              >
                <Img
                  src={staticFile("harvested/ta_hien_street_real.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    filter: "brightness(0.75) contrast(1.12)",
                    transform: `scale(${1.02 + frame * 0.0006})`,
                  }}
                />
              </div>
            </div>

            {/* Clean Studio HD Bia Hoi Glass Cutout (Zero jagged edges!) */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 860 + Math.sin(frame * 0.08) * 8,
                width: 340,
                transform: `translate(-50%, -50%) scale(${interpolate(s1Slam, [0, 1], [1.3, 1.0])}) rotate(-3deg)`,
                zIndex: 20,
              }}
            >
              <div
                style={{
                  position: "absolute",
                  bottom: -24,
                  left: "50%",
                  transform: "translateX(-50%)",
                  width: 300,
                  height: 46,
                  borderRadius: "50%",
                  background: "radial-gradient(ellipse, rgba(0,0,0,0.92) 0%, transparent 75%)",
                  filter: "blur(12px)",
                }}
              />
              <Img
                src={staticFile("harvested/bia_hoi_glass_cutout_hd.png")}
                style={{
                  width: "100%",
                  height: "auto",
                  filter:
                    "drop-shadow(0px 0px 14px rgba(255,230,0,0.45)) drop-shadow(0px 26px 36px rgba(0,0,0,0.95))",
                }}
              />
            </div>

            {/* Odometer & Comparative Bar Readout (Zero-Box Floating) */}
            <div
              style={{
                position: "absolute",
                left: 60,
                right: 60,
                bottom: 220,
                textAlign: "center",
                zIndex: 25,
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 66,
                  color: "#FFE600",
                  WebkitTextStroke: "10px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 34px rgba(255,230,0,0.75)",
                  marginBottom: 8,
                }}
              >
                {frame >= 74 ? `${odoLiters} LÍT / NGƯỜI` : "#2 ĐÔNG NAM Á"}
              </div>

              <svg width="960" height="310" viewBox="0 0 960 310">
                {/* Southeast Asia / Vietnam Geo Signal Path (top-right clear space) */}
                <path
                  d="M680,35 Q730,15 770,45 T830,75"
                  fill="none"
                  stroke="#42B2F2"
                  strokeWidth="3"
                  strokeDasharray="6 4"
                  opacity="0.7"
                />
                <circle cx="770" cy="45" r="7" fill="#FFE600" />
                <line x1="60" y1="220" x2="900" y2="220" stroke="#334155" strokeWidth="2" />
                {(() => {
                  const hVN = interpolate(frame, [74, 130], [70, 175], {
                    extrapolateLeft: "clamp",
                    extrapolateRight: "clamp",
                  });
                  return (
                    <g transform="translate(150, 220)">
                      <rect x="-42" y={-hVN} width="84" height={hVN} rx="10" fill="url(#goldGrad)" />
                      <text x="0" y={-hVN - 14} textAnchor="middle" fill="#FFE600" fontSize="30" fontWeight="900" fontFamily="KanitBlack">
                        170L
                      </text>
                      <text x="0" y="38" textAnchor="middle" fill="#FFFFFF" fontSize="26" fontWeight="900" fontFamily="BeVietnamProBlack">
                        VIỆT NAM
                      </text>
                      <text x="0" y="68" textAnchor="middle" fill="#FFE600" fontSize="20" fontWeight="800" fontFamily="BeVietnamProExtraBold">
                        #2 ĐÔNG NAM Á
                      </text>
                    </g>
                  );
                })()}
                <g transform="translate(380, 220)">
                  <rect x="-38" y={-146} width="76" height="146" rx="10" fill="#42B2F2" opacity="0.85" />
                  <text x="0" y={-160} textAnchor="middle" fill="#42B2F2" fontSize="26" fontWeight="900" fontFamily="KanitBlack">
                    142L
                  </text>
                  <text x="0" y="38" textAnchor="middle" fill="#CBD5E1" fontSize="24" fontWeight="800" fontFamily="BeVietnamProBlack">
                    THÁI LAN
                  </text>
                  <text x="0" y="68" textAnchor="middle" fill="#64748B" fontSize="18" fontWeight="700">
                    #3 ĐÔNG NAM Á
                  </text>
                </g>
                <g transform="translate(600, 220)">
                  <rect x="-36" y={-111} width="72" height="111" rx="10" fill="#475569" opacity="0.8" />
                  <text x="0" y={-125} textAnchor="middle" fill="#E2E8F0" fontSize="24" fontWeight="800" fontFamily="KanitBlack">
                    108L
                  </text>
                  <text x="0" y="38" textAnchor="middle" fill="#94A3B8" fontSize="24" fontWeight="800" fontFamily="BeVietnamProBlack">
                    NHẬT BẢN
                  </text>
                  <text x="0" y="68" textAnchor="middle" fill="#64748B" fontSize="18" fontWeight="700">
                    CHÂU Á
                  </text>
                </g>
                <g transform="translate(820, 220)">
                  <rect x="-34" y={-84} width="68" height="84" rx="8" fill="#334155" opacity="0.7" />
                  <text x="0" y={-98} textAnchor="middle" fill="#94A3B8" fontSize="22" fontWeight="800" fontFamily="KanitBlack">
                    82L
                  </text>
                  <text x="0" y="38" textAnchor="middle" fill="#94A3B8" fontSize="24" fontWeight="800" fontFamily="BeVietnamProBlack">
                    THẾ GIỚI
                  </text>
                  <text x="0" y="68" textAnchor="middle" fill="#64748B" fontSize="18" fontWeight="700">
                    TRUNG BÌNH
                  </text>
                </g>
                <defs>
                  <linearGradient id="goldGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#FFE600" />
                    <stop offset="100%" stopColor="#D97706" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </AbsoluteFill>
        )}

        {/* =================================================================
            SCENE 2A (228..336): NHÀ CHẬT ĐẨY NGƯỜI DÂN RA ĐƯỜNG
            Multi-layer: Old Quarter Houses + Density Callout + Outward Push + Sidewalk Preview
        ================================================================= */}
        {s2aActive && (
          <AbsoluteFill style={{ opacity: s2aOpacity }}>
            {/* Top-Left Floating Spatial Readout */}
            <div
              style={{
                position: "absolute",
                left: 60,
                top: 470,
                textAlign: "left",
                zIndex: 25,
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 48,
                  color: "#FF3B47",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 26px rgba(255,59,71,0.8)",
                }}
              >
                823 NGƯỜI / HA
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 26,
                  color: "#FFFFFF",
                  WebkitTextStroke: "5px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                PHỐ CỔ CHẬT 15–20M²
              </div>
            </div>

            {/* Top-Right Secondary Sidewalk Preview Card (Like 1907 Wall Street multi-card!) */}
            <div
              style={{
                position: "absolute",
                right: 55,
                top: 465,
                width: 310,
                height: 200,
                borderRadius: 20,
                overflow: "hidden",
                border: "3px solid #42B2F2",
                boxShadow: "0 18px 45px rgba(66,178,242,0.45)",
                transform: `rotate(3deg) translateY(${Math.sin(frame * 0.08) * 5}px)`,
                zIndex: 25,
              }}
            >
              <Img
                src={staticFile("harvested/vn_people_sidewalk_old_real.jpg")}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </div>

            {/* Animated Dashed Push Connector */}
            <svg width="960" height="160" viewBox="0 0 960 160" style={{ position: "absolute", left: 60, top: 530, zIndex: 22, pointerEvents: "none" }}>
              <path
                d="M 280,50 Q 460,10 600,45"
                fill="none"
                stroke="#FFE600"
                strokeWidth="6"
                strokeDasharray="14 8"
                strokeDashoffset={-frame * 2.5}
              />
              <polygon points="595,30 625,48 590,62" fill="#FFE600" />
            </svg>

            {/* Main 3D Tilted Old Quarter Houses Photo */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 990,
                width: 940,
                height: 540,
                perspective: 1100,
                transform: "translate(-50%, -50%)",
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: 30,
                  overflow: "hidden",
                  border: "3px solid rgba(255, 59, 71, 0.75)",
                  boxShadow: "0 30px 70px rgba(0,0,0,0.92)",
                  transform: "rotateX(5deg) rotateY(-2deg)",
                }}
              >
                <Img
                  src={staticFile("harvested/hanoi_old_quarter_houses_real.jpg")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    transform: `scale(${1.02 + (frame - 228) * 0.001})`,
                  }}
                />
              </div>
            </div>

            <div
              style={{
                position: "absolute",
                left: 60,
                right: 60,
                bottom: 240,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 54,
                  color: "#FFE600",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 28px rgba(255, 230, 0, 0.75)",
                }}
              >
                VỈA HÈ = PHÒNG KHÁCH MỞ RỘNG
              </div>
            </div>
          </AbsoluteFill>
        )}

        {/* =================================================================
            SCENE 2B (336..476): BIA HƠI MẬU DỊCH -> 1970s ARCHIVAL MONOCHROME
            Multi-layer: Studio Glass Cutout + Archival Tem Phieu Tag + Dashed Connector + 1970s Photo
        ================================================================= */}
        {s2bActive && (
          <AbsoluteFill style={{ opacity: s2bOpacity }}>
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 520,
                transform: "translate(-50%, -50%)",
                fontFamily: "KanitBlack, sans-serif",
                fontSize: 220,
                color: "rgba(255, 230, 0, 0.09)",
                pointerEvents: "none",
              }}
            >
              1970
            </div>

            {/* Top-Left Floating Bia Hoi Glass Cutout */}
            <div
              style={{
                position: "absolute",
                left: 190,
                top: 580 + Math.sin(frame * 0.08) * 6,
                width: 170,
                transform: "translate(-50%, -50%) rotate(-8deg)",
                zIndex: 25,
              }}
            >
              <Img
                src={staticFile("harvested/bia_hoi_glass_cutout_hd.png")}
                style={{
                  width: "100%",
                  height: "auto",
                  filter: "drop-shadow(0 0 18px rgba(255,230,0,0.55)) drop-shadow(0 18px 25px rgba(0,0,0,0.9))",
                }}
              />
            </div>

            {/* Top-Right Archival Tem Phieu Evidence Badge */}
            <div
              style={{
                position: "absolute",
                right: 70,
                top: 500,
                border: "4px dashed #FFE600",
                borderRadius: 16,
                padding: "14px 28px",
                transform: "rotate(3deg)",
                textAlign: "center",
                zIndex: 25,
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 38,
                  color: "#FFE600",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                TEM PHIẾU 1960–1985
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 24,
                  color: "#FFFFFF",
                  WebkitTextStroke: "4px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                XẾP HÀNG MUA BIA MẬU DỊCH
              </div>
            </div>

            {/* Dashed Connector from Top Cutout/Badge to Historical Photo */}
            <svg width="960" height="220" viewBox="0 0 960 220" style={{ position: "absolute", left: 60, top: 540, zIndex: 20, pointerEvents: "none" }}>
              <path
                d="M 210,120 Q 340,170 430,200"
                fill="none"
                stroke="#FFE600"
                strokeWidth="4"
                strokeDasharray="10 6"
                strokeDashoffset={-frame * 2}
              />
              <path
                d="M 680,100 Q 580,160 510,200"
                fill="none"
                stroke="#FFE600"
                strokeWidth="4"
                strokeDasharray="10 6"
                strokeDashoffset={-frame * 2}
              />
            </svg>

            <div
              style={{
                position: "absolute",
                left: 540,
                top: 1020,
                width: 940,
                height: 550,
                perspective: 1100,
                transform: "translate(-50%, -50%)",
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: 28,
                  overflow: "hidden",
                  border: "4px solid #FFE600",
                  boxShadow: "0 30px 70px rgba(0,0,0,0.92)",
                  transform: "rotateX(5deg) rotateY(2deg)",
                }}
              >
                <Img
                  src={staticFile("harvested/hanoi_bia_hoi_1970s_archive.jpg")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    transform: `scale(${1.02 + (frame - 336) * 0.0009})`,
                  }}
                />
              </div>
            </div>

            <div
              style={{
                position: "absolute",
                left: 60,
                right: 60,
                bottom: 240,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 32,
                  color: "#FFFFFF",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                TƯ LIỆU LỊCH SỬ BIA HƠI BAO CẤP HÀ NỘI
              </div>
            </div>
          </AbsoluteFill>
        )}

        {/* =================================================================
            SCENE 2C (476..667): SAU ĐỔI MỚI 1986 -> QUÁN XÁ BÌNH DÂN BÙNG NỔ
        ================================================================= */}
        {s2cActive && (
          <AbsoluteFill style={{ opacity: s2cOpacity }}>
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 800,
                width: 940,
                height: 600,
                perspective: 1100,
                transform: "translate(-50%, -50%)",
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: 28,
                  overflow: "hidden",
                  border: "3px solid rgba(66, 178, 242, 0.75)",
                  boxShadow: "0 30px 70px rgba(0,0,0,0.92)",
                  transform: "rotateX(5deg)",
                }}
              >
                <Img
                  src={staticFile("harvested/bia_hoi_outlet_hanoi_real.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    transform: `scale(${1.02 + (frame - 476) * 0.0008})`,
                  }}
                />
              </div>
            </div>

            {/* Slammed Historical Stamp */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 1090,
                transform: `translate(-50%, -50%) rotate(-4deg) scale(${stamp1986})`,
                textAlign: "center",
                width: 920,
                zIndex: 30,
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 74,
                  color: "#FFE600",
                  WebkitTextStroke: "11px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 38px rgba(255, 230, 0, 0.85)",
                }}
              >
                ĐỔI MỚI NĂM 1986
              </div>
            </div>

            {/* Timeline 1960 -> 1986 */}
            <svg width="920" height="170" viewBox="0 0 920 170" style={{ position: "absolute", left: 80, bottom: 250 }}>
              <line x1="80" y1="80" x2="840" y2="80" stroke="#334155" strokeWidth="6" />
              <g transform="translate(220, 80)">
                <circle cx="0" cy="0" r="18" fill="#D97706" stroke="#FFFFFF" strokeWidth="4" />
                <text x="0" y="-32" textAnchor="middle" fill="#FBBF24" fontSize="26" fontWeight="900" fontFamily="KanitBlack">
                  1960 MẬU DỊCH
                </text>
                <text x="0" y="42" textAnchor="middle" fill="#E2E8F0" fontSize="22" fontWeight="800" fontFamily="BeVietnamProBlack">
                  Phân Phối Tem Phiếu
                </text>
              </g>
              <g transform="translate(700, 80)">
                <circle cx="0" cy="0" r="22" fill="#FFE600" stroke="#FFFFFF" strokeWidth="5" />
                <text x="0" y="-32" textAnchor="middle" fill="#FFE600" fontSize="28" fontWeight="900" fontFamily="KanitBlack">
                  1986 ĐỔI MỚI
                </text>
                <text x="0" y="42" textAnchor="middle" fill="#42B2F2" fontSize="24" fontWeight="900" fontFamily="BeVietnamProBlack">
                  Kinh Tế Vỉa Hè Bùng Nổ
                </text>
              </g>
            </svg>
          </AbsoluteFill>
        )}

        {/* =================================================================
            SCENE 3A (667..857): ĐIỀU GÌ GIỮ CHÂN MỌI TẦNG LỚP NGỒI LẠI VỈA HÈ?
            Multi-layer: 3 Glowing Vector Class Icons + Converging Dashed Lines + Real Crowded Sidewalk + 25CM Callout
        ================================================================= */}
        {s3aActive && (
          <AbsoluteFill style={{ opacity: s3aOpacity }}>
            {/* 3 Floating Minimalist Glowing SVG Vector Class Icons */}
            <div
              style={{
                position: "absolute",
                left: 60,
                right: 60,
                top: 455,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                zIndex: 25,
              }}
            >
              {/* 1. SẾP / GIÁM ĐỐC */}
              <div
                style={{
                  width: 300,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  transform: `translateY(${Math.sin(frame * 0.08) * 6}px)`,
                }}
              >
                <svg
                  width="76"
                  height="76"
                  viewBox="0 0 64 64"
                  fill="none"
                  style={{ filter: "drop-shadow(0 0 16px rgba(255, 230, 0, 0.85))" }}
                >
                  <path
                    d="M10 46L14 20L26 31L32 14L38 31L50 20L54 46H10Z"
                    stroke="#FFE600"
                    strokeWidth="3.5"
                    strokeLinejoin="round"
                    fill="rgba(255, 230, 0, 0.14)"
                  />
                  <rect x="12" y="50" width="40" height="5" rx="2.5" fill="#FFE600" />
                </svg>
                <div
                  style={{
                    marginTop: 8,
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 30,
                    color: "#FFE600",
                    WebkitTextStroke: "6px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 18px rgba(255, 230, 0, 0.7)",
                    whiteSpace: "nowrap",
                  }}
                >
                  SẾP / GIÁM ĐỐC
                </div>
              </div>

              {/* 2. CÔNG SỞ */}
              <div
                style={{
                  width: 300,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  transform: `translateY(${Math.sin(frame * 0.08 + 1.4) * 6}px)`,
                }}
              >
                <svg
                  width="76"
                  height="76"
                  viewBox="0 0 64 64"
                  fill="none"
                  style={{ filter: "drop-shadow(0 0 16px rgba(66, 178, 242, 0.85))" }}
                >
                  <rect
                    x="12"
                    y="14"
                    width="40"
                    height="28"
                    rx="4"
                    stroke="#42B2F2"
                    strokeWidth="3.5"
                    fill="rgba(66, 178, 242, 0.14)"
                  />
                  <path d="M6 48H58" stroke="#42B2F2" strokeWidth="4" strokeLinecap="round" />
                  <path d="M26 24L32 30L38 24" stroke="#FFFFFF" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <div
                  style={{
                    marginTop: 8,
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 30,
                    color: "#42B2F2",
                    WebkitTextStroke: "6px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 18px rgba(66, 178, 242, 0.7)",
                    whiteSpace: "nowrap",
                  }}
                >
                  CÔNG SỞ
                </div>
              </div>

              {/* 3. LAO ĐỘNG */}
              <div
                style={{
                  width: 300,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  transform: `translateY(${Math.sin(frame * 0.08 + 2.8) * 6}px)`,
                }}
              >
                <svg
                  width="76"
                  height="76"
                  viewBox="0 0 64 64"
                  fill="none"
                  style={{ filter: "drop-shadow(0 0 16px rgba(52, 211, 153, 0.85))" }}
                >
                  <path
                    d="M14 38C14 25 22 17 32 17C42 17 50 25 50 38H14Z"
                    stroke="#34D399"
                    strokeWidth="3.5"
                    strokeLinejoin="round"
                    fill="rgba(52, 211, 153, 0.14)"
                  />
                  <path d="M32 13V24" stroke="#34D399" strokeWidth="4" strokeLinecap="round" />
                  <path d="M8 40H56" stroke="#34D399" strokeWidth="4" strokeLinecap="round" />
                </svg>
                <div
                  style={{
                    marginTop: 8,
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 30,
                    color: "#34D399",
                    WebkitTextStroke: "6px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 18px rgba(52, 211, 153, 0.7)",
                    whiteSpace: "nowrap",
                  }}
                >
                  LAO ĐỘNG
                </div>
              </div>
            </div>

            {/* Real Crowded All-Classes Sidewalk Photo */}
            <div
              style={{
                position: "absolute",
                left: 540,
                top: 985,
                width: 940,
                height: 540,
                perspective: 1100,
                transform: "translate(-50%, -50%)",
                zIndex: 18,
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: 30,
                  overflow: "hidden",
                  border: "3px solid rgba(255, 59, 71, 0.75)",
                  boxShadow: "0 30px 70px rgba(0,0,0,0.92)",
                  transform: "rotateX(5deg)",
                }}
              >
                <Img
                  src={staticFile("harvested/vn_crowded_all_classes_nhau.jpg")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    transform: `scale(${1.03 + (frame - 667) * 0.0009})`,
                  }}
                />
              </div>
            </div>

            {/* 3 Converging Dashed Lines straight into the center of the crowded table */}
            <svg
              width="1080"
              height="380"
              viewBox="0 0 1080 380"
              style={{ position: "absolute", left: 0, top: 580, zIndex: 24, pointerEvents: "none" }}
            >
              <path
                d="M 210,12 Q 330,130 540,210"
                fill="none"
                stroke="#FFE600"
                strokeWidth="4.5"
                strokeDasharray="11 7"
                strokeDashoffset={-frame * 2.2}
              />
              <path
                d="M 540,12 L 540,210"
                fill="none"
                stroke="#42B2F2"
                strokeWidth="4.5"
                strokeDasharray="11 7"
                strokeDashoffset={-frame * 2.2}
              />
              <path
                d="M 870,12 Q 750,130 540,210"
                fill="none"
                stroke="#34D399"
                strokeWidth="4.5"
                strokeDasharray="11 7"
                strokeDashoffset={-frame * 2.2}
              />
              <circle
                cx="540"
                cy="210"
                r={18 + Math.sin(frame * 0.16) * 4}
                fill="rgba(255, 59, 71, 0.25)"
                stroke="#FFE600"
                strokeWidth="3"
              />
              <circle cx="540" cy="210" r="10" fill="#FF3B47" stroke="#FFFFFF" strokeWidth="3" />
            </svg>

            <div
              style={{
                position: "absolute",
                left: 60,
                right: 60,
                bottom: 240,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 56,
                  color: "#FFE600",
                  WebkitTextStroke: "9px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 32px rgba(255, 230, 0, 0.75)",
                }}
              >
                GHẾ NHỰA THẤP 25CM
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 32,
                  color: "#FFFFFF",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  marginTop: 6,
                }}
              >
                XÓA MỌI RANH GIỚI ĐỊA VỊ
              </div>
            </div>
          </AbsoluteFill>
        )}

        {/* =================================================================
            SCENE 3B (857..1032): TÂM LÝ BÌNH DÂN, CỞI MỞ XÓA KHOẢNG CÁCH
            Multi-layer: Friends Toast Photo + Studio Bia Hoi Glass Cutout + Hierarchy=0 Badge
        ================================================================= */}
        {s3bActive && (
          <AbsoluteFill style={{ opacity: s3bOpacity }}>
            {/* Top-Left CẤP BẬC = 0 */}
            <div
              style={{
                position: "absolute",
                left: 70,
                top: 470,
                fontFamily: "KanitBlack, sans-serif",
                fontSize: 42,
                color: "#42B2F2",
                WebkitTextStroke: "7px #05070C",
                paintOrder: "stroke fill",
                zIndex: 25,
              }}
            >
              KHOẢNG CÁCH = 0
            </div>

            {/* Top-Right Floating Glass Cutout Accent */}
            <div
              style={{
                position: "absolute",
                right: 110,
                top: 520 + Math.sin(frame * 0.09) * 6,
                width: 130,
                transform: "translate(0, -50%) rotate(8deg)",
                zIndex: 28,
              }}
            >
              <Img
                src={staticFile("harvested/bia_hoi_glass_cutout_hd.png")}
                style={{
                  width: "100%",
                  height: "auto",
                  filter: "drop-shadow(0 0 18px rgba(66,178,242,0.6)) drop-shadow(0 16px 24px rgba(0,0,0,0.9))",
                }}
              />
            </div>

            <div
              style={{
                position: "absolute",
                left: 540,
                top: 890,
                width: 940,
                height: 580,
                perspective: 1100,
                transform: "translate(-50%, -50%)",
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: 30,
                  overflow: "hidden",
                  border: "3px solid rgba(66, 178, 242, 0.8)",
                  boxShadow: "0 30px 70px rgba(0,0,0,0.92)",
                  transform: "rotateX(5deg)",
                }}
              >
                <Img
                  src={staticFile("harvested/hanoi_friends_toast_real.jpg")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    transform: `scale(${1.02 + (frame - 857) * 0.0009})`,
                  }}
                />
              </div>
            </div>

            <div
              style={{
                position: "absolute",
                left: 60,
                right: 60,
                bottom: 245,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 44,
                  color: "#42B2F2",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 32px rgba(66, 178, 242, 0.8)",
                  whiteSpace: "nowrap",
                }}
              >
                THE THIRD PLACE — KHÔNG GIAN THỨ 3
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 30,
                  color: "#FFFFFF",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  marginTop: 8,
                }}
              >
                XÓA SẠCH ĐỊA VỊ — CHỈ CÒN SỰ CỞI MỞ BÌNH DÂN
              </div>
            </div>
          </AbsoluteFill>
        )}

        {/* =================================================================
            SCENE 3C (1032..1207): CỒN HẠ PHÒNG VỆ GIÚP KẾT NỐI CỰC NHANH
            3D Brain Cutout + Energy Pulse Beam + Cracking/Lowering Shield + 2 Clean Callouts
        ================================================================= */}
        {s3cActive && (() => {
          const s3cProg = interpolate(frame, [1045, 1175], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const shieldY = s3cProg * 76;
          const shieldRot = s3cProg * 16;
          const shieldOpacity = interpolate(s3cProg, [0, 1], [1, 0.38]);
          const crackOpacity = interpolate(s3cProg, [0.2, 0.55], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          return (
            <AbsoluteFill style={{ opacity: s3cOpacity }}>
              {/* Top Clean Label */}
              <div
                style={{
                  position: "absolute",
                  left: 60,
                  right: 60,
                  top: 475,
                  textAlign: "center",
                  zIndex: 25,
                }}
              >
                <div
                  style={{
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 46,
                    color: "#42B2F2",
                    WebkitTextStroke: "8px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 28px rgba(66, 178, 242, 0.8)",
                  }}
                >
                  VỎ NÃO TRƯỚC TRÁN
                </div>
              </div>

              {/* Left/Center-Left: 3D Brain Cutout with Breathing Pulse & Frontal Lobe Ring */}
              <div
                style={{
                  position: "absolute",
                  left: 70,
                  top: 635,
                  width: 430,
                  height: 430,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  zIndex: 22,
                }}
              >
                <Img
                  src={staticFile("harvested/brain_neural_cutout_hd.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                    filter: "drop-shadow(0 0 28px rgba(66, 178, 242, 0.8))",
                    transform: `scale(${1 + Math.sin(frame * 0.14) * 0.04})`,
                  }}
                />
                {/* Frontal Lobe Pulse Ring */}
                <div
                  style={{
                    position: "absolute",
                    right: 48,
                    top: 105,
                    width: 96,
                    height: 96,
                    borderRadius: "50%",
                    border: "4px solid #FFE600",
                    boxShadow: "0 0 30px #FFE600, inset 0 0 18px rgba(255, 230, 0, 0.45)",
                    transform: `scale(${0.95 + Math.sin(frame * 0.2) * 0.14})`,
                  }}
                />
              </div>

              {/* Center Energy Pulse Beam from Frontal Lobe to Shield */}
              <svg
                width="1080"
                height="460"
                viewBox="0 0 1080 460"
                style={{ position: "absolute", left: 0, top: 600, zIndex: 24, pointerEvents: "none" }}
              >
                <defs>
                  <linearGradient id="pulseBeamGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#FFE600" />
                    <stop offset="100%" stopColor="#FF3B47" />
                  </linearGradient>
                </defs>
                <path
                  d="M 415,190 Q 545,155 675,205"
                  fill="none"
                  stroke="url(#pulseBeamGrad)"
                  strokeWidth="8"
                  strokeDasharray="16 10"
                  strokeDashoffset={-frame * 4}
                  style={{ filter: "drop-shadow(0 0 14px rgba(255, 230, 0, 0.9))" }}
                />
                <polygon points="665,186 700,210 660,222" fill="#FF3B47" />
              </svg>

              {/* Right: 3D Shield Cracking & Lowering */}
              <div
                style={{
                  position: "absolute",
                  right: 85,
                  top: 635,
                  width: 340,
                  height: 340,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  zIndex: 23,
                  transform: `translateY(${shieldY}px) rotate(${shieldRot}deg)`,
                  opacity: shieldOpacity,
                }}
              >
                <Img
                  src={staticFile("objects/shield.png")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "contain",
                    filter: "drop-shadow(0 22px 45px rgba(255, 59, 71, 0.55))",
                  }}
                />
                {/* Glowing Crack Overlay */}
                <svg
                  width="240"
                  height="260"
                  viewBox="0 0 240 260"
                  style={{
                    position: "absolute",
                    opacity: crackOpacity,
                    pointerEvents: "none",
                    filter: "drop-shadow(0 0 12px #FF3B47)",
                  }}
                >
                  <path
                    d="M120 20 L105 85 L140 125 L95 175 L125 235"
                    fill="none"
                    stroke="#FFE600"
                    strokeWidth="6"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M105 85 L65 110 M140 125 L178 148"
                    fill="none"
                    stroke="#FF3B47"
                    strokeWidth="5"
                    strokeLinecap="round"
                  />
                </svg>
              </div>

              {/* Right-Bottom Indicators: PHÒNG VỆ ↓  &  KẾT NỐI ↑ */}
              <div
                style={{
                  position: "absolute",
                  right: 75,
                  top: 1085,
                  width: 360,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 12,
                  zIndex: 25,
                }}
              >
                <div
                  style={{
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 36,
                    color: "#FF3B47",
                    WebkitTextStroke: "7px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 20px rgba(255, 59, 71, 0.8)",
                  }}
                >
                  PHÒNG VỆ ↓
                </div>

                {/* Connection Waves + KẾT NỐI ↑ */}
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                    transform: `scale(${0.92 + s3cProg * 0.14})`,
                  }}
                >
                  <svg
                    width="44"
                    height="44"
                    viewBox="0 0 48 48"
                    fill="none"
                    style={{ filter: "drop-shadow(0 0 12px rgba(52, 211, 153, 0.85))" }}
                  >
                    <path d="M8 30C15 21 33 21 40 30" stroke="#34D399" strokeWidth="4" strokeLinecap="round" />
                    <path d="M14 37C19 31 29 31 34 37" stroke="#34D399" strokeWidth="4" strokeLinecap="round" />
                    <circle cx="24" cy="42" r="3.5" fill="#34D399" />
                  </svg>
                  <div
                    style={{
                      fontFamily: "KanitBlack, sans-serif",
                      fontSize: 38,
                      color: "#34D399",
                      WebkitTextStroke: "7px #05070C",
                      paintOrder: "stroke fill",
                      textShadow: "0 0 22px rgba(52, 211, 153, 0.85)",
                    }}
                  >
                    KẾT NỐI ↑
                  </div>
                </div>
              </div>

              {/* Bottom Clean Summary Line */}
              <div
                style={{
                  position: "absolute",
                  left: 50,
                  right: 50,
                  bottom: 240,
                  textAlign: "center",
                }}
              >
                <div
                  style={{
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 42,
                    color: "#FFE600",
                    WebkitTextStroke: "8px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 32px rgba(255, 230, 0, 0.75)",
                    whiteSpace: "nowrap",
                  }}
                >
                  CỒN HẠ PHÒNG VỆ ➔ KẾT NỐI CỰC NHANH
                </div>
              </div>
            </AbsoluteFill>
          );
        })()}

        {/* =================================================================
            SCENE 4 (1207..1521): ÉP UỐNG CẢ NỂ & SỢ LẠC LÕNG
            Multi-layer: Peer Pressure Photo + Toast Inset + Red Dashed Link + Forensic Stamp
        ================================================================= */}
        {s4Active && (
          <AbsoluteFill style={{ opacity: s4Opacity }}>
            {/* Top-Right Secondary Inset: Crowded Table Pressure */}
            <div
              style={{
                position: "absolute",
                right: 55,
                top: 470,
                width: 280,
                height: 185,
                borderRadius: 18,
                overflow: "hidden",
                border: "3px solid #FFE600",
                boxShadow: "0 16px 40px rgba(0,0,0,0.85)",
                transform: "rotate(4deg)",
                zIndex: 26,
              }}
            >
              <Img
                src={staticFile("harvested/hanoi_friends_toast_real.jpg")}
                style={{ width: "100%", height: "100%", objectFit: "cover", filter: "saturate(1.2)" }}
              />
            </div>

            {/* Top-Left Psychological Trigger Callout */}
            <div
              style={{
                position: "absolute",
                left: 60,
                top: 490,
                zIndex: 25,
              }}
            >
              <div style={{ fontFamily: "KanitBlack, sans-serif", fontSize: 40, color: "#FF3B47", WebkitTextStroke: "7px #05070C", paintOrder: "stroke fill" }}>
                ÁP LỰC ĐỒNG TRANG LỨA
              </div>
              <div style={{ fontFamily: "BeVietnamProBlack, sans-serif", fontSize: 26, color: "#FFFFFF", WebkitTextStroke: "5px #05070C", paintOrder: "stroke fill" }}>
                "Không uống là không nể"
              </div>
            </div>

            <div
              style={{
                position: "absolute",
                left: 540,
                top: 930,
                width: 820,
                height: 580,
                perspective: 1100,
                transform: "translate(-50%, -50%)",
              }}
            >
              <div
                style={{
                  width: "100%",
                  height: "100%",
                  borderRadius: 30,
                  overflow: "hidden",
                  border: "4px solid #FF3B47",
                  boxShadow: "0 30px 70px rgba(255, 59, 71, 0.35)",
                  transform: "rotateX(5deg)",
                }}
              >
                <Img
                  src={staticFile("harvested/hanoi_peer_pressure_real.jpg")}
                  style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    transform: `scale(${1.02 + (frame - 1207) * 0.0007})`,
                  }}
                />
              </div>
            </div>

            {frame >= 1296 && (
              <div
                style={{
                  position: "absolute",
                  left: 540,
                  top: 1120,
                  transform: `translate(-50%, -50%) rotate(-10deg) scale(${stampTrap})`,
                  border: "7px solid #FF3B47",
                  borderRadius: 20,
                  padding: "10px 34px",
                  background: "transparent",
                  boxShadow: "0 0 36px rgba(255, 59, 71, 0.75)",
                  zIndex: 40,
                }}
              >
                <div
                  style={{
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 64,
                    color: "#FF3B47",
                    WebkitTextStroke: "9px #05070C",
                    paintOrder: "stroke fill",
                    whiteSpace: "nowrap",
                  }}
                >
                  BẪY ÉP UỐNG CẢ NỂ
                </div>
              </div>
            )}

            <div
              style={{
                position: "absolute",
                left: 60,
                right: 60,
                bottom: 240,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 34,
                  color: "#FFFFFF",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                VUI BUỒN ĐỀU NHẬU — TỪ CHỐI LẠI SỢ LẠC LÕNG
              </div>
            </div>
          </AbsoluteFill>
        )}

        {/* =================================================================
            SCENE 5 (1521..1800): CLIMAX SPLIT CONFRONTATION + VACUUM DROP
            Dual Framing (Like Theranos vs FTX) + 3D Balance Scale
        ================================================================= */}
        {s5Active && (
          <AbsoluteFill style={{ opacity: s5Opacity }}>
            <div
              style={{
                position: "absolute",
                top: 520,
                left: 50,
                right: 50,
                display: "flex",
                justifyContent: "space-between",
                gap: 28,
                transform: `scale(${interpolate(s5Slam, [0, 1], [1.15, 1.0])})`,
              }}
            >
              {/* Left Card: THỰC SỰ VUI */}
              <div style={{ flex: 1, textAlign: "center" }}>
                <div
                  style={{
                    height: 520,
                    borderRadius: 26,
                    overflow: "hidden",
                    border: "4px solid #42B2F2",
                    boxShadow: "0 20px 50px rgba(66, 178, 242, 0.4)",
                  }}
                >
                  <Img
                    src={staticFile("harvested/hanoi_friends_toast_real.jpg")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      transform: `scale(${1.04 + (frame - 1521) * 0.0007})`,
                    }}
                  />
                </div>
                <div
                  style={{
                    marginTop: 18,
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 46,
                    color: "#42B2F2",
                    WebkitTextStroke: "8px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 28px rgba(66, 178, 242, 0.8)",
                  }}
                >
                  THỰC SỰ VUI
                </div>
              </div>

              {/* Right Card: CHỈ VÌ NỂ */}
              <div style={{ flex: 1, textAlign: "center" }}>
                <div
                  style={{
                    height: 520,
                    borderRadius: 26,
                    overflow: "hidden",
                    border: "4px solid #FF3B47",
                    boxShadow: "0 20px 50px rgba(255, 59, 71, 0.4)",
                  }}
                >
                  <Img
                    src={staticFile("harvested/hanoi_peer_pressure_real.jpg")}
                    style={{
                      width: "100%",
                      height: "100%",
                      objectFit: "cover",
                      transform: `scale(${1.04 + (frame - 1521) * 0.0007})`,
                    }}
                  />
                </div>
                <div
                  style={{
                    marginTop: 18,
                    fontFamily: "KanitBlack, sans-serif",
                    fontSize: 46,
                    color: "#FF3B47",
                    WebkitTextStroke: "8px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 28px rgba(255, 59, 71, 0.8)",
                  }}
                >
                  CHỈ VÌ NỂ?
                </div>
              </div>
            </div>

            {/* Bottom Debate Hook */}
            <div
              style={{
                position: "absolute",
                left: 60,
                right: 60,
                bottom: 270,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 52,
                  color: "#FFE600",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 32px rgba(255, 230, 0, 0.8)",
                }}
              >
                BẠN CHỌN VUI THẬT
              </div>
              <div
                style={{
                  fontFamily: "KanitBlack, sans-serif",
                  fontSize: 52,
                  color: "#FFFFFF",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 28px rgba(255, 255, 255, 0.45)",
                  marginTop: 4,
                }}
              >
                HAY CHỈ VÌ CẢ NỂ?
              </div>
            </div>
          </AbsoluteFill>
        )}
      </div>
    </AbsoluteFill>
  );
};
