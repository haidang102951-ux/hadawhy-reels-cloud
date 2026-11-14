import { CaptionPhrase } from "./components/KineticWordCaption";

// Chuẩn chính tả 100% từ script_scenes.json + đồng bộ mili-giây từng từ từ words.json
// Tuân thủ tuyệt đối Quy tắc 80/20: ~80% Trắng (#FFFFFF) + duy nhất 1 cụm từ khóa mang 1 màu nhấn mỗi phrase.
export const NVIDIA_CAPTIONS: CaptionPhrase[] = [
  // =========================================================================
  // SCENE 1 (0.00s - 5.75s): Hook Nghịch Lý (Ngai Vàng Lung Lay)
  // =========================================================================
  {
    startSec: 0.0,
    endSec: 2.6,
    lines: [
      [
        { text: "SAU", startSec: 0.0, endSec: 0.3, color: "#FFFFFF" },
        { text: "33", startSec: 0.3, endSec: 0.62, color: "#FFE600" },
        { text: "NĂM", startSec: 0.62, endSec: 0.94, color: "#FFE600" },
        { text: "NGỰ", startSec: 0.94, endSec: 1.06, color: "#FFFFFF" },
        { text: "TRỊ", startSec: 1.06, endSec: 1.28, color: "#FFFFFF" },
      ],
      [
        { text: "NGAI", startSec: 1.28, endSec: 1.5, color: "#FFFFFF" },
        { text: "VÀNG", startSec: 1.5, endSec: 1.76, color: "#FFFFFF" },
        { text: "CHIP", startSec: 1.76, endSec: 2.04, color: "#FFFFFF" },
        { text: "AI,", startSec: 2.04, endSec: 2.36, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 2.6,
    endSec: 3.88,
    lines: [
      [
        { text: "JENSEN", startSec: 2.96, endSec: 3.24, color: "#00E5FF" },
        { text: "HUANG", startSec: 3.24, endSec: 3.4, color: "#00E5FF" },
      ],
      [
        { text: "BẤT", startSec: 3.4, endSec: 3.62, color: "#FFFFFF" },
        { text: "NGỜ", startSec: 3.62, endSec: 3.88, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 3.88,
    endSec: 5.75,
    lines: [
      [
        { text: "BỊ", startSec: 3.88, endSec: 4.04, color: "#FFFFFF" },
        { text: "HỘI", startSec: 4.04, endSec: 4.18, color: "#FFFFFF" },
        { text: "ĐỒNG", startSec: 4.18, endSec: 4.34, color: "#FFFFFF" },
        { text: "QUẢN", startSec: 4.34, endSec: 4.58, color: "#FFFFFF" },
        { text: "TRỊ", startSec: 4.58, endSec: 4.74, color: "#FFFFFF" },
      ],
      [
        { text: "ĐIỀU", startSec: 4.74, endSec: 4.9, color: "#FFFFFF" },
        { text: "TRA", startSec: 4.9, endSec: 5.06, color: "#FFFFFF" },
        { text: "ĐỘC", startSec: 5.06, endSec: 5.28, color: "#FF3B47" },
        { text: "LẬP.", startSec: 5.28, endSec: 5.46, color: "#FF3B47" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 2 (5.75s - 12.25s): Bê Bối Tình Báo Singapore & 3.000 Tỷ USD
  // =========================================================================
  {
    startSec: 5.75,
    endSec: 6.72,
    lines: [
      [
        { text: "QUAN", startSec: 5.94, endSec: 6.04, color: "#FFFFFF" },
        { text: "HỆ", startSec: 6.04, endSec: 6.16, color: "#FFFFFF" },
        { text: "NGOÀI", startSec: 6.16, endSec: 6.36, color: "#FFFFFF" },
      ],
      [
        { text: "HÔN", startSec: 6.36, endSec: 6.56, color: "#FF3B47" },
        { text: "NHÂN", startSec: 6.56, endSec: 6.68, color: "#FF3B47" },
      ],
    ],
  },
  {
    startSec: 6.72,
    endSec: 8.45,
    lines: [
      [
        { text: "VỚI", startSec: 6.68, endSec: 6.9, color: "#FFFFFF" },
        { text: "ALICE", startSec: 6.9, endSec: 7.2, color: "#00E5FF" },
        { text: "HUANG", startSec: 7.2, endSec: 7.56, color: "#00E5FF" },
      ],
      [
        { text: "TẠI", startSec: 7.56, endSec: 7.66, color: "#FFFFFF" },
        { text: "SINGAPORE,", startSec: 7.66, endSec: 8.12, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 8.45,
    endSec: 10.6,
    lines: [
      [
        { text: "BỊ", startSec: 8.78, endSec: 8.86, color: "#FFFFFF" },
        { text: "NGHI", startSec: 8.86, endSec: 8.94, color: "#FFFFFF" },
        { text: "LÀ", startSec: 8.94, endSec: 9.12, color: "#FFFFFF" },
        { text: "ĐIỆP", startSec: 9.12, endSec: 9.22, color: "#FF3B47" },
        { text: "VIÊN,", startSec: 9.22, endSec: 9.5, color: "#FF3B47" },
      ],
      [
        { text: "ĐE", startSec: 9.5, endSec: 9.98, color: "#FFFFFF" },
        { text: "DỌA", startSec: 9.98, endSec: 10.1, color: "#FFFFFF" },
        { text: "AN", startSec: 10.1, endSec: 10.28, color: "#FFFFFF" },
        { text: "NINH", startSec: 10.28, endSec: 10.48, color: "#FFFFFF" },
        { text: "MỸ", startSec: 10.48, endSec: 10.6, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 10.6,
    endSec: 12.25,
    lines: [
      [
        { text: "VÀ", startSec: 10.6, endSec: 10.84, color: "#FFFFFF" },
        { text: "ĐẾ", startSec: 10.84, endSec: 10.96, color: "#FFFFFF" },
        { text: "CHẾ", startSec: 10.96, endSec: 11.18, color: "#FFFFFF" },
      ],
      [
        { text: "3", startSec: 11.18, endSec: 11.44, color: "#FFE600" },
        { text: "NGHÌN", startSec: 11.44, endSec: 11.58, color: "#FFE600" },
        { text: "TỶ", startSec: 11.58, endSec: 11.78, color: "#FFE600" },
        { text: "ĐÔ.", startSec: 11.78, endSec: 11.98, color: "#FFE600" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 3 (12.25s - 19.42s): Lỗ Hổng Quản Trị (Không COO, 60 Lãnh Đạo)
  // =========================================================================
  {
    startSec: 12.25,
    endSec: 13.7,
    lines: [
      [
        { text: "SUỐT", startSec: 12.54, endSec: 12.82, color: "#FFFFFF" },
        { text: "33", startSec: 12.82, endSec: 13.1, color: "#FFE600" },
        { text: "NĂM,", startSec: 13.1, endSec: 13.56, color: "#FFE600" },
      ],
    ],
  },
  {
    startSec: 13.7,
    endSec: 15.36,
    lines: [
      [
        { text: "NVIDIA", startSec: 13.84, endSec: 14.04, color: "#FFFFFF" },
        { text: "KHÔNG", startSec: 14.04, endSec: 14.58, color: "#FF3B47" },
        { text: "CÓ", startSec: 14.58, endSec: 14.72, color: "#FF3B47" },
      ],
      [
        { text: "GIÁM", startSec: 14.72, endSec: 14.88, color: "#FFFFFF" },
        { text: "ĐỐC", startSec: 14.88, endSec: 14.94, color: "#FFFFFF" },
        { text: "VẬN", startSec: 14.94, endSec: 15.14, color: "#FFFFFF" },
        { text: "HÀNH,", startSec: 15.14, endSec: 15.36, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 15.36,
    endSec: 17.72,
    lines: [
      [
        { text: "60", startSec: 15.36, endSec: 15.9, color: "#00E5FF" },
        { text: "LÃNH", startSec: 15.9, endSec: 16.14, color: "#00E5FF" },
        { text: "ĐẠO", startSec: 16.14, endSec: 16.26, color: "#00E5FF" },
        { text: "BÁO", startSec: 16.26, endSec: 16.44, color: "#FFFFFF" },
        { text: "CÁO", startSec: 16.44, endSec: 16.66, color: "#FFFFFF" },
      ],
      [
        { text: "THẲNG", startSec: 16.66, endSec: 16.84, color: "#FFFFFF" },
        { text: "CHO", startSec: 16.84, endSec: 17.0, color: "#FFFFFF" },
        { text: "JENSEN,", startSec: 17.0, endSec: 17.72, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 17.72,
    endSec: 19.42,
    lines: [
      [
        { text: "TẠO", startSec: 17.72, endSec: 17.96, color: "#FFFFFF" },
        { text: "KHOẢNG", startSec: 17.96, endSec: 18.14, color: "#FF3B47" },
        { text: "TRỐNG", startSec: 18.14, endSec: 18.32, color: "#FF3B47" },
      ],
      [
        { text: "QUYỀN", startSec: 18.32, endSec: 18.54, color: "#FFFFFF" },
        { text: "LỰC", startSec: 18.54, endSec: 18.68, color: "#FFFFFF" },
        { text: "KHỔNG", startSec: 18.68, endSec: 18.9, color: "#FFFFFF" },
        { text: "LỒ.", startSec: 18.9, endSec: 19.06, color: "#FFFFFF" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 4 (19.42s - 28.75s): Stephen Neal - Trụ Cột HĐQT từ 1993-1999
  // =========================================================================
  {
    startSec: 19.42,
    endSec: 21.25,
    lines: [
      [
        { text: "TÂM", startSec: 19.66, endSec: 19.78, color: "#FFFFFF" },
        { text: "ĐIỂM", startSec: 19.78, endSec: 19.96, color: "#FFFFFF" },
        { text: "THAY", startSec: 19.96, endSec: 20.08, color: "#FFFFFF" },
        { text: "THẾ", startSec: 20.08, endSec: 20.26, color: "#FFFFFF" },
        { text: "LÀ", startSec: 20.26, endSec: 20.44, color: "#FFFFFF" },
      ],
      [
        { text: "STEPHEN", startSec: 20.44, endSec: 20.78, color: "#00E5FF" },
        { text: "NEAL,", startSec: 20.78, endSec: 21.08, color: "#00E5FF" },
      ],
    ],
  },
  {
    startSec: 21.25,
    endSec: 22.4,
    lines: [
      [
        { text: "THÀNH", startSec: 21.46, endSec: 21.54, color: "#FFFFFF" },
        { text: "VIÊN", startSec: 21.54, endSec: 21.74, color: "#FFFFFF" },
      ],
      [
        { text: "ĐỘC", startSec: 21.74, endSec: 21.94, color: "#00E5FF" },
        { text: "LẬP,", startSec: 21.94, endSec: 22.18, color: "#00E5FF" },
      ],
    ],
  },
  {
    startSec: 22.4,
    endSec: 23.96,
    lines: [
      [
        { text: "CỰU", startSec: 22.6, endSec: 22.76, color: "#FFFFFF" },
        { text: "CEO", startSec: 22.76, endSec: 23.14, color: "#FFFFFF" },
        { text: "HÃNG", startSec: 23.14, endSec: 23.44, color: "#FFFFFF" },
        { text: "LUẬT", startSec: 23.44, endSec: 23.6, color: "#FFFFFF" },
      ],
      [{ text: "COOLEY", startSec: 23.6, endSec: 23.96, color: "#FFE600" }],
    ],
  },
  {
    startSec: 23.96,
    endSec: 28.78,
    lines: [
      [
        { text: "GẮN", startSec: 23.96, endSec: 24.34, color: "#FFFFFF" },
        { text: "BÓ", startSec: 24.34, endSec: 24.52, color: "#FFFFFF" },
        { text: "NVIDIA", startSec: 24.52, endSec: 24.88, color: "#FFFFFF" },
        { text: "TỪ", startSec: 24.88, endSec: 25.24, color: "#FFFFFF" },
        { text: "1993", startSec: 25.24, endSec: 26.32, color: "#FFFFFF" },
      ],
      [
        { text: "TỚI", startSec: 26.32, endSec: 26.98, color: "#FFFFFF" },
        { text: "IPO", startSec: 26.98, endSec: 27.46, color: "#FFE600" },
        { text: "1999,", startSec: 27.46, endSec: 28.78, color: "#FFE600" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 5 (28.78s - 36.67s): Hồ Sơ Ảo Thuật Gia Pháp Lý (Keating, Theranos, FTX)
  // =========================================================================
  {
    startSec: 28.78,
    endSec: 30.65,
    lines: [
      [
        { text: "LÀ", startSec: 28.78, endSec: 29.4, color: "#FFFFFF" },
        { text: "ẢO", startSec: 29.4, endSec: 29.62, color: "#FFE600" },
        { text: "THUẬT", startSec: 29.62, endSec: 29.84, color: "#FFE600" },
        { text: "GIA", startSec: 29.84, endSec: 29.98, color: "#FFE600" },
      ],
      [
        { text: "PHÁP", startSec: 29.98, endSec: 30.16, color: "#FFFFFF" },
        { text: "LÝ,", startSec: 30.16, endSec: 30.34, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 30.65,
    endSec: 31.66,
    lines: [
      [
        { text: "NEAL", startSec: 30.82, endSec: 30.9, color: "#FFFFFF" },
        { text: "GIÚP", startSec: 30.9, endSec: 31.16, color: "#FFFFFF" },
      ],
      [
        { text: "CHARLES", startSec: 31.16, endSec: 31.34, color: "#00E5FF" },
        { text: "KEATING", startSec: 31.34, endSec: 31.66, color: "#00E5FF" },
      ],
    ],
  },
  {
    startSec: 31.66,
    endSec: 33.1,
    lines: [
      [
        { text: "GIẢM", startSec: 31.66, endSec: 32.0, color: "#FFFFFF" },
        { text: "ÁN", startSec: 32.0, endSec: 32.18, color: "#FFFFFF" },
        { text: "TỪ", startSec: 32.18, endSec: 32.3, color: "#FFFFFF" },
        { text: "10", startSec: 32.3, endSec: 32.52, color: "#FFFFFF" },
      ],
      [
        { text: "XUỐNG", startSec: 32.52, endSec: 32.76, color: "#FFFFFF" },
        { text: "DƯỚI", startSec: 32.76, endSec: 32.9, color: "#FFFFFF" },
        { text: "5", startSec: 32.9, endSec: 33.0, color: "#FFE600" },
        { text: "NĂM,", startSec: 33.0, endSec: 33.1, color: "#FFE600" },
      ],
    ],
  },
  {
    startSec: 33.1,
    endSec: 34.55,
    lines: [
      [
        { text: "GỠ", startSec: 33.1, endSec: 33.78, color: "#FFFFFF" },
        { text: "RỐI", startSec: 33.78, endSec: 34.0, color: "#FFFFFF" },
      ],
      [{ text: "THERANOS", startSec: 34.0, endSec: 34.5, color: "#FF3B47" }],
    ],
  },
  {
    startSec: 34.55,
    endSec: 36.67,
    lines: [
      [
        { text: "VÀ", startSec: 34.5, endSec: 35.0, color: "#FFFFFF" },
        { text: "ĐƯỢC", startSec: 35.0, endSec: 35.12, color: "#FFFFFF" },
        { text: "ĐỀ", startSec: 35.12, endSec: 35.3, color: "#FFFFFF" },
        { text: "CỬ", startSec: 35.3, endSec: 35.46, color: "#FFFFFF" },
      ],
      [
        { text: "CHỦ", startSec: 35.46, endSec: 35.72, color: "#FFFFFF" },
        { text: "TỊCH", startSec: 35.72, endSec: 35.9, color: "#FFFFFF" },
        { text: "FTX.", startSec: 35.9, endSec: 36.46, color: "#FF3B47" },
      ],
    ],
  },

  // =========================================================================
  // SCENE 6 (36.67s - 42.90s): Nghịch Lý Luật Sư vs Chip AI & Chốt Hạ
  // =========================================================================
  {
    startSec: 36.67,
    endSec: 37.66,
    lines: [
      [
        { text: "NHƯNG", startSec: 36.84, endSec: 36.94, color: "#FFFFFF" },
        { text: "MỘT", startSec: 36.94, endSec: 37.1, color: "#FFFFFF" },
        { text: "LUẬT", startSec: 37.1, endSec: 37.22, color: "#FFE600" },
        { text: "SƯ", startSec: 37.22, endSec: 37.38, color: "#FFE600" },
      ],
      [
        { text: "KHÔNG", startSec: 37.38, endSec: 37.54, color: "#FFFFFF" },
        { text: "BIẾT", startSec: 37.54, endSec: 37.66, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 37.66,
    endSec: 38.9,
    lines: [
      [
        { text: "ĐIỀU", startSec: 37.66, endSec: 37.8, color: "#FFFFFF" },
        { text: "HÀNH", startSec: 37.8, endSec: 37.98, color: "#FFFFFF" },
      ],
      [
        { text: "CHIP", startSec: 37.98, endSec: 38.26, color: "#00E5FF" },
        { text: "AI.", startSec: 38.26, endSec: 38.48, color: "#00E5FF" },
      ],
    ],
  },
  {
    startSec: 38.9,
    endSec: 40.0,
    lines: [
      [
        { text: "KHÔNG", startSec: 39.1, endSec: 39.22, color: "#FFFFFF" },
        { text: "NGƯỜI", startSec: 39.22, endSec: 39.36, color: "#FFFFFF" },
      ],
      [
        { text: "KẾ", startSec: 39.36, endSec: 39.54, color: "#FF3B47" },
        { text: "NHIỆM,", startSec: 39.54, endSec: 39.76, color: "#FF3B47" },
      ],
    ],
  },
  {
    startSec: 40.0,
    endSec: 41.78,
    lines: [
      [
        { text: "LIỆU", startSec: 40.16, endSec: 40.26, color: "#FFFFFF" },
        { text: "NGAI", startSec: 40.26, endSec: 40.44, color: "#FFE600" },
        { text: "VÀNG", startSec: 40.44, endSec: 40.7, color: "#FFE600" },
        { text: "NVIDIA", startSec: 40.7, endSec: 41.02, color: "#FFFFFF" },
      ],
      [
        { text: "CÓ", startSec: 41.02, endSec: 41.46, color: "#FFFFFF" },
        { text: "GIỮ", startSec: 41.46, endSec: 41.64, color: "#FFFFFF" },
        { text: "VỮNG", startSec: 41.64, endSec: 41.78, color: "#FFFFFF" },
      ],
    ],
  },
  {
    startSec: 41.78,
    endSec: 42.9,
    lines: [
      [
        { text: "HAY", startSec: 41.78, endSec: 42.0, color: "#FFFFFF" },
        { text: "SẮP", startSec: 42.0, endSec: 42.14, color: "#FFFFFF" },
        { text: "CHUYỂN", startSec: 42.14, endSec: 42.34, color: "#FFFFFF" },
        { text: "GIAO", startSec: 42.34, endSec: 42.58, color: "#FFFFFF" },
      ],
      [
        { text: "LỊCH", startSec: 42.58, endSec: 42.62, color: "#FF3B47" },
        { text: "SỬ?", startSec: 42.62, endSec: 42.86, color: "#FF3B47" },
      ],
    ],
  },
];
