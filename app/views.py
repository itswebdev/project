from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.urls import reverse
import random
from datetime import datetime
from .utils import get_user_counts_context
from django.db.models import Count
from django.core.mail import send_mail

# Create your views here.

    # camp Registration form

def CampReg(request):
    if request.method=="POST":
        form=CampForm(request.POST)
        login=LoginForm(request.POST)
        if form.is_valid() and login.is_valid():
            user=login.save(commit=False)
            user.usertype='camp'
            user.save()
            a=form.save(commit=False)
            a.login_id=user
            a.save()
            messages.success(request,"Camp Registered Successfully")
            return redirect('UserLogin')
    else:
        form=CampForm()
        login=LoginForm()
    return render(request, 'common/campreg.html',{'form':form,'login':login})

    # station Registration form

def PoliceReg(request):
    if request.method=="POST":
        form=PoliceForm(request.POST)
        login=LoginForm(request.POST)
        if form.is_valid() and login.is_valid():
            user=login.save(commit=False)
            user.usertype='police_station'
            user.save()
            station=form.save(commit=False)
            station.login_id=user
            station.save()
            messages.success(request,"Police Station Registered Successfully")
            return redirect('UserLogin')
    else:

        form=PoliceForm()
        login=LoginForm()
    return render(request,'common/policereg.html',{'form':form,'login':login})

    # public Registration form

def PublicReg(request):
    if request.method=="POST":
        form=PublicForm(request.POST)
        login=LoginForm(request.POST)
        if form.is_valid() and login.is_valid():
            user=login.save(commit=False)
            user.usertype='public_user'
            user.save()
            a=form.save(commit=False)
            a.login_id=user
            a.save()
            messages.success(request,"User Registration Successfully")
            return redirect('UserLogin')
    else:

        form=PublicForm()
        login=LoginForm()
    return render(request, 'common/publicreg.html',{'form':form,'login':login})

    # volunteer Registration form

def VolunteerReg(request):
    if request.method=="POST":
        form=VolunteerForm(request.POST)
        login=LoginForm(request.POST)
        if form.is_valid() and login.is_valid():
            user=login.save(commit=False)
            user.usertype='volunteer'
            user.save()
            a=form.save(commit=False)
            a.login_id=user
            a.save()
            messages.success(request,"Volunteer Registered successfully")
            return redirect('UserLogin')
    else:
        form=VolunteerForm()
        login=LoginForm()
    return render(request,'common/volreg.html',{'form':form,'login':login})

# admin home page

def ViewAdmin(request):
    return render(request,'admin.html')

def CampTable(request):
    context = get_user_counts_context()
    camps=Camp.objects.all()
    context['camps'] = camps
    return render(request,'camp/camp_table.html',context)

def StationTable(request):
    context = get_user_counts_context()
    stations=Police.objects.all()
    context['stations'] = stations
    return render(request,'police/station_table.html',context)

def PublicTable(request):
    context = get_user_counts_context()
    publics=Public.objects.all()
    context['publics'] = publics

    return render(request,'public/public_table.html',context) 
 
def VolunteerTable(request):
    context = get_user_counts_context()
    volunteers=Volunteer.objects.all()
    context['volunteers'] = volunteers
    return render(request,'volunteer/volunteer_table.html',context)

    # camp home page

def CampHome(request):
    id=request.session.get('camp_id') 
    if not id:
        return redirect('UserLogin')  
    return render(request,'camp/camp.html')

    # station home page

def StationHome(request):
    id=request.session.get('station_id') 
    if not id:
        return redirect('UserLogin')  
    return render(request,'police/station.html')

    # public home page

def PublicHome(request):
    id=request.session.get('public_id') 
    if not id:
        return redirect('UserLogin')  
    return render(request,'public/public.html')

    
    # volunteer home page

def VolunteerHome(request):
    id=request.session.get('volunteer_id') 
    if not id:
        return redirect('UserLogin')  
    return render(request,'volunteer/volunteer.html')


    # user login 

