import json
import os
from PIL import Image, ImageDraw, ImageOps
from collage import Layout, ImageInfo, collages

# Constants for image orientation
ORIENTATION_NORMAL = 1
ORIENTATION_ROTATE_180 = 3
ORIENTATION_ROTATE_270 = 6
ORIENTATION_ROTATE_90 = 8


class Coordinate:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def __str__(self):
        return f'Coordinate(width={self.width}, height={self.height}, x={self.x}, y={self.y})'


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
        size = img.size
        print(f"Current image: {path}, size: {size}")
        return size


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
            Coordinate(width // 2, height // 2, 0, height // 2),
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


def image_collage(image_folder, image_size=(1200, 1800), layout_list=None, border_size=6, border_color="#fff",
                  callback=None, output="自动拼接"):
    if layout_list is None:
        layout_list = [1, 2]

    print(f'image_folder: {image_folder}, image_size: {image_size}, layout_list: {layout_list}')

    # Define allowed image file extensions
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.cr2')
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if
                   f.lower().endswith(allowed_extensions)]

    if not image_files:
        print("No image files found.")
        return

    if not os.path.exists(output):
        os.mkdir(output)

    layout_list = [layout for layout in layout_list if layout in range(1, 7)]

    images = [ImageInfo(path, *get_image_size(path)) for path in image_files]

    layouts = [Layout(str(layout), image_layout(image_size, layout)) for layout in layout_list]
    result = collages(images, layouts)

    print(result)
    collage_count = 1
    idx = 0

    for collage in result:
        print("Collage length:", len(collage))
        collage_image = Image.new('RGB', image_size)

        for image_info, coordinate in collage:
            print("Current image:", image_info.path, image_info.width, image_info.height)
            print("Current coordinates:", coordinate.width, coordinate.height, coordinate.x, coordinate.y)
            image = Image.open(image_info.path)
            image = correct_image_orientation(image)
            image = image.resize((coordinate.width, coordinate.height), Image.LANCZOS)
            collage_image.paste(image, (coordinate.x, coordinate.y))
            if callback:
                callback(image_info.path, idx)
            idx += 1

        collage_image = add_border(collage_image, size=border_size, color=border_color)
        collage_image.save(f"{output}/collage_{collage_count}.jpg")
        print(f"Generated collage image: collage_{collage_count}.jpg")
        collage_count += 1


if __name__ == '__main__':
    folder_path = 'D:\\workspace\\pythonProject\\image_collage\\image'
    image_collage(folder_path, image_size=(1200, 1800), layout_list=[1, 2])
