from datetime import date, timedelta
import datetime as dt
import os
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TRACKING KPI ĐDKD - SS Trương Thanh Tân",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ====================== LOGO ======================
logo_svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 158.15 61.91" width="110" height="42">
<title>Masan Group logo</title>
<path d="M490.29,502.16s17.83-12.81,45.76-12.93c25.9-.11,30.18,8.14,38,10.79,0,0-3.8,5.82-5.78,9.63s-13.32,17.93-26.5,22.21c0,0,18.71-15.72,21.55-27.57,0,0-26.87-20.43-73.26-1.92" transform="translate(-432.92 -481.05)" style="fill:#f36f21"/>
<path d="M521.55,489.11c42-10.64,59.59,9.56,59.59,9.56A60.39,60.39,0,0,1,561,521.3c11.28-1.28,21.79-13,24-16.69s6.16-9.17,6.16-9.17c-7.12-3.22-13.13-12-35.93-14.22-16.3-1.59-33.6,7.88-33.6,7.88" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M454.12,528V512.92a58.92,58.92,0,0,1-.15-6.31l-.06,0-7.1,21.11h-3.41l-7.25-21h-.09c0,2.33.1,5.52.09,6.28v15h-3.24V502.39h4.8L445.1,524h.07l7.17-21.31h5V528Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M465.15,515c.21-1.42.7-3.56,4.21-3.58,2.94,0,4.35,1,4.37,3s-.87,2.12-1.62,2.19l-5.11.65c-5.13.67-5.58,4.26-5.57,5.81,0,3.16,2.42,5.3,5.8,5.29a8.32,8.32,0,0,0,6.64-3c.12,1.42.55,2.82,3.3,2.81a6.24,6.24,0,0,0,1.69-.36v-2.26a4.84,4.84,0,0,1-1,.14c-.63,0-1-.3-1-1.09l-.05-10.6c0-4.73-5.37-5.13-6.85-5.13-4.54,0-7.47,1.76-7.6,6.17Zm8.42,6.37c0,2.48-2.85,4.35-5.74,4.36-2.35,0-3.38-1.17-3.39-3.19,0-2.32,2.42-2.8,4-3,3.86-.52,4.64-.78,5.15-1.18Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M492.47,514.47c0-1.17-.47-3.12-4.44-3.1-1,0-3.7.34-3.7,2.64,0,1.53,1,1.88,3.4,2.46l3.14.77c3.89.94,5.27,2.35,5.27,4.87,0,3.83-3.15,6.14-7.37,6.16-7.39,0-7.94-4.21-8-6.44h3c.11,1.45.55,3.78,5,3.75,2.24,0,4.27-.89,4.26-3,0-1.47-1-2-3.72-2.63l-3.65-.88c-2.59-.62-4.31-1.91-4.34-4.46,0-4.09,3.39-6,7.05-6,6.66,0,7.17,4.87,7.17,5.78Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M502.6,514.75c.2-1.42.68-3.58,4.2-3.6,2.91,0,4.33,1.06,4.33,3s-.86,2.13-1.61,2.18l-5.1.66c-5.11.65-5.57,4.27-5.56,5.79,0,3.19,2.41,5.31,5.79,5.31a8.34,8.34,0,0,0,6.63-3c.11,1.41.53,2.83,3.28,2.8a5.87,5.87,0,0,0,1.68-.35l0-2.26a6.5,6.5,0,0,1-1,.15c-.62,0-1-.32-1-1.1l0-10.61c0-4.72-5.35-5.11-6.83-5.11-4.53,0-7.44,1.76-7.56,6.16Zm8.36,6.49c0,2.47-2.82,4.36-5.74,4.37-2.35,0-3.37-1.18-3.39-3.18,0-2.34,2.44-2.8,4-3,3.87-.51,4.65-.8,5.14-1.2Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M534.55,527.71h-3v-11.5c-.13-3.2-1.07-4.83-4.13-4.81-1.77,0-4.88,1.15-4.7,6.15v10.16h-3.24l-.07-18.56h2.72l0,2.66h.07a6.85,6.85,0,0,1,5.67-3.19c2.91,0,6.58,1.15,6.6,6.45Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M468,533.85a1.19,1.19,0,0,1,.07.34.6.6,0,0,1-.19.46.81.81,0,0,1-.51.21l-.54-.18q-.45-.15-.75-.23a2.37,2.37,0,0,0-.59-.08,2.27,2.27,0,0,0-1.47.49,3.1,3.1,0,0,0-.92,1.27,4.89,4.89,0,0,0-.35,1.64,5.25,5.25,0,0,0,.56,2.41,2.27,2.27,0,0,0,1.91,1.26.77.77,0,0,1,.27,0l.43-.06.37-.1.37-.15L467,541a1,1,0,0,1,.4-.11.54.54,0,0,1,.42.19.69.69,0,0,1,.17.48,1,1,0,0,1-.82,1,5.35,5.35,0,0,1-1.69.27,4.1,4.1,0,0,1-2.28-.63,4.15,4.15,0,0,1-1.5-1.71,5.52,5.52,0,0,1-.55-2.35,7.3,7.3,0,0,1,.25-1.93,5,5,0,0,1,.76-1.63,3.74,3.74,0,0,1,1.34-1.14,4.33,4.33,0,0,1,1.91-.45,4.73,4.73,0,0,1,1.68.27,1.72,1.72,0,0,1,.91.62" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M470.75,537.9a4.78,4.78,0,0,0,.63,2.45,2.13,2.13,0,0,0,2,1.1,2.3,2.3,0,0,0,1.48-.48,2.78,2.78,0,0,0,.88-1.28,5.69,5.69,0,0,0,.31-1.78,5.11,5.11,0,0,0-.3-1.78,2.94,2.94,0,0,0-.89-1.29,2.21,2.21,0,0,0-1.44-.48,2.3,2.3,0,0,0-1.44.46,2.82,2.82,0,0,0-.91,1.27,5.12,5.12,0,0,0-.31,1.82m-1.59,0a5.74,5.74,0,0,1,.54-2.53,4.26,4.26,0,0,1,1.51-1.76,4,4,0,0,1,4.42.06,4.39,4.39,0,0,1,1.47,1.8,5.8,5.8,0,0,1,.51,2.43,5.89,5.89,0,0,1-.51,2.46,4.25,4.25,0,0,1-1.47,1.79,4.11,4.11,0,0,1-4.49,0,4.31,4.31,0,0,1-1.48-1.8,5.85,5.85,0,0,1-.51-2.44" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M479.44,534.07a.79.79,0,0,1,.21-.58.7.7,0,0,1,.52-.21.73.73,0,0,1,.53.21.78.78,0,0,1,.22.59v.14l0,0a3,3,0,0,1,1.13-.91,3.31,3.31,0,0,1,1.43-.32,3.46,3.46,0,0,1,1.63.4,3,3,0,0,1,1.21,1.21,4,4,0,0,1,.46,2V542a.68.68,0,0,1-.22.54.77.77,0,0,1-.53.19.73.73,0,0,1-.51-.19.69.69,0,0,1-.21-.53v-5.36a2.16,2.16,0,0,0-.65-1.67,2.21,2.21,0,0,0-1.55-.6,2.32,2.32,0,0,0-1.09.26,2,2,0,0,0-.82.79,2.41,2.41,0,0,0-.31,1.25v5.05a.81.81,0,0,1-.2.59.68.68,0,0,1-.51.21.74.74,0,0,1-.54-.22.77.77,0,0,1-.23-.58Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M488.69,541.75a1.05,1.05,0,0,1-.44-.77.7.7,0,0,1,.2-.49.64.64,0,0,1,.49-.21,1,1,0,0,1,.46.13,6.25,6.25,0,0,1,.57.37,3.06,3.06,0,0,0,.49.31,3,3,0,0,0,1.34.36,2.88,2.88,0,0,0,1.37-.32,1.06,1.06,0,0,0,.6-1A1.24,1.24,0,0,0,493,539a9.34,9.34,0,0,0-1.39-.65q-1-.4-1.55-.68a3.05,3.05,0,0,1-1-.79,1.94,1.94,0,0,1-.42-1.28,2.36,2.36,0,0,1,.39-1.31,2.79,2.79,0,0,1,1.11-1,4,4,0,0,1,1.64-.4,5,5,0,0,1,1.71.3,3.57,3.57,0,0,1,1.22.66,1.1,1.1,0,0,1,.38.74.65.65,0,0,1-.21.47.78.78,0,0,1-.5.23,4.06,4.06,0,0,1-.89-.41c-.39-.22-.67-.38-.86-.46a1.78,1.78,0,0,0-.69-.15,2,2,0,0,0-1.28.35,1.16,1.16,0,0,0-.46.86,1.34,1.34,0,0,0,.42.75,2.92,2.92,0,0,0,.78.52q.44.2,1.07.41c.42.14.71.25.87.32a3.77,3.77,0,0,1,1.54,1,2.2,2.2,0,0,1,.47,1.42,2.72,2.72,0,0,1-.42,1.37,2.86,2.86,0,0,1-1.19,1,4.49,4.49,0,0,1-2,.41,4.67,4.67,0,0,1-3.14-1.06" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M496.81,533.76a.74.74,0,0,1,.21-.56.71.71,0,0,1,.52-.21.74.74,0,0,1,.53.2.73.73,0,0,1,.22.56V539a2.75,2.75,0,0,0,.58,1.85,2.16,2.16,0,0,0,1.74.69q2.38,0,2.38-2.53v-5.22a.74.74,0,0,1,.21-.56.71.71,0,0,1,.51-.21.74.74,0,0,1,.53.2.73.73,0,0,1,.22.56v5.3a4.35,4.35,0,0,1-.4,1.86,3.14,3.14,0,0,1-1.27,1.38,4.23,4.23,0,0,1-2.22.53,4,4,0,0,1-2.11-.51,3.14,3.14,0,0,1-1.25-1.37,4.36,4.36,0,0,1-.4-1.88Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M506.53,533.81a.7.7,0,0,1,.22-.53.76.76,0,0,1,.54-.21.68.68,0,0,1,.51.2.84.84,0,0,1,.2.61v.3h.94a2.69,2.69,0,0,1,2.29-1.15,2.75,2.75,0,0,1,2.4,1.62,3.7,3.7,0,0,1,1.29-1.26,3.26,3.26,0,0,1,1.53-.36,3,3,0,0,1,1.52.44,3,3,0,0,1,1.1,1.21,3.92,3.92,0,0,1,.41,1.84v5.58a.74.74,0,0,1-.22.57.74.74,0,0,1-.53.21.7.7,0,0,1-.5-.22.76.76,0,0,1-.22-.56v-5.54a2.57,2.57,0,0,0-.27-1.21,1.78,1.78,0,0,0-.72-.76,2.08,2.08,0,0,0-1-.25,2.2,2.2,0,0,0-1.51.53,2.14,2.14,0,0,0-.6,1.69v5.5a.62.62,0,0,1-.22.51.8.8,0,0,1-.53.18.75.75,0,0,1-.5-.18.63.63,0,0,1-.22-.5v-5.34a2.48,2.48,0,0,0-.63-1.87,2.18,2.18,0,0,0-1.57-.6,2.85,2.85,0,0,0-1.12.26,1.84,1.84,0,0,0-.8.74,2.45,2.45,0,0,0-.3,1.28v5.57a.75.75,0,0,1-.22.57.73.73,0,0,1-.52.21.7.7,0,0,1-.51-.22.75.75,0,0,1-.22-.56Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M522.43,537.42h5.42a3.31,3.31,0,0,0-.7-2.13,2.38,2.38,0,0,0-1.86-.83,2.53,2.53,0,0,0-1.94.78,3.25,3.25,0,0,0-.79,2.18m-1.59.47a6.14,6.14,0,0,1,.56-2.34,4.52,4.52,0,0,1,1.46-1.79,3.92,3.92,0,0,1,4.43,0,4.44,4.44,0,0,1,1.49,1.78,5.34,5.34,0,0,1,.53,2.31q0,.78-.88.78h-6a3.22,3.22,0,0,0,.41,1.62,2.5,2.5,0,0,0,1.05,1,3.23,3.23,0,0,0,1.46.33,3.91,3.91,0,0,0,2.58-1,1.26,1.26,0,0,1,.6-.29.49.49,0,0,1,.41.2.78.78,0,0,1,.15.47.9.9,0,0,1-.23.58,4.46,4.46,0,0,1-1.5,1,5.2,5.2,0,0,1-2.09.42,4.42,4.42,0,0,1-2-.44,3.84,3.84,0,0,1-1.39-1.17,5,5,0,0,1-.77-1.58,6.65,6.65,0,0,1-.26-1.72l0-.06v0" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
<path d="M531,534a.83.83,0,0,1,.21-.59.69.69,0,0,1,.52-.22.72.72,0,0,1,.53.22.81.81,0,0,1,.22.6v.81h0a4.3,4.3,0,0,1,.87-1.13,1.77,1.77,0,0,1,1.13-.53.85.85,0,0,1,.59.23.76.76,0,0,1,.26.58.69.69,0,0,1-.26.6,2.4,2.4,0,0,1-.76.33,3.19,3.19,0,0,0-.65.23,2.54,2.54,0,0,0-1.2,2.4v4.66a.84.84,0,0,1-.2.6.68.68,0,0,1-.51.21.73.73,0,0,1-.54-.22.86.86,0,0,1-.22-.63Z" transform="translate(-432.92 -481.05)" style="fill:#034ea2"/>
</svg>
"""

# ====================== CSS ======================
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(90deg, #1a365d 0%, #2b6cb0 100%);
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.12);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .main-header .logo {
        flex-shrink: 0;
        background: white;
        border-radius: 6px;
        padding: 4px 6px;
        display: flex;
        align-items: center;
    }
    .main-header .title-block { flex: 1; text-align: center; }
    .main-header h1 {
        margin: 0;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    .main-header h2 {
        margin: 2px 0 0 0;
        font-size: 12px;
        font-weight: 600;
        color: #fefcbf;
        letter-spacing: 0.3px;
    }
    
    .filter-label {
        font-weight: 700 !important;
        color: #c53030 !important;
        font-size: 11px !important;
        margin-bottom: 2px;
    }
    
    [data-testid="stPopover"] button {
        color: #e53e3e !important;
        font-weight: 900 !important;
        font-size: 13px !important;
    }
    
    footer {visibility: hidden;}
    #MainMenu, header {visibility: visible !important;}
    
    .custom-kpi-table-container {
        max-height: none !important;
        overflow-x: auto !important;
        overflow-y: visible !important;
        position: relative;
        border: 1px solid #cbd5e0;
        border-radius: 6px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        background-color: #ffffff;
        margin-bottom: 15px;
        -webkit-overflow-scrolling: touch;
    }
    .custom-kpi-table {
        width: 100%;
        border-collapse: collapse !important;
        border-spacing: 0;
        font-family: sans-serif;
        font-size: 11px;
        background-color: #ffffff;
        white-space: nowrap;
    }
    .custom-kpi-table th {
        background-color: #1a365d !important;
        color: #ffffff !important;
        font-weight: bold !important;
        text-align: center !important;
        vertical-align: middle !important;
        border: 1px solid #cbd5e0 !important;
        padding: 8px 6px;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .custom-kpi-table td {
        border: 1px solid #e2e8f0 !important;
        padding: 6px 8px;
        vertical-align: middle !important;
        background-color: #ffffff;
    }
</style>
""",
    unsafe_allow_html=True,
)


