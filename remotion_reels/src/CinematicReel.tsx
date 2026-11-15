import React from "react";
import {
  AbsoluteFill,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { UniversalScenePlan, UniversalSceneSpec } from "./HaDaWhyUniversal9x16";
import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16";
import { KineticWordCaption } from "./components/KineticWordCaption";

type ExtendedScene = Omit<UniversalSceneSpec, "layout"> & {
  layout: string;
  asset?: string;
  sourceTag?: string;
  secondaryAsset?: string;
  timelineNodes?: string[];
};

interface Palette {
  bg: string;
  bg2: string;
  accent: string;
  accent2: string;
  stamp: string;
  highlight: string;
}

const PALETTES: Record<string, Palette> = {
  noir_dossier: {
    bg: "#090A0F",
    bg2: "#161218",
    accent: "#F59E0B",
    accent2: "#EF4444",
    stamp: "#DC2626",
    highlight: "rgba(245, 158, 11, 0.36)",
  },
  finance_vox: {
    bg: "#0A0F1A",
    bg2: "#121C2D",
    accent: "#38BDF8",
    accent2: "#F59E0B",
    stamp: "#E11D48",
    highlight: "rgba(56, 189, 248, 0.32)",
  },
  tech_cyber: {
    bg: "#060B14",
    bg2: "#0D1B2A",
    accent: "#22D3EE",
    accent2: "#A855F7",
    stamp: "#F43F5E",
    highlight: "rgba(34, 211, 238, 0.32)",
  },
  retail_warm: {
    bg: "#120D0A",
    bg2: "#221712",
    accent: "#FB923C",
    accent2: "#FACC15",
    stamp: "#DC2626",
    highlight: "rgba(251, 146, 60, 0.34)",
  },
};

function getPalette(theme?: string): Palette {
  return PALETTES[theme || "noir_dossier"] || PALETTES.noir_dossier;
}

function fitFontSize(text: string, base: number, maxChars: number, minSize: number): number {
  const len = (text || "").trim().length;
  if (len <= maxChars) return base;
  return Math.max(minSize, Math.round((base * maxChars) / len));
}

function normalizeAsset(path?: string): string {
  if (!path) return "";
  return path.startsWith("/") ? path.slice(1) : path;
}

function pickPrimaryAsset(scene: ExtendedScene): string {
  return (
    scene.primaryAsset ||
    scene.asset ||
    scene.centerAsset ||
    scene.leftAsset ||
    scene.bottomAsset ||
    scene.topLeftAsset ||
    ""
  );
}

function pickSecondaryAsset(scene: ExtendedScene): string {
  return scene.secondaryAsset || scene.rightAsset || scene.topRightAsset || "";
}

function formatStat(scene: ExtendedScene): string {
  if (scene.statNumber === undefined || scene.statNumber === null) return "";
  return `${scene.statNumber}${scene.statSuffix || ""}`;
}

const SafePhoto: React.FC<{
  src?: string;
  style?: React.CSSProperties;
}> = ({ src, style }) => {
  const clean = normalizeAsset(src);
  if (!clean) return null;
  return <Img src={staticFile(clean)} style={style} />;
};

const StudioBackdrop: React.FC<{ palette: Palette; frame: number }> = ({ palette, frame }) => {
  const pulse = 0.85 + Math.sin(frame * 0.04) * 0.12;
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 50% 38%, ${palette.bg2} 0%, ${palette.bg} 78%)`,
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)",
          backgroundSize: "64px 64px",
          opacity: 0.55,
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "18%",
          left: "15%",
          width: "70%",
          height: "42%",
          borderRadius: "50%",
          background: `radial-gradient(circle, ${palette.accent}24 0%, transparent 70%)`,
          transform: `scale(${pulse})`,
          filter: "blur(40px)",
        }}
      />
    </AbsoluteFill>
  );
};

/* 1. DOSSIER STAMP: 3D tilted evidence card + highlighter sweep + red forensic stamp slam */
const SceneDossierStamp: React.FC<{
  scene: ExtendedScene;
  palette: Palette;
  f: number;
  fps: number;
}> = ({ scene, palette, f, fps }) => {
  const cardIn = spring({ frame: f, fps, config: { damping: 14, stiffness: 120 } });
  const zoom = interpolate(f, [0, 180], [1.0, 1.09], { extrapolateRight: "clamp" });
  const rotY = interpolate(f, [0, 180], [-4, 3], { extrapolateRight: "clamp" });
  const highlightW = interpolate(f, [14, 38], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const stampFrame = Math.max(0, f - 20);
  const stampSpring = spring({ frame: stampFrame, fps, config: { damping: 10, stiffness: 260 } });
  const stampScale = f < 20 ? 3.2 : interpolate(stampSpring, [0, 1], [2.4, 1.0]);
  const stampOpacity = f < 20 ? 0 : interpolate(stampSpring, [0, 0.3, 1], [0, 1, 0.94]);

  const stampText = String(scene.stampText || formatStat(scene) || "HỒ SƠ MẬT").toUpperCase();
  const headline = scene.heroText || scene.subNote || "";
  const sourceTag = String(scene.sourceTag || scene.eyebrow || scene.infoTags?.[0] || "TÀI LIỆU ĐIỀU TRA").toUpperCase();

  return (
    <AbsoluteFill>
      <StudioBackdrop palette={palette} frame={f} />

      <div
        style={{
          position: "absolute",
          top: 230,
          left: 72,
          right: 72,
          height: 820,
          transform: `perspective(1200px) rotateX(4deg) rotateY(${rotY}deg) scale(${0.92 + 0.08 * cardIn})`,
          transformOrigin: "center center",
          borderRadius: 24,
          overflow: "hidden",
          border: "2px solid rgba(255,255,255,0.16)",
          boxShadow: "0 36px 90px rgba(0,0,0,0.75)",
          backgroundColor: "#11131A",
        }}
      >
        <SafePhoto
          src={pickPrimaryAsset(scene)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${zoom})`,
            filter: "contrast(1.1) saturate(0.92)",
          }}
        />
        <div
          style={{
            position: "absolute",
            inset: 0,
            background:
              "linear-gradient(180deg, rgba(0,0,0,0.45) 0%, rgba(0,0,0,0.08) 38%, rgba(0,0,0,0.78) 100%)",
          }}
        />
        <div
          style={{
            position: "absolute",
            top: 28,
            left: 28,
            padding: "8px 18px",
            borderRadius: 8,
            backgroundColor: palette.accent,
            color: "#090A0F",
            fontFamily: "Inter, sans-serif",
            fontWeight: 900,
            fontSize: 24,
            letterSpacing: 1.5,
          }}
        >
          {sourceTag}
        </div>

        {headline ? (
          <div style={{ position: "absolute", bottom: 34, left: 32, right: 32 }}>
            <div
              style={{
                position: "relative",
                display: "inline-block",
                fontFamily: "Inter, sans-serif",
                fontWeight: 900,
                fontSize: fitFontSize(headline, 48, 22, 32),
                lineHeight: 1.18,
                color: "#FFFFFF",
                textShadow: "0 4px 16px rgba(0,0,0,0.9)",
              }}
            >
              <span
                style={{
                  position: "absolute",
                  left: -6,
                  bottom: 2,
                  height: "42%",
                  width: `${highlightW}%`,
                  backgroundColor: palette.highlight,
                  zIndex: 0,
                }}
              />
              <span style={{ position: "relative", zIndex: 1 }}>{headline}</span>
            </div>
          </div>
        ) : null}

        <div
          style={{
            position: "absolute",
            top: "32%",
            right: 42,
            padding: "14px 28px",
            border: `7px solid ${palette.stamp}`,
            borderRadius: 14,
            color: palette.stamp,
            fontFamily: "Inter, sans-serif",
            fontWeight: 900,
            fontSize: fitFontSize(stampText, 50, 12, 28),
            letterSpacing: 3,
            backgroundColor: "rgba(15, 10, 12, 0.78)",
            transform: `rotate(-11deg) scale(${stampScale})`,
            opacity: stampOpacity,
            boxShadow: `0 0 36px ${palette.stamp}66`,
          }}
        >
          {stampText}
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* 2. CUTOUT AR STAGE: 3D subject stage + floor shadow + AR callout line + telemetry badge */
const SceneCutoutARStage: React.FC<{
  scene: ExtendedScene;
  palette: Palette;
  f: number;
  fps: number;
}> = ({ scene, palette, f, fps }) => {
  const pop = spring({ frame: f, fps, config: { damping: 12, stiffness: 135 } });
  const floatY = Math.sin(f * 0.055) * 10;
  const lineProg = interpolate(f, [15, 36], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const headline = scene.heroText || "";
  const callout = formatStat(scene) || scene.infoTags?.[0] || scene.eyebrow || "";

  return (
    <AbsoluteFill>
      <StudioBackdrop palette={palette} frame={f} />

      <div
        style={{
          position: "absolute",
          top: 930,
          left: 140,
          right: 140,
          height: 90,
          borderRadius: "50%",
          background: `radial-gradient(ellipse at center, rgba(0,0,0,0.88) 0%, ${palette.accent}22 52%, transparent 74%)`,
          transform: `scale(${0.8 + 0.2 * pop})`,
        }}
      />

      {headline ? (
        <div
          style={{
            position: "absolute",
            top: 210,
            left: 64,
            right: 64,
            textAlign: "center",
            fontFamily: "Inter, sans-serif",
            fontWeight: 900,
            fontSize: fitFontSize(headline, 54, 22, 34),
            color: "#FFFFFF",
            textTransform: "uppercase",
            letterSpacing: 1,
            textShadow: `0 4px 24px rgba(0,0,0,0.85), 0 0 28px ${palette.accent}44`,
            opacity: pop,
            transform: `translateY(${(1 - pop) * 24}px)`,
          }}
        >
          {headline}
        </div>
      ) : null}

      <div
        style={{
          position: "absolute",
          top: 320,
          left: 110,
          right: 110,
          height: 620,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          transform: `translateY(${floatY}px) scale(${0.86 + 0.14 * pop})`,
        }}
      >
        <SafePhoto
          src={pickPrimaryAsset(scene)}
          style={{
            maxWidth: "100%",
            maxHeight: "100%",
            objectFit: "contain",
            borderRadius: 22,
            filter: `drop-shadow(0 0 24px ${palette.accent}55) drop-shadow(0 28px 40px rgba(0,0,0,0.85))`,
          }}
        />
      </div>

      {callout ? (
        <>
          <svg
            width="1080"
            height="1920"
            style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
          >
            <circle cx="540" cy="600" r={8 * lineProg} fill={palette.accent} />
            <line
              x1="540"
              y1="600"
              x2={540 + 180 * lineProg}
              y2={600 - 150 * lineProg}
              stroke={palette.accent}
              strokeWidth="4"
            />
          </svg>
          <div
            style={{
              position: "absolute",
              top: 390,
              right: 76,
              padding: "12px 22px",
              borderRadius: 12,
              backgroundColor: "rgba(10, 14, 22, 0.86)",
              border: `2px solid ${palette.accent}`,
              color: palette.accent,
              fontFamily: "Inter, sans-serif",
              fontWeight: 900,
              fontSize: fitFontSize(callout, 38, 14, 24),
              opacity: lineProg,
              boxShadow: "0 12px 30px rgba(0,0,0,0.6)",
            }}
          >
            {callout}
          </div>
        </>
      ) : null}
    </AbsoluteFill>
  );
};

/* 3. SPLIT VERSUS: Dual comparison panels with glowing laser divider + center badge */
const SceneSplitVersus: React.FC<{
  scene: ExtendedScene;
  palette: Palette;
  f: number;
  fps: number;
}> = ({ scene, palette, f, fps }) => {
  const slide = spring({ frame: f, fps, config: { damping: 14, stiffness: 125 } });
  const topY = interpolate(slide, [0, 1], [-80, 0]);
  const botY = interpolate(slide, [0, 1], [80, 0]);
  const badge = String(formatStat(scene) || scene.stampText || "VS").toUpperCase();
  const labelTop = scene.leftLabel || scene.heroText || "";
  const labelBot = scene.rightLabel || scene.infoTags?.[0] || scene.subNote || "";
  const second = pickSecondaryAsset(scene);

  return (
    <AbsoluteFill style={{ backgroundColor: palette.bg }}>
      <div
        style={{
          position: "absolute",
          top: 165,
          left: 48,
          right: 48,
          height: 440,
          borderRadius: 22,
          overflow: "hidden",
          border: "2px solid rgba(255,255,255,0.16)",
          transform: `translateY(${topY}px)`,
        }}
      >
        <SafePhoto
          src={pickPrimaryAsset(scene)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${interpolate(f, [0, 180], [1.02, 1.1])})`,
          }}
        />
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(180deg, transparent 45%, rgba(0,0,0,0.82) 100%)",
          }}
        />
        {labelTop ? (
          <div
            style={{
              position: "absolute",
              bottom: 22,
              left: 26,
              right: 26,
              fontFamily: "Inter, sans-serif",
              fontWeight: 900,
              fontSize: fitFontSize(labelTop, 40, 22, 28),
              color: "#FFFFFF",
              textShadow: "0 3px 12px rgba(0,0,0,0.9)",
            }}
          >
            {labelTop}
          </div>
        ) : null}
      </div>

      <div
        style={{
          position: "absolute",
          top: 645,
          left: 48,
          right: 48,
          height: 440,
          borderRadius: 22,
          overflow: "hidden",
          border: `2px solid ${palette.accent}66`,
          transform: `translateY(${botY}px)`,
        }}
      >
        <SafePhoto
          src={second || pickPrimaryAsset(scene)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${interpolate(f, [0, 180], [1.08, 1.0])})`,
            filter: second ? "none" : "grayscale(0.7) contrast(1.2)",
          }}
        />
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.84) 100%)",
          }}
        />
        {labelBot ? (
          <div
            style={{
              position: "absolute",
              bottom: 22,
              left: 26,
              right: 26,
              fontFamily: "Inter, sans-serif",
              fontWeight: 900,
              fontSize: fitFontSize(labelBot, 40, 22, 28),
              color: palette.accent,
              textShadow: "0 3px 12px rgba(0,0,0,0.9)",
            }}
          >
            {labelBot}
          </div>
        ) : null}
      </div>

      <div
        style={{
          position: "absolute",
          top: 582,
          left: "50%",
          transform: `translate(-50%, 0) scale(${slide})`,
          padding: "12px 32px",
          borderRadius: 999,
          backgroundColor: palette.stamp,
          color: "#FFFFFF",
          fontFamily: "Inter, sans-serif",
          fontWeight: 900,
          fontSize: fitFontSize(badge, 40, 10, 26),
          letterSpacing: 2,
          boxShadow: `0 0 32px ${palette.stamp}AA`,
          border: "3px solid #FFFFFF",
        }}
      >
        {badge}
      </div>
    </AbsoluteFill>
  );
};

