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
        <div class="header-subtitle">TRACKING KPI ĐDKD - TEAM SS TRƯƠNG THANH TÂN TOTAL</div>
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
            
            u_sales = st.file_uploader("📂 Tải lên File Bán Hàng (Data.xlsx)", type=["xlsx", "csv"], key="u_sales")
            if u_sales: 
                st.session_state['df_sales_file'] = u_sales
                st.success("Đã nạp file bán hàng thành công!")

# --- TÌM FILE BÁN HÀNG ---
def find_available_sales_file():
    if st.session_state['df_sales_file'] is not None:
        return st.session_state['df_sales_file']
    for f in os.listdir('.'):
        if any(kw in f.lower() for kw in ['ban_hang', 'sales', 'don_hang', 'rpt', 'chitietdonhang', 'data']):
            return f
    return None

file_kpi_target = "Target_KPI.xlsx" if os.path.exists("Target_KPI.xlsx") else (os.path.join("data", "Target_KPI.xlsx") if os.path.exists(os.path.join("data", "Target_KPI.xlsx")) else None)
file_sales = find_available_sales_file()
file_mcp = "Data_MCP.xlsx" if os.path.exists("Data_MCP.xlsx") else (os.path.join("data", "Data_MCP.xlsx") if os.path.exists(os.path.join("data", "Data_MCP.xlsx")) else None)
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
    date_filter = st.date_input("NGÀY", datetime.date(2026, 9, 16))
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

# --- LOAD & PROCESS DATA (TỰ ĐỘNG DÒ HEADER CHUẨN HOẶC DÒNG 3) ---
@st.cache_data
def load_and_process_data(rpt_path, mcp_path):
    is_ex = str(rpt_path).endswith(('.xlsx', '.xls')) or (hasattr(rpt_path, 'name') and rpt_path.name.endswith(('.xlsx', '.xls')))
    
    # Dò tìm dòng header chính xác cho file Data.xlsx của Masan
    raw_peek = pd.read_excel(rpt_path, header=None, nrows=10) if is_ex else pd.read_csv(rpt_path, header=None, nrows=10)
    real_header_row = 0
    for idx, row in raw_peek.iterrows():
        row_str = " ".join([str(val).lower() for val in row.values])
        if any(k in row_str for k in ['sản phẩm', 'product', 'sku', 'mã ch', 'ship-to npp']):
            real_header_row = idx
            break
            
    df = pd.read_excel(rpt_path, header=real_header_row) if is_ex else pd.read_csv(rpt_path, header=real_header_row)
    df.columns = [str(c).strip() for c in df.columns]
    
    is_mcp_ex = str(mcp_path).endswith(('.xlsx', '.xls')) or (hasattr(mcp_path, 'name') and mcp_path.name.endswith(('.xlsx', '.xls')))
    mcp = pd.read_excel(mcp_path) if is_mcp_ex else pd.read_csv(mcp_path)
    mcp.columns = [str(c).strip() for c in mcp.columns]

    # Lọc đơn đã hủy
    status_col = next((c for c in df.columns if 'tình trạng' in c.lower()), None)
    if status_col:
        df = df[~df[status_col].astype(str).str.contains('hủy|cancel', case=False, na=False)].copy()
    
    date_col = next((c for c in df.columns if 'ngày tạo đơn hàng' in c.lower() or 'ngay' in c.lower()), df.columns[13])
    df['Ngày tạo đơn hàng'] = pd.to_datetime(df[date_col], errors='coerce')
    df['date'] = df['Ngày tạo đơn hàng'].dt.date

    # Map kênh từ MCP
    mcp_col_code = next((c for c in mcp.columns if 'outlet_code' in c.lower() or 'mã ch' in c.lower() or 'mã kh' in c.lower()), mcp.columns[0])
    mcp_col_l1 = next((c for c in mcp.columns if c.lower() in ['l1', 'kênh', 'channel']), mcp.columns[1] if len(mcp.columns)>1 else mcp.columns[0])
    
    mcp_map = mcp[[mcp_col_code, mcp_col_l1]].drop_duplicates(subset=[mcp_col_code])
    mcp_map.columns = ['Outlet_code', 'L1']
    mcp_map['Outlet_code'] = mcp_map['Outlet_code'].astype(str).str.strip()
    
    ch_sales_col = next((c for c in df.columns if 'mã ch' in c.lower()), df.columns[16] if len(df.columns)>16 else df.columns[0])
    df['Mã CH'] = df[ch_sales_col].astype(str).str.strip()
    df = df.merge(mcp_map, left_on='Mã CH', right_on='Outlet_code', how='left')
    
    prod_col = next((c for c in df.columns if 'tên sản phẩm' in c.lower() or 'product' in c.lower()), df.columns[24] if len(df.columns)>24 else df.columns[0])
    df['Tên SP lower'] = df[prod_col].astype(str).str.lower()

    return df, mcp

