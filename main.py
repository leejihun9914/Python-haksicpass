import numpy as np
import face_recognition
import pyrebase
import os

config = {
    "apiKey": "AIzaSyBlbH0Evbsw72oKTT_pMeU9sEe935755mM",
    "authDomain": "hasicpassandroid.firebaseapp.com",
    "databaseURL": "https://hasicpassandroid.firebaseio.com/",
    "projectId": "hasicpassandroid",
    "storageBucket": "hasicpassandroid.appspot.com",
    "messagingSenderId": "639723373505",
    "appId": "1:639723373505:web:d5ebb7f076a095d586a540"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# db에서 users 정보 받아오기


# 각각 db전체, 키값(UID), value값


def checkrequest():
    check = list((db.child('requests').get()).val().values())
    if check[0] == 'true':
        print('검사요청 확인!')
        db.child('requests').update({'checked': 'false'})
        db.child('results').update({'checked': 'false'})

        print('image downloading...')
        storage.child('faces/face.jpg').download('check/face.jpg')
        # 여기에서 에러남
        imgdownload()

        print('success!')

        print('checked image...')

        imgencoding()

        facecheck()
        print(known_face_names)
        print(tkey)

        print('check success!')
        db.child('results').update({'end': 'true'})
        # deleteimg()

    # elif check[0] == 'false':
    #     print('요청받은값이 없습니다.')


# 이미지 다운로드
def imgdownload():
    for i in range(len(key)):
        # 여기수정@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        storage.child('uploads/'+od[tkey[i]]['학번']+'_face').download('uploads/'+od[tkey[i]]['학번']+'_face.jpg')


# 저장된 얼굴과 이름을 배열에 저장
# 이미지를 불러와서 인코딩하기
known_face_encodings = []
known_face_names = []
encodingList = []
# 이미지변수이름 = face_recognition.load_image_file("이미지패스")
# 인코딩변수이름 = face_recognition.face_encodings(이미지변수이름)[0]
def imgencoding():
    known_face_names.clear()
    known_face_encodings.clear()
    encodingList.clear()
    for i in range(len(key)):
        student = od[tkey[i]]['학번']
        encodingList.append(tkey[i] + "_encoding")
        known_face_names.append(tkey[i])
        key[i] = face_recognition.load_image_file('uploads/' + student + '_face.jpg')
        encodingList[i] = face_recognition.face_encodings(key[i])[0]
        known_face_encodings.append(encodingList[i])


def facecheck():
    # 비교대상 이미지 인코딩
    test_image = face_recognition.load_image_file('check/face.jpg')
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # 등록된 얼굴과 가장 매치되는 얼굴 찾기
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        min_value = min(distances)

        # tolerance : 어느정도로 인식이 될지를 정하는 수치
        # 0.6이 가장 인식이 잘되는 값
        name = "Unknown"
        db.child('results').update({'checked': 'false'})

        if min_value < 0.4:
            index = np.argmin(distances)
            name = known_face_names[index]
            print('신원확인')
            db.child("results").update({"checked": "true"})
            db.child('results').update({'이메일': od[name]['이메일']})
            db.child('results').update({'비밀번호': od[name]['비밀번호']})
        face_names.append(name)


def deleteimg():
    for i in range(len(key)):
        file = './uploads/' + od[tkey[i]]['학번'] + '_face.jpg'
        if os.path.isfile(file):
            os.remove(file)

while True:
    test = db.child('users').get()
    od = test.val()
    key = list(test.val().keys())
    tkey = tuple(test.val().keys())
    sep = (test.val().values())
    checkrequest()

