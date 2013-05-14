from Tkinter import *
import math, Image, ImageTk
SIZE = 5

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title('Geolocalization')
        self.root.resizable(width=False, height=False)

        self.labeltext = StringVar()
        self.labeltext.set('Location')
        self.label = Label(self.root, textvariable=self.labeltext)
        self.label.pack(side=TOP)

        self.canvas = Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.bind('<Button-1>', self.clicked)
        self.canvas.pack(side=LEFT)

        person_image = Image.open('person.png')
        person_image = person_image.resize((40, 40), Image.ANTIALIAS)
        self.person_imagetk = ImageTk.PhotoImage(person_image)
        self.person = self.canvas.create_image(300, 200, image=self.person_imagetk)

        antenna_image = Image.open('antenna.png')
        antenna_image = antenna_image.resize((40, 60), Image.ANTIALIAS)
        self.antenna_imagetk = ImageTk.PhotoImage(antenna_image)

        self.a1x = 80
        self.a1y = 100
        self.antenna1 = self.canvas.create_image(self.a1x, self.a1y, image=self.antenna_imagetk)
        self.a2x = 450
        self.a2y = 100
        self.antenna2 = self.canvas.create_image(self.a2x, self.a2y, image=self.antenna_imagetk)
        self.a3x = 200
        self.a3y = 360
        self.antenna3 = self.canvas.create_image(self.a3x, self.a3y, image=self.antenna_imagetk)

    def clicked(self, event):
        x, y = event.x, event.y
        self.draw_antenna1(x, y)
        self.draw_antenna2(x, y)
        self.draw_antenna3(x, y)
        self.canvas.coords(self.person, x, y)
        self.trilateracion()

    def draw_antenna1(self, x, y):
        try:
            self.canvas.delete(self.antenna1_oval)
            self.canvas.delete(self.antenna1_radio)
            self.canvas.delete(self.antenna1_text)
        except:
            pass
        antenna_xpos = self.a1x
        antenna_ypos = self.a1y
        color = '#f00'
        base = abs(antenna_xpos-x)
        height = abs(antenna_ypos-y)
        d = math.sqrt(base**2 + height**2)
        self.r1 = d
        rxmedium = (antenna_xpos+x)/2
        rymedium = (antenna_ypos+y)/2
        radio = 'r=%d' % d
        self.antenna1_oval = self.canvas.create_oval(antenna_xpos-d, antenna_ypos-d, antenna_xpos+d, antenna_ypos+d, outline=color, width=1)
        self.antenna1_radio = self.canvas.create_line(antenna_xpos, antenna_ypos, x, y, fill=color, width=1)
        self.antenna1_text = self.canvas.create_text(rxmedium, rymedium-5, text=radio)

    def draw_antenna2(self, x, y):
        try:
            self.canvas.delete(self.antenna2_oval)
            self.canvas.delete(self.antenna2_radio)
            self.canvas.delete(self.antenna2_text)
        except:
            pass
        antenna_xpos = self.a2x
        antenna_ypos = self.a2y
        color = '#0f0'
        base = abs(antenna_xpos-x)
        height = abs(antenna_ypos-y)
        d = math.sqrt(base**2 + height**2)
        self.r2 = d
        rxmedium = (antenna_xpos+x)/2
        rymedium = (antenna_ypos+y)/2
        radio = 'r=%d' % d
        self.antenna2_oval = self.canvas.create_oval(antenna_xpos-d, antenna_ypos-d, antenna_xpos+d, antenna_ypos+d, outline=color, width=1)
        self.antenna2_radio = self.canvas.create_line(antenna_xpos, antenna_ypos, x, y, fill=color, width=1)
        self.antenna2_text = self.canvas.create_text(rxmedium, rymedium-5, text=radio)

    def draw_antenna3(self, x, y):
        try:
            self.canvas.delete(self.antenna3_oval)
            self.canvas.delete(self.antenna3_radio)
            self.canvas.delete(self.antenna3_text)
        except:
            pass
        antenna_xpos = self.a3x
        antenna_ypos = self.a3y
        color = '#00f'
        base = abs(antenna_xpos-x)
        height = abs(antenna_ypos-y)
        d = math.sqrt(base**2 + height**2)
        self.r3 = d
        rxmedium = (antenna_xpos+x)/2
        rymedium = (antenna_ypos+y)/2
        radio = 'r=%d' % d
        self.antenna3_oval = self.canvas.create_oval(antenna_xpos-d, antenna_ypos-d, antenna_xpos+d, antenna_ypos+d, outline=color, width=1)
        self.antenna3_radio = self.canvas.create_line(antenna_xpos, antenna_ypos, x, y, fill=color, width=1)
        self.antenna3_text = self.canvas.create_text(rxmedium, rymedium-5, text=radio)

    def trilateracion(self):
        r1 = self.r1
        r2 = self.r2
        r3 = self.r3
        d = self.a2x-self.a1x
        i = self.a3x-self.a1x
        j = self.a3y-self.a1y
        x = (r1**2 - r2**2 + d**2)/(2*d)
        y = (r1**2 - r3**2 - x**2 + (x-i)**2 + j**2)/(2*j)
        x += self.a1x
        y += self.a1y
        text = 'x=%d y=%d' % (x, y)
        self.labeltext.set(text)

def main():
    root = Tk()
    app = Interface(root)
    root.mainloop()

if __name__ == '__main__':
    main()

