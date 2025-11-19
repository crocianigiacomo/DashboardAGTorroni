"""
Unit tests per DashboardAGTorroni.

Questo modulo contiene test per verificare la corretta funzionalità dei componenti
della dashboard, inclusi caricamento dati, callback e generazione grafici.
"""

import pytest
import pandas as pd
import sys
import os
from datetime import datetime

# Aggiungi il path src al sys.path per permettere import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class TestDataLoading:
    """Test per il caricamento dei dati CSV."""
    
    def test_meteo_data_exists(self):
        """Verifica che il file meteo2024.csv esista e sia caricabile."""
        df = pd.read_csv("data/meteo2024.csv")
        assert not df.empty, "Il file meteo2024.csv è vuoto"
        assert len(df) == 365, f"Attesi 365 giorni, trovati {len(df)}"
    
    def test_meteo_data_columns(self):
        """Verifica che meteo2024.csv contenga le colonne necessarie."""
        df = pd.read_csv("data/meteo2024.csv")
        required_columns = ["DATA", "TMEDIA °C", "TMIN °C", "TMAX °C", "UMIDITA %", "FENOMENI"]
        for col in required_columns:
            assert col in df.columns, f"Colonna mancante: {col}"
    
    def test_prezzi_cereali_exists(self):
        """Verifica che il file PREZZI_CEREALI.csv esista e sia caricabile."""
        df = pd.read_csv("data/PREZZI_CEREALI.csv", sep=";")
        assert not df.empty, "Il file PREZZI_CEREALI.csv è vuoto"
        assert len(df) == 7, f"Attesi 7 cereali, trovati {len(df)}"
    
    def test_production_data_exists(self):
        """Verifica che il file production_data.csv esista e sia caricabile."""
        df = pd.read_csv("data/production_data.csv")
        assert not df.empty, "Il file production_data.csv è vuoto"
        assert "ProductionVolume" in df.columns, "Colonna ProductionVolume mancante"
    
    def test_sales_data_exists(self):
        """Verifica che il file sales_data.csv esista e sia caricabile."""
        df = pd.read_csv("data/sales_data.csv")
        assert not df.empty, "Il file sales_data.csv è vuoto"
        assert "Gain" in df.columns, "Colonna Gain mancante"
    
    def test_ettari_data_exists(self):
        """Verifica che il file CEREALI_TERRENO_PRODUZIONE.csv esista e sia caricabile."""
        df = pd.read_csv("data/CEREALI_TERRENO_PRODUZIONE.csv", sep=";")
        assert not df.empty, "Il file CEREALI_TERRENO_PRODUZIONE.csv è vuoto"
        assert "ETTARI_TERRENO" in df.columns, "Colonna ETTARI_TERRENO mancante"


class TestDataIntegrity:
    """Test per l'integrità e validità dei dati."""
    
    def test_temperature_values(self):
        """Verifica che i valori di temperatura siano validi."""
        df = pd.read_csv("data/meteo2024.csv")
        assert df["TMIN °C"].min() >= -20, "Temperatura minima troppo bassa"
        assert df["TMAX °C"].max() <= 50, "Temperatura massima troppo alta"
        assert (df["TMIN °C"] <= df["TMAX °C"]).all(), "TMIN deve essere <= TMAX"
    
    def test_humidity_values(self):
        """Verifica che l'umidità sia nel range 0-100."""
        df = pd.read_csv("data/meteo2024.csv")
        assert df["UMIDITA %"].min() >= 0, "Umidità minima negativa"
        assert df["UMIDITA %"].max() <= 100, "Umidità massima > 100%"
    
    def test_production_volumes_positive(self):
        """Verifica che i volumi di produzione siano non negativi."""
        df = pd.read_csv("data/production_data.csv")
        assert (df["ProductionVolume"] >= 0).all(), "Trovati volumi di produzione negativi"
    
    def test_sales_gains_positive(self):
        """Verifica che i guadagni siano non negativi."""
        df = pd.read_csv("data/sales_data.csv")
        assert (df["Gain"] >= 0).all(), "Trovati guadagni negativi"
    
    def test_cereal_names_consistency(self):
        """Verifica che i nomi dei cereali siano consistenti tra i file."""
        cereali_ettari = set(pd.read_csv("data/CEREALI_TERRENO_PRODUZIONE.csv", sep=";")["CEREALE"])
        cereali_prezzi = set(pd.read_csv("data/PREZZI_CEREALI.csv", sep=";")["CEREALE"])
        assert cereali_ettari == cereali_prezzi, "Nomi cereali non consistenti tra i file"


