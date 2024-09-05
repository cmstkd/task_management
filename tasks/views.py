from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Task, StaffTask
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader
import io


def home(request):
    admin_login_url = 'http://127.0.0.1:8000/admin/'
    staff_login_url = reverse('staff_login')
    return render(request, 'home.html', {
        'admin_login_url': admin_login_url,
        'staff_login_url': staff_login_url,
    })


@login_required
def task_list(request):
    is_admin = request.user.groups.filter(name='Admin').exists()
    tasks = Task.objects.all() if is_admin else Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'is_admin': is_admin,
    })


def logout_view(request):
    logout(request)
    return redirect('home')


def task_detail_public(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail_public.html', {'task': task})


@login_required
def change_task_status(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user == task.assigned_to or request.user.groups.filter(name='Admin').exists():
        if request.method == 'POST':
            task.status = 'Completed' if task.status == 'Pending' else 'Pending'
            task.save()
    return redirect('task_list')


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/admin_login.html', {'form': form})


def staff_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid credentials or not authorized as staff.')
    return render(request, 'tasks/staff_login.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:  # Assuming admin has superuser rights
            login(request, user)
            return redirect('admin_dashboard')  # Replace with actual admin dashboard URL
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'tasks/admin_login.html')


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})


def generate_and_upload_pdf(request):
    if request.method == 'POST':
        form = StaffTaskForm(request.POST, request.FILES)
        if form.is_valid():
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            p.drawString(100, 750, "Hello, this is a PDF file!")
            p.showPage()
            p.save()

            buffer.seek(0)
            pdf_writer = PdfWriter()
            pdf_reader = PdfReader(buffer)
            pdf_writer.append_pages_from_reader(pdf_reader)

            # Optionally encrypt the PDF (if needed)
            # pdf_writer.encrypt('password')  # Uncomment if password protection is needed

            pdf_buffer = io.BytesIO()
            pdf_writer.write(pdf_buffer)
            pdf_buffer.seek(0)

            task = form.save(commit=False)
            task.pdf_file.save(f"task_{task.title}.pdf", pdf_buffer)
            task.save()

            return redirect('task_success')  # Make sure this URL is defined in your URL patterns
    else:
        form = StaffTaskForm()

    return render(request, 'generate_and_upload_pdf.html', {'form': form})


def staff_task_list(request):
    tasks = StaffTask.objects.all()
    return render(request, 'staff_task_list.html', {'tasks': tasks})
