import sys
import os
import shlex
import subprocess
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
    top = int(h / float(config["top"]))
    first = int(w / float(config["first"]))
    step = int(w / float(config["step"]))
    res_w = int(w / float(config["res_w"]))
    res_h = int(h/ float(config["res_h"]))
    print "w,h: %d %d" %(w, h)
    print "top: %d" %top
    print "first: %d" %first
    print "step: %d" %step
    print "res_w: %d" %res_w
    print "res_h: %d" %res_h

    cmd = "convert -crop %dx%d+{}+%d \"%s\" \"{}.jpg\"" %(res_w, res_h, top, filename)
    print(cmd)

    files = []
    for i in xrange(3):
        subprocess.Popen(shlex.split(cmd.format(first, str(i))))
        print("saving {}.jpg".format(str(i)))
        files.append("%d.jpg" %i)
        first = first + res_w + step

    return files

def resize(files):
    sizea = Image.open(files[0]).size
    sizeb = Image.open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cards", "no_alpha", "Abomination.jpg")).size
    newx = min(sizea[0], sizeb[0])
    newy = min(sizea[1], sizeb[1])
    imgs = []
    for img in files:
        imgs.append({img: Image.open(img).convert("L").resize((newx, newy), Image.ANTIALIAS)})

    return imgs

def compare(imgs):
    local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cards", "no_alpha")
    for image in os.listdir(local_path):
        im = Image.open(os.path.join(local_path, image)).convert("L")
        diff = ImageChops.difference(imgs[0]["0.jpg"], im)
        # diff.save("tests/%s.jpg" %image)

def main(filename, kind):
    config = load_config(kind)
    files = crop(filename, config)
    imgs = resize(files)
    compare(imgs)

if __name__ == "__main__":
    if not len(sys.argv) >= 2:
        print("usage: {} image-name [full/label]".format(sys.argv[0]))
    else:
        try:
            kind = sys.argv[2]
        except IndexError:
            kind = "full"
        main(sys.argv[1], kind)
