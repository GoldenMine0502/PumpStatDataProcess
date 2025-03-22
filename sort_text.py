from util import list_all_files_recursive
from tqdm import tqdm


def sort_text(file_path):
    # 파일 읽기
    # input_file = 'input.txt'  # 파일 경로를 입력하세요
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 난이도 순서 정의
    difficulty_order = ["최상", "상", "중상", "중", "중하", "하", "최하", "종특"]

    # 데이터 처리
    data = []
    for line in lines:
        parts = line.split()  # 공백 기준으로 나눔
        if len(parts) >= 3:  # 최소 3개 요소 필요
            # name은 0부터 len - 2까지 결합
            name = ' '.join(parts[:-3])  # 맨 뒤 2개를 제외한 부분
            difficulty = parts[-3]  # 뒤에서 두 번째 (난이도)
            xpos = parts[-2]  # 마지막 값 (좌표 등)
            ypos = parts[-1]  # 마지막 값 (좌표 등)

            # None이면 스킵함
            if difficulty not in difficulty_order:
                continue

            data.append((name, difficulty, xpos, ypos))

    # 난이도 정렬
    data.sort(key=lambda x: difficulty_order.index(x[1]))

    # 정렬된 데이터 다시 파일에 쓰기
    with open(file_path, 'wt', encoding='utf-8') as file:
        for item in data:
            file.write(f"{item[0]} {item[1]} {item[2]} {item[3]}\n")

    # print("파일 정렬 완료!")


# main_images = [
#     'levels/서열표S19.png',
#     'levels/서열표S20.png',
#     'levels/서열표S21.png',
#     'levels/서열표S22.png',
#     'levels/서열표S23.png',
# ]
folder = input('폴더: ')
main_images = list_all_files_recursive(folder)
# for filename in difficulty_positions.keys():
for filename in tqdm(main_images):
    if filename.endswith('.txt'):
        sort_text(filename)
