from typing import Tuple

import cv2 as cv
import numpy as np

from exceptions import ReadImageError


# Constantes
G_MAX = 255


class BaseImageOperations:
    """Classe que implementa as operações básicas em imagens.
    """

    def __init__(self, path_of_image_i: str, image_name: str, window_length: int = 3, window_step: int = 1,
                 threshold: int = 125):
        """Construtor.
        """
        self._image_path = path_of_image_i
        try:
            self._image = self._read_image()
        except ReadImageError:
            print('Erro ao ler a imagem !!')
            self._image = None
        self._image_name = image_name
        self._binary_image = self._thresholding_operation(threshold)
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

    def _show_binary_image(self) -> None:
        """Exibe a imagem binária.

        Returns: None.
        """
        cv.imshow(f'{self._image_name} binary', self._binary_image)
        key = cv.waitKey(0)

        if key == ord("s"):
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

    def _thresholding_operation(self, threshold: int = 100) -> np.ndarray:
        """Cria a imagem binária da imagem base.

        Args:
            threshold: Limiar para definir se a imagem vai assumir o valor 0 ou 1.

        Returns: Imagem binária resultante.
        """
        img_j = np.zeros(self._image.shape, dtype=np.uint8())
        for i, x in enumerate(self._image):
            for j, y in enumerate(x):
                img_j[i][j] = G_MAX if self._image[i][j] < threshold else 0
        return img_j

    # Interfaces dos métodos
    def show_image(self) -> None:
        self._show_image()

    def show_binary_image(self) -> None:
        self._show_binary_image()

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
