"""ExportaÃ§Ã£o de relatÃ³rios para PDF e Excel."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUTPUT_DIR = Path("assets/reports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def export_pdf_report(stats: dict, alerts: list, output_path: Optional[str] = None) -> str:
    """Gera um relatÃ³rio resumido em PDF."""
    output = Path(output_path or OUTPUT_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(output), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("A.R.G.U.S. - RelatÃ³rio de Sistema", styles["Title"]))
    story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    rows = [["MÃ©trica", "Valor"]]
    for key, value in stats.items():
        if isinstance(value, (dict, list)):
            value = "-"
        rows.append([key, str(value)])

    table = Table(rows, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00aaff")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("Alertas recentes:", styles["Heading2"]))
    for alert in alerts[:10]:
        story.append(Paragraph(f"- {alert}", styles["BodyText"]))

    doc.build(story)
    return str(output)


def export_excel_report(stats: dict, alerts: list, output_path: Optional[str] = None) -> str:
    """Gera um relatÃ³rio resumido em Excel."""
    output = Path(output_path or OUTPUT_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for key, value in stats.items():
        rows.append({"metric": key, "value": value})
    df = pd.DataFrame(rows)
    df.to_excel(output, index=False)

    return str(output)


def export_summary_report(stats: dict, alerts: list, output_path: Optional[str] = None, format_type: str = "pdf") -> str:
    """Exporta relatÃ³rio em PDF ou Excel."""
    format_type = format_type.lower()
    if format_type == "excel":
        return export_excel_report(stats, alerts, output_path)
    return export_pdf_report(stats, alerts, output_path)

