from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from .ml_functions.cocoa_predict import predict_cocoa_disease

from django.http import JsonResponse #chatbot
from .ml_functions.chatbot_engine import get_bot_response #for chatbot
import json

from .decorators import role_required

# ================= ML MODULES =================
from .ml_functions.disease_predict import predict_disease
from .ml_models.soil_ai import predict_soil_ai

# ================= MODELS =================
from .models import (
    Profile,
    Farmer,
    AgricultureOfficer,
    Crop,
    DiseaseReport,
    FarmerQuery,
    MarketPrice,
    Feedback,
    SoilRecommendation,
    FertilizerRecommendation
)

# =====================================================
# HOME
# =====================================================
def home(request):
    return render(request, 'home.html')


#login (home - login - farmer dash)
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate( request,username=username,password=password)
#authenticate() checks auth_user (User model) , returns User object fields like username,password
        if user:
            login(request, user)
#login() stores request.session[] of user , access by request.user or (request.user.username)
            print("IN REQUEST:",user)

            if user.is_superuser:
                return redirect('/adminpanel/dashboard/')

            role = user.profile.role
            if role == 'admin':
                return redirect('/adminpanel/dashboard/')
            elif role == 'officer':
                return redirect('/officer/dashboard/')
            else:
                return redirect('/farmer/dashboard/')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


