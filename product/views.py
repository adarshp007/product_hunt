import datetime
from django.utils import  timezone
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . models import Product
# Create your views here.
def home(request):
    return render(request, 'products/home.html')
@login_required
def create(request):
    if request.method=="POST":
        product=Product()
        product.title=request.POST['title']
        product.body=request.POST['body']
        if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
            product.url=request.POST['url']
        else:
            product.url='http://' + request.POST['url']
        img=request.FILES['image']
        icon=request.FILES['icon']
        fs=FileSystemStorage()
        nam=datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        imgname=nam+".jpg"
        iconname=nam+".png"
        fs.save(iconname,icon)
        fs.save(imgname,img)
        imgurl='/media/photos/'+imgname
        iconurl='/media/photos/'+iconname
        product.icons=iconurl
        product.image=imgurl
        product.pub_date=timezone.datetime.now()
        product.hunter=request.user
        product.save()
        pr=Product.objects.all()
        print(len(pr))
        return render(request,'products/home.html',{'bb':pr})
    else:
        return render(request,'products/create.html')