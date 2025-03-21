import os

import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from difficulty_positions import difficulty_positions
from util import list_all_files_recursive


def find_object_in_image(main_image_path, template_image_path):
    # 이미지 불러오기
    main_image = cv2.imread(main_image_path, cv2.IMREAD_GRAYSCALE)
    # template_image = cv2.imread(template_image_path, cv2.IMREAD_GRAYSCALE)
    template_image = crop_16_9_to_5_4(template_image_path, )

    # SIFT 생성
    sift = cv2.SIFT_create(
        nfeatures=100000,
        contrastThreshold=0.1,
        nOctaveLayers=5,
        edgeThreshold=5,
        sigma=1.2,
    )

    # 특징점과 디스크립터 계산
    keypoints1, descriptors1 = sift.detectAndCompute(template_image, None)
    keypoints2, descriptors2 = sift.detectAndCompute(main_image, None)

    # 특징점 매칭 (KNN 매칭 사용)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # 좋은 매칭점 선택 (비율 테스트)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good_matches.append(m)

    # print(len(good_matches), template_image_path)
    # 최소 매칭 개수 설정
    # MIN_MATCH_COUNT = max(4, int(0.05 * len(keypoints1)))  # 최소 4개 또는 검출 특징점의 5%
    MIN_MATCH_COUNT = 10
    if len(good_matches) > MIN_MATCH_COUNT:
        # print(len(good_matches))
        # 좌표 추출
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Homography 계산
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if M is None:
            print("Homography 계산 실패!")
            return True, None
        matchesMask = mask.ravel().tolist()

        # 템플릿의 크기 구하기
        h, w = template_image.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        # print(pts, M)
        dst = cv2.perspectiveTransform(pts, M)

        # 결과 이미지에 박스 그리기
        # result_image = cv2.polylines(main_image.copy(), [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        # 결과 출력
        # plt.figure(figsize=(10, 10))
        # plt.imshow(result_image, cmap='gray')
        # plt.title("Detected Template in Main Image")
        # plt.axis("off")
        # plt.show()

        return True, dst

    else:
        # print("매칭되는 객체를 찾을 수 없습니다.")
        return False, None


def draw_x_mark(image, dst):
    """
    dst는 템플릿의 4개 꼭지점 좌표.
    중앙점을 구해서 빨간색 X를 표시.
    """
    # 중앙점 계산
    center_x = int((dst[0][0][0] + dst[2][0][0]) / 2)
    center_y = int((dst[0][0][1] + dst[2][0][1]) / 2)

    # X표 크기
    size = 20
    color = (0, 0, 255)  # 빨간색(BGR)
    thickness = 3

    cv2.line(image, (center_x - size, center_y - size),
             (center_x + size, center_y + size), color, thickness)
    cv2.line(image, (center_x + size, center_y - size),
             (center_x - size, center_y + size), color, thickness)


def check_similar_locations(locations, threshold=30):
    """
    SIFT 알고리즘으로 찾은 위치들이 비슷한지 검증하는 함수.

    Args:
        locations (list): SIFT의 위치 좌표 [(x1, y1), (x2, y2), ...].
        threshold (int): 거리 임계값. 두 위치가 이 거리보다 가까우면 '비슷'하다고 판단.

    Returns:
        list: 비슷한 위치 쌍 [(loc1, loc2, 거리), ...].
    """
    similar_pairs = []  # 비슷한 위치 저장 리스트

    # 위치 비교
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            # 두 위치의 중심 좌표 계산
            img_path1, loc1 = locations[i]
            img_path2, loc2 = locations[j]

            # 중심 좌표 추출
            center1 = np.mean(loc1, axis=0)[0]  # [(x1, y1), (x2, y2), ...]의 평균 좌표
            center2 = np.mean(loc2, axis=0)[0]

            # 두 중심점 사이 거리 계산 (유클리디안 거리)
            dist = np.linalg.norm(center1 - center2)
            if dist < threshold:  # 임계값 기준으로 비슷한 위치 판별
                similar_pairs.append((loc1, loc2, dist, img_path1, img_path2))

    return similar_pairs

