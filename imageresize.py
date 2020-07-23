from PIL import Image, ImageOps
import os
for image in os.listdir("size_test/"):
    original_image = Image.open("size_test/"+image)
    size = (800, 600)
    fit_and_resized_image = ImageOps.fit(original_image, size, Image.ANTIALIAS)
    fit_and_resized_image.save("size_test/"+image)
