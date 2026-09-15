import pytest

from shipping import delivery_cost, delivery_days


# ============================================================
# R1. weight — число больше 0 и не больше 30 кг
# ============================================================

@pytest.mark.parametrize("weight", [0.01, 1, 15.5, 30])
def test_r1_valid_weight_is_accepted(weight):
    result = delivery_cost(weight, 10)

    assert isinstance(result, (int, float))


@pytest.mark.parametrize("weight", [-1, 0, 30.01, 31])
def test_r1_weight_outside_range_raises_value_error(weight):
    with pytest.raises(ValueError):
        delivery_cost(weight, 10)


@pytest.mark.parametrize(
    "weight",
    ["1", None, [], {}, True],
    ids=["string", "none", "list", "dict", "bool"],
)
def test_r1_invalid_weight_type_raises_type_error(weight):
    with pytest.raises(TypeError):
        delivery_cost(weight, 10)


# ============================================================
# R2. distance — целое число от 1 до 2000 км включительно
# ============================================================

@pytest.mark.parametrize("distance", [1, 100, 500, 2000])
def test_r2_valid_distance_is_accepted(distance):
    assert isinstance(delivery_cost(1, distance), (int, float))
    assert isinstance(delivery_days(distance), int)


@pytest.mark.parametrize("distance", [-1, 0, 2001, 3000])
def test_r2_distance_outside_range_raises_value_error(distance):
    with pytest.raises(ValueError):
        delivery_cost(1, distance)

    with pytest.raises(ValueError):
        delivery_days(distance)


@pytest.mark.parametrize(
    "distance",
    [1.5, 100.0, "100", None, True],
    ids=["float", "whole_float", "string", "none", "bool"],
)
def test_r2_invalid_distance_type_raises_type_error(distance):
    with pytest.raises(TypeError):
        delivery_cost(1, distance)

    with pytest.raises(TypeError):
        delivery_days(distance)


# ============================================================
# R3. express принимает только True или False
# ============================================================

@pytest.mark.parametrize("express", [True, False])
def test_r3_boolean_express_is_accepted(express):
    assert isinstance(delivery_cost(1, 100, express), (int, float))
    assert isinstance(delivery_days(100, express), int)


@pytest.mark.parametrize(
    "express",
    [1, 0, "True", "yes", None, []],
    ids=["one", "zero", "true_string", "text", "none", "list"],
)
def test_r3_invalid_express_type_raises_type_error(express):
    with pytest.raises(TypeError):
        delivery_cost(1, 100, express)

    with pytest.raises(TypeError):
        delivery_days(100, express)


# ============================================================
# R4. Стоимость:
# 200 + weight × 35 + distance × 2
# ============================================================

@pytest.mark.parametrize(
    "weight, distance, expected",
    [
        (1, 1, 237.0),
        (2.5, 100, 487.5),
        (10, 500, 1550.0),
        (30, 2000, 5250.0),
    ],
)
def test_r4_regular_delivery_cost_formula(weight, distance, expected):
    actual = delivery_cost(weight, distance, express=False)

    assert actual == expected


# ============================================================
# R5. При express=True добавляется 500 рублей
# ============================================================

@pytest.mark.parametrize(
    "weight, distance",
    [
        (1, 1),
        (1.23, 10),
        (5, 300),
        (30, 2000),
    ],
)
def test_r5_express_adds_exactly_500(weight, distance):
    regular_cost = delivery_cost(weight, distance, express=False)
    express_cost = delivery_cost(weight, distance, express=True)

    assert express_cost - regular_cost == pytest.approx(500)


@pytest.mark.parametrize(
    "weight, distance, expected",
    [
        (1, 100, 935.0),
        (2, 50, 870.0),
        (1.23, 10, 763.05),
        (30, 2000, 5750.0),
    ],
)
def test_r5_express_delivery_total_cost(weight, distance, expected):
    assert delivery_cost(weight, distance, express=True) == expected


# ============================================================
# R6. Обычный срок доставки:
# 1–100 км     — 1 день
# 101–500 км   — 3 дня
# 501–2000 км  — 7 дней
# ============================================================

@pytest.mark.parametrize(
    "distance, expected",
    [
        (1, 1),
        (99, 1),
        (100, 1),
        (101, 3),
        (499, 3),
        (500, 3),
        (501, 7),
        (1999, 7),
        (2000, 7),
    ],
)
def test_r6_regular_delivery_days(distance, expected):
    assert delivery_days(distance, express=False) == expected


# ============================================================
# R7. Экспресс-доставка сокращает срок на 1 день,
# но результат не может быть меньше 1 дня
# ============================================================

@pytest.mark.parametrize(
    "distance, expected",
    [
        (1, 1),       # 1 - 1, но минимум 1
        (50, 1),      # 1 - 1, но минимум 1
        (100, 1),     # 1 - 1, но минимум 1
        (101, 2),     # 3 - 1
        (500, 2),     # 3 - 1
        (501, 6),     # 7 - 1
        (2000, 6),    # 7 - 1
    ],
)
def test_r7_express_delivery_days(distance, expected):
    assert delivery_days(distance, express=True) == expected


def test_r7_express_days_never_less_than_one():
    result = delivery_days(1, express=True)

    assert result >= 1


# ============================================================
# R8. Стоимость округляется до двух знаков после запятой
# ============================================================

@pytest.mark.parametrize(
    "weight, distance, express, expected",
    [
        (1.2345, 10, False, 263.21),
        (1.2345, 10, True, 763.21),
        (2.3456, 10, False, 302.10),
    ],
)
def test_r8_cost_is_rounded_to_two_decimal_places(
    weight,
    distance,
    express,
    expected,
):
    assert delivery_cost(weight, distance, express) == expected


# ============================================================
# R9. Неверный тип — TypeError,
# значение вне диапазона — ValueError
# ============================================================

def test_r9_wrong_type_raises_type_error():
    with pytest.raises(TypeError):
        delivery_cost("10", 100)

    with pytest.raises(TypeError):
        delivery_cost(10, "100")

    with pytest.raises(TypeError):
        delivery_cost(10, 100, "yes")

    with pytest.raises(TypeError):
        delivery_days("100")


def test_r9_value_outside_range_raises_value_error():
    with pytest.raises(ValueError):
        delivery_cost(0, 100)

    with pytest.raises(ValueError):
        delivery_cost(31, 100)

    with pytest.raises(ValueError):
        delivery_cost(10, 0)

    with pytest.raises(ValueError):
        delivery_cost(10, 2001)

    with pytest.raises(ValueError):
        delivery_days(0)

    with pytest.raises(ValueError):
        delivery_days(2001)
