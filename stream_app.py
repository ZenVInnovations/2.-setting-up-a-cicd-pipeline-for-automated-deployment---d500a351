import pickle
import streamlit as st
import pandas as pd
from PIL import Image

# Load model and feature encoder
model_file = 'model_C=1.0.bin'
with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

# Load images
logo_image = 'Images/icone.png'
banner_image = 'Images/image.png'

def main():
    # Page configuration
    st.set_page_config(
        page_title="Customer Churn Prediction",
        page_icon=banner_image,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar
    with st.sidebar:
        st.image(banner_image, use_container_width=True)
        st.markdown("""
            ### Welcome to the Churn Prediction System
            - **AI-Powered Predictions**  
            - Predict churn for individual customers or upload a dataset.
        """)
        st.markdown("---")
        mode = st.selectbox("Select Prediction Mode:", ["Online Prediction", "Batch Prediction"])
        threshold = st.slider("Churn Risk Threshold", min_value=0.1, max_value=0.9, value=0.5, step=0.05)

    # Header
    st.image(logo_image, use_container_width=True, caption="AI-Powered Customer Insights")
    st.title("Customer Churn Prediction Dashboard")
    st.markdown("""
        **Leverage predictive analytics to prevent churn.**  
        Proactively identify customers likely to churn and take action.
    """)
    st.markdown("---")

    if mode == "Online Prediction":
        # Online Prediction Input
        st.header("Enter Customer Details")
        st.write("Fill in the form below to predict churn probability for a single customer.")
        
        # Input Form
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", ["male", "female"])
            seniorcitizen = st.selectbox("Senior Citizen", [0, 1])
            partner = st.selectbox("Has Partner", ["yes", "no"])
            dependents = st.selectbox("Has Dependents", ["yes", "no"])
            phoneservice = st.selectbox("Has Phone Service", ["yes", "no"])
            multiplelines = st.selectbox("Has Multiple Lines", ["yes", "no", "no_phone_service"])
            internetservice = st.selectbox("Internet Service", ["dsl", "no", "fiber_optic"])

        with col2:
            onlinesecurity = st.selectbox("Online Security", ["yes", "no", "no_internet_service"])
            onlinebackup = st.selectbox("Online Backup", ["yes", "no", "no_internet_service"])
            deviceprotection = st.selectbox("Device Protection", ["yes", "no", "no_internet_service"])
            techsupport = st.selectbox("Tech Support", ["yes", "no", "no_internet_service"])
            streamingtv = st.selectbox("Streaming TV", ["yes", "no", "no_internet_service"])
            streamingmovies = st.selectbox("Streaming Movies", ["yes", "no", "no_internet_service"])
            contract = st.selectbox("Contract Type", ["month-to-month", "one_year", "two_year"])
            paperlessbilling = st.selectbox("Paperless Billing", ["yes", "no"])
            paymentmethod = st.selectbox(
                "Payment Method", 
                ["bank_transfer_(automatic)", "credit_card_(automatic)", "electronic_check", "mailed_check"]
            )

        tenure = st.number_input("Tenure (Months)", min_value=0, max_value=240, value=0, step=1)
        monthlycharges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=3000.0, value=0.0, step=0.01)
        totalcharges = st.number_input(
            "Total Charges ($)", value=tenure * monthlycharges, step=0.01, help="Automatically calculated as Tenure * Monthly Charges."
        )

        # Prediction Button
        if st.button("Predict Churn"):
            # Prepare input dictionary
            input_dict = {
                "gender": gender,
                "seniorcitizen": seniorcitizen,
                "partner": partner,
                "dependents": dependents,
                "phoneservice": phoneservice,
                "multiplelines": multiplelines,
                "internetservice": internetservice,
                "onlinesecurity": onlinesecurity,
                "onlinebackup": onlinebackup,
                "deviceprotection": deviceprotection,
                "techsupport": techsupport,
                "streamingtv": streamingtv,
                "streamingmovies": streamingmovies,
                "contract": contract,
                "paperlessbilling": paperlessbilling,
                "paymentmethod": paymentmethod,
                "tenure": tenure,
                "monthlycharges": monthlycharges,
                "totalcharges": totalcharges,
            }

            # Predict churn probability
            X = dv.transform([input_dict])
            y_pred = model.predict_proba(X)[0, 1]
            churn = y_pred >= threshold

            # Display prediction
            st.markdown(f"### Prediction Result")
            st.write(f"**Churn Risk:** {'Yes' if churn else 'No'}")
            st.write(f"**Risk Score:** {y_pred:.2f}")

    elif mode == "Batch Prediction":
        # Batch Prediction
        st.header("Batch Predictions")
        st.write("Upload a CSV file with customer data for bulk predictions.")
        file_upload = st.file_uploader("Upload CSV File", type=["csv"])

        if file_upload:
            try:
                data = pd.read_csv(file_upload)

                # Standardize column names to lowercase for consistency
                data.columns = data.columns.str.lower().str.strip()

                # Ensure required columns exist
                required_columns = {"tenure", "monthlycharges"}
                missing_columns = required_columns - set(data.columns)
                if missing_columns:
                    st.error(f"Missing columns in the uploaded file: {', '.join(missing_columns)}")
                    st.stop()

                # Convert columns to numeric, handling errors
                data["tenure"] = pd.to_numeric(data["tenure"], errors="coerce").fillna(0)
                data["monthlycharges"] = pd.to_numeric(data["monthlycharges"], errors="coerce").fillna(0)

                # Calculate total charges if not already present
                if "totalcharges" not in data.columns:
                    data["totalcharges"] = data["tenure"] * data["monthlycharges"]

                # Handle any NaN values in data
                if data.isnull().any().any():
                    st.warning("Some rows contain invalid or missing data. These rows will be skipped.")
                    data = data.dropna()

                # Predict churn for the entire dataset
                X = dv.transform(data.to_dict(orient="records"))
                y_pred = model.predict_proba(X)[:, 1]
                data["churn risk"] = ["Yes" if risk >= threshold else "No" for risk in y_pred]
                data["risk score"] = y_pred

                # Display results
                st.success("Predictions completed successfully!")
                st.write(data)

                # Download predictions
                st.download_button(
                    label="Download Results",
                    data=data.to_csv(index=False),
                    file_name="churn_predictions.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
