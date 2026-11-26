import { Easing, interpolate } from "remotion";

/**
 * Đường cong Graph Editor chuẩn After Effects (60fps mượt, dứt khoát, không nảy nhựa).
 */
export const AE_SNAP_OUT = Easing.bezier(0.16, 1, 0.3, 1);
export const AE_PUNCH_OUT = Easing.bezier(0.22, 1, 0.36, 1);
export const AE_WHIP_TRANSITION = Easing.bezier(0.76, 0, 0.24, 1);

export const SPRING_SNAPPY = {
  damping: 24,
  stiffness: 260,
  mass: 0.8,
} as const;

export const SPRING_HEAVY_SLAM = {
  damping: 20,
  stiffness: 320,
  mass: 1.0,
} as const;

/**
 * Micro-motion giữ khung hình luôn sống ở 60fps (dùng cho translate3d & rotate).
 */
export function getAliveFloat(
  frame: number,
  fps: number = 60,
  ampY: number = 6,
  ampRot: number = 0.8,
): { y: number; rot: number } {
  const t = frame / Math.max(1, fps);
  return {
    y: Math.sin(t * 2.1) * ampY,
    rot: Math.cos(t * 1.6) * ampRot,
  };
}

/**
 * Ken Burns zoom mượt trên GPU cho ảnh/thẻ trong suốt thời lượng cảnh.
 */
export function getKenBurnsScale(
  localFrame: number,
  durationInFrames: number,
  fromScale: number = 1.0,
  toScale: number = 1.06,
): number {
  return interpolate(
    localFrame,
    [0, Math.max(1, durationInFrames)],
    [fromScale, toScale],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );
}

/**
 * Độ trễ lệch nhịp (stagger 3-5 frames) giữa Tiêu đề -> Ảnh/Đạo cụ -> Số liệu.
 */
export function getStaggerDelay(index: number, stepFrames: number = 4): number {
  return Math.max(0, index) * stepFrames;
}
