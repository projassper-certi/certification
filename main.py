import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# [핵심] 캐시 삭제 (꼬인 기억 지우기)
st.cache_data.clear()

st.set_page_config(layout="wide")
st.title("🏥 2025년도 인증 조사 평가 시스템")

# 1. 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

# =========================================================
# [중요] Secrets가 아니라, 여기에 주소를 직접 적습니다.
# 이렇게 하면 에러 날 확률이 0%가 됩니다.
# =========================================================
sheet_url = "https://docs.google.com/spreadsheets/d/1CSvcbp_eI2fug0vCsjHKSMx2ETtIicxYckOyMyJblWM/edit"

try:
    # 2. 데이터 불러오기 (주소를 직접 명시!)
    
    # (1) 관리자 시트 읽기 (시트 이름: admin)
    # spreadsheet=sheet_url 을 넣어주면 무조건 그 파일을 찾아갑니다.
    df_admin = conn.read(spreadsheet=sheet_url, worksheet="admin", usecols=['이름', '기준번호'])
    
    # (2) 설문 데이터 시트 읽기 (시트 이름: 설문데이터)
    # 마찬가지로 spreadsheet=sheet_url 을 넣어줍니다.
    df_main = conn.read(spreadsheet=sheet_url, worksheet="설문데이터", skiprows=1)
    
    # (3) 데이터 다듬기
    df_main = df_main.dropna(subset=['기준번호'])
    df_main['기준번호'] = df_main['기준번호'].astype(str)

except Exception as e:
    st.error(f"데이터 로딩 중 오류 발생! 에러 내용: {e}")
    st.stop()

# ---------------------------------------------------------
# 3. 사이드바 로그인 화면
# ---------------------------------------------------------
with st.sidebar:
    st.header("🔐 위원 로그인")
    input_name = st.text_input("성함 입력", placeholder="예: 김철수")

# ---------------------------------------------------------
# 4. 메인 로직
# ---------------------------------------------------------
if input_name:
    user_row = df_admin[df_admin['이름'] == input_name]
    
    if user_row.empty:
        st.error(f"⛔ '{input_name}' 위원님은 등록되지 않았습니다.")
        st.info("admin 시트에 이름이 정확히 있는지 확인해주세요.")
    else:
        st.success(f"👋 환영합니다, **{input_name}** 위원님!")
        
        # 권한 가져오기
        permission_str = str(user_row.iloc[0]['기준번호'])
        target_ids = [x.strip() for x in permission_str.split(',')]
        
        # 내 번호만 필터링
        my_data = df_main[df_main['기준번호'].isin(target_ids)]
        
        if my_data.empty:
            st.warning(f"배정된 문항({target_ids})을 찾을 수 없습니다.")
        else:
            st.write(f"총 **{len(my_data)}개**의 평가 문항이 배정되었습니다.")
            
            # 평가 화면
            st.data_editor(
                my_data,
                hide_index=True,
                use_container_width=True,
                height=600,
                key="editor"
            )
else:
    st.info("👈 왼쪽 사이드바에 성함을 입력해주세요.")
    
    # (테스트용) 연결 잘 됐는지 눈으로 확인하기
    with st.expander("관리자 명단 확인 (테스트)"):
        st.dataframe(df_admin)