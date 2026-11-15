import React from "react";
import { Img, staticFile, useCurrentFrame } from "remotion";

export interface ChannelWatermark9x16Props {
  logoSrc?: string;
}

export const ChannelWatermark9x16: React.FC<ChannelWatermark9x16Props> = ({
  logoSrc = "brand/hadawhy_logo.png",
}) => {
  const frame = useCurrentFrame();
  const floatY = Math.sin(frame * 0.025) * 8;

  return (
    <>
      {/* Layer 1: Top-Left Safe Corner Channel Identity inside 9:16 Safe Zone */}
      <div
        style={{
          position: "absolute",
          top: 52,
          left: 40,
          width: 132,
          opacity: 0.9,
          zIndex: 60,
          pointerEvents: "none",
          filter: "drop-shadow(0 3px 10px rgba(0, 0, 0, 0.85))",
        }}
      >
        <Img
          src={staticFile(logoSrc)}
          style={{ width: "100%", height: "auto", display: "block" }}
        />
      </div>

      {/* Layer 2: Subtle Floating Center-Lower Anti-Crop Watermark */}
      <div
        style={{
          position: "absolute",
          left: 540,
          top: 1420 + floatY,
          width: 240,
          transform: "translate(-50%, -50%)",
          opacity: 0.09,
          zIndex: 12,
          pointerEvents: "none",
        }}
      >
        <Img
          src={staticFile(logoSrc)}
          style={{ width: "100%", height: "auto", display: "block" }}
        />
      </div>
    </>
  );
};
