
from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Step 1: Loan application details
    path(
        'apply/',
        views.loan_step1,
        name='loan_step1'
    ),
    path(
        'apply/step-2/',
        views.loan_step2,
        name='loan_step2'
    ),

    # Step 2: Personal information
    path(
        'apply/step-2/details/',
        views.loan_step2_page,
        name='loan_step2_page'
    ),
    path(
        'apply/personal-details/',
        views.personal_details,
        name='personal_details'
    ),

    # Step 3: Financial information
    path(
        'apply/step-3/',
        views.loan_step3,
        name='loan_step3'
    ),

    # Final demo completion page
    path(
        'apply/complete/',
        views.application_complete,
        name='application_complete'
    ),

    path(
    'apply/processing/',
    views.submission_processing,
    name='submission_processing'
),
path(
    'demo-wallet/',
    views.demo_wallet_login,
    name='demo_wallet_login'
),
]