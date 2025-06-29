import os
import re


def natural_sort_key(s):
    """
    实现特定排序规则：
    1. 带前导零的数字（如01.png）排在相同数值的普通数字前
    2. 数字按自然数值排序
    3. 字符串不区分大小写
    """

    def convert(text):
        if text.isdigit():
            num_val = int(text)
            # 处理前导零：0开头且长度>1的数字，赋予更小的排序键
            if text.startswith('0') and len(text) > 1:
                return (num_val - 0.5, text)  # 小数部分确保前导零数字优先
            return (num_val, text)
        return text.lower()  # 字符串转小写排序

    return [convert(p) for p in re.split(r'(\d+)', s)]


def batch_rename_images(image_folder, text_file):
    """按自定义规则重命名图片，前导零数字优先排序"""
    try:
        # 读取新文件名
        with open(text_file, 'r', encoding='utf-8') as f:
            new_names = [line.strip() for line in f if line.strip()]
        if not new_names:
            print("错误：文本文件中没有有效名字")
            return

        # 获取图片并按自定义规则排序
        png_files = [f for f in os.listdir(image_folder) if f.lower().endswith('.png')]
        if not png_files:
            print("错误：文件夹中未找到PNG图片")
            return

        # 应用带前导零优先的排序规则
        png_files.sort(key=natural_sort_key)

        # 显示排序结果（用于验证）
        print("\n【前导零优先排序后的图片列表】")
        for idx, file in enumerate(png_files, 1):
            print(f"{idx}. {file}")

        # 校验数量一致性
        max_rename = min(len(new_names), len(png_files))
        if len(new_names) < len(png_files):
            print(f"\n警告：名字数量不足，仅处理前{max_rename}张图片")

        # 执行重命名
        success_count = 0
        for i in range(max_rename):
            old_name = png_files[i]
            new_name = new_names[i].strip()
            if not new_name:
                print(f"跳过：文本行{i + 1}名字为空")
                continue

            old_path = os.path.join(image_folder, old_name)
            new_path = os.path.join(image_folder, f"{new_name}.png")

            # 冲突检测
            if old_path == new_path:
                print(f"跳过：{old_name} 新名与原名相同")
                continue
            if os.path.exists(new_path):
                print(f"冲突：{new_path} 已存在，跳过")
                continue

            os.rename(old_path, new_path)
            print(f"重命名：{old_name} → {new_name}.png")
            success_count += 1

        print(f"\n操作完成：共{success_count}张图片重命名成功")

    except FileNotFoundError:
        print("错误：文件夹或文本文件不存在")
    except PermissionError:
        print("错误：无操作权限，请以管理员身份运行")
    except Exception as e:
        print(f"未知错误：{str(e)}")


# 使用示例
if __name__ == "__main__":
    image_folder = r"C:\Users\HONOR\Desktop\新建文件夹"
    text_file = r"C:\Users\HONOR\Desktop\新建文本文档.txt"
    batch_rename_images(image_folder, text_file)