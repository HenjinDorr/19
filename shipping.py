__version__ = "1.1.0"


def delivery_cost(weight: int | float, distance: int, express: bool = False,) -> float:
    
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise TypeError("weight должен иметь тип int или float")
    if isinstance(distance, bool) or not isinstance(distance, int):
        raise TypeError("distance должен иметь тип int")
    if not isinstance(express, bool):
        raise TypeError("express должен иметь тип bool")

    if weight < 0.01 or weight > 30:
        raise ValueError('weight должен быть от 0.01 до 30 кг')
    if distance < 1 or distance > 2000:
        raise ValueError('distance должен быть от 1 до 2000 км')
    
    cost = 200 + weight * 35 + distance * 2

    if express:
        cost += 500

    return round(cost, 2)


def delivery_days(distance: int, express: bool = False,) -> int:
    
    if not isinstance(express, bool):
        raise TypeError("express должен иметь тип bool")
    if isinstance(distance, bool) or not isinstance(distance, int):
        raise TypeError("distance должен иметь тип int")
    
    if distance < 1 or distance > 2000:
        raise ValueError('distance должен быть от 1 до 2000 км')

    if distance <= 100:
        days = 1
    elif distance <= 500:
        days = 3
    else:
        days = 7

    if express:
        days = max(1, days - 1)

    return days
