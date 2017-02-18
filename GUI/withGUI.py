from bs4 import BeautifulSoup
import requests
import os
from Tkinter import *
import shutil

global mangaNamesList
global mangaNumChapters

def get_manga_names():

    page = requests.get("http://www.mangapanda.com/alphabetical").text
    soup = BeautifulSoup(page, "lxml")
    ul_li = soup.find_all("ul", {"class": "series_alpha"})

    for ul in ul_li:
        names = ul.find_all("li")
        for name in names:
            n = name.find("a").get("href")
            mangaNamesList.append(str(n).strip().replace("/", ""))

    # for i in range(1,500) :
    #     mangaNamesList.append(str(i))

    for m in mangaNamesList:
        curr_btn = Radiobutton(root_window, text=m, variable = mangaNameSelected, width=50, padx=20, value=m)
        text.window_create("end", window = curr_btn)
        text.insert("end", "\n")

    vsb.pack(side = "right", fill = "y" )
    text.pack(fill = "both", expand = True)

def get_manga_num_chapters(mangaName):

    try:
        url = "http://mangapanda.com/" + mangaName
        t = requests.get(url).text
        s = BeautifulSoup(t, "lxml")
        tbl_li = s.find('table', {'id': 'listing'}).find_all("a")
        return len(tbl_li)
    except:
        return 0


def get_mangas(start, end, mangaName):

    for c in range(start, end + 1):
        dir_path = mangaName + "/" + str(c)
        os.system("mkdir -p " + dir_path)

        for chpt in range(1, 100000):
            url = "http://mangapanda.com/" + mangaName + "/" + str(c) + "/" + str(chpt)
            page = requests.get(url)

            if page.status_code == 404:
                break
            else:
                soup = BeautifulSoup(page.text, "lxml")
                img_url = soup.find("div", {"id": "imgholder"}).find("a").find("img").get("src")
                os.system("wget " + str(img_url) + " -O " + dir_path + "/" + str(chpt))

                # r = requests.get(settings.STATICMAP_URL.format(**data), stream=True)
                # if r.status_code == 200:
                #     with open(path, 'wb') as f:
                #         for chunk in r:
                #             f.write(chunk)

def proxy_get_chapters():
    text2.delete(1.0,END)
    mn = mangaNameSelected.get()
    mangaNumChapters = get_manga_num_chapters(mn)


    l1 = Label(root_window, text="Total Chapters = " + str(mangaNumChapters))#.grid(column=1, row=2, sticky=E)
    text2.window_create("end", window=l1)
    text2.insert("end", "\n")

    l2 = Label(root_window, text="Start Chapter")# .grid(column=2, row=3, sticky=E)
    text2.window_create("end", window=l2)
    text2.insert("end", "\n")

    l3 = Label(root_window, text="End Chapter")# .grid(column=2, row=3, sticky=E)
    text2.window_create("end", window=l3)
    text2.insert("end", "\n")

    st = IntVar()
    en = IntVar()

    e1 = Entry(root_window, textvariable = st)# .grid(column=3, row=3, sticky=E)
    text2.window_create("end", window=e1)
    text2.insert("end", "\n")

    e2 = Entry(root_window, textvariable = en)# .grid(column=3, row=3, sticky=E)
    text2.window_create("end", window=e2)
    text2.insert("end", "\n")

    def proxy_download():
        get_mangas(int(st.get()),int(en.get()), mn)

    downloadButton = Button(root_window, text="download", command = proxy_download)
    text2.window_create("end", window=downloadButton)
    text2.insert("end", "\n")
    text2.pack()

mangaNamesList = []

root_window = Tk()
text = Text(root_window, wrap = "none")
vsb = Scrollbar(orient  = "vertical", command = text.yview)
text.configure(yscrollcommand = vsb.set)


close_button = Button(root_window, text="Close", command=root_window.quit).pack()#.grid(column=1,row=8,sticky=W)


# getMangaNamesButton = Button(root_window, text="Get Names", command=get_manga_names).pack()#.grid(column=1,row=1,sticky=W)
mangaNameSelected = StringVar()
mangaNameSelected.set("anima")
get_manga_names()

getMangaChaptersButton = Button(root_window, text="Get Chapters",
                                command=proxy_get_chapters).pack()#.grid(column=2,row=8,sticky=W)
text2 = Text(root_window, wrap = "none")

root_window.mainloop()