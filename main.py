from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import joblib
import pandas as pd
import numpy as np
from skimage import io
import sklearn.tree
from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy

def capture():
    global camimg
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('camera feed', cv2.WINDOW_NORMAL)
    width = cam.set(3, 1280)
    height = cam.set(4, 720)
    print(width, height)

    while True:
        ret, camimg = cam.read()
        resimg=cv2.resize(camimg,(250,200))
        cv2.imshow('camera feed', resimg)
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            break
        elif k % 256 == 32:
            #SPACE pressed
            file = filedialog.asksaveasfilename(filetypes=[("png file", ".png")], defaultextension='.png',title='Save image as')
            if file:
                cv2.imwrite(file,camimg) #save image in directory
            #convert cv img to pil img
            cv2image=cv2.cvtColor(resimg, cv2.COLOR_BGR2RGB)
            img= Image.fromarray(cv2image)
            #convert img to photoimg
            imgtk=ImageTk.PhotoImage(image=img)
            #display img on label
            pic.imgtk=imgtk
            pic.config(image=imgtk)
            break
    cam.release()
    cv2.destroyAllWindows()
    return camimg

def segment(image):
    # Load the image
    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of colors to threshold
    lower_color = (0, 30, 0)
    upper_color = (255, 255, 255)

    # Threshold the image to only select the desired colors
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Perform a bitwise AND on the image to apply the mask
    result = cv2.bitwise_and(image, image, mask=mask)

    return mask, result

def morph(image):

    #Find contours
    contours, _ = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Select largest contour
    cnt = max(contours, key = cv2.contourArea)
    
    # Calculate compactness
    perimeter = cv2.arcLength(cnt, True)
    area = cv2.contourArea(cnt)
    compactness = (perimeter ** 2) / area
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    solidity = area / hull_area

    return perimeter, compactness, solidity

def tex(image):
    gimg=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    # Calculate grey-level co-occurrence matrix (GLCM)
    glcm = graycomatrix(gimg, [1], [0], 256, symmetric=True, normed=True)
    
    # Calculate texture features
    correlation = graycoprops(glcm, 'correlation')[0, 0]
    entropy=shannon_entropy(glcm)
    return correlation, entropy

def clr(image):
    (b, g, r) = cv2.split(image)

    nb=np.nonzero(b)
    ng=np.nonzero(g)
    nr=np.nonzero(r)

    avg_b = np.average(nb)
    avg_g = np.average(ng)
    avg_r = np.average(nr)

    return avg_r, avg_g, avg_b  



def classify():

    clf = joblib.load("Lettuce_model.joblib")

    image=camimg
    tst=pd.DataFrame(columns=['perimeter','compactness', 
            'solidity','correlation', 'entropy', 'r','g', 'b'])

    binary, segImg=segment(image)
    per, com, sol=morph(binary)
    cor,ent=tex(segImg)
    r,g,b=clr(segImg)
    tst = tst.append({'perimeter': per,'compactness':com, 'solidity':sol,
            'correlation':cor, 'entropy':ent, 'r':r,'g':g, 'b':b}, ignore_index=True)

    ftrCols=['perimeter','compactness', 
            'solidity','correlation', 'entropy', 'r','g', 'b']
    Xx=tst[ftrCols]

    yy_pred = clf.predict(Xx)
    clas=(yy_pred[0])
    print(clas)
    classlabel.config(text=clas)
    

if __name__ == '__main__':


    root = Tk()
    root.title('Lettuce Seed Variety Classifier')
    root.geometry("400x250")
    root.configure(bg='#70CAD1')

    photo = PhotoImage(file = "letic.png")
    root.iconphoto(False, photo)
    imge = ImageTk.PhotoImage(Image.open("samplet.jpg"))
    pic = Label(root, image=imge)
    pic.grid(row=0, column=2, pady=2)

    classlabel = Label(root, text='')
    classlabel.grid(row=1, column=2, ipadx=20)
    clase = Label(root, text="Seed Variety", bg="#70CAD1")
    clase.grid(row=2, column=2, pady=2)

    cap = Button(root, text="CAPTURE", bg="#C4CBCA", command=capture )
    cap.grid(row=0, column=0, pady=5,padx=1)
    det = Button(root, text="CLASSIFY", bg="#C4CBCA", command=classify)
    det.grid(row=0, column=1, pady=5,padx=2)
    



    root.mainloop()