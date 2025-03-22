
import numpy as np

def classify_by_std(data, step_size=0.25, threshold_steps=1.5):
    """
    데이터에서 기준값(reference_value)과의 차이가 특정 단계(threshold_steps) 이상인지에 따라 분류

    :param data: 리스트 또는 배열 (비교 대상 값들)
    :param reference_value: 기준이 되는 값
    :param step_size: 단계 크기 (기본값: 0.25)
    :param threshold_steps: 몇 단계 이상의 차이를 기준으로 분류할지 (기본값: 1.5)
    :return: (차이가 큰 값 리스트, 차이가 작은 값 리스트)
    """
    threshold = threshold_steps * step_size  # 1.5단계 이상 차이의 임계값
    mean_value = np.mean(data)  # 평균값 계산
    std_dev = np.std(data)  # 표준편차 계산

    high_diff = [x for x in data if abs(x - mean_value) >= threshold]
    low_diff = [x for x in data if abs(x - mean_value) < threshold]

    return high_diff, low_diff, mean_value, std_dev


# 표준편차가 0.275 이상 차이나면 고유로 설정
# 0.275 = 평균적인 기여 차이가 하/중상 차이가 나야 넘을 수 있음
#
# 예제 데이터
# 한단계씩 차이나면 0.125 / 예시 = 하,중하 or 중상,상
# 두단계씩 차이나면 0.25
# 세단계씩 차이나면 0.375
# 하,중하,중 하나씩 기여시 0.204
# 하,중하,중,중상 하나씩 기여시 0.279
# 하,중하,중,중상,상 하나씩 기여시 0.3535
#
# 기존 v2.05 서열표에서 고유의 경우 하, 상으로 일괄 기여 = 0.5
data = [0, 0.75]

high_diff, low_diff, mean_val, std_dev = classify_by_std(data)

print("기준값과 차이가 큰 값:", high_diff)
print("기준값과 차이가 작은 값:", low_diff)
print("데이터 평균:", mean_val)
print("데이터 표준편차:", std_dev)