def UserLogin(request):
    if request.method=="POST":
        form=LoginCheck(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            try:
                user=Login.objects.get(email=email)         
                #   login object
                if user.password==password:
                    if user.usertype=="camp":
                        request.session['camp_id']=user.id
                        return redirect('CampHome')
                    elif user.usertype=="police_station":
                        request.session['station_id']=user.id
                        return redirect('StationHome')
                    elif user.usertype=="public_user":
                        request.session['public_id']=user.id
                        return redirect('PublicHome')
                    elif user.usertype=="volunteer":
                        request.session['volunteer_id']=user.id
                        return redirect('VolunteerHome')
                    elif user.usertype=="admin":
                        request.session['admin_id']=user.id
                        return redirect('ViewAdmin2')    
                else:
                    messages.error(request,"invalid password")
            except Login.DoesNotExist:
                    messages.error(request,"User Does not Exist")
    else:
        form=LoginCheck()
    return render(request,'common/login.html',{'form':form})


     # camp profile editing

def EditCamp(request):
    id=request.session['camp_id']
    user=get_object_or_404(Login, id=id)
    # print(user)
    camp=get_object_or_404(Camp, login_id=user)
    # print(camp)
    if request.method == "POST":
        login=LoginEditForm(request.POST, instance=user)
        form=CampForm(request.POST, instance=camp)
        if form.is_valid() and login.is_valid(): 
            form.save()
            login.save()
            messages.success(request,"Profile Updated Successfully")
            return redirect('CampHome')
    else:
        l=LoginEditForm(instance=user)
        c=CampForm(instance=camp)
    return render(request,'camp/edit_profile.html',{'c':c,'l':l})

    
     # station profile editing

def EditStation(request):
    id=request.session['station_id']                   
    user=get_object_or_404(Login, id=id)
    station=get_object_or_404(Police, login_id=user)
    if request.method=="POST":
            login=LoginEditForm(request.POST, instance=user)
            form=PoliceForm(request.POST, instance=station)
            if form.is_valid() and login.is_valid():
             form.save()
             login.save()
             messages.success(request,"Profile Updated Successfully")
             return redirect('StationHome')
    else:
      l=LoginEditForm(instance=user)
      c=PoliceForm(instance=station)
    return render(request,'police/edit_profile.html',{'c':c,'l':l})


     # public profile editing

def EditPublic(request):
    pid=request.session.get('public_id')                
    #  'get()' is used to avoid KeyError if the key is not found in the session.
    if not pid:
        return redirect('UserLogin')
    else:
        user=get_object_or_404(Login, id=pid)
        public=get_object_or_404(Public, login_id=user)
        if request.method=="POST":
                login=LoginEditForm(request.POST, instance=user)
                form=PublicForm(request.POST, instance=public)
                if form.is_valid() and login.is_valid():
                    form.save()
                    login.save()
                    messages.success(request,"Profile Updated Successfully")
                    return redirect('PublicHome')
        else:
            login=LoginEditForm(instance=user)
            form=PublicForm(instance=public)
        return render(request,'public/edit_profile.html',{'form':form,'login':login})
   

    # volunteer profile editing

def EditVolunteer(request):   
    id=request.session.get('volunteer_id') 
    if not id:
        return redirect('UserLogin')               
    user=get_object_or_404(Login, id=id)
    volunteer=get_object_or_404(Volunteer, login_id=user)
    if request.method=="POST":
        login=LoginEditForm(request.POST, instance=user)
        form=VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid() and login.is_valid():
            form.save() 
            login.save()
            messages.success(request,"Profile Updated Successfully")
            return redirect('VolunteerHome')
    else:
        l=LoginEditForm(instance=user)
        v=VolunteerForm(instance=volunteer)
    return render(request,'volunteer/edit_vol_profile.html',{'v':v,'l':l})

    # admin page view 2

def ViewAdmin2(request):
    context = get_user_counts_context()
    return render(request,'admin/admin2.html',context)

    #  Camp User Registration  

def CampAddUser(request):
    id=request.session.get('camp_id')
    if not id:
        return redirect('UserLogin')
    campdata=get_object_or_404(Login,id=id)
    if request.method=="POST":
        form=CampUserForm(request.POST,request.FILES)    # 'request.FILES' is used because image files are also stored here.
        if form.is_valid():
            camp_user=form.save(commit=False)
            camp_user.camp_id=campdata
            camp_user.save()
            messages.success(request,"Registered Successfully")
            return redirect('CampHome')
    else:

        form=CampUserForm()
    return render(request,'camp/camp_user_reg.html',{'form':form})

    # Camp user viewing

def CampUsersView(request):
    session_id=request.session.get('camp_id')
    if not id:
        return redirect('UserLogin')
    a=get_object_or_404(Login,id=session_id)
    users=CampUser.objects.filter(camp_id=a)
    return render(request,'camp/camp_users_table.html',{'users':users})

    # Editing camp user

def EditCampUser(request,id):
    check=request.session.get('camp_id')
    if not check:
        return redirect('UserLogin')
    user=get_object_or_404(CampUser, id=id)
    if request.method=="POST":
        form=CampUserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"Updated Successfully")
            return redirect('CampUsersView') 
    else:
        form=CampUserForm(instance=user)
    return render(request,'camp/edit_camp_user.html',{'form':form})

    # Deleting camp user
 
def CampUserDelete(request,id):
    check=request.session.get('camp_id')
    if not check:
        return redirect('UserLogin')
    user=get_object_or_404(CampUser, id=id)
    user.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('CampUsersView')

def Landing(request):
    return render(request,'common/landing.html')
   

def CampSearch(request):
    check=request.session.get('public_id')
    if not check:
        return redirect('UserLogin')
    if request.method == "POST":
        query = request.POST.get('search')
        camps = Camp.objects.filter(
            Q(camp_name__icontains=query) |
            Q(district__icontains=query) |
            Q(full_address__icontains=query) |
            Q(city__icontains=query) |
            Q(panchayath__icontains=query) |
            Q(thaluk__icontains=query) |
            Q(contact__icontains=query) 
        )
        return render(request, 'public/camp_search.html', {'camps': camps})
    else:
        return render(request, 'public/camp_search.html')


def CampNeedsSubmit(request):
    id=request.session.get('camp_id')
    if not id:
        return redirect('UserLogin')   
    campdata=get_object_or_404(Camp,login_id=id)
    if request.method =="POST":
        form=CampNeedsForm(request.POST)
        if form.is_valid():
            camp_need=form.save(commit=False)
            camp_need.camp_id=campdata
            camp_need.save()
            messages.success(request,"Needs are submitted successfully")
    else:
        form=CampNeedsForm()
    return render(request,'camp/camp_needs.html',{'form':form})

def CampNeedsTable(request):
    context = get_user_counts_context()
    needs=CampNeeds.objects.all()
    context['needs'] = needs
    return render(request,'admin/camp_needs_table.html',context)

