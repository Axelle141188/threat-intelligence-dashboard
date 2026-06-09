# Threat Intelligence Dashboard

🚀 **Live Demo** : [axelle-threat-intelligence.streamlit.app](https://axelle-threat-intelligence.streamlit.app)

A real-time cyber threat monitoring system that aggregates public threat feeds,
visualizes malicious IPs, and allows instant IP reputation checks.

> Built as part of a cybersecurity portfolio targeting fraud detection roles
> in the banking and financial sector.
## Features

- Real-time data collection from public threat feeds (Abuse.ch, Emerging Threats)
- Interactive dashboard with threat statistics and visualizations
- Instant IP reputation checker (MALICIOUS / CLEAN)
- Automated threat type classification
- Modular architecture (collector / analyzer / dashboard)
## Tech Stack

| Tool | Usage |
|------|-------|
| Python 3.x | Core language |
| Streamlit | Interactive dashboard |
| Plotly | Data visualizations |
| Pandas | Data processing |
| Requests | Threat feed collection |
## Installation

```bash
# 1. Clone le repository
git clone https://github.com/Axelle141188/threat-intelligence-dashboard
cd threat-intelligence-dashboard

# 2. Installe les dépendances
pip install -r requirements.txt

# 3. Lance le dashboard
streamlit run src/dashboard.py
```

Ouvre ton navigateur sur **http://localhost:8501**
## Data Sources

- **[Abuse.ch FeodoTracker](https://feodotracker.abuse.ch/)** — Tracks Command & Control
  servers of banking trojans (Emotet, TrickBot, Dridex). Directly relevant to
  financial sector threat monitoring.

- **[Emerging Threats](https://rules.emergingthreats.net/)** — Compromised IPs
  actively used in attack campaigns.

*All data sources are public, free, and updated daily.*
## Project Structure

```
threat-intelligence-dashboard/
├── data/
│   └── threat_data.csv        # Collected threat feeds (auto-generated)
├── src/
│   ├── collector.py           # Fetches & saves threat feed data
│   ├── analyzer.py            # Computes statistics & generates reports
│   └── dashboard.py           # Streamlit visual interface
├── requirements.txt
└── README.md
```

## Author

**Axelle** — Aspiring Behavioral Fraud Detection Specialist

- 🎓 Background in Psychology | Google Data Analytics Certificate
- 🔐 CompTIA Security+ in preparation | CySA+ planned
- 🌍 French (native) | Portuguese (native) | English (working knowledge)
- 🎯 Targeting fraud detection roles in the banking and financial sector

*"I designed this dashboard so that an analyst can see not only the IP,
but also the threat type — in order to adapt their response when
supporting victims of cybercrime."*
