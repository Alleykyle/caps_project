import os
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib import messages
from landing.models import File,Folder
from collections import defaultdict 
from django.contrib import messages
from django.contrib.auth import authenticate, login  # <-- import login here



def home(request):
    return render(request, 'landing/home.html')

def signin(request):
    return render(request, 'landing/signin.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('landing:login')  # make sure your login URL is named 'login'
    else:
        form = UserCreationForm()
    return render(request, 'landing/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('landing_page')  # ✅ This must match the URL name
        else:
            # Show error if login fails
            return render(request, 'landing/login.html', {'error': 'Invalid username or password'})

    return render(request, 'landing/login.html')

def landing_page(request):
    return render(request, "landing/landing_page.html")

def monitoring_calendar(request):
    return render(request, "landing/monitoring_calendar.html")

def csc_page(request):
    return render(request, "landing/csc_page.html")

def dashboard(request):
    return render(request, 'landing/dashboard.html')

def application_request(request) :
    return render(request, "landing/application_request.html")

def history(request) :
    return render(request, "landing/history.html")

def employees_profile(request) :
    return render(request, "landing/employees_profile.html")


def fold(request):
    uploaded_file_url = None

    # Handle folder creation
    if request.method == 'POST' and 'new_folder' in request.POST:
        folder_name = request.POST.get('new_folder')
        if folder_name:
            Folder.objects.get_or_create(name=folder_name.strip())

    # Handle file upload with categorization
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        filename = uploaded_file.name.lower()  # Normalize for case-insensitive matching

        # 🔍 Determine folder based on filename or extension
        if filename.endswith('.pdf'):
            folder_name = "Application Form"
        elif filename.endswith('.doc') or filename.endswith('.docx'):
            folder_name = "Request Letter"
        elif 'signature' in filename:
            folder_name = "Signature Images"
        elif 'id' in filename or 'identification' in filename:
            folder_name = "Identification Images"
        else:
            folder_name = "Others"

        folder, _ = Folder.objects.get_or_create(name=folder_name)
        new_file = File(file=uploaded_file, folder=folder)
        new_file.save()

        uploaded_file_url = new_file.file.url
        messages.success(request, f"File '{uploaded_file.name}' uploaded to '{folder.name}' folder.")

        return redirect('fold')

    folders = Folder.objects.all()
    files = File.objects.all()

    return render(request, 'landing/fold.html', {
        'folders': folders,
        'files': files,
        'uploaded_file_url': uploaded_file_url
    })


def folder_detail(request, folder_name):
    files = File.objects.filter(folder=folder_name)
    folders = Folder.objects.all()
    return render(request, 'landing/fold.html', {
        'files': files,
        'folders': folders,
        'selected_folder': folder_name,
    })


def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file.file.delete()  # Delete the actual file from storage
    file.delete()       # Delete the database record
    messages.success(request, f"File '{file.file.name}' deleted successfully.")
    return redirect('fold')

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name.lower()
        name_lower = file_name.lower()

        ext = file_name.split('.')[-1]

        # Determine folder based on extension and filename
        if file_name.lower().endswith('.pdf'):
            return "Application Form"
        elif ext in ['doc', 'docx'] and 'request' in file_name:
            folder = 'Request Letter'
        elif any(keyword in file_name for keyword in ['signature', 'sign', 'e-sign', 'esign']):
            folder = 'Signature Images'
        elif ext in ['jpg', 'jpeg', 'png', 'gif', 'jfif'] and any(k in file_name for k in ['id', 'identification']):
            folder = 'Identification Images'


        new_file = File(
            file=uploaded_file,
            file_type=ext,
            folder=folder
        )
        new_file.save()

        return redirect('fold', folder_name=folder)

    return render(request, 'landing/fold.html')



def settings(request):
    return render(request, "landing/settings.html")