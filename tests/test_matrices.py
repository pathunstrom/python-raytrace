from math import isclose

from tracer import Matrix, Vector, EPSILON


def test_matrix_4x4():
    matrix = Matrix(
        1, 2, 3, 4,
        5.5, 6.5, 7.5, 8.5,
        9, 10, 11, 12,
        13.5, 14.5, 15.5, 16.5,
    )

    assert matrix[0,0] == 1
    assert matrix[0,3] == 4
    assert matrix[1,0] == 5.5
    assert matrix[1,2] == 7.5
    assert matrix[2,2] == 11
    assert matrix[3,0] == 13.5
    assert matrix[3,2] == 15.5


def test_matrix_2x2():
    matrix = Matrix(
        -3, 5,
        1, -2
    )

    assert matrix[0,0] == -3
    assert matrix[0,1] == 5
    assert matrix[1,0] == 1
    assert matrix[1,1] == -2


def test_matrix_3x3():
    matrix = Matrix(
        -3, 5, 0,
        1, -2, -7,
        0, 1, 1
    )

    assert matrix[0,0] == -3
    assert matrix[1,1] == -2
    assert matrix[2,2] == 1


def test_matrix_equality():
    left_matrix = Matrix(
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 8, 7, 6,
        5, 4, 3, 2
    )

    right_matrix = Matrix(
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 8, 7, 6,
        5, 4, 3, 2
    )

    assert left_matrix == right_matrix


def test_matrix_inequality():
    left_matrix = Matrix(
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 8, 7, 6,
        5, 4, 3, 2
    )

    right_matrix = Matrix(
        2, 3, 4, 5,
        6, 7, 8, 9,
        8, 7, 6, 5,
        4, 3, 2, 1
    )

    assert left_matrix != right_matrix


def test_matrix_multiplication():
    left_matrix = Matrix(
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 8, 7, 6,
        5, 4, 3, 2
    )

    right_matrix = Matrix(
        -2, 1, 2, 3,
        3, 2, 1, -1,
        4, 3, 6, 5,
        1, 2, 7, 8
    )

    expected = Matrix(
        20, 22, 50, 48,
        44, 54, 114, 108,
        40, 58, 110, 102,
        16, 26, 46, 42
    )

    assert left_matrix @ right_matrix == expected


def test_matrix_by_tuple():
    matrix = Matrix(
        1, 2, 3, 4,
        2, 4, 4, 2,
        8, 6, 4, 1,
        0, 0, 0, 1
    )

    _tuple = Vector(1, 2, 3, 1)

    assert matrix * _tuple == Vector(18, 24, 33, 1)


def test_matrix_multiplication_identity():
    matrix = Matrix(
        0, 1, 2, 4,
        1, 2, 4, 8,
        2, 4, 8, 16,
        4, 8, 16, 32
    )

    assert matrix @ Matrix.identity == matrix


def test_matrix_transpose():
    matrix = Matrix(
        0, 9, 3, 0,
        9, 8, 0, 8,
        1, 8, 5, 3,
        0, 0, 5, 8
    )

    expected = Matrix(
        0, 9, 1, 0,
        9, 8, 8, 0,
        3, 0, 5, 5,
        0, 8, 3, 8
    )

    assert matrix.transpose() == expected
    assert Matrix.identity.transpose() == Matrix.identity


def test_2_by_2_determinant():
    matrix = Matrix(
        1, 5,
        -3, 2
    )

    assert matrix.determinant() == 17


def test_submatrix_3_by_3():
    matrix = Matrix(
        1, 5, 0,
        -3, 2, 7,
        0, 6, -3
    )

    expected = Matrix(
        -3, 2,
        0, 6
    )

    assert matrix.submatrix(0, 2) == expected


def test_submatrix_4_by_4():
    matrix = Matrix(
        -6, 1, 1, 6,
        -8, 5, 8, 6,
        -1, 0, 8, 2,
        -7, 1, -1, 1
    )

    expected = Matrix(
        -6, 1, 6,
        -8, 8, 6,
        -7, -1, 1
    )

    assert matrix.submatrix(2, 1) == expected


