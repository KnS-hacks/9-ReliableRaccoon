import random
import math

def make_emotion(): #30일간 감정을 임의로 정하기
    month = []
    for i in range(30):
        temp = random.randint(1, 5)
        month.append(temp)
    print(month)
    return month


def simple_algorism():
    month = make_emotion()

    happy = month.count(1)
    Lhappy = month.count(2)
    soso = month.count(3)
    Lsad = month.count(4)
    sad = month.count(5)

    string = f"지난 30일간 느끼신 감정은 행복 : {happy}  다소 행복 : {Lhappy}  쏘쏘 : {soso}  다소 우울 : {Lsad}  우울 : {sad} 입니다."
    print(string)

    result = happy*2 + Lhappy*1 + Lsad*-1 + sad*-2
    print('총 평가는 ' + str(result) + ' 입니다.')


def weight_algorism():
    month = make_emotion()
    emotion_value = { 1:2, 2:1, 3:0, 4:-1, 5:-2 }
    default_weight = 1.2 #초기 가중치
    increse_weight = 1.2 #증가 가중치 (복리 연산)
    weight = default_weight #가중치
    DoWeight = False    #가중치를 매길지 정하는 bool
    GoodOrBad = True   #좋고나쁨을 저장하여 좋은 것이 연속되면 가중치 부가 , 좋음(행복, 다소행복), 나쁨(슬픔, 다소 슬픔)
    result = 0

    happy = month.count(1)
    Lhappy = month.count(2)
    soso = month.count(3)
    Lsad = month.count(4)
    sad = month.count(5)

    string = f"지난 30일간 느끼신 감정은 행복 : {happy}  다소 행복 : {Lhappy}  쏘쏘 : {soso}  다소 우울 : {Lsad}  우울 : {sad} 입니다."
    print(string)

    for em in month :
        #맨 처음엔 가중치를 부과하지않고 GoodOrBad를 설정하는데 사용함
        if(em == month[0]):
            if(em < 3) : 
                GoodOrBad = True
                result += emotion_value[em]
            elif(em >3) : 
                GoodOrBad = False
                result += emotion_value[em]
            continue

        #가중치 여부 체크
         #1,2
        if(em < 3) :
            if(GoodOrBad == False):
                DoWeight = False
                GoodOrBad = True
                weight = default_weight
            else :
                DoWeight = True
                weight *= increse_weight
        #4,5
        elif(3 < em) :
            if(GoodOrBad):
                DoWeight = False
                GoodOrBad = False
                weight = default_weight
            else :
                DoWeight = True
                weight *= increse_weight
        #3
        else :
            GoodOrBad = GoodOrBad

        #result 계산
        if(DoWeight): result += emotion_value[em]*weight
        else : result += emotion_value[em]

    result = round(result) // 5  # 몫연산
    print('총 평가는 ' + str(result) + ' 입니다.')
    return result


'''
#100000번 시뮬레이션으로 
sad_count = 0
happy_count = 0
soso_count = 0
for i in range(100000):
    #if(i%10 == 0 and i>0 ):
    #    print("")
    result = weight_algorism()
    if(result < 0) : sad_count += 1
    elif(result > 0) : happy_count += 1
    else : soso_count += 1
print("")

print(happy_count)
print(soso_count)
print(sad_count)
'''

simple_algorism()
weight_algorism()