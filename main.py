import tkinter
import customtkinter
import tkinter.ttk as ttk
# from tkinter import messagebox
# import tksheet
import database
import tree_file

customtkinter.set_appearance_mode("System")

WIDTH = 1200
HEIGHT = 800
# application = customtkinter.CTk()




font1= ('Arial', 25,'bold')
font2 = ('Arial', 14)

HEIGHT_G = HEIGHT-40
WIDTH_G = 360

HIGHT_D = HEIGHT_G
WIDTH_D = WIDTH - WIDTH_G -100


if __name__ == '__main__':
    window = tkinter.Tk()  # create the Tk window like you normally do
    window.geometry(str(WIDTH)+"x"+str(HEIGHT))
    window.title("Inventaire meéicaments")
    window.iconbitmap("static/image/medicine.ico")
    # window.configure(background='white')
    # window.title("HI Yamina")
    # window.resizable(False)
    # Gets both half the screen width/height and window width/height
    positionRight = int(window.winfo_screenwidth()/2 - WIDTH/2)
    positionDown = int(window.winfo_screenheight()/2 - HEIGHT/2)
    
    # Positions the window in the center of the page.
    window.geometry("+{}+{}".format(positionRight, positionDown))
 
    database.create_table()
    tree = tree_file.tableau(window,font2)
    tree.place(x=WIDTH_G+10,y=50)
    # tree.pack(pady=5,padx=WIDTH_G+10+20,fill='both',expand=100)
    frame_gauche = tree_file.Frame_gauche(window=window,fontG=font1,WIDTH=WIDTH,HIGHT=HEIGHT,tree=tree)
    tree.bind('<ButtonRelease>',frame_gauche.display_data_gauche)
    tree.init_tab()

    search_bar = tree_file.Search_bar(window=window,tree=tree,w=WIDTH,h=HEIGHT)

    window.mainloop()
