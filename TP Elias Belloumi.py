import PIL.Image
import PIL.ImageTk
from random import randint
from tkinter import *
from functools import partial

def negatif(photo):
    '''fonction qui transforme une image en son négatif en soustraiant la valeur du pixel à 255. Prends en argument la photo trasformée par PIL'''
    taille=photo.size #obtiens la taille de la photo
    for i in range (taille[0]): #parcours chaque largeur
        for j in range (taille[1]): #parcours chaque hauteur
            pixel=photo.getpixel((i,j))#obtiens le pixel
            photo.putpixel((i,j),(255-pixel[0],255-pixel[1],255-pixel[2]))#transforme ce pixel en son inverse
    return photo

def filtrergb(photo,index):
    '''fonction qui applique un filtre rouge. Prends en argument une image transfromée pour pillow'''
    taille=photo.size
    for i in range (taille[0]): #parcours chaque largeur
        for j in range(taille[1]):#parcours chaque hauteur
            pixel=photo.getpixel((i,j))
            
            photo.putpixel((i,j),(pixel[0],0,0)) #transforme le pixel en rouge
        
        
    return photo

def NetB(photo, seuil):
    '''fonction qui transforme une image en sa version noir et blanc avec un seuil donné. On calcule le seuil de gris via une formule. Si ce seuil est plus grand que celui rentré par l'utilisateur, le pixel devient noir. Prends en arguments la photo trasformée par PIL et un nombre entier pour le seuil'''
    taille=photo.size
    for i in range (taille[0]): #parcours chaque largeur
        for j in range(taille[1]):#parcours chaque hauteur
            pixel=photo.getpixel((i,j))
            gray = int(round(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2] ))#calcule le gris
            if gray >= seuil :
                photo.putpixel((i,j),(0,0,0)) #transforme le pixel en pixel noir
            else:
                photo.putpixel((i,j),(255,255,255)) #transforme le pixel en pixel blanc
    return photo

def contour(photo,seuil):
    '''fonction qui transforme une image en sa version "contour" pour un seuil donné. Elle utilise la valeurs absolue de la moyenne de pixels pour définir si le pixel doit devenir blanc ou noir.Prends en arguments la photo trasformée par PIL et un nombre entier pour le seuil'''
    taille=photo.size
    taille = photo.size
    for i in range(0, taille[0] - 1):
        for j in range(0, taille[1] - 1):
            a = photo.getpixel((i, j))
            b = photo.getpixel((i + 1, j)) #obtiens le pixel a droite
            c = photo.getpixel((i, j + 1))#obtiens le pixel en bas
            if abs(moyennepixel(a) - moyennepixel(b)) > seuil or abs(moyennepixel(a) - moyennepixel(c)) > seuil: #calcule la valeur absolue et la compare au seuil
                photo.putpixel((i, j), (0, 0, 0)) #transforme le pixel en pixel noir
            else:
                photo.putpixel((i, j), (255, 255, 255))#transforme le pixel en pixel blanc
    return photo

def miroir(photo):
    '''fonction qui inverse l'image pour un effet miroir, cela en découpant la photo en 2 et en inversant les pixels. Prends en argument la photo trasformée par PIL'''
    taille=photo.size
    for i in range(int(taille[0]/2)): #pour la largeur de l'image divisée par 2
        for j in range(taille[1]):
            a=photo.getpixel((i,j))
            b=photo.getpixel((int(taille[0])-i-1,j)) #obtiens le pixel à l'opposé
            photo.putpixel((i,j),b)#met le pixel b à son opposé(le pixel a)
            photo.putpixel((int(taille[0])-i-1,j),a) #met le pixel a à son opposé (le pixel b)
    return photo

