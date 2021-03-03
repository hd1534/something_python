def combination(arr, child_count):
    " 음 조합 구해줘요 "

    if len(arr) < child_count:
        return []

    i, *arr = arr
    result = []

    if child_count == 2:
        for j in arr:
            result.append([i, j])
    else:
        result = [[i] + x for x in combination(arr, child_count-1)]

    return result + combination(arr, child_count)


if __name__ == "__main__":
    print("child count == 2 :\n", combination([1,2,3,4], 2))
    # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

    print("child count == 3 :\n", combination([1,2,3,4], 3))
    # [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
    
    print("child count == 4 :\n", combination([1,2,3,4], 4))
    # [[1, 2, 3, 4]]
