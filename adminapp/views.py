from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from . models import *
from user1.models import *
import datetime
from django.utils.timezone import now
from datetime import date,timedelta
import braintree
# Create your views here.
def LAFapply(request):
    if request.method == 'POST':
        try:
            name1 = request.POST.get('name')
            email1 = request.POST.get('email')
            phone1 = request.POST.get('phone')
            dob1 = request.POST.get('dob')
            address1 = request.POST.get('address')
            gender1 = request.POST.get('gender')
            emp1 = request.POST.get('emp')
            pan1 = request.POST.get('pan')
            panimage1 = request.FILES.get('panimage')
            income1 = request.FILES.get('income')
            loan1 = request.POST.get('amount')

            user1 = user_reg.objects.get(email=email1)
            laf = LAF.objects.create(
                profile=user1,
                employement_type=emp1,
                pannumber=pan1,
                panimage=panimage1,
                incomeproof=income1,
                loanamount=loan1
            )
            laf.save()
            return render(request, 'loanalert.html')
        except user_reg.DoesNotExist:
            return render(request, 'loanapply.html', {'error_3': 'User does not exist.'})
        except Exception as e:
            return render(request, 'loanapply.html', {'error_3': f'Something went wrong: {str(e)}'})

    return render(request, 'loanapply.html')

def adminlogin(request):
    if request.method == 'POST':
        adminid = request.POST.get('email')
        password1 = request.POST.get('pass')
        try:
            obj = admini.objects.filter(empid=adminid, password=password1)
            if obj:
                request.session['user_id'] = obj.first().id
                return render(request, 'adminindex.html', {'name': obj.first().name})
            else:
                return render(request, 'adminlogin.html', {'error_2': 'Invalid Email or Password..'})
        except Exception as e:
            return render(request, 'adminlogin.html', {'error_2': f'An error occurred: {str(e)}'})
    return render(request, 'adminlogin.html')

def customerdetails(request):
    try:
        obj = user_reg.objects.all()
        return render(request, 'customerdetails.html', {'obj': obj})
    except Exception as e:
        return render(request, 'customerdetails.html', {'error': f'An error occurred: {str(e)}'})

def customerapplication(request):
    try:
        undistributed_loans = LAF.objects.exclude(id__in=Loandisbursed.objects.values_list('profile_id', flat=True))
        return render(request, 'customerapplications.html', {'obj': undistributed_loans})
    except Exception as e:
        return render(request, 'customerapplications.html', {'error': f'An error occurred: {str(e)}'})

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return render(request, 'index.html')

def approvemail(request, id1):
    if request.method == 'GET':
        try:
            obj = LAF.objects.get(id=id1)
            r = 10 / (12 * 100)
            b = (1 + r) ** 24
            p = int(obj.loanamount)
            c = (p * r * b) / (b - 1)
            emi = c
            subject = 'Loan Application Approved'
            message = (f"Dear {obj.profile.name},\n\n"
                       f"We are pleased to inform you that your loan application has been approved. "
                       f"You have been approved for a loan amount of {obj.loanamount}.\n\n"
                       f"The monthly EMI for your loan will be {emi}. Payments will start on the 2nd of [Start Month], [Start Year]. "
                       f"The EMI payments will continue on the 2nd of every month for the next 2 years.\n\n"
                       f"If you have any questions or need further assistance, please feel free to contact us.\n\n"
                       f"Thank you for choosing CONSLOAN. We look forward to assisting you.\n\n"
                       f"Best regards,\n"
                       f"CONSLOAN Team")
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.profile.email], fail_silently=False)
            Loandisbursed.objects.create(profile=obj, Dateofapproval=date.today(), EMI=emi)
            return render(request, 'adminindex.html')
        except LAF.DoesNotExist:
            return HttpResponse("Loan Application not found.", status=404)
        except Exception as e:
            return HttpResponse(f"Failed to send email: {str(e)}", status=500)

def rejectemail(request, id1):
    if request.method == 'GET':
        try:
            obj = LAF.objects.get(id=id1)
            subject = 'Loan Application Rejected'
            message = (f"Dear {obj.profile.name},\n\n"
                       f"We regret to inform you that your loan application has been rejected. "
                       f"If you have any questions or need further assistance, please feel free to contact us.\n\n"
                       f"Thank you for choosing CONSLOAN. We look forward to assisting you.\n\n"
                       f"Best regards,\n"
                       f"CONSLOAN Team")
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.profile.email], fail_silently=False)
            obj.delete()
            return render(request, 'adminindex.html')
        except LAF.DoesNotExist:
            return HttpResponse("Loan Application not found.", status=404)
        except Exception as e:
            return HttpResponse(f"Failed to send email: {str(e)}", status=500)

def customerdisbursed(request):
    try:
        obj = Loandisbursed.objects.all()
        return render(request, 'customerdisbursed.html', {'obj': obj})
    except Exception as e:
        return render(request, 'customerdisbursed.html', {'error': f'An error occurred: {str(e)}'})

