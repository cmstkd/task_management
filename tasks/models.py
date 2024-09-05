from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    customer_mobile = models.CharField(max_length=15)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class StaffTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    pdf_file = models.FileField(upload_to='task_pdfs/')  # This stores the PDF files
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