def NeedsViewTable(request):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    a=get_object_or_404(Camp,login_id=session_id)
    needs=CampNeeds.objects.filter(camp_id=a)
    return render(request,'camp/needs_view_table.html',{'needs':needs})

def EditCampNeed(request,id):
    check=request.session.get('camp_id')
    if not check:
        return redirect('UserLogin')
    need=get_object_or_404(CampNeeds,id=id)
    if request.method=="POST":
        form=CampNeedsForm(request.POST,instance=need)
        if form.is_valid():
            form.save()
            messages.success(request,"Updated Successfully")
            return redirect('NeedsViewTable')
    else:
        f=CampNeedsForm(instance=need)  
    return render(request,'camp/camp_edit_needs.html',{'f':f})

def CampNeedsDelete(request,id):
    check=request.session.get('camp_id')
    if not check:
        return redirect('UserLogin')
    need=get_object_or_404(CampNeeds,id=id)
    need.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('NeedsViewTable')


   # function to logout

def Logout(request):
    request.session.flush()
    return redirect('Landing')

def SetCampNeedStatus(request,id):
    # print(id)
    need=get_object_or_404(CampNeeds,id=id)
    # print(need)
    if request.method=="POST":
        need.status=request.POST.get('status')  #  Similar functionality as the cleaned_data[] , but cleaned_data[] cannot be used without form validation
        need.save()
        messages.success(request,"Status Updated Successfully")
        return redirect('CampNeedsTable')
    else:
        form=CampNeedsForm(instance=need)
    return render(request,'admin/set_camp_status.html',{'form':form})

def SearchCampPerson(request):
    id=request.session.get('camp_id')
    if not id:
        return redirect('UserLogin')
    a=get_object_or_404(Login,id=id)
    if request.method=="POST":
        query=request.POST.get('search')
        users=CampUser.objects.filter(
            Q(camp_id=a) &
            Q(full_name__icontains=query) | 
            Q(address__icontains=query) | 
            Q(district__icontains=query) | 
            Q(city__icontains=query)| 
            Q(contact_no__icontains=query) | 
            Q(aadhar_no__icontains=query) |
            Q(panchayath__icontains=query) | 
            Q(village__icontains=query) |
            Q(thaluk__icontains=query) 
            )      
        return render(request,'camp/camp_search_person.html',{'users':users})
    else:
        return render(request,'camp/camp_search_person.html')
    
def SearchPerson(request):
    id=request.session.get('camp_id')
    if not id:
        return redirect('UserLogin')
    if request.method=="POST":
        query=request.POST.get('search')
        users=CampUser.objects.filter(
            Q(full_name__icontains=query) | 
            Q(address__icontains=query) | 
            Q(district__icontains=query) | 
            Q(city__icontains=query)| 
            Q(contact_no__icontains=query) | 
            Q(aadhar_no__icontains=query) |
            Q(panchayath__icontains=query) | 
            Q(village__icontains=query) |
            Q(thaluk__icontains=query) 
            )      
        return render(request,'public/search_persons.html',{'users':users})
    else:
        return render(request,'public/search_persons.html')
    
def CampAlerts(request):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    # print(session_id)
    alert=get_object_or_404(Camp,login_id=session_id)
    # print(alert)
    if request.method=='POST':
        form=CampAlertForm(request.POST)
        if form.is_valid():
            camp_alert=form.save(commit=False)
            camp_alert.login_id=alert
            camp_alert.save()
            messages.success(request,'Alert submitted successfully')
            return redirect('CampHome')
    else:
        form=CampAlertForm()
    return render(request,'camp/camp_alert.html',{'form':form})

def CampAlertTable(request):
    alerts=CampAlert.objects.all()
    context = get_user_counts_context()
    context['alerts'] = alerts
    return render(request,'admin/camp_alert_table.html',context)

def AlertCampTable(request):
    session_id=request.session['camp_id']                            #  getting the current session id .
    a=get_object_or_404(Camp,login_id=session_id)                    #  comparing the session id with the login id (foreign key of camp model),if true then saves  id  of the camp into a.
    alerts=CampAlert.objects.filter(login_id=a)                      #  filtering only from the camp whose id is stored in the variable a.
    return render(request,'camp/alert_message.html',{'alerts':alerts})    

def DeleteAlert(request,id):
    d=get_object_or_404(CampAlert,id=id)
    d.delete()
    return redirect('AlertCampTable')

def VolunteerReq(request):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    req=get_object_or_404(Camp,login_id=session_id)
    if request.method=='POST':
        form=VolunteerReqForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.login_id=req
            a.save()
            messages.success(request,'Request for volunteers send successfully')
            return redirect('CampHome')
    else:
        form=VolunteerReqForm()
    return render(request,'volunteer/volunteer_req.html',{'form':form})

def VolunteerReqTable(request):
    requests=VolunteerRequest.objects.all()
    context = get_user_counts_context()
    context['requests'] = requests
    return render(request,'admin/volunteer_req_table.html',context)

def ReqVolunteerTable(request):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    a=get_object_or_404(Camp,login_id=session_id)
    requests=VolunteerRequest.objects.filter(login_id=a)
    return render(request,'camp/req_volunteer_table.html',{'requests':requests})


def EditVolunteerReq(request,id):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    req=get_object_or_404(VolunteerRequest,id=id)
    if request.method=="POST":
          requests=VolunteerReqForm(request.POST,instance=req)
          if requests.is_valid():
              requests.save()
              messages.success(request,'Request edited successfullly')
              return redirect('ReqVolunteerTable')
    else:
        requests=VolunteerReqForm(instance=req)
    return render(request,'camp/edit_vol_req.html',{'requests':requests})


