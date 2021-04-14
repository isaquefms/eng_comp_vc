import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class HornSchunck:
    """Classe para implementações básicas de manipulações em vídeos.
    """

    # mascaras utilizadas para calcular a velocidade entre os pixels
    MASK_U_X = np.array([-1, 1, -1, 1]).reshape((2, 2))
    MASK_V_Y = np.array([-1, -1, 1, 1]).reshape((2, 2))
    # MASK_V_Y = np.array([1, 1, -1, -1]).reshape((2, 2))
    MASK_T = np.array([-1, -1, -1, -1]).reshape((2, 2))
    # mascara do laplaciano
    LAPLACIAN_MASK = np.array([1/12, 1/6, 1/12, 1/6, 0, 1/6, 1/12, 1/6, 1/12]).reshape((3, 3))

    def __init__(self, video_path: str, lambda_factor: float, max_iter: int):
        # fatores do algoritmo
        self._lambda_factor = lambda_factor
        self._max_iter = max_iter
        # capturando dois frames do vídeo e convertendo os mesmos para escalas de cinza
        self._video_captured = cv.VideoCapture(video_path)
        ret, self._first_image = self._video_captured.read()
        ret, self._second_image = self._video_captured.read()
        self._base_image = self._first_image
        self._first_image = cv.cvtColor(self._first_image, cv.COLOR_BGR2GRAY)
        self._second_image = cv.cvtColor(self._second_image, cv.COLOR_BGR2GRAY)
        # matriz de velocidades iniciada com zero
        self._u = np.zeros(self._first_image.shape)
        self._v = np.zeros(self._second_image.shape)

    def _horn_schunck(self):
        """Implementação do algoritmo de Horn and Schunck.

        Returns: None.
        """
        # variáveis utilizadas nas iterações
        u = np.zeros(self._first_image.shape)
        v = np.zeros(self._first_image.shape)
        u_1 = np.zeros(self._first_image.shape)
        v_1 = np.zeros(self._first_image.shape)
        f_x = np.zeros(self._first_image.shape)
        f_y = np.zeros(self._first_image.shape)
        f_t = np.zeros(self._first_image.shape)
        dim_x = self._first_image.shape[1] - 1
        dim_y = self._first_image.shape[0] - 1
        # iterando sobre os pixels para calcular f_x, f_y e f_t
        for y, lines in enumerate(self._first_image):
            for x, pixel in enumerate(lines):
                # evita obtenção de janelas na borda direita e inferior
                if y >= (dim_y - 1) or x >= (dim_x - 1):
                    continue
                # janela das imagens no tempo t e dt
                positions_1 = np.array([self._first_image[y][x], self._first_image[y][x+1], self._first_image[y+1][x],
                                        self._first_image[y+1][x+1]]).reshape((2, 2))
                positions_2 = np.array([self._second_image[y][x], self._second_image[y][x+1],
                                        self._second_image[y+1][x], self._second_image[y+1][x+1]]).reshape((2, 2))
                # cálculo das velocidades de x e y
                f_x[y][x] = 0.5 * sum(sum(np.multiply(positions_1, self.MASK_U_X))) + sum(sum(
                    np.multiply(positions_2, self.MASK_U_X)))
                f_y[y][x] = 0.5 * sum(sum(np.multiply(positions_1, self.MASK_V_Y))) + sum(sum(
                    np.multiply(positions_2, self.MASK_V_Y)))
                f_t[y][x] = sum(sum(positions_2 - positions_1))
        # calculando o vetor u e v
        for i in range(self._max_iter):
            print(f'Iteration: {i + 1}')
            for y, lines in enumerate(self._first_image):
                for x, pixel in enumerate(lines):
                    if y >= (dim_y - 3) or x >= (dim_x - 3):
                        continue
                    window_u = np.array([u[y-1][x-1], u[y-1][x], u[y-1][x+1], u[y][x-1], u[y][x], u[y][x+1],
                                         u[y+1][x-1], u[y+1][x], u[y+1][x+1]]).reshape((3, 3))
                    window_v = np.array([v[y-1][x-1], v[y-1][x], v[y-1][x+1], v[y][x-1], v[y][x],
                                         v[y][x+1], v[y+1][x-1], v[y+1][x], v[y+1][x+1]]).reshape((3, 3))
                    uav = sum(sum(np.multiply(window_u, self.LAPLACIAN_MASK)))
                    vav = sum(sum(np.multiply(window_v, self.LAPLACIAN_MASK)))
                    p = f_x[y][x]*uav + f_y[y][x]*vav + f_t[y][x]
                    d = self._lambda_factor + f_x[y][x]**2 + f_y[y][x]**2
                    u_1[y][x] = uav - (f_x[y][x]*(p/d))
                    v_1[y][x] = vav - (f_y[y][x]*(p/d))
            print(f'Mean of changes in U: {(sum(sum(u_1)) - sum(sum(u)))/2}')
            print(f'Mean of changes in V: {(sum(sum(v_1)) - sum(sum(v)))/2}')
            u = u_1
            v = v_1
        self._u = u
        self._v = v
        HornSchunck._show_image(self._u, 'Vetor U')
        HornSchunck._show_image(self._v, 'Vetor V')
        # self._show_image_hsv(self._u, self._v, 'HSV Image')

    def _show_velocities(self) -> None:
        """Exibe o gráfico das velocidades calculando os vetores tendo como base cada pixel.

        Returns: None
        """
        x = np.arange(0, self._first_image.shape[1], 1)
        y = np.arange(0, self._first_image.shape[0], 1)
        u = self._u
        v = self._v

        fig, ax = plt.subplots()
        q = ax.quiver(x, y, u, v)
        ax.quiverkey(q, X=0.5, Y=1.1, U=1, label='Velocidade', labelpos='E')
        plt.show()

    def _show_image_hsv(self, u: np.ndarray, v: np.ndarray, image_name: str) -> None:
        hsv = np.zeros_like(self._base_image)
        hsv[..., 1] = 255
        mag, ang = cv.cartToPolar(u, v)
        hsv[..., 0] = (ang * 180 / np.pi / 2)
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2RGB)
        cv.imshow(image_name, bgr)
        k = cv.waitKey(0)
        if k == 27:
            cv.destroyAllWindows()

    def horn_schunck(self):
        self._horn_schunck()

    def show_velocities(self):
        self._show_velocities()

    @staticmethod
    def _show_image(image: np.ndarray, image_name: str) -> None:
        """Método para exibir a imagem selecionada.

        Returns: None.
        """
        # exibindo a imagem
        cv.imshow(image_name, image)
        key = cv.waitKey(0)

        if key == ord('s'):
            cv.destroyAllWindows()


