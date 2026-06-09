import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from collector import ThreatIntelCollector
from analyzer import ThreatAnalyzer

st.set_page_config(
    page_title="Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide"
)

collector = ThreatIntelCollector()
analyzer = ThreatAnalyzer()

@st.cache_data(ttl=3600)
def load_threat_data():
    """Charge les feeds automatiquement — rafraîchi toutes les heures"""
    return collector.collect_all()

st.title("🛡️ Threat Intelligence Dashboard")
st.caption("Real-time Cyber Threat Monitoring System | Luxembourg Banking Sector Focus")
st.divider()

# Chargement automatique au démarrage
with st.spinner("Chargement des threat feeds en cours..."):
    load_threat_data()

col_btn, col_status = st.columns([1, 3])
with col_btn:
    update = st.button("🔄 Forcer la mise à jour")
with col_status:
    if update:
        st.cache_data.clear()
        with st.spinner("Collecte en cours..."):
            load_threat_data()
        st.success("✅ Données mises à jour avec succès !")

stats = analyzer.get_stats()
if stats:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Menaces", 
                  value=stats.get('total_threats', 0))
    with col2:
        st.metric(label="IPs Uniques", 
                  value=stats.get('unique_ips', 0))
    with col3:
        st.metric(label="Sources actives", 
                  value=len(stats.get('sources_count', {})))
    
    st.caption(f"Dernière mise à jour : {stats.get('last_update', 'Jamais')}")
else:
    st.warning("⚠️ Chargement des données en cours...")

st.divider()
st.subheader("Visualisations")
col_left, col_right = st.columns(2)
threat_types = analyzer.get_top_threat_types()
sources = analyzer.get_sources_breakdown()

with col_left:
    st.markdown("**Types de menaces**")
    if not threat_types.empty:
        fig_types = px.bar(
            threat_types, 
            x='count', 
            y='type', 
            orientation='h',
            color_discrete_sequence=['#ff4444']
        )
        fig_types.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_types, use_container_width=True)
    else:
        st.info("Pas de données disponibles.")

with col_right:
    st.markdown("**Sources de données**")
    if not sources.empty:
        fig_sources = px.pie(
            sources, 
            values='count', 
            names='source',
            color_discrete_sequence=['#00d4ff', '#ffaa00', '#00ff88']
        )
        fig_sources.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_sources, use_container_width=True)
    else:
        st.info("Pas de données disponibles.")

st.divider()
st.subheader("Vérifier une adresse IP")
ip_input = st.text_input(
    "Entrez une adresse IP",
    placeholder="ex: 192.168.1.1"
)

if st.button("Vérifier"):
    if ip_input:
        result = collector.check_ip(ip_input.strip())
        
        if result['status'] == 'MALICIOUS':
            st.error(f"⚠️ IP MALVEILLANTE : {ip_input}")
            st.write(f"**Sources :** {', '.join(result['sources'])}")
            st.write(f"**Types :** {', '.join(result['types'])}")
            
        elif result['status'] == 'CLEAN':
            st.success(f"✅ IP PROPRE : {ip_input}")
            st.write("Non détectée dans les threat feeds.")
            
        else:
            st.warning(result.get('message', 'Erreur inconnue.'))
    else:
        st.warning("Merci d'entrer une adresse IP.")
