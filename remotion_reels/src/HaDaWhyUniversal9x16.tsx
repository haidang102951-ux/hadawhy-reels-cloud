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
import { HaDaWhyMistBackground } from "./components/HaDaWhyMistBackground";
import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16";
import { KineticWordCaption, CaptionPhrase } from "./components/KineticWordCaption";
import {
  SAT_FRA_PARIS,
  SAT_FRA_PATH,
  SAT_UK_LONDON,
  SAT_UK_PATH,
  SAT_USA_NYC,
  SAT_USA_PATH,
  SAT_WORLD_HUBS,
} from "./friday13SatMapsData";
import defaultPlan from "./scene_plan.json";

export interface UniversalSceneSpec {
  id: string;
  startSec: number;
  endSec: number;
  layout:
    | "hero_prop"
    | "compare_two"
    | "sat_map"
    | "two_tier"
    | "split_duo"
    | "stat_odometer"
    | "bar_compare"
    | "archival_proof"
    | "causal_chain";
  eyebrow: string;
  heroText: string;
  heroColor?: string;
  subNote?: string;
  yearWatermark?: string;
  primaryAsset?: string;
  primaryLabel?: string;
  leftAsset?: string;
  leftLabel?: string;
  leftLabelColor?: string;
  rightAsset?: string;
  rightLabel?: string;
  rightLabelColor?: string;
  centerAsset?: string;
  mapRegion?: "uk" | "fra" | "usa" | "world";
  mapCaption?: string;
  topLeftAsset?: string;
  topLeftLabel?: string;
  topRightAsset?: string;
  bottomAsset?: string;
  bottomTitle?: string;
  bottomHighlight?: string;
  ctaText?: string;
  statNumber?: number;
  statSuffix?: string;
  statLabel?: string;
  leftValue?: number;
  rightValue?: number;
  stampText?: string;
  infoTags?: string[];
  chainSteps?: Array<{ badge?: string; title: string; detail: string }>;
}

export interface UniversalScenePlan {
  projectTitle: string;
  fps: number;
  mistIntensity?: number;
  scenes: UniversalSceneSpec[];
  captions: CaptionPhrase[];
}

export interface HaDaWhyUniversal9x16Props {
  plan?: UniversalScenePlan;
}

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

const FONT_HEADING = `BeVietnamProBlack, sans-serif`;
const FONT_BODY = `BeVietnamProExtraBold, BeVietnamProBlack, sans-serif`;

const ImpactHook: React.FC<{
  eyebrow?: string;
  heroText?: string;
  heroColor?: string;
  subNote?: string;
}> = ({ eyebrow = "", heroText = "", heroColor = "#FFE600", subNote }) => {
  const safeHero = String(heroText || "").toUpperCase();
  const safeEyebrow = String(eyebrow || "").toUpperCase();
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const slam = spring({ frame, fps, config: { damping: 12, stiffness: 260 } });
  const scale = interpolate(slam, [0, 1], [1.75, 1]);
  const opacity = interpolate(frame, [0, 5], [0, 1], { extrapolateRight: "clamp" });
  const shakeDecay = interpolate(frame, [0, 10], [1, 0], { extrapolateRight: "clamp" });
  const shakeX = Math.sin(frame * 2.7) * 6 * shakeDecay;
  const shakeY = Math.cos(frame * 3.1) * 4 * shakeDecay;
  const sweepPos = interpolate(frame, [10, 46], [-120, 220], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 124,
        left: 60,
        right: 60,
        textAlign: "center",
        zIndex: 25,
        opacity,
        transform: `translate(${shakeX}px, ${shakeY}px) scale(${scale})`,
      }}
    >
      {safeEyebrow ? (
        <div
          style={{
            display: "inline-flex",
            flexDirection: "column",
            alignItems: "center",
            marginBottom: 8,
          }}
        >
          <div
            style={{
              fontFamily: FONT_BODY,
              fontSize: 30,
              fontWeight: 800,
              letterSpacing: 4.5,
              color: "#E2E8F0",
              textShadow: "0 3px 12px rgba(0,0,0,0.95)",
            }}
          >
            {safeEyebrow}
          </div>
          <div
            style={{
              marginTop: 6,
              width: 110,
              height: 3,
              borderRadius: 2,
              background: `linear-gradient(90deg, transparent, ${heroColor}, transparent)`,
            }}
          />
        </div>
      ) : null}
      <div
        style={{
          position: "relative",
          display: "inline-block",
          fontFamily: FONT_HEADING,
          fontSize: safeHero.length > 14 ? 64 : safeHero.length > 9 ? 76 : 96,
          fontWeight: 900,
          lineHeight: 1.08,
          letterSpacing: "-0.02em",
          marginTop: 6,
          color: heroColor,
          textShadow: `-3px -3px 0 #05070B, 3px -3px 0 #05070B, -3px 3px 0 #05070B, 3px 3px 0 #05070B, 0 6px 0 #05070B, 0 16px 32px rgba(0,0,0,0.95), 0 0 34px ${heroColor}66`,
        }}
      >
        {safeHero}
        <span
          aria-hidden
          style={{
            position: "absolute",
            inset: 0,
            background: `linear-gradient(110deg, transparent ${sweepPos - 18}%, rgba(255,255,255,0.65) ${sweepPos}%, transparent ${sweepPos + 18}%)`,
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            textShadow: "none",
            pointerEvents: "none",
          }}
        >
          {safeHero}
        </span>
      </div>
      {subNote ? (
        <div
          style={{
            marginTop: 14,
            fontFamily: FONT_BODY,
            fontSize: 28,
            fontWeight: 800,
            color: "#FFFFFF",
            letterSpacing: 1.8,
            textShadow: "0 4px 14px rgba(0,0,0,0.98)",
          }}
        >
          {String(subNote).toUpperCase()}
        </div>
      ) : null}
    </div>
  );
};

