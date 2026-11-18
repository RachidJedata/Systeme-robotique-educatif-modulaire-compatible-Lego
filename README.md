
# Système robotique éducatif modulaire compatible LEGO

## Présentation

Ce projet consiste à développer une plateforme robotique éducative modulaire, compatible avec l'écosystème LEGO, basée sur une carte **SAM E54 Curiosity Ultra** et l'environnement **CircuitPython**.

Le système repose sur une architecture maître-esclave : un contrôleur principal permet de sélectionner, lancer et arrêter différentes applications embarquées de manière indépendante.

Une matrice LED WS2812B de 8 × 8 pixels assure l'affichage graphique du menu et des informations relatives aux programmes sélectionnés. Elle permet également de distinguer visuellement le mode menu du mode exécution.

L'objectif est de proposer une plateforme évolutive permettant d'expérimenter différentes fonctionnalités électroniques et robotiques à travers des applications Python indépendantes.

## Fonctionnalités

- Architecture modulaire séparant le contrôleur principal des applications.
- Détection automatique des fichiers Python présents à la racine de la carte.
- Support des noms de fichiers numériques : `1.py`, `2.py`, `3.py`, etc.
- Tri numérique automatique des applications.
- Affichage du nom du fichier sélectionné dans le terminal série.
- Sélection des applications à l'aide de deux boutons.
- Lancement et arrêt des applications avec un troisième bouton.
- Affichage du numéro du programme sur une matrice WS2812B 8 × 8.
- Indication visuelle de l'état du système :
  - Affichage numérique dans le menu.
  - Affichage vert lorsque l'application est en cours d'exécution.
- Mémoire partagée entre le contrôleur principal et les applications.
- Gestion des ressources avec des fonctions d'initialisation et de nettoyage.
- Animation de démarrage avec affichage d'un smiley.

## Matériel

| Composant | Description |
|---|---|
| Microcontrôleur | SAM E54 Curiosity Ultra |
| Environnement embarqué | CircuitPython |
| Affichage | Matrice LED WS2812B 8 × 8 |
| Interface utilisateur | Trois boutons poussoirs |
| Actionneurs | LEDs et autres périphériques |

### Configuration des broches

| Élément | Broche |
|---|---|
| Bouton précédent | `microcontroller.pin.PA03` |
| Bouton suivant | `microcontroller.pin.PB07` |
| Bouton exécuter / arrêter | `microcontroller.pin.PA04` |
| Matrice WS2812B | `board.PD10` |
| LED des applications | `microcontroller.pin.PB03` |

**Remarque :** les boutons utilisent des résistances internes de rappel vers le niveau haut (Pull-up). Ils doivent être raccordés entre leur broche respective et GND.

Vérifier également l'alimentation 5 V de la matrice WS2812B ainsi que la présence d'une masse commune entre les composants.

## Structure du projet

```text
Robot-Educatif/
│
├── code.py
├── matrice.py
│
├── 1.py
├── 2.py
├── 3.py
├── 4.py
│
└── README.md
```

| Fichier | Description |
|---|---|
| `code.py` | Contrôleur principal : menu, boutons et gestion des applications. |
| `matrice.py` | Bibliothèque de contrôle de la matrice WS2812B. |
| `1.py` | Première application embarquée. |
| `2.py` | Deuxième application embarquée. |
| `3.py` | Troisième application embarquée. |
| `4.py` | Quatrième application embarquée. |

Les fichiers `code.py` et `matrice.py` sont réservés au contrôleur principal et ne sont pas proposés dans le menu.

## Architecture logicielle

Le système adopte une architecture maître-esclave composée de deux parties :

- **Master Controller :** gère l'interface utilisateur, la navigation, les boutons, l'affichage et le cycle de vie des applications.
- **Slave Applications :** programmes indépendants chargés dynamiquement par le contrôleur principal.

Chaque application dispose de son propre cycle de vie avec trois fonctions :

