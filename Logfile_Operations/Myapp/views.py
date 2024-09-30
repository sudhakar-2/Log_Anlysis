from django.shortcuts import render, redirect
from .models import Register,User_Register,Forgot_Password
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
import pandas as pd
from io import StringIO
from collections import defaultdict
from django.http import JsonResponse
import re,io,csv,os,random
from collections import defaultdict
from collections import defaultdict
from datetime import datetime, timedelta
from django.urls import reverse

Log_File_Path=settings.KEYWORD_FILE_PATH
keywords={}
with open(Log_File_Path, 'a+', newline='', encoding='utf-8') as csv_file:
            csv_file.seek(0)
            data = csv_file.read()
            data=StringIO(data)
            reader=csv.DictReader(data)
            for i in reader:
                
                keywords[i['keyword']]=i['keyword_name']
#print(keywords)

# keywords = {
#                  'EPU_Ambient_Temperature': 'EPU Ambient Temperature',
#                 'batterycharge': 'Battery charge',
#                 'batterytemperature':'Battery Temperature',
#                 'ups_temperature':'c'
#                 # Add more keywords as needed
#         }



def Register(request):
    if request.method == 'POST':
        User_Name=request.POST['user_name']
        Email=request.POST['email']
        Password=request.POST['password']
        ##print(User_Name,Email,Password)
        Register_Data=User_Register(Name=User_Name,Email=Email,Password=Password)
        Register_Data.save()
        return render(request,'login.html')
    return render(request,'createAccount.html')

def User_Login(request):
    request.session['csv_data']=""
    if request.method=='POST':
        User_Email=request.POST['email']
        Password=request.POST['password']
        request.session['user_email']=User_Email
        ##print(User_Email,Password)
        User_Details=User_Register.objects.filter(Email=User_Email,Password=Password).values()
        if User_Details:
            return redirect(reverse('Dashboard',kwargs={'user_name':User_Details[0]['Name']}))
        else:
            return render(request,'login.html',{"message":"credentials are wrong! "})
    # return render(request,'Login_Page.html')
    return render(request,'login.html')


def Dashboard(request,user_name):
    substring_keywords_info = defaultdict(lambda: {}) 
    substring_devided_data = defaultdict(lambda: {'INFO': [], 'WARNING': [], 'ERROR': []}) 
    words_last_reading=dict()
    
    sub_string_data={}
    csv_file_path=settings.CSV_FILE_PATH
    
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
                    substring_keywords_info[string_value][keyword]=value

        sub_string_data=dict(sub_string_data)
        substring_devided_data=dict(substring_devided_data)
        substring_keywords_info=dict(substring_keywords_info)
        print(substring_keywords_info)
        ##print("the output",substring_devided_data)
        return render(request,'landing.html',{"user_name":user_name,"substring_devided_data":substring_devided_data,"data":sub_string_data,"alert_value":words_last_reading})
    except Exception as e:
        ##print("Erorr is coming at Dashboard function",e)
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
            ##print("the output is",output)
            return render(request,'landing.html',{"user_name":user_name,"data":output,"alert_value":list_values})     
    return render(request,'landing.html',{"user_name":user_name})