const WatermarkYear: React.FC<{ text?: string }> = ({ text }) => {
  if (!text) return null;
  return (
    <div
      style={{
        position: "absolute",
        top: 320,
        left: 0,
        right: 0,
        textAlign: "center",
        fontFamily: FONT_HEADING,
        fontSize: 280,
        fontWeight: 900,
        color: "rgba(66, 178, 242, 0.045)",
        letterSpacing: -6,
        userSelect: "none",
        pointerEvents: "none",
        zIndex: 2,
      }}
    >
      {text}
    </div>
  );
};

const InfoTagsRow: React.FC<{ tags?: string[]; accent?: string; top?: number }> = ({
  tags,
  accent = "#42B2F2",
  top = 1230,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!tags || tags.length === 0) return null;
  return (
    <div
      style={{
        position: "absolute",
        top,
        left: 56,
        right: 56,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: 14,
        zIndex: 18,
      }}
    >
      {tags.slice(0, 3).map((tag, idx) => {
        const pop = spring({ frame: frame - (8 + idx * 5), fps, config: { damping: 13, stiffness: 190 } });
        return (
          <div
            key={idx}
            style={{
              padding: "10px 22px",
              borderRadius: 999,
              background: "rgba(10, 18, 34, 0.78)",
              border: `2px solid ${accent}88`,
              boxShadow: `0 0 22px ${accent}33, 0 10px 22px rgba(0,0,0,0.65)`,
              fontFamily: FONT_BODY,
              fontSize: 25,
              fontWeight: 800,
              color: "#FFFFFF",
              letterSpacing: 0.8,
              transform: `translateY(${interpolate(pop, [0, 1], [18, 0])}px) scale(${interpolate(pop, [0, 1], [0.85, 1])})`,
              opacity: pop,
            }}
          >
            {String(tag).toUpperCase()}
          </div>
        );
      })}
    </div>
  );
};

