from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# from phonenumber_field.formfields import PhoneNumberField
from .models import Customer,ProductVariation

# from .tokens import account_activation_token




class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'})) 

# class CustomerRegistrationForm(UserCreationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
#     password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
     
#     class Meta:
#         model = User
#         fields = ['username','email','password1','password2']
        
class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already associated with an account.")
        return email
        
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Current Password",  widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    
    
    

        
        
        
        
        
class MyPasswordResetForm(PasswordResetForm ):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))
    new_password2=forms.CharField(label=' Confirm New Password',widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model  = Customer
        fields = ['name','locality','city','mobile','state','pincode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'pincode':forms.NumberInput(attrs={'class':'form-control'}),
            
            
        }
        

# class CustomerProfileForm(forms.ModelForm):
#     mobile = PhoneNumberField(
#         label='Mobile Number',
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}),
#     )

#     class Meta:
#         model = Customer
#         fields = ['name', 'locality', 'city', 'mobile', 'state', 'pincode']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'locality': forms.TextInput(attrs={'class': 'form-control'}),
#             'city': forms.TextInput(attrs={'class': 'form-control'}),
#             'state': forms.Select(attrs={'class': 'form-control'}),
#             'pincode': forms.NumberInput(attrs={'class': 'form-control'}),
#         }
     

class ProductVariationForm(forms.ModelForm):
    class Meta:
        model =ProductVariation
        fields=['product','quantity','selling_price','discounted_price']