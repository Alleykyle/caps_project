import os
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse,  Http404, FileResponse
from django.conf import settings
import mimetypes
from django.contrib import messages
from landing.models import File,Folder
from collections import defaultdict 
from django.contrib import messages
from .models import Folder, File, Barangay, Employee
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
from django.utils import timezone

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

def landing_page(request):
    return render(request, 'landing_page.html')

def monitoring_calendar(request):
    return render(request, "landing/monitoring_calendar.html")


def csc_page(request):
    return render(request, "landing/csc_page.html")

#DASHBOARD
def dashboard(request):
    """Main dashboard view"""

    try:
        # Safely get barangays - return empty list if any error
        top_barangays = Barangay.objects.all().order_by('-date_updated')[:5] if Barangay.objects.exists() else []
    except:
        top_barangays = []
    context = {
        'total_certificates': get_total_certificates(),
        'total_employees': Employee.objects.count(),
        'completed_count': get_completed_count(),
        'pending_count': get_pending_count(),
        'incomplete_count': get_incomplete_count(),
        'top_barangays': get_top_barangays(),
        'current_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    return render(request, 'landing/dashboard.html', context)

def dashboard_data_api(request):
    """API endpoint for real-time dashboard updates"""
    data = {
        'total_certificates': get_total_certificates(),
        'total_employees': Employee.objects.count(),
        'completed_count': get_completed_count(),
        'pending_count': get_pending_count(),
        'incomplete_count': get_incomplete_count(),
        'top_barangays': get_top_barangays_json(),
        'trend_data': get_trend_data(),
        'timestamp': timezone.now().isoformat(),
    }
    return JsonResponse(data)

# Helper functions
def get_total_certificates():
    """Count total certificates (assuming PDF files are certificates)"""
    return File.objects.filter(file_type='pdf').count()

def get_completed_count():
    """Count completed barangays"""
    return Barangay.objects.filter(status='Completed').count()

def get_pending_count():
    """Count pending barangays"""
    return Barangay.objects.filter(status='Pending').count()

def get_incomplete_count():
    """Count incomplete barangays"""
    return Barangay.objects.filter(status='Incomplete').count()

def get_top_barangays():
    """Get top performing barangays"""
    return Barangay.objects.all().order_by('-date_updated')[:5]

def get_top_barangays_json():
    """Get top barangays as JSON serializable data"""
    barangays = Barangay.objects.all().order_by('-date_updated')[:5]
    return [{
        'name': b.name,
        'status': b.status,
        'score': 95 if b.status == 'Completed' else 87 if b.status == 'Pending' else 60
    } for b in barangays]

def get_trend_data():
    """Get trend data for the last 6 months"""
    # This is sample data - replace with actual logic based on your date fields
    return [65, 78, 90, 81, 95, 108]

def application_request(request) :
    return render(request, "landing/application_request.html")

def history(request) :
    return render(request, "landing/history.html")

#EMPLOYEES PROFILE
def employees_profile(request):
    employees = Employee.objects.all().order_by('name')
    return render(request, "landing/employees_profile.html", {'employees': employees})

@csrf_exempt
@require_http_methods(["POST"])
def add_employee(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        employee_id = data.get('employee_id', '').strip()
        task_assign = data.get('task_assign', 'Monitoring')
        
        # Validation
        if not name:
            return JsonResponse({'success': False, 'error': 'Name is required'})
        
        if not employee_id:
            return JsonResponse({'success': False, 'error': 'Employee ID is required'})
        
        # Check if employee ID already exists
        if Employee.objects.filter(employee_id=employee_id).exists():
            return JsonResponse({'success': False, 'error': 'Employee ID already exists'})
        
        # Create new employee
        employee = Employee.objects.create(
            name=name,
            employee_id=employee_id,
            task_assign=task_assign
        )
        
        return JsonResponse({
            'success': True,
            'employee': {
                'id': employee.id,
                'name': employee.name,
                'employee_id': employee.employee_id,
                'task_assign': employee.task_assign
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def update_employee(request, employee_id):
    try:
        employee = get_object_or_404(Employee, id=employee_id)
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        emp_id = data.get('employee_id', '').strip()
        task_assign = data.get('task_assign', 'Monitoring')
        
        # Validation
        if not name:
            return JsonResponse({'success': False, 'error': 'Name is required'})
        
        if not emp_id:
            return JsonResponse({'success': False, 'error': 'Employee ID is required'})
        
        # Check if employee ID already exists (excluding current employee)
        if Employee.objects.filter(employee_id=emp_id).exclude(id=employee_id).exists():
            return JsonResponse({'success': False, 'error': 'Employee ID already exists'})
        
        # Update employee
        employee.name = name
        employee.employee_id = emp_id
        employee.task_assign = task_assign
        employee.save()
        
        return JsonResponse({
            'success': True,
            'employee': {
                'id': employee.id,
                'name': employee.name,
                'employee_id': employee.employee_id,
                'task_assign': employee.task_assign
            }
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
@require_http_methods(["POST"])
def delete_employee(request, employee_id):
    try:
        employee = get_object_or_404(Employee, id=employee_id)
        employee_name = employee.name
        employee.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Employee {employee_name} deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_http_methods(["GET"])
def get_employees(request):
    try:
        employees = Employee.objects.all().order_by('name')
        employees_data = []
        
        for employee in employees:
            employees_data.append({
                'id': employee.id,
                'name': employee.name,
                'employee_id': employee.employee_id,
                'task_assign': employee.task_assign
            })
        
        return JsonResponse({
            'success': True,
            'employees': employees_data
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



#FILE CATEGORIZATION
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
        ext = os.path.splitext(filename)[1][1:].lower()  # Get file extension (e.g., 'pdf', 'docx')

        # Determine folder based on file extension or keywords in filename
        if ext == 'pdf':
            folder = 'Application Form'
        elif ext in ['doc', 'docx']:
            folder = 'Request Letter'
        elif any(keyword in filename for keyword in ['signature', 'sign', 'e-sign', 'esign']):
            folder = 'Signature Images'
        elif ext in ['jpg', 'jpeg', 'png', 'gif', 'jfif'] and any(k in filename for k in ['id', 'identification']):
            folder = 'Identification Images'
        else:
            folder = "Others"

        # Save the file with the determined folder
        new_file = File(
            file=uploaded_file,
            folder=folder,
            file_type=ext
        )
        new_file.save()

        uploaded_file_url = new_file.file.url
        messages.success(request, f"File '{uploaded_file.name}' uploaded to '{folder}' folder Successfully.")

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

# List of allowed folders (for security)
ALLOWED_FOLDERS = ['Application Form', 'Identification Images', 'Request Letter']

@require_http_methods(["GET", "POST"])
def delete_folder(request):
    if request.method == "POST":
        folder_name = request.POST.get("folder_name")
        if not folder_name or folder_name not in ALLOWED_FOLDERS:
            messages.error(request, "Invalid folder selected.")
            return redirect("delete_folder")

        folder_path = os.path.join(settings.MEDIA_ROOT, 'uploads', folder_name)

        if not os.path.exists(folder_path):
            messages.warning(request, f"Folder '{folder_name}' does not exist.")
            return redirect("delete_folder")

        try:
            # Recursively delete the folder
            import shutil
            shutil.rmtree(folder_path)
            messages.success(request, f"✅ Folder '{folder_name}' has been deleted.")
        except Exception as e:
            messages.error(request, f"❌ Error deleting folder: {e}")

        return redirect("delete_folder")

    return render(request, "delete_folder.html", {
        "folders": ALLOWED_FOLDERS,
    })



def settings(request):
    return render(request, "landing/settings.html")


#Barangay Monitoring
def barangay_detail(request, barangay_id):
    tasks = [
        "Barangay Road Clean up Operation (BARCO)",
        "Barangay Assembly",
        "Community Health Check",
        "Waste Management Campaign",
    ]

    context = {
        'barangay_id': barangay_id,
        'tasks': tasks,
        'active_barangay': barangay_id,
        'barangay_range': range(1, 34),  # Pass the range for sidebar
        'current_status': 'accomplished', 
    }
    return render(request, 'monitoring/barangay_detail.html', context)




#Application letter
def serve_document(request, application_id, doc_type):
    """
    Serve documents for viewing in browser
    doc_type can be: 'request-letter', 'application-form', 'supporting-docs'
    """
    try:
        # Map document types to folder names
        folder_mapping = {
            'request-letter': 'Request Letter',
            'application-form': 'Application Form', 
            'supporting-docs': 'Others'  # or whatever folder you use for supporting docs
        }
        
        folder_name = folder_mapping.get(doc_type)
        if not folder_name:
            raise Http404("Document type not found")
        
        # Get files from the specified folder
        files = File.objects.filter(folder=folder_name)
        
        if not files.exists():
            raise Http404("No documents found")
        
        # For now, get the first file (you might want to filter by application_id if you have that field)
        file_obj = files.first()
        
        if not file_obj or not file_obj.file:
            raise Http404("Document not found")
        
        file_path = file_obj.file.path
        
        if not os.path.exists(file_path):
            raise Http404("File does not exist")
        
        # Get the mime type
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # For Word documents, set appropriate headers to open in browser
        if file_obj.file_type in ['doc', 'docx']:
            # For Word docs, we'll force download since browsers can't display them directly
            # But we can try to open with office online viewer or convert to PDF
            response = FileResponse(
                open(file_path, 'rb'),
                content_type=mime_type or 'application/octet-stream'
            )
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
            return response
        else:
            # For other file types (PDF, images, etc.)
            return FileResponse(
                open(file_path, 'rb'),
                content_type=mime_type or 'application/octet-stream'
            )
            
    except Exception as e:
        raise Http404(f"Error serving document: {str(e)}")


# Alternative view if you want to use Office Online Viewer for Word docs
def view_document_online(request, application_id, doc_type):
    """
    Alternative view that redirects to Office Online Viewer for Word documents
    """
    try:
        folder_mapping = {
            'request-letter': 'Request Letter',
            'application-form': 'Application Form', 
            'supporting-docs': 'Others'
        }
        
        folder_name = folder_mapping.get(doc_type)
        if not folder_name:
            raise Http404("Document type not found")
        
        files = File.objects.filter(folder=folder_name)
        
        if not files.exists():
            raise Http404("No documents found")
        
        file_obj = files.first()
        
        if not file_obj or not file_obj.file:
            raise Http404("Document not found")
        
        # For Word documents, create a URL to Office Online Viewer
        if file_obj.file_type in ['doc', 'docx']:
            # You'll need to make your file publicly accessible for this to work
            file_url = request.build_absolute_uri(file_obj.file.url)
            office_viewer_url = f"https://view.officeapps.live.com/op/embed.aspx?src={file_url}"
            
            return redirect(office_viewer_url)
        else:
            # For other files, serve directly
            return serve_document(request, application_id, doc_type)
            
    except Exception as e:
        raise Http404(f"Error viewing document: {str(e)}")