const SceneHeroProp: React.FC<{ scene: UniversalSceneSpec }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame: frame - 3, fps, config: { damping: 12, stiffness: 150 } });
  const floatY = Math.sin(frame * 0.065) * 14;
  const tiltDeg = Math.sin(frame * 0.04) * 2.4;
  const ringRot = frame * 0.6;
  const shadowScale = interpolate(floatY, [-14, 14], [0.85, 1.06]);
  const accent = scene.heroColor || "#42B2F2";

  return (
    <AbsoluteFill>
      <WatermarkYear text={scene.yearWatermark} />
      <ImpactHook
        eyebrow={scene.eyebrow}
        heroText={scene.heroText}
        heroColor={scene.heroColor}
        subNote={scene.subNote}
      />
      {/* Radial 3D stage spotlight & rotating HUD halo so dark hardware never blends into void */}
      <div
        style={{
          position: "absolute",
          top: 470,
          left: "50%",
          width: 660,
          height: 660,
          marginLeft: -330,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${accent}30 0%, rgba(66,178,242,0.12) 42%, transparent 72%)`,
          border: `2px dashed ${accent}33`,
          transform: `rotate(${ringRot}deg) scale(${interpolate(enter, [0, 1], [0.6, 1])})`,
          opacity: enter,
          pointerEvents: "none",
          zIndex: 8,
        }}
      />
      {scene.primaryAsset ? (
        <div
          style={{
            position: "absolute",
            top: 465,
            left: 0,
            right: 0,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            transform: `perspective(1200px) translateY(${floatY}px) rotateZ(${tiltDeg}deg) scale(${interpolate(enter, [0, 1], [0.78, 1])})`,
            opacity: enter,
            zIndex: 12,
          }}
        >
          <Img
            src={staticFile(scene.primaryAsset)}
            style={{
              height: 620,
              maxWidth: 820,
              objectFit: "contain",
              filter: `drop-shadow(0 0 24px ${accent}55) drop-shadow(0 30px 44px rgba(0,0,0,0.92))`,
            }}
          />
          <div
            style={{
              width: 440,
              height: 34,
              marginTop: -12,
              borderRadius: "50%",
              background: "radial-gradient(ellipse at center, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0) 72%)",
              transform: `scale(${shadowScale})`,
              pointerEvents: "none",
            }}
          />
          {scene.primaryLabel ? (
            <div
              style={{
                marginTop: 18,
                fontFamily: FONT_BODY,
                fontSize: 30,
                fontWeight: 900,
                color: "#FFFFFF",
                textShadow: "0 4px 12px rgba(0,0,0,0.95)",
              }}
            >
              {scene.primaryLabel}
            </div>
          ) : null}
        </div>
      ) : null}
      <InfoTagsRow tags={scene.infoTags} accent={accent} top={1225} />
    </AbsoluteFill>
  );
};

const SceneCompareTwo: React.FC<{ scene: UniversalSceneSpec }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const leftIn = spring({ frame: frame - 4, fps, config: { damping: 14, stiffness: 120 } });
  const rightIn = spring({ frame: frame - 10, fps, config: { damping: 14, stiffness: 120 } });

  return (
    <AbsoluteFill>
      <WatermarkYear text={scene.yearWatermark} />
      <ImpactHook eyebrow={scene.eyebrow} heroText={scene.heroText} heroColor={scene.heroColor} />

      <div
        style={{
          position: "absolute",
          top: 470,
          left: 44,
          right: 44,
          height: 820,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 12,
        }}
      >
        {/* Left subject */}
        <div
          style={{
            width: 440,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            transform: `translateX(${interpolate(leftIn, [0, 1], [-80, 0])}px) translateY(${Math.sin(frame * 0.06) * 12}px) rotateZ(${Math.sin(frame * 0.04) * 2.2}deg)`,
            opacity: leftIn,
          }}
        >
          {scene.leftAsset ? (
            <Img
              src={staticFile(scene.leftAsset)}
              style={{
                height: 620,
                maxWidth: 420,
                objectFit: "contain",
                filter: "drop-shadow(0 24px 36px rgba(0,0,0,0.92))",
              }}
            />
          ) : null}
          {scene.leftLabel ? (
            <div
              style={{
                marginTop: 18,
                fontFamily: FONT_BODY,
                fontSize: 24,
                fontWeight: 900,
                color: scene.leftLabelColor || "#facc15",
                textAlign: "center",
                textShadow: "0 4px 12px rgba(0,0,0,0.98)",
              }}
            >
              {scene.leftLabel}
            </div>
          ) : null}
        </div>

        {/* Center link / chain */}
        {scene.centerAsset ? (
          <Img
            src={staticFile(scene.centerAsset)}
            style={{
              position: "absolute",
              left: "50%",
              top: 210,
              width: 240,
              transform: `translateX(-50%) rotate(${-18 + Math.sin(frame * 0.07) * 6}deg) scale(${1 + Math.sin(frame * 0.08) * 0.07})`,
              opacity: 0.9,
              filter: "drop-shadow(0 12px 24px rgba(0,0,0,0.95))",
              zIndex: 14,
            }}
          />
        ) : null}

        {/* Right subject */}
        <div
          style={{
            width: 440,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            transform: `translateX(${interpolate(rightIn, [0, 1], [80, 0])}px) translateY(${Math.sin(frame * 0.06 + 2.2) * 12}px) rotateZ(${-Math.sin(frame * 0.04) * 2.2}deg)`,
            opacity: rightIn,
          }}
        >
          {scene.rightAsset ? (
            <Img
              src={staticFile(scene.rightAsset)}
              style={{
                height: 620,
                maxWidth: 420,
                objectFit: "contain",
                filter: "drop-shadow(0 24px 36px rgba(0,0,0,0.92))",
              }}
            />
          ) : null}
          {scene.rightLabel ? (
            <div
              style={{
                marginTop: 18,
                fontFamily: FONT_BODY,
                fontSize: 24,
                fontWeight: 900,
                color: scene.rightLabelColor || "#ff3b3b",
                textAlign: "center",
                textShadow: "0 4px 12px rgba(0,0,0,0.98)",
              }}
            >
              {scene.rightLabel}
            </div>
          ) : null}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const SceneSatMap: React.FC<{ scene: UniversalSceneSpec }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: frame - 3, fps, config: { damping: 14, stiffness: 110 } });
  const region = scene.mapRegion || "fra";

  const mapConfig = {
    uk: { img: "harvested/sat_uk.png", path: SAT_UK_PATH, pin: SAT_UK_LONDON },
    fra: { img: "harvested/sat_fra.png", path: SAT_FRA_PATH, pin: SAT_FRA_PARIS },
    usa: { img: "harvested/sat_usa.png", path: SAT_USA_PATH, pin: SAT_USA_NYC },
    world: { img: "harvested/sat_world.png", path: "", pin: SAT_WORLD_HUBS[0] },
  }[region];

  const pulse = 1 + Math.sin(frame * 0.14) * 0.22;

  return (
    <AbsoluteFill>
      <ImpactHook eyebrow={scene.eyebrow} heroText={scene.heroText} heroColor={scene.heroColor} />
      <div
        style={{
          position: "absolute",
          top: 470,
          left: 65,
          right: 65,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `perspective(1200px) rotateX(18deg) scale(${interpolate(pop, [0, 1], [0.9, 1])})`,
          opacity: pop,
          zIndex: 12,
        }}
      >
        <div
          style={{
            position: "relative",
            width: 920,
            height: 700,
            borderRadius: 28,
            overflow: "hidden",
            border: "3px solid rgba(66, 178, 242, 0.55)",
            boxShadow: "0 36px 72px rgba(0,0,0,0.92), 0 0 36px rgba(66,178,242,0.22)",
          }}
        >
          <Img
            src={staticFile(mapConfig.img)}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
          <svg
            viewBox="0 0 920 700"
            style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
          >
            {mapConfig.path ? (
              <path
                d={mapConfig.path}
                fill="rgba(250,204,21,0.08)"
                stroke="#facc15"
                strokeWidth={3.5}
              />
            ) : null}
            {mapConfig.pin ? (
              <g transform={`translate(${mapConfig.pin.x}, ${mapConfig.pin.y})`}>
                <circle r={18 * pulse} fill="rgba(239,68,68,0.28)" stroke="#ef4444" strokeWidth={2} />
                <circle r={8} fill="#ff3b3b" stroke="#ffffff" strokeWidth={2.5} />
              </g>
            ) : null}
          </svg>
        </div>
        {scene.mapCaption ? (
          <div
            style={{
              marginTop: 28,
              fontFamily: FONT_BODY,
              fontSize: 30,
              fontWeight: 900,
              color: "#facc15",
              letterSpacing: 1.5,
              textShadow: "0 4px 14px rgba(0,0,0,0.95)",
            }}
          >
            {scene.mapCaption}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

const SceneTwoTier: React.FC<{ scene: UniversalSceneSpec }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: frame - 4, fps, config: { damping: 14, stiffness: 120 } });

  return (
    <AbsoluteFill>
      <WatermarkYear text={scene.yearWatermark} />
      <ImpactHook eyebrow={scene.eyebrow} heroText={scene.heroText} heroColor={scene.heroColor} />

      {/* Tier 1: Top portrait + evidence */}
      <div
        style={{
          position: "absolute",
          top: 410,
          left: 70,
          right: 70,
          height: 410,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          opacity: pop,
          zIndex: 12,
        }}
      >
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 450 }}>
          {scene.topLeftAsset ? (
            <Img
              src={staticFile(scene.topLeftAsset)}
              style={{
                height: 330,
                objectFit: "contain",
                filter: "drop-shadow(0 18px 28px rgba(0,0,0,0.9))",
              }}
            />
          ) : null}
          {scene.topLeftLabel ? (
            <div
              style={{
                marginTop: 10,
                fontFamily: FONT_BODY,
                fontSize: 22,
                fontWeight: 900,
                color: "#FFFFFF",
              }}
            >
              {scene.topLeftLabel}
            </div>
          ) : null}
        </div>
        {scene.topRightAsset ? (
          <Img
            src={staticFile(scene.topRightAsset)}
            style={{
              height: 360,
              objectFit: "contain",
              transform: "rotate(4deg)",
              filter: "drop-shadow(0 22px 32px rgba(0,0,0,0.92))",
            }}
          />
        ) : null}
      </div>

      {/* Tier 2: Bottom archival backdrop + title */}
      <div
        style={{
          position: "absolute",
          top: 860,
          left: 70,
          right: 70,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          opacity: pop,
          zIndex: 12,
        }}
      >
        {scene.bottomAsset ? (
          <Img
            src={staticFile(scene.bottomAsset)}
            style={{
              width: 940,
              height: 360,
              objectFit: "cover",
              borderRadius: 18,
              border: "2px solid rgba(255,255,255,0.22)",
              boxShadow: "0 24px 48px rgba(0,0,0,0.9)",
            }}
          />
        ) : null}
        {scene.bottomTitle ? (
          <div style={{ marginTop: 18, textAlign: "center" }}>
            <div style={{ fontFamily: FONT_BODY, fontSize: 28, fontWeight: 900, color: "#FFFFFF" }}>
              {scene.bottomTitle}
            </div>
            {scene.bottomHighlight ? (
              <div style={{ fontFamily: FONT_HEADING, fontSize: 56, fontWeight: 900, color: "#ff3b3b" }}>
                {scene.bottomHighlight}
              </div>
            ) : null}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};

const SceneSplitDuo: React.FC<{ scene: UniversalSceneSpec }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: frame - 4, fps, config: { damping: 14, stiffness: 120 } });

  return (
    <AbsoluteFill>
      <ImpactHook eyebrow={scene.eyebrow} heroText={scene.heroText} heroColor={scene.heroColor} />
      <div
        style={{
          position: "absolute",
          top: 470,
          left: 60,
          right: 60,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          opacity: pop,
          zIndex: 12,
        }}
      >
        <div style={{ width: 410, textAlign: "center" }}>
          {scene.leftAsset ? (
            <Img
              src={staticFile(scene.leftAsset)}
              style={{ height: 480, maxWidth: 390, objectFit: "contain", transform: "rotate(-3deg)" }}
            />
          ) : null}
          {scene.leftLabel ? (
            <div style={{ marginTop: 14, fontFamily: FONT_BODY, fontSize: 26, fontWeight: 900, color: "#facc15" }}>
              {scene.leftLabel}
            </div>
          ) : null}
        </div>
        <div style={{ fontFamily: FONT_HEADING, fontSize: 64, fontWeight: 900, color: "#FFFFFF" }}>+</div>
        <div style={{ width: 410, textAlign: "center" }}>
          {scene.rightAsset ? (
            <Img
              src={staticFile(scene.rightAsset)}
              style={{
                height: 480,
                maxWidth: 390,
                objectFit: "contain",
                borderRadius: 12,
                transform: "rotate(3deg)",
              }}
            />
          ) : null}
          {scene.rightLabel ? (
            <div style={{ marginTop: 14, fontFamily: FONT_BODY, fontSize: 26, fontWeight: 900, color: "#ff3b3b" }}>
              {scene.rightLabel}
            </div>
          ) : null}
        </div>
      </div>
      {scene.ctaText ? (
        <div
          style={{
            position: "absolute",
            top: 1120,
            left: 70,
            right: 70,
            textAlign: "center",
            fontFamily: FONT_BODY,
            fontSize: 32,
            fontWeight: 900,
            color: "#FFFFFF",
            borderTop: "2px solid rgba(66, 178, 242, 0.45)",
            paddingTop: 22,
            zIndex: 14,
          }}
        >
          {scene.ctaText}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

const SceneStatOdometer: React.FC<{ scene: UniversalSceneSpec }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: frame - 3, fps, config: { damping: 12, stiffness: 160 } });
  const targetNum = Number(scene.statNumber ?? 100);
  const countProgress = interpolate(frame, [4, 38], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const eased = 1 - Math.pow(1 - countProgress, 3);
  const currentVal = Math.round(targetNum * eased);
  const floatY = Math.sin(frame * 0.06) * 10;

  return (
    <AbsoluteFill>
      <WatermarkYear text={scene.yearWatermark} />
      <ImpactHook eyebrow={scene.eyebrow} heroText={scene.heroText} heroColor={scene.heroColor} />
      <div
        style={{
          position: "absolute",
          top: 520,
          left: 60,
          right: 60,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `translateY(${floatY}px) scale(${interpolate(pop, [0, 1], [0.78, 1])})`,
          opacity: pop,
          zIndex: 14,
        }}
      >
        <div
          style={{
            fontFamily: FONT_HEADING,
            fontSize: 148,
            fontWeight: 900,
            color: scene.heroColor || "#FFE600",
            textShadow: `-4px -4px 0 #05070B, 4px -4px 0 #05070B, -4px 4px 0 #05070B, 4px 4px 0 #05070B, 0 8px 0 #05070B, 0 18px 34px rgba(0,0,0,0.95), 0 0 36px ${(scene.heroColor || "#FFE600")}88`,
            lineHeight: 1,
          }}
        >
          {currentVal.toLocaleString("en-US")}
          {scene.statSuffix || ""}
        </div>
        {scene.statLabel ? (
          <div
            style={{
              marginTop: 18,
              fontFamily: FONT_BODY,
              fontSize: 34,
              fontWeight: 900,
              color: "#FFFFFF",
              letterSpacing: 2,
              textAlign: "center",
              textShadow: "0 4px 16px rgba(0,0,0,0.95)",
            }}
          >
            {scene.statLabel}
          </div>
        ) : null}
        {scene.primaryAsset ? (
          <Img
            src={staticFile(scene.primaryAsset)}
            style={{
              marginTop: 24,
              height: 340,
              maxWidth: 660,
              objectFit: "contain",
              filter: "drop-shadow(0 0 24px rgba(66,178,242,0.45)) drop-shadow(0 24px 36px rgba(0,0,0,0.95))",
            }}
          />
        ) : null}
      </div>
      <InfoTagsRow tags={scene.infoTags} accent={scene.heroColor || "#FFE600"} top={1235} />
    </AbsoluteFill>
  );
};

