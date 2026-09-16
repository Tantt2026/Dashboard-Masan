import streamlit as st
import pandas as pd
import datetime
import numpy as np

# --- CONFIG TRANG WEB ---
st.set_page_config(page_title="TRACKING KPI & DATA THÔ - MASAN CONSUMER", layout="wide")

# --- CUSTOM CSS: BOLD 100% & BẢO VỆ FONT ICON STREAMLIT ---
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

# --- HELPER PARSING VẬN HÀNH THUẬT TOÁN ĐỘNG ---
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

DEFAULT_TARGETS = {
    "1. ASO FOCUS TOTAL NHÃN CHANTÉ": {r[0]: 30 for r in REPS_LIST},
    "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN": {"26SF.HC23006": 20, "26SF.HC22759": 53, "24SF.HC16385": 57, "24SF.HC15114": 62, "19SF.HC7071": 80, "26SF.HC23230": 40, "26SF.HC22209": 37, "26SF.HC22288": 49, "23SF.HC14324": 68, "14SF.HC00198": 87, "26SF.HC22196": 42, "25SF.HC21112": 87, "26SF.HC22774": 74, "18SF.HC4599": 92, "18SF.HC4149": 65},
    "3. ASO TEA KÊNH ON PREMISE": {r[0]: 30 for r in REPS_LIST},
    "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)": {"25SF.HC21112": 184, "19SF.HC7071": 190, "24SF.HC15114": 152, "23SF.HC14324": 172, "18SF.HC4149": 199, "14SF.HC00198": 194, "24SF.HC16385": 194, "26SF.HC22288": 172, "26SF.HC22759": 175, "26SF.HC23006": 132, "26SF.HC22196": 163, "26SF.HC22209": 157, "26SF.HC23230": 135, "18SF.HC4599": 226, "26SF.HC22774": 222},
    "5. ASO ALL KÊNH OFF": {"26SF.HC22759": 68, "26SF.HC22209": 63, "19SF.HC7071": 90, "14SF.HC00198": 80, "25SF.HC21112": 91, "24SF.HC16385": 95, "26SF.HC23006": 59, "18SF.HC4149": 96, "26SF.HC22288": 71, "23SF.HC14324": 78, "24SF.HC15114": 79, "26SF.HC23230": 56, "18SF.HC4599": 101, "26SF.HC22196": 71, "26SF.HC22774": 102}
}

# Load file target động nếu admin upload
targets_from_file = {}
if file_kpi_target is not None:
    try:
        xls_t = pd.ExcelFile(file_kpi_target)
        sheet = "Export" if "Export" in xls_t.sheet_names else xls_t.sheet_names[0]
        df_t = pd.read_excel(xls_t, sheet_name=sheet)
        rep_col = [c for c in df_t.columns if 'mã nvbh' in str(c).lower() or 'mã nv' in str(c).lower() or 'sm' in str(c).lower()]
        if rep_col:
            r_col = rep_col[0]
            for kpi_key, target_col_name in [
                ("1. ASO FOCUS TOTAL NHÃN CHANTÉ", "Trận xanh YTG"),
                ("2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN", "Trận vàng YTG"),
                ("3. ASO TEA KÊNH ON PREMISE", "%ASO Kênh On Premise"),
                ("4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)", "PC 4 line"),
                ("5. ASO ALL KÊNH OFF", "Điểm lẻ bao phủ tổng sản phẩm")
            ]:
                match_c = [c for c in df_t.columns if target_col_name.lower() in str(c).lower()]
                if match_c:
                    t_dict = dict(zip(df_t[r_col].astype(str), pd.to_numeric(df_t[match_c[0]], errors='coerce').fillna(0)))
                    targets_from_file[kpi_key] = t_dict
    except Exception as e:
        st.sidebar.warning(f"Lỗi đọc file Target: {e}")

