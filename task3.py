# 生成1-100的列表并筛选偶数
even_numbers = [num for num in range(1, 101) if num % 2 == 0]
print("1-100之间的偶数：", even_numbers)




def remove_duplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

# 示例用法
original_list = [3, 1, 2, 3, 4, 2, 5]
unique_list = remove_duplicates(original_list)
print("去重后的列表：", unique_list)




keys = ["a", "b", "c"]
values = [1, 2, 3]
combined_dict = dict(zip(keys, values))
print("合并后的字典：", combined_dict)




# 定义学生信息元组
student_info = ("张三", 20, 95.5)

# 解包元组并输出
name, age, score = student_info
print(f"姓名：{name}")
print(f"年龄：{age}")
print(f"成绩：{score}")