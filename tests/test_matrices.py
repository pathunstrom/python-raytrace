from tracer import Matrix, Tuple


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

    _tuple = Tuple(1, 2, 3, 1)

    assert matrix * _tuple == Tuple(18, 24, 33, 1)


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
