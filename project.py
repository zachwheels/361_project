import tkinter as tk
import os
import shutil
import webbrowser
import tkinter.messagebox
import requests
import json

HEIGHT = 500
WIDTH = 800
yvalue = .075
xvalue = .17

window = tk.Tk()

webbrowser.open(r"C:\Users\zachw\Desktop\361 mvp\readme.txt")

canvas = tk.Canvas(window, height = HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(window, bg = 'yellow')
frame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)

window.iconbitmap(r"C:\Users\zachw\Desktop\361 mvp\car.ico")

# --------------------------------Functions----------------------------------------------

def soldClick():
    if(tkinter.messagebox.askokcancel("warning", "you're about to move a part in your inventory press ok to proceed")):
        moveToSold()

def moveToSold():
    root = r"C:\Users\zachw\Desktop\361Parts"
    partNum = soldPartNumberEntry.get()
    soldPrice = soldPriceEntry.get()

    for dirpath, dirnames, filenames in os.walk(root):
        if partNum in dirnames:
            fullPath = dirpath + '\\' + partNum
            withPrice = fullPath + " $%s" %(soldPrice)
    

    os.rename(fullPath, withPrice)
    destination = r"C:\Users\zachw\Desktop\361Parts\sold"

    shutil.move(withPrice, destination)
    webbrowser.open(r"C:\Users\zachw\Desktop\361 mvp\moved.txt")
    return

def makeDirectory(partNum, boxNum):
    root = r"C:\Users\zachw\Desktop\361Parts"
    boxPath = root + r"\box #" + boxNum

    if(os.path.isdir(boxPath)):
        partPath = boxPath + "\\" + partNum
        try: 
            os.mkdir(partPath)
            print("Directory " , partPath , " Created ") 
        except FileExistsError:
            print("Directory " , partPath ,  " already exists")
    else:
        os.mkdir(boxPath)
        makeDirectory(partNum, boxNum)

def makeFile(grpNum, partNum, name, env, weight, box, manufacturer, notes, numItems):
    root = r"C:\Users\zachw\Desktop\361Parts"
    filePath = root + r"\box #" + box + "\\" + partNum + "\\description.txt"

    text = "group Number: %s \nname: %s \nweight: %s \nenvelope size: %s \nmanufacturer: %s \nnumber of items: %s \nbox number: %s \nnotes: %s \n" %(grpNum, name, weight, env, manufacturer, numItems, box, notes)

    f = open(filePath, "w")
    f.truncate(0)
    f.seek(0)
    f.write(text)
    f.close()

def addPart():
    grpNum = groupNumEntry.get()
    partNum = partNumEntry.get()
    boxNum = boxNumEntry.get()

    partName = partNameEntry.get()
    envelSize = envelopeSizeEntry.get()
    weight = weightEntry.get()
    manufacturer = manufacturerEntry.get()
    notes = notesEntry.get()
    numItems = numItemsEntry.get()
    
    makeDirectory(partNum, boxNum)
    makeFile(grpNum, partNum, partName, envelSize, weight, boxNum, manufacturer, notes, numItems)
    webbrowser.open(r"C:\Users\zachw\Desktop\361 mvp\added.txt")
    
    return

def shipping():
    weight = weightEntry.get()
    zone = zoneEntry.get()

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"weight": %s, "zone": %s}' %(weight, zone)

    response = requests.post('https://password-server.herokuapp.com/shipping', headers=headers, data=data)

    jason = response.json()

    total = jason['shippingTotal']

    tkinter.messagebox.showinfo('shipping', "Shipping will cost $%s" %(total) )
    return

def findBox():
    root = r"C:\Users\zachw\Desktop\361Parts"
    partNum = partNumberBoxFindEntry.get()

    for dirpath, dirnames, filenames in os.walk(root):
        if partNum in dirnames:
            partBoxPath = os.path.basename(dirpath)
            displayBoxNum(partBoxPath)
            
    return

def displayBoxNum(partBoxPath):
    tkinter.messagebox.showinfo('Box', "your part is in %s" %(partBoxPath) )
    return

# ----------------------------------Add part labels and fields----------------------------------------


groupNumLabel = tk.Label(frame, text = "Group Number: ")
groupNumLabel.place(relx = 0, rely = 0)