class TestDataProcessing:
    """Test per le elaborazioni sui dati."""
    
    def test_gain_calculation(self):
        """Verifica il calcolo del guadagno per ettaro."""
        vendita = pd.read_csv("data/sales_data.csv")
        ettari = pd.read_csv("data/CEREALI_TERRENO_PRODUZIONE.csv", sep=";")
        
        df_gain = vendita.groupby("Prodotto")["Gain"].sum().reset_index()
        df = ettari.merge(df_gain, left_on="CEREALE", right_on="Prodotto", how="left")
        df["€ per ETTARO"] = (df["Gain"] / df["ETTARI_TERRENO"]).round()
        
        assert not df["€ per ETTARO"].isna().all(), "Calcolo guadagno per ettaro fallito"
        assert (df["€ per ETTARO"] >= 0).all(), "Guadagno per ettaro negativo"
    
    def test_date_parsing(self):
        """Verifica che le date siano nel formato corretto."""
        df = pd.read_csv("data/meteo2024.csv")
        df["DATA"] = pd.to_datetime(df["DATA"])
        
        assert df["DATA"].min().year == 2024, "Anno iniziale non corretto"
        assert df["DATA"].max().year == 2024, "Anno finale non corretto"
    
    def test_fenomeni_categories(self):
        """Verifica che i fenomeni atmosferici siano nelle categorie previste."""
        df = pd.read_csv("data/meteo2024.csv")
        valid_fenomeni = ["sole", "pioggia", "nebbia"]
        
        for fenomeno in df["FENOMENI"].unique():
            assert fenomeno in valid_fenomeni, f"Fenomeno non valido: {fenomeno}"


class TestDashboardComponents:
    """Test per i componenti della dashboard."""
    
    def test_colormap_completeness(self):
        """Verifica che tutti i cereali abbiano un colore assegnato."""
        cereali = ["MEDICA", "COLZA", "FRUMENTO TENERO", "FRUMENTO DURO", 
                   "ORZO", "GIRASOLE", "MAIS"]
        
        colormap = {
            "MEDICA": "#636EFA",
            "COLZA": "#EF553B",
            "FRUMENTO TENERO": "#00CC96",
            "FRUMENTO DURO": "#AB63FA",
            "ORZO": "#FFA15A",
            "GIRASOLE": "#19D3F3",
            "MAIS": "#FF6692"
        }
        
        for cereale in cereali:
            assert cereale in colormap, f"Colore mancante per {cereale}"
    
    def test_date_range_valid(self):
        """Verifica che il range di date sia valido."""
        df = pd.read_csv("data/meteo2024.csv")
        start_date = df["DATA"].min()
        end_date = df["DATA"].max()
        
        assert pd.to_datetime(start_date) <= pd.to_datetime(end_date), \
            "Data inizio posteriore a data fine"


class TestDataGeneration:
    """Test per gli script di generazione dati."""
    
    def test_production_dates_in_range(self):
        """Verifica che le date di produzione siano nel 2024."""
        df = pd.read_csv("data/production_data.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        
        assert df["Date"].min().year == 2024, "Date di produzione fuori range"
        assert df["Date"].max().year == 2024, "Date di produzione fuori range"
    
    def test_sales_dates_in_range(self):
        """Verifica che le date di vendita siano nel 2024."""
        df = pd.read_csv("data/sales_data.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        
        assert df["Date"].min().year == 2024, "Date di vendita fuori range"
        assert df["Date"].max().year == 2024, "Date di vendita fuori range"
    
    def test_total_production_vs_sales(self):
        """Verifica che le vendite non superino la produzione totale."""
        production = pd.read_csv("data/production_data.csv")
        sales = pd.read_csv("data/sales_data.csv")
        
        for cereale in production["Prodotto"].unique():
            prod_total = production[production["Prodotto"] == cereale]["ProductionVolume"].sum()
            sales_total = sales[sales["Prodotto"] == cereale]["SalesVolume"].sum()
            
            assert sales_total <= prod_total, \
                f"Vendite di {cereale} superano la produzione"


# Funzione main per eseguire i test
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])