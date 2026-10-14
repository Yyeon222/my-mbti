"""MBTI로 단짝 포켓몬 찾기 - Streamlit 앱 (main.py 파일 하나로 실행)

실행 방법:  streamlit run main.py
필요한 패키지는 streamlit 하나뿐이에요.
"""

import streamlit as st

st.set_page_config(page_title="MBTI로 단짝 포켓몬 찾기", page_icon="⚡", layout="centered")

# 포켓몬 공식 아트워크 이미지 주소 (PokeAPI 제공, {no} 자리에 도감 번호가 들어가요)
IMAGE_URL = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/"
    "sprites/pokemon/other/official-artwork/{no}.png"
)

# 타입별 배지 색 (배경색, 글자색)
TYPE_COLORS = {
    "노말": ("#A8A878", "#3B2A18"),
    "불꽃": ("#F08030", "#3B2A18"),
    "물": ("#6890F0", "#3B2A18"),
    "전기": ("#F8D030", "#3B2A18"),
    "얼음": ("#98D8D8", "#3B2A18"),
    "격투": ("#C03028", "#FFFFFF"),
    "독": ("#A040A0", "#FFFFFF"),
    "비행": ("#A890F0", "#3B2A18"),
    "에스퍼": ("#F85888", "#3B2A18"),
    "고스트": ("#705898", "#FFFFFF"),
    "악": ("#705848", "#FFFFFF"),
    "페어리": ("#EE99AC", "#3B2A18"),
}

