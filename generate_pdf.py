import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class OrnamentDivider(Flowable):
    """A beautiful vintage divider with a center diamond and side dots."""
    def __init__(self, width, height=20, mini=False):
        super().__init__()
        self.width = width
        self.height = height
        self.mini = mini
        
    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(HexColor('#6E2A2A'))
        self.canv.setLineWidth(0.5)
        
        cy = self.height / 2.0
        cx = self.width / 2.0
        
        if self.mini:
            # Simple line with a center circle
            self.canv.line(cx - 80, cy, cx - 10, cy)
            self.canv.line(cx + 10, cy, cx + 80, cy)
            self.canv.setFillColor(HexColor('#6E2A2A'))
            self.canv.circle(cx, cy, 1.5, fill=True, stroke=False)
        else:
            # Full divider with diamond and dots
            self.canv.line(20, cy, cx - 20, cy)
            self.canv.line(cx + 20, cy, self.width - 20, cy)
            
            # Center diamond
            self.canv.setFillColor(HexColor('#6E2A2A'))
            p = self.canv.beginPath()
            p.moveTo(cx, cy + 4)
            p.lineTo(cx + 6, cy)
            p.lineTo(cx, cy - 4)
            p.lineTo(cx - 6, cy)
            p.close()
            self.canv.drawPath(p, fill=True, stroke=True)
            
            # Small dots on sides
            self.canv.circle(cx - 12, cy, 1.0, fill=True, stroke=False)
            self.canv.circle(cx + 12, cy, 1.0, fill=True, stroke=False)
        
        self.canv.restoreState()

def create_card(title_html, content_html, width, font_title, font_body):
    """Helper to create a beautiful card with a thin border and 3px burgundy top band."""
    style_title = ParagraphStyle(
        'CardTitle',
        fontName=font_title,
        fontSize=12,
        leading=14,
        textColor=HexColor('#6E2A2A'),
        alignment=1, # Center
        spaceAfter=6
    )
    
    style_content = ParagraphStyle(
        'CardContent',
        fontName=font_body,
        fontSize=9.5,
        leading=12,
        textColor=HexColor('#2D2525'),
        alignment=1 # Center
    )
    
    p_title = Paragraph(title_html, style_title)
    p_content = Paragraph(content_html, style_content)
    
    # Wrap in a single-column table to act as a card
    card_table = Table([[p_title], [p_content]], colWidths=[width])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#FFFFFF')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#C5A880')),
        ('LINEABOVE', (0,0), (0,0), 3.0, HexColor('#6E2A2A')), # 3px Burgundy top band
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return card_table

