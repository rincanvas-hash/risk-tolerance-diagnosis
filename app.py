"""投資初心者向けのリスク許容度診断 Streamlit アプリ。"""

from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent

QUESTIONS = [
    ("値動きが大きい商品についてどう思いますか？", ["なるべく避けたい", "少しなら大丈夫", "内容次第で検討できる", "成長のためなら前向き"]),
    ("投資額が一時的に減ったらどうしますか？", ["すぐ不安になる", "少し様子を見る", "理由を確認して判断する", "長期なら気にしない"]),
    ("投資の目的に近いものは？", ["元本重視", "生活防衛しながら少し増やしたい", "バランスよく増やしたい", "大きく成長を狙いたい"]),
    ("投資期間はどれくらい考えていますか？", ["1年未満", "1〜3年", "3〜10年", "10年以上"]),
    ("ニュースで相場下落を見たときの反応は？", ["かなり怖い", "少し不安", "冷静に様子を見る", "チャンスかもと思う"]),
    ("価格変動とリターンの関係についてどう考えますか？", ["変動はできるだけ小さい方がいい", "少しの変動なら受け入れられる", "リターンのために多少必要", "成長のためには当然あるもの"]),
    ("投資商品を選ぶなら？", ["預金に近い安心感が欲しい", "安定重視の商品", "分散された商品", "成長性の高い商品"]),
    ("あなたの性格に近いのは？", ["とても慎重", "やや慎重", "比較的前向き", "好奇心旺盛で挑戦的"]),
    ("損失が出る可能性についてどう感じますか？", ["できれば絶対避けたい", "少しなら仕方ない", "長期なら受け入れられる", "成長のためなら必要"]),
    ("投資を続ける上で一番大事なのは？", ["安心して眠れること", "無理をしないこと", "自分に合ったバランス", "将来の大きな成長"]),
]

TYPE_DETAILS = [
    (10, "超安定重視タイプ", "安心を最優先し、値動きをできるだけ抑えたいタイプです。", "生活資金を確保し、仕組みを理解できる商品から始める", "リターンだけを見て、無理にリスクを取らない"),
    (20, "堅実タイプ", "守りを大切にしながら、少しずつ資産形成を考えるタイプです。", "少額・長期・分散を意識して無理なく続ける", "短期的な成果を焦らず、余裕資金で取り組む"),
    (30, "慎重タイプ", "安全性を確かめながら、着実な成長を目指すタイプです。", "安定資産を中心に、成長資産を少し組み合わせる", "慎重になりすぎて機会を逃さないよう目的を整理する"),
    (40, "バランスタイプ", "安定と成長の両方を大切にできるタイプです。", "複数の資産に分散し、定期的に配分を見直す", "相場に合わせて頻繁に方針を変えすぎない"),
    (50, "マイペースタイプ", "自分に合ったペースでほどよいリスクを取れるタイプです。", "目標と期間を決め、積立で淡々と続ける", "慣れてきても投資額を急に増やしすぎない"),
    (60, "前向きタイプ", "値動きを受け入れながら、将来の成長を目指せるタイプです。", "長期目線で成長資産を取り入れ、分散を忘れない", "好調なときほどリスクの取りすぎに注意する"),
    (70, "成長重視タイプ", "一定の変動を許容し、資産の成長を重視するタイプです。", "長期・分散を軸に成長性のある資産を活用する", "下落時にも続けられる金額と配分を守る"),
    (80, "積極タイプ", "相場の変動に比較的強く、積極的に成長を狙えるタイプです。", "許容できる損失を決めたうえで成長機会を探す", "一つの商品や市場への集中を避ける"),
    (90, "チャレンジタイプ", "大きな値動きも理解し、挑戦を楽しめるタイプです。", "余裕資金の範囲で、明確なルールを持って運用する", "勢いや感情だけで売買せず、損失の上限を意識する"),
    (100, "ハイリスク許容タイプ", "高い変動を受け入れ、大きな成長を追求できるタイプです。", "リスク管理と分散を徹底し、長期の目標に沿って判断する", "許容度が高くても、生活資金まで投資に回さない"),
]


def calculate_result(answers: list[int]) -> tuple[int, tuple[int, str, str, str, str]]:
    """回答（各1〜4点）から許容度とタイプ情報を返す。"""
    score = sum(answers)
    tolerance = round((score - 10) / 30 * 100)
    detail = next(item for item in TYPE_DETAILS if tolerance <= item[0])
    return tolerance, detail


def show_guide(image_name: str, message: str) -> None:
    """キャラクター画像と吹き出しを横並びで表示する。"""
    image_col, message_col = st.columns([1, 2], vertical_alignment="center")
    with image_col:
        st.image(str(BASE_DIR / image_name), use_container_width=True)
    with message_col:
        st.markdown(f'<div class="speech">{message}</div>', unsafe_allow_html=True)


def go_to(page: str) -> None:
    st.session_state.page = page
    st.rerun()


