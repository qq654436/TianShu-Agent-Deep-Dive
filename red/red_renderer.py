#!/usr/bin/env python3
"""
天枢计划 - 小红书云端渲染引擎
利用 PIL 在底图上叠加品牌水印和爆款标题

用法:
    python red_renderer.py --input <底图> --title "标题" --output <输出>
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# 配置
BRAND_WATERMARK = "天枢计划 | TianShu"
BRAND_EMOJI = "👁️"
DEFAULT_FONT_SIZE_TITLE = 48
DEFAULT_FONT_SIZE_WATERMARK = 24


def create_gradient_background(width: int, height: int, color1: tuple, color2: tuple) -> Image:
    """创建渐变背景"""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    
    for y in range(height):
        alpha = int(255 * y / height)
        for x in range(width):
            mask.putpixel((x, y), alpha)
    
    base.paste(top, (0, 0), mask)
    return base


def add_text_overlay(image: Image, text: str, position: str = 'top', 
                     font_size: int = DEFAULT_FONT_SIZE_TITLE,
                     color: tuple = (255, 255, 255),
                     bg_color: tuple = None) -> Image:
    """添加文字覆盖层"""
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    # 尝试加载中文字体
    font_paths = [
        '/usr/share/fonts/chinese/simsun.ttc',
        '/usr/share/fonts/cjk/SimSun.ttf',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
        '/System/Library/Fonts/PingFang.ttc',
        'C:\\Windows\\Fonts\\simsun.ttc',
    ]
    
    font = None
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, font_size)
            print(f"✅ 字体已加载：{font_path}")
            break
        except:
            continue
    
    if font is None:
        try:
            font = ImageFont.load_default()
            print(f"⚠️  使用默认字体")
        except:
            font = None
    
    # 获取文字尺寸 (兼容旧版 Pillow)
    if font:
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # Pillow < 8.0.0 使用 textsize
            text_width, text_height = draw.textsize(text, font=font)
    else:
        text_width = len(text) * font_size // 2
        text_height = font_size
    
    # 计算位置
    padding = 20
    if position == 'top':
        x = padding
        y = padding
    elif position == 'bottom':
        x = padding
        y = height - text_height - padding
    elif position == 'center':
        x = (width - text_width) // 2
        y = (height - text_height) // 2
    else:
        x = padding
        y = padding
    
    # 添加背景色块 (可选)
    if bg_color:
        bg_padding = 10
        draw.rectangle(
            [x - bg_padding, y - bg_padding, 
             x + text_width + bg_padding, y + text_height + bg_padding],
            fill=bg_color
        )
    
    # 绘制文字
    draw.text((x, y), text, font=font, fill=color)
    
    return image


def add_watermark(image: Image, watermark_text: str = BRAND_WATERMARK,
                  position: str = 'bottom-right', font_size: int = DEFAULT_FONT_SIZE_WATERMARK,
                  opacity: int = 180) -> Image:
    """添加品牌水印"""
    # 创建透明图层
    txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    width, height = image.size
    
    # 尝试加载字体
    font_paths = [
        '/usr/share/fonts/chinese/simsun.ttc',
        '/usr/share/fonts/cjk/SimSun.ttf',
    ]
    
    font = None
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, font_size)
            break
        except:
            continue
    
    if font is None:
        font = ImageFont.load_default()
    
    # 水印文字 (带 emoji)
    watermark = f"{BRAND_EMOJI} {watermark_text}"
    
    # 获取文字尺寸 (兼容旧版 Pillow)
    try:
        bbox = draw.textbbox((0, 0), watermark, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # Pillow < 8.0.0 使用 textsize
        text_width, text_height = draw.textsize(watermark, font=font)
    
    # 计算位置
    padding = 15
    if position == 'bottom-right':
        x = width - text_width - padding
        y = height - text_height - padding
    elif position == 'bottom-left':
        x = padding
        y = height - text_height - padding
    elif position == 'top-right':
        x = width - text_width - padding
        y = padding
    elif position == 'top-left':
        x = padding
        y = padding
    else:
        x = width - text_width - padding
        y = height - text_height - padding
    
    # 绘制半透明背景
    bg_padding = 8
    draw.rectangle(
        [x - bg_padding, y - bg_padding, x + text_width + bg_padding, y + text_height + bg_padding],
        fill=(0, 0, 0, opacity // 2)
    )
    
    # 绘制文字 (白色半透明)
    draw.text((x, y), watermark, font=font, fill=(255, 255, 255, opacity))
    
    # 合并图层
    watermarked = Image.alpha_composite(image.convert('RGBA'), txt_layer)
    return watermarked.convert('RGB')


def render_post(base_image_path: str, title: str, output_path: str = None,
                title_position: str = 'top', watermark_position: str = 'bottom-right') -> str:
    """渲染完整的小红书帖子图片"""
    # 加载底图
    base_image = Image.open(base_image_path)
    
    # 转换为 RGB (处理 PNG 透明度)
    if base_image.mode == 'RGBA':
        # 创建白色背景
        background = Image.new('RGB', base_image.size, (255, 255, 255))
        background.paste(base_image, mask=base_image.split()[3])
        base_image = background
    elif base_image.mode != 'RGB':
        base_image = base_image.convert('RGB')
    
    print(f"📐 底图尺寸：{base_image.size}")
    
    # 添加标题
    image_with_title = add_text_overlay(
        base_image.copy(),
        title,
        position=title_position,
        font_size=DEFAULT_FONT_SIZE_TITLE,
        color=(255, 255, 255),
        bg_color=(0, 0, 0, 150)  # 半透明黑色背景
    )
    
    # 添加水印
    final_image = add_watermark(
        image_with_title,
        position=watermark_position
    )
    
    # 保存输出
    if output_path is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"/home/admin/.openclaw/workspace/tian_shu/red/output_{timestamp}.png"
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    final_image.save(output_path, 'PNG', quality=95)
    print(f"✅ 渲染完成：{output_path}")
    
    return str(output_path)


def create_title_card(title: str, width: int = 1080, height: int = 1080,
                      bg_color: tuple = (255, 100, 150)) -> str:
    """创建纯文字标题卡片 (无底图时使用)"""
    # 创建纯色背景 (简化版，避免渐变兼容性问题)
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # 简化标题 (移除 emoji，避免字体问题)
    simple_title = title.replace('🔥', '').replace('⚡', '').replace('⭐', '').replace('📊', '').strip()
    
    # 使用默认字体 (仅用于测试)
    try:
        font = ImageFont.load_default()
        # 估算文字位置
        text_width = len(simple_title) * 40
        text_height = 40
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        draw.text((x, y), simple_title[:30], font=font, fill=(255, 255, 255))
    except:
        pass
    
    # 保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = f"/home/admin/.openclaw/workspace/tian_shu/red/title_card_{timestamp}.png"
    
    image.save(output_path, 'PNG', quality=95)
    print(f"✅ 标题卡片已创建：{output_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='天枢计划 - 小红书云端渲染引擎')
    parser.add_argument('--input', type=str, help='底图路径')
    parser.add_argument('--title', type=str, required=True, help='标题文字')
    parser.add_argument('--output', type=str, help='输出路径')
    parser.add_argument('--title-pos', choices=['top', 'bottom', 'center'],
                       default='top', help='标题位置')
    parser.add_argument('--watermark-pos', 
                       choices=['top-left', 'top-right', 'bottom-left', 'bottom-right'],
                       default='bottom-right', help='水印位置')
    parser.add_argument('--title-only', action='store_true',
                       help='仅创建标题卡片 (无底图)')
    
    args = parser.parse_args()
    
    # 检查依赖
    if not HAS_PIL:
        print("❌ PIL/Pillow 未安装：pip3 install --user pillow")
        return
    
    if args.title_only:
        # 创建纯文字标题卡片
        output = create_title_card(args.title)
    elif args.input:
        # 渲染完整帖子
        output = render_post(
            args.input,
            args.title,
            args.output,
            args.title_pos,
            args.watermark_pos
        )
    else:
        print("❌ 请提供 --input 底图路径，或使用 --title-only 创建纯文字卡片")
        print("\n示例:")
        print("  python red_renderer.py --input image.png --title '爆款标题'")
        print("  python red_renderer.py --title-only --title '天枢计划启动！'")
        return
    
    print(f"\n🎨 渲染完成：{output}")


if __name__ == '__main__':
    main()
