from django.shortcuts import render, redirect
# from .models import UserSignup
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import os
import json
from datetime import date
from .models import addmahallumembers, addfamilymembers, masapirivu, pallifund, additionalfund, balance
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

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            response = redirect("dashboard")
            response.set_cookie("username", username)
            return response
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'myapp/login.html')

# def signup(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         # Check if the username already exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists!")
#             return render(request, "userlogin/signup.html")

#         try:
#             # Create a new user and save it to the database
#             user = User.objects.create_user(username=username, password=password)
#             user.save()  # Commit the user to the database
#             messages.success(request, "User created successfully! Please log in.")
#             return redirect("login")  # Redirect to the login page
#         except Exception as e:
#             messages.error(request, f"An error occurred: {e}")
#             return render(request, "userlogin/signup.html")

#     return render(request, 'myapp/signup.html')

def logout(request):
    response = redirect("login")
    response.delete_cookie('username')
    auth_logout(request)
    return response
    
@login_required
def index(request):
    return render(request, 'myapp/index.html')

@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'myapp/dashboard.html')

@login_required
def admin(request):
    return render(request, 'admin')

@login_required
def pallifund_view(request):

    if request.method == "POST":
        name = request.POST.get('name')
        id_no = request.POST.get('id_no')
        reciept_no = request.POST.get('reciept_no')
        main_fund_type = request.POST.get('fund_type')
        main_description = request.POST.get('description')
        main_amount = request.POST.get('amount')
        total_amount = request.POST.get('total_amount')
        debit_credit = request.POST.get('radio10')
        date = request.POST.get('date')

        # Save the main fund entry
        new_fund = pallifund(
            name=name,
            id_no=id_no,
            reciept_no=reciept_no,
            fund_type=main_fund_type,
            description=main_description,
            amount=main_amount,
            total_amount=total_amount,
            debit_credit=debit_credit,
            date=date
        )
        new_fund.save()

        # Use an incremental index to retrieve additional dynamic fields
        additional_funds = []
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

                additional_funds.append({
                    'fund_type': fund_type,
                    'description': description,
                    'amount': amount,
                })
                
            index += 1
            
        context = {
            'success': True,
            'submitted_data': {
                'id_no': id_no,
                'name': name,
                'reciept_no': reciept_no,
                'date': date,
                'main_fund': {
                    'fund_type': main_fund_type,
                    'description': main_description,
                    'amount': main_amount,
                },
                'total_amount': total_amount,
                'additional_funds': additional_funds,  # Dynamic fields included as a list
            }
        }
        print(f'context : {context}')
        return render(request, 'myapp/pallifund.html', context)
    return render(request, 'myapp/pallifund.html')


@login_required
def masapirivu_view(request):

    current_date = date.today().strftime('%Y-%m-%d')

    data = list(addmahallumembers.objects.values('id_no', 'name', 'father_name','house_name'))
    balances = list(balance.objects.all().values('id_no', 'balance'))
    masapirivu_data = list(masapirivu.objects.all().values('id_no', 'name', 'reciept_no'))

    

    if request.method == "POST":
        name = request.POST.get('name')
        id_no = request.POST.get('id_no')
        reciept_no = request.POST.get('reciept_no')
        palli = request.POST.get('palli')
        madrassa = request.POST.get('madrassa')
        mess = request.POST.get('mess')
        description = request.POST.get('description')
        total_amount = request.POST.get('total_amount')
        debit_credit = request.POST.get('radio10')
        balance_value = request.POST.get('balance')

        member = addmahallumembers.objects.get(id_no=id_no)
        father_name  = member.father_name
        house_name  = member.house_name

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
            date=current_date
        )
        new_fund.save()

        balance.objects.filter(id_no=id_no).delete()
        balance_amount = balance(
            id_no=id_no,
            balance=balance_value
        )
        balance_amount.save()

        context = {
            'data': json.dumps(data),
            # 'balances': json.dumps(balances),
            'balances': json.dumps(list(balance.objects.values('id_no', 'balance'))),
            'masapirivu_data': json.dumps(masapirivu_data),
            'success': True,
            'submitted_data': {
                'id_no': id_no,
                'name': name,
                'father_name': father_name,
                'house_name': house_name,
                'reciept_no': reciept_no,
                'date': current_date,
                'palli': palli,
                'madrassa': madrassa,
                'mess': mess,
                'description': description,
                'total_amount': total_amount,
            }
        }
        return render(request, 'myapp/masapirivu.html', context)

    return render(request, 'myapp/masapirivu.html', {
        'data': json.dumps(data),
        # 'balances': json.dumps(balances),
        'balances': json.dumps(list(balance.objects.values('id_no', 'balance'))),
        'masapirivu_data': json.dumps(masapirivu_data),
    })

