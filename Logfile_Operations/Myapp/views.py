from django.shortcuts import render
from .models import Register,User_Register,Forgot_Password
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import pandas as pd
from io import StringIO
from django.shortcuts import render
from django.http import HttpResponse
from collections import defaultdict
from django.http import JsonResponse
import re,io,csv,os,random

from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def Register(request):
    if request.method == 'POST':
        User_Name=request.POST['user_name']
        Email=request.POST['email']
        Password=request.POST['password']
        print(User_Name,Email,Password)
        Register_Data=User_Register(Name=User_Name,Email=Email,Password=Password)
        Register_Data.save()
        return render(request,'login.html')
        # return render(request,'Register.html',{"Status_Message":"Registration Completed Successfully"})
    # return render(request,'Register.html')
    return render(request,'createAccount.html')
def User_Login(request):
    request.session['csv_data']=""
    if request.method=='POST':
        User_Email=request.POST['email']
        Password=request.POST['password']
        request.session['user_email']=User_Email
        print(User_Email,Password)
        User_Details=User_Register.objects.filter(Email=User_Email,Password=Password).values()
        if User_Details:
            return redirect(reverse('Dashboard',kwargs={'user_name':User_Details[0]['Name']}))
        else:
            return render(request,'login.html',{"message":"credentials are wrong! "})
    # return render(request,'Login_Page.html')
    return render(request,'login.html')



def Dashboard(request,user_name):
    
    substring_devided_data = defaultdict(lambda: {'INFO': [], 'WARNING': [], 'ERROR': []}) 
    words_last_reading=dict()
    keywords = {
            'batterytemperature':'Battery Temperature',
        }
    sub_string_data={}
    csv_file_path=settings.CSV_FILE_PATH
    # if not request.session['csv_data']:
    #     return render(request,'result.html',{"message":"Please upload csv file in AddData.",'user_name':user_name,})
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            csv_data = file.read()
        
        # Convert CSV string to a file-like object
        csv_file_like = StringIO(csv_data)
        
        # Initialize a CSV DictReader to read the data
        reader = csv.DictReader(csv_file_like)
        for row in reader:
            string_value = row['Search_string']
            event_template = row['Event_Template']
            if string_value not in sub_string_data:
                sub_string_data[string_value] = []
                        
            sub_string_data[string_value].append(event_template)
            if 'INFO' in event_template:
                log_level = 'INFO'
            elif 'WARNING' in event_template:
                log_level = 'WARNING'
            elif 'ERROR' in event_template:
                log_level = 'ERROR'
            else:
                continue  # Skip if no recognized log level is found

                    # Update counts
            substring_devided_data[string_value][log_level].append(event_template)
            for keyword, search_string in keywords.items():
                    # Search for the keyword pattern
                pattern = re.compile(rf'{search_string} \(.*?\): (\d+)')
                match = pattern.search(event_template)
                        
                if match:
                    value = int(match.group(1))
                    words_last_reading[keyword]=value
            
        sub_string_data=dict(sub_string_data)
        substring_devided_data=dict(substring_devided_data)
        print("the output",substring_devided_data)
        return render(request,'landing.html',{"user_name":user_name,"substring_devided_data":substring_devided_data,"data":sub_string_data,"alert_value":words_last_reading})
    except Exception as e:
        print("Erorr is coming at Dashboard function",e)
        return render(request,'landing.html',{"user_name":user_name,"data":"","alert_value":"","sub_devided_data":"",})
#Not using this function this function is used for fetching csv file and processing
def Get_Strings_Logs(request,user_name):
    data={}
    list_values=dict()
    keywords = {
            'batterytemperature':'Battery Temperature',
        }
    if request.method == 'POST':
            csv_file=request.FILES['csv_file']
            csv_data = csv_file.read().decode('utf-8')
    
    # Store the CSV data in the session
            request.session['csv_data'] = csv_data
            csv_file.seek(0)
            csv_data=csv_file.read().decode('utf-8')
            csv_file = StringIO(csv_data)
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                string_value = row['Search_string']
                event_template = row['Event_Templete']
                if string_value not in data:
                    data[string_value] = []
                    
                data[string_value].append(event_template)
                for keyword, search_string in keywords.items():
                    # Search for the keyword pattern
                    pattern = re.compile(rf'{search_string} \(.*?\): (\d+)')
                    match = pattern.search(event_template)
                        
                    if match:
                        value = int(match.group(1))
                        list_values[keyword]=value
           
            output=dict(data)
            print("the output is",output)
            return render(request,'landing.html',{"user_name":user_name,"data":output,"alert_value":list_values})
                
            
    return render(request,'landing.html',{"user_name":user_name})

