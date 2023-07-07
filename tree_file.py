import customtkinter
import tkinter.ttk as ttk
from tkinter import messagebox
import database
from tkinter import filedialog as fd  
from PIL import Image,ImageTk
import os
import io

text_color_white = "#f4e9e9"
bg_color_lightblue ="#a6bdfa"
font_entre = ('Roboto',20)
font_titre = ('Roboto',25,'bold')

class tableau(ttk.Treeview):
    def __init__(self,window,font):
        super().__init__(master=window,height=7,columns=['Nom','Description',"Date","Quant"])
        self.images = []
        self.row_count = 0

        font_tab = ('Roboto', 15,'bold')
        font_h = ('Roboto', 19,'bold')
        style = ttk.Style(window)
        style.theme_use("default")
        style.configure("Treeview",
                        foreground="#1e1e1e",
                        rowheight=100,
                        background="white",
                        fieldbackground="#d3c9c9",
                        borderwidth=0,
                        font = font,padding=5)
        
        style.map('Treeview', background=[('selected', '#22559b')])
            
        style.configure("Treeview.Heading",
                        background="#d3c9c9",
                        foreground="#1e1e1e",
                        relief="flat",
                        font=font_h)
        style.map("Treeview.Heading",
                background=[('active', '#3484F0')])
        
        self.scrollbar = ttk.Scrollbar(window,orient="vertical",command=self.yview)
        self.scrollbar.pack(side="right",fill="y")

        self.configure(yscrollcommand=self.scrollbar.set)
        
        self.tag_configure('even', background='white')
        self.tag_configure('odd', background='#d3c9c9')

        self.heading('#0',text='Photo')
        self.heading('Nom',text='Médicament')
        self.heading('Description',text='Description')
        self.heading('Date',text="Date d'achat")
        self.heading('Quant',text='Quantité')

        self.column('#0',width=120) #,stretch=False
        for c in self['column']:
            self.column(c,anchor='center',width=170)
      
    def insertion_tab(self,valeurs):
        text_tag = ('even',) if self.row_count % 2 else ('odd',)
        self.row_count += 1
        self.images.append(ImageTk.PhotoImage(Image.open(io.BytesIO(valeurs.pop(0))).resize((90, 90), Image.LANCZOS)))
        print("pb de avant insert")
        self.insert('','end',image=self.images[-1],values=valeurs,tags=text_tag)
        print("pb de apres insert")
        # self.insert(image=valeurs[1])

    def init_tab(self):
        medocs = database.get_all()
        self.delete(*self.get_children())
        self.images = []
        self.row_count = 0
        for medoc in medocs :
            self.insertion_tab(list(medoc))