def resizing(photo,facteur):
    '''fonction qui redimensionne l'image pour un facteur donné. Prends en argument la photo trasformée par PIL et un float pour le facteur.'''
    taille=photo.size
    largeur=int(taille[0]*facteur) #crée la largeur de la nouvelle image
    hauteur=int(taille[1]*facteur) #crée la hauteur de la nouvelle image
    diffhauteur=taille[1]-hauteur-2 #calcule la différence de hauteur
    difflargeur=taille[0]-largeur-2 #calcule la différence de largeur
    newImage= PIL.Image.new('RGB',(largeur,hauteur)) #crée une nouvelle image avec ces données
    if facteur>1:
        newImage=photo.resize((largeur,hauteur)) #utilise un fonction pré-enregistrée pour augmenter la taille de l'image
    elif facteur<1:
        def créerindex(différence,tailleimg):
            '''crée une liste d'index de pixels d'une image'''
            liste=[]
            liste1=[]
            liste2=[]
            liste3=[]
            taille1=int(tailleimg/3) #divise l'image par 3
            taille2=int(taille1*2)
            for i in range(0,int(différence/3)):
                liste1.append(randint(0,taille1)) #ajoute des pixels du premier tier de l'image dans une liste
            liste.extend(liste1)#ajoute cette liste à une autre
            for i in range(0,int(différence/3)):#ajoute des pixels du 2ème tier de l'image dans une liste
                liste2.append(randint(taille1,taille2))
            for i in range(0,int(différence/3)):#ajoute des pixels du dernier tier de l'image dans une liste
                liste3.append(randint(taille2,tailleimg))
            liste.extend(liste2)
            liste.extend(liste3)
            return liste
        indexX=créerindex(diffhauteur,taille[1]-1)
        indexY=créerindex(difflargeur,taille[0]-1)
        b=0
        d=0
        for i in range(0,taille[0]-1):
            if i not in indexY: #si i n'est pas une des largeurs à supprimer
                for j in range (0,taille[1]-1):
                    if j not in indexX: #si j n'est pas une des hauteurs à supprimer
                        a=photo.getpixel((i,j))
                        newImage.putpixel((b,d),a) #met le pixel dans la nouvelle image
                        if d!=hauteur-1: #si la hauteur de la nouvelle image n'est pas dépassée, augmente de 1
                            d=d+1
                if b !=largeur-1:#si la largeur  de la nouvelle image n'est pas dépassée, l'incrémente de 1
                    b=b+1
                d=0 #réinitialise la hauteur
    return newImage

def moyennepixel(liste):
    '''fonction qui renvoie la moyenne de 2 pixels. Prend en argument un tuple ou une liste'''
    moyenne=0
    for i in range(0,len(liste)):#parcours toute la liste
        moyenne=moyenne+liste[i]
    moyenne=int(moyenne/len(liste)+1)
    return moyenne

def savephoto():
    '''fonction qui enregistre la photo. Ne prends pas d'arguments'''
    nom=modif+name #ajoute le nom à la liste des modifications
    photo.save(nom)

def checkboxes():
    '''fonction qui montre des cases à cocher et boutons dans l'interface tkinter. Ne prends pas d'arguments '''
    def changementsimage():
        '''fonction qui vérifié si les boutons ont été cochés et applique les filtres sélectionnés. Ne prends pas d'arguments'''        
        global photo
        global modif
        if statusnegatif.get()==1: #vérifie si le bouton négatif est coché
            photo=negatif(photo)#éxécute la fonction
            modif=modif+'négatif' #ajoute négatif à une chaîne de caractère
            
        if statusNB.get()==1:
            seuilNB=int(entrerNB.get())
            photo=NetB(photo,seuilNB)
            modif=modif+'NetB'
        
        if statuscontour.get()==1:
            seuilContour=int(entrerContour.get())
            photo=contour(photo,seuilContour)
            modif=modif+'contour'
            
        if statusmiroir.get()==1:
            photo=miroir(photo)
            modif=modif+'miroir'
            
        if statusrouge.get()==1:
            photo=filtrergb(photo,0)
            modif=modif+'filtrerouge'
            
        
        if statusresize.get()==1:
            facteurresize=float(entrerfacteur.get())
            photo=resizing(photo,facteurresize)
            modif=modif+'resize'
        taillenew=photo.size
        
        if taillenew[0]>400: #si la largeur est supérieure à 400
            newlargeur=400
            newhauteur=int(newlargeur*taillenew[1]/taillenew[0]) #calcule la hauteur de l'image pour une largeur de 400
            photodisplay=photo.resize((newlargeur,newhauteur), PIL.Image.ANTIALIAS) #redimensionne l'image
            photoinTK=PIL.ImageTk.PhotoImage(photodisplay) #convertis pour tkinter
            cadreimage.configure(image=photoinTK)
            cadreimage.image=photoinTK #l'affiche dans le cadre
        else: #sinon affiche l'image dans le cadre
            newphotoinTK=PIL.ImageTk.PhotoImage(photo)
            cadreimage.configure(image=newphotoinTK)
            cadreimage.image=newphotoinTK
    
    cadreoptions=Frame(fenetre,width=100,height=70,borderwidth=2) #crée un cadre pour afficher les options
    cadreoptions.pack(side=RIGHT,expand=1)
    
    statusnegatif=IntVar()
    indication= Label(cadreoptions,text="Séléctionnez les options que vous souhaitez appliquer à l'image. Elles seront appliquées consécutivement") #explique le fonctionnement
    indication.pack(padx=20,pady=30) #espace le bouton
    negatifbutton= Checkbutton(cadreoptions,text='Négatif',variable=statusnegatif)#crée un bouton à cocher
    negatifbutton.pack(padx=5,pady=9,anchor='center',fill=X)#espace le bouton

    statusNB=IntVar()
    packNB= Frame(cadreoptions,width=60,height=60,borderwidth=2, relief="sunken")#crée un cadre pour contenir le bouton et le champ texte
    packNB.pack(padx=10,pady=20)
    NBbutton= Checkbutton(packNB,text='Noir Et Blanc',variable=statusNB)
    NBbutton.pack(padx=5,pady=4,anchor='center',fill=X)
    demandeNB= Label(packNB,text='Choix Du Seuil')
    demandeNB.pack(pady=3)
    entrerNB=Entry(packNB,width=10)#l'utilisateur rentre un seuil
    entrerNB.pack(pady=5)

    statuscontour=IntVar()
    packContour= Frame(cadreoptions,width=60,height=60,borderwidth=2, relief="sunken")
    packContour.pack(padx=10,pady=20)
    Contourbutton= Checkbutton(packContour,text='Contour',variable=statuscontour)
    Contourbutton.pack(padx=5,pady=4,anchor='center',fill=X)
    demandeContour= Label(packContour,text='Choix Du Seuil')
    demandeContour.pack(pady=3)
    entrerContour=Entry(packContour,width=10)
    entrerContour.pack(pady=5)
    
    statusmiroir=IntVar()
    miroirbutton= Checkbutton(cadreoptions,text='Miroir',variable=statusmiroir)
    miroirbutton.pack(padx=5,pady=9,anchor='center',fill=X)

    statusrouge=IntVar()
    rougebutton= Checkbutton(cadreoptions,text='Filtre rouge',variable=statusrouge)
    rougebutton.pack(padx=5,pady=9,anchor='center',fill=X)
    
    statusresize=IntVar()
    packderesize= Frame(cadreoptions,width=60,height=60,borderwidth=2, relief="sunken")
    packderesize.pack(padx=10,pady=20)
    resizebutton= Checkbutton(packderesize,text="Changement de taille (ne s'affiche pas dans l'apercu",variable=statusresize)
    resizebutton.pack(padx=5,pady=4,anchor='center',fill=X)
    demandefacteur= Label(packderesize,text='Facteur de redimensionnement')
    demandefacteur.pack(pady=3)
    entrerfacteur=Entry(packderesize,width=10)
    entrerfacteur.pack(pady=5)
    
    global modif
    modif='' #crée une chaîne de caractère qui contiendra l'ensemble des modifications

    boutonvalid= Button(cadreoptions,text="Valider",command=changementsimage) #lance le processus de modification
    boutonvalid.pack(pady=40,padx=20)

    boutonsave=Button(cadreoptions,text="Sauvegarder dans le dossier",command=savephoto) #sauvegarde la photo
    boutonsave.pack(pady=10,padx=20)

    
