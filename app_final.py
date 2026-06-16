import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import json
from pathlib import Path

# ─────────────────────────────────────────
# Paleta de colores — Cálido Moderno
# ─────────────────────────────────────────
CORAL     = "#E17055"
SLATE     = "#4A6FA5"
FONDO     = "#F5F6FA"
TEXTO     = "#2D3436"
SUBTEXTO  = "#B2BEC3"
EXITO     = "#00B894"
ALERTA    = "#F39C12"
RIESGO    = "#D63031"

# ─────────────────────────────────────────
# Configuración general
# ─────────────────────────────────────────
st.set_page_config(
    page_title="TalentGuard",
    page_icon="\U0001f6e1\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).parent

# ─────────────────────────────────────────
# Carga de recursos
# ─────────────────────────────────────────
@st.cache_resource
def cargar_modelo():
    return joblib.load(BASE / "models" / "modelo_final.pkl")

@st.cache_data
def cargar_metadata():
    with open(BASE / "models" / "model_metadata.json") as f:
        return json.load(f)

@st.cache_data
def cargar_datos():
    return pd.read_csv(BASE / "data" / "processed" / "dataset_limpio.csv")

modelo   = cargar_modelo()
metadata = cargar_metadata()
df       = cargar_datos()

# ─────────────────────────────────────────
# Mapas de etiquetas para la UI
# ─────────────────────────────────────────
OVERTIME_MAP        = {1: "Sí", 0: "No"}
GENDER_MAP          = {1: "Masculino", 0: "Femenino"}
ATTRITION_MAP       = {1: "\u26a0\ufe0f Alto riesgo de abandono", 0: "\u2705 Bajo riesgo de abandono"}
SATISFACTION_LABELS = {1: "Bajo", 2: "Medio", 3: "Alto", 4: "Muy Alto"}
WORKLIFE_LABELS     = {1: "Malo", 2: "Bueno", 3: "Mejor", 4: "Óptimo"}
TRAVEL_LABELS       = {0: "Sin viajes", 1: "Viaja raramente", 2: "Viaja frecuentemente"}

DEPARTMENT_OPTIONS = ["Sales", "Research & Development", "Human Resources"]
JOBROLE_OPTIONS    = [
    "Sales Executive", "Research Scientist", "Laboratory Technician",
    "Manufacturing Director", "Healthcare Representative", "Manager",
    "Sales Representative", "Research Director", "Human Resources",
]
MARITAL_OPTIONS  = ["Divorced", "Married", "Single"]
EDFIELD_OPTIONS  = ["Life Sciences", "Medical", "Marketing", "Other", "Technical Degree", "Human Resources"]

# Medianas del training set para features no expuestas en la UI
MEDIANS = {
    "DailyRate": 802, "HourlyRate": 66, "MonthlyRate": 14236,
    "Education": 3, "JobInvolvement": 3, "JobLevel": 2,
    "PercentSalaryHike": 14, "PerformanceRating": 3,
    "RelationshipSatisfaction": 3, "StockOptionLevel": 1,
    "TrainingTimesLastYear": 3,
}

# Diccionario de variables para la sección Datos
DICCIONARIO_VARS = {
    "Age": "Edad del empleado",
    "Attrition": "¿Abandonó la empresa? (1=Sí, 0=No)",
    "BusinessTravel": "Frecuencia de viajes (0=No viaja, 1=Raramente, 2=Frecuentemente)",
    "DailyRate": "Tarifa diaria (USD)",
    "DistanceFromHome": "Distancia del hogar al trabajo (km)",
    "Education": "Nivel educativo (1=Básico a 5=Doctorado)",
    "EducationField": "Campo de estudio",
    "EnvironmentSatisfaction": "Satisfacción con el entorno laboral (1-4)",
    "Gender": "Género (1=Masculino, 0=Femenino)",
    "HourlyRate": "Tarifa por hora (USD)",
    "JobInvolvement": "Compromiso laboral (1-4)",
    "JobLevel": "Nivel del puesto (1-5)",
    "JobRole": "Rol del puesto",
    "JobSatisfaction": "Satisfacción laboral (1-4)",
    "MaritalStatus": "Estado civil",
    "MonthlyIncome": "Ingreso mensual (USD)",
    "MonthlyRate": "Tarifa mensual (USD)",
    "NumCompaniesWorked": "Número de empresas anteriores",
    "OverTime": "¿Hace horas extra? (1=Sí, 0=No)",
    "PercentSalaryHike": "Porcentaje de aumento salarial",
    "PerformanceRating": "Evaluación de desempeño (3=Buena, 4=Excelente)",
    "RelationshipSatisfaction": "Satisfacción con relaciones laborales (1-4)",
    "StockOptionLevel": "Nivel de opciones accionarias (0-3)",
    "TotalWorkingYears": "Años totales de experiencia laboral",
    "TrainingTimesLastYear": "Capacitaciones el último año",
    "WorkLifeBalance": "Balance vida-trabajo (1=Malo a 4=Óptimo)",
    "YearsAtCompany": "Años en la empresa",
    "YearsInCurrentRole": "Años en el rol actual",
    "YearsSinceLastPromotion": "Años desde la última promoción",
    "YearsWithCurrManager": "Años con el jefe actual",
}

# ─────────────────────────────────────────
# Sidebar — Navegación
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<h2 style='color: {SLATE}; margin-bottom: 0;'>TalentGuard</h2>", unsafe_allow_html=True)
    st.caption(f"Modelo: {metadata['modelo']} \u00b7 F1-macro: {metadata['valor_metrica']}")

    seccion = st.radio(
        "Secciones",
        [
            "Inicio",
            "Datos",
            "Análisis exploratorio",
            "Modelo",
            "Métricas",
            "Predicción",
            "Conclusiones",
        ],
        label_visibility="collapsed",
    )

# ══════════════════════════════════════════
# SECCIÓN 1 — INICIO
# ══════════════════════════════════════════
def seccion_inicio():
    st.markdown(
        f"<h1 style='color: {SLATE};'>\U0001f6e1\ufe0f TalentGuard</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size: 1.15rem; line-height: 1.6;'>"
        "Sistema inteligente para la predicción del riesgo de rotación de empleados. "
        "Este proyecto utiliza machine learning para estimar la probabilidad de que un "
        "empleado abandone la organización, permitiendo a Recursos Humanos tomar "
        "decisiones informadas y anticiparse a la pérdida de talento."
        "</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    # KPIs principales
    st.subheader("Indicadores clave")
    tasa_rotacion = df["Attrition"].mean()
    recall_val = metadata.get("recall_macro", metadata.get("valor_metrica", 0))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de empleados", f"{len(df):,}")
    c2.metric("Tasa de rotación", f"{tasa_rotacion:.1%}")
    c3.metric("Recall del modelo", f"{recall_val:.0%}")
    c4.metric("Precisión (Accuracy)", f"{metadata['accuracy']:.0%}")

    st.divider()

    # Resumen del proyecto
    st.markdown(
        f"<div style='background-color: {FONDO}; color: {TEXTO}; padding: 1.2rem; border-radius: 10px;'>"
        f"<h4 style='color: {SLATE}; margin: 0 0 0.5rem 0;'>\u00bfDe qu\u00e9 se trata?</h4>"
        "<p style='margin: 0; line-height: 1.6;'>"
        "El dataset <strong>IBM HR Analytics Employee Attrition & Performance</strong> "
        "contiene informaci\u00f3n de 1.470 empleados con 35 variables demogr\u00e1ficas, "
        "laborales y de satisfacci\u00f3n. A partir de estos datos, entrenamos un modelo de "
        "<strong>Regresi\u00f3n Log\u00edstica</strong> que estima la probabilidad de abandono "
        "voluntario.<br><br>"
        "Usa el men\u00fa lateral para explorar: datos \u2192 an\u00e1lisis \u2192 modelo \u2192 predicci\u00f3n."
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════
# SECCIÓN 2 — DATOS
# ══════════════════════════════════════════
def seccion_datos():
    st.markdown(f"<h1 style='color: {SLATE};'>\U0001f4ca Datos</h1>", unsafe_allow_html=True)

    st.markdown(
        f"<p>Dataset: <strong>IBM HR Analytics Employee Attrition & Performance</strong> &middot; "
        f"{df.shape[0]} registros &middot; {df.shape[1]} variables</p>",
        unsafe_allow_html=True,
    )

    tab_datos, tab_diccionario = st.tabs(["Vista previa", "Diccionario de variables"])

    with tab_datos:
        st.dataframe(df.head(20), use_container_width=True)
        st.caption("Las variables categóricas ya están codificadas para el modelo (Label Encoding y One-Hot Encoding).")

    with tab_diccionario:
        var_cols = list(DICCIONARIO_VARS.keys())
        desc_cols = list(DICCIONARIO_VARS.values())
        dicc_df = pd.DataFrame({"Variable": var_cols, "Descripción": desc_cols})
        st.dataframe(dicc_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════
# SECCIÓN 3 — ANÁLISIS EXPLORATORIO
# ══════════════════════════════════════════
def seccion_eda():
    st.markdown(f"<h1 style='color: {SLATE};'>\U0001f50d An\u00e1lisis exploratorio</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p>Visualizaciones interactivas para entender los factores asociados a la rotaci\u00f3n.</p>",
        unsafe_allow_html=True,
    )

    # ── Filtros ──
    st.subheader("Filtros")
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        overtime_ops = {"Todos": None, "Con horas extra": 1, "Sin horas extra": 0}
        overtime_sel = st.selectbox("Horas extra (OverTime)", list(overtime_ops.keys()))
    with col_f2:
        sat_ops = {"Todas": None, "Bajo (1)": 1, "Medio (2)": 2, "Alto (3)": 3, "Muy Alto (4)": 4}
        sat_sel = st.selectbox("Satisfacci\u00f3n laboral", list(sat_ops.keys()))
    with col_f3:
        attr_ops = {"Todos": None, "Abandon\u00f3 (S\u00ed)": 1, "Permaneci\u00f3 (No)": 0}
        attr_sel = st.selectbox("Estado de rotaci\u00f3n", list(attr_ops.keys()))

    df_f = df.copy()
    if overtime_ops[overtime_sel] is not None:
        df_f = df_f[df_f["OverTime"] == overtime_ops[overtime_sel]]
    if sat_ops[sat_sel] is not None:
        df_f = df_f[df_f["JobSatisfaction"] == sat_ops[sat_sel]]
    if attr_ops[attr_sel] is not None:
        df_f = df_f[df_f["Attrition"] == attr_ops[attr_sel]]

    st.caption(f"Registros mostrados: {len(df_f)} de {len(df)}")
    st.divider()

    # ── Métricas rápidas del filtro ──
    st.subheader("M\u00e9tricas del conjunto filtrado")
    m1, m2, m3, m4 = st.columns(4)
    if len(df_f) > 0:
        m1.metric("Tasa de abandono", f"{df_f['Attrition'].mean() * 100:.1f}%")
        m2.metric("Ingreso mediano", f"${df_f['MonthlyIncome'].median():,.0f}")
        m3.metric("Antigüedad mediana", f"{df_f['YearsAtCompany'].median():.0f} años")
        m4.metric("Con horas extra", f"{df_f['OverTime'].mean() * 100:.1f}%")
    else:
        for m in [m1, m2, m3, m4]:
            m.metric("—", "0")

    st.divider()

    if len(df_f) == 0:
        st.warning("No hay registros para la combinaci\u00f3n de filtros seleccionada.")
        return

    # ── Viz 1: Distribución de Attrition ──
    st.subheader("1. Distribuci\u00f3n de rotaci\u00f3n")
    col1, col2 = st.columns([1, 2])
    with col1:
        conteo = df_f["Attrition"].value_counts()
        labels = ["No abandona" if i == 0 else "Abandona" for i in conteo.index]
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        ax1.pie(
            conteo.values, labels=labels, autopct="%1.1f%%",
            colors=[SLATE, CORAL], startangle=90, textprops={"color": TEXTO},
        )
        ax1.set_title("El 16% de abandono justifica F1-Score sobre accuracy", color=SLATE)
        st.pyplot(fig1)
        plt.close()
    with col2:
        st.markdown(
            f"<div style='background-color: {FONDO}; color: {TEXTO}; padding: 1rem; border-radius: 8px; line-height: 1.6;'>"
            "<strong>Interpretaci\u00f3n:</strong> El dataset presenta un desbalance significativo: "
            "aproximadamente el <strong>16%</strong> de los empleados abandon\u00f3 la organizaci\u00f3n. "
            "Este desbalance justifica el uso de <strong>F1-Score</strong> como m\u00e9trica principal "
            "y el ajuste de pesos de clase (<code>class_weight='balanced'</code>) en el modelo."
            "</div>",
            unsafe_allow_html=True,
        )
    st.divider()

    # ── Viz 2: Horas Extra vs Attrition ──
    st.subheader("2. Impacto de las horas extra en la rotaci\u00f3n")
    ot_attr = df_f.groupby("OverTime")["Attrition"].mean() * 100
    ot_attr.index = ["Sin horas extra", "Con horas extra"]
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    bars2 = ax2.bar(ot_attr.index, ot_attr.values, color=[SLATE, CORAL], alpha=0.85, width=0.5)
    ax2.bar_label(bars2, fmt="%.1f%%", padding=5, fontsize=11)
    ax2.set_ylabel("Tasa de abandono (%)", color=TEXTO)
    ax2.set_title("Las horas extra triplican el riesgo de abandono", color=SLATE)
    ax2.set_ylim(0, 45)
    ax2.tick_params(colors=TEXTO)
    for spine in ax2.spines.values():
        spine.set_color(SUBTEXTO)
    st.pyplot(fig2)
    plt.close()
    st.caption("Los empleados con horas extra tienen una tasa de abandono ~3 veces mayor.")

    st.divider()

    # ── Viz 3: Ingreso Mensual por Attrition ──
    st.subheader("3. Distribuci\u00f3n del ingreso mensual")
    fig3, ax3 = plt.subplots(figsize=(9, 4))
    for val, label, color in [(0, "No abandona", SLATE), (1, "Abandona", CORAL)]:
        subset = df_f[df_f["Attrition"] == val]["MonthlyIncome"]
        if len(subset) > 0:
            ax3.hist(subset, bins=30, alpha=0.6, label=label, color=color)
    ax3.set_xlabel("Ingreso mensual (USD)", color=TEXTO)
    ax3.set_ylabel("Cantidad de empleados", color=TEXTO)
    ax3.set_title("Quienes abandonan tienen un ingreso mediano $2.000 menor", color=SLATE)
    ax3.legend()
    ax3.tick_params(colors=TEXTO)
    for spine in ax3.spines.values():
        spine.set_color(SUBTEXTO)
    st.pyplot(fig3)
    plt.close()
    st.caption("Los empleados que abandonan se concentran en rangos salariales m\u00e1s bajos.")

    st.divider()

    # ── Viz 4: Satisfacción Laboral ──
    st.subheader("4. Tasa de abandono por satisfacci\u00f3n laboral")
    sat_attr = df_f.groupby("JobSatisfaction")["Attrition"].mean() * 100
    sat_attr.index = [SATISFACTION_LABELS.get(i, i) for i in sat_attr.index]
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    bars4 = ax4.bar(sat_attr.index, sat_attr.values, color=SLATE, alpha=0.85, width=0.5)
    ax4.bar_label(bars4, fmt="%.1f%%", padding=4, fontsize=10)
    ax4.set_ylabel("Tasa de abandono (%)", color=TEXTO)
    ax4.set_title("Baja satisfacci\u00f3n laboral duplica la tasa de abandono", color=SLATE)
    ax4.set_ylim(0, 35)
    ax4.tick_params(colors=TEXTO)
    for spine in ax4.spines.values():
        spine.set_color(SUBTEXTO)
    st.pyplot(fig4)
    plt.close()
    st.caption("A menor satisfacci\u00f3n laboral, mayor probabilidad de abandono.")

    st.divider()

    # ── Viz 5: Antigüedad vs Attrition ──
    st.subheader("5. Riesgo de abandono por antig\u00fcedad en la empresa")
    df_bins = df_f.copy()
    df_bins["AniosGrupo"] = pd.cut(
        df_bins["YearsAtCompany"],
        bins=[0, 1, 3, 7, 15, 40],
        labels=["0\u20131 año", "2\u20133 años", "4\u20137 años", "8\u201315 años", "16+ años"],
        right=True,
    )
    years_attr = df_bins.groupby("AniosGrupo", observed=True)["Attrition"].mean() * 100
    fig5, ax5 = plt.subplots(figsize=(9, 4))
    bars5 = ax5.bar(years_attr.index, years_attr.values, color=SLATE, alpha=0.85, width=0.6)
    ax5.bar_label(bars5, fmt="%.1f%%", padding=4, fontsize=10)
    ax5.set_xlabel("Antig\u00fcedad en la empresa", color=TEXTO)
    ax5.set_ylabel("Tasa de abandono (%)", color=TEXTO)
    ax5.set_title("El 61% de los abandonos ocurren en los primeros 3 a\u00f1os", color=SLATE)
    ax5.set_ylim(0, 50)
    ax5.tick_params(colors=TEXTO)
    for spine in ax5.spines.values():
        spine.set_color(SUBTEXTO)
    st.pyplot(fig5)
    plt.close()
    st.caption(
        "El 61% de los abandonos ocurren en los primeros 3 a\u00f1os \u2014 "
        "per\u00edodo cr\u00edtico para las estrategias de retenci\u00f3n temprana."
    )


# ══════════════════════════════════════════
# SECCIÓN 4 — MODELO
# ══════════════════════════════════════════
def seccion_modelo():
    st.markdown(f"<h1 style='color: {SLATE};'>\U0001f916 Modelo</h1>", unsafe_allow_html=True)

    st.markdown(
        "<p style='line-height: 1.7;'>"
        "Entrenamos un modelo de <strong>Regresi\u00f3n Log\u00edstica</strong> para estimar "
        "la probabilidad de que un empleado abandone voluntariamente la organizaci\u00f3n. "
        "Este algoritmo fue seleccionado porque es <strong>interpretable</strong> — "
        "podemos entender qu\u00e9 variables influyen m\u00e1s en el resultado — "
        "y tiene un rendimiento competitivo frente a modelos m\u00e1s complejos."
        "</p>",
        unsafe_allow_html=True,
    )

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown(
            f"<div style='background-color: {FONDO}; color: {TEXTO}; padding: 1rem; border-radius: 8px;'>"
            f"<h4 style='color: {SLATE}; margin: 0 0 0.5rem 0;'>\u00bfC\u00f3mo funciona?</h4>"
            "<p style='line-height: 1.6; margin: 0;'>"
            "El modelo aprende patrones a partir de empleados del pasado: "
            "qui\u00e9nes se quedaron y qui\u00e9nes se fueron. Cuando ingresas "
            "los datos de un empleado nuevo, el modelo compara su perfil "
            "con los patrones aprendidos y estima una probabilidad de abandono."
            "</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    with col_m2:
        st.markdown(
            f"<div style='background-color: {FONDO}; color: {TEXTO}; padding: 1rem; border-radius: 8px;'>"
            f"<h4 style='color: {SLATE}; margin: 0 0 0.5rem 0;'>Variables utilizadas</h4>"
            "<p style='line-height: 1.6; margin: 0;'>"
            "El modelo considera <strong>43 variables</strong> que incluyen datos "
            "demogr\u00e1ficos (edad, g\u00e9nero, estado civil), laborales (ingreso, "
            "antig\u00fcedad, horas extra, cargo) y de satisfacci\u00f3n (satisfacci\u00f3n "
            "laboral, balance vida-trabajo, entorno)."
            "</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown(
        f"<div style='background-color: #FFF3E0; color: {TEXTO}; padding: 1rem; border-radius: 8px; border-left: 4px solid {ALERTA};'>"
        "<strong>\u26a0\ufe0f Importante:</strong> El modelo NO determina el futuro de una persona. "
        "Estima una <strong>probabilidad</strong> con base en datos hist\u00f3ricos. "
        "El resultado debe usarse como <strong>apoyo a la decisi\u00f3n</strong>, "
        "no como \u00fanico criterio para acciones de personal."
        "</div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════
# SECCIÓN 5 — MÉTRICAS
# ══════════════════════════════════════════
def seccion_metricas():
    st.markdown(f"<h1 style='color: {SLATE};'>\U0001f4c8 M\u00e9tricas del modelo</h1>", unsafe_allow_html=True)

    st.markdown(
        "<p>Rendimiento del modelo sobre el conjunto de prueba (294 registros reservados).</p>",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("F1-macro", f"{metadata['valor_metrica']:.3f}")
    c2.metric("Accuracy", f"{metadata['accuracy']:.3f}")
    c3.metric("ROC-AUC", f"{metadata['roc_auc']:.3f}")
    c4.metric("Precisi\u00f3n macro", f"{metadata.get('precision_macro', 0):.3f}")

    st.divider()

    # Lectura sencilla
    st.subheader("\U0001f4d6 Lectura sencilla de las m\u00e9tricas")

    f1_yes = metadata.get("f1_yes", 0)
    recall_val = metadata.get("recall_macro", 0)
    accuracy = metadata["accuracy"]
    auc = metadata["roc_auc"]

    st.markdown(
        f"<div style='background-color: {FONDO}; color: {TEXTO}; padding: 1.2rem; border-radius: 10px; line-height: 1.8;'>"
        f"<p style='margin: 0;'>"
        f"\u2022 <strong>Recall ({recall_val:.0%}):</strong> De cada 10 empleados que realmente "
        f"abandonan, el modelo detecta aproximadamente <strong>{round(recall_val * 10)}</strong>. "
        f"Este es el n\u00famero m\u00e1s importante para el negocio \u2014 preferimos "
        f"identificar a alguien en riesgo aunque de vez en cuando marquemos un falso positivo."
        f"<br><br>"
        f"\u2022 <strong>Accuracy ({accuracy:.0%}):</strong> El modelo acierta en "
        f"{round(accuracy * 100)} de cada 100 predicciones. En un dataset "
        f"desbalanceado (84% permanecen, 16% abandonan), esta m\u00e9trica por s\u00ed sola "
        f"no cuenta toda la historia."
        f"<br><br>"
        f"\u2022 <strong>ROC-AUC ({auc:.3f}):</strong> Mide la capacidad del modelo para "
        f"separar empleados que se quedan de los que se van. Un valor de 0.5 es "
        f"aleatorio, 1.0 es perfecto. Nuestro modelo obtiene <strong>{auc:.3f}</strong>, "
        f"lo que indica un poder predictivo s\u00f3lido."
        f"<br><br>"
        f"\u2022 <strong>F1-Yes ({f1_yes:.3f}):</strong> Mide el rendimiento espec\u00edficamente "
        f"en la clase minoritaria (abandono). Es menor que el F1-macro porque la clase "
        f"de abandono tiene solo 47 casos en el conjunto de prueba \u2014 "
        f"un error individual pesa m\u00e1s."
        f"</p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        f"<div style='background-color: #E8F8F5; color: {TEXTO}; padding: 1rem; border-radius: 8px; border-left: 4px solid {EXITO};'>"
        "<strong>\u00bfPor qu\u00e9 recall y no accuracy?</strong> En retenci\u00f3n de talento, "
        "el costo de un falso negativo (no detectar a alguien que se va) es mucho mayor "
        "que el de un falso positivo (agendar una reuni\u00f3n innecesaria). Por eso "
        "optimizamos el modelo para maximizar el recall, incluso si eso reduce la precisi\u00f3n general."
        "</div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════
# SECCIÓN 6 — PREDICCIÓN
# ══════════════════════════════════════════
def seccion_prediccion():
    st.markdown(f"<h1 style='color: {SLATE};'>\U0001f3af Predicci\u00f3n de riesgo de abandono</h1>", unsafe_allow_html=True)

    st.markdown(
        f"<div style='background-color: #FFF3E0; color: {TEXTO}; padding: 0.8rem; border-radius: 8px; border-left: 4px solid {ALERTA}; margin-bottom: 1rem;'>"
        "\u26a0\ufe0f El resultado es una <strong>estimaci\u00f3n estad\u00edstica</strong>. "
        "Debe ser revisado por una persona responsable de Recursos Humanos "
        "antes de tomar cualquier decisi\u00f3n sobre el empleado."
        "</div>",
        unsafe_allow_html=True,
    )

    # Formulario en 3 columnas
    st.subheader("Ingresa los datos del empleado")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**Datos personales**")
        age              = st.slider("Edad", 18, 60, 35)
        gender           = st.selectbox("Género", [0, 1], format_func=lambda x: GENDER_MAP[x])
        marital_status   = st.selectbox("Estado civil", MARITAL_OPTIONS)
        num_companies    = st.slider("Empresas anteriores", 0, 9, 2)
        distance         = st.slider("Distancia al trabajo (km)", 1, 29, 7)
        total_work_yrs   = st.slider("Años totales de experiencia", 0, 40, 10)

    with col_b:
        st.markdown("**Puesto y compensación**")
        department       = st.selectbox("Departamento", DEPARTMENT_OPTIONS)
        job_role         = st.selectbox("Rol", JOBROLE_OPTIONS)
        education_field  = st.selectbox("Campo de estudio", EDFIELD_OPTIONS)
        monthly_income   = st.number_input("Ingreso mensual (USD)", 1000, 20000, 5000, step=100)
        years_at_company = st.slider("Años en la empresa", 0, 40, 5)
        years_in_role    = st.slider("Años en el rol actual", 0, 18, 3)
        years_since_promo= st.slider("Años desde última promoción", 0, 15, 2)

    with col_c:
        st.markdown("**Satisfacción y condiciones**")
        overtime         = st.selectbox("¿Realiza horas extra?", [0, 1], format_func=lambda x: OVERTIME_MAP[x])
        job_satisfaction = st.selectbox("Satisfacción laboral", [1, 2, 3, 4], format_func=lambda x: SATISFACTION_LABELS[x], index=2)
        work_life        = st.selectbox("Balance vida-trabajo", [1, 2, 3, 4], format_func=lambda x: WORKLIFE_LABELS[x], index=2)
        env_satisfaction = st.selectbox("Satisfacción con el entorno", [1, 2, 3, 4], format_func=lambda x: SATISFACTION_LABELS[x], index=2)
        business_travel  = st.selectbox("Frecuencia de viajes", [0, 1, 2], format_func=lambda x: TRAVEL_LABELS[x])

    st.divider()

    if st.button("\U0001f3af Predecir riesgo de abandono", use_container_width=True, type="primary"):
        feature_names = metadata["variables_entrada"]

        # Base con medianas — evita z-scores extremos en el StandardScaler
        input_dict = {col: MEDIANS.get(col, 0) for col in feature_names}

        # Numéricos directos
        input_dict.update({
            "Age":                     age,
            "Gender":                  gender,
            "MonthlyIncome":           monthly_income,
            "YearsAtCompany":          years_at_company,
            "YearsInCurrentRole":      years_in_role,
            "YearsSinceLastPromotion": years_since_promo,
            "OverTime":                overtime,
            "JobSatisfaction":         job_satisfaction,
            "WorkLifeBalance":         work_life,
            "EnvironmentSatisfaction": env_satisfaction,
            "BusinessTravel":          business_travel,
            "TotalWorkingYears":       total_work_yrs,
            "NumCompaniesWorked":      num_companies,
            "DistanceFromHome":        distance,
        })

        # OHE — Department (referencia: Human Resources)
        input_dict["Department_Research & Development"] = int(department == "Research & Development")
        input_dict["Department_Sales"]                  = int(department == "Sales")

        # OHE — JobRole (referencia: Healthcare Representative)
        for role, col in {
            "Human Resources":        "JobRole_Human Resources",
            "Laboratory Technician":  "JobRole_Laboratory Technician",
            "Manager":                "JobRole_Manager",
            "Manufacturing Director": "JobRole_Manufacturing Director",
            "Research Director":      "JobRole_Research Director",
            "Research Scientist":     "JobRole_Research Scientist",
            "Sales Executive":        "JobRole_Sales Executive",
            "Sales Representative":   "JobRole_Sales Representative",
        }.items():
            input_dict[col] = int(job_role == role)

        # OHE — MaritalStatus (referencia: Divorced)
        input_dict["MaritalStatus_Married"] = int(marital_status == "Married")
        input_dict["MaritalStatus_Single"]  = int(marital_status == "Single")

        # OHE — EducationField (referencia: Human Resources)
        for field, col in {
            "Life Sciences":    "EducationField_Life Sciences",
            "Marketing":        "EducationField_Marketing",
            "Medical":          "EducationField_Medical",
            "Other":            "EducationField_Other",
            "Technical Degree": "EducationField_Technical Degree",
        }.items():
            if col in input_dict:
                input_dict[col] = int(education_field == field)

        input_df = pd.DataFrame([input_dict])

        prediccion    = modelo.predict(input_df)[0]
        probabilidad  = modelo.predict_proba(input_df)[0]
        prob_abandono = probabilidad[1]

        # ── Resultado ──
        st.divider()
        st.subheader("Resultado")
        color = RIESGO if prediccion == 1 else EXITO
        icono = "\U0001f534" if prediccion == 1 else "\U0001f7e2"
        st.markdown(f"## {icono} {ATTRITION_MAP[prediccion]}")

        col_r1, col_r2 = st.columns(2)
        col_r1.metric("Probabilidad de abandono", f"{prob_abandono * 100:.1f}%")
        col_r2.metric("Probabilidad de permanencia", f"{(1 - prob_abandono) * 100:.1f}%")

        # Barra de probabilidad
        fig_p, ax_p = plt.subplots(figsize=(8, 1.2))
        ax_p.barh(
            [""], [prob_abandono],
            color=color, height=0.5,
        )
        ax_p.barh(
            [""], [1 - prob_abandono], left=[prob_abandono],
            color="#e0e0e0", height=0.5,
        )
        ax_p.set_xlim(0, 1)
        ax_p.axvline(0.5, color="gray", linestyle="--", linewidth=1)
        ax_p.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax_p.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
        ax_p.set_title("Probabilidad de abandono", color=SLATE)
        st.pyplot(fig_p)
        plt.close()

        # ── Interpretación ──
        st.divider()
        st.subheader("Interpretaci\u00f3n")

        riesgo_txt = (
            f"El modelo estima que este empleado tiene una probabilidad del "
            f"**{prob_abandono * 100:.1f}%** de abandonar la organizaci\u00f3n. "
        )

        if prediccion == 1:
            st.warning(
                riesgo_txt +
                "Se recomienda que el \u00e1rea de Recursos Humanos priorice una reuni\u00f3n "
                "de seguimiento para identificar factores de insatisfacci\u00f3n y evaluar "
                "acciones de retenci\u00f3n: ajuste de carga laboral, plan de desarrollo "
                "profesional o revisi\u00f3n salarial."
            )
        else:
            st.success(
                riesgo_txt +
                "El perfil no presenta se\u00f1ales de alerta inmediatas. "
                "Se recomienda mantener el seguimiento peri\u00f3dico y los programas "
                "de bienestar vigentes."
            )

        # ── Factores de riesgo ──
        st.subheader("Factores de riesgo identificados en este perfil")
        factores = []
        if overtime == 1:
            factores.append("\U0001f534 Realiza horas extra — aumenta el riesgo hasta 3 veces según el EDA")
        if monthly_income < 3500:
            factores.append("\U0001f534 Ingreso por debajo de la mediana de quienes abandonan ($3.202)")
        if years_at_company <= 3:
            factores.append("\U0001f7e1 Menos de 3 años en la empresa — período crítico de fidelización")
        if job_satisfaction <= 2:
            factores.append("\U0001f534 Satisfacción laboral baja — tasa de abandono del 22.8% en nivel bajo")
        if work_life == 1:
            factores.append("\U0001f534 Balance vida-trabajo malo — mayor correlación con abandono")
        if business_travel == 2:
            factores.append("\U0001f7e1 Viajes frecuentes — factor de desgaste identificado en el EDA")
        if marital_status == "Single":
            factores.append("\U0001f7e1 Soltero/a — mayor movilidad laboral históricamente observada")
        if num_companies >= 4:
            factores.append("\U0001f7e1 Alta rotación previa — trabajó en 4 o más empresas anteriores")

        for f in factores:
            st.markdown(f)
        if not factores:
            st.markdown("\u2705 No se identificaron factores de riesgo destacados en este perfil.")

        st.divider()
        st.caption(
            "Este resultado es generado por un modelo de Machine Learning entrenado sobre "
            "datos históricos sintéticos. No representa una evaluación definitiva del empleado "
            "ni debe utilizarse como único criterio para decisiones de gestión de personal. "
            "La decisión final es responsabilidad exclusiva del área de Recursos Humanos."
        )


# ══════════════════════════════════════════
# SECCIÓN 7 — CONCLUSIONES
# ══════════════════════════════════════════
def seccion_conclusiones():
    st.markdown(f"<h1 style='color: {SLATE};'>\u2705 Conclusiones y limitaciones</h1>", unsafe_allow_html=True)

    st.subheader("\U0001f50d Hallazgos principales")
    st.markdown(
        f"<div style='background-color: {FONDO}; color: {TEXTO}; padding: 1.2rem; border-radius: 10px; line-height: 1.8;'>"
        "<ul>"
        "<li><strong>Horas extra:</strong> Los empleados que hacen horas extra tienen "
        "una tasa de abandono ~3 veces mayor que quienes no las hacen.</li>"
        "<li><strong>Ingreso:</strong> Los empleados que abandonan se concentran en "
        "rangos salariales m\u00e1s bajos (ingreso mediano de $3.020 vs. $5.310 de quienes permanecen).</li>"
        "<li><strong>Satisfacci\u00f3n laboral:</strong> A menor satisfacci\u00f3n, mayor rotaci\u00f3n. "
        "La tasa de abandono en satisfacci\u00f3n baja (1) es del 22.8%, vs. 9.6% en satisfacci\u00f3n muy alta (4).</li>"
        "<li><strong>Antig\u00fcedad cr\u00edtica:</strong> El 61% de los abandonos ocurren en los "
        "primeros 3 a\u00f1os en la empresa.</li>"
        f"<li><strong>Modelo:</strong> La Regresi\u00f3n Log\u00edstica logr\u00f3 un F1-macro de 0.661 "
        f"y un recall de {metadata.get('recall_macro', 0):.0%}, identificando la mayor\u00eda de los casos de abandono real.</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("\u26a0\ufe0f Limitaciones")
    st.markdown(
        f"<div style='background-color: #FFF3E0; color: {TEXTO}; padding: 1.2rem; border-radius: 10px; line-height: 1.8;'>"
        "<ul>"
        "<li><strong>Datos de una sola empresa:</strong> El dataset corresponde a una "
        "empresa estadounidense y un solo per\u00edodo de tiempo. Los resultados no "
        "necesariamente generalizan a otras organizaciones o pa\u00edses.</li>"
        "<li><strong>Variables no observadas:</strong> Factores importantes como el clima "
        "laboral real, ofertas externas de trabajo o problemas personales no est\u00e1n "
        "disponibles en el dataset.</li>"
        "<li><strong>Sesgos hist\u00f3ricos:</strong> El modelo puede reflejar sesgos "
        "presentes en los datos de entrenamiento (por ejemplo, decisiones de contrataci\u00f3n "
        "o promoci\u00f3n hist\u00f3ricas).</li>"
        f"<li><strong>Clase desbalanceada:</strong> Con solo 16% de casos de abandono, "
        f"el modelo tiene rendimiento limitado en la clase minoritaria (F1-Yes de {metadata.get('f1_yes', 0):.3f}).</li>"
        "<li><strong>Datos sint\u00e9ticos:</strong> El dataset de IBM es sint\u00e9tico "
        "(generado para fines educativos), por lo que los resultados no representan "
        "necesariamente patrones reales de rotaci\u00f3n.</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("\U0001f4a1 Pr\u00f3ximos pasos")
    st.markdown(
        f"<div style='background-color: #E8F8F5; color: {TEXTO}; padding: 1.2rem; border-radius: 10px; line-height: 1.8;'>"
        "<ul>"
        "<li>Probar algoritmos adicionales (XGBoost, Gradient Boosting) con ajuste de hiperpar\u00e1metros.</li>"
        "<li>Incorporar an\u00e1lisis de equidad para detectar sesgos por subgrupos (g\u00e9nero, edad).</li>"
        "<li>Exponer el modelo mediante una API para integraci\u00f3n con sistemas de RRHH.</li>"
        "<li>Desplegar el dashboard en la nube para acceso del equipo.</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        f"<div style='background-color: #F5F0FF; color: {TEXTO}; padding: 1.2rem; border-radius: 10px; line-height: 1.6; "
        f"border-left: 4px solid {SLATE};'>"
        "<strong>\U0001f6e1\ufe0f Advertencia de uso responsable:</strong> Este sistema es una "
        "herramienta de <strong>apoyo a la decisi\u00f3n</strong>, no un sustituto del "
        "criterio humano. Las predicciones deben ser interpretadas por profesionales "
        "de Recursos Humanos en el contexto de cada empleado. No utilizar este sistema "
        "como \u00fanico determinante para despidos, contrataciones o cualquier acci\u00f3n "
        "que afecte la carrera de una persona."
        "</div>",
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════
# Ruteo de secciones
# ══════════════════════════════════════════
SECCIONES = {
    "Inicio": seccion_inicio,
    "Datos": seccion_datos,
    "Análisis exploratorio": seccion_eda,
    "Modelo": seccion_modelo,
    "Métricas": seccion_metricas,
    "Predicción": seccion_prediccion,
    "Conclusiones": seccion_conclusiones,
}

SECCIONES[seccion]()
