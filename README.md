# NDMI – Normalized Difference Moisture Index (Streamlit + Docker)

## Opis projektu

Aplikacja webowa wykonana w Pythonie z wykorzystaniem frameworka **Streamlit**,  
służąca do obliczania oraz wizualizacji wskaźnika  
**Normalized Difference Moisture Index (NDMI)** na podstawie danych satelitarnych.

Aplikacja obsługuje jednocześnie:
- dane rastrowe (Sentinel-2: B8, B11),
- dane wektorowe (GeoJSON),

oraz wykonuje analizę przestrzenną łącząc oba typy danych.

---

## Wzór matematyczny


$$NDMI = \frac{B8 - B11}{B8 + B11}$$


gdzie:
- **B8** – pasmo NIR (Near Infrared),
- **B11** – pasmo SWIR (Short-Wave Infrared).

Zakres wartości NDMI: **-1 do 1**.

---

## Funkcjonalności aplikacji

- obliczanie NDMI z danych rastrowych (rasterio),
- wizualizacja NDMI w stylu QGIS,
- obsługa danych wektorowych GeoJSON (geopandas),
- rasteryzacja danych wektorowych,
- nakładanie obszaru na mapę NDMI,
- obliczanie statystyk NDMI w obrębie obszaru wektorowego:
  - średnia,
  - minimum,
  - maksimum,
  - liczba pikseli,
- dynamiczny tytuł mapy w zależności od obecności obszaru,
- tryb danych przykładowych (1 klik – bez ręcznego uploadu),
- możliwość ręcznego wgrywania plików,
- pełna konteneryzacja aplikacji (Docker, docker-compose).

---

## Struktura projektu
```text
project/
        │
        ├── app.py                # Główny plik aplikacji Streamlit
        ├── README.md             # Dokumentacja projektu
        ├── requirements.txt      # Lista zależności Python
        ├── Dockerfile            # Instrukcje budowania obrazu Dockera
        ├── docker-compose.yml    # Konfiguracja usług Docker Compose
        │
        └── data/                 # Katalog z danymi przestrzennymi
            ├── B8.tiff           # Zdjęcie satelitarne 
            ├── B11.tiff          # Zdjęcie satelitarne 
            └── area.geojson      # Granice obszaru analizy
```
---

## Dane wejściowe

### Tryb ręczny
Użytkownik może wgrać:
- raster **B8.tiff**
- raster **B11.tiff**
- (opcjonalnie) plik **area.geojson**

### Tryb danych przykładowych
Po kliknięciu przycisku  
**„Użyj danych przykładowych”**  
aplikacja automatycznie korzysta z plików znajdujących się w folderze `data/`.

---

## Analiza przestrzenna

Aplikacja wykonuje obliczenie indeksu NDMI z danych rastrowych  
oraz oblicza statystyki NDMI w obrębie obszaru zdefiniowanego przez dane wektorowe
(GeoJSON), co spełnia wymagania przetwarzania danych rastrowych i wektorowych
jednocześnie.

---

## Uruchomienie lokalne (bez Dockera)

Aby uruchomić aplikację lokalnie, upewnij się, że masz zainstalowanego Pythona, a następnie wykonaj poniższe kroki:

1. Zainstaluj wymagane biblioteki i uruchom:
   ```bash
   pip install -r requirements.txt
   streamlit run (i path projektu albo app.py)
   
## Instrukcja uruchomienia (z Dockerem)

Zaletą tej metody jest izolacja środowiska i brak konieczności ręcznej instalacji Pythona.

1. Zbuduj i uruchom kontenery:
   ```bash
   docker-compose up --build

## Autor Danyil Muzychenko
## Projekt wykonany w ramach zajęć z QGIS
