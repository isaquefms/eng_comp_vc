from typing import Tuple

import cv2 as cv
import numpy as np

from ps2_exceptions import ReadImageError


class BaseImageOperations:
    """Classe que implementa as operações básicas em imagens.
    """

    def __init__(self, path_of_image_i: str, image_name: str, window_length: int = 3, window_step: int = 1):
        """Construtor.
        """
        self._image_path = path_of_image_i
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

    def _show_image(self) -> None:
        """Método para exibir a imagem selecionada.

        Returns: None.
        """
        # exibindo a imagem
        cv.imshow(self._image_name, self._image)
        key = cv.waitKey(0)

        if key == ord('s'):
            cv.imread(self._image_path)

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

    def _calc_histogram(self) -> np.ndarray:
        """Calcula o histograma da imagem carregada em tons de cinza.

        Returns: Histograma da imagem. Único canal.
        """
        return cv.calcHist([self._image], [0], None, [256], [0, 256])

    # Interfaces dos métodos
    def show_image(self) -> None:
        self._show_image()

    def calc_histogram(self) -> np.ndarray:
        return self._calc_histogram()

    # Métodos estáticos
    @staticmethod
    def _calc_histogram_of_window(window: np.ndarray) -> np.ndarray:
        """Calcula o histograma da janela passada como parâmetro.

        Args:
            window: Janela desejada.

        Returns: Histograma da janela.
        """
        return cv.calcHist([window], [0], None, [256], [0, 256])
