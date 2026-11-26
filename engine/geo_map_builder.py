r"""
geo_map_builder.py - CÔNG CỤ TRÍCH XUẤT BẢN ĐỒ ĐỊA CHIẾN LƯỢC 3D TỰ ĐỘNG CHO MỌI QUỐC GIA (258 QUỐC GIA)
Đọc trực tiếp từ: D:\Đầu Não Video Ngắn FB (không xóa)\remotion_reels\public\maps\countries.geojson
Hỗ trợ tự động:
- Tra cứu tên quốc gia bằng cả Tiếng Việt lẫn Tiếng Anh (VD: "Việt Nam", "Mỹ", "Trung Quốc", "Nhật Bản", "Anh", "Nga", "Singapore"...)
- Tự động tính tọa độ tâm (Centroid lon/lat) của quốc gia lớn nhất nếu không truyền tay
- Tự động tính khung nhìn bản đồ (Bounding Box) bao trọn Quốc gia Nguồn + Quốc gia Đích kèm khoảng đệm thẩm mỹ
"""

import argparse
import json
import sys
from pathlib import Path

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

FB_BRAIN = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
GEOJSON_PATH = FB_BRAIN / "remotion_reels" / "public" / "maps" / "countries.geojson"
DEFAULT_OUT_TS = FB_BRAIN / "remotion_reels" / "src" / "components" / "eurasiaGeoPaths.ts"

VI_TO_EN_COUNTRY = {
    "việt nam": "Vietnam",
    "vietnam": "Vietnam",
    "anh": "United Kingdom",
    "vương quốc anh": "United Kingdom",
    "luân đôn": "United Kingdom",
    "mỹ": "United States of America",
    "hoa kỳ": "United States of America",
    "trung quốc": "China",
    "nhật bản": "Japan",
    "nhật": "Japan",
    "hàn quốc": "South Korea",
    "triều tiên": "North Korea",
    "đài loan": "Taiwan",
    "singapore": "Singapore",
    "thái lan": "Thailand",
    "ấn độ": "India",
    "nga": "Russia",
    "đức": "Germany",
    "pháp": "France",
    "ý": "Italy",
    "úc": "Australia",
    "canada": "Canada",
    "brazil": "Brazil",
    "iran": "Iran",
    "israel": "Israel",
    "ả rập xê út": "Saudi Arabia",
    "uae": "United Arab Emirates",
    "thổ nhĩ kỳ": "Turkey",
    "ukraina": "Ukraine",
    "malaysia": "Malaysia",
    "indonesia": "Indonesia",
    "philippines": "Philippines",
    "campuchia": "Cambodia",
    "lào": "Laos",
    "hà lan": "Netherlands",
    "thụy sĩ": "Switzerland",
}


def resolve_country_name(name: str) -> str:
    clean = name.strip().lower()
    return VI_TO_EN_COUNTRY.get(clean, name.strip())


def compute_main_polygon_centroid(polys: list) -> tuple[float, float]:
    """Tìm đa giác có nhiều điểm nhất (đất liền chính) và tính tâm (lon, lat)."""
    best_ring = []
    for poly in polys:
        if poly and len(poly[0]) > len(best_ring):
            best_ring = poly[0]
    if not best_ring:
        return (0.0, 0.0)
    lons = [p[0] for p in best_ring]
    lats = [p[1] for p in best_ring]
    return (round(sum(lons) / len(lons), 2), round(sum(lats) / len(lats), 2))


