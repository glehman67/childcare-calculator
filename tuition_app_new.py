import streamlit as st

# Income eligibility thresholds for Child Care Affordability Program
INCOME_THRESHOLDS = {
    1: 73618.35,
    2: 96270.15,
    3: 118921.95,
    4: 141573.75,
    5: 164225.55,
    6: 186877.35,
    7: 191124.56,
    8: 195371.78,
    9: 199618.99,
    10: 203866.20
}

def check_eligibility(household_size, annual_income):
    """Check if family is eligible for child care subsidy"""
    if household_size in INCOME_THRESHOLDS:
        return annual_income <= INCOME_THRESHOLDS[household_size]
    return False

def calculate_parent_fee(annual_income, household_size, care_type):
    """Calculate annual parent fee based on income percentage and brackets, adjusted for care type"""
    if household_size not in INCOME_THRESHOLDS:
        return "Ineligible"
    
    max_income = INCOME_THRESHOLDS[household_size]
    income_percentage = annual_income / max_income
    
    # Fee calculation based on income percentage brackets (full-time rates)
    # Effective 10/19/2024 - All families must meet income guidelines of gross family income at or below 125% of Maine's State Median Income
    if 0 < income_percentage < 0.299:
        full_time_fee = 0
    elif 0.2999 <= income_percentage < 0.341:
        full_time_fee = annual_income * 0.01
    elif 0.341 <= income_percentage < 0.391:
        full_time_fee = annual_income * 0.02
    elif 0.391 <= income_percentage < 0.441:
        full_time_fee = annual_income * 0.03
    elif 0.441 <= income_percentage < 0.541:
        full_time_fee = annual_income * 0.04
    elif 0.541 <= income_percentage < 0.641:
        full_time_fee = annual_income * 0.05
    elif 0.641 <= income_percentage < 0.741:
        full_time_fee = annual_income * 0.06
    elif 0.741 <= income_percentage < 0.891:
        full_time_fee = annual_income * 0.07
    elif 0.891 <= income_percentage < 0.991:
        full_time_fee = annual_income * 0.08
    elif 0.991 <= income_percentage < 1.091:
        full_time_fee = annual_income * 0.09
    elif 1.091 <= income_percentage < 1.25:
        full_time_fee = annual_income * 0.10
    else:
        return "Ineligible"
    
    # The total amount of assessed fees to a family shall not exceed 10% of the family's gross income for all children
    max_fee = annual_income * 0.10
    if full_time_fee > max_fee:
        full_time_fee = max_fee
    
    # Adjust for part-time care (50% of full-time fee)
    if care_type == "Part-time":
        return full_time_fee * 0.5
    else:
        return full_time_fee

st.title("Rangeley Child Care Center")
st.subheader("Maine State Child Care Affordability Program (CCAP) Calculator")
st.markdown("""
#### The Maine State Child Care Affordability Program (CCAP) helps income eligible families pay for child care so that parents can work, go to school or participate in a job training program.

**Individuals eligible for child care subsidy from the Department of Health and Human Services, Child Care Affordability Program must comply with income eligibility criteria below.**

#### Please provide the following information for an estimate of your weekly parent co-pay:
""", unsafe_allow_html=True)

# Input fields
care_type = st.selectbox(
    "Please select your child care arrangement:",
    ["Full-time", "Part-time"],
    help="Choose whether you need full-time or part-time child care"
)

household_size = st.selectbox(
    "Total number of people in your household:",
    list(range(1, 11)),
    help="Include all family members living in your household"
)

annual_income = st.number_input(
    "Your approximate annual gross household income (USD):",
    min_value=0.0,
    value=50000.0,
    step=1000.0,
    format="%.2f",
    help="Enter your total gross annual household income"
)

st.markdown("""
**Note:** The above is only an estimate. Eligibility and weekly parent fee information is only available after applying to the CCAP. See the "To Apply" link below or [click here](https://som04.my.site.com/family/s/).
""")

