# 펌스탯 데이터 알고리즘 모음

자켓 다운로드 API

서열표 난이도 추출 알고리즘

난이도 추출 정렬 알고리즘

그레이스케일 이미지


# requirements

먼저 최신 버전의 파이썬을 다운로드 받으시기 바랍니다. 또한 해당 소스코드를 다운받아 압축을 풀어주세요

https://www.python.org/

터미널을 켠뒤
```bash
cd 다운한경로
python -m venv venv
source venv/bin/activate (맥/리눅스) or source venv/Scripts/activate (윈도우)
pip install -r requirements.txt
```
를 입력하여 가상환경을 설치합니다.

# 자켓 다운로드 API

```
python download_images.py
```

id_title.png 포맷으로 저장됩니다.

저작권은 안다미로에 있음을 주의하셔야 합니다.

# 서열표 난이도 추출 알고리즘

levels 폴더에 원하는 서열표 이미지를 넣어줍니다.

또한 difficulty_positions.py 파일을 열어

```py
    'levels/서열표S15.png': {
        '최상': (324, 463),
        '상': (463, 699),
        '중상': (699, 919),
        '중': (919, 1370),
        '중하': (1370, 1804),
        '하': (1804, 2057),
        '종특': (2057, 2224)
    },
```
```py
    '경로': {
        '난이도1': (y축 시작, y축 끝), 
        '난이도2': (y1, y2), ...
    }
```
포맷으로 적어줍니다.
 
```
python imagesearch_sift.py
```

# 난이도 추출 정렬 알고리즘

```
python sort_text.py
```
위 imagesearch_sift.py 를 통해 얻은 난이도 텍스트 파일을 정렬해줍니다. 정렬 전 백업 권장