def Visualization_Task(request,user_name,calling_request):
    print("calling visualizaion function",calling_request)
    csv_file_path=settings.CSV_FILE_PATH
    values=defaultdict(list)
   
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
            
            event_template=row['Event_Template']
            string_value = row['Search_string']
            ##print(event_template)
            for keyword, search_string in keywords.items():
                # Search for the keyword pattern
                # print(search_string)
                pattern = re.compile(rf'{search_string} \(.*?\): (\d+)')
                match = pattern.search(event_template)
                if calling_request=="website":      
                    if match:
                        # print("calling this")
                        value = int(match.group(1))
                        # if len(values[keyword])<=5:
                        values[keyword].append(value)
                        list_values[keyword]=value
                
                            
                elif calling_request=="All_Data":      
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
        # print("last values2222 are",values)
        # if calling_request=="website":
        #     print("calling this thing only")
        #     for key in values:
        #         values[key].reverse()
            
        print("calling this",substring_devided_count) 
        # substring_devided_count=dict(substring_devided_count)
        # substring_keywords_info=dict(substring_keywords_info)
        print("this is substring keyrowd infor")
        # substring_devided_data=dict(substring_devided_data)
        #####print(substring_devided_count)
        #print("the values are",dict(values))
        print("last values are",values)
        print("calling above")
        if request.method=='POST':
            print("calling inside")
            Search_data=dict()
            devided_data=dict()
            Search_String=request.POST['search_string']
            print("search value",Search_String)
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
                ####print(row)
                event_template=row['Event_Template']
                if Search_String.lower()==row['Search_string'].lower():
                    ####print("execute")
                    Search_data[Search_String].append(row['Event_Template'])
                    ####print("uo to this",Search_data)
                    #####print(dict("searching data1",Search_data))
                    if 'INFO' in event_template:
                        log_level = 'INFO'
                    elif 'WARNING' in event_template:
                        log_level = 'WARNING'
                    elif 'ERROR' in event_template:
                        log_level = 'ERROR'
                    else:
                        continue
                    ###print("this is not ok",log_level)
                    devided_data[Search_String][log_level].append(event_template)  
            devided_data=dict(devided_data)
            ###print("this is serach data",devided_data)
            return render(request,'result.html',{"user_name":user_name,"substring_devided_data":devided_data,"Count_data":dict(substring_devided_count),"default_words":dict(values),"last_values":list_values,"Search_String":dict(Search_data)})
    except Exception as e:
        #####print("Error is comint at visulization task function",e)
        return render(request,'result.html',{"user_name":user_name,"Count_data":"","default_words":"","last_values":""})
    return render(request,'result.html',{"user_name":user_name,"Count_data":dict(substring_devided_count),"default_words":dict(values),"last_values":list_values})


def Visualization_Loop(request):
    csv_file_path=settings.CSV_FILE_PATH
    values=defaultdict(list)
    list_values=dict()
    sub_string_data = {}
    substring_devided_count = defaultdict(lambda: {'INFO': 0, 'WARNING': 0, 'ERROR': 0}) 
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_data = file.read()
          
        csv_file_like = StringIO(csv_data) 
         
        reader = csv.DictReader(csv_file_like)
        
        for row in reader:
            
            event_template=row['Event_Template']
            string_value = row['Search_string']
            ##print(event_template)
            for keyword, search_string in keywords.items():
                # Search for the keyword pattern
                # print(search_string)
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
        
        
        data={
        "Count_data":dict(substring_devided_count),"default_words":dict(values),"last_values":list_values
        }
        return JsonResponse(data)
        
    except Exception as e:
        #####print("Error is comint at visulization task function",e)
        data={
        "Count_data":"","default_words":"","last_values":""
        }
        return JsonResponse(data)
    
    

# Accourding to pavan requirement I am not using this function. I am separating data and sending information directly
def Soring_Word_Wise(request):
    request_data=[]
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        param1 = request.GET.get('param1', None)
        param2 = request.GET.get('param2', None)
        #print(param1,param2)
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
            if param2=="All_Data":
                for row in reader:
                    sub_string=row['Search_string']
                    event_template=row['Event_Template']
                ##print("event template is",event_template)
                    if sub_string==param1:
                        request_data.append(event_template)
            else:
                for row in reader:
                    sub_string=row['Search_string']
                    event_template=row['Event_Template']
                    ##print("event template is",event_template)
                    if sub_string==param1 and param2 in event_template:
                        request_data.append(event_template)
            ##print("requested data is",request_data)
            response_data = {
                "Requested_Data":request_data
            }
            
            return JsonResponse(response_data)
        except Exception as e:
            ##print("Error is coming at soring_word_wise function",e)
            response_data = {
                "Requested_Data":"Error is coming"
            }
            
            return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)
           


