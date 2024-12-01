import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def run():
    st.title('Altman Z modelio skaičiuoklė')

    st.subheader('Formulė')

    model_option = st.selectbox(
        'Pasirinkite Altman Z modelį:',
        ['Įmonių, kurių akcijos kotiruojamos vertybinių popierių biržoje', 
        'Įmonių, kurių akcijos nekotiruojamos vertybinių popierių biržoje',
        'Paslaugų ir individualių įmonių']
    )

    if model_option == 'Įmonių, kurių akcijos kotiruojamos vertybinių popierių biržoje':
        altman_formula = r'''Z = 1.2 \cdot X_1 + 1.4 \cdot X_2 + 3.3 \cdot X_3 + 0.6 \cdot X_4 + 1.0 \cdot X_5'''
    elif model_option == 'Įmonių, kurių akcijos nekotiruojamos vertybinių popierių biržoje':
        altman_formula = r'''Z = 0.717 \cdot X_1 + 0.847 \cdot X_2 + 3.107 \cdot X_3 + 0.420 \cdot X_4 + 0.995 \cdot X_5'''
    else:
        altman_formula = r'''Z = 6.56 \cdot X_1 + 3.26 \cdot X_2 + 6.72 \cdot X_3 + 1.05 \cdot X_4'''

    st.latex(altman_formula)

    # Input section
    st.subheader('Įmonių duomenys')
    num_companies = st.number_input("Įmonių skaičius", min_value=1, value=1, step=1)

    data = []
    for i in range(num_companies):
        st.subheader(f'Įmonė {i+1}')
        company = st.text_input(f"Įmonės pavadinimas (Company Name)", value=f"Įmonė {i+1}", key=f"company_{i}")
        working_capital = st.number_input(
            f"Apyvartinis kapitalas (Working Capital)", step=1000, key=f"working_capital_{i}"
        )
        total_assets = st.number_input(
            f"Turtas (Total Assets)", step=1000, key=f"total_assets_{i}"
        )
        retained_earnings = st.number_input(
            f"Nepaskirstytas pelnas (Retained Earnings)", step=1000, key=f"retained_earnings_{i}"
        )
        ebit = st.number_input(
            f"Pelnas iki apmokestinimo (EBIT)", step=1000, key=f"ebit_{i}"
        )
        if model_option == 'Įmonių, kurių akcijos kotiruojamos vertybinių popierių biržoje' or model_option == 'Paslaugų ir individualių įmonių':
            market_value_equity = st.number_input(
                f"Akcinio kapitalo rinkos vertė (Market Value of Equity)", step=1000, key=f"market_value_equity_{i}"
            )

        if model_option == 'Įmonių, kurių akcijos nekotiruojamos vertybinių popierių biržoje':
            equity_capital = st.number_input(
                f"Nuosavas kapitalas (Equity)", step=1000, key=f"equity_capital_{i}"
            )

        total_liabilities = st.number_input(
            f"Įsipareigojiimai (Total Liabilities)", step=1000, key=f"total_liabilities_{i}"
        )

        if model_option != 'Paslaugų ir individualių įmonių':
            sales = st.number_input(
                f"Pardavimo pajamos (Sales)", step=1000, key=f"sales_{i}"
            )

        if model_option == 'Įmonių, kurių akcijos kotiruojamos vertybinių popierių biržoje':
            data.append({
                'Company': company,
                'Working Capital': working_capital,
                'Total Assets': total_assets,
                'Retained Earnings': retained_earnings,
                'EBIT': ebit,
                'Market Value Equity': market_value_equity,
                'Total Liabilities': total_liabilities,
                'Sales': sales
            })
        elif model_option == 'Įmonių, kurių akcijos nekotiruojamos vertybinių popierių biržoje':
            data.append({
                'Company': company,
                'Working Capital': working_capital,
                'Total Assets': total_assets,
                'Retained Earnings': retained_earnings,
                'EBIT': ebit,
                'Equity': equity_capital,
                'Total Liabilities': total_liabilities,
                'Sales': sales
            })
        else:
            data.append({
                'Company': company,
                'Working Capital': working_capital,
                'Total Assets': total_assets,
                'Retained Earnings': retained_earnings,
                'EBIT': ebit,
                'Market Value Equity': market_value_equity,
                'Total Liabilities': total_liabilities,
            })




    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Calculate Z-Score Components
    def CalculateZValueByModel():
        if model_option == 'Įmonių, kurių akcijos kotiruojamos vertybinių popierių biržoje':
            df['X1'] = df['Working Capital'] / df['Total Assets']
            df['X2'] = df['Retained Earnings'] / df['Total Assets']
            df['X3'] = df['EBIT'] / df['Total Assets']
            df['X4'] = df['Market Value Equity'] / df['Total Liabilities']
            df['X5'] = df['Sales'] / df['Total Assets']
            df['Z-Score'] = 1.2 * df['X1'] + 1.4 * df['X2'] + 3.3 * df['X3'] + 0.6 * df['X4'] + 1.0 * df['X5']
        elif model_option == 'Įmonių, kurių akcijos nekotiruojamos vertybinių popierių biržoje':
            df['X1'] = df['Working Capital'] / df['Total Assets']
            df['X2'] = df['Sales'] / df['Total Assets']
            df['X3'] = df['EBIT'] / df['Total Assets']
            df['X4'] = df['Equity'] / df['Total Liabilities']
            df['X5'] = df['Retained Earnings'] / df['Total Assets']
            df['Z-Score'] = 0.717 * df['X1'] + 0.847 * df['X2'] + 3.107 * df['X3'] + 0.420 * df['X4'] + 0.995 * df['X5']
        else:
            df['X1'] = df['Working Capital'] / df['Total Assets']
            df['X2'] = df['Retained Earnings'] / df['Total Assets']
            df['X3'] = df['EBIT'] / df['Total Assets']
            df['X4'] = df['Market Value Equity'] / df['Total Liabilities']
            df['Z-Score'] = 6.56 * df['X1'] + 3.26 * df['X2'] + 6.72 * df['X3'] + 1.05 * df['X4']

    CalculateZValueByModel()

    # Add Risk Category
    def categorize_zscore(z):
        if model_option == 'Įmonių, kurių akcijos kotiruojamos vertybinių popierių biržoje':
            if z > 3.00:
                return 'Labai maža'
            elif 2.8 <= z <= 2.99:
                return 'Bankrotas galimas'
            elif 1.8 < z <= 2.79:
                return 'Didelė'
            else:
                return 'Labai didelė'
        elif model_option == 'Įmonių, kurių akcijos nekotiruojamos vertybinių popierių biržoje':
            if z > 2.9:
                return "Labai maža"
            elif 1.23 <= z <= 2.90:
                return "Bankrotas įmanomas"
            else:
                return "Labai didelė"
        else:
            if z > 2.6:
                return "Labai maža"
            elif 1.1 <= z <= 2.59:
                return "Bankrotas įmanomas"
            else:
                return "Labai didelė"

    def paint_axhlines(ax):
        if model_option == 'Įmonių, kurių akcijos kotiruojamos vertybinių popierių biržoje':
            ax.axhline(3, color='green', linestyle='--', label='Saugi zona')
            ax.axhline(1.8, color='red', linestyle='--', label='Pavojinga zona')
            ax.axhspan(1.8, 3, color='yellow', alpha=0.2, label='Galimas bankrotas')
        elif model_option == 'Įmonių, kurių akcijos nekotiruojamos vertybinių popierių biržoje':
            ax.axhline(2.9, color='green', linestyle='--', label='Saugi zona')
            ax.axhline(1.23, color='red', linestyle='--', label='Pavojinga zona')
            ax.axhspan(1.23, 2.9, color='yellow', alpha=0.2, label='Galimas bankrotas')
        else:
            ax.axhline(2.6, color='green', linestyle='--', label='Saugi zona')
            ax.axhline(1.1, color='red', linestyle='--', label='Pavojinga zona')
            ax.axhspan(1.1, 2.59, color='yellow', alpha=0.2, label='Galimas bankrotas')

    df['Bankroto tikimybė'] = df['Z-Score'].apply(categorize_zscore)

    cols = ['Bankroto tikimybė'] + [col for col in df if col != 'Bankroto tikimybė']
    df = df[cols]

    st.subheader('Rezultatas')

    st.write('Suskaičiuoti duomenys:', df)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df['Company'], df['Z-Score'], color='lightgrey')


    paint_axhlines(ax)
    ax.set_title('Altman Z modelis')
    ax.set_ylabel('Z-reikšmė')
    ax.legend()

    st.pyplot(fig)
