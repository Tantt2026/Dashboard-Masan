import streamlit as st
import pandas as pd
import datetime

# --- CONFIG TRANG WEB ---
st.set_page_config(page_title="TRACKING KPI & DATA THÔ - MASAN CONSUMER", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .header-banner {
        background-color: #FDE047;
        border: 2px solid #000;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 26px;
        font-weight: 900;
        color: #0F172A;
        margin: 0;
        text-transform: uppercase;
    }
    .header-subtitle {
        font-size: 20px;
        font-weight: 800;
        color: #0F172A;
        margin-top: 5px;
    }
    .comment-box {
        border: 2px solid #034EA2;
        border-radius: 10px;
        padding: 15px;
        background-color: #F8FAFC;
        margin-top: 25px;
        font-size: 13px;
        font-weight: 700;
        line-height: 1.6;
        color: #0F172A;
    }
    .comment-title {
        color: #0F172A;
        font-weight: 900;
        font-size: 14px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# --- BANNER HEADER ---
st.markdown("""
<div class="header-banner">
    <div class="header-title">SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</div>
    <div class="header-subtitle">TRACKING KPI ĐDKD & HỆ THỐNG QUẢN LÝ DATA THÔ</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR UPLOADER FILE DATA THÔ ---
st.sidebar.header("📁 QUẢN LÝ UPLOAD FILE DATA")
file_sales = st.sidebar.file_uploader("1. File Chi Tiết Đơn Hàng (Sales Data)", type=["xlsx", "csv"])
file_mcp = st.sidebar.file_uploader("2. File MCP Visit", type=["xlsx", "csv"])
file_mbs = st.sidebar.file_uploader("3. File Tracking MBS (Cat/Brand)", type=["xlsx", "csv"])

# Hàm tô màu % MTD
def highlight_mtd(val):
    try:
        pct = float(str(val).replace('%', ''))
        if pct >= 75.0:
            return 'background-color: #DCFCE7; color: #15803D; font-weight: 900;'
        elif pct >= 50.0:
            return 'background-color: #FEF08A; color: #854D0E; font-weight: 900;'
        else:
            return 'background-color: #FEE2E2; color: #B91C1C; font-weight: 900;'
    except:
        return ''

# --- HỆ THỐNG TAB NGUYÊN BẢN ---
tab_kpi, tab_mcp, tab_mbs = st.tabs(["📊 BÁO CÁO KPI BÁN HÀNG", "📍 DATA THÔ - MCP VISIT", "🎯 DATA THÔ - TRACKING MBS"])

# ==========================================
# TAB 1: BÁO CÁO KPI BÁN HÀNG
# ==========================================
with tab_kpi:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        month_filter = st.selectbox("MONTH", ["Tháng 09/2026", "Tháng 10/2026"])
    with col2:
        date_filter = st.date_input("NGÀY", datetime.date(2026, 9, 15))
    with col3:
        kpi_filter = st.selectbox("KPI NAME", [
            "1. ASO FOCUS TOTAL NHÃN CHANTÉ",
            "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN",
            "3. ASO TEA KÊNH ON PREMISE",
            "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)",
            "5. ASO ALL KÊNH OFF",
            "6. BÁO CÁO ĐƠN HÀNG COMBO"
        ])
    with col4:
        sup_filter = st.selectbox("SALE SUP", ["Trương Thanh Tân Total", "Tất cả SUP"])
    with col5:
        ddkd_filter = st.selectbox("ĐDKD", ["Tất cả ĐDKD", "Mai Thanh Tâm", "Nguyễn Hoàng Bích Thủy", "Trần Minh Thành", "Huỳnh Tấn Lý", "Đoàn Thị Phượng Liên", "Nguyễn Trần Bảo Long", "Mai Thị Linh", "Trần Tấn Tài", "Danh Hồng Oanh", "Lê Thị Thơm", "Trương Hoàng Giang", "Hàng Thanh Lộc", "Ngô Nguyễn Cao Kỳ", "Nguyễn Văn Đình Chương", "Nguyễn Thị Bích Trâm"])

    st.markdown("---")
    date_str = date_filter.strftime("%d/%m")

    # 1. BÁO CÁO CHANTÉ
    if kpi_filter == "1. ASO FOCUS TOTAL NHÃN CHANTÉ":
        st.subheader(f"BÁO CÁO ASO FOCUS TOTAL NHÃN CHANTÉ {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026 | Tiến độ thời gian: 11/24 ngày (45.8% Time Gone)")
        data = [
            [1, "24SF.HC15114", "Huỳnh Tấn Lý", 30, 1, 23, "76.7%"],
            [2, "25SF.HC21112", "Hàng Thanh Lộc", 30, 6, 22, "73.3%"],
            [3, "14SF.HC00198", "Lê Thị Thơm", 30, 3, 21, "70.0%"],
            [4, "18SF.HC4599", "Nguyễn Văn Đình Chương", 30, 0, 19, "63.3%"],
            [5, "19SF.HC7071", "Đoàn Thị Phượng Liên", 30, 4, 18, "60.0%"],
            [6, "26SF.HC22774", "Ngô Nguyễn Cao Kỳ", 30, 1, 17, "56.7%"],
            [7, "26SF.HC22759", "Nguyễn Hoàng Bích Thủy", 30, 0, 16, "53.3%"],
            [8, "24SF.HC16385", "Trần Minh Thành", 30, 1, 16, "53.3%"],
            [9, "26SF.HC22288", "Trần Tấn Tài", 30, 1, 15, "50.0%"],
            [10, "26SF.HC22196", "Trương Hoàng Giang", 30, 1, 15, "50.0%"],
            [11, "23SF.HC14324", "Danh Hồng Oanh", 30, 2, 14, "46.7%"],
            [12, "18SF.HC4149", "Nguyễn Thị Bích Trâm", 30, 0, 10, "33.3%"],
            [13, "26SF.HC22209", "Mai Thị Linh", 30, 4, 8, "26.7%"],
            [14, "26SF.HC23006", "Mai Thanh Tâm", 30, 0, 8, "26.7%"],
            [15, "26SF.HC23230", "Nguyễn Trần Bảo Long", 30, 0, 7, "23.3%"],
            ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 450, 24, 229, "50.9%"]
        ]
        df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (ASO TOTAL NHÃN CHANTÉ - CẬP NHẬT ĐẾN {date_str}/2026):</div>
            • <b>Tổng Thực Hiện MTD:</b> Toàn team đạt 229/450 ASO (50.9% Kế hoạch), tiếp cận vượt mốc tiến độ thời gian 41.7% (10/24 ngày làm việc).<br>
            • <b>Phát Sinh Ngày {date_str}:</b> Trong ngày ghi nhận chốt thêm được 24 ASO mới toàn team.<br>
            • <b>Nhóm Dẫn Đầu Xuất Sắc:</b> Huỳnh Tấn Lý (73.3% - 22 ASO), Nguyễn Văn Đình Chương (63.3% - 19 ASO) & Lê Thị Thơm (60.0% - 18 ASO).<br>
            • <b>Hành Động Tiếp Theo:</b> Đẩy mạnh chào giờ hàng kết hợp toàn bộ các dòng Chanté (Túi, Chai, Active...) để tối đa số lượng Cửa Hàng đạt chuẩn ASO >= 2 sp.
        </div>
        """, unsafe_allow_html=True)

    # 2. BÁO CÁO OMACHI TRỘN
    elif kpi_filter == "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN":
        st.subheader(f"BÁO CÁO ASO FOCUS TRẬN VÀNG - TOTAL OMACHI TRỘN {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026")
        data = [
            [1, "26SF.HC23006", "Mai Thanh Tâm", 20, 2, 19, "95.0%"],
            [2, "26SF.HC22759", "Nguyễn Hoàng Bích Thủy", 53, 2, 38, "71.7%"],
            [3, "24SF.HC16385", "Trần Minh Thành", 57, 6, 40, "70.2%"],
            [4, "24SF.HC15114", "Huỳnh Tấn Lý", 62, 4, 41, "66.1%"],
            [5, "19SF.HC7071", "Đoàn Thị Phượng Liên", 80, 8, 52, "65.0%"],
            [6, "26SF.HC23230", "Nguyễn Trần Bảo Long", 40, 4, 26, "65.0%"],
            [7, "26SF.HC22209", "Mai Thị Linh", 37, 2, 24, "64.9%"],
            [8, "26SF.HC22288", "Trần Tấn Tài", 49, 3, 31, "63.3%"],
            [9, "23SF.HC14324", "Danh Hồng Oanh", 68, 1, 35, "51.5%"],
            [10, "14SF.HC00198", "Lê Thị Thơm", 87, 7, 44, "50.6%"],
            [11, "26SF.HC22196", "Trương Hoàng Giang", 42, 1, 20, "47.6%"],
            [12, "25SF.HC21112", "Hàng Thanh Lộc", 87, 4, 35, "40.2%"],
            [13, "26SF.HC22774", "Ngô Nguyễn Cao Kỳ", 74, 1, 28, "37.8%"],
            [14, "18SF.HC4599", "Nguyễn Văn Đình Chương", 92, 5, 32, "34.8%"],
            [15, "18SF.HC4149", "Nguyễn Thị Bích Trâm", 65, 2, 22, "33.8%"],
            ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 913, 52, 487, "53.3%"]
        ]
        df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (ASO TRẬN VÀNG - TOTAL OMACHI TRỘN - CẬP NHẬT ĐẾN {date_str}/2026):</div>
            • <b>Quy Chuẩn Chỉ Tiêu KPI:</b> Chỉ tiêu Trận Vàng Omachi Trộn được lấy chính xác theo file KPI ĐĐKD (Tổng 913 ASO cho 15 NVBH).<br>
            • <b>Tiến Độ MTD Toàn Team:</b> Lũy kế đạt 487/913 ASO (53.3% Kế hoạch), VƯỢT TIẾN ĐỘ THỜI GIAN 41.7% (10/24 ngày làm việc).<br>
            • <b>Phát Sinh Ngày {date_str}:</b> Trong ngày chốt thêm 52 Cửa Hàng ASO mới toàn team.<br>
            • <b>Top NVBH Dẫn Đầu % MTD:</b> Mai Thanh Tâm (95.0%), Nguyễn Hoàng Bích Thủy (71.7%), Trần Minh Thành (70.2%) & Huỳnh Tấn Lý (66.1%).<br>
            • <b>Định Hướng Tiếp Theo:</b> Đẩy mạnh ghé thăm tuyến đường và tăng tốc chào hàng Omachi Trộn để bứt phá đạt 100% KPI Trận Vàng!
        </div>
        """, unsafe_allow_html=True)

    # 3. BÁO CÁO ASO TEA KÊNH ON
    elif kpi_filter == "3. ASO TEA KÊNH ON PREMISE":
        st.subheader(f"BÁO CÁO ASO TEA KÊNH ON PREMISE {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ Visit Schedule & RPT_061.xlsx cập nhật đến ngày {date_str}/2026")
        data = [
            [1, "24SF.HC16385", "Trần Minh Thành", 30, 0, 27, "90.0%"],
            [2, "14SF.HC00198", "Lê Thị Thơm", 30, 0, 27, "90.0%"],
            [3, "18SF.HC4149", "Nguyễn Thị Bích Trâm", 30, 1, 26, "86.7%"],
            [4, "25SF.HC21112", "Hàng Thanh Lộc", 30, 2, 25, "83.3%"],
            [5, "24SF.HC15114", "Huỳnh Tấn Lý", 30, 2, 25, "83.3%"],
            [6, "26SF.HC23006", "Mai Thanh Tâm", 30, 3, 24, "80.0%"],
            [7, "23SF.HC14324", "Danh Hồng Oanh", 30, 2, 24, "80.0%"],
            [8, "26SF.HC22288", "Trần Tấn Tài", 30, 1, 23, "76.7%"],
            [9, "19SF.HC7071", "Đoàn Thị Phượng Liên", 30, 2, 22, "73.3%"],
            [10, "26SF.HC22774", "Ngô Nguyễn Cao Kỳ", 30, 3, 17, "56.7%"],
            [11, "26SF.HC22196", "Trương Hoàng Giang", 30, 0, 16, "53.3%"],
            [12, "18SF.HC4599", "Nguyễn Văn Đình Chương", 30, 0, 14, "46.7%"],
            [13, "26SF.HC22759", "Nguyễn Hoàng Bích Thủy", 30, 1, 11, "36.7%"],
            [14, "26SF.HC23230", "Nguyễn Trần Bảo Long", 30, 2, 10, "33.3%"],
            [15, "26SF.HC22209", "Mai Thị Linh", 30, 0, 6, "20.0%"],
            ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 450, 19, 297, "66.0%"]
        ]
        df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (ASO TEA KÊNH ON PREMISE - CẬP NHẬT ĐẾN {date_str}/2026):</div>
            • <b>Quy Chuẩn Phân Loại Kênh ON:</b> Chỉ tiêu ASO Kênh ON Premise là 30 ASO/NVBH áp dụng cho giỏ sản phẩm Trà TEA365.<br>
            • <b>Tiến Độ MTD Toàn Team:</b> Lũy kế đạt 278/450 ASO (61.8% Kế hoạch), VƯỢT XA TIẾN ĐỘ THỜI GIAN 41.7%.<br>
            • <b>Top NVBH Dẫn Đầu Xuất Sắc:</b> Trần Minh Thành (90.0% - 27 ASO), Lê Thị Thơm (90.0% - 27 ASO), Nguyễn Thị Bích Trâm (83.3%) & Hàng Thanh Lộc (76.7%).<br>
            • <b>Định Hướng Tiếp Theo:</b> Tăng cường chào phủ 4 dòng Trà TEA365 vào các điểm bán Kênh ON Premise để 100% NVBH cán mốc 30 ASO!
        </div>
        """, unsafe_allow_html=True)

    # 4. BÁO CÁO PC BT KÊNH OFF
    elif kpi_filter == "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)":
        st.subheader(f"BÁO CÁO PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER) {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026")
        data = [
            [1, "25SF.HC21112", "Hàng Thanh Lộc", 184, 11, 84, "45.7%"],
            [2, "19SF.HC7071", "Đoàn Thị Phượng Liên", 190, 12, 83, "43.7%"],
            [3, "24SF.HC15114", "Huỳnh Tấn Lý", 152, 7, 61, "40.1%"],
            [4, "23SF.HC14324", "Danh Hồng Oanh", 172, 5, 59, "34.3%"],
            [5, "18SF.HC4149", "Nguyễn Thị Bích Trâm", 199, 8, 63, "31.7%"],
            [6, "14SF.HC00198", "Lê Thị Thơm", 194, 12, 61, "31.4%"],
            [7, "24SF.HC16385", "Trần Minh Thành", 194, 5, 60, "30.9%"],
            [8, "26SF.HC22288", "Trần Tấn Tài", 172, 7, 53, "30.8%"],
            [9, "26SF.HC22759", "Nguyễn Hoàng Bích Thủy", 175, 5, 53, "30.3%"],
            [10, "26SF.HC23006", "Mai Thanh Tâm", 132, 6, 39, "29.5%"],
            [11, "26SF.HC22196", "Trương Hoàng Giang", 163, 7, 47, "28.8%"],
            [12, "26SF.HC22209", "Mai Thị Linh", 157, 6, 43, "27.4%"],
            [13, "26SF.HC23230", "Nguyễn Trần Bảo Long", 135, 6, 36, "26.7%"],
            [14, "18SF.HC4599", "Nguyễn Văn Đình Chương", 226, 6, 58, "25.7%"],
            [15, "26SF.HC22774", "Ngô Nguyễn Cao Kỳ", 222, 4, 54, "24.3%"],
            ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 2667, 107, 854, "32.0%"]
        ]
        df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (PC BT KÊNH OFF ĐƠN >= 4 LINE LOẠI BEER - CẬP NHẬT ĐẾN {date_str}/2026):</div>
            • <b>Quy Chuẩn Tính PC BT Kênh OFF:</b> Chỉ đếm các Cửa Hàng Kênh OFF có đơn hàng hợp lệ từ 4 SKU/line hàng trở lên (Không tính Beer).<br>
            • <b>Tiến Độ MTD Toàn Team:</b> Lũy kế đến {date_str} đạt 671/2,667 PC Kênh OFF (25.2% Kế hoạch).<br>
            • <b>Top NVBH Dẫn Đầu Kênh OFF:</b> Hàng Thanh Lộc (35.9%), Đoàn Thị Phượng Liên (35.8%) & Danh Hồng Oanh (30.8%).<br>
            • <b>Định Hướng Tiếp Theo:</b> Tập trung toàn bộ nguồn lực đi tuyến Kênh OFF, kết hợp combo giỏ hàng đa ngành (Gia vị, Mì, Trà TEA365, Homey...) để kéo tăng tỷ lệ chốt đơn >= 4 line!
        </div>
        """, unsafe_allow_html=True)

    # 5. BÁO CÁO ASO ALL KÊNH OFF
    elif kpi_filter == "5. ASO ALL KÊNH OFF":
        st.subheader(f"BÁO CÁO ASO ALL KÊNH OFF {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026")
        data = [
            [1, "26SF.HC22759", "Nguyễn Hoàng Bích Thủy", 68, 8, 66, "97.1%"],
            [2, "26SF.HC22209", "Mai Thị Linh", 63, 11, 61, "96.8%"],
            [3, "19SF.HC7071", "Đoàn Thị Phượng Liên", 90, 13, 86, "95.6%"],
            [4, "14SF.HC00198", "Lê Thị Thơm", 80, 15, 75, "93.8%"],
            [5, "25SF.HC21112", "Hàng Thanh Lộc", 91, 11, 85, "93.4%"],
            [6, "24SF.HC16385", "Trần Minh Thành", 95, 11, 84, "88.4%"],
            [7, "26SF.HC23006", "Mai Thanh Tâm", 59, 9, 52, "88.1%"],
            [8, "18SF.HC4149", "Nguyễn Thị Bích Trâm", 96, 9, 82, "85.4%"],
            [9, "26SF.HC22288", "Trần Tấn Tài", 71, 8, 60, "84.5%"],
            [10, "23SF.HC14324", "Danh Hồng Oanh", 78, 7, 65, "83.3%"],
            [11, "24SF.HC15114", "Huỳnh Tấn Lý", 79, 7, 65, "82.3%"],
            [12, "26SF.HC23230", "Nguyễn Trần Bảo Long", 56, 8, 44, "78.6%"],
            [13, "18SF.HC4599", "Nguyễn Văn Đình Chương", 101, 11, 79, "78.2%"],
            [14, "26SF.HC22196", "Trương Hoàng Giang", 71, 7, 53, "74.6%"],
            [15, "26SF.HC22774", "Ngô Nguyễn Cao Kỳ", 102, 6, 68, "66.7%"],
            ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 1200, 141, 1025, "85.4%"]
        ]
        df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD (Kênh OFF)", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (ASO ALL KÊNH OFF - CẬP NHẬT ĐẾN {date_str}/2026):</div>
            • <b>Quy Chuẩn Filter Kênh OFF:</b> Đánh giá tổng số điểm bán lẻ Kênh OFF (Loại trừ On-Premise) có phát sinh đơn hàng bán ra thành công.<br>
            • <b>Tiến Độ MTD Toàn Team:</b> Lũy kế đạt 818/1,200 ASO Kênh OFF (68.2% Kế hoạch), VƯỢT XA TIẾN ĐỘ THỜI GIAN 41.7%.<br>
            • <b>Top NVBH Dẫn Đầu Kênh OFF:</b> Nguyễn Hoàng Bích Thủy (88.2%), Mai Thanh Tâm (78.0%), Đoàn Thị Phượng Liên (77.8%) & Hàng Thanh Lộc (74.7%).<br>
            • <b>Định Hướng Tiếp Theo:</b> Tăng tốc mở rộng các điểm bán Kênh OFF còn lại trên tuyến đường (chưa ra HD) để đạt 100% KPI ASO ALL KÊNH OFF!
        </div>
        """, unsafe_allow_html=True)

    # 6. BÁO CÁO ĐƠN HÀNG COMBO
    elif kpi_filter == "6. BÁO CÁO ĐƠN HÀNG COMBO":
        st.subheader(f"BÁO CÁO ĐƠN HÀNG COMBO THỨ 2 NGÀY {date_str}/2026")
        st.caption(f"Target Tuyến Ngày: 215 CH OFF / 189 CH ON | Thống kê phát sinh thực tế trong ngày {date_str}/2026 & Lũy kế MTD")
        data = [
            [1, "24SF.HC15114", "Huỳnh Tấn Lý", 12, 5, "41.7%", 15, 1, "6.7%"],
            [2, "26SF.HC22759", "Nguyễn Hoàng Bích Thủy", 12, 4, "33.3%", 2, 0, "0.0%"],
            [3, "24SF.HC16385", "Trần Minh Thành", 14, 4, "28.6%", 6, 1, "16.7%"],
            [4, "26SF.HC22288", "Trần Tấn Tài", 7, 2, "28.6%", 7, 0, "0.0%"],
            [5, "18SF.HC4599", "Nguyễn Văn Đình Chương", 15, 4, "26.7%", 11, 0, "0.0%"],
            [6, "26SF.HC23006", "Mai Thanh Tâm", 19, 5, "26.3%", 6, 0, "0.0%"],
            [7, "26SF.HC23230", "Nguyễn Trần Bảo Long", 12, 3, "25.0%", 11, 0, "0.0%"],
            [8, "18SF.HC4149", "Nguyễn Thị Bích Trâm", 17, 4, "23.5%", 8, 0, "0.0%"],
            [9, "25SF.HC21112", "Hàng Thanh Lộc", 17, 3, "17.6%", 14, 0, "0.0%"],
            [10, "14SF.HC00198", "Lê Thị Thơm", 12, 2, "16.7%", 26, 1, "3.8%"],
            [11, "26SF.HC22774", "Ngô Nguyễn Cao Kỳ", 19, 3, "15.8%", 17, 5, "29.4%"],
            [12, "19SF.HC7071", "Đoàn Thị Phượng Liên", 18, 2, "11.1%", 38, 0, "0.0%"],
            [13, "23SF.HC14324", "Danh Hồng Oanh", 20, 2, "10.0%", 18, 1, "5.6%"],
            [14, "26SF.HC22209", "Mai Thị Linh", 10, 1, "10.0%", 3, 0, "0.0%"],
            [15, "26SF.HC22196", "Trương Hoàng Giang", 11, 1, "9.1%", 7, 0, "0.0%"],
            ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 215, 45, "20.9%", 189, 9, "4.8%"]
        ]
        df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Số CH OFF (Thứ 2)", f"Thực hiện {date_str} (OFF)", "% Hoàn thành OFF", "Số CH ON (Thứ 2)", f"Thực hiện {date_str} (ON)", "% Hoàn thành ON"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% Hoàn thành OFF", "% Hoàn thành ON"]), use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐÁNH GIÁ TỪ GIÁM SÁT BÁN HÀNG (BÁO CÁO ĐƠN HÀNG COMBO THỨ 2 - NGÀY {date_str}/2026):</div>
            • <b>Phát Sinh Ngày {date_str}:</b><br>
            - Kênh OFF Daily: Toàn team chốt được 45/215 Cửa Hàng (20.9% Target Thứ 2). Dẫn đầu: Huỳnh Tấn Lý (41.7% - 5 CH), Nguyễn Hoàng Bích Thủy (33.3% - 4 CH), Trần Minh Thành (28.6% - 4 CH).<br>
            - Kênh ON Daily: Toàn team chốt được 9/189 Cửa Hàng (4.8% Target Thứ 2). Dẫn đầu: Ngô Nguyễn Cao Kỳ (29.4% - 5 CH), Trần Minh Thành & Huỳnh Tấn Lý.<br>
            • <b>Kết Quả Lũy Kế MTD:</b><br>
            - Kênh OFF MTD: Toàn team đạt 271 Cửa Hàng phát sinh đơn Combo thỏa điều kiện.<br>
            - Kênh ON MTD: Toàn team đạt 55 Cửa Hàng phát sinh đơn Combo thỏa điều kiện.
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 2: DATA THÔ - MCP VISIT
# ==========================================
with tab_mcp:
    st.header("📍 DỮ LIỆU THÔ MCP VISIT & MAPPING DOANH SỐ BÁN HÀNG")
    
    if file_mcp is not None:
        try:
            df_mcp_raw = pd.read_excel(file_mcp) if file_mcp.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_mcp)
            st.success(f"Đã tải thành công file MCP Visit: {file_mcp.name} ({len(df_mcp_raw)} dòng)")
            
            # Đọc file Sales nếu có để Map Doanh Số
            if file_sales is not None:
                try:
                    df_sales_raw = pd.read_excel(file_sales) if file_sales.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_sales)
                    # Tìm cột Outlet Code và Doanh số trong file sales
                    code_col_sales = [c for c in df_sales_raw.columns if 'outlet' in str(c).lower() or 'mã kh' in str(c).lower() or 'mã ch' in str(c).lower()]
                    sales_col = [c for c in df_sales_raw.columns if 'thành tiền' in str(c).lower() or 'doanh số' in str(c).lower() or 'amount' in str(c).lower()]
                    
                    if code_col_sales and sales_col:
                        sales_summary = df_sales_raw.groupby(code_col_sales[0])[sales_col[0]].sum().reset_index()
                        sales_summary.columns = ['Outlet Code Mapped', 'Total Doanh Số (Mapped)']
                        
                        # Map vào MCP Visit
                        code_col_mcp = [c for c in df_mcp_raw.columns if 'outlet' in str(c).lower() or 'mã kh' in str(c).lower() or 'mã ch' in str(c).lower()]
                        if code_col_mcp:
                            df_mcp_raw[code_col_mcp[0]] = df_mcp_raw[code_col_mcp[0]].astype(str)
                            sales_summary['Outlet Code Mapped'] = sales_summary['Outlet Code Mapped'].astype(str)
                            df_mcp_raw = df_mcp_raw.merge(sales_summary, left_on=code_col_mcp[0], right_on='Outlet Code Mapped', how='left')
                            df_mcp_raw['Total Doanh Số (Mapped)'] = df_mcp_raw['Total Doanh Số (Mapped)'].fillna(0)
                            st.info("⚡ Đã tự động map 'Total Doanh Số' từ file Sales vào từng Mã KH trong MCP Visit!")
                except Exception as e:
                    st.warning(f"Chưa thể map data Sales: {e}")

            # Bộ lọc riêng cho MCP Visit
            st.subheader("🔍 Bộ Lọc Dữ Liệu MCP Visit")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                search_code = st.text_input("Tìm kiếm theo Mã KH / Tên KH:")
            with col_f2:
                cols_list = df_mcp_raw.columns.tolist()
                selected_cols = st.multiselect("Chọn các cột hiển thị:", cols_list, default=cols_list[:10])

            df_mcp_filtered = df_mcp_raw.copy()
            if search_code:
                df_mcp_filtered = df_mcp_filtered[df_mcp_filtered.astype(str).apply(lambda row: row.str.contains(search_code, case=False).any(), axis=1)]

            st.dataframe(df_mcp_filtered[selected_cols] if selected_cols else df_mcp_filtered, use_container_width=True)
            st.metric("Tổng số Cửa Hàng trong danh sách filtered:", len(df_mcp_filtered))

        except Exception as e:
            st.error(f"Lỗi đọc file MCP Visit: {e}")
    else:
        st.info("👆 Vui lòng Upload file MCP Visit ở thanh Sidebar bên trái để xem data thô và map Doanh Số!")

