"""AI Career Guidance Chatbot - main Streamlit app.

Run with:  streamlit run app.py

This file only builds the web page. The real work is done by the helper
modules in the utils/ folder:
    utils/validators.py   -> checks what the student typed
    utils/recommender.py  -> scores careers and writes the explanations
    utils/feedback.py     -> saves feedback to data/feedback.csv
"""

# ---------------------------------------------------------------------------
# SECTION 1: Imports
# ---------------------------------------------------------------------------
import streamlit as st

from utils.feedback import load_feedback_summary, save_feedback
from utils.recommender import (
    EDUCATION_LEVELS,
    GOALS,
    INTERESTS,
    SKILLS,
    load_careers,
    recommend_careers,
)
from utils.validators import (
    validate_age,
    validate_feedback_comment,
    validate_name,
    validate_rating,
    validate_selection,
)

# ---------------------------------------------------------------------------
# SECTION 2: Page settings (must be the first Streamlit command that runs)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Career Guidance",
    page_icon="🎓",
    layout="wide",
)

# ---------------------------------------------------------------------------
# SECTION 3: Custom styling (CSS) for the colourful header banner
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
.hero {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 1.5rem;
}
.hero h1 { margin: 0; font-size: 2.2rem; color: white; }
.hero p  { margin: 0.4rem 0 0 0; font-size: 1.05rem; opacity: 0.92; }
</style>
"""


# ---------------------------------------------------------------------------
# SECTION 4: Loading the career data
# ---------------------------------------------------------------------------
@st.cache_data
def get_careers():
    """Read data/careers.json once and remember it.

    Streamlit re-runs this whole file every time the student clicks something.
    @st.cache_data stops us from re-reading the file on every click.
    """
    return load_careers()


# ---------------------------------------------------------------------------
# SECTION 5: Page pieces (header and sidebar)
# ---------------------------------------------------------------------------
def render_header():
    """Show the gradient banner at the top of the page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hero">
            <h1>🎓 AI Career Guidance Chatbot</h1>
            <p>Tell us about yourself and get personalised career paths and courses.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Show the left sidebar: about text, steps, rating and a restart button."""
    with st.sidebar:
        st.header("About")
        st.write(
            "This tool compares your interests, skills and education with a "
            "career database and explains why each career could suit you."
        )
        st.markdown("**How it works**")
        st.markdown("1. Fill in your profile\n2. Get your top 3 matches\n3. Share feedback")

        # Show the average student rating, but only if feedback exists
        count, average = load_feedback_summary()
        if count:
            st.divider()
            st.metric("Student rating", f"{average:.1f} / 5", help=f"{count} responses")

        # Let the student clear old results and begin again
        if "results" in st.session_state:
            st.divider()
            if st.button("Start over"):
                st.session_state.pop("results", None)
                st.session_state.pop("profile", None)
                st.rerun()


# ---------------------------------------------------------------------------
# SECTION 6: The questions form
# ---------------------------------------------------------------------------
def render_profile_form():
    """Show the questions. Returns the answers when submitted, otherwise None."""
    with st.chat_message("assistant"):
        st.write(
            "Hi! 👋 I'm your career guide. Answer a few quick questions and "
            "I'll suggest careers and courses that fit you."
        )

    # A form groups all inputs so nothing runs until the button is pressed
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Your name", max_chars=50)
        age = col2.number_input("Your age", min_value=0, max_value=100, value=18, step=1)

        education = st.selectbox("Current education level", EDUCATION_LEVELS)
        interests = st.multiselect("Your interests (pick 1-4)", INTERESTS)
        skills = st.multiselect("Your skills (pick 1-6)", SKILLS)
        goal = st.selectbox("Your main career goal", GOALS)

        submitted = st.form_submit_button("Get my career guidance", type="primary")

    if not submitted:
        return None

    return {
        "name": name,
        "age": age,
        "education": education,
        "interests": interests,
        "skills": skills,
        "goal": goal,
    }


# ---------------------------------------------------------------------------
# SECTION 7: Input validation
# ---------------------------------------------------------------------------
def validate_profile(profile):
    """Run every check and return a list of error messages.

    An empty list means everything is fine. Each validator returns
    (is_valid, message), so we keep the message of every failed check.
    """
    checks = [
        validate_name(profile["name"]),
        validate_age(profile["age"]),
        validate_selection(profile["interests"], "interest", 1, 4),
        validate_selection(profile["skills"], "skill", 1, 6),
    ]
    return [message for is_valid, message in checks if not is_valid]


# ---------------------------------------------------------------------------
# SECTION 8: Showing the recommendations
# ---------------------------------------------------------------------------
def render_recommendations(results):
    """Show one card per recommended career."""
    st.subheader("Your top career matches")

    for rank, career in enumerate(results, start=1):
        with st.container(border=True):
            left, right = st.columns([4, 1])
            left.subheader(f"{rank}. {career['name']}")
            right.metric("Match", f"{career['score']}%")
            st.progress(career["score"] / 100)
            st.write(career["description"])

            st.markdown("**Why this fits you**")
            st.write(career["explanation"])

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**Recommended courses**")
                for course in career["courses"]:
                    st.markdown(f"- {course}")
            with col_b:
                st.markdown("**Skills to build**")
                if career["missing_skills"]:
                    for skill in career["missing_skills"]:
                        st.markdown(f"- {skill}")
                else:
                    st.markdown("You already have all the core skills! 🎉")

            st.caption(f"Job outlook: {career['outlook']}")


# ---------------------------------------------------------------------------
# SECTION 9: Feedback form
# ---------------------------------------------------------------------------
def render_feedback_form(student_name):
    """Let the student rate the guidance and leave an optional comment."""
    st.divider()
    st.subheader("Was this helpful?")

    with st.form("feedback_form", clear_on_submit=True):
        rating = st.slider("Rate your experience (1 = poor, 5 = excellent)", 1, 5, 4)
        comment = st.text_area("Any comments? (optional, max 500 characters)")
        submitted = st.form_submit_button("Submit feedback")

    if not submitted:
        return

    # Validate first
    checks = [validate_rating(rating), validate_feedback_comment(comment)]
    errors = [message for is_valid, message in checks if not is_valid]
    if errors:
        for message in errors:
            st.error(message)
        return

    # Then save, and show a friendly message if saving fails
    try:
        save_feedback(student_name, rating, comment)
        st.success("Thank you for your feedback! 🙏")
    except RuntimeError as error:
        st.error(str(error))


# ---------------------------------------------------------------------------
# SECTION 10: main() - puts everything together in order
# ---------------------------------------------------------------------------
def main():
    render_header()
    render_sidebar()

    # Step 1: load the career data. If it is missing or broken, explain why.
    try:
        careers = get_careers()
    except (FileNotFoundError, ValueError) as error:
        st.error(f"Could not load career data: {error}")
        st.stop()

    # Step 2: show the questions
    profile = render_profile_form()

    # Step 3: when the student submits, validate then recommend
    if profile is not None:
        errors = validate_profile(profile)
        if errors:
            for message in errors:
                st.error(message)
        else:
            profile["name"] = profile["name"].strip()
            try:
                results = recommend_careers(profile, careers, top_n=3)
            except Exception as error:  # last safety net so the page never crashes
                st.error(f"Sorry, something went wrong while preparing your results: {error}")
            else:
                # session_state keeps results on screen when the page re-runs
                st.session_state["profile"] = profile
                st.session_state["results"] = results

    # Step 4: show results and the feedback form (if we have results)
    if "results" in st.session_state:
        name = st.session_state["profile"]["name"]
        with st.chat_message("assistant"):
            st.write(f"Thanks, {name}! Here are the careers that suit you best.")
        render_recommendations(st.session_state["results"])
        render_feedback_form(name)


main()