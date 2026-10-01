import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="COCOMO Estimation Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DARK / MINIMAL UI
# ============================================================
st.markdown("""
<style>
    /* Main application */
    .stApp {
        background: #050505;
        color: #F5F2ED;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #252525 !important;
        border-right: 1px solid #3A3A3A;
    }

    section[data-testid="stSidebar"] > div {
        background: #252525 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #F5F2ED !important;
    }

    /* Text */
    h1, h2, h3, h4, p, label, span, div {
        color: #F5F2ED;
    }

    h1 {
        font-weight: 700;
        letter-spacing: -0.8px;
    }

    h2, h3 {
        letter-spacing: -0.3px;
    }

    .subtle {
        color: #A7A29A !important;
    }

    /* Inputs */
    div[data-baseweb="input"] {
        background: #111111 !important;
        border-color: #484848 !important;
    }

    div[data-baseweb="input"] input {
        color: #F5F2ED !important;
        background: #111111 !important;
    }

    div[data-baseweb="select"] > div {
        background: #111111 !important;
        color: #F5F2ED !important;
    }

    /* Radio */
    div[role="radiogroup"] label {
        color: #F5F2ED !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #B9B4AC !important;
        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #E8CBB0 !important;
    }

    div[data-baseweb="tab-highlight"] {
        background: #D8A6B5 !important;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: #151515;
        border: 1px solid #303030;
        border-radius: 12px;
        padding: 16px;
    }

    div[data-testid="stMetricLabel"] {
        color: #AAA49C !important;
    }

    div[data-testid="stMetricValue"] {
        color: #F5F2ED !important;
    }

    /* Tables */
    div[data-testid="stDataFrame"] {
        border: 1px solid #303030;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Info / success / warning boxes */
    div[data-testid="stAlert"] {
        background: #151515 !important;
        border: 1px solid #393939 !important;
    }

    /* Sidebar project-size card */
    .project-card {
        background: #343434;
        border: 1px solid #444444;
        border-radius: 10px;
        padding: 14px 16px;
        color: #E8CBB0 !important;
        margin-top: 8px;
    }

    .project-card strong {
        color: #F5F2ED !important;
    }

    /* Divider */
    hr {
        border-color: #303030 !important;
    }

    /* Buttons */
    button[kind="secondary"] {
        background: #161616 !important;
        color: #F5F2ED !important;
        border-color: #454545 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# COCOMO DATA
# ============================================================
BASIC = {
    "Organic": (2.4, 1.05, 2.5, 0.38),
    "Semi-Detached": (3.0, 1.12, 2.5, 0.35),
    "Embedded": (3.6, 1.20, 2.5, 0.32),
}

INTERMEDIATE = BASIC.copy()

PHASE_DISTRIBUTION = {
    "Organic": {
        "Requirements & Planning": 0.06,
        "Product Design": 0.16,
        "Detailed Design": 0.24,
        "Coding & Unit Testing": 0.26,
        "Integration & Testing": 0.28,
    },
    "Semi-Detached": {
        "Requirements & Planning": 0.07,
        "Product Design": 0.17,
        "Detailed Design": 0.25,
        "Coding & Unit Testing": 0.26,
        "Integration & Testing": 0.25,
    },
    "Embedded": {
        "Requirements & Planning": 0.08,
        "Product Design": 0.18,
        "Detailed Design": 0.25,
        "Coding & Unit Testing": 0.24,
        "Integration & Testing": 0.25,
    },
}


def cocomo_estimate(kloc, mode, eaf=1.0):
    a, b, c, d = BASIC[mode]
    basic_effort = a * (kloc ** b)
    effort = basic_effort * eaf
    schedule = c * (effort ** d)
    staffing = effort / schedule if schedule else 0

    return {
        "Mode": mode,
        "Effort (Person-Months)": effort,
        "Development Time (Months)": schedule,
        "Average Staff": staffing,
    }


def detailed_phases(total_effort, mode):
    rows = []
    for phase, percentage in PHASE_DISTRIBUTION[mode].items():
        rows.append({
            "Phase": phase,
            "Percentage": percentage * 100,
            "Effort (Person-Months)": total_effort * percentage,
        })
    return pd.DataFrame(rows)


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## Project Input")
    st.markdown('<p class="subtle">Enter the estimated software size and adjustment factor.</p>',
                unsafe_allow_html=True)

    # IMPORTANT: LoC is the default because the assignment specifies LoC input.
    size_value = st.number_input(
        "Lines of Code (LoC)",
        min_value=1,
        value=10000,
        step=1000,
        help="Enter the estimated source lines of code.",
    )

    size_unit = st.radio(
        "Input unit",
        ["LoC", "KLoC"],
        index=0,
    )

    eaf = st.number_input(
        "EAF for Intermediate/Detailed COCOMO",
        min_value=0.01,
        value=1.00,
        step=0.01,
        help="Use 1.00 when no cost-driver adjustment is provided.",
    )

    kloc = size_value / 1000 if size_unit == "LoC" else size_value

    st.markdown(
        f'<div class="project-card">Project size: <strong>{kloc:,.3f} KLoC</strong></div>',
        unsafe_allow_html=True,
    )

# ============================================================
# HEADER
# ============================================================
st.markdown("# 📊 COCOMO Estimation Tool")
st.markdown(
    '<p class="subtle">Software Project Cost, Effort and Schedule Estimator</p>',
    unsafe_allow_html=True,
)
st.markdown(
    "This tool estimates software development effort, development time and "
    "average staffing using the three classical COCOMO approaches: "
    "**Basic, Intermediate and Detailed COCOMO.**"
)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Basic COCOMO",
    "⚙️ Intermediate COCOMO",
    "🔬 Detailed COCOMO",
    "📈 Comparison",
])

# ---------------- BASIC ----------------
with tab1:
    st.subheader("Basic COCOMO")

    st.latex(r"Effort = a(KLOC)^b")
    st.latex(r"Development\ Time = c(Effort)^d")
    st.latex(r"Average\ Staff = \frac{Effort}{Development\ Time}")

    rows = []
    for mode in BASIC:
        r = cocomo_estimate(kloc, mode)
        rows.append({
            "Project Mode": mode,
            "Effort (Person-Months)": round(r["Effort (Person-Months)"], 2),
            "Development Time (Months)": round(r["Development Time (Months)"], 2),
            "Average Staff": round(r["Average Staff"], 2),
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.info("Basic COCOMO uses the nominal project environment without an EAF adjustment.")

# ---------------- INTERMEDIATE ----------------
with tab2:
    st.subheader("Intermediate COCOMO")

    st.latex(r"Effort = a(KLOC)^b \times EAF")
    st.latex(r"Development\ Time = c(Effort)^d")

    st.markdown(f"Current EAF: **{eaf:.2f}**")

    rows = []
    for mode in INTERMEDIATE:
        r = cocomo_estimate(kloc, mode, eaf)
        rows.append({
            "Project Mode": mode,
            "Effort (Person-Months)": round(r["Effort (Person-Months)"], 2),
            "Development Time (Months)": round(r["Development Time (Months)"], 2),
            "Average Staff": round(r["Average Staff"], 2),
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.info(
        "For a full Intermediate COCOMO study, EAF is obtained from cost-driver "
        "ratings. This calculator accepts the resulting EAF directly."
    )

# ---------------- DETAILED ----------------
with tab3:
    st.subheader("Detailed COCOMO")

    detailed_mode = st.selectbox("Select project mode", list(BASIC))
    r = cocomo_estimate(kloc, detailed_mode, eaf)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Effort", f"{r['Effort (Person-Months)']:.2f} PM")
    c2.metric("Development Time", f"{r['Development Time (Months)']:.2f} months")
    c3.metric("Average Staff", f"{r['Average Staff']:.2f} persons")

    phase_df = detailed_phases(r["Effort (Person-Months)"], detailed_mode)

    st.subheader("Phase-wise Effort Distribution")
    st.dataframe(phase_df.round(2), use_container_width=True, hide_index=True)

    # User explicitly requested beige + pink aesthetics.
    phase_colors = ["#E8D6C0", "#D8A6B5", "#CBB79E", "#E6C8D2", "#BFAE9A"]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    fig.patch.set_facecolor("#050505")
    ax.set_facecolor("#050505")
    bars = ax.bar(
        phase_df["Phase"],
        phase_df["Effort (Person-Months)"],
        color=phase_colors,
        edgecolor="#F5F2ED",
        linewidth=0.4,
    )
    ax.set_ylabel("Effort (Person-Months)", color="#F5F2ED")
    ax.set_xlabel("Development Phase", color="#F5F2ED")
    ax.set_title(f"Detailed COCOMO — {detailed_mode} Mode", color="#F5F2ED")
    ax.tick_params(axis="x", rotation=25, colors="#CFC9C0")
    ax.tick_params(axis="y", colors="#CFC9C0")
    ax.spines["bottom"].set_color("#444444")
    ax.spines["left"].set_color("#444444")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#242424", linewidth=0.8)
    fig.tight_layout()
    st.pyplot(fig)

# ---------------- COMPARISON ----------------
with tab4:
    st.subheader("COCOMO Model Comparison")

    comparison_rows = []
    for mode in BASIC:
        b = cocomo_estimate(kloc, mode, 1.0)
        i = cocomo_estimate(kloc, mode, eaf)
        comparison_rows.append({
            "Mode": mode,
            "Basic Effort (PM)": round(b["Effort (Person-Months)"], 2),
            "Intermediate Effort (PM)": round(i["Effort (Person-Months)"], 2),
            "Basic Schedule (Months)": round(b["Development Time (Months)"], 2),
            "Intermediate Schedule (Months)": round(i["Development Time (Months)"], 2),
        })

    comparison_df = pd.DataFrame(comparison_rows)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    st.subheader("Effort Comparison")

    fig, ax = plt.subplots(figsize=(9, 4.7))
    fig.patch.set_facecolor("#050505")
    ax.set_facecolor("#050505")

    x = range(len(comparison_df))
    width = 0.34

    ax.bar(
        [i - width / 2 for i in x],
        comparison_df["Basic Effort (PM)"],
        width,
        label="Basic",
        color="#E8D6C0",       # warm beige
        edgecolor="#F5F2ED",
        linewidth=0.5,
    )
    ax.bar(
        [i + width / 2 for i in x],
        comparison_df["Intermediate Effort (PM)"],
        width,
        label="Intermediate",
        color="#D8A6B5",       # muted pink
        edgecolor="#F5F2ED",
        linewidth=0.5,
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(comparison_df["Mode"], color="#CFC9C0")
    ax.set_ylabel("Effort (Person-Months)", color="#F5F2ED")
    ax.set_title("Basic vs Intermediate COCOMO", color="#F5F2ED", pad=12)
    ax.tick_params(axis="y", colors="#CFC9C0")
    ax.spines["bottom"].set_color("#444444")
    ax.spines["left"].set_color("#444444")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#242424", linewidth=0.8)
    ax.legend(
        facecolor="#151515",
        edgecolor="#444444",
        labelcolor="#F5F2ED",
    )
    fig.tight_layout()
    st.pyplot(fig)

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    '<p class="subtle">Educational implementation of the classical COCOMO estimation equations. '
    'Use the coefficients and assumptions specified by your course material if they differ.</p>',
    unsafe_allow_html=True,
)