def Visualization_Task(request,user_name):
    csv_file_path=settings.CSV_FILE_PATH
    values=defaultdict(list)
    keywords = {
                'batterytemp': 'Battery Time Remaining',
                'batterycharge': 'Battery charge',
                'batterytemperature':'Battery Temperature',
                'ups_temperature':'UPS Temperature'
                # Add more keywords as needed
        }
    list_values=dict()
    sub_string_data = {}
    substring_devided_count = defaultdict(lambda: {'INFO': 0, 'WARNING': 0, 'ERROR': 0}) 
    # substring_devided_data = defaultdict(lambda: {'INFO': [], 'WARNING': [], 'ERROR': []}) 
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_data = file.read()
            # Convert CSV string to a file-like object
        csv_file_like = StringIO(csv_data) 
            # Initialize a CSV DictReader to read the data
        reader = csv.DictReader(csv_file_like)
        # Define your keywords and their default words
        
            # Retrieve CSV data from session
            
            
        for row in reader:
            ##print(row)
            ##print(row['Event_Template'])
            event_template=row['Event_Template']
                    
            for keyword, search_string in keywords.items():
                # Search for the keyword pattern
                pattern = re.compile(rf'{search_string} \(.*?\): (\d+)')
                match = pattern.search(event_template)
                        
                if match:
                    value = int(match.group(1))
                    values[keyword].append(value)
                    list_values[keyword]=value
                    
            string_value = row['Search_string']
            event_template = row['Event_Template']
            if string_value not in sub_string_data:
                sub_string_data[string_value] = []
                        
            sub_string_data[string_value].append(event_template)
                    # Determine log level from event_template
            if 'INFO' in event_template:
                log_level = 'INFO'
            elif 'WARNING' in event_template:
                log_level = 'WARNING'
            elif 'ERROR' in event_template:
                log_level = 'ERROR'
            else:
                continue  # Skip if no recognized log level is found

                    # Update counts
            substring_devided_count[string_value][log_level] += 1
            
        substring_devided_count=dict(substring_devided_count)
        # substring_devided_data=dict(substring_devided_data)
        ##print(substring_devided_count)
        ##print("the values are",dict(values))
        ##print("last values are",list_values)
        
        if request.method=='POST':
            Search_data=dict()
            devided_data=dict()
            Search_String=request.POST['search_string']
            #print("search value",Search_String)
                # Search_String="TrdRobot"
            Search_data[Search_String]=[]
            devided_data[Search_String]={'INFO':[],'WARNING':[],'ERROR':[]}
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_data = file.read()
            
            # Convert CSV string to a file-like object
            csv_file_like = StringIO(csv_data)
            
            # Initialize a CSV DictReader to read the data
            reader = csv.DictReader(csv_file_like)
            
            for row in reader:
                #print(row)
                event_template=row['Event_Template']
                if Search_String.lower()==row['Search_string'].lower():
                    #print("execute")
                    Search_data[Search_String].append(row['Event_Template'])
                    #print("uo to this",Search_data)
                    ##print(dict("searching data1",Search_data))
                    if 'INFO' in event_template:
                        log_level = 'INFO'
                    elif 'WARNING' in event_template:
                        log_level = 'WARNING'
                    elif 'ERROR' in event_template:
                        log_level = 'ERROR'
                    else:
                        continue
                    print("this is not ok",log_level)
                    devided_data[Search_String][log_level].append(event_template)  
            devided_data=dict(devided_data)
            print("this is serach data",devided_data)
            return render(request,'result.html',{"user_name":user_name,"substring_devided_data":devided_data,"Count_data":substring_devided_count,"default_words":dict(values),"last_values":list_values,"Search_String":dict(Search_data)})
    except Exception as e:
        ##print("Error is comint at visulization task function",e)
        return render(request,'result.html',{"user_name":user_name,"Count_data":"","default_words":"","last_values":""})
    return render(request,'result.html',{"user_name":user_name,"Count_data":substring_devided_count,"default_words":dict(values),"last_values":list_values})


                
# Accourding to pavan requirement I am not using this function. I am separating data and sending information directly
def Soring_Word_Wise(request):
    request_data=[]
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        param1 = request.GET.get('param1', None)
        param2 = request.GET.get('param2', None)
        print(param1,param2)
        csv_file_path=settings.CSV_FILE_PATH
        
    # if not request.session['csv_data']:
    #     return render(request,'result.html',{"message":"Please upload csv file in AddData.",'user_name':user_name,})
        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_data = file.read()
            
            # Convert CSV string to a file-like object
            csv_file_like = StringIO(csv_data)
            
            # Initialize a CSV DictReader to read the data
            reader = csv.DictReader(csv_file_like)
            for row in reader:
                sub_string=row['Search_string']
                event_template=row['Event_Template']
                print("event template is",event_template)
                if sub_string==param1 and param2 in event_template:
                    request_data.append(event_template)
            print("requested data is",request_data)
            response_data = {
                "Requested_Data":request_data
            }
            
            return JsonResponse(response_data)
        except Exception as e:
            print("Error is coming at soring_word_wise function",e)
            response_data = {
                "Requested_Data":"Error is coming"
            }
            
            return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)
           
