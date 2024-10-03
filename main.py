from PIL import Image
import numpy as np


class EqualizarHistograma:
    def _contar_pixels(self, imagem) -> dict[int, int]:
        pixels_por_nivel = {k: 0 for k in range(256)}
        for i in range(self.height):
            for j in range(self.width):
                pixels_por_nivel[imagem[i][j]] += 1

        return pixels_por_nivel

    def _normalizacao(
        self, num_pixels: int, pixels_por_nivel: dict[int, int]
    ) -> dict[int, float]:
        pixeis_por_nivel_normalizados = {
            k: v / num_pixels for k, v in pixels_por_nivel.items()
        }
        return pixeis_por_nivel_normalizados

    def _calculo_de_eq(self, pixeis_normalizados: dict[int, float]):
        lista_normalizados = [v for v in pixeis_normalizados.values()]
        lista_eq = {}
        niveis_cinza = [v for v in pixeis_normalizados.keys()]
        for i in range(len(lista_normalizados)):
            valor_eq = 0
            for j in range(i, -1, -1):
                valor_eq += 7 * lista_normalizados[j]
            valor_eq = round(valor_eq)
            lista_eq[niveis_cinza[i]] = valor_eq
        return lista_eq

    def normalizar_histograma(self, imagem):
        imagem = np.array(imagem)
        self.height, self.width = imagem.shape
        num_pixels = self.height * self.width

        pixeis_por_nivel = self._contar_pixels(imagem)
        pixeis_normalizados = self._normalizacao(num_pixels, pixeis_por_nivel)
        lista_eq = self._calculo_de_eq(pixeis_normalizados)

        for i in range(self.height):
            for j in range(self.width):
                imagem[i][j] = lista_eq[imagem[i][j]]
        return (np.matrix(imagem) * (255 // 7)).astype(np.uint8)


def main():
    img = Image.open("images.jpeg")
    img = img.convert("L")

    img_normalizada = EqualizarHistograma().normalizar_histograma(img)
    img_normalizada = Image.fromarray(img_normalizada, mode="L")
    img_normalizada.save("imagem-resultado.png")


if __name__ == "__main__":
    main()
