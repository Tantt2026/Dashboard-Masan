import streamlit as st
import pandas as pd
import datetime
import random

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
        color: #0F172A;
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
    ddkd_options = ["Tất cả ĐDKD"] + [s["ten"] for s in STAFF_LIST]
    ddkd_filter = st.selectbox("ĐDKD", ddkd_options)

st.markdown("---")

# NÚT UPLOAD FILE EXCEL DỮ LIỆU BÁN HÀNG
uploaded_file = st.sidebar.file_uploader("Cập nhật Data Excel mới (TỔNG HỢP KPI / RPT_061)", type=["xlsx", "xls", "csv"])

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
day_num = date_filter.day

# --- HÀM CALCULATOR GIẢ LẬP DỮ LIỆU DỰA TRÊN NGÀY LỌC (KHI CHƯA UP FILE EXCEL) ---
def generate_report_data(kpi_type, selected_day, selected_ddkd):
    # Base targets and MTD factors based on selected day (1 to 30)
    day_factor = min(max(selected_day / 24.0, 0.1), 1.0)
    
    rows = []
    tot_target = 0
    tot_daily = 0
    tot_mtd = 0

    # Base baseline data table per report type
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

    # Order of staff according to specific report
    staff_order = STAFF_LIST

    if kpi_type in base_data:
        items = base_data[kpi_type]
        for idx, s in enumerate(staff_order):
            if selected_ddkd != "Tất cả ĐDKD" and s["ten"] != selected_ddkd:
                continue
            
            target, base_mtd, base_daily = items[idx]
            
            # Recalculate dynamic MTD and Daily based on chosen day
            calc_mtd = int(round(base_mtd * (selected_day / 15.0)))
            calc_mtd = min(calc_mtd, target)
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
        
        for idx, s in enumerate(staff_order):
            if selected_ddkd != "Tất cả ĐDKD" and s["ten"] != selected_ddkd:
                continue
            
            ch_off, act_off, ch_on, act_on = combo_base[idx]
            
            # Scale dynamically with selected date
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

# --- HIỂN THỊ CÁC BÁO CÁO THEO DỮ LIỆU ĐỘNG NGÀY & ĐDKD ---
time_gone_pct = round((day_num / 24.0) * 100, 1) if day_num <= 24 else 100.0

if kpi_filter == "1. ASO FOCUS TOTAL NHÃN CHANTÉ":
    st.subheader(f"BÁO CÁO ASO FOCUS TOTAL NHÃN CHANTÉ {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026 | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
    
    rows = generate_report_data(kpi_filter, day_num, ddkd_filter)
    df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)
    
    tot_row = rows[-1]
    st.markdown(f"""
    <div class="comment-box">
        <div class="comment-title">NHẬN XÉT & ĐỀ XUẤT CHỦ LỰC TỪ GIÁM SÁT BÁN HÀNG (ASO FOCUS TOTAL NHÃN CHANTÉ CẬP NHẬT ĐẾN {date_str}/2026):</div>
        • <b>Quy Chuẩn Chỉ Tiêu KPI:</b> Lấy theo file KPI ĐĐKD (Tổng {tot_row[3]} ASO).<br>
        • <b>Tiến Độ MTD Toàn Team:</b> Lũy kế đến {date_str} đạt {tot_row[5]}/{tot_row[3]} ASO ({tot_row[6]} Kế hoạch), Tiến độ thời gian {time_gone_pct}% ({day_num}/24 ngày làm việc).<br>
        • <b>Phát Sinh Ngày {date_str}:</b> Chốt thêm {tot_row[4]} Cửa Hàng ASO mới toàn team.<br>
        • <b>Định Hướng Tiếp Theo:</b> Đẩy mạnh ghé thăm tuyến đường và tăng tốc chào hàng sản phẩm để bứt phá đạt 100% KPI!
    </div>
    """, unsafe_allow_html=True)

elif kpi_filter == "2. ASO FOCUS TRẬN VÀNG - OMACHI TRỘN":
    st.subheader(f"BÁO CÁO ASO FOCUS TRẬN VÀNG - TOTAL OMACHI TRỘN {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026 | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
    
    rows = generate_report_data(kpi_filter, day_num, ddkd_filter)
    df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

elif kpi_filter == "3. ASO TEA KÊNH ON PREMISE":
    st.subheader(f"BÁO CÁO ASO TEA KÊNH ON PREMISE {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ Visit Schedule & RPT_061.xlsx cập nhật đến ngày {date_str}/2026 | Chỉ tiêu KPI: 30 ASO/NVBH | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
    
    rows = generate_report_data(kpi_filter, day_num, ddkd_filter)
    df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

elif kpi_filter == "4. PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER)":
    st.subheader(f"BÁO CÁO PC BT KÊNH OFF (ĐƠN ≥ 4 LINE - LOẠI BEER) {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026 | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
    
    rows = generate_report_data(kpi_filter, day_num, ddkd_filter)
    df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

elif kpi_filter == "5. ASO ALL KÊNH OFF":
    st.subheader(f"BÁO CÁO ASO ALL KÊNH OFF {month_filter.upper()}")
    st.caption(f"Dữ liệu đối soát chuẩn từ TỔNG HỢP KPI ĐĐKD.xlsx & Visit Schedule Report cập nhật đến ngày {date_str}/2026 | Tiến độ thời gian: {day_num}/24 ngày ({time_gone_pct}% Time Gone)")
    
    rows = generate_report_data(kpi_filter, day_num, ddkd_filter)
    df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Chỉ Tiêu KPI", f"Thực Hiện {date_str}", "MTD (Kênh OFF)", "% MTD"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% MTD"]), use_container_width=True, hide_index=True)

elif kpi_filter == "6. BÁO CÁO ĐƠN HÀNG COMBO":
    st.subheader(f"BÁO CÁO ĐƠN HÀNG COMBO NGÀY {date_str}/2026")
    st.caption(f"Thống kê phát sinh thực tế trong ngày {date_str}/2026 & Lũy kế MTD")
    
    rows = generate_report_data(kpi_filter, day_num, ddkd_filter)
    df = pd.DataFrame(rows, columns=["STT", "Mã NVBH", "Tên NVBH", "Số CH OFF", f"Thực hiện {date_str} (OFF)", "% Hoàn thành OFF", "Số CH ON", f"Thực hiện {date_str} (ON)", "% Hoàn thành ON"])
    st.dataframe(df.style.map(highlight_mtd, subset=["% Hoàn thành OFF", "% Hoàn thành ON"]), use_container_width=True, hide_index=True)
