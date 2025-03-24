import numpy as np


def calculate_convergence_score(votes, step_values=None):
    if step_values is None:
        # 기본 7단계 (-0.25, 0.0, ..., 1.25), 0.25 간격
        step_values = np.arange(-0.25, 1.26, 0.25)

    votes = np.array(votes)
    total_votes = np.sum(votes)

    probs = votes / total_votes
    mean = np.sum(probs * step_values)
    variance = np.sum(probs * (step_values - mean) ** 2)
    std = np.sqrt(variance)

    # 고유일수록 중급에 수렴하는 경향이 있으므로 극단으로 수렴하는 고유 곡을 높게 쳐줍니다.
    centrality = 1 - abs(mean - 0.5) / 0.75  # 0.75는 최대 거리
    extremity = 0.5 + 0.5 * abs(mean - 0.5) / 0.75

    # 집중도: 한 투표로 몰린 정도. 한 투표로 몰릴수록 높게 쳐줍니다.
    focus_score = 0.5 + 0.5 * np.max(probs)

    # 응집도: 표준편차가 낮을수록 높음
    sigma_max = 0.75
    convergence_score = focus_score * extremity * (1 - std / sigma_max)

    return {
        "mean": round(mean, 3),
        "std": round(std, 3),
        "centrality": round(centrality, 3),
        "extremity": round(extremity, 3),
        "focus_score": round(focus_score, 3),
        "convergence_score": round(convergence_score, 3)
    }


examples = {
    "중간 수렴": [0, 1, 2, 4, 2, 1, 0],
    "끝에 수렴": [0, 0, 0, 0, 0, 2, 8],
    "양쪽 끝 몰림": [2, 2, 2, 1, 2, 2, 2],
    "완전 집중": [0, 0, 0, 0, 0, 0, 10],
    "완전 평평": [1, 1, 1, 1, 1, 1, 1],
    "왼쪽 일부": [1, 1, 1, 0, 0, 0, 0],
    "왼쪽 일부1": [1, 1, 0, 1, 0, 0, 0],
    "왼쪽 일부2": [1, 0, 0, 1, 0, 0, 0],
    "왼쪽 일부3": [1, 0, 0, 1, 0, 0, 0],
    "왼쪽 일부4": [1, 0, 0, 0, 1, 0, 0],
    "왼쪽 일부5": [1, 1, 0, 0, 0, 0, 0],
    "왼쪽 일부6": [1, 1, 1, 0, 0, 0, 0],
    "왼쪽 일부7": [1, 1, 1, 1, 0, 0, 0],
    "왼쪽 일부8": [1, 1, 1, 1, 1, 0, 0],
    "한쪽": [0, 1, 0, 0, 0, 1, 0],
    "한쪽2": [0, 2, 0, 0, 0, 1, 0],
    "한쪽3": [0, 3, 0, 0, 0, 1, 0],
    "한쪽4": [0, 4, 0, 0, 0, 1, 0],
    "2한쪽": [1, 0, 0, 0, 0, 0, 1],
    "2한쪽2": [3, 0, 0, 0, 0, 0, 1],
    "2한쪽3": [5, 0, 0, 0, 0, 0, 1],
    "2한쪽3_": [6, 0, 0, 0, 0, 0, 1],
    "2한쪽4": [7, 0, 0, 0, 0, 0, 1],
    "2한쪽5": [9, 0, 0, 0, 0, 0, 1],
    "2한쪽6": [11, 0, 0, 0, 0, 0, 1],
    "쥬숏": [3, 3, 0, 0, 0, 1, 0],
    "라푸스": [0, 1, 2, 0, 0, 1, 0],
    "팬텀": [0, 1, 1, 0, 1, 1, 0],
    "러쉬-모어": [0, 1, 1, 2, 0, 1, 0],
}

for label, votes in examples.items():
    result = calculate_convergence_score(votes)

    # if result['convergence_score'] >= 0.2:
    #     continue

    print(f"{label} : {votes}")
    print(f"  Mean: {result['mean']}, Std: {result['std']}, Centrality: {result['centrality']}, extremity: {result['extremity']}, focus_score: {result['focus_score']}, Score: {result['convergence_score']}")