def DeleteVolunteerReq(request,id):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    req=get_object_or_404(VolunteerRequest,id=id)
    req.delete()
    messages.success(request,'Request deleted successfully')
    return redirect('ReqVolunteerTable')

def VolunteerAllocateTable(request,id,requestid):
    #print(id)                            check  the volunteer_req_table.html  file
    id=get_object_or_404(Camp,id=id)
    volunteers = Volunteer.objects.filter(allocation="false") | Volunteer.objects.filter(allocation__isnull=True) | Volunteer.objects.filter(id__in=Allocate.objects.filter(camp_id=id).values_list('volunteer_id')) # Here added filtering allocation field where value is NULL   
    volreq=get_object_or_404(VolunteerRequest,id=requestid)
    return render(request,'admin/volunteer_allocate_table.html',{'volunteers':volunteers,'campid':id,'volreq':volreq}) 


def VolAllocateNow(request,campid,id,volreqid):
    a=get_object_or_404(Camp,id=campid)
    vol=get_object_or_404(Volunteer,id=id)
    req=get_object_or_404(VolunteerRequest,id=volreqid)
    if not Allocate.objects.filter(camp=a,volunteer=vol).exists():
       Allocate.objects.create(camp=a,volunteer=vol)
       vol.allocation="true"
       vol.save()
       req.totalallocated+=1
       req.save()
       messages.success(request,'Allocated successfully')
       return redirect('VolunteerAllocateTable',id=campid,requestid=volreqid)
    else:
       messages.error(request,'Already allocated')
       return redirect('VolunteerAllocateTable',id=campid,requestid=volreqid)

def VolDeAllocate(request,campid,id,volreqid):
    a=get_object_or_404(Camp,id=campid)
    vol=get_object_or_404(Volunteer,id=id)
    req=get_object_or_404(VolunteerRequest,id=volreqid)
    if Allocate.objects.filter(camp=a,volunteer=vol).exists():
       Allocate.objects.filter(camp=a,volunteer=vol).delete()
       vol.allocation="false"
       vol.save()
       if int(req.totalallocated)>0:
        req.totalallocated-=1
        req.save()
       messages.success(request,'Deallocated successfully')
       return redirect('VolunteerAllocateTable',id=campid,requestid=volreqid)

    else:
       messages.error(request,'Already deallocated')
       return redirect('VolunteerAllocateTable',id=campid,requestid=volreqid)

def Notification(request):
    session_id=request.session.get('volunteer_id')
    if not session_id:
        return redirect('UserLogin')              
    a = request.session.get('volunteer_id')
    user = get_object_or_404(Login, id=a)
    volunteer = get_object_or_404(Volunteer, login_id=user)
    isallocated = Allocate.objects.filter(volunteer=volunteer).first()

    if isallocated:
        camp = isallocated.camp
        duties = Duty.objects.filter(volunteer_id=volunteer) 
        messages.success(request, f'You have been assigned to the camp {camp.camp_name}')
    else:
        camp = None
        duties = []
        messages.warning(request, 'You are not assigned to any camp')

    return render(request, 'volunteer/notification.html', {'camp': camp, 'duties': duties})


def PublicComplaint(request):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    if request.method=="POST":
        form=ComplaintForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            user=get_object_or_404(Login,id=request.session['public_id'])
            a.login_id=user
            a.save()
            messages.success(request,'Complaint submitted successfully')
            return redirect('PublicHome')
    else:
        form=ComplaintForm()
    return render(request,'public/public_complaint.html',{'form':form})

def ViewComplaints(request):
    complaints=Complaint.objects.all()
    context = get_user_counts_context()
    context['complaints'] = complaints
    return render(request,'admin/view_complaint.html',context)

def ListComplaints(request):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    user=get_object_or_404(Login,id=request.session['public_id'])
    complaints=Complaint.objects.filter(login_id=user)
    return render(request,'public/list_complaints.html',{'complaints':complaints})

def EditComplaint(request,id):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    complaint=get_object_or_404(Complaint,id=id)
    if request.method=="POST":
        form=ComplaintForm(request.POST,instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request,'Complaint edited successfully')
            return redirect('ListComplaints')
    else:
        complaints=ComplaintForm(instance=complaint)
    return render(request,'public/edit_complaint.html',{'complaints':complaints})

def DeleteComplaint(request,id):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    complaint=get_object_or_404(Complaint,id=id)
    complaint.delete()
    messages.success(request,'Complaint deleted successfully')
    return redirect('ListComplaints')

def AllocatedVolList(request):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    a=get_object_or_404(Camp,login_id=session_id)
    allocated_vol=Allocate.objects.filter(camp=a)
    return render(request,'camp/vol_allocated_list.html',{'allocated_vol':allocated_vol})

def ComplaintReply(request,id):
    complaint=get_object_or_404(Complaint,id=id)
    if request.method=="POST":
        form=ComplaintReplyForm(request.POST,instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request,'Complaint edited successfully')
            return redirect('ViewComplaints')
    else:
        form=ComplaintReplyForm(instance=complaint)
    return render(request,'admin/reply.html',{'form':form,'complaint':complaint})

def ShowReply(request,id):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    complaint=get_object_or_404(Complaint,id=id)
    return render(request,'public/view_reply.html',{'complaint':complaint})

