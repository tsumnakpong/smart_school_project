import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
# lms/utils.py
import qrcode
import io
import base64

def draw_static_elements(canvas, doc):
    """ วาด Logo หัวกระดาษ และ Watermark กลางหน้า """
    seal_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'ST.png')
    
    if os.path.exists(seal_path):
        canvas.saveState()
        
        # --- 1. วาด Logo หัวกระดาษ (มุมซ้ายบน) ---
        # วาดที่ x=1.5cm, y=เกือบขอบบนสุด, ขนาดกว้าง 2.5cm
        canvas.drawImage(seal_path, 9.2*cm, A4[1] - 3.5*cm, width=2.5*cm, height=2.5*cm, mask='auto', preserveAspectRatio=True)
        
        # --- 2. วาด Watermark จางๆ กลางหน้า ---
        canvas.setFillAlpha(0.1)  # ความจาง 10%
        img_width = 14*cm
        img_height = 14*cm
        # คำนวณกึ่งกลางหน้า
        center_x = (A4[0] - img_width) / 2
        center_y = (A4[1] - img_height) / 2
        canvas.drawImage(seal_path, center_x, center_y, width=img_width, height=img_height, mask='auto', preserveAspectRatio=True)
        
        canvas.restoreState()
    else:
        canvas.saveState()
        canvas.setFont('Helvetica', 10)
        canvas.drawString(1.5*cm, A4[1] - 2*cm, "LOGO NOT FOUND")
        canvas.restoreState()

def render_to_pdf(template_src, context):
    buffer = BytesIO()
    
    # ปรับ topMargin เป็น 3.5cm เพื่อเว้นที่ให้ Logo หัวกระดาษ
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=2*cm, 
        leftMargin=2*cm, 
        topMargin=3.5*cm, 
        bottomMargin=0.5*cm
    )
    elements = []

    # --- การจัดการฟอนต์ ---
    font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'THSarabunNew.ttf')
    font_bold_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'THSarabunNew-Bold.ttf')

    pdfmetrics.registerFont(TTFont('Thai', font_path))
    if os.path.exists(font_bold_path):
        pdfmetrics.registerFont(TTFont('Thai-Bold', font_bold_path))
    else:
        pdfmetrics.registerFont(TTFont('Thai-Bold', font_path))

    # --- Styles ---
    styles = getSampleStyleSheet()
    style_header = ParagraphStyle(name='Header', fontName='Thai-Bold', fontSize=22, alignment=1, spaceAfter=18)
    style_subhead = ParagraphStyle(name='SubHead', fontName='Thai', fontSize=16, alignment=1, spaceAfter=5)
    style_normal = ParagraphStyle(name='Normal', fontName='Thai', fontSize=16, leading=20)

    # --- หัวข้อรายงาน ---
    subject_code = context.get('subject_code', '')
    subject_name = context.get('subject_name', '')
    
    elements.append(Paragraph("รายงานผลการเรียนรายบุคคล", style_header))
    elements.append(Paragraph(f"รหัสวิชา {subject_code} รายวิชา {subject_name}", style_subhead))
    elements.append(Paragraph("(Smart School Project)", style_subhead))
    
    # เส้นคั่น
    line_table = Table([['']], colWidths=[17*cm])
    line_table.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 1, colors.black)]))
    elements.append(line_table)
    elements.append(Spacer(1, 15))

    # --- ข้อมูลนักเรียน ---
    student = context.get('student')
    student_name = student.user.get_full_name() if student.user.get_full_name() else student.user.username
    
    info_data = [
        [Paragraph(f"<b>ชื่อ-นามสกุล:</b> {student_name}", style_normal), 
         Paragraph(f"<b>รหัสประจำตัว:</b> {student.student_id or '-'}", style_normal)],
        [Paragraph(f"<b>คะแนนเฉลี่ยสะสม:</b> {context.get('avg_score', '0.00')}", style_normal), ""]
    ]
    info_table = Table(info_data, colWidths=[9*cm, 8*cm])
    info_table.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    elements.append(info_table)
    elements.append(Spacer(1, 15))

    # --- ตารางคะแนน ---
    scores = context.get('scores')
    if scores:
        data = [['ลำดับ', 'บทเรียน / แบบทดสอบ', 'คะแนน', 'วันที่สอบ']]
        for i, s in enumerate(scores, 1):
            date_str = s.timestamp.strftime("%d %b %Y") if s.timestamp else "-"
            data.append([
                str(i),
                Paragraph(s.lesson.title, style_normal),
                f"{s.score} / {s.total_questions or 10}",
                date_str
            ])

        t = Table(data, colWidths=[1.5*cm, 9*cm, 3*cm, 3.5*cm])
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Thai'),
            ('FONTNAME', (0,0), (-1,0), 'Thai-Bold'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('ALIGN', (1,1), (1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("<font color='red'>*** ยังไม่พบข้อมูลการทำแบบทดสอบในระบบ ***</font>", style_subhead))

    # --- ท้ายกระดาษ ---
    elements.append(Spacer(1, 50))
    teacher_name = context.get('teacher_name') or "ครูผู้สอน"
    footer_data = [
        ["", f"ลงชื่อ............................................................"],
        ["", f"( {teacher_name} )"],
        ["", "ครูผู้สอน"],
        ["", f"พิมพ์เมื่อวันที่: {context.get('print_date', '')}"]
    ]
    footer_table = Table(footer_data, colWidths=[9*cm, 8*cm])
    footer_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Thai'),
        ('FONTSIZE', (0,0), (-1,-1), 16),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
         ('TOPPADDING', (0,0), (-1,-1), 5), # วางตำแหน่งลายเซ็นให้ดูสมดุล
    ]))


    elements.append(footer_table)

    # 4. สร้าง PDF โดยเรียกฟังก์ชันวาด Logo และ Watermark
    doc.build(elements, onFirstPage=draw_static_elements, onLaterPages=draw_static_elements)
    
    pdf_out = buffer.getvalue()
    buffer.close()
    return HttpResponse(pdf_out, content_type='application/pdf')