def render_metric_card(label, value):
    st.markdown(
        f"""
    <div style="background: #ebf8ff; border: 1px solid #bee3f8; border-radius: 6px; padding: 8px; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.04); margin-bottom: 6px;">
        <div style="color: #c53030; font-weight: 800; font-size: 0.95rem; margin-bottom: 2px;">{label}</div>
        <div style="color: #c53030; font-weight: 800; font-size: 1.3rem;">{value}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def generate_top_bottom_analysis(
    df_source, name_col, pct_col, total_mtd, total_tgt
):
    if df_source is None or df_source.empty:
        return ''
    df_clean = df_source[
        ~df_source[name_col]
        .astype(str)
        .str.contains('TỔNG CỘNG|Tổng cộng', case=False, na=False)
    ].copy()
    if df_clean.empty:
        return ''
    df_clean['__sort_val'] = (
        df_clean[pct_col].astype(str).str.replace('%', '').str.strip()
    )
    df_clean['__sort_val'] = pd.to_numeric(
        df_clean['__sort_val'], errors='coerce'
    ).fillna(0)
    df_sorted = df_clean.sort_values(by='__sort_val', ascending=False)
    top3 = df_sorted.head(3)
    bottom3 = df_sorted.tail(3).sort_values(by='__sort_val', ascending=True)
    top_str = ', '.join(
        [f'**{r[name_col]}** ({r[pct_col]})' for _, r in top3.iterrows()]
    )
    bottom_str = ', '.join(
        [f'**{r[name_col]}** ({r[pct_col]})' for _, r in bottom3.iterrows()]
    )
    team_pct = round(total_mtd / total_tgt * 100, 1) if total_tgt else 0
    return f"""
* **Kết Quả Thực Hiện:** Đạt {total_mtd:,} / {total_tgt:,} ({team_pct}% MTD).
* **Top 3 ĐDKD Dẫn Đầu:** {top_str}.
* **Bottom 3 ĐDKD Cần Cải Thiện:** {bottom_str}.
* **Đề Xuất Hành Động Cho 3 Bạn Bottom:** Tập trung rà soát tuyến chưa mua, đẩy mạnh combo kích cầu và SS đồng hành đi thị trường (Field Coaching) trong 2 ngày tới.
    """


# ====================== ĐƯỜNG DẪN & LOAD DATA ======================
DATA_DIR = 'data'
RPT_PATH = os.path.join(DATA_DIR, 'RPT_061.xlsx')
MCP_PATH = os.path.join(DATA_DIR, 'Data_MCP.xlsx')
KPI_PATH = os.path.join(DATA_DIR, 'Target_KPI.xlsx')
CAT_PATH = 'Data_Cat.xlsx'
BRAND_PATH = 'Data_Brand.xlsx'

if not os.path.exists(MCP_PATH) and os.path.exists('Data_MCP.xlsx'):
    MCP_PATH = 'Data_MCP.xlsx'

combo_off_files = (
    [f for f in os.listdir(DATA_DIR) if 'Combo' in f and 'OFF' in f]
    if os.path.exists(DATA_DIR)
    else []
)
combo_on_files = (
    [f for f in os.listdir(DATA_DIR) if 'Combo' in f and 'On' in f]
    if os.path.exists(DATA_DIR)
    else []
)
COMBO_OFF_PATH = (
    os.path.join(DATA_DIR, combo_off_files[0])
    if combo_off_files
    else os.path.join(DATA_DIR, 'Tân_Combo Kênh OFF.xlsx')
)
COMBO_ON_PATH = (
    os.path.join(DATA_DIR, combo_on_files[0])
    if combo_on_files
    else os.path.join(DATA_DIR, 'Tân_Combo Kênh On.xlsx')
)


@st.cache_data(ttl=600)
def load_main_data():
    if not os.path.exists(RPT_PATH) or not os.path.exists(MCP_PATH):
        st.error('Thiếu file RPT_061.xlsx hoặc Data_MCP.xlsx')
        st.stop()
    df = pd.read_excel(RPT_PATH)
    mcp = pd.read_excel(MCP_PATH)
    df = df[df['Tình trạng đơn hàng'] != 'Đã hủy'].copy()
    df['Ngày tạo đơn hàng'] = pd.to_datetime(
        df['Ngày tạo đơn hàng'], format='%d/%m/%Y %H:%M:%S', errors='coerce'
    )
    df['date'] = df['Ngày tạo đơn hàng'].dt.date
    mcp_map = mcp[['Outlet_code', 'L1']].drop_duplicates('Outlet_code')
    mcp_map['Outlet_code'] = mcp_map['Outlet_code'].astype(str)
    df['Mã CH'] = df['Mã CH'].astype(str)
    df = df.merge(mcp_map, left_on='Mã CH', right_on='Outlet_code', how='left')
    df['Tên SP lower'] = df['Tên sản phẩm'].astype(str).str.lower()
    return df, mcp


@st.cache_data(ttl=600)
def load_combo_data():
    df_off, df_on = pd.DataFrame(), pd.DataFrame()
    try:
        if os.path.exists(COMBO_OFF_PATH):
            raw_off = pd.read_excel(COMBO_OFF_PATH, header=2)
            new_cols = raw_off.iloc[0].values
            df_off = raw_off.iloc[1:].copy()
            df_off.columns = [
                str(c) if pd.notna(c) else f'Col_{i}'
                for i, c in enumerate(new_cols)
            ]
    except Exception:
        pass
    try:
        if os.path.exists(COMBO_ON_PATH):
            raw_on = pd.read_excel(COMBO_ON_PATH, header=2)
            new_cols = raw_on.iloc[0].values
            df_on = raw_on.iloc[1:].copy()
            df_on.columns = [
                str(c) if pd.notna(c) else f'Col_{i}'
                for i, c in enumerate(new_cols)
            ]
    except Exception:
        pass
    return df_off, df_on


@st.cache_data(ttl=600)
def load_cat_data():
    for path in [CAT_PATH, os.path.join(DATA_DIR, 'Data_Cat.xlsx')]:
        if os.path.exists(path):
            try:
                return pd.read_excel(path)
            except:
                pass
    return pd.DataFrame()


@st.cache_data(ttl=600)
def load_brand_data():
    for path in [BRAND_PATH, os.path.join(DATA_DIR, 'Data_Brand.xlsx')]:
        if os.path.exists(path):
            try:
                return pd.read_excel(path)
            except:
                pass
    return pd.DataFrame()


@st.cache_data(ttl=600)
def get_targets():
    if not os.path.exists(KPI_PATH):
        return {}
    try:
        kpi = pd.read_excel(KPI_PATH, header=None).iloc[2:]
        kpi.columns = [
            'Region',
            'Month',
            'Ship to',
            'Distributor',
            'SUP',
            'SM pos',
            'SM code',
            'SM name',
            'Saleteam',
            'KPI type',
            'KPI Name',
            'Target',
            'Thực hiện',
            '% actual',
            '% Contrib',
            'Chưa ra HĐ',
        ]
        kpi = kpi.dropna(subset=['SM code'])
        kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')
        targets = {}
        for _, r in kpi.iterrows():
            sm, ktype, kname, tgt = (
                str(r['SM code']).strip(),
                str(r['KPI type']).strip(),
                str(r['KPI Name']).strip(),
                r['Target'],
            )
            if pd.isna(tgt):
                continue
            ktype_lower, kname_lower = ktype.lower(), kname.lower()
            if ktype_lower == 'aso_all':
                targets.setdefault(sm, {})['ASO_ALL'] = int(tgt)
            elif ktype_lower == 'pc_bt':
                targets.setdefault(sm, {})['PC_BT'] = int(tgt)
            elif ktype_lower == 'aso_on':
                targets.setdefault(sm, {})['ASO_ON'] = int(tgt)
            elif ktype_lower == 'aso_focus' or 'xanh' in kname_lower:
                targets.setdefault(sm, {})['ASO_CHANTE'] = int(tgt)
            elif (
                ktype_lower == 'aso_focus_2'
                or 'vàng' in kname_lower
                or 'trận vàng' in kname_lower
            ):
                targets.setdefault(sm, {})['ASO_OMACHI'] = int(tgt)
        return targets
    except:
        return {}


@st.cache_data(ttl=600)
def get_turnover_targets():
    if not os.path.exists(KPI_PATH):
        return {}
    try:
        kpi = pd.read_excel(KPI_PATH, header=None).iloc[2:]
        kpi.columns = [
            'Region',
            'Month',
            'Ship to',
            'Distributor',
            'SUP',
            'SM pos',
            'SM code',
            'SM name',
            'Saleteam',
            'KPI type',
            'KPI Name',
            'Target',
            'Thực hiện',
            '% actual',
            '% Contrib',
            'Chưa ra HĐ',
        ]
        kpi = kpi.dropna(subset=['SM code'])
        kpi['Target'] = pd.to_numeric(kpi['Target'], errors='coerce')
        targets = {}
        for _, r in kpi.iterrows():
            sm, ktype = str(r['SM code']).strip(), str(r['KPI type']).strip().lower()
            tgt = r['Target']
            if pd.isna(tgt):
                continue
            if ktype == 'turnover':
                targets[sm] = float(tgt)
        return targets
    except:
        return {}


def color_pct_bg(val):
    try:
        v = float(str(val).replace('%', '').strip())
        if v >= 70:
            return 'background-color: #c6f6d5; color:#22543d; font-weight:600;'
        elif v >= 50:
            return 'background-color: #fefcbf; color:#744210; font-weight:600;'
        else:
            return 'background-color: #fed7d7; color:#742a2a; font-weight:600;'
    except:
        return ''


def find_col(df, candidates):
    cols = {c.lower().strip(): c for c in df.columns}
    for c in candidates:
        if c.lower() in cols:
            return cols[c.lower()]
    return None


def filter_by_thu_multi(df, col_thu, f_thu_list):
    if not f_thu_list or not col_thu:
        return df
    thu_s = df[col_thu].astype(str).str.strip()
    mask = pd.Series(False, index=df.index)
    mapping_rules = {
        '2': ['2', '25'],
        '3': ['3', '36'],
        '4': ['4', '47'],
        '5': ['5', '25'],
        '6': ['6', '36'],
        '7': ['7', '47'],
        '25': ['25'],
        '36': ['36'],
        '47': ['47'],
    }
    for f_thu in f_thu_list:
        valid_set = mapping_rules.get(str(f_thu).strip(), [str(f_thu).strip()])
        mask = mask | thu_s.isin(valid_set)
    return df[mask]


def process_mcp_sales(df_rpt, df_mcp):
    if df_mcp.empty or df_rpt.empty:
        return df_mcp
    valid_df = df_rpt[df_rpt['Tình trạng đơn hàng'] != 'Đã hủy'].copy()
    val_col = (
        find_col(valid_df, ['Tổng tiền', 'Giá trị sau CK', 'Doanh thu'])
        or 'Tổng tiền'
    )
    valid_df['Mã CH_str'] = valid_df['Mã CH'].astype(str).str.strip()
    sales_agg = valid_df.groupby('Mã CH_str')[val_col].sum().reset_index()
    sales_agg.columns = ['Outlet_code_key', 'Total_Sales']
    df_out = df_mcp.copy()
    code_col = find_col(df_out, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    sales_col = find_col(df_out, ['Doanh Số MTD', 'Doanh số MTD', 'Doanh_so_MTD'])
    if not code_col:
        return df_out
    df_out['_key'] = df_out[code_col].astype(str).str.strip()
    sales_agg['Outlet_code_key'] = sales_agg['Outlet_code_key'].astype(str)
    df_out = df_out.merge(
        sales_agg, left_on='_key', right_on='Outlet_code_key', how='left'
    )
    target_sales_col = sales_col if sales_col else 'Doanh Số MTD'
    df_out[target_sales_col] = df_out['Total_Sales'].fillna(0.0)
    drop_cols = [
        c for c in ['_key', 'Outlet_code_key', 'Total_Sales'] if c in df_out.columns
    ]
    return df_out.drop(columns=drop_cols)


def process_cat_sales(df_rpt, df_cat):
    if df_cat.empty or df_rpt.empty:
        return df_cat
    sub_map = {
        'Beer': 'Bia',
        'Coffee': 'Cà phê',
        'Seasoning': 'Gia vị',
        'Home Care': 'Hóa Mỹ Phẩm',
        'Convenience Foods': 'Mì, Lẩu, Phở, Hủ Tiếu',
        'Refreshment Drinks': 'Nước giải khát',
        'Nutrition': 'Ngũ cốc',
        'Processed Meats': 'Xúc xích, Thịt chế biến',
    }
    df_clean = df_rpt.copy()
    sub_div_col = find_col(df_clean, ['Sub Division', 'SubDivision', 'Phân nhóm'])
    val_col = (
        find_col(df_clean, ['Tổng tiền', 'Giá trị sau CK']) or 'Tổng tiền'
    )
    status_col = find_col(df_clean, ['Tình trạng đơn hàng', 'Trạng thái'])
    df_clean['Mapped_Cat'] = (
        df_clean[sub_div_col].map(sub_map).fillna(df_clean[sub_div_col])
        if sub_div_col
        else 'Khác'
    )
    df_clean['Mã CH_str'] = df_clean['Mã CH'].astype(str).str.strip()
    df_valid = (
        df_clean[df_clean[status_col] != 'Đã hủy'] if status_col else df_clean
    )
    agg_cat1 = (
        df_valid.groupby(['Mã CH_str', 'Mapped_Cat'])[val_col]
        .sum()
        .reset_index()
    )
    agg_cat1.columns = ['Outlet_key', 'Cat_Key', 'Val1']
    df_out = df_cat.copy()
    c_code = find_col(df_out, ['Outlet Code', 'Outlet_code', 'Mã CH'])
    c_cat = find_col(df_out, ['Danh sách full cat', 'Category', 'Cat'])
    col_val1 = find_col(
        df_out,
        ['Doanh số thực đạt của CAT', 'Doanh số thực đạt CAT'],
    )
    if not c_code or not c_cat:
        return df_out
    df_out['_outlet_key'] = df_out[c_code].astype(str).str.strip()
    df_out['_cat_key'] = df_out[c_cat].astype(str).str.strip()
    df_out = df_out.merge(
        agg_cat1,
        left_on=['_outlet_key', '_cat_key'],
        right_on=['Outlet_key', 'Cat_Key'],
        how='left',
    )
    if 'Outlet_key' in df_out.columns:
        df_out = df_out.drop(columns=['Outlet_key', 'Cat_Key'])
    if col_val1:
        df_out[col_val1] = df_out['Val1'].fillna(0.0)
    drop_cols = [
        c for c in ['_outlet_key', '_cat_key', 'Val1'] if c in df_out.columns
    ]
    return df_out.drop(columns=drop_cols)


def process_brand_sales(df_rpt, df_brand):
    if df_brand.empty or df_rpt.empty:
        return df_brand
    c_brand_col = [
        c
        for c in df_brand.columns
        if 'brand' in c.lower() and 'danh sách' in c.lower()
    ]
    brand_col_name = c_brand_col[0] if c_brand_col else 'Danh sách full brand'
    df_clean = df_rpt.copy()
    sku_col1 = find_col(df_clean, ['Group std', 'Tên sản phẩm']) or 'Tên sản phẩm'
    sku_col2 = find_col(df_clean, ['Tên sản phẩm']) or 'Tên sản phẩm'
    df_clean['Search_Str'] = (
        df_clean[sku_col1].astype(str) + ' ' + df_clean[sku_col2].astype(str)
    )
    val_col = find_col(df_clean, ['Tổng tiền', 'Giá trị sau CK']) or 'Tổng tiền'
    status_col = find_col(df_clean, ['Tình trạng đơn hàng'])
    df_out = df_brand.copy()
    c_code = find_col(df_out, ['Outlet Code', 'Outlet_code', 'Mã CH'])
    col_val1 = find_col(df_out, ['Doanh số thực đạt của brand'])
    if not c_code:
        return df_out
    return df_out


# Báo cáo các tab KPI
def build_report(
    df, report_date, targets, report_type, filter_nv=None, mcp_df=None
):
    df_mtd = df[
        df['date'] >= date(report_date.year, report_date.month, 1)
    ].copy()
    if filter_nv and filter_nv != 'Tất cả ĐDKD':
        df_mtd = df_mtd[df_mtd['Tên NVBH'] == filter_nv]
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())

    if report_type == 'ASO_ALL':
        off = df_mtd[df_mtd['L1'] == 'Kênh Off Premise'].copy()
        mtd = off.groupby('Mã NVBH')['Mã CH'].nunique()
        first = (
            off.groupby(['Mã NVBH', 'Mã CH'])['date'].min().reset_index()
        )
        first.columns = ['Mã NVBH', 'Mã CH', 'first_date']
        ngay = (
            first[first['first_date'] == report_date]
            .groupby('Mã NVBH')['Mã CH']
            .nunique()
        )
        key, title = 'ASO_ALL', '5. ASO ALL KÊNH OFF'
    elif report_type == 'PC_BT':
        off = df_mtd[
            (df_mtd['L1'] == 'Kênh Off Premise')
            & ~df_mtd['Sub Division']
            .astype(str)
            .str.contains('Beer|Bia', case=False, na=False)
        ]
        lines = off.groupby(['Mã NVBH', 'Mã đơn hàng'])['Mã sản phẩm'].nunique()
        mtd = (
            lines[lines >= 4]
            .reset_index()
            .groupby('Mã NVBH')['Mã đơn hàng']
            .nunique()
        )
        df_today = df[df['date'] == report_date]
        if filter_nv and filter_nv != 'Tất cả ĐDKD':
            df_today = df_today[df_today['Tên NVBH'] == filter_nv]
        off_t = df_today[
            (df_today['L1'] == 'Kênh Off Premise')
            & ~df_today['Sub Division']
            .astype(str)
            .str.contains('Beer|Bia', case=False, na=False)
        ]
        lines_t = off_t.groupby(['Mã NVBH', 'Mã đơn hàng'])[
            'Mã sản phẩm'
        ].nunique()
        ngay = (
            lines_t[lines_t >= 4]
            .reset_index()
            .groupby('Mã NVBH')['Mã đơn hàng']
            .nunique()
        )
        key, title = 'PC_BT', '4. PC BT (PC 4LINE - BEER)'
    elif report_type == 'PC_ON':
        on_mtd = df_mtd[df_mtd['L1'] == 'Kênh On Premise']
        mtd = on_mtd.groupby('Mã NVBH')['Mã CH'].nunique()
        df_today = df[df['date'] == report_date]
        if filter_nv and filter_nv != 'Tất cả ĐDKD':
            df_today = df_today[df_today['Tên NVBH'] == filter_nv]
        on_today = df_today[df_today['L1'] == 'Kênh On Premise']
        ngay = on_today.groupby('Mã NVBH')['Mã đơn hàng'].nunique()
        on_targets = {}
        if mcp_df is not None and not mcp_df.empty:
            c_nv_mcp = find_col(mcp_df, ['SM Code', 'Mã NVBH', 'SM code'])
            c_l1 = find_col(mcp_df, ['L1', 'Channel'])
            c_ma = find_col(mcp_df, ['Outlet_code', 'Outlet Code', 'Mã CH'])
            if c_nv_mcp and c_l1 and c_ma:
                on_mcp = mcp_df[
                    mcp_df[c_l1].astype(str).str.contains('On', case=False, na=False)
                ].copy()
                on_targets = (
                    on_mcp.groupby(c_nv_mcp)[c_ma].nunique().to_dict()
                )
        title = '6. ASO ACTIVE KÊNH ON'
    elif report_type == 'ASO_TEA':
        on = df_mtd[df_mtd['L1'] == 'Kênh On Premise']
        tea = on[
            on['Tên SP lower'].str.contains(
                'tea|trà|ô long|olong|búp non', na=False
            )
        ].copy()
        tea['qty'] = pd.to_numeric(tea['Tổng lẻ'], errors='coerce').fillna(0)
        ch = tea.groupby(['Mã NVBH', 'Mã CH'])['qty'].sum()
        mtd = (
            ch[ch >= 12].reset_index().groupby('Mã NVBH')['Mã CH'].nunique()
        )
        df_today = df[df['date'] == report_date]
        if filter_nv and filter_nv != 'Tất cả ĐDKD':
            df_today = df_today[df_today['Tên NVBH'] == filter_nv]
        on_t = df_today[df_today['L1'] == 'Kênh On Premise']
        tea_t = on_t[
            on_t['Tên SP lower'].str.contains(
                'tea|trà|ô long|olong|búp non', na=False
            )
        ]
        ngay = tea_t.groupby('Mã NVBH')['Mã CH'].nunique()
        key, title = 'ASO_ON', '3. ASO TEA KÊNH ON'
    elif report_type == 'OMACHI':
        mask = df_mtd['Tên SP lower'].str.contains(
            'omachi', na=False
        ) & df_mtd['Tên SP lower'].str.contains('trộn|tron|xào|xao', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        first = (
            df_mtd[mask]
            .groupby(['Mã NVBH', 'Mã CH'])['date']
            .min()
            .reset_index()
        )
        first.columns = ['Mã NVBH', 'Mã CH', 'first_date']
        ngay = (
            first[first['first_date'] == report_date]
            .groupby('Mã NVBH')['Mã CH']
            .nunique()
        )
        key, title = 'ASO_OMACHI', '2. ASO FOCUS OMC TRỘN'
    elif report_type == 'CHANTE':
        mask = df_mtd['Tên SP lower'].str.contains('chanté|chante', na=False)
        mtd = df_mtd[mask].groupby('Mã NVBH')['Mã CH'].nunique()
        first = (
            df_mtd[mask]
            .groupby(['Mã NVBH', 'Mã CH'])['date']
            .min()
            .reset_index()
        )
        first.columns = ['Mã NVBH', 'Mã CH', 'first_date']
        ngay = (
            first[first['first_date'] == report_date]
            .groupby('Mã NVBH')['Mã CH']
            .nunique()
        )
        key, title = 'ASO_CHANTE', '1. ASO FOCUS CHANTÉ'
    else:
        return pd.DataFrame(), 0, ''

    results = []
    for sm in all_sms:
        tgt = (
            int(on_targets.get(sm, 0))
            if report_type == 'PC_ON'
            else targets.get(sm, {}).get(key, 0)
        )
        m = int(mtd.get(sm, 0))
        n = int(ngay.get(sm, 0))
        pct = round(m / tgt * 100, 1) if tgt else 0
        results.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Chỉ Tiêu KPI': tgt,
            'Thực Hiện Ngày': n,
            'MTD': m,
            '% MTD': f'{pct}%',
            '_ratio': (m / tgt if tgt else 0),
        })
    df_out = (
        pd.DataFrame(results)
        .sort_values('_ratio', ascending=True)
        .drop(columns=['_ratio'])
        .reset_index(drop=True)
    )
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))
    total_ngay = int(df_out['Thực Hiện Ngày'].sum()) if not df_out.empty else 0
    total_mtd = int(df_out['MTD'].sum()) if not df_out.empty else 0
    team_tgt = int(df_out['Chỉ Tiêu KPI'].sum()) if not df_out.empty else 0
    total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0
    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': (
            'SS Trương Thanh Tân Total'
            if filter_nv == 'Tất cả ĐDKD'
            else filter_nv
        ),
        'Chỉ Tiêu KPI': team_tgt,
        'Thực Hiện Ngày': total_ngay,
        'MTD': total_mtd,
        '% MTD': f'{total_pct}%',
    }])
    return pd.concat([df_out, total_row], ignore_index=True), team_tgt, title


def build_turnover_report(df, report_date, turnover_targets, filter_nv=None):
    df_mtd = df[
        df['date'] >= date(report_date.year, report_date.month, 1)
    ].copy()
    df_today = df[df['date'] == report_date].copy()
    if filter_nv and filter_nv != 'Tất cả ĐDKD':
        df_mtd = df_mtd[df_mtd['Tên NVBH'] == filter_nv]
        df_today = df_today[df_today['Tên NVBH'] == filter_nv]
    sm_names = df_mtd.groupby('Mã NVBH')['Tên NVBH'].first().to_dict()
    all_sms = sorted(sm_names.keys())
    val_col = find_col(df_mtd, ['Thành tiền trước CK']) or 'Thành tiền trước CK'
    mtd_sales = df_mtd.groupby('Mã NVBH')[val_col].sum().to_dict()
    today_sales = df_today.groupby('Mã NVBH')[val_col].sum().to_dict()
    results = []
    for sm in all_sms:
        tgt = turnover_targets.get(sm, 0.0)
        m = float(mtd_sales.get(sm, 0.0))
        t_val = float(today_sales.get(sm, 0.0))
        pct = round(m / tgt * 100, 1) if tgt else 0.0
        results.append({
            'Mã NVBH': sm,
            'Tên NVBH': sm_names.get(sm, ''),
            'Chỉ Tiêu Doanh Số': tgt,
            'Thực Hiện Ngày': t_val,
            'Doanh Số MTD': m,
            '% MTD': f'{pct}%',
            '_ratio': (m / tgt if tgt else 0),
        })
    df_out = (
        pd.DataFrame(results)
        .sort_values('_ratio', ascending=True)
        .drop(columns=['_ratio'])
        .reset_index(drop=True)
    )
    df_out.insert(0, 'STT', range(1, len(df_out) + 1))
    total_mtd = float(df_out['Doanh Số MTD'].sum()) if not df_out.empty else 0.0
    total_today = (
        float(df_out['Thực Hiện Ngày'].sum()) if not df_out.empty else 0.0
    )
    team_tgt = (
        float(df_out['Chỉ Tiêu Doanh Số'].sum()) if not df_out.empty else 0.0
    )
    total_pct = round(total_mtd / team_tgt * 100, 1) if team_tgt else 0.0
    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': (
            'SS Trương Thanh Tân Total'
            if filter_nv == 'Tất cả ĐDKD'
            else filter_nv
        ),
        'Chỉ Tiêu Doanh Số': team_tgt,
        'Thực Hiện Ngày': total_today,
        'Doanh Số MTD': total_mtd,
        '% MTD': f'{total_pct}%',
    }])
    return (
        pd.concat([df_out, total_row], ignore_index=True),
        team_tgt,
        '8. BÁO CÁO DOANH SỐ TURNOVER',
    )


def build_visit_report(df_mcp, df_rpt, report_date, filter_nv=None, f_thu_list=None):
    if df_mcp.empty:
        return pd.DataFrame(), '10. BÁO CÁO LỊCH VIẾNG THĂM'
    mcp_f = df_mcp.copy()
    iso_year, iso_week, _ = report_date.isocalendar()
    is_odd_iso_week = iso_week % 2 == 1
    c_odd = find_col(mcp_f, ['ODD_WEEK', 'Odd_Week'])
    if c_odd:
        if is_odd_iso_week:
            mcp_f = mcp_f[
                mcp_f[c_odd]
                .astype(str)
                .str.strip()
                .isin(['Odd Week', 'Both', 'both', 'odd week'])
            ]
        else:
            mcp_f = mcp_f[
                mcp_f[c_odd]
                .astype(str)
                .str.strip()
                .isin(['Even Week', 'Both', 'both', 'even week'])
            ]
    if filter_nv and filter_nv != 'Tất cả ĐDKD':
        c_nv = find_col(mcp_f, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        if c_nv:
            mcp_f = mcp_f[mcp_f[c_nv].astype(str).str.strip() == filter_nv]
    if f_thu_list:
        c_thu = find_col(mcp_f, ['Thứ', 'Frequency', 'Tần suất'])
        mcp_f = filter_by_thu_multi(mcp_f, c_thu, f_thu_list)

    c_nv_name = (
        find_col(mcp_f, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        or 'SM name'
    )
    c_nv_code = (
        find_col(mcp_f, ['SM Code', 'Mã NVBH', 'SM code']) or 'SM code'
    )
    c_ma_col = (
        find_col(mcp_f, ['Outlet_code', 'Outlet Code', 'Mã CH']) or 'Outlet_code'
    )
    c_vip = find_col(mcp_f, ['VIP MCH', 'VIP_MCH'])
    c_l1 = find_col(mcp_f, ['L1', 'Channel'])

    df_mtd = df_rpt[
        df_rpt['date'] >= date(report_date.year, report_date.month, 1)
    ].copy()
    valid_bought_mas = set(
        df_mtd[df_mtd['Tình trạng đơn hàng'] != 'Đã hủy']['Mã CH']
        .astype(str)
        .str.strip()
        .unique()
    )
    nv_list = (
        sorted(mcp_f[c_nv_name].dropna().astype(str).unique().tolist())
        if c_nv_name in mcp_f.columns
        else []
    )
    rows = []
    for nv in nv_list:
        sub = mcp_f[mcp_f[c_nv_name].astype(str).str.strip() == nv]
        sm_code = (
            sub[c_nv_code].iloc[0]
            if c_nv_code in sub.columns and not sub[c_nv_code].empty
            else ''
        )
        sub['MA_str'] = sub[c_ma_col].astype(str).str.strip()
        sub['Is_Bought'] = sub['MA_str'].isin(valid_bought_mas)
        total_kh = sub['MA_str'].nunique()
        da_mua_total = sub[sub['Is_Bought']]['MA_str'].nunique()
        pct_total = round(da_mua_total / total_kh * 100, 1) if total_kh else 0

        sub_v3 = (
            sub[sub[c_vip].astype(str).str.strip() == 'VIP3']
            if c_vip
            else pd.DataFrame()
        )
        v3_kh = sub_v3['MA_str'].nunique() if not sub_v3.empty else 0
        v3_mua = (
            sub_v3[sub_v3['Is_Bought']]['MA_str'].nunique()
            if not sub_v3.empty
            else 0
        )
        v3_pct = round(v3_mua / v3_kh * 100, 1) if v3_kh else 0

        sub_v5 = (
            sub[sub[c_vip].astype(str).str.strip() == 'VIP5']
            if c_vip
            else pd.DataFrame()
        )
        v5_kh = sub_v5['MA_str'].nunique() if not sub_v5.empty else 0
        v5_mua = (
            sub_v5[sub_v5['Is_Bought']]['MA_str'].nunique()
            if not sub_v5.empty
            else 0
        )
        v5_pct = round(v5_mua / v5_kh * 100, 1) if v5_kh else 0

        sub_vsi = (
            sub[sub[c_vip].astype(str).str.strip() == 'VIPSI']
            if c_vip
            else pd.DataFrame()
        )
        vsi_kh = sub_vsi['MA_str'].nunique() if not sub_vsi.empty else 0
        vsi_mua = (
            sub_vsi[sub_vsi['Is_Bought']]['MA_str'].nunique()
            if not sub_vsi.empty
            else 0
        )
        vsi_pct = round(vsi_mua / vsi_kh * 100, 1) if vsi_kh else 0

        off_sub = (
            sub[~sub[c_l1].astype(str).str.contains('On', case=False, na=False)]
            if c_l1
            else sub
        )
        sub_ch_le = (
            off_sub[
                ~off_sub[c_vip]
                .astype(str)
                .str.strip()
                .isin(['VIP3', 'VIP5', 'VIPSI'])
            ]
            if c_vip
            else off_sub
        )
        le_kh = sub_ch_le['MA_str'].nunique() if not sub_ch_le.empty else 0
        le_mua = (
            sub_ch_le[sub_ch_le['Is_Bought']]['MA_str'].nunique()
            if not sub_ch_le.empty
            else 0
        )
        le_pct = round(le_mua / le_kh * 100, 1) if le_kh else 0

        sub_on = (
            sub[sub[c_l1].astype(str).str.contains('On', case=False, na=False)]
            if c_l1
            else pd.DataFrame()
        )
        on_kh = sub_on['MA_str'].nunique() if not sub_on.empty else 0
        on_mua = (
            sub_on[sub_on['Is_Bought']]['MA_str'].nunique()
            if not sub_on.empty
            else 0
        )
        on_pct = round(on_mua / on_kh * 100, 1) if on_kh else 0

        rows.append({
            'Mã NVBH': sm_code,
            'Tên NVBH': nv,
            'Lịch VT - Tổng KH': total_kh,
            'Lịch VT - Đã Mua': da_mua_total,
            'Lịch VT - % Active': f'{pct_total}%',
            'VIP 3 - Tổng KH': v3_kh,
            'VIP 3 - Đã Mua': v3_mua,
            'VIP 3 - % Active': f'{v3_pct}%',
            'VIP 5 - Tổng KH': v5_kh,
            'VIP 5 - Đã Mua': v5_mua,
            'VIP 5 - % Active': f'{v5_pct}%',
            'VIPSI - Tổng KH': vsi_kh,
            'VIPSI - Đã Mua': vsi_mua,
            'VIPSI - % Active': f'{vsi_pct}%',
            'Lẻ - Tổng KH': le_kh,
            'Lẻ - Đã Mua': le_mua,
            'Lẻ - % Active': f'{le_pct}%',
            'Kênh ON - Tổng KH': on_kh,
            'Kênh ON - Đã Mua': on_mua,
            'Kênh ON - % Active': f'{on_pct}%',
            '_sort': total_kh,
        })

    df_out = pd.DataFrame(rows)
    if not df_out.empty:
        df_out = (
            df_out.sort_values('_sort', ascending=False)
            .drop(columns=['_sort'])
            .reset_index(drop=True)
        )
        df_out.insert(0, 'STT', range(1, len(df_out) + 1))
        tot_vt_kh = int(df_out['Lịch VT - Tổng KH'].sum())
        tot_vt_mua = int(df_out['Lịch VT - Đã Mua'].sum())
        tot_vt_pct = round(tot_vt_mua / tot_vt_kh * 100, 1) if tot_vt_kh else 0
        total_row = pd.DataFrame([{
            'STT': '-',
            'Mã NVBH': 'TỔNG CỘNG',
            'Tên NVBH': f'{len(df_out)} Nhân viên',
            'Lịch VT - Tổng KH': tot_vt_kh,
            'Lịch VT - Đã Mua': tot_vt_mua,
            'Lịch VT - % Active': f'{tot_vt_pct}%',
            'VIP 3 - Tổng KH': int(df_out['VIP 3 - Tổng KH'].sum()),
            'VIP 3 - Đã Mua': int(df_out['VIP 3 - Đã Mua'].sum()),
            'VIP 3 - % Active': '0%',
            'VIP 5 - Tổng KH': int(df_out['VIP 5 - Tổng KH'].sum()),
            'VIP 5 - Đã Mua': int(df_out['VIP 5 - Đã Mua'].sum()),
            'VIP 5 - % Active': '0%',
            'VIPSI - Tổng KH': int(df_out['VIPSI - Tổng KH'].sum()),
            'VIPSI - Đã Mua': int(df_out['VIPSI - Đã Mua'].sum()),
            'VIPSI - % Active': '0%',
            'Lẻ - Tổng KH': int(df_out['Lẻ - Tổng KH'].sum()),
            'Lẻ - Đã Mua': int(df_out['Lẻ - Đã Mua'].sum()),
            'Lẻ - % Active': '0%',
            'Kênh ON - Tổng KH': int(df_out['Kênh ON - Tổng KH'].sum()),
            'Kênh ON - Đã Mua': int(df_out['Kênh ON - Đã Mua'].sum()),
            'Kênh ON - % Active': '0%',
        }])
        df_out = pd.concat([df_out, total_row], ignore_index=True)
    return df_out, f'10. BÁO CÁO LỊCH VIẾNG THĂM & % ACTIVE (Tuần ISO {iso_week})'


def render_visit_html_table(df):
    html = [
        '<div class="custom-kpi-table-container"><table'
        ' class="custom-kpi-table">'
    ]
    html.append(
        '<thead><tr><th rowspan="2">STT</th><th'
        ' rowspan="2">Mã NVBH</th><th rowspan="2">Tên NVBH</th>'
    )
    sections = ['Lịch VT', 'VIP 3', 'VIP 5', 'VIPSI', 'Lẻ', 'Kênh ON']
    for sec in sections:
        html.append(
            f'<th colspan="3" style="background-color: #1a365d; color:'
            f' #ffffff;">{sec}</th>'
        )
    html.append('</tr><tr>')
    for _ in sections:
        html.append('<th>Tổng KH</th><th>Đã Mua</th><th>% Active</th>')
    html.append('</tr></thead><tbody>')
    for _, row in df.iterrows():
        is_total = (
            str(row.get('Tên NVBH', '')).strip().startswith('TỔNG CỘNG')
        )
        html.append('<tr>')
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                val = ''
            is_pct = '%' in col
            style_bg = color_pct_bg(val) if is_pct else ''
            style = (
                f'background-color: #fff5f5; color: #c53030; font-weight: 900;'
                if is_total
                else style_bg
            )
            html.append(f'<td style="{style}">{val}</td>')
        html.append('</tr>')
    html.append('</tbody></table></div>')
    return ''.join(html)


def build_combo_matrix(
    df, report_date, df_off_master, df_on_master, filter_nv=None
):
    df_mtd = df[
        df['date'] >= date(report_date.year, report_date.month, 1)
    ].copy()
    if filter_nv and filter_nv != 'Tất cả ĐDKD':
        df_mtd = df_mtd[df_mtd['Tên NVBH'] == filter_nv]
    nv_list = sorted(df['Tên NVBH'].dropna().unique().tolist())
    off_target_map, on_target_map = {}, {}
    if (
        not df_off_master.empty
        and 'Tên NV' in df_off_master.columns
        and 'outlet_code' in df_off_master.columns
    ):
        off_target_map = (
            df_off_master.groupby('Tên NV')['outlet_code'].nunique().to_dict()
        )
    if (
        not df_on_master.empty
        and 'Tên NV' in df_on_master.columns
        and 'outlet_code' in df_on_master.columns
    ):
        on_target_map = (
            df_on_master.groupby('Tên NV')['outlet_code'].nunique().to_dict()
        )
    rows = []
    for idx, nv in enumerate(nv_list, 1):
        if filter_nv and filter_nv != 'Tất cả ĐDKD' and nv != filter_nv:
            continue
        rows.append({
            'Mã NVBH': '',
            'Tên NVBH': nv,
            'Target (OFF)': off_target_map.get(nv, 0),
            'Phát sinh Ngày (OFF)': 0,
            'MTD (OFF)': 0,
            '% MTD (OFF)': '0%',
            '_pct_off_val': 0,
            'Target (ON)': on_target_map.get(nv, 0),
            'Phát sinh Ngày (ON)': 0,
            'MTD (ON)': 0,
            '% MTD (ON)': '0%',
        })
    df_out = pd.DataFrame(rows)
    if not df_out.empty:
        df_out.insert(0, 'STT', range(1, len(df_out) + 1))
    total_row = pd.DataFrame([{
        'STT': '-',
        'Mã NVBH': 'TỔNG CỘNG',
        'Tên NVBH': 'Tổng',
        'Target (OFF)': 0,
        'Phát sinh Ngày (OFF)': 0,
        'MTD (OFF)': 0,
        '% MTD (OFF)': '0%',
        'Target (ON)': 0,
        'Phát sinh Ngày (ON)': 0,
        'MTD (ON)': 0,
        '% MTD (ON)': '0%',
    }])
    return pd.concat([df_out, total_row], ignore_index=True), 0, 0


def render_html_table(df):
    html = ['<div class="custom-kpi-table-container"><table class="custom-kpi-table">']
    html.append('<thead><tr>')
    for col in df.columns:
        html.append(f'<th>{col}</th>')
    html.append('</tr></thead><tbody>')
    for _, row in df.iterrows():
        is_total = (
            str(row.get('Tên NVBH', '')).strip() == 'TỔNG CỘNG'
            or str(row.get('Tên NV', '')).strip() == 'TỔNG CỘNG'
        )
        html.append('<tr>')
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                val = ''
            style = 'background-color: #fff5f5; color: #c53030 !important; font-weight: 900 !important;' if is_total else ''
            if '% MTD' in col:
                style += color_pct_bg(val)
            html.append(f'<td style="{style}">{val}</td>')
        html.append('</tr>')
    html.append('</tbody></table></div>')
    return ''.join(html)


# ====================== GIAO DIỆN CHÍNH ======================
st.markdown(
    f"""
<div class="main-header">
    <div class="logo">{logo_svg}</div>
    <div class="title-block">
        <h1>SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</h1>
        <h2>TRACKING KPI ĐDKD - TEAM SS TRƯƠNG THANH TÂN</h2>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

col_reload, _ = st.columns([2, 5])
with col_reload:
    if st.button('🔄 Xóa Cache & Reload Dữ Liệu'):
        st.cache_data.clear()
        st.rerun()

with st.spinner('Đang tải dữ liệu...'):
    df, mcp = load_main_data()
    targets = get_targets()
    turnover_targets = get_turnover_targets()
    df_cat = load_cat_data()
    df_brand = load_brand_data()
    df_combo_off, df_combo_on = load_combo_data()

    mcp = process_mcp_sales(df, mcp)
    df_cat = process_cat_sales(df, df_cat)
    df_brand = process_brand_sales(df, df_brand)

nv_list = sorted(df['Tên NVBH'].dropna().unique().tolist())
vn_time = dt.datetime.utcnow() + dt.timedelta(hours=7)
default_date_t_minus_1 = (vn_time - timedelta(days=1)).date()

f1, f2, f3 = st.columns([1, 1, 1.3])
with f1:
    st.markdown('<p class="filter-label">MONTH</p>', unsafe_allow_html=True)
    st.selectbox(
        '', ['Tháng 09/2026'], key='month', label_visibility='collapsed'
    )
with f2:
    st.markdown('<p class="filter-label">NGÀY</p>', unsafe_allow_html=True)
    report_date = st.date_input(
        '', value=default_date_t_minus_1, key='ngay', label_visibility='collapsed'
    )
with f3:
    st.markdown('<p class="filter-label">KPI NAME</p>', unsafe_allow_html=True)
    kpi_map = {
        '1. ASO FOCUS CHANTÉ': 'CHANTE',
        '2. ASO FOCUS OMC TRỘN': 'OMACHI',
        '3. ASO TEA KÊNH ON': 'ASO_TEA',
        '4. PC BT (PC 4LINE - BEER)': 'PC_BT',
        '5. ASO ALL': 'ASO_ALL',
        '6. ASO ACTIVE KÊNH ON': 'PC_ON',
        '7. BÁO CÁO ĐH COMBO': 'COMBO',
        '8. BÁO CÁO DOANH SỐ TURNOVER': 'TURNOVER',
        '9. BÁO CÁO TỔNG HỢP': 'SUMMARY',
        '10. BÁO CÁO LỊCH VIẾNG THĂM': 'VISIT',
    }
    selected_name = st.selectbox(
        '', list(kpi_map.keys()), key='kpi', label_visibility='collapsed'
    )
    selected_kpi = kpi_map[selected_name]

f4, f5 = st.columns([1, 1])
with f4:
    st.markdown('<p class="filter-label">SALE SUP</p>', unsafe_allow_html=True)
    st.selectbox(
        '',
        ['Trương Thanh Tân Total'],
        key='sup',
        label_visibility='collapsed',
    )
with f5:
    st.markdown(
        '<p class="filter-label">ĐDKD (Nhân viên)</p>', unsafe_allow_html=True
    )
    filter_nv = st.selectbox(
        '',
        ['Tất cả ĐDKD'] + nv_list,
        key='ddkd',
        label_visibility='collapsed',
    )

st.markdown('---')

tab_kpi, tab_mcp, tab_cat, tab_brand, tab_dskh_off, tab_dskh_on = st.tabs([
    '📊 BÁO CÁO KPI',
    '🗺️ MCP VISIT',
    '📦 TRACKING MBS - CAT',
    '🏷️ TRACKING MBS - BRAND',
    '📋 DSKH_Combo OFF',
    '📋 DSKH_Combo ON',
])

with tab_kpi:
    if selected_kpi == 'TURNOVER':
        df_r, team_tgt, title = build_turnover_report(
            df, report_date, turnover_targets, filter_nv
        )
        total_row = df_r.iloc[-1]
        st.markdown(
            f'<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">{title}</h3>',
            unsafe_allow_html=True,
        )
        st.markdown(render_html_table(df_r), unsafe_allow_html=True)
    elif selected_kpi != 'COMBO' and selected_kpi != 'SUMMARY' and selected_kpi != 'VISIT':
        df_r, team_tgt, title = build_report(
            df, report_date, targets, selected_kpi, filter_nv, mcp_df=mcp
        )
        st.markdown(
            f'<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">{title}</h3>',
            unsafe_allow_html=True,
        )
        st.markdown(render_html_table(df_r), unsafe_allow_html=True)
    else:
        st.info(
            'Vui lòng chọn các tab chuyên biệt bên cạnh hoặc xem báo cáo tổng hợp tương ứng.'
        )

# ==================== TAB MCP ====================
with tab_mcp:
    st.markdown(
        '<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">🗺️ MCP VISIT & MAPPING DOANH SỐ BÁN HÀNG</h3>',
        unsafe_allow_html=True,
    )
    if mcp.empty:
        st.warning('Chưa có dữ liệu MCP')
    else:
        col_nv = find_col(mcp, ['SM name', 'SM Name', 'Tên NVBH', 'Nhân viên'])
        col_thu = find_col(mcp, ['Thứ', 'Frequency', 'Tần suất'])
        col_ma = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH'])
        col_ten = find_col(mcp, ['Outlet_name', 'Outlet Name', 'Tên CH'])

        # 4 Bộ lọc chuẩn theo yêu cầu
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(
                '<p class="filter-label">👤 Tên NVBH</p>', unsafe_allow_html=True
            )
            nv_opts = (
                sorted(mcp[col_nv].dropna().astype(str).unique().tolist())
                if col_nv
                else []
            )
            f_nv = st.multiselect(
                '', nv_opts, key='mcp_nv_filter', label_visibility='collapsed'
            )
        with c2:
            st.markdown(
                '<p class="filter-label">📅 Thứ</p>', unsafe_allow_html=True
            )
            thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
            f_thu = st.multiselect(
                '',
                thu_opts,
                key='mcp_thu_filter',
                label_visibility='collapsed',
            )
        with c3:
            st.markdown(
                '<p class="filter-label">🔑 Mã Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ma = st.text_input(
                '',
                key='mcp_ma_filter',
                placeholder='Nhập mã KH...',
                label_visibility='collapsed',
            )
        with c4:
            st.markdown(
                '<p class="filter-label">🏷️ Tên Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ten = st.text_input(
                '',
                key='mcp_ten_filter',
                placeholder='Nhập tên KH...',
                label_visibility='collapsed',
            )

        df_f = mcp.copy()
        if f_nv and col_nv:
            df_f = df_f[df_f[col_nv].astype(str).isin(f_nv)]
        df_f = filter_by_thu_multi(df_f, col_thu, f_thu)
        if f_ma and col_ma:
            df_f = df_f[
                df_f[col_ma]
                .astype(str)
                .str.lower()
                .str.contains(f_ma.lower(), na=False)
            ]
        if f_ten and col_ten:
            df_f = df_f[
                df_f[col_ten]
                .astype(str)
                .str.lower()
                .str.contains(f_ten.lower(), na=False)
            ]

        st.dataframe(df_f, use_container_width=True, height=450, hide_index=True)
        st.caption(f'Hiển thị: {len(df_f):,} / {len(mcp):,} cửa hàng')

# ==================== TAB MBS CAT ====================
with tab_cat:
    st.markdown(
        '<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">📦 TRACKING MBS - THEO NGÀNH HÀNG (CATEGORY)</h3>',
        unsafe_allow_html=True,
    )
    if df_cat.empty:
        st.error('❌ Không tìm thấy Data_Cat.xlsx')
    else:
        c_nv_cat = find_col(df_cat, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        c_thu_cat = find_col(df_cat, ['Thứ', 'Frequency', 'Tần suất'])
        c_ma_cat = find_col(df_cat, ['Outlet Code', 'Outlet_code', 'Mã CH'])
        c_ten_cat = find_col(df_cat, ['Outlet Name', 'Outlet_name', 'Tên CH'])

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(
                '<p class="filter-label">👤 Tên NVBH</p>', unsafe_allow_html=True
            )
            nv_cat_opts = (
                sorted(df_cat[c_nv_cat].dropna().astype(str).unique().tolist())
                if c_nv_cat
                else []
            )
            f_nv_cat = st.multiselect(
                '', nv_cat_opts, key='cat_nv_filter', label_visibility='collapsed'
            )
        with c2:
            st.markdown(
                '<p class="filter-label">📅 Thứ</p>', unsafe_allow_html=True
            )
            thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
            f_thu_cat = st.multiselect(
                '',
                thu_opts,
                key='cat_thu_filter',
                label_visibility='collapsed',
            )
        with c3:
            st.markdown(
                '<p class="filter-label">🔑 Mã Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ma_cat = st.text_input(
                '',
                key='cat_ma_filter',
                placeholder='Nhập mã KH...',
                label_visibility='collapsed',
            )
        with c4:
            st.markdown(
                '<p class="filter-label">🏷️ Tên Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ten_cat = st.text_input(
                '',
                key='cat_ten_filter',
                placeholder='Nhập tên KH...',
                label_visibility='collapsed',
            )

        df_cat_f = df_cat.copy()
        if f_nv_cat and c_nv_cat:
            df_cat_f = df_cat_f[df_cat_f[c_nv_cat].astype(str).isin(f_nv_cat)]
        df_cat_f = filter_by_thu_multi(df_cat_f, c_thu_cat, f_thu_cat)
        if f_ma_cat and c_ma_cat:
            df_cat_f = df_cat_f[
                df_cat_f[c_ma_cat]
                .astype(str)
                .str.lower()
                .str.contains(f_ma_cat.lower(), na=False)
            ]
        if f_ten_cat and c_ten_cat:
            df_cat_f = df_cat_f[
                df_cat_f[c_ten_cat]
                .astype(str)
                .str.lower()
                .str.contains(f_ten_cat.lower(), na=False)
            ]

        st.dataframe(df_cat_f, use_container_width=True, height=450, hide_index=True)
        st.caption(f'Hiển thị: {len(df_cat_f):,} / {len(df_cat):,} dòng dữ liệu')

# ==================== TAB MBS BRAND ====================
with tab_brand:
    st.markdown(
        '<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">🏷️ TRACKING MBS - THEO THƯƠNG HIỆU (BRAND)</h3>',
        unsafe_allow_html=True,
    )
    if df_brand.empty:
        st.error('❌ Không tìm thấy Data_Brand.xlsx')
    else:
        c_nv_brand = find_col(df_brand, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên'])
        c_thu_brand = find_col(df_brand, ['Thứ', 'Frequency', 'Tần suất'])
        c_ma_brand = find_col(df_brand, ['Outlet Code', 'Outlet_code', 'Mã CH'])
        c_ten_brand = find_col(df_brand, ['Outlet Name', 'Outlet_name', 'Tên CH'])

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(
                '<p class="filter-label">👤 Tên NVBH</p>', unsafe_allow_html=True
            )
            nv_brand_opts = (
                sorted(df_brand[c_nv_brand].dropna().astype(str).unique().tolist())
                if c_nv_brand
                else []
            )
            f_nv_brand = st.multiselect(
                '', nv_brand_opts, key='brand_nv_filter', label_visibility='collapsed'
            )
        with c2:
            st.markdown(
                '<p class="filter-label">📅 Thứ</p>', unsafe_allow_html=True
            )
            thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
            f_thu_brand = st.multiselect(
                '',
                thu_opts,
                key='brand_thu_filter',
                label_visibility='collapsed',
            )
        with c3:
            st.markdown(
                '<p class="filter-label">🔑 Mã Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ma_brand = st.text_input(
                '',
                key='brand_ma_filter',
                placeholder='Nhập mã KH...',
                label_visibility='collapsed',
            )
        with c4:
            st.markdown(
                '<p class="filter-label">🏷️ Tên Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ten_brand = st.text_input(
                '',
                key='brand_ten_filter',
                placeholder='Nhập tên KH...',
                label_visibility='collapsed',
            )

        df_brand_f = df_brand.copy()
        if f_nv_brand and c_nv_brand:
            df_brand_f = df_brand_f[df_brand_f[c_nv_brand].astype(str).isin(f_nv_brand)]
        df_brand_f = filter_by_thu_multi(df_brand_f, c_thu_brand, f_thu_brand)
        if f_ma_brand and c_ma_brand:
            df_brand_f = df_brand_f[
                df_brand_f[c_ma_brand]
                .astype(str)
                .str.lower()
                .str.contains(f_ma_brand.lower(), na=False)
            ]
        if f_ten_brand and c_ten_brand:
            df_brand_f = df_brand_f[
                df_brand_f[c_ten_brand]
                .astype(str)
                .str.lower()
                .str.contains(f_ten_brand.lower(), na=False)
            ]

        st.dataframe(df_brand_f, use_container_width=True, height=450, hide_index=True)
        st.caption(f'Hiển thị: {len(df_brand_f):,} / {len(df_brand):,} dòng dữ liệu')

# ==================== TAB DSKH COMBO OFF ====================
with tab_dskh_off:
    st.markdown(
        '<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">📋 DANH SÁCH KHÁCH HÀNG COMBO OFF</h3>',
        unsafe_allow_html=True,
    )
    if df_combo_off.empty:
        st.warning('Chưa có dữ liệu Combo OFF')
    else:
        c_nv_off = find_col(df_combo_off, ['Tên NV', 'SM name', 'Nhân viên'])
        c_thu_off = find_col(df_combo_off, ['Thứ', 'Frequency'])
        c_ma_off = find_col(df_combo_off, ['outlet_code', 'Outlet Code', 'Mã CH'])
        c_ten_off = find_col(df_combo_off, ['outlet_name', 'Outlet Name', 'Tên CH'])

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(
                '<p class="filter-label">👤 Tên NVBH</p>', unsafe_allow_html=True
            )
            off_nv_opts = (
                sorted(df_combo_off[c_nv_off].dropna().astype(str).unique().tolist())
                if c_nv_off
                else []
            )
            f_off_nv = st.multiselect(
                '', off_nv_opts, key='off_nv_filter', label_visibility='collapsed'
            )
        with c2:
            st.markdown(
                '<p class="filter-label">📅 Thứ</p>', unsafe_allow_html=True
            )
            thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
            f_thu_off = st.multiselect(
                '',
                thu_opts,
                key='off_thu_filter',
                label_visibility='collapsed',
            )
        with c3:
            st.markdown(
                '<p class="filter-label">🔑 Mã Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ma_off = st.text_input(
                '',
                key='off_ma_filter',
                placeholder='Nhập mã KH...',
                label_visibility='collapsed',
            )
        with c4:
            st.markdown(
                '<p class="filter-label">🏷️ Tên Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ten_off = st.text_input(
                '',
                key='off_ten_filter',
                placeholder='Nhập tên KH...',
                label_visibility='collapsed',
            )

        df_off_f = df_combo_off.copy()
        if f_off_nv and c_nv_off:
            df_off_f = df_off_f[df_off_f[c_nv_off].astype(str).isin(f_off_nv)]
        df_off_f = filter_by_thu_multi(df_off_f, c_thu_off, f_thu_off)
        if f_ma_off and c_ma_off:
            df_off_f = df_off_f[
                df_off_f[c_ma_off]
                .astype(str)
                .str.lower()
                .str.contains(f_ma_off.lower(), na=False)
            ]
        if f_ten_off and c_ten_off:
            df_off_f = df_off_f[
                df_off_f[c_ten_off]
                .astype(str)
                .str.lower()
                .str.contains(f_ten_off.lower(), na=False)
            ]

        st.dataframe(df_off_f, use_container_width=True, height=450, hide_index=True)
        st.caption(f'Hiển thị: {len(df_off_f):,} / {len(df_combo_off):,} cửa hàng')

# ==================== TAB DSKH COMBO ON ====================
with tab_dskh_on:
    st.markdown(
        '<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">📋 DANH SÁCH KHÁCH HÀNG COMBO ON</h3>',
        unsafe_allow_html=True,
    )
    if df_combo_on.empty:
        st.warning('Chưa có dữ liệu Combo ON')
    else:
        c_nv_on = find_col(df_combo_on, ['Tên NV', 'SM name', 'Nhân viên'])
        c_thu_on = find_col(df_combo_on, ['Thứ', 'Frequency'])
        c_ma_on = find_col(df_combo_on, ['outlet_code', 'Outlet Code', 'Mã CH'])
        c_ten_on = find_col(df_combo_on, ['outlet_name', 'Outlet Name', 'Tên CH'])

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(
                '<p class="filter-label">👤 Tên NVBH</p>', unsafe_allow_html=True
            )
            on_nv_opts = (
                sorted(df_combo_on[c_nv_on].dropna().astype(str).unique().tolist())
                if c_nv_on
                else []
            )
            f_on_nv = st.multiselect(
                '', on_nv_opts, key='on_nv_filter', label_visibility='collapsed'
            )
        with c2:
            st.markdown(
                '<p class="filter-label">📅 Thứ</p>', unsafe_allow_html=True
            )
            thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
            f_thu_on = st.multiselect(
                '',
                thu_opts,
                key='on_thu_filter',
                label_visibility='collapsed',
            )
        with c3:
            st.markdown(
                '<p class="filter-label">🔑 Mã Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ma_on = st.text_input(
                '',
                key='on_ma_filter',
                placeholder='Nhập mã KH...',
                label_visibility='collapsed',
            )
        with c4:
            st.markdown(
                '<p class="filter-label">🏷️ Tên Khách Hàng</p>',
                unsafe_allow_html=True,
            )
            f_ten_on = st.text_input(
                '',
                key='on_ten_filter',
                placeholder='Nhập tên KH...',
                label_visibility='collapsed',
            )

        df_on_f = df_combo_on.copy()
        if f_on_nv and c_nv_on:
            df_on_f = df_on_f[df_on_f[c_nv_on].astype(str).isin(f_on_nv)]
        df_on_f = filter_by_thu_multi(df_on_f, c_thu_on, f_thu_on)
        if f_ma_on and c_ma_on:
            df_on_f = df_on_f[
                df_on_f[c_ma_on]
                .astype(str)
                .str.lower()
                .str.contains(f_ma_on.lower(), na=False)
            ]
        if f_ten_on and c_ten_on:
            df_on_f = df_on_f[
                df_on_f[c_ten_on]
                .astype(str)
                .str.lower()
                .str.contains(f_ten_on.lower(), na=False)
            ]

        st.dataframe(df_on_f, use_container_width=True, height=450, hide_index=True)
        st.caption(f'Hiển thị: {len(df_on_f):,} / {len(df_combo_on):,} cửa hàng')