def ScheduleDuty(request,camp,volunteer):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    vol=get_object_or_404(Volunteer,id=volunteer)
    print(vol)
    c=get_object_or_404(Camp,id=camp)
    if request.method == "POST":
        alloc=get_object_or_404(Allocate,volunteer=vol)
        if Allocate.objects.filter(camp=c,volunteer=vol).exists():
            alloc.duty_status="scheduled"  
            alloc.save()
        form=DutyForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.volunteer_id=vol
            a.camp_id=c
            a.save()
            messages.success(request,'Duty successfully scheduled')
            return redirect('AllocatedVolList')
    else:
        form=DutyForm()
    return render(request,'camp/vol_duty_schedule.html',{'form':form})

def FundAllocationRequest(request):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    if request.method=="POST":
        form=FundAllocationForm(request.POST,request.FILES)
        if form.is_valid():
            a=form.save(commit=False)
            user=get_object_or_404(Login,id=request.session['public_id'])
            a.login_id=user
            a.save()
            return redirect('PublicHome')
    else:
        form=FundAllocationForm()
    return render(request,'public/fund_allocation.html',{'form':form})

def FundAllocationRequestList(request):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    user=get_object_or_404(Login,id=request.session['public_id'])
    requests=FundAllocationModel.objects.filter(login_id=user)
    return render(request,'public/fund_allocation_list.html',{'requests':requests})

def FundAllocationRequestEdit(request,id):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    req=get_object_or_404(FundAllocationModel,id=id)
    if request.method=="POST":
        form=FundAllocationForm(request.POST,request.FILES, instance=req)
        if form.is_valid():
            form.save()
            return redirect('FundAllocationRequestList')
    else:
            form=FundAllocationForm(instance=req)
    return render(request,'public/edit_fund_allocation.html',{'form':form})

def FundAllocationRequestDelete(request,id):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    req=get_object_or_404(FundAllocationModel,id=id)
    req.delete()
    return redirect('FundAllocationRequestList')

def FundAllocationRequestView(request):
    context = get_user_counts_context()
    requests=FundAllocationModel.objects.all()
    context['requests'] = requests
    return render(request,'admin/fund_allocation_table.html',context)
     

def ReScheduleDuty(request,camp,volunteer):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin') 
    vol=get_object_or_404(Volunteer,id=volunteer)
    c=get_object_or_404(Camp,id=camp)
    realloc=get_object_or_404(Duty,volunteer_id=vol)
    if request.method =="POST":
        form=DutyForm(request.POST,instance=realloc)
        if form.is_valid():
            form.save()
            messages.success(request,'Duty successfully scheduled')
            return redirect('AllocatedVolList')
    else:
        form=DutyForm(instance=realloc)
    return render(request,'camp/vol_duty_reschedule.html',{'form':form})

def ReportMissingPerson(request,id):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin')
    a=get_object_or_404(Login,id=session_id)
    user=get_object_or_404(Public,login_id=a)
    b=get_object_or_404(Login,id=id)
    station=get_object_or_404(Police,login_id=b)
    if request.method =="POST":
        form=MissingPersonForm(request.POST,request.FILES)
        if form.is_valid():
            a=form.save(commit=False)
            a.public_id=user
            a.station_id=station
            a.save() 
            messages.success(request,'public/missing_report.html',{'form':form})
            return redirect('PublicHome')
    else:
        form=MissingPersonForm()
    return render(request,'public/missing_report.html',{'form':form})


def ViewMissingReports(request):
    session_id=request.session.get('station_id')
    if not session_id:
        return redirect('UserLogin') 
    a=get_object_or_404(Police,login_id=session_id)
    reports=MissingPerson.objects.filter(station_id=a)
    return render(request,'police/missing_report_table.html',{'reports':reports}) 
  
def ViewFundAllocationRequest(request,id):
    view=get_object_or_404(FundAllocationModel,id=id)
    return render(request,'admin/view_fund_request.html',{'view':view})

def Payment(request,id,amount):
    req=get_object_or_404(FundAllocationModel,id=id)
    if request.method=="POST":
        form=FundPaymentForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.req_id = req
            a.amount = amount
            a.save()
            req.status = 1
            req.save()
            return redirect('FundAllocationRequestView') 
    else:
        form2=FundPaymentForm()
    return render(request,'admin/fund_payment.html',{'form2':form2,'id':id,'amount':amount})

def AllocateFund(request,id):
    if request.method == "POST":
        amount=request.POST.get('amount')
        return redirect(reverse('Payment', kwargs={'id':id, 'amount':amount}))
    return render(request,'admin/allocate_fund.html' ,{'id':id})

 

def StationSearch(request):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin')
    if request.method == "POST":
        query = request.POST.get('stationinfo')
        stations = Police.objects.filter(
            Q(station_id__icontains=query) |
            Q(address_line_1__icontains=query) |
            Q(address_line_2__icontains=query) |
            Q(city__icontains=query)  
        )
        return render(request, 'public/station_search.html', {'stations': stations})
    else:
        return render(request, 'public/station_search.html')
    
def AddMissingStatus(request,id):
    session_id=request.session.get('station_id')
    if not session_id:
        return redirect('UserLogin') 
    id=get_object_or_404(MissingPerson,id=id)
    if request.method == "POST":
       form=MissingPersonStatusForm(request.POST)
       if  form.is_valid():
           a=form.cleaned_data['status']
           id.status=a
           id.save()
           return redirect('ViewMissingReports')
    else:
        form=MissingPersonStatusForm()
    return render(request,'police/missing_case_status.html',{'form':form,'id':id})

