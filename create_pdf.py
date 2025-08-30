#!/usr/bin/env python3
"""
Convert Markdown documentation to PDF with proper formatting and visual diagrams.
"""

import os
import re
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black, darkblue, darkgreen, red, orange
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.graphics.shapes import Drawing, Line, Circle, Rect, String
from reportlab.graphics import renderPDF
from io import BytesIO
import markdown

class NumberedCanvas(canvas.Canvas):
    """Custom canvas for page numbers and headers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for (page_num, page_state) in enumerate(self._saved_page_states):
            self.__dict__.update(page_state)
            self.draw_page_number(page_num + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_num, total_pages):
        width, height = letter
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        
        # Page number at bottom center
        self.drawCentredText(width / 2, 0.75 * inch, f"Page {page_num} of {total_pages}")
        
        # Header
        if page_num > 1:  # Skip header on first page
            self.drawString(inch, height - 0.75 * inch, "Godot TileMap vs TileSet Editors Guide")
            # Draw line under header
            self.setStrokeColor(colors.grey)
            self.line(inch, height - 0.85 * inch, width - inch, height - 0.85 * inch)

def create_visual_diagram(diagram_type, width=400, height=200):
    """Create visual diagrams for the PDF"""
    d = Drawing(width, height)
    
    if diagram_type == "tileset_structure":
        # TileSet structure diagram
        d.add(Rect(50, 150, 300, 40, fillColor=colors.lightblue, strokeColor=colors.darkblue))
        d.add(String(200, 165, "TileSet Resource", fontSize=14, textAnchor="middle", fillColor=colors.darkblue))
        
        # Tile boxes
        for i, (x, tile_name) in enumerate([(80, "Grass"), (160, "Stone"), (240, "Water")]):
            d.add(Rect(x, 100, 60, 40, fillColor=colors.lightgreen, strokeColor=colors.darkgreen))
            d.add(String(x + 30, 115, f"Tile {i}", fontSize=10, textAnchor="middle"))
            d.add(String(x + 30, 105, tile_name, fontSize=8, textAnchor="middle"))
            
            # Connection lines
            d.add(Line(x + 30, 140, x + 30, 150, strokeColor=colors.darkblue))
    
    elif diagram_type == "tilemap_structure":
        # TileMap structure diagram
        d.add(Rect(50, 150, 300, 40, fillColor=colors.lightyellow, strokeColor=colors.orange))
        d.add(String(200, 165, "TileMap Node", fontSize=14, textAnchor="middle", fillColor=colors.red))
        
        # Grid representation
        grid_size = 20
        start_x, start_y = 100, 50
        for row in range(4):
            for col in range(8):
                x = start_x + col * grid_size
                y = start_y + row * grid_size
                color = [colors.lightgreen, colors.lightgrey, colors.lightblue][((row + col) % 3)]
                d.add(Rect(x, y, grid_size-1, grid_size-1, fillColor=color, strokeColor=colors.black))
        
        # Connection line
        d.add(Line(200, 130, 200, 150, strokeColor=colors.orange))
    
    elif diagram_type == "workflow_comparison":
        # Workflow comparison
        # TileSet workflow (left side)
        ts_x = 50
        d.add(String(ts_x + 50, 180, "TileSet Workflow", fontSize=12, fillColor=colors.darkblue))
        workflow_steps = ["Create", "Import", "Configure", "Save"]
        for i, step in enumerate(workflow_steps):
            y = 150 - i * 30
            d.add(Rect(ts_x, y, 100, 20, fillColor=colors.lightblue, strokeColor=colors.darkblue))
            d.add(String(ts_x + 50, y + 10, step, fontSize=10, textAnchor="middle"))
            if i < len(workflow_steps) - 1:
                d.add(Line(ts_x + 50, y, ts_x + 50, y - 10, strokeColor=colors.darkblue))
        
        # TileMap workflow (right side)
        tm_x = 250
        d.add(String(tm_x + 50, 180, "TileMap Workflow", fontSize=12, fillColor=colors.darkgreen))
        workflow_steps = ["Add Node", "Assign", "Paint", "Test"]
        for i, step in enumerate(workflow_steps):
            y = 150 - i * 30
            d.add(Rect(tm_x, y, 100, 20, fillColor=colors.lightgreen, strokeColor=colors.darkgreen))
            d.add(String(tm_x + 50, y + 10, step, fontSize=10, textAnchor="middle"))
            if i < len(workflow_steps) - 1:
                d.add(Line(tm_x + 50, y, tm_x + 50, y - 10, strokeColor=colors.darkgreen))
    
    return d

def create_pdf_from_markdown(markdown_file, output_file):
    """Convert markdown file to PDF with enhanced formatting"""
    
    # Read markdown content
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        canvasmaker=NumberedCanvas
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        spaceBefore=24,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=16,
        textColor=colors.darkgreen,
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=12,
        textColor=colors.black,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        spaceAfter=6,
        fontName='Courier',
        backColor=colors.lightgrey,
        borderColor=colors.grey,
        borderWidth=1,
        borderPadding=6
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=3,
        leftIndent=20,
        bulletIndent=10,
        fontName='Helvetica'
    )
    
    # Story elements
    story = []
    
    # Split content into sections
    lines = md_content.split('\n')
    current_section = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('# '):
            # Main title
            title_text = line[2:].strip()
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 20))
            
        elif line.startswith('## '):
            # Section heading
            heading_text = line[3:].strip()
            story.append(Paragraph(heading_text, heading1_style))
            story.append(Spacer(1, 12))
            
            # Add visual diagrams for specific sections
            if "Key Differences" in heading_text:
                # Add comparison table
                story.append(Spacer(1, 10))
                
        elif line.startswith('### '):
            # Subsection heading
            heading_text = line[4:].strip()
            story.append(Paragraph(heading_text, heading2_style))
            story.append(Spacer(1, 8))
            
        elif line.startswith('#### '):
            # Sub-subsection heading
            heading_text = line[5:].strip()
            story.append(Paragraph(heading_text, heading3_style))
            story.append(Spacer(1, 6))
            
        elif line.startswith('```'):
            # Code block
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            
            code_text = '\n'.join(code_lines)
            # Split long code blocks
            if len(code_text) > 500:
                for chunk in [code_text[j:j+500] for j in range(0, len(code_text), 500)]:
                    story.append(Paragraph(f'<pre>{chunk}</pre>', code_style))
            else:
                story.append(Paragraph(f'<pre>{code_text}</pre>', code_style))
            story.append(Spacer(1, 10))
            
        elif line.startswith('| '):
            # Table
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            i -= 1  # Back up one line
            
            if len(table_lines) > 2:  # Has header and data
                # Parse table
                table_data = []
                for table_line in table_lines:
                    if '---' in table_line:
                        continue  # Skip separator line
                    cells = [cell.strip() for cell in table_line.split('|')[1:-1]]
                    table_data.append(cells)
                
                if table_data:
                    table = Table(table_data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 9),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(table)
                    story.append(Spacer(1, 12))
        
        elif line.startswith('- ✅') or line.startswith('- ❌'):
            # Checkmark/X bullet points
            text = line[2:].strip()
            color = colors.darkgreen if '✅' in text else colors.red
            story.append(Paragraph(f'<font color="{color.hexval()}">{text}</font>', bullet_style))
            
        elif line.startswith('- '):
            # Regular bullet point
            text = line[2:].strip()
            story.append(Paragraph(f'• {text}', bullet_style))
            
        elif line.startswith('**') and line.endswith('**'):
            # Bold text paragraph
            text = line[2:-2].strip()
            story.append(Paragraph(f'<b>{text}</b>', body_style))
            
        elif line and not line.startswith('#'):
            # Regular paragraph
            # Handle inline formatting
            text = line
            text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
            text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # Italic
            text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', text)  # Inline code
            
            if text.strip():
                story.append(Paragraph(text, body_style))
                story.append(Spacer(1, 6))
        
        elif line == '---':
            # Horizontal rule
            story.append(Spacer(1, 12))
            # Add a line here if needed
            story.append(Spacer(1, 12))
        
        # Add visual diagrams at appropriate points
        if i == 50:  # After introduction
            story.append(Spacer(1, 20))
            diagram = create_visual_diagram("tileset_structure", 400, 150)
            # Convert to image and add
            # For now, just add a placeholder
            story.append(Paragraph("<b>TileSet Structure Diagram</b>", heading3_style))
            story.append(Spacer(1, 10))
        
        i += 1
    
    # Build PDF
    doc.build(story)
    print(f"PDF created successfully: {output_file}")

def main():
    """Main function to create the PDF"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    markdown_file = os.path.join(current_dir, "Godot_TileMap_vs_TileSet_Guide.md")
    output_file = os.path.join(current_dir, "Godot_TileMap_vs_TileSet_Guide.pdf")
    
    if not os.path.exists(markdown_file):
        print(f"Error: Markdown file not found: {markdown_file}")
        return
    
    create_pdf_from_markdown(markdown_file, output_file)

if __name__ == "__main__":
    main()