df, mcp_df = None, None
if file_sales is not None:
    try:
        df, mcp_df = load_and_process_data(file_sales, file_mcp if file_mcp else file_sales)
    except Exception as e:
        st.error(f"⚠️ Lỗi đọc File Sales / MCP: {e}")

# --- GET TARGETS ---
def get_targets(kpi_path=file_kpi_target):
    if not kpi_path or not os.path.exists(kpi_path):
        return {}
    try:
        kpi_raw = pd.read_excel(kpi_path, header=None)
        kpi = kpi_raw.iloc[2:].copy()
        kpi.columns = [
            'Region', 'Month', 'Ship to', 'Distributor', 'SUP', 'SM pos',
            'SM code', 'SM name', 'Saleteam', 'KPI type', 'KPI Name',
            'Target', 'Thực hiện', '% actual', '% Contrib', 'Chưa ra HĐ'
        ][:len(kpi.columns)]
        kpi = kpi.dropna(subset=['SM code'])
        kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')

        targets = {}
        for _, r in kpi.iterrows():
            sm = str(r['SM code']).strip()
            ktype = str(r['KPI type']).strip()
            kname = str(r['KPI Name']).strip()
            tgt = r['Target']
            if pd.isna(tgt):
                continue
            if ktype == 'ASO_ALL':
                targets.setdefault(sm, {})['ASO_ALL'] = int(tgt)
            elif ktype == 'PC_BT':
                targets.setdefault(sm, {})['PC_BT'] = int(tgt)
            elif ktype == 'ASO_ON':
                targets.setdefault(sm, {})['ASO_ON'] = int(tgt)
            elif ktype == 'ASO_Focus' and 'xanh' in kname.lower():
                targets.setdefault(sm, {})['ASO_CHANTE'] = int(tgt)
        return targets
    except Exception:
        return {}

targets = get_targets()

