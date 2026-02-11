import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import seaborn as sns

# === CONFIGURACIÓN DE LA PÁGINA ===
st.set_page_config(page_title="Monitor de Riesgo Soberano - CAPRD",page_icon="🚩", layout="wide")


# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# === CONFIGURACIÓN DE USUARIO Y REPOSITORIO ===
USUARIO_GH = "aifs82-langston"
REPO_GH = "monitor_riesgopais_CAPRD"
FECHA_ARC = "11042025"
URL_BASE = f"https://raw.githubusercontent.com/{USUARIO_GH}/{REPO_GH}/main/data/"

# === DICCIONARIOS DE CALIFICACIÓN ===
orden_fitch_snp = {
    'D': 1, 'C': 2, 'CC': 3, 'CCC-': 4, 'CCC': 5, 'CCC+': 6, 'B-': 7, 'B': 8, 'B+': 9,
    'BB-': 10, 'BB': 11, 'BB+': 12, 'BBB-': 13, 'BBB': 14, 'BBB+': 15, 'A-': 16,
    'A': 17, 'A+': 18, 'AA-': 19, 'AA': 20, 'AA+': 21, 'AAA': 22
}

orden_moodys = {
    'C': 1, 'Ca': 2, 'Caa3': 3, 'Caa2': 4, 'Caa1': 5, 'B3': 6, 'B2': 7, 'B1': 8,
    'Ba3': 9, 'Ba2': 10, 'Ba1': 11, 'Baa3': 12, 'Baa2': 13, 'Baa1': 14, 'A3': 15,
    'A2': 16, 'A1': 17, 'Aa3': 18, 'Aa2': 19, 'Aa1': 20, 'Aaa': 21
}

perspectiva_map = {'Negativa': 0, 'Estable': 1, 'Positiva': 2, 'n.p': None}

dict_paises = {
    'Costa Rica': ('CR', ['Fitch', 'Moodys', 'S&P']),
    'El Salvador': ('SV', ['Fitch', 'Moodys', 'S&P']),
    'Guatemala': ('GT', ['Fitch', 'Moodys', 'S&P']),
    'Honduras': ('HN', ['Moodys', 'S&P']),
    'Nicaragua': ('NI', ['Fitch', 'Moodys', 'S&P']),
    'Panamá': ('PA', ['Fitch', 'Moodys', 'S&P']),
    'República Dominicana': ('DO', ['Fitch', 'Moodys', 'S&P'])
}

# === FUNCIONES DE CARGA ===
@st.cache_data
def cargar_datos(agencia, cod):
    ruta = f"{URL_BASE}{agencia}{cod}_{FECHA_ARC}.xlsx"
    escala = orden_moodys if agencia == 'Moodys' else orden_fitch_snp
    try:
        df = pd.read_excel(ruta)
        df['Fecha'] = pd.PeriodIndex(df['Fecha'], freq='Q').astype(str)
        df['Calif_num'] = df['Calificación'].map(escala)
        df['Perspectiva_num'] = df['Perspectiva'].map(perspectiva_map)
        return df, escala
    except:
        return None, None

# === ENCABEZADO Y LOGO ===
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    st.image("FullLogo.png", width=200)

with col_titulo:
    st.title("📊 Monitor de Riesgo Soberano: Calificación y Perspectiva")
    st.subheader("Centroamérica, Panamá y República Dominicana (CAPRD)")
    st.markdown("Alfredo Ibrahim Flores Sarria ©2026")

st.divider()

# === SELECTOR DE PAÍS (Corregido: movido al cuerpo principal) ===
col_sel, _ = st.columns([1, 2])
with col_sel:
    pais_sel = st.selectbox("🌍 Seleccione un País para analizar:", list(dict_paises.keys()))

cod_pais, agencias = dict_paises[pais_sel]

# --- BLOQUE DE MÉTRICAS ---
#st.markdown(f"### 📌 Resumen Actual: {pais_sel}")
#cols_met = st.columns(len(agencias))

#for i, ag in enumerate(agencias):
    #df_temp, _ = cargar_datos(ag, cod_pais)
    #if df_temp is not None:
        #ultima_calif = df_temp['Calificación'].iloc[-1]
        #ultima_persp = df_temp['Perspectiva'].iloc[-1]
        #delta_color = "normal" if ultima_persp == "Estable" else "inverse" if ultima_persp == "Negativa" else "normal"

        #with cols_met[i]:
            #st.metric(label=f"Última {ag}", value=ultima_calif, delta=ultima_persp, delta_color=delta_color)

#st.divider()

# --- BLOQUE DE MÉTRICAS (Sin flechas) ---
st.markdown(f"### 📌 Resumen Actual: {pais_sel}")
cols_met = st.columns(len(agencias))

