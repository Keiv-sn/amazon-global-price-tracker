import streamlit as st
import pandas as pd
import plotly.express as px
from scraper import search_amazon
from countries import AMAZON_DOMAINS

st.set_page_config(page_title="Amazon Global Tracker", layout="wide")
st.title("Amazon Price Tracker - 11 países en vivo")

col1, col2 = st.columns(2)
keyword = col1.text_input("Producto", "iphone 15")
country = col2.selectbox("Amazon país", options=list(AMAZON_DOMAINS.keys()), index=0)

if st.button("Buscar precios"):
    with st.spinner("Buscando…"):
        df = search_amazon(keyword, country, pages=4)
    
    if not df.empty:
        st.success(f"{len(df)} productos encontrados en Amazon {country}")
        st.dataframe(df[["title", "price", "link"]], use_container_width=True)
        fig = px.histogram(df, x="price", title="Distribución de precios")
        st.plotly_chart(fig, use_container_width=True)
        st.download_button("Descargar CSV", df.to_csv(index=False).encode(), f"amazon_{keyword}_{country}.csv")
    else:
        st.error("No se encontraron productos. Prueba otra palabra.")