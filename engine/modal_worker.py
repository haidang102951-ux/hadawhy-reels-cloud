#!/usr/bin/env python3
"""
HaDa Why GPU Worker on Modal (T4 GPU, ~1.5-2.5 min/video).
Invoked automatically by GitHub Actions when MODAL_TOKEN_ID & MODAL_TOKEN_SECRET are set:
  modal run engine/modal_worker.py --mode auto --feedback "..."
"""

from __future__ import annotations

import os
import subprocess
import sys

import modal

app = modal.App("hadawhy-reels-gpu")

CACHE_VOL = modal.Volume.from_name("hadawhy-models-cache", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        "git",
        "ffmpeg",
        "curl",
        "ca-certificates",
        "libnss3",
        "libatk1.0-0",
        "libatk-bridge2.0-0",
        "libcups2",
        "libdrm2",
        "libxkbcommon0",
        "libxcomposite1",
        "libxdamage1",
        "libxfixes3",
        "libxrandr2",
        "libgbm1",
        "libasound2",
    )
    .run_commands(
        "curl -fsSL https://deb.nodesource.com/setup_20.x | bash -",
        "apt-get install -y nodejs",
    )
    .pip_install(
        "google-genai",
        "vieneu",
        "edge-tts",
        "rembg[cpu]",
        "pillow",
        "requests",
    )
)


@app.function(
    image=image,
    gpu="T4",
    cpu=4.0,
    memory=8192,
    timeout=900,
    volumes={"/cache": CACHE_VOL},
)
def run_pipeline_gpu(
    mode: str,
    feedback: str,
    github_token: str = "",
    openrouter_key: str = "",
    gemini_key: str = "",
    deepseek_key: str = "",
    serper_key: str = "",
    tg_token: str = "",
    tg_chat_id: str = "",
) -> int:
    repo_dir = "/tmp/hadawhy-reels-cloud"
    auth_prefix = f"x-access-token:{github_token}@" if github_token else ""
    clone_url = f"https://{auth_prefix}github.com/haidang102951-ux/hadawhy-reels-cloud.git"
    if os.path.exists(repo_dir):
        subprocess.run(["git", "-C", repo_dir, "pull", "--ff-only"], check=False)
    else:
        subprocess.run(
            ["git", "clone", "--depth", "1", clone_url, repo_dir],
            check=True,
        )

    remotion_dir = os.path.join(repo_dir, "remotion_reels")
    if not os.path.exists(os.path.join(remotion_dir, "node_modules")):
        subprocess.run(["npm", "install"], cwd=remotion_dir, check=True)

    env = os.environ.copy()
    env["HF_HOME"] = "/cache/huggingface"
    env["U2NET_HOME"] = "/cache/u2net"
    if openrouter_key:
        env["OPENROUTER_API_KEY"] = openrouter_key
    if gemini_key:
        env["GEMINI_API_KEY"] = gemini_key
    if deepseek_key:
        env["DEEPSEEK_API_KEY"] = deepseek_key
    if serper_key:
        env["SERPER_API_KEY"] = serper_key
    if tg_token:
        env["TELEGRAM_BOT_TOKEN"] = tg_token
    if tg_chat_id:
        env["TELEGRAM_CHAT_ID"] = tg_chat_id

    proc = subprocess.run(
        [sys.executable, "engine/cloud_reels_runner.py", "--mode", mode, "--feedback", feedback],
        cwd=repo_dir,
        env=env,
    )
    CACHE_VOL.commit()
    return proc.returncode


@app.local_entrypoint()
def main(mode: str = "auto", feedback: str = "") -> None:
    rc = run_pipeline_gpu.remote(
        mode=mode,
        feedback=feedback,
        github_token=os.getenv("GITHUB_TOKEN", ""),
        openrouter_key=os.getenv("OPENROUTER_API_KEY", ""),
        gemini_key=os.getenv("GEMINI_API_KEY", ""),
        deepseek_key=os.getenv("DEEPSEEK_API_KEY", ""),
        serper_key=os.getenv("SERPER_API_KEY", ""),
        tg_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        tg_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
    )
    if rc != 0:
        raise SystemExit(rc)