def farmer_register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        profile_pic = request.FILES.get('profile_pic') #optional do get()

        if User.objects.filter(username=username).exists():
            return render(request, 'farmer/register.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

         #To create the profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = 'farmer'
        profile.save()


       
        Farmer.objects.create(
            user=user,
            phone=request.POST['phone'],
            region=request.POST['region'],
            profile=profile_pic,
        )

        return redirect('/login/')

    return render(request, 'farmer/register.html')


#Famer Module
@role_required(allowed_roles=['farmer'])
def farmer_dashboard(request):
    print("USER(farmer):",request.user.username)

    crop_count = DiseaseReport.objects.filter(farmer__user=request.user) \
                                  .values('crop_name') \
                                  .distinct() \
                                  .count()
    crops=Crop.objects.filter(user=request.user)

    return render(request, 'farmer/dashboard.html', {
        'prices': MarketPrice.objects.all()[:5],
        'reports': DiseaseReport.objects.filter(farmer__user=request.user),
        'crop_count':crop_count,
        'crops':crops,
        
    })


@role_required(allowed_roles=['farmer'])
def disease_detection(request):

    if request.method == "POST":

        fs = FileSystemStorage()
        filename = fs.save(
            request.FILES['image'].name,
            request.FILES['image']
        )

        image_path = fs.path(filename)

        crop_name = request.POST['crop_name']
        crop = crop_name.strip().lower()

        cocoa_words = [
            "cocoa",
            "cacao",
            "cococa",
            "cocao",
            "coocoa"
        ]

        # Choose model (cocoa or potato/tomato)
        if crop in cocoa_words:
            predictions = predict_cocoa_disease(image_path)
            model="cocoa_disease_model"
        else:
            predictions = predict_disease(image_path)
            model="potato_tomato_model"

        DiseaseReport.objects.create(
            farmer=Farmer.objects.get(user=request.user),
            crop_name=crop_name,
            image=filename,
            detected_disease=predictions[0]['disease'],
            verified_by_officer=False
        )

        print("IMP & SYM :",predictions)

        return render(request, 'farmer/disease_result.html', {
            'predictions': predictions,
            'model':model,
        })

    return render(request, 'farmer/disease_upload.html')

@role_required(allowed_roles=['farmer'])
def farmer_all_results(request):
    user = request.user
    farmer = Farmer.objects.get(user=user)
    Reports = DiseaseReport.objects.filter(farmer=farmer).order_by('-created_at')

    if request.method == "POST":  #to delete the report
        report_id = request.POST.get('report_id')
        row = DiseaseReport.objects.get(id=report_id)
        row.delete()


    return render(request,'farmer/all_results.html',
                  {
                    'Reports':Reports
                  })

@role_required(allowed_roles=['farmer'])
def send_query(request):
    if request.method == "POST":
        FarmerQuery.objects.create(
            farmer=Farmer.objects.get(user=request.user),
            question=request.POST['question']
        )
        return render(request,'farmer/send_query.html')

    return render(request, 'farmer/send_query.html')


@role_required(allowed_roles=['farmer'])
def submit_feedback(request):
    if request.method == "POST":
        Feedback.objects.create(
            farmer=Farmer.objects.get(user=request.user),
            message=request.POST['message']
        )
        return redirect('/farmer/dashboard/')

    return render(request, 'farmer/feedback.html')


@role_required(allowed_roles=['farmer'])
def farmer_queries(request):
    return render(request, 'farmer/view_replies.html', {
        'queries': FarmerQuery.objects.filter(
            farmer=Farmer.objects.get(user=request.user)
        )
    })


@role_required(allowed_roles=['farmer'])
def farmer_crops(request):

    if request.method == "POST":
        cropname = request.POST['cropname']
        farmer = request.user

        Crop.objects.create(name=cropname , user=farmer, )

        crops=Crop.objects.filter(user=request.user)

        return render(request, 'farmer/view_crops.html',
                      {
                          'crops':crops,
                      })


    crops=Crop.objects.filter(user=request.user)
    return render(request, 'farmer/view_crops.html',{'crops':crops})


@role_required(allowed_roles=['farmer'])
def farmer_market_prices(request):
    crop_count=MarketPrice.objects.values('crop').distinct().count()
    print(crop_count,":CROP COUNT")
    return render(request, 'farmer/market_prices.html', {
        'prices': MarketPrice.objects.all(),
        'crop_count':crop_count,
    })


@role_required(allowed_roles=['farmer'])
def smart_soil_recommendation(request):

    result = None

    if request.method == "POST":
        crop = request.POST['crop']
        weather = request.POST['weather']

        result = predict_soil_ai(crop, weather)

    return render(request, "farmer/smart_soil.html", {
        "result": result
    })

@role_required(allowed_roles=['farmer']) #farmer profile
def farmer_profile(request):
    user = request.user
    farmer = Farmer.objects.get(user=user)

    crop_count = Crop.objects.filter(user=request.user).count()
    crop = Crop.objects.filter(user=request.user)

    report = DiseaseReport.objects.filter(farmer=farmer).order_by('-created_at')
    report_count = report.count()
    
    query = FarmerQuery.objects.filter(farmer=farmer)
    query_count = query.count()
    reply_count = query.filter(reply__isnull=False).exclude(reply="").count()

    print("PIC:",user.farmer.profile)

    return render(request,'farmer/profile.html',
                  {
                      'user':user , 
                      'crop':crop ,
                      'crop_count':crop_count,
                      'report':report,
                      'report_count':report_count,
                      'query_count':query_count,
                      'query':query,
                      'reply_count':reply_count,
                  })


@role_required(allowed_roles='farmer')
def edit_profile(request):
    user = request.user
    print("USER email:",user.email)
    farmer = Farmer.objects.filter(user=user)

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        region = request.POST.get('region')
        address = request.POST.get('address')

        profile_pic = request.FILES.get('profile_pic') #optional do get()

        print("EDIT NAME:",name)

        edit_row_user = User.objects.get(id=user.id) #User table
        edit_row_farmer = Farmer.objects.get(user=user) #Farmer table

        if name:
            edit_row_user.username=name
        if email:
            edit_row_user.email=email
        if password:
            edit_row_user.set_password(password)
        if region:
            edit_row_farmer.region=region
        if address:
            edit_row_farmer.address=address
        if profile_pic:
            edit_row_farmer.profile=profile_pic

        edit_row_user.save()
        edit_row_farmer.save()

    return render(request,'farmer/edit_profile.html',
                  {
                      'farmer':farmer,
                      'user':user,
                  })

#=====================================
#ChatBot
def chatbot_page(request):
    return render(request, 'farmer/chatbot.html')

def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        msg = data.get('message')

        if not msg:
            return JsonResponse({'response': 'Empty Message'})

        reply = get_bot_response(msg)

        return JsonResponse({'response': reply})

    return JsonResponse({'response': 'Invalid request'})

# =====================================================
# OFFICER MODULE
# =====================================================
@role_required(allowed_roles=['officer'])
def officer_dashboard(request):
    return render(request, 'officer/dashboard.html', {
        'reports': DiseaseReport.objects.all(),
        'queries': FarmerQuery.objects.all(),
        'feedbacks': Feedback.objects.all()
    })


@role_required(allowed_roles=['officer'])
def officer_verify_disease(request, report_id):
    report = DiseaseReport.objects.get(id=report_id)

    if request.method == "POST":
        report.treatment = request.POST['treatment']
        report.verified_by_officer = True
        report.save()
        return redirect('/officer/dashboard/')

    return render(request, 'officer/verify_disease.html', {'report': report})


@role_required(allowed_roles=['officer'])
def reply_query(request, query_id):
    query = FarmerQuery.objects.get(id=query_id)

    if request.method == "POST":
        query.reply = request.POST['reply']
        query.replied = True
        query.save()
        return redirect('/officer/dashboard/')

    return render(request, 'officer/reply_query.html', {'query': query})


# =====================================================
# ADMIN MODULE
# =====================================================
@role_required(allowed_roles=['admin'])
def admin_dashboard(request):
    return render(request, 'adminpanel/dashboard.html', {
        'farmer_count': Farmer.objects.count(),
        'officer_count': AgricultureOfficer.objects.count(),
        'crop_count': Crop.objects.count(),
        'report_count': DiseaseReport.objects.count()
    })


@role_required(allowed_roles=['admin'])
def manage_farmers(request):
    return render(request, 'adminpanel/farmers.html', {
        'farmers': Farmer.objects.all()
    })


@role_required(allowed_roles=['admin'])
def manage_officers(request):
    return render(request, 'adminpanel/officers.html', {
        'officers': AgricultureOfficer.objects.all()
    })


@role_required(allowed_roles=['admin'])
def manage_crops(request):
    if request.method == "POST":
        Crop.objects.create(
            name=request.POST['name'],
            suitable_soil=request.POST['suitable_soil'],
            season=request.POST['season']
        )
        return redirect('/adminpanel/crops/')

    return render(request, 'adminpanel/crops.html', {
        'crops': Crop.objects.all()
    })


@role_required(allowed_roles=['admin'])
def manage_market_prices(request):
    if request.method == "POST":
        MarketPrice.objects.create(
            crop=Crop.objects.get(id=request.POST['crop']),
            price=request.POST['price'],
            date=request.POST['date']
        )
        return redirect('/adminpanel/market-prices/')

    return render(request, 'adminpanel/market_prices.html', {
        'prices': MarketPrice.objects.all(),
        'crops': Crop.objects.all()
    })


@role_required(allowed_roles=['admin'])
def add_officer(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        user.profile.role = 'officer'
        user.profile.save()

        AgricultureOfficer.objects.create(
            user=user,
            region=request.POST['region'],
            qualification=request.POST['qualification']
        )

        return redirect('/adminpanel/officers/')

    return render(request, 'adminpanel/add_officer.html')


@role_required(allowed_roles=['admin'])
def edit_officer(request, officer_id):
    officer = AgricultureOfficer.objects.get(id=officer_id)

    if request.method == "POST":
        officer.user.username = request.POST['username']
        officer.region = request.POST['region']
        officer.qualification = request.POST['qualification']

        if request.POST.get('password'):
            officer.user.set_password(request.POST['password'])

        officer.user.save()
        officer.save()
        return redirect('/adminpanel/officers/')

    return render(request, 'adminpanel/edit_officer.html', {'officer': officer})


@role_required(allowed_roles=['admin'])
def delete_officer(request, officer_id):
    officer = AgricultureOfficer.objects.get(id=officer_id)
    officer.user.delete()
    officer.delete()
    return redirect('/adminpanel/officers/')