# --- HÀM BUILD BÁO CÁO KPI ---
def build_report(df, report_date, targets, report_type):
    if df is None or len(df) == 0:
        return pd.DataFrame(), 0
    
    df_mtd = df[df['date'] >= datetime.date(report_date.year, report_date.month, 1)].copy()
    
    rep_code_col = next((c for c in df_mtd.columns if 'mã nvbh' in c.lower() or 'nvbh' in c.lower()), 'Mã NVBH')
    rep_name_col = next((c for c in df_mtd.columns if 'tên nvbh' in c.lower()), 'Tên NVBH')
    
    sm_names = df_mtd.groupby(rep_code_col)[rep_name_col].first().to_dict()
    all_sms = sorted(sm_names.keys())

    # 1. ASO ALL Kênh OFF
    if report_type == 'ASO_ALL':
        off = df_mtd[df_mtd['L1'] == 'Kênh Off Premise'].copy()
        mtd = off.groupby(rep_code_col)['Mã CH'].nunique()
        first_buy = off.groupby([rep_code_col, 'Mã CH'])['date'].min().reset_index()
        first_buy.columns = [rep_code_col, 'Mã CH', 'first_date']
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby(rep_code_col)['Mã CH'].nunique()
        team_tgt = 1200
        key = 'ASO_ALL'

    # 2. PC BT Kênh OFF ≥ 4 line
    elif report_type == 'PC_BT':
        sub_div_col = next((c for c in df_mtd.columns if 'sub division' in c.lower() or 'division' in c.lower()), 'Sub Division')
        order_id_col = next((c for c in df_mtd.columns if 'mã đơn hàng' in c.lower() or 'order' in c.lower()), 'Mã đơn hàng')
        prod_id_col = next((c for c in df_mtd.columns if 'mã sản phẩm' in c.lower() or 'sku' in c.lower()), 'Mã sản phẩm')

        off = df_mtd[
            (df_mtd['L1'] == 'Kênh Off Premise') &
            ~df_mtd[sub_div_col].astype(str).str.contains('Beer|Bia', case=False, na=False)
        ]
        lines = off.groupby([rep_code_col, order_id_col])[prod_id_col].nunique()
        mtd = lines[lines >= 4].reset_index().groupby(rep_code_col)[order_id_col].nunique()

        df_today = df[df['date'] == report_date]
        off_t = df_today[
            (df_today['L1'] == 'Kênh Off Premise') &
            ~df_today[sub_div_col].astype(str).str.contains('Beer|Bia', case=False, na=False)
        ]
        lines_t = off_t.groupby([rep_code_col, order_id_col])[prod_id_col].nunique()
        ngay = lines_t[lines_t >= 4].reset_index().groupby(rep_code_col)[order_id_col].nunique()

        team_tgt = 2667
        key = 'PC_BT'

    # 3. ASO Tea Kênh ON ≥ 12 chai
    elif report_type == 'ASO_TEA':
        on = df_mtd[df_mtd['L1'] == 'Kênh On Premise']
        tea = on[on['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)].copy()
        qty_col = next((c for c in tea.columns if 'tổng lẻ' in c.lower() or 'qty' in c.lower()), 'Tổng lẻ')
        tea['qty'] = pd.to_numeric(tea[qty_col], errors='coerce').fillna(0)
        ch = tea.groupby([rep_code_col, 'Mã CH'])['qty'].sum()
        mtd = ch[ch >= 12].reset_index().groupby(rep_code_col)['Mã CH'].nunique()

        df_today = df[df['date'] == report_date]
        on_t = df_today[df_today['L1'] == 'Kênh On Premise']
        tea_t = on_t[on_t['Tên SP lower'].str.contains('tea|trà|ô long|olong|búp non', na=False)]
        ngay = tea_t.groupby(rep_code_col)['Mã CH'].nunique()

        team_tgt = 450
        key = 'ASO_ON'

    # 4. ASO Omachi Trộn
    elif report_type == 'OMACHI':
        mask = (
            df_mtd['Tên SP lower'].str.contains('omachi', na=False) &
            df_mtd['Tên SP lower'].str.contains('trộn|tron|xào|xao', na=False)
        )
        mtd = df_mtd[mask].groupby(rep_code_col)['Mã CH'].nunique()

        omachi = df_mtd[mask].copy()
        first_buy = omachi.groupby([rep_code_col, 'Mã CH'])['date'].min().reset_index()
        first_buy.columns = [rep_code_col, 'Mã CH', 'first_date']
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby(rep_code_col)['Mã CH'].nunique()

        team_tgt = 754
        key = None

    # 5. ASO Total Chanté
    elif report_type == 'CHANTE':
        mask = df_mtd['Tên SP lower'].str.contains('chanté|chante', na=False)
        mtd = df_mtd[mask].groupby(rep_code_col)['Mã CH'].nunique()

        chante = df_mtd[mask].copy()
        first_buy = chante.groupby([rep_code_col, 'Mã CH'])['date'].min().reset_index()
        first_buy.columns = [rep_code_col, 'Mã CH', 'first_date']
        new_today = first_buy[first_buy['first_date'] == report_date]
        ngay = new_today.groupby(rep_code_col)['Mã CH'].nunique()

        team_tgt = 450
        key = 'ASO_CHANTE'

    else:
        return pd.DataFrame(), 0

    results = []
    for sm in all_sms:
        tgt = targets.get(sm, {}).get(key, team_tgt // 15) if key else (team_tgt // 15)
        m = int(mtd.get(sm, 0))
        n = int(ngay.get(sm, 0))
        pct = round(m / tgt * 100, 1) if tgt else 0
        results.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Chỉ tiêu': tgt,
            'Thực hiện (Ngày)': n,
            'MTD': m,
            '% MTD': f"{pct}%"
        })

    df_out = pd.DataFrame(results).sort_values('MTD', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))

    total_ngay = int(df_out['Thực hiện (Ngày)'].sum())
    total_mtd = int(df_out['MTD'].sum())
    total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0

    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Trương Thanh Tân Total',
        'Chỉ tiêu': team_tgt,
        'Thực hiện (Ngày)': total_ngay,
        'MTD': total_mtd,
        '% MTD': f"{total_pct}%"
    }])
    df_out = pd.concat([df_out, total_row], ignore_index=True)

    return df_out, team_tgt

