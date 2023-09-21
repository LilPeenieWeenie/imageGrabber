import tkinter as tk
from bs4 import BeautifulSoup
import requests
from tkinter import ttk 
from tkinter import *
from PIL import Image, ImageTk
from urllib.request import urlopen



def main():

    def dlText():
        # getting vars
        searchItem = searchItem_entry.get()
        filePath = filePath_entry.get() or "C:\\Users\\jaady\\Downloads"

        url = f"https://www.google.com/search?q={searchItem}&tbm=isch"
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")

        images = doc.find_all("img")

        
        def createFile():
            try:
                outFile = open(filePath + f'/{searchItem}.txt', 'x')
            except FileExistsError:
                outFile = open(filePath + f'/{searchItem}.txt', 'a')
            return outFile

        def writeFile(images):
            image_urls = [image["src"] for image in images if image["src"].startswith("https")]
            with createFile() as outFile:
                for image in image_urls:
                    outFile.write(f"""
        {image}:
        ------------------------------------------------------------------
            """)
                    
        writeFile(images)
    

    def dlImage():
        
        canvas = tk.Canvas(root, highlightbackground="blue", height=root.winfo_reqheight(), width=root.winfo_reqwidth())
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1) 
        
        def hide_content():
            canvas.place_forget()
            backButton.pack_forget()
        
        backButton = tk.Button(root, text="back", command=hide_content)
        backButton.pack(side="bottom", pady=10)
        
        searchItem = searchItem_entry.get()
        filePath = filePath_entry.get() or "D:\\Code\\Image grabber\\Test images"

 
        url = f"https://www.google.com/search?q={searchItem}&tbm=isch"
        
        response = requests.get(url)
    
   
        if response.status_code != 200:
            print("Failed to fetch the URL")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all("img")
        image_urls = [image["src"] for image in images if image["src"].startswith("https")]
        
        x = 0
        l = 0
        rownum = 0
        for image in image_urls:
            
            if x == 5:
                rownum += 1
                x = 0
                l = 0
                
            u = urlopen(image)
            raw_data = u.read()
            u.close()
            
            
            photo = ImageTk.PhotoImage(data=raw_data)
            label = tk.Label(canvas, image=photo)
            label.image = photo
            label.grid(row=rownum, column=l, padx=10, pady=10)
            x +=1
            l +=1
        

    if combo_var.get() == "Image":
        dlImage()
    elif combo_var.get() == "Txt":
        dlText()
        
root = tk.Tk()
root.title("Image grabber")
root.geometry("900x650")


# labels
searchItem_label = tk.Label(root, text="What would you like to search for?")
filePath_label = tk.Label(root, text="Storage location(filepath)")
comboBox_label = tk.Label(root, text="Storage type")

# entry fields
searchItem_entry = tk.Entry(root)
filePath_entry = tk.Entry(root)

#combo boxes
combo_var = tk.StringVar()
combo = ttk.Combobox(root, textvariable=combo_var, values=["Txt", "Image"])
combo.current(1)

#initializing
searchItem_label.pack(pady=5)
searchItem_entry.pack(pady=10)
filePath_label.pack(pady=5)
filePath_entry.pack(pady=10)
comboBox_label.pack()
combo.pack()

    
# buttons
button = tk.Button(root, text="Submit", command=main)
button.pack()

# end main

root.mainloop()