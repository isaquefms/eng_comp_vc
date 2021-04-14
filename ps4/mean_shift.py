import cv2 as cv
import numpy as np


class MeanShift:
    """Classe para teste do algoritmo de MeanShift.
    """

    def __init__(self, image_path: str):
        # carregando a imagem
        self._image = cv.imread(image_path)
        if self._image is None:
            print('Cannot load the image')
        self._shifted_image = self._image.copy()

    def _display_original_image(self) -> None:
        """Função para exibição da imagem original.

        Returns: None.
        """
        cv.imshow('Original Image', self._image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def _display_mean_shifted_image(self) -> None:
        cv.imshow('Shifted Image', self._shifted_image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def _mean_shift(self) -> None:
        """Compara os resultados do algoritmo MeanShift.

        Returns: None.
        """
        term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
        cv.pyrMeanShiftFiltering(self._image, 25, 25, self._shifted_image, 1, termcrit=term_crit)
        h, w = self._shifted_image.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        cv.floodFill(self._shifted_image, mask, (0, 0), 255)
        # self._display_original_image()
        self._display_mean_shifted_image()

    def mean_shift(self) -> None:
        self._mean_shift()