# --- HÀM BUILD COMBO ---
def build_combo(df, report_date):
    if df is None or len(df) == 0:
        return pd.DataFrame()
    
    df_mtd = df[df['date'] >= datetime.date(report_date.year, report_date.month, 1)].copy()
    rep_code_col = next((c for c in df_mtd.columns if 'mã nvbh' in c.lower() or 'nvbh' in c.lower()), 'Mã NVBH')
    rep_name_col = next((c for c in df_mtd.columns if 'tên nvbh' in c.lower()), 'Tên NVBH')
    
    sm_names = df_mtd.groupby(rep_code_col)[rep_name_col].first().to_dict()
    all_sms = sorted(sm_names.keys())

    def is_combo(row):
        km = str(row.get('Hàng KM', 'N')).upper() == 'Y'
        giatri = float(pd.to_numeric(row.get('Giá trị hàng KM', 0), errors='coerce') or 0)
        ck = float(pd.to_numeric(row.get('Chiết khấu', 0), errors='coerce') or 0)
        channel = str(row.get('L1', ''))
        if channel == 'Kênh Off Premise':
            return km or giatri > 0 or ck >= 10000
        elif channel == 'Kênh On Premise':
            return km
        return False

    df_mtd = df_mtd.copy()
    df_mtd['is_c'] = df_mtd.apply(is_combo, axis=1)

    off_mtd = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh Off Premise')].groupby(rep_code_col)['Mã CH'].nunique()
    on_mtd  = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh On Premise')].groupby(rep_code_col)['Mã CH'].nunique()

    off_combo = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh Off Premise')]
    first_off = off_combo.groupby([rep_code_col, 'Mã CH'])['date'].min().reset_index()
    first_off.columns = [rep_code_col, 'Mã CH', 'first_date']
    new_off = first_off[first_off['first_date'] == report_date]
    off_ngay = new_off.groupby(rep_code_col)['Mã CH'].nunique()

    on_combo = df_mtd[(df_mtd['is_c']) & (df_mtd['L1'] == 'Kênh On Premise')]
    first_on = on_combo.groupby([rep_code_col, 'Mã CH'])['date'].min().reset_index()
    first_on.columns = [rep_code_col, 'Mã CH', 'first_date']
    new_on = first_on[first_on['first_date'] == report_date]
    on_ngay = new_on.groupby(rep_code_col)['Mã CH'].nunique()

    rows = []
    for sm in all_sms:
        rows.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Phát sinh Ngày (OFF)': int(off_ngay.get(sm, 0)),
            'MTD (OFF)': int(off_mtd.get(sm, 0)),
            'Phát sinh Ngày (ON)': int(on_ngay.get(sm, 0)),
            'MTD (ON)': int(on_mtd.get(sm, 0)),
        })

    df_out = pd.DataFrame(rows).sort_values('MTD (OFF)', ascending=False).reset_index(drop=True)
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))

    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'SS Trương Thanh Tân Total',
        'Phát sinh Ngày (OFF)': int(df_out['Phát sinh Ngày (OFF)'].sum()),
        'MTD (OFF)': int(df_out['MTD (OFF)'].sum()),
        'Phát sinh Ngày (ON)': int(df_out['Phát sinh Ngày (ON)'].sum()),
        'MTD (ON)': int(df_out['MTD (ON)'].sum()),
    }])
    df_out = pd.concat([df_out, total_row], ignore_index=True)
    return df_out