- `setup(context)` : initialisation de l'application.
- `loop(context)` : exécution principale.
- `cleanup(context)` : libération des ressources.

Cette architecture permet d'ajouter de nouvelles fonctionnalités sans modifier le fonctionnement général du contrôleur.

## Installation

1. Installer CircuitPython sur la carte SAM E54 Curiosity Ultra.
2. Connecter la carte à l'ordinateur.
3. Copier les fichiers suivants à la racine du lecteur CircuitPython :
   - `code.py`
   - `matrice.py`
   - Les fichiers Python correspondant aux applications.
4. Redémarrer la carte.
5. Ouvrir un terminal série pour consulter les messages de démarrage.

Le fichier `code.py` constitue le point d'entrée automatiquement exécuté par CircuitPython.

## Utilisation

### Démarrage

Au démarrage du système :

1. Le contrôleur initialise la matrice WS2812B.
2. Un smiley est affiché pendant deux secondes.
3. Les applications disponibles sont détectées automatiquement.
4. Le menu principal apparaît avec la première application sélectionnée.

### Navigation dans le menu

- Appuyer sur **Précédent** pour sélectionner l'application précédente.
- Appuyer sur **Suivant** pour sélectionner l'application suivante.
- La navigation est circulaire : après la dernière application, le menu revient à la première.

Le terminal série affiche le nom exact du fichier sélectionné, par exemple :

```text
========== MENU ==========
[MENU] Selected application: 2.py
[MENU] Status: READY
==========================
```

### Lancement et arrêt d'une application

Appuyer sur **Exécuter / Arrêter** pour lancer l'application sélectionnée.

Pendant son exécution :

- La matrice LED devient entièrement verte.
- Le terminal série indique le nom de l'application active.
- Le contrôleur exécute continuellement la fonction `loop(context)`.

Exemple dans le terminal :

```text
========== APPLICATION ==========
[RUNNING] Application: 2.py
[RUNNING] Status: ACTIVE
=================================
```

Pour arrêter l'application, appuyer une nouvelle fois sur le bouton **Exécuter / Arrêter**.

Le contrôleur appelle alors `cleanup(context)`, arrête l'application et retourne automatiquement au menu en conservant la dernière sélection.

### Indication visuelle des états

| État | Affichage de la matrice | Signification |
|---|---|---|
| Menu | Numéro du programme | Une application peut être sélectionnée. |
| Running | Vert | Une application est en cours d'exécution. |
| Retour au menu | Numéro du dernier programme | L'application a été arrêtée. |

Un mécanisme d'antirebond est utilisé pour éviter les déclenchements multiples des boutons.

## Interface de développement des applications

Chaque application est chargée dynamiquement depuis `code.py`.

Une application doit respecter l'interface suivante :

```python
def setup(context):
    # Initialisation des périphériques
    pass


def loop(context):
    # Fonction exécutée pendant que l'application est active
    pass


def cleanup(context):
    # Libération des ressources
    pass
```

Le dictionnaire `context` contient notamment :

```python
{
    "shared": shared_memory,
    "exit_requested": False
}
```

La mémoire partagée permet d'échanger des informations entre le contrôleur et les applications.

Elle contient actuellement :

- `counter` : compteur numérique.
- `selected_program` : nom du fichier du programme sélectionné.
- `application_running` : indique si une application est active.
- `led_state` : état de la LED.
- `message` : état courant du contrôleur (`MENU`, `RUNNING`, `Stopped`, etc.).

Pour demander l'arrêt d'une application depuis son propre code :

```python
context["exit_requested"] = True
```

Le contrôleur prend ensuite en charge l'arrêt et appelle `cleanup(context)`.

**Important :** la fonction `loop(context)` doit rester non bloquante afin de permettre au contrôleur de détecter les demandes d'arrêt.

## Ajouter une nouvelle application

Pour ajouter un programme :