const SceneBarCompare: React.FC<{ scene: UniversalSceneSpec }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const grow = spring({ frame: frame - 6, fps, config: { damping: 14, stiffness: 120 } });
  const lv = Math.max(1, Number(scene.leftValue ?? 25));
  const rv = Math.max(1, Number(scene.rightValue ?? 90));
  const maxV = Math.max(lv, rv);
  const leftH = Math.round((lv / maxV) * 520 * grow);
  const rightH = Math.round((rv / maxV) * 520 * grow);

  return (
    <AbsoluteFill>
      <WatermarkYear text={scene.yearWatermark} />
      <ImpactHook eyebrow={scene.eyebrow} heroText={scene.heroText} heroColor={scene.heroColor} />
      <div
        style={{
          position: "absolute",
          top: 520,
          left: 90,
          right: 90,
          height: 700,
          display: "flex",
          justifyContent: "space-around",
          alignItems: "flex-end",
          zIndex: 14,
        }}
      >
        {/* Left Bar */}
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 320 }}>
          <div style={{ fontFamily: FONT_HEADING, fontSize: 56, color: scene.leftLabelColor || "#94a3b8", marginBottom: 14 }}>
            {Math.round(lv * grow)}
          </div>
          <div
            style={{
              width: 170,
              height: Math.max(24, leftH),
              borderRadius: "18px 18px 6px 6px",
              background: `linear-gradient(180deg, ${scene.leftLabelColor || "#64748b"} 0%, rgba(15,23,42,0.85) 100%)`,
              boxShadow: `0 0 28px ${(scene.leftLabelColor || "#64748b")}55`,
            }}
          />
          <div style={{ marginTop: 18, fontFamily: FONT_BODY, fontSize: 28, color: "#FFFFFF", textAlign: "center" }}>
            {scene.leftLabel || "TRƯỚC"}
          </div>
        </div>
        {/* Right Bar */}
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", width: 320 }}>
          <div style={{ fontFamily: FONT_HEADING, fontSize: 64, color: scene.rightLabelColor || "#FFE600", marginBottom: 14 }}>
            {Math.round(rv * grow)}
          </div>
          <div
            style={{
              width: 170,
              height: Math.max(24, rightH),
              borderRadius: "18px 18px 6px 6px",
              background: `linear-gradient(180deg, ${scene.rightLabelColor || "#FFE600"} 0%, rgba(120,53,15,0.85) 100%)`,
              boxShadow: `0 0 36px ${(scene.rightLabelColor || "#FFE600")}77`,
            }}
          />
          <div style={{ marginTop: 18, fontFamily: FONT_BODY, fontSize: 28, color: scene.rightLabelColor || "#FFE600", textAlign: "center" }}>
            {scene.rightLabel || "SAU"}
          </div>
        </div>
      </div>
      <InfoTagsRow tags={scene.infoTags} accent={scene.heroColor || "#FFE600"} top={1245} />
    </AbsoluteFill>
  );
};