for i, ag in enumerate(agencias):
    df_temp, _ = cargar_datos(ag, cod_pais)
    if df_temp is not None:
        ultima_calif = df_temp['Calificación'].iloc[-1]
        ultima_persp = df_temp['Perspectiva'].iloc[-1]

        # Definir color según la perspectiva (Verde para Positiva, Rojo para Negativa, Gris para Estable)
        color_persp = "#09ab3b" if ultima_persp == "Positiva" else "#ff4b4b" if ultima_persp == "Negativa" else "#6d7178"

        with cols_met[i]:
            # Usamos un div manual para aprovechar el estilo .stMetric que ya definiste en tu CSS
            st.markdown(f"""
                <div class="stMetric">
                    <p style="color: #555; font-size: 14px; margin-bottom: 5px;">Última {ag}</p>
                    <h2 style="margin: 0; color: #31333f; font-size: 2rem;">{ultima_calif}</h2>
                    <p style="color: {color_persp}; font-size: 15px; font-weight: bold; margin-top: 5px;">{ultima_persp}</p>
                </div>
            """, unsafe_allow_html=True)
# --- GRÁFICOS ---
n_agencias = len(agencias)
fig, axs = plt.subplots(2, n_agencias, figsize=(5 * n_agencias, 7), sharex='col')

if n_agencias == 1: axs = axs.reshape(2, 1)

for i, ag in enumerate(agencias):
    df_temp, escala = cargar_datos(ag, cod_pais)
    if df_temp is not None:
        axs[0, i].plot(df_temp['Fecha'], df_temp['Calif_num'], marker='o', color='#1f77b4', linewidth=2)
        axs[0, i].set_title(f"{ag}: Calificación", fontsize=12, fontweight='bold')
        axs[0, i].set_yticks(list(escala.values()))
        axs[0, i].set_yticklabels(list(escala.keys()))
        axs[0, i].grid(True, linestyle='--', alpha=0.5)

        df_p = df_temp.dropna(subset=['Perspectiva_num'])
        axs[1, i].step(df_p['Fecha'], df_p['Perspectiva_num'], where='mid', marker='s', color='#ff7f0e', linewidth=2)
        axs[1, i].set_title(f"{ag}: Perspectiva", fontsize=12, fontweight='bold')
        axs[1, i].set_yticks([0, 1, 2])
        axs[1, i].set_yticklabels(['Negativa', 'Estable', 'Positiva'])
        axs[1, i].grid(True, linestyle='--', alpha=0.5)
        axs[1, i].tick_params(axis='x', rotation=90)

plt.tight_layout()
st.pyplot(fig)

st.caption(f"Fuente: Elaboración propia basada en reportes de Fitch, Moody's y S&P al cuarto trimestre de 2025")

# --- COMPARATIVA REGIONAL ---
st.divider()
st.header("🗺️ Comparativa Regional (Última Calificación)")

@st.cache_data
def generar_matriz_regional():
    datos_matriz = []
    for nombre, (cod, ags) in dict_paises.items():
        fila = {'País': nombre}
        for ag in ['Fitch', 'Moodys', 'S&P']:
            if ag in ags:
                df_t, _ = cargar_datos(ag, cod)
                fila[ag] = df_t['Calif_num'].iloc[-1] if df_t is not None else None
            else:
                fila[ag] = None
        datos_matriz.append(fila)
    return pd.DataFrame(datos_matriz).set_index('País')

df_matrix = generar_matriz_regional()
fig_heat, ax_heat = plt.subplots(figsize=(10, 6))
sns.heatmap(df_matrix, annot=True, cmap="RdYlGn", cbar=False, ax=ax_heat)
ax_heat.set_title("Puntaje de Riesgo (Valores más altos = Menor Riesgo)", fontsize=14)
st.pyplot(fig_heat)

st.info("💡 **Nota:** El **Grado de Inversión** comienza en el puntaje **13** (BBB- / Baa3).")

# --- TABLA COMPARATIVA FINAL (Calificación + Perspectiva) ---
with st.expander("🔍 Ver Tabla Comparativa Detallada"):
    tabla_data = []
    for nombre, (cod, ags) in dict_paises.items():
        fila = {'País': nombre}
        for ag in ['Fitch', 'Moodys', 'S&P']:
            if ag in ags:
                df_t, _ = cargar_datos(ag, cod)
                if df_t is not None:
                    fila[ag] = f"{df_t['Calificación'].iloc[-1]} ({df_t['Perspectiva'].iloc[-1]})"
                else:
                    fila[ag] = "N/A"
            else:
                fila[ag] = "N/A"
        tabla_data.append(fila)
    st.table(pd.DataFrame(tabla_data))
