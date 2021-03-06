from sigma_filter import SigmaFilter
import cv2 as cv

# Constantes
IMAGE_PATH = '../imgs/noisy_lenna.jpg'
IMAGE_NAME = 'Lenna'
IMAGE_WINDOW_LENGTH = 3
IMAGE_WINDOW_STEP = 1


def main():
    """Função que dá início a execução.
    """
    sigma_filter = SigmaFilter(IMAGE_PATH, IMAGE_NAME, IMAGE_WINDOW_LENGTH, IMAGE_WINDOW_STEP)
    image_j = sigma_filter.histogram_equalization()

    # exibindo a mensagem
    cv.imshow('Exemplo', image_j)
    key = cv.waitKey(0)

    if key == ord('s'):
        cv.imread('../imgs/noisy_lenna.jpg')


main()