def Sorting_Data(request, user_name):
    ##print("calling sorting data function")
    values = defaultdict(list)
    today = datetime.now().date()
    
    list_values = {}
    sub_string_data = {}
    substring_devided_count = defaultdict(lambda: {'INFO': 0, 'WARNING': 0, 'ERROR': 0})

    csv_file_path = settings.CSV_FILE_PATH
    if request.method == 'POST':
        param1 = request.POST.get('option_name')

        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
                csv_data = file.read()

            csv_file_like = StringIO(csv_data)
            reader = csv.DictReader(csv_file_like)

            ##print("this is value", param1)
            if param1 == "Last_Day":
                end_date = today - timedelta(days=1)
                start_date = end_date  # Yesterday

            elif param1 == "Today":
                start_date = today
                end_date = today  # Today

            elif param1 == "Last_Week":
                end_date = today
                start_date = today - timedelta(days=7)

            elif param1 == "Last_Month":
                end_date = today
                start_date = today - timedelta(days=30)

            elif param1 == "All_Data":
                return redirect(reverse('Visualization_Task', kwargs={'user_name': user_name,"calling_request":"All_Data"}))

            ##print("last day", end_date, start_date)
            for row in reader:
                date_value = row['Datetime']
                log_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S').date()
                
                if start_date <= log_datetime <= end_date:
                    ##print("Processing date:", log_datetime)
                    event_template = row['Event_Template']
                    ##print("Event template:", event_template)
                    
                    for keyword, search_string in keywords.items():
                        ##print("Searching for:", search_string)
                        pattern = re.compile(rf'{search_string} \(.*?\): (\d+)')
                        match = pattern.search(event_template)

                        if match:
                            value = int(match.group(1))
                            values[keyword].append(value)
                            list_values[keyword] = value
                            

                    
                    string_value = row['Search_string']

                    if string_value not in sub_string_data:
                        sub_string_data[string_value] = []
                    sub_string_data[string_value].append(event_template)

                    # Determine log level
                    if 'INFO' in event_template:
                        log_level = 'INFO'
                    elif 'WARNING' in event_template:
                        log_level = 'WARNING'
                    elif 'ERROR' in event_template:
                        log_level = 'ERROR'
                    else:
                        ##print("Unrecognized log level in event_template")
                        continue  # Skip if no recognized log level is found

                   
                    
                    # Update counts
                    substring_devided_count[string_value][log_level] += 1
                    

            ##print("The values are:", dict(values))
            ##print("Last values are:", list_values)

          
            return render(request, 'result.html', {
                "user_name": user_name,
                "Count_data": dict(substring_devided_count),
                "default_words": dict(values),
                "last_values": dict(list_values),
                "option_value": param1
            })

        except Exception as e:
            ##print(f"Error in Sorting_Data function: {e}")
            return render(request, 'result.html', {
                "user_name": user_name,
                "Count_data": "",
                "default_words": "",
                "last_values": "",
                "option_value": param1,
                "error_message": str(e)  
            })

def Warning_Loop(request):
    today = datetime.now().date()
    start_date = today
    end_date = today
    csv_file_path=settings.CSV_FILE_PATH
    Warning_Data=[]
    try:
        with open(csv_file_path,'r',newline='',encoding='utf-8') as file:
            csv_data=file.read()
        csv_flie_like=StringIO(csv_data)
        reader=csv.DictReader(csv_flie_like)
        for row in reader:
            event_template=row['Event_Template']
            date_value = row['Datetime']
            log_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S').date()
            if start_date <= log_datetime <= end_date:
                if "WARNING" in event_template:
                    Warning_Data.append(event_template)
        data={
            "response":Warning_Data
        }
        return JsonResponse(data)
    except Exception as e:
        print("error coming at show warning funciton",e)
        data={
            "response":""
            }
        return JsonResponse(data)
