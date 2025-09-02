def f5(n):
    if n == 1:
        return 1
    else:
        cnt = 0
        for i in range(1, n + 1):
            cnt += f5(n - i)
        return cnt


N = int(input("Введите натуральное число: "))
print(f"Количество разложений: {f5(N)}")
