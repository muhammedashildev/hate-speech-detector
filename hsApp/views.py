from django import views
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from PIL import Image
from django.db.models import Count
# Create your views here.


def index(request):
    return render(request, "index.html")


def login(request):
    if request.method == "POST":
        email = request.POST['name']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        if user is not None:
            request.session['email'] = email
            if user.is_active:
                if user.is_superuser:
                    return redirect("/adminHome")
                else:
                    sf = Users.objects.get(email=email)
                    request.session['id'] = sf.id
                    return redirect("/sfHome")
            else:
                msg = "Account is not Active..."
                return render(request, "login.html", {"msg": msg})
        else:
            msg1 = "User Dosent Exists..."
            return render(request, "login.html", {"msg": msg1})
    else:
        return render(request, "login.html")
    
def logout(request):
    request.session.flush()
    return redirect("/login")


def sfReg(request):
    flag = 0
    msg = ""
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        img = request.FILES.get('file', None)
        if img:
            try:
                # Attempt to open the uploaded file as an image
                image = Image.open(img)
                image.verify()  # Verify that it is, indeed, an image
            except (IOError, FileNotFoundError):
                msg = "Invalid File.Upload correct image file"
                return render(request, "sfReg.html", {"msg": msg})


        if User.objects.filter(username=email).exists():
            msg = "Email already exists..."

        else:
            user = User.objects.create_user(
                username=email, password=password, is_active=1)
            user.save()
            sf = Users.objects.create(
                name=name, email=email, phone=phone, address=address, document=img, user=user)
            sf.save()
            msg = "Registration Successful..."
            flag = 1

    return render(request, "sfReg.html", {"msg": msg, "flag": flag})


def adminHome(request):
    if 'email' in request.session:
     request.session['email']
     return render(request, "adminHome.html")
    else:
       return redirect("/login")


def adminStartUp(request):
    if 'email' in request.session:
     request.session['email']
     data = Users.objects.filter(user__is_active=0)
     dataActive = Users.objects.filter(user__is_active=1)
     return render(request, "adminStartup.html", {"data": data, "dataActive": dataActive})
    else:
       return redirect("/login")


def approveStartUp(request):
     id = request.GET['id']
     status = request.GET['status']
     sf = User.objects.get(id=id)
     sf.is_active = status
     sf.save()
     return redirect("/adminStartUp")
    


def adminViewFeedback(request):
    if 'email' in request.session:
     request.session['email']

     data = Feedback.objects.all()
     return render(request, "adminViewFeedback.html", {"data": data})
    else:
       return redirect("/login")


def adminViewDetections(request):
    if 'email' in request.session:
     request.session['email']
     data = Detection.objects.all().order_by("id")
     return render(request, "adminViewDetections.html", {"data": data })
    else:
       return redirect("/login")


def sfHome(request):
    if 'id' in request.session:
     id = request.session['id']

     data = Users.objects.get(id=id)
     post = Post.objects.exclude(user=id)
     if request.method == "POST":
        search = request.POST['search']
        post = Post.objects.filter(idea__contains=search).exclude(user=id)
     return render(request, "sfHome.html", {"data": data, "post": post})
    else:
        return redirect("/login")
 


def sfProfile(request):
    if 'id' in request.session:
     id = request.session['id']

     data = Users.objects.get(id=id)
     if request.method == "POST":
         name = request.POST['name']
         email = request.POST['email']
         phone = request.POST['phone']
         address = request.POST['address']
         password = request.POST['password']
         proUp = Users.objects.get(id=id)
         proUp.name = name
         proUp.email = email
         proUp.phone = phone
         proUp.address = address
         proUp.save()
         logUp = User.objects.get(username=data.user)
         logUp.set_password(password)
         logUp.username = email
         logUp.save()
         return redirect("/sfHome")
     return render(request, "sfProfile.html", {"data": data})
    else:
        return redirect("/login")



def sfChangeImage(request):
    if 'id' in request.session:
     id = request.session['id']
     data = Users.objects.get(id=id)
     if request.method == "POST":
        img = request.FILES["file"]

        data.document = img
        data.save()
        return redirect("/sfHome")
     return render(request, "sfChangeImage.html", {"data": data})
    else:
        return redirect("/login")
    


