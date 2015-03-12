import os
import time
import ConfigParser
import Image
import ImageChops
from Tkinter import Tk, Frame, Button, Listbox
from tkMessageBox import askokcancel
from Window import Window
from Webpage import Webpage


class App(Frame):
    """App window"""
    def __init__(self, parent, path):
        Frame.__init__(self, parent)
        self.parent = parent
        self.path = path
        self.pick_buttons = []
        self.initialize()

    def initialize(self):
        self.window = Window(self.path, "Chrome")
        self.webpage = Webpage()
        self.header = Frame(self.parent, width=150, height=50)
        self.header.pack(fill="x")
        self.button_frame = Frame(self.parent, width=150, height=50)
        self.button_frame.pack(fill="x")
        self.choices_list = Listbox(self.parent)
        self.choices_list.insert("end", "Choices:")
        self.choices_list.pack(fill="both", side="left", expand=1)
        self.pick_list = Listbox(self.parent)
        self.pick_list.insert("end", "Pick:")
        self.pick_list.pack(fill="both", side="left", expand=1)
        for i in xrange(3):
            self.pick_buttons.append(Button(self.button_frame))
        self.detect_hero = Button(self.header, text="Detect Hero Class")
        self.detect_hero.bind("<Button-1>", lambda event, kind="heroes": self.run(event, kind))
        self.detect_hero.pack(side="left", padx=10)

    def run(self, event, kind):
        original_text = event.widget["text"]
        event.widget["text"] = "Working..."
        event.widget["state"] = "disabled"
        self.parent.update_idletasks()
        self.window.screenshot()
        self.crop(kind)
        results = self.compare(kind)
        self.choices_list.insert("end", " | ".join(results))
        if kind == "cards":
            self.detect_pick.unbind("<Button 1>")
            self.do_cards(event, results, original_text)
        else:
            self.detect_hero.unbind("<Button 1>")
            self.do_heroes(event, results, original_text)

    def do_cards(self, event, results, original_text):
        print results
        self.webpage.enter_picks(results)
        time.sleep(0.3) # to prevent getting '-' instead of the value
        values = self.webpage.get_values()
        for i in xrange(len(results)):
            command = lambda x=i+1, text=results[i]: self.card_command(x, text)
            self.pick_buttons[i].config(text="%s - %d" %(results[i], values[i]), command=command)
            self.pick_buttons[i].pack(side="left", padx=10)
        event.widget["text"] = original_text
        # event.widget["state"] = "active"

    def card_command(self, x, text):
        self.unpack_buttons()
        self.pick_list.insert("end", text)
        self.webpage.make_pick(x)
        self.detect_pick.config(state="active")
        self.detect_pick.bind("<Button-1>", lambda event, kind="cards": self.run(event, kind))

    def do_heroes(self, event, results, original_text):
        for i in xrange(len(results)):
            command = lambda x=results[i]: self.hero_command(x)
            self.pick_buttons[i].config(text=results[i], command=command)
            self.pick_buttons[i].pack(side="left", padx=10)
        # Label(self.parent, text="    |    ".join(results)).pack()
        event.widget["text"] = original_text

    def hero_command(self, x):
        self.unpack_buttons()
        self.webpage.choose_class(x)
        self.create_detect_button()
        self.detect_pick.bind("<Button-1>", lambda event, kind="cards": self.run(event, kind))
        self.pick_list.insert("end", x)

    def unpack_buttons(self):
        for button in self.pick_buttons:
            button.pack_forget()

    def create_detect_button(self):
        self.detect_pick = Button(self.header, text="Detect Pick")
        self.detect_pick.pack(side="left", padx=10)

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
            results.append(os.path.splitext(name)[0]) # remove file extension
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
    root.wm_attributes("-topmost", 1)#, "-alpha", 0.5)  make app window always on top optionally make it transparent for future use
    app = App(root, path)
    root.protocol("WM_DELETE_WINDOW", app.ask_quit)
    root.mainloop()

if __name__ == "__main__":
    main("c:\\Temp\\test.bmp")
