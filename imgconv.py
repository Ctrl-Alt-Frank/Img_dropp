from PIL import Image, ImageFilter
import pillow_heif
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import whatimage

filetype = 'JPEG'
dir_path = '.'

#derive file name from file path
def picture_name(picture_path):
	pic_path = picture_path
	pic_name = pic_path[pic_path.rfind('/')+1:] #remove file path string before the last '/' character
	pic_name = pic_name[:pic_name.rfind('.')] # remove characters after the last '.'
	return pic_name

#save picture with the same name as the original one
def save_picture(dir_path,image,pic, filetype):
	image.save(f"{dir_path}/{picture_name(pic)}.{filetype}", format(filetype))

def convert_pic(dropped_pic):

	with open(dropped_pic, 'rb') as f:
		data = f.read()
		frmt = whatimage.identify_image(data)

	if(frmt == 'heic'):
		heif_file = pillow_heif.read_heif(dropped_pic)
		image = Image.frombytes(
			heif_file.mode,
			heif_file.size,
        	heif_file.data,
        	"raw",  
    		)
		save_picture(dir_path,image,dropped_pic,filetype)
	elif(frmt == None):
		lb.insert(tk.END, "Not a picture! Try again!")
	else:
		image = Image.open(dropped_pic)
		save_picture(dir_path,image,dropped_pic,filetype)


#---------set up UI---------
#---------------------------

root = TkinterDnD.Tk()
root.geometry('300x400')

header_frame = tk.Frame(root)
options_frame = tk.Frame(root)
drop_frame = tk.Frame(root)
advanced_frame = tk.Frame(root)


#Set up List Box

lb = tk.Listbox(drop_frame)
lb.insert(1, "drag your pictures to here!")
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', lambda e: lb.insert(tk.END, convert_pic(e.data)))

#Set up Radio Buttons
def sel():
	ext = ['JPEG','PNG']
	selection = "Converting to " + ext[var.get()]
	label.config(text = selection)
	global filetype
	filetype = ext[var.get()].lower()

var = tk.IntVar()

jpg_button=tk.Radiobutton(options_frame,text="JPG", variable=var, value=0, command=sel)
png_button=tk.Radiobutton(options_frame,text="PNG", variable=var, value=1, command=sel)
label = tk.Label(options_frame, text="Converting to JPG")

#Set Up Path Button

def openfile():
	global dir_path
	dir_path = tk.filedialog.askdirectory()
	label_text = 'saving your file to '+dir_path
	buttonlabel.config(text = label_text)

button = ttk.Button(advanced_frame, text = "Select Folder", command = openfile)
buttonlabel = tk.Label(advanced_frame, text="Select where I should drop your pics")

#Set Up Misc

header_title = tk.Label(header_frame, text="| IMAGE DROPPINGS 2000|")

#Organize UI elements

header_frame.pack()
options_frame.pack()
drop_frame.pack()
advanced_frame.pack()

header_title.pack(pady=10, anchor='center')
label.pack(side='left')
jpg_button.pack(side='left')
png_button.pack(side='left')
lb.pack(padx=10,pady=10, anchor='center')
buttonlabel.pack()
button.pack()
root.mainloop()