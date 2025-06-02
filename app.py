import streamlit as st

st.title('Health-Finance ML Predictor')
st.write('🚀 Predict health risk, insurance premium, and claims using ML.')

# Placeholder UI
age = st.slider('Age', 18, 100, 30)
income = st.number_input('Annual Income (in ₹)', min_value=10000, step=1000)

if st.button('Predict'):
    st.success('Prediction: ₹12,450 premium | Medium Risk')