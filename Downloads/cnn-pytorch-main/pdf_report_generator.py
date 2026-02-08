"""
PDF Report Generator for Crop Disease Diagnosis Results

SOLID Principles Applied:
- SRP: Single responsibility for generating PDF reports
- OCP: Open for extension (can add new report formats)
- DIP: Depends on abstractions (DiagnosisResult dataclass)
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import datetime
from typing import List
import io
from pathlib import Path


class PDFReportGenerator:
    """
    Generates professional PDF reports for crop disease diagnosis results.
    
    Follows SRP: Only responsible for PDF generation logic.
    """
    
    def __init__(self):
        """Initialize PDF report generator with default settings"""
        self.page_size = letter
        self.margin = 0.75 * inch
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2e7d32'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#388e3c'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#4caf50'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#212121'),
            spaceAfter=6,
            fontName='Helvetica'
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='CustomFooter',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#757575'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        ))
    
    def _add_header(self, elements: List, title: str = "Crop Disease Diagnosis Report"):
        """Add header section to the report"""
        # Title
        title_para = Paragraph(title, self.styles['CustomTitle'])
        elements.append(title_para)
        elements.append(Spacer(1, 0.2 * inch))
        
        # Subtitle
        subtitle = Paragraph(
            "AI-Powered Disease Detection System",
            self.styles['CustomBody']
        )
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3 * inch))
    
    def _add_diagnosis_summary(self, elements: List, diagnosis_result):
        """Add diagnosis summary section"""
        # Section heading
        heading = Paragraph("Diagnosis Summary", self.styles['CustomHeading'])
        elements.append(heading)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Create summary table
        disease_name = diagnosis_result.disease_name.replace('_', ' ').title()
        confidence_pct = diagnosis_result.confidence * 100
        
        # Determine confidence level
        if confidence_pct >= 80:
            confidence_level = "High"
            confidence_color = colors.HexColor('#4caf50')
        elif confidence_pct >= 60:
            confidence_level = "Moderate"
            confidence_color = colors.HexColor('#ff9800')
        else:
            confidence_level = "Low"
            confidence_color = colors.HexColor('#f44336')
        
        summary_data = [
            ['Detected Disease:', disease_name],
            ['Confidence Score:', f'{confidence_pct:.2f}%'],
            ['Confidence Level:', confidence_level],
            ['Analysis Date:', diagnosis_result.timestamp.strftime('%Y-%m-%d %H:%M:%S')],
            ['Image File:', diagnosis_result.image_filename]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#212121')),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c8e6c9')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3 * inch))
    
    def _add_image(self, elements: List, image: Image.Image):
        """Add the uploaded crop image to the report"""
        heading = Paragraph("Analyzed Image", self.styles['CustomHeading'])
        elements.append(heading)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Convert PIL Image to ReportLab Image
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Calculate image dimensions to fit within page
        max_width = 5 * inch
        max_height = 4 * inch
        
        img_width, img_height = image.size
        aspect_ratio = img_width / img_height
        
        if aspect_ratio > 1:  # Landscape
            width = min(max_width, img_width)
            height = width / aspect_ratio
        else:  # Portrait
            height = min(max_height, img_height)
            width = height * aspect_ratio
        
        rl_image = RLImage(img_buffer, width=width, height=height)
        elements.append(rl_image)
        elements.append(Spacer(1, 0.3 * inch))
    
    def _add_predictions_table(self, elements: List, predictions: List):
        """Add detailed predictions table"""
        heading = Paragraph("Detailed Predictions", self.styles['CustomHeading'])
        elements.append(heading)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Create table data
        table_data = [['Rank', 'Disease Name', 'Confidence', 'Probability']]
        
        for i, pred in enumerate(predictions, 1):
            disease_name = pred.class_name.replace('_', ' ').title()
            confidence_pct = pred.confidence * 100
            
            # Create visual bar for confidence
            bar_length = int(confidence_pct / 5)  # Scale to 20 chars max
            bar = '█' * bar_length + '░' * (20 - bar_length)
            
            table_data.append([
                str(i),
                disease_name,
                f'{confidence_pct:.2f}%',
                bar
            ])
        
        predictions_table = Table(table_data, colWidths=[0.6*inch, 2.5*inch, 1.2*inch, 2.2*inch])
        predictions_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4caf50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#212121')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('ALIGN', (3, 1), (3, -1), 'LEFT'),
            
            # Grid and padding
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c8e6c9')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))
        
        elements.append(predictions_table)
        elements.append(Spacer(1, 0.3 * inch))
    
    def _add_footer(self, elements: List):
        """Add footer section with disclaimer"""
        elements.append(Spacer(1, 0.5 * inch))
        
        disclaimer = Paragraph(
            "<b>Disclaimer:</b> This diagnosis is generated by an AI model and should be used as a reference only. "
            "For critical decisions, please consult with agricultural experts or plant pathologists.",
            self.styles['CustomBody']
        )
        elements.append(disclaimer)
        elements.append(Spacer(1, 0.2 * inch))
        
        footer = Paragraph(
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
            "Crop Disease Diagnosis System © 2026",
            self.styles['CustomFooter']
        )
        elements.append(footer)
    
    def generate_report(self, diagnosis_result, image: Image.Image) -> bytes:
        """
        Generate a complete PDF report.
        
        Args:
            diagnosis_result: DiagnosisResult object containing diagnosis information
            image: PIL Image object of the analyzed crop
            
        Returns:
            bytes: PDF file content as bytes
        """
        # Create PDF buffer
        pdf_buffer = io.BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=self.page_size,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        # Build document elements
        elements = []
        
        # Add sections
        self._add_header(elements)
        self._add_diagnosis_summary(elements, diagnosis_result)
        self._add_image(elements, image)
        self._add_predictions_table(elements, diagnosis_result.all_predictions)
        self._add_footer(elements)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
