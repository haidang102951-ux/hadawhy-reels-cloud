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
TG_STATE = modal.Dict.from_name("hadawhy-tg-memory", create_if_missing=True)

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
        "libxshmfence1",
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
    motapi_key: str = "",
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
    if motapi_key:
        env["MOTAPI_KEY"] = motapi_key
    if tg_token:
        env["TELEGRAM_BOT_TOKEN"] = tg_token
    if tg_chat_id:
        env["TELEGRAM_CHAT_ID"] = tg_chat_id

    proc = subprocess.run(
        [sys.executable, "engine/cloud_reels_runner.py", "--mode", mode, "--feedback", feedback],
        cwd=repo_dir,
        env=env,
        capture_output=True,
        text=True,
    )
    print(proc.stdout[-3000:] if proc.stdout else "")
    if proc.stderr:
        print(proc.stderr[-2000:])
    if proc.returncode != 0 and tg_token and tg_chat_id:
        import urllib.parse
        import urllib.request
        err_tail = ((proc.stderr or "").strip()[-1800:] or (proc.stdout or "").strip()[-1500:])
        data = urllib.parse.urlencode({"chat_id": tg_chat_id, "text": f"❌ Lỗi khi chạy mode={mode}:\n{err_tail}"[:4000]}).encode()
        try:
            urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tg_token}/sendMessage", data=data), timeout=15).read()
        except Exception:
            pass
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
    update_id = payload.get("update_id")
    chat_id = str((msg.get("chat") or {}).get("id") or "").strip()
    text = str(msg.get("text") or "").strip()
    if not chat_id or not text:
        return {"ok": True}

    # Deduplicate Telegram webhook retries (Telegram resends same update_id if reply >5s)
    if update_id is not None:
        try:
            dedup_key = f"upd_{update_id}"
            if TG_STATE.get(dedup_key):
                return {"ok": True, "dup": True}
            TG_STATE[dedup_key] = True
        except Exception:
            pass

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
    if low in ("/start", "/help", "help", "menu"):
        reply(
            "Ê chào ông! Tôi là trợ lý làm video HaDa Why đây 🎬\n"
            "Ông cứ chat tự nhiên như bạn bè (hỏi ý tưởng, check tiến độ, nhờ góp ý kịch bản), "
            "khi nào chốt thì bảo tôi 'làm video về...' hoặc dùng nhanh:\n"
            "• /auto <chủ đề> — Làm trọn gói từ A-Z\n"
            "• /create <chủ đề> — Viết kịch bản + preview trước\n"
            "• /revise <góp ý> — Sửa kịch bản\n"
            "• /render — Xuất video 60fps"
        )
        return {"ok": True}

    mode = ""
    feedback = ""
    reply_text = ""

    if low.startswith("/create"):
        mode, feedback = "create", text[len("/create"):].strip()
    elif low.startswith("/revise"):
        mode, feedback = "revise", text[len("/revise"):].strip()
    elif low.startswith("/render"):
        mode, feedback = "render", ""
    elif low.startswith("/auto"):
        mode, feedback = "auto", text[len("/auto"):].strip()
    else:
        # Chat tự nhiên như bạn bè bằng Gemini + nhớ ngữ cảnh
        import json
        import time
        import requests  # type: ignore

        history = []
        last_job = {}
        try:
            history = TG_STATE.get(f"hist_{chat_id}", []) or []
            last_job = TG_STATE.get(f"job_{chat_id}", {}) or {}
        except Exception:
            pass

        job_info = ""
        if last_job:
            elapsed = int(time.time() - float(last_job.get("ts", time.time())))
            job_info = f"Job gần nhất: mode={last_job.get('mode')}, topic='{last_job.get('topic')}', đã chạy được {elapsed} giây."

        motapi_keys = [k.strip() for k in os.getenv("MOTAPI_KEY", "").split(",") if k.strip()]
        if motapi_keys:
            sys_prompt = (
                "Bạn là cộng sự thân thiết (nói chuyện tự nhiên như bạn bè, xưng 'tôi/mình' gọi 'ông/bạn', ngắn gọn, thông minh, thẳng thắn, KHÔNG kiểu robot AI) "
                "đang cùng vận hành hệ thống sản xuất video ngắn HaDa Why (@hadawhy).\n\n"
                "THÔNG TIN THẬT VỀ HỆ THỐNG HIỆN TẠI (để trả lời chính xác khi bạn hỏi):\n"
                "- Hạ tầng: Chạy trên Modal T4 GPU (scale-to-zero, không cần mở máy tính).\n"
                "- Não AI: Dùng MotAPI (`claude-sonnet-4-6` viết code TSX 3D & soi bố cục, `gpt-5.6-sol` dự phòng) — đã bỏ Gemini free & OpenRouter.\n"
                "- Giọng đọc: VieNeu-TTS giọng Hải Đăng.\n"
                "- Hình ảnh & Tách nền: Google Images (Serper) + Wikipedia + tách nền GPU `bria-rmbg` + Vision kiểm tra.\n"
                "- Nhạc & Âm thanh: ACE-Step 5-Beat Trailer độc bản + 43 file foley thật xoay vòng + chuẩn -14.0 LUFS.\n"
                "- QC trước render: tsc --noEmit + pre_render_gate + OpenCV & Vision soi từng Beat still rồi mới render 1080x1920 @ 60fps + Thumbnail 9:16 + 3 tiêu đề SEO.\n"
                f"{job_info}\n"
                f"Lịch sử chat gần đây: {json.dumps(history[-8:], ensure_ascii=False)}\n"
                f"Tin nhắn mới nhất từ bạn: {json.dumps(text, ensure_ascii=False)}\n\n"
                "Hãy trả lời ĐÚNG JSON (không markdown):\n"
                '{"action": "chat" | "auto" | "create" | "revise" | "render", "topic_or_feedback": "chủ đề/góp ý nếu action khác chat", "reply": "câu trả lời tự nhiên như bạn bè"}\n\n'
                "QUY TẮC HÀNH ĐỘNG (CẤM HỨA MỒM):\n"
                "- Chào hỏi ('alo'), hỏi thăm ('làm tới đâu rồi'), hỏi về hệ thống, góp ý/bàn ý tưởng chưa chốt ('đừng đem tiếng anh vào kịch bản') -> action='chat'.\n"
                "- KHI NGƯỜI DÙNG CHỐT / RA LỆNH (kể cả câu ngắn dựa trên ngữ cảnh đang bàn như: 'làm đi', 'ok triển đi', 'chạy đi', 'làm video này đi'):\n"
                "  + Mặc định đặt action='auto' (để làm trọn gói ra luôn Video 60fps + Thumbnail + SEO), topic_or_feedback = TÓM TẮT ĐẦY ĐỦ CHỦ ĐỀ + MỌI YÊU CẦU ĐÃ THỐNG NHẤT TRONG LỊCH SỬ CHAT (ví dụ: thời lượng 40s, 100% tiếng Việt không chèn tiếng Anh).\n"
                "  + CHỈ đặt action='create' nếu người dùng nói rõ 'chỉ viết kịch bản trước' hoặc 'xem trước'.\n"
                "  + Nếu yêu cầu sửa kịch bản vừa tạo -> action='revise'. Nếu duyệt render -> action='render'.\n"
                "- TUYỆT ĐỐI CẤM HỨA MỒM: Nếu bạn chọn action='chat', KHÔNG BAO GIỜ được nói 'mình đang viết ngay / chút lát gửi ông' vì action='chat' KHÔNG chạy máy!"
            )
            for m_key in motapi_keys:
                if reply_text:
                    break
                for m_model in ("claude-sonnet-4-6", "gpt-5.6-sol", "deepseek-v4.1-flash-1017"):
                    try:
                        r = requests.post(
                            "https://motapis.com/v1/chat/completions",
                            headers={"Authorization": f"Bearer {m_key}", "Content-Type": "application/json", "User-Agent": "HaDaWhyBot/1.0"},
                            json={"model": m_model, "messages": [{"role": "user", "content": sys_prompt}], "temperature": 0.4, "max_tokens": 500},
                            timeout=20,
                        )
                        if r.ok:
                            raw = str((r.json().get("choices") or [{}])[0].get("message", {}).get("content") or "").strip()
                            raw_clean = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                            s_idx, e_idx = raw_clean.find("{"), raw_clean.rfind("}")
                            if s_idx != -1 and e_idx > s_idx:
                                parsed = json.loads(raw_clean[s_idx:e_idx + 1])
                                act = str(parsed.get("action", "chat")).strip().lower()
                                reply_text = str(parsed.get("reply", "")).strip()
                                if act in ("auto", "create", "revise", "render"):
                                    mode = act
                                    feedback = str(parsed.get("topic_or_feedback") or text).strip()
                                else:
                                    mode = "chat"
                                break
                            elif raw:
                                mode = "chat"
                                reply_text = raw
                                break
                    except Exception as exc:
                        print(f"[TG-CHAT-MOTAPI] {m_model} error: {exc}")

        if not mode:
            mode = "chat"
        reply_text = reply_text or "Nghe rõ rồi ông ơi! Cứ hỏi hoặc bàn thoải mái, muốn làm video chủ đề gì cứ bảo thẳng tôi nhé."

        try:
            history.append({"user": text, "bot": reply_text})
            TG_STATE[f"hist_{chat_id}"] = history[-10:]
        except Exception:
            pass

    if mode == "chat":
        reply(reply_text)
        return {"ok": True, "action": "chat"}

    if mode in ("auto", "create", "revise") and not feedback:
        reply(f"Ê thiếu nội dung cho lệnh /{mode} rồi. Ví dụ: /{mode} Tại sao nước đóng chai đắt hơn xăng, làm 20s")
        return {"ok": True}

    import time
    try:
        TG_STATE[f"job_{chat_id}"] = {"mode": mode, "topic": feedback, "ts": time.time()}
    except Exception:
        pass

    run_pipeline_gpu.spawn(
        mode=mode,
        feedback=feedback,
        github_token=os.getenv("GH_PAT", ""),
        openrouter_key=os.getenv("OPENROUTER_API_KEY", ""),
        gemini_key=os.getenv("GEMINI_API_KEY", ""),
        deepseek_key=os.getenv("DEEPSEEK_API_KEY", ""),
        serper_key=os.getenv("SERPER_API_KEY", ""),
        gh_models_token=os.getenv("GH_MODELS_TOKEN", ""),
        motapi_key=os.getenv("MOTAPI_KEY", ""),
        tg_token=tg_token,
        tg_chat_id=chat_id,
    )

    if reply_text:
        reply(reply_text)
    elif mode == "render":
        reply("Ok chốt đơn! Đang đẩy lên Modal T4 GPU render 60fps, vài phút nữa xong tôi gửi video qua đây nhé.")
    elif mode == "create":
        reply(f"Ok đang lên kịch bản & preview cho chủ đề:\n\"{feedback}\"\nChờ tôi tí nhé!")
    elif mode == "revise":
        reply(f"Rồi nhận góp ý:\n\"{feedback}\"\nĐể tôi sửa lại kịch bản ngay!")
    else:
        reply(f"Ok triển luôn chủ đề:\n\"{feedback}\"\nĐang chạy 5 bước trên Modal T4 GPU (~2–4 phút), xong tôi gửi video qua liền!")

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
        motapi_key=os.getenv("MOTAPI_KEY", ""),
        tg_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        tg_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
    )
    if rc != 0:
        raise SystemExit(rc)
