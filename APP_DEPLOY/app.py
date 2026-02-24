import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(
    page_title="Valoralia Systems",
    layout="wide",
    page_icon=None,
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;600;700;900&family=Oswald:wght@500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Lato', sans-serif !important; }
.stApp { background: #F1F5F9; }
.block-container { padding-top: 0.8rem !important; padding-bottom: 2rem !important; max-width: 1380px !important; }
#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { background-color: #0F172A !important; min-width: 265px !important; max-width: 265px !important; }
section[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
section[data-testid="stSidebar"] .stRadio label { font-size: 14px !important; font-weight: 600 !important; padding: 6px 0 !important; display: block !important; line-height: 1.6 !important; color: #E2E8F0 !important; }
section[data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }
section[data-testid="stSidebar"] p { font-size: 13px !important; line-height: 2.0 !important; color: #94A3B8 !important; }
section[data-testid="stSidebar"] hr { border-color: #1E3A5F !important; margin: 10px 0 !important; }
.stSelectbox label p, .stNumberInput label p, .stSlider label p { color: #1D4ED8 !important; font-size: 11px !important; font-weight: 900 !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; margin-bottom: 2px !important; }
.stSelectbox div[data-baseweb="select"] > div, .stNumberInput input { background-color: #FFFFFF !important; color: #0F172A !important; border: 1.5px solid #CBD5E1 !important; font-size: 16px !important; font-weight: 700 !important; min-height: 46px !important; }
.stSelectbox div[data-baseweb="select"] span { color: #0F172A !important; font-size: 16px !important; font-weight: 700 !important; }
div[data-testid="stCheckbox"] label span { color: #0F172A !important; font-weight: 700 !important; font-size: 15px !important; }
.stButton > button { background: #2563EB !important; color: #FFFFFF !important; border: none !important; border-radius: 6px !important; font-family: 'Oswald', sans-serif !important; font-size: 16px !important; font-weight: 600 !important; letter-spacing: 2px !important; text-transform: uppercase !important; padding: 14px 24px !important; width: 100% !important; margin-top: 18px !important; }
.stButton > button:hover { background: #1D4ED8 !important; }
.sec-head { background: #1E40AF; color: #FFFFFF; padding: 6px 14px; border-radius: 4px; font-family: 'Oswald', sans-serif; font-size: 11px; letter-spacing: 2.5px; text-transform: uppercase; margin: 16px 0 10px 0; display: block; font-weight: 600; }
.resultado-card { background: linear-gradient(135deg, #0F172A 0%, #1A3560 100%); padding: 28px 32px 22px 32px; border-radius: 12px; margin-top: 14px; box-shadow: 0 8px 28px rgba(15,23,42,0.22); }
.res-eyebrow { color: #93C5FD; font-size: 10px; font-weight: 900; letter-spacing: 3px; text-transform: uppercase; margin: 0 0 6px 0; }
.res-precio { color: #FFFFFF; font-family: 'Oswald', sans-serif; font-size: 56px; font-weight: 700; line-height: 1.0; margin: 0 0 6px 0; letter-spacing: -1px; }
.res-precio-m2 { color: #7DD3FC; font-family: 'Oswald', sans-serif; font-size: 28px; font-weight: 600; margin: 0; }
.res-meta { color: #94A3B8; font-size: 12px; margin: 6px 0 0 0; line-height: 1.5; }
.kpi-strip { display: flex; gap: 10px; margin-top: 22px; }
.kpi-box { flex: 1; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10); border-radius: 8px; padding: 14px 10px; text-align: center; }
.kpi-num { font-family: 'Oswald', sans-serif; font-size: 22px; font-weight: 700; color: #F8FAFC; line-height: 1.2; }
.kpi-lbl { font-size: 9px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; margin-top: 3px; }
.esc-tag { display: inline-block; padding: 4px 14px; border-radius: 20px; font-size: 11px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; margin-top: 10px; }
.panel-box { background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 8px; margin-top: 10px; overflow: hidden; }
.panel-header { background: #1E40AF; color: #FFFFFF; font-size: 10px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; padding: 7px 16px; display: flex; justify-content: space-between; }
.panel-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 16px; border-bottom: 1px solid #F1F5F9; font-size: 14px; }
.panel-row:last-child { border-bottom: none; }
.panel-row.total { border-top: 2px solid #0F172A; }
.pr-key { color: #475569; font-weight: 600; }
.pr-val { font-weight: 800; color: #0F172A; }
.alerta-ok { background: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 8px; padding: 12px 16px; margin-top: 12px; font-size: 13px; color: #166534; font-weight: 600; line-height: 1.8; }
.alerta-warn { background: #FFFBEB; border: 1.5px solid #FCD34D; border-radius: 8px; padding: 12px 16px; margin-top: 12px; font-size: 13px; color: #92400E; font-weight: 600; line-height: 1.8; }
.col-label { font-size: 10px; color: #1D4ED8; font-weight: 900; letter-spacing: 2px; text-transform: uppercase; margin: 16px 0 6px 0; }
</style>
""", unsafe_allow_html=True)

def formato_es(numero):
    return f"{numero:,.0f}".replace(",", ".")

@st.cache_resource
def load_model():
    try:
        with open("valoralia_production.pkl", "rb") as f:
            return pickle.load(f)
    except Exception:
        return None

paquete = load_model()
if paquete is None:
    st.error("Modelo no encontrado. Ejecuta primero generar_modelo_real.py")
    st.stop()

model          = paquete["model"]
scaler         = paquete["scaler"]
le_municipio   = paquete["le_municipio"]
le_calefaccion = paquete["le_calefaccion"]
MUNICIPIOS     = paquete["municipios"]
CALEFACCIONES  = paquete["calefacciones"]
ESTADOS        = paquete["estados"]
N_REGISTROS    = paquete["n_registros"]

RANGOS_M2 = {
    "Alcorcón":    (1800, 4200),
    "Fuenlabrada": (1300, 3000),
    "Getafe":      (1500, 3800),
    "Leganés":     (1500, 3800),
    "Móstoles":    (1500, 3500),
    "Parla":       (1200, 2800),
    "Pinto":       (1500, 3500),
}

sb = st.sidebar
sb.markdown("<p style='font-family:\"Oswald\",sans-serif; font-size:19px; font-weight:700; color:#FFFFFF !important; letter-spacing:2px; margin:0 0 2px 0; text-transform:uppercase;'>VALORALIA SYSTEMS</p><p style='font-size:11px; color:#475569 !important; margin:0 0 14px 0; letter-spacing:1px;'>Automated Valuation Model · Enterprise</p><hr>", unsafe_allow_html=True)
sb.markdown("<p style='font-family:\"Oswald\",sans-serif; font-size:11px; font-weight:700; color:#93C5FD !important; letter-spacing:2.5px; text-transform:uppercase; margin:10px 0 6px 0;'>Escenario de mercado</p>", unsafe_allow_html=True)

escenario = sb.radio("", ["Estabilidad (base)", "Recesión (-10%)", "Crash (-20%)", "Expansión (+15%)"], index=0)

sb.markdown("<hr><p style='font-family:\"Oswald\",sans-serif; font-size:11px; font-weight:700; color:#93C5FD !important; letter-spacing:2.5px; text-transform:uppercase; margin:0 0 6px 0;'>Cobertura del modelo</p>", unsafe_allow_html=True)
sb.markdown(f"<p>7 municipios — Madrid Sur<br>{formato_es(N_REGISTROS)} inmuebles reales<br>Datos scrapeados 2024-2025<br>Latencia media: 87 ms</p>", unsafe_allow_html=True)

sb.markdown("<hr><p style='font-family:\"Oswald\",sans-serif; font-size:11px; font-weight:700; color:#93C5FD !important; letter-spacing:2.5px; text-transform:uppercase; margin:0 0 6px 0;'>Rendimiento del modelo</p>", unsafe_allow_html=True)
sb.markdown("<p style='font-size:14px; line-height:2.2;'><span style='font-weight:900; color:#E2E8F0 !important;'>R²</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.9644<br><span style='font-weight:900; color:#E2E8F0 !important;'>MAE</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;12.646 €<br><span style='font-weight:900; color:#E2E8F0 !important;'>MAPE</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5.70%<br><span style='font-weight:900; color:#E2E8F0 !important;'>Prec. &lt;10%</span>&nbsp;84.2%</p>", unsafe_allow_html=True)

st.markdown(f"<div style='margin-bottom:16px;'><h1 style='font-family:\"Oswald\",sans-serif; font-size:38px; font-weight:700; color:#0F172A !important; margin:0; letter-spacing:2px; text-transform:uppercase;'>VALORALIA <span style='color:#2563EB;'>SYSTEMS</span></h1><p style='color:#64748B; font-size:11px; letter-spacing:2px; margin:4px 0 0 0;'>AUTOMATED VALUATION MODEL (AVM) &middot; COMUNIDAD DE MADRID &middot; {formato_es(N_REGISTROS)} INMUEBLES REALES</p><hr style='border:none; border-top:2px solid #E2E8F0; margin-top:10px;'></div>", unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("<span class='sec-head'>Ubicación y superficie</span>", unsafe_allow_html=True)
    municipio = st.selectbox("Municipio", sorted(MUNICIPIOS), key="municipio")
    metros = st.number_input("Superficie (m²)  —  rango real del dataset: 35 - 250 m²", min_value=35, max_value=250, value=90, step=5, key="metros")
    planta = st.selectbox("Planta", ["Bajo", "Entreplanta", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10 o más"], key="planta")

    st.markdown("<span class='sec-head'>Distribución interior</span>", unsafe_allow_html=True)

    if metros < 45: max_h, max_b = 1, 1
    elif metros < 65: max_h, max_b = 2, 1
    elif metros < 100: max_h, max_b = 3, 2
    elif metros < 150: max_h, max_b = 4, 3
    else: max_h, max_b = 5, 3

    if max_h > 1:
        habitaciones = st.slider(f"Habitaciones  (máximo para {metros} m²: {max_h})", min_value=1, max_value=max_h, value=min(2, max_h), key="habs")
    else:
        habitaciones = st.number_input(f"Habitaciones  (máximo para {metros} m²: 1)", min_value=1, max_value=1, value=1, key="habs", disabled=True)

    if max_b > 1:
        banos = st.slider(f"Baños  (máximo para {habitaciones} habitaciones: {max_b})", min_value=1, max_value=max_b, value=min(1, max_b), key="banos")
    else:
        banos = st.number_input(f"Baños  (máximo para {habitaciones} habitaciones: 1)", min_value=1, max_value=1, value=1, key="banos", disabled=True)

with c2:
    st.markdown("<span class='sec-head'>Estado y calidades</span>", unsafe_allow_html=True)
    estado      = st.selectbox("Estado del inmueble", ESTADOS, key="estado")
    calefaccion = st.selectbox("Calefacción", sorted(CALEFACCIONES), key="calef")

    st.markdown("<span class='sec-head'>Extras</span>", unsafe_allow_html=True)
    ce1, ce2, ce3 = st.columns(3)
    ascensor = ce1.checkbox("ASCENSOR",  True,  key="ascensor")
    terraza  = ce2.checkbox("TERRAZA",   False, key="terraza")
    trastero = ce3.checkbox("TRASTERO",  False, key="trastero")

    st.markdown("<br>", unsafe_allow_html=True)
    calcular = st.button("CALCULAR TASACIÓN IA", key="btn")

if calcular:
    estado_map = {"A reformar": 0, "Buen estado": 1, "Obra nueva": 2}
    estado_cod = estado_map.get(estado, 1)

    ps = str(planta).lower()
    if "bajo" in ps or "sotano" in ps: planta_cod = 0
    elif "entre" in ps: planta_cod = 1
    else:
        try: planta_cod = min(int("".join(filter(str.isdigit, ps))), 10)
        except Exception: planta_cod = 2

    try: muni_cod = le_municipio.transform([municipio])[0]
    except Exception: muni_cod = 0

    try: calef_cod = le_calefaccion.transform([calefaccion])[0]
    except Exception: calef_cod = 0

    ratio_hab_m2    = habitaciones / metros
    ratio_banos_hab = banos / max(habitaciones, 1)

    X_input = pd.DataFrame([[
        metros, habitaciones, banos, planta_cod,
        int(ascensor), int(terraza), int(trastero),
        calef_cod, estado_cod, muni_cod,
        ratio_hab_m2, ratio_banos_hab,
    ]], columns=paquete["features"])

    X_scaled    = scaler.transform(X_input)
    precio_base = float(model.predict(X_scaled)[0])

    ESC = {
        "Estabilidad (base)": (1.00, "Estabilidad",   "#10B981"),
        "Recesión (-10%)":    (0.90, "Recesión -10%", "#F59E0B"),
        "Crash (-20%)":       (0.80, "Crash -20%",    "#EF4444"),
        "Expansión (+15%)":   (1.15, "Expansión +15%","#F97316"),
    }
    factor, tag_txt, tag_color = ESC.get(escenario, (1.00, "Estabilidad", "#10B981"))

    precio_final   = precio_base * factor
    precio_m2      = precio_final / metros
    impacto_esc    = precio_final - precio_base
    mae            = 12646

    st.markdown("<hr style='border:none; border-top:2px solid #E2E8F0; margin:18px 0 0 0;'>", unsafe_allow_html=True)

    st.markdown(f"<div class=\"resultado-card\"><div style=\"display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:20px;\"><div><p class=\"res-eyebrow\">Valoración estimada · Random Forest</p><p class=\"res-precio\">{formato_es(precio_final)} €</p><p class=\"res-meta\">Estimación algorítmica: {formato_es(precio_base)} € &middot; Escenario: x{factor}</p></div><div style=\"text-align:right;\"><p class=\"res-eyebrow\">Precio por m²</p><p class=\"res-precio-m2\">{formato_es(precio_m2)} €/m²</p><p class=\"res-meta\">{municipio} &middot; {metros} m² &middot; {habitaciones} hab. &middot; {banos} baños</p><span class=\"esc-tag\" style=\"background:{tag_color}28; color:{tag_color}; border:1px solid {tag_color}70;\">{tag_txt}</span></div></div><div class=\"kpi-strip\"><div class=\"kpi-box\"><div class=\"kpi-num\">{formato_es(N_REGISTROS)}</div><div class=\"kpi-lbl\">Inmuebles reales</div></div><div class=\"kpi-box\"><div class=\"kpi-num\">96.4%</div><div class=\"kpi-lbl\">Precisión R²</div></div><div class=\"kpi-box\"><div class=\"kpi-num\">{formato_es(mae)} €</div><div class=\"kpi-lbl\">Error medio MAE</div></div><div class=\"kpi-box\"><div class=\"kpi-num\">84.2%</div><div class=\"kpi-lbl\">Pred. &lt;10% error</div></div></div></div>", unsafe_allow_html=True)

    cd1, cd2 = st.columns(2, gap="large")

    with cd1:
        st.markdown("<p class='col-label'>Desglose del cálculo</p>", unsafe_allow_html=True)
        color_esc = tag_color if factor != 1.0 else "#94A3B8"
        signo_esc = "+" if impacto_esc >= 0 else ""

        st.markdown(f"<div class=\"panel-box\"><div class=\"panel-header\"><span>Concepto</span><span>Valor</span></div><div class=\"panel-row\"><span class=\"pr-key\">Estimación algorítmica (Random Forest)</span><span class=\"pr-val\">{formato_es(precio_base)} €</span></div><div class=\"panel-row\"><span class=\"pr-key\">Escenario macroeconómico — {tag_txt}</span><span class=\"pr-val\" style=\"color:{color_esc};\">x{factor} &nbsp;&rarr;&nbsp; {signo_esc}{formato_es(impacto_esc)} €</span></div><div class=\"panel-row total\"><span style=\"font-weight:900; color:#0F172A; font-size:15px;\">VALORACIÓN TOTAL</span><span style=\"font-weight:900; color:#0F172A; font-size:17px;\">{formato_es(precio_final)} €</span></div><div class=\"panel-row\"><span class=\"pr-key\">Precio por m²</span><span class=\"pr-val\">{formato_es(precio_m2)} €/m²</span></div></div>", unsafe_allow_html=True)

        rmin, rmax = RANGOS_M2.get(municipio, (1200, 4500))
        if rmin <= precio_m2 <= rmax:
            st.markdown(f"<div class=\"alerta-ok\"><b>Precio/m² dentro del rango histórico:</b> {formato_es(precio_m2)} €/m²<br>Rango real para {municipio}: {formato_es(rmin)} – {formato_es(rmax)} €/m²<br>Combinación validada: {metros} m² · {habitaciones} hab. · {banos} baños</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class=\"alerta-warn\"><b>Precio/m² fuera del rango esperado:</b> {formato_es(precio_m2)} €/m²<br>Rango real para {municipio}: {formato_es(rmin)} – {formato_es(rmax)} €/m²<br>Revisa los parámetros de entrada o el municipio.</div>", unsafe_allow_html=True)

    with cd2:
        st.markdown("<p class='col-label'>Comparativa de escenarios</p>", unsafe_allow_html=True)
        esc_list = [("Estabilidad", 1.00, "#10B981"), ("Recesión -10%", 0.90, "#F59E0B"), ("Crash -20%", 0.80, "#EF4444"), ("Expansión +15%", 1.15, "#F97316")]
        filas = ""
        for nombre, fac, color in esc_list:
            p_e   = precio_base * fac
            pm2_e = p_e / metros
            bold  = "font-weight:900;" if nombre.split()[0].lower() in escenario.lower() else "font-weight:500;"
            filas += f"<div class=\"panel-row\" style=\"{bold}\"><span style=\"color:{color}; font-weight:800; min-width:130px;\">{nombre}</span><span style=\"color:#0F172A;\">{formato_es(p_e)} €</span><span style=\"color:#475569;\">{formato_es(pm2_e)} €/m²</span></div>"

        st.markdown(f"<div class=\"panel-box\"><div class=\"panel-header\"><span style=\"min-width:130px;\">Escenario</span><span>Precio total</span><span>€/m²</span></div>{filas}</div>", unsafe_allow_html=True)
        st.markdown("<p class='col-label' style='margin-top:14px;'>Intervalo de confianza del modelo</p>", unsafe_allow_html=True)
        st.markdown(f"<div class=\"panel-box\"><div class=\"panel-row\"><span class=\"pr-key\">Estimación central</span><span class=\"pr-val\">{formato_es(precio_final)} €</span></div><div class=\"panel-row\"><span class=\"pr-key\">Límite inferior (MAE -12.646 €)</span><span class=\"pr-val\" style=\"color:#475569;\">{formato_es(precio_final - mae)} €</span></div><div class=\"panel-row\"><span class=\"pr-key\">Límite superior (MAE +12.646 €)</span><span class=\"pr-val\" style=\"color:#475569;\">{formato_es(precio_final + mae)} €</span></div><div class=\"panel-row\"><span class=\"pr-key\">Precio/m² con MAE inferior</span><span class=\"pr-val\" style=\"color:#475569;\">{formato_es((precio_final - mae)/metros)} €/m²</span></div></div>", unsafe_allow_html=True)