st.set_page_config(page_title="リスク許容度診断", page_icon="📊", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #eff9ff 0%, #f3fbf6 100%); color: #183b4e; }
    .block-container { max-width: 780px; padding-top: 4rem !important; padding-bottom: 3rem; }
    h1, h2, h3 { color: #176b87 !important; }
    .subtitle { text-align: center; color: #347a74; font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem; }
    .speech { position: relative; background: white; border: 3px solid #73b8b1; border-radius: 18px; padding: 1rem; font-weight: 700; color: #205c61; box-shadow: 0 4px 12px #1c65751c; }
    .speech:before { content: ""; position: absolute; left: -15px; top: 45%; border-width: 10px 15px 10px 0; border-style: solid; border-color: transparent #73b8b1 transparent transparent; }
    div.stButton > button { width: 100%; min-height: 64px; border: 0; border-radius: 14px; background: #d84949; color: white; font-size: 1.2rem; font-weight: 800; box-shadow: 0 4px 0 #a72e2e; }
    div.stButton > button:hover { background: #c83d3d; color: white; border: 0; }
    div[data-testid="stRadio"] { background: #ffffffcc; border: 1px solid #cce7e3; border-radius: 14px; padding: .8rem 1rem; margin-bottom: .7rem; }
    .result-card { background: white; border: 2px solid #a6d8d0; border-radius: 18px; padding: 1.3rem; margin: 1rem 0; box-shadow: 0 6px 18px #1c65751a; }
    .score { text-align: center; font-size: 1.35rem; font-weight: 700; color: #347a74; }
    .score strong { display: block; color: #d84949; font-size: 3rem; line-height: 1.1; }
    .type-name { text-align: center; font-size: 1.7rem; font-weight: 800; color: #176b87; margin: .6rem 0; }
    .disclaimer { background: #e9f3f5; border-radius: 10px; padding: .8rem; font-size: .85rem; color: #526b73; margin: 1.2rem 0; }
    @media (max-width: 600px) { .block-container { padding: 3rem 1rem 2rem !important; } h1 { font-size: 2rem !important; } .speech { padding: .7rem; font-size: .9rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

if "page" not in st.session_state:
    st.session_state.page = "intro"

if st.session_state.page == "intro":
    st.title("リスク許容度診断")
    st.markdown('<div class="subtitle">10問でわかるあなたの投資スタイル</div>', unsafe_allow_html=True)
    show_guide("guide_intro2.png", "10問でわかるあなたの投資スタイル")
    st.write("")
    if st.button("診断をはじめる", type="primary", use_container_width=True):
        go_to("questions")

elif st.session_state.page == "questions":
    st.title("10問に答えてみましょう")
    show_guide("guide_question.png", "直感で答えて大丈夫です")
    st.progress(sum(f"answer_{i}" in st.session_state for i in range(10)) / 10, text="回答状況")

    with st.form("diagnosis_form"):
        for index, (question, choices) in enumerate(QUESTIONS):
            labels = [f"{letter}. {choice}" for letter, choice in zip("ABCD", choices)]
            st.radio(
                f"{index + 1}. {question}",
                options=range(1, 5),
                format_func=lambda value, labels=labels: labels[value - 1],
                index=None,
                key=f"answer_{index}",
            )
        submitted = st.form_submit_button("結果を見る", type="primary", use_container_width=True)

    if submitted:
        answers = [st.session_state.get(f"answer_{i}") for i in range(10)]
        if any(answer is None for answer in answers):
            st.error("未回答の質問があります。10問すべてに回答してください。")
        else:
            tolerance, detail = calculate_result(answers)
            st.session_state.result = (tolerance, detail)
            go_to("result")

else:
    tolerance, detail = st.session_state.get("result", calculate_result([1] * 10))
    _, type_name, description, suitable, caution = detail
    st.title("診断結果")
    show_guide("guide_result2.png", "あなたのタイプはこちらです！")

    fig, ax = plt.subplots(figsize=(7, 7))
    values = [tolerance, 100 - tolerance]
    if tolerance == 0:
        values = [0.0001, 99.9999]
    ax.pie(values, colors=["#45a99a", "#dcefed"], startangle=90, counterclock=False, wedgeprops={"edgecolor": "white", "linewidth": 3})
    ax.text(0, 0.08, f"{tolerance}%", ha="center", va="center", fontsize=38, fontweight="bold", color="#176b87")
    ax.axis("equal")
    fig.patch.set_alpha(0)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown(
        f"""
        <div class="result-card">
          <div class="score">リスク許容度<strong>{tolerance}%</strong></div>
          <div class="type-name">{type_name}</div>
          <p>{description}</p>
          <h3>向いている考え方</h3><p>{suitable}</p>
          <h3>注意点</h3><p>{caution}</p>
        </div>
        <div class="disclaimer">この診断は参考用の簡易コンテンツです。投資判断を行うものではありません。</div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("もう一度診断する", type="primary", use_container_width=True):
        for i in range(10):
            st.session_state.pop(f"answer_{i}", None)
        st.session_state.pop("result", None)
        go_to("intro")
