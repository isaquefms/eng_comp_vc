from alg_h_s import HornSchunck
from mean_shift import MeanShift
from detection_calibration_marks import DetectionCalibrationMarks


def main():
    # questão 1
    video = HornSchunck('../videos/taxi.mpg', 0.1, 40)
    video.horn_schunck()
    video.show_velocities()

    # questão 2
    # mean_shift = MeanShift('../imgs/spring.png')
    # mean_shift.mean_shift()

    # questão 3
    # dcm = DetectionCalibrationMarks('../imgs/Image15.tif')
    # dcm.detect_lines()


main()
