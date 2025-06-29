#第四题
"""矩形计算模块：包含面积和周长计算函数"""

def calculate_area(length, width):
    """计算矩形面积"""
    if length <= 0 or width <= 0:
        raise ValueError("长和宽必须为正数")
    return length * width

def calculate_perimeter(length, width):
    """计算矩形周长"""
    if length <= 0 or width <= 0:
        raise ValueError("长和宽必须为正数")
    return 2 * (length + width)