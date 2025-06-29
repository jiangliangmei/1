# 问题1：判断变量数据类型
x = 10
y = "10"
z = True

print(f"x的数据类型：{type(x)}")  # 输出：<class 'int'>
print(f"y的数据类型：{type(y)}")  # 输出：<class 'str'>
print(f"z的数据类型：{type(z)}")  # 输出：<class 'bool'>

# 问题2：计算圆的面积
radius = float(input("请输入圆的半径："))
pi = 3.14
area = pi * radius ** 2
print(f"半径为{radius}的圆面积是：{area:.2f}")  # 保留两位小数输出

# 问题3：类型转换实验
str_num = "3.14"
float_num = float(str_num)
int_num = int(float_num)

print(f"原始字符串：{str_num}，类型：{type(str_num)}")
print(f"转浮点数后：{float_num}，类型：{type(float_num)}")
print(f"转整数后：{int_num}，类型：{type(int_num)}")
print(f"转换差异说明：字符串转浮点数保留小数部分，再转整数会直接截断小数部分（非四舍五入）")
