import os
import ConfigParser
import Image
import ImageChops
from Tkinter import Tk, Frame, Button, Label
from tkMessageBox import askokcancel
from Window import Window
from Webpage import Webpage


class App(Frame):
    """App window"""
    def __init__(self, parent, path):
        Frame.__init__(self, parent)
        self.parent = parent
        self.path = path
        self.window = Window(path, "Chrome")
        self.webpage = Webpage()
        self.detect_hero = Button(self.parent, text="Detect Hero Class")
        self.detect_hero.bind("<Button-1>", lambda event, kind="heroes": self.run(event, kind))
        self.detect_hero.pack()

    def run(self, event, kind):
        original_text = event.widget["text"]
        event.widget["text"] = "Working..."
        event.widget["state"] = "disabled"
        self.parent.update_idletasks()
        self.window.screenshot()
        self.crop(kind)
        results = self.compare(kind)
        # Label(self.parent, text="    |    ".join(results)).pack()
        if kind == "cards":
            self.webpage.enter_picks(results)
        for i in xrange(len(results)):
            if kind == "heroes":
                command = lambda x=results[i][:-4]: self.webpage.choose_class(x)
            else:
                command = lambda x=i: self.webpage.make_pick(i + 1)
            Button(self.parent, text=results[i][:-4], command=command).pack()
        event.widget["text"] = original_text
        if kind == "heroes":
            self.create_detect_button()
        else:
            event.widget["state"] = "active"

    def create_detect_button(self):
        self.detect_pick = Button(self.parent, text="Detect Pick")
        self.detect_pick.bind("<Button-1>", lambda event, kind="cards": self.run(event, kind))
        self.detect_pick.pack()

    def load_config(self, section):
        config = ConfigParser.RawConfigParser()
        config.read("dimensions_config")
        result = {}
        for field in config.items(section):
            result[field[0]] = field[1]

        return result

    def crop(self, section):
        img = Image.open(self.path)
        config = self.load_config(section)
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

        self.files = files

    def resize(self, section):
        config = self.load_config(section)
        sizea = self.files[0].size
        box = [int(x) for x in config["local_art"].split(",")]
        sizeb = (box[2] - box[0], box[3] - box[1])
        newx = min(sizea[0], sizeb[0])
        newy = min(sizea[1], sizeb[1])
        return (newx, newy)

    def compare(self, kind):
        maximum, name, results = None, None, []
        local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), kind)
        config = self.load_config(kind)
        resize_box = self.resize(kind)
        for crop in self.files:
            print("*****************************")
            crop = crop.convert("L").resize(resize_box, Image.ANTIALIAS)
            for image in os.listdir(local_path):
                if ".jpg" in image or ".png" in image:
                    box = (int(x) for x in config["local_art"].split(","))
                    im = Image.open(os.path.join(local_path, image)).convert("L").crop(box).resize(resize_box, Image.ANTIALIAS)
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

    def ask_quit(self):
        message = "Quit the program?"
        if askokcancel("Quit", message):
            self.webpage.quit()
            self.parent.destroy()

def main(path):
    root = Tk()
    root.geometry("200x200")
    app = App(root, path)
    root.protocol("WM_DELETE_WINDOW", app.ask_quit)
    root.mainloop()

if __name__ == "__main__":
    main("c:\\Temp\\test.bmp")
