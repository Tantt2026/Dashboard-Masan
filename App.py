elif selected_kpi == "VISIT":
        saved_visit_thu = st.query_params.get("visit_thu", "")
        default_visit_thu_list = [x.strip() for x in saved_visit_thu.split(",") if x.strip()] if saved_visit_thu else []
        
        def update_visit_params():
            st.query_params["visit_thu"] = ",".join(st.session_state.visit_thu_input) if st.session_state.visit_thu_input else ""

        col_f_thu_v, _ = st.columns([1, 1.5])
        with col_f_thu_v:
            st.markdown('<p class="filter-label">📅 Lọc Theo Thứ / Chu kỳ Viếng Thăm (Chọn nhiều)</p>', unsafe_allow_html=True)
            thu_opts = ["2","3","4","5","6","7","25","36","47"]
            valid_visit_thu = [t for t in default_visit_thu_list if t in thu_opts]
            f_thu_visit = st.multiselect("", thu_opts, default=valid_visit_thu, key="visit_thu_input", on_change=update_visit_params, label_visibility="collapsed")
            
        st.query_params["visit_thu"] = ",".join(st.session_state.visit_thu_input) if st.session_state.visit_thu_input else ""

        df_visit, title_v = build_visit_report(mcp, report_date, filter_nv, f_thu_visit)
        tot_row_v = df_visit.iloc[-1] if not df_visit.empty else None
        tot_visit_val = tot_row_v['Lịch Viếng Thăm Hôm Nay'] if tot_row_v is not None else 0
        tot_v3_val = tot_row_v['Nhóm KH VIP3'] if tot_row_v is not None else 0
        tot_v5_val = tot_row_v['Nhóm KH VIP5'] if tot_row_v is not None else 0
        tot_on_val = tot_row_v['Nhóm KH Kênh ON'] if tot_row_v is not None else 0
        
        weekday_map = {0: "THỨ HAI", 1: "THỨ BA", 2: "THỨ TƯ", 3: "THỨ NĂM", 4: "THỨ SÁU", 5: "THỨ BẢY", 6: "CHỦ NHẬT"}
        wname = weekday_map.get(report_date.weekday(), "")
        iso_year, iso_week, _ = report_date.isocalendar()
        week_type_str = "ODD WEEK (Tuần Lẻ)" if iso_week % 2 == 1 else "EVEN WEEK (Tuần Chẵn)"
        
        st.markdown(f'<h3 style="color: #034ea2; font-weight: 800; margin-bottom: 2px; font-size: 16px; text-align: center;">BÁO CÁO LỊCH VIẾNG THĂM {wname} NĂM {report_date.strftime("%d/%m/%Y")} (TUẦN ISO {iso_week} - {week_type_str})</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: center; font-size: 12px; color: #4a5568; margin-bottom: 12px;">Dữ liệu cập nhật {wname} ngày {report_date.strftime("%d/%m/%Y")} | Tuần ISO {iso_week} | Tách chi tiết tập KH VIP3, VIP5, VIPSI, CH Lẻ & Kênh ON</p>', unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: render_metric_card("Tổng Lịch Viếng Thăm", f"{tot_visit_val:,}")
        with c2: render_metric_card("Tổng KH VIP3", f"{tot_v3_val:,}")
        with c3: render_metric_card("Tổng KH VIP5", f"{tot_v5_val:,}")
        with c4: render_metric_card("Tổng KH Kênh ON", f"{tot_on_val:,}")
        
        st.markdown(render_html_table(df_visit), unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="note-box">
            <b>NHẬN XÉT & ĐÁNH GIÁ LỊCH VIẾNG THĂM {wname} - NGÀY {report_date.strftime('%d/%m/%Y')} (TUẦN ISO {iso_week} - {week_type_str}):</b><br>
            • <b>Tổng Số Cửa Hàng Lịch Viếng Thăm Hôm Nay:</b> Toàn team có tổng cộng <b>{tot_visit_val:,} cửa hàng</b> cần viếng thăm theo lịch tuyến tuần ISO {iso_week}.<br>
            • <b>Tách Chi Tiết Tập KH Key/Kênh Focus:</b> Bao gồm {tot_v3_val} KH VIP3, {tot_v5_val} KH VIP5, {tot_row_v['Nhóm KH VIPSI']} KH VIPSI, {tot_row_v['Nhóm KH CH Lẻ']} CH Lẻ thông thường và {tot_on_val} CH Kênh ON Premise.<br>
            • <b>Trọng Tâm Vận Hành:</b> Ưu tiên viếng thăm 100% nhóm Cửa Hàng VIP & Kênh ON Premise để tập trung chào chốt các dòng sản phẩm ASO Focus (Trà TEA365, Chanté, Total Omachi Trộn...).
        </div>
        """, unsafe_allow_html=True)
