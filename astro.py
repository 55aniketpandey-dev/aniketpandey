import streamlit as st
from groq import Groq

# ==========================
# GROQ CONFIG
# ==========================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

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

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AstroAdvisor AI",
    page_icon="🔮",
    layout="wide"
)

# ==========================
# SESSION STATE
# ==========================

if "report" not in st.session_state:
    st.session_state.report = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================
# HEADER
# ==========================

st.title("🔮 AstroAdvisor AI")
st.subheader("Your Personal Astrology Assistant")

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.header("🌟 Birth Details")

    name = st.text_input("Name")
    dob = st.date_input("Date of Birth")
    birth_time = st.time_input("Time of Birth")
    birthplace = st.text_input("Place of Birth")

    if st.button("🔮 Generate Prediction"):

        prompt = f"""
        Name: {name}
        Date Of Birth: {dob}
        Time Of Birth: {birth_time}
        Place Of Birth: {birthplace}

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
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )

            answer = response.choices[0].message.content

            st.session_state.report = answer

        except Exception as e:
            st.error(f"Error: {e}")

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

# ==========================
# TABS
# ==========================

tab1, tab2 = st.tabs(
    ["📜 Astrology Report", "💬 Ask Astro AI"]
)

# ==========================
# REPORT TAB
# ==========================

with tab1:

    if st.session_state.report:
        st.markdown(st.session_state.report)
    else:
        st.info("Enter birth details and click Generate Prediction.")

# ==========================
# CHAT TAB
# ==========================

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
        Date Of Birth: {dob}
        Time Of Birth: {birth_time}
        Place Of Birth: {birthplace}

        Existing Report:
        {st.session_state.report}

        Chat History:
        {history}

        User Question:
        {user_prompt}
        """

        with st.chat_message("assistant"):

            with st.spinner("Consulting the stars..."):

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
