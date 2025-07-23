from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.contrib import messages
from .forms import AnonymousReportForm, CitizenReportForm, CitizenReportStatusForm, UserUpdateForm, ProfileUpdateForm
from .models import CitizenReport, AnonymousReport, Profile
from django.contrib.auth.decorators import login_required
import folium, geocoder
from django.http import HttpResponse
from .models import ChatMessage




def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

# @login_required(login_url='index')
# def map(request):
#     # Get coordinates of a location 
#     location = geocoder.osm("Nigeria")
#     lat, lng = location.latlng

#     # Create a Folium map centered at the location
#     m = folium.Map(location=[lat, lng], zoom_start=12)

#     # Add a marker for the location
#     folium.Marker([lat, lng], popup='Nigeria').add_to(m)

#     # Render the map to the template
#     return render(request, 'map.html', {'map': m})

@login_required(login_url='index')
def map(request):
    return render(request, 'map.html')


    
@login_required(login_url='index')
def stats(request):
    return render(request, 'stats.html', {})

@login_required(login_url='index')
def agent_portal(request):
    anonymous = AnonymousReport.objects.all()
    citizen = CitizenReport.objects.all()
    context = {
         'anonymous' : anonymous,
         'citizen' : citizen,
    }
    return render(request, 'agent.html', context)


def agent_signup(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            agent_id = request.POST.get('AgentID')
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Create the user object
            user = User.objects.create_user(username=username, email=email, password=password)

            # Assign the user to the "Law Enforcement Agents" group
            law_enforcement_group, created = Group.objects.get_or_create(name='Law Enforcement Agents')
            user.groups.add(law_enforcement_group)

            # Additional attributes specific to Law Enforcement agent
            user.agent_id = agent_id
            user.save()

            # Log in the user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully signed up, Sign in to view Your dashboard.')
            # Redirect to the sign-in page
            return redirect('agent-signin')
        except IntegrityError:
            messages.success(request, "Username or email already exists. Please choose a different username/email.")
            return render(request, 'agent_signup.html', {})
    else:
        return render(request, 'agent_signup.html', {})



def agent_signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        agent_id = request.POST.get('AgentID')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if the user is a member of the Law Enforcement Agent group
            if user.groups.filter(name='Law Enforcement Agents').exists():
                login(request, user)
                return redirect('agent-portal')  # Redirect to home page after signin
            else:
                messages.success(request, "You are not authorized to access this page.")
        else:
            messages.success(request, "Invalid username, agent ID, or password.")

    else:
        messages.success(request, None)

    return render(request, 'agent_signin.html', {})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.success(request, 'Passwords do not match')
            return render(request, 'signup.html', {})

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.success(request, 'Username or email already taken')
            return render(request, 'signup.html', {})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'You have successfully signed up, Sign in to view Your dashboard')

        return redirect('signin')
    else:
        return render(request, 'signup.html', {})


def signin(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('citizen-portal')  
        else:
            messages.success(request, 'Invalid username or password')
            return render(request, 'signin.html', {})
    else:
        return render(request, 'signin.html', {})

@login_required(login_url='index')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully Logged Out...')
    return redirect('index')  

    
def anonymous_report(request):
    if request.method == 'POST':
        form = AnonymousReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your report has been submitted successfully. Thanks!')  # Add success message
            return redirect('index')  # Redirect to the index page after successful submission
    else:
        form = AnonymousReportForm()
    return render(request, 'anonymous.html', {'form': form})


@login_required(login_url='index')
def citizen_portal(request):
    if request.method == 'POST':
        form = CitizenReportForm(request.POST, request.FILES)  # Include request.FILES for handling file uploads
        if form.is_valid():
            # Associate the current user with the report before saving
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, 'A new report has been added')
            return redirect('citizen-portal')
    else:
        form = CitizenReportForm()
    citizen_reports = CitizenReport.objects.filter(user=request.user)
    context = {
        'citizen_reports': citizen_reports,
        'form': form,
    }
    return render(request, 'citizen.html', context)

@login_required(login_url='index')
def report(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		report = CitizenReport.objects.get(id=pk)
		return render(request, 'report.html', {'report':report})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('citizen-portal')
@login_required(login_url='index')     
def view_report(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		report = AnonymousReport.objects.get(id=pk)
		return render(request, 'view_report.html', {'report':report})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('agent-portal')
     
@login_required(login_url='index')
def delete_report(request, pk):
	if request.user.is_authenticated:
		delete_it = CitizenReport.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Report Deleted Successfully...")
		return redirect('citizen-portal')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('citizen-portal')
@login_required(login_url='index')    
def update_report(request, pk):
	if request.user.is_authenticated:
		report = CitizenReport.objects.get(id=pk)
		form = CitizenReportForm(request.POST or None, instance=report)
		if form.is_valid():
			form.save()
			messages.success(request, "Report Has Been Updated!")
			return redirect('citizen-portal')
		return render(request, 'update_report.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('index')

@login_required(login_url='index')
def update_status(request, pk):
    if request.user.groups.filter(name='Law Enforcement Agents').exists():
        report = get_object_or_404(CitizenReport, pk=pk)
        form = CitizenReportStatusForm(request.POST or None, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Report status has been updated successfully!")
            return redirect('agent-portal')
        return render(request, 'update_status.html', {'form': form, 'report': report})
    else:
        messages.error(request, "You must be logged in as a Law Enforcement Agent to perform this action.")
        return redirect('index')
    
def profile(request):
     
     return render(request, 'profile.html')

def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'update_profile.html', context)



@login_required(login_url='index')
def chat(request):
    # Check if user is an agent to determine UI
    is_agent = request.user.groups.filter(name='Law Enforcement Agents').exists()
    
    # Get recent messages for the user
    recent_messages = ChatMessage.objects.select_related('sender').order_by('-timestamp')[:50][::-1]
    
    context = {
        'is_agent': is_agent,
        'recent_messages': recent_messages,
    }
    return render(request, 'chat.html', context)