if st.button("Calculate Eligibility and Weekly Parent Co-Pay"):
    if annual_income > 0:
        # Check eligibility
        is_eligible = check_eligibility(household_size, annual_income)
        
        st.markdown("---")
        
        if is_eligible:
            st.success("✅ Your family appears to be eligible for the Maine State Child Care Affordability Program (CCAP)!")
            
            # Calculate parent fee
            parent_fee = calculate_parent_fee(annual_income, household_size, care_type)
            
            if parent_fee == "Ineligible":
                st.warning("⚠️ Your income exceeds the maximum threshold for subsidy assistance.")
            elif parent_fee == 0:
                st.success("🎉 Your estimated annual parent co-pay is $0!")
                st.info("Your income qualifies you for the lowest fee bracket.")
            else:
                monthly_fee = parent_fee / 12
                weekly_fee = parent_fee / 52
                # Weekly fee assessments must be rounded down to the nearest dollar
                weekly_fee_rounded = int(weekly_fee)  # This rounds down
                
                st.markdown(f"""
                <div style='background-color:#e8f5e8;padding:20px;border-radius:10px;border-left:5px solid #4caf50;'>
                <h4 style='color:#2e7d32;margin-top:0;'>Your Estimated Parent Co-Pay ({care_type} Care):</h4>
                <ul style='color:#2e7d32;font-size:16px;'>
                <li><strong>Annual Co-Pay:</strong> ${parent_fee:,.2f}</li>
                <li><strong>Monthly Co-Pay:</strong> ${monthly_fee:,.2f}</li>
                <li><strong>Weekly Co-Pay:</strong> ${weekly_fee_rounded:,.0f} (rounded down to nearest dollar)</li>
                </ul>
                <p style='color:#2e7d32;font-style:italic;margin-top:15px;'>
                All assessed parent fees shall be paid directly to the caregiver by the parent.
                </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Show eligibility details
            max_income = INCOME_THRESHOLDS[household_size]
            income_percentage = (annual_income / max_income) * 100
            
            st.markdown(f"""
            <div style='background-color:rgba(128, 128, 128, 0.1);padding:15px;border-radius:5px;margin-top:15px;border:1px solid rgba(128, 128, 128, 0.3);'>
            <h5 style='color:inherit;'>Eligibility Details:</h5>
            <ul style='color:inherit;'>
            <li><strong>Household Size:</strong> {household_size} people</li>
            <li><strong>Your Gross Annual Income:</strong> ${annual_income:,.2f}</li>
            <li><strong>Maximum Income for Your Household Size:</strong> ${max_income:,.2f} (125% of Maine's State Median Income)</li>
            <li><strong>Income Percentage of Maximum:</strong> {income_percentage:.1f}%</li>
            <li><strong>Care Type:</strong> {care_type}</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            max_income = INCOME_THRESHOLDS[household_size]
            excess_income = annual_income - max_income
            
            st.error("❌ Your family does not qualify for the Maine State Child Care Affordability Program (CCAP).")
            st.markdown(f"""
            <div style='background-color:#ffebee;padding:15px;border-radius:5px;border-left:5px solid #f44336;'>
            <h5 style='color:#c62828;'>Eligibility Details:</h5>
            <ul style='color:#c62828;'>
            <li><strong>Your Gross Annual Income:</strong> ${annual_income:,.2f}</li>
            <li><strong>Maximum Income for Household Size {household_size}:</strong> ${max_income:,.2f} (125% of Maine's State Median Income)</li>
            <li><strong>Income Exceeds Limit by:</strong> ${excess_income:,.2f}</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Please enter a valid annual income amount.")

# Information section
st.markdown("""
---
### About the Maine State Child Care Affordability Program (CCAP)

**Funding Sources:**
- State Funds (SPSS)
- Fund for a Healthy Maine (FHM)  
- Child Care Development Funds (CCDF)
- Temporary Assistance to Needy Families (TANF)

**Income Eligibility:** All families must meet income guidelines of gross family income at or below 125% of Maine's State Median Income.

**Fee Assessment:** Fees are assessed to all families. For families with more than one child in care, the youngest child is always considered the first child enrolled. **The total amount of assessed fees to a family shall not exceed 10% of the family's gross income for all of their children.**

**Effective Date:** 10/19/2024

**Important Resources:**
- **Income Guidelines:** [Download PDF](https://www.maine.gov/dhhs/sites/maine.gov.dhhs/files/inline-files/10192024%20income%20guidelines.pdf)
- **To Apply:** [Apply Online](https://som04.my.site.com/family/s/)
- **Speak to Someone:** 1-877-680-5866
- **Email:** CCAP.DHHS@Maine.Gov
""")
