import streamlit as st
import pandas as pd

# Load the provided CSV (assuming it has a 'group_id' column)
df = pd.read_csv('spark_interview_questions.csv')

st.title("🚀 Spark Interview Grouped Interleaved Practice")

# Sidebar dropdown: Select a group ID
group_ids = df['id'].unique()
selected_group_id = st.sidebar.selectbox("🔍 Select a Group ID:", group_ids)

# Filter all questions under this group (same 'id')
group_questions = df[df['id'] == selected_group_id]

# Show selected group header
st.header(f"📝 Practice Questions for Group ID {selected_group_id}")

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'asked' not in st.session_state:
    st.session_state.asked = set()

# Display all questions under the selected group
for idx, q in group_questions.iterrows():
    if idx in st.session_state.asked:
        continue

    st.subheader(f"❓ {q['question']}")
    user_answer = ""

    if q['type'] == 'MCQ':
        options = q['options'].split(';')
        user_answer = st.radio("Choose one:", options, key=f"q{idx}")
    elif q['type'] in ['Fill', 'Scenario']:
        user_answer = st.text_input("Your answer:", key=f"q{idx}")
    elif q['type'] == 'TrueFalse':
        user_answer = st.radio("True or False:", ['True', 'False'], key=f"q{idx}")

    if st.button(f"Check Answer {idx}"):
        st.session_state.total += 1
        correct_answer = str(q['answer']).strip().lower()
        user_response = str(user_answer).strip().lower()

        if user_response == correct_answer:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Correct answer: {q['answer']}")

        st.session_state.asked.add(idx)
        st.experimental_rerun()

# Final score summary
if st.session_state.total > 0:
    st.write(f"### 🌟 Score: {st.session_state.score} / {st.session_state.total}")