def Error_Loop(request):
    today = datetime.now().date()
    start_date = today
    end_date = today
    csv_file_path=settings.CSV_FILE_PATH
    Error_Data=[]
    try:
        with open(csv_file_path,'r',newline='',encoding='utf-8') as file:
            csv_data=file.read()
        csv_file_like=StringIO(csv_data)
        reader=csv.DictReader(csv_file_like)
        for row in reader:
            event_template=row['Event_Template']
            date_value = row['Datetime']
            log_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S').date()
            if start_date <= log_datetime <= end_date:
                if "ERROR" in event_template:
                    Error_Data.append(event_template)
        data={
            "response":Error_Data
        }
        return JsonResponse(data)
    except Exception as e:
        print('exception occuring in error loop',e)
        data={
            "response":""
        }
        return JsonResponse(data)
def Show_Warning(request,user_name):
    today = datetime.now().date()
    start_date = today
    end_date = today
    #print("calling this function",user_name)
    csv_file_path=settings.CSV_FILE_PATH
    Warning_Data=[]
    try:
        with open(csv_file_path,'r',newline='',encoding='utf-8') as file:
            csv_data=file.read()
        csv_flie_like=StringIO(csv_data)
        reader=csv.DictReader(csv_flie_like)
        for row in reader:
            date_value = row['Datetime']
            log_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S').date()
            if log_datetime < end_date:
                event_template=row['Event_Template']
                if "WARNING" in event_template:
                    Warning_Data.append(event_template)
        return render(request,'Warning_Data.html',{"user_name":user_name,"Warning_Data":Warning_Data})
    except Exception as e:
        #print("error coming at show warning funciton",e)
        return render(request,'Warning_Data.html',{"user_name":user_name,"Warning_Data":""})
def Show_Errors(request,user_name):
    today = datetime.now().date()
    start_date = today
    end_date = today
    #print("calling this Show_Errors",user_name)
    csv_file_path=settings.CSV_FILE_PATH
    Error_Data=[]
    try:
        with open(csv_file_path,'r',newline='',encoding='utf-8') as file:
            csv_data=file.read()
        csv_flie_like=StringIO(csv_data)
        reader=csv.DictReader(csv_flie_like)
        for row in reader:
            date_value = row['Datetime']
            log_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S').date()
            if log_datetime < end_date:
                event_template=row['Event_Template']
                if "ERROR" in event_template:
                    Error_Data.append(event_template)
        return render(request,'Error_Data.html',{"user_name":user_name,"Error_Data":Error_Data})
    except Exception as e:
        #print("error coming at show warning funciton",e)
        return render(request,'Error_Data.html',{"user_name":user_name,"Error_Data":""})
