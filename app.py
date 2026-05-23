import streamlit as st
import time
import io

st.set_page_config(
    page_title="ResearchMesh",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;800&display=swap');

/* ── root ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0f1117 !important;
    color: #c8d0dc;
}

/* ── main container ── */
.block-container {
    max-width: 900px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
    background-color: #0f1117 !important;
}

/* ── Force dark bg on streamlit wrappers ── */
.stApp, .main, section[data-testid="stSidebar"], 
div[data-testid="stAppViewContainer"], div[data-testid="stHeader"] {
    background-color: #0f1117 !important;
}

/* ── hero header ── */
.hero {
    text-align: center;
    margin-bottom: 2.5rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3rem;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #00e5ff 0%, #00b4d8 40%, #7b2ff7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}
.hero p {
    color: #5a6478;
    font-size: 1rem;
    letter-spacing: 0.05em;
    margin-top: 0;
}

/* ── input text box — smoky dark gray, NOT pure black ── */
.stTextInput > div > div > input {
    background: #1c2130 !important;
    border: 1.5px solid #2a3348 !important;
    border-radius: 10px !important;
    color: #d4dbe8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
    caret-color: #00e5ff;
}
.stTextInput > div > div > input::placeholder {
    color: #4a5568 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00e5ff !important;
    box-shadow: 0 0 0 3px rgba(0,229,255,0.10) !important;
    outline: none !important;
}
.stTextInput > label { 
    color: #7a8699 !important; 
    font-size: 0.78rem !important; 
    letter-spacing: 0.1em; 
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
}

/* ── run button ── */
.stButton > button {
    background: linear-gradient(135deg, #00b4d8, #7b2ff7) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.06em !important;
    padding: 0.65rem 2.2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

/* ── pipeline timeline ── */
.timeline {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    margin: 1.5rem 0 2rem 0;
}
.tl-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    min-width: 90px;
}
.tl-dot {
    width: 38px; height: 38px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.82rem;
    font-family: 'JetBrains Mono', monospace;
    border: 2px solid #252d3d;
    background: #161c28;
    color: #3d4a60;
    transition: all 0.45s ease;
    position: relative;
}
/* active = blue, pulsing */
.tl-dot.active {
    border-color: #00e5ff;
    color: #00e5ff;
    background: rgba(0,229,255,0.10);
    box-shadow: 0 0 0 4px rgba(0,229,255,0.15), 0 0 18px rgba(0,229,255,0.25);
    animation: pulse-blue 1.6s ease-in-out infinite;
}
/* done = green, steady */
.tl-dot.done {
    border-color: #34d399;
    color: #34d399;
    background: rgba(52,211,153,0.10);
    box-shadow: 0 0 10px rgba(52,211,153,0.18);
}
@keyframes pulse-blue {
    0%, 100% { box-shadow: 0 0 0 4px rgba(0,229,255,0.15), 0 0 14px rgba(0,229,255,0.2); }
    50%       { box-shadow: 0 0 0 8px rgba(0,229,255,0.08), 0 0 26px rgba(0,229,255,0.35); }
}

.tl-label { 
    font-size: 0.68rem; 
    color: #3d4a60; 
    text-align: center; 
    letter-spacing: 0.06em; 
    font-family: 'JetBrains Mono', monospace;
    transition: color 0.4s;
}
.tl-label.active { color: #00e5ff; }
.tl-label.done   { color: #34d399; }

.tl-line { 
    flex: 1; 
    height: 2px; 
    background: #1e2736; 
    min-width: 40px; 
    margin-bottom: 24px; 
    transition: background 0.5s;
    position: relative;
    overflow: hidden;
}
.tl-line.active {
    background: linear-gradient(90deg, #34d399 0%, #00e5ff 100%);
}
.tl-line.done {
    background: linear-gradient(90deg, #34d399, #00b4d8);
}

/* ── expander override ── */
.streamlit-expanderHeader {
    background: #0b0f1a !important;
    border: 1px solid rgba(58,123,255,0.45) !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    font-size: 0.88rem !important;
    padding: 0.75rem 1rem !important;
    box-shadow: 0 0 12px rgba(58,123,255,0.2);
}
.streamlit-expanderContent {
    background: #131921 !important;
    border: 1px solid #1e2a38 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

div[data-testid="stExpander"] { margin-top: 0.4rem; margin-bottom: 0.6rem; }

/* ── output boxes — smoky blue-gray, NOT black ── */
.output-box {
    background: #0b0f1a;
    border: 1px solid rgba(0,240,255,0.35);
    border-radius: 10px;
    width: 100%;
    padding: 1.1rem 1.25rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: #eaf9ff;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 420px;
    overflow-y: auto;
    overflow-x: auto;
    box-shadow: 0 0 18px rgba(0,240,255,0.18), inset 0 0 12px rgba(0,240,255,0.08);
}

.output-box::-webkit-scrollbar { width: 6px; height: 6px; }
.output-box::-webkit-scrollbar-track { background: transparent; }
.output-box::-webkit-scrollbar-thumb { background: #2a3a50; border-radius: 4px; }
.output-box::-webkit-scrollbar-thumb:hover { background: #3a4e68; }

/* ── report box — slightly warmer smoky tone ── */
.report-box {
    background: #0c1020;
    border: 1px solid rgba(255,60,248,0.35);
    border-radius: 10px;
    width: 100%;
    padding: 1.4rem 1.5rem;
    font-family: 'Syne', sans-serif;
    font-size: 0.93rem;
    color: #f7eaff;
    line-height: 1.85;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 520px;
    overflow-y: auto;
    overflow-x: auto;
    box-shadow: 0 0 20px rgba(255,60,248,0.18), inset 0 0 12px rgba(255,60,248,0.08);
}

.report-box::-webkit-scrollbar { width: 6px; height: 6px; }
.report-box::-webkit-scrollbar-track { background: transparent; }
.report-box::-webkit-scrollbar-thumb { background: #2a3a50; border-radius: 4px; }
.report-box::-webkit-scrollbar-thumb:hover { background: #3a4e68; }

/* ── download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1.5px solid #34d399 !important;
    color: #34d399 !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.55rem 1.6rem !important;
    transition: background 0.2s, color 0.2s !important;
    background-color: rgba(52,211,153,0.05) !important;
}
.stDownloadButton > button:hover {
    background: rgba(52,211,153,0.14) !important;
}

/* ── spinner ── */
.stSpinner > div { color: #00e5ff !important; }
div[data-testid="stStatusWidget"] { color: #00e5ff !important; }

/* ── section label ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    color: #4a5a72;
    letter-spacing: 0.12em;
    font-size: 0.75rem;
    margin-bottom: 1.2rem;
    text-transform: uppercase;
}

/* ── divider ── */
hr { border-color: #1e2736 !important; }

/* ── scroll bar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2a3a50; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3a4e68; }

/* ── warning ── */
.stAlert { background: rgba(251,191,36,0.08) !important; border-color: rgba(251,191,36,0.25) !important; color: #fbbf24 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Session state init
# ─────────────────────────────────────────────
for key in ["pipeline_state", "pipeline_done", "current_step", "pipeline_running"]:
    if key not in st.session_state:
        if key == "pipeline_state":
            st.session_state[key] = None
        elif key == "pipeline_done":
            st.session_state[key] = False
        elif key == "pipeline_running":
            st.session_state[key] = False
        else:
            st.session_state[key] = 0


# ─────────────────────────────────────────────
#  Hero
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔬 ResearchMesh</h1>
    <p>MULTI-AGENT RESEARCH PIPELINE  ·  SEARCH → SCRAPE → WRITE → CRITIQUE</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Pipeline timeline — single persistent render
#  step 0 = idle, 1-4 = active step, 5 = all done
# ─────────────────────────────────────────────
PIPELINE_PLACEHOLDER = st.empty()

def render_timeline(step: int):
    steps = ["Search", "Scrape", "Write", "Critique"]
    nodes_html = ""
    for i, label in enumerate(steps):
        num = i + 1
        if num < step:
            dot_cls = "done"
            lbl_cls = "done"
        elif num == step:
            dot_cls = "active"
            lbl_cls = "active"
        else:
            dot_cls = ""
            lbl_cls = ""

        # checkmark for done, number for others
        inner = "✓" if dot_cls == "done" else str(num)
        nodes_html += (
            f'<div class="tl-node">'
            f'  <div class="tl-dot {dot_cls}">{inner}</div>'
            f'  <div class="tl-label {lbl_cls}">{label}</div>'
            f'</div>'
        )
        if i < len(steps) - 1:
            if num < step:
                line_cls = "done"
            elif num == step:
                line_cls = "active"
            else:
                line_cls = ""
            nodes_html += f'<div class="tl-line {line_cls}"></div>'

    PIPELINE_PLACEHOLDER.markdown(
        f'<div class="timeline">{nodes_html}</div>',
        unsafe_allow_html=True,
    )


# ── Initial idle render ───────────────────────
render_timeline(st.session_state.current_step or 0)


# ─────────────────────────────────────────────
#  Input + run button
# ─────────────────────────────────────────────
def start_run():
    st.session_state.pipeline_running = True

col_input, col_btn = st.columns([4, 1], gap="small")
with col_input:
    topic = st.text_input(
        "RESEARCH TOPIC",
        placeholder="e.g. Latest breakthroughs in quantum computing 2024",
        label_visibility="visible",
    )
with col_btn:
    st.write("")
    st.write("")
    run_clicked = st.button(
        "⚡ Run",
        use_container_width=True,
        disabled=st.session_state.pipeline_running,
        on_click=start_run,
    )

loading_placeholder = st.empty()
if st.session_state.pipeline_running:
    loading_placeholder.info("Researching...", icon="⏳")


# ─────────────────────────────────────────────
#  Run pipeline
# ─────────────────────────────────────────────
from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

if run_clicked and topic.strip():
    st.session_state.pipeline_state = None
    st.session_state.pipeline_done  = False
    st.session_state.current_step   = 0
    st.session_state.pipeline_running = True

    result = {}

    # ── Step 1: Search ───────────────────────
    st.session_state.current_step = 1
    render_timeline(1)
    with st.spinner("🔍  Search agent crawling the web…"):
        search_agent  = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user",
                f"Use the web_search tool. Return ONLY the raw tool output with titles, URLs, snippets. "
                f"Do not summarize. Topic: {topic}"
            )]
        })
        result["search_results"] = search_result["messages"][-1].content

    # ── Step 2: Scrape ───────────────────────
    st.session_state.current_step = 2
    render_timeline(2)
    with st.spinner("📄  Reader agent scraping the best source…"):
        reader_agent  = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{result['search_results'][:800]}"
            )]
        })
        result["scraped_content"] = reader_result["messages"][-1].content

    # ── Step 3: Write ────────────────────────
    st.session_state.current_step = 3
    render_timeline(3)
    with st.spinner("✍️  Writer drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{result['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{result['scraped_content']}"
        )
        result["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })

    # ── Step 4: Critique ─────────────────────
    st.session_state.current_step = 4
    render_timeline(4)
    with st.spinner("🧠  Critic reviewing the report…"):
        result["feedback"] = critic_chain.invoke({
            "report": result["report"]
        })

    st.session_state.pipeline_state = result
    st.session_state.pipeline_done  = True
    st.session_state.current_step   = 5   # all done
    st.session_state.pipeline_running = False
    render_timeline(5)

elif not topic.strip() and run_clicked:
    st.session_state.pipeline_running = False
    st.warning("Please enter a research topic first.")


# ─────────────────────────────────────────────
#  Render results (only when pipeline complete)
# ─────────────────────────────────────────────
if st.session_state.pipeline_done and st.session_state.pipeline_state:
    state = st.session_state.pipeline_state

    st.markdown("---")
    st.markdown('<p class="section-label">Pipeline Outputs</p>', unsafe_allow_html=True)

    with st.expander("01 · Search Agent  —  Raw Web Results", expanded=False):
        st.markdown(
            f'<div class="output-box">{state["search_results"]}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("02 · Reader Agent  —  Scraped Page Content", expanded=False):
        st.markdown(
            f'<div class="output-box">{state["scraped_content"]}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("03 · Writer Chain  —  Research Report", expanded=True):
        report_text = state["report"]
        if hasattr(report_text, "content"):
            report_text = report_text.content

        st.markdown(
            f'<div class="report-box">{report_text}</div>',
            unsafe_allow_html=True,
        )
        report_bytes = io.BytesIO(report_text.encode("utf-8"))
        safe_topic   = "".join(c if c.isalnum() or c in " _-" else "_" for c in (st.session_state.get("last_topic") or "report"))
        filename     = f"report_{safe_topic[:40].strip().replace(' ','_')}.txt"
        st.download_button(
            label="⬇  Download Report (.txt)",
            data=report_bytes,
            file_name=filename,
            mime="text/plain",
        )

    with st.expander("04 · Critic Chain  —  Review & Feedback", expanded=False):
        feedback_text = state["feedback"]
        if hasattr(feedback_text, "content"):
            feedback_text = feedback_text.content
        st.markdown(
            f'<div class="output-box">{feedback_text}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;color:#2d3d55;font-size:0.75rem;"
        "font-family:JetBrains Mono,monospace;'>ResearchMesh · pipeline complete</p>",
        unsafe_allow_html=True,
    )

elif not st.session_state.pipeline_done:
    st.markdown(
        "<p style='text-align:center;color:#2d3d55;font-size:0.82rem;"
        "font-family:JetBrains Mono,monospace;margin-top:1rem;'>"
        "Enter a topic above and hit ⚡ Run to start the pipeline.</p>",
        unsafe_allow_html=True,
    )

# store topic for filename use
if topic:
    st.session_state["last_topic"] = topic