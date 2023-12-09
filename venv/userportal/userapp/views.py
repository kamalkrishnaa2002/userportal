from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .forms import FileUploadForm
from .models import UploadedFile,SharedFile
from .forms import UserSearchForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseNotFound, JsonResponse
from django.db.models import Q
import mimetypes
from django.template.loader import render_to_string



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):
    # Redirect to the home page if the user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')  # Change 'home' to your desired home URL

@login_required(login_url='login')  # Specify the login URL
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})

@login_required(login_url='login')
def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'file_list.html', {'files': files})

@login_required(login_url='login')
def user_search(request):
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Exclude the current logged-in user from the search results
            users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)

            if not users:
                # If no users found, return a JSON response with a message
                return JsonResponse({'message': 'No users found'})

            # If users are found, render the template and return the HTML
            return render(request, 'user_search_results.html', {'users': users})
    else:
        form = UserSearchForm()

    return render(request, 'user_search.html', {'form': form})


@login_required(login_url='login')
def share_files(request):
    if request.method == 'POST':
        if 'selected_users[]' in request.POST:
            # Process form submission from search results
            selected_user_ids = request.POST.getlist('selected_users[]')
            # Exclude the current logged-in user from the selected users
            selected_users = User.objects.filter(id__in=selected_user_ids).exclude(id=request.user.id)
            return render(request, 'user_search_results.html', {'users': selected_users})

        elif 'selected_files[]' in request.POST:
            # Process form submission from share_files_page
            selected_user_id = request.POST.get('selected_user')
            selected_user = get_object_or_404(User, id=selected_user_id)
            selected_file_ids = request.POST.getlist('selected_files[]')
            selected_files = UploadedFile.objects.filter(id__in=selected_file_ids)

            # Perform the logic to share the selected files with the selected user
            for file_to_share in selected_files:
                SharedFile.objects.create(user_shared_from=request.user, user_shared_with=selected_user, file=file_to_share)

            return redirect('home')  # Change 'success_page' to your actual success page name

    # Handle the case where the form is not submitted properly
    return redirect('user_search')  # Change 'user_search' to your actual search page name

@login_required(login_url='login')
def share_files_page(request, user_id):
    selected_user = get_object_or_404(User, id=user_id)
    user_uploaded_files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'share_files_page.html', {'selected_user': selected_user, 'user_uploaded_files': user_uploaded_files})

@login_required(login_url='login')
def shared_files_view(request):
    shared_files = SharedFile.objects.filter(user_shared_with=request.user)
    return render(request, 'shared_files.html', {'shared_files': shared_files})

@login_required(login_url='login')
def view_shared_file(request, shared_file_id):
    shared_file = get_object_or_404(SharedFile, id=shared_file_id, user_shared_with=request.user)

    # Check if the file is an image based on its MIME type
    mime_type, encoding = mimetypes.guess_type(shared_file.file.file.name)
    if mime_type and mime_type.startswith('image'):
        # If it's an image, serve it in a new tab
        return render(request, 'view_shared_image.html', {'shared_file': shared_file})

    # If it's not an image, return a 404 Not Found response
    return HttpResponseNotFound("File not found or not viewable online.")

@login_required(login_url='login')
def download_shared_file(request, shared_file_id):
    shared_file = get_object_or_404(SharedFile, id=shared_file_id, user_shared_with=request.user)
    response = HttpResponse(shared_file.file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{shared_file.file.file.name}"'
    return response

