import os
import re


def natural_key(string_):
    """
    生成自然排序的键，模拟Windows资源管理器的排序规则
    示例："img10.png" -> ("img", 10, ".png")
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', string_)]


def batch_rename_images(image_folder, text_file):
    """
    批量将image_folder中的PNG图片按照text_file中的名字顺序重命名
    使用自定义自然排序，与Windows资源管理器排序规则一致
    """
    try:
        # 读取文本文件中的所有行作为新文件名
        with open(text_file, 'r', encoding='utf-8') as f:
            new_names = [line.strip() for line in f if line.strip()]

        # 获取文件夹中所有PNG文件，并按自然排序规则排序
        png_files = [f for f in os.listdir(image_folder)
                     if f.lower().endswith('.png')]
        png_files.sort(key=natural_key)  # 应用自然排序

        # 显示排序后的文件列表（用于调试）
        print("\n检测到的图片文件（按Windows排序）：")
        for idx, file in enumerate(png_files, 1):
            print(f"{idx}. {file}")

        # 确保有足够的新名字
        if len(new_names) < len(png_files):
            print(f"\n警告: 文本文件中的名字数量({len(new_names)})少于图片数量({len(png_files)})")
            print(f"只有前{len(new_names)}张图片会被重命名")

        # 执行重命名操作
        renamed_count = 0
        for i, old_name in enumerate(png_files):
            if i >= len(new_names):
                break  # 没有更多新名字了

            old_path = os.path.join(image_folder, old_name)
            new_name_with_ext = f"{new_names[i]}.png"
            new_path = os.path.join(image_folder, new_name_with_ext)

            # 避免同名文件冲突
            if os.path.exists(new_path):
                print(f"冲突: 新文件名 {new_name_with_ext} 已存在，跳过此文件")
                continue

            os.rename(old_path, new_path)
            print(f"已重命名: {old_name} -> {new_name_with_ext}")
            renamed_count += 1

        print(f"\n操作完成! 共成功重命名了{renamed_count}张图片")

    except Exception as e:
        print(f"发生错误: {e}")


# 使用示例
if __name__ == "__main__":
    image_folder = r"C:\Users\HONOR\Desktop\新建文件夹"
    text_file = r"C:\Users\HONOR\Desktop\新建文本文档.txt"

    # 验证路径是否存在
    if not os.path.exists(image_folder):
        print(f"错误: 图片文件夹路径不存在 - {image_folder}")
    elif not os.path.exists(text_file):
        print(f"错误: 文本文件路径不存在 - {text_file}")
    else:
        batch_rename_images(image_folder, text_file)