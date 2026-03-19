"""
Generate Christian AI Survival Guide PDF - Enhanced Visual Design
Run: python build_pdfs/generate_survival_guide.py
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor, white
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(os.path.dirname(OUTPUT_DIR), 'christian-ai-survival-guide.pdf')

doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch,
                        leftMargin=0.75*inch, rightMargin=0.75*inch)
story = []
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=26, textColor=white, 
                              spaceAfter=0, alignment=TA_CENTER, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=16, textColor=HexColor('#15803d'),
                                 spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica')
heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=15, textColor=white,
                                spaceAfter=0, fontName='Helvetica-Bold', alignment=TA_LEFT)
subheading_style = ParagraphStyle('SubHeading', parent=styles['Heading3'], fontSize=14, textColor=HexColor('#16a34a'),
                                   spaceAfter=8, spaceBefore=0, fontName='Helvetica-Bold')
body_style = ParagraphStyle('CustomBody', parent=styles['BodyText'], fontSize=11, alignment=TA_JUSTIFY, 
                             spaceAfter=10, leading=15)
action_style = ParagraphStyle('ActionStyle', parent=styles['BodyText'], fontSize=12, textColor=white,
                               spaceAfter=0, fontName='Helvetica-Bold', alignment=TA_LEFT)
box_text_style = ParagraphStyle('BoxText', parent=styles['BodyText'], fontSize=11, alignment=TA_LEFT,
                                 spaceAfter=0, leading=14)
scripture_style = ParagraphStyle('Scripture', parent=styles['BodyText'], fontSize=11, textColor=HexColor('#15803d'),
                                  alignment=TA_CENTER, fontName='Helvetica-Oblique', spaceAfter=10)

def create_header_box(text):
    """Create a green header box for section titles"""
    header = Table([[Paragraph(text, heading_style)]], colWidths=[6.5*inch])
    header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#16a34a')),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))
    return header

def create_action_box(text):
    """Create an action step box"""
    action = Table([[Paragraph("✓ ACTION STEP", action_style)], 
                    [Paragraph(text, box_text_style)]],
                   colWidths=[6.5*inch])
    action.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#15803d')),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#f0fdf4')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))
    return action

def create_info_box(title, content):
    """Create an info box with title and content"""
    info = Table([[Paragraph(title, action_style)], 
                  [Paragraph(content, box_text_style)]],
                 colWidths=[6.5*inch])
    info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#2c5aa0')),
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#eff6ff')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))
    return info

# Title Page
story.append(Spacer(1, 0.5*inch))

header_data = [[Paragraph("THE CHRISTIAN AI<br/>SURVIVAL GUIDE", title_style)]]
header_table = Table(header_data, colWidths=[6.5*inch])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor('#16a34a')),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 30),
    ('BOTTOMPADDING', (0,0), (-1,-1), 30),
]))
story.append(header_table)
story.append(Spacer(1, 0.3*inch))

story.append(Paragraph("7 Safeguards for Using Artificial Intelligence<br/>Without Losing Your Soul", subtitle_style))
story.append(Spacer(1, 0.4*inch))

icon_text = "✓ Protect Your Mind  •  ✓ Guard Your Family  •  ✓ Honor God"
story.append(Paragraph(icon_text, ParagraphStyle('IconStyle', parent=styles['Normal'], fontSize=12, 
                                 textColor=HexColor('#15803d'), alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Spacer(1, 0.5*inch))

story.append(Paragraph("By Edward Fong", ParagraphStyle('Author', parent=styles['Normal'], fontSize=13, 
                                         alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Paragraph("Author of <i>The Necessary Evil</i>", ParagraphStyle('BookRef', parent=styles['Normal'], 
                                                              fontSize=11, alignment=TA_CENTER)))
story.append(PageBreak())

# Introduction
story.append(create_header_box("📖 INTRODUCTION"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("Artificial Intelligence is no longer a distant technology. It is already embedded in search engines, "
                       "social media algorithms, workplace automation, creative tools, education systems, and government systems.", body_style))
story.append(Paragraph("The question is not whether Christians will interact with AI. The question is <b>how we will interact with it</b>.", body_style))
story.append(Paragraph("AI can be a powerful tool for productivity and creativity. But if used without discernment, it can also "
                       "erode critical thinking, weaken relationships, and distort truth.", body_style))
story.append(Paragraph("This guide gives you <b>seven practical safeguards</b> for navigating the AI age with wisdom and faith.", body_style))
story.append(PageBreak())

# Safeguard 1
story.append(create_header_box("⚡ SAFEGUARD 1"))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Remember What AI Is — and What It Is Not", subheading_style))
story.append(Paragraph("AI is not a mind. AI is not conscious. AI is not a moral authority.", body_style))
story.append(Paragraph("AI is <b>pattern prediction</b> based on training data. It does not understand truth, morality, or spiritual reality.", body_style))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("\"So God created man in His own image...\" — Genesis 1:26-27", scripture_style))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Scripture reminds us that humans alone are created in the <b>image of God</b>. "
                       "Machines can process information, but they cannot possess a soul or moral conscience.", body_style))
story.append(Paragraph("When AI becomes an authority instead of a tool, we risk placing technology where only God belongs.", body_style))
story.append(Spacer(1, 0.15*inch))
story.append(create_action_box("Ask yourself: Am I using AI as a tool? Or am I letting it shape my thinking?"))
story.append(PageBreak())

# Safeguard 2
story.append(create_header_box("⚡ SAFEGUARD 2"))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Never Replace Human Discernment", subheading_style))
story.append(Paragraph("AI can summarize information. AI can generate ideas. AI can assist research. "
                       "But AI <b>cannot discern truth from falsehood with moral wisdom</b>.", body_style))
story.append(Paragraph("AI systems often reflect the assumptions and biases of the institutions that train them. "
                       "Because of this, Christians must practice discernment.", body_style))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("\"Test everything; hold fast what is good.\" — 1 Thessalonians 5:21", scripture_style))
story.append(Spacer(1, 0.15*inch))
story.append(create_action_box("When using AI: verify important claims, compare multiple sources, apply biblical discernment."))
story.append(PageBreak())

# Safeguard 3
story.append(create_header_box("⚡ SAFEGUARD 3"))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Protect Your Mind From Cognitive Atrophy", subheading_style))
story.append(Paragraph("One of the hidden dangers of AI is <b>mental outsourcing</b>. When AI writes our emails, summarizes our reading, "
                       "answers our questions, and makes our decisions, our own reasoning muscles weaken.", body_style))
story.append(Paragraph("Just as unused muscles atrophy, unused thinking skills fade.", body_style))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("\"Do not be conformed to this world, but be transformed by the renewal of your mind.\" — Romans 12:2", scripture_style))
story.append(Spacer(1, 0.15*inch))
story.append(create_action_box("Before asking AI, try solving the problem yourself first."))
story.append(PageBreak())

# Safeguard 4
story.append(create_header_box("⚡ SAFEGUARD 4"))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Guard Your Relationships", subheading_style))
story.append(Paragraph("AI can simulate conversation. But it cannot replace real friendship, community, church fellowship, or family relationships.", body_style))
story.append(Paragraph("Human relationships require effort, patience, and empathy. The Bible repeatedly calls believers into <b>real community</b>.", body_style))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("\"Let us consider how to stir up one another to love and good works.\" — Hebrews 10:24", scripture_style))
story.append(Paragraph("AI should never become a substitute for human connection.", body_style))
story.append(Spacer(1, 0.15*inch))
story.append(create_action_box("Set boundaries for AI usage in social life. Prioritize face-to-face relationships."))
story.append(PageBreak())

# Safeguard 5
story.append(create_header_box("⚡ SAFEGUARD 5"))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Protect Children From AI Influence", subheading_style))
story.append(Paragraph("Children are particularly vulnerable to AI systems. AI chatbots can simulate friendship, influence thinking, and shape beliefs.", body_style))
story.append(Paragraph("Parents must take an active role in guiding how children interact with technology.", body_style))
story.append(Spacer(1, 0.15*inch))
story.append(create_info_box("⚠ PARENT WARNING", 
                             "AI systems can give incorrect information confidently, reflect biased training data, "
                             "simulate emotional connection, and influence beliefs subtly over time."))
story.append(Spacer(1, 0.15*inch))
story.append(create_action_box("Parents should: supervise AI usage, discuss technology openly, and teach critical thinking."))
story.append(PageBreak())

# Safeguard 6
story.append(create_header_box("⚡ SAFEGUARD 6"))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Use AI for Stewardship, Not Idolatry", subheading_style))
story.append(Paragraph("Technology can easily become an idol. Idolatry occurs when created things replace the Creator in our priorities.", body_style))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("\"They exchanged the truth about God for a lie and worshiped the creature rather than the Creator.\" — Romans 1:25", scripture_style))
story.append(Paragraph("AI should serve human flourishing—not redefine humanity. When used wisely, AI can assist learning, "
                       "support creativity, reduce repetitive work, and amplify ministry.", body_style))
story.append(Paragraph("But it must remain a <b>servant, not a master</b>.", body_style))
story.append(PageBreak())

# Safeguard 7
story.append(create_header_box("⚡ SAFEGUARD 7"))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Anchor Your Identity in God", subheading_style))
story.append(Paragraph("The greatest protection against technological confusion is spiritual clarity.", body_style))
story.append(Paragraph("Your value is not determined by productivity, intelligence, output, or technological capability. "
                       "Your value comes from being created in the <b>image of God</b>.", body_style))
story.append(Paragraph("AI may transform society. But it cannot change the foundation of human dignity.", body_style))
story.append(Spacer(1, 0.15*inch))
story.append(create_info_box("✓ REMEMBER", 
                             "You are not data. You are not a profile. You are not a user. "
                             "You are a child of God, created in His image, with eternal value."))
story.append(PageBreak())

# Final Thoughts
story.append(create_header_box("💡 FINAL THOUGHTS"))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph("Artificial intelligence will shape the future. Christians must respond with wisdom rather than fear.", body_style))
story.append(Paragraph("The goal is not to reject technology. The goal is to <b>master it responsibly</b>.", body_style))
story.append(Paragraph("AI is a powerful tool that must remain under human stewardship rather than replacing human judgment or moral responsibility.", body_style))
story.append(Paragraph("The future will belong to those who combine faith, discernment, wisdom, and technological literacy.", body_style))
story.append(Spacer(1, 0.3*inch))

# CTA Box
cta_box = Table([[Paragraph("📘 WANT TO GO DEEPER?", action_style)], 
                 [Paragraph("This guide is based on the book <b>The Necessary Evil</b> by Edward Fong.<br/><br/>"
                           "Inside the book you'll discover: The two possible paths AI can take, the ideology behind transhumanism, "
                           "the cultural consequences of unchecked AI, and practical strategies for families, churches, and professionals.<br/><br/>"
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
