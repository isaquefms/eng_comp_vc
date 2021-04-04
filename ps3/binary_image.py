from typing import Set, List, Tuple

from base import BaseImageOperations

import cv2 as cv

# variáveis globais
clicked_pixel = None


def mouse_callback(event, x, y, flags, params):
    global clicked_pixel
    if event == cv.EVENT_LBUTTONDBLCLK:
        clicked_pixel = (x, y)


class BinaryImage(BaseImageOperations):
    """Classe para a implementação da formulation 1 do ps3.
    """

    # Constantes
    EIGHT_ADJACENCY = 8
    FOUR_ADJACENCY = 4
    G_MAX = 255
    BLACK = 0
    WHITE = G_MAX

    def __init__(self, path_of_image_i: str, image_name: str, threshold: int = 125):
        """Construtor.

        Args:
            path_of_image_i: Path da imagem utilizada como base para operações.
            image_name: Nome da imagem.
            threshold: Limiar para geração da imagem binária.
        """
        super().__init__(path_of_image_i, image_name, threshold=threshold)

    def _execute_flow(self) -> None:
        """Executa o fluxo de processamento.

        Returns: None.
        """
        while True:
            option = input('Select one option:\n(1) Counting Components \n'
                           '(2) Geometric Features of a Selected Component \n'
                           '(3) Exit \n'
                           'Enter the option -> ')

            if option == '1':
                adjacency = input('Select the adjacency:\n(1) Eight \n(2) Four \nEnter the value: ')
                if adjacency not in ['1', '2']:
                    print('Invalid option\n\n')
                    continue
                elif adjacency == '1':
                    components = self._counting_components(self.EIGHT_ADJACENCY)
                else:
                    components = self._counting_components(self.FOUR_ADJACENCY)
                print(f'Number of components: {components}\n\n')

            elif option == "2":
                # cadastrando a callback do mouse para a janela
                cv.namedWindow(f'{self._image_name} binary', cv.WINDOW_NORMAL)
                cv.setMouseCallback(f'{self._image_name} binary', mouse_callback)
                self._show_binary_image()
                perimeter, area, diameter = self._mensure_geometric_features(clicked_pixel[0],
                                                                             clicked_pixel[1])
                print(f'Perimeter: {perimeter}, area: {area} e diameter: {diameter}\n\n')

            elif option == "3":
                print('Abort')
                break

            else:
                print('Invalid option')

    def _get_eight_adjacency(self, x: int, y: int) -> List[tuple]:
        """Monta o vetor da adjacência de 8 para um determinado pixel.

        Args:
            x: Valor x do pixel.
            y: Valor y do pixel.

        Returns: Coordenadas dos pixels adjacentes.
        """
        adjacency = [(x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1), (x, y-1), (x+1, y-1)]
        # retornamos apenas elementos não negativos e com tamanho menor que o máximo possível
        return [(x, y) for x, y in adjacency if 0 <= x < self._binary_image.shape[0]
                and 0 <= y < self._binary_image.shape[1]]

    def _get_four_adjacency(self, x: int, y: int) -> List[tuple]:
        """Monta o vetor da adjacência de 4 para um determinado pixel.

        Args:
            x: Valor x do pixel.
            y: Valor y do pixel.

        Returns: Coordenadas dos pixels adjacentes.
        """
        adjacency = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
        return [(x, y) for x, y in adjacency if 0 <= x < self._binary_image.shape[0]
                and 0 <= y < self._binary_image.shape[1]]

    def _counting_components(self, adjacency: int = EIGHT_ADJACENCY) -> int:
        """Conta o componentes na imagem utilizando a adjacência de 4 ou de 8.

        Args:
            adjacency: Adjacência utilizada.

        Returns: Número de componentes na imagem.
        """
        visited_pixels: Set[tuple] = set()
        actual_pixel: List[int] = [0, 0]
        regions: int = 0

        for y, line in enumerate(self._binary_image):
            for x, pixel in enumerate(line):
                # a procura por uma região se inicia ao se encontrar um pixel preto não visitado
                if self._binary_image[y][x] == BinaryImage.BLACK and (x, y) not in visited_pixels:
                    # marcamos o pixel inicial como o pixel atual
                    actual_pixel[0], actual_pixel[1] = x, y
                    # enquanto o pixel atual for preto e for possível acessar alguma adjacência
                    while (self._binary_image[actual_pixel[1]][actual_pixel[0]] == self.BLACK
                           and (actual_pixel[0], actual_pixel[1]) not in visited_pixels):
                        # adicionando o pixel aos pixels visitados
                        visited_pixels.add((actual_pixel[0], actual_pixel[1]))
                        # calculando os pixels adjacentes
                        if adjacency == self.EIGHT_ADJACENCY:
                            adjacent_pixels = self._get_eight_adjacency(actual_pixel[0], actual_pixel[1])
                        else:
                            adjacent_pixels = self._get_four_adjacency(actual_pixel[0], actual_pixel[1])
                        # iterando pelos pixels adjacentes para procurarmos o caminho
                        for x_adjacent_pixel, y_adjacent_pixel in adjacent_pixels:
                            if (self._binary_image[y_adjacent_pixel][x_adjacent_pixel] == self.BLACK
                                    and (x_adjacent_pixel, y_adjacent_pixel) not in visited_pixels):
                                # encontramos o próximo pixel e podemos parar o laço
                                actual_pixel[0], actual_pixel[1] = x_adjacent_pixel, y_adjacent_pixel
                                break
                    else:
                        regions += 1

        return regions

    def _get_border_pixel(self, x: int, y: int, direction: int) -> Tuple[int, int]:
        """Procura pelo pixel de borda na direção selecionada.

        Args:
            x: Posição x do pixel selecionado.
            y: Posição y do pixel selecionado.
            direction: Direção selecionada para a procura do pixel de borda.

        Returns: Valor do pixel
        """
        border_pixel = None
        next_x, next_y = x, y

        while self._binary_image[next_y][next_x] == self.BLACK:
            border_pixel = (next_x, next_y)
            # procurando o pixel de borda inferior
            if direction == 0:
                next_x = next_x
                next_y = next_y + 1
            # procurando o pixel de borda superior
            elif direction == 1:
                next_x = next_x
                next_y = next_y - 1
            # procurando o pixel de borda a esquerda
            elif direction == 2:
                next_x = next_x - 1
                next_y = next_y
            # procurando o pixel de borda a direita
            else:
                next_x = next_x + 1
                next_y = next_y
            # verificando se estamos em uma condição de parada
            if not (0 <= next_x < self._binary_image.shape[0]) or not (0 <= next_y < self._binary_image.shape[1]):
                break

        # retornando o pixel encontrado
        return border_pixel

    def _mensure_geometric_features(self, x: int, y: int) -> Tuple[int, int, int]:
        """Realiza uma aproximação do perímetro, diâmetro e area de um componente da imagem.

        Args:
            x: Posição x do pixel selecionado.
            y: Posição y do pixel selecionado.

        Returns: Área, perímetro e diâmetro do componente selecionado.
        """
        bottom_pixel = self._get_border_pixel(x, y, 0)
        top_pixel = self._get_border_pixel(x, y, 1)
        left_pixel = self._get_border_pixel(x, y, 2)
        right_pixel = self._get_border_pixel(x, y, 3)

        # estimando as métricas geométricas
        diameter = right_pixel[0] - left_pixel[0]
        height = bottom_pixel[1] - top_pixel[1]
        area = diameter * height
        perimeter = 2 * height + 2 * diameter
        return perimeter, area, diameter

    # Interfaces
    def execute_flow(self) -> None:
        self._execute_flow()

    def counting_components(self, adjacency) -> int:
        return self._counting_components(adjacency=adjacency)