/* 4. ODOMETER SHOCK: Full-bleed photo + giant 3D rolling number pop in upper-middle safe zone */
const SceneOdometerShock: React.FC<{
  scene: ExtendedScene;
  palette: Palette;
  f: number;
  fps: number;
}> = ({ scene, palette, f, fps }) => {
  const pop = spring({ frame: f, fps, config: { damping: 11, stiffness: 160 } });
  const zoom = interpolate(f, [0, 180], [1.02, 1.12], { extrapolateRight: "clamp" });
  const stat = formatStat(scene) || scene.heroText || "";
  const sub = scene.statLabel || scene.infoTags?.[0] || scene.subNote || "";

  let displayStat = stat;
  const match = stat.match(/([\d.,]+)/);
  if (match && f < 28) {
    const rawNum = parseFloat(match[1].replace(/,/g, ""));
    if (!Number.isNaN(rawNum) && rawNum > 0) {
      const prog = interpolate(f, [0, 26], [0.15, 1], { extrapolateRight: "clamp" });
      const cur = Math.round(rawNum * prog);
      displayStat = stat.replace(match[1], cur.toLocaleString("en-US"));
    }
  }

  return (
    <AbsoluteFill style={{ backgroundColor: palette.bg }}>
      <SafePhoto
        src={pickPrimaryAsset(scene)}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${zoom})`,
          filter: "brightness(0.84) contrast(1.08)",
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(180deg, rgba(6,8,14,0.82) 0%, rgba(6,8,14,0.18) 38%, rgba(6,8,14,0.22) 64%, rgba(6,8,14,0.88) 100%)",
        }}
      />

      <div
        style={{
          position: "absolute",
          top: 235,
          left: 56,
          right: 56,
          textAlign: "center",
          transform: `scale(${0.7 + 0.3 * pop})`,
          opacity: pop,
        }}
      >
        <div
          style={{
            fontFamily: "Inter, sans-serif",
            fontWeight: 900,
            fontSize: fitFontSize(displayStat, 124, 9, 54),
            lineHeight: 1.02,
            color: palette.accent,
            textShadow: "0 8px 34px rgba(0,0,0,0.95), 0 0 42px rgba(245,158,11,0.35)",
          }}
        >
          {displayStat}
        </div>
        {sub ? (
          <div
            style={{
              marginTop: 14,
              fontFamily: "Inter, sans-serif",
              fontWeight: 800,
              fontSize: fitFontSize(sub, 40, 24, 26),
              color: "#FFFFFF",
              textTransform: "uppercase",
              letterSpacing: 2,
              textShadow: "0 4px 16px rgba(0,0,0,0.95)",
            }}
          >
            {sub}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

/* 5. HEADLINE EVIDENCE: Floating editorial press card with red/amber underline sweep */
const SceneHeadlineEvidence: React.FC<{
  scene: ExtendedScene;
  palette: Palette;
  f: number;
  fps: number;
}> = ({ scene, palette, f, fps }) => {
  const cardIn = spring({ frame: f, fps, config: { damping: 14, stiffness: 130 } });
  const underlineW = interpolate(f, [14, 38], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const headline = scene.heroText || "";
  const source = String(scene.sourceTag || scene.eyebrow || scene.infoTags?.[0] || "BẰNG CHỨNG THỰC TẾ").toUpperCase();

  return (
    <AbsoluteFill>
      <StudioBackdrop palette={palette} frame={f} />

      <div
        style={{
          position: "absolute",
          top: 250,
          left: 64,
          right: 64,
          borderRadius: 24,
          overflow: "hidden",
          backgroundColor: "#141720",
          border: "2px solid rgba(255,255,255,0.16)",
          boxShadow: "0 30px 80px rgba(0,0,0,0.78)",
          transform: `perspective(1100px) rotateY(${interpolate(f, [0, 180], [3, -3])}deg) scale(${0.9 + 0.1 * cardIn})`,
        }}
      >
        <div style={{ height: 520, overflow: "hidden" }}>
          <SafePhoto
            src={pickPrimaryAsset(scene)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              transform: `scale(${interpolate(f, [0, 180], [1.0, 1.08])})`,
            }}
          />
        </div>
        <div style={{ padding: "28px 32px 34px 32px" }}>
          <div
            style={{
              display: "inline-block",
              padding: "6px 14px",
              borderRadius: 6,
              backgroundColor: palette.stamp,
              color: "#FFFFFF",
              fontFamily: "Inter, sans-serif",
              fontWeight: 900,
              fontSize: 22,
              letterSpacing: 1.5,
              marginBottom: 16,
            }}
          >
            {source}
          </div>
          <div
            style={{
              fontFamily: "Inter, sans-serif",
              fontWeight: 900,
              fontSize: fitFontSize(headline, 46, 24, 30),
              lineHeight: 1.2,
              color: "#FFFFFF",
            }}
          >
            {headline}
          </div>
          <div
            style={{
              marginTop: 14,
              height: 6,
              width: `${underlineW}%`,
              borderRadius: 3,
              background: `linear-gradient(90deg, ${palette.accent}, ${palette.stamp})`,
            }}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* 6. TIMELINE REVEAL: Sequentially lit nodes over parallax photo */
const SceneTimelineReveal: React.FC<{
  scene: ExtendedScene;
  palette: Palette;
  f: number;
  fps: number;
}> = ({ scene, palette, f, fps }) => {
  const nodes =
    scene.timelineNodes && scene.timelineNodes.length >= 2
      ? scene.timelineNodes.slice(0, 3)
      : scene.chainSteps && scene.chainSteps.length >= 2
      ? scene.chainSteps.slice(0, 3).map((s) => `${s.badge ? s.badge + " " : ""}${s.title}`)
      : [
          scene.heroText || "KHỞI ĐIỂM",
          formatStat(scene) || "CƠ CHẾ ẨN",
          scene.infoTags?.[0] || scene.subNote || "KẾT QUẢ THỰC TẾ",
        ].filter(Boolean);

  return (
    <AbsoluteFill style={{ backgroundColor: palette.bg }}>
      <SafePhoto
        src={pickPrimaryAsset(scene)}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${interpolate(f, [0, 180], [1.04, 1.12])})`,
          filter: "brightness(0.45) contrast(1.12)",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: 260,
          left: 84,
          right: 84,
          display: "flex",
          flexDirection: "column",
          gap: 44,
        }}
      >
        {nodes.map((txt, idx) => {
          const delay = idx * 14;
          const nodeSpring = spring({
            frame: Math.max(0, f - delay),
            fps,
            config: { damping: 12, stiffness: 150 },
          });
          return (
            <div
              key={idx}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 24,
                opacity: nodeSpring,
                transform: `translateX(${(1 - nodeSpring) * 40}px)`,
              }}
            >
              <div
                style={{
                  width: 34,
                  height: 34,
                  borderRadius: "50%",
                  backgroundColor: palette.accent,
                  border: "4px solid #FFFFFF",
                  boxShadow: `0 0 24px ${palette.accent}`,
                  flexShrink: 0,
                }}
              />
              <div
                style={{
                  fontFamily: "Inter, sans-serif",
                  fontWeight: 900,
                  fontSize: fitFontSize(txt, 46, 22, 30),
                  color: idx === nodes.length - 1 ? palette.accent : "#FFFFFF",
                  textShadow: "0 4px 18px rgba(0,0,0,0.95)",
                }}
              >
                {txt}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/* 7. FLOW DIAGRAM: 3D glowing mechanism / money-flow pipeline (100% data-driven from chainSteps) */
const SceneFlowDiagram: React.FC<{
  scene: ExtendedScene;
  palette: Palette;
  f: number;
  fps: number;
}> = ({ scene, palette, f, fps }) => {
  const steps =
    scene.chainSteps && scene.chainSteps.length >= 2
      ? scene.chainSteps.slice(0, 3)
      : [
          { badge: "01", title: scene.heroText || "NGUỒN VÀO", detail: scene.eyebrow || "" },
          { badge: "02", title: formatStat(scene) || "CƠ CHẾ CHÍNH", detail: scene.subNote || "" },
          { badge: "03", title: scene.infoTags?.[0] || "KẾT QUẢ CUỐI", detail: scene.stampText || "" },
        ];
  const title = scene.heroText || scene.eyebrow || "CƠ CHẾ HOẠT ĐỘNG";
  const pulseY = ((f % 45) / 45) * 100;

  return (
    <AbsoluteFill>
      <StudioBackdrop palette={palette} frame={f} />
      <SafePhoto
        src={pickPrimaryAsset(scene)}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: 0.22,
          transform: `scale(${interpolate(f, [0, 180], [1.03, 1.11])})`,
          filter: "grayscale(0.35) contrast(1.15)",
        }}
      />

      <div
        style={{
          position: "absolute",
          top: 195,
          left: 60,
          right: 60,
          textAlign: "center",
          fontFamily: "Inter, sans-serif",
          fontWeight: 900,
          fontSize: fitFontSize(title, 46, 24, 30),
          color: palette.accent,
          textTransform: "uppercase",
          letterSpacing: 1.5,
          textShadow: "0 4px 18px rgba(0,0,0,0.95)",
        }}
      >
        {title}
      </div>

      <div
        style={{
          position: "absolute",
          top: 300,
          left: 72,
          right: 72,
          display: "flex",
          flexDirection: "column",
          gap: 38,
        }}
      >
        {steps.map((st, idx) => {
          const delay = idx * 12;
          const pop = spring({
            frame: Math.max(0, f - delay),
            fps,
            config: { damping: 12, stiffness: 150 },
          });
          const isLast = idx === steps.length - 1;
          return (
            <React.Fragment key={idx}>
              <div
                style={{
                  position: "relative",
                  padding: "24px 28px",
                  borderRadius: 20,
                  backgroundColor: isLast ? "rgba(220, 38, 38, 0.2)" : "rgba(14, 19, 30, 0.88)",
                  border: `2px solid ${isLast ? palette.stamp : palette.accent}99`,
                  boxShadow: `0 20px 50px rgba(0,0,0,0.65), 0 0 28px ${
                    isLast ? palette.stamp : palette.accent
                  }33`,
                  transform: `perspective(1000px) rotateX(3deg) translateY(${(1 - pop) * 28}px) scale(${0.92 + 0.08 * pop})`,
                  opacity: pop,
                }}
              >
                <div
                  style={{
                    fontFamily: "Inter, sans-serif",
                    fontWeight: 900,
                    fontSize: 22,
                    color: isLast ? "#FCA5A5" : palette.accent,
                    letterSpacing: 1.5,
                    marginBottom: 6,
                  }}
                >
                  {(st.badge || `BƯỚC ${idx + 1}`).toUpperCase()}
                </div>
                <div
                  style={{
                    fontFamily: "Inter, sans-serif",
                    fontWeight: 900,
                    fontSize: fitFontSize(st.title, 40, 24, 26),
                    color: "#FFFFFF",
                    lineHeight: 1.18,
                  }}
                >
                  {st.title}
                </div>
                {st.detail ? (
                  <div
                    style={{
                      marginTop: 6,
                      fontFamily: "Inter, sans-serif",
                      fontWeight: 700,
                      fontSize: 26,
                      color: "rgba(255,255,255,0.78)",
                    }}
                  >
                    {st.detail}
                  </div>
                ) : null}
              </div>

              {idx < steps.length - 1 ? (
                <div
                  style={{
                    position: "relative",
                    alignSelf: "center",
                    width: 6,
                    height: 36,
                    marginTop: -28,
                    marginBottom: -28,
                    borderRadius: 3,
                    background: `linear-gradient(180deg, ${palette.accent}, ${palette.stamp})`,
                    boxShadow: `0 0 16px ${palette.accent}`,
                    opacity: pop,
                  }}
                >
                  <div
                    style={{
                      position: "absolute",
                      left: -5,
                      top: `${pulseY}%`,
                      width: 16,
                      height: 16,
                      borderRadius: "50%",
                      backgroundColor: "#FFFFFF",
                      boxShadow: `0 0 18px ${palette.accent}`,
                    }}
                  />
                </div>
              ) : null}
            </React.Fragment>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/* 8. BAR VERSUS: 3D animated comparison columns (100% data-driven from leftValue/rightValue) */
const SceneBarVersus: React.FC<{
  scene: ExtendedScene;
  palette: Palette;
  f: number;
  fps: number;
}> = ({ scene, palette, f, fps }) => {
  const grow = spring({ frame: Math.max(0, f - 6), fps, config: { damping: 14, stiffness: 105 } });
  const lVal = typeof scene.leftValue === "number" ? scene.leftValue : 100;
  const rVal = typeof scene.rightValue === "number" ? scene.rightValue : 0;
  const maxVal = Math.max(1, lVal, rVal);
  const lPct = Math.max(10, Math.round((lVal / maxVal) * 100));
  const rPct = Math.max(6, Math.round((rVal / maxVal) * 100));
  const unit = scene.statSuffix || "%";
  const lLabel = scene.leftLabel || "MỨC THƯỜNG";
  const rLabel = scene.rightLabel || "THỰC TẾ";
  const title = scene.heroText || "SO SÁNH TRỰC DIỆN";

  return (
    <AbsoluteFill>
      <StudioBackdrop palette={palette} frame={f} />
      <SafePhoto
        src={pickPrimaryAsset(scene)}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: 0.2,
          transform: `scale(${interpolate(f, [0, 180], [1.02, 1.1])})`,
        }}
      />

      <div
        style={{
          position: "absolute",
          top: 210,
          left: 60,
          right: 60,
          textAlign: "center",
          fontFamily: "Inter, sans-serif",
          fontWeight: 900,
          fontSize: fitFontSize(title, 48, 22, 30),
          color: "#FFFFFF",
          textTransform: "uppercase",
          textShadow: "0 4px 18px rgba(0,0,0,0.95)",
        }}
      >
        {title}
      </div>

      {/* 3D Bar Stage */}
      <div
        style={{
          position: "absolute",
          top: 340,
          left: 86,
          right: 86,
          height: 620,
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "space-around",
          paddingBottom: 60,
          borderBottom: "4px solid rgba(255,255,255,0.28)",
        }}
      >
        {[
          { val: lVal, pct: lPct, label: lLabel, col: scene.leftLabelColor || palette.accent },
          { val: rVal, pct: rPct, label: rLabel, col: scene.rightLabelColor || palette.stamp },
        ].map((item, idx) => {
          const h = Math.round((420 * item.pct) / 100) * grow;
          return (
            <div
              key={idx}
              style={{
                width: 300,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <div
                style={{
                  fontFamily: "Inter, sans-serif",
                  fontWeight: 900,
                  fontSize: 64,
                  color: item.col,
                  marginBottom: 14,
                  textShadow: "0 4px 18px rgba(0,0,0,0.95)",
                  opacity: grow,
                }}
              >
                {Math.round(item.val * grow)}
                {unit}
              </div>
              <div
                style={{
                  width: 190,
                  height: Math.max(24, h),
                  borderRadius: "18px 18px 4px 4px",
                  background: `linear-gradient(135deg, ${item.col} 0%, ${item.col}88 100%)`,
                  borderTop: "4px solid rgba(255,255,255,0.65)",
                  boxShadow: `0 0 36px ${item.col}55, 14px 0 24px rgba(0,0,0,0.55)`,
                }}
              />
              <div
                style={{
                  marginTop: 18,
                  fontFamily: "Inter, sans-serif",
                  fontWeight: 900,
                  fontSize: fitFontSize(item.label, 34, 16, 24),
                  color: "#FFFFFF",
                  textAlign: "center",
                }}
              >
                {item.label}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/* 9. EVIDENCE STACK: Multi-layer parallax (backdrop + tilted card + floating 3D cutout) */
const SceneEvidenceStack: React.FC<{
  scene: ExtendedScene;
  palette: Palette;
  f: number;
  fps: number;
}> = ({ scene, palette, f, fps }) => {
  const s1 = spring({ frame: f, fps, config: { damping: 14, stiffness: 120 } });
  const s2 = spring({ frame: Math.max(0, f - 10), fps, config: { damping: 12, stiffness: 140 } });
  const headline = scene.heroText || "";
  const second = pickSecondaryAsset(scene);

  return (
    <AbsoluteFill style={{ backgroundColor: palette.bg }}>
      <SafePhoto
        src={pickPrimaryAsset(scene)}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${interpolate(f, [0, 180], [1.04, 1.13])})`,
          filter: "brightness(0.45) contrast(1.12)",
        }}
      />

      {/* Mid-ground tilted card */}
      <div
        style={{
          position: "absolute",
          top: 230,
          left: 72,
          right: 170,
          height: 580,
          borderRadius: 22,
          overflow: "hidden",
          border: "2px solid rgba(255,255,255,0.22)",
          boxShadow: "0 30px 70px rgba(0,0,0,0.8)",
          transform: `perspective(1100px) rotateY(7deg) translateX(${(1 - s1) * -90}px)`,
          opacity: s1,
        }}
      >
        <SafePhoto
          src={pickPrimaryAsset(scene)}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      </div>

      {/* Foreground 3D floating cutout / second proof */}
      <div
        style={{
          position: "absolute",
          top: 430,
          right: 48,
          width: 480,
          height: 520,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          transform: `translateX(${(1 - s2) * 110}px) translateY(${Math.sin(f * 0.05) * 8}px)`,
          opacity: s2,
        }}
      >
        <SafePhoto
          src={second || pickPrimaryAsset(scene)}
          style={{
            maxWidth: "100%",
            maxHeight: "100%",
            objectFit: "contain",
            borderRadius: 18,
            filter: `drop-shadow(0 0 22px ${palette.accent}66) drop-shadow(0 24px 36px rgba(0,0,0,0.9))`,
          }}
        />
      </div>

      {headline ? (
        <div
          style={{
            position: "absolute",
            top: 930,
            left: 64,
            right: 64,
            fontFamily: "Inter, sans-serif",
            fontWeight: 900,
            fontSize: fitFontSize(headline, 44, 24, 28),
            color: palette.accent,
            textShadow: "0 4px 18px rgba(0,0,0,0.98)",
          }}
        >
          {headline}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

function resolveArchetype(layout?: string, index = 0): string {
  const l = (layout || "").toLowerCase();
  if (
    l === "dossier_stamp" ||
    l === "cutout_ar_stage" ||
    l === "split_versus" ||
    l === "odometer_shock" ||
    l === "headline_evidence" ||
    l === "timeline_reveal" ||
    l === "flow_diagram" ||
    l === "bar_versus" ||
    l === "evidence_stack"
  ) {
    return l;
  }
  if (l.includes("flow") || l.includes("chain") || l.includes("causal")) return "flow_diagram";
  if (l.includes("bar")) return "bar_versus";
  if (l.includes("stack") || l.includes("multi")) return "evidence_stack";
  if (l.includes("odometer") || l.includes("stat")) return "odometer_shock";
  if (l.includes("card") || l.includes("evidence") || l.includes("archival")) return "headline_evidence";
  if (l.includes("split") || l.includes("compare")) return "split_versus";
  if (l.includes("cutout") || l.includes("ar") || l.includes("hero_prop")) return "cutout_ar_stage";
  if (l.includes("timeline")) return "timeline_reveal";
  const cycle = [
    "dossier_stamp",
    "flow_diagram",
    "bar_versus",
    "cutout_ar_stage",
    "evidence_stack",
    "odometer_shock",
  ];
  return cycle[index % cycle.length];
}

const SceneDispatcher: React.FC<{
  scene: ExtendedScene;
  index: number;
  palette: Palette;
  durationFrames: number;
}> = ({ scene, index, palette, durationFrames }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const archetype = resolveArchetype(scene.layout, index);

  const entryShake = f < 8 ? Math.sin(f * 2.5) * (8 - f) * 1.1 : 0;
  const stampShake =
    archetype === "dossier_stamp" && f >= 20 && f <= 28
      ? Math.sin(f * 3.1) * (28 - f) * 1.4
      : 0;
  const driftX = Math.sin(f * 0.035 + index) * 5 + entryShake + stampShake;
  const driftY = Math.cos(f * 0.028 + index) * 4 + (entryShake + stampShake) * 0.6;

  const opacity = interpolate(
    f,
    [0, 6, Math.max(7, durationFrames - 6), durationFrames],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        opacity,
        transform: `translate(${driftX}px, ${driftY}px)`,
      }}
    >
      {archetype === "dossier_stamp" && (
        <SceneDossierStamp scene={scene} palette={palette} f={f} fps={fps} />
      )}
      {archetype === "cutout_ar_stage" && (
        <SceneCutoutARStage scene={scene} palette={palette} f={f} fps={fps} />
      )}
      {archetype === "split_versus" && (
        <SceneSplitVersus scene={scene} palette={palette} f={f} fps={fps} />
      )}
      {archetype === "odometer_shock" && (
        <SceneOdometerShock scene={scene} palette={palette} f={f} fps={fps} />
      )}
      {archetype === "headline_evidence" && (
        <SceneHeadlineEvidence scene={scene} palette={palette} f={f} fps={fps} />
      )}
      {archetype === "timeline_reveal" && (
        <SceneTimelineReveal scene={scene} palette={palette} f={f} fps={fps} />
      )}
      {archetype === "flow_diagram" && (
        <SceneFlowDiagram scene={scene} palette={palette} f={f} fps={fps} />
      )}
      {archetype === "bar_versus" && (
        <SceneBarVersus scene={scene} palette={palette} f={f} fps={fps} />
      )}
      {archetype === "evidence_stack" && (
        <SceneEvidenceStack scene={scene} palette={palette} f={f} fps={fps} />
      )}
    </AbsoluteFill>
  );
};

export const CinematicReel: React.FC<{ plan: UniversalScenePlan }> = ({ plan }) => {
  const { fps } = useVideoConfig();
  const palette = getPalette(plan.theme);

  const scenes = (plan.scenes || []) as unknown as ExtendedScene[];
  const captions = plan.captions || [];

  return (
    <AbsoluteFill style={{ backgroundColor: palette.bg }}>
      {scenes.map((scene, idx) => {
        const startFrame = Math.round((scene.startSec || 0) * fps);
        const endFrame = Math.round((scene.endSec || (scene.startSec || 0) + 4) * fps);
        const dur = Math.max(15, endFrame - startFrame);
        return (
          <Sequence key={idx} from={startFrame} durationInFrames={dur}>
            <SceneDispatcher scene={scene} index={idx} palette={palette} durationFrames={dur} />
          </Sequence>
        );
      })}

      <ChannelWatermark9x16 />
      <KineticWordCaption phrases={captions} placement="bottom" />
    </AbsoluteFill>
  );
};
