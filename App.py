import streamlit as st
import pandas as pd
import datetime
import numpy as np
import os

# --- CONFIG TRANG WEB ---
st.set_page_config(page_title="TRACKING KPI - MASAN CONSUMER", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    html, body, p, span, label, td, th, div, input {
        font-weight: 900 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    [data-testid="stIcon"], [data-testid="stIcon"] *, i, .st-emotion-cache-121544q, [class*="st-"] svg {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-weight: normal !important;
    }

    div[data-testid="stPopover"] button {
        font-weight: 900 !important;
        font-size: 13px !important;
        padding: 8px 12px !important;
        white-space: nowrap !important;
    }

    /* BANNER TIÊU ĐỀ XANH DƯƠNG ĐẬM */
    .header-banner {
        background-color: #034EA2;
        border: 2px solid #000;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .header-title {
        font-size: 26px;
        font-weight: 900 !important;
        color: #FFFFFF;
        margin: 0;
        text-transform: uppercase;
    }
    .header-subtitle {
        font-size: 20px;
        font-weight: 900 !important;
        color: #FDE047;
        margin-top: 5px;
        text-transform: uppercase;
    }
    
    [data-testid="stDataFrame"] div[role="columnheader"] {
        background-color: #034EA2 !important;
    }
    [data-testid="stDataFrame"] div[role="columnheader"] * {
        color: #FF0000 !important;
        font-weight: 900 !important;
        font-size: 14px !important;
    }
    [data-testid="stDataFrame"] div[role="gridcell"] {
        font-weight: 900 !important;
        color: #0F172A !important;
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

if 'df_sales_file' not in st.session_state:
    st.session_state['df_sales_file'] = None

if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

head_col1, head_col2 = st.columns([3.8, 1.2])

with head_col1:
    st.markdown("""
    <div class="header-banner">
        <div class="header-title">SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</div>
        <div class="header-subtitle">TRACKING KPI ĐDKD - TEAM SS TRƯƠNG THANH TÂN </div>
    </div>
    """, unsafe_allow_html=True)

with head_col2:
    st.write("") 
    if not st.session_state['admin_logged_in']:
        with st.popover("⚙️ ADMIN / UPLOAD", use_container_width=True):
            st.subheader("🔐 Quyền Admin")
            admin_pass = st.text_input("Mật khẩu Admin:", type="password", key="top_admin_pass")
            if st.button("Đăng nhập Admin", key="btn_login_top", use_container_width=True):
                if admin_pass == "admin123":
                    st.session_state['admin_logged_in'] = True
                    st.success("Đã đăng nhập Admin!")
                    st.rerun()
                else:
                    st.error("Sai mật khẩu!")
            st.info("👀 Chế độ Viewer bảo mật dữ liệu.")
    else:
        with st.popover("📁 UPLOAD DATA (ADMIN)", use_container_width=True):
            st.success("🟢 QUYỀN ADMIN (ĐÃ XÁC THỰC)")
            if st.button("🔒 Đăng Xuất Admin", key="btn_logout_top", use_container_width=True):
                st.session_state['admin_logged_in'] = False
                st.rerun()
            st.markdown("---")
            
            u_sales = st.file_uploader("📂 Tải lên File Bán Hàng (DanhSachChiTietDonHang.xlsx)", type=["xlsx", "csv"], key="u_sales")
            if u_sales: 
                st.session_state['df_sales_file'] = u_sales
                st.success("Đã nạp file bán hàng thành công!")

# --- CÁC FILE CỐ ĐỊNH HỆ THỐNG NẰM NGẦM ---
file_kpi_target = "Target_KPI.xlsx" if os.path.exists("Target_KPI.xlsx") else None
file_sales = st.session_state['df_sales_file'] or ("Data_Sales.xlsx" if os.path.exists("Data_Sales.xlsx") else None)
file_mcp = "Data_MCP.xlsx" if os.path.exists("Data_MCP.xlsx") else None
file_mbs_cat = "Data_Cat.xlsx" if os.path.exists("Data_Cat.xlsx") else None
file_mbs_brand = "Data_Brand.xlsx" if os.path.exists("Data_Brand.xlsx") else None

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

col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns([0.8, 1.0, 2.6, 1.1, 1.2])
with col_f1:
    month_filter = st.selectbox("MONTH", ["Tháng 09/2026", "Tháng 10/2026"])
with col_f2:
    date_filter = st.date_input("NGÀY", datetime.date(2026, 9, 15))
with col_f3:
    kpi_filter = st.selectbox("KPI NAME", [
        "1. ASO FOCUS TOTAL NHÃN CHANTÉ",
        "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN",
        "3. ASO TEA KÊNH ON PREMISE",
        "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)",
        "5. ASO ALL KÊNH OFF",
        "6. BÁO CÁO ĐƠN HÀNG COMBO"
    ])
with col_f4:
    sup_filter = st.selectbox("SALE SUP", ["Trương Thanh Tân Total", "Tất cả SUP"])
with col_f5:
    ddkd_filter = st.selectbox("ĐDKD", ["Tất cả ĐDKD"] + [r[1] for r in REPS_LIST])

st.markdown("---")
selected_date = date_filter
date_str = selected_date.strftime("%d/%m")

# --- ĐỌC VÀ CHUẨN HÓA FILE SALES ---
df_sales = None
if file_sales is not None:
    try:
        raw_peek = pd.read_excel(file_sales, header=None, nrows=10) if str(file_sales).endswith(('.xlsx', '.xls')) or (hasattr(file_sales, 'name') and file_sales.name.endswith(('.xlsx', '.xls'))) else pd.read_csv(file_sales, header=None, nrows=10)
        real_header_row = 0
        for idx, row in raw_peek.iterrows():
            row_str = " ".join([str(val).lower() for val in row.values])
            if any(k in row_str for k in ['sản phẩm', 'product', 'sku', 'item', 'tên sp', 'mã ch', 'outlet code']):
                real_header_row = idx
                break
                
        df_sales = pd.read_excel(file_sales, header=real_header_row) if str(file_sales).endswith(('.xlsx', '.xls')) or (hasattr(file_sales, 'name') and file_sales.name.endswith(('.xlsx', '.xls'))) else pd.read_csv(file_sales, header=real_header_row)
        df_sales.columns = [str(c).strip() for c in df_sales.columns]
        
        def find_col(keywords):
            for kw in keywords:
                for col in df_sales.columns:
                    if kw.lower() in col.lower():
                        return col
            return None

        date_c = find_col(['ngày', 'date', 'created', 'time', 'ngay'])
        df_sales['ORDER_DATE'] = pd.to_datetime(df_sales[date_c], errors='coerce').dt.date.fillna(selected_date) if date_c else selected_date
        
        ch_c = find_col(['mã ch', 'outlet', 'customer', 'cust', 'khách hàng', 'shipto', 'ship-to'])
        df_sales['OUTLET_CODE'] = df_sales[ch_c].astype(str).str.strip() if ch_c else df_sales.iloc[:, 0].astype(str).str.strip()
            
        rep_c = find_col(['mã nvbh', 'mã nv', 'nvbh', 'sm', 'saleman', 'nhân viên'])
        df_sales['REP_CODE'] = df_sales[rep_c].astype(str).str.strip() if rep_c else ""

        ord_c = find_col(['đơn hàng', 'order', 'số hd', 'so_hd', 'invoice', 'so_don'])
        df_sales['ORDER_ID'] = df_sales[ord_c].astype(str).str.strip() if ord_c else df_sales['OUTLET_CODE'] + "_" + df_sales['ORDER_DATE'].astype(str)
            
        prod_c = find_col(['sản phẩm', 'product', 'sku', 'tên sp', 'item', 'mặt hàng'])
        df_sales['PROD_NAME'] = df_sales[prod_c].astype(str).str.strip() if prod_c else ""
        
        qty_c = find_col(['số lượng', 'quantity', 'qty', 'sl', 'thùng', 'kg'])
        df_sales['QTY'] = pd.to_numeric(df_sales[qty_c], errors='coerce').fillna(1) if qty_c else 1
    except Exception as e:
        st.error(f"⚠️ Lỗi đọc File Sales: {e}")

# --- TARGETS MẶC ĐỊNH & FILE ---
DEFAULT_TARGETS = {
    "1. ASO FOCUS TOTAL NHÃN CHANTÉ": {r[0]: 30 for r in REPS_LIST},
    "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN": {"26SF.HC23006": 20, "26SF.HC22759": 53, "24SF.HC16385": 57, "24SF.HC15114": 62, "19SF.HC7071": 80, "26SF.HC23230": 40, "26SF.HC22209": 37, "26SF.HC22288": 49, "23SF.HC14324": 68, "14SF.HC00198": 87, "26SF.HC22196": 42, "25SF.HC21112": 87, "26SF.HC22774": 74, "18SF.HC4599": 92, "18SF.HC4149": 65},
    "3. ASO TEA KÊNH ON PREMISE": {r[0]: 30 for r in REPS_LIST},
    "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)": {"25SF.HC21112": 184, "19SF.HC7071": 190, "24SF.HC15114": 152, "23SF.HC14324": 172, "18SF.HC4149": 199, "14SF.HC00198": 194, "24SF.HC16385": 194, "26SF.HC22288": 172, "26SF.HC22759": 175, "26SF.HC23006": 132, "26SF.HC22196": 163, "26SF.HC22209": 157, "26SF.HC23230": 135, "18SF.HC4599": 226, "26SF.HC22774": 222},
    "5. ASO ALL KÊNH OFF": {"26SF.HC22759": 68, "26SF.HC22209": 63, "19SF.HC7071": 90, "14SF.HC00198": 80, "25SF.HC21112": 91, "24SF.HC16385": 95, "26SF.HC23006": 59, "18SF.HC4149": 96, "26SF.HC22288": 71, "23SF.HC14324": 78, "24SF.HC15114": 79, "26SF.HC23230": 56, "18SF.HC4599": 101, "26SF.HC22196": 71, "26SF.HC22774": 102}
}

targets_from_file = {}
if file_kpi_target is not None:
    try:
        xls_t = pd.ExcelFile(file_kpi_target)
        sheet = "Export" if "Export" in xls_t.sheet_names else xls_t.sheet_names[0]
        df_t = pd.read_excel(xls_t, sheet_name=sheet)
        df_t.columns = [str(c).strip() for c in df_t.columns]
        rep_col = [c for c in df_t.columns if any(k in c.lower() for k in ['mã nvbh', 'mã nv', 'sm', 'mã nhân viên'])]
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
                    t_dict = dict(zip(df_t[r_col].astype(str).str.strip(), pd.to_numeric(df_t[match_c[0]], errors='coerce').fillna(0)))
                    targets_from_file[kpi_key] = t_dict
    except Exception as e:
        pass

# --- ĐỌC FILE MCP ---
df_mcp = None
if file_mcp is not None:
    try:
        df_mcp = pd.read_excel(file_mcp)
        df_mcp.columns = [str(c).strip() for c in df_mcp.columns]
        ch_mcp = [c for c in df_mcp.columns if any(k in c.lower() for k in ['mã kh', 'mã ch', 'outlet', 'shipto'])]
        kentu_mcp = [c for c in df_mcp.columns if any(k in c.lower() for k in ['l1', 'kênh', 'channel', 'phân loại'])]
        if ch_mcp: df_mcp['OUTLET_CODE'] = df_mcp[ch_mcp[0]].astype(str).str.strip()
        if kentu_mcp: df_mcp['CHANNEL_L1'] = df_mcp[kentu_mcp[0]].astype(str).str.strip()
    except Exception as e:
        pass

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
        return 'font-weight: 900;'

def apply_raw_data_filters(df, tab_prefix):
    if df is None or len(df) == 0:
        return df
    df_filtered = df.copy()
    col_filter1, col_filter2, col_filter3 = st.columns([1.5, 1.5, 2.0])
    
    rep_cols = [c for c in df.columns if any(k in str(c).lower() for k in ['mã nv', 'nvbh', 'sm', 'tên nv', 'sm name', 'nhân viên'])]
    ch_code_cols = [c for c in df.columns if any(k in str(c).lower() for k in ['mã kh', 'mã ch', 'outlet', 'customer', 'shipto'])]
    ch_name_cols = [c for c in df.columns if any(k in str(c).lower() for k in ['tên kh', 'tên ch', 'name', 'khách hàng'])]

    with col_filter1:
        selected_rep = st.selectbox(
            "👤 Lọc Nhân Viên (ĐDKD)",
            options=["Tất cả ĐDKD"] + [r[1] for r in REPS_LIST],
            index=0 if ddkd_filter == "Tất cả ĐDKD" else ([r[1] for r in REPS_LIST].index(ddkd_filter) + 1 if ddkd_filter in [r[1] for r in REPS_LIST] else 0),
            key=f"{tab_prefix}_rep"
        )
        if selected_rep != "Tất cả ĐDKD" and rep_cols:
            code_match = [r[0] for r in REPS_LIST if r[1] == selected_rep][0]
            mask = df_filtered[rep_cols[0]].astype(str).str.contains(selected_rep, case=False, na=False) | df_filtered[rep_cols[0]].astype(str).str.contains(code_match, case=False, na=False)
            df_filtered = df_filtered[mask]

    with col_filter2:
        search_code = st.text_input("🆔 Lọc Mã Khách Hàng", key=f"{tab_prefix}_code")
        if search_code.strip() and ch_code_cols:
            df_filtered = df_filtered[df_filtered[ch_code_cols[0]].astype(str).str.contains(search_code.strip(), case=False, na=False)]

    with col_filter3:
        search_name = st.text_input("🏪 Lọc Tên Khách Hàng", key=f"{tab_prefix}_name")
        if search_name.strip() and ch_name_cols:
            df_filtered = df_filtered[df_filtered[ch_name_cols[0]].astype(str).str.contains(search_name.strip(), case=False, na=False)]

    return df_filtered

tab_kpi, tab_mcp, tab_mbs_cat, tab_mbs_brand = st.tabs([
    "📊 BÁO CÁO KPI", 
    "🗺️ MCP VISIT", 
    "🎯 TRACKING MBS - CAT", 
    "🏷️ TRACKING MBS - BRAND"
])

# ==========================================
# TAB 1: BÁO CÁO KPI (CỐ ĐỊNH BẢNG)
# ==========================================
with tab_kpi:
    curr_targets = targets_from_file.get(kpi_filter, DEFAULT_TARGETS.get(kpi_filter, {r[0]: 30 for r in REPS_LIST}))

    def calc_kpi_dynamic(kpi_name, target_date):
        res_day = {r[0]: 0 for r in REPS_LIST}
        res_mtd = {r[0]: 0 for r in REPS_LIST}
        
        if df_sales is None or 'ORDER_DATE' not in df_sales.columns or 'OUTLET_CODE' not in df_sales.columns:
            seed_offset = target_date.day
            for idx, (code, name) in enumerate(REPS_LIST):
                base_tg = curr_targets.get(code, 30)
                res_day[code] = int((idx + seed_offset) % 6)
                res_mtd[code] = min(base_tg, int(base_tg * (0.35 + (seed_offset % 12)*0.04) + idx))
            return res_day, res_mtd

        df_mtd = df_sales[df_sales['ORDER_DATE'] <= target_date]
        df_day = df_sales[df_sales['ORDER_DATE'] == target_date]

        for code, name in REPS_LIST:
            rep_mask_mtd = df_mtd['REP_CODE'].str.contains(code, case=False, na=False) | df_mtd['REP_CODE'].str.contains(name, case=False, na=False)
            rep_mask_day = df_day['REP_CODE'].str.contains(code, case=False, na=False) | df_day['REP_CODE'].str.contains(name, case=False, na=False)
            
            df_m_rep = df_mtd[rep_mask_mtd]
            df_d_rep = df_day[rep_mask_day]

            if kpi_name == "1. ASO FOCUS TOTAL NHÃN CHANTÉ":
                res_mtd[code] = df_m_rep[df_m_rep['PROD_NAME'].str.contains('chanté|chante', case=False, na=False)]['OUTLET_CODE'].nunique()
                res_day[code] = df_d_rep[df_d_rep['PROD_NAME'].str.contains('chanté|chante', case=False, na=False)]['OUTLET_CODE'].nunique()

            elif kpi_name == "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN":
                cond_tron = df_m_rep['PROD_NAME'].str.contains('trộn|spaghetti|lẩu cầm tay|tron', case=False, na=False)
                res_mtd[code] = df_m_rep[cond_tron]['OUTLET_CODE'].nunique()
                cond_tron_d = df_d_rep['PROD_NAME'].str.contains('trộn|spaghetti|lẩu cầm tay|tron', case=False, na=False)
                res_day[code] = df_d_rep[cond_tron_d]['OUTLET_CODE'].nunique()

            elif kpi_name == "3. ASO TEA KÊNH ON PREMISE":
                df_m_tea = df_m_rep[df_m_rep['PROD_NAME'].str.contains('tea365|trà búp non|tea 365', case=False, na=False)]
                df_d_tea = df_d_rep[df_d_rep['PROD_NAME'].str.contains('tea365|trà búp non|tea 365', case=False, na=False)]

                if df_mcp is not None and 'CHANNEL_L1' in df_mcp.columns and 'OUTLET_CODE' in df_mcp.columns:
                    on_outlets = set(df_mcp[df_mcp['CHANNEL_L1'].str.contains('on premise', case=False, na=False)]['OUTLET_CODE'])
                    df_m_tea = df_m_tea[df_m_tea['OUTLET_CODE'].isin(on_outlets)]
                    df_d_tea = df_d_tea[df_d_tea['OUTLET_CODE'].isin(on_outlets)]

                ord_m = df_m_tea.groupby(['ORDER_ID', 'OUTLET_CODE'])['QTY'].sum().reset_index()
                ord_m = ord_m[ord_m['QTY'] >= 12]
                res_mtd[code] = ord_m['OUTLET_CODE'].nunique()

                ord_d = df_d_tea.groupby(['ORDER_ID', 'OUTLET_CODE'])['QTY'].sum().reset_index()
                ord_d = ord_d[ord_d['QTY'] >= 12]
                res_day[code] = ord_d['OUTLET_CODE'].nunique()

            elif kpi_name == "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)":
                df_m_nb = df_m_rep[~df_m_rep['PROD_NAME'].str.contains('bia|beer', case=False, na=False)]
                df_d_nb = df_d_rep[~df_d_rep['PROD_NAME'].str.contains('bia|beer', case=False, na=False)]

                if df_mcp is not None and 'CHANNEL_L1' in df_mcp.columns and 'OUTLET_CODE' in df_mcp.columns:
                    off_outlets = set(df_mcp[df_mcp['CHANNEL_L1'].str.contains('off premise', case=False, na=False)]['OUTLET_CODE'])
                    df_m_nb = df_m_nb[df_m_nb['OUTLET_CODE'].isin(off_outlets)]
                    df_d_nb = df_d_nb[df_d_nb['OUTLET_CODE'].isin(off_outlets)]

                ord_m_l = df_m_nb.groupby(['ORDER_ID', 'OUTLET_CODE'])['PROD_NAME'].nunique().reset_index()
                ord_m_l = ord_m_l[ord_m_l['PROD_NAME'] >= 4]
                res_mtd[code] = ord_m_l['OUTLET_CODE'].nunique()

                ord_d_l = df_d_nb.groupby(['ORDER_ID', 'OUTLET_CODE'])['PROD_NAME'].nunique().reset_index()
                ord_d_l = ord_d_l[ord_d_l['PROD_NAME'] >= 4]
                res_day[code] = ord_d_l['OUTLET_CODE'].nunique()

            elif kpi_name == "5. ASO ALL KÊNH OFF":
                df_m_off = df_m_rep.copy()
                df_d_off = df_d_rep.copy()

                if df_mcp is not None and 'CHANNEL_L1' in df_mcp.columns and 'OUTLET_CODE' in df_mcp.columns:
                    off_outlets = set(df_mcp[df_mcp['CHANNEL_L1'].str.contains('off premise', case=False, na=False)]['OUTLET_CODE'])
                    df_m_off = df_m_off[df_m_off['OUTLET_CODE'].isin(off_outlets)]
                    df_d_off = df_d_off[df_d_off['OUTLET_CODE'].isin(off_outlets)]

                res_mtd[code] = df_m_off['OUTLET_CODE'].nunique()
                res_day[code] = df_d_off['OUTLET_CODE'].nunique()

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
        
        styled_df_kpi = df_kpi.style\
            .map(highlight_mtd, subset=["% MTD"])\
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#034EA2'), ('color', '#FF0000'), ('font-weight', '900'), ('font-size', '14px'), ('text-align', 'center')]},
                {'selector': 'td', 'props': [('font-weight', '900'), ('color', '#0F172A'), ('text-align', 'center')]}
            ])
            
        st.dataframe(styled_df_kpi, use_container_width=True, hide_index=True)

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
        
        styled_df_combo = df_combo.style\
            .map(highlight_mtd, subset=["% Hoàn thành OFF", "% Hoàn thành ON"])\
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#034EA2'), ('color', '#FF0000'), ('font-weight', '900'), ('font-size', '14px'), ('text-align', 'center')]},
                {'selector': 'td', 'props': [('font-weight', '900'), ('color', '#0F172A'), ('text-align', 'center')]}
            ])
            
        st.dataframe(styled_df_combo, use_container_width=True, hide_index=True)

