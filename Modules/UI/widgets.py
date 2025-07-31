import streamlit as st

def show_tfidf_widgets(conferences, tf_dfs):
    available_words= tf_dfs['annual'][0].index.values
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Widgets for the left column
        conf = st.selectbox("Select Conference", conferences)
        region_key = "annual" if conf == "International" else conf.lower()
        
        # Get the specific years for the selected conference
        years_for_conf = sorted(tf_dfs[region_key][0].columns.values.tolist())
        
        # Create a slider for the year range
        start_year, end_year = st.slider(
            "Select Year Range",
            min_value=min(years_for_conf),
            max_value=max(years_for_conf),
            value=(min(years_for_conf), max(years_for_conf))
        )
        # The current logic of semmantic_drift_plot_matplotlib expects a single year,
        # so we'll need to adapt this. For now, let's just use the start year.
        # We'll use start_year for plotting and the slider for UI.
        year = start_year
    
    
    with col2:
        # Widget for the right column
        st.markdown("### 🔍 Keywords to Highlight")
        keywords_input = st.multiselect(
            "Select KeyWords", options=available_words, 
            default=[
                    # AI & Machine Learning
                    "generative ai", "ai", "machine learning", "llm", "reinforcement learning",
                    "deep learning", "computer vision", "natural language processing", "neural network",
                    # Supply Chain & Logistics
                    "supply chain", "smart logistics", "logistics", "lean manufacturing", "green supply chain",
                    "six sigma", "tqm", "agile", "warehouse layout", "inventory management", "circular economy",       
                    # Digital Transformation & Technologies
                    "digital transformation", "digital twin", "blockchain", "iot", "internet thing",
                    "cloud computing", "automation", "digital",
                    # Data & Analytics
                    "data", "big data", "clustering", "data analytics", "business intelligence",
                    "data driven", "predictive analytics",
                    # Optimization & Modeling
                    "optimization", "simulation", "linear programming", "queuing theory",
                    # Human & Management
                    "management", "leadership", "ethic", "ethical", "kpis", "education",
                    # Sustainability & Resilience
                    "sustainability", "carbon footprint", "energy",
                    #"green manufacturing", "resilience", "uncertainty",
                    # Domain-Specific
                    #"covid", "healthcare", "tariff"
                ]

        )

    return region_key, start_year, end_year, keywords_input
