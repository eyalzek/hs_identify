import sys
import os
import ConfigParser
import Image
import ImageChops


def load_config(section):
    config = ConfigParser.RawConfigParser()
    config.read("dimensions_config")
    result = {}
    for field in config.items(section):
        result[field[0]] = field[1]

    return result

def crop(filename, config):
    img = Image.open(filename)
    w, h = img.size
    left = int(w / float(config["left"]))
    top = int(h / float(config["top"]))
    right = int(w / float(config["right"]))
    bottom = int(h / float(config["bottom"]))
    step = int(w / float(config["step"]))
    img_w = right - left

    files = []
    for i in xrange(3):
        im = img.crop((left, top, right, bottom))
        im.save("%d.jpg" %i)
        print("saving %d.jpg" %i)
        files.append(im)
        left = right + step
        right = right + step + img_w

    return files

def resize(files, config):
    sizea = files[0].size
    box = [int(x) for x in config["local_art"].split(",")]
    sizeb = (box[2] - box[0], box[3] - box[1])
    newx = min(sizea[0], sizeb[0])
    newy = min(sizea[1], sizeb[1])
    resized = []
    for img in files:
        resized.append(img.convert("L").resize((newx, newy), Image.ANTIALIAS))
        img.convert("L").resize((newx, newy), Image.ANTIALIAS).save("resized-bw.jpg")

    return resized

def compare(imgs, config):
    maximum, name, results = None, None, []
    local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "heroes")
    for crop in imgs:
        print("*****************************")
        for image in os.listdir(local_path):
            box = (int(x) for x in config["local_art"].split(","))
            im = Image.open(os.path.join(local_path, image)).convert("L").crop(box)
            im.save(image)
            h = ImageChops.difference(crop, im).histogram()
            black_pixels = sum(h[:50]) # check how many pixels exist in the first 50 indexes of the histogram
            print("%s: %d" %(image, black_pixels))
            if black_pixels > maximum or maximum == None:
                maximum = black_pixels
                name = image
        results.append(name)
        maximum, name = None, None

    fixed_results = [name.replace("#", ":") for name in results]
    print(fixed_results)
        

def main(filename, kind):
    config = load_config(kind)
    files = crop(filename, config)
    imgs = resize(files, config)
    compare(imgs, config)

if __name__ == "__main__":
    if not len(sys.argv) >= 2:
        print("usage: {} image-name [full/label]".format(sys.argv[0]))
    else:
        try:
            kind = sys.argv[2]
        except IndexError:
            kind = "heroes"
        main(sys.argv[1], kind)
        
