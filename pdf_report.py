from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

def create_pdf(
    transcript,
    similarity,
    filler_ratio,
    pause_ratio,
    confidence,
    score,
    level,
):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(
        Paragraph("<b>Voice-Based Concept Understanding Report</b>", styles["Title"])
    )
    elements.append(Spacer(1, 15))

    # Reference Concept
    elements.append(Paragraph("<b>Reference Concept</b>", styles["Heading2"]))
    elements.append(
        Paragraph(
            "Machine Learning is a subset of Artificial Intelligence that enables systems to learn from data.",
            styles["BodyText"],
        )
    )

    elements.append(Spacer(1, 15))

    # Student Transcription
    elements.append(Paragraph("<b>Student Transcription</b>", styles["Heading2"]))
    elements.append(Paragraph(transcript, styles["BodyText"]))

    elements.append(Spacer(1, 15))

    # Audio Visualization
    elements.append(Paragraph("<b>Audio Visualization</b>", styles["Heading2"]))

    if os.path.exists("waveform.png"):
        img = Image("waveform.png")
        img.drawWidth = 450
        img.drawHeight = 170
        elements.append(img)
    else:
        elements.append(
            Paragraph("Waveform image not available.", styles["BodyText"])
        )

    elements.append(Spacer(1, 20))

    # Evaluation Summary
    elements.append(Paragraph("<b>Evaluation Summary</b>", styles["Heading2"]))

    data = [
    ["Metric", "Value"],
    ["Semantic Similarity", f"{similarity:.2f}"],
    ["Filler Word Ratio", f"{filler_ratio:.2f}"],
    ["Pause Ratio", f"{pause_ratio:.2f}"],
    ["Confidence (Energy)", f"{confidence:.4f}"],
    ["Final Score", f"{score}/100"],
    ["Understanding Level", level],
]

    table = Table(data, colWidths=[250, 200])

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )

    elements.append(table)

    doc.build(elements)