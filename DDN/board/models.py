from django.db import models

# Create your models here.
class board_model(models.Model):
    #file_ ~ : 사진(3~4개)
    image = models.ImageField(blank=True,null=True, upload_to = "board/static/upload")

    title = models.CharField(max_length=100, blank=True,null=True,)

    author = models.CharField(max_length=100, blank=True,null=True,)

    weather = models.CharField(max_length=100,blank=True,null=True,) #날씨

    api_emotion = models.CharField(max_length=100,blank=True,null=True,) #api 원시 감정

    api_emotion_score = models.CharField(max_length=100,blank=True,null=True,) #api 감정 점수

    result_emotion = models.CharField(max_length=100,blank=True,null=True,) #최종 감정

    auto_pick = models.BooleanField(blank=True,null=True,) #감정 자동 판단을 선택했는지 여부

    write_day = models.DateField(blank=True,null=True,)  #작성날짜

    modify_day = models.DateField(blank=True,null=True,)  #수정시간

    views = models.IntegerField(blank=True,null=True,)  #조회수

    body = models.TextField(blank=True,null=True,) #일기 내용