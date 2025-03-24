import numpy as np
import math


def calculate_focus_convergence(votes, step_values=None):
    if step_values is None:
        step_values = np.arange(-0.25, 1.26, 0.25)

    votes = np.array(votes)
    total_votes = np.sum(votes)

    if total_votes == 0:
        return {
            "mean": None,
            "std": None,
            "focus_score": None,
            "focus_convergence": None
        }

    probs = votes / total_votes
    mean = np.sum(probs * step_values)
    variance = np.sum(probs * (step_values - mean) ** 2)
    std = np.sqrt(variance)

    sigma_max = 0.75
    cohesive_convergence = 1 - (std / sigma_max)
    focus_score = np.max(probs)

    # 새 수렴도: 표준편차 기반 수렴도 × 집중도
    focus_convergence = cohesive_convergence * focus_score

    return {
        "mean": round(mean, 3),
        "std": round(std, 3),
        "cohesive_convergence": round(cohesive_convergence, 3),
        "focus_score": round(focus_score, 3),
        "focus_convergence": round(focus_convergence, 3)
    }


def calculate_convergence_score(votes, step_values=None):
    if step_values is None:
        # 기본 7단계 (-0.25, 0.0, ..., 1.25), 0.25 간격
        step_values = np.arange(-0.25, 1.26, 0.25)

    votes = np.array(votes)
    total_votes = np.sum(votes)

    # if total_votes == 0:
    #     return {
    #         "mean": None,
    #         "std": None,
    #         "centrality": None,
    #         "convergence_score": None
    #     }

    probs = votes / total_votes
    mean = np.sum(probs * step_values)
    variance = np.sum(probs * (step_values - mean) ** 2)
    std = np.sqrt(variance)

    # 중앙성: 평균이 0.5에서 얼마나 가까운가
    centrality = 1 - abs(mean - 0.5) / 0.75  # 0.75는 최대 거리
    extremity = 0.5 + 0.5 * abs(mean - 0.5) / 0.75

    # print(np.max(probs))
    # focus_score = math.log(1 + np.max(probs))
    focus_score = 0.5 + 0.5 * np.max(probs)

    # 최대 표준편차
    sigma_max = 0.75
    # convergence_score = centrality * (1 - std / sigma_max)
    # convergence_score = focus_score * extremity * (1 - std / sigma_max)
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

# for label, votes in examples.items():
#     result = calculate_focus_convergence(votes)
#
#     # if result['focus_convergence'] >= 0:
#     #     continue
#
#     print(f"{label}")
#     print(f"  Mean: {result['mean']}, Std: {result['std']}")
#     print(f"  Cohesive Convergence: {result['cohesive_convergence']}, Focus Score: {result['focus_score']}, Final Convergence: {result['focus_convergence']}")

for label, votes in examples.items():
    result = calculate_convergence_score(votes)
    # result['convergence_score']) >= 0.2
    # -convergence_score <= 0.2
    # 0.475 - convergence_score <= 0.675
    # if (0.475 - result['convergence_score']) < 0.275:
    #     continue

    print(f"{label} : {votes}")
    # print(1 - result['convergence_score'])
    print(f"  Mean: {result['mean']}, Std: {result['std']}, Centrality: {result['centrality']}, extremity: {result['extremity']}, focus_score: {result['focus_score']}, Score: {result['convergence_score']}")