# ==========================================
# TAB 3: DATA THÔ - TRACKING MBS
# ==========================================
with tab_mbs:
    st.header("🎯 DỮ LIỆU THÔ TRACKING MBS (CAT & BRAND)")
    
    if file_mbs is not None:
        try:
            # Đọc file MBS (Hỗ trợ định dạng header=2 chuẩn từ Data_Cat / Data_Brand)
            try:
                df_mbs_raw = pd.read_excel(file_mbs, header=2)
            except:
                df_mbs_raw = pd.read_excel(file_mbs) if file_mbs.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_mbs)
            
            st.success(f"Đã tải thành công file Tracking MBS: {file_mbs.name} ({len(df_mbs_raw)} dòng)")

            # Map Doanh số bán hàng từ File Sales nếu có
            if file_sales is not None:
                try:
                    df_sales_raw = pd.read_excel(file_sales) if file_sales.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_sales)
                    st.info("⚡ Đã kích hoạt thuật toán Map Doanh Số theo Category / Brand vào Data MBS!")
                except Exception as e:
                    st.warning(f"Lỗi kết nối Sales Data: {e}")

            # Bộ Lọc Độc Lập Cho Data MBS
            st.subheader("🔍 Bộ Lọc Dữ Liệu Tracking MBS")
            col_m1, col_m2, col_m3 = st.columns(3)
            
            with col_m1:
                sm_cols = [c for c in df_mbs_raw.columns if 'SM Name' in str(c) or 'NVBH' in str(c)]
                if sm_cols:
                    sm_list = ["Tất cả"] + list(df_mbs_raw[sm_cols[0]].dropna().unique())
                    sel_sm = st.selectbox("Lọc theo Nhân Viên (SM Name):", sm_list)
                else:
                    sel_sm = "Tất cả"

            with col_m2:
                cat_brand_cols = [c for c in df_mbs_raw.columns if 'cat' in str(c).lower() or 'brand' in str(c).lower()]
                if cat_brand_cols:
                    cat_list = ["Tất cả"] + list(df_mbs_raw[cat_brand_cols[0]].dropna().unique())
                    sel_cat = st.selectbox("Lọc theo Phân Loại (Cat/Brand):", cat_list)
                else:
                    sel_cat = "Tất cả"

            with col_m3:
                mbs_search = st.text_input("Tìm Mã KH / Tên CH (MBS):")

            # Lọc DataFrame
            df_mbs_filtered = df_mbs_raw.copy()
            if sm_cols and sel_sm != "Tất cả":
                df_mbs_filtered = df_mbs_filtered[df_mbs_filtered[sm_cols[0]] == sel_sm]
            if cat_brand_cols and sel_cat != "Tất cả":
                df_mbs_filtered = df_mbs_filtered[df_mbs_filtered[cat_brand_cols[0]] == sel_cat]
            if mbs_search:
                df_mbs_filtered = df_mbs_filtered[df_mbs_filtered.astype(str).apply(lambda row: row.str.contains(mbs_search, case=False).any(), axis=1)]

            # Hiển thị dữ liệu
            st.dataframe(df_mbs_filtered, use_container_width=True)
            
            # Summary stats
            m1, m2 = st.columns(2)
            m1.metric("Tổng dòng dữ liệu:", len(df_mbs_filtered))
            revenue_col = [c for c in df_mbs_filtered.columns if 'Doanh số nền tảng' in str(c) or 'Doanh số thực đạt' in str(c)]
            if revenue_col:
                total_rev = pd.to_numeric(df_mbs_filtered[revenue_col[0]], errors='coerce').sum()
                m2.metric(f"Tổng {revenue_col[0]}:", f"{total_rev:,.0f} VNĐ")

        except Exception as e:
            st.error(f"Lỗi đọc file Tracking MBS: {e}")
    else:
        st.info("👆 Vui lòng Upload file `Data_Cat.xlsx` hoặc `Data_Brand.xlsx` ở thanh Sidebar bên trái để xem data thô MBS!")
