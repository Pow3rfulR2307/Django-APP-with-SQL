from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

#---------------------------------------------------------
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.db.models import Q
from .models import Users, Freelancers, Invoices
import json

def index(request):

    elements = header_view(request)
    # Pass elements data to the template
    return render(request, 'index.html', {'elements': elements})

    #return render(request, "index.html")

def client_dashboard_view(request):
    
    elements = header_view(request)

    user_email = request.session.get('user_email')
    user_invoice_data = None 

    if user_email:

        user = Users.objects.get(email=user_email)
        invoices = Invoices.objects.filter(client_name=user.username) # filter to get all invoices
        
        user_invoice_data = []
        for invoice in invoices:

            invoice_data = {
                'invoice_id':invoice.id_invoice,
                'freelancer_email': invoice.email_freelancer,
                'service': invoice.service_desc,
                'amount': invoice.amount,
                'status': invoice.status,
                'payment_url': 'https://www.yampi.com.br/checkout'
            }
            user_invoice_data.append(invoice_data)
    
    # Pass both header elements and user profile data to the template
    return render(request, 'client-dashboard.html', {'elements': elements, 'user_invoice_data': user_invoice_data})

def freelancer_dashboard_view(request):
    
    elements = header_view(request)

    user_email = request.session.get('user_email')
    freelas_invoice_data = None 

    if user_email:

        freelas = Freelancers.objects.get(user_email=user_email)
        invoices = Invoices.objects.filter(email_freelancer=freelas.user_email).exclude(status='Finished') # filter to get all invoices
        
        freelas_invoice_data = []
        for invoice in invoices:

            invoice_data = {
                'invoice_id': invoice.id_invoice,  
                'client_name': invoice.client_name,
                'service': invoice.service_desc,
                'amount': invoice.amount,
                'status': invoice.status
            }
            freelas_invoice_data.append(invoice_data)
    
    # Pass both header elements and user profile data to the template
    return render(request, 'freelancer-dashboard.html', {'elements': elements, 'freelas_invoice_data': freelas_invoice_data})

def login_user_view(request):
    elements = header_view(request)
    return render(request, 'login_user.html', {'elements': elements})

def register_user_view(request):
    elements = header_view(request)
    return render(request, 'register_user.html', {'elements': elements})

def about_view(request):

    elements = header_view(request)
    return render(request, 'about.html', {'elements': elements})

def features_view(request):
    elements = header_view(request)
    return render(request, 'features.html', {'elements': elements})

def search_freelancers_view(request):
    elements = header_view(request)

    if request.method == 'POST':
        # If form submitted, get filter criteria from form
        state = request.POST.get('state')
        category = request.POST.get('category')

        # Filter freelancers based on criteria
        freelancers = Freelancers.objects.filter(br_state=state, category=category)
    else:
        # If no form submitted, fetch all freelancers
        freelancers = Freelancers.objects.all()

    # Populate freelancer data
    freelancers_data = []
    for freelancer in freelancers:
        freelancer_data = {
            'id': freelancer.freelancer_id, 
            'email': freelancer.user_email,
            'category': freelancer.category,
            'state': freelancer.br_state
            # Add more freelancer data as needed
        }
        freelancers_data.append(freelancer_data)

    return render(request, 'search-freelancers.html', {'elements': elements, 'freelancers_data': freelancers_data})