class Frame_gauche(customtkinter.CTkFrame):
    def __init__(self,window,fontG,WIDTH,HIGHT,tree):
        HEIGHT_G = 780
        WIDTH_G = 340
        super().__init__(master=window, width=WIDTH_G,height=HEIGHT_G,corner_radius=20,fg_color="#211818")
        self.place(x=10,y=10)
        Y = 20
        X= 10
        X_entre = 32
        width_entre = 270
        self.tree = tree
        self.title_frame_gauche = customtkinter.CTkLabel(self,text_color=text_color_white,text="Gestion panel",font=fontG)
        self.title_frame_gauche.place(x = 100, y = Y)

        self.path_image= None

        self.photo_medoc_entre= customtkinter.CTkButton(self,height=35,width=width_entre,font=font_entre,text_color='#fff',text="click pour ouvrir la photo",cursor="hand2",command=self.openFile)
        self.photo_medoc_entre.place(x=X_entre,y=83)

        self.name_medoc_titre = customtkinter.CTkLabel(self,text_color=text_color_white,text='Nom médicaments :',font=font_titre)
        self.name_medoc_titre.place(x=X,y = 149)

        self.name_medoc_entre= customtkinter.CTkEntry(self,height=35,width=width_entre,text_color='#000',fg_color=text_color_white,font=font_entre)
        self.name_medoc_entre.place(x=X_entre,y = 186)


        self.description_medoc_titre = customtkinter.CTkLabel(self,text_color=text_color_white,text='description :',font=font_titre)
        self.description_medoc_titre.place(x=X,y = 241)

        self.description_medoc_entre = customtkinter.CTkTextbox(self,height=80,width=width_entre,font=font_entre,fg_color=text_color_white,text_color="#000")
        self.description_medoc_entre.place(x=X_entre,y = 288)

        self.date_titre = customtkinter.CTkLabel(self,text_color=text_color_white,text="date d'achat :",font=font_titre)
        self.date_titre.place(x=X,y = 398)

        self.date_entre= customtkinter.CTkEntry(self,height=35,width=width_entre,text_color='#000',font=font_entre,fg_color=text_color_white)
        self.date_entre.place(x=X_entre,y = 435)

        self.quantite_titre = customtkinter.CTkLabel(self,text_color=text_color_white,text="quantité :",font=font_titre)
        self.quantite_titre.place(x=X,y = 500)

        self.quantite_entre= customtkinter.CTkEntry(self,height=35,width=width_entre,text_color='#000',font=font_entre,fg_color=text_color_white)
        self.quantite_entre.place(x=X_entre,y = 537)

                
        self.btn_ajouter = customtkinter.CTkButton(self,font=font_titre,text="Ajouter",width=142,height=35,cursor="hand2",command=self.insertion_gen)
        self.btn_ajouter.place(x=14,y=639)

        self.btn_supprimer = customtkinter.CTkButton(self,font=font_titre,text="Supprimer",width=142,height=35,cursor="hand2",command=self.supprimer_gen)
        self.btn_supprimer.place(x=179,y=639)

        self.btn_clear = customtkinter.CTkButton(self,font=font_titre,text="Clear",width=142,height=35,cursor="hand2",command=lambda:self.clear_gauche(True))
        self.btn_clear.place(x=96,y=688)

    def get_info_gauche(self):
        return [self.path_image,self.name_medoc_entre.get(),self.description_medoc_entre.get("0.0", "end"),self.date_entre.get(),self.quantite_entre.get()]
    
    def clear_gauche(self,*cliqued):
        if cliqued:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.name_medoc_entre.delete(0,'end')
        self.description_medoc_entre.delete("0.0",'end')
        self.date_entre.delete(0,'end')
        self.quantite_entre.delete(0,'end')
        self.photo_medoc_entre.configure(text="click pour ouvrir la photo")

    def display_data_gauche(self,event):
        item_selectione = self.tree.focus()
        print("les elements elec de tree "+item_selectione)
        if item_selectione:
            self.clear_gauche(False)
            ligne = self.tree.item(item_selectione)['values']
            self.name_medoc_entre.insert(0,ligne[0])
            self.description_medoc_entre.insert("0.0",ligne[1])
            self.date_entre.insert(0,ligne[2])
            self.quantite_entre.insert(0,ligne[3])
    
    def insertion_gen(self):
        try:
            # self.copy_dest(self.photo_medoc_entre.cget('text'))
            valeurs = self.get_info_gauche()
            if len(valeurs) < 5:
                messagebox.showerror('Erreur','Veuillez remplir tous les champs')
            elif database.existe_deja(valeurs[1]):
                messagebox.showerror('Erreur','Le médicament existe déja')
            else :
                q = int(valeurs[4])
                database.insertion(photo=valeurs[0],nom=valeurs[1],description=valeurs[2],date=valeurs[3],quantite=q)
                self.tree.init_tab()
                messagebox.showinfo('Excelent','Insertion réussite')
        except Exception as e :
            messagebox.showerror('Erreur','Photo ou quantité entrée est incorrecte') #"La quantité doit etre un entier"
        
    def supprimer_gen(self):
        id = self.name_medoc_entre.get()
        print(id)
        if(database.existe_deja(id)):
            print(id)
            database.supprimer(id=id)
            self.clear_gauche(True)
            self.tree.init_tab()
            messagebox.showinfo('Excelent','Suppression réussite')
        else :
            messagebox.showerror('Erreur',"Le médicaments n'existe pas")

    def openFile(self):  
        # selecting the file using the askopenfilename() method of filedialog  
        the_file = fd.askopenfilename(  
        title = "Choisissez une image",  
        filetypes = [('image files', '*.png'),('image files', '*.jpg')]  
        ) 
        self.path_image= the_file
        the_file = the_file.split('/')[-1]
        self.photo_medoc_entre.configure(text=the_file,require_redraw=True)
        
                
    def copy_dest(self,the_file):
        directoryToPaste = os.path.join('./', './static/image')
        try:  
                new_file = the_file
                # new_file = shutil.copy(the_file, directoryToPaste)  
                self.path_image= new_file
                # showing success message using the messagebox's showinfo() method  
                # messagebox.showinfo(title = "File copied!",message = "The selected file has been copied to the selected location.")  
        except Exception as e:   
                print("copy paste fonc ", e)  

class Search_bar():
    def __init__(self,window,tree,w,h):
        self.tree = tree

        self.search_entre= customtkinter.CTkEntry(window,height=37,width=220,text_color='#000',fg_color=text_color_white,font=font_entre)
        self.search_entre.place(x=w -200-220 ,y =10)

        self.btn_entre = customtkinter.CTkButton(window,font=font_titre,text="Entré",width=142,height=35,cursor="hand2",command=self.search)
        self.btn_entre.place(x=w - 142 - 30,y=10)
        print(self.btn_entre.winfo_height())

    def search(self):
        query = self.search_entre.get()
        for child in self.tree.get_children():
            print(self.tree.item(child)['values'])
            if query.lower() in self.tree.item(child)['values'][0].lower():   # compare strings in  lower cases.
                print(self.tree.item(child)['values'])
                selection = child
                break     
        print('search completed')
        if(selection == None):
            messagebox.showerror('Erreur',"Médicaments n'existe pas ")
        else:
            self.tree.selection_set(selection)       
    