# --- MAP DOANH SỐ MTD CHO TAB MCP ---
if mcp_df is not None and df is not None:
    try:
        df_sales_mtd = df[df['date'] <= selected_date].copy()
        qty_col = next((c for c in df.columns if 'tổng chẵn' in c.lower() or 'sl' in c.lower()), 'Tổng chẵn')
        df_sales_mtd['QTY_NUM'] = pd.to_numeric(df_sales_mtd[qty_col], errors='coerce').fillna(1)
        sales_summary = df_sales_mtd.groupby('Mã CH')['QTY_NUM'].sum().to_dict()
        
        mcp_code_col = next((c for c in mcp_df.columns if 'outlet_code' in c.lower() or 'mã ch' in c.lower()), mcp_df.columns[0])
        mcp_df['OUTLET_STR'] = mcp_df[mcp_code_col].astype(str).str.strip()
        mcp_df['Doanh Số MTD'] = mcp_df['OUTLET_STR'].map(sales_summary).fillna(0)
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

def apply_raw_data_filters(df_input, tab_prefix):
    if df_input is None or len(df_input) == 0:
        return df_input
    df_filtered = df_input.copy()
    
    if tab_prefix == "mcp":
        col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([1.2, 1.2, 1.2, 1.4])
    else:
        col_filter1, col_filter2, col_filter3 = st.columns([1.5, 1.5, 2.0])
    
    rep_cols = [c for c in df_input.columns if any(k in str(c).lower() for k in ['mã nv', 'nvbh', 'sm', 'tên nv', 'sm name', 'nhân viên'])]
    ch_code_cols = [c for c in df_input.columns if any(k in str(c).lower() for k in ['mã kh', 'mã ch', 'outlet', 'customer', 'shipto'])]
    ch_name_cols = [c for c in df_input.columns if any(k in str(c).lower() for k in ['tên kh', 'tên ch', 'name', 'khách hàng'])]

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

    if tab_prefix == "mcp":
        with col_filter4:
            selected_day = st.selectbox(
                "📅 Lọc Theo Thứ",
                options=["Tất cả các thứ", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"],
                key=f"{tab_prefix}_day"
            )
            if selected_day != "Tất cả các thứ":
                day_mapping = {
                    "Thứ 2": [2, 25, "2", "25"],
                    "Thứ 3": [3, 36, "3", "36"],
                    "Thứ 4": [4, 47, "4", "47"],
                    "Thứ 5": [5, 25, "5", "25"],
                    "Thứ 6": [6, 36, "6", "36"],
                    "Thứ 7": [7, 47, "7", "47"],
                    "Chủ Nhật": []
                }
                target_vals = day_mapping.get(selected_day, [])
                match_mask = pd.Series(False, index=df_filtered.index)
                for col in df_filtered.columns:
                    col_check = df_filtered[col].isin(target_vals) | df_filtered[col].astype(str).str.strip().isin([str(v) for v in target_vals])
                    match_mask = match_mask | col_check
                df_filtered = df_filtered[match_mask]

    return df_filtered

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
    if kpi_filter == "1. ASO FOCUS TOTAL NHÃN CHANTÉ":
        rtype = 'CHANTE'
    elif kpi_filter == "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN":
        rtype = 'OMACHI'
    elif kpi_filter == "3. ASO TEA KÊNH ON PREMISE":
        rtype = 'ASO_TEA'
    elif kpi_filter == "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)":
        rtype = 'PC_BT'
    elif kpi_filter == "5. ASO ALL KÊNH OFF":
        rtype = 'ASO_ALL'
    else:
        rtype = 'COMBO'

    if rtype != 'COMBO':
        res_df, team_tgt = build_report(df, selected_date, targets, rtype)
        st.subheader(f"{kpi_filter.upper()} - {month_filter.upper()}")
        st.caption(f"⚡ Dữ liệu cập nhật động theo Ngày: {date_str}/2026")

        if not res_df.empty:
            if ddkd_filter != "Tất cả ĐDKD":
                res_df = res_df[(res_df['Tên NVBH'] == ddkd_filter) | (res_df['Mã NVBH'] == 'TỔNG CỘNG')]
            
            styled_df = res_df.style\
                .map(highlight_mtd, subset=["% MTD"] if "% MTD" in res_df.columns else [])\
                .set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#034EA2'), ('color', '#FF0000'), ('font-weight', '900'), ('font-size', '14px'), ('text-align', 'center')]},
                    {'selector': 'td', 'props': [('font-weight', '900'), ('color', '#0F172A'), ('text-align', 'center')]}
                ])
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ Không có dữ liệu thỏa điều kiện báo cáo.")
    else:
        combo_df = build_combo(df, selected_date)
        st.subheader(f"BÁO CÁO ĐƠN HÀNG COMBO - NGÀY {date_str}/2026")
        st.caption("⚡ Phân tách 2 Kênh OFF & ON")
        if not combo_df.empty:
            if ddkd_filter != "Tất cả ĐDKD":
                combo_df = combo_df[(combo_df['Tên NVBH'] == ddkd_filter) | (combo_df['Mã NVBH'] == 'TỔNG CỘNG')]
            st.dataframe(combo_df, use_container_width=True, hide_index=True)
        else:
            st.warning("⚠️ Không có dữ liệu Combo.")

