"""
LOA (Letter of Authorization) PDF Generator for Number Porting

Generates Twilio-compliant LOA documents for UK number porting.
"""

import os
from datetime import datetime
from typing import Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io


def generate_loa_pdf(
    number_to_port: str,
    current_provider: str,
    account_number: str,
    account_holder_name: str,
    billing_postcode: str,
    authorized_signature: str,
    business_name: Optional[str] = None,
    request_id: Optional[str] = None,
) -> bytes:
    """
    Generate a Letter of Authorization PDF for number porting.
    
    Returns PDF as bytes.
    """
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=25*mm,
        leftMargin=25*mm,
        topMargin=25*mm,
        bottomMargin=25*mm,
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20,
    )
    
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=15,
        spaceAfter=10,
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14,
    )
    
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        spaceAfter=5,
    )
    
    # Build document content
    story = []
    
    # Header
    story.append(Paragraph("LETTER OF AUTHORIZATION", title_style))
    story.append(Paragraph("For Telephone Number Porting", styles['Heading3']))
    story.append(Spacer(1, 10*mm))
    
    # Reference info
    today = datetime.now().strftime("%d %B %Y")
    ref_data = [
        ["Date:", today],
        ["Reference:", request_id or f"PORT-{datetime.now().strftime('%Y%m%d%H%M')}"],
    ]
    ref_table = Table(ref_data, colWidths=[30*mm, 80*mm])
    ref_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    story.append(ref_table)
    story.append(Spacer(1, 10*mm))
    
    # Authorization text
    story.append(Paragraph("AUTHORIZATION TO PORT TELEPHONE NUMBER", heading_style))
    
    auth_text = f"""
    I, <b>{account_holder_name}</b>, hereby authorize Covered AI Limited to act on my behalf 
    to port the telephone number(s) listed below from my current service provider to Covered AI's 
    telecommunications platform powered by Twilio.
    """
    story.append(Paragraph(auth_text, body_style))
    
    # Number details table
    story.append(Paragraph("TELEPHONE NUMBER DETAILS", heading_style))
    
    number_data = [
        ["Number to Port:", number_to_port],
        ["Current Provider:", current_provider],
        ["Account Number:", account_number],
        ["Account Holder:", account_holder_name],
        ["Billing Postcode:", billing_postcode],
    ]
    
    number_table = Table(number_data, colWidths=[50*mm, 100*mm])
    number_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.Color(0.95, 0.95, 0.95)),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(number_table)
    story.append(Spacer(1, 10*mm))
    
    # Declarations
    story.append(Paragraph("DECLARATIONS", heading_style))
    
    declarations = [
        "I am the account holder or an authorized representative with full authority to request this port.",
        "I understand that porting my number will transfer it from my current provider to Covered AI.",
        "I authorize my current provider to release the above telephone number(s) to Covered AI Limited.",
        "I understand that my current provider may charge an early termination fee if applicable.",
        "I confirm that all information provided above is accurate and complete.",
        "I understand that the porting process typically takes 5-10 business days in the UK.",
    ]
    
    for i, dec in enumerate(declarations, 1):
        story.append(Paragraph(f"{i}. {dec}", body_style))
    
    story.append(Spacer(1, 15*mm))
    
    # Signature section
    story.append(Paragraph("AUTHORIZATION SIGNATURE", heading_style))
    
    sig_data = [
        ["Electronic Signature:", authorized_signature],
        ["Full Name:", account_holder_name],
        ["Date Signed:", today],
    ]
    
    if business_name:
        sig_data.insert(2, ["Business Name:", business_name])
    
    sig_table = Table(sig_data, colWidths=[50*mm, 100*mm])
    sig_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Oblique'),  # Signature in italic
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(sig_table)
    
    story.append(Spacer(1, 15*mm))
    
    # Footer
    story.append(Paragraph(
        "This Letter of Authorization is submitted electronically and constitutes a valid authorization "
        "under UK telecommunications regulations. The electronic signature above has the same legal "
        "effect as a handwritten signature.",
        small_style
    ))
    
    story.append(Spacer(1, 5*mm))
    
    story.append(Paragraph(
        "Covered AI Limited | Company No. XXXXXXXX | hello@covered.ai | 0800 COVERED",
        small_style
    ))
    
    # Build PDF
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def save_loa_pdf(
    output_path: str,
    number_to_port: str,
    current_provider: str,
    account_number: str,
    account_holder_name: str,
    billing_postcode: str,
    authorized_signature: str,
    business_name: Optional[str] = None,
    request_id: Optional[str] = None,
) -> str:
    """
    Generate and save LOA PDF to file.
    
    Returns the file path.
    """
    pdf_bytes = generate_loa_pdf(
        number_to_port=number_to_port,
        current_provider=current_provider,
        account_number=account_number,
        account_holder_name=account_holder_name,
        billing_postcode=billing_postcode,
        authorized_signature=authorized_signature,
        business_name=business_name,
        request_id=request_id,
    )
    
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)
    
    return output_path


# Test function
if __name__ == "__main__":
    pdf_path = save_loa_pdf(
        output_path="test_loa.pdf",
        number_to_port="0191 123 4567",
        current_provider="BT",
        account_number="ACC123456",
        account_holder_name="John Smith",
        billing_postcode="NE1 4ST",
        authorized_signature="John Smith",
        business_name="Smith Plumbing Ltd",
        request_id="PORT-001",
    )
    print(f"Generated: {pdf_path}")