def test_matrix_minor_3_by_3():
    matrix = Matrix(
        3, 5, 0,
        2, -1, -7,
        6, -1, 5
    )

    assert matrix.submatrix(1, 0).determinant() == 25
    assert matrix.minor(1, 0) == 25


def test_matix_cofactor_3_by_3():
    matrix = Matrix(
        3, 5, 0,
        2, -1, -7,
        6, -1, 5
    )

    assert matrix.minor(0, 0) == -12
    assert matrix.cofactor(0, 0) == -12
    assert matrix.minor(1, 0) == 25
    assert matrix.cofactor(1, 0) == -25


def test_matrix_determinant_3_by_3():
    matrix = Matrix(
        1, 2, 6,
        -5, 8, -4,
        2, 6, 4
    )

    assert matrix.cofactor(0, 0) == 56
    assert matrix.cofactor(0, 1) == 12
    assert matrix.cofactor(0, 2) == -46
    assert matrix.determinant() == -196


def test_matrix_determinant_4_by_4():
    matrix = Matrix(
        -2, -8, 3, 5,
        -3, 1, 7, 3,
        1, 2, -9, 6,
        -6, 7, 7, -9
    )

    assert matrix.cofactor(0, 0) == 690
    assert matrix.cofactor(0, 1) == 447
    assert matrix.cofactor(0, 2) == 210
    assert matrix.cofactor(0, 3) == 51
    assert matrix.determinant() == -4071


def test_matrix_invertible_is_invertible():
    matrix = Matrix(
        6, 4, 4, 4,
        5, 5, 7, 6,
        4, -9, 3, -7,
        9, 1, 7, -6
    )

    assert matrix.determinant() == -2120
    assert matrix.invertible


def test_matrix_invertible_is_not_invertible():
    matrix = Matrix(
        -4, 2, -2, -3,
        9, 6, 2, 6,
        0, -5, 1, -5,
        0, 0, 0, 0
    )

    assert matrix.determinant() == 0
    assert not matrix.invertible


def test_matrix_inverse():
    matrix = Matrix(
        -5, 2, 6, -8,
        1, -5, 1, 8,
        7, 7, -6, -7,
        1, -3, 7, 4
    )

    expected = Matrix(
        0.21805, 0.45113, 0.24060, -0.04511,
        -0.80827, -1.45677, -0.44361, 0.52068,
        -0.07895, -0.22368, -0.05263, 0.19737,
        -0.52256, -0.81391, -0.30075, 0.30639
    )

    actual = matrix.inverse()

    assert matrix.determinant() == 532
    assert matrix.cofactor(2, 3) == -160
    assert isclose(actual[3, 2], -160/532, abs_tol=EPSILON)
    assert matrix.cofactor(3, 2) == 105
    assert isclose(actual[2, 3], 105/532, abs_tol=EPSILON)
    assert actual == expected


def test_matrix_inverse_another():
    matrix = Matrix(
        8, -5, 9, 2,
        7, 5, 6, 1,
        -6, 0, 9, 6,
        -3, 0, -9, -4
    )

    expected = Matrix(
        -0.15385, -0.15385, -0.28205, -0.53846,
        -0.07692, 0.12308, 0.02564, 0.03077,
        0.35897, 0.35897, 0.43590, 0.92308,
        -0.69231, -0.69231, -0.76923, -1.92308
    )
    assert matrix.inverse() == expected


def test_matrix_inverse_a_third():
    matrix = Matrix(
        9, 3, 0, 9,
        -5, -2, -6, -3,
        -4, 9, 6, 4,
        -7, 6, 6, 2
    )

    expected = Matrix(
        -0.04074, -0.07778, 0.14444, -0.22222,
        -0.07778, 0.03333, 0.36667, -0.33333,
        -0.02901, -0.14630, -0.10926, 0.12963,
        0.17778, 0.06667, -0.26667, 0.33333
    )

    assert matrix.inverse() == expected


def test_multiply_matrix_product_by_component_inverse():
    left = Matrix(
        3, -9, 7, 3,
        3, -8, 2, -9,
        -4, 4, 4, 1,
        -6, 5, -1, 1
    )

    right = Matrix(
        8, 2, 2, 2,
        3, -1, 7, 0,
        7, 0, 5, 4,
        6, -2, 0, 5
    )

    product = left @ right
    assert product @ right.inverse() == left
