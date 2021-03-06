import sys
import numpy as np
from typing import List, Tuple

import cv2 as cv


def step_1() -> None:
    """Passo A da questão 4.

    Returns: None.
    """
    img = cv.imread('../imgs/lenna.png')
    # verificando o carregamento da imagem
    if img is None:
        sys.exit("Não foi possível abrir a imagem")

    h = img.shape[0]
    w = img.shape[1]

    for y in range(0, h):
        for x in range(0, w):
            img[x, y] = 120

    cv.imshow('Teste', img)
    key = cv.waitKey(250)

    if key == ord('s'):
        cv.imread('../imgs/lenna.png')


step_1()