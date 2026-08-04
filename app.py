"""
Mumbai Climate Disclosure Dashboard (2021-2025)
Native Streamlit build — layout and content use Streamlit widgets
(columns, metrics, buttons, dataframes, plotly charts) rather than
raw HTML blocks. A small CSS snippet is injected only to set colors
(sidebar background, button styling) — not to build structure.

Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Mumbai Climate Disclosure Dashboard · 2021-2025",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="auto",
)

# ---------------------------------------------------------------
# COLOR PALETTE
# ---------------------------------------------------------------
INK = "#12233B"
MONSOON = "#1F6F78"
AMBER = "#D69A2D"
RED = "#B5423A"
PAPER = "#F6F3EC"
MUTED = "#5B6B76"

# ---------------------------------------------------------------
# THEME (colors only — no structural HTML)
# ---------------------------------------------------------------
st.markdown(f"""
<style>
    .stApp {{ background-color: {PAPER}; }}
    section[data-testid="stSidebar"] {{ background-color: {INK}; }}
    section[data-testid="stSidebar"] * {{ color: #E8ECEA !important; }}

    /* Sidebar nav buttons: force transparent background + visible light text */
    section[data-testid="stSidebar"] button {{
        background-color: transparent !important;
        background: transparent !important;
        color: #4A6572 !important;
        border: none !important;
        text-align: left !important;
        box-shadow: none !important;
        justify-content: flex-start !important;
    }}
    section[data-testid="stSidebar"] button * {{
        color: inherit !important;
    }}
    section[data-testid="stSidebar"] button:hover {{
        background-color: rgba(255,255,255,0.10) !important;
        color: #ffffff !important;
    }}

    [data-testid="stMetricValue"] {{ color: {INK}; }}
    div.stButton > button {{ border-radius: 8px; }}
    div.stButton > button[kind="primary"] {{ background-color: {RED}; border: none; color: #fff !important; }}

    /* Let table cells wrap instead of getting cut off */
    [data-testid="stTable"] td, [data-testid="stTable"] th {{
        white-space: normal !important;
        vertical-align: top !important;
        text-align: left !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# SESSION STATE — controls which "page" is showing
# ---------------------------------------------------------------
if "view" not in st.session_state:
    st.session_state.view = "cover"

def go_to(view_id):
    st.session_state.view = view_id

# ---------------------------------------------------------------
# TAB / NAV CONFIG
# ---------------------------------------------------------------
TABS = [
    {"id": "overview", "cat": None,               "label": "Overview"},
    {"id": "q1",  "cat": "Trend & progress", "label": "🌊 1 · Hazard trend"},
    {"id": "q2",  "cat": "Trend & progress", "label": "🎯 2 · Climate targets"},
    {"id": "q3",  "cat": "Trend & progress", "label": "✅ 3 · Completeness"},
    {"id": "q4",  "cat": "Trend & progress", "label": "🔢 4 · Quantitative shift"},
    {"id": "q5",  "cat": "Data quality",     "label": "📋 5 · Copy-paste answers"},
    {"id": "q6",  "cat": "Data quality",     "label": "🏙️ 6 · Basic facts"},
    {"id": "q7",  "cat": "Data quality",     "label": "⬜ 7 · Consistently blank"},
    {"id": "q8",  "cat": "Governance",       "label": "🏛️ 8 · Institutional shift"},
    {"id": "q9",  "cat": "Governance",       "label": "🤝 9 · Other govt levels"},
    {"id": "q10", "cat": "Financial",        "label": "💰 10 · Financing strategy"},
    {"id": "q11", "cat": "Financial",        "label": "📉 11 · Financial impact"},
]

# ---------------------------------------------------------------
# SMALL HELPERS
# ---------------------------------------------------------------
def verdict(text):
    """Renders the dark 'short answer' callout using a native container + colored border."""
    box = st.container(border=True)
    box.markdown(f":orange[**SHORT ANSWER**]")
    box.write(text)

def table(rows, columns):
    df = pd.DataFrame(rows, columns=columns)
    df.index = [""] * len(df)   # blank out the index column
    st.table(df)

def bar(df, x, y, color=None, colors=None, horizontal=False, height=320, stacked=False):
    if horizontal:
        fig = px.bar(df, x=y, y=x, color=color, orientation="h",
                     color_discrete_sequence=colors or [MONSOON])
    else:
        fig = px.bar(df, x=x, y=y, color=color, color_discrete_sequence=colors or [MONSOON],
                     barmode="stack" if stacked else "group")
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=10, b=10),
                       plot_bgcolor="white", paper_bgcolor="white",
                       font=dict(size=12, color=MUTED),
                       legend=dict(orientation="h", y=-0.25))
    fig.update_xaxes(gridcolor="#EAE5D8")
    fig.update_yaxes(gridcolor="#EAE5D8")
    st.plotly_chart(fig, use_container_width=True)

def line(df, x, y, height=320):
    fig = px.line(df, x=x, y=y, markers=True)
    fig.update_traces(line_color=MONSOON, fill="tozeroy", fillcolor="rgba(31,111,120,0.12)")
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=10, b=10),
                       plot_bgcolor="white", paper_bgcolor="white",
                       font=dict(size=12, color=MUTED), showlegend=False)
    fig.update_xaxes(gridcolor="#EAE5D8")
    fig.update_yaxes(gridcolor="#EAE5D8")
    st.plotly_chart(fig, use_container_width=True)

DATA = {
    "years": [
        2021,
        2022,
        2023,
        2024,
        2025
    ],
    "completeness": [
        {
            "year": 2021,
            "total": 53,
            "na": 52,
            "answered": 1,
            "pct": 1.9
        },
        {
            "year": 2022,
            "total": 75,
            "na": 5,
            "answered": 70,
            "pct": 93.3
        },
        {
            "year": 2023,
            "total": 79,
            "na": 5,
            "answered": 74,
            "pct": 93.7
        },
        {
            "year": 2024,
            "total": 190,
            "na": 0,
            "answered": 190,
            "pct": 100.0
        },
        {
            "year": 2025,
            "total": 179,
            "na": 0,
            "answered": 179,
            "pct": 100.0
        }
    ],
    "quant": [
        {
            "year": 2021,
            "answered": 1,
            "quant": 0,
            "pct": 0.0
        },
        {
            "year": 2022,
            "answered": 70,
            "quant": 17,
            "pct": 24.3
        },
        {
            "year": 2023,
            "answered": 74,
            "quant": 20,
            "pct": 27.0
        },
        {
            "year": 2024,
            "answered": 190,
            "quant": 63,
            "pct": 33.2
        },
        {
            "year": 2025,
            "answered": 179,
            "quant": 55,
            "pct": 30.7
        }
    ],
    "hazards_by_year": {
        "2021": [],
        "2022": [
            {
                "hazard": "Urban flooding",
                "pop_exposed": "30-40%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Increasing"
            },
            {
                "hazard": "Extreme heat",
                "pop_exposed": "20-30%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Increasing"
            }
        ],
        "2023": [
            {
                "hazard": "Urban flooding",
                "pop_exposed": "30-40%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Increasing"
            },
            {
                "hazard": "Extreme heat",
                "pop_exposed": "20-30%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Increasing"
            }
        ],
        "2024": [
            {
                "hazard": "Urban flooding",
                "pop_exposed": "31-40%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Increasing"
            },
            {
                "hazard": "Extreme heat",
                "pop_exposed": "21-30%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Increasing"
            },
            {
                "hazard": "Other: Air quality",
                "pop_exposed": "n/a",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Decreasing"
            }
        ],
        "2025": [
            {
                "hazard": "Urban flooding",
                "pop_exposed": "31-40%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Increasing"
            },
            {
                "hazard": "Extreme heat",
                "pop_exposed": "21-30%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Increasing"
            },
            {
                "hazard": "Other: Air Pollution",
                "pop_exposed": "31-40%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Decreasing"
            },
            {
                "hazard": "Coastal flooding (incl. sea level rise)",
                "pop_exposed": "31-40%",
                "probability": "Medium High",
                "magnitude": "Medium High",
                "future_intensity": "Increasing",
                "future_frequency": "Do not know"
            }
        ]
    },
    "mitigation_action_counts": [
        {
            "year": 2022,
            "count": 2
        },
        {
            "year": 2023,
            "count": 2
        },
        {
            "year": 2024,
            "count": 10
        },
        {
            "year": 2025,
            "count": 6
        }
    ],
    "copy_paste": [
        {
            "question": "Risks related to transition to a low-carbon economy",
            "years": "2022, 2023, 2024, 2025",
            "text": "A low-carbon economy essentially requires lowering of consumption at many levels. Reducing consumption may lead to the loss of jobs in the informal sector in the city."
        },
        {
            "question": "Current magnitude of impact of hazard (both Urban flooding & Extreme heat)",
            "years": "2022, 2023, 2024, 2025",
            "text": "Medium High"
        },
        {
            "question": "Current probability of hazard (both Urban flooding & Extreme heat)",
            "years": "2022, 2023, 2024, 2025",
            "text": "Medium High"
        },
        {
            "question": "Boundary of risk/vulnerability assessment relative to jurisdiction boundary",
            "years": "2022, 2023, 2024, 2025",
            "text": "Same - covers entire jurisdiction and nothing else"
        },
        {
            "question": "End year of climate action plan",
            "years": "2022, 2023, 2024",
            "text": "2050"
        },
        {
            "question": "Year of formal approval of climate action plan",
            "years": "2022, 2023, 2024",
            "text": "2022"
        },
        {
            "question": "Description of hazard impacts – Extreme heat narrative",
            "years": "2022, 2023, 2024, 2025",
            "text": "Increase in frequency of warmer years observed, with three out of the last five years showing a departure of more than 1°C from the baseline average air temperature (1973-2020)... (full ~200-word paragraph repeated verbatim each year)"
        },
        {
            "question": "Description of hazard impacts – Urban flooding narrative",
            "years": "2022, 2023, 2024, 2025",
            "text": "Around 35% of Mumbai’s population lives within 250 m of flood hotspots... (full ~250-word paragraph repeated verbatim each year, citing a 2013 study and 2015 Directory of Establishments data without ever updating the source year)"
        },
        {
            "question": "Jurisdiction / low-carbon-economy background narrative (city profile paragraph)",
            "years": "2022, 2023, 2024, 2025",
            "text": "Mumbai is the most populous city in India and, globally, the 7th largest in terms of population... (full city-profile paragraph repeated verbatim every year, still citing 2011 Census and a 2010 informal-sector study)"
        }
    ],
    "blank_sections": [
        {
            "code": "1.5",
            "topic": "Transparency of the planning process (civil society engagement, prioritization criteria, reporting commitments)"
        },
        {
            "code": "2.0a",
            "topic": "Methodology used for risk & vulnerability assessment"
        },
        {
            "code": "2.0b",
            "topic": "Attachment / details of the risk & vulnerability assessment document (9 sub-fields: title, link, year, boundary, author, etc.)"
        },
        {
            "code": "2.0c",
            "topic": "Explanation for why no risk & vulnerability assessment exists"
        },
        {
            "code": "2.0d",
            "topic": "Update/revision process for a risk assessment older than 4 years"
        },
        {
            "code": "2.1b",
            "topic": "Climate exposure scenarios for high-risk hazards"
        },
        {
            "code": "2.1c",
            "topic": "Baseline synthesis report on risk, vulnerability and adaptive capacity"
        },
        {
            "code": "2.3a",
            "topic": "Health-specific risk and vulnerability assessment"
        },
        {
            "code": "3.2a",
            "topic": "Synergies/trade-offs/co-benefits assessment of adaptation actions (one sub-field)"
        },
        {
            "code": "5.5a / 5.5b",
            "topic": "Attachment and boundary details of a stand-alone mitigation/energy-access plan document"
        },
        {
            "code": "6.12",
            "topic": "How the city plans to enhance ambition / scale up the Climate Action Plan"
        }
    ],
    "financing": [
        {
            "year": 2022,
            "figures": [
                "Rs 1.5 billion earmarked in the 2022-23 BMC budget specifically to reduce flooding",
                "Rs 13.91 billion spent historically by BMC to tackle flooding",
                "Rs 140 billion in estimated flood losses, 2005-2015 (USTDA/KPMG study)"
            ],
            "mechanism": "Jurisdiction's own resources; Public-private partnerships"
        },
        {
            "year": 2023,
            "figures": [
                "₹2,570.65 crore (~Rs 25.7 billion) proposed in the 2023-24 budget estimate for stormwater drainage capital works",
                "Repeats the Rs 1.5bn and Rs 13.91bn figures from 2022 verbatim",
                "Repeats the Rs 140 billion 2005-2015 loss estimate verbatim"
            ],
            "mechanism": "Jurisdiction's own resources; Public-private partnerships"
        },
        {
            "year": 2024,
            "figures": [
                "No rupee figures given at all — replaced by a qualitative description of ‘climate budgeting’ as a governance process",
                "Individual mitigation actions do carry numeric emission-reduction outcomes (e.g. 1244, 798, 36.1, 12.8, 1037, 5,163,480 — units not stated in the extract)"
            ],
            "mechanism": "National funds and programmes; Public-private partnerships; Jurisdiction's own resources"
        },
        {
            "year": 2025,
            "figures": [
                "Same qualitative ‘climate budgeting’ description as 2024, no rupee figures",
                "Same per-action emission-reduction numbers as 2024, largely unchanged",
                "One new field: a planned project pipeline for external financing (Q9.3) appears for the first time, listing projects seeking investment"
            ],
            "mechanism": "Jurisdiction's own resources; Public-private partnerships; National funds and programmes"
        }
    ],
    "governance": [
        {
            "year": 2022,
            "detail": "Oversight described only generically: ‘relevant departments, committees and/or subcommittees’ inform council/management on climate issues. No department or role is named."
        },
        {
            "year": 2023,
            "detail": "Same generic oversight description as 2022, expanded slightly to list more named stakeholder categories consulted on the plan (state government, NGOs, business, citizens)."
        },
        {
            "year": 2024,
            "detail": "First year a specific institutional home is named: the Brihanmumbai Municipal Corporation (BMC) Environment and Climate Change Department is identified as the nodal department for the Mumbai Climate Action Plan, Majhi Vasundhara Abhiyan and the National Clean Air Programme. Named roles: Addl. Municipal Commissioner (City), Deputy Municipal Commissioner (Env & CC), Chief Engineer, Deputy Engineers, Municipal Architects. 20 departments are listed as climate-relevant (Disaster Management, Mechanical & Engineering, Gardens, Storm Water Drains, etc). A new field also appears: implementation status of the plan (‘Underway – moderate progress made’)."
        },
        {
            "year": 2025,
            "detail": "Repeats the 2024 department/role description essentially verbatim. Plan preparation credits expand to include a Dedicated team within jurisdiction and an International organization, alongside the Regional/state government and Consultant already credited in 2024."
        }
    ],
    "plan_targets": [
        {
            "year": 2022,
            "approval_year": "2022",
            "end_year": "2050",
            "monitoring": "Evaluation annually; progress publicly reported annually; updates published annually",
            "status_field": "not collected this year"
        },
        {
            "year": 2023,
            "approval_year": "2022",
            "end_year": "2050",
            "monitoring": "Evaluation annually; progress publicly reported annually; updates published annually",
            "status_field": "not collected this year"
        },
        {
            "year": 2024,
            "approval_year": "2022",
            "end_year": "2050",
            "monitoring": "Evaluation every 3-5 years; updates published every 5+ years — a much less frequent cadence than the ‘annually’ stated in 2022-2023",
            "status_field": "Underway – moderate progress made"
        },
        {
            "year": 2025,
            "approval_year": "2022",
            "end_year": "2050",
            "monitoring": "Same reduced cadence as 2024 (evaluation every 3-5 years, updates every 5+ years)",
            "status_field": "Underway – moderate progress made"
        }
    ],
    "govt_engagement_stakeholders": [
        {
            "year": 2022,
            "list": "Business and private sector; Citizens; Local government(s)/agencies; NGOs; State/regional government(s)/agencies"
        },
        {
            "year": 2023,
            "list": "State/regional government(s)/agencies; Business and private sector; Local government(s)/agencies; Citizens; NGOs"
        },
        {
            "year": 2024,
            "list": "NGOs; Citizens; Academia; Business and private sector; State/regional government(s)/agencies; Local government(s)/agencies"
        },
        {
            "year": 2025,
            "list": "NGOs; Academia; Citizens; Business and private sector; State/regional government(s)/agencies; Local government(s)/agencies; (plan preparation also now credits a Dedicated team within jurisdiction, a Consultant, and an International organization)"
        }
    ],
    "monitoring_cadence": [
        {
            "year": 2022,
            "years_between_review": 1,
            "label": "Annual"
        },
        {
            "year": 2023,
            "years_between_review": 1,
            "label": "Annual"
        },
        {
            "year": 2024,
            "years_between_review": 4,
            "label": "Every 3–5 yrs"
        },
        {
            "year": 2025,
            "years_between_review": 4,
            "label": "Every 3–5 yrs"
        }
    ],
    "population_density_comparison": [
        {
            "category": "Mumbai City & Suburban districts",
            "value": 20000
        },
        {
            "category": "Maharashtra state average",
            "value": 365
        },
        {
            "category": "National (India) average",
            "value": 382
        }
    ],
    "blank_subfield_counts": [
        {
            "code": "1.5",
            "count": 3
        },
        {
            "code": "2.0a",
            "count": 2
        },
        {
            "code": "2.0b",
            "count": 9
        },
        {
            "code": "2.0c",
            "count": 2
        },
        {
            "code": "2.0d",
            "count": 2
        },
        {
            "code": "2.1b",
            "count": 2
        },
        {
            "code": "2.1c",
            "count": 2
        },
        {
            "code": "2.3a",
            "count": 2
        },
        {
            "code": "3.2a",
            "count": 2
        },
        {
            "code": "5.5a/5.5b",
            "count": 16
        },
        {
            "code": "6.12",
            "count": 1
        }
    ],
    "governance_specificity": [
        {
            "year": 2022,
            "named_roles": 0,
            "named_departments": 0
        },
        {
            "year": 2023,
            "named_roles": 0,
            "named_departments": 0
        },
        {
            "year": 2024,
            "named_roles": 5,
            "named_departments": 20
        },
        {
            "year": 2025,
            "named_roles": 5,
            "named_departments": 20
        }
    ],
    "stakeholder_counts": [
        {
            "year": 2022,
            "count": 5
        },
        {
            "year": 2023,
            "count": 5
        },
        {
            "year": 2024,
            "count": 6
        },
        {
            "year": 2025,
            "count": 6
        }
    ],
    "financing_mechanism_counts": [
        {
            "year": 2022,
            "count": 2
        },
        {
            "year": 2023,
            "count": 2
        },
        {
            "year": 2024,
            "count": 3
        },
        {
            "year": 2025,
            "count": 3
        }
    ],
    "rupee_figure_counts": [
        {
            "year": 2022,
            "count": 3
        },
        {
            "year": 2023,
            "count": 4
        },
        {
            "year": 2024,
            "count": 0
        },
        {
            "year": 2025,
            "count": 0
        }
    ],
    "copy_paste_span": [
        {
            "question": "Risks related to transition to a low-carbon economy",
            "years": 4
        },
        {
            "question": "Current magnitude of impact of hazard",
            "years": 4
        },
        {
            "question": "Current probability of hazard",
            "years": 4
        },
        {
            "question": "Boundary of risk/vulnerability assessment",
            "years": 4
        },
        {
            "question": "End year of climate action plan (2050)",
            "years": 3
        },
        {
            "question": "Year of formal approval of plan (2022)",
            "years": 3
        },
        {
            "question": "Extreme heat impact narrative",
            "years": 4
        },
        {
            "question": "Urban flooding impact narrative",
            "years": 4
        },
        {
            "question": "Jurisdiction background paragraph",
            "years": 4
        }
    ]
}

# ---------------------------------------------------------------
# COVER PAGE — built entirely from native Streamlit widgets
# ---------------------------------------------------------------
def render_cover():
    st.caption("BMC · CDP-ICLEI TRACK CLIMATE DISCLOSURES")
    st.title("Reading Mumbai's climate disclosures across five reporting years")
    st.write(
        "An evidence-based dashboard built directly from the city's own 2021-2025 "
        "hazard, risk and mitigation submissions — answering 11 questions about "
        "trends, data quality and institutional change with the actual "
        "question/answer pairs behind each finding."
    )

    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reporting years", "5")
    c2.metric("Question/answer pairs", "576")
    c3.metric("Completeness, 2021→2024", "1.9% → 100%")
    c4.metric("Verbatim repeated answers found", "9")

    st.write("")
    if st.button("Enter dashboard →", type="primary"):
        go_to("overview")
        st.rerun()

    st.caption(
        "Source: Mumbai_Hazard_Risk_Mitigation_2019_2025.xlsx — "
        "576 question/answer rows across 2021–2025."
    )

# ---------------------------------------------------------------
# SIDEBAR NAVIGATION — native grouped buttons
# ---------------------------------------------------------------
def render_sidebar():
    with st.sidebar:
        st.markdown("**Mumbai Climate Disclosures**")
        st.caption("2021–2025 · BMC submissions")
        if st.button("← Back to cover"):
            go_to("cover")
            st.rerun()
        st.divider()

        last_cat = None
        for t in TABS:
            if t["cat"] and t["cat"] != last_cat:
                st.markdown(f"<small style='color:#7C9793; text-transform:uppercase; "
                            f"letter-spacing:.08em;'>{t['cat']}</small>", unsafe_allow_html=True)
                last_cat = t["cat"]
            is_active = st.session_state.view == t["id"]
            label = f"➜ {t['label']}" if is_active else t["label"]
            if st.button(label, key=f"nav_{t['id']}", use_container_width=True):
                go_to(t["id"])
                st.rerun()

# ---------------------------------------------------------------
# PAGE: OVERVIEW
# ---------------------------------------------------------------
def render_overview():
    st.subheader("Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Years covered", "2021–2025")
    c2.metric("Question/answer rows", "576")
    c3.metric("Distinct question codes", "117")
    c4.metric("Sections never once answered", "11")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Answer completeness by year**")
        df = pd.DataFrame(DATA["completeness"])
        df_long = df.melt(id_vars="year", value_vars=["answered", "na"],
                           var_name="type", value_name="count")
        df_long["type"] = df_long["type"].map({"answered": "Answered", "na": "N/A or blank"})
        bar(df_long, "year", "count", color="type", colors=[MONSOON, "#DBD5C6"], stacked=True)
    with col2:
        st.markdown("**Share of answers containing a number**")
        line(pd.DataFrame(DATA["quant"]), "year", "pct")

    st.markdown("**Year-by-year summary**")
    rows = []
    for c, q in zip(DATA["completeness"], DATA["quant"]):
        hz = len(DATA["hazards_by_year"].get(str(c["year"]), []))
        mit = next((m["count"] for m in DATA["mitigation_action_counts"] if m["year"] == c["year"]), "—")
        rows.append([c["year"], c["total"], f'{c["pct"]}%', f'{q["pct"]}%', hz, mit])
    table(rows, ["Year", "Total rows", "% answered", "% quantitative", "Hazards named", "Mitigation actions"])

    st.markdown("**What changed most, at a glance**")
    st.markdown("""
- **2021 was effectively a blank submission** — 52 of 53 rows are "Not Applicable."
- **Hazard list grew from 2 to 4** named hazards (2022→2025), but severity ratings stayed "Medium High" every year.
- **A named nodal department appears for the first time in 2024** (BMC's Environment & Climate Change Department).
- **Specific rupee figures disappeared after 2023**, replaced by qualitative "climate budgeting" text.
    """)

# ---------------------------------------------------------------
# PAGE: Q1 — Hazard trend
# ---------------------------------------------------------------
def render_q1():
    st.caption("Q1 · Trend & progress")
    st.subheader("Has the number and severity of reported hazards increased — real risk change, or reporting change?")
    verdict(
        "The count of named hazards climbed from 2 (2022–23) to 3 (2024) to 4 (2025). But severity "
        "ratings — probability, magnitude, future trend — stay frozen at 'Medium High / Increasing' "
        "for every hazard, every year, and the descriptive paragraphs are copied word-for-word. This "
        "looks like expanding disclosure scope, not freshly reassessed risk."
    )
    col1, col2 = st.columns([1, 1.3])
    with col1:
        st.markdown("**Number of hazards reported, by year**")
        counts = [(y, len(v)) for y, v in DATA["hazards_by_year"].items()]
        bar(pd.DataFrame(counts, columns=["year", "count"]), "year", "count", colors=[RED])
        st.caption("2021 reported none (section entirely 'Not Applicable').")
    with col2:
        st.markdown("**Hazard detail, year by year**")
        rows = []
        for yr, hlist in DATA["hazards_by_year"].items():
            if not hlist:
                rows.append([yr, "— none reported —", "", "", "", ""])
            for h in hlist:
                rows.append([yr, h["hazard"], h["pop_exposed"], h["probability"], h["magnitude"],
                             f'{h["future_intensity"]} intensity, {h["future_frequency"].lower()} frequency'])
        table(rows, ["Year", "Hazard", "Pop. exposed", "Probability", "Magnitude", "Future trend"])

    st.markdown("**Why this looks like a reporting artifact, not fresh risk analysis**")
    st.markdown("""
- Every hazard, every year: "Medium High" probability and magnitude — never upgraded or downgraded.
- The "Urban flooding" narrative paragraph is identical 2022–2025, still citing a 2013 study.
- Question coding changed from "1.2 C1…C11" (2021-23) to "Q2.2 … [Row N]" (2024-25) — a questionnaire redesign.
    """)

# ---------------------------------------------------------------
# PAGE: Q2 — Climate targets
# ---------------------------------------------------------------
def render_q2():
    st.caption("Q2 · Trend & progress")
    st.subheader("Have the city's stated climate targets been met, revised, delayed or dropped?")
    verdict(
        "The Climate Action Plan's headline numbers — approved 2022, running to 2050 — never changed. "
        "What did quietly shift: the promised monitoring cadence, from 'annual' (2022-23) to "
        "'every 3-5 years' (2024-25) — a real downgrade in disclosed accountability."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Climate Action Plan facts, by year**")
        table([[p["year"], p["approval_year"], p["end_year"], p["monitoring"]] for p in DATA["plan_targets"]],
              ["Year", "Approved", "End year", "Monitoring cadence stated"])
    with col2:
        st.markdown("**Stated review cadence (years between reviews)**")
        bar(pd.DataFrame(DATA["monitoring_cadence"]), "year", "years_between_review", colors=[RED])
        st.caption("2024-25's 'every 3-5 years' plotted at the 4-year midpoint for comparability.")

    st.markdown("**Net-zero framing first appears in 2024**")
    st.info(
        '"Mumbai has a Climate Action Plan aimed at achieving net-zero emissions by 2050." '
        "— stated verbatim in 2024 and 2025; absent from 2022-2023 narrative answers."
    )

# ---------------------------------------------------------------
# PAGE: Q3 — Completeness
# ---------------------------------------------------------------
def render_q3():
    st.caption("Q3 · Trend & progress")
    st.subheader('Is the response getting more complete — real data vs. "Not Applicable" or blank?')
    verdict(
        "Yes, dramatically. Completeness rose from 1.9% in 2021 to 93-94% in 2022-2023 to a full "
        "100% in 2024 and 2025. Note the total number of rows also grew (53 → 190), so later years "
        "answer far more questions, not just the same fixed set more thoroughly."
    )
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown('**Answered vs. "Not Applicable" / blank, by year**')
        df = pd.DataFrame(DATA["completeness"])
        df_long = df.melt(id_vars="year", value_vars=["answered", "na"], var_name="type", value_name="count")
        df_long["type"] = df_long["type"].map({"answered": "Answered", "na": "N/A or blank"})
        bar(df_long, "year", "count", color="type", colors=[MONSOON, "#DBD5C6"], stacked=True, height=360)
    with col2:
        st.markdown("**Raw counts**")
        table([[c["year"], c["total"], c["answered"], c["na"], f'{c["pct"]}%'] for c in DATA["completeness"]],
              ["Year", "Total rows", "Answered", "N/A / blank", "% complete"])
        st.caption("2021's single non-blank row is essentially a non-response year.")

# ---------------------------------------------------------------
# PAGE: Q4 — Quantitative shift
# ---------------------------------------------------------------
def render_q4():
    st.caption("Q4 · Trend & progress")
    st.subheader("Are answers becoming more quantitative, or staying narrative?")
    verdict(
        "Modestly and unevenly — 24% of answered rows had a number in 2022, rising to 33% in 2024, "
        "dipping to 31% in 2025. The clearest gain: mitigation-action reporting (2 actions with "
        "little detail → 6-10 actions with specific emission-reduction figures). The clearest loss: "
        "financial-impact reporting (see Q11), where rupee figures vanished after 2023."
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Share of answers containing a number**")
        line(pd.DataFrame(DATA["quant"]), "year", "pct")
    with col2:
        st.markdown("**Mitigation actions logged per year**")
        bar(pd.DataFrame(DATA["mitigation_action_counts"]), "year", "count", colors=[AMBER])

    st.markdown("**Underlying figures**")
    rows = []
    for q in DATA["quant"]:
        mit = next((m["count"] for m in DATA["mitigation_action_counts"] if m["year"] == q["year"]), "—")
        rows.append([q["year"], q["answered"], q["quant"], f'{q["pct"]}%', mit])
    table(rows, ["Year", "Answered rows", "Rows with a number", "% quantitative", "Mitigation actions logged"])

# ---------------------------------------------------------------
# PAGE: Q5 — Copy-paste answers
# ---------------------------------------------------------------
def render_q5():
    st.caption("Q5 · Data quality")
    st.subheader("Are any answers identical every year — a sign of copy-paste rather than fresh reporting?")
    verdict(
        "Yes — at least 9 distinct answers (several full paragraphs) recur word-for-word across "
        "3-4 consecutive years, most strikingly the hazard-description narratives and the "
        "jurisdiction background paragraph, none of which have been refreshed even as their "
        "cited sources (2013, 2015, 2011 Census) get older each time."
    )
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown("**Verbatim-repeated answers found in the data**")
        table([[c["question"], c["years"], c["text"]] for c in DATA["copy_paste"]],
              ["Question / field", "Years repeated", "Text (truncated)"])
    with col2:
        st.markdown("**Consecutive years each was repeated**")
        bar(pd.DataFrame(DATA["copy_paste_span"]), "question", "years", horizontal=True,
            colors=[MONSOON], height=380)

# ---------------------------------------------------------------
# PAGE: Q6 — Basic facts
# ---------------------------------------------------------------
def render_q6():
    st.caption("Q6 · Data quality")
    st.subheader("Do basic facts like population or jurisdiction area move plausibly, or suggest data-entry errors?")
    verdict(
        "This extract has no dedicated jurisdiction-basics section — population/area figures only "
        "appear embedded inside the repeated city-profile paragraph, so there's no year-on-year "
        "movement to check for plausibility; the figure was never independently re-entered."
    )
    col1, col2 = st.columns([1.1, 1])
    with col1:
        st.markdown("**What population/area figures actually appear**")
        st.markdown("""
- **2011 Census figure, unchanged 2022-2025:** density in Mumbai City & Suburban districts "exceeds 20,000 persons/km²," vs. national average 382/km² and state average 365/km².
- **SRA estimate, unchanged:** "around 55% of Mumbai's population lives in slums... about 65% employed in the informal sector" (2010 study).
- Both are pasted into the same paragraph every year rather than a live jurisdiction field.
        """)
    with col2:
        st.markdown("**Population density cited (persons/km²)**")
        bar(pd.DataFrame(DATA["population_density_comparison"]), "category", "value",
            horizontal=True, colors=[RED, AMBER, MONSOON], height=260)

# ---------------------------------------------------------------
# PAGE: Q7 — Consistently blank
# ---------------------------------------------------------------
def render_q7():
    st.caption("Q7 · Data quality")
    st.subheader("Which questions does the city leave blank every year — and why?")
    verdict(
        "11 question sections are marked 'Not Applicable' in every year they appear — none was ever "
        "answered with real data 2021-2025. Most cluster around formal risk-assessment documentation "
        "and stand-alone plan attachments — plausible if Mumbai folds this into its single, "
        "already-reported Climate Action Plan instead of producing separate documents."
    )
    col1, col2 = st.columns([1.1, 1])
    with col1:
        st.markdown("**Sections never once answered with real data**")
        table([[b["code"], b["topic"]] for b in DATA["blank_sections"]], ["Section code", "Topic asked about"])
    with col2:
        st.markdown("**Sub-fields left blank, by section**")
        bar(pd.DataFrame(DATA["blank_subfield_counts"]), "code", "count",
            horizontal=True, colors=[RED], height=360)

    st.caption(
        "Sections 5.5a/5.5b (attachment + boundary of a stand-alone mitigation plan) account for "
        "16 blank sub-fields alone — the largest share — consistent with Mumbai reporting one "
        "integrated plan rather than the separate document the questionnaire asks for."
    )

# ---------------------------------------------------------------
# PAGE: Q8 — Institutional shift
# ---------------------------------------------------------------
def render_q8():
    st.caption("Q8 · Governance")
    st.subheader("Has responsibility for climate reporting shifted departments or roles over time?")
    verdict(
        "The generic oversight description of 2022-2023 gives way in 2024 to a first-time naming "
        "of a specific institutional home: the BMC Environment and Climate Change Department, with "
        "named senior roles and 20 climate-relevant departments listed."
    )
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown("**How the city described its own governance, year by year**")
        table([[g["year"], g["detail"]] for g in DATA["governance"]], ["Year", "What the city disclosed"])
    with col2:
        st.markdown("**Named roles & departments disclosed**")
        df = pd.DataFrame(DATA["governance_specificity"])
        df_long = df.melt(id_vars="year", value_vars=["named_roles", "named_departments"],
                           var_name="type", value_name="count")
        df_long["type"] = df_long["type"].map({"named_roles": "Named roles", "named_departments": "Named departments"})
        bar(df_long, "year", "count", color="type", colors=[AMBER, MONSOON], stacked=True)

# ---------------------------------------------------------------
# PAGE: Q9 — Other govt levels
# ---------------------------------------------------------------
def render_q9():
    st.caption("Q9 · Governance")
    st.subheader("Has engagement with state/national government changed in nature or intensity?")
    verdict(
        "No dedicated intergovernmental-engagement question exists, but the stakeholder list for "
        "the Climate Action Plan widens over time — by 2025 it also credits an international "
        "organization and a dedicated in-house team. 'National funds and programmes' appears as a "
        "financing mechanism only from 2024 onward."
    )
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown("**Stakeholders credited in preparing the Climate Action Plan**")
        table([[g["year"], g["list"]] for g in DATA["govt_engagement_stakeholders"]], ["Year", "Stakeholders credited"])
    with col2:
        st.markdown("**Number of distinct stakeholder categories listed**")
        bar(pd.DataFrame(DATA["stakeholder_counts"]), "year", "count", colors=[MONSOON])

# ---------------------------------------------------------------
# PAGE: Q10 — Financing strategy
# ---------------------------------------------------------------
def render_q10():
    st.caption("Q10 · Financial")
    st.subheader("Has the city's climate financing strategy evolved?")
    verdict(
        "Financing mechanisms broadened — 'National funds and programmes' joins the mix from 2024 "
        "— and 2025 adds a first-time project financing pipeline. No mention anywhere of a formal "
        "credit rating process or an explicit 'decarbonizing investments' mechanism."
    )
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown("**Financing mechanisms and figures, by year**")
        rows = []
        for f in DATA["financing"]:
            rows.append([f["year"], f["mechanism"], "; ".join(f["figures"])])
        table(rows, ["Year", "Mechanism(s)", "Detail"])
    with col2:
        st.markdown("**Number of distinct financing mechanisms cited**")
        bar(pd.DataFrame(DATA["financing_mechanism_counts"]), "year", "count", colors=[AMBER])

# ---------------------------------------------------------------
# PAGE: Q11 — Financial impact
# ---------------------------------------------------------------
def render_q11():
    st.caption("Q11 · Financial")
    st.subheader("Do financial impact estimates grow, shrink, or stay static — and is any change explained?")
    verdict(
        "Financial figures became LESS specific over time — the opposite of the overall Q4 trend. "
        "2022 gave three concrete rupee figures; 2023 added a fourth. 2024 and 2025 then dropped "
        "every rupee figure, replaced by qualitative 'climate budgeting' text, with no explanation "
        "anywhere in the data for why the numbers disappeared."
    )
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown("**Financial-impact figures cited, by year**")
        rows = [[f["year"], "; ".join(f["figures"])] for f in DATA["financing"]]
        table(rows, ["Year", "Financial figures cited"])
    with col2:
        st.markdown("**Distinct rupee figures cited per year**")
        bar(pd.DataFrame(DATA["rupee_figure_counts"]), "year", "count", colors=[RED])

    st.caption(
        "This looks arbitrary rather than a deliberate methodology change: the 2024/2025 narrative "
        "doesn't say the old figures were withdrawn, superseded, or under review."
    )

# ---------------------------------------------------------------
# ROUTER — dispatches to the correct render function
# ---------------------------------------------------------------
PAGES = {
    "overview": render_overview,
    "q1": render_q1, "q2": render_q2, "q3": render_q3, "q4": render_q4,
    "q5": render_q5, "q6": render_q6, "q7": render_q7,
    "q8": render_q8, "q9": render_q9,
    "q10": render_q10, "q11": render_q11,
}

def main():
    if st.session_state.view == "cover":
        render_cover()
    else:
        render_sidebar()
        PAGES.get(st.session_state.view, render_overview)()
        st.divider()
        st.caption(
            "Source file: Mumbai_Hazard_Risk_Mitigation_2019_2025.xlsx (worksheet "
            "'Hazard Risk Mitigation', plus topic-filtered Risk/Mitigation/Hazard/Vulnerability "
            "tabs). Data covers 2021-2025 only — no 2019/2020 rows exist despite the filename."
        )

if __name__ == "__main__":
    main()

 
    