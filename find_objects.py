from PIL import Image

wood = Image.open("img/wood.png")
stone = Image.open("img/stone.png")
chest = Image.open("img/chest.png")


def close_color(c1, c2):
    dif = 15
    r1, g1, b1 = c1[:3]
    r2, g2, b2 = c2[:3]
    if abs(r1 - r2) > dif:
        return False
    if abs(g1 - g2) > dif:
        return False
    if abs(b1 - b2) > dif:
        return False
    return True


# try to recognize object on picture with start in x,y
def recognize(pix, x, y, obj):
    obj_pix = obj.load()
    ox, oy = obj.size

    for delta_x in range(ox // 2):
        for delta_y in range(oy // 2):
            if not close_color(pix[x + delta_x, y + delta_y], obj_pix[delta_x, delta_y]):
                return False

    return True


# compare pixels with images of objects
def analysis(pix, x, y):
    if recognize(pix, x, y, wood):
        return 'wood'

    elif recognize(pix, x, y, stone):
        return 'stone'

    elif recognize(pix, x, y, chest):
        return 'chest'
    return 'nothing'


def find_exit(img):
    sx, sy = img.size
    pix = img.load()
    menu_color = (255, 248, 221)
    start_pos = int(((701 / 1920) * sx)), int((357 / 1080) * sy)
    for delta in range(10):
        if not close_color(pix[start_pos[0], start_pos[1] + delta], menu_color):
            return False
    return True