const SceneArchivalProof: React.FC<{ scene: UniversalSceneSpec }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: frame - 3, fps, config: { damping: 13, stiffness: 150 } });
  const stampPop = spring({ frame: frame - 16, fps, config: { damping: 10, stiffness: 280 } });
  const scanY = interpolate(frame % 60, [0, 60], [0, 620]);

  return (
    <AbsoluteFill>
      <WatermarkYear text={scene.yearWatermark} />
      <ImpactHook eyebrow={scene.eyebrow} heroText={scene.heroText} heroColor={scene.heroColor} />
      <div
        style={{
          position: "absolute",
          top: 480,
          left: 80,
          right: 80,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          transform: `perspective(1200px) rotateY(-6deg) rotateX(4deg) scale(${interpolate(pop, [0, 1], [0.85, 1])})`,
          opacity: pop,
          zIndex: 14,
        }}
      >
        <div
          style={{
            position: "relative",
            width: 840,
            height: 640,
            borderRadius: 20,
            overflow: "hidden",
            border: "3px solid rgba(250,204,21,0.65)",
            boxShadow: "0 36px 72px rgba(0,0,0,0.95)",
            background: "#0b1120",
          }}
        >
          {scene.primaryAsset ? (
            <Img src={staticFile(scene.primaryAsset)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          ) : null}
          <div
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              top: scanY,
              height: 4,
              background: "linear-gradient(90deg, transparent, #ff3b47, transparent)",
              boxShadow: "0 0 18px #ff3b47",
            }}
          />
          <div
            style={{
              position: "absolute",
              right: 36,
              bottom: 36,
              padding: "10px 26px",
              border: "5px solid #ff3b47",
              borderRadius: 10,
              fontFamily: FONT_HEADING,
              fontSize: 34,
              color: "#ff3b47",
              background: "rgba(10,10,14,0.82)",
              transform: `rotate(-12deg) scale(${interpolate(stampPop, [0, 1], [2.2, 1])})`,
              opacity: stampPop,
            }}
          >
            {scene.stampText || "XÁC THỰC 100%"}
          </div>
        </div>
      </div>
      <InfoTagsRow tags={scene.infoTags} accent={scene.heroColor || "#ff3b47"} top={1180} />
    </AbsoluteFill>
  );
};

