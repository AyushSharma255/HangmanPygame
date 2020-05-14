import pygame
import os
import threading
import textwrap
from helper import GameHelper
from time import sleep

pygame.init()


def getFrame(num):
    return os.path.join(GameHelper.image, f"man{num}.png")


rootSettings, playerSettings = {}, {}


def setup():
    global rootSettings, playerSettings

    rootSettings = {
        "dimensions": (600, 600),
        "color": (255, 255, 255),
        "icon": pygame.image.load(getFrame(6)),
        "caption": "Hangman",
        "scene": "menu",
        "font": pygame.font.SysFont(os.path.join(GameHelper.assets, "roboto.ttf"), 84),
        "cap": pygame.font.SysFont(os.path.join(GameHelper.assets, "roboto.ttf"), 24)
    }

    playerSettings = {
        "frame": 0,
        "word": GameHelper.getWord().strip(),
        "secret": "",
        "unlockedWord": "",
        "definition": "",
    }

    playerSettings["unlockedWord"] = len(playerSettings["word"]) * "-"
    playerSettings["definition"] = GameHelper.defineWord(playerSettings["word"])
    playerSettings["secret"] = playerSettings["word"]
    # print(playerSettings["word"])

def reload():
    rootSettings["scene"] = "menu"
    playerSettings["frame"] = 0
    playerSettings["word"] = GameHelper.getWord().strip()
    playerSettings["secret"] = playerSettings["word"]
    playerSettings["unlockedWord"] = len(playerSettings["word"]) * "-"
    playerSettings["definition"] = GameHelper.defineWord(playerSettings["word"])

setup()
root: pygame.SurfaceType = pygame.display.set_mode(rootSettings["dimensions"])
pygame.display.set_caption(rootSettings["caption"])
pygame.display.set_icon(rootSettings["icon"])


def draw():
    root.fill(rootSettings["color"])

    if rootSettings["scene"] == "game":
        renderWord = rootSettings["font"].render(playerSettings["unlockedWord"], True, (0, 0, 0))
        root.blit(
            renderWord,
            (50, 0)
        )

        root.blit(
            pygame.transform.scale(
                pygame.image.load(getFrame(playerSettings["frame"])),
                (400, 450)
            ),
            (150, 100)
        )

    if rootSettings["scene"] == "over":
        renderWord = rootSettings["font"].render(playerSettings["secret"], True, (0, 0, 0))
        words = textwrap.wrap(playerSettings["definition"], 50)

        for word in words:
            renderDefinition = rootSettings["cap"].render(word, True, (0, 0, 0))

            root.blit(
                renderDefinition,
                (50, 100 + words.index(word) * 15)
            )

        root.blit(
            renderWord,
            (50, 25)
        )

    if rootSettings["scene"] == "menu":
        renderWord = rootSettings["font"].render("Hangman", True, (0, 0, 0))

        root.blit(
            renderWord,
            (50, 25)
        )

        root.blit(
            pygame.transform.scale(
                pygame.image.load(getFrame(6)),
                (400, 450)
            ),
            (150, 100)
        )

    pygame.display.update()


running = True
while running:
    draw()

    if playerSettings["frame"] == 6 or playerSettings["unlockedWord"] == playerSettings["word"]:
        def fadeBack():
            playerSettings["word"] = "_"
            playerSettings["unlockedWord"] = "__"
            playerSettings["frame"] = 0
            sleep(0.05)
            rootSettings["scene"] = "over"
            while rootSettings["scene"] != "over":
                rootSettings["scene"] = "over"
            sleep(
                len(playerSettings["definition"]) / 25
            )
            reload()


        threading.Thread(target=fadeBack).start()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rootSettings["scene"] == "menu":
                rootSettings["scene"] = "game"
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and rootSettings["scene"] == "game":
            if event.unicode in ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j",
                                 "k", "l", "z", "x", "c", "v", "b", "n", "m"]:
                key = event.unicode

                indexes = []

                for index, letter in enumerate(playerSettings["word"]):
                    if letter == key:
                        indexes.append(index)

                if len(indexes) == 0:
                    if playerSettings["frame"] != 6:
                        playerSettings["frame"] += 1

                unlockedList = list(playerSettings["unlockedWord"])

                for index in indexes:
                    unlockedList[index] = playerSettings["word"][index]

                playerSettings["unlockedWord"] = "".join(unlockedList)
