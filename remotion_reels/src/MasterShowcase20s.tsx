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
import { StickerPop } from "./components/StickerPop";
import { CoinStream } from "./components/CoinStream";
import { KineticWordCaption, MASTER_20S_PHRASES } from "./components/KineticWordCaption";
import { GeoStrategicMap3D } from "./components/GeoStrategicMap3D";
import { ScaleComparison3D } from "./components/ScaleComparison3D";

export const MasterShowcase20s: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // =========================================================================
  // GLOBAL CAMERA SHAKE ON HEAVY MECHANICAL / GAVEL / SCISSORS IMPACTS
  // =========================================================================
  const impactFrames = [38, 165, 290, 512, 790, 1035, 1212];
  let shakeX = 0;
  let shakeY = 0;
  for (const imp of impactFrames) {
    if (frame >= imp && frame < imp + 14) {
      const dt = frame - imp;
      const decay = Math.exp(-dt * 0.28);
      shakeX += Math.sin(dt * 2.9) * 14 * decay;
      shakeY += Math.cos(dt * 3.3) * 12 * decay;
    }
  }

  // =========================================================================
  // SCENE 1 & 2 CONTINUOUS CAMERA RIG (Frames 0 .. 666)
  // =========================================================================
  const panToFreeze = spring({
    frame: Math.max(0, frame - 142), // 2.37s: "Khi dịch bệnh ập tới..."
    fps,
    config: { damping: 15, stiffness: 80, mass: 0.9 },
  });

  const panToBank = spring({
    frame: Math.max(0, frame - 352), // 5.87s: "Mỗi tháng tiền thuê vẫn phải trả đủ..."
    fps,
    config: { damping: 16, stiffness: 75, mass: 0.95 },
  });

  const camY12 =
    interpolate(panToFreeze, [0, 1], [0, -680]) +
    interpolate(panToBank, [0, 1], [0, -760]);

  const hookCardOpacity = interpolate(panToFreeze, [0, 0.65], [1, 0], {
    extrapolateRight: "clamp",
  });

  const freezeStageOpacity = interpolate(panToBank, [0, 0.65], [1, 0], {
    extrapolateRight: "clamp",
  });

  const scene12ExitOpacity = interpolate(frame, [652, 666], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // =========================================================================
  // SCENE 1A (0.0s - 2.38s): 3D FORENSIC EVIDENCE DOSSIER + REAL VIETJET JET
  // =========================================================================
  const cardPop = spring({
    frame,
    fps,
    config: { damping: 13, stiffness: 130 },
  });
  const highlightSweep = interpolate(frame, [28, 72], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // =========================================================================
  // SCENE 1B (2.38s - 5.88s): VIETJET REAL JET BRAKE + COVID FREEZE + VAULT 0
  // =========================================================================
  const planeFly = spring({
    frame: Math.max(0, frame - 150),
    fps,
    config: { damping: 12, stiffness: 110, mass: 0.8 },
  });
  const planeX = interpolate(planeFly, [0, 1], [-180, 280]);
  const planeY = interpolate(planeFly, [0, 1], [1160, 1235]) + Math.sin(frame * 0.1) * 6;
  const planeRot =
    interpolate(planeFly, [0, 0.75, 1], [12, -10, -3]) + Math.cos(frame * 0.08) * 1.5;

  // =========================================================================
  // SCENE 2 (5.88s - 11.10s): VAULT -> BANK LEASE + SCISSORS CUT CONTRACT
  // =========================================================================
  const scissorsCutProgress = spring({
    frame: Math.max(0, frame - 505), // ~8.42s: "cắt hợp đồng"
    fps,
    config: { damping: 11, stiffness: 190 },
  });
  const isContractSevered = frame >= 514;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#070A12",
        overflow: "hidden",
      }}
    >
      {/* Load Vietnamese TrueType Fonts */}
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

      {/* Deep Radial Studio Lighting */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(circle at 50% 34%, rgba(28, 48, 86, 0.58) 0%, rgba(10, 14, 24, 0.94) 60%, #05070C 100%)",
        }}
      />

      {/* Ambient Parallax Dust Motes */}
      {Array.from({ length: 16 }).map((_, i) => {
        const px = ((i * 173) % 980) + 50;
        const py = ((i * 293) % 1920) - frame * (0.7 + (i % 3) * 0.35);
        const wrappedY = ((py % 1920) + 1920) % 1920;
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
              background:
                i % 3 === 0 ? "rgba(255, 214, 0, 0.26)" : "rgba(120, 180, 255, 0.20)",
              filter: "blur(1px)",
            }}
          />
        );
      })}

      {/* =====================================================================
          TOP FIXED LAYER: ZERO-BOX 2-COLOR KINETIC VIETNAMESE WORD CAPTIONS
         ===================================================================== */}
      <KineticWordCaption phrases={MASTER_20S_PHRASES} />

      {/* =====================================================================
          MAIN CAMERA SHAKE WRAPPER
         ===================================================================== */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate3d(${shakeX}px, ${shakeY}px, 0)`,
        }}
      >
        {/* ===================================================================
            SCENES 1 & 2 WORLD CANVAS (Frames 0 .. 666 | 0.00s .. 11.10s)
           =================================================================== */}
        {frame <= 666 && (
          <div
            style={{
              position: "absolute",
              left: 0,
              top: 0,
              width: 1080,
              height: 3400,
              opacity: scene12ExitOpacity,
              transform: `translate3d(0, ${camY12}px, 0)`,
            }}
          >
            {/* ---------------------------------------------------------------
                STAGE 1A (0.00s - 2.38s): 3D FORENSIC DOSSIER + REAL VIETJET JET
               --------------------------------------------------------------- */}
            <div style={{ opacity: hookCardOpacity }}>
              {/* 3D Tilted Legal Case File Card */}
              <div
                style={{
                  position: "absolute",
                  left: 540,
                  top: 760,
                  width: 820,
                  perspective: 1100,
                  transform: `translate(-50%, -50%) scale(${cardPop})`,
                }}
              >
                <div
                  style={{
                    transform: "rotateX(10deg) rotateY(-8deg) rotateZ(-2deg)",
                    borderRadius: 26,
                    overflow: "hidden",
                    background: "rgba(15, 23, 42, 0.92)",
                    border: "3px solid rgba(255, 230, 0, 0.78)",
                    boxShadow:
                      "0 35px 70px rgba(0,0,0,0.92), 0 0 40px rgba(255, 230, 0, 0.25)",
                    padding: 24,
                  }}
                >
                  <Img
                    src={staticFile("harvested/london_high_court_real.png")}
                    style={{
                      width: "100%",
                      height: 360,
                      objectFit: "cover",
                      borderRadius: 16,
                    }}
                  />
                  {/* Highlighter Sweep over 250M $ Claim */}
                  <div
                    style={{
                      position: "relative",
                      marginTop: 22,
                      padding: "12px 20px",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "space-between",
                    }}
                  >
                    <div
                      style={{
                        position: "absolute",
                        left: 0,
                        top: 0,
                        bottom: 0,
                        width: `${highlightSweep * 100}%`,
                        background:
                          "linear-gradient(90deg, rgba(255, 230, 0, 0.35) 0%, rgba(255, 59, 71, 0.40) 100%)",
                        borderRadius: 12,
                      }}
                    />
                    <span
                      style={{
                        position: "relative",
                        fontFamily: "BeVietnamProBlack, sans-serif",
                        fontSize: 36,
                        color: "#FFFFFF",
                        WebkitTextStroke: "6px #05070C",
                        paintOrder: "stroke fill",
                      }}
                    >
                      HỒ SƠ KIỆN:
                    </span>
                    <span
                      style={{
                        position: "relative",
                        fontFamily: "BeVietnamProBlack, sans-serif",
                        fontSize: 58,
                        color: "#FFE600",
                        WebkitTextStroke: "9px #05070C",
                        paintOrder: "stroke fill",
                      }}
                    >
                      250 TRIỆU USD
                    </span>
                  </div>
                </div>
              </div>

              {/* Real Scraped & AI-Cutout VietJet Air Airbus A321 Popping Out in Front */}
              <StickerPop
                src="demo_archive/vietjet_real_aircraft.png"
                x={540}
                y={1240}
                width={740}
                startFrame={14}
                baseRotate={-6}
                floatSpeed={0.09}
                floatAmp={12}
                rimColor="rgba(255, 255, 255, 0.95)"
                shudderAtFrame={38}
              />
            </div>

            {/* ---------------------------------------------------------------
                STAGE 1B (2.38s - 5.88s): VIETJET JET LOCKDOWN + VAULT 0 ĐỒNG
               --------------------------------------------------------------- */}
            <div style={{ opacity: freezeStageOpacity }}>
              {/* Real VietJet Air Airbus A321 flying in and braking */}
              {frame >= 150 && (
                <div
                  style={{
                    position: "absolute",
                    left: planeX,
                    top: planeY,
                    width: 460,
                    transform: `translate(-50%, -50%) rotate(${planeRot}deg)`,
                  }}
                >
                  <Img
                    src={staticFile("demo_archive/vietjet_real_aircraft.png")}
                    style={{
                      width: "100%",
                      height: "auto",
                      filter:
                        "drop-shadow(0px 0px 5px rgba(255,255,255,0.92)) drop-shadow(0px 22px 30px rgba(0,0,0,0.88))",
                    }}
                  />
                </div>
              )}

              {/* 3D Road Barrier + Padlock + Red Virus */}
              <StickerPop
                src="objects/barrier.png"
                x={565}
                y={1280}
                width={220}
                startFrame={156}
                baseRotate={-14}
                floatSpeed={0.07}
                floatAmp={6}
                rimColor="rgba(255, 230, 0, 0.9)"
              />
              <StickerPop
                src="objects/padlock.png"
                x={575}
                y={1135}
                width={115}
                startFrame={168}
                floatSpeed={0.09}
                floatAmp={7}
                rimColor="rgba(255, 215, 0, 0.95)"
              />
              <StickerPop
                src="objects/virus.png"
                x={810}
                y={1165}
                width={205}
                startFrame={148}
                floatSpeed={0.11}
                floatAmp={11}
                rotateAmp={8}
                rimColor="rgba(255, 70, 90, 0.95)"
              />

              {/* Blocked CoinStream curving towards Steel Vault */}
              <CoinStream
                p0={{ x: 460, y: 1420 }}
                p1={{ x: 640, y: 1620 }}
                p2={{ x: 700, y: 1850 }}
                startFrame={240}
                endFrame={355}
                coinCount={5}
                blockedAtT={0.55}
                dotColor="#FF3B47"
              />

              {/* Steel Vault (DOANH THU 0 ĐỒNG) */}
              <StickerPop
                src="objects/vault.png"
                x={710}
                y={1920}
                width={350}
                startFrame={265}
                floatSpeed={0.06}
                floatAmp={8}
                rimColor="rgba(160, 230, 255, 0.9)"
                shudderAtFrame={290}
              />

              {frame >= 275 && (
                <div
                  style={{
                    position: "absolute",
                    left: 310,
                    top: 1930,
                    transform: "translate(-50%, -50%)",
                    textAlign: "center",
                    whiteSpace: "nowrap",
                  }}
                >
                  <div
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 44,
                      color: "#FFFFFF",
                      WebkitTextStroke: "9px #05070C",
                      paintOrder: "stroke fill",
                    }}
                  >
                    DOANH THU
                  </div>
                  <div
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 56,
                      color: "#FFE600",
                      WebkitTextStroke: "9px #05070C",
                      paintOrder: "stroke fill",
                    }}
                  >
                    0 ĐỒNG
                  </div>
                </div>
              )}
            </div>

            {/* ---------------------------------------------------------------
                STAGE 2 (5.88s - 11.10s): BANK LEASE + SCISSORS CUTTING CONTRACT
               --------------------------------------------------------------- */}
            {/* Vault at top of Stage 2 */}
            <StickerPop
              src="objects/vault.png"
              x={730}
              y={1950}
              width={320}
              startFrame={345}
              floatSpeed={0.06}
              floatAmp={7}
              rimColor="rgba(160, 230, 255, 0.9)"
            />

            {/* Active Coin & Dollar Stream pouring from Vault to Classical Bank */}
            <CoinStream
              p0={{ x: 590, y: 2050 }}
              p1={{ x: 440, y: 2260 }}
              p2={{ x: 280, y: 2440 }}
              startFrame={360}
              endFrame={510}
              coinCount={6}
              dotColor="#FFE600"
              useDollarNotes={true}
            />

            {/* Classical Stone Bank (NGÂN HÀNG CHO THUÊ) */}
            <StickerPop
              src="objects/bank.png"
              x={270}
              y={2540}
              width={330}
              startFrame={356}
              floatSpeed={0.065}
              floatAmp={7}
              rimColor="rgba(255, 230, 140, 0.92)"
            />

            {frame >= 365 && (
              <div
                style={{
                  position: "absolute",
                  left: 270,
                  top: 2755,
                  transform: "translate(-50%, -50%)",
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 40,
                  color: "#FFFFFF",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                  whiteSpace: "nowrap",
                }}
              >
                NGÂN HÀNG
              </div>
            )}

            {/* Contract & Scissors Severing Animation (8.0s - 11.1s | Frames 480 - 666) */}
            {frame >= 480 && (
              <>
                {/* Dotted Debt Transfer Link from Bank (270, 2540) to Foreign Fund (800, 2940) */}
                <CoinStream
                  p0={{ x: 390, y: 2620 }}
                  p1={{ x: 580, y: 2780 }}
                  p2={{ x: 780, y: 2920 }}
                  startFrame={525}
                  endFrame={666}
                  coinCount={6}
                  dotColor="#FF3B47"
                  useDollarNotes={true}
                />

                {/* 3D Lease Contract in the center being cut */}
                <StickerPop
                  src="objects/contract.png"
                  x={610}
                  y={2520}
                  width={230}
                  startFrame={482}
                  baseRotate={isContractSevered ? 16 : -6}
                  floatSpeed={0.08}
                  floatAmp={7}
                  rimColor={
                    isContractSevered
                      ? "rgba(255, 59, 71, 0.95)"
                      : "rgba(255, 230, 0, 0.9)"
                  }
                  shudderAtFrame={512}
                />

                {/* 3D Scissors lunging in to sever the Lease Contract */}
                <div
                  style={{
                    position: "absolute",
                    left: interpolate(scissorsCutProgress, [0, 1], [960, 625]),
                    top: interpolate(scissorsCutProgress, [0, 1], [2320, 2495]),
                    width: 225,
                    transform: `translate(-50%, -50%) rotate(${interpolate(
                      scissorsCutProgress,
                      [0, 1],
                      [-45, -12]
                    )}deg) scale(${interpolate(scissorsCutProgress, [0, 0.8, 1], [0.5, 1.15, 1.0])})`,
                    filter:
                      "drop-shadow(0 0 22px rgba(255, 59, 71, 0.95)) drop-shadow(0 18px 28px rgba(0,0,0,0.9))",
                  }}
                >
                  <Img
                    src={staticFile("objects/scissors.png")}
                    style={{ width: "100%", height: "auto" }}
                  />
                </div>

                {/* Foreign Debt Fund (QUỸ NGOẠI FITZWALTER) receiving the debt */}
                {frame >= 545 && (
                  <div
                    style={{
                      position: "absolute",
                      left: 760,
                      top: 2960,
                      transform: `translate(-50%, -50%) scale(${spring({
                        frame: frame - 545,
                        fps,
                        config: { damping: 11, stiffness: 200 },
                      })})`,
                      textAlign: "center",
                      whiteSpace: "nowrap",
                    }}
                  >
                    <div
                      style={{
                        fontFamily: "BeVietnamProExtraBold, sans-serif",
                        fontSize: 28,
                        color: "#FFFFFF",
                        WebkitTextStroke: "6px #05070C",
                        paintOrder: "stroke fill",
                      }}
                    >
                      BÁN KHOẢN NỢ CHO
                    </div>
                    <div
                      style={{
                        fontFamily: "BeVietnamProBlack, sans-serif",
                        fontSize: 54,
                        color: "#FF3B47",
                        WebkitTextStroke: "10px #05070C",
                        paintOrder: "stroke fill",
                        textShadow: "0 0 28px rgba(255, 59, 71, 0.9)",
                      }}
                    >
                      QUỸ NGOẠI ANH
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* ===================================================================
            SCENE 3 (Frames 666 .. 939 | 11.10s .. 15.65s):
            3D GEO-STRATEGIC MAP (VIETNAM -> LONDON) + REAL LONDON HIGH COURT
           =================================================================== */}
        <GeoStrategicMap3D
          startFrame={666}
          endFrame={939}
          originLabel="VIỆT NAM"
          targetLabel="LUÂN ĐÔN (ANH)"
          evidenceImageSrc="demo_archive/london_high_court_real.png"
          evidenceTitle="TÒA ÁN TỐI CAO LUÂN ĐÔN"
          leftFloatingIconSrc="objects/contract.png"
          rightFloatingIconSrc="objects/gavel.png"
        />

        {/* ===================================================================
            SCENE 4 (Frames 939 .. 1344 | 15.65s .. 22.40s):
            ABSTRACT-TO-PHYSICAL 3D SCALE COMPARISON (4 JETS vs 250M $ TOWER)
           =================================================================== */}
        <ScaleComparison3D
          startFrame={939}
          endFrame={1344}
          leftItemSrc="demo_archive/vietjet_real_aircraft.png"
          leftItemCount={4}
          leftLabel="4 TÀU BAY THUÊ"
          rightPrimaryStackSrc="objects/dollar.png"
          rightSecondaryStackSrc="objects/coin.png"
          rightTopTitle="ĐÒI BỒI THƯỜNG"
          rightStartNumber={12}
          rightTargetNumber={250}
          rightUnitSuffix="M $"
          rightLabel="VỤ KIỆN QUỸ NGOẠI"
          stampText="ĐÒN BẨY TÀI CHÍNH QUỐC TẾ"
        />
      </div>
    </AbsoluteFill>
  );
};
