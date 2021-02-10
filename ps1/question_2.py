import sys
import numpy as np
from typing import List, Tuple

import cv2 as cv


def step_1() -> None:
    """Realiza o passo A da questão 2.

    Returns: None.
    """
    cap = cv.VideoCapture('../videos/video.mp4')
    # verificando se o video foi carregado corretamente
    if cap is None:
        sys.exit('Erro ao ler o arquivo!')
    # quantidade de frames no vídeo
    length = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    print(length)


def step_2() -> Tuple[np.array, np.array, np.array]:
    """Realiza o passo B da questão 2.

    Returns: As três estatísticas calculadas da sequência de imagens.
    """
    # lendo o vídeo e iterando sobre os frames
    cap = cv.VideoCapture('../videos/video.mp4')
    # verificando se o vídeo foi carregado corretamente
    if cap is None:
        sys.exit('Erro ao ler o arquivo!')

    # iterando sobre cada frame
    success: bool = True
    # guardando as estatísticas selecionadas
    mean_per_frame = np.array([])
    std_per_frame = np.array([])
    contrast_per_frame = np.array([])
    while success:
        success, image = cap.read()
        if success:
            mean_per_frame = np.append(mean_per_frame, image.mean())
            std_per_frame = np.append(std_per_frame, image.std())
            contrast_per_frame = np.append(contrast_per_frame, cv.cvtColor(image, cv.COLOR_BGR2GRAY).std())
    return mean_per_frame, std_per_frame, contrast_per_frame


def step_3() -> Tuple[List[float], List[float], List[float]]:
    """Realiza o passo C da segunda questão.

    Returns: Lista com as novas funções normalizadas
    """
    # usaremos o passo anterior para receber as funções f, g e h do vídeo de teste
    f, g, h = step_2()  # mean per frame, std_per_frame e contrast_per_frame
    # calculando o valor de alpha e beta para g_new
    alpha_g_new = (g.std() / f.std()) * (f.mean() - g.mean())
    beta_g_new = (f.std() / g.std())
    # calculando o valor de alpha e beta para h_new
    alpha_h_new = (h.std() / f.std()) * (f.mean() - h.mean())
    beta_h_new = (h.std() / g.std())
    # normalizando as funções
    f_new: List[float] = []
    g_new: List[float] = []
    h_new: List[float] = []
    # iterando sobre os valores para obter as novas funções
    for i, _ in enumerate(f):
        f_new.append(f[i])
        g_new.append(beta_g_new * (g[i] + alpha_g_new))
        h_new.append(beta_h_new * (h[i] + alpha_h_new))
    return f_new, g_new, h_new


def step_4() -> None:
    """Realiza o passo D da questão 2.

    Returns: None.
    """
    f_new, g_new, h_new = step_3()
    # para verificarmos a normalização precisamos calcular a distância entre as funções
    d_1 = 0.0
    d_2 = 0.0
    # iterando sobre os valores das funções para obter a distância
    for i, _ in enumerate(f_new):
        d_1 += abs(f_new[i] - g_new[i])
        d_2 += abs(f_new[i] - h_new[i])
    d_1 = d_1 / len(f_new)
    d_2 = d_2 / len(f_new)
    print(f'Distance between f and g_new: {d_1}')
    print(f'Distance between f and h_new: {d_2}')


step_4()
