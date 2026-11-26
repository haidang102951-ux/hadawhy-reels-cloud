import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import { ChannelWatermark9x16 } from "./components/ChannelWatermark9x16";
import { HaDaWhyMistBackground } from "./components/HaDaWhyMistBackground";
import { HaDaWhyOutroCTA } from "./components/HaDaWhyOutroCTA";
import { HaDaWhyFontFaces } from "./components/KineticHookHeader";
import { CameraStageWrapper } from "./components/fx";

export interface RootSkeletonExampleProps {
  audioSrc?: string;
}

/**
 * Khung mẫu kỹ thuật phi chủ đề (60fps, 0% nội dung cụ thể).
 * Tham khảo cú pháp gắn Audio, nền xanh dương ADN, watermark và CameraStageWrapper cho từng Beat.
 */
export const RootSkeletonExample: React.FC<RootSkeletonExampleProps> = ({
  audioSrc,
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#030812", overflow: "hidden" }}>
      <HaDaWhyFontFaces />
      <HaDaWhyMistBackground />

      {audioSrc ? <Audio src={staticFile(audioSrc)} /> : null}

      {/* Beat 1 (60fps): Hiện đầy đủ hình + số ngay trong 0..30 frames đầu */}
      <Sequence from={0} durationInFrames={300}>
        <CameraStageWrapper durationInFrames={300} enterDirection="zoom">
          <AbsoluteFill />
        </CameraStageWrapper>
      </Sequence>

      {/* Beat 2..N: Cắt dứt khoát khớp mốc words.json + 30 frames (0.5s) đệm cuối */}
      <Sequence from={300} durationInFrames={300}>
        <CameraStageWrapper durationInFrames={300} enterDirection="up">
          <AbsoluteFill />
        </CameraStageWrapper>
      </Sequence>

      {/* CTA KẾT VIDEO DUY NHẤT (3.5s cuối = 210 frames @ 60fps, tự khớp 3 mốc SFX) — đặt ngay trước ChannelWatermark9x16 */}
      <HaDaWhyOutroCTA />

      {/* BẮT BUỘC đặt dòng cuối cùng ngay trước </AbsoluteFill> để 2 lớp thương hiệu + chống re-up luôn nổi trên cùng */}
      <ChannelWatermark9x16 />
    </AbsoluteFill>
  );
};
