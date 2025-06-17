def dot(vector1: list[float], vector2: list[float]) -> float:
    result = 0
    for num1, num2 in zip(vector1, vector2):
        result += num1 * num2
    return result

def normalize(vector: list[float]) -> list[float]:
    norm = dot(vector, vector) ** 0.5
    return [num / norm for num in vector]