# MBTI 유형별 단짝 포켓몬
POKEMON = {
    "INTJ": {
        "nick": "전략가", "name": "뮤츠", "en": "Mewtwo", "no": 150, "types": ["에스퍼"],
        "feature": "뮤의 유전자로 만들어진 포켓몬이에요. 엄청난 초능력을 가졌고 혼자 있는 걸 좋아해요.",
        "reasons": [
            "혼자 조용히 생각하며 큰 그림을 그리는 모습이 닮았어요.",
            "남의 말보다 스스로 판단한 길을 믿고 나아가요.",
            "차가워 보여도 속으로는 깊은 고민을 품고 있어요.",
        ],
    },
    "INTP": {
        "nick": "사색가", "name": "후딘", "en": "Alakazam", "no": 65, "types": ["에스퍼"],
        "feature": "IQ가 5000이나 된다는 천재 포켓몬이에요. 숟가락 두 개로 초능력을 더 강하게 만들어요.",
        "reasons": [
            "머릿속에 궁금한 것이 끝없이 떠오르는 모습이 닮았어요.",
            "어려운 문제를 풀어낼 때 가장 즐거워해요.",
            "조용히 생각에 잠겨 있다가 놀라운 답을 내놓아요.",
        ],
    },
    "ENTJ": {
        "nick": "지휘관", "name": "리자몽", "en": "Charizard", "no": 6, "types": ["불꽃", "비행"],
        "feature": "큰 날개로 하늘을 날며 바위도 녹이는 뜨거운 불꽃을 뿜어요. 강한 상대를 찾아다녀요.",
        "reasons": [
            "목표가 생기면 불꽃처럼 뜨겁게 밀어붙여요.",
            "앞장서서 모두를 이끄는 타고난 리더예요.",
            "강한 상대를 만나면 오히려 더 힘이 나요.",
        ],
    },
    "ENTP": {
        "nick": "발명가", "name": "팬텀", "en": "Gengar", "no": 94, "types": ["고스트", "독"],
        "feature": "그림자 속에 숨어 지내는 장난꾸러기 유령 포켓몬이에요. 사람을 깜짝 놀라게 하는 걸 좋아해요.",
        "reasons": [
            "장난기가 많고 모두를 깜짝 놀라게 하는 걸 좋아해요.",
            "기발한 아이디어가 그림자처럼 끝없이 튀어나와요.",
            "어디서든 대화를 재미있게 만드는 분위기 메이커예요.",
        ],
    },
    "INFJ": {
        "nick": "조언자", "name": "가디안", "en": "Gardevoir", "no": 282, "types": ["에스퍼", "페어리"],
        "feature": "트레이너를 지키기 위해서라면 온 힘을 다하는 포켓몬이에요. 미래를 내다보는 힘이 있다고 해요.",
        "reasons": [
            "말하지 않아도 상대의 마음을 잘 알아채요.",
            "소중한 사람을 위해서라면 어떤 일도 해내요.",
            "조용하지만 마음속에 단단한 신념이 있어요.",
        ],
    },
    "INFP": {
        "nick": "몽상가", "name": "뮤", "en": "Mew", "no": 151, "types": ["에스퍼"],
        "feature": "모든 포켓몬의 유전자를 가졌다는 환상의 포켓몬이에요. 모든 기술을 쓸 수 있다고 해요.",
        "reasons": [
            "순수한 마음과 끝없는 상상력을 가졌어요.",
            "자유롭게 떠다니며 나만의 세계를 즐겨요.",
            "무엇이든 될 수 있는 무한한 가능성을 품고 있어요.",
        ],
    },
    "ENFJ": {
        "nick": "선생님", "name": "라프라스", "en": "Lapras", "no": 131, "types": ["물", "얼음"],
        "feature": "사람을 등에 태우고 바다를 건너는 걸 좋아하는 포켓몬이에요. 아름다운 노랫소리를 내요.",
        "reasons": [
            "친구를 등에 태워 바다를 건너게 해 주는 다정한 리더예요.",
            "사람들의 마음을 모아 함께 나아가는 걸 좋아해요.",
            "노래하듯 부드러운 말로 모두를 위로해요.",
        ],
    },
    "ENFP": {
        "nick": "활동가", "name": "피카츄", "en": "Pikachu", "no": 25, "types": ["전기"],
        "feature": "볼에 있는 주머니에 전기를 모으는 포켓몬이에요. 신이 나면 찌릿찌릿 전기를 내요.",
        "reasons": [
            "어디서나 밝고 반짝이는 에너지를 뿜어요.",
            "처음 만난 사람과도 금방 친구가 돼요.",
            "호기심이 많아 새로운 모험이 늘 신나요.",
        ],
    },
    "ISTJ": {
        "nick": "원칙주의자", "name": "거북왕", "en": "Blastoise", "no": 9, "types": ["물"],
        "feature": "등껍질의 대포에서 강력한 물줄기를 쏘는 포켓몬이에요. 몸이 무겁고 아주 단단해요.",
        "reasons": [
            "단단한 등껍질처럼 믿음직하고 흔들림이 없어요.",
            "맡은 일은 끝까지 책임지고 해내요.",
            "약속과 규칙을 소중히 여겨요.",
        ],
    },
    "ISFJ": {
        "nick": "수호자", "name": "럭키", "en": "Chansey", "no": 113, "types": ["노말"],
        "feature": "영양 만점의 알을 다친 사람이나 포켓몬에게 나눠 주는 다정한 포켓몬이에요.",
        "reasons": [
            "다친 친구를 정성껏 돌봐 주는 따뜻한 마음씨예요.",
            "눈에 띄지 않아도 묵묵히 주변을 챙겨요.",
            "가진 것을 기꺼이 나누는 다정한 성격이에요.",
        ],
    },
    "ESTJ": {
        "nick": "관리자", "name": "괴력몬", "en": "Machamp", "no": 68, "types": ["격투"],
        "feature": "네 개의 팔로 사방에서 쉴 새 없이 펀치를 날리는 힘센 포켓몬이에요.",
        "reasons": [
            "네 개의 팔로 일을 척척 해내는 해결사예요.",
            "계획을 세우고 차근차근 움직이는 걸 좋아해요.",
            "모두가 믿고 따르는 든든한 리더예요.",
        ],
    },
    "ESFJ": {
        "nick": "다정한 친구", "name": "토게키스", "en": "Togekiss", "no": 468, "types": ["페어리", "비행"],
        "feature": "서로를 아끼는 사람들 곁에 나타나 행복을 나눠 준다는 포켓몬이에요.",
        "reasons": [
            "사람들 사이에 행복과 평화를 나눠 줘요.",
            "친구들의 기분을 잘 살피고 먼저 다가가요.",
            "모두가 함께 웃을 때 가장 행복해요.",
        ],
    },
    "ISTP": {
        "nick": "장인", "name": "개굴닌자", "en": "Greninja", "no": 658, "types": ["물", "악"],
        "feature": "물을 단단하게 뭉친 수리검을 던지는 닌자 포켓몬이에요. 빠르고 날렵하게 움직여요.",
        "reasons": [
            "조용하지만 위기 상황에서 누구보다 빠르게 움직여요.",
            "직접 해 보며 몸으로 배우는 걸 좋아해요.",
            "혼자만의 시간과 자유를 소중히 여겨요.",
        ],
    },
    "ISFP": {
        "nick": "예술가", "name": "이브이", "en": "Eevee", "no": 133, "types": ["노말"],
        "feature": "주변 환경에 따라 여러 모습으로 진화할 수 있는 포켓몬이에요. 진화할 수 있는 모습이 8가지나 돼요.",
        "reasons": [
            "주변에 따라 다양한 모습으로 변하는 감성파예요.",
            "자기만의 속도로 아름다운 것을 즐겨요.",
            "조용하지만 다정하고 부드러운 마음을 가졌어요.",
        ],
    },
    "ESTP": {
        "nick": "모험가", "name": "윈디", "en": "Arcanine", "no": 59, "types": ["불꽃"],
        "feature": "하루에 1만 km를 달린다고 할 만큼 빠른 포켓몬이에요. 늠름한 모습에 반하는 사람이 많아요.",
        "reasons": [
            "생각보다 몸이 먼저 움직이는 행동파예요.",
            "바람처럼 빠르게 달리며 모험을 즐겨요.",
            "위기 상황에서도 겁먹지 않는 용감한 성격이에요.",
        ],
    },
    "ESFP": {
        "nick": "연예인", "name": "푸린", "en": "Jigglypuff", "no": 39, "types": ["노말", "페어리"],
        "feature": "동그란 눈으로 상대를 바라보며 자장가를 불러 잠들게 하는 포켓몬이에요.",
        "reasons": [
            "무대에 서면 누구보다 반짝이는 타고난 스타예요.",
            "노래와 웃음으로 주변을 즐겁게 만들어요.",
            "지금 이 순간을 마음껏 즐길 줄 알아요.",
        ],
    },
}

