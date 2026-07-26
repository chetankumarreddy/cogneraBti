from pathlib import Path
import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class FCAExporter:
    def __init__(self):
        self.out = Path(__file__).resolve().parents[3] / "evidence"
        self.out.mkdir(exist_ok=True)

    def export_csv(self, evs):
        path = self.out / "fca_export.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["txn_id", "entity", "risk_level", "risk_score", "rules"])
            for evidence in evs:
                writer.writerow([
                    evidence["transaction"]["txn_id"],
                    evidence["transaction"]["entity"],
                    evidence["risk"]["risk_level"],
                    evidence["risk"]["risk_score"],
                    ",".join(rule["rule_id"] for rule in evidence["rules"])
                ])
        return str(path)

    def export_pdf(self, evs):
        path = self.out / "fca_export.pdf"
        styles = getSampleStyleSheet()
        story = [Paragraph("Cognira BTI FCA Evidence Pack", styles["Title"]), Spacer(1, 12)]
        for evidence in evs:
            story.append(Paragraph(evidence["transaction"]["txn_id"], styles["Heading2"]))
            narrative = evidence["narrative"]["text"].replace("\n", "<br/>")
            story.append(Paragraph(narrative, styles["Normal"]))
            story.append(Spacer(1, 12))
        SimpleDocTemplate(str(path)).build(story)
        return str(path)