def build_geo_paths_ts(
    origin_country: str = "Vietnam",
    target_country: str = "United Kingdom",
    origin_lonlat: tuple[float, float] | None = None,
    target_lonlat: tuple[float, float] | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    out_ts_path: Path | None = None,
    project_dir: Path | None = None,
):
    if out_ts_path is None:
        if project_dir is not None:
            out_ts_path = Path(project_dir) / "temp" / "geoPaths.ts"
        else:
            out_ts_path = DEFAULT_OUT_TS
    out_ts_path = Path(out_ts_path)
    out_ts_path.parent.mkdir(parents=True, exist_ok=True)
    origin_en = resolve_country_name(origin_country)
    target_en = resolve_country_name(target_country)

    data = json.loads(GEOJSON_PATH.read_text(encoding="utf-8"))

    # Bước 1: Tự động tìm tâm (lon, lat) từ GeoJSON nếu chưa truyền tay
    auto_orig_lonlat = (105.85, 21.02)
    auto_targ_lonlat = (-0.12, 51.50)
    for feat in data.get("features", []):
        name = str(feat.get("properties", {}).get("name", ""))
        geom = feat.get("geometry", {})
        gtype = geom.get("type", "")
        coords = geom.get("coordinates", [])
        polys = [coords] if gtype == "Polygon" else coords if gtype == "MultiPolygon" else []
        if name.lower() == origin_en.lower():
            auto_orig_lonlat = compute_main_polygon_centroid(polys)
        elif name.lower() == target_en.lower():
            auto_targ_lonlat = compute_main_polygon_centroid(polys)

    if origin_lonlat is None:
        origin_lonlat = auto_orig_lonlat
    if target_lonlat is None:
        target_lonlat = auto_targ_lonlat

    # Bước 2: Tự động tính Bounding Box bao trọn 2 nước + khoảng đệm thẩm mỹ nếu chưa truyền tay
    if bbox is None:
        min_lon = min(origin_lonlat[0], target_lonlat[0])
        max_lon = max(origin_lonlat[0], target_lonlat[0])
        min_lat = min(origin_lonlat[1], target_lonlat[1])
        max_lat = max(origin_lonlat[1], target_lonlat[1])
        span_lon = max(35.0, max_lon - min_lon)
        span_lat = max(25.0, max_lat - min_lat)
        pad_lon = max(14.0, span_lon * 0.22)
        pad_lat = max(12.0, span_lat * 0.28)
        bbox = (
            max(-179.0, min_lon - pad_lon),
            min(179.0, max_lon + pad_lon),
            max(-65.0, min_lat - pad_lat),
            min(78.0, max_lat + pad_lat),
        )

    lon_min, lon_max, lat_min, lat_max = bbox
    w, h = 1000.0, 640.0

    def proj(lon: float, lat: float) -> tuple[float, float]:
        x = (lon - lon_min) / (lon_max - lon_min) * w
        y = (lat_max - lat) / (lat_max - lat_min) * h
        return round(x, 1), round(y, 1)

    def ring_to_path(ring: list, step: int = 1) -> str:
        pts = ring[::step]
        if len(pts) < 3:
            return ""
        coords = [proj(p[0], p[1]) for p in pts]
        d = f"M{coords[0][0]},{coords[0][1]}"
        for cx, cy in coords[1:]:
            d += f"L{cx},{cy}"
        return d + "Z"

    bg_paths, origin_paths, target_paths = [], [], []

    for feat in data.get("features", []):
        props = feat.get("properties", {})
        name = str(props.get("name", ""))
        geom = feat.get("geometry", {})
        gtype = geom.get("type", "")
        coords = geom.get("coordinates", [])

        polys = [coords] if gtype == "Polygon" else coords if gtype == "MultiPolygon" else []
        is_orig = name.lower() == origin_en.lower()
        is_targ = name.lower() == target_en.lower()

        for poly in polys:
            if not poly:
                continue
            ring = poly[0]
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]
            if max(lons) < lon_min or min(lons) > lon_max or max(lats) < lat_min or min(lats) > lat_max:
                continue
            step = 1 if (is_orig or is_targ) else max(1, len(ring) // 45)
            d = ring_to_path(ring, step=step)
            if not d:
                continue
            if is_orig:
                origin_paths.append(d)
            elif is_targ:
                target_paths.append(d)
            else:
                bg_paths.append(d)

    orig_pt = proj(*origin_lonlat)
    targ_pt = proj(*target_lonlat)

    ts_code = f"""// Auto-generated by geo_map_builder.py from countries.geojson
export const MAP_WIDTH = {int(w)};
export const MAP_HEIGHT = {int(h)};
export const ORIGIN_COORD = {{ x: {orig_pt[0]}, y: {orig_pt[1]} }};
export const TARGET_COORD = {{ x: {targ_pt[0]}, y: {targ_pt[1]} }};
export const ORIGIN_PATHS: string[] = {json.dumps(origin_paths)};
export const TARGET_PATHS: string[] = {json.dumps(target_paths)};
export const BG_PATHS: string[] = {json.dumps(bg_paths)};
// Backwards-compatible aliases
export const HANOI_COORD = ORIGIN_COORD;
export const LONDON_COORD = TARGET_COORD;
export const VIETNAM_PATHS = ORIGIN_PATHS;
export const UK_PATHS = TARGET_PATHS;
export const EURASIA_BG_PATHS = BG_PATHS;
"""
    out_ts_path.write_text(ts_code, encoding="utf-8")
    print(f"[GEO MAP BUILDER OK] Origin={origin_en} ({len(origin_paths)} paths, pt={orig_pt}), Target={target_en} ({len(target_paths)} paths, pt={targ_pt}) -> {out_ts_path.name}")
    return out_ts_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Trích xuất tọa độ bản đồ địa chiến lược vào <project>/temp/geoPaths.ts (0 rác Đầu Não)")
    ap.add_argument("--project", required=True, help="Thư mục WIP dự án (VD: D:\\DuAn_DangLam\\ten_du_an)")
    ap.add_argument("--origin", default="Vietnam", help="Quốc gia nguồn (VN hoặc EN)")
    ap.add_argument("--target", default="United Kingdom", help="Quốc gia đích (VN hoặc EN)")
    ap.add_argument("--out", default="", help="Đường dẫn file .ts tùy chọn (mặc định: <project>/temp/geoPaths.ts)")
    args = ap.parse_args()

    out_p = Path(args.out) if args.out else (Path(args.project) / "temp" / "geoPaths.ts")
    build_geo_paths_ts(
        origin_country=args.origin,
        target_country=args.target,
        out_ts_path=out_p,
        project_dir=Path(args.project),
    )
