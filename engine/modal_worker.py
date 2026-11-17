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
        "fastapi[standard]",
        "google-genai",
        "vieneu",
        "edge-tts",
        "rembg[gpu]",
        "onnxruntime-gpu",
        "opencv-python-headless",
        "numpy",
        "pillow",
        "requests",
    )
)


@app.function(
    image=image,
    gpu="T4",
    cpu=4.0,
    memory=8192,
    timeout=1800,
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
    gh_models_token: str = "",
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
    env["PYTHONUNBUFFERED"] = "1"
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
    if gh_models_token:
        env["GH_MODELS_TOKEN"] = gh_models_token
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


@app.function(
    image=image,
    secrets=[modal.Secret.from_name("hadawhy-secrets")],
    cpu=0.5,
    memory=512,
    timeout=30,
)
@modal.fastapi_endpoint(method="POST")
def telegram_webhook(payload: dict) -> dict:
    """2-way Telegram Bot Webhook on Modal (Scale-to-zero, instant reply + spawns T4 GPU video job)."""
    import urllib.parse
    import urllib.request

    msg = payload.get("message") or payload.get("edited_message") or {}
    chat_id = str((msg.get("chat") or {}).get("id") or "").strip()
    text = str(msg.get("text") or "").strip()
    if not chat_id or not text:
        return {"ok": True}

    allowed_chat = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()

    def reply(txt: str) -> None:
        if not tg_token:
            return
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": txt[:4000]}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{tg_token}/sendMessage", data=data)
        try:
            urllib.request.urlopen(req, timeout=10).read()
        except Exception as exc:
            print(f"[TG-REPLY] Error: {exc}")

    if allowed_chat and chat_id != allowed_chat:
        return {"ok": True, "ignored": True}

    low = text.lower()
    if low in ("/start", "/help", "/status", "help", "menu"):
        reply(
            "🤖 TRỢ LÝ VIDEO HADA WHY (MODAL T4 GPU)\n"
            "• Nhắn thẳng chủ đề bất kỳ (hoặc /auto <chủ đề>) → Tự viết kịch bản, tự code TSX, tự soi Vision & render 60fps gửi về đây.\n"
            "• /create <chủ đề> → Tạo kịch bản + ảnh preview trước.\n"
            "• /revise <góp ý> → Sửa kịch bản theo góp ý.\n"
            "• /render → Render MP4 từ kịch bản đã tạo."
        )
        return {"ok": True}

    mode = "auto"
    feedback = text
    if low.startswith("/create"):
        mode = "create"
        feedback = text[len("/create"):].strip()
    elif low.startswith("/revise"):
        mode = "revise"
        feedback = text[len("/revise"):].strip()
    elif low.startswith("/render"):
        mode = "render"
        feedback = ""
    elif low.startswith("/auto"):
        mode = "auto"
        feedback = text[len("/auto"):].strip()

    if mode in ("auto", "create", "revise") and not feedback:
        reply(f"⚠️ Thiếu nội dung cho lệnh /{mode}. Ví dụ: /{mode} Tại sao nước đóng chai đắt hơn xăng, làm 20s")
        return {"ok": True}

    run_pipeline_gpu.spawn(
        mode=mode,
        feedback=feedback,
        github_token=os.getenv("GH_PAT", ""),
        openrouter_key=os.getenv("OPENROUTER_API_KEY", ""),
        gemini_key=os.getenv("GEMINI_API_KEY", ""),
        deepseek_key=os.getenv("DEEPSEEK_API_KEY", ""),
        serper_key=os.getenv("SERPER_API_KEY", ""),
        gh_models_token=os.getenv("GH_MODELS_TOKEN", ""),
        tg_token=tg_token,
        tg_chat_id=chat_id,
    )

    if mode == "render":
        reply("🎬 Đã nhận lệnh RENDER! Đang chạy trên Modal T4 GPU, xong sẽ gửi Video + Thumbnail + 3 Tiêu đề SEO về đây.")
    elif mode == "create":
        reply(f"📝 Đã nhận lệnh TẠO KỊCH BẢN:\n\"{feedback}\"\nĐang xử lý trên Modal GPU...")
    elif mode == "revise":
        reply(f"✏️ Đã nhận góp ý sửa:\n\"{feedback}\"\nĐang cập nhật...")
    else:
        reply(f"🚀 Đã nhận chủ đề:\n\"{feedback}\"\nĐang chạy quy trình 5 bước trên Modal T4 GPU (~2–4 phút), xong sẽ gửi Video + Thumbnail + 3 Tiêu đề SEO về đây!")

    return {"ok": True, "spawned": mode}


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
        gh_models_token=os.getenv("GH_MODELS_TOKEN", ""),
        tg_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        tg_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
    )
    if rc != 0:
        raise SystemExit(rc)
