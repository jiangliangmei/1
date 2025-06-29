#第一题
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [x for x in range(1, 101) if is_prime(x)]
print("1-100之间的素数：", primes)

#第二题
a, b = 0, 1
fibonacci = [a, b]  # 初始化前两项

for _ in range(18):  # 再生成18项（共20项）
    a, b = b, a + b
    fibonacci.append(b)

print("斐波那契数列前20项：", fibonacci)


#第三题
i = 1
total = 0

while i <= 10000:
    if (i % 3 == 0 or i % 5 == 0) and i % 15 != 0:
        total += i
    i += 1

print("1-10000之间满足条件的数的和：", total)