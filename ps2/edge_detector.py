from typing import Tuple

import cv2 as cv
import numpy as np
from ps2.ps2_exceptions import ReadImageError

# Constantes
G_MAX = 255


class EdgeDetector:
    """Classe que implementa o detector de bordas.
    """

    def __init__(self, path_image: str, image_name: str, window_length: int, window_step: int):
        """Construtor.
        """
        self._image_path = path_image
        try:
            self._image = self._read_image()
        except ReadImageError:
            print('Erro ao ler a imagem !!')
            self._image = None
        self._image_name = image_name
        self._window_length = window_length
        self._window_step = window_step

    def _read_image(self) -> np.array:
        """Realiza a leitura da imagem.

        Returns: None
        """
        image = cv.imread(self._image_path, cv.IMREAD_GRAYSCALE)

        # verificando o carregamento da imagem e retornando o erro
        if image is None:
            raise ReadImageError(self._image_path)
        else:
            return image

    def _sliding_window(self) -> Tuple[int, int, np.ndarray]:
        """Método que cria janelas de uma determinada imagem percorrendo a mesma.

        Returns: x, y e a janela.
        """
        for y in range(0, self._image.shape[0], self._window_step):
            for x in range(0, self._image.shape[1], self._window_step):
                yield x, y, self._image[y:y + self._window_length, x:x + self._window_length]

    def _sliding_window_image(self, image: np.ndarray) -> Tuple[int, int, np.ndarray]:
        """Método que itera por uma imagem criando janelas de cada parte da imagem.

        Args:
            image: Imagem base.

        Returns: x, y e a janela.
        """
        for y in range(0, image.shape[0], self._window_step):
            for x in range(0, image.shape[1], self._window_step):
                yield x, y, image[y:y + self._window_length, x:x + self._window_length]
