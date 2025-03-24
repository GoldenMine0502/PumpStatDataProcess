import os
import time
import zipfile
import io
import re
from io import BytesIO

import requests
from PIL import Image


def download_and_verify_image(url, save_path):
    if os.path.exists(save_path):
        print('skip (already exist)', save_path)
        return
    try:
        # URL에서 이미지 다운로드
        response = requests.get(url, verify=False)
        response.raise_for_status()  # HTTP 오류 체크

        # 이미지 검증
        img = Image.open(BytesIO(response.content))  # 이미지 검증 시도
        img.save(save_path)  # 이미지 저장
        print(f"이미지가 성공적으로 저장되었습니다: {save_path}")
        time.sleep(1)
    except Exception as e:
        if os.path.exists(save_path):
            os.remove(save_path)
        print(f"이미지 다운로드 또는 검증 실패: {e}")


def clean_filename(filename):
    name, ext = os.path.splitext(filename)  # 파일명과 확장자 분리
    cleaned_name = re.sub(r"[^가-힣a-zA-Z0-9 ]", "", name)  # 한글, 영어, 숫자만 남기고 제거
    return cleaned_name + ext  # 확장자 유지


def main():
    ROOT_PATH = 'images'
    os.makedirs(ROOT_PATH, exist_ok=False)

    #             "songId": 1,
    #             "stepId": 1,
    #             "title": "익스트림 음악학원 1교시 feat. Nanahira",
    #             "artist": "Massive New Krew & RoughSketch",
    #             "imageUrl": "https://piugame.com/data/song_img/abec5c2e20d275765d72cbe1c98bb4bb.png?v=20241128114126",
    #             "difficulty": "S20"

    data = {'date': '2024-01-01'}
    headers = {
        'Content-Type': 'application/json',
    }
    res = requests.post("https://home.goldenmine.kr/pump/song/all", headers=headers, json=data).json()

    ids = {}
    for song in res['list']:
        # print(song)
        song_id = song['songId']
        song_title = song['title']
        song_difficulty = song['difficulty']
        print(f'id: {song_id} name: {song_title}, difficulty: {song_difficulty}')

        ids[song_id] = song_title

    size = len(ids)
    print(f'size: {size}')
    response = requests.get(f"https://home.goldenmine.kr/pump/song/image/1/{size}", stream=True)
    # 메모리 내에서 ZIP 파일 처리
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    # 압축 해제 및 저장
    zip_file.extractall(ROOT_PATH)

    to_change = input('이름 타이틀 추가 [Y/n]: ')

    if to_change == 'Y':
        # id에 이름 붙이기
        for image_name in os.listdir(ROOT_PATH):
            old_path = os.path.join(ROOT_PATH, image_name)  # 기존 파일 경로
            image_id, ext = os.path.splitext(image_name)
            image_id = int(image_id)
            new_filename = clean_filename(ids[image_id])
            new_filename = f'{image_id}_{new_filename}{ext}'
            new_path = os.path.join(ROOT_PATH, new_filename)  # 새 파일 경로

            os.rename(old_path, new_path)


if __name__ == "__main__":
    main()