# 버튼 표시 순서 (4줄 × 4칸)
ORDER = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

# ---------------------------------------------------------------- 화면 꾸미기 (CSS)
CSS = """
<style>
:root {
  --bg: #FFF7E3;
  --card: #FFFDF6;
  --yellow: #FFD54F;
  --yellow-soft: #FFF0B8;
  --yellow-deep: #F2B200;
  --line: #F0DDA4;
  --text: #4A3420;
  --text-soft: #7A5C3E;
}

html { font-size: 18px; }

/* 앱 전체 배경과 글자 (어두운 테마에서도 같은 색으로 보이게 고정) */
.stApp {
  background-color: var(--bg);
  background-image: radial-gradient(#FBE8B4 1.5px, transparent 1.5px);
  background-size: 26px 26px;
  color: var(--text);
  font-family: "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", sans-serif;
  word-break: keep-all;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stMainBlockContainer"], .block-container {
  max-width: 780px;
  padding-top: 2.5rem;
  padding-bottom: 3rem;
}

/* 제목 */
.app-header { text-align: center; margin-bottom: 0.5rem; }
.app-logo {
  display: inline-flex; align-items: center; justify-content: center;
  width: 84px; height: 84px; border-radius: 50%;
  background: var(--yellow); box-shadow: 0 6px 0 var(--yellow-deep);
  font-size: 44px; margin-bottom: 12px;
}
.app-title { margin: 0 0 6px; font-size: 2.1rem; font-weight: 800; line-height: 1.3; color: var(--text); }
.app-sub { margin: 0; font-size: 1.1rem; color: var(--text-soft); }
.step { margin: 1.2rem 0 0.4rem; text-align: center; font-size: 1.3rem; font-weight: 800; color: var(--text); }
.hint { margin: 0.6rem 0 0; text-align: center; font-size: 0.95rem; color: var(--text-soft); }

/* MBTI 버튼 (칸을 꽉 채우도록) */
[data-testid="stElementContainer"]:has(> .stButton),
.element-container:has(> .stButton),
.stButton { width: 100% !important; }
.stButton > button {
  width: 100%;
  min-height: 4.6rem;
  background: #fff;
  color: var(--text);
  border: 3px solid var(--line);
  border-radius: 20px;
  box-shadow: 0 5px 0 var(--line);
  font-family: inherit;
  transition: background-color .15s, border-color .15s, transform .1s, box-shadow .1s;
}
.stButton > button p { font-size: 0.85rem; line-height: 1.35; color: var(--text-soft); }
.stButton > button strong { font-size: 1.45rem; font-weight: 800; letter-spacing: 1px; color: var(--text); }
.stButton > button:hover {
  background: var(--yellow-soft);
  border-color: var(--yellow);
  box-shadow: 0 5px 0 var(--yellow-deep);
  color: var(--text);
}
.stButton > button:active { transform: translateY(4px); box-shadow: 0 1px 0 var(--yellow-deep); }
.stButton > button:focus-visible { outline: 4px solid #D98E00; outline-offset: 3px; }

/* '다시 고르기' 버튼 (노란색) */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
  min-height: 3.6rem;
  background: var(--yellow);
  border: none;
  border-radius: 999px;
  box-shadow: 0 6px 0 var(--yellow-deep);
}
.stButton > button[kind="primary"] p,
.stButton > button[data-testid="stBaseButton-primary"] p {
  font-size: 1.3rem; font-weight: 800; color: var(--text);
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover { background: #FFCC2E; }

/* 휴대폰에서는 버튼을 2칸씩 */
@media (max-width: 640px) {
  [data-testid="stHorizontalBlock"] { flex-wrap: wrap; gap: 0.8rem; }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    flex: 1 1 calc(50% - 0.8rem) !important;
    width: calc(50% - 0.8rem) !important;
    min-width: calc(50% - 0.8rem) !important;
  }
  .app-title { font-size: 1.55rem; }
}

/* 축하 배너 */
.cheer {
  margin: 0.4rem 0 1rem;
  padding: 18px 16px;
  border-radius: 24px;
  background: var(--yellow);
  box-shadow: 0 6px 0 var(--yellow-deep);
  text-align: center;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text);
  animation: cheer-pop .6s ease-out;
}
.cheer small { display: block; margin-top: 2px; font-size: 1rem; font-weight: 600; color: var(--text-soft); }

/* 결과 카드 */
.result-card {
  background: var(--card);
  border: 3px solid var(--line);
  border-radius: 28px;
  box-shadow: 0 8px 0 var(--line);
  padding: 28px 22px;
  text-align: center;
  color: var(--text);
}
.result-title { margin: 0 0 18px; font-size: 1.25rem; font-weight: 700; }
.badge {
  display: inline-block; padding: 2px 14px; margin-right: 4px;
  border-radius: 999px; background: var(--yellow);
  font-weight: 800; letter-spacing: 1px;
}
.poke-circle {
  display: flex; align-items: center; justify-content: center;
  width: 250px; height: 250px; margin: 10px auto 22px;
  border-radius: 50%; background: #fff;
  border: 6px solid var(--yellow);
  box-shadow: 0 0 0 10px var(--yellow-soft);
  animation: cheer-pop .6s ease-out;
}
.poke-circle img { width: 200px; height: 200px; object-fit: contain; }
.poke-no { margin: 0; font-size: 1rem; font-weight: 700; color: var(--text-soft); }
.poke-name { margin: 0; font-size: 2.4rem; font-weight: 800; line-height: 1.3; }
.poke-en { font-size: 1.3rem; font-weight: 700; color: var(--text-soft); }
.types { margin: 10px 0 22px; }
.type {
  display: inline-block; margin: 0 4px; padding: 3px 16px;
  border-radius: 999px; font-size: 1rem; font-weight: 800;
}
.box {
  max-width: 580px; margin: 0 auto 16px; padding: 16px 20px;
  text-align: left; background: #fff;
  border: 2px solid var(--line); border-radius: 20px;
}
.box-title { margin: 0 0 6px; font-size: 1.1rem; font-weight: 800; }
.box p { margin: 0; font-size: 1.05rem; line-height: 1.65; }
.box ul { margin: 0; padding: 0; list-style: none; }
.box li { position: relative; padding-left: 32px; font-size: 1.05rem; line-height: 1.65; }
.box li + li { margin-top: 6px; }
.box li::before { content: "⭐"; position: absolute; left: 0; top: 0; }

@keyframes cheer-pop {
  0%   { transform: scale(.6); opacity: 0; }
  70%  { transform: scale(1.06); opacity: 1; }
  100% { transform: scale(1); }
}

/* 축하 꽃가루 (화면 위에서 떨어져요) */
.confetti {
  position: fixed; inset: 0; overflow: hidden;
  pointer-events: none; z-index: 1000001;
}
.confetti span {
  position: absolute; top: -12vh;
  animation-name: confetti-fall;
  animation-timing-function: ease-in;
  animation-fill-mode: forwards;
}
@keyframes confetti-fall {
  0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
  100% { transform: translateY(125vh) rotate(540deg); opacity: .8; }
}

.footer { margin-top: 1.6rem; text-align: center; font-size: 0.85rem; line-height: 1.7; color: var(--text-soft); }
.footer a { color: var(--text-soft); }

@media (prefers-reduced-motion: reduce) {
  .cheer, .poke-circle { animation: none; }
  .confetti { display: none; }
}
</style>
"""