def displayimg(namebutton):
    '''fontion qui montre l'image sélectionnée dans une fênetre tkinter. Prends en argument un nom de bouton'''
    global cadreimage
    global name
    name=getEntry(namebutton)#obtiens le nom entré par l'utilisateur
    cadrenom.pack_forget()#cache le cadre pour rentrer le nom
    global photo
    photo= PIL.Image.open(name)#ouvre la photo
    global photoinTK
    photoinTK=PIL.ImageTk.PhotoImage(PIL.Image.open(name)) #convertis l'image pour l'afficher dans Tkinter
    taille=photo.size
    global cadreimage
    if taille[0]>400:#meme fonctionnement que dans changementsimage()
        newlargeur=400
        newhauteur=int(newlargeur*taille[1]/taille[0])
        photodisplay=photo.resize((newlargeur,newhauteur), PIL.Image.ANTIALIAS)
        photoinTK=PIL.ImageTk.PhotoImage(photodisplay)
        cadreimage=Label(fenetre,image=photoinTK)
    else:
        cadreimage=Label(fenetre,image=photoinTK) #crée une fenetre pour récuperer l'image
    cadreimage.pack(side=LEFT, fill='both',expand="yes")
    checkboxes()

def getEntry(var):
    """obtiens le résultat de l'Entry et le retourne sous forme de chaîne de caractères. Prends en argument un nom de variable"""
    name= var.get()
    return str(name)

    
fenetre= Tk()
fenetre.title('Photoshop Maison')

def askname():
    '''fonction qui demande le nom de l'image grâce à une ihm. Pas d'arguments'''
    #créer un cadre pour demander le nom de l'image
    global cadrenom
    cadrenom=Frame(fenetre,width=90,height=70,borderwidth=1)
    cadrenom.pack(side=LEFT)

    #demander le nom du fichier
    name_label=Label(cadrenom,text="Saissisez le nom de votre image contenue dans le dossier avec l'extension")
    name_label.pack()
    select_photo= Entry(cadrenom,width=30) #l'utilisateur écrit
    select_photo.pack()
    select_photo.focus_set()
    valider_name=Button(cadrenom,text="Valider",command=partial(displayimg,select_photo))#l'utilisateur valide ce qu'il a écrit
    valider_name.pack()


askname() #demande le nom de l'image. Première étape de l'IHM
fenetre.mainloop()#ne lis plus les lignes suivantes et lance l'IHM
    