def sfPost(request):
    if 'id' in request.session:
     id = request.session['id']
     user = Users.objects.get(id=id)
     msg = ''
     if request.method == "POST":
        idea = request.POST['idea']
        description = request.POST['description']
        image = request.FILES.get('image', None)
        if image:
            try:
                # Attempt to open the uploaded file as an image
                img = Image.open(image)
                img.verify()  # Verify that it is, indeed, an image
            except (IOError, FileNotFoundError):
                msg = "Invalid File.Upload correct image file"
                return render(request, "sfPost.htmls", {"msg": msg})        
        flag = 'SAFE'

        from bad_word_detector import main as check
        import nltk
        nltk.download('vader_lexicon')
        from nltk.sentiment.vader import SentimentIntensityAnalyzer

        resultTitle = check(idea)
        resultDesc = check(description)
        print(resultDesc, resultTitle)
        if resultDesc == 'Good' and resultTitle == 'Good' and flag == 'SAFE':
            db = Post.objects.create(idea=idea, desc=description, user=user,image=image)
            msg = "Post Created Successfully"
            db.save()
        else:
            sid = SentimentIntensityAnalyzer()
            scores1 = sid.polarity_scores(idea)
            scores2 = sid.polarity_scores(description)
            print(scores1['compound'], scores2['compound'])
            if scores1['compound'] < 0 or scores2['compound'] < 0:
                det = Detection.objects.create(
                    user=user, title=idea, desc=description,image=image)
                det.save()
                msg = "Offensive language used. Cant post the content"
            else:
                db = Post.objects.create(idea=idea, desc=description, user=user,image=image)
                msg = "Offensive language detected"
                db.save()

     return render(request, "sfPost.html", {"msg": msg})
    else:
        return redirect("/login")
    

def sfViewSelfPost(request):
    if 'id' in request.session:
     id = request.session['id']

     data = Post.objects.filter(user=id)
     return render(request, "sfViewSelfPost.html", {"data": data})
    else:
        return redirect("/login")


def sfUpdateIdea(request):
    id = request.GET['id']
    data = Post.objects.get(id=id)
    if request.method == "POST":
        idea = request.POST['idea']
        description = request.POST['description']
        data.idea = idea
        data.desc = description
        data.save()
        return redirect("/sfViewSelfPost")
    return render(request, "sfUpdateIdea.html", {"data": data})


def sfDeleteIdea(request):
    id = request.GET['id']
    data = Post.objects.get(id=id)
    data.delete()

    return redirect("/sfViewSelfPost")


def sfViewIdea(request):
    if 'id' in request.session:
     id = request.GET['post']
     sfid = request.session['id']

     data = Post.objects.get(id=id)
     if request.method == "POST":
        comment = request.POST['comment']

        user = Users.objects.get(id=sfid)
        db = Comments.objects.create(comment=comment, idea=data, user=user)
        db.save()

     comments = Comments.objects.filter(idea=id)
     return render(request, "sfViewIdea.html", {"data": data, "comments": comments})
    else:
        return redirect("/login")


def sfViewSf(request):
    id = request.GET['sfid']
    user = Users.objects.get(id=id)

    post = Post.objects.filter(user=id)
    return render(request, "sfViewSf.html", {"user": user, "post": post})


def sfAddFeedBack(request):
    if 'id' in request.session:
     id = request.session['id']
     if request.method == "POST":
        feedback = request.POST['feedback']
        user = Users.objects.get(id=id)

        db = Feedback.objects.create(feedback=feedback, user=user)
        db.save()
     data = Feedback.objects.filter(user=id)
     return render(request, "sfAddFeedBack.html", {"data": data})
    else:
        return redirect("/login")


def sfChat(request):
    if 'email' in request.session:
     sender = request.session["email"]
     data = Chat.objects.filter(
        Q(sender=sender) | Q(receiver=sender)).distinct()
     print(data)
     newData = set()
     for d in data:
        newData.add(d.sender)
        newData.add(d.receiver)
     return render(request, "sfChat.html", {"data": newData, "user": sender})
    else:
        return redirect("/login")
    


def sfChatPer(request):
    if 'email' in request.session:
     sender = request.session['email']
     receiver = request.GET['email']
     data = Users.objects.all()
     if request.method == "POST":
        msg = request.POST['msg']
        db = Chat.objects.create(sender=sender, receiver=receiver, message=msg)
        db.save()
     messages = Chat.objects.filter(
        Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))
     return render(request, "sfChatPer.html", {"data":data, "receiver":receiver, "messages": messages, "user": sender})
    else:
        return redirect("/login")
