#第一题
def is_palindrome(num):
    """
    判断一个数是否为回文数
    :param num: 待判断的数字
    :return: 布尔值，True表示是回文数，False表示不是
    """
    # 负数不可能是回文数
    if num < 0:
        return False
    # 将数字转为字符串并对比正序与逆序
    return str(num) == str(num)[::-1]

# 测试案例
print(is_palindrome(121))   # True
print(is_palindrome(123))   # False
print(is_palindrome(-121))  # False
print(is_palindrome(10))    # False
print(is_palindrome(11))    # True

#第二题
def calculate_average(*args):
    """
    计算任意数量参数的平均值
    :param args: 任意数量的数值参数
    :return: 平均值，参数为空时返回0
    """
    if not args:
        return 0
    return sum(args) / len(args)

# 测试案例
print(calculate_average(1, 2, 3, 4, 5))    # 3.0
print(calculate_average(10, 20))           # 15.0
print(calculate_average(5, 5, 5))          # 5.0
print(calculate_average(1.5, 2.5, 3.5))    # 2.5
print(calculate_average())                 # 0



#第三题
def find_longest_string(*strings):
    """
    找到输入中最长的字符串
    :param strings: 任意数量的字符串参数
    :return: 最长的字符串，无参数时返回空字符串
    """
    if not strings:
        return ""
    longest = strings[0]
    for string in strings:
        if len(string) > len(longest):
            longest = string
    return longest

# 测试案例
print(find_longest_string("apple", "banana", "cherry"))  # banana
print(find_longest_string("hi", "hello", "world"))       # hello
print(find_longest_string("a", ""))                      # a
print(find_longest_string())                             # ""



#第四题
from rectangle import calculate_area, calculate_perimeter

# 计算长8、宽2的矩形
area = calculate_area(8, 2)
perimeter = calculate_perimeter(8, 2)
print(f"矩形面积：{area}，周长：{perimeter}")  # 面积：16，周长：20
