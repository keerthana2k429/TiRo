import streamlit as st
import requests
import base64
import json
from PIL import Image
import io

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TiRo",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #060d1a;
    color: #f1f5f9;
}
.stApp { background-color: #060d1a; }

/* Header */
.rw-header {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border-bottom: 1px solid #334155;
    padding: 18px 24px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 24px;
    border-radius: 0 0 16px 16px;
}
.rw-logo {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.rw-title { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; margin: 0; color: #f1f5f9; letter-spacing: -0.5px; }
.rw-sub { font-size: 11px; color: #64748b; letter-spacing: 2px; text-transform: uppercase; margin: 0; }

/* Cards */
.road-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
}
.road-card:hover { border-color: #f59e0b; }
.road-type-badge {
    font-size: 11px; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #f59e0b; margin-bottom: 4px;
}
.road-name { font-family: 'Syne', sans-serif; font-size: 18px; color: #f1f5f9; margin: 0; }
.road-meta { font-size: 13px; color: #64748b; margin-top: 2px; }

/* Status badges */
.badge-good { background: #22c55e22; color: #22c55e; border: 1px solid #22c55e55; border-radius: 20px; padding: 2px 12px; font-size: 12px; font-weight: 700; }
.badge-fair { background: #f59e0b22; color: #f59e0b; border: 1px solid #f59e0b55; border-radius: 20px; padding: 2px 12px; font-size: 12px; font-weight: 700; }
.badge-poor { background: #ef444422; color: #ef4444; border: 1px solid #ef444455; border-radius: 20px; padding: 2px 12px; font-size: 12px; font-weight: 700; }

/* Info boxes */
.info-box {
    background: #0f172a; border-radius: 10px; padding: 12px 16px;
    border: 1px solid #1e293b; margin-bottom: 8px;
}
.info-label { font-size: 11px; color: #64748b; margin-bottom: 3px; }
.info-value { font-size: 14px; color: #cbd5e1; font-weight: 600; }

/* AI result box */
.ai-box {
    background: #0a1628; border: 1px solid #1e3a5f;
    border-radius: 12px; padding: 16px; margin-top: 12px;
}
.ai-label { font-size: 11px; color: #3b82f6; font-weight: 700; letter-spacing: 2px; margin-bottom: 10px; }

/* Chat bubbles */
.chat-user {
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: #000; font-weight: 600;
    border-radius: 18px 18px 4px 18px;
    padding: 12px 16px; margin: 8px 0;
    margin-left: 20%; font-size: 14px; line-height: 1.6;
}
.chat-ai {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155; color: #cbd5e1;
    border-radius: 18px 18px 18px 4px;
    padding: 12px 16px; margin: 8px 0;
    margin-right: 20%; font-size: 14px; line-height: 1.6;
}

/* Budget bar */
.budget-bar-bg { background: #1e293b; border-radius: 8px; height: 10px; overflow: hidden; }
.budget-bar-fill { height: 100%; border-radius: 8px; background: linear-gradient(90deg, #3b82f6, #22c55e); }
.source-note { font-size: 11px; color: #64748b; margin-top: 6px; }

/* Complaint success */
.success-box {
    background: #0a1a0a; border: 1px solid #22c55e44;
    border-radius: 16px; padding: 24px; text-align: center;
}

/* Tabs override */
.stTabs [data-baseweb="tab-list"] {
    background: #0f172a; border-radius: 12px; padding: 4px;
    border: 1px solid #1e293b; gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 9px;
    color: #64748b; font-weight: 500; font-family: 'DM Sans', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #f59e0b22, #ef444422) !important;
    color: #f59e0b !important; font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: #0f172a !important; border: 1px solid #334155 !important;
    color: #f1f5f9 !important; border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #f59e0b, #ef4444) !important;
    color: #000 !important; font-weight: 800 !important;
    border: none !important; border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important; letter-spacing: 0.5px !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.9 !important; }

div[data-testid="stFileUploader"] {
    background: #060d1a; border: 2px dashed #334155;
    border-radius: 12px; padding: 8px;
}
</style>
""", unsafe_allow_html=True)

# ─── Data ─────────────────────────────────────────────────────────────────────
ROADS_DB = {
    "NH-48": {
        "name": "NH-48 (Delhi–Mumbai Expressway)",
        "type": "NH", "typeLabel": "National Highway",
        "contractor": "L&T Construction Ltd.",
        "lastRelayed": "March 2024",
        "engineer": "Executive Engineer, NHAI Delhi Zone",
        "engineerEmail": "ee.nhai.delhi@gov.in",
        "authority": "NHAI",
        "budget": {"sanctioned": 4200, "spent": 3870, "currency": "Cr",
                   "source": "Ministry of Road Transport & Highways, Annual Report 2024"},
        "status": "Good", "length": "1,350 km", "country": "India",
    },
    "NH-44": {
        "name": "NH-44 (Srinagar–Kanyakumari)",
        "type": "NH", "typeLabel": "National Highway",
        "contractor": "Gawar Construction",
        "lastRelayed": "January 2023",
        "engineer": "Executive Engineer, NHAI Chennai Zone",
        "engineerEmail": "ee.nhai.chennai@gov.in",
        "authority": "NHAI",
        "budget": {"sanctioned": 6800, "spent": 6100, "currency": "Cr",
                   "source": "NHAI Annual Report 2023–24"},
        "status": "Fair", "length": "3,745 km", "country": "India",
    },
    "SH-1": {
        "name": "SH-1 (Maharashtra State Highway 1)",
        "type": "SH", "typeLabel": "State Highway",
        "contractor": "IRB Infrastructure",
        "lastRelayed": "August 2023",
        "engineer": "Executive Engineer, PWD Maharashtra",
        "engineerEmail": "ee.pwd.mh@maharashtra.gov.in",
        "authority": "PWD Maharashtra",
        "budget": {"sanctioned": 320, "spent": 290, "currency": "Cr",
                   "source": "Maharashtra PWD Budget 2023–24"},
        "status": "Good", "length": "412 km", "country": "India",
    },
    "MDR-7": {
        "name": "MDR-7 (Pune District Road)",
        "type": "MDR", "typeLabel": "Major District Road",
        "contractor": "Dilip Buildcon",
        "lastRelayed": "June 2022",
        "engineer": "Executive Engineer, ZP Pune",
        "engineerEmail": "ee.zp.pune@maharashtra.gov.in",
        "authority": "Zila Parishad Pune",
        "budget": {"sanctioned": 45, "spent": 42, "currency": "Cr",
                   "source": "Zila Parishad Pune Annual Report 2022–23"},
        "status": "Poor", "length": "67 km", "country": "India",
    },
    "A2": {
        "name": "A2 (London–Dover Motorway)",
        "type": "NH", "typeLabel": "Motorway",
        "contractor": "Balfour Beatty",
        "lastRelayed": "November 2023",
        "engineer": "Regional Director, National Highways SE",
        "engineerEmail": "southeast@nationalhighways.co.uk",
        "authority": "National Highways UK",
        "budget": {"sanctioned": 180, "spent": 162, "currency": "M GBP",
                   "source": "National Highways Annual Report 2023–24"},
        "status": "Good", "length": "110 km", "country": "UK",
    },
}

ISSUE_TYPES = [
    "Pothole / Crater", "Road Surface Damage", "Missing Road Markings",
    "Broken Guardrails", "Poor Drainage / Flooding", "Missing Signage",
    "Streetlight Failure", "Encroachment on Road", "Bridge / Flyover Damage", "Other",
]

STATUS_BADGE = {
    "Good": '<span class="badge-good">● GOOD</span>',
    "Fair": '<span class="badge-fair">● FAIR</span>',
    "Poor": '<span class="badge-poor">● POOR</span>',
}

SEVERITY_COLOR = {"Critical": "#ef4444", "Moderate": "#f59e0b", "Minor": "#22c55e"}
RISK_COLOR     = {"High": "#ef4444",     "Medium": "#f59e0b",   "Low": "#22c55e"}

ANTHROPIC_API = "https://api.anthropic.com/v1/messages"
HEADERS = {"Content-Type": "application/json"}


# ─── API Helpers ──────────────────────────────────────────────────────────────
def call_claude(messages, system="", max_tokens=1000):
    body = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system:
        body["system"] = system
    try:
        r = requests.post(ANTHROPIC_API, headers=HEADERS, json=body, timeout=30)
        data = r.json()
        return "".join(b.get("text", "") for b in data.get("content", []))
    except Exception as e:
        return f"Error: {e}"


def analyse_image(img_bytes, mime="image/jpeg"):
    b64 = base64.b64encode(img_bytes).decode()
    system = """You are a road quality inspector AI. Analyse the road image and return ONLY a valid JSON object (no markdown, no backticks):
{
  "severity": "Critical" | "Moderate" | "Minor",
  "issueType": "<one of the standard issue types>",
  "confidence": <0-100>,
  "description": "<2-3 sentences describing damage>",
  "urgency": "<one sentence on repair urgency>",
  "safetyRisk": "High" | "Medium" | "Low"
}"""
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}},
            {"type": "text", "text": "Analyse this road image for damage or issues."}
        ]
    }]
    raw = call_claude(messages, system=system)
    try:
        return json.loads(raw.replace("```json", "").replace("```", "").strip())
    except Exception:
        return None


# ─── Session state init ───────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "complaint_submitted" not in st.session_state:
    st.session_state.complaint_submitted = False
if "ai_result" not in st.session_state:
    st.session_state.ai_result = None
if "complaint_road_key" not in st.session_state:
    st.session_state.complaint_road_key = None


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rw-header">
  <div class="rw-logo">🛣️</div>
  <div>
    <p class="rw-title">TiRo</p>
    <p class="rw-sub">Road Transparency Platform</p>
  </div>
</div>
""", unsafe_allow_html=True)

# Country filter in sidebar
with st.sidebar:
    st.markdown("### 🌍 Filter by Country")
    country_filter = st.selectbox("", ["All", "India", "UK"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### ℹ️ About TiRo")
    st.markdown("""
TiRo is an AI-powered platform helping citizens monitor:
- Road quality & contractors
- Public spending transparency
- Filing complaints to the right authority

**Built for the RoadWatch Hackathon** 🏆
    """)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Assistant", "🛣️ Road Explorer", "💰 Budget Tracker", "📢 File Complaint"])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — AI CHATBOT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("#### Ask anything about roads, budgets, or contractors")

    SYSTEM_PROMPT = f"""You are TiRo AI, a helpful assistant for a road transparency platform.
You help citizens find information about road contractors, budgets, maintenance history, and how to file complaints.

Available roads: {', '.join(ROADS_DB.keys())}

Road data:
{json.dumps(ROADS_DB, indent=2)}

Guidelines:
- Give specific contractor, budget, and engineer details from the data
- If a road is not in the DB, say so politely
- Help route complaints to the correct authority based on road type
- Be concise, factual, and citizen-friendly
- Use ₹ for Indian roads, £ for UK roads
- Keep responses under 200 words"""

    # Quick prompts
    st.markdown("**Quick questions:**")
    cols = st.columns(4)
    quick = ["Who built NH-48?", "Budget for MDR-7?", "How to complain for SH-1?", "Status of A2 UK?"]
    for i, q in enumerate(quick):
        if cols[i].button(q, key=f"quick_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": q})
            with st.spinner("Thinking…"):
                reply = call_claude(
                    [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history],
                    system=SYSTEM_PROMPT
                )
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # Display history
    for msg in st.session_state.chat_history:
        cls = "chat-user" if msg["role"] == "user" else "chat-ai"
        prefix = "You" if msg["role"] == "user" else "🤖 TiRo AI"
        st.markdown(f'<div class="{cls}"><strong>{prefix}:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    with st.container():
        user_input = st.text_input("Your question", placeholder="e.g. Who is responsible for NH-44 maintenance?", label_visibility="collapsed", key="chat_input")
        send = st.button("Send ➤", key="send_btn")

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("TiRo AI is thinking…"):
            reply = call_claude(
                [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history],
                system=SYSTEM_PROMPT
            )
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ROAD EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### Search & Explore Road Data")
    search = st.text_input("🔍 Search by road name, contractor, or type…", label_visibility="collapsed", key="road_search")

    filtered = [
        r for r in ROADS_DB.values()
        if (country_filter == "All" or r["country"] == country_filter)
        and (search.lower() in r["name"].lower()
             or search.lower() in r["contractor"].lower()
             or search.lower() in r["type"].lower()
             or search.lower() in r["authority"].lower())
    ]

    for road in filtered:
        sym = "₹" if road["budget"]["currency"] == "Cr" else "£"
        pct = int(road["budget"]["spent"] / road["budget"]["sanctioned"] * 100)

        with st.expander(f"{road['type']} · {road['name']}", expanded=False):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f'<div class="road-type-badge">{road["typeLabel"]} · {road["country"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="road-name">{road["name"]}</div>', unsafe_allow_html=True)
            with c2:
                st.markdown(STATUS_BADGE[road["status"]], unsafe_allow_html=True)

            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🏗️ Contractor", road["contractor"])
            col2.metric("📅 Last Relayed", road["lastRelayed"])
            col3.metric("📏 Length", road["length"])
            col4.metric("🏛️ Authority", road["authority"])

            st.markdown("**💰 Budget Utilisation**")
            st.progress(min(pct / 100, 1.0))
            st.markdown(f"`{sym}{road['budget']['spent']} {road['budget']['currency']}` spent of `{sym}{road['budget']['sanctioned']} {road['budget']['currency']}` sanctioned  ·  **{pct}%**")
            st.caption(f"📌 Source: {road['budget']['source']}")

            st.markdown(f"**👷 Complaint Officer:** {road['engineer']}  \n📧 `{road['engineerEmail']}`")

            if st.button(f"⚠️ Report Issue on {road['type']}", key=f"complain_{road['type']}"):
                st.session_state.complaint_road_key = [k for k, v in ROADS_DB.items() if v["name"] == road["name"]][0]
                st.session_state.complaint_submitted = False
                st.session_state.ai_result = None
                st.info(f"➡️ Switch to the **📢 File Complaint** tab — {road['name']} is pre-selected.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — BUDGET TRACKER
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("#### Budget Transparency — All figures from official sources")

    budget_roads = [r for r in ROADS_DB.values() if country_filter == "All" or r["country"] == country_filter]

    for road in budget_roads:
        sym = "₹" if road["budget"]["currency"] == "Cr" else "£"
        pct = int(road["budget"]["spent"] / road["budget"]["sanctioned"] * 100)
        remaining = road["budget"]["sanctioned"] - road["budget"]["spent"]
        over = road["budget"]["spent"] > road["budget"]["sanctioned"]

        with st.container():
            st.markdown(f"""
<div class="road-card">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
    <div>
      <div class="road-type-badge">{road['type']} · {road['country']}</div>
      <div class="road-name">{road['name']}</div>
    </div>
    <div style="text-align:right;">
      <div style="font-size:26px; font-weight:800; color:{'#ef4444' if over or pct > 95 else '#22c55e'};">{pct}%</div>
      <div style="font-size:11px; color:#64748b;">of budget spent</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("Sanctioned", f"{sym}{road['budget']['sanctioned']} {road['budget']['currency']}", delta=None)
            c2.metric("Spent", f"{sym}{road['budget']['spent']} {road['budget']['currency']}")
            c3.metric("Remaining", f"{sym}{remaining} {road['budget']['currency']}")

            color = "#ef4444" if over or pct > 95 else "#3b82f6"
            st.markdown(f"""
<div class="budget-bar-bg">
  <div class="budget-bar-fill" style="width:{min(pct,100)}%; background:{'#ef4444' if over else 'linear-gradient(90deg,#3b82f6,#22c55e)'};"></div>
</div>
<div class="source-note">📌 {road['budget']['source']}</div>
""", unsafe_allow_html=True)
            st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — FILE COMPLAINT
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("#### Report a Road Issue")

    if st.session_state.complaint_submitted:
        road = ROADS_DB[st.session_state.complaint_road_key]
        import random, string
        ref = "TR-" + "".join(random.choices(string.digits, k=6))
        st.markdown(f"""
<div class="success-box">
  <div style="font-size:52px; margin-bottom:12px;">✅</div>
  <h3 style="color:#22c55e; font-family:'Syne',sans-serif; margin:0 0 8px;">Complaint Filed Successfully!</h3>
  <p style="color:#94a3b8; font-size:15px;">
    Routed to:<br/>
    <strong style="color:#93c5fd;">{road['engineer']}</strong><br/>
    <span style="color:#64748b;">{road['engineerEmail']}</span>
  </p>
  <p style="color:#64748b; font-size:13px; margin-top:10px;">Reference ID: <strong>{ref}</strong></p>
</div>
""", unsafe_allow_html=True)

        if st.session_state.ai_result:
            ar = st.session_state.ai_result
            sc = SEVERITY_COLOR.get(ar.get("severity",""), "#64748b")
            rc = RISK_COLOR.get(ar.get("safetyRisk",""), "#64748b")
            st.markdown(f"""
<div class="ai-box" style="margin-top:16px;">
  <div class="ai-label">🤖 AI DAMAGE REPORT ATTACHED</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
    <span style="background:{sc}22;color:{sc};border:1px solid {sc}44;border-radius:20px;padding:3px 12px;font-size:12px;font-weight:700;">{ar.get('severity','')} Severity</span>
    <span style="background:{rc}22;color:{rc};border:1px solid {rc}44;border-radius:20px;padding:3px 12px;font-size:12px;font-weight:700;">{ar.get('safetyRisk','')} Risk</span>
    <span style="background:#1e293b;color:#94a3b8;border-radius:20px;padding:3px 12px;font-size:12px;">{ar.get('confidence',0)}% confidence</span>
  </div>
  <p style="color:#cbd5e1;font-size:13px;line-height:1.6;">{ar.get('description','')}</p>
  <p style="color:#f59e0b;font-size:12px;font-style:italic;">⏱ {ar.get('urgency','')}</p>
</div>
""", unsafe_allow_html=True)

        if st.button("📋 File Another Complaint"):
            st.session_state.complaint_submitted = False
            st.session_state.ai_result = None
            st.rerun()

    else:
        # Road selector
        road_keys = list(ROADS_DB.keys())
        default_idx = road_keys.index(st.session_state.complaint_road_key) if st.session_state.complaint_road_key in road_keys else 0
        selected_key = st.selectbox(
            "Select Road",
            road_keys,
            index=default_idx,
            format_func=lambda k: ROADS_DB[k]["name"]
        )
        road = ROADS_DB[selected_key]

        st.markdown(f"""
<div class="info-box" style="border-color:#1e3a5f;">
  <div class="info-label">👷 Will be routed to</div>
  <div class="info-value" style="color:#93c5fd;">{road['engineer']}</div>
  <div style="font-size:12px;color:#475569;">{road['engineerEmail']}</div>
</div>
""", unsafe_allow_html=True)

        # ── Photo Upload ──────────────────────────────────────────────────────
        st.markdown("**📸 Upload Photo of the Issue**")
        uploaded_file = st.file_uploader(
            "Upload road photo",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
            key="road_photo"
        )

        ai_result = None
        auto_issue = ""
        auto_desc = ""

        if uploaded_file:
            img_bytes = uploaded_file.read()
            mime = uploaded_file.type or "image/jpeg"

            # Show preview
            img = Image.open(io.BytesIO(img_bytes))
            st.image(img, caption="Uploaded photo", use_column_width=True)

            # AI Analysis
            with st.spinner("🤖 AI is analysing the road damage…"):
                ai_result = analyse_image(img_bytes, mime)
                st.session_state.ai_result = ai_result

            if ai_result:
                sc = SEVERITY_COLOR.get(ai_result.get("severity", ""), "#64748b")
                rc = RISK_COLOR.get(ai_result.get("safetyRisk", ""), "#64748b")
                st.markdown(f"""
<div class="ai-box">
  <div class="ai-label">🤖 AI DAMAGE ANALYSIS</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">
    <span style="background:{sc}22;color:{sc};border:1px solid {sc}44;border-radius:20px;padding:3px 12px;font-size:12px;font-weight:700;">{ai_result.get('severity','')} Severity</span>
    <span style="background:{rc}22;color:{rc};border:1px solid {rc}44;border-radius:20px;padding:3px 12px;font-size:12px;font-weight:700;">{ai_result.get('safetyRisk','')} Risk</span>
    <span style="background:#1e293b;color:#94a3b8;border-radius:20px;padding:3px 12px;font-size:12px;">{ai_result.get('confidence',0)}% confidence</span>
  </div>
  <p style="color:#cbd5e1;font-size:13px;line-height:1.6;margin-bottom:8px;">{ai_result.get('description','')}</p>
  <p style="color:#f59e0b;font-size:12px;font-style:italic;">⏱ {ai_result.get('urgency','')}</p>
  <p style="color:#475569;font-size:11px;margin-top:8px;">Issue type & description pre-filled below ↓</p>
</div>
""", unsafe_allow_html=True)
                auto_issue = ai_result.get("issueType", "")
                auto_desc  = ai_result.get("description", "")
            else:
                st.warning("⚠️ Could not auto-analyse the image. Please fill in details manually.")

        st.markdown("---")

        # ── Form fields ───────────────────────────────────────────────────────
        issue_options = [""] + ISSUE_TYPES
        issue_idx = issue_options.index(auto_issue) if auto_issue in issue_options else 0
        issue = st.selectbox("Issue Type *", issue_options, index=issue_idx)

        location = st.text_input("Exact Location / Landmark *", placeholder="e.g. Near Km 142, beside Toll Plaza 4")
        description = st.text_area("Description *", value=auto_desc, placeholder="Describe the issue in detail…", height=100)

        label = "📤 Submit Complaint with AI Report" if ai_result else "📤 Submit Complaint"
        if st.button(label):
            if not issue or not location or not description:
                st.error("Please fill in Issue Type, Location, and Description before submitting.")
            else:
                st.session_state.complaint_submitted = True
                st.session_state.complaint_road_key = selected_key
                if ai_result:
                    st.session_state.ai_result = ai_result
                st.rerun()
