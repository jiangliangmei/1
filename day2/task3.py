import os
import re


def natural_key(string_):
    """
    生成符合Windows资源管理器排序规则的键
    支持数字按数值排序、不区分大小写、特殊字符处理
    """
    parts = re.split(r'(\d+)', string_)
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def batch_rename_images(image_folder, text_file, first_name, last_name):
    """
    按Windows自然排序重命名图片，指定首尾名字对应第一张和最后一张图片
    """
    try:
        # 读取新文件名列表
        with open(text_file, 'r', encoding='utf-8') as f:
            new_names = [line.strip() for line in f if line.strip()]
        if len(new_names) < 2:
            print("错误：文本文件中名字数量不足，至少需要2个名字")
            return

        # 获取图片文件并按Windows规则排序
        png_files = [f for f in os.listdir(image_folder)
                     if f.lower().endswith('.png')]
        if len(png_files) < 2:
            print(f"错误：文件夹中仅找到{len(png_files)}张图片，至少需要2张")
            return

        # 应用自然排序
        png_files.sort(key=natural_key)
        print("\n【Windows排序后的图片列表】")
        for idx, file in enumerate(png_files, 1):
            print(f"{idx}. {file}")

        # 校验名字与图片数量一致性
        if len(new_names) != len(png_files):
            print(f"错误：名字数量({len(new_names)})与图片数量({len(png_files)})不匹配")
            return

        # 确保首尾名字存在
        if first_name not in new_names:
            print(f"错误：文本文件中未找到指定的第一个名字：{first_name}")
            return
        if last_name not in new_names:
            print(f"错误：文本文件中未找到指定的最后一个名字：{last_name}")
            return

        # 调整名字顺序：将指定首尾名字移到对应位置
        new_names = new_names.copy()
        first_idx = new_names.index(first_name)
        last_idx = new_names.index(last_name)

        # 交换第一个名字
        new_names[0], new_names[first_idx] = new_names[first_idx], new_names[0]
        # 交换最后一个名字
        new_names[-1], new_names[last_idx] = new_names[last_idx], new_names[-1]

        print(f"\n【调整后的名字顺序】（{first_name}→第1，{last_name}→最后）")
        for idx, name in enumerate(new_names, 1):
            print(f"{idx}. {name}")

        # 执行重命名
        success_count = 0
        for old_name, new_name in zip(png_files, new_names):
            new_path = os.path.join(image_folder, f"{new_name}.png")
            old_path = os.path.join(image_folder, old_name)

            if os.path.exists(new_path) and new_path != old_path:
                print(f"冲突：{new_path} 已存在，跳过")
                continue

            os.rename(old_path, new_path)
            print(f"重命名：{old_name} → {new_name}.png")
            success_count += 1

        print(f"\n操作完成：{success_count}张图片已按指定规则重命名")

    except Exception as e:
        print(f"错误：{str(e)}")


# 使用示例
if __name__ == "__main__":
    image_folder = r"C:\Users\HONOR\Desktop\新建文件夹"
    text_file = r"C:\Users\HONOR\Desktop\新建文本文档.txt"

    # 指定首尾名字
    first_name = "冯秋华"
    last_name = "陈义谋"

    batch_rename_images(image_folder, text_file, first_name, last_name)