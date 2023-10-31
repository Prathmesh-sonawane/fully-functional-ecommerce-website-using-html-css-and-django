from django.shortcuts import render, HttpResponse
from .models import Product, Order, Contact, admin
import requests
from itertools import chain
import smtplib

# Create your views here.
def home(request):
    catprods = Product.objects.values()
    
    if catprods:
        last_product = catprods.last()
        idd = last_product['id']
    else:
        idd = None  # or handle it as appropriate in your context
    
    newprod = Product.objects.filter(id=idd)
    allprod = Product.objects.values()
    webprod = Product.objects.filter(Cateogary="earbuds")
    params = {'newprod': newprod, 'allprod': allprod, 'gui': webprod, 'clas': 'active'}
    return render(request, 'index.html', params)


def about(request):
    params = {'abou': 'active'}
    return render(request, 'about.html',params)

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def contact(request, methods = ['GET', 'POST']):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        contact = Contact(fname=fname, lname=lname, subject=subject, message=message, email=email)
        contact.save()
        sender_add = 'help.bits.it@gmail.com'
        password = 'hppc gtmq exyw mjxh'
        reciever_add = email
        server = smtplib.SMTP('smtp.gmail.com:587')
        subb = f'{fname} Thank you for your feedback'
        mailBody = f"support team from Bits.it\n\nHello {fname} {lname}\n\n, Thank you for taking the time to share your feedback with us. \n\n We appreciate you taking the time to let us know about your experience with us.Sharing the Details with You but with a Request to not to share your Customers Data . \n\nWe are taking your feedback seriously and will be working on making improvements. We are committed to providing the best possible products and services to our customers, and your feedback will help us achieve that goal."
        mailBody += f'\n\n Name : {fname} {lname}\nSubject for Contacting : {subject}\nEmail : {email}\nMessage : {message}\n\nWe would work to solve the issue at the earliest. In the meanwhile if there is anyting we could help you with;\nPlease let us know.Thank you again for your feedback,\n we hope you continue to enjoy shopping with us.\n\Sincerely\n (bits.it Community)'
        msg1 = f"""Subject : {subb}\n\n{mailBody}"""
        server.starttls()
        server.login(sender_add, password)
        server.sendmail(sender_add, reciever_add, msg1)
        string = f'Thank You Your Message has been sucessfully Sent to the {admin}'
        params = {'string': string, 'cont': 'active'}
        return render(request, 'contact.html', params)
    params2 = {'cont': 'active'}
    return render(request, 'contact.html', params2)

def shop(request, methods=['GET', 'POST']):
    if request.method == 'POST':
        allProds = []
        catProds = Product.objects.values()
        params = {'allprods': catProds}
        return render(request, 'shop.html', params)
    lengthofConsole = Product.objects.filter(Cateogary = "headphone")
    lengthofWeb = Product.objects.filter(Cateogary = "earbuds")
    lengthofDesktop = Product.objects.filter(Cateogary = "soundbar")
    catProds = Product.objects.values()
    params = {'allprods': catProds, 'shop': 'active', 'console': len(lengthofConsole), 'web': len(lengthofWeb), 'desktop': len(lengthofDesktop)}
    return render(request, 'shop.html', params)

