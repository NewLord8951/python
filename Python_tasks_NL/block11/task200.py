from random import randint

arr = sorted([randint(1, 1000) for i in range(100)])


def print_elements_after_n(arr, n):
    for i, num in enumerate(arr):
        if num > n:
            result = arr[i+1:]
            if result:
                print
                ("Элементы, следующие за первым элементом >", n, ":", result)
                print(f"Количество элементов: {len(result)}")
            else:
                print("После первого элемента >", n, "нет следующих элементов")
            return

    print("В массиве нет элементов, больших", n)


print("Массив (первые 10 элементов):", arr[:10])
print_elements_after_n(arr, 500)
print("-" * 50)
print_elements_after_n(arr, 900)
print("-" * 50)
print_elements_after_n(arr, 1000)
