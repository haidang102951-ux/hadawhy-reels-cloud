# -*- coding: utf-8 -*-
r"""
fact_researcher.py - CÀO SÂU TOÀN VĂN BÀI GỐC & DỮ KIỆN CỨNG TRẠM 1 (0 API TRẢ PHÍ)
- Nhận >= 4-5 truy vấn chuyên sâu (cơ chế | số liệu | bằng chứng/vụ việc | tài liệu/luật gốc | từ khóa tiếng Anh).
- Cào song song Wikipedia API (vi + en) + DuckDuckGo HTML + Bing Web/News.
- Truy cập trực tiếp top 5-8 URL uy tín nhất, lọc sạch menu/quảng cáo và trích 2.500-4.000 ký tự toàn văn
  chứa dữ kiện cứng (%, tiền tệ, năm, điều luật, cơ chế) lưu vào temp/research_raw.json.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SSL_CTX = ssl._create_unverified_context()
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}
WIKI_HEADERS = {"User-Agent": "HaDaWhyFactResearcher/2.0 (mailto:admin@hadawhy.vn)"}

FACT_NUM_RE = re.compile(
    r"(\d[\d.,]*\s*(?:%|phần trăm|tỷ|triệu|nghìn|ngàn|usd|đô|vnđ|đồng|năm|tháng|ngày|giờ|phút|giây|km|m2|ha|lần|điều\s+\d+|khoản\s+\d+|nghị định|luật|billion|million|percent|years?))",
    re.IGNORECASE,
)

SKIP_ARTICLE_DOMAINS = (
    "facebook.com", "tiktok.com", "instagram.com", "youtube.com", "pinterest.com",
    "shopee.vn", "lazada.vn", "tiki.vn", "ebay.com", "amazon.com", "duckduckgo.com", "bing.com",
)


def _strip_tags(raw: str) -> str:
    txt = re.sub(r"<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip()


def _fetch_text(url: str, headers: Dict[str, str], timeout: int = 12) -> str:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
        raw_bytes = resp.read(850_000)
        return raw_bytes.decode("utf-8", errors="ignore")


def _unwrap_ddg_url(href: str) -> str:
    if "uddg=" in href:
        m = re.search(r"uddg=([^&]+)", href)
        if m:
            return urllib.parse.unquote(m.group(1))
    return href


def extract_clean_article_body(url: str) -> Dict[str, Any] | None:
    """Truy cập trực tiếp URL bài gốc, lọc menu/quảng cáo và trích 2.500-4.000 ký tự toàn văn + dữ kiện cứng."""
    try:
        parsed = urllib.parse.urlparse(url)
        domain = (parsed.netloc or "").lower()
        if not domain or any(bad in domain for bad in SKIP_ARTICLE_DOMAINS):
            return None

        raw_html = _fetch_text(url, HEADERS, timeout=11)
        title_m = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.IGNORECASE | re.DOTALL)
        title = _strip_tags(title_m.group(1))[:160] if title_m else domain

        # Lọc sạch script, style, nav, header, footer, aside, form, iframe, quảng cáo
        cleaned = re.sub(
            r"<(?:script|style|noscript|svg|nav|header|footer|aside|form|iframe|button)[^>]*>[\s\S]*?</(?:script|style|noscript|svg|nav|header|footer|aside|form|iframe|button)>",
            " ",
            raw_html,
            flags=re.IGNORECASE,
        )
        paragraphs = re.findall(r"<p[^>]*>([\s\S]*?)</p>", cleaned, flags=re.IGNORECASE)
        good_paras: List[str] = []
        for p_raw in paragraphs:
            p_txt = _strip_tags(p_raw)
            if len(p_txt) < 45:
                continue
            if any(junk in p_txt.lower() for junk in ("bản quyền thuộc về", "đăng ký nhận tin", "quảng cáo", "cookie", "chính sách bảo mật")):
                continue
            good_paras.append(p_txt)

        full_body = " ".join(good_paras).strip()
        if len(full_body) < 350:
            return None

        excerpt = full_body[:3800]
        sentences = re.split(r"(?<=[.!?])\s+", full_body)
        extracted_facts = [s.strip()[:340] for s in sentences if len(s.strip()) >= 40 and FACT_NUM_RE.search(s)][:12]
        raw_excerpts = [p[:500] for p in good_paras[:8]]

        return {
            "url": url,
            "source_name": domain.replace("www.", ""),
            "title": title,
            "char_length": len(excerpt),
            "full_excerpt": excerpt,
            "extracted_facts": extracted_facts,
            "raw_excerpts": raw_excerpts,
        }
    except Exception:
        return None


def search_wikipedia_deep(query: str, lang: str = "vi", limit: int = 3) -> List[Dict[str, Any]]:
    articles: List[Dict[str, Any]] = []
    try:
        q = urllib.parse.quote(query)
        api = (
            f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search"
            f"&srsearch={q}&srlimit={limit}&utf8=1&format=json"
        )
        data = json.loads(_fetch_text(api, WIKI_HEADERS))
        for item in data.get("query", {}).get("search", []):
            title = item.get("title", "")
            if not title:
                continue
            ext_api = (
                f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=extracts"
                f"&explaintext=1&exchars=4000&titles={urllib.parse.quote(title)}&format=json"
            )
            ext_data = json.loads(_fetch_text(ext_api, WIKI_HEADERS))
            pages = ext_data.get("query", {}).get("pages", {})
            for _, p in pages.items():
                extract = re.sub(r"\s+", " ", (p.get("extract") or "")).strip()
                if len(extract) < 200:
                    continue
                sents = re.split(r"(?<=[.!?])\s+", extract)
                facts = [s.strip()[:340] for s in sents if len(s.strip()) >= 35 and FACT_NUM_RE.search(s)][:10]
                wiki_url = f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                articles.append({
                    "url": wiki_url,
                    "source_name": f"Wikipedia ({lang})",
                    "title": title,
                    "char_length": len(extract[:3800]),
                    "full_excerpt": extract[:3800],
                    "extracted_facts": facts,
                    "raw_excerpts": [extract[i:i + 600] for i in range(0, min(len(extract), 2400), 600)],
                })
    except Exception as exc:
        print(f"[WIKI WARN {lang}] {query}: {exc}")
    return articles


def discover_search_urls(query: str) -> List[Dict[str, str]]:
    found: List[Dict[str, str]] = []
    # 1. DuckDuckGo HTML
    try:
        ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        page = _fetch_text(ddg_url, HEADERS, timeout=12)
        blocks = re.findall(
            r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>[\s\S]*?<a[^>]*class="result__snippet"[^>]*>(.*?)</a>',
            page,
        )
        for href, t_raw, s_raw in blocks[:8]:
            real_u = _unwrap_ddg_url(html.unescape(href))
            if real_u.startswith("http"):
                found.append({"url": real_u, "title": _strip_tags(t_raw), "snippet": _strip_tags(s_raw)})
    except Exception:
        pass

    # 2. Bing Web
    try:
        bing_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&setlang=vi"
        page = _fetch_text(bing_url, HEADERS, timeout=12)
        items = re.findall(
            r'<li class="b_algo"[\s\S]*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a></h2>[\s\S]*?<p[^>]*>(.*?)</p>',
            page,
        )
        for href, t_raw, s_raw in items[:8]:
            real_u = html.unescape(href)
            if real_u.startswith("http"):
                found.append({"url": real_u, "title": _strip_tags(t_raw), "snippet": _strip_tags(s_raw)})
    except Exception:
        pass
    return found


def run_research(topic: str, queries: List[str], project_dir: Path) -> Path:
    all_queries = [q.strip() for q in queries if q.strip()]
    if topic.strip() and topic.strip() not in all_queries:
        all_queries.insert(0, topic.strip())

    wiki_articles: List[Dict[str, Any]] = []
    discovered: List[Dict[str, str]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        w_futs = [ex.submit(search_wikipedia_deep, q, "vi", 2) for q in all_queries[:4]]
        w_futs += [ex.submit(search_wikipedia_deep, q, "en", 2) for q in all_queries[:3]]
        s_futs = [ex.submit(discover_search_urls, q) for q in all_queries]
        for fut in concurrent.futures.as_completed(w_futs):
            try:
                wiki_articles.extend(fut.result())
            except Exception:
                pass
        for fut in concurrent.futures.as_completed(s_futs):
            try:
                discovered.extend(fut.result())
            except Exception:
                pass

    # Chọn top URL uy tín không trùng để đọc sâu toàn văn
    seen_urls: set[str] = set()
    candidate_urls: List[str] = []
    for d in discovered:
        u = d["url"].split("#")[0]
        dom = urllib.parse.urlparse(u).netloc.lower()
        if not dom or any(b in dom for b in SKIP_ARTICLE_DOMAINS) or "wikipedia.org" in dom:
            continue
        if u not in seen_urls:
            seen_urls.add(u)
            candidate_urls.append(u)

    deep_web_articles: List[Dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        art_futs = [ex.submit(extract_clean_article_body, u) for u in candidate_urls[:14]]
        for fut in concurrent.futures.as_completed(art_futs):
            res = fut.result()
            if res is not None:
                deep_web_articles.append(res)

    deep_web_articles.sort(key=lambda a: (len(a["extracted_facts"]), a["char_length"]), reverse=True)
    top_web_articles = deep_web_articles[:8]

    # Khử trùng wiki articles
    seen_w: set[str] = set()
    clean_wiki: List[Dict[str, Any]] = []
    for wa in wiki_articles:
        if wa["url"] not in seen_w:
            seen_w.add(wa["url"])
            clean_wiki.append(wa)

    all_articles = top_web_articles + clean_wiki[:4]
    flat_facts: List[Dict[str, Any]] = []
    seen_fact_keys: set[str] = set()
    for art in all_articles:
        for f_txt in art.get("extracted_facts", []):
            fk = re.sub(r"\W+", "", f_txt.lower())[:85]
            if fk and fk not in seen_fact_keys:
                seen_fact_keys.add(fk)
                flat_facts.append({
                    "source": f"{art['source_name']} — {art['title']}",
                    "url": art["url"],
                    "has_number": True,
                    "snippet": f_txt,
                })

    # Bổ sung thêm snippet tìm kiếm có số liệu nếu cần
    for d in discovered:
        if FACT_NUM_RE.search(d.get("snippet", "")):
            fk = re.sub(r"\W+", "", d["snippet"].lower())[:85]
            if fk and fk not in seen_fact_keys:
                seen_fact_keys.add(fk)
                flat_facts.append({
                    "source": d["title"][:90],
                    "url": d["url"],
                    "has_number": True,
                    "snippet": d["snippet"][:340],
                })

    out_path = project_dir / "temp" / "research_raw.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "topic": topic,
        "queries": all_queries,
        "deep_urls_count": len(all_articles),
        "hard_facts_count": len(flat_facts),
        "articles": all_articles,
        "facts": flat_facts[:40],
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"[FACT RESEARCHER DEEP OK] Đã đọc sâu {len(all_articles)} bài gốc (2.500-4.000 ký tự/bài) "
        f"& trích {len(flat_facts)} dữ kiện cứng -> {out_path}"
    )
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser(description="Cào sâu toàn văn bài gốc & số liệu sự thật (Wikipedia VI/EN + Top URLs)")
    ap.add_argument("--topic", required=True, help="Chủ đề chính của video")
    ap.add_argument("--queries", default="", help="4-5 truy vấn chuyên sâu cách nhau dấu | (VD: 'q1|q2|q3|q4')")
    ap.add_argument("--project", required=True, help="Thư mục dự án WIP (VD: D:\\DuAn_DangLam\\ten_du_an)")
    args = ap.parse_args()

    q_list = [q.strip() for q in args.queries.split("|") if q.strip()]
    run_research(args.topic, q_list, Path(args.project))
    return 0


if __name__ == "__main__":
    sys.exit(main())