def thankyou(request, methods = ['GET', 'POST']):
    allprods = Product.objects.values()
    if request.method == 'POST':
        country = request.POST.get('countryinput')
        itemsJson = request.POST.get('itemsJson')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        state = request.POST.get('state')
        zipcode = request.POST.get('zip')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        link = {}
        name = {}
        space = 0
        mailBody=f'Hey {fname},\n\nYour Order has Been Place\n\n'
        try:
            for i in range(0, len(allprods)):
                space = space + 3
                if allprods[i]["Product_Name"] == str(itemsJson).split('"')[space]:
                    name.update( {f'product{i}': allprods[i]["Product_Name"] } )
                    j = i + 1
                    mailBody += f'{j}. {allprods[i]["Product_Name"]}:  \n\n'
                    space = space + 3
        except IndexError as e:
            pass
        link2 = {'item': link, 'name': name}
        order = Order(itemsJson=itemsJson, firstName=fname, lastName=lname, email=email, address=address,
                       state=state, zipcode=zipcode, phone=phone, amount=amount, country=country)
        order.save()
        sender_add = 'help.bits.it@gmail.com'
        password = 'hppc gtmq exyw mjxh'
        reciever_add = email
        server = smtplib.SMTP('smtp.gmail.com:587')
        subb = f'{fname} Your order has been placed !!!'
        mailBody += f"Hey {fname}, \nWe have recieved your order and it would be delivered to your address soon.\n\nThank you for shopping with us,\n We hope to see you again with another order !!\n\nBITS IT Community,\n\nFor more Updates, Offers and deals stay connected with us."

        msg1 = f"""Subject: {subb}\n\n{mailBody}""".encode('utf-8')
        server.starttls()
        server.login(sender_add, password)
        server.sendmail(sender_add, reciever_add, msg1)
        return render(request, 'thankyou.html', link2)

def view(request, Product_Name, ID_of_the_Product):
    allProds = []
    idprod = int(ID_of_the_Product)
    catProds = Product.objects.filter(id=idprod)
    allProds = Product.objects.values()
    params = {'allprods': allProds, 'catprods': catProds}
    return render(request, 'shop-single.html', params)

def web(request):
    head = "headphone"
    Prods = Product.objects.filter(Cateogary = "headphone")
    allprods = Product.objects.values()
    lengthofConsole = Product.objects.filter(Cateogary = "earbuds")
    lengthofWeb = Product.objects.filter(Cateogary = "headphone")
    lengthofDesktop = Product.objects.filter(Cateogary = "soundbar")
    prods = {'head': head, 'style': 'active', 'prod': Prods, 'allprods': allprods, 'web': len(lengthofWeb), 'desktop': len(lengthofDesktop), 'console': len(lengthofConsole)}
    return render(request, 'DiffrentiatedPoducts.html', prods)

def desktop(request):
    head = "earbuds"
    Prods = Product.objects.filter(Cateogary = "earbuds")
    allprods = Product.objects.values()
    lengthofConsole = Product.objects.filter(Cateogary = "soundbar")
    lengthofWeb = Product.objects.filter(Cateogary = "headphone")
    lengthofDesktop = Product.objects.filter(Cateogary = "earbuds")
    prods = {'head': head, 'style': 'active', 'prod': Prods, 'allprods': allprods, 'web': len(lengthofWeb), 'desktop': len(lengthofDesktop), 'console': len(lengthofConsole)}
    return render(request, 'DiffrentiatedPoducts.html', prods)

def console(request):
    head = "soundbar"
    Prods = Product.objects.filter(Cateogary = "soundbar")
    allprods = Product.objects.values()
    lengthofConsole = Product.objects.filter(Cateogary = "earbuds")
    lengthofWeb = Product.objects.filter(Cateogary = "headphone")
    lengthofDesktop = Product.objects.filter(Cateogary = "soundbar")
    prods = {'head': head, 'style': 'active', 'prod': Prods, 'allprods': allprods, 'web': len(lengthofWeb), 'desktop': len(lengthofDesktop), 'console': len(lengthofConsole)}
    return render(request, 'DiffrentiatedPoducts.html', prods)

def frontend(request):
    params = {'style': 'active'}
    return render(request, 'currentlyInBuild.html', params)

def backend(request):
    params = {'style': 'active'}
    return render(request, 'currentlyInBuild.html', params)

def search(request, keyword):
    catprods = Product.objects.filter(Cateogary = keyword)
    allprods = Product.objects.values()
    params = {'allprods': allprods, 'catprods': catprods, 'cat': keyword}
    return render(request, 'search.html', params)

def sub(request, email):
    response = requests.post('convominds.com', data = {'name' : email})
