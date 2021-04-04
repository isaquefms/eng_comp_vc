import math
import numpy as np

from base import BaseImageOperations


# Constantes
G_MAX = 255


class SigmaFilter(BaseImageOperations):
    """Classe que implementa o filtro Sigma gerando uma nova imagem.
    """

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

    def histogram_equalization(self) -> np.ndarray:
        return self._histogram_equalization()

    @staticmethod
    def _q(relative_frequencies: np.array, r: float) -> float:
        """Calcula a função Q.

        Args:
            relative_frequencies: Vetor de frequências relativas.
            r: Escalar de ajuste.

        Returns: Resultado do somatório.
        """
        return sum(
            math.pow(relative_frequencies[index], r) for index in range(G_MAX + 1)
        )

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
        for index in range(u+1):
            scalar = G_MAX / SigmaFilter._q(relative_frequencies, r)
            sum_g_equal += (scalar * math.pow(relative_frequencies[index], r))
        return sum_g_equal
