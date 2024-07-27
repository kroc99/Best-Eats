import random
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and ((arr[j - gap]['score'], arr[j - gap]['review_count']) < (temp['score'], temp['review_count'])):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2

def bogo_sort(arr):
    it_count = 0
    while not is_sorted(arr):
        random.shuffle(arr)
        it_count += 1
        print("it count: " + str(it_count) + "\n")
        print(arr)
        print("\n")
    return arr

def is_sorted(arr):
    for i in range(1, len(arr)):
        if (arr[i]['score'], arr[i]['review_count']) > (arr[i - 1]['score'], arr[i - 1]['review_count']):
            return False
    return True

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less_than_pivot = [x for x in arr[1:] if (x['score'],x['review_count']) < (pivot['score'],pivot['review_count'])]
        greater_than_pivot = [x for x in arr[1:] if (x['score'],x['review_count']) >= (pivot['score'],pivot['review_count'])]
        sorted_less_than = quick_sort(less_than_pivot)
        sorted_greater_than = quick_sort(greater_than_pivot)
        return sorted_greater_than + [pivot] + sorted_less_than