def count_banner_image_2(main_image_path, positions):
    # 메인 이미지를 컬러로 불러옴 (X표를 그리기 위해)
    main_image_color = cv2.imread(main_image_path, cv2.IMREAD_COLOR)

    # 전체 배너 이미지 목록
    banner_images = list(filter(lambda x: 'SHORT CUT' not in x and 'FULL SONG' not in x,
                                list_all_files_recursive('images')))

    found_locations = []

    results = []

    for banner_image in tqdm(banner_images):
        found, location = find_object_in_image(main_image_path, banner_image)
        if found and location is not None:
            center_x = int((location[0][0][0] + location[2][0][0]) / 2)
            center_y = int((location[0][0][1] + location[2][0][1]) / 2)
            position = find_range(center_y, positions)

            found_locations.append((banner_image, location))
            results.append((banner_image, position, center_x, center_y))

    # 모든 찾은 위치에 대해 X표 그리기
    for _, loc in found_locations:
        draw_x_mark(main_image_color, loc)

    # 최종 결과 출력
    plt.figure(figsize=(12, 12))
    # BGR -> RGB 변환
    plt.imshow(cv2.cvtColor(main_image_color, cv2.COLOR_BGR2RGB))
    plt.title("Detected Templates (X Marked) in Main Image")
    plt.axis("off")
    plt.show()

    similars = check_similar_locations(found_locations)
    if len(similars) > 0:
        print("===일치===", len(similars))
        print(similars)
    print('찾은 이미지 개수', main_image_path, len(results))

    save_path = main_image_path.replace('.png', '_result.png')
    cv2.imwrite(save_path, main_image_color)

    return results


def crop_16_9_to_5_4(image_path):
    # 이미지 불러오기
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR, matplotlib은 RGB

    # 이미지 크기 가져오기
    height, width = image.shape[:2]
    # aspect_ratio = width / height

    # 16:9 비율인지 확인
    # if aspect_ratio != 16 / 9:
    #     print("입력 이미지는 16:9 비율이 아닙니다.")
    #     return

    # 새로운 5:4 비율 크기 계산
    new_height = height
    new_width = int(new_height * 5 / 4)  # 5:4 비율 적용

    # 중심 기준 크롭 좌표 계산
    x_center = width // 2
    crop_left = x_center - new_width // 2
    crop_right = x_center + new_width // 2

    # 이미지 크롭
    cropped_image = image[:, crop_left:crop_right]

    # 크롭한 이미지 표시
    # plt.figure(figsize=(10, 8))
    # plt.imshow(cropped_image)
    # plt.axis('off')
    # plt.title("5:4 비율로 크롭된 이미지")
    # plt.show()

    # 결과 반환
    return cropped_image


def find_range(value, ranges):
    for key, (start, end) in ranges.items():
        if start <= value < end:  # 범위 검사
            return key
    return None  # 범위에 없을 경우


def count_banner_image(main_image_path):
    # 필터링 안하면 588개
    # 필터링 하면 520개
    banner_images = list(filter(lambda x: 'SHORT CUT' not in x and 'FULL SONG' not in x, list_all_files_recursive('images')))
    # banner_images = list_all_files_recursive('images')

    count = 0
    for banner_image in banner_images:
        if 'SHORT CUT' in banner_image or 'FULL SONG' in banner_image:
            continue

        found, location = find_object_in_image(main_image_path, banner_image)

        if found:
            count += 1
            print(banner_image, location)

    return count


def save_file(file_path, results):
    # 파일 저장
    with open(file_path, 'wt', encoding='utf-8') as file:
        for banner_image, position, center_x, center_y in results:
            file.write(f'{banner_image} {position} {center_x} {center_y}\n')


def main():
    # main_images = [
    #     'levels/서열표S18.png',
    #     'levels/서열표S20.png',
    #     'levels/서열표S21.png',
    #     'levels/서열표S22.png',
    #     'levels/서열표S23.png',
    # ]
    main_images = list_all_files_recursive('levels')
    for main_image in main_images:
        if 'txt' in main_image or '_result' in main_image:
            continue

        if main_image not in difficulty_positions:
            print('no', main_image)
            continue
        print(f'processing {main_image}')
        positions = difficulty_positions[main_image]
        results = count_banner_image_2(main_image, positions)
        save_file(f'{main_image}.txt', results)

    # main_image = 'levels/서열표S20.png'
    # positions = difficulty_positions[main_image]
    # results = count_banner_image_2(main_image, positions)
    # save_file(f'{main_image}.txt', results)


if __name__ == '__main__':
    main()