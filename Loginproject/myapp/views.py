from base64 import urlsafe_b64decode
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import logout,login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
import random


from .models import EmailVerification





def home(request):
    return render(request, "Loginproject/index.html")


def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username= username):
            messages.error(request, " Username is already Exist")
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, " Email is already Exist")
            return redirect('signup')
        
        if len(username)>10:
            messages.error(request, "Username is too long")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords did not match" )
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        
        myuser.is_active = False
        
        
        myuser.save()
        
        messages.success(request, "your account has been successfully created")
        
        # Welcome Email
        
        subject = "Welcome to Danial's Website  -  Login confirmation!!"
        message = " Hello " + myuser.first_name + "!! \n Welcome to my website \n PLEASE CONFIRM YOUR EMAIL, WE SEND YOU THE VERIFICATION CODE! "
        form_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, form_email, to_list, fail_silently=False)
        
        # Email Address Confirmation
        
#        current_site = get_current_site(request)
 #       email_subject = "Confirm your email @ my site - django login!!"
  #      message2 =  render_to_string('email_confirmation.html',{
   #         'name' : myuser.first_name,
    #        'domain': current_site.domain,
     #       'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
      #      'token' : generate_token.make_token(myuser)
       # })
      # email = EmailMessage(
     #       email_subject,
    #        message2,
    #        settings.EMAIL_HOST_USER,
    #        [myuser.email]
    #    )
     #   email.fail_silently = True
     #   email.send()
     #   
     # In your signup view:
        if myuser.is_active == False:
            verification = EmailVerification.objects.create(user=myuser)
            send_verification_email(myuser, verification.verification_code)

        return redirect('verify_email') 
        
        
    return render(request,"Loginproject/signup.html" )




def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)

        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "Loginproject/index.html", {'fname': fname})
            
        else:
            messages.error(request, "bad credentials")
            return redirect('home')
            
        
    return render(request, "Loginproject/signin.html")



def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')



#def activate(request, uidb64, token):
 #   try:
  #      uid = force_str(urlsafe_b64decode(uidb64))
  #      myuser = User.objects.get(pk=uid)
  #  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
  #      myuser = None
  #      
  #  if myuser is not None and generate_token.check_token(myuser, token):
  #      myuser.is_active = True
  #      myuser.save()
  #      login(request, myuser)
  #      return redirect('home')
  #  else:
  #      return render(request, 'activation_failed.html')
    
    
def activate(request, uidb64, token):
    try:
        # Decode the UID
        uid = force_str(urlsafe_b64decode(uidb64))
        # Retrieve the user corresponding to the UID
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    # If the user exists and the token checks out, activate the account
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        # Redirect to a success page, for example 'home'
        return redirect('home')
    else:
        # If there was an error, display some error message or redirect
        return render(request, 'activation_invalid.html')  # Provide a template for an invalid or expired token
    
    
    
    
def generate_verification_code(length=6):
    """Generate a random numerical verification code."""
    return str(random.randint(10**(length-1), 10**length - 1))
    
    
def send_verification_email(user, verification_code):
    verification = EmailVerification.objects.get(user=user)

    send_mail(
        'Verify your email',
        f'Please use the following code to verify your email address: {verification.verification_code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    
    
    

def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            verification = EmailVerification.objects.get(verification_code=code)
            user = verification.user
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, 'Your email has been verified successfully!')
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('home')
            else:
                messages.warning(request, 'This account is already active.')
        except EmailVerification.DoesNotExist:
            messages.error(request, 'Invalid verification code.')
    return render(request, 'verify_email.html')
