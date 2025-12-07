import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(layout="wide")
st.title("🏥 2025년도 인증 조사 평가 시스템")

# 1. 구글 시트 연결
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 2. 데이터 두 개 다 불러오기!
    # (주의: worksheet="시트이름"을 정확히 적어야 합니다)
    
    # 2-1. 관리자(권한) 테이블 읽기
    df_admin = conn.read(worksheet="1", usecols=['이름', '기준번호'])
    
    # 2-2. 전체 체크리스트 데이터 읽기 (기존 시트 이름이 '시트1'이라면 그대로 둠)
    # worksheet 이름을 안 적으면 첫 번째 시트를 가져옵니다.
    # 만약 시트 이름이 '설문데이터'라면 worksheet="설문데이터" 라고 적어주세요.
    df_main = conn.read() 
    
    # 숫자/문자 혼동 방지를 위해 '기준번호'를 강제로 문자로 통일
    df_main['기준번호'] = df_main['기준번호'].astype(str)

except Exception as e:
    st.error(f"구글 시트 읽기 실패! 시트 이름(탭 이름)이 'admin'이 맞는지 확인해주세요. 에러: {e}")
    st.stop()

# --- 사이드바 로그인 ---
with st.sidebar:
    st.header("🔐 위원 로그인")
    input_name = st.text_input("성함을 입력하세요")

if input_name:
    # 3. 관리자 시트에서 이름 찾기
    # df_admin에서 '이름' 열이 입력한 이름과 같은 줄을 찾음
    user_row = df_admin[df_admin['이름'] == input_name]
    
    if user_row.empty:
        st.error("등록되지 않은 위원입니다. 관리자 시트에 이름이 있는지 확인해주세요.")
    else:
        st.success(f"환영합니다, **{input_name}** 위원님!")
        
        # 4. 콤마로 된 문자열을 리스트로 변환하는 마법 (핵심 로직!)
        # 예: "1.1, 1.2, 1.3"  --->  ['1.1', '1.2', '1.3']
        
        # 엑셀에서 가져온 권한 문자열
        permission_str = str(user_row.iloc[0]['기준번호']) 
        
        # 콤마(,)로 자르고, 공백제거(strip)해서 리스트로 만듦
        target_ids = [x.strip() for x in permission_str.split(',')]
        
        # 5. 내 번호에 해당하는 데이터만 필터링
        my_data = df_main[df_main['기준번호'].isin(target_ids)]
        
        if my_data.empty:
            st.warning(f"배정된 기준번호({target_ids})에 해당하는 데이터가 없습니다.")
        else:
            # 6. 데이터 편집 화면 보여주기
            st.info(f"총 {len(my_data)}건의 평가 항목이 배정되었습니다.")
            edited_df = st.data_editor(
                my_data,
                hide_index=True,
                use_container_width=True,
                height=600
            )
            
            # (저장 버튼 로직은 나중에 추가)
            if st.button("평가 저장"):
                st.toast("저장 기능은 다음 단계에서 구현해요!", icon="🚧")
                
else:
    st.write("👈 왼쪽에서 성함을 입력해주세요.")