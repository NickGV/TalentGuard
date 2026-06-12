import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import json
from pathlib import Path

# ─────────────────────────────────────────
# Configuración general
# ─────────────────────────────────────────
st.set_page_config(
    page_title="TalentGuard",
    page_icon="🛡️",
    layout="wide"
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
ATTRITION_MAP       = {1: "⚠️ Alto riesgo de abandono", 0: "✅ Bajo riesgo de abandono"}
SATISFACTION_LABELS = {1: "Bajo", 2: "Medio", 3: "Alto", 4: "Muy Alto"}
WORKLIFE_LABELS     = {1: "Malo", 2: "Bueno", 3: "Mejor", 4: "Óptimo"}
TRAVEL_LABELS       = {0: "Sin viajes", 1: "Viaja raramente", 2: "Viaja frecuentemente"}

DEPARTMENT_OPTIONS = ["Sales", "Research & Development", "Human Resources"]
JOBROLE_OPTIONS    = [
    "Sales Executive", "Research Scientist", "Laboratory Technician",
    "Manufacturing Director", "Healthcare Representative", "Manager",
    "Sales Representative", "Research Director", "Human Resources"
]
MARITAL_OPTIONS  = ["Divorced", "Married", "Single"]
EDFIELD_OPTIONS  = ["Life Sciences", "Medical", "Marketing", "Other", "Technical Degree", "Human Resources"]

# Medianas del training set para features no expuestas en la UI.
# Usar 0 causaría z-scores fuera de rango en el StandardScaler del pipeline.
MEDIANS = {
    "DailyRate": 802, "HourlyRate": 66, "MonthlyRate": 14236,
    "Education": 3, "JobInvolvement": 3, "JobLevel": 2,
    "PercentSalaryHike": 14, "PerformanceRating": 3,
    "RelationshipSatisfaction": 3, "StockOptionLevel": 1,
    "TrainingTimesLastYear": 3,
}

# ─────────────────────────────────────────
# Encabezado
# ─────────────────────────────────────────
st.title("🛡️ TalentGuard")
st.caption(
    "Sistema Inteligente para la Predicción del Riesgo de Rotación de Empleados · "
    f"Modelo: {metadata['modelo']} · "
    f"F1-macro: {metadata['valor_metrica']}"
)
st.divider()

tab1, tab2 = st.tabs(["📊 Análisis Exploratorio", "🔮 Predicción de Riesgo"])

# ══════════════════════════════════════════
# TAB 1 — Análisis Exploratorio
# ══════════════════════════════════════════
with tab1:
    st.header("Exploración del Dataset")
    st.markdown(
        "Dataset: **IBM HR Analytics Employee Attrition & Performance** · "
        f"{df.shape[0]} registros · {df.shape[1]} variables"
    )

    # ── Filtros ──────────────────────────────────────────────────────
    st.subheader("Filtros")
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        overtime_ops = {"Todos": None, "Con horas extra": 1, "Sin horas extra": 0}
        overtime_sel = st.selectbox("Horas extra (OverTime)", list(overtime_ops.keys()))
    with col_f2:
        sat_ops = {"Todas": None, "Bajo (1)": 1, "Medio (2)": 2, "Alto (3)": 3, "Muy Alto (4)": 4}
        sat_sel = st.selectbox("Satisfacción laboral", list(sat_ops.keys()))
    with col_f3:
        attr_ops = {"Todos": None, "Abandonó (Yes)": 1, "Permaneció (No)": 0}
        attr_sel = st.selectbox("Estado de rotación", list(attr_ops.keys()))

    df_f = df.copy()
    if overtime_ops[overtime_sel] is not None:
        df_f = df_f[df_f["OverTime"] == overtime_ops[overtime_sel]]
    if sat_ops[sat_sel] is not None:
        df_f = df_f[df_f["JobSatisfaction"] == sat_ops[sat_sel]]
    if attr_ops[attr_sel] is not None:
        df_f = df_f[df_f["Attrition"] == attr_ops[attr_sel]]

    st.caption(f"Registros mostrados: {len(df_f)} de {len(df)}")
    st.divider()

    # ── Métricas rápidas ─────────────────────────────────────────────
    st.subheader("Métricas del Dataset Filtrado")
    m1, m2, m3, m4 = st.columns(4)
    if len(df_f) > 0:
        tasa_rot  = df_f["Attrition"].mean() * 100
        ing_med   = df_f["MonthlyIncome"].median()
        anios_med = df_f["YearsAtCompany"].median()
        pct_ot    = df_f["OverTime"].mean() * 100
    else:
        tasa_rot = ing_med = anios_med = pct_ot = 0

    m1.metric("Tasa de abandono",   f"{tasa_rot:.1f}%")
    m2.metric("Ingreso mediano",    f"${ing_med:,.0f}")
    m3.metric("Antigüedad mediana", f"{anios_med:.0f} años")
    m4.metric("Con horas extra",    f"{pct_ot:.1f}%")
    st.divider()

    if len(df_f) == 0:
        st.warning("No hay registros para la combinación de filtros seleccionada.")
    else:
        # ── Viz 1: Distribución de Attrition ─────────────────────────
        st.subheader("1. Distribución de Rotación")
        col1, col2 = st.columns([1, 2])
        with col1:
            conteo = df_f["Attrition"].value_counts()
            labels = ["No abandona" if i == 0 else "Abandona" for i in conteo.index]
            fig1, ax1 = plt.subplots(figsize=(4, 4))
            ax1.pie(
                conteo.values, labels=labels, autopct="%1.1f%%",
                colors=["#4C72B0", "#DD8452"], startangle=90
            )
            ax1.set_title("Distribución de Attrition")
            st.pyplot(fig1)
            plt.close()
        with col2:
            st.markdown("""
            **Interpretación:**
            El dataset presenta un desbalance significativo: aproximadamente el **16%** de los
            empleados abandonó la organización. Este desbalance justifica el uso de F1-Score
            como métrica principal y el ajuste de pesos de clase (`class_weight='balanced'`)
            en el modelo.
            """)
        st.divider()

        # ── Viz 2: Horas Extra vs Attrition ──────────────────────────
        st.subheader("2. Impacto de las Horas Extra en la Rotación")
        ot_attr = df_f.groupby("OverTime")["Attrition"].mean() * 100
        ot_attr.index = ["Sin horas extra", "Con horas extra"]
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        bars2 = ax2.bar(ot_attr.index, ot_attr.values, color=["#4C72B0", "#DD8452"], alpha=0.85, width=0.5)
        ax2.bar_label(bars2, fmt="%.1f%%", padding=5, fontsize=11)
        ax2.set_ylabel("Tasa de abandono (%)")
        ax2.set_title("Tasa de Abandono según Horas Extra")
        ax2.set_ylim(0, 45)
        st.pyplot(fig2)
        plt.close()
        st.caption("Los empleados con horas extra tienen una tasa de abandono ~3 veces mayor.")
        st.divider()

        # ── Viz 3: Ingreso Mensual por Attrition ─────────────────────
        st.subheader("3. Distribución del Ingreso Mensual")
        fig3, ax3 = plt.subplots(figsize=(9, 4))
        for val, label, color in [(0, "No abandona", "#4C72B0"), (1, "Abandona", "#DD8452")]:
            subset = df_f[df_f["Attrition"] == val]["MonthlyIncome"]
            if len(subset) > 0:
                ax3.hist(subset, bins=30, alpha=0.6, label=label, color=color)
        ax3.set_xlabel("Ingreso mensual (USD)")
        ax3.set_ylabel("Cantidad de empleados")
        ax3.set_title("Distribución del Ingreso Mensual por Attrition")
        ax3.legend()
        st.pyplot(fig3)
        plt.close()
        st.caption("Los empleados que abandonan se concentran en rangos salariales más bajos.")
        st.divider()

        # ── Viz 4: Satisfacción Laboral ───────────────────────────────
        st.subheader("4. Tasa de Abandono por Satisfacción Laboral")
        sat_attr = df_f.groupby("JobSatisfaction")["Attrition"].mean() * 100
        sat_attr.index = [SATISFACTION_LABELS.get(i, i) for i in sat_attr.index]
        fig4, ax4 = plt.subplots(figsize=(8, 4))
        bars4 = ax4.bar(sat_attr.index, sat_attr.values, color="#4C72B0", alpha=0.85, width=0.5)
        ax4.bar_label(bars4, fmt="%.1f%%", padding=4, fontsize=10)
        ax4.set_ylabel("Tasa de abandono (%)")
        ax4.set_title("Tasa de Abandono por Nivel de Satisfacción Laboral")
        ax4.set_ylim(0, 35)
        st.pyplot(fig4)
        plt.close()
        st.caption("A menor satisfacción laboral, mayor probabilidad de abandono.")
        st.divider()

        # ── Viz 5: Antigüedad vs Attrition ───────────────────────────
        st.subheader("5. Riesgo de Abandono por Antigüedad en la Empresa")
        df_bins = df_f.copy()
        df_bins["AniosGrupo"] = pd.cut(
            df_bins["YearsAtCompany"],
            bins=[0, 1, 3, 7, 15, 40],
            labels=["0–1 año", "2–3 años", "4–7 años", "8–15 años", "16+ años"],
            right=True
        )
        years_attr = df_bins.groupby("AniosGrupo", observed=True)["Attrition"].mean() * 100
        fig5, ax5 = plt.subplots(figsize=(9, 4))
        bars5 = ax5.bar(years_attr.index, years_attr.values, color="#4C72B0", alpha=0.85, width=0.6)
        ax5.bar_label(bars5, fmt="%.1f%%", padding=4, fontsize=10)
        ax5.set_xlabel("Antigüedad en la empresa")
        ax5.set_ylabel("Tasa de abandono (%)")
        ax5.set_title("Tasa de Abandono por Tramos de Antigüedad")
        ax5.set_ylim(0, 50)
        st.pyplot(fig5)
        plt.close()
        st.caption(
            "El 61% de los abandonos ocurren en los primeros 3 años — "
            "período crítico para las estrategias de retención temprana."
        )

# ══════════════════════════════════════════
# TAB 2 — Predicción
# ══════════════════════════════════════════
with tab2:
    st.header("Predicción de Riesgo de Abandono")

    # Métricas del modelo leídas desde model_metadata.json
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Modelo",    metadata["modelo"])
    mc2.metric("F1-macro",  metadata["valor_metrica"])
    mc3.metric("ROC-AUC",   metadata["roc_auc"])
    mc4.metric("Accuracy",  metadata["accuracy"])

    st.info(
        "⚠️ El resultado es una estimación generada por el modelo. "
        "Debe ser revisado por una persona responsable del área de Recursos Humanos "
        "antes de tomar cualquier decisión sobre el empleado."
    )
    st.divider()

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

    if st.button("🔮 Predecir riesgo de abandono", use_container_width=True, type="primary"):

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

        # ── Resultado ────────────────────────────────────────────────
        st.divider()
        st.subheader("Resultado")
        color = "🔴" if prediccion == 1 else "🟢"
        st.markdown(f"## {color} {ATTRITION_MAP[prediccion]}")

        col_r1, col_r2 = st.columns(2)
        col_r1.metric("Probabilidad de abandono",    f"{prob_abandono*100:.1f}%")
        col_r2.metric("Probabilidad de permanencia", f"{(1-prob_abandono)*100:.1f}%")

        fig_p, ax_p = plt.subplots(figsize=(8, 1.2))
        ax_p.barh([""], [prob_abandono],
                  color="#DD8452" if prediccion == 1 else "#4C72B0", height=0.5)
        ax_p.barh([""], [1 - prob_abandono], left=[prob_abandono], color="#e0e0e0", height=0.5)
        ax_p.set_xlim(0, 1)
        ax_p.axvline(0.5, color="gray", linestyle="--", linewidth=1)
        ax_p.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax_p.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
        ax_p.set_title("Probabilidad de abandono")
        st.pyplot(fig_p)
        plt.close()

        # ── Interpretación ───────────────────────────────────────────
        st.divider()
        st.subheader("Interpretación")
        if prediccion == 1:
            st.warning(
                f"El modelo estima que este empleado tiene una probabilidad del "
                f"**{prob_abandono*100:.1f}%** de abandonar la organización. "
                f"Se recomienda que el área de Recursos Humanos priorice una reunión "
                f"de seguimiento para identificar factores de insatisfacción y evaluar "
                f"acciones de retención: ajuste de carga laboral, plan de desarrollo "
                f"profesional o revisión salarial."
            )
        else:
            st.success(
                f"El modelo estima que este empleado tiene una probabilidad del "
                f"**{prob_abandono*100:.1f}%** de abandonar la organización. "
                f"El perfil no presenta señales de alerta inmediatas. "
                f"Se recomienda mantener el seguimiento periódico y los programas "
                f"de bienestar vigentes."
            )

        # ── Factores de riesgo ───────────────────────────────────────
        st.subheader("Factores de riesgo identificados en este perfil")
        factores = []
        if overtime == 1:
            factores.append("🔴 Realiza horas extra — aumenta el riesgo hasta 3 veces según el EDA")
        if monthly_income < 3500:
            factores.append("🔴 Ingreso por debajo de la mediana de quienes abandonan ($3.202)")
        if years_at_company <= 3:
            factores.append("🟡 Menos de 3 años en la empresa — período crítico de fidelización")
        if job_satisfaction <= 2:
            factores.append("🔴 Satisfacción laboral baja — tasa de abandono del 22.8% en nivel bajo")
        if work_life == 1:
            factores.append("🔴 Balance vida-trabajo malo — mayor correlación con abandono")
        if business_travel == 2:
            factores.append("🟡 Viajes frecuentes — factor de desgaste identificado en el EDA")
        if marital_status == "Single":
            factores.append("🟡 Soltero/a — mayor movilidad laboral históricamente observada")
        if num_companies >= 4:
            factores.append("🟡 Alta rotación previa — trabajó en 4 o más empresas anteriores")

        for f in factores:
            st.markdown(f)
        if not factores:
            st.markdown("✅ No se identificaron factores de riesgo destacados en este perfil.")

        st.divider()
        st.caption(
            "Este resultado es generado por un modelo de Machine Learning entrenado sobre "
            "datos históricos sintéticos. No representa una evaluación definitiva del empleado "
            "ni debe utilizarse como único criterio para decisiones de gestión de personal. "
            "La decisión final es responsabilidad exclusiva del área de Recursos Humanos."
        )
