from utility import *

def validator_test():
    test_data1 = [(1, 0), (1, 2), (3, 4)]
    assert pos_validator(test_data1, 10, 10) == True
    assert pos_validator(test_data1, 3, 5) == False
    assert pos_validator(test_data1, 4, 4) == False

    test_data2 = [(1, 0), (-1, 0)]
    assert pos_validator(test_data2, 10, 10) == False

    print("Pass Validator Function Test")

def find_lines_test1():
    coord1 = [0, 0]
    pos1 = 0
    lines = find_lines(coord1, pos1)

    assert len(lines) == 3

    pos2 = 1
    lines = find_lines(coord1, pos2)

    assert lines == []

    print("Pass find lines Function Test 1")

def find_lines_test2():
    coord2 = [14, 14]
    pos1 = 4

    lines = find_lines(coord2, pos1)
    assert len(lines) == 3

    pos2 = 3
    lines = find_lines(coord2, pos2)
    assert lines == []

    print("Pass find lines Function Test 2")

def find_lines_test3():
    coord3 = [7, 7]

    for pos in range(5):
        lines = find_lines(coord3, pos)
        assert len(lines) == 4
    
    print("Pass find lines Function Test 3")

validator_test()
find_lines_test1()
find_lines_test2()
find_lines_test3()