def process_array(arr, a):
    """
    Обрабатывает массив, упорядоченный по убыванию.
    Находит первый элемент, меньший a, и выводит требуемые элементы.
    """
    # Проверка, что массив упорядочен по убыванию
    if not all(arr[i] >= arr[i+1] for i in range(len(arr)-1)):
        print("Ошибка: массив не упорядочен по убыванию!")
        return
    
    # Поиск первого элемента, меньшего a
    first_smaller_index = None
    for i, num in enumerate(arr):
        if num < a:
            first_smaller_index = i
            break
    
    if first_smaller_index is None:
        print("В массиве нет элементов, меньших заданного числа a.")
        return
    
    # Элементы, следующие за первым меньшим a
    following_elements = arr[first_smaller_index + 1:]
    
    # Все элементы, большие a
    greater_than_a = [num for num in arr if num > a]
    
    print(f"Первое число, меньшее {a}: {arr[first_smaller_index]} (индекс {first_smaller_index})")
    print("Элементы, следующие за ним:", following_elements)
    print("Все элементы, большие a:", greater_than_a)

# Пример использования
array = [10, 8, 7, 5, 4, 3, 2, 1]  # упорядочен по убыванию
a = 6

process_array(array, a)
