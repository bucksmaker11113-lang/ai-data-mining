from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def create_report(self, ai_stats, feedback, correlation):
        """Magyar nyelvű napi riport szöveg"""
        report = f"""
AI Data Mining 2.0 Napi Jelentés – {self.date}
===============================================

📊 TANULÁSI EREDMÉNYEK
-----------------------
• Modell pontosság: {ai_stats.get('accuracy', 0):.2%}
• Value bias változás: {ai_stats.get('bias_shift', 0):+.2f}
• ROI stabilitás: {ai_stats.get('roi_stability', 0):+.2f}
• Aktív tanulási motor: {ai_stats.get('engine', 'FusionCore')}

📈 RENDSZER TELJESÍTMÉNY
-------------------------
• Összes tréningfutás: {ai_stats.get('train_count', 0)}
• Átlagos visszacsatolási pont
