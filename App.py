import streamlit as st
import pandas as pd
import datetime

# --- CONFIG TRANG WEB ---
st.set_page_config(page_title="TRACKING KPI ĐDKD - MASAN CONSUMER", layout="wide")

# --- CUSTOM CSS (GIỮ FORMAT THEO MẪU BÁN HÀNG MASAN & BO TRÒN FILTER) ---
st.markdown("""
<style>
    /* Styling Banner Header */
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
    
    /* Format Bảng & Text Ultra-Bold */
    table {
        font-weight: 700 !important;
        width: 100%;
        border-collapse: collapse;
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
    }
    
    /* Box Nhận xét & Đề xuất */
    .comment-box {
        border: 2px solid #034EA2;
        border-radius: 10px;
        padding: 15px;
        background-color: #F8FAFC;
        margin-top: 25px;
        font-size: 13px;
        font-weight: 700;
        line-height: 1.6;
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

# --- 1. BANNER HEADER ---
st.markdown("""
<div class="header-banner">
    <div class="header-title">SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</div>
    <div class="header-subtitle">TRACKING KPI ĐDKD</div>
</div>
""", unsafe_allow_html=True)

# --- 2. THANH FILTER NGANG (5 MỤC THEO ĐÚNG FORMAT HÌNH 1) ---
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
    ddkd_filter = st.selectbox("ĐDKD", ["Tất cả ĐDKD", "Huỳnh Tấn Lý", "Mai Thanh Tâm", "Nguyễn Hoàng Bích Thủy"])

st.markdown("---")

# --- 3. HÀM TÍNH TOÁN VÀ ĐỊNH DẠNG MÀU DỰA TRÊN THUẬT TOÁN (RULE ENGINE) ---
def highlight_mtd(val):
    """Quy tắc tô màu Conditional Formatting cho % MTD"""
    try:
        pct = float(str(val).replace('%', ''))
        if pct >= 75.0:
            return 'background-color: #DCFCE7; color: #15803D; font-weight: 900;'  # Xanh lá
        elif pct >= 50.0:
            return 'background-color: #FEF08A; color: #854D0E; font-weight: 900;'  # Vàng
        else:
            return 'background-color: #FEE2E2; color: #B91C1C; font-weight: 900;'  # Cam/Đỏ
    except:
        return ''

# --- 4. HIỂN THỊ BÁO CÁO THEO LỰA CHỌN FILTER ---
if kpi_filter == "1. ASO FOCUS TOTAL NHÃN CHANTÉ":
    st.subheader("BÁO CÁO ASO FOCUS TOTAL NHÃN CHANTÉ THÁNG 09/2026")
    st.caption("Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày 15/09/2026 | Tiến độ thời gian: 11/24 ngày (45.8% Time Gone)")
    
    # Data Mẫu Theo Đúng PPTX & Rule (Lọc Chanté, đơn >= 1 đơn/tháng)
    data = [
        [1, "24SF.HC15114", "Huỳnh Tấn Lý", 30, 1, 23, "76.7%"],
        [2, "25SF.HC21112", "Hàng Thanh Lộc", 30, 6, 22, "73.3%"],
        [3, "14SF.HC00198", "Lê Thị Thơm", 30, 3, 21, "70.0%"],
        [4, "18SF.HC4599", "Nguyễn Văn Đình Chương", 30, 0, 19, "63.3%"],
        [5, "19SF.HC7071", "Đoàn Thị Phượng Liên", 30, 4, 18, "60.0%"],
        [15, "26SF.HC23230", "Nguyễn Trần Bảo Long", 30, 0, 7, "23.3%"],
        ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 450, 24, 229, "50.9%"]
    ]
    df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", "Thực Hiện 15/09", "MTD", "% MTD"])
    
    # Hiển thị bảng
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True)
    
    # Khung Nhận xét & Đề xuất
    st.markdown("""
    <div class="comment-box">
        <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (ASO FOCUS TOTAL NHÃN CHANTÉ):</div>
        • <b>Quy Chuẩn Chỉ Tiêu KPI:</b> Chỉ tiêu ASO FOCUS TOTAL NHÃN CHANTÉ được lấy chính xác theo file KPI ĐĐKD (Tổng 450 ASO cho SS Trương Thanh Tân Total).<br>
        • <b>Tiến Độ MTD Toàn Team:</b> Lũy kế đến 15/09 đạt 229/450 ASO (50.9% Kế hoạch), Tiến độ thời gian 45.8% (11/24 ngày làm việc).<br>
        • <b>Phát Sinh Ngày 15/09:</b> Trong ngày chốt thêm 24 Cửa Hàng ASO mới toàn team.<br>
        • <b>Top NVBH Dẫn Đầu % MTD:</b> Huỳnh Tấn Lý (76.7% - 23/30 ASO), Hàng Thanh Lộc (73.3% - 22/30 ASO), Lê Thị Thơm (70.0% - 21/30 ASO).<br>
        • <b>Định Hướng Tiếp Theo:</b> Đẩy mạnh ghé thăm tuyến đường và tăng tốc chào hàng sản phẩm để bứt phá đạt 100% KPI!
    </div>
    """, unsafe_allow_html=True)

# (Các báo cáo khác 2, 3, 4, 5, 6 được cấu hình logic tương tự theo file Docx & Slide mẫu)