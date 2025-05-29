import pickle

class Serializador:
    def salvar_em_arquivo(self, caminho, dados):
        with open(caminho, 'wb') as f:
            pickle.dump(dados, f)

    def carregar_de_arquivo(self, caminho):
        try:
            with open(caminho, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return []
