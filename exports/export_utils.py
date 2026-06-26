import pandas as pd
import io
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.lib.colors import black, white, HexColor
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Assuming RADAR_BENCHMARKS is needed for some formatting within PDF, if not, can be removed
# This import will only be used if REPORTLAB_AVAILABLE is True and within the export_comparison_pdf function
from services.chart_service import RADAR_BENCHMARKS
from ai.scouting_report import generate_scouting_report # To reuse the existing report logic

def _safe_value(value, default="N/A"):
    """Safely return a string representation of a value, handling None/NaN."""
    if pd.isna(value) or value is None or str(value).strip() == "":
        return default
    return str(value)

def export_comparison_csv(df: pd.DataFrame) -> bytes:
    """
    Generates a CSV file for player comparison data.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing player comparison statistics.

    Returns:
    --------
    bytes
        CSV content encoded as bytes.
    """
    # Define the columns to export and their display names
    export_columns = {
        "player_name": "Player Name",
        "sporta_score": "SPORTA Score",
        "goals": "Goals",
        "shots": "Shots",
        "total_xg": "xG",
        "assists": "Assists",
        "passes": "Passes",
        "dribbles": "Dribbles",
        "carries": "Carries",
        "recoveries": "Recoveries",
        "pressures": "Pressures",
        "tackles": "Tackles",
        "interceptions": "Interceptions",
    }

    # Ensure all required columns exist, fill missing with NaN
    export_df = pd.DataFrame(columns=export_columns.keys())
    for col in export_columns.keys():
        if col in df.columns:
            export_df[col] = df[col]
        else:
            export_df[col] = pd.NA
    
    # Rename columns for display and handle missing values
    export_df = export_df.rename(columns=export_columns)
    export_df = export_df.fillna("N/A")

    csv_buffer = io.StringIO()
    export_df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue().encode("utf-8")

