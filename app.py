# En la función obtener_datos_financieros, modifica la parte de dividendos:
def obtener_datos_financieros(tk, Tc_def):
    try:
        # ... (código existente)
        
        # Dividendos - cálculo mejorado
        div_yield = info.get("dividendYield")
        payout = info.get("payoutRatio")
        
        # Calcular el dividendo anual por acción
        dividend_rate = info.get("dividendRate")  # Dividendo anual por acción
        if dividend_rate is None:
            # Si no está disponible, calcularlo manualmente
            last_dividend = info.get("lastDividendValue")
            if last_dividend and price:
                # Asumir que es trimestral (común en EE.UU.)
                dividend_rate = last_dividend * 4
            else:
                dividend_rate = None
        
        # Calcular significado: $ por cada $100 invertidos
        div_significado = None
        if dividend_rate and price:
            div_significado = f"${dividend_rate / price * 100:.2f} anual por cada $100 invertidos"
        elif div_yield and price:
            div_significado = f"${div_yield * 100:.2f} anual por cada $100 invertidos"
        
        return {
            # ... (campos existentes)
            "Dividend Yield %": div_yield,
            "Dividend Significado": div_significado,  # Nueva columna
            "Payout Ratio": payout,
            # ... (resto de campos)
        }
    except Exception as e:
        st.error(f"Error obteniendo datos para {tk}: {str(e)}")
        return None

# En la sección de formateo para visualización, agrega:
def main():
    # ... (código existente)
    
    # Formatear valores para visualización
    df_disp = df.copy()
    
    # Nueva columna para el significado del dividendo (no necesita formateo adicional)
    df_disp["Dividend Significado"] = df["Dividend Significado"].fillna("N/D")
    
    # ... (resto del formateo existente)

# En la tabla principal, agrega la nueva columna:
st.dataframe(
    df_disp[[
        "Ticker", "Nombre", "País", "Industria", "Sector",
        "Precio", "P/E", "P/B", "P/FCF",
        "Dividend Yield %", "Dividend Significado", "Payout Ratio", "ROA", "ROE",  # Agregada nueva columna
        "Current Ratio", "Debt/Eq", "Oper Margin", "Profit Margin",
        "WACC", "ROIC", "Creacion Valor (Wacc vs Roic)", "MarketCap"
    ]],
    use_container_width=True,
    height=500
)

# En el análisis individual, también puedes mostrar esta información:
st.header("🔍 Análisis por Empresa")
pick = st.selectbox("Selecciona empresa", df_disp["Ticker"].unique())
det_disp = df_disp[df_disp["Ticker"] == pick].iloc[0]
det_raw = df[df["Ticker"] == pick].iloc[0]

# ... (código existente)

with cC:
    st.metric("ROE", det_disp["ROE"])
    st.metric("Dividend Yield", det_disp["Dividend Yield %"])
    st.metric("Dividend por $100", det_disp["Dividend Significado"].split(" ")[0])  # Solo el valor numérico
    st.metric("Current Ratio", det_disp["Current Ratio"])
    st.metric("Debt/Eq", det_disp["Debt/Eq"])
