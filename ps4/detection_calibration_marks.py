import cv2 as cv
import numpy as np


class DetectionCalibrationMarks:
    """Classe para implementação da detecção das marcas de calibração.
    """

    def __init__(self, image_path: str):
        self._image = cv.imread(image_path)
        if self._image is None:
            print('Cannot load the image')

    def _detect_lines(self) -> None:
        """Método para detecção de linhas em uma imagem. Utilizaremos o Hough Lines.

        Returns: None.
        """
        gray = cv.cvtColor(self._image, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray, 50, 150, apertureSize=3)
        min_line_length = 100
        max_line_gap = 10
        lines = cv.HoughLinesP(edges, 1, np.pi/180, 50, None, minLineLength=min_line_length, maxLineGap=max_line_gap)
        if lines is not None:
            for i in range(0, len(lines)):
                l = lines[i][0]
                cv.line(self._image, (l[0], l[1]), (l[2], l[3]), (0, 255, 0), 3, cv.LINE_AA)
        cv.imshow('Lines', self._image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def detect_lines(self) -> None:
        self._detect_lines()
