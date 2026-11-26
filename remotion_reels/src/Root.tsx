import React from "react";
import { Composition, Still } from "remotion";
import { ActiveEpisode, ACTIVE_DURATION_FRAMES } from "./ActiveEpisode";
import { ThumbnailCover9x16, ThumbnailCover9x16Props } from "./components/ThumbnailCover9x16";

export const Root: React.FC = () => {
  return (
    <>
      {/* FIXED EPISODE SLOT (1080x1920 @ 60fps) — CẤM AI SỬA Root.tsx KHI LÀM TẬP MỚI */}
      <Composition
        id="ActiveEpisode"
        component={ActiveEpisode}
        durationInFrames={ACTIVE_DURATION_FRAMES}
        fps={60}
        width={1080}
        height={1920}
      />

      {/* 3D THUMBNAIL COVER STILL (1080x1920) */}
      <Still
        id="ThumbnailCover9x16"
        component={ThumbnailCover9x16}
        width={1080}
        height={1920}
        defaultProps={{
          headlineLine1: "BÍ MẬT",
          headlineLine2: "HADA WHY",
          heroSubjectSrc: "brand/hadawhy_logo.png",
        } as ThumbnailCover9x16Props}
      />
    </>
  );
};