# ---------------------------------------------------------------- 화면 상태
if "mbti" not in st.session_state:
    st.session_state.mbti = None       # 지금 고른 MBTI
if "celebrate" not in st.session_state:
    st.session_state.celebrate = False  # 축하 효과를 보여 줄 차례인지


def choose(code):
    st.session_state.mbti = code
    st.session_state.celebrate = True


def go_back():
    st.session_state.mbti = None


def confetti_html():
    """화면 위에서 꽃가루가 떨어지는 효과"""
    pieces = ["🎉", "⭐", "✨", "🎊", "💛", "🌟"]
    spans = []
    for i in range(28):
        left = (i * 37) % 100                 # 가로 위치를 고르게 흩뿌리기
        delay = (i % 7) * 0.18                # 조금씩 늦게 출발
        duration = 2.6 + (i % 5) * 0.35       # 떨어지는 속도도 조금씩 다르게
        size = 1.6 + (i % 4) * 0.4
        spans.append(
            f'<span style="left:{left}%;font-size:{size}rem;'
            f'animation-delay:{delay:.2f}s;animation-duration:{duration:.2f}s">'
            f"{pieces[i % len(pieces)]}</span>"
        )
    return '<div class="confetti" aria-hidden="true">' + "".join(spans) + "</div>"


