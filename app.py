import streamlit as st

st.title("Prédition voiture d'occasion")

with st.form("car_form"):
    year = st.number_input("Année de fabrication", min_value=1900, max_value=2026, step=1)
    manufacturer = st.text_input("Marque du véhicule")
    odometer = st.number_input("Kilométrage (miles)", min_value=0, step=1000)
    price = st.number_input("Prix actuel ($)", min_value=0, step=100)

    submitted = st.form_submit_button("Prédire")
    if submitted:
        st.write(f"Année : {year}, Marque : {manufacturer}, Kilométrage : {odometer}, Prix : ${price}")
