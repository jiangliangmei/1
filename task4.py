#第一题
s1 = "Python is a powerful programming language"

# (1) 提取最后一个单词 "language"
last_word = s1.split()[-1]
print("任务1-1结果：", last_word)

# (2) 连接s1和s2并重复输出3次
s2 = " Let's learn together"
combined = (s1 + s2) * 3
print("任务1-2结果：", combined)

# (3) 输出以p/P开头的单词
p_words = [word for word in s1.split() if word.lower().startswith('p')]
print("任务1-3结果：", p_words)

#第二题
s3 = " Hello, World! This is a test string. "

# (1) 去除前后空格
stripped = s3.strip()
print("任务2-1结果：", stripped)

# (2) 转换为大写
uppercase = stripped.upper()
print("任务2-2结果：", uppercase)

# (3) 查找子串"test"的起始下标
index = stripped.find("test")
print("任务2-3结果：", index)

# (4) 替换"test"为"practice"
replaced = stripped.replace("test", "practice")
print("任务2-4结果：", replaced)

# (5) 空格分割后用"-"连接
split_joined = "-".join(stripped.split())
print("任务2-5结果：", split_joined)