def type_badges(types):
    badges = []
    for t in types:
        bg, fg = TYPE_COLORS[t]
        badges.append(f'<span class="type" style="background:{bg};color:{fg}">{t}</span>')
    return "".join(badges)


# ---------------------------------------------------------------- 화면 그리기
st.html(CSS)

st.html(
    """
    <div class="app-header">
      <div class="app-logo" aria-hidden="true">⚡</div>
      <p class="app-title">MBTI로 단짝 포켓몬 찾기</p>
      <p class="app-sub">나와 꼭 닮은 단짝 포켓몬은 누구일까요?</p>
    </div>
    """
)

if st.session_state.mbti is None:
    # 1단계: MBTI 고르기
    st.html('<p class="step">👇 나의 MBTI를 눌러 주세요</p>')
    for row in range(4):
        cols = st.columns(4)
        for col, code in zip(cols, ORDER[row * 4:(row + 1) * 4]):
            with col:
                st.button(
                    f"**{code}**  \n{POKEMON[code]['nick']}",
                    key=f"pick_{code}",
                    on_click=choose,
                    args=(code,),
                )
    st.html('<p class="hint">버튼 하나만 누르면 바로 단짝 포켓몬이 나와요!</p>')

else:
    # 2단계: 단짝 포켓몬 보여 주기
    code = st.session_state.mbti
    p = POKEMON[code]

    if st.session_state.celebrate:
        st.balloons()                 # 스트림릿 기본 풍선 효과
        st.html(confetti_html())      # 꽃가루 효과
        st.session_state.celebrate = False

    reasons = "".join(f"<li>{r}</li>" for r in p["reasons"])
    st.html(
        f"""
        <div class="cheer">🎉 축하해요! 단짝 포켓몬을 찾았어요!
          <small>{code} 유형과 꼭 맞는 포켓몬을 소개할게요</small>
        </div>
        <div class="result-card">
          <p class="result-title"><span class="badge">{code}</span> 의 단짝 포켓몬은...</p>
          <div class="poke-circle">
            <img src="{IMAGE_URL.format(no=p['no'])}" alt="{p['name']} ({p['en']}) 공식 이미지">
          </div>
          <p class="poke-no">No.{p['no']:03d}</p>
          <p class="poke-name">{p['name']} <span class="poke-en">({p['en']})</span></p>
          <div class="types">{type_badges(p['types'])}</div>
          <div class="box">
            <p class="box-title">📖 이런 포켓몬이에요</p>
            <p>{p['feature']}</p>
          </div>
          <div class="box">
            <p class="box-title">💛 이래서 나와 잘 어울려요</p>
            <ul>{reasons}</ul>
          </div>
        </div>
        """
    )
    st.write("")
    st.button("🔄 다시 고르기", on_click=go_back, type="primary")

st.html(
    """
    <p class="footer">
      재미로 보는 결과예요. 즐겁게 봐 주세요 😊<br>
      포켓몬 이미지 © Nintendo · Creatures · GAME FREAK · The Pokémon Company<br>
      이미지 출처: <a href="https://github.com/PokeAPI/sprites" target="_blank">PokeAPI</a>
    </p>
    """
)
