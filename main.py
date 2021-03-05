from PIL import Image
import pyautogui as pg

from time import sleep, localtime
import keyboard


# [wood, stone, trees, stones]
amounts = [0 for _ in range(4)]

wood = Image.open("img/wood.png")
stone = Image.open("img/stone.png")
chest = Image.open("img/chest.png")

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


def get_time():
    t = localtime()
    hour = '0' * (2 - len(str(t[3]))) + str(t[3])
    minute = '0' * (2 - len(str(t[4]))) + str(t[4])
    sec = '0' * (2 - len(str(t[5]))) + str(t[5])
    return '[{}:{}:{}]\t'.format(hour, minute, sec)


def close_color(c1, c2):
    dif = 20
    r1, g1, b1 = c1[:3]
    r2, g2, b2 = c2[:3]
    if abs(r1 - r2) > dif:
        return False
    if abs(g1 - g2) > dif:
        return False
    if abs(b1 - b2) > dif:
        return False
    return True


def recognize(pix, x, y, obj):
    obj_pix = obj.load()
    ox, oy = obj.size

    for delta_x in range(ox // 2):
        for delta_y in range(oy // 2):
            if not close_color(pix[x + delta_x, y + delta_y], obj_pix[delta_x, delta_y]):
                return False

    return True


def analysis(pix, x, y):
    obj = ''

    if recognize(pix, x, y, wood):
        obj = 'wood'
        amounts[0] += 1
    elif recognize(pix, x, y, stone):
        obj = 'stone'
        amounts[1] += 1
    elif recognize(pix, x, y, chest):
        obj = 'chest'

    if obj != '':
        print(get_time() + "Found {} on: {}, {}".format(obj, x, y))
        click(x, y)
        return True

    return False


def click(x, y):
    # click on object
    pg.moveTo(x + 5, y + 5)
    pg.click()

    # move cursor to top left corner
    pg.moveTo(1, 1)


def run():
    img = pg.screenshot()
    sx, sy = img.size
    pix = img.load()

    for x in range(sx - 50):
        for y in range(sy - 50):
            if analysis(pix, x, y) or pause:
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
    while True:

        if pause:
            print(get_time() + "Paused")
            while pause:
                sleep(1)
            print(get_time() + "UnPaused")

        run()
        sleep(3)
