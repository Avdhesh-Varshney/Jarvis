import streamlit as st
import requests

def currencyConvertor():
    def get_exchange_rates():
        url = "https://api.frankfurter.app/currencies"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def convert_currency(amount, from_currency, to_currency):
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    st.title("Currency Converter")

    currencies = get_exchange_rates()

    if currencies:
        with st.form(key="currency_form"):
            amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
            from_currency = st.selectbox("From currency", options=currencies.keys())
            to_currency = st.selectbox("To currency", options=currencies.keys())
            submit_button = st.form_submit_button(label="Convert")

        if submit_button:
            conversion_result = convert_currency(amount, from_currency, to_currency)
            if conversion_result:
                rate = conversion_result["rates"][to_currency]
                st.success(f"{amount} {from_currency} = {rate} {to_currency}")
            else:
                st.error("Conversion failed. Please try again.")
    else:
        st.error("Failed to load currency data. Please try again later.")
