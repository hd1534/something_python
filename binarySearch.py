n = 10
sortedArr = range(n)

def binarySearch(target: int) -> int:
    l = 0, u = n - 1, m = 0

    while l <= u and sortedArr[l] < sortedArr[u]:
        m = (l+u) // 2
        if sortedArr[m] < target:
            l = m + 1
        elif sortedArr[m] == target:
            return m
        else:  # sortedArr[m] > t
            u = m - 1

    return -1
