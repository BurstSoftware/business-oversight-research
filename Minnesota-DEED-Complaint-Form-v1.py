import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

st.set_page_config(
    page_title="MN DEED Complaint Form",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Minnesota DEED Complaint Form")
st.markdown("""
Use this form to prepare a complaint for submission to the  
**Minnesota Department of Employment and Economic Development (DEED)**.

⚠️ This app does **not** automatically submit the complaint.
You will be able to **download your complaint** and submit it per DEED instructions.
""")

st.divider()

# -----------------------------
# Complaint Form
# -----------------------------
with st.form("complaint_form"):
    st.subheader("Complainant Information")

    full_name = st.text_input("Full Name *")
    email = st.text_input("Email Address *")
    phone = st.text_input("Phone Number")
    address = st.text_area("Mailing Address")

    st.subheader("Business / Organization Being Complained About")

    business_name = st.text_input("Business or Organization Name *")
    business_address = st.text_area("Business Address")
    business_phone = st.text_input("Business Phone Number")

    st.subheader("Complaint Details")

    complaint_type = st.selectbox(
        "Type of Complaint *",
        [
            "Select one",
            "Fraud or Misrepresentation",
            "Unfair Business Practices",
            "Licensing Issue",
            "Grant or Loan Misuse",
            "Other"
        ]
    )

    incident_date = st.date_input("Date of Incident")
    complaint_description = st.text_area(
        "Describe the Complaint in Detail *",
        height=200
    )

    submitted = st.form_submit_button("Submit Complaint")

# -----------------------------
# Validation
# -----------------------------
if submitted:
    if not all([
        full_name,
        email,
        business_name,
        complaint_description,
        complaint_type != "Select one"
    ]):
        st.error("Please complete all required fields marked with *.")
    else:
        st.success("Complaint completed successfully!")

        # -----------------------------
        # Store Complaint Data
        # -----------------------------
        complaint_data = {
            "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Full Name": full_name,
            "Email": email,
            "Phone": phone,
            "Address": address,
            "Business Name": business_name,
            "Business Address": business_address,
            "Business Phone": business_phone,
            "Complaint Type": complaint_type,
            "Incident Date": incident_date.strftime("%Y-%m-%d"),
            "Complaint Description": complaint_description
        }

        df = pd.DataFrame([complaint_data])

        # -----------------------------
        # Download as CSV
        # -----------------------------
        st.download_button(
            label="⬇️ Download Complaint (CSV)",
            data=df.to_csv(index=False),
            file_name="mn_deed_complaint.csv",
            mime="text/csv"
        )

        # -----------------------------
        # Generate PDF
        # -----------------------------
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)

        pdf.cell(0, 10, "Minnesota DEED Complaint", ln=True)
        pdf.ln(5)

        for key, value in complaint_data.items():
            pdf.multi_cell(0, 8, f"{key}: {value}")
            pdf.ln(1)

        pdf_output = pdf.output(dest="S").encode("latin-1")

        st.download_button(
            label="⬇️ Download Complaint (PDF)",
            data=pdf_output,
            file_name="mn_deed_complaint.pdf",
            mime="application/pdf"
        )

        st.info("""
### Next Steps
Submit your downloaded complaint to the Minnesota Department of Employment and Economic Development (DEED):

- 🌐 Website: https://mn.gov/deed/
- 📧 Email or mail as instructed by the relevant DEED division
- 📎 Attach any supporting documentation

Keep a copy for your records.
""")