def myaccounts(request):
    userid = request.session.get('user_id')
    if userid:
        try:
            a = user_reg.objects.filter(id=userid).first()
            b = LAF.objects.filter(profile=a).first()
            c = Loandisbursed.objects.filter(profile=b)
            if c:
                r = 10 / (12 * 100)
                d = (1 + r) ** 24
                p = int(b.loanamount)
                emi = int((p * r * d) / (d - 1))
                disp = c.first()
                num = Emipayment.objects.filter(emi=disp)
                num_emi = sum(i.No_of_Payments for i in num if i.No_of_Payments is not None)
                return render(request, 'myaccounts.html', {'obj': c, 'emi': emi, 'noemi': num_emi})
            else:
                return render(request, 'myaccounts.html')
        except Exception as e:
            return render(request, 'myaccounts.html', {'error': f'An error occurred: {str(e)}'})
    return redirect('signin')  # Redirect to sign-in if user is not logged in

# Braintree Configuration
braintree.Configuration.configure(
    environment=braintree.Environment.Sandbox if settings.BRAINTREE_ENVIRONMENT == 'sandbox' else braintree.Environment.Production,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC_KEY,
    private_key=settings.BRAINTREE_PRIVATE_KEY
)

def payment(request, id1):
    try:
        obj = Loandisbursed.objects.get(id=id1)
        amount = int(obj.EMI)
        paid = {'amount': amount, 'currency': 'INR', 'payment_capture': '1'}
        order = braintree.ClientToken.generate()
        payment = Emipayment.objects.create(emi=obj, amount=amount, status='Pending')
        context = {
            'order': order,
            'amount': amount,
            'emi_id': obj.id,
            'payment_id': payment.id
        }
        return render(request, 'paymentindex.html', context)
    except Loandisbursed.DoesNotExist:
        return HttpResponse("Loan not found.", status=404)
    except Exception as e:
        return render(request, 'paymentindex.html', {'error': f'An error occurred: {str(e)}'})

def paymentsuccess(request):
    nonce = request.POST.get('payment_method_nonce')
    amount = request.POST.get('amount')
    paymentid = request.POST.get('payment_id')
    emiid = request.POST.get('emi_id')

    try:
        emipayment = Emipayment.objects.get(id=paymentid)
        result = braintree.Transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })
        if result.is_success:
            if emipayment.No_of_Payments < 24:
                emipayment.No_of_Payments += 1
                emipayment.status = 'Success'
                emipayment.save()
                return render(request, 'paymentsuccess.html', {'success': True, 'transaction_id': result.transaction.id})
            else:
                return render(request, 'paymentsuccess.html', {
                    'success': False,
                    'message': 'Maximum number of payments reached.'
                })
        else:
            emipayment.status = 'Failed'
            emipayment.save()
            return render(request, 'paymentsuccess.html', {'success': False})
    except Emipayment.DoesNotExist:
        return HttpResponse("Payment record not found.", status=404)
    except Exception as e:
        return render(request, 'paymentsuccess.html', {'success': False, 'error': str(e)})

def pendingemi(request):
    pending = []
    try:
        obj = Loandisbursed.objects.all()
        for i in obj:
            daysafterapproval = (now().date() - i.Dateofapproval).days
            requiredcount = daysafterapproval // 1
            actualcount = Emipayment.objects.filter(emi=i, status='Success').count()
            if requiredcount > actualcount:
                pending.append({
                    'profile': i.profile,
                    'emi': i.EMI,
                    'dateofapproval': i.Dateofapproval,
                    'actualcount': actualcount,
                    'requiredcount': requiredcount
                })
        context = {'pending': pending}
        return render(request, 'pendingemi.html', context)
    except Exception as e:
        return render(request, 'pendingemi.html', {'error': f'An error occurred: {str(e)}'})

def empreg(request):
    if request.method == 'POST':
        try:
            name1 = request.POST.get('name')
            address1 = request.POST.get('address')
            dob1 = request.POST.get('dob')
            gender1 = request.POST.get('gender')
            email1 = request.POST.get('email')
            empid1 = request.POST.get('empid')
            phone1 = request.POST.get('phone')
            pass1 = request.POST.get('pass')
            confirmpass = request.POST.get('pass1')

            if employee.objects.filter(email=email1).exists():
                return render(request, 'empreg.html', {'error_1': 'Employee Email Already Exists!!!'})
            if pass1 == confirmpass:
                obj1 = employee.objects.create(
                    name=name1,
                    address=address1,
                    dob=dob1,
                    gender=gender1,
                    email=email1,
                    password=confirmpass,
                    empid=empid1,
                    phone=phone1
                )
                obj1.save()
                return render(request, 'adminindex.html')
            else:
                return render(request, 'empreg.html', {'error_2': 'Passwords do not match.'})
        except Exception as e:
            return render(request, 'empreg.html', {'error_2': f'An error occurred: {str(e)}'})

    return render(request, 'empreg.html')

def empdetails(request):
    try:
        obj = employee.objects.all()
        return render(request, 'empdetails.html', {'obj': obj})
    except Exception as e:
        return render(request, 'empdetails.html', {'error': f'An error occurred: {str(e)}'})

def empapplications(request):
    try:
        obj1 = Loandisbursed.objects.values_list('profile_id', flat=True)
        obj = LAF.objects.exclude(id__in=obj1).filter(empid__isnull=False)
        return render(request, 'empapplications.html', {'obj': obj})
    except Exception as e:
        return render(request, 'empapplications.html', {'error': f'An error occurred: {str(e)}'})