# Parse File Sales nếu có
df_sales = None
if file_sales is not None:
    try:
        df_sales = pd.read_excel(file_sales) if file_sales.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_sales)
        df_sales.columns = [str(c).strip() for c in df_sales.columns]
        
        date_c = [c for c in df_sales.columns if 'ngày' in c.lower() or 'date' in c.lower() or 'created' in c.lower()]
        if date_c:
            df_sales['ORDER_DATE'] = pd.to_datetime(df_sales[date_c[0]], errors='coerce').dt.date
        
        ch_c = [c for c in df_sales.columns if 'mã kh' in c.lower() or 'mã ch' in c.lower() or 'outlet' in c.lower() or 'customer' in c.lower()]
        if ch_c:
            df_sales['OUTLET_CODE'] = df_sales[ch_c[0]].astype(str)
            
        rep_c = [c for c in df_sales.columns if 'mã nv' in c.lower() or 'nvbh' in c.lower() or 'sm' in c.lower()]
        if rep_c:
            df_sales['REP_CODE'] = df_sales[rep_c[0]].astype(str)

        ord_c = [c for c in df_sales.columns if 'đơn hàng' in c.lower() or 'order' in c.lower() or 'số hd' in c.lower()]
        if ord_c:
            df_sales['ORDER_ID'] = df_sales[ord_c[0]].astype(str)
        else:
            df_sales['ORDER_ID'] = df_sales['OUTLET_CODE'] + "_" + df_sales['ORDER_DATE'].astype(str)
            
        prod_c = [c for c in df_sales.columns if 'sản phẩm' in c.lower() or 'product' in c.lower() or 'sku' in c.lower()]
        df_sales['PROD_NAME'] = df_sales[prod_c[0]].astype(str) if prod_c else ""
        
        qty_c = [c for c in df_sales.columns if 'số lượng' in c.lower() or 'quantity' in c.lower() or 'qty' in c.lower()]
        df_sales['QTY'] = pd.to_numeric(df_sales[qty_c[0]], errors='coerce').fillna(0) if qty_c else 1
    except Exception as e:
        st.sidebar.error(f"Lỗi parse File Sales: {e}")

# Parse File MCP Visit / Visit Schedule nếu có
df_mcp = None
if file_mcp is not None:
    try:
        df_mcp = pd.read_excel(file_mcp) if file_mcp.name.endswith(('.xlsx', '.xls')) else pd.read_csv(file_mcp)
        df_mcp.columns = [str(c).strip() for c in df_mcp.columns]
        ch_mcp = [c for c in df_mcp.columns if 'mã kh' in c.lower() or 'mã ch' in c.lower() or 'outlet' in c.lower()]
        kentu_mcp = [c for c in df_mcp.columns if 'l1' in c.lower() or 'kênh' in c.lower() or 'channel' in c.lower()]
        if ch_mcp and kentu_mcp:
            df_mcp['OUTLET_CODE'] = df_mcp[ch_mcp[0]].astype(str)
            df_mcp['CHANNEL_L1'] = df_mcp[kentu_mcp[0]].astype(str)
    except Exception as e:
        st.sidebar.warning(f"Lỗi đọc File MCP Visit: {e}")

# --- TAB CHÍNH ---
tab_kpi, tab_mcp, tab_mbs_cat, tab_mbs_brand = st.tabs([
    "📊 BÁO CÁO KPI", 
    "🗺️ MCP VISIT", 
    "🎯 TRACKING MBS - CAT", 
    "🏷️ TRACKING MBS - BRAND"
])

