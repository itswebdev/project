from django import forms
from .models import *
# from .models import Camp, Login, Police, Public, Volunteer, CampUser,CampNeeds,CampAlert,VolunteerRequest,Complaint,Duty,FundAllocationModel,FundPayment,EmergencyAlert

class CampForm(forms.ModelForm):
    
    class Meta:
        model=Camp
        fields=['camp_name','full_address','district','city','panchayath','thaluk','contact']

class LoginForm(forms.ModelForm):
    class Meta:
        model=Login
        fields=['email','password']

class PoliceForm(forms.ModelForm):
    class Meta:
        model=Police
        fields=['station_id','address_line_1','address_line_2','district','city','contact']

class PublicForm(forms.ModelForm):
    class Meta:
        model=Public
        fields=['fullname','address','pincode','district','city','panchayath','village','contact']

class VolunteerForm(forms.ModelForm):
    class Meta:
        model=Volunteer
        fields=['volunteer_name','gender','date_of_birth','aadhar_no','contact']
        widgets={
            'date_of_birth' : forms.DateInput(attrs={'class':'form-control','type':'date'})
        }

class LoginCheck(forms.Form):
    email=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)

class LoginEditForm(forms.ModelForm): # form for profile editing
    class Meta:
        model=Login
        fields=['email']


class CampUserForm(forms.ModelForm):
    class Meta:
        model=CampUser
        fields=['photo','full_name','address','district','city','contact_no','aadhar_no','panchayath','village','thaluk']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'custom-input peer',
                'placeholder': '',
                'required': True,
                'pattern': '^[A-Za-z ]{2,50}$',
                'title': 'Name must be letters and spaces only (2–50 characters)'
            }),
            'address': forms.TextInput(attrs={
                'class': 'custom-input',
                'placeholder': 'Address',
                'required': True,
                'pattern': '^[A-Za-z ]{2,50}$',
                'title': 'Name must be letters and spaces only (2–50 characters)'
            }),
         }

class CampNeedsForm(forms.ModelForm):
    class Meta:
        model=CampNeeds
        fields=['needs'] 

class CampAlertForm(forms.ModelForm):
    class Meta:
        model=CampAlert
        fields=['emergency_message']

class VolunteerReqForm(forms.ModelForm):
    class Meta:
        model=VolunteerRequest
        fields=['no_of_volunteers','volunteer_details']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=['complaint_sub','complaint']

class ComplaintReplyForm(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=['reply']

CHOICES = [
    ('Cooking', 'Cooking'),
    ('Cleaning', 'Cleaning'),
    ('Cloth collecting', 'Cloth collecting'),
]

class DutyForm(forms.ModelForm):
    spec = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Duty
        fields = ['spec', 'duty']

class FundAllocationForm(forms.ModelForm):
    class Meta:
        model=FundAllocationModel
        fields=['image','full_name','full_address','district','city','panchayath','ration_card_no','contact','other_details']


class MissingPersonForm(forms.ModelForm):
    class Meta: 
        model=MissingPerson
        fields=['photo','name','address','gender','age','other_details']

class MissingPersonStatusForm(forms.ModelForm):
    class Meta:
        model=MissingPerson
        fields=['status']

class FundPaymentForm(forms.ModelForm):
    class Meta:
        model=FundPayment
        fields=['name_on_card','card_no','expiring_date','cvv_no']
        widgets={
            'expiring_date' : forms.DateInput(attrs={'class':'form-control','type':'date'})
        }
        
class EmergencyAlertForm(forms.ModelForm):
    class Meta:
        model=EmergencyAlert
        fields=['alert_message']

class EnquiryForm(forms.ModelForm):
    class Meta:
        model=Enquiry
        fields=['enq']

class EnquiryResponseForm(forms.ModelForm):
    class Meta:
        model=Enquiry
        fields=['response']

class VehicleForm(forms.ModelForm):
    class Meta:
        model=Vehicle
        fields=['category','company','model_name','vehicle_num','missing_place','missing_date']
        widgets={
            'missing_date':forms.DateInput(attrs={'class':'form-control','type':'date'})
        }
    
class VehicleStatusForm(forms.ModelForm):
    class Meta:
        model=Vehicle
        fields=['status']


class ChangePasswordForm(forms.Form):                   #      form for changing passwo
    current_pass=forms.CharField(max_length=30)
    new_pass=forms.CharField(widget=forms.PasswordInput)
    confirm_pass=forms.CharField(widget=forms.PasswordInput)


products=[
    ('','--select an option--'),
    ('Cloths' , 'Cloths'),
    ('Food items' , 'Food items'),
    ('Medicines' , 'Medicines'),
]

class ProductForm(forms.ModelForm):

    prod_category = forms.ChoiceField(
        choices=products
        # widget=forms.Select(attrs={'placeholder': 'Select a category'})
    )

    class Meta:
        model = Product
        fields = ['prod_category', 'prod_name', 'quantity', 'prod_description']
        widgets = {
            'prod_name': forms.TextInput(attrs={'placeholder': 'Enter product name'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
            'prod_description': forms.Textarea(attrs={'placeholder': 'Enter product description'}),
        }

class ProductUsageForm(forms.ModelForm):
    class Meta:
        model=ProductUsage
        fields=['prod_quantity']


class ReportSearchForm(forms.Form):
    date = forms.DateInput(attrs={'class':'form-control','type':'date'})

#  forgot password section

class EmailForm(forms.Form):  
    email = forms.EmailField()


class OTPForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(max_length=6)


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match.")


class misscheck(forms.Form):
    pic=forms.ImageField()