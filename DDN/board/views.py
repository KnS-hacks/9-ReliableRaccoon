from django.shortcuts import render,redirect, get_object_or_404
from django.utils import timezone  #글 작성시간을 자동으로 가져오는 용도
from .models import board_model #게시글 DB

def boardlist(request) : #날짜별로 분류
    selected = board_model.objects.filter(write_day__range=["2021-11-14", "2021-11-15"])
    print(selected)
    return render(request, "boardlist.html")

def boardview(request) : #일기 보기
    return render(request, "boardview.html")

def boardwrite(request) : #일기 작성
    if request.method == "POST":
        result = request.POST
        new_writer = board_model.objects.create(title = result['title'])    
        new_writer.title = request.POST['title']
        new_writer.author = "든든너구리"
        new_writer.weather= request.POST['weather']
        user_pick = request.POST['emotion']
        if(user_pick != "자동"):
            new_writer.auto_pick = False
        else :
            new_writer.auto_pick = True
        new_writer.result_emotion = user_pick
        new_writer.body = request.POST['body']
        if request.FILES :
            new_writer.image = request.FILES['image']
        new_writer.views = 0
        new_writer.write_day = timezone.now()
        print(new_writer.write_day.day)
        new_writer.modify_day = timezone.now()
        new_writer.save()
        return redirect('boardlist')    
    return render(request,"boardwrite.html")


# def update(request):
#     new_writer = board_model.objects.get(pk=request.POST['num'])
#     new_writer.title = request.POST['title']
#     new_writer.author = request.POST['author']
#     new_writer.weather = request.POST['weather']
#     new_writer.api_emotion = request.POST['api_emotion']
#     new_writer.result_emotion = request.POST['result_emotion']
#     new_writer.lauto_pick = request.POST['auto_pick']
#     new_writer.body = request.POST['body']

#     if request.FILES :
#         new_writer.image = request.FILES['image']
        
#     new_writer.modify_day = timezone.now()
#     new_writer.save()
#     #return redirect('/detail'+'/?num='+request.POST['num'])