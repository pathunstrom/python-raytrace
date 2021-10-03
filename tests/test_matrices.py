from tracer import Matrix


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
