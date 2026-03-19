"""
Generate AI Parent Guide PDF - Enhanced Visual Design
Run: python build_pdfs/generate_parent_guide.py
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor, white
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(os.path.dirname(OUTPUT_DIR), 'ai-parent-guide.pdf')

doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch,
                        leftMargin=0.75*inch, rightMargin=0.75*inch)
story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=26, textColor=white, 
                              spaceAfter=0, alignment=TA_CENTER, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=16, textColor=HexColor('#991b1b'),
                                 spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica')
heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=15, textColor=white,
                                spaceAfter=0, fontName='Helvetica-Bold', alignment=TA_LEFT)
subheading_style = ParagraphStyle('SubHeading', parent=styles['Heading3'], fontSize=14, textColor=HexColor('#dc2626'),
                                   spaceAfter=8, spaceBefore=0, fontName='Helvetica-Bold')
body_style = ParagraphStyle('CustomBody', parent=styles['BodyText'], fontSize=11, alignment=TA_JUSTIFY, 
                             spaceAfter=10, leading=15)
box_text_style = ParagraphStyle('BoxText', parent=styles['BodyText'], fontSize=11, alignment=TA_LEFT,
                                 spaceAfter=0, leading=14)
scripture_style = ParagraphStyle('Scripture', parent=styles['BodyText'], fontSize=11, textColor=HexColor('#991b1b'),
                                  alignment=TA_CENTER, fontName='Helvetica-Oblique', spaceAfter=10)

def create_header_box(text):
    header = Table([[Paragraph(text, heading_style)]], colWidths=[6.5*inch])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#dc2626')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
    ]))
    return header

def create_warning_box(title, text):
    box = Table([[Paragraph(title, ParagraphStyle('WarningTitle', parent=styles['Normal'], fontSize=12, 
                                                   textColor=white, fontName='Helvetica-Bold'))], 
                 [Paragraph(text, box_text_style)]],
                colWidths=[6.5*inch])
    box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#991b1b')),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#fee2e2')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))
    return box

def create_checklist_box(title, items):
    content = "<br/>".join([f"✓ {item}" for item in items])
    box = Table([[Paragraph(title, ParagraphStyle('CheckTitle', parent=styles['Normal'], fontSize=12, 
                                                   textColor=white, fontName='Helvetica-Bold'))], 
                 [Paragraph(content, box_text_style)]],
                colWidths=[6.5*inch])
    box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#16a34a')),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#f0fdf4')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))
    return box

# Title Page
story.append(Spacer(1, 0.5*inch))

header_data = [[Paragraph("AI PARENT GUIDE", title_style)]]
header_table = Table(header_data, colWidths=[6.5*inch])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor('#dc2626')),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 30),
    ('BOTTOMPADDING', (0,0), (-1,-1), 30),
]))
story.append(header_table)
story.append(Spacer(1, 0.3*inch))

story.append(Paragraph("How to Protect Your Children<br/>in an AI-Driven World", subtitle_style))
story.append(Spacer(1, 0.4*inch))

icon_text = "⚠ Essential Reading for Every Parent"
story.append(Paragraph(icon_text, ParagraphStyle('IconStyle', parent=styles['Normal'], fontSize=13, 
                                 textColor=HexColor('#991b1b'), alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Spacer(1, 0.5*inch))

story.append(Paragraph("By Edward Fong", ParagraphStyle('Author', parent=styles['Normal'], fontSize=13, 
                                         alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Paragraph("Author of <i>The Necessary Evil</i>", ParagraphStyle('BookRef', parent=styles['Normal'], 
                                                              fontSize=11, alignment=TA_CENTER)))
story.append(PageBreak())

# Message to Parents
story.append(create_header_box("⚠ A MESSAGE TO PARENTS"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("Artificial Intelligence is not coming. <b>It is already here.</b>", body_style))
story.append(Paragraph("Your children are interacting with it at school, on their phones, through apps and chatbots, and through social media algorithms.", body_style))
story.append(Paragraph("Most parents are <b>completely unprepared</b>.", body_style))
story.append(Spacer(1, 0.15*inch))
story.append(create_warning_box("⚠ THE REALITY", 
                                "This guide will help you understand the real risks, set clear boundaries, protect your child's mind and identity, "
                                "and use AI wisely instead of fearfully."))
story.append(PageBreak())

# What AI Really Is
story.append(create_header_box("🤖 WHAT AI REALLY IS"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("AI is not intelligent in the way humans are. It is pattern recognition, probability prediction, and trained on massive datasets.", body_style))
story.append(Paragraph("It does <b>not</b> understand truth, have a conscience, or possess a soul.", body_style))
story.append(Paragraph("It predicts what sounds right—not what <i>is</i> right.", body_style))
story.append(Spacer(1, 0.15*inch))
story.append(create_warning_box("⚠ PARENT WARNING", 
                                "AI systems can give incorrect information confidently, reflect biased training data, "
                                "simulate emotional connection, and influence beliefs subtly over time. Your child may trust it more than they should."))
story.append(PageBreak())

# The 7 Safeguards
story.append(create_header_box("🛡 THE 7 AI SAFEGUARDS FOR PARENTS"))
story.append(Spacer(1, 0.2*inch))

# Safeguard 1
story.append(Paragraph("1. Establish Clear Boundaries", subheading_style))
story.append(Paragraph("Children should not have unrestricted AI access.", body_style))
story.append(Spacer(1, 0.1*inch))
story.append(create_checklist_box("SET THESE RULES", [
    "No AI use without parental awareness",
    "No AI during homework unless supervised",
    "No AI in private or hidden environments"
]))
story.append(PageBreak())

# Safeguard 2
story.append(Paragraph("2. Teach Critical Thinking Early", subheading_style))
story.append(Paragraph("Train your child to ask: 'Is this true?' 'Where did this come from?' 'Can I verify this?'", body_style))
story.append(Paragraph("AI should assist thinking—<b>not replace it</b>.", body_style))
story.append(PageBreak())

# Safeguard 3
story.append(Paragraph("3. Keep AI Use Visible", subheading_style))
story.append(Paragraph("AI should be used in shared spaces, on family devices (when possible), and with occasional review.", body_style))
story.append(Spacer(1, 0.15*inch))
story.append(create_warning_box("⚠ REMEMBER", "Hidden use = unmonitored influence."))
story.append(PageBreak())

# Safeguard 4
story.append(Paragraph("4. Protect Emotional Development", subheading_style))
story.append(Paragraph("AI chatbots can simulate friendship, empathy, and understanding. But they are not real relationships.", body_style))
story.append(Paragraph("<b>Children must not replace human connection with AI.</b>", body_style))
story.append(PageBreak())

# Safeguard 5
story.append(Paragraph("5. Guard Against Identity Confusion", subheading_style))
story.append(Paragraph("Your child's identity must come from God, family, and truth—NOT from technology, algorithms, or online validation.", body_style))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("\"So God created man in His own image...\" — Genesis 1:27", scripture_style))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Your child is not data, not a profile, not a user. They are created in the image of God.", body_style))
story.append(PageBreak())

# Safeguard 6
story.append(Paragraph("6. Set Family AI Rules", subheading_style))
story.append(Paragraph("Create a simple household policy:", body_style))
story.append(Spacer(1, 0.15*inch))

# Family Agreement Box
agreement_items = [
    "We use AI as a tool—not a replacement for thinking",
    "We verify what AI tells us",
    "We prioritize real relationships",
    "We do not share personal information",
    "We honor God in how we use technology"
]
agreement_box = Table([[Paragraph("📋 OUR FAMILY AI AGREEMENT", ParagraphStyle('AgreementTitle', parent=styles['Normal'], 
                                                                                fontSize=12, textColor=white, fontName='Helvetica-Bold'))], 
                       [Paragraph("<br/>".join(agreement_items) + "<br/><br/><i>(Sign and post in your home)</i>", box_text_style)]],
                      colWidths=[6.5*inch])
agreement_box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor('#2c5aa0')),
    ('BACKGROUND', (0,1), (-1,-1), HexColor('#eff6ff')),
    ('TOPPADDING', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING', (0,0), (-1,-1), 15),
    ('RIGHTPADDING', (0,0), (-1,-1), 15),
]))
story.append(agreement_box)
story.append(PageBreak())

# Safeguard 7
story.append(Paragraph("7. Model the Behavior Yourself", subheading_style))
story.append(Paragraph("Children follow what you do—not what you say.", body_style))
story.append(Paragraph("Ask yourself: Do I rely on AI too much? Am I thinking critically? Am I present with my family?", body_style))
story.append(Paragraph("<b>You are the example.</b>", body_style))
story.append(PageBreak())

# The Hidden Danger
story.append(create_header_box("⚠ THE HIDDEN DANGER MOST PARENTS MISS"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("AI doesn't need to 'teach' your child directly. It can influence them through tone, framing, repetition, and subtle suggestions.", body_style))
story.append(Paragraph("Over time, this shapes beliefs, worldview, and values.", body_style))
story.append(PageBreak())

# Daily Checklist
story.append(create_header_box("✓ PRACTICAL DAILY CHECKLIST"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("Each day ask:", body_style))
story.append(Spacer(1, 0.1*inch))
story.append(create_checklist_box("DAILY QUESTIONS", [
    "Did my child use AI today?",
    "Do I know how they used it?",
    "Did we have real conversation time?",
    "Are they thinking independently?"
]))
story.append(PageBreak())

# Final Encouragement
story.append(create_header_box("💪 FINAL ENCOURAGEMENT"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("You are not powerless in this. God entrusted your children to you—not to technology.", body_style))
story.append(Paragraph("AI may shape the world... But <b>you shape your child</b>.", body_style))
story.append(Spacer(1, 0.3*inch))

# CTA Box
cta_box = Table([[Paragraph("📘 WANT TO GO DEEPER?", ParagraphStyle('CTA', parent=styles['Normal'], fontSize=12, 
                                                                     textColor=white, fontName='Helvetica-Bold'))], 
                 [Paragraph("This guide is based on <b>The Necessary Evil</b> by Edward Fong.<br/><br/>"
                           "Inside the book: The real dangers of AI, the two paths of the future, how families and churches must respond, "
                           "and practical strategies for everyday life.<br/><br/>"
                           "Visit: <b>ChristianConservativesToday.com</b>", box_text_style)]],
                colWidths=[6.5*inch])
cta_box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), HexColor('#d4af37')),
    ('BACKGROUND', (0,1), (-1,-1), HexColor('#fffbeb')),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('LEFTPADDING', (0,0), (-1,-1), 15),
    ('RIGHTPADDING', (0,0), (-1,-1), 15),
]))
story.append(cta_box)

doc.build(story)
print(f"Generated: {OUTPUT_FILE}")
