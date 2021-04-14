class ReadImageError(Exception):
    """Exceção para tratar casos de erro de leitura de imagens.
    """

    def __init__(self, path: str):
        """Construtor
        """
        self._path = path
        super().__init__(f'Não foi possível exibir a imagem {self._path}.')
