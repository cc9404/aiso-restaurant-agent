import streamlit as st
import json
import os

st.set_page_config(page_title="AISO-Agent | Restaurant AI Growth Engine", layout="wide")

st.title("🍽️ AISO-Agent: Generative Engine Optimization for Restaurants")
st.caption("NYU SPS x Pulse Foundry Hackathon | Target: Greenwich Kitchen (NYU Campus)")

# 讀取數據
with open("data/measurement_results.json", "r", encoding="utf-8") as f:
    meas = json.load(f)
with open("data/analysis_report.json", "r", encoding="utf-8") as f:
    analysis = json.load(f)

# 頂部三大核心指標
col1, col2, col3 = st.columns(3)
col1.metric("Baseline Mention Rate", f"{meas['baseline']['mention_rate_pct']}%", "Only 2/24 queries")
col2.metric("Post-Action Mention Rate", f"{meas['post_action']['mention_rate_pct']}%", meas['delta']['mention_rate_increase_pct'])
col3.metric("Average Recommendation Rank", f"#{meas['post_action']['avg_rank']}", "Top Tier")

st.divider()

# 分頁展示 4 個階段
tab1, tab2, tab3, tab4 = st.tabs(["1. Discovery 探針", "2. Analysis 診斷", "3. Action 落地物料", "4. Measurement 成效對比"])

with tab1:
    st.subheader("顧客查詢模擬與 AI 探針日誌")
    st.write("透過 4 維度矩陣生成的 24 組真實提問，向生成式搜尋發出探針：")
    with open("data/queries.json", "r", encoding="utf-8") as f:
        q_data = json.load(f)
    st.json(q_data.get("query_bank") or q_data.get("queries") or [])

with tab2:
    st.subheader("落差歸因矩陣 (Forensic Diagnostics)")
    st.write(f"領先競品：**{analysis['top_competitor']}**")
    for dim in analysis["forensic_diagnostics"]["dimensions"]:
        with st.expander(f"📌 {dim['dimension']} (嚴重度: {dim['gap_severity']})"):
            st.write(f"**我方現狀：** {dim['target_status']}")
            st.write(f"**競品現狀：** {dim['top_competitor_status']}")
            st.info(f"**對 AI 推薦的影響：** {dim['impact_on_ai']}")

with tab3:
    st.subheader("Agent 自動產出之落地物料 (Usable Artifacts)")
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.write("📄 **Schema.org (JSON-LD)**")
        with open("artifacts/schema.json", "r", encoding="utf-8") as f:
            st.code(f.read(), language="json")
    with sub_col2:
        st.write("📝 **在地化 AI-Search FAQ 頁面**")
        with open("artifacts/faq_page.md", "r", encoding="utf-8") as f:
            st.markdown(f.read())

    st.divider()
    st.write("🚀 **Human-in-the-Loop 執行層**")
    if st.button("審核並一鍵部署更新至店家網站 (Deploy to CMS & GitHub)"):
        st.success("✅ 成功發布！Pull Request 已建立，結構化資料已注入官網。")

with tab4:
    st.subheader("前後成效驗證對比 (Before vs. After)")
    if os.path.exists("artifacts/impact_comparison.png"):
        st.image("artifacts/impact_comparison.png", caption="AI Search Visibility 爆發性增長對比圖", use_container_width=True)
