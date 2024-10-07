from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user1.models import *

@api_view(['GET'])
def mock_cibil_score(request):
    mock_data = [
        {
            "pan_number": "ABCDE1234F",
            "dob": "1985-05-20",
            "client_name": "John Doe",
            "score": 780,
            "score_date": "2024-01-15",
            "credit_limit": 500000.00,
            "outstanding_balance": 150000.00
        },
        {
            "pan_number": "FGHIJ5678K",
            "dob": "1990-07-10",
            "client_name": "Jane Smith",
            "score": 720,
            "score_date": "2024-02-10",
            "credit_limit": 400000.00,
            "outstanding_balance": 100000.00
        },
        {
            "pan_number": "LMNOP1234Q",
            "dob": "1978-11-15",
            "client_name": "anu",
            "score": 750,
            "score_date": "2024-03-05",
            "credit_limit": 300000.00,
            "outstanding_balance": 200000.00
        },
        {
            "pan_number": "QRSTU6789V",
            "dob": "1995-03-25",
            "client_name": "Emily Davis",
            "score": 810,
            "score_date": "2024-04-18",
            "credit_limit": 600000.00,
            "outstanding_balance": 50000.00
        },
        {
            "pan_number": "WXYZ1234A",
            "dob": "1988-09-30",
            "client_name": "Michael Johnson",
            "score": 740,
            "score_date": "2024-05-22",
            "credit_limit": 450000.00,
            "outstanding_balance": 120000.00
        },
 {
        "pan_number": "ABCD5678K",
        "dob": "1990-03-15",
        "client_name": "Anand Menon",
        "score": 785,
        "score_date": "2024-07-10",
        "credit_limit": 600000.00,
        "outstanding_balance": 150000.00
    },
    {
        "pan_number": "EFGH2345L",
        "dob": "1985-11-25",
        "client_name": "Nikhil Nair",
        "score": 720,
        "score_date": "2024-06-01",
        "credit_limit": 500000.00,
        "outstanding_balance": 180000.00
    },
    {
        "pan_number": "IJKL6789M",
        "dob": "1992-02-12",
        "client_name": "Deepa Krishnan",
        "score": 765,
        "score_date": "2024-04-18",
        "credit_limit": 350000.00,
        "outstanding_balance": 90000.00
    },
    {
        "pan_number": "MNOP3456N",
        "dob": "1989-07-08",
        "client_name": "Ravi Pillai",
        "score": 810,
        "score_date": "2024-08-30",
        "credit_limit": 700000.00,
        "outstanding_balance": 200000.00
    },
    {
        "pan_number": "QRST1234P",
        "dob": "1995-05-20",
        "client_name": "Meera Thomas",
        "score": 730,
        "score_date": "2024-09-05",
        "credit_limit": 400000.00,
        "outstanding_balance": 120000.00
    },
    {
        "pan_number": "UVWX9876Q",
        "dob": "1987-01-10",
        "client_name": "Sreejith Kumar",
        "score": 750,
        "score_date": "2024-03-15",
        "credit_limit": 550000.00,
        "outstanding_balance": 130000.00
    },
    {
        "pan_number": "YZAB4321R",
        "dob": "1991-04-22",
        "client_name": "Aishwarya Rajan",
        "score": 795,
        "score_date": "2024-02-28",
        "credit_limit": 620000.00,
        "outstanding_balance": 170000.00
    },
    {
        "pan_number": "CDEF8765S",
        "dob": "1984-09-17",
        "client_name": "Manoj Varma",
        "score": 780,
        "score_date": "2024-07-21",
        "credit_limit": 480000.00,
        "outstanding_balance": 110000.00
    },
    {
        "pan_number": "GHIJ5432T",
        "dob": "1993-06-05",
        "client_name": "Lekshmi Menon",
        "score": 770,
        "score_date": "2024-08-12",
        "credit_limit": 520000.00,
        "outstanding_balance": 95000.00
    },
    {
        "pan_number": "KLMN2109U",
        "dob": "1988-12-30",
        "client_name": "Ajith Sankar",
        "score": 800,
        "score_date": "2024-09-14",
        "credit_limit": 650000.00,
        "outstanding_balance": 140000.00
    }


    ]
    name=request.GET.get('name')
    pan_number = request.GET.get('pan_number')
    dob = request.GET.get('dob')
    print(f"Received Name: {name}")
    print(f"Received PAN: {pan_number}")
    print(f"Received DOB: {dob}")


    client_data = next((i for i in mock_data if i['pan_number'] == pan_number and i['dob'] == dob and i['client_name']==name), None)

    if client_data:
        elgible=client_data['score']>=700
        a={
            'cibilscore':client_data,
            'elgible':elgible
        }
        return render(request,'score.html',a)
    else:
        return JsonResponse({"error": "No data found for the provided PAN and DOB"}, status=404)
    
def loanform(request):
    return render(request,'loanapply.html')






