from django.shortcuts import render, redirect
# from .models import UserSignup
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os
from .models import addmahallumembers, addfamilymembers, masapirivu, pallifund, additionalfund
from django.shortcuts import get_object_or_404


@csrf_exempt
def service_worker(request):
    file_path = os.path.join(os.path.dirname(__file__), 'static', 'service-worker.js')
    with open(file_path, 'r') as file:
        response = HttpResponse(file.read(), content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/'
    return response


def login(request):
    if request.method == "POST":
        # Get the form data
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Use Django's authenticate function to check the username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentication successful
            auth_login(request, user)  # Log the user in (session is managed automatically)
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # Replace "home" with the name of your home URL pattern
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password.")

    return render(request, 'myapp/login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "userlogin/signup.html")

        try:
            # Create a new user and save it to the database
            user = User.objects.create_user(username=username, password=password)
            user.save()  # Commit the user to the database
            messages.success(request, "User created successfully! Please log in.")
            return redirect("login")  # Redirect to the login page
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, "userlogin/signup.html")

    return render(request, 'myapp/signup.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")
    
@login_required
def index(request):
    return render(request, 'myapp/index.html')

# @login_required
def dashboard(request):
    return render(request, 'myapp/dashboard.html')

# @login_required
def pallifund_view(request):
    if request.method == "POST":

        # Capture the static fields
        name = request.POST.get('name')
        id_no = request.POST.get('id_no')
        reciept_no = request.POST.get('reciept_no')
        fund_type = request.POST.get('fund_type')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        total_amount = request.POST.get('total_amount')
        debit_credit = request.POST.get('radio10')
        date = request.POST.get('date')

        # Save the main fund entry
        new_fund = pallifund(
            name=name,
            id_no=id_no,
            reciept_no=reciept_no,
            fund_type=fund_type,
            description=description,
            amount=amount,
            total_amount=total_amount,
            debit_credit=debit_credit,
            date=date
        )
        new_fund.save()

        # Use an incremental index to retrieve additional dynamic fields
        index = 1  # Start from 1
        while True:
            fund_type_key = f"fund_type{index}"
            description_key = f"description{index}"
            amount_key = f"amount{index}"

            fund_type = request.POST.get(fund_type_key)
            description = request.POST.get(description_key)
            amount = request.POST.get(amount_key)

            # Stop if there are no more fund_type fields
            if not fund_type:
                break

            # Save additional fund details if both fund_type and amount are present
            if fund_type and amount:
                new_fund_detail = additionalfund(
                    reciept_no=reciept_no,
                    fund_type=fund_type,
                    description=description,
                    amount=amount
                )
                new_fund_detail.save()
                print(f"Saved Fund Detail: {new_fund_detail}")

            # Increment to check the next set of fields
            index += 1

        messages.success(request, "Palli Fund entry saved successfully!")
        return redirect('pallifund')

    return render(request, 'myapp/pallifund.html')


# @login_required
def masapirivu_view(request):
    if request.method == "POST":

        # Main fields
        name = request.POST.get('name')
        id_no = request.POST.get('id_no')
        reciept_no = request.POST.get('reciept_no')
        palli = request.POST.get('palli')
        madrassa = request.POST.get('madrassa')
        mess = request.POST.get('mess')
        description = request.POST.get('description')
        total_amount = request.POST.get('total_amount')
        debit_credit = request.POST.get('radio10')
        date = request.POST.get('date')

        # Save the main fund record
        new_fund = masapirivu(
            name=name,
            id_no=id_no,
            reciept_no=reciept_no,
            palli=palli,
            madrassa=madrassa,
            mess=mess,
            description=description,
            total_amount=total_amount,
            debit_credit=debit_credit,
            date=date
        )
        new_fund.save()

        # Process dynamic fields
        fund_type_keys = [key for key in request.POST.keys() if key.startswith('fund_type')]
        description_keys = [key for key in request.POST.keys() if key.startswith('description')]
        amount_keys = [key for key in request.POST.keys() if key.startswith('amount')]

        for i in range(len(fund_type_keys)):  # Iterate over the dynamically added fields
            fund_type = request.POST.get(fund_type_keys[i])
            description = request.POST.get(description_keys[i])
            amount = request.POST.get(amount_keys[i])

            # Only save if both fund_type and amount are provided
            if fund_type and amount:
                new_fund_detail = additionalfund(
                    reciept_no=reciept_no,
                    fund_type=fund_type,
                    description=description,
                    amount=amount
                )
                new_fund_detail.save()
                print(f"Saved Fund Detail: {new_fund_detail}")

        messages.success(request, "Masa Pirivu Data saved successfully!")
        return redirect('masapirivu')

    return render(request, 'myapp/masapirivu.html')



# @login_required
def add_members_view(request):
    if request.method == "POST":
        print(f"Request POST data: {request.POST}")

        # Main member details
        id_no = request.POST.get('id_no')
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        house_name = request.POST.get('house_name')
        family_member = request.POST.get('family_member')
        relation = request.POST.get('relation')

        # Save the main member
        new_member = addmahallumembers(
            id_no=id_no,
            name=name,
            father_name=father_name,
            house_name=house_name,
            family_member=family_member,
            relation=relation
        )
        new_member.save()
        print(f"New member saved: {new_member}")

        # Initialize counters for incremental numeric keys
        index = 1
        
        while True:
            family_member_key = f'family_member{index}'
            relation_key = f'relation{index}'

            # Break the loop if neither key exists in POST data
            if family_member_key not in request.POST and relation_key not in request.POST:
                break

            # Get values from POST data
            family_member_name = request.POST.get(family_member_key)
            family_member_relation = request.POST.get(relation_key)

            # Debugging each pair
            print(f"Processing: {family_member_key} -> {family_member_name}, {relation_key} -> {family_member_relation}")

            if family_member_name and family_member_relation:  # Ensure both fields are present
                new_family_member = addfamilymembers(
                    id_no=id_no,
                    family_member=family_member_name,
                    relation=family_member_relation
                )
                new_family_member.save()
                print(f"Saved family member: {new_family_member}")

            # Increment the index
            index += 1

        messages.success(request, "Mahallu Members Added Successfully, including family members!")
        return redirect('add_members')

    return render(request, 'myapp/add_members.html')


# @login_required
def individual_statement(request):
    id_no = request.GET.get('id_no')  # Get id_no from the query parameter
    if id_no:
        pallifund_data = pallifund.objects.filter(id_no=id_no)
        masapirivu_data = masapirivu.objects.filter(id_no=id_no)
        additionalfund_data = additionalfund.objects.all()
        addmahallumembers_data = addmahallumembers.objects.filter(id_no=id_no)
        addfamilymembers_data = addfamilymembers.objects.filter(id_no=id_no)

        print("Palli Fund Data:")
        print(f"{id_no}")

        return render(request, 'myapp/individual_statement.html', {
            'id_no' : id_no,
            'pallifund_data': pallifund_data,
            'masapirivu_data': masapirivu_data,
            'additionalfund_data': additionalfund_data,
            'addmahallumembers_data': addmahallumembers_data,
            'addfamilymembers_data': addfamilymembers_data,
        })
    else:
        pallifund_data = pallifund.objects.all()
        masapirivu_data = masapirivu.objects.all()
        additionalfund_data = additionalfund.objects.all()

    return render(request, 'myapp/individual_statement.html', {
        'id_no': id_no,
        'pallifund_data': pallifund_data,
        'masapirivu_data': masapirivu_data,
        'additionalfund_data': additionalfund_data,
    })



# @login_required
def acc_statement(request):

    pallifund_data = pallifund.objects.all()
    masapirivu_data = masapirivu.objects.all()
    additionalfund_data = additionalfund.objects.all()

    print("Palli Fund Data:")
    for fund in pallifund_data:
        print(f"ID: {fund.id}, Name: {fund.name}, Receipt No: {fund.reciept_no}, Amount: {fund.amount}")

    return render(request, 'myapp/acc_statement.html', {
        'pallifund_data': pallifund_data,
        'masapirivu_data': masapirivu_data,
        'additionalfund_data': additionalfund_data,
    })

# @login_required
def list_members(request):

    mahallumembers = addmahallumembers.objects.all()
    members = sorted(mahallumembers, key=lambda x: int(x.id_no))

    # sorted_ids = [member.id_no for member in members]
    # print("Sorted Member ID_NOs:", sorted_ids)

    return render(request, 'myapp/list_members.html', {'mahallumembers': members})

# @login_required
def list_masapirivu(request):

    data = masapirivu.objects.all()
    sorted_data = sorted(data, key=lambda x: int(x.id_no))

    # sorted_ids = [member.id_no for member in members]
    # print("Sorted Member ID_NOs:", sorted_ids)

    return render(request, 'myapp/list_masapirivu.html', {'sorted_data': sorted_data})



