import { continueRender, delayRender, staticFile } from "remotion";

/**
 * Self-loading fonts for every FX primitive, so no component can ever fall back
 * to a system font (broken Vietnamese diacritics) even if a composition forgets @font-face.
 */
const FX_FONTS: Array<[string, string]> = [
  ["BeVietnamProBlack", "fonts/BeVietnamPro-Black.ttf"],
  ["BeVietnamProExtraBold", "fonts/BeVietnamPro-ExtraBold.ttf"],
  ["KanitBlack", "fonts/Kanit-Black.ttf"],
];

let loaded = false;

export const ensureFxFonts = (): void => {
  if (loaded || typeof document === "undefined") return;
  loaded = true;
  const handle = delayRender("Loading FX fonts");
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