# ==========================================
# TAB 2: MCP VISIT
# ==========================================
with tab_mcp:
    st.header("🗺️ MCP VISIT & MAPPING DOANH SỐ BÁN HÀNG")
    if mcp_df is not None:
        try:
            df_mcp_filtered = apply_raw_data_filters(mcp_df, "mcp")
            st.success(f"Hiển thị {len(df_mcp_filtered)} / {len(mcp_df)} dòng dữ liệu MCP Visit (Cột cuối: Doanh Số MTD)")
            st.dataframe(df_mcp_filtered, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file MCP Visit: {e}")
    else:
        st.warning("⚠️ Không tìm thấy file MCP Visit hệ thống.")

# ==========================================
# TAB 3: TRACKING MBS CAT
# ==========================================
with tab_mbs_cat:
    st.header("🎯 TRACKING MBS - THEO NGÀNH HÀNG (CATEGORY)")
    if file_mbs_cat and os.path.exists(file_mbs_cat):
        try:
            df_cat = pd.read_excel(file_mbs_cat)
            df_cat_filtered = apply_raw_data_filters(df_cat, "cat")
            st.dataframe(df_cat_filtered, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file Category: {e}")
    else:
        st.warning("⚠️ Không tìm thấy file Category hệ thống.")

# ==========================================
# TAB 4: TRACKING MBS BRAND
# ==========================================
with tab_mbs_brand:
    st.header("🏷️ TRACKING MBS - THEO NHÃN HÀNG (BRAND)")
    if file_mbs_brand and os.path.exists(file_mbs_brand):
        try:
            df_brand = pd.read_excel(file_mbs_brand)
            df_brand_filtered = apply_raw_data_filters(df_brand, "brand")
            st.dataframe(df_brand_filtered, use_container_width=True)
        except Exception as e:
            st.error(f"Lỗi đọc file Brand: {e}")
    else:
        st.warning("⚠️ Không tìm thấy file Brand hệ thống.")
