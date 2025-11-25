# scraper FUNCIONA, NOVIEMBRE 2025

import cloudscraper
import pandas as pd
import time
from fake_useragent import UserAgent
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from countries import AMAZON_DOMAINS


# -----------------------------------------------------
# CONFIGURACIÓN DEL SCRAPER
# -----------------------------------------------------
ua = UserAgent()
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)


# -----------------------------------------------------
# FUNCIÓN PARA PROCESAR EL PRECIO
# -----------------------------------------------------
def parse_price(whole, frac):
    """
    Convierte la parte entera y fraccionaria del precio en un float correcto.
    Ejemplo:
        whole = "1.234"
        frac = "56"
        -> 1234.56
    """
    try:
        whole_clean = whole.replace(",", "").replace(".", "")
        frac_clean = frac if frac else "00"
        return float(f"{whole_clean}.{frac_clean}")
    except:
        return None


# -----------------------------------------------------
# FUNCIÓN PRINCIPAL DE BÚSQUEDA
# -----------------------------------------------------
def search_amazon(keyword, country="USA", pages=2):
    """
    Busca productos en Amazon según palabra clave y país.
    Mantiene tu misma estructura y lógica original.
    """
    
    domain = AMAZON_DOMAINS[country]
    products = []
    keyword = keyword.replace(" ", "+")

    for page in range(1, pages + 1):

        url = f"https://www.{domain}/s?k={keyword}&page={page}"
        
        try:
            html = scraper.get(url, timeout=15).text
            soup = BeautifulSoup(html, "lxml")

            # Cada resultado de Amazon usa este contenedor
            items = soup.find_all("div", {"data-component-type": "s-search-result"})

            for item in items:
                try:
                    # -------------------------------
                    # TÍTULO
                    # -------------------------------
                    h2 = item.find("h2")
                    title = h2.get_text(strip=True) if h2 else "Sin título"

                    # -------------------------------
                    # PRECIO
                    # -------------------------------
                    price_whole = item.find("span", class_="a-price-whole")
                    price_frac = item.find("span", class_="a-price-fraction")

                    if price_whole:
                        price = parse_price(price_whole.text, price_frac.text if price_frac else "00")
                    else:
                        price = None

                    # -------------------------------
                    # LINK DEL PRODUCTO
                    # -------------------------------
                    link_tag = item.find("a", class_="a-link-normal s-no-outline")
                    href = link_tag.get("href") if link_tag else None
                    link = urljoin(f"https://www.{domain}", href) if href else ""

                    # -------------------------------
                    # GUARDAR RESULTADO
                    # -------------------------------
                    products.append({
                        "title": title,
                        "price": price,
                        "link": link
                    })

                except Exception as e:
                    print("Error procesando item:", e)
                    continue

            time.sleep(3)

        except Exception as e:
            print("Error procesando página:", e)
            continue

    if products:
        return pd.DataFrame(products)
    else:
        return pd.DataFrame()