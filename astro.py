import streamlit as st
from groq import Groq


# ===================================
# GEMINI CONFIGURATION
# ===================================

client = Groq(
    api_key=st.secrets["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"]
)
GROQ_API_KEY="gsk_your_actual_key_here"

SYSTEM_INSTRUCTION = """
You are AstroAdvisor AI.

You are an expert astrology assistant.

When given birth details:

- Analyze personality
- Career
- Finance
- Relationships
- Marriage
- Health tendencies
- Strengths
- Challenges
- Spiritual outlook

Use headings and bullet points.

Keep responses simple and easy to understand.

Do not claim guaranteed future events.
"""

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(
    page_title="AstroAdvisor AI",
    page_icon="🔮",
    layout="wide"
)

# ===================================
# CUSTOM CSS
# ===================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.header-box{
    background: linear-gradient(135deg,#4c1d95,#7c3aed);
    padding:25px;
    border-radius:15px;
    text-align:center;
    color:white;
    margin-bottom:20px;
}

.metric-card{
    background:#f3f4f6;
    padding:10px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ===================================
# HEADER
# ===================================

st.markdown("""
<div class="header-box">
<h1>🔮 AstroAdvisor AI</h1>
<p>Your Personal Astrology Assistant</p>
</div>
""", unsafe_allow_html=True)

# ===================================
# SESSION STATE
# ===================================

if "report" not in st.session_state:
    st.session_state.report = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# ===================================
# SIDEBAR
# ===================================

with st.sidebar:

    st.header("🌟 Birth Details")

    name = st.text_input("Name")

    dob = st.date_input("Date of Birth")

    birth_time = st.time_input("Time of Birth")

    birthplace = st.text_input("Place of Birth")

   if st.button("🔮 Generate Prediction"):
 
prompt = f"""
Name: {name}
Date of Birth: {dob}
Time of Birth: {birth_time}
Place of Birth: {birthplace}
 
Provide:
 
1. Personality Analysis
2. Career Analysis
3. Financial Analysis
4. Marriage Analysis
5. Health Tendencies
6. Strengths
7. Challenges
8. Spiritual Outlook
"""
 
try:

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.5,
        max_tokens=2000
    )

    answer = response.choices[0].message.content

except Exception as e:

    answer = f"❌ Error: {e}"

    st.divider()

    st.markdown("### ⚡ Quick Questions")

    if st.button("💼 Career"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": "Tell me about my career."
            }
        )

    if st.button("💰 Wealth"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": "Tell me about my finances."
            }
        )

    if st.button("❤️ Marriage"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": "Tell me about marriage prospects."
            }
        )

    if st.button("🧘 Spirituality"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": "Tell me about my spiritual growth."
            }
        )

    st.divider()

    st.markdown("### 📖 Astrology FAQ")

    with st.expander("What is Astrology?"):
        st.write(
            "Astrology studies planetary positions and their symbolic influence."
        )

    with st.expander("What is Ascendant?"):
        st.write(
            "The zodiac sign rising on the eastern horizon at birth."
        )

    with st.expander("What is Moon Sign?"):
        st.write(
            "The zodiac sign occupied by the Moon at birth."
        )

    st.divider()

    if st.session_state.report:

        st.download_button(
            "📥 Download Report",
            st.session_state.report,
            file_name="astro_report.txt"
        )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.report = ""
        st.rerun()

# ===================================
# TABS
# ===================================

tab1, tab2 = st.tabs(
    [
        "📜 Astrology Report",
        "💬 Ask Astro AI"
    ]
)

# ===================================
# REPORT TAB
# ===================================

with tab1:

    if st.session_state.report:

        st.markdown(st.session_state.report)

    else:

        st.info(
            "Enter birth details and click Generate Prediction."
        )

# ===================================
# CHAT TAB
# ===================================

with tab2:

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input(
        "Ask anything about astrology..."
    )

    if user_prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(user_prompt)

        history = "\n".join(
            [
                f"{m['role']}: {m['content']}"
                for m in st.session_state.messages[-10:]
            ]
        )

        final_prompt = f"""
        Name: {name}
        Date of Birth: {dob}
        Time of Birth: {birth_time}
        Place of Birth: {birthplace}

        Existing Report:
        {st.session_state.report}

        Chat History:
        {history}

        User Question:
        {user_prompt}
        """

        with st.chat_message("assistant"):

            with st.spinner(
                "Consulting the stars..."
            ):

             try:

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.5,
        max_tokens=2000
    )

    answer = response.choices[0].message.content

except Exception as e:

    answer = f"❌ Error: {e}"

            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
