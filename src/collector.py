import requests
import pandas as pd
from datetime import datetime
import os

class ThreatIntelCollector:
    def __init__(self):
        self.sources = {
            'abuse_ch': 'https://feodotracker.abuse.ch/downloads/ipblocklist.csv',
            'emerging_threats': 'https://rules.emergingthreats.net/blockrules/compromised-ips.txt'
        }
        self.data_dir = 'data'

    def fetch_abuse_ch(self):
        """Récupère les IPs malveillantes depuis Abuse.ch FeodoTracker"""
        try:
            response = requests.get(self.sources['abuse_ch'], timeout=10)
            lines = response.text.strip().split('\n')
            
            ips = []
            for line in lines:
                if not line.startswith('#') and line.strip():
                    parts = line.split(',')
                    if len(parts) >= 3:
                        ips.append({
                            'ip': parts[1].strip(),
                            'type': parts[2].strip(),
                            'source': 'abuse.ch',
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
            
            print(f"✅ Abuse.ch : {len(ips)} IPs récupérées")
            return pd.DataFrame(ips)
            
        except Exception as e:
            print(f"❌ Erreur Abuse.ch : {e}")
            return pd.DataFrame()

    def fetch_emerging_threats(self):
        """Récupère les IPs compromises depuis Emerging Threats"""
        try:
            response = requests.get(self.sources['emerging_threats'], timeout=10)
            lines = response.text.strip().split('\n')
            
            ips = []
            for line in lines:
                if not line.startswith('#') and line.strip():
                    ips.append({
                        'ip': line.strip(),
                        'type': 'compromised',
                        'source': 'emerging_threats',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            print(f"✅ Emerging Threats : {len(ips)} IPs récupérées")
            return pd.DataFrame(ips)
            
        except Exception as e:
            print(f"❌ Erreur Emerging Threats : {e}")
            return pd.DataFrame()

    def collect_all(self):
        """Collecte toutes les sources et sauvegarde en CSV"""
        print(" Collecte des threat feeds en cours...")
        
        df_abuse = self.fetch_abuse_ch()
        df_emerging = self.fetch_emerging_threats()
        
        all_data = pd.concat([df_abuse, df_emerging], ignore_index=True)
        
        if not all_data.empty:
            filepath = os.path.join(self.data_dir, 'threat_data.csv')
            all_data.to_csv(filepath, index=False)
            print(f" Données sauvegardées : {len(all_data)} entrées")
            return all_data
        else:
            print(" Aucune donnée collectée")
            return pd.DataFrame()

    def check_ip(self, ip_to_check):
        """Vérifie si une IP est dans la liste des menaces"""
        filepath = os.path.join(self.data_dir, 'threat_data.csv')
        
        if not os.path.exists(filepath):
            return {
                "status": "error", 
                "message": "Aucune donnée. Clique sur 'Mettre à jour les données' d'abord."
            }
        
        df = pd.read_csv(filepath)
        matches = df[df['ip'] == ip_to_check]
        
        if not matches.empty:
            return {
                "status": "MALICIOUS",
                "ip": ip_to_check,
                "sources": matches['source'].tolist(),
                "types": matches['type'].tolist()
            }
        else:
            return {
                "status": "CLEAN",
                "ip": ip_to_check,
                "message": "IP non trouvée dans les threat feeds"
            }


if __name__ == "__main__":
    collector = ThreatIntelCollector()
    data = collector.collect_all()
    print(data.head())
    