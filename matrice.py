
import neopixel
import time

# Nombre de LED sur la matrice
NB_LEDS = 64

# À remplacer par la broche DATA réellement choisie
DATA_PIN = None

pixels = None

NOIR = (0, 0, 0)
JAUNE = (255, 180, 0)
BLEU = (0, 0, 255)

# Dessins en 8 lignes de 8 pixels
SMILEY = [
    "00111100",
    "01000010",
    "10100101",
    "10000001",
    "10100101",
    "10011001",
    "01000010",
    "00111100",
]

CHIFFRES = {
    1: [
        "00011000",
        "00111000",
        "00011000",
        "00011000",
        "00011000",
        "00011000",
        "00111100",
        "00000000",
    ],
    2: [
        "00111100",
        "01000010",
        "00000010",
        "00000100",
        "00011000",
        "00100000",
        "01111110",
        "00000000",
    ],
    3: [
        "00111100",
        "01000010",
        "00000010",
        "00011100",
        "00000010",
        "00000010",
        "01111100",
        "00000000",
    ],
    4: [
        "00000000",
        "00000110",
        "00011110",
        "00100110",
        "01111111",
        "01111111",
        "00000110",
        "00000000",
    ],
}


def initialiser_matrice(pin):
    global pixels
    pixels = neopixel.NeoPixel(
        pin,
        NB_LEDS,
        brightness=0.2,
        auto_write=False
    )


def afficher(dessin, couleur):

    if pixels is None:
        print("Erreur : matrice non initialisee")
        return

    pixels.fill(NOIR)

    for y in range(8):
        for x in range(8):
            if dessin[y][x] == "1":
                index = y * 8 + x
                pixels[index] = couleur

    pixels.show()


def afficher_smiley():
    afficher(SMILEY, JAUNE)


def afficher_numero(numero):
    if numero in CHIFFRES:
        afficher(CHIFFRES[numero], BLEU)
