import os
import Image

path = "../new_cards/"

for img in os.listdir(path):
    if ".png" in img:
        im = Image.open(os.path.join(path, img))
        im.load()
        new = Image.new("RGB", im.size, (255, 255, 255))
        new.paste(im, mask=im.split()[3])
        new.save(os.path.join(path, img.replace("png", "jpg")), "JPEG", quality=100)
