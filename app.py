# ==============================================
# ✨ AGRIHUB ✨
# Plateforme de Pilotage des Exploitations Agricoles
# Analyse de Données
# ==============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

# -------------------- CONFIGURATION DE LA PAGE --------------------
st.set_page_config(
    page_title="AgriHub | Pilotage Agricole",
    page_icon="🌾",
    layout="wide"
)

# -------------------- STYLE PROFESSIONNEL --------------------
st.markdown("""
    <style>
    .stApp {
        background: #F5F7F5;
    }
    h1 {
        color: #2E7D32 !important;
        font-family: 'Segoe UI', 'Arial', sans-serif !important;
        text-align: center !important;
        font-size: 2.8rem !important;
        letter-spacing: 2px;
        border-bottom: 2px solid #2E7D32;
        padding-bottom: 15px;
    }
    h3 {
        color: #1B5E20 !important;
        font-family: 'Arial', sans-serif !important;
    }
    .stButton > button {
        background: #2E7D32 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
    }
    .stButton > button:hover {
        background: #1B5E20 !important;
    }
    [data-testid="stMetric"] {
        background: white !important;
        border-radius: 10px !important;
        padding: 20px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
        border-left: 4px solid #2E7D32 !important;
    }
    .stForm {
        background: white !important;
        border-radius: 10px !important;
        padding: 30px !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05) !important;
        border: 1px solid #E0E0E0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- BARRE LATÉRALE --------------------
with st.sidebar:
    st.markdown("### 🌾 AGRIHUB")
    st.markdown("Direction de l'Analyse Agricole")
    st.markdown("---")
    st.markdown(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    st.markdown("---")
    st.markdown("*Module :* Collecte & Analyse")
    st.markdown("*Version :* 1.0")

# -------------------- TITRE --------------------
st.title("AGRIHUB")
st.markdown("### Plateforme de Pilotage des Exploitations Agricoles")
st.markdown("---")

# -------------------- CHEMIN DU FICHIER --------------------
DATA_FILE = os.path.join("data", "agriculteurs.csv")

# -------------------- FONCTIONS --------------------
def charger_donnees():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except:
            return pd.DataFrame(columns=["Date", "Nom", "Prénom", "Produit", "Localisation", "Prix", "Quantité"])
    return pd.DataFrame(columns=["Date", "Nom", "Prénom", "Produit", "Localisation", "Prix", "Quantité"])

def sauvegarder(data):
    df_ancien = charger_donnees()
    df_final = pd.concat([df_ancien, data], ignore_index=True)
    os.makedirs("data", exist_ok=True)
    df_final.to_csv(DATA_FILE, index=False)
    return True

# -------------------- COLONNES --------------------
col1, col2 = st.columns([1, 2])

# ==============================================
# PARTIE GAUCHE : FORMULAIRE DE COLLECTE
# ==============================================
with col1:
    st.subheader("Enregistrement d'un Agriculteur")
    st.markdown("Formulaire de collecte terrain")
    
    with st.form("form_agriculteur", clear_on_submit=True):
        nom = st.text_input("Nom", placeholder="Ex: TCHINDA")
        prenom = st.text_input("Prénom", placeholder="Ex: Joseph")
        produit = st.text_input("Produit à vendre", placeholder="Ex: Maïs, Cacao, Tomates...")
        localisation = st.text_input("Localisation", placeholder="Ex: Bafoussam, Yaoundé...")
        prix = st.number_input("Prix unitaire (FCFA)", min_value=0, value=1000, step=100)
        quantite = st.number_input("Quantité (kg)", min_value=0, value=10, step=1)
        
        envoyer = st.form_submit_button("Enregistrer les données", use_container_width=True)
        
        if envoyer:
            if nom == "" or prenom == "" or produit == "" or localisation == "":
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                nouvelle = pd.DataFrame([{
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nom": nom.strip(),
                    "Prénom": prenom.strip(),
                    "Produit": produit.strip(),
                    "Localisation": localisation.strip(),
                    "Prix": prix,
                    "Quantité": quantite
                }])
                sauvegarder(nouvelle)
                st.success(f"Agriculteur {prenom} {nom} enregistré avec succès !")

# ==============================================
# PARTIE DROITE : ANALYSE DES DONNÉES
# ==============================================
with col2:
    st.subheader("Analyse des Données")
    
    df = charger_donnees()
    
    if df.empty:
        st.warning("Aucune donnée collectée. Remplissez le formulaire.")
        st.info("Affichage avec un jeu de données exemple.")
        
        donnees_exemple = {
            "Nom": ["TCHINDA", "FOTSO", "MOUAFO", "TAGNE", "EKAMBI", "NGANGO", "TCHATO", "WAMBA", "KUETE", "SIMEN"],
            "Prénom": ["Joseph", "Marie", "Paul", "Esther", "David", "Alice", "Roger", "Sophie", "Jean", "Lucie"],
            "Produit": ["Maïs", "Cacao", "Tomates", "Maïs", "Cacao", "Tomates", "Maïs", "Cacao", "Tomates", "Maïs"],
            "Localisation": ["Bafoussam", "Yaoundé", "Bafoussam", "Douala", "Yaoundé", "Bafoussam", "Douala", "Yaoundé", "Bafoussam", "Douala"],
            "Prix": [500, 1500, 300, 450, 1600, 280, 520, 1400, 310, 480],
            "Quantité": [200, 50, 150, 180, 45, 120, 210, 55, 130, 190]
        }
        df = pd.DataFrame(donnees_exemple)
        df["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # ----- INDICATEURS CLES -----
    st.markdown("#### Indicateurs de Performance")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total Agriculteurs", len(df))
    with k2:
        st.metric("Prix Moyen", f"{df['Prix'].mean():,.0f} FCFA".replace(",", " "))
    with k3:
        st.metric("Quantité Totale", f"{df['Quantité'].sum():,.0f} kg".replace(",", " "))
    with k4:
        st.metric("Valeur Totale", f"{(df['Prix'] * df['Quantité']).sum():,.0f} FCFA".replace(",", " "))
    
    st.markdown("---")
    
    # ----- ANALYSES -----
    tab1, tab2, tab3 = st.tabs(["Corrélation Prix/Quantité", "Analyse par Localisation", "Données Brutes"])
    
    with tab1:
        st.markdown("### Analyse de Corrélation : Prix Unitaire vs Quantité Vendue")
        
        fig, ax = plt.subplots(figsize=(8, 5))
        x = df['Prix'].values
        y = df['Quantité'].values
        ax.scatter(x, y, alpha=0.6, color='#2E7D32', s=80)
        ax.set_xlabel("Prix Unitaire (FCFA)")
        ax.set_ylabel("Quantité Vendue (kg)")
        
        if len(x) > 1:
            # Régression linéaire avec NumPy (au lieu de scipy)
            A = np.vstack([x, np.ones(len(x))]).T
            pente, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
            line = pente * x + intercept
            ax.plot(x, line, color='red', linewidth=2)
            
            # Calcul du R²
            y_pred = pente * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r2 = 1 - (ss_res / ss_tot)
            r_value = np.sqrt(r2) if r2 >= 0 else -np.sqrt(-r2)
            
            ax.set_title(f"Droite de Régression | R² = {r2:.3f}")
            ax.annotate(f"R² = {r2:.3f}\nÉquation : y = {pente:.2f}x + {intercept:.2f}", 
                       xy=(0.05, 0.95), xycoords='axes fraction', 
                       fontsize=11, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        st.pyplot(fig)
        
        if len(x) > 1:
            st.markdown("#### Interprétation")
            if abs(r_value) > 0.7:
                st.success("*Corrélation forte détectée.* Le prix unitaire influence significativement la quantité vendue.")
            elif abs(r_value) > 0.3:
                st.warning("*Corrélation modérée détectée.* Le prix influence partiellement la quantité vendue.")
            else:
                st.info("*Corrélation faible détectée.* D'autres facteurs sont probablement en jeu.")
    
    with tab2:
        st.markdown("### Performances par Zone Géographique")
        
        colA, colB = st.columns(2)
        
        with colA:
            st.subheader("Agriculteurs par Localisation")
            loc_counts = df['Localisation'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            ax2.bar(loc_counts.index, loc_counts.values, color='#2E7D32')
            ax2.set_xlabel("Localisation")
            ax2.set_ylabel("Nombre d'agriculteurs")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig2)
        
        with colB:
            st.subheader("Prix Moyen par Localisation")
            prix_loc = df.groupby('Localisation')['Prix'].mean().sort_values(ascending=False)
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            ax3.bar(prix_loc.index, prix_loc.values, color='#4CAF50')
            ax3.set_xlabel("Localisation")
            ax3.set_ylabel("Prix moyen (FCFA)")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig3)
        
        st.markdown("---")
        st.subheader("Répartition des Produits")
        produit_counts = df['Produit'].value_counts()
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        ax4.pie(produit_counts.values, labels=produit_counts.index, autopct='%1.1f%%', 
               colors=['#2E7D32', '#4CAF50', '#81C784', '#A5D6A7', '#C8E6C9'])
        st.pyplot(fig4)
    
    with tab3:
        st.subheader("Base de Données Brutes")
        st.dataframe(df.sort_values('Date', ascending=False), use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les données (CSV)",
            data=csv,
            file_name='export_agrihub.csv',
            mime='text/csv',
            use_container_width=True
        )

# -------------------- PIED DE PAGE --------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: grey; font-size: 12px; margin-top: 20px;'>
        <p>© 2026 <b>AgriHub</b> - Solution de Pilotage Agricole</p>
        <p>Tous droits réservés</p>
    </div>
""", unsafe_allow_html=True)