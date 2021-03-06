from typing import Tuple

import math
import cv2 as cv
import numpy as np
from ps2_exceptions import ReadImageError


# Constantes
G_MAX = 255


class SigmaFilter:
    """Classe que implementa o filtro Sigma gerando uma nova imagem.
    """

    def __init__(self, path_of_image_i: str, image_name: str, window_length: int, window_step: int):
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

    def _apply_sigma_filter(self) -> np.ndarray:
        """Executa a aplicação do filtro sigma na imagem passada como parâmetro.

        Returns: Imagem (J) com o filtro aplicado.
        """
        image_j: np.ndarray = np.zeros(self._image.shape, dtype=np.uint8())
        image_windows = self._sliding_window()

        # iterando e montando a nova imagem
        for window in image_windows:
            # p(x), p(y) e a janela em si
            p_x, p_y, window = window
            # obtendo o histograma da janela
            window_hist = SigmaFilter._calc_histogram_of_window(window)
            sigma = int(window.std())
            # calculando os limites
            upper_limit = self._image[p_x][p_y] + sigma
            inferior_limit = self._image[p_x][p_y] - sigma
            # ajustando os limites
            upper_limit = G_MAX if upper_limit > G_MAX else upper_limit
            inferior_limit = 0 if inferior_limit < 0 else inferior_limit
            # calculando a média
            sum_u_h_u = 0
            s = 0
            for u in range(inferior_limit, upper_limit + 1):
                sum_u_h_u += u * window_hist[u]
                s += window_hist[u]
            image_j[p_x][p_y] = int(sum_u_h_u / s) if s != 0 else 0
        return image_j

    def _histogram_equalization(self) -> np.ndarray:
        """Realiza a equalização do histograma.

        Returns: Imagem após a equalização do histograma.
        """
        image_to_equalize = self._image
        image_g = np.zeros(image_to_equalize.shape, dtype=np.uint8())
        histogram_to_equalize = SigmaFilter._calc_histogram_of_window(image_to_equalize)
        cardinality = image_to_equalize.shape[0] * image_to_equalize.shape[1]
        relative_frequencies = np.divide(histogram_to_equalize, cardinality)
        r = 1

        # iterando sobre a imagem
        for x, line in enumerate(image_to_equalize):
            print(f'Linha {x}')
            for y, column in enumerate(line):
                pixel_u = column
                g_equal_u = SigmaFilter._g_equal(relative_frequencies, pixel_u, r)
                image_g[x][y] = g_equal_u
        return image_g

    # Interfaces dos métodos
    def show_image(self) -> None:
        self._show_image()

    def calc_histogram(self) -> np.ndarray:
        return self._calc_histogram()

    def histogram_equalization(self) -> np.ndarray:
        return self._histogram_equalization()

    # Métodos estáticos
    @staticmethod
    def _calc_histogram_of_window(window: np.ndarray) -> np.ndarray:
        """Calcula o histograma da janela passada como parâmetro.

        Args:
            window: Janela desejada.

        Returns: Histograma da janela.
        """
        return cv.calcHist([window], [0], None, [256], [0, 256])

    @staticmethod
    def _q(relative_frequencies: np.array, r: float) -> float:
        """Calcula a função Q.

        Args:
            relative_frequencies: Vetor de frequências relativas.
            r: Escalar de ajuste.

        Returns: Resultado do somatório.
        """
        sum_q = 0
        for index in range(0, G_MAX+1):
            sum_q += math.pow(relative_frequencies[index], r)
        return sum_q

    @staticmethod
    def _g_equal(relative_frequencies: np.array, u: int, r: float) -> float:
        """Realiza a operação de cálculo da normalização.

        Args:
            relative_frequencies: Frequências relativas.
            u: Valor do pixel.
            r: Escalar de ajuste.

        Returns: Escalar resultante da operação.
        """
        sum_g_equal = 0
        for index in range(0, u+1):
            scalar = G_MAX / SigmaFilter._q(relative_frequencies, r)
            sum_g_equal += (scalar * math.pow(relative_frequencies[index], r))
        return sum_g_equal
