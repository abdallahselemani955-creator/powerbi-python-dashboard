import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Kichwa cha Dashibodi kwenye mtandao
st.title("📊 Executive Business Performance Dashboard")
st.write("Dashibodi hii inasoma data za biashara moja kwa moja kupitia Wingu.")

# Kusoma faili la Excel
EXCEL_FILE = "mauzo_na_uchambuzi_biashara.xlsx"

try:
    df = pd.read_excel(EXCEL_FILE)
    
    if 'Faida' not in df.columns:
        df['Faida'] = df['Jumla_Mauzo'] - df['Gharama']

    # KPI Metrics juu kabisa
    total_sales = df['Jumla_Mauzo'].sum()
    total_profit = df['Faida'].sum()
    total_units = df['Idadi_Iliyouzwa'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Jumla ya Mauzo", f"TZS {total_sales:,.0f}")
    col2.metric("Jumla ya Faida", f"TZS {total_profit:,.0f}")
    col3.metric("Idadi Iliyouzwa", f"{total_units:,.0f} Pcs")

    st.markdown("---")

    # Chati ya Mwenendo wa Mwezi
    df['Tarehe'] = pd.to_datetime(df['Tarehe'])
    df['Mwezi_Mwaka'] = df['Tarehe'].dt.to_period('M').astype(str)
    monthly_summary = df.groupby('Mwezi_Mwaka')[['Jumla_Mauzo', 'Gharama']].sum().reset_index()

    st.subheader("Mwenendo wa Mauzo na Gharama kwa Kila Mwezi")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(monthly_summary['Mwezi_Mwaka'], monthly_summary['Jumla_Mauzo'] / 1e6, marker='o', color='#0078D4', label='Mauzo (M)')
    ax.plot(monthly_summary['Mwezi_Mwaka'], monthly_summary['Gharama'] / 1e6, marker='s', color='#D13438', label='Gharama (M)')
    ax.set_ylabel('Milioni TZS')
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)
    st.pyplot(fig)

    # Kuonyesha Jedwali la Data chini
    st.subheader("Orodha Kamili ya Data za Mauzo")
    st.dataframe(df)

except Exception as e:
    st.error(f"Hitilafu katika kusoma faili la Excel: {e}")