import os
from tkinter import *
from PIL import ImageTk,Image

def browse_button():
    os.system('cmd /c "explorer C:\\Users\\pahar\\SAR\\target.data\\"')

def main():

    Image.MAX_IMAGE_PIXELS = None
    root = Tk()
    root.title("Output")
    
    Button(text="Click To Open Path of Generated Files", command=browse_button).pack(pady=10)
    canvas = Canvas(root, width = 2000, height = 2000)
    canvas.pack()
    foo = Image.open("original.png")
    print(foo.size)
    foo = foo.resize((1000,600),Image.ANTIALIAS)
    foo.save("image_scaled.png",quality=95)
    foo1=Image.open("image_scaled.png")
    print(foo1.size)
    img = ImageTk.PhotoImage(Image.open("image_scaled.png"))
    #print(img.size)
    canvas.create_image(100, 100, anchor=NW, image=img)
    root.mainloop()

if __name__=="__main__":
    main()