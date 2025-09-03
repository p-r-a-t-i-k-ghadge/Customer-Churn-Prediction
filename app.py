import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("churn_model.pkl")

st.title("Customer Churn Prediction App")
st.write("Enter customer details to predict churn:")

# Collect raw inputs
gender = st.selectbox("Gender", ["Male", "Female"])
senior_citizen = st.selectbox("Senior Citizen (0 = No, 1 = Yes)", [0, 1])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["Yes", "No"])
tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=12)
phone_service = st.selectbox("Phone Service", ["Yes", "No"])
multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])
contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
payment_method = st.selectbox("Payment Method", [
    "Electronic check", 
    "Mailed check", 
    "Bank transfer (automatic)", 
    "Credit card (automatic)"
])
monthly_charges = st.number_input("Monthly Charges", min_value=0.0, max_value=200.0, value=50.0)
total_charges = st.number_input("Total Charges", min_value=0.0, max_value=10000.0, value=1000.0)

# ---- Encoding exactly as training ----
gender = 0 if gender == "Female" else 1
partner = 1 if partner == "Yes" else 0
dependents = 1 if dependents == "Yes" else 0
phone_service = 1 if phone_service == "Yes" else 0
paperless_billing = 1 if paperless_billing == "Yes" else 0

multiple_lines_map = {"No":0, "Yes":1, "No phone service":2}
internet_service_map = {"DSL":0, "Fiber optic":1, "No":2}
online_security_map = {"No":0, "Yes":1, "No internet service":2}
online_backup_map = {"No":0, "Yes":1, "No internet service":2}
device_protection_map = {"No":0, "Yes":1, "No internet service":2}
tech_support_map = {"No":0, "Yes":1, "No internet service":2}
streaming_tv_map = {"No":0, "Yes":1, "No internet service":2}
streaming_movies_map = {"No":0, "Yes":1, "No internet service":2}
contract_map = {"Month-to-month":0, "One year":1, "Two year":2}
payment_method_map = {
    "Electronic check":0, 
    "Mailed check":1, 
    "Bank transfer (automatic)":2, 
    "Credit card (automatic)":3
}

multiple_lines = multiple_lines_map[multiple_lines]
internet_service = internet_service_map[internet_service]
online_security = online_security_map[online_security]
online_backup = online_backup_map[online_backup]
device_protection = device_protection_map[device_protection]
tech_support = tech_support_map[tech_support]
streaming_tv = streaming_tv_map[streaming_tv]
streaming_movies = streaming_movies_map[streaming_movies]
contract = contract_map[contract]
payment_method = payment_method_map[payment_method]

# ---- Arrange in same column order as training ----
features = pd.DataFrame([[
    gender, senior_citizen, partner, dependents, tenure,
    phone_service, multiple_lines, internet_service, online_security,
    online_backup, device_protection, tech_support, streaming_tv,
    streaming_movies, contract, paperless_billing, payment_method,
    monthly_charges, total_charges
]])

# Predict button
if st.button("Predict Churn"):
    prediction = model.predict(features)
    result = "Customer is LIKELY to churn." if prediction[0] == 1 else "Customer is NOT likely to churn."
    st.success(result)
