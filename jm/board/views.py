from django.shortcuts import render,redirect, get_object_or_404
from django.utils import timezone  #글 작성시간을 자동으로 가져오는 용도
from .models import board_model #게시글 DB

def date_selecter_temp(request) : #날짜 선택 (임시확인) 
    All_model = board_model.objects.all()
    date_list = []
    for tmp in All_model :
        string = str(tmp.write_day.year) + "-" + str(tmp.write_day.month) + "-" + str(tmp.write_day.day)
        if(string in date_list) :
            continue
        else :
            date_list.append(string)
    print(date_list)
    return render(request, "date_selecter_temp.html", {'date_list':date_list})



def boardlist(request) : #날짜별로 분류
    date = request.GET.get('date') #2021-11-15
    selected = board_model.objects.filter(write_day__range=[date, date])
    return render(request, "boardlist.html", {'selected':selected, 'date':date})



def boardview(request) : #일기 보기
    num = request.GET.get('num')
    selected = board_model.objects.get(id=num) # pk 는 primaty key (num)

    weather = ""
    if selected.weather == "맑음" :
        weather = "🌞"
    elif selected.weather == "흐림" :
        weather = "🌤️"
    elif selected.weather == "비" :
        weather = "⛈️"       
    elif selected.weather == "눈" :
        weather = "🌨️"   

    emotion = ""
    if selected.result_emotion == "행복" : 
        emotion = "😀"
    elif selected.result_emotion == "우울" :
        emotion = "😰"
    elif selected.result_emotion == "쏘쏘" :
        emotion = "😐"

    image_url = ""
    if selected.image :
        image_url = selected.image.url
        image_url = image_url[6:]

    return render(request, "boardview.html", {'selected':selected, 'emotion':emotion, 'weather':weather , 'image_url':image_url})

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
        return redirect('date_selecter_temp')    
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