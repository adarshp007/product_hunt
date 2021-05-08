import datetime
from django.utils import  timezone
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Product
# Create your views here.
def home(request):
    product=Product.objects.all()
    return render(request, 'products/home.html',{'prod':product})
@login_required(login_url="/account/signup/")
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

        return redirect('/product/'+str(product.id))
    else:
        return render(request,'products/create.html')
def detail(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    return render(request,'products/detail.html',{'prod':product})
@login_required(login_url="/account/signup/")
def upvote(request,product_id):
    if request.method=="POST":
        product=get_object_or_404(Product,pk=product_id)
        product.votes += 1
        product.save()
        return redirect('/product/'+str(product.id))