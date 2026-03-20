from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.encoding = r.apparent_encoding
        return BeautifulSoup(r.text, "html.parser")
    except:
        return None

def scrape_lagaceta():
    soup = fetch_soup("https://www.lagaceta.com.ar")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_eltucumano():
    soup = fetch_soup("https://www.eltucumano.com")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a, h4 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_infobae():
    soup = fetch_soup("https://www.infobae.com")
    if not soup: return []
    titles = []
    for tag in soup.select("h2, h3"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_lanacion():
    soup = fetch_soup("https://www.lanacion.com.ar")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_comunicaciontucuman():
    soup = fetch_soup("https://www.comunicaciontucuman.gob.ar")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a, h4 a, .titulo a, .entry-title a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_lv12():
    soup = fetch_soup("https://www.lv12.com.ar")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a, h4 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_ambito():
    soup = fetch_soup("https://www.ambito.com")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_cnt():
    soup = fetch_soup("https://www.cnt.com.ar")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a, h4 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_elsiglo():
    soup = fetch_soup("https://elsigloweb.com")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a, h4 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_losprimeros():
    soup = fetch_soup("https://www.losprimeros.tv")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a, h4 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_lv7():
    soup = fetch_soup("https://lv7.com.ar")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a, h4 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

def scrape_radiobicentenario():
    soup = fetch_soup("https://www.radiobicentenario.com.ar")
    if not soup: return []
    titles = []
    for tag in soup.select("h2 a, h3 a, h4 a"):
        t = tag.get_text(strip=True)
        if t and len(t) > 20 and t not in titles:
            titles.append(t)
        if len(titles) == 5: break
    return titles

SCRAPERS = {
    "La Gaceta":               scrape_lagaceta,
    "El Tucumano":             scrape_eltucumano,
    "Infobae":                 scrape_infobae,
    "La Nación":               scrape_lanacion,
    "Comunicación Tucumán":    scrape_comunicaciontucuman,
    "LV12":                    scrape_lv12,
    "Ámbito":                  scrape_ambito,
    "CNT":                     scrape_cnt,
    "El Siglo":                scrape_elsiglo,
    "Los Primeros":            scrape_losprimeros,
    "LV7":                     scrape_lv7,
    "Radio Bicentenario":      scrape_radiobicentenario,
}

@app.route("/noticias", methods=["GET"])
def noticias():
    resultado = {}
    for nombre, fn in SCRAPERS.items():
        try:
            titles = fn()
            resultado[nombre] = titles if titles else ["No se pudieron obtener títulos"]
        except:
            resultado[nombre] = ["Error al acceder al medio"]
    return jsonify(resultado)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Scraper de noticias activo"})

if __name__ == "__main__":
    app.run(debug=True)
