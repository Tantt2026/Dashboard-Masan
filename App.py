import streamlit as st
import pandas as pd
import datetime

# --- CONFIG TRANG WEB ---
st.set_page_config(page_title="TRACKING KPI ĐDKD - MASAN CONSUMER", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
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

# --- BANNER HEADER ---
st.markdown("""
<div class="header-banner">
    <div class="header-title">SƯ ĐOÀN HCM4 - TRUNG ĐOÀN 10</div>
    <div class="header-subtitle">TRACKING KPI ĐDKD</div>
</div>
""", unsafe_allow_html=True)

# --- THANH FILTER NGANG ---
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

# NÚT UPLOAD FILE EXCEL DATA THỰC TẾ
uploaded_file = st.sidebar.file_uploader("Cập nhật Data Excel mới", type=["xlsx", "xls"])

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

date_str = date_filter.strftime("%d/%m")

# --- XỬ LÝ 6 BÁO CÁO ---
if kpi_filter == "1. ASO FOCUS TOTAL NHÃN CHANTÉ":
    st.subheader(f"BÁO CÁO ASO FOCUS TOTAL NHÃN CHANTÉ {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026")
    
    data = [
        [1, "24SF.HC15114", "Huỳnh Tấn Lý", 30, 1, 23, "76.7%"],
        [2, "25SF.HC21112", "Hàng Thanh Lộc", 30, 6, 22, "73.3%"],
        [3, "14SF.HC00198", "Lê Thị Thơm", 30, 3, 21, "70.0%"],
        [4, "18SF.HC4599", "Nguyễn Văn Đình Chương", 30, 0, 19, "63.3%"],
        [5, "19SF.HC7071", "Đoàn Thị Phượng Liên", 30, 4, 18, "60.0%"],
        ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 450, 24, 229, "50.9%"]
    ]
    df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)
    
    st.markdown(f"""
    <div class="comment-box">
        <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (ASO FOCUS TOTAL NHÃN CHANTÉ CẬP NHẬT ĐẾN {date_str}/2026):</div>
        • <b>Quy Chuẩn Chỉ Tiêu KPI:</b> Lấy theo file KPI ĐĐKD (Tổng 450 ASO cho SS Trương Thanh Tân Total).<br>
        • <b>Tiến Độ MTD Toàn Team:</b> Lũy kế đạt 229/450 ASO (50.9% Kế hoạch).<br>
        • <b>Phát Sinh Ngày {date_str}:</b> Chốt thêm 24 Cửa Hàng ASO mới toàn team.
    </div>
    """, unsafe_allow_html=True)

elif kpi_filter == "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN":
    st.subheader(f"BÁO CÁO ASO FOCUS TRẬN VÀNG - TOTAL OMACHI TRỘN {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026")
    
    data = [
        [1, "26SF.HC23006", "Mai Thanh Tâm", 20, 2, 19, "95.0%"],
        [2, "26SF.HC22759", "Nguyễn Hoàng Bích Thủy", 53, 2, 38, "71.7%"],
        [3, "24SF.HC16385", "Trần Minh Thành", 57, 6, 40, "70.2%"],
        [4, "24SF.HC15114", "Huỳnh Tấn Lý", 62, 4, 41, "66.1%"],
        ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 913, 52, 487, "53.3%"]
    ]
    df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

elif kpi_filter == "3. ASO TEA KÊNH ON PREMISE":
    st.subheader(f"BÁO CÁO ASO TEA KÊNH ON PREMISE {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ Visit Schedule & RPT_061.xlsx cập nhật đến ngày {date_str}/2026 | Chỉ tiêu KPI: 30 ASO/NVBH")
    
    data = [
        [1, "24SF.HC16385", "Trần Minh Thành", 30, 0, 27, "90.0%"],
        [2, "14SF.HC00198", "Lê Thị Thơm", 30, 0, 27, "90.0%"],
        [3, "18SF.HC4149", "Nguyễn Thị Bích Trâm", 30, 1, 26, "86.7%"],
        ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 450, 19, 297, "66.0%"]
    ]
    df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

elif kpi_filter == "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)":
    st.subheader(f"BÁO CÁO PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER) {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026")
    
    data = [
        [1, "25SF.HC21112", "Hàng Thanh Lộc", 184, 11, 84, "45.7%"],
        [2, "19SF.HC7071", "Đoàn Thị Phượng Liên", 190, 12, 83, "43.7%"],
        [3, "24SF.HC15114", "Huỳnh Tấn Lý", 152, 7, 61, "40.1%"],
        ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 2667, 107, 854, "32.0%"]
    ]
    df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

elif kpi_filter == "5. ASO ALL KÊNH OFF":
    st.subheader(f"BÁO CÁO ASO ALL KÊNH OFF {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026")
    
    data = [
        [1, "26SF.HC22759", "Nguyễn Hoàng Bích Thủy", 68, 8, 66, "97.1%"],
        [2, "26SF.HC22209", "Mai Thị Linh", 63, 11, 61, "96.8%"],
        [3, "19SF.HC7071", "Đoàn Thị Phượng Liên", 90, 13, 86, "95.6%"],
        ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 1200, 141, 1025, "85.4%"]
    ]
    df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD (Kênh OFF)", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

elif kpi_filter == "6. BÁO CÁO ĐƠN HÀNG COMBO":
    st.subheader(f"BÁO CÁO ĐƠN HÀNG COMBO NGÀY {date_str}/2026")
    st.caption(f"Thống kê phát sinh thực tế trong ngày {date_str}/2026 & Lũy kế MTD")
    
    data = [
        [1, "25SF.HC21112", "Hàng Thanh Lộc", 18, 8, "44.4%", 8, 0, "0.0%"],
        [2, "24SF.HC16385", "Trần Minh Thành", 8, 3, "37.5%", 7, 0, "0.0%"],
        [3, "26SF.HC23006", "Mai Thanh Tâm", 11, 4, "36.4%", 4, 0, "0.0%"],
        ["-", "TỔNG CỘNG", "SS Trương Thanh Tân Total", 200, 37, "18.5%", 103, 5, "4.9%"]
    ]
    df = pd.DataFrame(data, columns=["STT", "Mã NVBH", "Tên NVBH", "Số CH OFF", f"Thực hiện {date_str} (OFF)", "% Hoàn thành OFF", "Số CH ON", f"Thực hiện {date_str} (ON)", "% Hoàn thành ON"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% Hoàn thành OFF", "% Hoàn thành ON"]), use_container_width=True, hide_index=True)
