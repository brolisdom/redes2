import cv2
import numpy as np
import threading

images = {} # variable global (diccionario)

'''
Funcion para obtener una imagen en el color indicado

Recibe:
    - el color que se quiere obtener
    - la imagen que se va a modificar

Devuelve:
    - nada

Notas:
    - la imagen resultante se almacena en la variable global
    - las imagenes del mismo color se combinaran verticalmente
'''
def img_rgb(color, img):
    if color == 'red': img[:,:,0] = img[:,:,1] = 0
    if color == 'blue': img[:,:,1] = img[:,:,2] = 0
    if color == 'green': img[:,:,0] = img[:,:,2] = 0
    if not color in images: images[color] = img
    else: images[color] = cv2.vconcat([images[color], img])

'''
Programa para obtener los colores R-G-B de una imagen:
R => Rojo
G => Verde
B => Blue

Restricciones:
    - solo se permite utilizar 2 hilos
    - el color verde se debe obtener en conjunto de ambos hilos
'''
if __name__ == "__main__":
    img = cv2.imread('image.jpg')

    img_r = img.copy()
    thread_1 = threading.Thread(target=img_rgb, args=('red', img_r))
    thread_1.start()

    img_b = img.copy()
    thread_2 = threading.Thread(target=img_rgb, args=('blue', img_b))
    thread_2.start()
    
    thread_1.join()
    thread_2.join()

    img_g1 = img.copy()[:len(img)//2] # primera mitad vertical
    thread_1 = threading.Thread(target=img_rgb, args=('green', img_g1))
    thread_1.start()

    img_g2 = img.copy()[len(img)//2:] # segunda mitad vertical
    thread_2 = threading.Thread(target=img_rgb, args=('green', img_g2))
    thread_2.start()
    
    thread_1.join()
    thread_2.join()

    for color in images: 
        cv2.imwrite("./images/"+color+".jpg", images[color])
