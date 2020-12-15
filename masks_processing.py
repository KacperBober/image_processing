from os import path
from PIL import Image, ImageOps


image_path = path.join("images", "Van_Gogh_Noc.jpg")
image = Image.open(image_path)
print(image.format, image.size, image.mode)


box = (0 + int(image.size[0] * 0.2), 0 + int(image.size[1] * 0.2), int(image.size[0] * 0.8), int(image.size[1] * 0.8))

region = image.crop(box)
region = region.transpose(Image.ROTATE_180)
image.paste(region, box)
image.show()

r, g, b = image.split()
im = Image.merge("RGB", (b, g, r))
r_histogram = r.histogram()
#im = im.filter(ImageFilter.BLUR)
out = im.point(lambda i: i * 1.2)
print(sum(r_histogram))
im_gray = image.convert(mode='L')
im_gray.show()
out.show()

