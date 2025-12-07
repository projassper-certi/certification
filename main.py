import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🛠️ 연결 테스트 모드")

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 1. 시트 이름 지정 없이 그냥 읽어봅니다 (무조건 첫 번째 시트 가져옴)
    st.write("📡 구글 시트 연결 시도 중...")
    df_test = conn.read()
    
    st.success("✅ 연결 성공! 첫 번째 시트 데이터를 불러왔습니다.")
    st.dataframe(df_test)
    
except Exception as e:
    st.error("❌ 연결 실패! Secrets 설정을 다시 확인해야 합니다.")
    # 에러의 진짜 원인(e)을 화면에 그대로 뿌려줍니다.
    st.code(e)