import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Dropout Risk Analyzer", page_icon="🎓", layout="centered")

st.title("🎓 Student Dropout Risk Analyzer")
st.caption("Education – Data Mining prototype for identifying students who may need early academic support.")

st.info(
    "This is an educational prototype using user-entered/synthetic-style indicators. "
    "It is not a validated institutional decision system and should not be used to punish or exclude students."
)

st.subheader("Enter Student Indicators")

attendance = st.slider("Attendance (%)", 0, 100, 75)
marks = st.slider("Average Academic Score (%)", 0, 100, 60)
assignments = st.slider("Assignments Completed (%)", 0, 100, 70)
study_hours = st.slider("Average Study Hours per Day", 0.0, 10.0, 2.5, 0.5)
failed_subjects = st.number_input("Number of Failed / Backlog Subjects", min_value=0, max_value=10, value=0)
engagement = st.slider("Class Engagement (1 = very low, 5 = very high)", 1, 5, 3)

def analyse_risk(attendance, marks, assignments, study_hours, failed_subjects, engagement):
    score = 0
    reasons = []

    if attendance < 60:
        score += 3
        reasons.append("Very low attendance")
    elif attendance < 75:
        score += 2
        reasons.append("Attendance needs improvement")
    elif attendance < 85:
        score += 1

    if marks < 40:
        score += 3
        reasons.append("Very low academic score")
    elif marks < 55:
        score += 2
        reasons.append("Academic score needs support")
    elif marks < 65:
        score += 1

    if assignments < 50:
        score += 2
        reasons.append("Low assignment completion")
    elif assignments < 70:
        score += 1

    if study_hours < 1:
        score += 2
        reasons.append("Very low self-study time")
    elif study_hours < 2:
        score += 1

    if failed_subjects >= 3:
        score += 3
        reasons.append("Multiple failed/backlog subjects")
    elif failed_subjects >= 1:
        score += 2
        reasons.append("Failed/backlog subject present")

    if engagement <= 2:
        score += 2
        reasons.append("Low class engagement")
    elif engagement == 3:
        score += 1

    if score >= 9:
        risk = "HIGH"
    elif score >= 5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return score, risk, reasons

if st.button("Analyse Dropout Risk", type="primary"):
    score, risk, reasons = analyse_risk(
        attendance, marks, assignments, study_hours, failed_subjects, engagement
    )

    st.subheader("Analysis Result")
    if risk == "HIGH":
        st.error(f"Risk Level: {risk}")
    elif risk == "MEDIUM":
        st.warning(f"Risk Level: {risk}")
    else:
        st.success(f"Risk Level: {risk}")

    st.metric("Risk Score", f"{score}/15")

    st.write("**Indicators requiring attention:**")
    if reasons:
        for reason in reasons:
            st.write(f"- {reason}")
    else:
        st.write("- No major risk indicator detected.")

    st.write("**Suggested early interventions:**")
    suggestions = []
    if attendance < 75:
        suggestions.append("Attendance mentoring and follow-up")
    if marks < 55 or failed_subjects > 0:
        suggestions.append("Academic counselling, tutoring, and remedial support")
    if assignments < 70:
        suggestions.append("Assignment tracking with weekly targets")
    if study_hours < 2:
        suggestions.append("Structured study plan and time-management support")
    if engagement <= 2:
        suggestions.append("Mentor interaction and participation-focused activities")
    if not suggestions:
        suggestions.append("Continue regular monitoring and positive academic support")

    for item in suggestions:
        st.write(f"- {item}")

st.divider()
st.caption(
    "Purpose: To demonstrate how simple educational indicators can support early identification "
    "and timely intervention. Human review should always be used for real student support decisions."
)