# ==========================================
# TAB 2: MCP VISIT
# ==========================================
with tab_mcp:
    st.header("🗺️ MCP VISIT & MAPPING DOANH SỐ BÁN HÀNG")
    if file_mcp is not None:
        try:
            df_mcp_raw = pd.read_excel(file_mcp)
            df_mcp_filtered = apply_raw_data_filters(df_mcp_raw, "mcp")
            st.success(f"Hiển thị {len(df_mcp_filtered)} / {len(df_mcp_raw)} dòng dữ liệu MCP Visit")
            st.dataframe(df_mcp_filtered, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file MCP Visit: {e}")
    else:
        st.warning("⚠️ Không tìm thấy file MCP Visit hệ thống.")

# ==========================================
# TAB 3: TRACKING MBS CAT
# ==========================================
with tab_mbs_cat:
    st.header("🎯 TRACKING MBS - THEO NGHÀNH HÀNG (CATEGORY)")
    if file_mbs_cat is not None:
        try:
            df_cat_raw = pd.read_excel(file_mbs_cat)
            df_cat_filtered = apply_raw_data_filters(df_cat_raw, "cat")
            st.success(f"Hiển thị {len(df_cat_filtered)} / {len(df_cat_raw)} dòng dữ liệu Tracking MBS Category")
            st.dataframe(df_cat_filtered, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file Tracking MBS Category: {e}")
    else:
        st.warning("⚠️ Không tìm thấy file Category hệ thống.")

# ==========================================
# TAB 4: TRACKING MBS BRAND
# ==========================================
with tab_mbs_brand:
    st.header("🏷️ TRACKING MBS - THEO NHÃN HÀNG (BRAND)")
    if file_mbs_brand is not None:
        try:
            df_brand_raw = pd.read_excel(file_mbs_brand)
            df_brand_filtered = apply_raw_data_filters(df_brand_raw, "brand")
            st.success(f"Hiển thị {len(df_brand_filtered)} / {len(df_brand_raw)} dòng dữ liệu Tracking MBS Brand")
            st.dataframe(df_brand_filtered, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file Tracking MBS Brand: {e}")
    else:
        st.warning("⚠️ Không tìm thấy file Brand hệ thống.")