const SceneCausalChain: React.FC<{ scene: UniversalSceneSpec }> = ({ scene }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const accent = scene.heroColor || "#42B2F2";
  const steps = (scene.chainSteps && scene.chainSteps.length > 0)
    ? scene.chainSteps.slice(0, 3)
    : (scene.infoTags || []).slice(0, 3).map((t, i) => ({
        badge: `BƯỚC 0${i + 1}`,
        title: String(t),
        detail: "",
      }));

  return (
    <AbsoluteFill>
      <WatermarkYear text={scene.yearWatermark} />
      <ImpactHook
        eyebrow={scene.eyebrow}
        heroText={scene.heroText}
        heroColor={scene.heroColor}
        subNote={scene.subNote}
      />
      {scene.primaryAsset ? (
        <Img
          src={staticFile(scene.primaryAsset)}
          style={{
            position: "absolute",
            top: 480,
            left: "50%",
            width: 720,
            height: 720,
            marginLeft: -360,
            objectFit: "contain",
            opacity: 0.16,
            filter: "blur(1px) drop-shadow(0 0 28px rgba(66,178,242,0.4))",
            pointerEvents: "none",
            zIndex: 6,
          }}
        />
      ) : null}
      <div
        style={{
          position: "absolute",
          top: 470,
          left: 72,
          right: 72,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 14,
          zIndex: 16,
        }}
      >
        {steps.map((st, idx) => {
          const pop = spring({ frame: frame - (4 + idx * 11), fps, config: { damping: 13, stiffness: 185 } });
          const beamProg = spring({ frame: frame - (10 + idx * 11), fps, config: { damping: 15, stiffness: 140 } });
          const nodeColor = idx === 0 ? "#42B2F2" : idx === 1 ? "#FFE600" : "#FF4D5A";
          const pulseY = ((frame * 2.4 + idx * 14) % 44);
          return (
            <React.Fragment key={idx}>
              <div
                style={{
                  width: "100%",
                  padding: "22px 28px",
                  borderRadius: 22,
                  background: "linear-gradient(135deg, rgba(14,24,46,0.92) 0%, rgba(7,12,24,0.94) 100%)",
                  border: `2.5px solid ${nodeColor}`,
                  boxShadow: `0 0 28px ${nodeColor}38, 0 18px 36px rgba(0,0,0,0.85)`,
                  transform: `translateX(${interpolate(pop, [0, 1], [idx % 2 === 0 ? -90 : 90, 0])}px) scale(${interpolate(pop, [0, 1], [0.88, 1])})`,
                  opacity: pop,
                  display: "flex",
                  alignItems: "center",
                  gap: 20,
                }}
              >
                <div
                  style={{
                    minWidth: 112,
                    padding: "10px 14px",
                    borderRadius: 14,
                    background: nodeColor,
                    color: "#05070B",
                    fontFamily: FONT_HEADING,
                    fontSize: 24,
                    fontWeight: 900,
                    textAlign: "center",
                    letterSpacing: 1,
                  }}
                >
                  {st.badge || `0${idx + 1}`}
                </div>
                <div style={{ flex: 1 }}>
                  <div
                    style={{
                      fontFamily: FONT_HEADING,
                      fontSize: 34,
                      fontWeight: 900,
                      color: "#FFFFFF",
                      lineHeight: 1.15,
                    }}
                  >
                    {String(st.title || "").toUpperCase()}
                  </div>
                  {st.detail ? (
                    <div
                      style={{
                        marginTop: 6,
                        fontFamily: FONT_BODY,
                        fontSize: 24,
                        fontWeight: 700,
                        color: "#CBD5E1",
                        lineHeight: 1.25,
                      }}
                    >
                      {st.detail}
                    </div>
                  ) : null}
                </div>
              </div>
              {idx < steps.length - 1 ? (
                <div
                  style={{
                    position: "relative",
                    width: 6,
                    height: 46,
                    borderRadius: 3,
                    background: `linear-gradient(180deg, ${nodeColor}, ${accent})`,
                    opacity: beamProg,
                    transform: `scaleY(${beamProg})`,
                  }}
                >
                  <div
                    style={{
                      position: "absolute",
                      left: -5,
                      top: pulseY,
                      width: 16,
                      height: 16,
                      borderRadius: "50%",
                      background: "#FFFFFF",
                      boxShadow: `0 0 16px ${nodeColor}`,
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

const SceneMotionGate: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const punch = spring({ frame, fps, config: { damping: 14, stiffness: 220 } });
  const camScale = interpolate(punch, [0, 1], [1.1, 1]);
  const camShiftY = interpolate(punch, [0, 1], [28, 0]);
  const flashOpacity = interpolate(frame, [0, 7], [0.24, 0], { extrapolateRight: "clamp" });
  const exitOpacity = interpolate(
    frame,
    [Math.max(0, durationInFrames - 5), durationInFrames],
    [1, 0.85],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ transform: `translateY(${camShiftY}px) scale(${camScale})`, opacity: exitOpacity }}>
      {children}
      {flashOpacity > 0.01 ? (
        <AbsoluteFill
          style={{
            background: "radial-gradient(circle at 50% 45%, rgba(66,178,242,0.55) 0%, rgba(255,255,255,0.22) 35%, transparent 75%)",
            opacity: flashOpacity,
            pointerEvents: "none",
            zIndex: 40,
          }}
        />
      ) : null}
    </AbsoluteFill>
  );
};

const AtmosphericMotes: React.FC = () => {
  const frame = useCurrentFrame();
  const motes = Array.from({ length: 18 }, (_, i) => {
    const x = ((i * 173) % 1000) + 40;
    const baseY = (i * 251) % 1800;
    const speed = 0.9 + (i % 4) * 0.45;
    const y = (baseY - frame * speed + 1920) % 1920;
    const size = 4 + (i % 4) * 3;
    const alpha = 0.16 + (i % 3) * 0.09;
    return { x, y, size, alpha };
  });
  return (
    <AbsoluteFill style={{ pointerEvents: "none", zIndex: 4 }}>
      {motes.map((m, idx) => (
        <div
          key={idx}
          style={{
            position: "absolute",
            left: m.x,
            top: m.y,
            width: m.size,
            height: m.size,
            borderRadius: "50%",
            background: idx % 3 === 0 ? "#42B2F2" : "#FFFFFF",
            opacity: m.alpha,
            boxShadow: `0 0 ${m.size * 3}px ${idx % 3 === 0 ? "#42B2F2" : "#FFFFFF"}`,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

export const HaDaWhyUniversal9x16: React.FC<HaDaWhyUniversal9x16Props> = ({
  plan = defaultPlan as unknown as UniversalScenePlan,
}) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#04060a" }}>
      <style>{FONT_CSS}</style>
      <HaDaWhyMistBackground intensity={plan.mistIntensity ?? 0.11} />
      <AtmosphericMotes />
      <ChannelWatermark9x16 />

      {plan.scenes.map((scene) => {
        const from = Math.round(scene.startSec * fps);
        const durationInFrames = Math.max(1, Math.round((scene.endSec - scene.startSec) * fps));
        return (
          <Sequence key={scene.id} from={from} durationInFrames={durationInFrames}>
            <SceneMotionGate>
              {scene.layout === "hero_prop" && <SceneHeroProp scene={scene} />}
              {scene.layout === "compare_two" && <SceneCompareTwo scene={scene} />}
              {scene.layout === "sat_map" && <SceneSatMap scene={scene} />}
              {scene.layout === "two_tier" && <SceneTwoTier scene={scene} />}
              {scene.layout === "split_duo" && <SceneSplitDuo scene={scene} />}
              {scene.layout === "stat_odometer" && <SceneStatOdometer scene={scene} />}
              {scene.layout === "bar_compare" && <SceneBarCompare scene={scene} />}
              {scene.layout === "archival_proof" && <SceneArchivalProof scene={scene} />}
              {scene.layout === "causal_chain" && <SceneCausalChain scene={scene} />}
            </SceneMotionGate>
          </Sequence>
        );
      })}

      <KineticWordCaption phrases={plan.captions} placement="bottom" />
    </AbsoluteFill>
  );
};
