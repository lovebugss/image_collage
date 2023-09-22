import random


class ImageInfo:
    def __init__(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height

    def __str__(self):
        return f'ImageInfo(path={self.path}, width={self.width}, height={self.height})'


class Layout:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates

    def __str__(self):
        return f'Layout(name={self.name}, coordinates=[{",".join(map(str, self.coordinates))}])'


class Collage:
    def __init__(self, layout, images):
        self.layout = layout
        self.images = images


def collages(images, layouts, size=(1200, 1800)):
    result = []
    print("collage", images, layouts)
    # 图片排序
    images.sort(key=lambda img: img.width * img.height, reverse=True)

    while len(images) >= 2:
        collage = generate_collage(images, layouts)
        if collage and len(collage) > 0:
            result.extend(collage)
    return result


def generate_collage(images, layouts):
    collage = []
    print("generate_collage", images, layouts)
    for i, layout in enumerate(layouts):
        if not images:
            break
        coordinates = layout.coordinates
        collage_images = []

        for j, coordinate in enumerate(coordinates):
            suitable_image = find_suitable_image(images, coordinate)
            if suitable_image:
                collage_images.append((suitable_image, coordinate))
        collage.append(collage_images)
    return collage


def find_suitable_image(images, coordinate):

    for image in images:
        desired_aspect_ratio = coordinate.width / coordinate.height
        image_aspect_ratio = image.width / image.height
        if abs(desired_aspect_ratio - image_aspect_ratio) < 0.01:
            print("image1", image)
            images.remove(image)
            return image
    for image in images:
        is_horizontal_coordinate = coordinate.width > coordinate.height
        is_horizontal_image = image.width > image.height
        if is_horizontal_coordinate and is_horizontal_image:
            images.remove(image)
            print("image2", image)
            return image
    if len(images) > 1:
        image = images[0]
        images.remove(image)
        print("image3", image)
        return image
    return None


if __name__ == '__main__':
    image_list = [
        ImageInfo("image/IMG_0048.JPG", 6400, 6400),
        ImageInfo("image/IMG_0098.JPG", 6400, 4000),
        ImageInfo("image/IMG_0098.JPG", 6400, 4000),
        ImageInfo("image/IMG_0098.JPG", 4000, 4000),
        ImageInfo("image/IMG_0098.JPG", 6400, 4000),
        ImageInfo("image/IMG_0048.JPG", 6400, 6400),
        ImageInfo("image/IMG_0098.JPG", 6400, 4000),
        ImageInfo("image/IMG_0098.JPG", 6400, 4000),
        ImageInfo("image/IMG_0098.JPG", 4000, 4000),
        ImageInfo("image/IMG_0098.JPG", 6400, 4000),
    ]

    layout_list = []  # Define your layout_list here
    result = collages(image_list, layout_list)
    print(result)