def Sorting_Data(request,user_name):
    print("calling sorting data function")
    values = defaultdict(list)
    today=datetime.now().date()
    end_date=""
    start_date=""
    keywords = {
            'batterytemp': 'Battery Time Remaining',
            'batterycharge': 'Battery charge',
            'batterytemperature':'Battery Temperature',
            'ups_temperature':'UPS Temperature'
            # Add more keywords as needed
        }
    list_values=dict()
    sub_string_data = {}
    substring_devided_count = defaultdict(lambda: {'INFO': 0, 'WARNING': 0, 'ERROR': 0}) 
    csv_file_path=settings.CSV_FILE_PATH
    if request.method=='POST':
        param1=request.POST.get('option_name')
    # if not request.session['csv_data']:
    #     return render(request,'result.html',{"message":"Please upload csv file in AddData.",'user_name':user_name,})
        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_data = file.read()
                
                # Convert CSV string to a file-like object
            csv_file_like = StringIO(csv_data)
                
                # Initialize a CSV DictReader to read the data
            reader = csv.DictReader(csv_file_like)
        
        
    
            print("this is value",param1)
            if param1=="Last_Day":
                end_date=today-timedelta(days=1)
                start_date=end_date

            elif param1=="Today":
                end_date=today.date()
                start_date=end_date

            elif param1=="Last_Week":
                end_date=today-timedelta(days=1)
                start_date=today-timedelta(days=7)
            
            elif param1=="Last_Month":
                
                end_date=today-timedelta(days=1)
                start_date=today-timedelta(days=30)
            elif param1=="All_Data":
                return redirect(reverse('Visualization_Task', kwargs={'user_name': user_name}))
            print("last day",end_date,start_date)
            for row in reader:
                date_value=row['Datetime']
                log_datetime = datetime.strptime(row['Datetime'], '%Y-%m-%d %H:%M:%S').date()
                if start_date <= log_datetime <= end_date:
                    
                    event_template = row['Event_Template']
                        
                    for keyword, search_string in keywords.items():
                        # Search for the keyword pattern
                        pattern = re.compile(rf'{search_string} \(.*?\): (\d+)')
                        match = pattern.search(event_template)
                            
                        if match:
                            value = int(match.group(1))
                            values[keyword].append(value)
                            list_values[keyword]=value
                        
                    string_value = row['Search_string']
                    event_template = row['Event_Template']
                    if string_value not in sub_string_data:
                        sub_string_data[string_value] = []
                            
                    sub_string_data[string_value].append(event_template)
                        # Determine log level from event_template
                    if 'INFO' in event_template:
                        log_level = 'INFO'
                    elif 'WARNING' in event_template:
                        log_level = 'WARNING'
                    elif 'ERROR' in event_template:
                        log_level = 'ERROR'
                    else:
                        continue  # Skip if no recognized log level is found

                        # Update counts
                    substring_devided_count[string_value][log_level] += 1
                substring_devided_count=dict(substring_devided_count)
                
            print("the values are",dict(values))
            print("last values are",list_values)
            # Process the selected value
            return render(request,'result.html',{"user_name":user_name,"Count_data":substring_devided_count,"default_words":dict(values),"last_values":list_values,"option_value":param1})
        except Exception as e:
            print("Error is coming at Sorting_Data function",e)
            return render(request,'result.html',{"user_name":user_name,"Count_data":"","default_words":"","last_values":"","option_value":""})

def Healthy(request,user_name):
    list_values=dict()
    keywords = {
            'batterytemp': 'Battery Time Remaining',
            'batterycharge': 'Battery charge',
            'batterytemperature':'Battery Temperature',
            'ups_temperature':'UPS Temperature'
            # Add more keywords as needed
        }
    csv_file_path=settings.CSV_FILE_PATH
        
    # if not request.session['csv_data']:
    #     return render(request,'result.html',{"message":"Please upload csv file in AddData.",'user_name':user_name,})
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            csv_data = file.read()
            
            # Convert CSV string to a file-like object
        csv_file_like = StringIO(csv_data)
            
            # Initialize a CSV DictReader to read the data
        reader = csv.DictReader(csv_file_like)
        for row in reader:
            event_template = row['Event_Template']
            for keyword, search_string in keywords.items():
                    # Search for the keyword pattern
                    pattern = re.compile(rf'{search_string} \(.*?\): (\d+)')
                    match = pattern.search(event_template)
                        
                    if match:
                        value = int(match.group(1))
                        list_values[keyword]=value
        return render(request,'Healthy.html',{"Keyword_Values":list_values,"user_name":user_name})
    except Exception as e:
        print("Error is coming at Healthy funtion")
        return render(request,'Healthy.html',{"Keyword_Values":"","user_name":user_name})
    
