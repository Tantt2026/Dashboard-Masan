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


def render_metric_card(label, value, sub_val=None):
  st.markdown(
      f"""
    <div style="background: #ffffff; border: 1px solid #bee3f8; border-radius: 6px; padding: 6px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 8px;">
        <div style="color: #2b6cb0; font-weight: 700; font-size: 0.85rem; margin-bottom: 2px;">{label}</div>
        <div style="color: #c53030; font-weight: 800; font-size: 1.25rem;">{value}</div>
    </div>
    """,
      unsafe_allow_html=True,
  )


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
  except:
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
  except:
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
  df_out[target_sales_col] = df_out['Total_Sales'].fillna(0.0) / 1000000.0
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

  df_closed = (
      df_clean[df_clean[status_col] == 'Đã đóng'] if status_col else df_clean
  )
  agg_cat2 = (
      df_closed.groupby(['Mã CH_str', 'Mapped_Cat'])[val_col]
      .sum()
      .reset_index()
  )
  agg_cat2.columns = ['Outlet_key', 'Cat_Key', 'Val2']

  df_out = df_cat.copy()
  c_code = find_col(df_out, ['Outlet Code', 'Outlet_code', 'Mã CH'])
  c_cat = find_col(df_out, ['Danh sách full cat', 'Category', 'Cat'])
  col_val1 = find_col(
      df_out,
      ['Doanh số thực đạt của CAT', 'Doanh số thực đạt CAT'],
  )
  col_val2 = find_col(
      df_out,
      [
          'Doanh số thực đạt của CAT(Not Cancel/Pending)',
          'Doanh số thực đạt của CAT (Not Cancel/Pending)',
      ],
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
  df_out = df_out.merge(
      agg_cat2,
      left_on=['_outlet_key', '_cat_key'],
      right_on=['Outlet_key', 'Cat_Key'],
      how='left',
  )
  if 'Outlet_key' in df_out.columns:
    df_out = df_out.drop(columns=['Outlet_key', 'Cat_Key'])

  if col_val1:
    df_out[col_val1] = df_out['Val1'].fillna(0.0) / 1000000.0
  if col_val2:
    df_out[col_val2] = df_out['Val2'].fillna(0.0) / 1000000.0

  drop_cols = [
      c
      for c in ['_outlet_key', '_cat_key', 'Val1', 'Val2']
      if c in df_out.columns
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
  brands_list = df_brand[brand_col_name].dropna().unique().tolist()

  def match_brand(sku_str):
    if pd.isna(sku_str):
      return 'Khác'
    s = str(sku_str).lower()
    sorted_brands = sorted(brands_list, key=len, reverse=True)
    for b in sorted_brands:
      b_clean = str(b).lower()
      if b_clean in s:
        return b
      if b_clean == 'vinacafe' and (
          'vinacafé' in s or 'vinacafe' in s or 'phil' in s
      ):
        return b
      if b_clean == 'wake up 247' and (
          'wake up 247' in s or 'wake-up 247' in s
      ):
        return b
      if b_clean == 'wake up' and ('wake up' in s and '247' not in s):
        return b
      if b_clean == 'heo cao bồi' and ('cao bồi' in s or 'cao boi' in s):
        return b
      if b_clean == 'bupnon tea365' and (
          'búp non' in s or 'tea 365' in s or 'tea365' in s
      ):
        return b
      if b_clean == 'sư tử trắng' and ('sư tử' in s or 'su tu' in s):
        return b
      if b_clean == 'tam thái tử' and ('tam thái tử' in s or 'tam thai tu' in s):
        return b
      if b_clean == 'vivant' and (
          'vivant' in s or 'vĩnh hảo' in s or 'vinh hao' in s
      ):
        return b
    return 'Khác'

  df_clean = df_rpt.copy()
  sku_col1 = find_col(df_clean, ['Group std', 'Tên sản phẩm']) or 'Tên sản phẩm'
  sku_col2 = find_col(df_clean, ['Tên sản phẩm']) or 'Tên sản phẩm'
  df_clean['Search_Str'] = (
      df_clean[sku_col1].astype(str) + ' ' + df_clean[sku_col2].astype(str)
  )
  val_col = find_col(df_clean, ['Tổng tiền', 'Giá trị sau CK']) or 'Tổng tiền'
  status_col = find_col(df_clean, ['Tình trạng đơn hàng'])

  df_clean['Mapped_Brand'] = df_clean['Search_Str'].apply(match_brand)
  df_clean['Mã CH_str'] = df_clean['Mã CH'].astype(str).str.strip()

  df_valid = (
      df_clean[df_clean[status_col] != 'Đã hủy'] if status_col else df_clean
  )
  agg_b1 = (
      df_valid.groupby(['Mã CH_str', 'Mapped_Brand'])[val_col]
      .sum()
      .reset_index()
  )
  agg_b1.columns = ['Outlet_key', 'Brand_Key', 'Val1']

  df_closed = (
      df_clean[df_clean[status_col] == 'Đã đóng'] if status_col else df_clean
  )
  agg_b2 = (
      df_closed.groupby(['Mã CH_str', 'Mapped_Brand'])[val_col]
      .sum()
      .reset_index()
  )
  agg_b2.columns = ['Outlet_key', 'Brand_Key', 'Val2']

  df_out = df_brand.copy()
  c_code = find_col(df_out, ['Outlet Code', 'Outlet_code', 'Mã CH'])
  c_brand = brand_col_name
  col_val1 = find_col(df_out, ['Doanh số thực đạt của brand'])
  col_val2 = find_col(df_out, ['Doanh số thực đạt của brand (Not Cancel/Pending)'])

  if not c_code:
    return df_out
  df_out['_outlet_key'] = df_out[c_code].astype(str).str.strip()
  df_out['_brand_key'] = df_out[c_brand].astype(str).str.strip()

  df_out = df_out.merge(
      agg_b1,
      left_on=['_outlet_key', '_brand_key'],
      right_on=['Outlet_key', 'Brand_Key'],
      how='left',
  )
  if 'Outlet_key' in df_out.columns:
    df_out = df_out.drop(columns=['Outlet_key', 'Brand_Key'])
  df_out = df_out.merge(
      agg_b2,
      left_on=['_outlet_key', '_brand_key'],
      right_on=['Outlet_key', 'Brand_Key'],
      how='left',
  )
  if 'Outlet_key' in df_out.columns:
    df_out = df_out.drop(columns=['Outlet_key', 'Brand_Key'])

  if col_val1:
    df_out[col_val1] = df_out['Val1'].fillna(0.0) / 1000000.0
  if col_val2:
    df_out[col_val2] = df_out['Val2'].fillna(0.0) / 1000000.0

  drop_cols = [
      c
      for c in ['_outlet_key', '_brand_key', 'Val1', 'Val2']
      if c in df_out.columns
  ]
  return df_out.drop(columns=drop_cols)


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
    tgt = turnover_targets.get(sm, 0.0) / 1000000.0
    m = float(mtd_sales.get(sm, 0.0)) / 1000000.0
    t_val = float(today_sales.get(sm, 0.0)) / 1000000.0
    pct = round(m / tgt * 100, 1) if tgt else 0.0
    results.append({
        'Mã NVBH': sm,
        'Tên NVBH': sm_names.get(sm, ''),
        'Chỉ Tiêu Doanh Số': round(tgt, 2),
        'Thực Hiện Ngày': round(t_val, 2),
        'Doanh Số MTD': round(m, 2),
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
      'Chỉ Tiêu Doanh Số': round(team_tgt, 2),
      'Thực Hiện Ngày': round(total_today, 2),
      'Doanh Số MTD': round(total_mtd, 2),
      '% MTD': f'{total_pct}%',
  }])
  return (
      pd.concat([df_out, total_row], ignore_index=True),
      team_tgt,
      '8. BÁO CÁO DOANH SỐ TURNOVER',
  )


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
      c_nv_mcp = find_col(mcp_df, ['SM Code', 'Mã NVBH', 'SM code', 'Tên NVBH'])
      c_l1 = find_col(mcp_df, ['L1', 'Channel'])
      c_ma = find_col(mcp_df, ['Outlet_code', 'Outlet Code', 'Mã CH'])
      if c_nv_mcp and c_l1 and c_ma:
        on_mcp = mcp_df[
            mcp_df[c_l1].astype(str).str.contains('On', case=False, na=False)
        ].copy()
        on_targets = (
            on_mcp.groupby(c_nv_mcp)[c_ma].nunique().to_dict()
        )
    key, title = 'PC_ON', '6. ASO ACTIVE KÊNH ON'
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
    if report_type == 'PC_ON':
      tgt = int(on_targets.get(sm, 0))
    else:
      tgt = targets.get(sm, {}).get(key, 0)
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


def render_html_table(df):
  html = [
      '<div class="custom-kpi-table-container"><table'
      ' class="custom-kpi-table">'
  ]
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
      style = (
          'background-color: #fff5f5; color: #c53030 !important; font-weight:'
          ' 900 !important;'
          if is_total
          else ''
      )
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
    tot_mtd = (
        float(df_r.iloc[-1]['Doanh Số MTD'])
        if not df_r.empty
        else 0
    )
    tot_day = (
        float(df_r.iloc[-1]['Thực Hiện Ngày'])
        if not df_r.empty
        else 0
    )
    tot_pct = round(tot_mtd / team_tgt * 100, 1) if team_tgt else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
      render_metric_card('🎯 Target', f'{team_tgt:,.1f}')
    with c2:
      render_metric_card('📈 MTD', f'{tot_mtd:,.1f}')
    with c3:
      render_metric_card('📊 % MTD', f'{tot_pct}%')
    with c4:
      render_metric_card('📅 Ngày', f'+{tot_day:,.1f}')

    st.markdown(
        f'<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">{title} - Tháng 09/2026</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(render_html_table(df_r), unsafe_allow_html=True)
  elif selected_kpi in ['CHANTE', 'OMACHI', 'ASO_TEA', 'PC_BT', 'ASO_ALL', 'PC_ON']:
    df_r, team_tgt, title = build_report(
        df, report_date, targets, selected_kpi, filter_nv, mcp
    )
    tot_mtd = int(df_r.iloc[-1]['MTD']) if not df_r.empty else 0
    tot_day = (
        int(df_r.iloc[-1]['Thực Hiện Ngày'])
        if not df_r.empty
        else 0
    )
    tot_pct = round(tot_mtd / team_tgt * 100, 1) if team_tgt else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
      render_metric_card('🎯 Target', f'{team_tgt:,}')
    with c2:
      render_metric_card('📈 MTD', f'{tot_mtd:,}')
    with c3:
      render_metric_card('📊 % MTD', f'{tot_pct}%')
    with c4:
      render_metric_card('📅 Ngày', f'+{tot_day:,}')

    st.markdown(
        f'<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">{title} - Tháng 09/2026</h3>',
        unsafe_allow_html=True,
    )
    st.markdown(render_html_table(df_r), unsafe_allow_html=True)
  else:
    st.info('Vui lòng chọn xem các tab chi tiết hoặc báo cáo tổng hợp tương ứng.')

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
    col_ma = find_col(mcp, ['Outlet_code', 'Outlet Code', 'Mã CH'])
    col_ten = find_col(mcp, ['Outlet_name', 'Outlet Name', 'Tên CH'])
    col_thu = find_col(mcp, ['Thứ', 'Frequency', 'Tần suất'])
    col_vip = find_col(mcp, ['VIP MCH', 'VIP_MCH'])
    col_ds = find_col(mcp, ['Doanh Số MTD', 'Doanh số MTD'])

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD)</p>',
          unsafe_allow_html=True,
      )
      nv_opts = (
          sorted(mcp[col_nv].dropna().astype(str).unique().tolist())
          if col_nv
          else []
      )
      f_nv = st.multiselect(
          '', nv_opts, key='mcp_nv_input', label_visibility='collapsed'
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ</p>', unsafe_allow_html=True
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      f_thu = st.multiselect(
          '', thu_opts, key='mcp_thu_input', label_visibility='collapsed'
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ma_text = st.text_input(
          '',
          key='mcp_ma_txt',
          placeholder='Nhập mã CH...',
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏢 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ten_text = st.text_input(
          '',
          key='mcp_ten_txt',
          placeholder='Nhập tên CH...',
          label_visibility='collapsed',
      )

    c5, c6 = st.columns(2)
    with c5:
      st.markdown(
          '<p class="filter-label">⭐ Lọc VIP MCH</p>', unsafe_allow_html=True
      )
      vip_opts = (
          sorted(mcp[col_vip].dropna().astype(str).unique().tolist())
          if col_vip and col_vip in mcp.columns
          else []
      )
      f_vip_val = st.multiselect(
          '', vip_opts, key='mcp_vip_input', label_visibility='collapsed'
      )
    with c6:
      st.markdown(
          '<p class="filter-label">💰 Lọc Doanh Số MTD Thực Tế</p>',
          unsafe_allow_html=True,
      )
      ds_cond = st.selectbox(
          '',
          ['Tất cả', '> 0', '= 0'],
          key='mcp_ds_cond',
          label_visibility='collapsed',
      )

    df_f = mcp.copy()
    if f_nv and col_nv:
      df_f = df_f[df_f[col_nv].astype(str).isin(f_nv)]
    df_f = filter_by_thu_multi(df_f, col_thu, f_thu)
    if f_ma_text and col_ma:
      df_f = df_f[
          df_f[col_ma].astype(str).str.contains(f_ma_text, case=False, na=False)
      ]
    if f_ten_text and col_ten:
      df_f = df_f[
          df_f[col_ten]
          .astype(str)
          .str.contains(f_ten_text, case=False, na=False)
      ]
    if f_vip_val and col_vip:
      df_f = df_f[df_f[col_vip].astype(str).isin(f_vip_val)]
    if ds_cond == '> 0' and col_ds:
      df_f = df_f[pd.to_numeric(df_f[col_ds], errors='coerce').fillna(0) > 0]
    elif ds_cond == '= 0' and col_ds:
      df_f = df_f[pd.to_numeric(df_f[col_ds], errors='coerce').fillna(0) == 0]

    all_cols = list(df_f.columns)
    with st.expander('👁️ Chọn cột hiển thị (MCP)'):
      selected_mcp_cols = st.multiselect(
          'Bỏ chọn để ẩn cột:', all_cols, default=all_cols
      )
    if selected_mcp_cols:
      df_f = df_f[selected_mcp_cols]

    st.dataframe(df_f, use_container_width=True, height=450, hide_index=True)
    st.caption(f'Hiển thị: {len(df_f):,} / {len(mcp):,} cửa hàng')

# ==================== TAB CAT ====================
with tab_cat:
  st.markdown(
      '<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">📦 TRACKING MBS - THEO NGÀNH HÀNG (CATEGORY)</h3>',
      unsafe_allow_html=True,
  )
  if df_cat.empty:
    st.error('❌ Không tìm thấy Data_Cat.xlsx')
  else:
    c_cat_nv = find_col(
        df_cat, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên']
    )
    c_cat_ma = find_col(df_cat, ['Outlet Code', 'Outlet_code', 'Mã CH'])
    c_cat_ten = find_col(df_cat, ['Outlet Name', 'Outlet_name', 'Tên CH'])
    c_cat_thu = find_col(df_cat, ['Thứ', 'Frequency', 'Tần suất'])

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD)</p>',
          unsafe_allow_html=True,
      )
      nv_cat_opts = (
          sorted(df_cat[c_cat_nv].dropna().astype(str).unique().tolist())
          if c_cat_nv
          else []
      )
      f_cat_nv = st.multiselect(
          '', nv_cat_opts, key='cat_nv_input', label_visibility='collapsed'
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ</p>', unsafe_allow_html=True
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      f_cat_thu = st.multiselect(
          '', thu_opts, key='cat_thu_input', label_visibility='collapsed'
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_cat_ma = st.text_input(
          '',
          key='cat_ma_txt',
          placeholder='Nhập mã CH...',
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏢 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_cat_ten = st.text_input(
          '',
          key='cat_ten_txt',
          placeholder='Nhập tên CH...',
          label_visibility='collapsed',
      )

    df_cat_f = df_cat.copy()
    if f_cat_nv and c_cat_nv:
      df_cat_f = df_cat_f[df_cat_f[c_cat_nv].astype(str).isin(f_cat_nv)]
    df_cat_f = filter_by_thu_multi(df_cat_f, c_cat_thu, f_cat_thu)
    if f_cat_ma and c_cat_ma:
      df_cat_f = df_cat_f[
          df_cat_f[c_cat_ma]
          .astype(str)
          .str.contains(f_cat_ma, case=False, na=False)
      ]
    if f_cat_ten and c_cat_ten:
      df_cat_f = df_cat_f[
          df_cat_f[c_cat_ten]
          .astype(str)
          .str.contains(f_cat_ten, case=False, na=False)
      ]

    all_cat_cols = list(df_cat_f.columns)
    with st.expander('👁️ Chọn cột hiển thị (Category)'):
      selected_cat_cols = st.multiselect(
          'Bỏ chọn để ẩn cột:', all_cat_cols, default=all_cat_cols
      )
    if selected_cat_cols:
      df_cat_f = df_cat_f[selected_cat_cols]

    st.dataframe(
        df_cat_f, use_container_width=True, height=450, hide_index=True
    )
    st.caption(f'Hiển thị: {len(df_cat_f):,} / {len(df_cat):,} dòng dữ liệu')

# ==================== TAB BRAND ====================
with tab_brand:
  st.markdown(
      '<h3 style="color: #034ea2; font-weight: 800; font-size: 15px;">🏷️ TRACKING MBS - THEO THƯƠNG HIỆU (BRAND)</h3>',
      unsafe_allow_html=True,
  )
  if df_brand.empty:
    st.error('❌ Không tìm thấy Data_Brand.xlsx')
  else:
    c_brand_nv = find_col(
        df_brand, ['SM Name', 'SM name', 'Tên NVBH', 'Nhân viên']
    )
    c_brand_ma = find_col(df_brand, ['Outlet Code', 'Outlet_code', 'Mã CH'])
    c_brand_ten = find_col(df_brand, ['Outlet Name', 'Outlet_name', 'Tên CH'])
    c_brand_thu = find_col(df_brand, ['Thứ', 'Frequency', 'Tần suất'])

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD)</p>',
          unsafe_allow_html=True,
      )
      nv_brand_opts = (
          sorted(df_brand[c_brand_nv].dropna().astype(str).unique().tolist())
          if c_brand_nv
          else []
      )
      f_brand_nv = st.multiselect(
          '', nv_brand_opts, key='brand_nv_input', label_visibility='collapsed'
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ</p>', unsafe_allow_html=True
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      f_brand_thu = st.multiselect(
          '', thu_opts, key='brand_thu_input', label_visibility='collapsed'
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_brand_ma = st.text_input(
          '',
          key='brand_ma_txt',
          placeholder='Nhập mã CH...',
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏢 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_brand_ten = st.text_input(
          '',
          key='brand_ten_txt',
          placeholder='Nhập tên CH...',
          label_visibility='collapsed',
      )

    df_brand_f = df_brand.copy()
    if f_brand_nv and c_brand_nv:
      df_brand_f = df_brand_f[df_brand_f[c_brand_nv].astype(str).isin(f_brand_nv)]
    df_brand_f = filter_by_thu_multi(df_brand_f, c_brand_thu, f_brand_thu)
    if f_brand_ma and c_brand_ma:
      df_brand_f = df_brand_f[
          df_brand_f[c_brand_ma]
          .astype(str)
          .str.contains(f_brand_ma, case=False, na=False)
      ]
    if f_brand_ten and c_brand_ten:
      df_brand_f = df_brand_f[
          df_brand_f[c_brand_ten]
          .astype(str)
          .str.contains(f_brand_ten, case=False, na=False)
      ]

    all_brand_cols = list(df_brand_f.columns)
    with st.expander('👁️ Chọn cột hiển thị (Brand)'):
      selected_brand_cols = st.multiselect(
          'Bỏ chọn để ẩn cột:', all_brand_cols, default=all_brand_cols
      )
    if selected_brand_cols:
      df_brand_f = df_brand_f[selected_brand_cols]

    st.dataframe(
        df_brand_f, use_container_width=True, height=450, hide_index=True
    )
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
    c_ma_off = find_col(df_combo_off, ['outlet_code', 'Outlet Code', 'Mã CH'])
    c_ten_off = find_col(df_combo_off, ['outlet_name', 'Outlet Name', 'Tên CH'])
    c_thu_off = find_col(df_combo_off, ['Thứ', 'Frequency'])

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD)</p>',
          unsafe_allow_html=True,
      )
      off_nv_opts = (
          sorted(df_combo_off[c_nv_off].dropna().astype(str).unique().tolist())
          if c_nv_off
          else []
      )
      f_off_nv = st.multiselect(
          '', off_nv_opts, key='off_nv_input', label_visibility='collapsed'
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ</p>', unsafe_allow_html=True
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      f_thu_off = st.multiselect(
          '', thu_opts, key='off_thu_input', label_visibility='collapsed'
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ma_off = st.text_input(
          '',
          key='off_ma_txt',
          placeholder='Nhập mã CH...',
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏢 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ten_off = st.text_input(
          '',
          key='off_ten_txt',
          placeholder='Nhập tên CH...',
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
          .str.contains(f_ma_off, case=False, na=False)
      ]
    if f_ten_off and c_ten_off:
      df_off_f = df_off_f[
          df_off_f[c_ten_off]
          .astype(str)
          .str.contains(f_ten_off, case=False, na=False)
      ]

    all_cols_off = list(df_off_f.columns)
    with st.expander('👁️ Chọn cột hiển thị (Combo OFF)'):
      selected_cols_off = st.multiselect(
          'Bỏ chọn để ẩn cột:', all_cols_off, default=all_cols_off
      )
    if selected_cols_off:
      df_off_f = df_off_f[selected_cols_off]

    st.dataframe(
        df_off_f, use_container_width=True, height=450, hide_index=True
    )
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
    c_ma_on = find_col(df_combo_on, ['outlet_code', 'Outlet Code', 'Mã CH'])
    c_ten_on = find_col(df_combo_on, ['outlet_name', 'Outlet Name', 'Tên CH'])
    c_thu_on = find_col(df_combo_on, ['Thứ', 'Frequency'])

    c1, c2 = st.columns(2)
    with c1:
      st.markdown(
          '<p class="filter-label">👤 Lọc Nhân Viên (ĐDKD)</p>',
          unsafe_allow_html=True,
      )
      on_nv_opts = (
          sorted(df_combo_on[c_nv_on].dropna().astype(str).unique().tolist())
          if c_nv_on
          else []
      )
      f_on_nv = st.multiselect(
          '', on_nv_opts, key='on_nv_input', label_visibility='collapsed'
      )
    with c2:
      st.markdown(
          '<p class="filter-label">📅 Lọc Theo Thứ</p>', unsafe_allow_html=True
      )
      thu_opts = ['2', '3', '4', '5', '6', '7', '25', '36', '47']
      f_thu_on = st.multiselect(
          '', thu_opts, key='on_thu_input', label_visibility='collapsed'
      )

    c3, c4 = st.columns(2)
    with c3:
      st.markdown(
          '<p class="filter-label">🆔 Lọc Mã Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ma_on = st.text_input(
          '',
          key='on_ma_txt',
          placeholder='Nhập mã CH...',
          label_visibility='collapsed',
      )
    with c4:
      st.markdown(
          '<p class="filter-label">🏢 Lọc Tên Khách Hàng</p>',
          unsafe_allow_html=True,
      )
      f_ten_on = st.text_input(
          '',
          key='on_ten_txt',
          placeholder='Nhập tên CH...',
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
          .str.contains(f_ma_on, case=False, na=False)
      ]
    if f_ten_on and c_ten_on:
      df_on_f = df_on_f[
          df_on_f[c_ten_on]
          .astype(str)
          .str.contains(f_ten_on, case=False, na=False)
      ]

    all_cols_on = list(df_on_f.columns)
    with st.expander('👁️ Chọn cột hiển thị (Combo ON)'):
      selected_cols_on = st.multiselect(
          'Bỏ chọn để ẩn cột:', all_cols_on, default=all_cols_on
      )
    if selected_cols_on:
      df_on_f = df_on_f[selected_cols_on]

    st.dataframe(df_on_f, use_container_width=True, height=450, hide_index=True)
    st.caption(f'Hiển thị: {len(df_on_f):,} / {len(df_combo_on):,} cửa hàng')
