from binary_image import BinaryImage


def main():
    """Execução do algoritmo.

    Returns: None.
    """
    # captando o path da imagem e o seu nome
    image_path = input('Insert the image path: ')
    image_name = input('Insert the image name: ')
    # criamos a imagem e executamos o fluxo de processamento com a mesma
    b_image = BinaryImage(image_path, image_name, 150)
    # b_image.show_binary_image()
    b_image.execute_flow()


main()
