import json

from PIL import Image, ImageDraw, ImageFont
import os
from collage import Layout, Coordinate, ImageInfo, collages


def rotate_image(img):
    if hasattr(img, '_getexif'):
        exif = img._getexif()
        if exif is not None:
            orientation = exif.get(0x0112)
            if orientation is not None:
                if orientation == 1:
                    # 正常方向，无需旋转
                    pass
                elif orientation == 3:
                    # 需要旋转180度
                    img = img.transpose(Image.ROTATE_180)
                elif orientation == 6:
                    # 需要顺时针旋转270度
                    img = img.transpose(Image.ROTATE_270)
                elif orientation == 8:
                    # 需要顺时针旋转90度
                    img = img.transpose(Image.ROTATE_90)
    return img


def get_image_size(path):
    with Image.open(path) as img:
        if hasattr(img, '_getexif'):
            exif = img._getexif()
            if exif is not None:
                orientation = exif.get(0x0112)
                if orientation is not None:
                    if orientation == 1:
                        # 正常方向，无需旋转
                        pass
                    elif orientation == 3:
                        # 需要旋转180度
                        img = img.transpose(Image.ROTATE_180)
                    elif orientation == 6:
                        # 需要顺时针旋转270度
                        img = img.transpose(Image.ROTATE_270)
                    elif orientation == 8:
                        # 需要顺时针旋转90度
                        img = img.transpose(Image.ROTATE_90)
        size = img.size
        print(f"当前图片:  {path}, size: {size}")
        return size


def image_layout(size, layout):
    def layout1(width, height):
        return [Coordinate(width, height // 2, 0, 0), Coordinate(width, height // 2, 0, height // 2)]

    def layout2(width, height):
        return [Coordinate(width, height // 2, 0, 0), Coordinate(width // 2, height // 2, 0, height // 2),
                Coordinate(width // 2, height // 2, width // 2, height // 2)]

    def layout3(width, height):
        return [Coordinate(width // 2, height // 2, 0, 0), Coordinate(width // 2, height // 2, 0, height // 2),
                Coordinate(width // 2, height // 2, width // 2, 0),
                Coordinate(width // 2, height // 2, width // 2, height // 2)]

    def layout4(width, height):
        return [Coordinate(width // 2, height // 2, 0, 0), Coordinate(width // 2, height // 2, 0, height // 2),
                Coordinate(width // 2, height // 2, width // 2, 0),
                Coordinate(width // 2, height // 2, width // 2, height // 2)]

    def layout5(width, height):
        return []  # Add your custom layout logic here

    def layout6(width, height):
        return []  # Add your custom layout logic here

    layout_map = {
        "1": layout1(size[0], size[1]),
        "2": layout2(size[0], size[1]),
        "3": layout3(size[0], size[1]),
        "4": layout4(size[0], size[1]),
        "5": layout5(size[0], size[1]),
        "6": layout6(size[0], size[1]),
    }
    return layout_map.get(str(layout), [])


def to_image_info(path):
    size = get_image_size(path)
    return ImageInfo(path, size[0], size[1])


def to_layout():
    pass


def calculate_optimal_layout(image_files, layout_list, image_size):
    '''

    :param image_files:
    :param layout_list:
    :param image_size:
    :return: [[(width, height, x, y),(width, height, x, y)],[(width, height, x, y),(width, height, x, y)]]
    '''
    images = list(map(to_image_info, image_files))
    layouts = []
    for i in layout_list:
        c = image_layout(image_size, i)
        print("当前布局: ", i, len(c))

        layouts.append(Layout(i, c))
    result = collages(images, layouts)
    print(result)
    return result


def resize_image(image, width, height):
    return image.resize((width, height), Image.LANCZOS)


def image_collage(image_folder: str, image_size=(1200, 1800), layout_list=None, callback=None):
    if layout_list is None:
        layout_list = [1, 2]
    print(f'image_folder: {image_folder}, image_size: {image_size}, layout_list: {layout_list}')
    image_files = [f for f in os.listdir(image_folder) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.cr2'))]

    if not image_files:
        print("未找到任何图片文件.")
        return

    layout_list = [layout for layout in layout_list if layout in range(1, 7)]

    image_stack = [os.path.join(image_folder, image_file) for image_file in image_files]

    collages = calculate_optimal_layout(image_stack, layout_list, image_size)

    collage_count = 1
    idx = 0
    if os.path.exists("output") is False:
        os.mkdir("output")
    for collage in collages:
        print("拼贴图长度", len(collage))
        collage_image = Image.new('RGB', image_size)
        for image_info, coordinate in collage:
            print("当前图片: ", image_info.path, image_info.width, image_info.height)
            print("当前坐标: ", coordinate.width, coordinate.height, coordinate.x, coordinate.y)
            image = Image.open(image_info.path)
            image = rotate_image(image)
            image = resize_image(image, coordinate.width, coordinate.height)
            collage_image.paste(image, (coordinate.x, coordinate.y))
            if callback:
                callback(image_info.path, idx)
            idx = idx + 1

        collage_image.save(f"output/collage_{collage_count}.jpg")
        print(f"已生成拼贴图片: collage_{collage_count}.jpg")
        collage_count += 1


if __name__ == '__main__':
    folder_path = './image/'
    image_collage(folder_path, image_size=(1200, 1800), layout_list=[1, 2])
    # res = calculate_optimal_layout(10, [1, 2, 5], None)
    # print(res)
