"""
Generate Church Discussion Guide PDF - Enhanced Visual Design
Run: python build_pdfs/generate_discussion_guide.py
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor, white
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(os.path.dirname(OUTPUT_DIR), 'church-discussion-guide.pdf')

doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch,
                        leftMargin=0.75*inch, rightMargin=0.75*inch)
story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=26, textColor=white, 
                              spaceAfter=0, alignment=TA_CENTER, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=16, textColor=HexColor('#2c5aa0'),
                                 spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica')
heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=15, textColor=white,
                                spaceAfter=0, fontName='Helvetica-Bold', alignment=TA_LEFT)
subheading_style = ParagraphStyle('SubHeading', parent=styles['Heading3'], fontSize=13, textColor=HexColor('#2c5aa0'),
                                   spaceAfter=8, spaceBefore=0, fontName='Helvetica-Bold')
body_style = ParagraphStyle('CustomBody', parent=styles['BodyText'], fontSize=11, alignment=TA_JUSTIFY, 
                             spaceAfter=10, leading=15)
question_style = ParagraphStyle('QuestionStyle', parent=styles['BodyText'], fontSize=11, textColor=HexColor('#8b4513'),
                                 spaceAfter=6, fontName='Helvetica-Bold')
box_text_style = ParagraphStyle('BoxText', parent=styles['BodyText'], fontSize=11, alignment=TA_LEFT,
                                 spaceAfter=0, leading=14)
scripture_style = ParagraphStyle('Scripture', parent=styles['BodyText'], fontSize=11, textColor=HexColor('#2c5aa0'),
                                  alignment=TA_CENTER, fontName='Helvetica-Oblique', spaceAfter=10)

def create_header_box(text):
    header = Table([[Paragraph(text, heading_style)]], colWidths=[6.5*inch])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#2c5aa0')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
    ]))
    return header

def create_key_idea_box(text):
    box = Table([[Paragraph("💡 KEY IDEA", ParagraphStyle('KeyTitle', parent=styles['Normal'], fontSize=11, 
                                                          textColor=white, fontName='Helvetica-Bold'))], 
                 [Paragraph(text, box_text_style)]],
                colWidths=[6.5*inch])
    box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#8b4513')),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#fef3c7')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))
    return box

# Title Page
story.append(Spacer(1, 0.5*inch))

header_data = [[Paragraph("THE NECESSARY EVIL<br/>DISCUSSION GUIDE", title_style)]]
header_table = Table(header_data, colWidths=[6.5*inch])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor('#2c5aa0')),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 30),
    ('BOTTOMPADDING', (0,0), (-1,-1), 30),
]))
story.append(header_table)
story.append(Spacer(1, 0.3*inch))

story.append(Paragraph("10-Session Study on AI, Faith, and Human Dignity", subtitle_style))
story.append(Spacer(1, 0.4*inch))

icon_text = "✓ Small Groups  •  ✓ Men's Ministry  •  ✓ Homeschool Co-ops"
story.append(Paragraph(icon_text, ParagraphStyle('IconStyle', parent=styles['Normal'], fontSize=12, 
                                 textColor=HexColor('#2c5aa0'), alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Spacer(1, 0.5*inch))

story.append(Paragraph("By Edward Fong", ParagraphStyle('Author', parent=styles['Normal'], fontSize=13, 
                                         alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(PageBreak())

# Introduction
story.append(create_header_box("📖 INTRODUCTION"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("This study guide is designed for church small groups, men's groups, homeschool co-ops, and Christian discussion groups.", body_style))
story.append(Paragraph("Each session includes key ideas, scripture reflection, discussion questions, and practical application.", body_style))
story.append(Paragraph("The goal is to help believers understand AI's impact on faith, family, and culture—and respond with wisdom and courage.", body_style))
story.append(PageBreak())

# Session 1
story.append(create_header_box("SESSION 1: Understanding the AI Revolution"))
story.append(Spacer(1, 0.15*inch))
story.append(create_key_idea_box("Artificial intelligence represents a major technological shift affecting work, culture, and human identity."))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("\"Be fruitful and multiply and fill the earth and subdue it...\" — Genesis 1:28", scripture_style))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. What is artificial intelligence?", body_style))
story.append(Paragraph("2. How has AI already impacted your life?", body_style))
story.append(Paragraph("3. What opportunities does AI present?", body_style))
story.append(Paragraph("4. What concerns do you have about AI?", body_style))
story.append(PageBreak())

# Session 2
story.append(create_header_box("SESSION 2: The Two Paths of AI"))
story.append(Spacer(1, 0.15*inch))
story.append(create_key_idea_box("AI can either augment human abilities or replace human dignity."))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. Where do you see AI improving life?", body_style))
story.append(Paragraph("2. Where do you see risks?", body_style))
story.append(Paragraph("3. How can Christians ensure AI serves humanity rather than replaces it?", body_style))
story.append(Paragraph("4. What does it mean to 'master' AI rather than be mastered by it?", body_style))
story.append(PageBreak())

# Session 3
story.append(create_header_box("SESSION 3: Human Identity and the Image of God"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("\"So God created man in His own image, in the image of God He created him...\" — Genesis 1:26-27", scripture_style))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. What distinguishes humans from machines?", body_style))
story.append(Paragraph("2. Why does this matter in an AI-driven world?", body_style))
story.append(Paragraph("3. How does being made in God's image shape how we use technology?", body_style))
story.append(Paragraph("4. What happens when society forgets human dignity?", body_style))
story.append(PageBreak())

# Session 4
story.append(create_header_box("SESSION 4: Cognitive and Social Impact of AI"))
story.append(Spacer(1, 0.15*inch))
story.append(create_key_idea_box("AI can weaken critical thinking and human relationships if used carelessly."))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. Could AI weaken thinking skills? How?", body_style))
story.append(Paragraph("2. How can we prevent cognitive atrophy?", body_style))
story.append(Paragraph("3. How does AI affect human relationships?", body_style))
story.append(Paragraph("4. What boundaries should families set?", body_style))
story.append(PageBreak())

# Session 5
story.append(create_header_box("SESSION 5: AI and Culture"))
story.append(Spacer(1, 0.15*inch))
story.append(create_key_idea_box("Technology shapes culture, and Christians have a responsibility to engage wisely."))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. How does technology shape culture?", body_style))
story.append(Paragraph("2. What responsibility do Christians have in shaping technology?", body_style))
story.append(Paragraph("3. How can believers influence AI development and use?", body_style))
story.append(Paragraph("4. What does faithful cultural engagement look like?", body_style))
story.append(PageBreak())

# Session 6
story.append(create_header_box("SESSION 6: AI and the Church"))
story.append(Spacer(1, 0.15*inch))
story.append(create_key_idea_box("The Church must respond to AI with wisdom, not fear or ignorance."))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. Should churches ignore AI? Why or why not?", body_style))
story.append(Paragraph("2. How could churches respond wisely to AI?", body_style))
story.append(Paragraph("3. What role should pastors play in teaching about technology?", body_style))
story.append(Paragraph("4. How can the Church protect human dignity in an AI age?", body_style))
story.append(PageBreak())

# Session 7
story.append(create_header_box("SESSION 7: Family and Technology"))
story.append(Spacer(1, 0.15*inch))
story.append(create_key_idea_box("Families must set boundaries and teach discernment around AI."))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. How should families approach AI tools?", body_style))
story.append(Paragraph("2. What boundaries should exist for children?", body_style))
story.append(Paragraph("3. How can parents teach critical thinking about technology?", body_style))
story.append(Paragraph("4. What does healthy technology use look like in a Christian home?", body_style))
story.append(PageBreak())

# Session 8
story.append(create_header_box("SESSION 8: Work and Automation"))
story.append(Spacer(1, 0.15*inch))
story.append(create_key_idea_box("AI will change careers, and Christians should prepare wisely."))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. How might AI change careers and industries?", body_style))
story.append(Paragraph("2. How should Christians prepare for these changes?", body_style))
story.append(Paragraph("3. What does faithful work look like in an automated world?", body_style))
story.append(Paragraph("4. How can believers maintain purpose and dignity in their work?", body_style))
story.append(PageBreak())

# Session 9
story.append(create_header_box("SESSION 9: Technology and Faith"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("\"Do not be conformed to this world, but be transformed by the renewal of your mind.\" — Romans 12:2", scripture_style))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. How do we guard our thinking in an AI-saturated world?", body_style))
story.append(Paragraph("2. How can technology serve faith rather than replace it?", body_style))
story.append(Paragraph("3. What does it mean to renew our minds in this context?", body_style))
story.append(Paragraph("4. How can we use AI for ministry without compromising truth?", body_style))
story.append(PageBreak())

# Session 10
story.append(create_header_box("SESSION 10: A Vision for the Future"))
story.append(Spacer(1, 0.15*inch))
story.append(create_key_idea_box("Christians must engage technology with wisdom, humility, discernment, and faith."))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("<b>Discussion Questions:</b>", question_style))
story.append(Paragraph("1. What role should Christians play in shaping technology?", body_style))
story.append(Paragraph("2. What does faithful stewardship of AI look like?", body_style))
story.append(Paragraph("3. How can we ensure technology serves human dignity and God's purposes?", body_style))
story.append(Paragraph("4. What is your personal commitment moving forward?", body_style))
story.append(PageBreak())

# Final Challenge
story.append(create_header_box("💡 FINAL CHALLENGE"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("Artificial intelligence will influence the future. Christians must engage technology with wisdom, humility, discernment, and faith.", body_style))
story.append(Paragraph("The goal is not to reject innovation. The goal is to ensure technology serves <b>human dignity and God's purposes</b>.", body_style))
story.append(Spacer(1, 0.3*inch))

# CTA Box
cta_box = Table([[Paragraph("📘 CONTINUE THE JOURNEY", ParagraphStyle('CTA', parent=styles['Normal'], fontSize=12, 
                                                                      textColor=white, fontName='Helvetica-Bold'))], 
                 [Paragraph("This guide is based on <b>The Necessary Evil</b> by Edward Fong.<br/><br/>"
                           "For more resources, visit: <b>ChristianConservativesToday.com</b>", box_text_style)]],
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
