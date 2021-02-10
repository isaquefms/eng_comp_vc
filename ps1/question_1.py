import cv2 as cv
import sys
from matplotlib import pyplot as plt

drawing = False
point = (0, 0)


def step_1() -> None:
    """Carrega uma imagem e a exibe.

    Returns: None.
    """
    img = cv.imread('../imgs/lenna.png', )
    # verificando o carregamento da imagem
    if img is None:
        sys.exit("Não foi possível abrir a imagem")

    # exibindo a mensagem
    cv.imshow('Exemplo', img)
    key = cv.waitKey(0)

    if key == ord('s'):
        cv.imread('../imgs/lenna.png')


def step_2() -> None:
    """Calculando o histograma.

    Returns: None.
    """
    img = cv.imread('../imgs/lenna.png')
    colors = ('b', 'g', 'r')
    for i, col in enumerate(colors):
        hist = cv.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist, color=col)
        plt.xlim([0, 256])
    plt.title('Histogramas')
    plt.show()


def step_3() -> None:
    """Obtendo dados da imagem em tempo real.

    Returns: None.
    """
    img = cv.imread('../imgs/lenna.png')

    # função de intensidade
    def intensity(red: int, green: int, blue: int) -> float:
        """Calcula a intensidade de um pixel.

        Args:
            red: Escala de vermelho.
            green: Escala de verde.
            blue: Escala de azul.

        Returns: Intensidade do pixel
        """
        return round(sum([red, green, blue])/3, 2)

    # callback
    def mouse_drawing(event, x, y, flags, params) -> None:
        global point, drawing
        if event == cv.EVENT_MOUSEMOVE:
            drawing = True
            point = (x, y)

    cv.namedWindow('Rectangle')
    cv.setMouseCallback('Rectangle', mouse_drawing)

    while True:
        frame = img  # nova referência ao objeto da imagem
        x = point[0]  # x do mouse
        y = point[1]  # y do mouse
        x_initial = x - 13
        y_initial = y - 13
        x_final = x + 13
        y_final = y + 13
        rect = frame[x_initial: y_initial+1, y_final: y_final + 1]  # retângulo
        b = img[y, x, 0]  # obtendo o valor da escala blue do pixel
        g = img[y, x, 1]  # obtendo o valor da escala verde do pixel
        r = img[y, x, 2]  # obtendo o valor da escala vermelha do pixel
        # caso o evento tenha ocorrido
        if drawing:
            # desenhamos o retângulo e exibimos as informações
            cv.rectangle(frame, (x_initial, y_initial), (x_final, y_final), (0, 255, 0), 0)
            print(f'Cursor at: {x, y}. RGB values: R: {r}, G: {g} and B: {b}. Intensity: {intensity(r, g, b)}')
            print(f'Average gray level: {rect.mean()}, Std Deviation: {rect.std()}')

        cv.imshow('Rectangle', frame)
        key = cv.waitKey(25)
        if drawing:
            img = cv.imread('../imgs/lenna.png')
        if key == 13:
            print('Terminado')
        elif key == 27:
            break

    cv.destroyAllWindows()


def step_4() -> None:
    """Discussão sobre os resultados anteriores.

    Returns: None.
    """
    discuss = 'Given the above exercises we tried defining the homogeneousity in terms of histograms and variances.' \
              ' Using the histograms we should observe that homogeneousity is related with the constant distribution ' \
              'in all frequencies of the graph.' \
              '' \
              'Using the standard deviation we should observe that homogeneousity is closely related with low values ' \
              'of variance. That represents that in mean the value is close to the average.'
    print(discuss)


step_4()
