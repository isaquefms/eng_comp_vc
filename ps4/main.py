from alg_h_s import HornSchunck


def main():
    video = HornSchunck('../videos/taxi.mpg', 0.1, 40)
    video.horn_schunck()
    video.show_velocities()


main()
