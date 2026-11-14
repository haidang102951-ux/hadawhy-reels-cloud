import { CaptionPhrase } from "./components/KineticWordCaption";

// ============================================================================
// CHUẨN CHÍNH TẢ 100% TỪ script_scenes.json + ĐỒNG BỘ MILI-GIÂY TỪ words.json
// QUY TẮC THÉP:
// 1. MỖI DÒNG TỐI ĐA 3 - 4 TỪ (TUYỆT ĐỐI CẤM 5-6 TỪ TRÀN KHUNG).
// 2. 80/20: ~80% TRẮNG (#FFFFFF) + DUY NHẤT 1 CỤM TỪ KHÓA MANG MÀU NHẤN MỖI PHRASE.
// 3. ZERO-BOX: KHÔNG HỘP NỀN, NẰM GỌN TRONG SAFE ZONE X: [80..920px], TOP: 108px.
// ============================================================================
export const FRIDAY13_CAPTIONS: CaptionPhrase[] = [
  // =========================================================================
  // SCENE 1 (0.00s - 2.86s): Hook Nghịch Lý Thứ Sáu ngày 13 & Phố Wall
  // =========================================================================
  {
    startSec: 0.0,
    endSec: 1.0,
    lines: [
      [
        { text: "THỨ", startSec: 0.0, endSec: 0.2, color: "#FFFFFF" },
        { text: "SÁU", startSec: 0.2, endSec: 0.44, color: "#FF3B47" },
      ],
      [
        { text: "NGÀY", startSec: 0.44, endSec: 0.56, color: "#FF3B47" },
        { text: "13", startSec: 0.56, endSec: 0.8, color: "#FF3B47" },
      ],
    ],
  },
  {
    startSec: 1.0,
    endSec: 2.0,
    lines: [
      [
        { text: "KHÔNG", startSec: 0.8, endSec: 1.06, color: "#FFFFFF" },
        { text: "PHẢI", startSec: 1.06, endSec: 1.26, color: "#FFFFFF" },
      ],
      [
        { text: "LỜI", startSec: 1.26, endSec: 1.4, color: "#FFFFFF" },
        { text: "NGUYỀN", startSec: 1.4, endSec: 1.58, color: "#FFFFFF" },
        { text: "CỔ,", startSec: 1.58, endSec: 1.78, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 2.1,
    endSec: 2.86,
    lines: [
      [
        { text: "MÀ", startSec: 2.24, endSec: 2.32, color: "#FFFFFF" },
        { text: "TỪ", startSec: 2.32, endSec: 2.44, color: "#FFFFFF" },
      ],
      [
        { text: "PHỐ", startSec: 2.44, endSec: 2.65, color: "#FFE600" },
        { text: "WALL!", startSec: 2.65, endSec: 2.86, color: "#FFE600" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 2 (3.38s - 9.14s): Giải Thích Số 13 (12 tháng, 12 tiếng -> Dư thừa)
  // =========================================================================
  {
    startSec: 3.38,
    endSec: 4.88,
    lines: [
      [
        { text: "NGÀY", startSec: 3.38, endSec: 3.48, color: "#FFFFFF" },
        { text: "XƯA", startSec: 3.48, endSec: 3.7, color: "#FFFFFF" },
        { text: "NGƯỜI", startSec: 3.7, endSec: 3.86, color: "#FFFFFF" },
        { text: "TA", startSec: 3.86, endSec: 3.98, color: "#FFFFFF" },
      ],
      [
        { text: "GHÉT", startSec: 3.98, endSec: 4.2, color: "#FFFFFF" },
        { text: "SỐ", startSec: 4.2, endSec: 4.38, color: "#FF3B47" },
        { text: "13", startSec: 4.38, endSec: 4.68, color: "#FF3B47" },
        { text: "VÌ", startSec: 4.68, endSec: 4.88, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 5.0,
    endSec: 7.35,
    lines: [
      [
        { text: "NĂM", startSec: 5.0, endSec: 5.16, color: "#FFFFFF" },
        { text: "CÓ", startSec: 5.16, endSec: 5.34, color: "#FFFFFF" },
        { text: "12", startSec: 5.34, endSec: 5.56, color: "#FFE600" },
        { text: "THÁNG,", startSec: 5.56, endSec: 5.9, color: "#FFE600" },
      ],
      [
        { text: "ĐỒNG", startSec: 6.36, endSec: 6.46, color: "#FFFFFF" },
        { text: "HỒ", startSec: 6.46, endSec: 6.58, color: "#FFFFFF" },
        { text: "12", startSec: 6.58, endSec: 6.86, color: "#FFE600" },
        { text: "TIẾNG,", startSec: 6.86, endSec: 7.2, color: "#FFE600" },
      ],
    ],
  },
  {
    startSec: 7.5,
    endSec: 9.14,
    lines: [
      [
        { text: "DƯ", startSec: 7.66, endSec: 7.74, color: "#FFFFFF" },
        { text: "RA", startSec: 7.74, endSec: 7.9, color: "#FFFFFF" },
        { text: "SỐ", startSec: 7.9, endSec: 8.06, color: "#FFFFFF" },
        { text: "13", startSec: 8.06, endSec: 8.36, color: "#FFFFFF" },
      ],
      [
        { text: "TRÔNG", startSec: 8.36, endSec: 8.6, color: "#FFFFFF" },
        { text: "RẤT", startSec: 8.6, endSec: 8.74, color: "#FFFFFF" },
        { text: "THỪA", startSec: 8.74, endSec: 8.92, color: "#FF3B47" },
        { text: "THÃI.", startSec: 8.92, endSec: 9.14, color: "#FF3B47" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 3 (9.76s - 14.80s): Thứ Sáu Chúa Chịu Nạn & Treo Cổ Tử Tù Ở Anh
  // =========================================================================
  {
    startSec: 9.76,
    endSec: 11.2,
    lines: [
      [
        { text: "CÒN", startSec: 9.76, endSec: 9.82, color: "#FFFFFF" },
        { text: "THỨ", startSec: 9.82, endSec: 9.96, color: "#FFFFFF" },
        { text: "SÁU", startSec: 9.96, endSec: 10.22, color: "#FFFFFF" },
      ],
      [
        { text: "LÀ", startSec: 10.22, endSec: 10.4, color: "#FFFFFF" },
        { text: "NGÀY", startSec: 10.4, endSec: 10.52, color: "#FFFFFF" },
        { text: "CHÚA", startSec: 10.52, endSec: 10.7, color: "#FFE600" },
        { text: "CHỊU", startSec: 10.7, endSec: 10.9, color: "#FFE600" },
        { text: "NẠN,", startSec: 10.9, endSec: 11.08, color: "#FFE600" },
      ],
    ],
  },
  {
    startSec: 11.4,
    endSec: 13.85,
    lines: [
      [
        { text: "LẠI", startSec: 11.54, endSec: 11.62, color: "#FFFFFF" },
        { text: "TỪNG", startSec: 11.62, endSec: 11.92, color: "#FFFFFF" },
        { text: "LÀ", startSec: 11.92, endSec: 12.04, color: "#FFFFFF" },
        { text: "NGÀY", startSec: 12.04, endSec: 12.22, color: "#FFFFFF" },
      ],
      [
        { text: "NƯỚC", startSec: 12.22, endSec: 12.36, color: "#FFFFFF" },
        { text: "ANH", startSec: 12.36, endSec: 12.58, color: "#FFFFFF" },
        { text: "HAY", startSec: 12.58, endSec: 12.94, color: "#FFFFFF" },
      ],
      [
        { text: "TREO", startSec: 12.94, endSec: 13.18, color: "#FF3B47" },
        { text: "CỔ", startSec: 13.18, endSec: 13.3, color: "#FF3B47" },
        { text: "TỬ", startSec: 13.3, endSec: 13.48, color: "#FF3B47" },
        { text: "TÙ,", startSec: 13.48, endSec: 13.74, color: "#FF3B47" },
      ],
    ],
  },
  {
    startSec: 14.0,
    endSec: 14.8,
    lines: [
      [
        { text: "NÊN", startSec: 14.08, endSec: 14.16, color: "#FFFFFF" },
        { text: "AI", startSec: 14.16, endSec: 14.4, color: "#FFFFFF" },
        { text: "CŨNG", startSec: 14.4, endSec: 14.52, color: "#FFFFFF" },
      ],
      [
        { text: "NGÁN.", startSec: 14.52, endSec: 14.8, color: "#FF3B47" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 4 (16.42s - 22.90s): Plot Twist Hiệp Sĩ Dòng Đền 13/10/1307
  // =========================================================================
  {
    startSec: 16.42,
    endSec: 17.5,
    lines: [
      [
        { text: "NHIỀU", startSec: 16.42, endSec: 16.64, color: "#FFFFFF" },
        { text: "NGƯỜI", startSec: 16.64, endSec: 16.82, color: "#FFFFFF" },
        { text: "TƯỞNG", startSec: 16.82, endSec: 16.94, color: "#FFFFFF" },
      ],
      [
        { text: "TỪ", startSec: 16.94, endSec: 17.14, color: "#FFFFFF" },
        { text: "THỨ", startSec: 17.14, endSec: 17.34, color: "#FFFFFF" },
        { text: "SÁU", startSec: 17.34, endSec: 17.54, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 17.54,
    endSec: 19.45,
    lines: [
      [
        { text: "NGÀY", startSec: 17.54, endSec: 17.8, color: "#FFFFFF" },
        { text: "13/10/1307", startSec: 17.8, endSec: 19.3, color: "#FFE600" },
      ],
    ],
  },
  {
    startSec: 19.5,
    endSec: 21.6,
    lines: [
      [
        { text: "LÚC", startSec: 19.6, endSec: 19.68, color: "#FFFFFF" },
        { text: "VUA", startSec: 19.68, endSec: 19.88, color: "#FFFFFF" },
        { text: "PHÁP", startSec: 19.88, endSec: 20.1, color: "#FFFFFF" },
        { text: "BẮT", startSec: 20.1, endSec: 20.32, color: "#FFFFFF" },
      ],
      [
        { text: "HIỆP", startSec: 20.32, endSec: 20.44, color: "#FFFFFF" },
        { text: "SĨ", startSec: 20.44, endSec: 20.62, color: "#FFFFFF" },
        { text: "DÒNG", startSec: 20.62, endSec: 20.86, color: "#FFFFFF" },
        { text: "ĐỀN", startSec: 20.86, endSec: 21.0, color: "#FFFFFF" },
      ],
      [
        { text: "ĐỂ", startSec: 20.98, endSec: 21.06, color: "#FF3B47" },
        { text: "XÙ", startSec: 21.06, endSec: 21.24, color: "#FF3B47" },
        { text: "NỢ,", startSec: 21.24, endSec: 21.38, color: "#FF3B47" },
      ],
    ],
  },
  {
    startSec: 21.8,
    endSec: 22.9,
    lines: [
      [
        { text: "NHƯNG", startSec: 21.88, endSec: 21.98, color: "#FFFFFF" },
        { text: "HỒI", startSec: 21.98, endSec: 22.14, color: "#FFFFFF" },
        { text: "ĐÓ", startSec: 22.14, endSec: 22.26, color: "#FFFFFF" },
      ],
      [
        { text: "CHẲNG", startSec: 22.26, endSec: 22.5, color: "#FFE600" },
        { text: "AI", startSec: 22.5, endSec: 22.66, color: "#FFE600" },
        { text: "SỢ.", startSec: 22.66, endSec: 22.9, color: "#FFE600" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 5 (22.90s - 29.74s): Thủ Phạm Thật 1907 - Thomas Lawson & Sập Sàn
  // =========================================================================
  {
    startSec: 22.9,
    endSec: 24.8,
    lines: [
      [
        { text: "MÃI", startSec: 22.9, endSec: 23.6, color: "#FFFFFF" },
        { text: "NĂM", startSec: 23.6, endSec: 23.82, color: "#FFE600" },
        { text: "1907,", startSec: 23.82, endSec: 24.6, color: "#FFE600" },
      ],
      [
        { text: "MỘT", startSec: 25.12, endSec: 25.2, color: "#FFFFFF" },
        { text: "TAY", startSec: 25.2, endSec: 25.34, color: "#FFFFFF" },
        { text: "BUÔN", startSec: 25.34, endSec: 25.58, color: "#FFFFFF" },
      ],
      [
        { text: "CHỨNG", startSec: 25.58, endSec: 25.76, color: "#FFFFFF" },
        { text: "KHOÁN", startSec: 25.76, endSec: 25.92, color: "#FFFFFF" },
        { text: "MỸ", startSec: 25.92, endSec: 26.14, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 26.14,
    endSec: 27.4,
    lines: [
      [
        { text: "VIẾT", startSec: 26.14, endSec: 26.4, color: "#FFFFFF" },
        { text: "TIỂU", startSec: 26.4, endSec: 26.62, color: "#FFFFFF" },
        { text: "THUYẾT", startSec: 26.62, endSec: 26.86, color: "#FFFFFF" },
      ],
      [
        { text: "KỂ", startSec: 27.18, endSec: 27.26, color: "#FFFFFF" },
        { text: "CHUYỆN", startSec: 27.26, endSec: 27.46, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 27.46,
    endSec: 28.66,
    lines: [
      [
        { text: "THAO", startSec: 27.46, endSec: 27.66, color: "#FF3B47" },
        { text: "TÚNG", startSec: 27.66, endSec: 27.88, color: "#FF3B47" },
        { text: "SẬP", startSec: 27.88, endSec: 28.12, color: "#FF3B47" },
      ],
      [
        { text: "SÀN", startSec: 28.12, endSec: 28.3, color: "#FF3B47" },
        { text: "PHỐ", startSec: 28.3, endSec: 28.44, color: "#FF3B47" },
        { text: "WALL", startSec: 28.44, endSec: 28.66, color: "#FF3B47" },
      ],
    ],
  },
  {
    startSec: 28.66,
    endSec: 29.74,
    lines: [
      [
        { text: "ĐÚNG", startSec: 28.66, endSec: 28.88, color: "#FFFFFF" },
        { text: "THỨ", startSec: 28.88, endSec: 29.06, color: "#FFFFFF" },
        { text: "SÁU", startSec: 29.06, endSec: 29.32, color: "#FF3B47" },
      ],
      [
        { text: "NGÀY", startSec: 29.32, endSec: 29.48, color: "#FF3B47" },
        { text: "13.", startSec: 29.48, endSec: 29.74, color: "#FF3B47" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 6 (30.44s - 35.94s): Lan Truyền Toàn Nước Mỹ 1907 & Phim 1980
  // =========================================================================
  {
    startSec: 30.44,
    endSec: 32.2,
    lines: [
      [
        { text: "SÁCH", startSec: 30.44, endSec: 30.62, color: "#FFFFFF" },
        { text: "BÁN", startSec: 30.62, endSec: 30.72, color: "#FFFFFF" },
        { text: "CHẠY", startSec: 30.72, endSec: 30.98, color: "#FFFFFF" },
        { text: "KHIẾN", startSec: 30.98, endSec: 31.2, color: "#FFFFFF" },
      ],
      [
        { text: "CẢ", startSec: 31.2, endSec: 31.3, color: "#FFFFFF" },
        { text: "NƯỚC", startSec: 31.3, endSec: 31.4, color: "#FFFFFF" },
        { text: "MỸ", startSec: 31.4, endSec: 31.62, color: "#FF3B47" },
        { text: "ÁM", startSec: 31.62, endSec: 31.76, color: "#FF3B47" },
        { text: "ẢNH,", startSec: 31.76, endSec: 31.94, color: "#FF3B47" },
      ],
    ],
  },
  {
    startSec: 32.3,
    endSec: 34.02,
    lines: [
      [
        { text: "RỒI", startSec: 32.48, endSec: 32.6, color: "#FFFFFF" },
        { text: "PHIM", startSec: 32.6, endSec: 32.86, color: "#FFE600" },
        { text: "KINH", startSec: 32.86, endSec: 33.08, color: "#FFE600" },
        { text: "DỊ", startSec: 33.08, endSec: 33.28, color: "#FFE600" },
      ],
      [
        { text: "NĂM", startSec: 33.28, endSec: 33.44, color: "#FFE600" },
        { text: "1980", startSec: 33.44, endSec: 34.02, color: "#FFE600" },
      ],
    ],
  },
  {
    startSec: 34.02,
    endSec: 35.94,
    lines: [
      [
        { text: "THỔI", startSec: 34.02, endSec: 34.82, color: "#FFFFFF" },
        { text: "BÙNG", startSec: 34.82, endSec: 35.02, color: "#FFFFFF" },
        { text: "NỖI", startSec: 35.02, endSec: 35.16, color: "#FFFFFF" },
        { text: "SỢ", startSec: 35.16, endSec: 35.36, color: "#FFFFFF" },
      ],
      [
        { text: "RA", startSec: 35.36, endSec: 35.54, color: "#FFFFFF" },
        { text: "KHẮP", startSec: 35.54, endSec: 35.64, color: "#FF3B47" },
        { text: "THẾ", startSec: 35.64, endSec: 35.8, color: "#FF3B47" },
        { text: "GIỚI.", startSec: 35.8, endSec: 35.94, color: "#FF3B47" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 7 (36.48s - 41.18s): Chốt Hạ Cực Gọn - Do Tiểu Thuyết & Phim Tự Tạo Ra
  // =========================================================================
  {
    startSec: 36.48,
    endSec: 39.1,
    lines: [
      [
        { text: "HÓA", startSec: 36.48, endSec: 36.72, color: "#FFFFFF" },
        { text: "RA", startSec: 36.72, endSec: 36.86, color: "#FFFFFF" },
        { text: "NGÀY", startSec: 36.86, endSec: 37.04, color: "#FFE600" },
        { text: "XUI", startSec: 37.04, endSec: 37.22, color: "#FFE600" },
      ],
      [
        { text: "NHẤT", startSec: 37.22, endSec: 37.36, color: "#FFE600" },
        { text: "LỊCH", startSec: 37.36, endSec: 37.6, color: "#FFE600" },
        { text: "SỬ", startSec: 37.6, endSec: 37.78, color: "#FFE600" },
      ],
      [
        { text: "CHẲNG", startSec: 37.78, endSec: 37.96, color: "#FFFFFF" },
        { text: "PHẢI", startSec: 37.96, endSec: 38.14, color: "#FFFFFF" },
        { text: "LỜI", startSec: 38.14, endSec: 38.3, color: "#FFFFFF" },
        { text: "NGUYỀN", startSec: 38.3, endSec: 38.46, color: "#FFFFFF" },
        { text: "CỔ", startSec: 38.46, endSec: 38.6, color: "#FFFFFF" },
        { text: "NÀO,", startSec: 38.6, endSec: 38.86, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 39.2,
    endSec: 41.18,
    lines: [
      [
        { text: "MÀ", startSec: 39.36, endSec: 39.42, color: "#FFFFFF" },
        { text: "DO", startSec: 39.42, endSec: 39.54, color: "#FFFFFF" },
        { text: "TIỂU", startSec: 39.54, endSec: 39.8, color: "#FF3B47" },
        { text: "THUYẾT", startSec: 39.8, endSec: 40.02, color: "#FF3B47" },
      ],
      [
        { text: "VÀ", startSec: 40.02, endSec: 40.18, color: "#FF3B47" },
        { text: "PHIM", startSec: 40.18, endSec: 40.34, color: "#FF3B47" },
        { text: "ẢNH", startSec: 40.34, endSec: 40.48, color: "#FF3B47" },
      ],
      [
        { text: "TỰ", startSec: 40.48, endSec: 40.64, color: "#FFFFFF" },
        { text: "TAY", startSec: 40.64, endSec: 40.82, color: "#FFFFFF" },
        { text: "TẠO", startSec: 40.82, endSec: 41.04, color: "#FFE600" },
        { text: "RA!", startSec: 41.04, endSec: 41.18, color: "#FFE600" },
      ],
    ],
  },
];
