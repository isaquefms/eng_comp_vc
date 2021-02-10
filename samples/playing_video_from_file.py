import numpy as np
import cv2 as cv

# carregando o vídeo
cap = cv.VideoCapture("Nome_video.avi")

while cap.isOpened():
    ret, frame = cap.read()

    # se o frame estiver correto retorna True
    if not ret:
        print("Saindo ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
