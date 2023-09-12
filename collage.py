import random


class ImageInfo:
    def __init__(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height

    def __str__(self):
        return ', '.join(list((self.path, self.width, self.height)))


class Layout:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates


class Coordinate:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y


def collages(images, layouts):
    result = []

    # 按图片面积从大到小排序图片列表
    images.sort(key=lambda img: img.width * img.height, reverse=True)

    while len(images) >= len(layouts):
        collage = generate_collage(images, layouts)
        if collage is not None:
            print("collage len: ", len(collage))
            result.append(collage)

    return result


def generate_collage(images, layouts):
    collage = []

    for i in range(len(layouts)):
        if not images:
            break  # 没有足够的图片可用

        layout = layouts[i]
        print("当前布局: ", layout.name, len(layout.coordinates))
        coordinates = layout.coordinates
        collage_images = []

        for j in range(len(coordinates)):
            suitable_image = find_suitable_image(images, coordinates[j])
            if suitable_image is not None:
                collage_images.append((suitable_image, coordinates[j]))
            else:
                break  # 如果找不到合适的图片，跳出循环

        if len(collage_images) == len(coordinates):
            collage.extend(collage_images)
        else:
            print("跳出布局循环")
            break  # 如果无法填充完整布局，跳出循环

    return collage


def find_suitable_image(images, coordinate):
    for image in images:
        desired_aspect_ratio = coordinate.width / coordinate.height
        is_horizontal_coordinate = coordinate.width > coordinate.height

        image_aspect_ratio = image.width / image.height
        is_horizontal_image = image.width > image.height

        # if (image.width >= coordinate.width and
        #         image.height >= coordinate.height and
        #         (abs(desired_aspect_ratio - image_aspect_ratio) < 0.01 or
        #          (is_horizontal_coordinate and is_horizontal_image) or
        #          (not is_horizontal_coordinate and not is_horizontal_image))):
        if (image.width >= coordinate.width and image.height >= coordinate.height and
                (abs(desired_aspect_ratio - image_aspect_ratio) < 0.01
                 or (is_horizontal_coordinate and is_horizontal_image))):
            # 找到合适的图片，满足要求
            print("查找到合适图片")
            images.remove(image)  # 从可用图片列表中移除
            return image

    return None  # 找不到合适的图片
