import math
import pytest
from Boat.boat import Boat
from Boat.paddle import Paddle


@pytest.mark.parametrize('damage,result', [(0, 5), (1, 4), (5, 0), (6, 0)])
def test_success_paddle_damage(damage, result):
    paddle = Paddle(0, 1)
    value = paddle.damage(damage)
    assert value and paddle.current_durability == result


def test_failed_paddle_damage():
    paddle = Paddle(0, 1)
    value = paddle.damage(-1)
    assert not value


def test_failed_paddle_break_damage():
    paddle = Paddle(0, 1)
    paddle.damage(5)
    value = paddle.damage(5)
    assert not value


@pytest.mark.parametrize('start_angle,result_angle,angle_value_change,direction,n',
                         [(0, 30, 10, 1, 3), (0, 330, 10, -1, 3), (340, 20, 10, 1, 4), (40, 300, 20, -1, 5),
                          (0, 360, 360, 1, 1), (0, 0, 10, 0, 5)])
def test_left_paddle_twist(start_angle, result_angle, angle_value_change, direction, n):
    boat = Boat()
    boat.angle = start_angle
    for t in range(1, n + 1):
        boat.left_paddle.twist(direction, angle_value_change)
    print(boat.angle)
    assert math.isclose(boat.angle, result_angle)


@pytest.mark.parametrize('start_angle,result_angle,angle_value_change,direction,n',
                         [(0, 330, 10, 1, 3), (0, 30, 10, -1, 3), (340, 300, 10, 1, 4), (40, 140, 20, -1, 5),
                          (0, 0, 10, 0, 5)])
def test_right_paddle_twist(start_angle, result_angle, angle_value_change, direction, n):
    boat = Boat()
    boat.angle = start_angle
    for t in range(1, n + 1):
        boat.right_paddle.twist(direction, angle_value_change)
    print(boat.angle)
    assert math.isclose(boat.angle, result_angle)


def test_paddle_broke_not_twist():
    boat = Boat()
    boat.left_paddle.damage(100)
    boat.left_paddle_move(1, 10)
    print(boat.angle)
    assert boat.angle == 0


def test_left_paddle_not_twist_if_boat_broke():
    boat = Boat()
    boat.damage(100)
    assert not boat.left_paddle_move(1, 1)


def test_right_paddle_not_twist_if_boat_broke():
    boat = Boat()
    boat.damage(100)
    assert not boat.right_paddle_move(1, 1)


@pytest.mark.parametrize('t,direction,result_x,result_y',
                         [(5, 1, 0, 125), (1, -1, 0, -5), (2, 0, 0, 0)])
def test_boat_move_y(t, direction, result_x, result_y):
    boat = Boat()
    boat.move(t, direction)
    assert math.isclose(boat.x, result_x) and math.isclose(boat.y, result_y)


@pytest.mark.parametrize('weight,result', [(10, 10), (100, 100), (101, 101), (-10, 0)])
def test_weight_add_boat(weight, result):
    boat = Boat()
    boat.add_weight(weight)
    print(boat.current_weight)
    assert boat.current_weight == result


@pytest.mark.parametrize('add_weight,subtract_weight,result', [(10, 5, 5), (100, 120, 0), (101, 101, 0), (-10, -10, 0)])
def test_weight_subtract_boat(add_weight, subtract_weight, result):
    boat = Boat()
    boat.add_weight(add_weight)
    boat.subtract_weight(subtract_weight)
    print(boat.current_weight)
    assert boat.current_weight == result


def test_weight_if_boat_broken():
    boat = Boat()
    boat.damage(100)
    boat.add_weight(10)
    print(boat.current_weight)
    assert boat.current_weight == 0


@pytest.mark.parametrize('weight,result_y', [(125, 3.75), (100, 5), (150, 2.5),(1000,0)])
def test_weight_modifier(weight, result_y):
    boat = Boat()
    boat.add_weight(weight)
    print(boat.exceed_weight_modifier)
    boat.move(1, 1)
    assert math.isclose(boat.y, result_y)


@pytest.mark.parametrize('t,direction,result_x,result_y',
                         [(5, 1, 125, 0), (1, -1, -5, 0), (2, 0, 0, 0)])
def test_boat_move_x(t, direction, result_x, result_y):
    boat = Boat()
    boat.angle = 90.0
    boat.move(t, direction)
    assert math.isclose(boat.x, result_x, abs_tol=1e-9) and math.isclose(boat.y, result_y, abs_tol=1e-9)


@pytest.mark.parametrize('start_angle,result', [(10, 10), (350, 350), (-10, 0), (371, 0)])
def test_angle_set(start_angle, result):
    boat = Boat()
    boat.angle = start_angle
    assert math.isclose(boat.angle, result)


@pytest.mark.parametrize('value,result', [(371, 371), (10, 10), (-10, 100)])
def test_max_weight_set(value, result):
    boat = Boat()
    boat.max_weight = value
    print(boat.max_weight)
    assert math.isclose(boat.max_weight, result)


@pytest.mark.parametrize('value,result', [(371, 371), (20, 20), (-10, 10)])
def test_acceleration_set(value, result):
    boat = Boat()
    boat.acceleration = value
    print(boat.acceleration)
    assert math.isclose(boat.acceleration, result)


@pytest.mark.parametrize('value,result', [(371, 371), (20, 20), (-10, 10)])
def test_boat_max_durability_set(value, result):
    boat = Boat()
    boat.max_durability = value
    print(boat.max_durability)
    assert math.isclose(boat.max_durability, result)


@pytest.mark.parametrize('value,result', [(371, 371), (20, 20), (-10, 5)])
def test_paddle_max_durability_set(value, result):
    paddle = Paddle(0, 1)
    paddle.max_durability = value
    print(paddle.max_durability)
    assert math.isclose(paddle.max_durability, result)


@pytest.mark.parametrize('rotate_direction,angle,t,move_direction,x,y', [(1, 30, math.sqrt(10), 1, 25, 43.30127018922)])
def test_boat_move_to_pos(rotate_direction, angle, t, move_direction, x, y):
    boat = Boat()
    boat.left_paddle_move(rotate_direction, angle)
    boat.move(t, move_direction)
    assert math.isclose(boat.x, x, abs_tol=1e-9) and math.isclose(boat.y, y, abs_tol=1e-9)
