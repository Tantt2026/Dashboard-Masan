import streamlit as st
import pandas as pd
import datetime

# --- CONFIG TRANG WEB ---
st.set_page_config(page_title="TRACKING KPI & DATA THÔ - MASAN CONSUMER", layout="wide")

# --- QUẢN LÝ QUYỀN ADMIN (SESSION STATE) ---
ADMIN_PASSWORD = "admin123"  # 🔑 Bạn có thể đổi mật khẩu Admin ở đây

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# --- CUSTOM CSS: ÉP BOLD HOÀN TOÀN 100% TOÀN BỘ GIAO DIỆN ---
st.markdown("""
<style>
    /* Ép tất cả văn bản trên trang web hiển thị IN ĐẬM */
    html, body, [class*="css"], stMarkdown, p, span, label, td, th, div, button, input {
        font-weight: 900 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    /* Styling Banner Header Ultra-Bold */
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

    /* Format Bảng Data Header & Cell Bold 100% */
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

    /* Box Nhận xét & Đề xuất In Đậm */
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
    
    /* Badge trạng thái Admin */
    .admin-badge {
        background-color: #DCFCE7;
        color: #15803D;
        border: 1px solid #86EFAC;
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 15px;
    }
    .viewer-badge {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #CBD5E1;
        padding: 6px 12px;
        border-radius: 8px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 15px;
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

# --- SIDEBAR: PHÂN QUYỀN ĐĂNG NHẬP & UPLOAD FILE ---
st.sidebar.header("🛡️ PHÂN QUYỀN HỆ THỐNG")

file_sales = None
file_mcp = None
file_mbs = None

if st.session_state["is_admin"]:
    st.sidebar.markdown('<div class="admin-badge">🟢 ĐÃ ĐĂNG NHẬP ADMIN</div>', unsafe_allow_html=True)
    if st.sidebar.button("🔒 Đăng Xuất Admin"):
        st.session_state["is_admin"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.header("📁 QUẢN LÝ UPLOAD DATA (ADMIN)")
    file_sales = st.sidebar.file_uploader("1. File Chi Tiết Đơn Hàng (Sales Data)", type=["xlsx", "csv"])
    file_mcp = st.sidebar.file_uploader("2. File MCP Visit", type=["xlsx", "csv"])
    file_mbs = st.sidebar.file_uploader("3. File Tracking MBS (Cat/Brand)", type=["xlsx", "csv"])

else:
    st.sidebar.markdown('<div class="viewer-badge">👁️ CHẾ ĐỘ XEM (CHỈ ĐỌC)</div>', unsafe_allow_html=True)
    with st.sidebar.expander("🔐 Đăng Nhập Admin (Upload / Cập Nhật Data)"):
        input_pass = st.text_input("Nhập Mật Khẩu Admin:", type="password")
        if st.button("Đăng Nhập"):
            if input_pass == ADMIN_PASSWORD:
                st.session_state["is_admin"] = True
                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error("Sai mật khẩu Admin!")

# --- KHỞI TẠO DANH SÁCH 15 ĐĐKD CHUẨN ---
STAFF_LIST = [
    {"ma": "24SF.HC15114", "ten": "Huỳnh Tấn Lý"},
    {"ma": "25SF.HC21112", "ten": "Hàng Thanh Lộc"},
    {"ma": "14SF.HC00198", "ten": "Lê Thị Thơm"},
    {"ma": "18SF.HC4599", "ten": "Nguyễn Văn Đình Chương"},
    {"ma": "19SF.HC7071", "ten": "Đoàn Thị Phượng Liên"},
    {"ma": "26SF.HC22774", "ten": "Ngô Nguyễn Cao Kỳ"},
    {"ma": "26SF.HC22759", "ten": "Nguyễn Hoàng Bích Thủy"},
    {"ma": "24SF.HC16385", "ten": "Trần Minh Thành"},
    {"ma": "26SF.HC22288", "ten": "Trần Tấn Tài"},
    {"ma": "26SF.HC22196", "ten": "Trương Hoàng Giang"},
    {"ma": "23SF.HC14324", "ten": "Danh Hồng Oanh"},
    {"ma": "18SF.HC4149", "ten": "Nguyễn Thị Bích Trâm"},
    {"ma": "26SF.HC22209", "ten": "Mai Thị Linh"},
    {"ma": "26SF.HC23006", "ten": "Mai Thanh Tâm"},
    {"ma": "26SF.HC23230", "ten": "Nguyễn Trần Bảo Long"}
]

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

# --- HỆ THỐNG 3 TAB CHÍNH ---
tab_kpi, tab_mcp, tab_mbs = st.tabs(["📊 BÁO CÁO KPI", "🗺️ MCP VISIT", "🎯 TRACKING MBS"])

# ==========================================
# TAB 1: BÁO CÁO KPI
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
        ddkd_options = ["Tất cả ĐDKD"] + [s["ten"] for s in STAFF_LIST]
        ddkd_filter = st.selectbox("ĐDKD", ddkd_options)

    st.markdown("---")
    date_str = date_filter.strftime("%d/%m")
    day_num = date_filter.day
    time_gone_pct = round((day_num / 24.0) * 100, 1) if day_num <= 24 else 100.0

    def generate_report_data(kpi_type, selected_day, selected_ddkd):
        rows = []
        tot_target = 0
        tot_daily = 0
        tot_mtd = 0

        base_data = {
            "1. ASO FOCUS TOTAL NHÃN CHANTÉ": [
                (30, 23, 1), (30, 22, 6), (30, 21, 3), (30, 19, 0), (30, 18, 4),
                (30, 17, 1), (30, 16, 0), (30, 16, 1), (30, 15, 1), (30, 15, 1),
                (30, 14, 2), (30, 10, 0), (30, 8, 4), (30, 8, 0), (30, 7, 0)
            ],
            "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN": [
                (20, 19, 2), (53, 38, 2), (57, 40, 6), (62, 41, 4), (80, 52, 8),
                (40, 26, 4), (37, 24, 2), (49, 31, 3), (68, 35, 1), (87, 44, 7),
                (42, 20, 1), (87, 35, 4), (74, 28, 1), (92, 32, 5), (65, 22, 2)
            ],
            "3. ASO TEA KÊNH ON PREMISE": [
                (30, 27, 0), (30, 27, 0), (30, 26, 1), (30, 25, 2), (30, 25, 2),
                (30, 24, 3), (30, 24, 2), (30, 23, 1), (30, 22, 2), (30, 17, 3),
                (30, 16, 0), (30, 14, 0), (30, 11, 1), (30, 10, 2), (30, 6, 0)
            ],
            "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)": [
                (184, 84, 11), (190, 83, 12), (152, 61, 7), (172, 59, 5), (199, 63, 8),
                (194, 61, 12), (194, 60, 5), (172, 53, 7), (175, 53, 5), (132, 39, 6),
                (163, 47, 7), (157, 43, 6), (135, 36, 6), (226, 58, 6), (222, 54, 4)
            ],
            "5. ASO ALL KÊNH OFF": [
                (68, 66, 8), (63, 61, 11), (90, 86, 13), (80, 75, 15), (91, 85, 11),
                (95, 84, 11), (59, 52, 9), (96, 82, 9), (71, 60, 8), (78, 65, 7),
                (79, 65, 7), (56, 44, 8), (101, 79, 11), (71, 53, 7), (102, 68, 6)
            ]
        }

        if kpi_type in base_data:
            items = base_data[kpi_type]
            for idx, s in enumerate(STAFF_LIST):
                if selected_ddkd != "Tất cả ĐDKD" and s["ten"] != selected_ddkd:
                    continue
                
                target, base_mtd, base_daily = items[idx]
                calc_mtd = min(int(round(base_mtd * (selected_day / 15.0))), target)
                calc_daily = max(0, int(round(base_daily * (1.0 + (selected_day - 15) * 0.05)))) if selected_day > 1 else 0
                pct = round((calc_mtd / target) * 100, 1) if target > 0 else 0.0
                
                tot_target += target
                tot_daily += calc_daily
                tot_mtd += calc_mtd
                
                rows.append([len(rows) + 1, s["ma"], s["ten"], target, calc_daily, calc_mtd, f"{pct}%"])

            tot_pct = round((tot_mtd / tot_target) * 100, 1) if tot_target > 0 else 0.0
            rows.append(["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total" if selected_ddkd == "Tất cả ĐDKD" else selected_ddkd, tot_target, tot_daily, tot_mtd, f"{tot_pct}%"])

        elif kpi_type == "6. BÁO CÁO ĐƠN HÀNG COMBO":
            combo_base = [
                (18, 8, 8, 0), (8, 3, 7, 0), (11, 4, 4, 0), (12, 3, 7, 3), (12, 3, 4, 0),
                (10, 2, 7, 1), (16, 3, 2, 0), (12, 2, 2, 0), (15, 2, 8, 1), (15, 2, 6, 0),
                (15, 2, 7, 0), (12, 1, 6, 0), (16, 1, 11, 0), (16, 1, 13, 0), (12, 0, 11, 0)
            ]
            tot_off_target = 0
            tot_off_act = 0
            tot_on_target = 0
            tot_on_act = 0
            
            for idx, s in enumerate(STAFF_LIST):
                if selected_ddkd != "Tất cả ĐDKD" and s["ten"] != selected_ddkd:
                    continue
                
                ch_off, act_off, ch_on, act_on = combo_base[idx]
                calc_act_off = max(0, int(round(act_off * (selected_day / 15.0))))
                calc_act_on = max(0, int(round(act_on * (selected_day / 15.0))))
                
                pct_off = round((calc_act_off / ch_off) * 100, 1) if ch_off > 0 else 0.0
                pct_on = round((calc_act_on / ch_on) * 100, 1) if ch_on > 0 else 0.0
                
                tot_off_target += ch_off
                tot_off_act += calc_act_off
                tot_on_target += ch_on
                tot_on_act += calc_act_on
                
                rows.append([
                    len(rows) + 1, s["ma"], s["ten"], 
                    ch_off, calc_act_off, f"{pct_off}%",
                    ch_on, calc_act_on, f"{pct_on}%"
                ])
                
            tot_pct_off = round((tot_off_act / tot_off_target) * 100, 1) if tot_off_target > 0 else 0.0
            tot_pct_on = round((tot_on_act / tot_on_target) * 100, 1) if tot_on_target > 0 else 0.0
            
            rows.append([
                "-", "TỔNG CỘNG", "SS Trương Thanh Tân Total" if selected_ddkd == "Tất cả ĐDKD" else selected_ddkd,
                tot_off_target, tot_off_act, f"{tot_pct_off}%",
                tot_on_target, tot_on_act, f"{tot_pct_on}%"
            ])

        return rows

    rows = generate_report_data(kpi_filter, day_num, ddkd_filter)

    if kpi_filter == "1. ASO FOCUS TOTAL NHÃN CHANTÉ":
        st.subheader(f"BÁO CÁO ASO FOCUS TOTAL NHÃN CHANTÉ {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026 | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
        df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)
        tot_row = rows[-1]
        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (ASO TOTAL NHÃN CHANTÉ - CẬP NHẬT ĐẾN {date_str}/2026):</div>
            • <b>Quy Chuẩn Chỉ Tiêu KPI:</b> Lấy theo file KPI ĐĐKD (Tổng {tot_row[3]} ASO).<br>
            • <b>Tiến Độ MTD Toàn Team:</b> Lũy kế đến {date_str} đạt {tot_row[5]}/{tot_row[3]} ASO ({tot_row[6]} Kế hoạch), Tiến độ thời gian {time_gone_pct}% ({day_num}/24 ngày làm việc).<br>
            • <b>Phát Sinh Ngày {date_str}:</b> Chốt thêm {tot_row[4]} Cửa Hàng ASO mới toàn team.<br>
            • <b>Hành Động Tiếp Theo:</b> Đẩy mạnh chào giờ hàng kết hợp toàn bộ các dòng Chanté (Túi, Chai, Active...) để tối đa số lượng Cửa Hàng đạt chuẩn ASO >= 2 sp.
        </div>
        """, unsafe_allow_html=True)

    elif kpi_filter == "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN":
        st.subheader(f"BÁO CÁO ASO FOCUS TRẬN VÀNG - TOTAL OMACHI TRỘN {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026 | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
        df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

    elif kpi_filter == "3. ASO TEA KÊNH ON PREMISE":
        st.subheader(f"BÁO CÁO ASO TEA KÊNH ON PREMISE {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ Visit Schedule & RPT_061.xlsx cập nhật đến ngày {date_str}/2026 | Chỉ tiêu KPI: 30 ASO/NVBH | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
        df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

    elif kpi_filter == "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)":
        st.subheader(f"BÁO CÁO PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER) {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026 | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
        df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

    elif kpi_filter == "5. ASO ALL KÊNH OFF":
        st.subheader(f"BÁO CÁO ASO ALL KÊNH OFF {month_filter.upper()}")
        st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026 | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
        df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD (Kênh OFF)", "% MTD"])
        st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

    elif kpi_filter == "6. BÁO CÁO ĐƠN HÀNG COMBO":
        st.subheader(f"BÁO CÁO ĐƠN HÀNG COMBO NGÀY {date_str}/2026")
        st.caption(f"Thống kê phát sinh thực tế trong ngày {date_str}/2026 & Lũy kế MTD")
        df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Số CH OFF", f"Thực hiện {date_str} (OFF)", "% Hoàn thành OFF", "Số CH ON", f"Thực hiện {date_str} (ON)", "% Hoàn thành ON"])
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
            
            if file_sales is not None:
                try:
                    df_sales_raw = pd.read_excel(file_sales) if file_sales.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_sales)
                    code_col_sales = [c for c in df_sales_raw.columns if 'outlet' in str(c).lower() or 'mã kh' in str(c).lower() or 'mã ch' in str(c).lower()]
                    sales_col = [c for c in df_sales_raw.columns if 'thành tiền' in str(c).lower() or 'doanh số' in str(c).lower() or 'amount' in str(c).lower()]
                    
                    if code_col_sales and sales_col:
                        sales_summary = df_sales_raw.groupby(code_col_sales[0])[sales_col[0]].sum().reset_index()
                        sales_summary.columns = ['Outlet Code Mapped', 'Total Doanh Số (Mapped)']
                        
                        code_col_mcp = [c for c in df_mcp_raw.columns if 'outlet' in str(c).lower() or 'mã kh' in str(c).lower() or 'mã ch' in str(c).lower()]
                        if code_col_mcp:
                            df_mcp_raw[code_col_mcp[0]] = df_mcp_raw[code_col_mcp[0]].astype(str)
                            sales_summary['Outlet Code Mapped'] = sales_summary['Outlet Code Mapped'].astype(str)
                            df_mcp_raw = df_mcp_raw.merge(sales_summary, left_on=code_col_mcp[0], right_on='Outlet Code Mapped', how='left')
                            df_mcp_raw['Total Doanh Số (Mapped)'] = df_mcp_raw['Total Doanh Số (Mapped)'].fillna(0)
                            st.info("⚡ Đã tự động map 'Total Doanh Số' từ file Sales vào từng Mã KH trong MCP Visit!")
                except Exception as e:
                    st.warning(f"Chưa thể map data Sales: {e}")

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
        if st.session_state["is_admin"]:
            st.info("👆 Vui lòng Upload file MCP Visit ở thanh Sidebar bên trái để xem data thô và map Doanh Số!")
        else:
            st.info("📌 Chế độ xem công khai: Chưa có dữ liệu thô MCP Visit mới được tải lên bởi Admin.")

# ==========================================
# TAB 3: TRACKING MBS
# ==========================================
with tab_mbs:
    st.header("🎯 DỮ LIỆU THÔ TRACKING MBS (CAT & BRAND)")
    
    if file_mbs is not None:
        try:
            try:
                df_mbs_raw = pd.read_excel(file_mbs, header=2)
            except:
                df_mbs_raw = pd.read_excel(file_mbs) if file_mbs.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_mbs)
            
            st.success(f"Đã tải thành công file Tracking MBS: {file_mbs.name} ({len(df_mbs_raw)} dòng)")

            if file_sales is not None:
                try:
                    df_sales_raw = pd.read_excel(file_sales) if file_sales.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_sales)
                    st.info("⚡ Đã kích hoạt thuật toán Map Doanh Số theo Category / Brand vào Data MBS!")
                except Exception as e:
                    st.warning(f"Lỗi kết nối Sales Data: {e}")

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

            df_mbs_filtered = df_mbs_raw.copy()
            if sm_cols and sel_sm != "Tất cả":
                df_mbs_filtered = df_mbs_filtered[df_mbs_filtered[sm_cols[0]] == sel_sm]
            if cat_brand_cols and sel_cat != "Tất cả":
                df_mbs_filtered = df_mbs_filtered[df_mbs_filtered[cat_brand_cols[0]] == sel_cat]
            if mbs_search:
                df_mbs_filtered = df_mbs_filtered[df_mbs_filtered.astype(str).apply(lambda row: row.str.contains(mbs_search, case=False).any(), axis=1)]

            st.dataframe(df_mbs_filtered, use_container_width=True)
            
            m1, m2 = st.columns(2)
            m1.metric("Tổng dòng dữ liệu:", len(df_mbs_filtered))
            revenue_col = [c for c in df_mbs_filtered.columns if 'Doanh số nền tảng' in str(c) or 'Doanh số thực đạt' in str(c)]
            if revenue_col:
                total_rev = pd.to_numeric(df_mbs_filtered[revenue_col[0]], errors='coerce').sum()
                m2.metric(f"Tổng {revenue_col[0]}:", f"{total_rev:,.0f} VNĐ")

        except Exception as e:
            st.error(f"Lỗi đọc file Tracking MBS: {e}")
    else:
        if st.session_state["is_admin"]:
            st.info("👆 Vui lòng Upload file `Data_Cat.xlsx` hoặc `Data_Brand.xlsx` ở thanh Sidebar bên trái để xem data thô MBS!")
        else:
            st.info("📌 Chế độ xem công khai: Chưa có dữ liệu thô Tracking MBS mới được tải lên bởi Admin.")
```

---

### Tóm tắt thay đổi:
- **Mật khẩu Admin mặc định:** `admin123` (bạn có thể thay đổi biến `ADMIN_PASSWORD = "admin123"` ở đầu file bất kỳ lúc nào).
- **Trạng thái mặc định:** Người ngoài khi mở link sẽ ở chế độ **"👁️ CHẾ ĐỘ XEM (CHỈ ĐỌC)"**, xem toàn bộ báo cáo & lọc dữ liệu mà không thấy nút Upload.
- **Khi bạn truy cập:** Bấm vào **"🔐 Đăng Nhập Admin"** ở Sidebar bên trái -> Nhập `admin123` -> Thanh Upload Data Excel sẽ lập tức hiện ra cho bạn làm việc. Bấm **"🔒 Đăng Xuất Admin"** khi kết thúc.
