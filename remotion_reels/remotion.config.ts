import { Config } from "@remotion/cli/config";
import fs from "fs";
import os from "os";

if (process.platform === "win32") {
  const D_TEMP = "D:\\DuAn_DangLam\\temp";
  if (!fs.existsSync(D_TEMP)) {
    fs.mkdirSync(D_TEMP, { recursive: true });
  }
  process.env.TEMP = D_TEMP;
  process.env.TMP = D_TEMP;
}

const cpuCount = Math.max(1, os.cpus().length);
Config.setChromiumOpenGlRenderer("angle");
Config.setConcurrency(Math.min(6, cpuCount));
Config.setOverwriteOutput(true);