def User_Forgot_Password(request):
    request.session['user_email']=""
    Date_Time_Values=datetime.now()
    formatted_datetime = Date_Time_Values.strftime('%Y-%m-%d %H:%M:%S.%f')
    if request.method=='POST':
        email=request.POST['email'] 
        request.session['user_email']=email
        print("email is",email)
        User_Details=User_Register.objects.filter(Email=email).values()
        
        if User_Details:
            OtpNumber=random.randint(100000,999999)
            subject = 'Email with Template'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [User_Details[0]['Email'],]
            message=" your request to change password is accepted \n Your 6 digit otp is"+str(OtpNumber)
            context = {'name': 'John Doe'}
            send_mail(subject, message, from_email, recipient_list, )
            try:
                Forgot_Password_Details=Forgot_Password.objects.get(Email=email)
                if Forgot_Password_Details:
                    Forgot_Password_Details.OTP=str(OtpNumber)
                    print("upto this")
                    Forgot_Password_Details.save()
            except Exception as e:
                Otp_Details=Forgot_Password(Name=User_Details[0]['Name'],Email=User_Details[0]['Email'],DateTime=formatted_datetime,OTP=str(OtpNumber))
                Otp_Details.save()
                print("getting error in userforgot_password",{e})
            return render(request,'forgotPassword.html',{"message":"OTP sent to your mail","username":User_Details[0]['Name']})
            pass
        else:
            return render(request,'forgotPassword.html',{"message":"Not a valid email, Please check!"})
    return render(request,'forgotPassword.html')

def User_Verfiy_Otp(request):
    print("calling user verify otp")
    if request.method == 'POST':
        otp=request.POST['otp']
        new_password=request.POST.get('new_password').strip()
        confirm_password=request.POST.get('confirm_password').strip()
        print(new_password,confirm_password,len(confirm_password),len(confirm_password))
        if new_password != confirm_password:
            return render(request,'forgotPassword.html',{"message":"new_password and confirm password should be same"})
        print(otp,new_password,confirm_password)
        User_Change_Password=User_Register.objects.filter(Email=request.session['user_email'])
        Otp_Verify_Details=Forgot_Password.objects.filter(Email=request.session['user_email'],OTP=otp).values()
        print(Otp_Verify_Details)
        if Otp_Verify_Details and User_Change_Password:
            User_Register.objects.filter(Email=request.session['user_email']).update(Password=new_password)
            Forgot_Password.objects.filter(Email=request.session['user_email']).update(OTP="")
            return render(request,'forgotPassword.html',{"message":"Password updated successfully"})
        else:
            return render(request,'forgotPassword.html',{"message":"Wrong OTP!"})

    return render(request,'forgotPassword.html')
def User_Logout(request):
    if request.method=='POST':
        return render(request,'login.html')
def Resend_Otp(request):
    if not request.session['user_email']:
        return render(request,'forgotPassword.html',{"message":"Please enter email."})
    Date_Time_Values=datetime.now()
    formatted_datetime = Date_Time_Values.strftime('%Y-%m-%d %H:%M:%S.%f')
    email=request.session['user_email']
    print("email is",email)
    User_Details=User_Register.objects.filter(Email=email).values()
        
    if User_Details:
        OtpNumber=random.randint(100000,999999)
        subject = 'Email with Template'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [User_Details[0]['Email'],]
        message=" your request to change password is accepted \n Your 6 digit otp is"+str(OtpNumber)
        context = {'name': 'John Doe'}
        send_mail(subject, message, from_email, recipient_list, )
        try:
            Forgot_Password_Details=Forgot_Password.objects.get(Email=email)
            if Forgot_Password_Details:
                Forgot_Password_Details.OTP=str(OtpNumber)
                print("upto this")
                Forgot_Password_Details.save()
        except Exception as e:
            Otp_Details=Forgot_Password(Name=User_Details[0]['Name'],Email=User_Details[0]['Email'],DateTime=formatted_datetime,OTP=str(OtpNumber))
            Otp_Details.save()
            print("getting error in userforgot_password",{e})
        return render(request,'forgotPassword.html',{"message":"OTP sent to your mail","username":User_Details[0]['Name']})



