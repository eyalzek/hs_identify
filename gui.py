import os
import ConfigParser
import Image
import ImageChops
from Tkinter import *
from Window import Window
from Webpage import Webpage


class App(Frame):
    """App window"""
    def __init__(self, parent, path, section):
        Frame.__init__(self, parent)
        self.parent = parent
        self.path = path
        self.config = self.load_config(section)
        self.window = Window(path, "Hearthstone")
        self.webpage = self.init_webpage()
        self.button = Button(self.parent, text="Detect Pick")
        self.button.bind("<Button-1>", self.run)
        self.button.pack()

    def run(self, event):
        event.widget["text"] = "Working..."
        event.widget["state"] = "disabled"
        self.parent.update_idletasks()
        self.window.screenshot()
        self.crop()
        self.resize()
        Label(self.parent, text="    |    ".join(self.compare())).pack()
        event.widget["text"] = "Detect Pick"
        event.widget["state"] = "active"
        # results = self.compare()
        
    def load_config(self, section):
        config = ConfigParser.RawConfigParser()
        # print("filed found? %b" %os.path.exists("dimensions_config"))
        config.read("dimensions_config")
        result = {}
        for field in config.items(section):
            result[field[0]] = field[1]

        return result

    def init_webpage(self):
        p = Webpage()
        heroClass = self.detectClass()
        p.choose_class(heroClass)
        return p
        # p.enter_picks(picks)
        # print(p.get_values())
        # p.make_pick(2)
        # p.quit()

    def detectClass(self):
        pass

    def crop(self):
        img = Image.open(self.path)
        w, h = img.size
        left = int(w / float(self.config["left"]))
        top = int(h / float(self.config["top"]))
        right = int(w / float(self.config["right"]))
        bottom = int(h / float(self.config["bottom"]))
        step = int(w / float(self.config["step"]))
        img_w = right - left

        files = []
        for i in xrange(3):
            im = img.crop((left, top, right, bottom))
            files.append(im)
            left = right + step
            right = right + step + img_w

        self.files = files

    def resize(self):
        sizea = self.files[0].size
        box = [int(x) for x in self.config["local_art"].split(",")]
        sizeb = (box[2] - box[0], box[3] - box[1])
        newx = min(sizea[0], sizeb[0])
        newy = min(sizea[1], sizeb[1])
        resized = []
        for img in self.files:
            resized.append(img.convert("L").resize((newx, newy), Image.ANTIALIAS))

        self.files = resized

    def compare(self):
        maximum, name, results = None, None, []
        local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cards")
        for crop in self.files:
            print("*****************************")
            for image in os.listdir(local_path):
                if ".jpg" in image:
                    box = (int(x) for x in self.config["local_art"].split(","))
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
        return fixed_results

def main(path, section):
    root = Tk()
    root.geometry("200x200")
    app = App(root, path, section)
    # root.protocol("WM_DELETE_WINDOW", app.ask_quit)
    root.mainloop()

if __name__ == "__main__":
    main("c:\\Temp\\test.bmp", "portrait")
