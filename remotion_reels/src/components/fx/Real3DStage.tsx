import React, { useEffect, useMemo, useState } from "react";
import { ThreeCanvas } from "@remotion/three";
import { useThree } from "@react-three/fiber";
import * as THREE from "three";
import {
  continueRender,
  delayRender,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

/* ------------------------------------------------------------------ */
/*  Shared camera rig: same math used inside the canvas and for HTML   */
/*  label projection, so overlays stay glued to the 3D objects.        */
/* ------------------------------------------------------------------ */
export interface OrbitParams {
  radius: number;
  height: number;
  startAngleDeg: number;
  sweepDeg: number;
  durationFrames: number;
  target?: [number, number, number];
  fov?: number;
}

export const orbitCameraPosition = (rel: number, p: OrbitParams): THREE.Vector3 => {
  const t = Math.min(1, Math.max(0, rel / p.durationFrames));
  const eased = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  const ang = THREE.MathUtils.degToRad(p.startAngleDeg + p.sweepDeg * eased);
  return new THREE.Vector3(Math.sin(ang) * p.radius, p.height, Math.cos(ang) * p.radius);
};

const CameraRig: React.FC<{ rel: number; orbit: OrbitParams }> = ({ rel, orbit }) => {
  const { camera } = useThree();
  const pos = orbitCameraPosition(rel, orbit);
  const target = orbit.target ?? [0, 0, 0];
  camera.position.copy(pos);
  camera.lookAt(new THREE.Vector3(...target));
  if ((camera as THREE.PerspectiveCamera).isPerspectiveCamera) {
    (camera as THREE.PerspectiveCamera).fov = orbit.fov ?? 38;
    (camera as THREE.PerspectiveCamera).updateProjectionMatrix();
  }
  return null;
};

export const projectToScreen = (
  world: [number, number, number],
  rel: number,
  orbit: OrbitParams,
  width: number,
  height: number,
): { x: number; y: number } => {
  const cam = new THREE.PerspectiveCamera(orbit.fov ?? 38, width / height, 0.1, 100);
  cam.position.copy(orbitCameraPosition(rel, orbit));
  cam.lookAt(new THREE.Vector3(...(orbit.target ?? [0, 0, 0])));
  cam.updateMatrixWorld();
  cam.updateProjectionMatrix();
  const v = new THREE.Vector3(...world).project(cam);
  return { x: (v.x * 0.5 + 0.5) * width, y: (-v.y * 0.5 + 0.5) * height };
};

/* ------------------------------------------------------------------ */
/*  Texture loader that blocks rendering until the image is ready      */
/* ------------------------------------------------------------------ */
const useRemotionTexture = (src: string): THREE.Texture | null => {
  const [tex, setTex] = useState<THREE.Texture | null>(null);
  const [handle] = useState(() => delayRender(`texture ${src}`));
  useEffect(() => {
    new THREE.TextureLoader().load(
      staticFile(src),
      (t) => {
        t.colorSpace = THREE.SRGBColorSpace;
        t.anisotropy = 8;
        setTex(t);
        continueRender(handle);
      },
      undefined,
      () => continueRender(handle),
    );
  }, [src, handle]);
  return tex;
};

/* ------------------------------------------------------------------ */
/*  Real3DPhotoStage: real cutout photo standing in true 3D space,     */
/*  real shadow on floor, coloured rim light, orbiting camera.         */
/* ------------------------------------------------------------------ */
export const Real3DPhotoStage: React.FC<{
  cutoutSrc: string;
  aspect?: number; // image width / height
  startFrame?: number;
  orbit?: Partial<OrbitParams>;
  rimColor?: string;
  keyColor?: string;
  floorShadowOpacity?: number;
  width?: number;
  height?: number;
  children?: (rel: number, orbit: OrbitParams) => React.ReactNode; // HTML overlays (labels)
}> = ({
  cutoutSrc,
  aspect = 1,
  startFrame = 0,
  orbit: orbitIn,
  rimColor = "#F59E0B",
  keyColor = "#FFFFFF",
  floorShadowOpacity = 0.45,
  width = 1080,
  height = 1920,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const tex = useRemotionTexture(cutoutSrc);
  const orbit: OrbitParams = {
    radius: 6.2,
    height: 1.4,
    startAngleDeg: -28,
    sweepDeg: 56,
    durationFrames: 240,
    target: [0, 1.0, 0],
    fov: 38,
    ...orbitIn,
  };

  const rise = spring({ frame: rel, fps, config: { damping: 15, stiffness: 120, mass: 0.9 } });
  // Auto-fit: object always fits inside the portrait viewport (78% of visible width, 42% of visible height)
  const vfov = THREE.MathUtils.degToRad(orbit.fov ?? 38);
  const visibleH = 2 * orbit.radius * Math.tan(vfov / 2);
  const visibleW = visibleH * (width / height);
  const objW = Math.min(visibleW * 0.78, visibleH * 0.42 * aspect);
  const objH = objW / aspect;
  // Keep the object vertically centred unless the caller sets its own camera target
  if (!orbitIn?.target) orbit.target = [0, objH / 2, 0];
  const y = interpolate(rise, [0, 1], [-1.6, objH / 2]) + Math.sin(rel * 0.05) * 0.05;

  const depthMat = useMemo(
    () =>
      tex
        ? new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: tex, alphaTest: 0.5 })
        : undefined,
    [tex],
  );

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <ThreeCanvas width={width} height={height} shadows="soft" gl={{ antialias: true, alpha: true }}>
        <CameraRig rel={rel} orbit={orbit} />
        <ambientLight intensity={0.35} />
        <directionalLight
          position={[3.5, 6, 4]}
          intensity={2.2}
          color={keyColor}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
          shadow-camera-left={-5}
          shadow-camera-right={5}
          shadow-camera-top={5}
          shadow-camera-bottom={-5}
        />
        <pointLight position={[-3, 2.5, -2.5]} intensity={18} color={rimColor} distance={12} />
        <pointLight position={[3, 2.0, -2.5]} intensity={10} color={rimColor} distance={12} />
        {tex && (
          <mesh position={[0, y, 0]} castShadow customDepthMaterial={depthMat}>
            <planeGeometry args={[objW, objH]} />
            <meshStandardMaterial map={tex} transparent alphaTest={0.08} side={THREE.DoubleSide} roughness={0.55} metalness={0.05} />
          </mesh>
        )}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
          <planeGeometry args={[30, 30]} />
          <shadowMaterial opacity={floorShadowOpacity} />
        </mesh>
      </ThreeCanvas>
      {children ? children(rel, orbit) : null}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/*  DataBars3D: real lit 3D bars rising, camera orbit, HTML labels     */
/*  projected from 3D so numbers stay anchored to each bar.            */
/* ------------------------------------------------------------------ */
export interface Bar3D {
  label: string;
  value: number;
  color: string;
  display?: string;
}

export const DataBars3D: React.FC<{
  bars: Bar3D[];
  startFrame?: number;
  staggerFrames?: number;
  maxHeight?: number;
  orbit?: Partial<OrbitParams>;
  width?: number;
  height?: number;
  labelFont?: string;
}> = ({
  bars,
  startFrame = 0,
  staggerFrames = 10,
  maxHeight = 3.2,
  orbit: orbitIn,
  width = 1080,
  height = 1920,
  labelFont = "'KanitBlack', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const gap = 1.25;
  const span = (bars.length - 1) * gap + 0.8;
  // Auto-fit camera distance so every bar + label fits the portrait frame
  const fovDeg = orbitIn?.fov ?? 40;
  const fitRadius = span / (0.72 * 2 * Math.tan(THREE.MathUtils.degToRad(fovDeg) / 2) * (width / height));
  const orbit: OrbitParams = {
    radius: Math.max(8, fitRadius),
    height: 3.2,
    startAngleDeg: -30,
    sweepDeg: 34,
    durationFrames: 300,
    target: [0, 1.4, 0],
    fov: fovDeg,
    ...orbitIn,
  };
  const maxVal = Math.max(...bars.map((b) => b.value), 1);
  const x0 = -((bars.length - 1) * gap) / 2;

  const heights = bars.map((b, i) => {
    const s = spring({ frame: rel - i * staggerFrames, fps, config: { damping: 16, stiffness: 110, mass: 0.9 } });
    return Math.max(0.02, (b.value / maxVal) * maxHeight * s);
  });

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <ThreeCanvas width={width} height={height} shadows="soft" gl={{ antialias: true, alpha: true }}>
        <CameraRig rel={rel} orbit={orbit} />
        <ambientLight intensity={0.4} />
        <directionalLight
          position={[1.5, 10, 7]}
          intensity={2.4}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
          shadow-camera-left={-10}
          shadow-camera-right={10}
          shadow-camera-top={10}
          shadow-camera-bottom={-10}
          shadow-bias={-0.0002}
          shadow-normalBias={0.02}
        />
        <pointLight position={[-4, 3, -3]} intensity={14} color="#60A5FA" distance={14} />
        {bars.map((b, i) => (
          <mesh key={i} position={[x0 + i * gap, heights[i] / 2, 0]} castShadow receiveShadow>
            <boxGeometry args={[0.8, heights[i], 0.8]} />
            <meshStandardMaterial color={b.color} roughness={0.35} metalness={0.25} emissive={b.color} emissiveIntensity={0.12} />
          </mesh>
        ))}
        <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
          <planeGeometry args={[30, 30]} />
          <shadowMaterial opacity={0.4} />
        </mesh>
      </ThreeCanvas>
      {bars.map((b, i) => {
        const top = projectToScreen([x0 + i * gap, heights[i] + 0.15, 0], rel, orbit, width, height);
        const base = projectToScreen([x0 + i * gap, -0.25, 0.5], rel, orbit, width, height);
        const op = interpolate(rel - i * staggerFrames, [8, 18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        return (
          <React.Fragment key={i}>
            <div
              style={{
                position: "absolute",
                left: top.x,
                top: top.y,
                transform: "translate(-50%, -100%)",
                opacity: op,
                fontFamily: labelFont,
                fontSize: 46,
                fontWeight: 900,
                color: b.color,
                WebkitTextStroke: "2px rgba(0,0,0,0.85)",
                textShadow: "0 6px 18px rgba(0,0,0,0.9)",
                whiteSpace: "nowrap",
              }}
            >
              {b.display ?? b.value.toLocaleString("vi-VN")}
            </div>
            <div
              style={{
                position: "absolute",
                left: base.x,
                top: base.y,
                transform: "translate(-50%, 0)",
                opacity: op,
                fontFamily: "'BeVietnamProExtraBold', sans-serif",
                fontSize: 28,
                color: "#F1F5F9",
                textShadow: "0 4px 14px rgba(0,0,0,0.95)",
                whiteSpace: "nowrap",
              }}
            >
              {b.label}
            </div>
          </React.Fragment>
        );
      })}
    </div>
  );
};
