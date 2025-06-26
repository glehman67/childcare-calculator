import streamlit as st
from tuition_data import DATA  # Assuming tuition_data.py contains the DATA list


def get_tuition(care_type, age_group, household_size, income_level):
    for row in DATA:
        if (
            row["Care Type"] == care_type and
            row["Age Group"] == age_group and
            row["Household Size"] == household_size and
            row["Income Level"] == income_level
        ):
            return row["Tuition"]
    return None

st.title("Rangeley Child Care Center Tuition Estimator")
st.markdown("""
#### This form will provide an <u>**approximate**</u> weekly tuition at Rangeley Child Care Center (RCCC). Tuition is calculated using a sliding scale based on type of care, child age, household size, and gross household income. Please note that there may be other benefits available to lower the tuition.  

#### If you qualify for Maine CCAP benefits, the amount of child care fees a family pays WILL NOT EXCEED 10% OF THE FAMILY’S GROSS ANNUAL INCOME FOR ALL CHILDREN IN CHILD CARE.
#### This is only an estimate and is subject to change upon formal enrollment.
""", unsafe_allow_html=True)

care_type = st.selectbox("Please select full-time or part-time child care:", ["Full-Time", "Part-Time"])
age_group = st.selectbox("Please select age group of child:", [
    "Infant - 6 Weeks to 12 months",
    "Toddler - 13 - 36 Months",
    "Pre-School - Over 36 Months"
])
household_size = st.selectbox("Total number of people in your household:", [2, 3, 4, 5, 6])
income_level = st.selectbox("Please select your gross household annual income:", [
    "Approximately $40K",
    "Approximately $60K",
    "Approximately $80K",
    "Approximately $100K",
    "Approximately $120K"
])

if st.button("Calculate Tuition"):
    tuition = get_tuition(care_type, age_group, household_size, income_level)
    if tuition is not None:
        st.success(f"Approximate Weekly Tuition: ${tuition}")
        # Extract X from income_level string
        import re
        match = re.search(r"\$(\d+)K", income_level)
        if match:
            x = int(match.group(1)) * 1000
            y = x * 0.1
            z = y / 52
            st.markdown(f"""
            <div style='background-color:#b3e5fc;padding:10px;border-radius:5px;color:#111;'>
            Based on your provided gross household annual income of <b>${x:,.0f}</b>, <u>if your family qualifies for Maine CCAP</u>, the MAXIMUM yearly amount your family will pay for child care fees is approximately <b>${y:,.0f}</b>, which equals <b>${z:,.2f}</b> per week, for ALL children in child care.  As stated above, this <u>may</u> be further reduced by other Maine benefits.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("No tuition data found for the selected options.")

st.markdown("""
---
Thank you for your interest in the Rangeley Child Care Center.  We look forward to further conversations about enrollment.
""")
