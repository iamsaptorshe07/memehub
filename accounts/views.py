from django.shortcuts import render,redirect,HttpResponse
from accounts.models import UserProfile,OTP
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
import random
import math

# Create your views here.

def otp_generator():
    digits = [i for i in range(0, 10)]
    otp = ""
    for i in range(4):
        index = math.floor(random.random() * 10)
        otp += str(digits[index])
    return otp



#####################################SIGNUP######################################################  

def signup(request):
	if request.user.is_authenticated:
		return redirect('index')
	if request.method == 'POST':
		#Get the post paramaters
		email = request.POST['email']
		name = request.POST.get('name').capitalize()
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']		
		check = UserProfile.objects.filter(email=email).exists()
		if check:
			messages.error(request,f'{email} already exist')
			return redirect('signup')
		else:
			if len(pass1)<5:
				messages.error(request,'Password should be more than 5 character')
				return redirect('signup')
			if pass1.isalnum():
				messages.error(request,'Password should contain at least a special character')
				return redirect('signup')						
			if pass1!=pass2:
				messages.error(request,"Passwords dont match ")
				return redirect('signup')	 	
			user = UserProfile.objects.create_user(email,pass1)
			user.name = name
			user.is_active = False
			user.save()
			otp = OTP.objects.create(otp=otp_generator(),user=user)
			email_from = settings.EMAIL_HOST_USER
			msg = f"Hello {user.email},\nYour OTP for Email Verification is:{otp.otp}\nThanks!\nTeam Memebook"
			send_mail(
			'Welcome to Memebook - Verify Your Email',
			msg,
			email_from,
			[user.email]
			)
			messages.success(request,f'Account Registered.OTP send to {user.email} to Verify Account')
			return redirect('signup')					
	else:
		return render(request,'accounts/signupOTP/signup.html')

def verify_email(request):
	if request.user.is_authenticated:
		return redirect('index')
	if request.method == 'POST':
		email= request.POST['email']
		otp = request.POST['otp']
		register = UserProfile.objects.filter(email=email).exists()
		if register:
			user = UserProfile.objects.filter(email=email,is_active=False).first()
			if user is not None:
				check = OTP.objects.filter(otp=otp,user=user,is_password=False).last()
				if check is not None:
					user.is_active=True
					user.save()
					check.delete()
					messages.success(request,f'Verified {user.email} ')
					return redirect('login')
				else:
					messages.error(request,'Wrong OTP')
					return redirect('verify_email') 
			else:
				messages.error(request,f'Already verified {email}')
				return redirect('login')
		else:
			messages.error(request,f'{email} is not Registered')
			return redirect('signup')			
	return render(request,'accounts/signupOTP/verify_email.html')

############################################################LOGIN################################################
def userLogin(request):
	if request.user.is_authenticated:
		return redirect('index')
	if request.method == 'POST':
		email = request.POST['email']
		loginpass = request.POST['loginpass']
		user = authenticate(username=email, password=loginpass) 
		check = UserProfile.objects.filter(email=email,is_active=True).first()
		register = UserProfile.objects.filter(email=email).first()
		if register is not None:
			if check is not None:
				if user is not None:
					login(request,user)
					messages.success(request,f'Successfully signed in as {user.email}')
					return redirect('profile')			
				else:
					messages.error(request,'Invalid Credential')
					return redirect('login')		
			else:
				messages.error(request,f'User {email} is inactive')
				return redirect('signup')
		else:									
			messages.error(request,f'{email} is not Registered')
			return redirect('login')
	return render(request,'accounts/login.html')  
def userLogout(request): 
  logout(request)
  messages.success(request,'Successfully Logout')
  return redirect('login')	