@login_required
def add_members_view(request):
    if request.method == "POST":
        print(f"Request POST data: {request.POST}")

        # Main member details
        id_no = request.POST.get('id_no')
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        house_name = request.POST.get('house_name')
        family_members = request.POST.getlist('family_member')
        relations = request.POST.getlist('relation')
        phone = request.POST.getlist('phone_no')
        balance_value = request.POST.get('balance')

        # Save the main member
        new_member = addmahallumembers(
            id_no=id_no,
            name=name,
            father_name=father_name,
            house_name=house_name,
            family_member=family_members[0],
            relation=relations[0],
            phone_no=phone[0],
        )
        new_member.save()

        balance.objects.filter(id_no=id_no).delete()
        balance_amount = balance(
            id_no=id_no,
            balance=balance_value
        )
        balance_amount.save()

        # Save the additional family members
        for i in range(1, len(family_members)):
            new_family_member = addfamilymembers(
                id_no=id_no,
                family_member=family_members[i],
                relation=relations[i]
            )
            new_family_member.save()

        context = {
            'success': True
        }
        return render(request, 'myapp/add_members.html', context)

    return render(request, 'myapp/add_members.html')

@login_required
def individual_statement(request):
    id_no = request.GET.get('id_no')  # Get id_no from the query parameter
    if id_no:
        pallifund_data = pallifund.objects.filter(id_no=id_no)
        masapirivu_data = masapirivu.objects.filter(id_no=id_no)
        additionalfund_data = additionalfund.objects.all()
        addmahallumembers_data = addmahallumembers.objects.filter(id_no=id_no)
        addfamilymembers_data = addfamilymembers.objects.filter(id_no=id_no)
        balance_data = balance.objects.filter(id_no=id_no)

        print(f"id = {id_no}")

        for record in balance_data:
                print(f"Balance for ID {id_no}: {record.balance}")

        return render(request, 'myapp/individual_statement.html', {
            'id_no' : id_no,
            'pallifund_data': pallifund_data,
            'masapirivu_data': masapirivu_data,
            'additionalfund_data': additionalfund_data,
            'addmahallumembers_data': addmahallumembers_data,
            'addfamilymembers_data': addfamilymembers_data,
            'balance' : balance_data,    
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

@login_required
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

@login_required
def list_members(request):

    mahallumembers = addmahallumembers.objects.all()
    members = sorted(mahallumembers, key=lambda x: int(x.id_no))

    return render(request, 'myapp/list_members.html', {'mahallumembers': members})

@login_required
def list_masapirivu(request):

    data = masapirivu.objects.all()
    sorted_data = sorted(data, key=lambda x: int(x.id_no))

    mahallumembers = addmahallumembers.objects.all()

    fathersname_map = {member.id_no: member.father_name for member in mahallumembers}
    housename_map = {member.id_no: member.house_name for member in mahallumembers}

    # Add fathersname to each masapirivu entry
    for entry in sorted_data:
        entry.fathersname = fathersname_map.get(entry.id_no, "N/A")  # Default to "N/A" if not found
        entry.housename = housename_map.get(entry.id_no, "N/A")

    return render(request, 'myapp/list_masapirivu.html', {'sorted_data': sorted_data})

@login_required
def list_pallifund(request):

    data = pallifund.objects.all()
    # sorted_data = sorted(data, key=lambda x: int(x.id_no))
    sorted_data = sorted(data, key=lambda x: x.id_no)

    mahallumembers = addmahallumembers.objects.all()

    fathersname_map = {member.id_no: member.father_name for member in mahallumembers}
    housename_map = {member.id_no: member.house_name for member in mahallumembers}

    # Add fathersname to each masapirivu entry
    for entry in sorted_data:
        entry.fathersname = fathersname_map.get(entry.id_no, "N/A")  # Default to "N/A" if not found
        entry.housename = housename_map.get(entry.id_no, "N/A")

    return render(request, 'myapp/list_pallifund.html', {'sorted_data': sorted_data})


@login_required
def edit_member_details(request):
    id_no = request.GET.get('id_no')
    print(f"GET ID: {id_no}")

    if request.method == "POST":
        print(f"Request POST data: {request.POST}")

        id_no = request.POST.get('id_no')  # Keep ID consistent
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        house_name = request.POST.get('house_name')
        family_members = request.POST.getlist('family_member')
        relations = request.POST.getlist('relation')
        phone = request.POST.getlist('phone_no')
        balance_values = request.POST.getlist('balance')

        # Validate the POST data
        if not id_no or not family_members or not relations:
            print("Missing required data!")
            return render(
                request, 
                'myapp/edit_member_details.html', 
                {'error': 'Required fields are missing.'}
            )

        balance_value = balance_values[0] if balance_values else "0"  # Default balance if not provided

        # Ensure balance_value does not exceed the max length of 7
        if len(balance_value) > 7:
            print(f"Error: Balance value '{balance_value}' exceeds length limit.")
            return render(
                request,
                'myapp/edit_member_details.html',
                {'error': f"Balance value '{balance_value}' exceeds the allowed length."}
            )

        # Save the primary member to variable
        new_member = addmahallumembers(
            id_no=id_no,
            name=name,
            father_name=father_name,
            house_name=house_name,
            family_member=family_members[0],
            relation=relations[0],
            phone_no=phone[0],
        )

        # Delete process
        addmahallumembers.objects.filter(id_no=id_no).delete()
        addfamilymembers.objects.filter(id_no=id_no).delete()
        balance.objects.filter(id_no=id_no).delete()

        # Save the Relations
        new_member.save()
        # Save the Relations
        new_balance = balance(
            id_no=id_no,
            balance=balance_value,
        )

        new_balance.save()

        # Save the additional family members
        for i in range(1, len(family_members)):
            new_family_member = addfamilymembers(
                id_no=id_no,
                family_member=family_members[i],
                relation=relations[i]
            )
            new_family_member.save()

        # Redirect to the same page after processing POST
        return redirect(f'/edit_member_details/?id_no={id_no}')

    mahallumembers_data = addmahallumembers.objects.filter(id_no=id_no)
    familymembers_data = addfamilymembers.objects.filter(id_no=id_no)
    balance_data = balance.objects.filter(id_no=id_no).values()

    if balance_data.exists():  # Check if there's any data
        balance_list = list(balance_data)  # Convert QuerySet to a list
        print(f"Balance data found: {balance_list}")
    else:
        balance_list = [{"id": None, "id_no": id_no, "balance": "0"}]  # Pass default 0 balance if none
        print(f"No balance data found. Setting default: {balance_list}")

    return render(request, 'myapp/edit_member_details.html', {
        'mahallumembers_data': mahallumembers_data,
        'familymembers_data': familymembers_data,
        'balance': (balance_list),
    })

@login_required
def edit_masapirivu_details(request):
    reciept_no = request.GET.get('reciept_no')
    print(f"GET ID: {reciept_no}")

    if request.method == "POST":
        print(f"Request POST data: {request.POST}")

        id_no = request.POST.get('id_no')
        name = request.POST.get('name')
        date = request.POST.get('date')
        reciept_no = request.POST.get('reciept_no')
        palli_amount = request.POST.get('palli_amount')
        madrassa_amount = request.POST.get('madrassa_amount')
        mess_amount = request.POST.get('mess_amount')
        description = request.POST.get('description')
        total = request.POST.get('total')

        new_data = masapirivu(
            id_no=id_no,
            name=name,
            reciept_no =reciept_no ,
            palli=palli_amount,
            madrassa=madrassa_amount,
            mess=mess_amount,
            description=description,
            total_amount=total,
            date=date,
        )

        masapirivu.objects.filter(reciept_no=reciept_no).delete()

        new_data.save()
        

    masapirivu_data = masapirivu.objects.filter(reciept_no=reciept_no)

    return render(request, 'myapp/edit_masapirivu_details.html', {
        'masapirivu_data':masapirivu_data,
        })


