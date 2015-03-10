import os
import ConfigParser
import Image
import ImageChops
import Window


def load_config(section):
    config = ConfigParser.RawConfigParser()
    # print("filed found? %b" %os.path.exists("dimensions_config"))
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

    return resized

def compare(imgs, config):
    maximum, name, results = None, None, []
    local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cards")
    for crop in imgs:
        print("*****************************")
        for image in os.listdir(local_path):
            if ".jpg" in image:
                box = (int(x) for x in config["local_art"].split(","))
                im = Image.open(os.path.join(local_path, image)).convert("L").crop(box)
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
    with open("output.txt", "a+") as f:
        for result in fixed_results:
            f.write(result.replace(".jpg", " "))
        f.write("\n")
        os.startfile("output.txt", "open")
        f.close()
        

def main(path):
    window = Window(path, "Hearthstone")
    window.screenshot()
    files = crop(path, load_config("cards"))
    imgs = resize(files, load_config("cards"))
    compare(imgs, load_config("cards"))

if __name__ == "__main__":
    main("c:\\Temp\\test.bmp")
