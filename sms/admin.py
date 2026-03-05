from django.contrib import admin
from .models import Classroom, Subject, Student, Enrollment

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name_th', 'category', 'credit')
    list_filter = ('category',)
    search_fields = ('code', 'name_th')

admin.site.register(Classroom)
admin.site.register(Student)
admin.site.register(Enrollment)