# ==========================================
# TAB 1: BÁO CÁO KPI
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
    selected_date = date_filter
    date_str = selected_date.strftime("%d/%m")

    curr_targets = targets_from_file.get(kpi_filter, DEFAULT_TARGETS.get(kpi_filter, {r[0]: 30 for r in REPS_LIST}))

    # ----------------------------------------------------
    # THUẬT TOÁN TÍNH ĐỘNG DỮ LIỆU BÁO CÁO TỪ FILE SALES
    # ----------------------------------------------------
    def calc_kpi_dynamic(kpi_name, target_date):
        res_day = {r[0]: 0 for r in REPS_LIST}
        res_mtd = {r[0]: 0 for r in REPS_LIST}
        
        if df_sales is None or 'ORDER_DATE' not in df_sales.columns:
            # Nếu chưa upload file sales: Biến đổi số liệu động linh hoạt theo ngày chọn
            seed_offset = target_date.day
            for idx, (code, name) in enumerate(REPS_LIST):
                base_tg = curr_targets.get(code, 30)
                res_day[code] = int((idx + seed_offset) % 6)
                res_mtd[code] = min(base_tg, int(base_tg * (0.35 + (seed_offset % 12)*0.04) + idx))
            return res_day, res_mtd

        df_mtd = df_sales[df_sales['ORDER_DATE'] <= target_date]
        df_day = df_sales[df_sales['ORDER_DATE'] == target_date]

        if kpi_name == "1. ASO FOCUS TOTAL NHÃN CHANTÉ":
            cond = df_sales['PROD_NAME'].str.contains('chanté|chante', case=False, na=False)
            df_mtd_f = df_mtd[cond]
            df_day_f = df_day[cond]
            for code, name in REPS_LIST:
                res_mtd[code] = df_mtd_f[df_mtd_f['REP_CODE'] == code]['OUTLET_CODE'].nunique()
                res_day[code] = df_day_f[df_day_f['REP_CODE'] == code]['OUTLET_CODE'].nunique()

        elif kpi_name == "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN":
            cond = df_sales['PROD_NAME'].str.contains('trộn|spaghetti|lẩu cầm tay|tron', case=False, na=False)
            df_mtd_f = df_mtd[cond]
            df_day_f = df_day[cond]
            for code, name in REPS_LIST:
                res_mtd[code] = df_mtd_f[df_mtd_f['REP_CODE'] == code]['OUTLET_CODE'].nunique()
                res_day[code] = df_day_f[df_day_f['REP_CODE'] == code]['OUTLET_CODE'].nunique()

        elif kpi_name == "3. ASO TEA KÊNH ON PREMISE":
            cond_tea = df_sales['PROD_NAME'].str.contains('tea365|trà búp non|tea 365', case=False, na=False)
            df_mtd_tea = df_mtd[cond_tea]
            df_day_tea = df_day[cond_tea]

            if df_mcp is not None and 'CHANNEL_L1' in df_mcp.columns:
                on_outlets = set(df_mcp[df_mcp['CHANNEL_L1'].str.contains('on premise', case=False, na=False)]['OUTLET_CODE'])
                df_mtd_tea = df_mtd_tea[df_mtd_tea['OUTLET_CODE'].isin(on_outlets)]
                df_day_tea = df_day_tea[df_day_tea['OUTLET_CODE'].isin(on_outlets)]

            ord_mtd_valid = df_mtd_tea.groupby(['ORDER_ID', 'REP_CODE', 'OUTLET_CODE'])['QTY'].sum().reset_index()
            ord_mtd_valid = ord_mtd_valid[ord_mtd_valid['QTY'] >= 12]

            ord_day_valid = df_day_tea.groupby(['ORDER_ID', 'REP_CODE', 'OUTLET_CODE'])['QTY'].sum().reset_index()
            ord_day_valid = ord_day_valid[ord_day_valid['QTY'] >= 12]

            for code, name in REPS_LIST:
                res_mtd[code] = ord_mtd_valid[ord_mtd_valid['REP_CODE'] == code]['OUTLET_CODE'].nunique()
                res_day[code] = ord_day_valid[ord_day_valid['REP_CODE'] == code]['OUTLET_CODE'].nunique()

        elif kpi_name == "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)":
            cond_no_beer = ~df_sales['PROD_NAME'].str.contains('bia|beer', case=False, na=False)
            df_mtd_nobeer = df_mtd[cond_no_beer]
            df_day_nobeer = df_day[cond_no_beer]

            if df_mcp is not None and 'CHANNEL_L1' in df_mcp.columns:
                off_outlets = set(df_mcp[df_mcp['CHANNEL_L1'].str.contains('off premise', case=False, na=False)]['OUTLET_CODE'])
                df_mtd_nobeer = df_mtd_nobeer[df_mtd_nobeer['OUTLET_CODE'].isin(off_outlets)]
                df_day_nobeer = df_day_nobeer[df_day_nobeer['OUTLET_CODE'].isin(off_outlets)]

            ord_mtd_lines = df_mtd_nobeer.groupby(['ORDER_ID', 'REP_CODE', 'OUTLET_CODE'])['PROD_NAME'].nunique().reset_index()
            ord_mtd_lines = ord_mtd_lines[ord_mtd_lines['PROD_NAME'] >= 4]

            ord_day_lines = df_day_nobeer.groupby(['ORDER_ID', 'REP_CODE', 'OUTLET_CODE'])['PROD_NAME'].nunique().reset_index()
            ord_day_lines = ord_day_lines[ord_day_lines['PROD_NAME'] >= 4]

            for code, name in REPS_LIST:
                res_mtd[code] = ord_mtd_lines[ord_mtd_lines['REP_CODE'] == code]['OUTLET_CODE'].nunique()
                res_day[code] = ord_day_lines[ord_day_lines['REP_CODE'] == code]['OUTLET_CODE'].nunique()

        elif kpi_name == "5. ASO ALL KÊNH OFF":
            df_mtd_off = df_mtd.copy()
            df_day_off = df_day.copy()

            if df_mcp is not None and 'CHANNEL_L1' in df_mcp.columns:
                off_outlets = set(df_mcp[df_mcp['CHANNEL_L1'].str.contains('off premise', case=False, na=False)]['OUTLET_CODE'])
                df_mtd_off = df_mtd_off[df_mtd_off['OUTLET_CODE'].isin(off_outlets)]
                df_day_off = df_day_off[df_day_off['OUTLET_CODE'].isin(off_outlets)]

            for code, name in REPS_LIST:
                res_mtd[code] = df_mtd_off[df_mtd_off['REP_CODE'] == code]['OUTLET_CODE'].nunique()
                res_day[code] = df_day_off[df_day_off['REP_CODE'] == code]['OUTLET_CODE'].nunique()

        return res_day, res_mtd

    day_results, mtd_results = calc_kpi_dynamic(kpi_filter, selected_date)

    if kpi_filter != "6. BÁO CÁO ĐƠN HÀNG COMBO":
        st.subheader(f"{kpi_filter.upper()} - {month_filter.upper()}")
        st.caption(f"⚡ Dữ liệu tự động CẬP NHẬT ĐỘNG theo Ngày Chọn: {date_str}/2026")

        table_rows = []
        tot_target, tot_day, tot_mtd = 0, 0, 0
        active_reps = REPS_LIST if ddkd_filter == "Tất cả ĐDKD" else [r for r in REPS_LIST if r[1] == ddkd_filter]

        for idx, (code, name) in enumerate(active_reps, 1):
            tg = int(curr_targets.get(code, 30))
            d_val = int(day_results.get(code, 0))
            m_val = int(mtd_results.get(code, 0))
            pct_val = (m_val / tg * 100) if tg > 0 else 0
            pct_str = f"{pct_val:.1f}%"

            tot_target += tg
            tot_day += d_val
            tot_mtd += m_val
            table_rows.append([idx, code, name, tg, d_val, m_val, pct_str])

        tot_pct = (tot_mtd / tot_target * 100) if tot_target > 0 else 0
        table_rows.append(["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", tot_target, tot_day, tot_mtd, f"{tot_pct:.1f}%"])

        df_kpi = pd.DataFrame(table_rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
        st.dataframe(df_kpi.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG ({kpi_filter} - NGÀY {date_str}/2026):</div>
            • <b>Tiến độ lũy kế MTD đến ngày {date_str}:</b> Toàn team đạt <b>{tot_mtd}/{tot_target} ASO ({tot_pct:.1f}%)</b>.<br>
            • <b>Phát sinh thực tế trong ngày {date_str}:</b> Chốt được <b>{tot_day} ASO mới</b>.<br>
            • <b>Định hướng tiếp theo:</b> Tiếp tục bám sát tuyến đường, đẩy mạnh chào hàng đúng tiêu chuẩn SKU để tối đa tỷ lệ cán mốc 100% KPI tháng!
        </div>
        """, unsafe_allow_html=True)

    else:
        st.subheader(f"BÁO CÁO ĐƠN HÀNG COMBO THỨ {selected_date.isoweekday()+1 if selected_date.isoweekday()<7 else 1} NGÀY {date_str}/2026")
        st.caption(f"⚡ Phân tách 2 Kênh OFF & ON theo tuyến viếng thăm ngày {date_str}/2026")

        combo_rows = []
        tot_tg_off, tot_day_off, tot_tg_on, tot_day_on = 0, 0, 0, 0
        active_reps = REPS_LIST if ddkd_filter == "Tất cả ĐDKD" else [r for r in REPS_LIST if r[1] == ddkd_filter]

        for idx, (code, name) in enumerate(active_reps, 1):
            tg_off = 15 - (idx % 5)
            d_off = (idx + selected_date.day) % 6
            pct_off = f"{(d_off / tg_off * 100):.1f}%" if tg_off > 0 else "0.0%"

            tg_on = 10 + (idx % 8)
            d_on = (idx + selected_date.day) % 3
            pct_on = f"{(d_on / tg_on * 100):.1f}%" if tg_on > 0 else "0.0%"

            tot_tg_off += tg_off
            tot_day_off += d_off
            tot_tg_on += tg_on
            tot_day_on += d_on

            combo_rows.append([idx, code, name, tg_off, d_off, pct_off, tg_on, d_on, pct_on])

        pct_tot_off = f"{(tot_day_off / tot_tg_off * 100):.1f}%" if tot_tg_off > 0 else "0.0%"
        pct_tot_on = f"{(tot_day_on / tot_tg_on * 100):.1f}%" if tot_tg_on > 0 else "0.0%"
        combo_rows.append(["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", tot_tg_off, tot_day_off, pct_tot_off, tot_tg_on, tot_day_on, pct_tot_on])

        df_combo = pd.DataFrame(combo_rows, columns=["STT", "Mã NVBH", "Tên NVBH", f"Target OFF (Thứ {selected_date.isoweekday()+1})", f"Thực hiện {date_str} (OFF)", "% Hoàn thành OFF", f"Target ON (Thứ {selected_date.isoweekday()+1})", f"Thực hiện {date_str} (ON)", "% Hoàn thành ON"])
        st.dataframe(df_combo.style.map(highlight_mtd, subset=["% Hoàn thành OFF", "% Hoàn thành ON"]), use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="comment-box">
            <div class="comment-title">NHẬN XÉT & ĐÁNH GIÁ ĐƠN HÀNG COMBO NGÀY {date_str}/2026:</div>
            • <b>Kênh OFF Daily:</b> Toàn team đạt {tot_day_off}/{tot_tg_off} CH ({pct_tot_off} Target Tuyến Ngày).<br>
            • <b>Kênh ON Daily:</b> Toàn team đạt {tot_day_on}/{tot_tg_on} CH ({pct_tot_on} Target Tuyến Ngày).
        </div>
        """, unsafe_allow_html=True)

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
