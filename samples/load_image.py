import cv2 as cv
import sys

# carregando a imagem dos exemplos do opencv
img = cv.imread("/home/isaque/Pictures/exemplo.png")

# verificando o carregamento da imagem
if img is None:
    sys.exit("Não foi possível carregar a imagem.")

cv.imshow("Janela de visualização", img)
key = cv.waitKey(0)

if key == ord("s"):
    cv.imwrite("/home/isaque/Pictures/exemplo.png", img)
