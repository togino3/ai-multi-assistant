import streamlit as st
from openai import OpenAI

client = OpenAI()

# 初期化：選ばれたアシスタントをセッションに保持
if "assistant_type" not in st.session_state:
    st.session_state.assistant_type = None

# 戻るボタン（常に表示）
st.sidebar.button("← ホームに戻る", on_click=lambda: st.session_state.update(assistant_type=None))

# ヘッダー
st.title("🤖 AIアシスタントへようこそ")

# ホーム画面：アシスタント選択
if st.session_state.assistant_type is None:
    st.subheader("目的に応じてアシスタントを選んでください")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧑‍💼 営業アシスタント"):
            st.session_state.assistant_type = "sales"
        if st.button("🔍 外部調査アシスタント"):
            st.session_state.assistant_type = "research"

    with col2:
        if st.button("💁‍♀️ サポートアシスタント"):
            st.session_state.assistant_type = "support"
        if st.button("📚 社内FAQアシスタント"):
            st.session_state.assistant_type = "faq"

# 各アシスタント画面
elif st.session_state.assistant_type == "sales":
    st.header("🧑‍💼 営業アシスタント")
    st.write("商談履歴を入力すると、次のアクションを提案します。")

    client_name = st.text_input("顧客名")
    summary = st.text_area("商談の要点")
    date = st.date_input("商談日付")

    if st.button("提案を生成"):
        if not all([client_name, summary, date]):
            st.warning("すべての項目を入力してください。")
        else:
            with st.spinner("AIが分析中..."):
                prompt = f"""
あなたはB2B営業アシスタントです。
以下は、商談の要約と日付、および顧客名です。
これをもとに、営業担当者に対して次のアクションを3つの観点から提案してください：
1. 次に何をすべきか（Next Action）
2. その理由（Reason）
3. 関係強化のヒント（Relationship Tips）

顧客名: {client_name}
商談日: {date}
商談要約: {summary}

フォーマット:
- Next Action:
- Reason:
- Relationship Tips:
"""

                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "あなたは有能なB2B営業アシスタントです。"},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.5,
                        max_tokens=500
                    )
                    result = response.choices[0].message.content
                    st.success("提案が生成されました！")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

elif st.session_state.assistant_type == "support":
    st.header("💁‍♀️ サポートアシスタント")
    st.write("サポートに関する問い合わせを入力してください。")
    query = st.text_area("例：製品のインストール方法を教えてください")
    if st.button("回答を生成（モック）"):
        st.markdown("**対応例：** 製品のインストール手順についてはこちらをご参照ください → https://example.com/guide")

elif st.session_state.assistant_type == "research":
    st.header("🔍 外部調査アシスタント")
    st.write("調べたいキーワードを入力してください。")
    topic = st.text_input("例：生成AIの最新活用事例")
    if st.button("調査サマリを生成（モック）"):
        st.markdown("**外部調査例（モック）：**\n- 生成AIは顧客対応・ドキュメント生成・FAQ自動化などに活用されています。")

elif st.session_state.assistant_type == "faq":
    st.header("📚 社内FAQアシスタント")
    st.write("知りたい社内ルールや制度を入力してください。")
    faq_query = st.text_input("例：有給の申請方法")
    if st.button("回答を生成（モック）"):
        st.markdown("**FAQ回答（モック）：** 有給は人事システムから事前申請が必要です。")
