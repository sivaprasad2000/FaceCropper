from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os
from PIL import Image, ImageTk
import numpy as np
import cv2

classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def saveImage() :
    global faces
    global img_clean_copy
    save_folder = filedialog.askdirectory()
    count = 1
    for face in faces :
        x, y, w, h = face
        crop_img = img_clean_copy[y:y+h, x:x+w]
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(save_folder+"/face_rec_"+str(count)+".jpg", crop_img)
        count = count+1

def browseImage() :
    filename = filedialog.askopenfilename(initialdir="~/", title="Select An Image", filetypes=(("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"), ("PNG files", "*.png"), ("webp files", "*.webp")))
    
    global img
    global faces
    global img_clean_copy

    img = cv2.imread(filename)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_clean_copy = np.copy(img)

    faces = classifier.detectMultiScale(img)

    for face in faces :
        x, y, w, h = face
        img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    temp_img = Image.fromarray(img)

    width, height = temp_img.size
    width += 80
    height += 100

    temp_img = ImageTk.PhotoImage(temp_img)
    lbl.configure(image=temp_img)
    lbl.image = temp_img

    root.geometry(str(width)+"x"+str(height))

    if len(faces) != 0 :
        btn3["state"] = NORMAL
        error_msg.configure(text=str(len(faces))+" face(s) detected")
    else :
        btn3["state"] = DISABLED
        error_msg.configure(text="Sorry no faces detected")

root = Tk()

frm = Frame(root)
frm.pack(side=BOTTOM, padx=15, pady=15)

lbl = Label(root)
lbl.pack()

img = cv2.imread("./images/mainIcon.jpeg")
img_clean_copy = np.copy(img)
faces = classifier.detectMultiScale(img)
temp_img = Image.fromarray(img)

width, height = temp_img.size
width += 80
height += 100

temp_img = ImageTk.PhotoImage(temp_img)
lbl.configure(image=temp_img)
lbl.image = temp_img

root.geometry(str(width)+"x"+str(height))

error_msg = Label(root)
error_msg.pack()

btn = Button(frm, text="Browse Image", command=browseImage)
btn.pack(side=tk.LEFT)

btn2 = Button(frm, text="Exit", command=lambda : exit())
btn2.pack(side=tk.LEFT)

btn3 = Button(frm, text="Save Image", command=saveImage)
btn3.pack(side=tk.RIGHT)
btn3["state"] = DISABLED

root.title("Face Cropper")
root.mainloop()


