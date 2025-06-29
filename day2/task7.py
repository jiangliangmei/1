from PIL import Image, ImageEnhance, ImageFilter
import os


def enhance_tif_image(input_path, output_path, scale_factor=1.5, contrast_factor=1.3, sharpen_strength=1.5):
    """
    增强TIF图像并保存到指定位置，包含完整的错误处理和路径验证
    """
    try:
        # 验证输入路径是否存在
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入文件不存在: {input_path}")

        # 打开图像
        with Image.open(input_path) as img:
            # 显示原始图像信息（调试用）
            print(f"原始图像尺寸: {img.width}x{img.height}, 模式: {img.mode}")

            # 1. 调整图像大小（提高分辨率）
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            img = img.resize(new_size, Image.LANCZOS)  # 高质量重采样

            # 2. 增强对比度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast_factor)

            # 3. 应用锐化滤镜
            img = img.filter(ImageFilter.UnsharpMask(
                radius=2,  # 锐化范围（1-3为宜）
                percent=int(sharpen_strength * 100)  # 锐化强度百分比
            ))

            # 4. 保存处理后的图像（使用LZW无损压缩）
            img.save(output_path, compression="tiff_lzw")

            # 验证输出文件是否生成
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / 1024  # KB为单位
                print(f"✅ 图像处理完成！")
                print(f"输出路径: {output_path}")
                print(f"输出尺寸: {img.width}x{img.height}")
                print(f"文件大小: {file_size:.2f} KB")
            else:
                raise FileNotFoundError("输出文件未生成，请检查权限")

    except FileNotFoundError as fnf_error:
        print(f"❌ 文件错误: {fnf_error}")
    except PermissionError as perm_error:
        print(f"❌ 权限错误: {perm_error}，请确保有读写权限")
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {str(e)}")


# 指定你的图像路径（已使用原始字符串处理反斜杠）
image_path = r"C:\Users\HONOR\Desktop\2020_0427_fire_B2348_B12_10m_roi.tif"

# 生成输出路径（在原文件名前添加"enhanced_"前缀）
output_dir = os.path.dirname(image_path)  # 确保输出到同一目录
filename = os.path.basename(image_path)
output_path = os.path.join(output_dir, f"enhanced_{filename}")

# 执行图像增强
print("开始处理图像...")
enhance_tif_image(image_path, output_path)

# 打开输出目录（Windows系统专用，方便查看结果）
if os.name == 'nt':  # Windows系统
    os.system(f'explorer "{output_dir}"')