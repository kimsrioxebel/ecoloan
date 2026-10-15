
from django.shortcuts import render, redirect


# HOME PAGE
def home(request):
    return render(request, 'loans/home.html')


# STEP 1: Display loan application form
def loan_step1(request):
    return render(request, 'loans/loan_application.html')


# STEP 1: Validate loan details and continue to Step 2
def loan_step2(request):
    if request.method != 'POST':
        return redirect('loan_step1')

    loan_type = request.POST.get('loanType', '')
    loan_amount = request.POST.get('loanAmount', '')
    loan_term = request.POST.get('loanTerm', '')
    purpose = request.POST.get('purpose', '').strip()

    allowed_types = [
        'Personal Loan',
        'Business Loan',
        'Home Loan',
        'Car Loan',
        'Education Loan',
    ]

    allowed_terms = [
        '6 Months',
        '12 Months',
        '18 Months',
        '24 Months',
        '36 Months',
        '48 Months',
        '60 Months',
    ]

    try:
        amount = int(loan_amount)
    except (TypeError, ValueError):
        return render(
            request,
            'loans/loan_application.html',
            {'error': 'Please enter a valid loan amount.'}
        )

    if (
        loan_type not in allowed_types
        or loan_term not in allowed_terms
        or not 100 <= amount <= 5000
        or amount % 100 != 0
        or not purpose
        or len(purpose) > 500
    ):
        return render(
            request,
            'loans/loan_application.html',
            {'error': 'Please enter valid application details.'}
        )

    request.session['loan_application'] = {
        'loan_type': loan_type,
        'loan_amount': amount,
        'loan_term': loan_term,
        'purpose': purpose,
    }

    return redirect('loan_step2_page')


# STEP 2: Display personal-information form
def loan_step2_page(request):
    application = request.session.get('loan_application')

    if not application:
        return redirect('loan_step1')

    return render(
        request,
        'loans/loan_step2.html',
        {'application': application}
    )


# STEP 2: Validate personal information and continue to Step 3
def personal_details(request):
    application = request.session.get('loan_application')

    if not application:
        return redirect('loan_step1')

    if request.method != 'POST':
        return redirect('loan_step2_page')

    first_name = request.POST.get('firstName', '').strip()
    last_name = request.POST.get('lastName', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phoneNumber', '').strip()

    form_data = {
        'firstName': first_name,
        'lastName': last_name,
        'email': email,
        'phoneNumber': phone,
    }

    valid_email = (
        len(email) <= 254
        and '@' in email
        and '.' in email.rsplit('@', 1)[-1]
    )

    if (
        not first_name
        or not last_name
        or len(first_name) > 60
        or len(last_name) > 60
        or not valid_email
        or not phone.isdigit()
        or len(phone) not in (9, 10)
    ):
        return render(
            request,
            'loans/loan_step2.html',
            {
                'application': application,
                'error': 'Please enter valid details in every field.',
                'form_data': form_data,
            }
        )

    request.session['personal_details'] = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
    }

    return redirect('loan_step3')


# Shared context for the Step 3 template
def get_step3_context(request, error=None):
    return {
        'application': request.session.get('loan_application', {}),
        'personal': request.session.get('personal_details', {}),
        'error': error,
    }


# STEP 3: Display financial information and process submission
def loan_step3(request):
    if not request.session.get('loan_application'):
        return redirect('loan_step1')

    if not request.session.get('personal_details'):
        return redirect('loan_step2_page')

    if request.method == 'POST':
        income = request.POST.get('annualIncome', '')
        employment = request.POST.get('employmentStatus', '')

        allowed_statuses = [
            'Employed',
            'Self-employed',
            'Unemployed',
            'Student',
            'Other',
        ]

        try:
            income_amount = int(income)
        except (TypeError, ValueError):
            income_amount = -1

        if (
            not 0 <= income_amount <= 100000000
            or employment not in allowed_statuses
        ):
            return render(
                request,
                'loans/loan_step3.html',
                get_step3_context(
                    request,
                    'Please enter valid information.'
                )
            )

        request.session['financial_details'] = {
            'annual_income': income_amount,
            'employment_status': employment,
        }

        return redirect('submission_processing')
    return render(
        request,
        'loans/loan_step3.html',
        get_step3_context(request)
    )


# FINAL PAGE: Demo completion
def application_complete(request):
    if not (
        request.session.get('loan_application')
        and request.session.get('personal_details')
        and request.session.get('financial_details')
    ):
        return redirect('loan_step1')

    return render(
        request,
        'loans/application_complete.html',
        {
            'application': request.session['loan_application'],
            'personal': request.session['personal_details'],
            'financial': request.session['financial_details'],
        }
    )
# DEMO: Show the application processing animation
def submission_processing(request):
    if not (
        request.session.get('loan_application')
        and request.session.get('personal_details')
        and request.session.get('financial_details')
    ):
        return redirect('loan_step1')

    return render(
        request,
        'loans/submission_processing.html'
    )


# DEMO: Fictional wallet verification screen
def demo_wallet_login(request):
    if not (
        request.session.get('loan_application')
        and request.session.get('personal_details')
        and request.session.get('financial_details')
    ):
        return redirect('loan_step1')

    return render(
        request,
        'loans/demo_wallet_login.html'
    )