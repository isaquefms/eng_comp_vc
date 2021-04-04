import cv2 as cv
import numpy as np

from base import BaseImageOperations

# Constantes
G_MAX = 255


class LocalFT(BaseImageOperations):
    """Classe que implementa os operadores locais.
    """

    def _apply_local_operators(self) -> None:
        """Algoritmo para a aplicação dos operadores locais.

        Returns: None.
        """
        m_image = np.zeros(self._image.shape, dtype=np.uint8())
        p_image = np.zeros(self._image.shape, dtype=np.uint8())

        # iterando sobre as janelas da imagem
        windows = self._sliding_window()
        for window in windows:
            x, y, ins_window = window
            print(x*y)
            window_ft = LocalFT._get_image_in_frequency_domain(ins_window)
            amplitude, phase = 0, 0
            window_ft_shape = window_ft.shape
            pos_x = window_ft_shape[0] // 2
            pos_y = window_ft_shape[1] // 2
            # obtendo a parte complexa e real
            value = str(window_ft[pos_x][pos_y])
            if '+' in value:
                amplitude, phase = value.split('+')
            elif '-' in value:
                amplitude, phase = value.split('-')
            # montando as imagens resultantes
            m_image[y][x] = np.uint8(amplitude.replace('(', ''))
            p_image[y][x] = np.uint8(abs(complex(phase.replace(')', ''))))
        cv.imshow('Amplitude Window', m_image)
        cv.imshow('Phase Window', p_image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def _show_edges(self, low_treshold: int, high_treshold: int) -> None:
        """Exibindo as bordas da imagem tomando como base o método Canny.

        Returns: None.
        """
        image_canny = cv.Canny(self._image, low_treshold, high_treshold)
        cv.imshow('Image Canny', image_canny)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def show_edges(self, low_theshold: int, high_treshold: int) -> None:
        self._show_edges(low_theshold, high_treshold)

    def apply_local_operators(self) -> None:
        self._apply_local_operators()

    # Static Methods
    @staticmethod
    def _get_image_in_frequency_domain(image, dp_shifted: bool = True) -> np.ndarray:
        """ Método estático que realiza a transformação de uma imagem para o domínio da frequência.

        Args:
            image: Imagem original.
            dp_shifted: Flag para alterar o centro da imagem.

        Returns:
        """
        frequency_img = np.fft.fft2(image)
        if dp_shifted:
            frequency_img = np.fft.fftshift(frequency_img)
        return frequency_img
