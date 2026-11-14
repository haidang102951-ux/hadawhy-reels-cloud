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
import { KineticWordCaption } from "./components/KineticWordCaption";

export const PilotCashFlowScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // =========================================================================
  // 1. CONTINUOUS CAMERA RIG (Strict Spatial Isolation: Zero Caption Overlap)
  // =========================================================================
  const panToVault = spring({
    frame: Math.max(0, frame - 168), // ~2.80s: "doanh thu không về két"
    fps,
    config: { damping: 15, stiffness: 75, mass: 0.9 },
  });

  const panToBank = spring({
    frame: Math.max(0, frame - 252), // ~4.20s: "nhưng mỗi tháng, tiền thuê..."
    fps,
    config: { damping: 16, stiffness: 70, mass: 0.95 },
  });

  // Camera pans down cleanly so upper stages exit above the caption zone or dim out
  const camY =
    interpolate(panToVault, [0, 1], [0, -540]) +
    interpolate(panToBank, [0, 1], [0, -620]);

  // Fade out Stage 1 when camera pans down to Stage 2 & 3 so it NEVER collides with top captions
  const stage1Opacity = interpolate(panToVault, [0, 0.7], [1, 0], {
    extrapolateRight: "clamp",
  });

  // Continuous slow push-in + zoom out on wide payoff
  const baseZoom = interpolate(frame, [0, 168, 260, 444], [1.03, 1.08, 0.96, 1.02], {
    extrapolateRight: "clamp",
  });

  // Camera impact shake on heavy mechanical hits
  const impactFrames = [12, 66, 180, 264];
  let shakeX = 0;
  let shakeY = 0;
  for (const imp of impactFrames) {
    if (frame >= imp && frame < imp + 14) {
      const dt = frame - imp;
      const decay = Math.exp(-dt * 0.28);
      shakeX += Math.sin(dt * 2.8) * 14 * decay;
      shakeY += Math.cos(dt * 3.2) * 12 * decay;
    }
  }

  // =========================================================================
  // 2. AIRLINER FLIGHT & HARD BRAKE CHOREOGRAPHY
  // =========================================================================
  const planeFly = spring({
    frame: Math.max(0, frame - 26),
    fps,
    config: { damping: 12, stiffness: 110, mass: 0.8 },
  });
  const planeX = interpolate(planeFly, [0, 1], [-180, 275]);
  const planeY = interpolate(planeFly, [0, 1], [590, 685]) + Math.sin(frame * 0.1) * 7;
  const planeRot =
    interpolate(planeFly, [0, 0.75, 1], [14, -12, -3]) + Math.cos(frame * 0.08) * 1.8;

  // =========================================================================
  // 3. MONTHS 1 - 2 - 3 TIMELINE & RED FREEZE LINE
  // =========================================================================
  const lineProgress = spring({
    frame: Math.max(0, frame - 54),
    fps,
    config: { damping: 18, stiffness: 80 },
  });

  // Outflow counter when paying bank lease every month
  const outflowProgress = interpolate(frame, [285, 425], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const outflowMillions = Math.round(outflowProgress * 250);

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
      {Array.from({ length: 18 }).map((_, i) => {
        const px = ((i * 173) % 980) + 50;
        const py =
          ((i * 293) % 2200) + 100 + camY * 0.35 - frame * (0.6 + (i % 3) * 0.3);
        const wrappedY = ((py % 2000) + 2000) % 2000;
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
                i % 3 === 0 ? "rgba(255, 214, 0, 0.28)" : "rgba(120, 180, 255, 0.22)",
              filter: "blur(1px)",
            }}
          />
        );
      })}

      {/* =====================================================================
          TOP FIXED LAYER: ZERO-BOX KINETIC VIETNAMESE WORD CAPTIONS
         ===================================================================== */}
      <KineticWordCaption />

      {/* =====================================================================
          WORLD CANVAS (Panned & Zoomed by CameraRig at 60fps)
         ===================================================================== */}
      <div
        style={{
          position: "absolute",
          left: 0,
          top: 0,
          width: 1080,
          height: 3000,
          transformOrigin: "540px 960px",
          transform: `translate3d(${shakeX}px, ${camY + shakeY}px, 0) scale(${baseZoom})`,
        }}
      >
        {/* -----------------------------------------------------------------
            STAGE 1 (TOP): AIRLINER + BARRIER + RED COVID VIRUS + MONTHS 1-2-3
           ----------------------------------------------------------------- */}
        <div style={{ opacity: stage1Opacity }}>
          {frame >= 4 && (
            <div
              style={{
                position: "absolute",
                left: 785,
                top: 615,
                width: 240,
                height: 240,
                borderRadius: "50%",
                border: "4px solid rgba(255, 45, 70, 0.55)",
                transform: `translate(-50%, -50%) scale(${1 + ((frame * 0.03) % 0.85)})`,
                opacity: 1 - ((frame * 0.03) % 0.85),
              }}
            />
          )}

          {/* 3D Red Covid Virus */}
          <StickerPop
            src="objects/virus.png"
            x={785}
            y={615}
            width={215}
            startFrame={4}
            floatSpeed={0.11}
            floatAmp={12}
            rotateAmp={8}
            rimColor="rgba(255, 70, 90, 0.95)"
          />

          {/* Real Scraped & AI-Cutout VietJet Air Airbus A321 flying in and braking */}
          {frame >= 26 && (
            <div
              style={{
                position: "absolute",
                left: planeX,
                top: planeY,
                width: 455,
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

          {/* 3D Road Barrier slamming down in front of the airliner */}
          <StickerPop
            src="objects/barrier.png"
            x={555}
            y={735}
            width={225}
            startFrame={12}
            baseRotate={-14}
            floatSpeed={0.07}
            floatAmp={6}
            rimColor="rgba(255, 230, 0, 0.9)"
            shudderAtFrame={58}
          />

          {/* 3D Padlock snapping onto the blocked flight path */}
          <StickerPop
            src="objects/padlock.png"
            x={565}
            y={585}
            width={118}
            startFrame={66}
            floatSpeed={0.09}
            floatAmp={7}
            rimColor="rgba(255, 215, 0, 0.95)"
          />

          {/* ZERO-BOX Floating Title: CHUYẾN BAY */}
          {frame >= 40 && (
            <div
              style={{
                position: "absolute",
                left: 265,
                top: 855,
                transform: `translate(-50%, -50%) scale(${spring({
                  frame: frame - 40,
                  fps,
                  config: { damping: 12, stiffness: 200 },
                })})`,
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 46,
                color: "#FFFFFF",
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 8px 18px rgba(0,0,0,0.9)",
                letterSpacing: "0.02em",
                whiteSpace: "nowrap",
              }}
            >
              CHUYẾN BAY
            </div>
          )}

          {/* Months 1 - 2 - 3 Freeze Counter */}
          {[1, 2, 3].map((m, idx) => {
            const mStart = 54 + idx * 14;
            if (frame < mStart) return null;
            const mPop = spring({
              frame: frame - mStart,
              fps,
              config: { damping: 10, stiffness: 220 },
            });
            const mx = 140 + idx * 180;
            return (
              <div
                key={`month-${m}`}
                style={{
                  position: "absolute",
                  left: mx,
                  top: 985,
                  transform: `translate(-50%, -50%) scale(${mPop})`,
                  textAlign: "center",
                }}
              >
                <div
                  style={{
                    fontFamily: "BeVietnamProExtraBold, sans-serif",
                    fontSize: 26,
                    color: "#CBD5E1",
                    WebkitTextStroke: "5px #05070C",
                    paintOrder: "stroke fill",
                  }}
                >
                  THÁNG
                </div>
                <div
                  style={{
                    fontFamily: "BeVietnamProBlack, sans-serif",
                    fontSize: 64,
                    color: "#FF3B47",
                    lineHeight: 1.0,
                    WebkitTextStroke: "8px #05070C",
                    paintOrder: "stroke fill",
                    textShadow: "0 0 22px rgba(255, 59, 71, 0.75)",
                  }}
                >
                  {m}
                </div>
              </div>
            );
          })}

          {/* Glowing Red Freeze Line under Months 1-2-3 */}
          {frame >= 54 && (
            <div
              style={{
                position: "absolute",
                left: 80,
                top: 1068,
                width: 470 * lineProgress,
                height: 10,
                borderRadius: 6,
                background: "linear-gradient(90deg, #FF2A40 0%, #FF6B00 100%)",
                boxShadow: "0 0 20px rgba(255, 42, 64, 0.9)",
              }}
            />
          )}
        </div>

        {/* -----------------------------------------------------------------
            STAGE 2 (MIDDLE): BLOCKED STREAM -> STEEL VAULT (DOANH THU = 0)
           ----------------------------------------------------------------- */}

        {/* Blocked CoinStream curving towards Vault */}
        <CoinStream
          p0={{ x: 560, y: 980 }}
          p1={{ x: 740, y: 1210 }}
          p2={{ x: 700, y: 1470 }}
          startFrame={118}
          endFrame={275}
          coinCount={5}
          blockedAtT={0.55}
          dotColor="#FF3B47"
        />

        {/* Heavy 3D Steel Vault (DOANH THU) */}
        <StickerPop
          src="objects/vault.png"
          x={700}
          y={1660}
          width={380}
          startFrame={176}
          floatSpeed={0.06}
          floatAmp={8}
          rotateAmp={1.2}
          rimColor="rgba(160, 230, 255, 0.9)"
          shudderAtFrame={210}
        />

        {/* ZERO-BOX Floating Title below Vault: DOANH THU: 0 ĐỒNG */}
        {frame >= 186 && (
          <div
            style={{
              position: "absolute",
              left: 700,
              top: 1905,
              transform: `translate(-50%, -50%) scale(${spring({
                frame: frame - 186,
                fps,
                config: { damping: 11, stiffness: 210 },
              })})`,
              textAlign: "center",
              whiteSpace: "nowrap",
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 46,
                color: "#FFFFFF",
                WebkitTextStroke: "9px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 8px 20px rgba(0,0,0,0.95)",
              }}
            >
              DOANH THU
            </div>
            {frame >= 206 && (
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 52,
                  color: "#FF3B47",
                  WebkitTextStroke: "9px #05070C",
                  paintOrder: "stroke fill",
                  textShadow: "0 0 25px rgba(255,59,71,0.85)",
                  marginTop: -4,
                }}
              >
                0 ĐỒNG
              </div>
            )}
          </div>
        )}

        {/* -----------------------------------------------------------------
            STAGE 3 (BOTTOM): CONTINUOUS LEASE OUTFLOW -> CLASSICAL BANK
           ----------------------------------------------------------------- */}

        {/* Active Gold Coin & Dollar Stream pouring from Vault to Bank */}
        <CoinStream
          p0={{ x: 540, y: 1810 }}
          p1={{ x: 430, y: 2070 }}
          p2={{ x: 310, y: 2260 }}
          startFrame={276}
          coinCount={7}
          dotColor="#FFE600"
          useDollarNotes={true}
        />

        {/* 3D Classical Stone Bank (TRẢ TIỀN THUÊ) */}
        <StickerPop
          src="objects/bank.png"
          x={285}
          y={2360}
          width={380}
          startFrame={258}
          floatSpeed={0.065}
          floatAmp={7}
          rotateAmp={1.0}
          rimColor="rgba(255, 230, 140, 0.92)"
          shudderAtFrame={295}
        />

        {/* ZERO-BOX Floating Title below Bank: TRẢ TIỀN THUÊ */}
        {frame >= 268 && (
          <div
            style={{
              position: "absolute",
              left: 285,
              top: 2605,
              transform: `translate(-50%, -50%) scale(${spring({
                frame: frame - 268,
                fps,
                config: { damping: 11, stiffness: 205 },
              })})`,
              textAlign: "center",
              whiteSpace: "nowrap",
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 46,
                color: "#FFE600",
                WebkitTextStroke: "9px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 8px 22px rgba(0,0,0,0.95)",
              }}
            >
              TRẢ TIỀN THUÊ
            </div>
          </div>
        )}

        {/* Dynamic Odometer Outflow Counter next to Bank (strictly single-line nowrap) */}
        {frame >= 285 && (
          <div
            style={{
              position: "absolute",
              left: 735,
              top: 2365,
              transform: `translate(-50%, -50%) scale(${spring({
                frame: frame - 285,
                fps,
                config: { damping: 12, stiffness: 190 },
              })})`,
              textAlign: "center",
              whiteSpace: "nowrap",
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProExtraBold, sans-serif",
                fontSize: 30,
                color: "#CBD5E1",
                WebkitTextStroke: "6px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              TIỀN THUÊ CỘNG DỒN
            </div>
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 78,
                color: "#FF3B47",
                WebkitTextStroke: "11px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 0 34px rgba(255, 59, 71, 0.9)",
                lineHeight: 1.08,
                whiteSpace: "nowrap",
              }}
            >
              -{outflowMillions}M $
            </div>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
