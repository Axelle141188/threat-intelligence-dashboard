import pandas as pd
import os
from datetime import datetime

class ThreatAnalyzer:
    def __init__(self):
        self.data_dir = 'data'
        self.filepath = os.path.join(self.data_dir, 'threat_data.csv')

    def load_data(self):
        """Charge le fichier de données collectées"""
        if not os.path.exists(self.filepath):
            print("❌ Aucune donnée trouvée. Lance le collector d'abord.")
            return pd.DataFrame()
        return pd.read_csv(self.filepath)

    def get_stats(self):
        """Calcule les statistiques générales pour le dashboard"""
        df = self.load_data()
        if df.empty:
            return {}
        
        stats = {
            'total_threats': len(df),
            'unique_ips': df['ip'].nunique(),
            'sources_count': df['source'].value_counts().to_dict(),
            'types_count': df['type'].value_counts().to_dict(),
            'last_update': df['timestamp'].max()
        }
        return stats

    def get_top_threat_types(self, n=10):
        """Retourne les N types de menaces les plus fréquents"""
        df = self.load_data()
        if df.empty:
            return pd.DataFrame()
        return df['type'].value_counts().head(n).reset_index()

    def get_sources_breakdown(self):
        """Retourne la répartition des données par source"""
        df = self.load_data()
        if df.empty:
            return pd.DataFrame()
        return df['source'].value_counts().reset_index()

    def generate_report(self):
        """Génère un rapport texte complet"""
        stats = self.get_stats()
        if not stats:
            return "Aucune donnée disponible."
        
        report = f"""
========================================
   THREAT INTELLIGENCE REPORT
   Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
========================================

📊 STATISTIQUES GÉNÉRALES
- Total menaces détectées : {stats['total_threats']}
- IPs uniques malveillantes : {stats['unique_ips']}
- Dernière mise à jour : {stats['last_update']}

📡 SOURCES DE DONNÉES
"""
        for source, count in stats['sources_count'].items():
            report += f"- {source} : {count} entrées\n"
        
        report += "\n🔴 TYPES DE MENACES\n"
        for threat_type, count in stats['types_count'].items():
            report += f"- {threat_type} : {count}\n"
        
        report += "\n========================================"
        return report


if __name__ == "__main__":
    analyzer = ThreatAnalyzer()
    print(analyzer.generate_report())
    