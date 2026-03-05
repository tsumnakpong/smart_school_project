# iot/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AttendanceLog
from sms.models import Student

class CheckInAPI(APIView):
    def post(self, request):
        s_id = request.data.get('student_id')
        print(f"📡 API ได้รับรหัส: '{s_id}'") # ดูว่ามีช่องว่างติดมาไหม
        
        # ค้นหาแบบไม่สนตัวเล็กตัวใหญ่ และตัดช่องว่างทิ้ง (.strip())
        student = Student.objects.filter(student_id__iexact=str(s_id).strip()).first()
        
        if student:
            AttendanceLog.objects.create(
                student=student,
                method="AI Simulator",
                status="PRESENT"
            )
            print(f"✅ สำเร็จ! พบนักเรียน: {student.user.first_name}")
            return Response({"message": "success"}, status=status.HTTP_201_CREATED)
        else:
            print(f"❌ ไม่พบรหัส: '{s_id}' ในระบบ")
            # โชว์รหัสทั้งหมดที่มีในระบบตอนนี้เพื่อเทียบกัน
            all_ids = list(Student.objects.values_list('student_id', flat=True))
            print(f"🔍 รหัสที่มีในระบบตอนนี้คือ: {all_ids}")
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)