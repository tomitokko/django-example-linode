from hashlib import new
from construct import If
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
import requests
from .models import Order, ProjectList, Alert
import json
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='/login')
def dashboard(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(current_user=request.user.username, finished='False')
        project_list = ProjectList.objects.all()
        print(project_list)
        return render(request, 'dashboard.html', {'orders': orders, 'project_list':project_list})
    else:
        return redirect('/')

@login_required(login_url='/login')
def history(request):
    finished_orders = Order.objects.filter(current_user=request.user.username, finished='True')
    return render(request, 'history.html', {'finished_orders': finished_orders})

@login_required(login_url='/login')
def new_order(request):
    project_name = request.POST['project_name']
    discord_link = request.POST['discord_link']
    amount_of_invites = request.POST['amount_of_invites']
    verification_message = request.POST['verification_message']
    current_user = request.user.username

    new_order = Order.objects.create(project_name=project_name, discord_link=discord_link, amount_of_invites=amount_of_invites, verification_message=verification_message, current_user=current_user)
    new_order.save()

    return redirect('dashboard')


@login_required(login_url='/login')
def project_form(request):
    return render(request, 'project-form.html')

@login_required(login_url='/login')
def project_notification(request):
    if request.method == "POST":
        
        def get_project_details(symbol):
            import requests

            symbol = symbol

            url = "http://api-mainnet.magiceden.dev/v2/collections/{symbol}/stats".format(symbol=symbol.lower().replace(" ", "_"))

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            json_data = json.loads(response.text)
            return json_data

        magiceden_name = request.POST['magiceden_name']
        project_details = get_project_details(magiceden_name)

        def get_project_image(symbol):

            symbol = symbol

            url = 'https://magiceden.io/marketplace/{symbol}'.format(symbol=symbol.lower().replace(" ", "_"))
            res = requests.get(url)

            soup = BeautifulSoup(res.content)
            image = soup.find('meta', {'property': 'og:image'})['content']
            image_link = image.split('https')[2]
            
            return image_link

        project_image = get_project_image(magiceden_name)

        context = {
            'project_name' : project_details.get('symbol'),
            'floorPrice' : int(project_details.get('floorPrice'))/1000000000,
            'listedCount' : project_details.get('listedCount'),
            'avgPrice24hr' : int(project_details.get('avgPrice24hr'))//1000000000,
            'volumeAll' : int(project_details.get('volumeAll'))/1000000000,
            'image_link' : project_image,
        }
        
        return render(request, 'project-notification.html', context)
    else:
        return HttpResponse("<h1>Invalid Request</h1>")

@login_required(login_url='/login')
def alert_success(request):
    if request.method == 'POST':
        above_or_below = request.POST['above_or_below']
        price = request.POST['price']
        email = request.POST['email']
        current_user = request.user.username
        project_name = request.POST['project_name']
        project_image = request.POST['project_image']

        new_alert = Alert.objects.create(above_or_below=above_or_below, price=price, email=email, current_user=current_user, project_name=project_name, project_image=project_image)
        new_alert.save()
        return redirect('current-alerts')
    else:
        return HttpResponse("<h1>Invalid Request</h1>")

@login_required(login_url='/login')
def current_alerts(request):
    current_user = request.user.username
    alerts = Alert.objects.filter(current_user=current_user)
    return render(request, 'current-alerts.html', {'alerts': alerts})

@login_required(login_url='/login')
def delete_alert(request):
    alert_id = request.GET.get('alert_id')
    alert = Alert.objects.get(id=alert_id)
    if alert.current_user == request.user.username:
        alert.delete()
    return redirect('current-alerts')

def send_alert(request):


    def get_project_details(symbol):
        import requests

        symbol = symbol

        url = "http://api-mainnet.magiceden.dev/v2/collections/{symbol}/stats".format(symbol=symbol.lower().replace(" ", "_"))

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        json_data = json.loads(response.text)
        return json_data


    for alert in Alert.objects.all():
        project_details = get_project_details(alert.project_name)
        if alert.above_or_below == 'above':
            if int(project_details.get('floorPrice'))/1000000000 > int(alert.price):
                send_mail(
                    'Floor Price Alert For ' + alert.project_name,
                    'The floor price of ' + alert.project_name + ' is now above ' + str(alert.price) + '.',
                    'accessnft09@gmail.com',
                    [alert.email],
                    fail_silently=False)
        elif alert.above_or_below == 'below':
            if int(project_details.get('floorPrice'))/1000000000 < int(alert.price):
                send_mail(
                    'Floor Price Alert For ' + alert.project_name,
                    'The floor price of ' + alert.project_name + ' is now below ' + str(alert.price) + '.',
                    'accessnft09@gmail.com',
                    [alert.email],
                    fail_silently=False)
    return HttpResponse("<h1>Alerts Sent</h1>")

# def test_alert(request):
#     send_mail(
#                     'Floor Price Alert For trippin_ape_tribe',
#                     'The floor price of trippin_ape_tribe is now below 45.0 SOL.',
#                     'accessnft09@gmail.com',
#                     ['jopiv51952@nifect.com'],
#                     fail_silently=False)

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/#login')

    else:
        return redirect('/#login')

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect('/')