def EditMissingStatus(request,id):
    session_id=request.session.get('station_id')
    if not session_id:
        return redirect('UserLogin') 
    id=get_object_or_404(MissingPerson,id=id)
    if request.method == "POST":
       form=MissingPersonStatusForm(request.POST,instance=id)
       if  form.is_valid():
           a=form.cleaned_data['status']
           id.status=a
           id.save()
           return redirect('ViewMissingReports')
    else:
        form=MissingPersonStatusForm(instance=id)
    return render(request,'police/missing_case_status.html',{'form':form })

def DeleteMissingStatus(request,id):
    session_id=request.session.get('station_id')
    if not session_id:
        return redirect('UserLogin')
    stat=get_object_or_404(MissingPerson,id=id)
    stat.status=None
    stat.save()
    return redirect('ViewMissingReports')


def ViewMissingList(request):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin') 
    login=get_object_or_404(Login,id=session_id)
    public=get_object_or_404(Public,login_id=login)
    results=MissingPerson.objects.filter(public_id=public)
    return render(request,'public/missing_person_view.html',{'results':results})

def EmergencyMessageAlert(request):
    if request.method =="POST":
        form=EmergencyAlertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('EmergencyMessageAlert')
    else:
        form=EmergencyAlertForm()
    return render(request,'admin/emergency_alert.html',{'form':form})

def EmergencyAlertList(request):
    results=EmergencyAlert.objects.all()
    return render(request,'admin/emergency_alert_list.html',{'results':results})

def EditEmergencyAlert(request,id):
    alert=get_object_or_404(EmergencyAlert,id=id)
    if request.method =="POST":
        form=EmergencyAlertForm(request.POST,instance=alert)
        if form.is_valid():
            form.save()
            return redirect('EmergencyAlertList')
    else:
        form=EmergencyAlertForm(instance=alert)
    return render(request,'admin/emergency_alert.html',{'form':form,'alert':alert})

def DeleteEmergencyAlert(request,id):
    alert=get_object_or_404(EmergencyAlert,id=id)
    alert.delete()
    return redirect('EmergencyAlertList')


def EmergencyAlertView(request):
    results=EmergencyAlert.objects.all()
    return render(request,'common/emergency_alert_view.html',{'results':results})

def TableCamp(request):
    camps=Camp.objects.all()
    return render(request,'public/camp_table_enq.html',{'camps':camps})

def CampEnquiry(request,id):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin')
    camp_login=get_object_or_404(Login,id=id)
    public_id=get_object_or_404(Public,login_id=session_id)
    if request.method == "POST":
        form=EnquiryForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.camp=camp_login
            a.public=public_id
            a.save()
            return redirect('TableCamp')
    else:
        form=EnquiryForm()
    return render(request,'public/camp_enq.html',{'form':form})


def EnquiryTable(request):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    id=get_object_or_404(Login,id=session_id)
    results=Enquiry.objects.filter(camp=id)
    return render(request,'camp/public_enq_table.html',{'results':results})

def EnquiryReply(request,id):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    id=get_object_or_404(Enquiry,id=id) 
    if request.method == "POST":
       form=EnquiryResponseForm(request.POST)
       if  form.is_valid():
           a=form.cleaned_data['response']
           id.response=a
           id.save()
           return redirect('EnquiryTable')
    else:
        form=EnquiryResponseForm()
    return render(request,'camp/enq_response.html',{'form':form ,'id':id})

def EnqResponseTable(request):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin')
    id=get_object_or_404(Login,id=session_id)
    p=get_object_or_404(Public,login_id=id)
    results=Enquiry.objects.filter(public=p)
    return render(request,'public/enq_response_table.html',{'results':results})

def VehicleMissing(request,id):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin')
    public_id=get_object_or_404(Login,id=session_id)
    # vehicle_id=get_object_or_404(Login,id=public_id)
    station_id=get_object_or_404(Police,login_id=id)
    if request.method == "POST":
        form=VehicleForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.public=public_id
            a.police=station_id
            a.save()
            return redirect('PublicHome')
    else:
        form=VehicleForm()
    return render(request,'public/vehicle_missing_form.html',{'form':form})


def VehicleMissingReports(request):
    session_id=request.session.get('station_id')
    if not session_id:
        return redirect('UserLogin')
    a=get_object_or_404(Police,login_id=session_id)
    reports=Vehicle.objects.filter(police=a)
    return render(request,'police/vehicle_missing_table.html',{'reports':reports})

def VehicleStatus(request,id):
    session_id=request.session.get('station_id')
    if not session_id:
        return redirect('UserLogin')
    vehicle_id=get_object_or_404(Vehicle,id=id)
    if request.method == "POST":
        form=VehicleStatusForm(request.POST)
        if form.is_valid():
            a=form.cleaned_data['status']
            vehicle_id.status=a
            vehicle_id.save()
            return redirect('VehicleMissingReports')
    else:
        form=VehicleStatusForm()
    return render(request,'police/missing_case_status.html',{'form':form})

def EditVehicleStatus(request,id):
    session_id=request.session.get('station_id')
    if not session_id:
        return redirect('UserLogin')
    vehicle_id=get_object_or_404(Vehicle,id=id)
    if request.method == "POST":
        form=VehicleStatusForm(request.POST,instance=vehicle_id)
        if form.is_valid():
            a=form.cleaned_data['status']
            vehicle_id.status=a
            vehicle_id.save()
            return redirect('VehicleMissingReports')
    else:
        form=VehicleStatusForm(instance=vehicle_id)
    return render(request,'police/missing_case_status.html',{'form':form})

