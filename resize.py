import math
import os
from PIL import Image, ImageDraw, ImageOps
from datetime import datetime


class ImageInfo:
    path = ''
    width = 0
    height = 0

    def __init__(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height

    def __str__(self):
        return f'Image(path={self.path}, width={self.width}, height={self.height})'


class Layout:

    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.count = len(coordinates)

    def __str__(self):
        return f'Layout(name={self.name}, count={self.count}, coordinates=[{", ".join(map(str, self.coordinates))}])'


class Coordinate:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def __str__(self):
        return f'Coordinate(width={self.width}, height={self.height}, x={self.x}, y={self.y})'


class Collage:
    def __init__(self, layout, images):
        self.layout = layout
        self.images = images


def image_layout(size, layout):
    def layout1(width, height):
        return [
            Coordinate(width, height // 2, 0, 0),
            Coordinate(width, height // 2, 0, height // 2)]

    def layout2(width, height):
        return [
            Coordinate(width, height // 2, 0, 0),
            Coordinate(width // 2, height // 2, 0, height // 2),
            Coordinate(width // 2, height // 2, width // 2, height // 2)]

    def layout3(width, height):
        return [
            Coordinate(width, height // 2, 0, height // 2),
            Coordinate(width // 2, height // 2, 0, 0),
            Coordinate(width // 2, height // 2, width // 2, 0)]

    def layout4(width, height):
        return [
            Coordinate(width // 2, height // 2, 0, 0),
            Coordinate(width // 2, height // 2, 0, height // 2),
            Coordinate(width // 2, height // 2, width // 2, 0),
            Coordinate(width // 2, height // 2, width // 2, height // 2)]

    def layout5(width, height):
        return [
            Coordinate((width // 3), height // 2, 0, 0),
            Coordinate((width // 3 * 2), height // 2, (width // 3), 0),
            Coordinate((width // 3 * 2), height // 2, 0, height // 2),
            Coordinate((width // 3), height // 2, (width // 3 * 2), height // 2)]

    def layout6(width, height):
        return [
            Coordinate((width // 3 * 2), height // 2, 0, 0),
            Coordinate(width // 3, height // 2, (width // 3 * 2), 0),
            Coordinate(width // 3, height // 2, 0, height // 2),
            Coordinate((width // 3 * 2), height // 2, (width // 3), height // 2)]

    def layout7(width, height):
        return [
            Coordinate(width // 3, height // 2, 0, 0),
            Coordinate(width // 3, height // 2, width // 3, 0),
            Coordinate(width // 3, height // 2, width // 3 * 2, 0),
            Coordinate(width, height // 2, 0, height // 2)]

    def layout8(width, height):
        return [
            Coordinate(width, height // 2, 0, 0),
            Coordinate(width // 3, height // 2, 0, height // 2),
            Coordinate(width // 3, height // 2, width // 3, height // 2),
            Coordinate(width // 3, height // 2, width // 3 * 2, height // 2),
        ]

    def layout9(width, height):
        return [
            Coordinate(width // 2, height // 2, 0, 0),
            Coordinate(width // 2, height // 4, width // 2, 0),
            Coordinate(width // 2, height // 4, width // 2, height // 4),
            Coordinate(width, height // 2, 0, height // 2)]

    def layout10(width, height):
        return [
            Coordinate(width, height // 4, 0, 0),
            Coordinate(width, height // 4, 0, height // 4),
            Coordinate(width, height // 4, 0, height // 2),
            Coordinate(width, height // 4, 0, height // 4 * 3)]

    layout_map = {
        "1": layout1(size[0], size[1]),
        "2": layout2(size[0], size[1]),
        "3": layout3(size[0], size[1]),
        "4": layout4(size[0], size[1]),
        "5": layout5(size[0], size[1]),
        "6": layout6(size[0], size[1]),
        "7": layout7(size[0], size[1]),
        "8": layout8(size[0], size[1]),
        "9": layout9(size[0], size[1]),
        "10": layout10(size[0], size[1]),
    }
    return layout_map.get(str(layout), [])


def find_layout(image_count, layouts):
    # 初始化一个数组 dp，用于记录每个金额对应的最小找零硬币数量
    dp = [float('inf')] * (image_count + 1)
    dp[0] = 0  # 0元的最小找零硬币数量为0

    # 遍历每个硬币面额
    for layout in layouts:
        # 从硬币面额开始遍历到目标金额
        for i in range(layout.count, image_count + 1):
            # 更新 dp[i]，表示金额 i 的最小找零硬币数量
            if dp[i - layout.count] != float('inf'):
                dp[i] = min(dp[i], dp[i - layout.count] + 1)

        # 重构找零组合
    change = []
    # 剩余图片
    current_amount = image_count
    while current_amount > 0:
        found_coin = False
        for layout in layouts:
            # 找到当前硬币面额，使得 dp[current_amount] = dp[current_amount - coin] + 1
            if current_amount >= layout.count and dp[current_amount] == dp[current_amount - layout.count] + 1:
                change.append(layout)
                current_amount -= layout.count
                found_coin = True
                break
        if not found_coin:
            print("无法找到合适的组合")
            break

    return change


def make_change_dp(layouts, image_count):
    '''

    :param layouts:
    :param image_count:
    :return:
    '''
    # 初始化一个数组 dp，用于记录每个金额对应的最小找零硬币数量
    dp = [float('inf')] * (image_count + 1)
    dp[0] = 0  # 0元的最小找零硬币数量为0

    # 遍历每个硬币面额
    for layout_item_count in layouts:
        # 从硬币面额开始遍历到目标金额
        for i in range(layout_item_count, image_count + 1):
            # 更新 dp[i]，表示金额 i 的最小找零硬币数量
            dp[i] = min(dp[i], dp[i - layout_item_count] + 1)

        print(dp)
    # 重构找零组合
    change = []
    # 剩余图片
    current_amount = image_count
    while current_amount > 0:
        for layout_item_count in layouts:
            # 找到当前硬币面额，使得 dp[current_amount] = dp[current_amount - coin] + 1
            if current_amount >= layout_item_count and dp[current_amount] == dp[current_amount - layout_item_count] + 1:
                change.append(layout_item_count)
                current_amount -= layout_item_count
                break

    return change


ORIENTATION_NORMAL = 1
ORIENTATION_ROTATE_180 = 3
ORIENTATION_ROTATE_270 = 6
ORIENTATION_ROTATE_90 = 8


def correct_image_orientation(image):
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if exif is not None:
            orientation = exif.get(0x0112)
            if orientation is not None:
                if orientation == ORIENTATION_ROTATE_180:
                    return image.transpose(Image.ROTATE_180)
                elif orientation == ORIENTATION_ROTATE_270:
                    return image.transpose(Image.ROTATE_270)
                elif orientation == ORIENTATION_ROTATE_90:
                    return image.transpose(Image.ROTATE_90)
    return image


def add_border(image, size=16, color=(255, 255, 255)):
    image_with_border = ImageOps.expand(image, size, color)
    width, height = image_with_border.size
    draw = ImageDraw.Draw(image_with_border)
    line_y = height // 2
    draw.line([(0, line_y), (width, line_y)], fill=color, width=size)
    return image_with_border


def get_image_size(path):
    with Image.open(path) as img:
        img = correct_image_orientation(img)
        return img.size


def resize_image(original_image, coordinate, image_info):
    # 1. 等比例缩放
    # 计算缩放比例
    original_width, original_height = original_image.size
    width = coordinate.width
    height = coordinate.height
    # 原图尺寸
    img_size = original_image.size

    # 计算新图片尺寸
    if (original_width - width) > (original_height - height):
        new_size = int(height / original_height * original_width)
        # 等比缩放后的尺寸
        resize_arr = (new_size, height)
        x = math.ceil((new_size - width) / 2)
        # 裁剪的数据
        crop_arr = (x, 0, x + width, height)
    else:
        new_size = int(width / original_width * original_height)
        # 等比缩放后的尺寸
        resize_arr = (width, new_size)
        y = math.ceil((new_size - height) / 2)
        # 裁剪的数据
        crop_arr = (0, y, width, y + height)

    # 缩放图像
    resized_image = original_image.resize(resize_arr)

    return resized_image.crop(crop_arr)


def image_collage(image_folder, image_size=(1200, 1800), layout_list=None, border_size=6, border_color="#fff",
                  callback=None, output="自动拼接"):
    if layout_list is None:
        layout_list = [1]
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.cr2')
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if
                   f.lower().endswith(allowed_extensions)]
    images = [ImageInfo(path, *get_image_size(path)) for path in image_files]
    if not os.path.exists(output):
        os.mkdir(output)

    image_count = len(images)
    print(f'当前图片数量: {image_count}, 布局: {layout_list}')
    layout_list = [Layout('布局-' + str(i), image_layout(image_size, i)) for i in layout_list]

    # 查找最优布局组合
    layout_change = find_layout(image_count, layout_list)
    print(layout_change)
    idx = 0
    collage_count = 1
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    # 读取所有照片
    for layout in layout_change:
        print(layout)
        collage_image = Image.new('RGB', image_size)
        for coordinate in layout.coordinates:
            print(coordinate)
            image_info = images.pop()
            image = Image.open(image_info.path)
            # 选择图片
            image = correct_image_orientation(image)
            # 调整大小
            image = resize_image(image, coordinate, image_info)
            collage_image.paste(image, (coordinate.x, coordinate.y))
            if callback:
                callback(image_info.path, idx)
            idx += 1
        # 添加边框
        collage_image = add_border(collage_image, size=border_size, color=border_color)
        collage_image.save(f"{output}/{now}-collage-{collage_count}.jpg")
        print(f"Generated collage image: collage_{collage_count}.jpg")
        collage_count += 1


if __name__ == '__main__':
    folder_path = 'D:\\workspace\\pythonProject\\image_collage\\image'
    image_collage(folder_path, image_size=(1200, 1800), layout_list=[1, 2])
