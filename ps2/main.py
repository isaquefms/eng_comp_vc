from local_ft import LocalFT
from sigma_filter import SigmaFilter
import cv2 as cv

# Constantes
IMAGE_PATH = '../imgs/noisy_lenna.jpg'
IMAGE_PATH_2 = '../imgs/lenna.png'
IMAGE_NAME = 'Lenna'
IMAGE_WINDOW_LENGTH = 3
IMAGE_WINDOW_STEP = 1


def main():
    """Função que dá início a execução.
    """
    # Atividade 1
    # sigma_filter = SigmaFilter(IMAGE_PATH, IMAGE_NAME, IMAGE_WINDOW_LENGTH, IMAGE_WINDOW_STEP)
    # image_j = sigma_filter.histogram_equalization()
    #
    # # exibindo a mensagem
    # cv.imshow('Exemplo', image_j)
    # key = cv.waitKey(0)
    #
    # if key == ord('s'):
    #     cv.imread('../imgs/noisy_lenna.jpg')
    # Atividade 3
    local_ft = LocalFT(IMAGE_PATH_2, IMAGE_NAME, IMAGE_WINDOW_LENGTH, IMAGE_WINDOW_STEP)
    # local_ft.apply_local_operators()
    local_ft.show_edges(40, 120)


main()
