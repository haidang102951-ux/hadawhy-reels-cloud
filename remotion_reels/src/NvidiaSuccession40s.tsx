import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { KineticWordCaption } from "./components/KineticWordCaption";
import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16";
import { RealPersonSpotlight3D } from "./components/RealPersonSpotlight3D";
import { GeoStrategicMap3D } from "./components/GeoStrategicMap3D";
import { TimelineTrack3D } from "./components/TimelineTrack3D";
import { StickerPop } from "./components/StickerPop";
import {
  ORIGIN_COORD,
  TARGET_COORD,
  ORIGIN_PATHS,
  TARGET_PATHS,
  BG_PATHS,
} from "./components/usSingaporeGeoPaths";
import { NVIDIA_CAPTIONS } from "./nvidiaCaptionsData";

const TITAN_SCREWS = [
  { top: 12, left: 12 },
  { top: 12, right: 12 },
  { bottom: 12, left: 12 },
  { bottom: 12, right: 12 },
] as const;

export const NvidiaSuccession40s: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // =========================================================================
  // GLOBAL CAMERA SHAKE ON HEAVY PHYSICAL / FORENSIC IMPACTS
  // =========================================================================
  const impactFrames = [178, 284, 610, 1078, 1425, 1890, 2080, 2545];
  let shakeX = 0;
  let shakeY = 0;
  for (const imp of impactFrames) {
    if (frame >= imp && frame < imp + 14) {
      const dt = frame - imp;
      const decay = Math.exp(-dt * 0.28);
      shakeX += Math.sin(dt * 3.1) * 14 * decay;
      shakeY += Math.cos(dt * 3.5) * 12 * decay;
    }
  }

  // =========================================================================
  // SCENE 1 (0..345 frames | 0.00s..5.75s): JENSEN HUANG + 33 NĂM + GAVEL SLAM
  // =========================================================================
  const s1Active = frame <= 355;
  const s1Exit = interpolate(frame, [332, 348], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const odometerVal = Math.round(
    interpolate(frame, [12, 62], [0, 33], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );
  const odoPop = spring({
    frame: Math.max(0, frame - 8),
    fps,
    config: { damping: 12, stiffness: 170 },
  });
  const gavelSwing = spring({
    frame: Math.max(0, frame - 150),
    fps,
    config: { damping: 10, stiffness: 195 },
  });
  const gavelImpact = spring({
    frame: Math.max(0, frame - 172),
    fps,
    config: { damping: 9, stiffness: 250 },
  });
  const crownTilt = interpolate(gavelImpact, [0, 1], [0, -24]);
  const stamp1Pop = spring({
    frame: Math.max(0, frame - 280),
    fps,
    config: { damping: 10, stiffness: 240, mass: 0.7 },
  });

  // =========================================================================
  // SCENE 2 (345..735 frames | 5.75s..12.25s): US-SINGAPORE MAP + ALICE HUANG
  // =========================================================================
  const s2Active = frame >= 340 && frame <= 745;
  const s2Fade =
    interpolate(frame, [340, 354], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [722, 738], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  const foreignAssetPop = spring({
    frame: Math.max(0, frame - 518),
    fps,
    config: { damping: 10, stiffness: 230 },
  });
  const shieldScanY = ((frame * 5.5) % 150) - 75;
  const val3000Pop = spring({
    frame: Math.max(0, frame - 662),
    fps,
    config: { damping: 11, stiffness: 210 },
  });
  const val3000Pulse = 0.8 + 0.2 * Math.sin(frame * 0.35);

  // =========================================================================
  // SCENE 3 (735..1165 frames | 12.25s..19.42s): 60-RAY ORG WEB + NO COO
  // =========================================================================
  const s3Active = frame >= 730 && frame <= 1175;
  const s3Local = frame - 735;
  const s3Opacity =
    interpolate(frame, [730, 745], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [1152, 1168], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  const webDraw = spring({
    frame: Math.max(0, s3Local - 12),
    fps,
    config: { damping: 16, stiffness: 85 },
  });
  const noCooSlash = spring({
    frame: Math.max(0, frame - 842),
    fps,
    config: { damping: 10, stiffness: 220 },
  });
  const webFractureProgress = interpolate(frame, [930, 1085], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const powerVoidPop = spring({
    frame: Math.max(0, frame - 1074),
    fps,
    config: { damping: 11, stiffness: 200 },
  });

  // =========================================================================
  // SCENE 4 (1165..1725 frames | 19.42s..28.75s): TIMELINE 1993-1999 + NEAL
  // =========================================================================
  const s4Active = frame >= 1160 && frame <= 1735;
  const s4Exit = interpolate(frame, [1710, 1726], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const cooleyCardPop = spring({
    frame: Math.max(0, frame - 1345),
    fps,
    config: { damping: 13, stiffness: 160 },
  });
  const cooleyBeatAFade = interpolate(frame, [1412, 1435], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const nealPop = spring({
    frame: Math.max(0, frame - 1412),
    fps,
    config: { damping: 13, stiffness: 145 },
  });
  const lightSweep4 = interpolate(frame, [1455, 1525], [-120, 130], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // =========================================================================
  // SCENE 5 (1725..2200 frames | 28.75s..36.67s): TIME 1997 + THERANOS & FTX
  // =========================================================================
  const s5Active = frame >= 1720 && frame <= 2210;
  const s5Exit = interpolate(frame, [2186, 2202], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s5BeatAOpacity =
    interpolate(frame, [1720, 1735], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }) *
    interpolate(frame, [1950, 1975], [1, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  const timePop = spring({
    frame: Math.max(0, frame - 1732),
    fps,
    config: { damping: 13, stiffness: 150 },
  });
  const sentenceStrike = interpolate(frame, [1915, 1945], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const s5BeatBOpacity = interpolate(frame, [1950, 1972], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const theranosPop = spring({
    frame: Math.max(0, frame - 1965),
    fps,
    config: { damping: 12, stiffness: 165 },
  });
  const ftxPop = spring({
    frame: Math.max(0, frame - 2015),
    fps,
    config: { damping: 12, stiffness: 165 },
  });
  const wallStStampPop = spring({
    frame: Math.max(0, frame - 2075),
    fps,
    config: { damping: 10, stiffness: 240 },
  });

  // =========================================================================
  // SCENE 6 (2200..2572 frames | 36.67s..42.86s): SCALE CONFLICT + CLIMAX
  // =========================================================================
  const s6Active = frame >= 2195;
  const s6Enter = interpolate(frame, [2195, 2212], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const scaleTilt = Math.sin((frame - 2200) * 0.14) * 7;
  const beat6Dim = interpolate(frame, [2376, 2394], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const scale6Zoom = interpolate(frame, [2380, 2405], [1, 0.84], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const nvCardPop = spring({
    frame: Math.max(0, frame - 2384),
    fps,
    config: { damping: 11, stiffness: 185 },
  });
  const nvShudderX =
    frame >= 2440 ? Math.sin(frame * 1.9) * (frame >= 2528 ? 9 : 4) : 0;
  const nvShudderRot =
    frame >= 2440 ? Math.cos(frame * 1.6) * (frame >= 2528 ? 3.5 : 1.5) : 0;
  const finalQPop = spring({
    frame: Math.max(0, frame - 2535),
    fps,
    config: { damping: 10, stiffness: 230 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#030710",
        overflow: "hidden",
      }}
    >
      {/* Vietnamese Fonts */}
      <style>
        {`
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
        `}
      </style>

      {/* Theme DNA: tech_ai_auto Radial Cyber Backdrop */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(circle at 50% 34%, rgba(12, 52, 88, 0.65) 0%, rgba(6, 14, 28, 0.95) 62%, #030710 100%)",
        }}
      />

      {/* Subtle Tech Circuit Grid */}
      <svg
        width={1080}
        height={1920}
        style={{ position: "absolute", inset: 0, opacity: 0.12, pointerEvents: "none" }}
      >
        {Array.from({ length: 12 }).map((_, i) => (
          <line
            key={`gx-${i}`}
            x1={i * 90}
            y1={0}
            x2={i * 90}
            y2={1920}
            stroke="#00E5FF"
            strokeWidth={1}
          />
        ))}
        {Array.from({ length: 22 }).map((_, i) => (
          <line
            key={`gy-${i}`}
            x1={0}
            y1={i * 90}
            x2={1080}
            y2={i * 90}
            stroke="#00E5FF"
            strokeWidth={1}
          />
        ))}
      </svg>

      {/* Ambient Parallax Cyber Motes */}
      {Array.from({ length: 18 }).map((_, i) => {
        const px = ((i * 157) % 900) + 60;
        const py = ((i * 271) % 1920) - frame * (0.75 + (i % 3) * 0.35);
        const wrappedY = ((py % 1920) + 1920) % 1920;
        const dotBg =
          i % 3 === 0
            ? "rgba(0, 229, 255, 0.28)"
            : i % 3 === 1
              ? "rgba(118, 185, 0, 0.25)"
              : "rgba(255, 230, 0, 0.22)";
        return (
          <div
            key={`mote-${i}`}
            style={{
              position: "absolute",
              left: px,
              top: wrappedY,
              width: 4 + (i % 4) * 2,
              height: 4 + (i % 4) * 2,
              borderRadius: "50%",
              background: dotBg,
              filter: "blur(1px)",
            }}
          />
        );
      })}

      {/* DUAL-LAYER BRAND WATERMARK (brand/hadawhy_logo.png) */}
      <ChannelWatermark9x16 />

      {/* TOP FIXED ZERO-BOX 80/20 KINETIC CAPTIONS */}
      <KineticWordCaption phrases={NVIDIA_CAPTIONS} />

      {/* MAIN CAMERA SHAKE STAGE */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate3d(${shakeX}px, ${shakeY}px, 0)`,
        }}
      >
        {/* =================================================================
            SCENE 1 (0..345 frames | 0.00s..5.75s)
           ================================================================= */}
        {s1Active && (
          <div style={{ position: "absolute", inset: 0, opacity: s1Exit }}>
            {/* Glowing Cyber Circuit Floor Platform */}
            <div
              style={{
                position: "absolute",
                left: 495,
                top: 1295,
                width: 580,
                height: 112,
                transform: "translate(-50%, -50%)",
                borderRadius: "50%",
                background:
                  frame >= 178
                    ? "radial-gradient(ellipse, rgba(255,59,71,0.45) 0%, rgba(12,52,88,0.2) 60%, rgba(0,0,0,0) 75%)"
                    : "radial-gradient(ellipse, rgba(0,229,255,0.45) 0%, rgba(118,185,0,0.22) 60%, rgba(0,0,0,0) 75%)",
                border:
                  frame >= 178
                    ? "3px solid rgba(255,59,71,0.85)"
                    : "3px solid rgba(0,229,255,0.85)",
                boxShadow:
                  frame >= 178
                    ? "0 0 42px rgba(255,59,71,0.55)"
                    : "0 0 42px rgba(0,229,255,0.55)",
              }}
            />

            <RealPersonSpotlight3D
              startFrame={0}
              endFrame={345}
              centerX={495}
              backdropWidth={740}
              backdropSrc="harvested/nvidia_hq_real.png"
              cutoutSrc="harvested/jensen_huang_real.png"
              cutoutWidth={475}
              cutoutTop={985}
              labelTop={1465}
              rimGlowColor={
                frame >= 178 ? "rgba(255, 59, 71, 0.92)" : "rgba(0, 229, 255, 0.92)"
              }
              subjectSubtitle="CEO NVIDIA"
              subjectName="JENSEN HUANG"
            />

            {/* Floating Golden Crown above Jensen (tilts & cracks in Beat B) */}
            <StickerPop
              src="objects/crown.png"
              x={495}
              y={475}
              width={170}
              startFrame={6}
              baseRotate={crownTilt}
              floatSpeed={0.08}
              floatAmp={7}
              rimColor={
                frame >= 178 ? "rgba(255, 59, 71, 0.95)" : "rgba(255, 230, 0, 0.95)"
              }
              shudderAtFrame={178}
            />
            {frame >= 178 && (
              <svg
                width={1080}
                height={1920}
                style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
              >
                <path
                  d="M 485 415 L 502 455 L 484 485 L 508 525"
                  fill="none"
                  stroke="#FF3B47"
                  strokeWidth={6}
                  strokeLinecap="round"
                  style={{ filter: "drop-shadow(0 0 12px #FF3B47)" }}
                />
              </svg>
            )}

            {/* Mechanical Odometer: 33 NĂM */}
            <div
              style={{
                position: "absolute",
                left: 225,
                top: 525,
                transform: `translate(-50%, -50%) scale(${odoPop})`,
                textAlign: "center",
                whiteSpace: "nowrap",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 66,
                  color: "#FFE600",
                  WebkitTextStroke: "10px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 28px rgba(255, 230, 0, 0.75)",
                  lineHeight: 1,
                }}
              >
                {odometerVal} NĂM
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 26,
                  color: "#00E5FF",
                  WebkitTextStroke: "6px #05070C",
                  paintOrder: "stroke fill",
                  marginTop: 4,
                }}
              >
                NGỰ TRỊ CHIP AI
              </div>
            </div>

            {/* Beat B: Judge Gavel slamming down + Red Forensic Stamp */}
            {frame >= 150 && (
              <div
                style={{
                  position: "absolute",
                  left: interpolate(gavelImpact, [0, 1], [775, 685]),
                  top: interpolate(gavelImpact, [0, 1], [435, 650]),
                  width: 245,
                  transform: `translate(-50%, -50%) scale(${gavelSwing}) rotate(${interpolate(
                    gavelImpact,
                    [0, 1],
                    [-36, 10]
                  )}deg)`,
                  filter:
                    "drop-shadow(0 0 18px rgba(255,59,71,0.8)) drop-shadow(0 20px 28px rgba(0,0,0,0.9))",
                }}
              >
                <Img
                  src={staticFile("objects/judge_gavel.png")}
                  style={{ width: "100%", height: "auto" }}
                />
              </div>
            )}

            {frame >= 280 && (
              <div
                style={{
                  position: "absolute",
                  left: 495,
                  top: 1175,
                  transform: `translate(-50%, -50%) scale(${interpolate(
                    stamp1Pop,
                    [0, 1],
                    [2.3, 1.0]
                  )}) rotate(-7deg)`,
                  padding: "16px 38px",
                  borderRadius: 16,
                  background: "rgba(22, 4, 10, 0.9)",
                  border: "5px solid #FF3B47",
                  boxShadow:
                    "0 24px 48px rgba(0,0,0,0.92), 0 0 38px rgba(255, 59, 71, 0.65)",
                  whiteSpace: "nowrap",
                }}
              >
                <div
                  style={{
                    fontFamily: "BeVietnamProBlack, sans-serif",
                    fontSize: 48,
                    color: "#FF3B47",
                    letterSpacing: "0.04em",
                    WebkitTextStroke: "6px #05070C",
                    paintOrder: "stroke fill",
                  }}
                >
                  ĐIỀU TRA ĐỘC LẬP
                </div>
              </div>
            )}
          </div>
        )}

        {/* =================================================================
            SCENE 2 (345..735 frames | 5.75s..12.25s)
           ================================================================= */}
        {s2Active && (
          <div style={{ position: "absolute", inset: 0, opacity: s2Fade }}>
            <GeoStrategicMap3D
              startFrame={345}
              endFrame={735}
              originLabel="THUNG LŨNG SILICON"
              targetLabel="SINGAPORE"
              originCoord={ORIGIN_COORD}
              targetCoord={TARGET_COORD}
              originPaths={ORIGIN_PATHS}
              targetPaths={TARGET_PATHS}
              bgPaths={BG_PATHS}
              containerLeft={95}
              containerTop={320}
              containerWidth={800}
              containerHeight={512}
              originLabelPos={{ x: 215, y: 195 }}
              targetLabelPos={{ x: 640, y: 445 }}
              evidenceImageSrc="harvested/alice_huang_dossier.png"
              evidenceTitle="HỒ SƠ: ALICE HUANG - SINGAPORE"
              evidenceCenterX={465}
              evidenceTop={1115}
              evidenceWidth={500}
              evidenceHeight={375}
              evidenceObjectPosition="center 16%"
              evidenceTitleFontSize={31}
              leftFloatingIconSrc="objects/shield.png"
              leftFloatingIconPos={{ x: 175, y: 1095, width: 175 }}
              rightFloatingIconSrc="objects/padlock.png"
              rightFloatingIconPos={{ x: 785, y: 1095, width: 185 }}
            />

            {/* Red Laser Scanning Bar across US Security Shield (Beat B) */}
            {frame >= 540 && (
              <div
                style={{
                  position: "absolute",
                  left: 175,
                  top: 1095 + shieldScanY,
                  width: 195,
                  height: 6,
                  transform: "translate(-50%, -50%)",
                  background: "#FF3B47",
                  boxShadow: "0 0 18px #FF3B47, 0 0 32px #FF3B47",
                  borderRadius: 4,
                  pointerEvents: "none",
                }}
              />
            )}

            {/* FOREIGN ASSET Stamp on Alice Huang Dossier */}
            {frame >= 518 && (
              <div
                style={{
                  position: "absolute",
                  left: 615,
                  top: 965,
                  transform: `translate(-50%, -50%) scale(${interpolate(
                    foreignAssetPop,
                    [0, 1],
                    [2.1, 1.0]
                  )}) rotate(-10deg)`,
                  padding: "8px 20px",
                  borderRadius: 10,
                  background: "rgba(18, 5, 10, 0.9)",
                  border: "4px solid #FF3B47",
                  boxShadow: "0 0 24px rgba(255, 59, 71, 0.7)",
                  whiteSpace: "nowrap",
                }}
              >
                <span
                  style={{
                    fontFamily: "BeVietnamProBlack, sans-serif",
                    fontSize: 28,
                    color: "#FF3B47",
                  }}
                >
                  FOREIGN ASSET
                </span>
              </div>
            )}

            {/* 3.000 TỶ USD Warning Pulse */}
            {frame >= 662 && (
              <div
                style={{
                  position: "absolute",
                  left: 495,
                  top: 1495,
                  transform: `translate(-50%, -50%) scale(${val3000Pop})`,
                  textAlign: "center",
                  whiteSpace: "nowrap",
                  opacity: val3000Pulse,
                }}
              >
                <div
                  style={{
                    fontFamily: "BeVietnamProBlack, sans-serif",
                    fontSize: 64,
                    color: "#FFE600",
                    WebkitTextStroke: "10px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 30px rgba(255, 59, 71, 0.85)",
                  }}
                >
                  3.000 TỶ USD
                </div>
                <div
                  style={{
                    fontFamily: "BeVietnamProExtraBold, sans-serif",
                    fontSize: 28,
                    color: "#FF3B47",
                    WebkitTextStroke: "6px #05070C",
                    paintOrder: "stroke fill",
                  }}
                >
                  ĐẾ CHẾ BỊ ĐE DỌA
                </div>
              </div>
            )}
          </div>
        )}

        {/* =================================================================
            SCENE 3 (735..1165 frames | 12.25s..19.42s)
           ================================================================= */}
        {s3Active && (
          <div style={{ position: "absolute", inset: 0, opacity: s3Opacity }}>
            {/* Blurred Luxury Nvidia Headquarters Context Backdrop */}
            <div
              style={{
                position: "absolute",
                left: 495,
                top: 900,
                width: 810,
                height: 1120,
                transform: "translate(-50%, -50%)",
                borderRadius: 36,
                overflow: "hidden",
                opacity: 0.24,
                maskImage:
                  "radial-gradient(ellipse at center, black 45%, transparent 98%)",
                WebkitMaskImage:
                  "radial-gradient(ellipse at center, black 45%, transparent 98%)",
              }}
            >
              <Img
                src={staticFile("harvested/nvidia_hq_real.png")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  filter: "blur(3px) contrast(1.15) brightness(0.75)",
                }}
              />
            </div>

            {/* 60-Ray Power Spiderweb SVG */}
            <svg
              width={1080}
              height={1920}
              style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
            >
              {Array.from({ length: 60 }).map((_, idx) => {
                const isInner = idx < 24;
                const count = isInner ? 24 : 36;
                const localIdx = isInner ? idx : idx - 24;
                const angle =
                  (localIdx / count) * Math.PI * 2 + (isInner ? 0 : 0.14);
                const radius = isInner ? 205 : 315;
                const cx = 495;
                const cy = 835;
                const nx = cx + Math.cos(angle) * radius;
                const ny = cy + Math.sin(angle) * radius;
                const isBroken = webFractureProgress > 0.15;
                const endX = cx + (nx - cx) * webDraw;
                const endY = cy + (ny - cy) * webDraw;

                return (
                  <g key={`ray-${idx}`}>
                    {!isBroken ? (
                      <line
                        x1={cx}
                        y1={cy}
                        x2={endX}
                        y2={endY}
                        stroke={isInner ? "#00E5FF" : "#76B900"}
                        strokeWidth={isInner ? 2.5 : 1.8}
                        strokeOpacity={0.78}
                      />
                    ) : (
                      <>
                        <line
                          x1={cx}
                          y1={cy}
                          x2={cx + (nx - cx) * 0.35}
                          y2={cy + (ny - cy) * 0.35}
                          stroke="#FF3B47"
                          strokeWidth={2.2}
                          strokeDasharray="6 6"
                          strokeOpacity={0.85}
                        />
                        <line
                          x1={cx + (nx - cx) * 0.65}
                          y1={cy + (ny - cy) * 0.65}
                          x2={nx}
                          y2={ny}
                          stroke="#FF3B47"
                          strokeWidth={2.0}
                          strokeDasharray="5 7"
                          strokeOpacity={0.65}
                        />
                      </>
                    )}
                    <rect
                      x={endX - (isInner ? 6 : 5)}
                      y={endY - (isInner ? 6 : 5)}
                      width={isInner ? 12 : 10}
                      height={isInner ? 12 : 10}
                      rx={3}
                      fill={isBroken ? "#FF3B47" : "#00E5FF"}
                      stroke="#FFFFFF"
                      strokeWidth={1.5}
                      opacity={webDraw}
                    />
                  </g>
                );
              })}
            </svg>

            {/* Missing COO Position Node (Top-Center inside Safe Zone) */}
            <div
              style={{
                position: "absolute",
                left: 495,
                top: 430,
                transform: "translate(-50%, -50%)",
                padding: "12px 32px",
                borderRadius: 16,
                border: "3px dashed #FF3B47",
                background: "rgba(25, 8, 14, 0.85)",
                textAlign: "center",
                whiteSpace: "nowrap",
              }}
            >
              <div
                style={{
                  fontFamily: "BeVietnamProExtraBold, sans-serif",
                  fontSize: 24,
                  color: "#CBD5E1",
                }}
              >
                GHẾ GIÁM ĐỐC VẬN HÀNH
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 38,
                  color: "#FF3B47",
                }}
              >
                {frame >= 842 ? "✕ KHÔNG CÓ COO" : "COO SLOT"}
              </div>
              {frame >= 842 && (
                <div
                  style={{
                    position: "absolute",
                    inset: -6,
                    borderRadius: 18,
                    border: "4px solid #FF3B47",
                    transform: `scale(${interpolate(noCooSlash, [0, 1], [1.4, 1])})`,
                    boxShadow: "0 0 28px rgba(255, 59, 71, 0.8)",
                    pointerEvents: "none",
                  }}
                />
              )}
            </div>

            {/* Central Jensen Huang Node */}
            <div
              style={{
                position: "absolute",
                left: 495,
                top: 835,
                width: 175,
                height: 175,
                transform: `translate(-50%, -50%) rotate(${
                  webFractureProgress > 0.2 ? -6 : 0
                }deg)`,
                borderRadius: "50%",
                overflow: "hidden",
                border:
                  webFractureProgress > 0.2
                    ? "5px solid #FF3B47"
                    : "5px solid #00E5FF",
                background: "#0B1628",
                boxShadow:
                  webFractureProgress > 0.2
                    ? "0 0 42px rgba(255,59,71,0.9)"
                    : "0 0 42px rgba(0,229,255,0.85)",
              }}
            >
              <Img
                src={staticFile("harvested/jensen_huang_real.png")}
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  objectPosition: "center top",
                }}
              />
            </div>
            <div
              style={{
                position: "absolute",
                left: 495,
                top: 948,
                transform: "translate(-50%, -50%)",
                padding: "4px 16px",
                borderRadius: 10,
                background: "rgba(3, 7, 16, 0.9)",
                border: "1.5px solid rgba(0, 229, 255, 0.55)",
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 25,
                color: "#FFFFFF",
                whiteSpace: "nowrap",
              }}
            >
              JENSEN HUANG
            </div>

            {/* Counter: 60 Lãnh Đạo */}
            {frame < 1065 && (
              <div
                style={{
                  position: "absolute",
                  left: 495,
                  top: 1275,
                  transform: "translate(-50%, -50%)",
                  textAlign: "center",
                  whiteSpace: "nowrap",
                }}
              >
                <div
                  style={{
                    fontFamily: "BeVietnamProBlack, sans-serif",
                    fontSize: 52,
                    color: "#00E5FF",
                    WebkitTextStroke: "9px #05070C",
                    paintOrder: "stroke fill",
                  }}
                >
                  60 LÃNH ĐẠO
                </div>
                <div
                  style={{
                    fontFamily: "BeVietnamProExtraBold, sans-serif",
                    fontSize: 30,
                    color: "#FFFFFF",
                    WebkitTextStroke: "7px #05070C",
                    paintOrder: "stroke fill",
                  }}
                >
                  BÁO CÁO TRỰC TIẾP
                </div>
              </div>
            )}

            {/* Beat B: Barrier Slam + Power Vacuum */}
            <StickerPop
              src="objects/barrier.png"
              x={495}
              y={1145}
              width={295}
              startFrame={1055}
              floatSpeed={0.07}
              floatAmp={6}
              rimColor="rgba(255, 59, 71, 0.95)"
              shudderAtFrame={1078}
            />
            {frame >= 1074 && (
              <div
                style={{
                  position: "absolute",
                  left: 495,
                  top: 1410,
                  transform: `translate(-50%, -50%) scale(${powerVoidPop})`,
                  textAlign: "center",
                  whiteSpace: "nowrap",
                }}
              >
                <div
                  style={{
                    fontFamily: "BeVietnamProBlack, sans-serif",
                    fontSize: 54,
                    color: "#FF3B47",
                    WebkitTextStroke: "10px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 30px rgba(255,59,71,0.85)",
                  }}
                >
                  KHOẢNG TRỐNG QUYỀN LỰC
                </div>
                <div
                  style={{
                    fontFamily: "BeVietnamProExtraBold, sans-serif",
                    fontSize: 30,
                    color: "#FFE600",
                    WebkitTextStroke: "7px #05070C",
                    paintOrder: "stroke fill",
                  }}
                >
                  KHỦNG HOẢNG KẾ NHIỆM
                </div>
              </div>
            )}
          </div>
        )}

        {/* =================================================================
            SCENE 4 (1165..1725 frames | 19.42s..28.75s)
           ================================================================= */}
        {s4Active && (
          <div style={{ position: "absolute", inset: 0, opacity: s4Exit }}>
            {/* Beat A: Timeline 1993 -> 1999 + White-Card Cooley Logo */}
            <div style={{ opacity: cooleyBeatAFade }}>
              <TimelineTrack3D
                startFrame={1165}
                endFrame={1440}
                centerX={495}
                columnOffset={235}
                spineTop={425}
                spineMaxHeight={620}
                startNodeY={515}
                nodeStepY={340}
                spineColors={["#00E5FF", "#FFE600"]}
                milestones={[
                  {
                    dateLabel: "1993",
                    title: "THÀNH LẬP NVIDIA",
                    iconOrCutoutSrc: "objects/computer_chip.png",
                    accentColor: "#00E5FF",
                    triggerOffsetFrames: 12,
                  },
                  {
                    dateLabel: "1999",
                    title: "IPO NASDAQ",
                    iconOrCutoutSrc: "objects/chart_up.png",
                    accentColor: "#FFE600",
                    triggerOffsetFrames: 75,
                  },
                ]}
              />

              {/* Cooley Logo in White Titanium Glass Card (Beat A) */}
              {frame >= 1345 && (
                <div
                  style={{
                    position: "absolute",
                    left: 495,
                    top: 1295,
                    width: 550,
                    transform: `translate(-50%, -50%) scale(${cooleyCardPop})`,
                    borderRadius: 22,
                    background: "rgba(255, 255, 255, 0.95)",
                    border: "4px solid #94A3B8",
                    boxShadow:
                      "0 24px 50px rgba(0,0,0,0.85), 0 0 32px rgba(0,229,255,0.4)",
                    padding: "24px 36px",
                    textAlign: "center",
                  }}
                >
                  <Img
                    src={staticFile("harvested/cooley_logo.png")}
                    style={{
                      width: 280,
                      height: "auto",
                      margin: "0 auto",
                      display: "block",
                    }}
                  />
                  <div
                    style={{
                      marginTop: 14,
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 28,
                      color: "#0F172A",
                    }}
                  >
                    CỰU CEO HÃNG LUẬT COOLEY
                  </div>
                </div>
              )}
            </div>

            {/* Beat B (frame >= 1410): Stephen Neal Cyan 3D Spotlight + Titan Director Badge */}
            {frame >= 1410 && (
              <div style={{ opacity: nealPop }}>
                {/* Compact Timeline & Cooley Pill Badges floating cleanly beside Neal */}
                <div
                  style={{
                    position: "absolute",
                    left: 225,
                    top: 475,
                    transform: "translate(-50%, -50%)",
                    padding: "14px 26px",
                    borderRadius: 16,
                    background: "rgba(255, 255, 255, 0.94)",
                    border: "3px solid #94A3B8",
                    boxShadow: "0 16px 32px rgba(0,0,0,0.85)",
                  }}
                >
                  <Img
                    src={staticFile("harvested/cooley_logo.png")}
                    style={{ width: 170, height: "auto", display: "block" }}
                  />
                </div>

                <div
                  style={{
                    position: "absolute",
                    left: 745,
                    top: 475,
                    transform: "translate(-50%, -50%)",
                    padding: "12px 24px",
                    borderRadius: 16,
                    background: "rgba(8, 22, 42, 0.9)",
                    border: "3px solid #FFE600",
                    boxShadow: "0 0 24px rgba(255, 230, 0, 0.45)",
                    whiteSpace: "nowrap",
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 32,
                      color: "#FFE600",
                    }}
                  >
                    1993 ➔ 1999
                  </div>
                  <div
                    style={{
                      fontFamily: "BeVietnamProExtraBold, sans-serif",
                      fontSize: 20,
                      color: "#FFFFFF",
                    }}
                  >
                    IPO NASDAQ
                  </div>
                </div>

                {/* Stephen Neal Cutout with Cyan Neon Rim Glow */}
                <div
                  style={{
                    position: "absolute",
                    left: 495,
                    top: 905 + Math.sin(frame * 0.08) * 7,
                    width: 455,
                    transform: `translate(-50%, -50%) scale(${nealPop})`,
                  }}
                >
                  <Img
                    src={staticFile("harvested/stephen_neal_real.png")}
                    style={{
                      width: "100%",
                      height: "auto",
                      filter:
                        "drop-shadow(0px 0px 8px #00E5FF) drop-shadow(0px 0px 26px rgba(0,229,255,0.65)) drop-shadow(0px 26px 38px rgba(0,0,0,0.92))",
                    }}
                  />
                </div>

                {/* Forensic Titan Acrylic Plate */}
                <div
                  style={{
                    position: "absolute",
                    left: 495,
                    top: 1410,
                    width: 740,
                    transform: "translate(-50%, -50%)",
                    borderRadius: 22,
                    background: "rgba(8, 18, 36, 0.92)",
                    border: "3px solid #00E5FF",
                    boxShadow:
                      "0 28px 56px rgba(0,0,0,0.92), 0 0 36px rgba(0, 229, 255, 0.35)",
                    padding: "24px 36px",
                    textAlign: "center",
                    overflow: "hidden",
                  }}
                >
                  {/* Titanium Corner Screws */}
                  {TITAN_SCREWS.map((pos, si) => (
                    <div
                      key={`scr4-${si}`}
                      style={{
                        position: "absolute",
                        ...pos,
                        width: 12,
                        height: 12,
                        borderRadius: "50%",
                        background: "linear-gradient(135deg, #E2E8F0, #475569)",
                        border: "1px solid #94A3B8",
                      }}
                    />
                  ))}
                  {/* Metallic Light Sweep */}
                  <div
                    style={{
                      position: "absolute",
                      top: 0,
                      bottom: 0,
                      left: `${lightSweep4}%`,
                      width: 110,
                      background:
                        "linear-gradient(90deg, transparent, rgba(255,255,255,0.22), transparent)",
                      transform: "skewX(-20deg)",
                      pointerEvents: "none",
                    }}
                  />
                  <div
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 50,
                      color: "#FFFFFF",
                      letterSpacing: "0.02em",
                    }}
                  >
                    STEPHEN NEAL
                  </div>
                  <div
                    style={{
                      fontFamily: "BeVietnamProExtraBold, sans-serif",
                      fontSize: 28,
                      color: "#00E5FF",
                      letterSpacing: "0.05em",
                      marginTop: 4,
                    }}
                  >
                    LEAD INDEPENDENT DIRECTOR
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* =================================================================
            SCENE 5 (1725..2200 frames | 28.75s..36.67s)
           ================================================================= */}
        {s5Active && (
          <div style={{ position: "absolute", inset: 0, opacity: s5Exit }}>
            {/* Beat A: TIME 1997 "Legal Houdini" + Keating + Handcuffs Opening */}
            {frame < 1978 && (
              <div style={{ opacity: s5BeatAOpacity }}>
                {/* Header Tag */}
                <div
                  style={{
                    position: "absolute",
                    left: 495,
                    top: 385,
                    transform: "translate(-50%, -50%)",
                    padding: "10px 28px",
                    borderRadius: 12,
                    background: "rgba(255, 230, 0, 0.14)",
                    border: "3px solid #FFE600",
                    whiteSpace: "nowrap",
                  }}
                >
                  <span
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 30,
                      color: "#FFE600",
                    }}
                  >
                    TIME 1997: LEGAL HOUDINI
                  </span>
                </div>

                {/* Tilted TIME 1997 Cover */}
                <div
                  style={{
                    position: "absolute",
                    left: 365,
                    top: 825,
                    width: 470,
                    transform: `translate(-50%, -50%) scale(${timePop}) rotate(-3deg)`,
                    borderRadius: 18,
                    overflow: "hidden",
                    border: "4px solid #FFE600",
                    boxShadow:
                      "0 30px 60px rgba(0,0,0,0.92), 0 0 36px rgba(255, 230, 0, 0.35)",
                  }}
                >
                  <Img
                    src={staticFile("harvested/time_magazine_1997.png")}
                    style={{ width: "100%", height: "auto", display: "block" }}
                  />
                </div>

                {/* Charles Keating Cutout Badge */}
                <div
                  style={{
                    position: "absolute",
                    left: 745,
                    top: 615,
                    width: 240,
                    transform: `translate(-50%, -50%) scale(${timePop})`,
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      width: 215,
                      height: 215,
                      margin: "0 auto",
                      borderRadius: "50%",
                      overflow: "hidden",
                      border: "4px solid #00E5FF",
                      background: "#0B1628",
                      boxShadow: "0 0 30px rgba(0,229,255,0.5)",
                    }}
                  >
                    <Img
                      src={staticFile("harvested/charles_keating_real.png")}
                      style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        objectPosition: "center top",
                      }}
                    />
                  </div>
                  <div
                    style={{
                      marginTop: 10,
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 26,
                      color: "#FFFFFF",
                      WebkitTextStroke: "6px #05070C",
                      paintOrder: "stroke fill",
                    }}
                  >
                    CHARLES KEATING
                  </div>
                </div>

                {/* Opening Handcuffs 3D */}
                <StickerPop
                  src="objects/handcuffs.png"
                  x={735}
                  y={1015}
                  width={260}
                  startFrame={1825}
                  baseRotate={14}
                  floatSpeed={0.09}
                  floatAmp={8}
                  rimColor="rgba(255, 230, 0, 0.92)"
                  shudderAtFrame={1890}
                />

                {/* Sentence Reduction Zero-Box Graphic */}
                <div
                  style={{
                    position: "absolute",
                    left: 495,
                    top: 1385,
                    transform: "translate(-50%, -50%)",
                    display: "flex",
                    alignItems: "center",
                    gap: 24,
                    whiteSpace: "nowrap",
                  }}
                >
                  <div style={{ position: "relative" }}>
                    <span
                      style={{
                        fontFamily: "BeVietnamProBlack, sans-serif",
                        fontSize: 58,
                        color: "#CBD5E1",
                        WebkitTextStroke: "9px #05070C",
                        paintOrder: "stroke fill",
                      }}
                    >
                      10 NĂM
                    </span>
                    <div
                      style={{
                        position: "absolute",
                        left: -8,
                        top: "50%",
                        width: `${sentenceStrike * 110}%`,
                        height: 8,
                        background: "#FF3B47",
                        transform: "translateY(-50%) rotate(-5deg)",
                        boxShadow: "0 0 14px #FF3B47",
                      }}
                    />
                  </div>
                  <span
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 52,
                      color: "#FFFFFF",
                      WebkitTextStroke: "8px #05070C",
                      paintOrder: "stroke fill",
                    }}
                  >
                    ➔
                  </span>
                  <span
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 66,
                      color: "#FFE600",
                      WebkitTextStroke: "10px #05070C",
                      paintOrder: "stroke fill",
                      textShadow: "0 0 28px rgba(255, 230, 0, 0.8)",
                    }}
                  >
                    &lt; 5 NĂM
                  </span>
                </div>
              </div>
            )}

            {/* Beat B: Two Parallel Frosted Glass Cards (Theranos & FTX) */}
            {frame >= 1950 && (
              <div style={{ opacity: s5BeatBOpacity }}>
                {/* Left Card: Elizabeth Holmes / THERANOS */}
                <div
                  style={{
                    position: "absolute",
                    left: 285,
                    top: 845,
                    width: 375,
                    transform: `translate(-50%, -50%) scale(${theranosPop}) rotate(-1.5deg)`,
                    borderRadius: 24,
                    background: "rgba(18, 12, 24, 0.92)",
                    border: "4px solid #FF3B47",
                    boxShadow:
                      "0 26px 52px rgba(0,0,0,0.92), 0 0 34px rgba(255,59,71,0.45)",
                    padding: 18,
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      height: 365,
                      borderRadius: 16,
                      overflow: "hidden",
                      background: "radial-gradient(circle, #2A121C 0%, #0D070C 100%)",
                    }}
                  >
                    <Img
                      src={staticFile("harvested/elizabeth_holmes_real.png")}
                      style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        objectPosition: "center top",
                      }}
                    />
                  </div>
                  <div
                    style={{
                      marginTop: 16,
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 44,
                      color: "#FF3B47",
                    }}
                  >
                    THERANOS
                  </div>
                  <div
                    style={{
                      fontFamily: "BeVietnamProExtraBold, sans-serif",
                      fontSize: 24,
                      color: "#FFFFFF",
                    }}
                  >
                    ĐẠI ÁN LỪA ĐẢO Y TẾ
                  </div>
                </div>

                {/* Right Card: FTX Logo on Bright White Frosted Glass */}
                <div
                  style={{
                    position: "absolute",
                    left: 705,
                    top: 845,
                    width: 375,
                    transform: `translate(-50%, -50%) scale(${ftxPop}) rotate(1.5deg)`,
                    borderRadius: 24,
                    background: "rgba(12, 20, 38, 0.92)",
                    border: "4px solid #00E5FF",
                    boxShadow:
                      "0 26px 52px rgba(0,0,0,0.92), 0 0 34px rgba(0,229,255,0.4)",
                    padding: 18,
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      position: "relative",
                      height: 365,
                      borderRadius: 16,
                      background: "rgba(255, 255, 255, 0.96)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      padding: 28,
                      overflow: "hidden",
                    }}
                  >
                    <Img
                      src={staticFile("harvested/ftx_logo.png")}
                      style={{ width: "92%", height: "auto" }}
                    />
                    {/* Red Fracture Lines over FTX */}
                    <svg
                      width={340}
                      height={365}
                      style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
                    >
                      <path
                        d="M 40 30 L 145 165 L 115 215 L 285 335 M 275 45 L 175 180 L 210 235 L 70 325"
                        fill="none"
                        stroke="#FF3B47"
                        strokeWidth={5}
                        strokeLinecap="round"
                        opacity={0.78}
                      />
                    </svg>
                  </div>
                  <div
                    style={{
                      marginTop: 16,
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 44,
                      color: "#00E5FF",
                    }}
                  >
                    FTX
                  </div>
                  <div
                    style={{
                      fontFamily: "BeVietnamProExtraBold, sans-serif",
                      fontSize: 24,
                      color: "#FFFFFF",
                    }}
                  >
                    ĐỀ CỬ CHỦ TỊCH
                  </div>
                </div>

                {/* Forensic Stamp: CHUYÊN GIA DẬP LỬA PHỐ WALL */}
                {frame >= 2075 && (
                  <div
                    style={{
                      position: "absolute",
                      left: 495,
                      top: 1365,
                      transform: `translate(-50%, -50%) scale(${interpolate(
                        wallStStampPop,
                        [0, 1],
                        [2.1, 1.0]
                      )}) rotate(-2deg)`,
                      padding: "16px 34px",
                      borderRadius: 16,
                      background: "rgba(10, 14, 26, 0.94)",
                      border: "4px solid #FFE600",
                      boxShadow:
                        "0 22px 44px rgba(0,0,0,0.95), 0 0 36px rgba(255,230,0,0.45)",
                      whiteSpace: "nowrap",
                    }}
                  >
                    <span
                      style={{
                        fontFamily: "BeVietnamProBlack, sans-serif",
                        fontSize: 38,
                        color: "#FFE600",
                      }}
                    >
                      CHUYÊN GIA DẬP LỬA PHỐ WALL
                    </span>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* =================================================================
            SCENE 6 (2200..2572 frames | 36.67s..42.86s)
           ================================================================= */}
        {s6Active && (
          <div style={{ position: "absolute", inset: 0, opacity: s6Enter }}>
            {/* Beat A: 3D Balance Scale Conflict (Lawyer Gavel vs AI GPU Chip) */}
            <div
              style={{
                position: "absolute",
                inset: 0,
                opacity: beat6Dim,
                transform: `scale(${scale6Zoom})`,
                transformOrigin: "495px 780px",
              }}
            >
              {/* Balance Scale Base */}
              <div
                style={{
                  position: "absolute",
                  left: 495,
                  top: 955,
                  width: 440,
                  transform: `translate(-50%, -50%) rotate(${scaleTilt}deg)`,
                }}
              >
                <Img
                  src={staticFile("objects/balance_scale.png")}
                  style={{
                    width: "100%",
                    height: "auto",
                    filter:
                      "drop-shadow(0 0 18px rgba(255,230,0,0.35)) drop-shadow(0 24px 36px rgba(0,0,0,0.9))",
                  }}
                />
              </div>

              {/* Left Pan: Judge Gavel (Legal) */}
              <div
                style={{
                  position: "absolute",
                  left: 245,
                  top: 525 + scaleTilt * 3.5,
                  transform: "translate(-50%, -50%)",
                  textAlign: "center",
                  whiteSpace: "nowrap",
                }}
              >
                <div
                  style={{
                    fontFamily: "BeVietnamProBlack, sans-serif",
                    fontSize: 34,
                    color: "#FFE600",
                    WebkitTextStroke: "8px #05070C",
                    paintOrder: "stroke fill",
                  }}
                >
                  LUẬT SƯ PHÁP LÝ
                </div>
              </div>
              <StickerPop
                src="objects/judge_gavel.png"
                x={245}
                y={685 + scaleTilt * 3.5}
                width={215}
                startFrame={2202}
                baseRotate={-10}
                floatSpeed={0.08}
                floatAmp={6}
                rimColor="rgba(255, 230, 0, 0.9)"
              />

              {/* Right Pan: Real Silicon AI GPU Chip */}
              <div
                style={{
                  position: "absolute",
                  left: 745,
                  top: 525 - scaleTilt * 3.5,
                  transform: "translate(-50%, -50%)",
                  textAlign: "center",
                  whiteSpace: "nowrap",
                }}
              >
                <div
                  style={{
                    fontFamily: "BeVietnamProBlack, sans-serif",
                    fontSize: 34,
                    color: "#00E5FF",
                    WebkitTextStroke: "8px #05070C",
                    paintOrder: "stroke fill",
                  }}
                >
                  ĐIỀU HÀNH CHIP AI
                </div>
              </div>
              <StickerPop
                src="objects/ai_gpu_chip.png"
                x={745}
                y={685 - scaleTilt * 3.5}
                width={235}
                startFrame={2212}
                baseRotate={8}
                floatSpeed={0.08}
                floatAmp={6}
                rimColor="rgba(0, 229, 255, 0.95)"
              />

              {/* Center Conflict Symbol ≠ */}
              <div
                style={{
                  position: "absolute",
                  left: 495,
                  top: 660,
                  transform: "translate(-50%, -50%)",
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 82,
                  color: "#FF3B47",
                  WebkitTextStroke: "10px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 32px rgba(255,59,71,0.95)",
                }}
              >
                ≠
              </div>

              {/* No Successor Warning */}
              {frame >= 2340 && (
                <div
                  style={{
                    position: "absolute",
                    left: 495,
                    top: 1300,
                    transform: "translate(-50%, -50%)",
                    fontFamily: "BeVietnamProBlack, sans-serif",
                    fontSize: 48,
                    color: "#FF3B47",
                    WebkitTextStroke: "9px #05070C",
                    paintOrder: "stroke fill",
                    whiteSpace: "nowrap",
                  }}
                >
                  KHÔNG NGƯỜI KẾ NHIỆM
                </div>
              )}
            </div>

            {/* Beat B (~2380..2572): Shuddering NVIDIA Card + Big Verdict Question */}
            {frame >= 2380 && (
              <>
                <div
                  style={{
                    position: "absolute",
                    left: 495 + nvShudderX,
                    top: 760,
                    width: 630,
                    transform: `translate(-50%, -50%) scale(${nvCardPop}) rotate(${nvShudderRot}deg)`,
                    borderRadius: 28,
                    background: "rgba(255, 255, 255, 0.96)",
                    border: "6px solid #76B900",
                    boxShadow:
                      "0 28px 60px rgba(0,0,0,0.95), 0 0 56px rgba(118, 185, 0, 0.8)",
                    padding: "44px 48px",
                    textAlign: "center",
                  }}
                >
                  <Img
                    src={staticFile("harvested/nvidia_logo_3d.png")}
                    style={{ width: "100%", height: "auto", display: "block" }}
                  />
                </div>

                {/* Climax Zero-Box Verdict Question inside Safe Zone */}
                <div
                  style={{
                    position: "absolute",
                    left: 495,
                    top: 1255,
                    transform: "translate(-50%, -50%)",
                    textAlign: "center",
                    whiteSpace: "nowrap",
                  }}
                >
                  <div
                    style={{
                      fontFamily: "BeVietnamProExtraBold, sans-serif",
                      fontSize: 40,
                      color: "#FFE600",
                      WebkitTextStroke: "8px #05070C",
                      paintOrder: "stroke fill",
                      marginBottom: 8,
                    }}
                  >
                    NGAI VÀNG NVIDIA
                  </div>
                  <div
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 70,
                      color: "#FFFFFF",
                      WebkitTextStroke: "11px #05070C",
                      paintOrder: "stroke fill",
                      lineHeight: 1.08,
                    }}
                  >
                    CHUYỂN GIAO
                  </div>
                  <div
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 92,
                      color: "#FF3B47",
                      WebkitTextStroke: "12px #05070C",
                      paintOrder: "stroke fill",
                      textShadow: "0 0 42px rgba(255, 59, 71, 0.95)",
                      transform: `scale(${interpolate(finalQPop, [0, 1], [1.6, 1.0])})`,
                      lineHeight: 1.08,
                    }}
                  >
                    LỊCH SỬ?
                  </div>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
