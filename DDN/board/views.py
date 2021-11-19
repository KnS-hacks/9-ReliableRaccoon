from django.shortcuts import render,redirect, get_object_or_404
from django.utils import timezone  #글 작성시간을 자동으로 가져오는 용도
from .models import board_model #게시글 DB
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import random
# pip install azure-ai-textanalytics==5.1.0 
# azure 설치

SECRET_KEY = 'ed2ec6a21ae24e4cb1559d22a6c8142c'
END_POINT = 'https://hyun0310.cognitiveservices.azure.com/'

def boardlist(request) : #날짜별로 분류
    date = request.GET.get('date') #2021-11-15
    selected = board_model.objects.filter(write_day__range=[date, date])
    return render(request, "boardlist.html", {'selected':selected, 'date':date})


def boardview(request, num) : #일기 보기
    # num = request.GET.get('num')
    selected = board_model.objects.get(id=num) # pk 는 primaty key (num)
    context = {'selected': selected}
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


def date_selecter_temp(request) : #날짜 선택 (임시확인)
    recent_board = board_model.objects.order_by('-pk')
    if len(recent_board) > 2 and suggest_board(recent_board[0].id) ==3:
        high_emotion_board = list(board_model.objects.filter(result_emotion='행복'))
        random_num = random.randrange(0,len(high_emotion_board))
        return render(request, "date_selecter_temp.html", {'high_emotion_board':high_emotion_board[random_num].id})
    return render(request, "date_selecter_temp.html")


def boardwrite(request) : #일기 작성
    if request.method == "POST":
        result = request.POST
        new_writer = board_model.objects.create(title = result['title'])    
        new_writer.title = request.POST['title']
        new_writer.author = "든든너구리"
        new_writer.weather= request.POST['weather']
        user_pick = request.POST['emotion']
        new_writer.body = request.POST['body']
        if(user_pick != "자동"):
            new_writer.auto_pick = False
            new_writer.result_emotion = user_pick
        else :
            new_writer.auto_pick = True
            sentences=new_writer.body.split('.')
            new_writer.api_emotion_score = analyze_text(sentences, new_writer.id)
            new_writer.api_emotion = api_to_result(new_writer.api_emotion_score)
            new_writer.result_emotion = api_to_result(new_writer.api_emotion_score)
        if request.FILES :
            new_writer.image = request.FILES['image']
        new_writer.views = 0
        new_writer.write_day = timezone.now()
        print(new_writer.write_day.day)
        new_writer.modify_day = timezone.now()
        new_writer.save()
        return redirect('date_selecter_temp')    
    return render(request,"boardwrite.html")

def boardrewrite(request, board_id) : #일기 수정
    re_writer = board_model.objects.get(id = board_id)    
    if request.method == "POST":        
        re_writer.title = request.POST['title']
        re_writer.author = "든든너구리"
        re_writer.weather= request.POST['weather']
        user_pick = request.POST['emotion']
        re_writer.body = request.POST['body']
        if(user_pick != "자동"):
            re_writer.auto_pick = False
            re_writer.result_emotion = user_pick
        else :
            re_writer.auto_pick = True
            sentences=re_writer.body.split('.')
            re_writer.api_emotion_score=analyze_text(sentences, re_writer.id)
            re_writer.api_emotion =api_to_result(re_writer.api_emotion_score)
            re_writer.result_emotion =api_to_result(re_writer.api_emotion_score)
        if request.FILES :
            re_writer.image = request.FILES['image']
        re_writer.views = 0
        re_writer.write_day = timezone.now()
        print(re_writer.write_day.day)
        re_writer.modify_day = timezone.now()
        re_writer.save()
        return redirect('date_selecter_temp')    
    return render(request,"boardrewrite.html")

def boardDelete(request, board_id):
    content = board_model.objects.get(id = board_id)    
    content.delete()
    return redirect('date_selecter_temp')


def analyze_text(documents, board_id):
    endpoint = END_POINT
    key = SECRET_KEY
    del documents[len(documents)-1]
    text_analytics_client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))
    results = text_analytics_client.analyze_sentiment(documents, language='ko')
    total_emotion_positive =0
    total_emotion_negative =0
    total_emotion_neutral =0
    last_emotion =0
    now_emotion =0
    for index,result in enumerate(results):
        print(documents[index])
        if result=='':
            break
        else:
            print('positive :',result.confidence_scores.positive)
            print('negative :',result.confidence_scores.negative)
            print('neutral :',result.confidence_scores.neutral)
            #이전 문장 감정 판별, 긍정적이면 1 부정적이면 -1 모호하면 0
            if results[index-1].confidence_scores.positive > results[index-1].confidence_scores.negative and results[index-1].confidence_scores.positive > results[index-1].confidence_scores.neutral:
                last_emotion = 1
            elif results[index-1].confidence_scores.negative > results[index-1].confidence_scores.neutral: 
                last_emotion = -1
            else:
                last_emotion = 0
            #현재 문장 감정 판별, 긍정적이면 1 부정적이면 -1 모호하면 0
            if results[index].confidence_scores.positive > results[index].confidence_scores.negative and results[index].confidence_scores.positive > results[index].confidence_scores.neutral:
                now_emotion = 1
            elif results[index].confidence_scores.negative > results[index].confidence_scores.neutral: 
                now_emotion = -1
            else:
                now_emotion = 0
            # 현재의 문장이 긍정적이고 이전이 부정적이면 긍정적 점수 X 1.3
            if now_emotion > last_emotion:
                total_emotion_positive +=(result.confidence_scores.positive*1.3)
                total_emotion_negative+=result.confidence_scores.negative
                total_emotion_neutral +=result.confidence_scores.neutral
            # 현재의 문장이 부정적이고 이전이 긍정적이면 부정적 점수 X 1.3
            elif now_emotion < last_emotion:
                total_emotion_positive +=result.confidence_scores.positive
                total_emotion_negative+=(result.confidence_scores.negative*1.3)
                total_emotion_neutral +=result.confidence_scores.neutral
            # 서로 같으면 그대로 더해줌
            else:
                total_emotion_positive +=result.confidence_scores.positive
                total_emotion_negative+=result.confidence_scores.negative
                total_emotion_neutral +=result.confidence_scores.neutral


    total_emotion_positive = total_emotion_positive/len(results)
    total_emotion_negative = total_emotion_negative/len(results)
    total_emotion_neutral = total_emotion_neutral/len(results)

    total_emotion = (-total_emotion_negative if total_emotion_negative>total_emotion_positive or total_emotion_negative==total_emotion_positive else total_emotion_positive)
    # print(total_emotion)
    
    # 오늘의 감정 분석 결과 도출
    if total_emotion > total_emotion_neutral or total_emotion == total_emotion_neutral:
        total_emotion = total_emotion/(total_emotion_negative+(total_emotion_neutral//5)+total_emotion_positive)
    else :
        total_emotion = total_emotion/(total_emotion_negative+total_emotion_positive)
    # print(total_emotion,'종합')
    print(total_emotion)
    return total_emotion
    
def api_to_result(total_emotion):
    # 오늘의 감정 분석 결과를 DB에 저장
    if total_emotion >0:
        total_emotion = '행복'
    elif total_emotion <0:
        total_emotion = '우울'
    else:
        total_emotion = '쏘쏘'
    return total_emotion

def suggest_board(board_id):
    depress_count=0
    for index in range(board_id-2, board_id+1):
        today = board_model.objects.get(id = index)
        try: 
            if float(today.api_emotion_score) < 0 :
                depress_count+=1
        except TypeError:
            if today.result_emotion =='우울':
                depress_count+=1
    return depress_count

