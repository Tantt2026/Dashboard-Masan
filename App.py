import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="TRACKING KPI ĐDKD - SS Trương Thanh Tân",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMultiSelect div[data-baseweb="select"] {
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.title("📊 TRACKING KPI ĐDKD - SS Trương Thanh Tân")
st.markdown("---")

# ====================== FILTER MAPPING LOGIC ======================
# Mapping dictionary for filter values requested by user:
# Thứ 2 -> ['2', '25']
# Thứ 3 -> ['3', '36']
# Thứ 4 -> ['4', '47']
# Thứ 5 -> ['5', '25']
# Thứ 6 -> ['6', '36']
# Thứ 7 -> ['7', '47']

day_mapping = {
    '2': ['2', '25'], 'Thứ 2': ['2', '25'],
    '3': ['3', '36'], 'Thứ 3': ['3', '36'],
    '4': ['4', '47'], 'Thứ 4': ['4', '47'],
    '5': ['5', '25'], 'Thứ 5': ['5', '25'],
    '6': ['6', '36'], 'Thứ 6': ['6', '36'],
    '7': ['7', '47'], 'Thứ 7': ['7', '47']
}

# Sidebar or Main Filter Section
st.sidebar.header("⚙️ Tùy Chọn Bộ Lọc")

# Multiselect input for days
all_filter_options = ['2', '3', '4', '5', '6', '7', '25', '36', '47', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7']
selected_days = st.multiselect(
    "📅 Lọc Theo Thứ (Chọn nhiều)",
    options=all_filter_options,
    default=['2', '25']
)

# Resolve actual mapped values
resolved_values = set()
for day in selected_days:
    if day in day_mapping:
        resolved_values.update(day_mapping[day])
    else:
        resolved_values.add(day)

st.sidebar.markdown("---")
st.sidebar.info(f"Các giá trị được map thực tế: **{list(resolved_values)}**")

# ====================== MAIN CONTENT AREA ======================
st.subheader("📋 Bảng Dữ Liệu Tracking KPI")

# Mock data frame representing KPI data for demonstration
np.random.seed(42)
mock_data = pd.DataFrame({
    'Mã ĐDKD': [f'NV0{i}' for i in range(1, 11)],
    'Tên ĐDKD': ['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Phạm Thị D', 'Hoàng Văn E', 'Đỗ Thị F', 'Bùi Văn G', 'Ngô Thị H', 'Dương Văn I', 'Vũ Thị K'],
    'Thứ/Route': np.random.choice(['2', '3', '4', '5', '6', '7', '25', '36', '47'], 10),
    'KPI Doanh Thu (VNĐ)': np.random.randint(50000000, 150000000, 10),
    'Thực Tế (VNĐ)': np.random.randint(40000000, 160000000, 10),
})

# Apply filtering based on resolved mapping values
if resolved_values:
    filtered_df = mock_data[mock_data['Thứ/Route'].isin(list(resolved_values))]
else:
    filtered_df = mock_data

# Display metrics & dataframe
col1, col2, col3 = st.columns(3)
col1.metric("Tổng Nhân Sự Lọc", len(filtered_df))
col2.metric("Tổng KPI", f"{filtered_df['KPI Doanh Thu (VNĐ)'].sum():,.0f} đ")
col3.metric("Tổng Thực Tế", f"{filtered_df['Thực Tế (VNĐ)'].sum():,.0f} đ")

st.markdown("---")
st.dataframe(filtered_df, use_container_width=True)