def DeleteVehicleStatus(request,id):
    session_id=request.session.get('station_id')
    if not session_id:
        return redirect('UserLogin')
    vehicle_id=get_object_or_404(Vehicle,id=id)
    vehicle_id.status=None
    vehicle_id.save()
    return redirect('VehicleMissingReports')

def VehicleList(request):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin')
    id=get_object_or_404(Login,id=session_id)
    reports=Vehicle.objects.filter(public=id)
    return render(request,'public/missing_vehicle_list.html',{'reports':reports})


def ComfirmPassCamp(request):
    session_id=request.session.get('camp_id')
    if not session_id:
        return redirect('UserLogin')
    id=get_object_or_404(Login,id=session_id)
    if request.method == "POST":
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            curr=form.cleaned_data['current_pass']
            new=form.cleaned_data['new_pass']
            confirm=form.cleaned_data['confirm_pass']

            if id.password == curr:
                if new == confirm:
                    id.password=confirm
                    id.save()
                    messages.success(request,'password updated.')
                    return redirect('CampHome')
                else:
                    messages.error(request,'New and confirm should be the same.')
                    return redirect('ComfirmPassCamp')
            else:
                messages.error(request,'Incorrect password.')
                return redirect('ComfirmPassCamp')
    else:
        form=ChangePasswordForm()

    return render(request,'common/change_password.html',{'form':form})


def ComfirmPassPublic(request):
    session_id=request.session.get('public_id')
    if not session_id:
        return redirect('UserLogin')
    id=get_object_or_404(Login,id=session_id)
    if request.method == "POST":
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            curr=form.cleaned_data['current_pass']
            new=form.cleaned_data['new_pass']
            confirm=form.cleaned_data['confirm_pass']

            if id.password == curr:
                if new == confirm:
                    id.password=confirm
                    id.save()
                    messages.success(request,'password updated.')
                    return redirect('PublicHome')
                else:
                    messages.error(request,'New and confirm should be the same.')
                    return redirect('ComfirmPassCamp')
            else:
                messages.error(request,'Incorrect password.')
                return redirect('ComfirmPassCamp')
    else:
        form=ChangePasswordForm()

    return render(request,'common/change_password.html',{'form':form})


def ComfirmPassVolunteer(request):
    session_id=request.session.get('volunteer_id')
    if not session_id:
        return redirect('UserLogin')
    id=get_object_or_404(Login,id=session_id)
    if request.method == "POST":
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            curr=form.cleaned_data['current_pass']
            new=form.cleaned_data['new_pass']
            confirm=form.cleaned_data['confirm_pass']

            if id.password == curr:
                if new == confirm:
                    id.password=confirm
                    id.save()
                    messages.success(request,'password updated.')
                    return redirect('VolunteerHome')
                else:
                    messages.error(request,'New and confirm should be the same.')
                    return redirect('ComfirmPassCamp')
            else:
                messages.error(request,'Incorrect password.')
                return redirect('ComfirmPassCamp')
    else:
        form=ChangePasswordForm()

    return render(request,'common/change_password.html',{'form':form})

def ComfirmPassStation(request):
    session_id=request.session.get('station_id')
    if not session_id:
        return redirect('UserLogin')
    id=get_object_or_404(Login,id=session_id)
    if request.method == "POST":
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            curr=form.cleaned_data['current_pass']
            new=form.cleaned_data['new_pass']
            confirm=form.cleaned_data['confirm_pass']

            if id.password == curr:
                if new == confirm:
                    id.password=confirm
                    id.save()
                    messages.success(request,'password updated.')
                    return redirect('StationHome')
                else:
                    messages.error(request,'New and confirm should be the same.')
                    return redirect('ComfirmPassCamp')
            else:
                messages.error(request,'Incorrect password.')
                return redirect('ComfirmPassCamp')
    else:
        form=ChangePasswordForm()

    return render(request,'common/change_password.html',{'form':form})


def AddProduct(request):
    session_id=request.session['camp_id']
    camp=get_object_or_404(Login,id=session_id)
    if request.method == "POST":
        form=ProductForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.camp_id=camp
            a.save()
            messages.success(request,"Product added successfully.")
            return redirect('ViewProduct')

    else:
        form=ProductForm()
    return render(request,'camp/add_prod.html',{'form':form})

def ViewProduct(request):
    session_id=request.session['camp_id']
    camp=get_object_or_404(Login,id=session_id)
    prods=Product.objects.filter(camp_id=camp)    
    for prod in prods:
        if prod.quantity <= 10:
            messages.warning(request,f'{prod.prod_name} is running low.')
    return render(request,'camp/prod_list.html',{'prods':prods})

def EditProduct(request,id):
    prod=get_object_or_404(Product,id=id)
    if request.method == "POST":
        form=ProductForm(request.POST,instance=prod)
        if form.is_valid():
            form.save()
            return redirect('ViewProduct')
    else:
        form=ProductForm(instance=prod)
    return render(request,'camp/edit_prod.html',{'form':form})

def DeleteProduct(request,id):
    prod=get_object_or_404(Product,id=id)
    prod.delete()
    return redirect('ViewProduct')