def generate_tran_script(student, grades):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # 1. ลงทะเบียนฟอนต์ไทย (ครูต้องวางไฟล์ .ttf ไว้ในโฟลเดอร์ static/fonts/)
    # pdfmetrics.registerFont(TTFont('ThaiFont', 'static/fonts/THSarabunNew.ttf'))
    p.setFont('Helvetica', 16) # ใช้ Helvetica แทนก่อนถ้ายังไม่มีฟอนต์ไทย

    # 2. วาดหัวเอกสาร
    p.drawCentredString(width/2, height - 2*cm, "OFFICIAL TRANSCRIPT")
    p.setFont('Helvetica', 12)
    p.drawString(2*cm, height - 3.5*cm, f"Student Name: {student.user.get_full_name()}")
    p.drawString(2*cm, height - 4.2*cm, f"Student ID: {student.student_id}")
    p.drawString(2*cm, height - 4.9*cm, f"Class: {student.classroom.name}")

    # 3. วาดตารางคะแนน
    y = height - 6.5*cm
    p.line(2*cm, y + 0.5*cm, width - 2*cm, y + 0.5*cm) # เส้นบน
    p.drawString(2.5*cm, y, "Subject Code")
    p.drawString(6*cm, y, "Subject Name")
    p.drawString(14*cm, y, "Score")
    p.drawString(17*cm, y, "Grade")
    p.line(2*cm, y - 0.2*cm, width - 2*cm, y - 0.2*cm) # เส้นล่างหัวตาราง

    y -= 0.8*cm
    for g in grades:
        p.drawString(2.5*cm, y, g.subject.code)
        p.drawString(6*cm, y, g.subject.name_th)
        p.drawString(14*cm, y, str(g.total_score))
        p.drawCentredString(17.5*cm, y, g.grade)
        y -= 0.7*cm

    # 4. ลายเซ็นต์
    p.drawString(13*cm, 4*cm, "__________________________")
    p.drawCentredString(15.5*cm, 3.5*cm, "( นายทะเบียน )")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer



def generate_student_qr_base64(student_id):
    # ตั้งค่า QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(student_id)
    qr.make(fit=True)

    # สร้างรูปภาพ (ใช้สีดำ-ขาว มาตรฐาน)
    img = qr.make_image(fill_color="black", back_color="white")

    # แปลงรูปภาพเป็น Byte Stream
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    
    # แปลงเป็น Base64 string
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"