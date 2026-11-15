import React from "react";
import { Composition, Still } from "remotion";
import { PilotCashFlowScene } from "./PilotCashFlowScene";
import { MasterShowcase20s } from "./MasterShowcase20s";
import { NvidiaSuccession40s } from "./NvidiaSuccession40s";
import { Friday13Origins45s } from "./Friday13Origins45s";
import { HaDaWhyUniversal9x16, UniversalScenePlan } from "./HaDaWhyUniversal9x16";
import { DynamicReel } from "./DynamicReel";
import defaultUniversalPlan from "./scene_plan.json";
import { ThumbnailCover9x16 } from "./components/ThumbnailCover9x16";
import { ThumbnailDNAStudy9x16 } from "./components/ThumbnailDNAStudy9x16";

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="PilotCashFlow"
        component={PilotCashFlowScene}
        durationInFrames={444}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="MasterShowcase20s"
        component={MasterShowcase20s}
        durationInFrames={1344}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="NvidiaSuccession40s"
        component={NvidiaSuccession40s}
        durationInFrames={2572}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="Friday13Origins45s"
        component={Friday13Origins45s}
        durationInFrames={2505}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="HaDaWhyUniversal9x16"
        component={HaDaWhyUniversal9x16}
        durationInFrames={1260}
        fps={60}
        width={1080}
        height={1920}
        defaultProps={{
          plan: defaultUniversalPlan as unknown as UniversalScenePlan,
        }}
        calculateMetadata={({ props }) => {
          const p = (props?.plan || defaultUniversalPlan) as unknown as UniversalScenePlan;
          const fps = p.fps || 60;
          const maxEnd = (p.scenes || []).reduce((m, s) => Math.max(m, s.endSec || 0), 10);
          return {
            fps,
            durationInFrames: Math.max(60, Math.round(maxEnd * fps)),
          };
        }}
      />
      <Composition
        id="DynamicReel"
        component={DynamicReel}
        durationInFrames={1260}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          plan: defaultUniversalPlan as unknown as UniversalScenePlan,
        }}
        calculateMetadata={({ props }) => {
          const p = (props?.plan || defaultUniversalPlan) as unknown as UniversalScenePlan;
          const fps = p.fps || 30;
          const maxEnd = (p.scenes || []).reduce((m, s) => Math.max(m, s.endSec || 0), 10);
          return {
            fps,
            durationInFrames: Math.max(60, Math.round(maxEnd * fps)),
          };
        }}
      />
      <Still
        id="ThumbnailCover9x16"
        component={ThumbnailCover9x16}
        width={1080}
        height={1920}
        defaultProps={{
          backgroundPhotoSrc: "harvested/nvidia_empire_tower_real.png",
          backgroundBlurPx: 0,
          backgroundScale: 1.0,
          backgroundObjectPosition: "50% 50%",
          backgroundBrightness: 0.88,
          backgroundContrast: 1.15,
          backgroundSaturate: 1.0,
          heroSubjectSrc: "harvested/jensen_huang_real.png",
          mysteryOrSecondarySrc: "harvested/stephen_neal_real.png",
          headlineLine1: "NGAI VÀNG 3.000 TỶ $:",
          headlineLine2: "AI THAY JENSEN HUANG?",
          brandLogoSrc: "brand/hadawhy_logo.png",
          glowAccentColor: "#E11D2E",
          headlineLine1Color: "#42B2F2",
          headlineLine2Color: "#FFFFFF",
          heroBwHighContrast: true,
          mysterySilhouetteMode: true,
          mysterySymbol: "?",
        }}
      />
      <Still
        id="PreviewDNA1IvoryDossier"
        component={ThumbnailDNAStudy9x16}
        width={1080}
        height={1920}
        defaultProps={{
          variant: "ivory_dossier",
          brandLogoSrc: "brand/hadawhy_logo.png",
          topTag: "HỒ SƠ TỐI MẬT",
          headlineLine1: "NGAI VÀNG 3.000 TỶ $:",
          headlineLine2: "AI THAY JENSEN HUANG?",
          mainSubjectSrc: "harvested/jensen_huang_real.png",
          mysterySilhouetteSrc: "harvested/stephen_neal_real.png",
        }}
      />
      <Still
        id="PreviewDNA2NoirRed"
        component={ThumbnailDNAStudy9x16}
        width={1080}
        height={1920}
        defaultProps={{
          variant: "noir_red",
          brandLogoSrc: "brand/hadawhy_logo.png",
          topTag: "HỒ SƠ TỐI MẬT",
          headlineLine1: "NGAI VÀNG 3.000 TỶ $:",
          headlineLine2: "AI THAY JENSEN HUANG?",
          mainSubjectSrc: "harvested/jensen_huang_real.png",
          mysterySilhouetteSrc: "harvested/stephen_neal_real.png",
        }}
      />
      <Still
        id="PreviewDNA3GraphiteGold"
        component={ThumbnailDNAStudy9x16}
        width={1080}
        height={1920}
        defaultProps={{
          variant: "graphite_gold",
          brandLogoSrc: "brand/hadawhy_logo.png",
          topTag: "HỒ SƠ TỐI MẬT",
          headlineLine1: "NGAI VÀNG 3.000 TỶ $:",
          headlineLine2: "AI THAY JENSEN HUANG?",
          mainSubjectSrc: "harvested/jensen_huang_real.png",
          mysterySilhouetteSrc: "harvested/stephen_neal_real.png",
        }}
      />
    </>
  );
};