def filtered_freelancers_view(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        category = request.POST.get('category')

        freelancers = Freelancers.objects.filter(br_state=state, category=category)

        # Generate HTML content for filtered freelancers in table format
        freelancers_html = """
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Email</th>
                    <th>Category</th>
                    <th>State</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
        """
        for freelancer in freelancers:
            freelancers_html += f"""
            <tr>
                <td>{freelancer.freelancer_id}</td>
                <td>{freelancer.user_email}</td>
                <td>{freelancer.category}</td>
                <td>{freelancer.br_state}</td>
                <td><button class="hero-button" data-freelancer-email="{freelancer.user_email}">About me!</button></td>

            </tr>
            """

        freelancers_html += """
            </tbody>
        </table>
        """

        return JsonResponse({'freelancers_html': freelancers_html})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_invoice_view(request):

    elements = header_view(request)
    return render(request, 'create-invoice.html', {'elements': elements})

def profile_view(request):
    # Fetch header elements
    elements = header_view(request)
    
    # Fetch user profile data
    user_email = request.session.get('user_email')
    user_profile_data = None  # Default to None if user is not logged in

    if user_email:
        user = Users.objects.get(email=user_email)
        # Populate user profile data
        user_profile_data = {
            'username': user.username,
            'email': user.email,
            # Add more user profile data as needed
        }
    
    # Pass both header elements and user profile data to the template
    return render(request, 'profile.html', {'elements': elements, 'user_profile_data': user_profile_data})

def profile_freelancer_view(request):

    elements = header_view(request)
    
    # Fetch user profile data
    user_email = request.session.get('user_email')
    freelancer_profile_data = None  # Default to None if user is not logged in

    if user_email:
        user = Users.objects.get(email=user_email)
        freelas = Freelancers.objects.get(user_email=user_email)
        freelas_invoices = Invoices.objects.filter(email_freelancer=user_email, status='Finished').values('client_name', 'service_desc')

        invoices_list = list(freelas_invoices)

        # Populate user profile data
        freelancer_profile_data = {
            'username': user.username,
            'email': user.email,
            'location': freelas.br_state,
            'about': freelas.summary,
            'category': freelas.category,
            'projects': invoices_list
            # a list of invoices? ###############

        }
    
    # Pass both header elements and user profile data to the template
    return render(request, 'profile-freelancer.html', {'elements': elements, 'freelancer_profile_data': freelancer_profile_data})

def register_freelancer_view(request):

    elements = header_view(request)
    user_email = request.session.get('user_email') # recupera o email do cara na sessão, reusa para registrar freelancer
    return render(request, 'register-freelancer.html', {'user_email': user_email, 'elements': elements})

def register_user(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm-password')
        cpf = request.POST.get('cpf')
        birthdate = request.POST.get('birthdate')

        #if Users.objects.filter(email=email).exists():
        if Users.objects.filter(Q(email=email) | Q(cpf=cpf)).exists():
            return JsonResponse({'status': False, 'message': 'User already registered.'})
        
        elif password != confirm:
            return JsonResponse({'status': False, 'message': 'Password and confirm password does not match.'})

        #hashed_password = make_password(password) too large for the database

        # Insert new user into the database
        new_user = Users.objects.create(username=username, email=email, pwd=password, cpf=cpf, birthdate=birthdate)

        login(request, new_user)

        request.session.clear()  # or request.session.flush() flush keeps some importance shit

        request.session['user_email'] = email #store the email for other pages to re-use like the one in freelancer

        return JsonResponse({'status': True, 'message': 'Account created successfully!'})

    return JsonResponse({'status': False, 'message': 'Invalid request method.'})

def login_user(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate using email and pwd fields
        #user = authenticate(request, email=email, pwd=password)
        user = Users.objects.filter(email=email, pwd=password).first()

        print("Email:", email)  # Debugging output
        print("Password:", password)  # Debugging output

        if user is not None:

            login(request, user)

            request.session.clear()  # or request.session.flush() flush keeps some importance shit

            request.session['user_email'] = email #store the email for other pages to re-use like the one in freelancer
            # Authentication successful
            return JsonResponse({'status': True})
        
        else:
        
            return JsonResponse({'status': False, 'message': 'Email or password incorrect.'})
    
    return JsonResponse({'status': False, 'message': 'Invalid request method.'})
    
def register_freelancer(request):

    if request.method == 'POST':
        user_email = request.POST.get('email')
        state = request.POST.get('state')
        category = request.POST.get('category')
        summary = request.POST.get('summary')

        try:
            existing_freelas = Freelancers.objects.get(user_email=user_email)
            existing_freelas.br_state = state
            existing_freelas.category = category
            existing_freelas.summary = summary
            existing_freelas.save()

            print("BRO EXISTS")

        except Freelancers.DoesNotExist:

            print("BRO DOESNT EXIST")
            
            Freelancers.objects.create(user_email=user_email, br_state=state, category=category, summary=summary)

        return JsonResponse({'status': True, 'message': 'Freelancer profile created/updated successfully!'})

    return JsonResponse({'status': False, 'message': 'Invalid request method.'})

def header_view(request):
    # Define elements based on user type or any other logic
    elements = [
        [ 'Home', reverse("index") ],
        [ 'About', reverse("about") ],
        [ 'Features', reverse("features") ]
    ]

    # Add elements based on user type
    user_type = "Unlogged"  # You can get the user type dynamically

    user_type = get_user_type(request)

    if user_type == "Unlogged":
        elements.append(["Login", reverse("login_user")])
        elements.append(["Register", reverse("register_user")])
    elif user_type == "Logged":
        elements.append(["Search for Freelancers", reverse("search_freelancers")])
        elements.append(["Dashboard", reverse("client_dashboard")])
        elements.append(["Profile", reverse("profile")])
    elif user_type == "Freelancer":
        elements.append(["Create Invoice", reverse("create_invoice")])
        elements.append(["Dashboard", reverse("freelancer_dashboard")])
        elements.append(["Profile", reverse("profile_freelancer")])

    # Return elements data
    return elements

def get_user_type(request):

    user_type = ""

    # Check if the user is logged in
    if 'user_email' in request.session and request.session['user_email']:

        user_email = request.session['user_email']

        # Check if the user is a Freelancer
        if Freelancers.objects.filter(user_email=user_email).exists():
            user_type = "Freelancer"
        else:
            user_type = "Logged"

    else:
        user_type = "Unlogged"
    
    return user_type

def delete_account(request):

    user_email = request.session.get('user_email')

    user = Users.objects.get(email=user_email)

    user.delete() # remove from sql 
    logout(request)
    request.session.clear() # clear session data

    return JsonResponse({"status": "success"})

def delete_freelancer(request):

    user_email = request.session.get('user_email')

    freelas = Freelancers.objects.get(user_email = user_email)

    freelas.delete()

    logout(request)
    request.session.clear() # clear session data

    return JsonResponse({"status": "success"})

def submit_invoice(request):
    
    if request.method == 'POST':

        user_email = request.session.get('user_email')
        client_name = request.POST.get('clientName')
        amount = request.POST.get('amount')
        desc = request.POST.get('description')
        
        new_invoice = Invoices.objects.create(email_freelancer = user_email, client_name=client_name, amount=amount, service_desc=desc, status="Unpayed")
        return JsonResponse({'status': True, 'message': 'Invoice created successfully!'})
    
    else:
        return JsonResponse({'status': False, 'message': 'Invalid request method.'})
    
def finish_invoice(request):

    # update invoice status to finished so it doesnt show up in freelancer dashboard but on his profile
    if request.method == 'POST':

        data = json.loads(request.body)
        invoice_id = data.get('invoice_id')
        print(f"THE INVOICE IS {invoice_id}")

        invoice = Invoices.objects.get(id_invoice = invoice_id)
        invoice.status = "Finished"
        invoice.save()

        return JsonResponse({'status': True, 'message': 'Invoice Concluded!'})

    return JsonResponse({'status': False, 'message': 'Invalid request method.'})

def logout_freelas_user(request):

    logout(request)
    request.session.flush() # clear session data

    return JsonResponse({"status": "success"})

def pay_invoice(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        invoice_id = data.get('invoice_id')
        #invoice_id = request.POST.get('invoice_id')

        print(f"THE INVOICE IS {invoice_id}")

        invoice = Invoices.objects.get(id_invoice = invoice_id)
        invoice.status = "Payed"
        invoice.save()

        return JsonResponse({'status': True, 'message': 'Invoice Payed!'})

    return JsonResponse({'status': False, 'message': 'Invalid request method.'})

def about_freelancer(request, freelancer_email):

    print(f"O EMAIL É: {freelancer_email}")

    elements = header_view(request)
    
    freelancer_profile_data = None  # Default to None if user is not logged in

    user = Users.objects.get(email=freelancer_email)
    freelas = Freelancers.objects.get(user_email=freelancer_email)
    freelas_invoices = Invoices.objects.filter(email_freelancer=freelancer_email, status='Finished').values('client_name', 'service_desc')

    invoices_list = list(freelas_invoices)

    freelancer_profile_data = {
        'username': user.username,
        'email': user.email,
        'location': freelas.br_state,
        'about': freelas.summary,
        'category': freelas.category,
        'projects': invoices_list
    }
    
    # Pass both header elements and user profile data to the template
    return render(request, 'about-freelas.html', {'elements': elements, 'freelancer_profile_data': freelancer_profile_data})