import streamlit as st

# Load the calculators based on selection
model_option = st.selectbox(
    'Pasirinkite skaičiuoklę arba analizę:',
    ['Altman Z modelis', 'Grigaravičiaus', 'Vertikali analizė']
)

if model_option == 'Altman Z modelis':
    import altman
    altman.run()

elif model_option == 'Grigaravičiaus':
    import grigaravicius
    grigaravicius.run()

elif model_option == 'Vertikali analizė':
    import vertical_analysis
    vertical_analysis.run()

