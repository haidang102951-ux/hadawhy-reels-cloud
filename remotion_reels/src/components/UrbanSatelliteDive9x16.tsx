import React from "react";
import {
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export interface RealEstatePinSpec {
  label: string;
  value?: string;
  image?: string;
  xPercent: number; // 15..85 on map canvas
  yPercent: number; // 20..80 on map canvas
  color?: string;
  startFrame?: number;
}

export type MapOverlayMode = "pins" | "route" | "radius_zone" | "hex_grid" | "clean_highlight";

export interface RealEstateSatelliteDiveProps {
  locationName: string;
  zoneLabel: string;
  zoneMetric: string; // e.g. "5 KM² • X2.0 GIÁ" or "1.200 M² • 150 TỶ"
  mapImageSrc?: string; // Ảnh bản đồ/vệ tinh thật cào riêng theo địa danh kịch bản
  satelliteBgSrc?: string; // Alias tương thích ngược
  overlayMode?: MapOverlayMode; // Mặc định "pins"; chỉ bật "hex_grid" khi kịch bản nói về lưới lục giác
  zoneColor?: string;
  routePoints?: { x: number; y: number }[]; // Normalized 0..1000 canvas points
  routeDistanceLabel?: string;
  pins?: RealEstatePinSpec[];
  durationFrames: number;
}

/**
 * UrbanSatelliteDive9x16 — Bản đồ Vệ tinh 3D phong cách Bất động sản cao cấp
 * Nằm gọn trong Sân khấu tầng giữa (Y: 480..1540px) trên nền <HaDaWhyMistBackground />:
 * 1. Camera bay bổ nhào nghiêng 3D (Pitch 42° -> 56°, Rotate Bearing -12° -> +10°, Zoom 0.86 -> 1.14).
 * 2. Khoanh ranh giới khu đất / vùng nóng nổi khối 3D (Extruded Parcel / Hex Polygon + mặt phủ bán trong suốt + nhãn nổi ở tâm).
 * 3. Tia dẫn đường chạy dọc trục đường thật (Animated Route Line + nhãn khoảng cách).
 * 4. Chân ghim 3D cắm vuông góc xuống mặt đất bung thẻ ảnh thật (--no-rim).
 */
export const UrbanSatelliteDive9x16: React.FC<RealEstateSatelliteDiveProps> = ({
  locationName,
  zoneLabel,
  zoneMetric,
  mapImageSrc,
  satelliteBgSrc,
  overlayMode = "pins",
  zoneColor = "#FF3B47",
  routePoints = [
    { x: 180, y: 690 },
    { x: 370, y: 540 },
    { x: 520, y: 460 },
    { x: 760, y: 310 },
  ],
  routeDistanceLabel,
  pins = [],
  durationFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const diveSpring = spring({
    frame,
    fps,
    config: { damping: 16, stiffness: 80, mass: 1.1 },
  });

  const pitchDeg = interpolate(frame, [0, durationFrames], [38, 54], {
    extrapolateRight: "clamp",
  });
  const rotateZDeg = interpolate(frame, [0, durationFrames], [-9, 7], {
    extrapolateRight: "clamp",
  });
  const zoomScale = interpolate(frame, [0, durationFrames], [0.92, 1.12], {
    extrapolateRight: "clamp",
  });

  const polyProgress = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const routeProgress = interpolate(frame, [10, 48], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const routePathD =
    routePoints.length >= 2
      ? routePoints
          .map((pt, idx) => `${idx === 0 ? "M" : "L"} ${pt.x} ${pt.y}`)
          .join(" ")
      : "M 200 680 L 480 480 L 780 300";

  const activeBgSrc = mapImageSrc || satelliteBgSrc;
  const resolvedSatSrc = activeBgSrc
    ? activeBgSrc.startsWith("http") || activeBgSrc.startsWith("/")
      ? activeBgSrc
      : staticFile(activeBgSrc)
    : undefined;

  return (
    <div
      style={{
        position: "absolute",
        left: 48,
        top: 475,
        width: 984,
        height: 1030,
        perspective: "1350px",
        zIndex: 25,
      }}
    >
      {/* Top Location Coordinate Telemetry Bar */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 14,
          padding: "10px 22px",
          borderRadius: 16,
          background: "rgba(7, 15, 30, 0.88)",
          border: "2px solid rgba(66, 178, 242, 0.55)",
          boxShadow: "0 14px 28px rgba(0, 0, 0, 0.85)",
        }}
      >
        <div
          style={{
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: 26,
            color: "#42B2F2",
            letterSpacing: "0.04em",
          }}
        >
          ◉ VỆ TINH 3D • {locationName.toUpperCase()}
        </div>
        <div
          style={{
            fontFamily: "KanitBlack, sans-serif",
            fontSize: 26,
            color: "#FFE600",
          }}
        >
          {zoneLabel.toUpperCase()}
        </div>
      </div>

      {/* 3D Tilted Real-Estate Satellite Terrain Slab */}
      <div
        style={{
          position: "relative",
          width: 984,
          height: 820,
          borderRadius: 28,
          overflow: "hidden",
          background:
            "radial-gradient(circle at 50% 45%, #0E223D 0%, #06101E 75%, #030710 100%)",
          border: "3px solid rgba(66, 178, 242, 0.65)",
          boxShadow:
            "0 36px 70px rgba(0, 0, 0, 0.95), inset 0 0 60px rgba(0, 0, 0, 0.85)",
          transform: `scale(${interpolate(diveSpring, [0, 1], [0.85, 1])})`,
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: -80,
            transformStyle: "preserve-3d",
            transform: `rotateX(${pitchDeg}deg) rotateZ(${rotateZDeg}deg) scale(${zoomScale})`,
            transformOrigin: "50% 52%",
          }}
        >
          {resolvedSatSrc ? (
            <Img
              src={resolvedSatSrc}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "brightness(0.92) contrast(1.14) saturate(1.12)",
              }}
            />
          ) : null}

          {/* Urban Road Grid & 3D Extruded Parcel / Hex Zone SVG */}
          <svg
            viewBox="0 0 1000 900"
            style={{
              position: "absolute",
              inset: 0,
              width: "100%",
              height: "100%",
            }}
          >
            {/* Subtle Cadastral Road Grid */}
            <g stroke="rgba(66, 178, 242, 0.18)" strokeWidth={1.5}>
              {[150, 300, 450, 600, 750].map((v) => (
                <React.Fragment key={v}>
                  <line x1={v} y1={0} x2={v} y2={900} />
                  <line x1={0} y1={v} x2={1000} y2={v} />
                </React.Fragment>
              ))}
            </g>

            {/* Overlay động theo overlayMode (mặc định "pins", chỉ bật hex_grid khi kịch bản yêu cầu) */}
            {overlayMode === "hex_grid" && (
              <g stroke="rgba(34, 211, 238, 0.45)" strokeWidth={2.5} fill="rgba(34, 211, 238, 0.08)">
                {[
                  { cx: 500, cy: 420 },
                  { cx: 360, cy: 340 },
                  { cx: 640, cy: 340 },
                  { cx: 360, cy: 500 },
                  { cx: 640, cy: 500 },
                ].map((h, hi) => {
                  const pts = Array.from({ length: 6 })
                    .map((_, pi) => {
                      const a = (pi * 60 * Math.PI) / 180;
                      return `${h.cx + 88 * Math.cos(a)},${h.cy + 88 * Math.sin(a)}`;
                    })
                    .join(" ");
                  return <polygon key={`hx-${hi}`} points={pts} />;
                })}
              </g>
            )}

            {overlayMode === "radius_zone" && (
              <g>
                <circle cx={500} cy={430} r={220 * polyProgress} fill="rgba(255, 59, 71, 0.2)" stroke={zoneColor} strokeWidth={5} />
                <circle cx={500} cy={430} r={120 * polyProgress} fill="none" stroke="#FFE600" strokeWidth={3} strokeDasharray="10 8" />
              </g>
            )}

            {(overlayMode === "clean_highlight" || overlayMode === "pins" || overlayMode === "route") && (
              <>
                {/* 3D Extruded Parcel Base Shadow & Side Wall */}
                <polygon
                  points="500,245 690,340 650,555 360,575 310,365"
                  fill="rgba(0, 0, 0, 0.55)"
                  transform="translate(0, 22)"
                />
                <polygon
                  points="500,245 690,340 650,555 360,575 310,365"
                  fill={zoneColor === "#FF3B47" ? "rgba(255, 59, 71, 0.26)" : "rgba(66, 178, 242, 0.26)"}
                  stroke={zoneColor}
                  strokeWidth={7}
                  strokeLinejoin="round"
                  pathLength={1}
                  strokeDasharray={1}
                  strokeDashoffset={1 - polyProgress}
                />
              </>
            )}

            {/* Animated Turf Route Along Real Road Axis */}
            <path
              d={routePathD}
              fill="none"
              stroke="rgba(255, 230, 0, 0.28)"
              strokeWidth={12}
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d={routePathD}
              fill="none"
              stroke="#FFE600"
              strokeWidth={7}
              strokeLinecap="round"
              strokeLinejoin="round"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - routeProgress}
            />
          </svg>
        </div>

        {/* Floating Parcel Metric Badge (Đẩy xuống dưới cụm lục giác +32px để viền không bao giờ cắt chữ) */}
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: "76%",
            transform: `translate(-50%, -50%) scale(${interpolate(polyProgress, [0, 1], [0.85, 1])})`,
            opacity: polyProgress,
            padding: "10px 26px",
            borderRadius: 14,
            background: "rgba(5, 10, 22, 0.95)",
            border: `2.5px solid ${zoneColor}`,
            boxShadow: "0 18px 36px rgba(0, 0, 0, 0.95)",
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontFamily: "KanitBlack, sans-serif",
              fontSize: zoneMetric.length > 14 ? 36 : 46,
              color: "#FFE600",
              WebkitTextStroke: "6px #05070C",
              paintOrder: "stroke fill",
              lineHeight: 1.05,
              whiteSpace: "nowrap",
            }}
          >
            {zoneMetric}
          </div>
        </div>

        {/* Route Distance Badge */}
        {routeDistanceLabel && routeProgress > 0.4 && (
          <div
            style={{
              position: "absolute",
              right: 28,
              bottom: 24,
              padding: "10px 22px",
              borderRadius: 14,
              background: "rgba(5, 10, 22, 0.92)",
              border: "2px solid #FFE600",
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 26,
              color: "#FFFFFF",
              boxShadow: "0 12px 24px rgba(0,0,0,0.9)",
            }}
          >
            TUYẾN ĐƯỜNG: <span style={{ color: "#FFE600" }}>{routeDistanceLabel}</span>
          </div>
        )}

        {/* 3D Ground Pins Anchored to Map with Real Cutout Photos */}
        {pins.map((pin, idx) => {
          const pStart = pin.startFrame ?? 25 + idx * 22;
          const pPop = spring({
            frame: Math.max(0, frame - pStart),
            fps,
            config: { damping: 12, stiffness: 180 },
          });
          if (frame < pStart) return null;
          const pinImg = pin.image
            ? pin.image.startsWith("http") || pin.image.startsWith("/")
              ? pin.image
              : staticFile(pin.image)
            : undefined;
          return (
            <div
              key={idx}
              style={{
                position: "absolute",
                left: `${pin.xPercent}%`,
                top: `${pin.yPercent}%`,
                transform: `translate(-50%, -100%) scale(${pPop})`,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                zIndex: 30 + idx,
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 12,
                  padding: "10px 16px",
                  borderRadius: 18,
                  background: "rgba(6, 13, 26, 0.94)",
                  border: `3px solid ${pin.color ?? "#42B2F2"}`,
                  boxShadow: "0 18px 34px rgba(0, 0, 0, 0.95)",
                }}
              >
                {pinImg && (
                  <Img
                    src={pinImg}
                    style={{
                      width: 74,
                      height: 74,
                      objectFit: "contain",
                      filter: "drop-shadow(0 8px 12px rgba(0,0,0,0.85))",
                    }}
                  />
                )}
                <div>
                  <div
                    style={{
                      fontFamily: "BeVietnamProBlack, sans-serif",
                      fontSize: 22,
                      color: "#FFFFFF",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {pin.label}
                  </div>
                  {pin.value && (
                    <div
                      style={{
                        fontFamily: "KanitBlack, sans-serif",
                        fontSize: 30,
                        color: pin.color ?? "#FFE600",
                        lineHeight: 1.05,
                      }}
                    >
                      {pin.value}
                    </div>
                  )}
                </div>
              </div>
              {/* Vertical 3D Ground Stem + Target Ring */}
              <div
                style={{
                  width: 4,
                  height: 36,
                  background: pin.color ?? "#42B2F2",
                  boxShadow: "0 4px 10px rgba(0,0,0,0.9)",
                }}
              />
              <div
                style={{
                  width: 18,
                  height: 18,
                  borderRadius: "50%",
                  background: "#FFFFFF",
                  border: `4px solid ${pin.color ?? "#42B2F2"}`,
                }}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};
