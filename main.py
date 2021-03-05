from PIL import Image
import pyautogui as pg
from find_objects import analysis, find_exit

from time import sleep, localtime
import keyboard

# [wood, stone, trees, stones]
amount = {'wood': 0, 'stone': 0, 'trees': 0, 'cobblestone': 0}

trees = []
stones = []


def usage():
    print("ZombieFarm afk bot v1.0")
    print("RULES:")
    print("\t1) Use only in second zoom (one click on -zoom)")
    print("\t2) Don`t move you screen since you have started bot")
    print("First of all add trees and stones that you want break")
    print("\t1) Move cursor on object")
    print("\t2) Press 'g' to add tree, 'h' to add stone")
    print("\t3) Press Ctrl to end this part\n")
    print("Then move your cursor to neutral position for you zombie and press 'm' ")
    print("\t\t(better to move on water)")
    print("Now you can go drink you tea and chill ^_^\n")
    print("You can set pause anytime by pressing 'p'")
    print("-------------------------------------------------------")


# Take some events like pause, add tree/stone and etc.
def work_with_keyboard(e):
    global stage

    if e.event_type == 'up':
        return

    if stage == "game":
        global pause

        if e.name == 'p':
            pause = not pause

    if stage == "adding_objects":
        global end_adding_objects

        if end_adding_objects:
            return
        if e.name == 'g':
            trees.append(pg.position())

        elif e.name == 'h':
            stones.append(pg.position())

        elif e.name == 'ctrl':
            end_adding_objects = True


# try to break some objects
def try_to_break(array, name):
    if len(array) > 0:
        click(array[0][0], array[0][1])
        sleep(3)
        img = pg.screenshot()
        if find_exit(img):
            click(0, 0)
        else:
            print(get_time() + 'Destroying new {}'.format(name))
            del array[0]


# return time like [hh:mm:ss]
def get_time():
    t = localtime()
    hour = '0' * (2 - len(str(t[3]))) + str(t[3])
    minute = '0' * (2 - len(str(t[4]))) + str(t[4])
    sec = '0' * (2 - len(str(t[5]))) + str(t[5])
    return '[{}:{}:{}]\t'.format(hour, minute, sec)


def click(x, y):
    # click on object
    pg.moveTo(x + 5, y + 5)
    pg.click()

    # move cursor to top left corner
    pg.moveTo(1, 1)


# analysis every pixel and try to find objects
def run():
    img = pg.screenshot()
    sx, sy = img.size
    pix = img.load()

    for x in range(sx - 50):
        for y in range(sy - 50):
            obj = analysis(pix, x, y)
            if obj != 'nothing':
                click(x, y)
                amount[obj] += 1
                print(get_time() + 'Found ' + obj)
                return

            elif pause:
                return


if __name__ == '__main__':
    keyboard.hook(work_with_keyboard)
    usage()

    time = get_time()
    print(time + "Bot have started...")

    # Objects to break (trees and stones)
    stage = 'adding_objects'

    end_adding_objects = False
    while not end_adding_objects:
        sleep(1)

    print(time + "Added trees: " + str(len(trees)))
    print(time + "Added stones: " + str(len(stones)))

    pause = False
    stage = 'game'

    # number of iterations
    n = 0
    while True:
        n += 1

        #pause bot
        if pause:
            print(get_time() + "Paused")
            while pause:
                sleep(1)
            print(get_time() + "UnPaused")

        #try to destroy objects
        if not n % 20:
            try_to_break(trees, 'tree')
            sleep(3)
            try_to_break(stones, 'stone')

        #Check menu
        if not n % 30 and find_exit(pg.screenshot()):
            click(0, 0)

        run()
        sleep(3)