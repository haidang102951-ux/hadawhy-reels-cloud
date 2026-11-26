import { continueRender, delayRender, staticFile } from "remotion";

/**
 * Khóa 100% font tiếng Việt đầy đủ dấu (BeVietnamPro) cho mọi FX primitive,
 * kể cả alias KanitBlack cũng trỏ về BeVietnamPro-Black.ttf để không bao giờ vỡ dấu Ả, Ẩ, Ỡ.
 */
const FX_FONTS: Array<[string, string]> = [
  ["BeVietnamProBlack", "fonts/BeVietnamPro-Black.ttf"],
  ["BeVietnamProExtraBold", "fonts/BeVietnamPro-ExtraBold.ttf"],
  ["KanitBlack", "fonts/BeVietnamPro-Black.ttf"],
];

let loaded = false;

export const ensureFxFonts = (): void => {
  if (loaded || typeof document === "undefined") return;
  loaded = true;
  const handle = delayRender("Loading FX Vietnamese fonts");
  Promise.all(
    FX_FONTS.map(([family, file]) => {
      const face = new FontFace(family, `url(${staticFile(file)})`, { weight: "100 900" });
      return face.load().then((f) => {
        document.fonts.add(f);
      });
    }),
  )
    .then(() => continueRender(handle))
    .catch((err) => {
      console.error("FX font load failed", err);
      continueRender(handle);
    });
};

ensureFxFonts();