def build_pdf():
    # 1. Register Fonts from Windows System Fonts
    font_dir = "C:\\Windows\\Fonts"
    
    try:
        pdfmetrics.registerFont(TTFont('Garamond', os.path.join(font_dir, 'GARA.TTF')))
        pdfmetrics.registerFont(TTFont('Garamond-Bold', os.path.join(font_dir, 'GARABD.TTF')))
        pdfmetrics.registerFont(TTFont('Garamond-Italic', os.path.join(font_dir, 'GARAIT.TTF')))
        pdfmetrics.registerFont(TTFont('Gabriola', os.path.join(font_dir, 'Gabriola.ttf')))
        font_title = 'Gabriola'
        font_body = 'Garamond'
        font_body_bold = 'Garamond-Bold'
        font_body_italic = 'Garamond-Italic'
        font_card_header = 'Garamond-Bold'
    except Exception as e:
        print(f"Error loading system fonts: {e}. Falling back to standard Helvetica/Times.")
        font_title = 'Times-Bold'
        font_body = 'Times-Roman'
        font_body_bold = 'Times-Bold'
        font_body_italic = 'Times-Italic'
        font_card_header = 'Times-Bold'

    pdf_filename = "family_tree.pdf"
    
    # Setup document: A4 (595.27 x 841.89 points) with 40pt margins
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName=font_title,
        fontSize=38,
        leading=40,
        textColor=HexColor('#6E2A2A'),
        alignment=1, # Center
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName=font_body_bold,
        fontSize=18,
        leading=20,
        textColor=HexColor('#5C5252'),
        alignment=1, # Center
        spaceAfter=15
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName=font_body_bold,
        fontSize=18,
        leading=20,
        textColor=HexColor('#6E2A2A'),
        alignment=1, # Center
        spaceBefore=14,
        spaceAfter=14,
        keepWithNext=True
    )
    
    details_style = ParagraphStyle(
        'DetailsText',
        parent=styles['Normal'],
        fontName=font_body,
        fontSize=9.5,
        leading=12,
        textColor=HexColor('#5C5252'),
        alignment=1,
        spaceAfter=4
    )
    
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName=font_body_italic,
        fontSize=10,
        leading=12,
        textColor=HexColor('#6E2A2A'),
        alignment=1,
        spaceBefore=4,
        spaceAfter=15
    )

    story = []
    
    # ==========================================
    # PAGE 1: TITLE & PHOTO & PARENTS
    # ==========================================
    story.append(Spacer(1, 35)) # 100px (75pt) total top margin (40pt topMargin + 35pt spacer)
    story.append(Paragraph("Familienstammbaum", title_style))
    story.append(Paragraph("Baumhöver / Rohlmann", subtitle_style))
    
    # Group Photo
    photo_width = 420
    photo_height = 286
    photo_img = Image('group-photo.jpg', width=photo_width, height=photo_height)
    photo_table = Table([[photo_img]], colWidths=[photo_width + 12], rowHeights=[photo_height + 12])
    photo_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, HexColor('#C5A880')),
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#FFFFFF')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    
    story.append(photo_table)
    story.append(Paragraph("Von links nach rechts: Mia Mönkehues, Bernhard Rohlmann, Anni Schmidt, Alfons Baumhöver, Cilly Bohnen", details_style))
    story.append(Paragraph("Die Geschwister Baumhöver und Rohlmann", caption_style))
    
    story.append(OrnamentDivider(480, 20))
    story.append(Spacer(1, 5))
    
    story.append(Paragraph("Unsere Eltern", section_heading))
    
    # Parents side-by-side
    card_father = create_card("Hubert Baumhöver", "geb. 05.02.1906<br/>gest. 30.03.1944<br/><i>(im Krieg in Polen gefallen)</i>", 220, font_card_header, font_body)
    card_mother = create_card("Maria Baumhöver, <font size=10>geb. Kohues</font>", "geb. 28.12.1908<br/>gest. 19.05.1994", 220, font_card_header, font_body)
    
    parent_table = Table([[card_father, card_mother]], colWidths=[240, 240])
    parent_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(parent_table)
    
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 2: SIBLINGS / CHILDREN (BAUMHÖVER)
    # ==========================================
    story.append(Spacer(1, 35)) # 100px (75pt) total top margin (40pt topMargin + 35pt spacer)
    story.append(Paragraph("Familie Baumhöver", section_heading))
    
    # Parents Row
    card_father_p2 = create_card("Hubert Baumhöver", "geb. 05.02.1906<br/>gest. 30.03.1944<br/><i>(im Krieg in Polen gefallen)</i>", 220, font_card_header, font_body)
    card_mother_p2 = create_card("Maria Baumhöver, <font size=10>geb. Kohues</font>", "geb. 28.12.1908<br/>gest. 19.05.1994", 220, font_card_header, font_body)
    
    parent_table_p2 = Table([[card_father_p2, card_mother_p2]], colWidths=[240, 240])
    parent_table_p2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(parent_table_p2)
    
    story.append(OrnamentDivider(480, 20, mini=True))
    
    # Children listed vertically in the center
    child1 = create_card("Anni Baumhöver", "geb. 26.07.1939<br/>verh. mit Franz Schmidt<br/><font size=8.5 color='#5C5252'>(* 16.11.1930 &dagger; 03.12.2023)</font>", 300, font_card_header, font_body)
    child2 = create_card("Cilly (Cecilia) Baumhöver", "geb. 10.09.1940<br/>verh. mit Helmut Bohnen<br/><font size=8.5 color='#5C5252'>(* 31.12.???? &dagger;)</font>", 300, font_card_header, font_body)
    child3 = create_card("Alfons Baumhöver", "geb. 13.05.1943<br/>gest. 23.09.2025<br/>verh. mit Anne Bauersachs", 300, font_card_header, font_body)
    
    for child in [child1, child2, child3]:
        # Center table
        wrapper = Table([[child]], colWidths=[480])
        wrapper.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(wrapper)
        
    story.append(PageBreak())
    
    # ==========================================
    # PAGE 3: SIBLINGS / CHILDREN (ROHLMANN)
    # ==========================================
    story.append(Spacer(1, 35)) # 100px (75pt) total top margin (40pt topMargin + 35pt spacer)
    story.append(Paragraph("Familie Rohlmann", section_heading))
    
    # Parents Row
    card_father_p3 = create_card("Heinrich Rohlmann", "geb. um 1900<br/>gest. um 1981", 220, font_card_header, font_body)
    card_mother_p3 = create_card("Maria Rohlmann, <font size=10>geb. Kohues</font>", "geb. 28.12.1908<br/>gest. 19.05.1994<br/><i>(verwitwete Baumhöver)</i>", 220, font_card_header, font_body)
    
    parent_table_p3 = Table([[card_father_p3, card_mother_p3]], colWidths=[240, 240])
    parent_table_p3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(parent_table_p3)
    
    story.append(OrnamentDivider(480, 20, mini=True))
    
    # Children listed vertically in the center
    child4 = create_card("Bernhard Rohlmann", "geb. 16.10.1948<br/>verh. mit Hanni Wolke", 300, font_card_header, font_body)
    child5 = create_card("Mia (Maria) Rohlmann", "geb. 05.02.1950<br/>verh. mit Friedel Mönkehues", 300, font_card_header, font_body)
    
    for child in [child4, child5]:
        wrapper = Table([[child]], colWidths=[480])
        wrapper.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(wrapper)
        
    # Canvas decorations for printing (Background: white, Page number)
    def draw_decorations(canvas, doc):
        canvas.saveState()
        
        # Background: pure white
        canvas.setFillColor(HexColor('#FFFFFF'))
        canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=True, stroke=False)
        
        # Page numbers
        canvas.setFont(font_body_italic, 9)
        canvas.setFillColor(HexColor('#6E2A2A'))
        page_num = canvas.getPageNumber()
        canvas.drawCentredString(doc.pagesize[0] / 2.0, 32, f"Seite {page_num}")
        
        canvas.restoreState()
        
    doc.build(story, onFirstPage=draw_decorations, onLaterPages=draw_decorations)
    print("PDF successfully generated.")

if __name__ == '__main__':
    build_pdf()
