import streamlit as st

# Load the calculators based on selection
model_option = st.selectbox(
    'Pasirinkite skaičiuoklę:',
    ['Altman Z modelis', 'Grigaravičiaus']
)

if model_option == 'Altman Z modelis':
    # Import and run Altman Z model calculator
    import altman
    altman.run()  # Assuming the run() function starts the Altman Z calculator

elif model_option == 'Grigaravičiaus':
    # Import and run Grigaravičiaus model calculator
    import grigaravicius
    grigaravicius.run()  # Assuming the run() function starts the Grigaravičiaus calculator