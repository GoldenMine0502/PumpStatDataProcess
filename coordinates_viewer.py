import cv2
import os
import glob

# 1. 이미지 폴더 경로 지정
IMAGE_FOLDER = input("이미지 폴더: ")  # 여기만 바꿔도 됨

# 2. 이미지 확장자별로 경로 불러오기
image_paths = sorted(
    glob.glob(os.path.join(IMAGE_FOLDER, "*.png")) +
    glob.glob(os.path.join(IMAGE_FOLDER, "*.jpg")) +
    glob.glob(os.path.join(IMAGE_FOLDER, "*.jpeg"))
)

if not image_paths:
    print("❌ 이미지 파일이 없습니다.")
    exit()


# 3. 마우스 클릭 콜백 함수
def click_callback(event, x, y, flags, param):
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        b, g, r = img[y, x]
        print(f"📍 좌표: ({x}, {y}) - 색상(BGR): ({b}, {g}, {r})")


# 4. 이미지 순회
index = 0
while index < len(image_paths):
    path = image_paths[index]
    img = cv2.imread(path)

    if img is None:
        print(f"⚠ 이미지를 불러올 수 없음: {path}")
        index += 1
        continue

    window_name = f"[{index+1}/{len(image_paths)}] {os.path.basename(path)}"
    cv2.imshow(window_name, img)
    cv2.setMouseCallback(window_name, click_callback, img)

    print(f"🖼 {os.path.basename(path)} 열림 (스페이스: 다음 / ESC: 종료)")

    key = cv2.waitKey(0)

    if key == 27:  # ESC 키
        print("👋 종료합니다.")
        break
    elif key == 32:  # 스페이스 키
        index += 1
        cv2.destroyWindow(window_name)

cv2.destroyAllWindows()