def Add_New_Keyword(request,user_name):
    check_values=["sudhakar","mahesh"]
    global keywords
    Log_File_Path=settings.KEYWORD_FILE_PATH
    #print(Log_File_Path)
    if request.method=="POST":
        keyword_name=request.POST['keyword_name']
        action=request.POST.get('action')
    check_values.append(keyword_name)
    print(check_values)
    print(keyword_name,action)
    try:
        file_exists = os.path.isfile(Log_File_Path)
        with open(Log_File_Path, 'a+', newline='', encoding='utf-8') as csv_file:
            csv_file.seek(0)
            data = csv_file.read()
            csv_writer = csv.writer(csv_file)

            # Write the header only if the file is empty or doesn't exist
            if action=="Add":
                if not file_exists or os.stat(Log_File_Path).st_size == 0:
                    csv_writer.writerow(['keyword','keyword_name'])
                if keyword_name not in data:
                    csv_writer.writerow([keyword_name,keyword_name])
                else:
                    print("already present")
            elif action=="Delete":
                updated_data = []
                with open(Log_File_Path, mode='r', newline='', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    header = next(csv_reader, None)  # Read the header

                     # Ensure we have the correct header
                    if header == ['keyword', 'keyword_name']:
                        updated_data.append(header)  # Keep the header

                        for row in csv_reader:
                            if row[0] != keyword_name:  # Check if the keyword is not the one to delete
                                updated_data.append(row)

                    # Write the updated data back to the CSV file
                with open(Log_File_Path, mode='w+', newline='', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(updated_data)
                    keywords.pop(keyword_name)
    except Exception as e:
        print("error at add_new_data function",e)      
    with open(Log_File_Path, 'a+', newline='', encoding='utf-8') as csv_file:
            print("I am calling for both")
            csv_file.seek(0)
            data = csv_file.read()
            data=StringIO(data)
            reader=csv.DictReader(data)
            for i in reader:
                keywords[i['keyword']]=i['keyword_name']
        #print("keywords are",keywords)
            
    print(keywords)
    return redirect('Healthy',user_name=user_name)
def Healthy(request,user_name):
    list_values=dict()
    #print(keywords)
   
    csv_file_path=settings.CSV_FILE_PATH
    substring_keywords_info = defaultdict(lambda: {}) 
    # if not request.session['csv_data']:
    #     return render(request,'result.html',{"message":"Please upload csv file in AddData.",'user_name':user_name,})
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
            csv_data = file.read()
            
            # Convert CSV string to a file-like object
        csv_file_like = StringIO(csv_data)
            
            # Initialize a CSV DictReader to read the data
        reader = csv.DictReader(csv_file_like)
        reader=list(reader)
        for row in reversed(reader):
            string_value=row['Search_string']
            event_template = row['Event_Template']
            #print(event_template)
            for keyword, search_string in keywords.items():
                    # Search for the keyword pattern
                    pattern = re.compile(rf'{search_string} \(.*?\): (\d+)')
                    match = pattern.search(event_template)
                        
                    if match:
                        value = int(match.group(1))
                        list_values[keyword]=value
                        substring_keywords_info[string_value][keyword]=value
        substring_keywords_info=dict(substring_keywords_info)    
        ##print("list values are",list_values)
        return render(request,'Healthy.html',{"Keyword_Values":substring_keywords_info,"user_name":user_name})
    except Exception as e:
        ##print("Error is coming at Healthy funtion")
        return render(request,'Healthy.html',{"Keyword_Values":"","user_name":user_name})

def Meter_values(request):
    print("calling meter values this function")
    list_values=dict()
    #print(keywords)
    substring_keywords_info = defaultdict(lambda: {}) 
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
            string_value=row['Search_string']
            event_template = row['Event_Template']
            #print(event_template)
            for keyword, search_string in keywords.items():
                    # Search for the keyword pattern
                    pattern = re.compile(rf'{search_string} \(.*?\): (\d+)')
                    match = pattern.search(event_template)
                        
                    if match:
                        value = int(match.group(1))
                        list_values[keyword]=value
                        substring_keywords_info[string_value][keyword]=value
        ##print("list values are",list_values)
        substring_keywords_info=dict(substring_keywords_info)
        print(substring_keywords_info)
        data = {"response": substring_keywords_info}
        return JsonResponse(data)
        
    except Exception as e:
        print("Error is coming at Healthy funtion",e)
        data = {"response": "Error is coming"}
        return JsonResponse(data)
        
    
def User_Forgot_Password(request):
    request.session['user_email']=""
    Date_Time_Values=datetime.now()
    formatted_datetime = Date_Time_Values.strftime('%Y-%m-%d %H:%M:%S.%f')
    if request.method=='POST':
        email=request.POST['email'] 
        request.session['user_email']=email
        ##print("email is",email)
        User_Details=User_Register.objects.filter(Email=email).values()
        
        if User_Details:
            OtpNumber=random.randint(100000,999999)
            subject = 'Email with Template'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [User_Details[0]['Email'],]
            message = "Your request to change your password has been accepted.\nYour 6-digit OTP is: " + str(OtpNumber)
            context = {'name': 'John Doe'}
            send_mail(subject, message, from_email, recipient_list, )
            try:
                Forgot_Password_Details=Forgot_Password.objects.get(Email=email)
                if Forgot_Password_Details:
                    Forgot_Password_Details.OTP=str(OtpNumber)
                    ##print("upto this")
                    Forgot_Password_Details.save()
            except Exception as e:
                Otp_Details=Forgot_Password(Name=User_Details[0]['Name'],Email=User_Details[0]['Email'],DateTime=formatted_datetime,OTP=str(OtpNumber))
                Otp_Details.save()
                ##print("getting error in userforgot_password",{e})
            return render(request,'forgotPassword.html',{"message":"OTP sent to your mail","username":User_Details[0]['Name']})
            pass
        else:
            return render(request,'forgotPassword.html',{"message":"Not a valid email, Please check!"})
    return render(request,'forgotPassword.html')

def User_Verfiy_Otp(request):
    ##print("calling user verify otp")
    if request.method == 'POST':
        otp=request.POST['otp']
        new_password=request.POST.get('new_password').strip()
        confirm_password=request.POST.get('confirm_password').strip()
        ##print(new_password,confirm_password,len(confirm_password),len(confirm_password))
        if new_password != confirm_password:
            return render(request,'forgotPassword.html',{"message":"new_password and confirm password should be same"})
        ##print(otp,new_password,confirm_password)
        User_Change_Password=User_Register.objects.filter(Email=request.session['user_email'])
        Otp_Verify_Details=Forgot_Password.objects.filter(Email=request.session['user_email'],OTP=otp).values()
        ##print(Otp_Verify_Details)
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
    ##print("email is",email)
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
                ##print("upto this")
                Forgot_Password_Details.save()
        except Exception as e:
            Otp_Details=Forgot_Password(Name=User_Details[0]['Name'],Email=User_Details[0]['Email'],DateTime=formatted_datetime,OTP=str(OtpNumber))
            Otp_Details.save()
            ##print("getting error in userforgot_password",{e})
        return render(request,'forgotPassword.html',{"message":"OTP sent to your mail","username":User_Details[0]['Name']})

def All_Data(request,user_name):
    today = datetime.now().date()
    start_date = today
    end_date = today
    csv_file_path=settings.CSV_FILE_PATH
    all_data=[]
    try:
        with open(csv_file_path,'r',newline='',encoding='utf-8') as file:
            csv_file=file.read()
        csv_file_like=StringIO(csv_file)
        reader=csv.DictReader(csv_file_like)
        print(reader)
        # all_data=list(reader)
        for row in reader:
                date_value = row['Datetime']
                log_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S').date()
                if log_datetime < end_date:
                    
                    all_data.append(row['Event_Template'])
        print(all_data)
        return render(request,'All_Data.html',{"user_name":user_name,"all_data":all_data})
    except Exception as e:
        print("getting exception in all data",e)
        return render(request,'All_Data.html',{"user_name":user_name,"all_data":""})

def All_Data_Loop(request):
    today = datetime.now().date()
    start_date = today
    end_date = today
    csv_file_path=settings.CSV_FILE_PATH
    today_data=[]
    try:
        with open(csv_file_path,'r',newline='',encoding='utf-8') as file:
            csv_file=file.read()
        csv_file_like=StringIO(csv_file)
        reader=csv.DictReader(csv_file_like)
        # all_data=list(reader)
        for row in reader:
                date_value = row['Datetime']
                log_datetime = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S').date()
                if start_date <= log_datetime <= end_date:
                    print(row['Event_Template'])
                    today_data.append(row['Event_Template'])

        data={
            'response':today_data
        }
        return JsonResponse(data)
    except Exception as e:
        print("exception is occuring in all_data",e)
        data={
            'response':""
        }
        return JsonResponse(data)
    