def ProdUsage(request,id):
    session_id=request.session['camp_id']
    camp=get_object_or_404(Login,id=session_id)
    prod=get_object_or_404(Product,id=id)
    if request.method == "POST":
        form=ProductUsageForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['prod_quantity']
            prod.quantity -= int(quantity)
            prod.save()
            a=form.save(commit=False)
            a.prod_id = prod
            a.camp_id=camp
            a.save()
            return redirect('ViewProduct')
    else:
        form=ProductUsageForm()
    
    return render(request,'camp/prod_usage.html',{'form':form})
            
def MonthlyReport(request):
    session_id=request.session['camp_id']
    camp=get_object_or_404(Login,id=session_id)
    current_month=datetime.now().month
    current_year=datetime.now().year
    months=ProductUsage.objects.filter(
         Q(camp_id=camp) &
         Q(current_date__icontains=current_month) &
         Q(current_date__icontains=current_year)
    )   # for filtering current month and year
    return render(request,'camp/monthly_report.html',{'months':months})


def PerDayReport(request):  
    session_id=request.session.get('camp_id')
    camp=get_object_or_404(Login,id=session_id)
    if request.method == "POST":
        query = request.POST.get('date')
        days = ProductUsage.objects.filter( 
            Q(current_date__icontains=query) &
            Q(camp_id=camp) 
        )
        return render(request, 'camp/per_day_report.html', {'days': days}) 
    else:
        return render(request, 'camp/per_day_report.html')


#    forgot password section

def send_otp_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Login.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                PasswordResetOTP.objects.create(user=user, otp=otp)
                send_mail(
                    'Your Password Reset OTP',
                    f'Use this OTP to reset your password: {otp}',
                    'dmsproject1234@gmail.com', 
                    [email],
                    fail_silently=False  # Enable error reporting

                )
                return redirect('verify_otp_view',email=email)  # URL for OTP verification
            except Login.DoesNotExist:
                messages.error(request,"No user with this email.")
    else:
        form = EmailForm()
    return render(request, 'common/send_otp.html', {'form': form})

def verify_otp_view(request,email):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp_input = form.cleaned_data['otp']
            try:
                user = Login.objects.get(email=email)
                otp_record = PasswordResetOTP.objects.filter(user=user, otp=otp_input).order_by('-created_at').first()
                if otp_record and otp_record.is_valid():
                    request.session['reset_user_id'] = user.id
                    return redirect('reset_password_view')  # URL for password reset form
                else:
                    form.add_error('otp', 'Invalid or expired OTP.')
            except Login.DoesNotExist:
                form.add_error('email', 'No user with this email.')
    else:
        form = OTPForm()
    return render(request, 'common/verify_otp.html', {'form': form,'email':email})


def reset_password_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('send_otp')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = Login.objects.get(id=user_id)
            user.password = form.cleaned_data['new_password']          # make_password(form.cleaned_data['new_password'])
            user.save()
            del request.session['reset_user_id']
            return redirect('UserLogin')
    else:
        form = ResetPasswordForm()
    return render(request, 'common/reset_password.html', {'form': form})



#            API and alogrithm starts from here

import requests

API_KEY = "7c8f76a84fb1b06e3990c51bedf0a2fa"


def get_weather(request):
    latitude = request.GET.get("lat", None)
    longitude = request.GET.get("lon", None)

    if not latitude or not longitude:
        return render(request, "public/weather.html", {"error": "Location not provided!"})

    URL = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"
    response = requests.get(URL)
    data = response.json()

    if response.status_code == 200:
        prediction = predict_disaster(data)
        context = {
            "latitude": latitude,
            "longitude": longitude,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "weather_condition": data["weather"][0]["description"],
            "prediction": prediction
        }
    else:
        context = {"error": "Could not fetch weather data"}

    return render(request, "public/weather.html", context)

def predict_disaster(data):
    """Predict disaster risk based on weather data"""
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    weather_condition = data["weather"][0]["main"]

    if weather_condition in ["Thunderstorm", "Tornado"]:
        return "⚠️ High Risk of Storm"
    elif weather_condition == "Rain" and humidity > 80:
        return "⚠️ Flood Risk Due to Heavy Rain"
    elif temp > 40 and humidity < 30:
        return "🔥 Extreme Heat Warning"
    else:
        return "✅ No Disaster Risk Detected"

from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
import os
import face_recognition
from .forms import misscheck
from .models import MissingPerson

def encode_image(image_path):
    """Load and encode a face from an image path."""
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None

def misschecking(request):
    if request.method == 'POST':
        form = misscheck(request.POST, request.FILES)
        if form.is_valid():
            uploaded_pic = form.cleaned_data['pic']

            # Save the uploaded image temporarily
            file_path = default_storage.save(f'temp/{uploaded_pic.name}', uploaded_pic)
            full_file_path = default_storage.path(file_path)

            # Encode the uploaded face
            uploaded_encoding = encode_image(full_file_path)

            matches = []

            if uploaded_encoding is not None:
                for person in MissingPerson.objects.all():
                    stored_image_path = person.photo.path

                    # Double-check the file exists (usually not needed if using person.photo.path)
                    if not os.path.exists(stored_image_path):
                        print(f"Image not found: {stored_image_path}")
                        continue

                    known_encoding = encode_image(stored_image_path)

                    if known_encoding is not None:
                        result = face_recognition.compare_faces([known_encoding], uploaded_encoding)
                        if result and result[0]:
                            matches.append(person)

            # Clean up: delete temp file
            if os.path.exists(full_file_path):
                os.remove(full_file_path)

            return render(request, 'police/miss_checking.html', {
                'form': form,
                'matches': matches
            })

    else:
        form = misscheck()
    return render(request, 'police/miss_checking.html', {'form': form})