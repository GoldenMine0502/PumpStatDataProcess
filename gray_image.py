from PIL import Image

input_path = input('경로 입력: ')
output_path = f'{input_path}_black.png'

# 이미지 열기
image = Image.open(input_path)

# 그레이스케일 변환
gray_image = image.convert("LA")  # "L" 모드는 그레이스케일 모드

# 변환된 이미지 저장
gray_image.save(output_path)

print(f"그레이스케일 이미지가 {output_path}에 저장되었습니다.")