partNumLabel = tk.Label(frame, text = "Part Number: ")
partNumLabel.place(relx = 0, rely = yvalue)

partNameLabel = tk.Label(frame, text = "Part Name: ")
partNameLabel.place(relx = 0, rely = 2 * yvalue)

boxNumLabel = tk.Label(frame, text = "Box Number: ")
boxNumLabel.place(relx = 0, rely = 3 * yvalue)

weightLabel = tk.Label(frame, text = "Weight: ")
weightLabel.place(relx = 0, rely = 4 * yvalue)

envelopeSizeLabel = tk.Label(frame, text = "Envelope Size: ")
envelopeSizeLabel.place(relx = 0, rely = 5 * yvalue)

imagesLabel = tk.Label(frame, text = "Images: ")
imagesLabel.place(relx = 0, rely = 6 * yvalue)

manufacturerLabel = tk.Label(frame, text = "Manufacturer: ")
manufacturerLabel.place(relx = 0, rely = 7 * yvalue)

notesLabel = tk.Label(frame, text = "Notes: ")
notesLabel.place(relx = 0, rely = 8 * yvalue)

numItemsLabel = tk.Label(frame, text = "Number of Items: ")
numItemsLabel.place(relx = 0, rely = 9 * yvalue)

groupNumEntry = tk.Entry(frame)
groupNumEntry.place(relx = xvalue, rely = 0)

partNumEntry = tk.Entry(frame)
partNumEntry.place(relx = xvalue, rely = yvalue)

partNameEntry = tk.Entry(frame)
partNameEntry.place(relx = xvalue, rely = 2* yvalue)

boxNumEntry = tk.Entry(frame)
boxNumEntry.place(relx = xvalue, rely = 3 * yvalue)

weightEntry = tk.Entry(frame)
weightEntry.place(relx = xvalue, rely = 4 * yvalue)

envelopeSizeEntry = tk.Entry(frame)
envelopeSizeEntry.place(relx = xvalue, rely = 5 * yvalue)

imagesEntry = tk.Entry(frame)
imagesEntry.place(relx = xvalue, rely = 6 * yvalue)

manufacturerEntry = tk.Entry(frame)
manufacturerEntry.place(relx = xvalue, rely = 7 * yvalue)

notesEntry = tk.Entry(frame)
notesEntry.place(relx = xvalue, rely = 8 * yvalue)

numItemsEntry = tk.Entry(frame)
numItemsEntry.place(relx = xvalue, rely = 9 * yvalue)

add = tk.Button(frame, text = "Add Part", command = addPart)
add.place(relx = .15, rely = .8)

# -------------------------------------Move to sold labels and fields----------------------------------

soldPartNumber = tk.Label(frame, text = "Part number: ")
soldPartNumber.place(relx = .5, rely = 0)

soldPrice = tk.Label(frame, text = "Sold for: ")
soldPrice.place(relx = .5, rely = .08)

soldPartNumberEntry = tk.Entry(frame)
soldPartNumberEntry.place(relx = .65, rely = 0)

soldPriceEntry = tk.Entry(frame)
soldPriceEntry.place(relx = .65, rely = .08)

add = tk.Button(frame, text = "Move to Sold", command = soldClick)
add.place(relx = .65, rely = .2)

# -------------------------------------shipping calculator labels and fields-----------------------------

weight = tk.Label(frame, text = "weight: ")
weight.place(relx = .5, rely = .4)

zone = tk.Label(frame, text = "zone: ")
zone.place(relx = .5, rely = .48)

weightEntry = tk.Entry(frame)
weightEntry.place(relx = .65, rely = .4)

zoneEntry = tk.Entry(frame)
zoneEntry.place(relx = .65, rely = .48)

add = tk.Button(frame, text = "Shipping Cost", command = shipping)
add.place(relx = .65, rely = .57)

# -------------------------------------shipping calculator labels and fields-----------------------------

partNumberBoxFind = tk.Label(frame, text = "Part Number: ")
partNumberBoxFind.place(relx = .5, rely = .72)

partNumberBoxFindEntry = tk.Entry(frame)
partNumberBoxFindEntry.place(relx = .65, rely = .72)

add = tk.Button(frame, text = "Find Box", command = findBox)
add.place(relx = .65, rely = .81)


window.mainloop()