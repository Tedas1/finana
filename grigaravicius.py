import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def run():
    st.title('Grigaravičiaus modelio skaičiuoklė')

    st.subheader('Formulė')

    grigar_formula = r'''
        \begin{aligned}
        Z = &\ -0.762 + 0.003 \cdot \frac{\text{Trumpalaikis turtas}}{\text{Trumpalaikiai įsipareigojimai}} \\
            &\ - 0.424 \cdot \frac{\text{Apyvartinis kapitalas}}{\text{Turtas}} \\
            &\ - 0.006 \cdot \frac{\text{Turtas}}{\text{Paprastųjų vardinių akcijų savininko nuosavybė}} \\
            &\ + 0.22 \cdot \frac{\text{Nuosavas kapitalas}}{\text{Įsipareigojimai}} \\
            &\ - 0.774 \cdot \frac{\text{Veiklos pelnas}}{\text{Palūkanos}} \\
            &\ - \left( -0.189 \cdot \frac{\text{Veiklos pelnas}}{\text{Pardavimų pajamos}} \right) \\
            &\ + 6.842 \cdot \frac{\text{Grynasis pelnas}}{\text{Turtas}} \\
            &\ - 12.262 \cdot \frac{\text{Pardavimų pajamos}}{\text{Apyvartinis kapitalas}} \\
            &\ - 5.257 \cdot \frac{\text{Pardavimų pajamos}}{\text{Turtas}}
        \end{aligned}
    '''
    st.latex(grigar_formula)

    # Input section
    st.subheader('Įmonių duomenys')
    num_companies = st.number_input("Įmonių skaičius", min_value=1, value=1, step=1)

    data = []
    for i in range(num_companies):
        st.subheader(f'Įmonė {i+1}')
        company = st.text_input(f"Įmonės pavadinimas (Company Name)", value=f"Įmonė {i+1}", key=f"company_{i}")
        short_term_assets = st.number_input(
            f"Trumpalaikis turtas (Short-Term Assets)", step=1000, key=f"short_term_assets_{i}"
        )
        short_term_liabilities = st.number_input(
            f"Trumpalaikiai įsipareigojimai (Short-Term Liabilities)", step=1000, key=f"short_term_liabilities_{i}"
        )
        working_capital = st.number_input(
            f"Apyvartinis kapitalas (Working Capital)", step=1000, key=f"working_capital_{i}"
        )
        total_assets = st.number_input(
            f"Turtas (Total Assets)", step=1000, key=f"total_assets_{i}"
        )
        owner_equity = st.number_input(
            f"Paprastųjų vardinių akcijų savininko nuosavybė (Owner's Equity of Common Shares)", step=1000, key=f"owner_equity_{i}"
        )
        equity_capital = st.number_input(
            f"Nuosavas kapitalas (Equity)", step=1000, key=f"equity_capital_{i}"
        )
        liabilities = st.number_input(
            f"Įsipareigojimai (Liabilities)", step=1000, key=f"liabilities_{i}"
        )
        operating_profit = st.number_input(
            f"Veiklos pelnas (Operating Profit)", step=1000, key=f"operating_profit_{i}"
        )
        interest = st.number_input(
            f"Palūkanos (Interest)", step=1000, key=f"interest_{i}"
        )
        sales_revenue = st.number_input(
            f"Pardavimų pajamos (Sales Revenue)", step=1000, key=f"sales_revenue_{i}"
        )
        net_profit = st.number_input(
            f"Grynasis pelnas (Net Profit)", step=1000, key=f"net_profit_{i}"
        )

        data.append({
            'Company': company,
            'Short-Term Assets': short_term_assets,
            'Short-Term Liabilities': short_term_liabilities,
            'Working Capital': working_capital,
            'Total Assets': total_assets,
            'Owner Equity': owner_equity,
            'Equity Capital': equity_capital,
            'Liabilities': liabilities,
            'Operating Profit': operating_profit,
            'Interest': interest,
            'Sales Revenue': sales_revenue,
            'Net Profit': net_profit
        })

    # Convert to DataFrame
    df = pd.DataFrame(data)

    def paint_axhlines(ax):
        ax.axhspan(1.8, 3, color='yellow', alpha=0.2, label='GREY')

    df['Z-score'] = -0.762 + 0.003 * df['Short-Term Assets'] / df['Short-Term Liabilities'] - 0.424 * df['Working Capital'] / df['Total Assets'] - 0.006 * df['Total Assets'] / df['Owner Equity'] + 0.22 * df['Equity Capital'] / df['Liabilities'] - 0.774 * df['Operating Profit'] / df['Interest'] - (-0.189 * df['Operating Profit'] / df['Sales Revenue']) + 6.842 * df['Net Profit'] / df['Total Assets'] - 12.262 * df['Sales Revenue'] / df['Working Capital'] - 5.257 * df['Sales Revenue'] / df['Total Assets']
    df['Tikimybinis įvykis'] = np.exp(df['Z-score']) / (1 + df['Z-score'])
    
    st.subheader('Rezultatas')

    st.write('Z reikšmė:', df['Z-score'])
    st.write('Tikimybinis įvykis:', df['Tikimybinis įvykis'])