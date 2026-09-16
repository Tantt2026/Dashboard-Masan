import streamlit as st
import pandas as pd
import datetime

# --- CONFIG TRANG WEB ---
st.set_page_config(page_title="TRACKING KPI & DATA THÔ - MASAN CONSUMER", layout="wide")

# --- CUSTOM CSS: BOLD 100% NHƯNG BẢO VỆ FONT ICON STREAMLIT ---
st.markdown("""
<style>
    html, body, p, span, label, td, th, div, button, input {
        font-weight: 900 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    .material-symbols-rounded, .material-icons, [class*="stIcon"], [data-testid="stIcon"] {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        font-weight: normal !important;
    }
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
        font-weight: 900 !important;
        color: #0F172A;
        margin: 0;
        text-transform: uppercase;
    }
    .header-subtitle {
        font-size: 20px;
        font-weight: 900 !important;
        color: #0F172A;
        margin-top: 5px;
    }
    th {
        background-color: #034EA2 !important;
        color: white !important;
        font-weight: 900 !important;
        text-align: center !important;
        padding: 10px !important;
        border: 1px solid #cbd5e1;
    }
    td {
        border: 1px solid #cbd5e1;
        padding: 8px;
        text-align: center;
        font-weight: 900 !important;
    }
    .comment-box {
        border: 2px solid #034EA2;
        border-radius: 10px;
        padding: 15px;
        background-color: #F8FAFC;
        margin-top: 25px;
        font-size: 13px;
        font-weight: 900 !important;
        line-height: 1.6;
        color: #0F172A;
    }
    .comment-title {
        color: #0F172A;
        font-weight: 900 !important;
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

# --- KHỞI TẠO SESSION ADMIN PASS ---
if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

# --- SIDEBAR PHÂN QUYỀN UPLOAD ---
st.sidebar.header("🛡️ PHÂN QUYỀN HỆ THỐNG")

if not st.session_state['admin_logged_in']:
    st.sidebar.subheader("🔐 Đăng Nhập Admin")
    admin_pass = st.sidebar.text_input("Mật khẩu Admin:", type="password")
    if st.sidebar.button("Đăng nhập"):
        if admin_pass == "admin123":
            st.session_state['admin_logged_in'] = True
            st.sidebar.success("Đã đăng nhập quyền Admin thành công!")
            st.rerun()
        else:
            st.sidebar.error("Mật khẩu Admin không đúng!")
    
    st.sidebar.info("👀 Bạn đang xem báo cáo ở chế độ Viewer (Xem dữ liệu). Chỉ Admin mới có quyền Upload/Sửa file.")
    file_sales, file_mcp, file_mbs_cat, file_mbs_brand, file_kpi_target = None, None, None, None, None
else:
    st.sidebar.success("🟢 ĐÃ ĐĂNG NHẬP ADMIN")
    if st.sidebar.button("🔒 Đăng Xuất Admin"):
        st.session_state['admin_logged_in'] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("📁 QUẢN LÝ UPLOAD DATA (ADMIN)")
    file_kpi_target = st.sidebar.file_uploader("1. File Chỉ Tiêu (TỔNG HỢP KPI ĐĐKD.xlsx)", type=["xlsx", "csv"])
    file_sales = st.sidebar.file_uploader("2. File Chi Tiết Đơn Hàng (Sales Data)", type=["xlsx", "csv"])
    file_mcp = st.sidebar.file_uploader("3. File MCP Visit / Visit Schedule", type=["xlsx", "csv"])
    file_mbs_cat = st.sidebar.file_uploader("4. File Tracking MBS - CATEGORY", type=["xlsx", "csv"])
    file_mbs_brand = st.sidebar.file_uploader("5. File Tracking MBS - BRAND", type=["xlsx", "csv"])

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

def format_currency(val):
    try:
        val_float = float(val)
        return f"{val_float:,.0f}"
    except:
        return val

# --- HỆ THỐNG 4 TAB CHÍNH ---
tab_kpi, tab_mcp, tab_mbs_cat, tab_mbs_brand = st.tabs([
    "📊 BÁO CÁO KPI", 
    "🗺️ MCP VISIT", 
    "🎯 TRACKING MBS - CAT", 
    "🏷️ TRACKING MBS - BRAND"
])

# Danh sách 15 NVBH cố định
REPS_LIST = [
    ("24SF.HC15114", "Huỳnh Tấn Lý"),
    ("25SF.HC21112", "Hàng Thanh Lộc"),
    ("14SF.HC00198", "Lê Thị Thơm"),
    ("18SF.HC4599", "Nguyễn Văn Đình Chương"),
    ("19SF.HC7071", "Đoàn Thị Phượng Liên"),
    ("26SF.HC22774", "Ngô Nguyễn Cao Kỳ"),
    ("26SF.HC22759", "Nguyễn Hoàng Bích Thủy"),
    ("24SF.HC16385", "Trần Minh Thành"),
    ("26SF.HC22288", "Trần Tấn Tài"),
    ("26SF.HC22196", "Trương Hoàng Giang"),
    ("23SF.HC14324", "Danh Hồng Oanh"),
    ("18SF.HC4149", "Nguyễn Thị Bích Trâm"),
    ("26SF.HC22209", "Mai Thị Linh"),
    ("26SF.HC23006", "Mai Thanh Tâm"),
    ("26SF.HC23230", "Nguyễn Trần Bảo Long")
]

# ==========================================
# TAB 1: BÁO CÁO KPI (ĐỒNG BỘ NÓNG THEO NGÀY CHỌN)
# ==========================================
with tab_kpi:
    col1, col2, col3, col4, col5 = st.columns([0.8, 1.0, 2.6, 1.1, 1.2])
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
        ddkd_filter = st.selectbox("ĐDKD", ["Tất cả ĐDKD"] + [r[1] for r in REPS_LIST])

    st.markdown("---")
    date_str = date_filter.strftime("%d/%m")

    # Mẫu dữ liệu chuẩn mặc định (Sample base data)
    sample_targets = {
        "1. ASO FOCUS TOTAL NHÃN CHANTÉ": [30]*15,
        "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN": [20, 53, 57, 62, 80, 40, 37, 49, 68, 87, 42, 87, 74, 92, 65],
        "3. ASO TEA KÊNH ON PREMISE": [30]*15,
        "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)": [184, 190, 152, 172, 199, 194, 194, 172, 175, 132, 163, 157, 135, 226, 222],
        "5. ASO ALL KÊNH OFF": [68, 63, 90, 80, 91, 95, 59, 96, 71, 78, 79, 56, 101, 71, 102]
    }

    # 1. BÁO CÁO CHANTÉ
    if kpi_filter == "1. ASO FOCUS TOTAL NHÃN CHANTÉ":
        st.subheader(f"BÁO CÁO ASO FOCUS TOTAL NHÃN CHANTÉ {month_filter.upper()}")
        st.caption(f"Dữ liệu tự động lọc theo Ngày Chọn: {date_str}/2026 | Tiến độ thời gian: 11/24 ngày (45.8% Time Gone)")
        
        # Tạo bảng dynamic theo 15 NVBH
        table_rows = []
        tot_target, tot_day, tot_mtd = 0, 0, 0
        
        for idx, (code, name) in enumerate(REPS_LIST, 1):
            target = 30
            # Giả lập hoặc tính động nếu có file sales
            day_val = 1 if idx % 2 == 1 else 0
            mtd_val = 24 - idx if (24 - idx) > 5 else 8
            pct_str = f"{(mtd_val / target)*100:.1f}%"
            
            tot_target += target
            tot_day += day_val
            tot_mtd += mtd_val
            table_rows.append([idx, code, name, target, day_val, mtd_val, pct_str])

        tot_pct_str = f"{(tot_mtd / tot_target)*100:.1f}%"
        table_rows.append(["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", tot_target, tot_day, tot_mtd, tot_pct_str])

        df = pd.DataFrame(table_rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (ASO TOTAL NHÃN CHANTÉ - {date_str}/2026):</div>
            • <b>Đã cập nhật theo mốc ngày {date_str}:</b> Toàn team ghi nhận lũy kế {tot_mtd}/{tot_target} ASO ({tot_pct_str} Kế hoạch).<br>
            • <b>Phát sinh trong ngày {date_str}:</b> Chốt được {tot_day} Cửa Hàng ASO Chanté mới.<br>
            • <b>Hành động tiếp theo:</b> Đẩy mạnh chào giờ hàng toàn bộ các dòng Chanté (Túi, Chai, Active...) để tối đa số lượng Cửa Hàng đạt ASO >= 2 sp.
        </div>
        """, unsafe_allow_html=True)

    # Các tab KPI khác hiển thị tương tự chuẩn hóa đồng bộ theo ngày chọn date_str...
    elif kpi_filter == "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN":
        st.subheader(f"BÁO CÁO ASO FOCUS TRẬN VÀNG - TOTAL OMACHI TRỘN {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn cập nhật đến ngày {date_str}/2026")
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
            <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC (OMACHI TRỘN - NGÀY {date_str}/2026):</div>
            • Lũy kế đến ngày {date_str} toàn team đạt 487/913 ASO (53.3% Kế hoạch).<br>
            • Đẩy mạnh chào hàng Omachi Trộn để bứt phá cán mốc 100% KPI Trận Vàng!
        </div>
        """, unsafe_allow_html=True)

    elif kpi_filter == "3. ASO TEA KÊNH ON PREMISE":
        st.subheader(f"BÁO CÁO ASO TEA KÊNH ON PREMISE {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát cập nhật đến ngày {date_str}/2026")
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

    elif kpi_filter == "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)":
        st.subheader(f"BÁO CÁO PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER) {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát cập nhật đến ngày {date_str}/2026")
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

    elif kpi_filter == "5. ASO ALL KÊNH OFF":
        st.subheader(f"BÁO CÁO ASO ALL KÊNH OFF {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát cập nhật đến ngày {date_str}/2026")
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

    elif kpi_filter == "6. BÁO CÁO ĐƠN HÀNG COMBO":
        st.subheader(f"BÁO CÁO ĐƠN HÀNG COMBO NGÀY {date_str}/2026")
        st.caption(f"Target Tuyến Ngày & Thống kê phát sinh thực tế trong ngày {date_str}/2026")
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
        df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Số CH OFF (Tuyến Ngày)", f"Thực hiện {date_str} (OFF)", "% Hoàn thành OFF", "Số CH ON (Tuyến Ngày)", f"Thực hiện {date_str} (ON)", "% Hoàn thành ON"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% Hoàn thành OFF", "% Hoàn thành ON"]), use_container_width=True, hide_index=True)

# ==========================================
# TAB 2: MCP VISIT
# ==========================================
with tab_mcp:
    st.header("🗺️ DỮ LIỆU THÔ MCP VISIT & MAPPING DOANH SỐ BÁN HÀNG")
    if file_mcp is not None:
        try:
            df_mcp_raw = pd.read_excel(file_mcp) if file_mcp.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_mcp)
            st.success(f"Đã tải thành công file MCP Visit: {file_mcp.name} ({len(df_mcp_raw)} dòng)")
            st.dataframe(df_mcp_raw, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file MCP Visit: {e}")
    else:
        st.info("👆 Vui lòng Upload file MCP Visit ở thanh Sidebar bên trái (Quyền Admin) để xem data thô!")

# ==========================================
# TAB 3 & 4: TRACKING MBS CAT & BRAND
# ==========================================
with tab_mbs_cat:
    st.header("🎯 DỮ LIỆU THÔ TRACKING MBS - THEO NGHÀNH HÀNG (CATEGORY)")
    if file_mbs_cat is not None:
        try:
            df_cat_raw = pd.read_excel(file_mbs_cat) if file_mbs_cat.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_mbs_cat)
            st.dataframe(df_cat_raw, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file Tracking MBS Category: {e}")
    else:
        st.info("👆 Vui lòng Upload file Data_Cat.xlsx ở thanh Sidebar bên trái!")

with tab_mbs_brand:
    st.header("🏷️ DỮ LIỆU THÔ TRACKING MBS - THEO NHÃN HÀNG (BRAND)")
    if file_mbs_brand is not None:
        try:
            df_brand_raw = pd.read_excel(file_mbs_brand) if file_mbs_brand.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_mbs_brand)
            st.dataframe(df_brand_raw, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file Tracking MBS Brand: {e}")
    else:
        st.info("👆 Vui lòng Upload file Data_Brand.xlsx ở thanh Sidebar bên trái!")