1. Créer un nouveau fichier Python, par exemple `5.py`.
2. Implémenter les fonctions `setup(context)`, `loop(context)` et `cleanup(context)`.
3. Copier le fichier à la racine du lecteur CircuitPython.
4. Redémarrer le contrôleur.

La découverte des applications est automatique : tous les fichiers `.py` présents à la racine sont détectés, à l'exception de `code.py` et `matrice.py`.

### Tri des applications

Les applications dont le nom est numérique sont triées selon leur valeur numérique :

```text
1.py
2.py
3.py
4.py
5.py
10.py
11.py
```

Les autres fichiers Python sont également détectés et placés après les fichiers numériques, selon l'ordre alphabétique.

Il est donc possible d'utiliser des noms tels que :

- `1.py`
- `2.py`
- `robot.py`
- `led_test.py`
- `sensor.py`

Aucune modification du contrôleur principal n'est nécessaire pour ajouter une nouvelle application.

## Gestion de la matrice WS2812B

La bibliothèque `matrice.py` fournit les fonctions nécessaires au pilotage de la matrice LED 8 × 8.

Exemples d'utilisation :

```python
import matrice

matrice.initialiser_matrice()

# Afficher le numéro d'une application
matrice.afficher_numero(1)

# Afficher un smiley
matrice.afficher_smiley()

# Afficher une couleur uniforme
matrice.afficher_couleur((255, 0, 0))

# Afficher la couleur verte pendant l'exécution
matrice.afficher_couleur((0, 255, 0))

# Effacer la matrice
matrice.effacer_matrice()
```

Il est également possible d'afficher un motif personnalisé :

```python
motif = [
    "00111100",
    "01000010",
    "10000001",
    "10000001",
    "10011001",
    "10000001",
    "01000010",
    "00111100"
]

matrice.afficher_motif(motif, (0, 100, 255))
```

Chaque ligne représente une rangée de huit pixels. Les caractères `1` et `0` indiquent respectivement les pixels allumés et éteints.

**Remarque :** une application qui utilise elle-même la matrice peut modifier son affichage vert. L'indication visuelle Running est donc garantie uniquement tant que l'application ne modifie pas la matrice.

## Dépannage

### Aucun programme n'apparaît

- Vérifier que les fichiers possèdent l'extension `.py`.
- Vérifier qu'ils sont placés à la racine du lecteur CircuitPython.
- Vérifier que `code.py` et `matrice.py` sont présents.
- Consulter le terminal série pour identifier les erreurs de chargement.

### Les programmes ne sont pas triés correctement

- Vérifier que les noms numériques ne contiennent pas de caractères supplémentaires.
- Vérifier que les fichiers respectent le format `1.py`, `2.py`, `3.py`, etc.

### La matrice ne s'allume pas

- Vérifier la broche `board.PD10`.
- Vérifier l'alimentation 5 V et la masse commune.
- Vérifier que `initialiser_matrice()` est appelée.
- Vérifier le paramètre de luminosité `LUMINOSITE` dans `matrice.py`.

### Les boutons ne fonctionnent pas

- Vérifier les broches `PA03`, `PB07` et `PA04`.
- Vérifier le raccordement des boutons entre les broches et GND.
- Vérifier la configuration Pull-up.
- Vérifier que les boutons sont correctement relâchés après chaque pression.

### Une application ne s'arrête pas

- Vérifier le fonctionnement du bouton configuré sur `PA04`.
- Vérifier que `loop(context)` ne contient pas de boucle infinie bloquante.
- Vérifier que l'application respecte le mécanisme `exit_requested`.
- Vérifier que `cleanup(context)` libère correctement les ressources.

## Perspectives d'évolution

- Intégration de nouveaux modules électroniques et capteurs.
- Développement de nouvelles applications robotiques.
- Ajout de fonctionnalités de communication entre modules.
- Développement d'une interface graphique plus avancée.
- Extension de la plateforme à différents projets éducatifs compatibles LEGO.

---

**Technologies :** CircuitPython, Python, SAM E54, WS2812B et électronique numérique.
