import { Config } from "@remotion/cli/config";
import fs from "fs";

const D_TEMP = "D:\\DuAn_DangLam\\temp";
if (!fs.existsSync(D_TEMP)) {
  fs.mkdirSync(D_TEMP, { recursive: true });
}
process.env.TEMP = D_TEMP;
process.env.TMP = D_TEMP;

Config.setChromiumOpenGlRenderer("angle");
Config.setConcurrency(6);
Config.setOverwriteOutput(true);