def export_comparison_pdf(player1_profile: dict, player2_profile: dict, 
                          player1_stats: pd.Series, player2_stats: pd.Series) -> bytes | None:
    """
    Generates a PDF report for player comparison, including KPI summary and AI scouting report.

    Parameters:
    -----------
    player1_profile : dict
        Player 1\'s profile data.
    player2_profile : dict
        Player 2\'s profile data.
    player1_stats : pd.Series
        Player 1\'s detailed statistics.
    player2_stats : pd.Series
        Player 2\'s detailed statistics.

    Returns:
    --------
    bytes or None
        PDF content encoded as bytes, or None if ReportLab is not available.
    """
    if not REPORTLAB_AVAILABLE:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                            rightMargin=inch/2, leftMargin=inch/2,
                            topMargin=inch/2, bottomMargin=inch/2)
    styles = getSampleStyleSheet()
    
    # Custom styles for dark theme
    styles.add(ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=24, leading=28, alignment=TA_CENTER, textColor=HexColor('#F1F5F9')))
    styles.add(ParagraphStyle(name='SubtitleStyle', fontName='Helvetica', fontSize=14, leading=18, alignment=TA_CENTER, textColor=HexColor('#94A3B8')))
    styles.add(ParagraphStyle(name='H2Style', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=HexColor('#F1F5F9'), spaceBefore=12, spaceAfter=6)) 
    styles.add(ParagraphStyle(name='H3Style', fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=HexColor('#E2E8F0'), spaceBefore=8, spaceAfter=4))
    styles.add(ParagraphStyle(name='NormalWhite', fontName='Helvetica', fontSize=10, leading=12, textColor=HexColor('#E2E8F0')))
    styles.add(ParagraphStyle(name='NormalGrey', fontName='Helvetica', fontSize=10, leading=12, textColor=HexColor('#94A3B8')))
    styles.add(ParagraphStyle(name='ListItem', fontName='Helvetica', fontSize=10, leading=14, textColor=HexColor('#E2E8F0'), leftIndent=20))
    styles.add(ParagraphStyle(name='FooterStyle', fontName='Helvetica', fontSize=9, alignment=TA_CENTER, textColor=HexColor('#64748B'), spaceBefore=20))

    story = []

    # Header
    story.append(Paragraph("SPORTA VISTA PRO", styles['SubtitleStyle']))
    story.append(Paragraph("Player Comparison Report", styles['TitleStyle']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['NormalGrey']))
    story.append(Spacer(1, 0.2 * inch))

    # Compared Players
    p1_name = _safe_value(player1_profile.get("player_name", "Player 1"))
    p2_name = _safe_value(player2_profile.get("player_name", "Player 2"))
    story.append(Paragraph("Compared Players", styles['H2Style']))
    story.append(Paragraph(f"<b>Player 1:</b> {p1_name}", styles['NormalWhite']))
    story.append(Paragraph(f"<b>Player 2:</b> {p2_name}", styles['NormalWhite']))
    story.append(Spacer(1, 0.2 * inch))

    # KPI Summary
    story.append(Paragraph("KPI Summary", styles['H2Style']))
    kpi_data = [
        ["Metric", p1_name, p2_name],
        ["SPORTA Score", _safe_value(player1_stats.get("sporta_score")), _safe_value(player2_stats.get("sporta_score"))],
        ["Goals", _safe_value(player1_stats.get("goals")), _safe_value(player2_stats.get("goals"))],
        ["xG", _safe_value(player1_stats.get("total_xg")), _safe_value(player2_stats.get("total_xg"))],
        ["Passes", _safe_value(player1_stats.get("passes")), _safe_value(player2_stats.get("passes"))],
        ["Dribbles", _safe_value(player1_stats.get("dribbles")), _safe_value(player2_stats.get("dribbles"))],
        ["Recoveries", _safe_value(player1_stats.get("recoveries")), _safe_value(player2_stats.get("recoveries"))],
        ["Pressures", _safe_value(player1_stats.get("pressures")), _safe_value(player2_stats.get("pressures"))],
    ]
    kpi_table = Table(kpi_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#F1F5F9')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#334155')),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#0F172A')),
        ('TEXTCOLOR', (0,1), (-1,-1), HexColor('#E2E8F0')),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.2 * inch))

    # AI Scouting Report (reuse logic from ai/scouting_report.py)
    ai_report = generate_scouting_report(player1_stats, player2_stats)
    story.append(Paragraph("AI Scouting Report", styles['H2Style']))
    
    def add_ai_section(title, content, style):
        story.append(Paragraph(f"<b>{title}:</b>", styles['H3Style']))
        if isinstance(content, list):
            if content:
                for item in content:
                    story.append(Paragraph(item, styles['ListItem']))
            else:
                story.append(Paragraph("N/A", style))
        else:
            story.append(Paragraph(content, style))
        story.append(Spacer(1, 0.05 * inch))

    add_ai_section("Best Attacker", ai_report["best_attacker"], styles['NormalWhite'])
    add_ai_section("Best Creator", ai_report["best_creator"], styles['NormalWhite'])
    add_ai_section("Best Ball Carrier", ai_report["best_ball_carrier"], styles['NormalWhite'])
    add_ai_section("Best Defender", ai_report["best_defender"], styles['NormalWhite'])
    add_ai_section(f"Key Strengths ({p1_name})", ai_report["strengths_player1"], styles['NormalWhite'])
    add_ai_section(f"Key Weaknesses ({p1_name})", ai_report["weaknesses_player1"], styles['NormalWhite'])
    add_ai_section(f"Key Strengths ({p2_name})", ai_report["strengths_player2"], styles['NormalWhite'])
    add_ai_section(f"Key Weaknesses ({p2_name})", ai_report["weaknesses_player2"], styles['NormalWhite'])
    add_ai_section("Tactical Recommendation", ai_report["tactical_recommendation"], styles['NormalWhite'])
    add_ai_section("Overall Verdict", ai_report["overall_verdict"], styles['NormalWhite'])
    story.append(Spacer(1, 0.2 * inch))

    # Footer
    story.append(Paragraph("Generated by SPORTA VISTA PRO.", styles['FooterStyle']))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def export_ai_report_text(report_dict: dict, player1_name: str, player2_name: str) -> str:
    """
    Formats the AI scouting report dictionary into a human-readable string.
    """
    report_text = f"# SPORTA VISTA PRO Scouting Report - {player1_name} vs {player2_name}\n\n"
    report_text += f"## ⚽ Best Attacker\n{report_dict.get('best_attacker', 'N/A')}\n\n"
    report_text += f"## 🎯 Best Creator\n{report_dict.get('best_creator', 'N/A')}\n\n"
    report_text += f"## 👟 Best Ball Carrier\n{report_dict.get('best_ball_carrier', 'N/A')}\n\n"
    report_text += f"## 🛡️ Best Defender\n{report_dict.get('best_defender', 'N/A')}\n\n"
    
    report_text += f"## 💪 Key Strengths ({player1_name})\n"
    if report_dict.get('strengths_player1'):
        report_text += "\n".join([f"- {s}" for s in report_dict['strengths_player1']]) + "\n\n"
    else:
        report_text += "- N/A\n\n"

    report_text += f"## ⚠️ Key Weaknesses ({player1_name})\n"
    if report_dict.get('weaknesses_player1'):
        report_text += "\n".join([f"- {w}" for w in report_dict['weaknesses_player1']]) + "\n\n"
    else:
        report_text += "- N/A\n\n"

    report_text += f"## 💪 Key Strengths ({player2_name})\n"
    if report_dict.get('strengths_player2'):
        report_text += "\n".join([f"- {s}" for s in report_dict['strengths_player2']]) + "\n\n"
    else:
        report_text += "- N/A\n\n"

    report_text += f"## ⚠️ Key Weaknesses ({player2_name})\n"
    if report_dict.get('weaknesses_player2'):
        report_text += "\n".join([f"- {w}" for w in report_dict['weaknesses_player2']]) + "\n\n"
    else:
        report_text += "- N/A\n\n"

    report_text += f"## 🧠 Tactical Recommendation\n{report_dict.get('tactical_recommendation', 'N/A')}\n\n"
    report_text += f"## 🏆 Overall Verdict\n{report_dict.get('overall_verdict', 'N/A')}\n"

    return report_text
