import streamlit as st
import random

# --- 페이지 기본 설정 및 제목 ---
st.set_page_config(page_title="천재 해커의 버그 치료", page_icon="🚨", layout="centered")
st.title("🚨 천재 해커: 버그를 치료하라!")
st.subheader("[데드라인 1시간 전]")
st.markdown("당신은 천재 해커입니다. 시스템 해킹을 막기 위해 버그를 치료하세요!")

# --- 게임 규칙 안내 (사이드바) ---
with st.sidebar:
    st.header("🎯 게임 규칙")
    st.markdown("""
    1. 문제를 맞추면 **성공도**가 올라갑니다.
    2. 문제를 틀리면 **멘탈**이 깎입니다.
    3. 아주 가끔! 문제를 맞춰도 성공도가 안 오르는 **가짜 버그**가 있습니다.
    4. **성공도 100%**면 칼퇴근, **멘탈이 0%**가 되면 야근 실패!
    """)
    if st.button("🔄 게임 초기화 (다시 시작)"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- 게임 상태 초기화 (Session State) ---
if "mental" not in st.session_state:
    st.session_state.mental = 100
if "progress" not in st.session_state:
    st.session_state.progress = 0
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "msg_type" not in st.session_state: # 메세지 종류 (success, warning, error 등)
    st.session_state.msg_type = "info"
if "msg_text" not in st.session_state:
    st.session_state.msg_text = "게임을 시작합니다! 첫 번째 문제를 풀어보세요."

# --- 새로운 문제 생성 함수 ---
def generate_question():
    op = random.choice(["+", "-", "*", "/"])
    success_flag = random.random() > 0.15  # 15% 확률로 가짜 버그
    display_op = op

    if op == "+":
        num1 = random.randint(5, 30)
        num2 = random.randint(5, 30)
        answer = num1 + num2
    elif op == "-":
        num1 = random.randint(20, 50)
        num2 = random.randint(5, num1)
        answer = num1 - num2
    elif op == "*":
        num1 = random.randint(2, 9)
        num2 = random.randint(2, 9)
        answer = num1 * num2
    else:  # "/" 나누기
        display_op = "÷"
        num2 = random.randint(2, 6)
        answer = random.randint(2, 6)
        num1 = num2 * answer

    st.session_state.num1 = num1
    st.session_state.num2 = num2
    st.session_state.display_op = display_op
    st.session_state.answer = answer
    st.session_state.success_flag = success_flag

# 첫 문제 생성
if "answer" not in st.session_state:
    generate_question()

# --- 게임 종료 조건 확인 ---
if st.session_state.mental <= 0:
    st.session_state.game_over = True
elif st.session_state.progress >= 100:
    st.session_state.game_over = True

# --- 화면 표시 레이아웃 ---
if not st.session_state.game_over:
    # 진행 상황 시각화
    st.markdown(f"### 📟 [STAGE {st.session_state.stage}]")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="❤️ 현재 멘탈", value=f"{st.session_state.mental}%")
        st.progress(st.session_state.mental / 100)
    with col2:
        st.metric(label="📈 현재 성공도", value=f"{st.session_state.progress}%")
        st.progress(st.session_state.progress / 100)
        
    st.divider()

    # 이전 라운드 결과 알림창
    if st.session_state.msg_type == "success":
        st.success(st.session_state.msg_text)
    elif st.session_state.msg_type == "warning":
        st.warning(st.session_state.msg_text)
    elif st.session_state.msg_type == "error":
        st.error(st.session_state.msg_text)
    else:
        st.info(st.session_state.msg_text)

    # 문제 출제 구역
    st.markdown(f"#### 🔥 문제: `{st.session_state.num1}` {st.session_state.display_op} `{st.session_state.num2}` = ?")
    
    # 정답 입력창 (엔터키를 누르거나 버튼을 누르면 제출됨)
    with st.form(key="answer_form", clear_on_submit=True):
        user_input = st.number_input("정답을 입력하세요:", step=1, value=None, placeholder="숫자 입력 후 채점 버튼 클릭")
        submit_button = st.form_submit_button(label="💻 채점하기")

    # 정답 판정 로직
    if submit_button:
        if user_input is None:
            st.session_state.msg_type = "error"
            st.session_state.msg_text = "❌ 숫자가 입력되지 않았습니다! 해킹 방어 실패! 멘탈이 깎입니다."
            st.session_state.mental -= 20
        elif user_input == st.session_state.answer:
            if st.session_state.success_flag:
                st.session_state.msg_type = "success"
                st.session_state.msg_text = f"✅ [DEBUG SUCCESS] 버그 치료 완료! 성공도가 상승합니다 (+10%)."
                st.session_state.progress += 10
            else:
                st.session_state.msg_type = "warning"
                st.session_state.msg_text = "⚠️ [SPAGHETTI CODE!] 문제를 맞췄지만, 꼬여있는 가짜 버그였습니다! 성공도가 오르지 않습니다."
        else:
            st.session_state.msg_type = "error"
            st.session_state.msg_text = f"❌ [DEFENSE FAILED] 틀렸습니다! (정답은 {st.session_state.answer}였습니다.) 멘탈이 바닥납니다 (-20%)."
            st.session_state.mental -= 20
        
        st.session_state.stage += 1
        generate_question() # 다음 문제 세팅
        st.rerun()

else:
    # --- 엔딩 화면 ---
    st.divider()
    if st.session_state.progress >= 100:
        st.balloons()
        st.success("👑 [MISSION COMPLETE] 정시 퇴근 성공!\n\n모든 버그를 막아내고 무사히 퇴근합니다. 당신은 최고의 프로그래머!")
    else:
        st.error("💀 [MISSION FAILED] 멘탈 붕괴... 야근 확정!\n\n멘탈이 전부 소모되었습니다. 밤새도록 버그를 고쳐야 합니다...")
    
    if st.button("🎮 게임 다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
