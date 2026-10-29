import joblib
import json
import numpy as np
import pandas as pd
import streamlit as st

with open('data/options.json', 'r') as f:
    options = json.load(f)

model = joblib.load('data/model.pkl')

CURRENT_YEAR = 2026
YEAR_MEAN = 2011.167249647705

def prepare_input(year, manufacturer, odometer, fuel, transmission, title_status, car_type, state):
    odometer_log = np.log1p(odometer)
    year_centered = year - YEAR_MEAN
    data = {
        'year': year,
        'odometer': odometer_log,
        'year_squared': year_centered ** 2,
        'odometer_squared': odometer_log ** 2,
        'car_age': CURRENT_YEAR - year,
        'age_odometer_interaction': year * odometer_log,
    }

    for m in options['manufacturers']:
        data[f'manufacturer_{m}'] = int(manufacturer == m)

    for f in options['fuels']:
        data[f'fuel_{f}'] = int(fuel == f)

    for t in options['transmissions']:
        data[f'transmission_{t}'] = int(transmission == t)

    for ts in options['title_status']:
        data[f'title_status_{ts}'] = int(title_status == ts)

    for tp in options['types']:
        data[f'type_{tp}'] = int(car_type == tp)

    for s in options['states']:
        data[f'state_{s}'] = int(state == s)

    return pd.DataFrame([data])


st.title("Prédition voiture d'occasion")

with st.form("car_form"):
    year = st.number_input("Année de fabrication", min_value=1900, max_value=2026, step=1)
    manufacturer = st.selectbox("Marque du véhicule", options["manufacturers"])
    odometer = st.number_input("Kilométrage (miles)", min_value=0, step=1000)
    fuel = st.selectbox("Carburant", options["fuels"])
    transmission = st.selectbox("Transmission", options["transmissions"])
    title_status = st.selectbox("Statut du titre", options["title_status"])
    car_type = st.selectbox("Type de véhicule", options["types"])
    state = st.selectbox("État (US)", options["states"])

    submitted = st.form_submit_button("Prédire")

if submitted:
    car = prepare_input(year, manufacturer, odometer, fuel, transmission, title_status, car_type, state)
    pred_log = model.predict(car)[0]
    pred_price = np.expm1(pred_log)
    st.subheader("Résultat de la prédiction")
    st.success(f"Prix estimé : ${pred_price:,.2f}")
