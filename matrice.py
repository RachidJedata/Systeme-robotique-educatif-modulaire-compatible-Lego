
# ==========================================
# WS2812B 8x8 - SAM E54 Curiosity Ultra
# CircuitPython
# ==========================================

import board
import neopixel

LARGEUR = 8
HAUTEUR = 8
NB_LEDS = LARGEUR * HAUTEUR

PIN_DATA = board.PD10 

LUMINOSITE = 0.15

pixels = None


# ==========================================
# INITIALISATION
# ==========================================

def initialiser_matrice():

    global pixels

    if pixels is None:

        pixels = neopixel.NeoPixel(
            PIN_DATA,
            NB_LEDS,
            brightness=LUMINOSITE,
            auto_write=False
        )

    effacer_matrice()


# ==========================================
# COORDONNEES X / Y
# ==========================================

def index_led(x, y):

    if x < 0 or x >= LARGEUR:
        return None

    if y < 0 or y >= HAUTEUR:
        return None

    # câblage en lignes,
    # de gauche à droite, de haut en bas.
    return y * LARGEUR + x


# ==========================================
# CONTROLE DES PIXELS
# ==========================================

def afficher_pixel(x, y, couleur):

    index = index_led(x, y)

    if index is not None:
        pixels[index] = couleur


def effacer_matrice():

    pixels.fill((0, 0, 0))
    pixels.show()


def afficher_couleur(couleur):
    pixels.fill(couleur)
    pixels.show()


# ==========================================
# AFFICHER UN MOTIF 8x8
# ==========================================

def afficher_motif(motif, couleur=(255, 180, 0)):

    pixels.fill((0, 0, 0))

    for y in range(HAUTEUR):

        for x in range(LARGEUR):

            if motif[y][x] == "1":

                afficher_pixel(x, y, couleur)

    pixels.show()


# ==========================================
# SMILEY
# ==========================================

def afficher_smiley():

    smiley = [
        "00111100",
        "01000010",
        "10100101",
        "10000001",
        "10100101",
        "10011001",
        "01000010",
        "00111100"
    ]

    afficher_motif(smiley, (255, 180, 0))


# ==========================================
# CHIFFRES 0 A 9
# ==========================================

CHIFFRES = {

    0: [
        "00111100",
        "01000010",
        "01000110",
        "01001010",
        "01010010",
        "01100010",
        "01000010",
        "00111100"
    ],

    1: [
        "00011000",
        "00111000",
        "00011000",
        "00011000",
        "00011000",
        "00011000",
        "00011000",
        "00111100"
    ],

    2: [
        "00111100",
        "01000010",
        "00000010",
        "00000100",
        "00011000",
        "00100000",
        "01000000",
        "01111110"
    ],

    3: [
        "01111100",
        "00000010",
        "00000010",
        "00111100",
        "00000010",
        "00000010",
        "01000010",
        "00111100"
    ],

    4: [
        "00000100",
        "00001100",
        "00010100",
        "00100100",
        "01000100",
        "01111110",
        "00000100",
        "00000100"
    ],

    5: [
        "01111110",
        "01000000",
        "01000000",
        "01111100",
        "00000010",
        "00000010",
        "01000010",
        "00111100"
    ],

    6: [
        "00111100",
        "01000000",
        "01000000",
        "01111100",
        "01000010",
        "01000010",
        "01000010",
        "00111100"
    ],

    7: [
        "01111110",
        "00000010",
        "00000100",
        "00001000",
        "00010000",
        "00010000",
        "00010000",
        "00010000"
    ],

    8: [
        "00111100",
        "01000010",
        "01000010",
        "00111100",
        "01000010",
        "01000010",
        "01000010",
        "00111100"
    ],

    9: [
        "00111100",
        "01000010",
        "01000010",
        "01000010",
        "00111110",
        "00000010",
        "00000010",
        "00111100"
    ]
}


def afficher_numero(numero):

    if numero not in CHIFFRES:
        effacer_matrice()
        return

    afficher_motif(CHIFFRES[numero], (0, 100, 255))


# ==========================================
# FIN DU MODULE
# ==========================================
