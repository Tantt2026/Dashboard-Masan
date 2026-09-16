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
    .header-banner {
        background-color: #FDE047;
        border: 2px solid #000;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
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
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
for key in ['df_sales_file', 'df_mcp_file', 'df_cat_file', 'df_brand_file', 'df_target_file']:
    if key not in st.session_state:
        st.session_state[key] = None

if 'admin_logged_in' not in st.session_state:
    st.session_state['admin_logged_in'] = False

# --- HEADER & ADMIN ---
head_col1, head_col2 = st.columns([3.8, 1.2])

with head_col1:
    st.markdown("""
    <div class="header-banner">
        <div class="header-title">SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</div>
        <div class="header-subtitle">TRACKING KPI ĐDKD</div>
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
    else:
        with st.popover("📁 UPLOAD FILE (ADMIN)", use_container_width=True):
            st.success("🟢 QUYỀN ADMIN")
            if st.button("🔒 Đăng Xuất Admin", key="btn_logout_top", use_container_width=True):
                st.session_state['admin_logged_in'] = False
                st.rerun()
            st.markdown("---")
            u_target = st.file_uploader("1. File Chỉ Tiêu (KPI.xlsx)", type=["xlsx", "csv"], key="u_target")
            u_sales = st.file_uploader("2. File Sales Chi Tiết", type=["xlsx", "csv"], key="u_sales")
            u_mcp = st.file_uploader("3. File MCP Visit", type=["xlsx", "csv"], key="u_mcp")
            u_cat = st.file_uploader("4. File MBS Category", type=["xlsx", "csv"], key="u_cat")
            u_brand = st.file_uploader("5. File MBS Brand", type=["xlsx", "csv"], key="u_brand")

            if u_target: st.session_state['df_target_file'] = u_target
            if u_sales: st.session_state['df_sales_file'] = u_sales
            if u_mcp: st.session_state['df_mcp_file'] = u_mcp
            if u_cat: st.session_state['df_cat_file'] = u_cat
            if u_brand: st.session_state['df_brand_file'] = u_brand

# --- LẤY FILE ---
file_kpi_target = st.session_state['df_target_file'] or ("Target_KPI.xlsx" if os.path.exists("Target_KPI.xlsx") else None)
file_sales = st.session_state['df_sales_file'] or ("Data_Sales.xlsx" if os.path.exists("Data_Sales.xlsx") else None)
file_mcp = st.session_state['df_mcp_file'] or ("Data_MCP.xlsx" if os.path.exists("Data_MCP.xlsx") else None)
file_mbs_cat = st.session_state['df_cat_file'] or ("Data_Cat.xlsx" if os.path.exists("Data_Cat.xlsx") else None)
file_mbs_brand = st.session_state['df_brand_file'] or ("Data_Brand.xlsx" if os.path.exists("Data_Brand.xlsx") else None)

# --- DANH SÁCH NHÂN VIÊN ---
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

# --- BỘ FILTER CHUNG ---
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

# --- ĐỌC FILE SALES ---
df_sales = None
if file_sales is not None:
    try:
        df_sales = pd.read_excel(file_sales) if str(file_sales).endswith(('.xlsx', '.xls')) or (hasattr(file_sales, 'name') and file_sales.name.endswith(('.xlsx', '.xls'))) else pd.read_csv(file_sales)
        df_sales.columns = [str(c).strip() for c in df_sales.columns]
    except Exception as e:
        st.error(f"Lỗi đọc file Sales: {e}")

# --- TABS ---
tab_kpi, tab_mcp, tab_mbs_cat, tab_mbs_brand = st.tabs([
    "📊 BÁO CÁO KPI", 
    "🗺️ MCP VISIT", 
    "🎯 TRACKING MBS - CAT", 
    "🏷️ TRACKING MBS - BRAND"
])

with tab_kpi:
    st.subheader(f"{kpi_filter} - {month_filter}")
    st.info("Đang ở phiên bản code gốc. Bro có thể đối chiếu lại logic tính toán.")

with tab_mcp:
    st.header("MCP VISIT")
    if file_mcp is not None:
        df_m = pd.read_excel(file_mcp) if hasattr(file_mcp, 'name') and file_mcp.name.endswith('.xlsx') else pd.read_csv(file_mcp)
        st.dataframe(df_m, use_container_width=True)

with tab_mbs_cat:
    st.header("TRACKING MBS - CATEGORY")
    if file_mbs_cat is not None:
        df_c = pd.read_excel(file_mbs_cat) if hasattr(file_mbs_cat, 'name') and file_mbs_cat.name.endswith('.xlsx') else pd.read_csv(file_mbs_cat)
        st.dataframe(df_c, use_container_width=True)

with tab_mbs_brand:
    st.header("TRACKING MBS - BRAND")
    if file_mbs_brand is not None:
        df_b = pd.read_excel(file_mbs_brand) if hasattr(file_mbs_brand, 'name') and file_mbs_brand.name.endswith('.xlsx') else pd.read_csv(file_mbs_brand)
        st.dataframe(df_b, use_container_width=True)
