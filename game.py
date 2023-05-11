import math
import os
import random
import time

import pygame  # 版本2.1.2及以上
from pygame.locals import *

pygame.init()
pygame.mixer.init()  # 加载pygame

# 加载字体
myfonts = []
for i in range(90):
    myfonts.append(pygame.font.Font(r'./data/unifont-15.0.01.otf', (i + 10)))
presse_up = {}
s = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_a, K_AMPERSAND, K_ASTERISK, K_AT, K_b, K_BACKQUOTE, K_BACKSLASH, K_BACKSPACE, K_BREAK, K_c, K_CAPSLOCK, K_CARET, K_CLEAR, K_COLON, K_COMMA,
     K_d, K_DELETE, K_DOLLAR, K_DOWN, K_e, K_END, K_EQUALS, K_ESCAPE, K_EURO, K_EXCLAIM, K_f, K_F1, K_F10, K_F11, K_F12, K_F13, K_F14, K_F15, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9,
     K_g, K_GREATER, K_h, K_HASH, K_HELP, K_HOME, K_i, K_INSERT, K_j, K_k, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]
# 名称：起始点x，起始点y，长，宽，显示长，显示宽
texture_number = {'choose_ul': (448, 0, 32, 32, 32, 32), 'choose_ur': (480, 0, 32, 32, 32, 32), 'choose_dl': (448, 32, 32, 32, 32, 32), 'choose_dr': (480, 32, 32, 32, 32, 32),
                  'grass': (64, 0, 64, 64, 64, 64), 'mud': (0, 0, 64, 64, 64, 64), 'stone': (384, 0, 64, 64, 64, 64), 'stone_u': (64, 64, 64, 64, 64, 64), 'stone_ul': (128, 64, 64, 64, 64, 64),
                  'stone_ulr': (192, 64, 64, 64, 64, 64), 'stone_ur': (256, 64, 64, 64, 64, 64), 'stone_udlr': (320, 64, 64, 64, 64, 64), 'stone_udr': (384, 64, 64, 64, 64, 64),
                  'stone_udl': (448, 64, 64, 64, 64, 64), 'stone_ud': (512, 64, 64, 64, 64, 64), 'sky': (192, 0, 64, 64, 64, 64), 'player': (256, 0, 64, 64, 64, 64), 'bag1': (0, 64, 64, 64, 50, 50),
                  'ying1': (32, 128, 32, 32, 32, 32), 'ying2': (0, 128, 32, 32, 32, 32), 'ying3': (0, 160, 32, 32, 32, 32), 'ying4': (32, 160, 32, 32, 32, 32), 'iron': (64, 128, 64, 64, 64, 64),
                  'water': (320, 0, 64, 64, 64, 64), 'tree': (0, 192, 64, 64, 128, 128)}
object_texture = {'error': (32, 0, 16, 16), 'iron': (0, 0, 16, 16), 'wood': (0, 16, 16, 16)}
object_number = {'iron': 1, 'tree': 2}
goods_number = {1: 'iron', 2: 'wood'}
for i in s:
    presse_up[i] = False
next_music_time = int(time.time())  # 音乐截止时间
screen_size = (1080, 768)  # 窗口大小
pygame.display.set_caption('mine')  # 窗口名称
music_list = []  # 加载音乐列表
music_path = os.listdir('./data/music')
m1 = 0
music_volume = 1  # 音乐声音大小
r = 0  # 播放的音乐

for t1 in range(len(music_path)):
    try:
        music_list.append(pygame.mixer.Sound(r'./data/music/' + str(music_path[t1])))
    except FileNotFoundError:
        print(str(music_path[t1]) + '错误')


def crop(image, rect):  # 图片裁剪
    return image.subsurface(rect[0], rect[1], rect[2], rect[3])


def zoom(image, size):  # 图片缩放
    return pygame.transform.scale(image, size)


screen = pygame.display.set_mode(screen_size, flags=pygame.RESIZABLE)  # 创建窗口
texture = pygame.image.load(r'./data/texture/texture1.png').convert_alpha()
goods = pygame.image.load(r'./data/texture/texture2.png').convert_alpha()
texture_list = {}  # 贴图表
for bn in texture_number:
    sn = texture_number[bn]
    if sn[2] == sn[4] and sn[3] == sn[5]:
        texture_list[bn] = crop(texture, (sn[0], sn[1], sn[2], sn[3]))
    else:
        texture_list[bn] = zoom(crop(texture, (sn[0], sn[1], sn[2], sn[3])), (sn[4], sn[5]))
object_list = {}
for bn in object_texture:
    sn = object_texture[bn]
    object_list[bn] = zoom(crop(goods, (sn[0], sn[1], sn[2], sn[3])), (40, 40))
# pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
backgroud = pygame.Surface(screen_size)
backgroud.set_alpha(150)
backgroud.fill((0, 0, 0))
show_f3 = False
show_bag = False
drag = []
get_cd = 0  # 资源获取进度
last_get = [0, 0]  # 上一个获取的资源的位置
move = False  # 玩家的运动 True则为移动
if __name__ == '__main__':
    run = True
else:
    run = False  # 代码循环部分的开关 True则为循环
fps = 0  # 一个负责检测帧数的变量
t = time.time() + 1
presse = []  # 按键检测
xt = 0  # 视角X坐标
yt = 0  # 视角Y坐标
ts = 10  # 视角大小
seed = ''  # 种子
start_player_bag = []  # 玩家初始背包
for n in range(45):
    start_player_bag.append([0, 0])
pause = False  # 暂停
jm = 0  # 界面数值
pzx = []  # 碰撞箱存储
cover = False  # 指针方块碰到玩家
draws = ()
resource_box = []  # 资源碰撞箱

# 地图 [方块标签,方块属性]
the_map = []


class mouse_set:
    press = [False, False, False]  # 鼠标放开
    xy = (0, 0)  # 鼠标位置
    up = [False, False, False]  # 鼠标按下
    wheel = 0  # 鼠标滚轮
    point_xz = ()  # 鼠标指向方块
    last_press = 0
    last2 = 0
    start_press = 0
    hold = [0, 0]  # 光标指向位置
    x = 0
    y = 0


class player_set:
    x = 0  # 玩家X轴坐标
    y = 0  # 玩家Y轴坐标
    z = 0  # 玩家Z轴坐标
    pzx = [int(screen_size[0] / 2 - 10), int(screen_size[1] / 2), int(screen_size[0] / 2 + 10), int(screen_size[1] / 2 + 20)]  # 玩家碰撞箱
    cd = 0  # 玩家受伤CD
    x_offset = 0  # 玩家x轴偏移量
    z_offset = 0  # 玩家y轴偏移量
    bag = start_player_bag.copy()  # 玩家背包
    speed = 5  # 玩家速度
    max_speed = 6  # 玩家最大速度
    heath = 20  # 玩家生命值


player = player_set()
mouse = mouse_set()


def pzx_updata():  # 碰撞箱数据更新
    global the_map, pzx
    pass


def draw(thing, pos):
    global screen
    screen.blit(thing, pos)


def write(thing, pos, size=50, colour=(255, 255, 255), kjc=False):  # 打印文本，kjc=抗锯齿
    global myfonts, screen
    if size > 100:
        size = 100
    elif size < 10:
        size = 10
    st = myfonts[size - 10].render(str(thing), kjc, colour)
    draw(st, pos)


def anniu(rect, zi='', rect_color=(120, 120, 120), text_color=(255, 255, 255)):  # 按钮
    global mouse
    pygame.draw.rect(screen, rect_color, rect)
    write(zi, (int(rect[0] + (rect[2] / 2) - ((rect[3] - 20) * len(zi) / 2)), int(rect[1] + 10)), (rect[3] - 20), text_color)
    if rect[0] < mouse.xy[0] < (rect[0] + rect[2]) and rect[1] < mouse.xy[1] < (rect[1] + rect[3]):
        pygame.draw.rect(screen, (255, 255, 255), rect, 4)
        if mouse.up[0]:
            return True
        else:
            return False
    else:
        pygame.draw.rect(screen, (0, 0, 0), rect, 4)
        return False


def press_line(rect, number, number_min, number_max, text='', text_color=(255, 255, 255), rect_color=(120, 120, 120), line_color=(50, 50, 50), rect_width=4):  # 拖动条
    global mouse
    pygame.draw.line(screen, line_color, (rect[0], rect[1] + rect[3] / 2), (rect[0] + rect[2], rect[1] + rect[3] / 2), rect[3])
    write(text, (int(rect[0] + (rect[2] / 2) - ((rect[3] - 20) * len(text) / 2)), int(rect[1])), rect[3], text_color)
    pygame.draw.rect(screen, rect_color, (rect[0] + number / (number_max - number_min) * rect[2], rect[1], rect_width, rect[3]))
    if rect[0] < mouse.xy[0] < (rect[0] + rect[2]) and rect[1] < mouse.xy[1] < (rect[1] + rect[3]) and number_max > number_min:
        if mouse.press[0]:
            return (mouse.x - rect[0]) / rect[2] * (number_max - number_min)
        else:
            return number
    return number


def press():  # 侦测按键
    global move, player, pzx
    up, down, right, left = True, True, True, True
    s1 = 0
    for n1 in pzx:
        if player.pzx[0] < n1[2] and player.pzx[2] > n1[0]:
            if n1[1] < player.pzx[1] + player.x_offset < n1[3]:
                up = False
                player.z_offset = 2
            if n1[1] < player.pzx[3] + player.x_offset < n1[3]:
                down = False
                player.z_offset = -2
        if player.pzx[3] > n1[1] and player.pzx[1] < n1[3]:
            if n1[0] < player.pzx[0] + player.z_offset < n1[2]:
                left = False
                player.x_offset = 2
            if n1[0] < player.pzx[2] + player.z_offset < n1[2]:
                right = False
                player.x_offset = -2
        if not up or not right or not down or not left:
            s1 = s1 + 1
        if s1 > 3:
            pass
    move = False
    if presse[K_w] and up:
        player.z_offset = player.z_offset - player.speed
        move = True
    if presse[K_s] and down:
        player.z_offset = player.z_offset + player.speed
        move = True
    if presse[K_a] and left:
        player.x_offset = player.x_offset - player.speed
        move = True
    if presse[K_d] and right:
        player.x_offset = player.x_offset + player.speed
        move = True
    if player.x_offset > player.max_speed:
        player.x_offset = player.max_speed
    if player.x_offset < -player.max_speed:
        player.x_offset = -player.max_speed
    if player.z_offset > player.max_speed:
        player.z_offset = player.max_speed
    if player.z_offset < -player.max_speed:
        player.z_offset = -player.max_speed
    if player.x > (len(the_map) * 64):
        player.x = 0
    if player.x < 0:
        player.x = (len(the_map) * 64)
    if player.z > (len(the_map) * 64):
        player.z = 0
    if player.z < 0:
        player.z = (len(the_map) * 64)
    if player.x_offset > 0:
        player.x_offset = player.x_offset - 1
    if player.x_offset < 0:
        player.x_offset = player.x_offset + 1
    if player.z_offset > 0:
        player.z_offset = player.z_offset - 1
    if player.z_offset < 0:
        player.z_offset = player.z_offset + 1
    player.x = player.x + player.x_offset
    player.z = player.z + player.z_offset


def fill_block(x, y, size, block, the_block_type):
    global the_map
    for yi in range(size * 2 - 1):
        for xi in range(size * 2 - 1):
            the_map[(yi + y - size + 1) % len(the_map)][(xi + x - size + 1) % len(the_map)] = [block, the_block_type]


def player_hurt(number):  # 玩家受伤
    global player
    if player.cd <= time.time():
        player.heath = player.heath - number
        player.cd = time.time() + 0.5


def player_updata():  # 玩家更新
    global player, pzx
    for n1 in pzx:
        if player.pzx[0] > n1[0] and player.pzx[2] < n1[2] and player.pzx[1] > n1[1] and player.pzx[3] < n1[3]:
            player.heath = player.heath - 1
        if player.pzx[2] > n1[0] and player.pzx[0] < n1[2]:
            if n1[1] < player.pzx[1] < n1[3]:
                player.z = player.z + player.speed
                player.z_offset = player.speed
            if n1[1] < player.pzx[3] < n1[3]:
                player.z = player.z - player.speed
                player.z_offset = -player.speed
        if player.pzx[3] > n1[1] and player.pzx[1] < n1[3]:
            if n1[0] < player.pzx[0] < n1[2]:
                player.x_offset = player.speed
                player.x = player.x + player.speed
            if n1[0] < player.pzx[2] < n1[2]:
                player.x_offset = -player.speed
                player.x = player.x - player.speed


def ying(yi, xi, pos):
    global texture_list, the_map
    if the_map[yi - 1][xi][0] == 1:
        draw(texture_list['ying1'], (pos[0] + 32, pos[1]))
        if the_map[yi - 1][xi - 1][0] != 1:
            draw(texture_list['ying2'], pos)
        elif the_map[yi - 1][xi - 1][0] == 1:
            draw(texture_list['ying1'], pos)
    if the_map[yi - 1][xi][0] != 1:
        if the_map[yi - 1][xi - 1][0] == 1 and the_map[yi][xi - 1][0] != 1:
            draw(texture_list['ying4'], pos)
        elif the_map[yi - 1][xi - 1][0] == 1 and the_map[yi][xi - 1][0] == 1:
            draw(texture_list['ying4'], pos)
    if the_map[yi][xi - 1][0] == 1:
        draw(texture_list['ying4'], (pos[0], pos[1] + 32))
        if the_map[yi - 1][xi - 1][0] != 1:
            draw(texture_list['ying3'], pos)


def block_type(x, y, pos):
    global the_map, texture_list, pzx, resource_box
    if 0 < x < len(the_map):
        xi = x
    elif x < 0:
        xi = -(-x % 64)
    else:
        xi = x % len(the_map)
    if 0 < y < len(the_map):
        yi = y
    elif y < 0:
        yi = -(-y % 64)
    else:
        yi = y % len(the_map)
    block = the_map[yi][xi][0]
    if block == 0:
        draw(texture_list['grass'], pos)
        if the_map[yi][xi][1] == 'iron':
            resource_box.append([pos[0], pos[1], pos[0] + 64, pos[1] + 64, 'iron', xi, yi])
            draw(texture_list['iron'], pos)
        elif the_map[yi][xi][1] == 'tree':
            resource_box.append([pos[0] - 32, pos[1] - 96, pos[0] + 96, pos[1] + 32, 'tree', xi, yi])
            draw(texture_list['tree'], [pos[0] - 32, pos[1] - 96])
        ying(yi, xi, pos)
    elif block == 1:
        pzx.append([pos[0], pos[1], (pos[0] + 64), (pos[1] + 64)])
        draw(texture_list['stone'], pos)
        draw(texture_list['stone_' + str(the_map[yi][xi][1])], (pos[0], (pos[1])))
    elif block == 2:
        pzx.append([pos[0], pos[1], (pos[0] + 64), (pos[1] + 64)])
        draw(texture_list['water'], pos)
        ying(yi, xi, pos)
    elif block == 3:
        draw(texture_list['stone'], pos)
        ying(yi, xi, pos)
    else:
        write(the_map[yi][xi], pos, 20, (0, 0, 0))
        draw(texture_list['sky'], pos)


def goods_type(thing, pos, write_number=False):
    global player, goods_number, object_list
    if thing != [0, 0]:
        try:
            draw(object_list[goods_number[thing[0]]], (pos[0] + 5, pos[1] + 5))
        except IndexError:
            draw(object_list['error'], (pos[0] + 5, pos[1] + 5))
        if write_number:
            write(thing[1], pos, 20)


def add_thing_bag(thing, number=1):
    for n2 in range(len(player.bag)):
        if player.bag[n2][0] == thing:
            if player.bag[n2][1] >= 64:
                continue
            player.bag[n2][1] = player.bag[n2][1] + number
            break
        elif player.bag[n2][0] == 0:
            player.bag[n2] = [thing, number]
            break


def draw_block():  # 绘制方块
    global screen_size, move, mouse, draws, player, pause
    for z in range(screen_size[1] // 64 + 3):
        for x in range(screen_size[0] // 64 + 3):
            # 设置坐标
            pos = (int(x * 64 - (player.x % 64) - 64), int(z * 64 - ((player.z - player.y) % 64) - 64))

            # 判断是否能填充
            uz = int(math.ceil((player.z - player.y) / 64))
            ux = int(math.ceil(player.x / 64))
            if player.z == 0:
                uz = 1
            elif player.z % 64 == 0:
                uz = uz + 1
            if player.x == 0:
                ux = 1
            elif player.x % 64 == 0:
                ux = ux + 1
            yu = int((z - 1) + uz - screen_size[1] // 128 - 1)
            xu = int((x - 1) + ux - screen_size[0] // 128 - 0)
            block_type(xu, yu, pos)
        if int(z * 64 - (player.z % 64) - 64 + player.speed) <= player.pzx[3]:
            draw(texture_list['player'], (int(screen_size[0] / 2 - 32), int(screen_size[1] / 2 - 32)))


def xy_3d(x, z, y):
    global xt, yt, ts
    xy = [(math.cos(math.radians(xt)) * x - math.sin(math.radians(xt)) * y) * ts + screen_size[0] // 2,
          (math.cos(math.radians(yt)) * (math.sin(math.radians(xt)) * x + math.cos(math.radians(xt)) * y) + math.sin(math.radians(yt)) * z) * ts + screen_size[1] // 2]
    return xy


def galaxy():
    global xt, yt, ts, mouse, jm
    if ts < 1:
        ts = 1
    screen.fill((0, 0, 0))
    pygame.draw.polygon(screen, (255, 255, 255), (xy_3d(1, 1, 1), xy_3d(-1, 1, 1), xy_3d(-1, 1, -1), xy_3d(1, 1, -1), xy_3d(1, 1, 1)))
    xt = mouse.xy[0] - screen_size[0] // 2
    yt = mouse.xy[1] - screen_size[1] // 2
    if mouse.wheel == 1:
        ts = ts + 2
    elif mouse.wheel == -1:
        ts = ts - 2
    if anniu((screen_size[0] / 2 - 100, screen_size[1] - 40, 200, 40), '返回', text_color=(0, 0, 0)):
        jm = 1
    write(str(yt), (0, 20), 20)


def block_update(x, y, size=1):  # 方块更新
    global the_map
    for yi in range(size * 2 - 1):
        for xi in range(size * 2 - 1):
            if the_map[(yi + y - size + 1) % len(the_map)][(xi + x - size + 1) % len(the_map)][0] == 1:
                do = ''
                le = ''
                ri = ''
                if the_map[yi + y - size + 1][(xi + x + 1 - size + 1) % len(the_map)][0] == 1:
                    ri = 'r'
                if the_map[yi + y - size + 1][xi + x - 1 - size + 1][0] == 1:
                    le = 'l'
                if the_map[(yi + y + 1 - size + 1) % len(the_map)][xi + x - size + 1][0] == 1:
                    do = 'd'
                the_map[(yi + y) - size + 1 % len(the_map)][(xi + x - size + 1) % len(the_map)] = [1, 'u' + do + le + ri]


def bag_block(pos, n2):
    global drag, player, texture_list
    if n2 in drag:
        pygame.draw.rect(screen, (128, 128, 128), (pos[0], pos[1], 50, 50))
    if pos[0] < mouse.xy[0] < (pos[0] + 50) and pos[1] < mouse.xy[1] < (pos[1] + 50):
        pygame.draw.rect(screen, (128, 128, 128), (pos[0], pos[1], 50, 50))
        if mouse.up[0] and len(drag) == 0:
            if mouse.hold == [0, 0]:
                mouse.hold = player.bag[n2]
                player.bag[n2] = [0, 0]
            elif player.bag[n2][0] == mouse.hold[0]:
                if (mouse.hold[1] + player.bag[n2][1]) > 64:
                    mouse.hold[1] = mouse.hold[1] - (64 - player.bag[n2][1])
                    player.bag[n2][1] = 64
                else:
                    player.bag[n2][1] = player.bag[n2][1] + mouse.hold[1]
                    mouse.hold = [0, 0]
            elif player.bag[n2] == [0, 0] and mouse.hold != [0, 0]:
                if time.time() - mouse.last2 > 0.2:
                    x = mouse.hold
                    mouse.hold = player.bag[n2]
                    player.bag[n2] = x
                else:
                    w1 = mouse.hold[1]
                    for n3 in range(36):
                        if w1 < 64 and player.bag[n3][0] == mouse.hold[0] and player.bag[n3][1] != 64:
                            if (player.bag[n3][1] + w1) <= 64:
                                w1 = w1 + player.bag[n3][1]
                                player.bag[n3] = [0, 0]
                            elif (player.bag[n3][1] + w1) > 64:
                                player.bag[n3] = [player.bag[n3][0], (player.bag[n3][1] + w1) - 64]
                                w1 = 64
                    player.bag[n2] = [mouse.hold[0], w1]
                    mouse.hold = [0, 0]
        elif mouse.up[2]:
            if mouse.hold == [0, 0] and player.bag[n2][1] > 0.2:
                mouse.hold[0] = player.bag[n2][0]
                x = player.bag[n2][1] // 2
                mouse.hold[1] = x
                player.bag[n2][1] = player.bag[n2][1] - x
            elif (player.bag[n2][0] == mouse.hold[0] or player.bag[n2] == [0, 0]) and mouse.hold[1] > 0:
                if player.bag[n2][1] != 64:
                    player.bag[n2][1] = player.bag[n2][1] + 1
                    player.bag[n2][0] = mouse.hold[0]
                    mouse.hold[1] = mouse.hold[1] - 1
        elif mouse.press[0] and time.time() - mouse.start_press > 0.2:
            if mouse.hold != [0, 0] and player.bag[n2] == [0, 0] and mouse.hold[1] != 1:
                if not (n2 in drag):
                    drag.append(n2)
    draw(texture_list['bag1'], pos)
    goods_type(player.bag[n2], pos, True)


def draw_game():  # 绘制游戏画面
    global get_cd, last_get, screen_size, pzx, mouse, player, show_f3, cover, pause, backgroud, seed, jm, run, show_bag, resource_box, drag
    mouse.point_xz = [math.ceil((player.x + mouse.xy[0]) / 64) - screen_size[0] // 128, math.floor((player.z + mouse.xy[1]) / 64) - screen_size[1] // 128]
    pzx = []
    resource_box = []
    draw_block()
    for n3 in range(9):
        ipos = ((screen_size[0] // 2) - 225 + n3 * 50, screen_size[1] - 50)
        draw(texture_list['bag1'], ipos)
        goods_type(player.bag[n3], ipos, True)
    if player.bag[40] != [0, 0]:
        draw(texture_list['bag1'], ((screen_size[0] // 2) - 225 - 80, screen_size[1] - 50))
        goods_type(player.bag[40], ((screen_size[0] // 2) - 225 - 80, screen_size[1] - 50), True)
    if show_bag:
        get_cd = 0
        draw(backgroud, (0, 0))
        pygame.draw.rect(screen, (64, 64, 64), (screen_size[0] / 2 - 235, screen_size[1] / 2 - 260, 470, 420))
        pygame.draw.rect(screen, (0, 0, 0), (screen_size[0] / 2 - 165, screen_size[1] / 2 - 220, 64, 100))
        draw(texture_list['player'], (screen_size[0] / 2 - 165, screen_size[1] / 2 - 220))
        for n2 in range(45):
            if n2 <= 35:
                pos = (screen_size[0] / 2 - 225 + (n2 % 9) * 50, screen_size[1] / 2 + 100 - n2 // 9 * 50)
            elif 36 <= n2 <= 39:
                pos = (screen_size[0] / 2 - 235, screen_size[1] / 2 - 205 + (n2 - 37) * 50)
            elif n2 == 40:
                pos = (screen_size[0] / 2 - 101, screen_size[1] / 2 - 100)
            elif 41 <= n2 <= 42:
                pos = (screen_size[0] / 2 + (n2 - 41) * 50, screen_size[1] / 2 - 200)
            else:
                pos = (screen_size[0] / 2 + (n2 - 43) * 50, screen_size[1] / 2 - 150)
            bag_block(pos, n2)
        if len(drag) != 0 and mouse.hold != [0, 0] and mouse.press[0]:
            if mouse.hold[1] >= len(drag):
                nn = mouse.hold[1] // len(drag)
                for m in drag:
                    player.bag[m] = [0, 0]
                for m in drag:
                    player.bag[m] = [mouse.hold[0], nn]
            else:
                for m in drag:
                    player.bag[m] = [0, 0]
                drag = []
        if len(drag) != 0 and mouse.hold != [0, 0] and mouse.up[0]:
            if mouse.hold[1] >= len(drag):
                nn = mouse.hold[1] // len(drag)
                nx = mouse.hold[1] % len(drag)
                for m in drag:
                    player.bag[m] = [mouse.hold[0], nn]
                if nx > 0:
                    mouse.hold[1] = nx
                else:
                    mouse.hold = [0, 0]
        if len(drag) != 0 and not mouse.press[0]:
            drag = []
        if mouse.hold != [0, 0]:
            goods_type(mouse.hold, (mouse.xy[0] - 20, mouse.xy[1] - 20), True)
        if mouse.hold[1] <= 0:
            mouse.hold = [0, 0]
    if show_f3 and not pause and not show_bag:
        write(str(player.x) + '/' + str(player.y) + '/' + str(player.z), (0, 20), 20, (255, 255, 255))
        write(str(player.heath) + '血量', (0, 40), 20, (255, 255, 255))
        write(str(mouse.point_xz), (0, 60), 20)
        write(str(cover), (0, 80), 20)
        write(str((int(mouse.point_xz[0] * 64 - player.x + screen_size[0] / 2 - 64), int(mouse.point_xz[1] * 64 - player.z - player.y + screen_size[1] / 2 - 12))), (0, 100), 20)
        write(str(seed), (0, 120), 20)
        for n3 in pzx:
            pygame.draw.rect(screen, (255, 255, 255), (n3[0], n3[1], (n3[2] - n3[0]), (n3[3] - n3[1])), 1)
        for n3 in resource_box:
            pygame.draw.rect(screen, (255, 255, 255), (n3[0], n3[1], (n3[2] - n3[0]), (n3[3] - n3[1])), 1)
        pygame.draw.rect(screen, (255, 255, 255), (player.pzx[0], player.pzx[1], (player.pzx[2] - player.pzx[0]), (player.pzx[3] - player.pzx[1])), 1)
    if presse_up[K_ESCAPE]:
        if show_bag:
            show_bag = False
            if mouse.hold != [0, 0]:
                add_thing_bag(mouse.hold[0], mouse.hold[1])
                mouse.hold = [0, 0]
        else:
            if pause:
                pause = False
            else:
                pause = True
    for n1 in range(36):
        if player.bag[n1] != [0, 0]:
            if player.bag[n1][1] <= 0:
                player.bag[n1] = [0, 0]
    if pause:
        draw(backgroud, (0, 0))
        if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 - 20, 200, 40), '返回主菜单', (128, 128, 128)):
            jm = 1
        if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 40, 200, 40), '退出至桌面', (128, 128, 128)):
            run = False
    else:
        if get_cd > 0:
            pygame.draw.rect(screen, (0, 255, 0), (screen_size[0] / 2 - 50, screen_size[1] / 2 - 10, get_cd, 20))
        if presse_up[K_e]:
            if show_bag:
                show_bag = False
                if mouse.hold != [0, 0]:
                    add_thing_bag(mouse.hold[0], mouse.hold[1])
                    mouse.hold = [0, 0]
            else:
                show_bag = True
        if not show_bag:
            for box in resource_box:
                if box[0] < mouse.xy[0] < box[2] and box[1] < mouse.xy[1] < box[3]:
                    draw(texture_list['choose_ul'], (box[0], box[1]))
                    draw(texture_list['choose_ur'], (box[2] - 32, box[1]))
                    draw(texture_list['choose_dl'], (box[0], box[3] - 32))
                    draw(texture_list['choose_dr'], (box[2] - 32, box[3] - 32))
                    if mouse.press[0]:
                        for i1 in object_number:
                            if box[4] == i1:
                                if last_get == [box[5], box[6]] and get_cd != 0:
                                    if get_cd >= 100:
                                        add_thing_bag(object_number[i1], 1)
                                        last_get = [box[5], box[6]]
                                        get_cd = 0
                                    else:
                                        get_cd = get_cd + 1
                                elif get_cd == 0:
                                    last_get = [box[5], box[6]]
                                    get_cd = get_cd + 1
                    break
                elif last_get == [box[5], box[6]]:
                    get_cd = 0
            # if mouse.up[0] and the_map[mouse.point_xz[1]][mouse.point_xz[0]][1] == 0:
            #    try:
            #        the_map[y1][x1] = [0, 0]
            #        block_update(x1, y1, 2)
            #    except IndexError:
            #        print('清除错误')
            # if mouse.up[2] and not cover:
            #    try:
            #        the_map[y1][x1] = [1, 'u']
            #        block_update(x1, y1, 3)
            #    except IndexError:
            #        print('放置错误')
            press()
            pzx_updata()
        cover = False
        mxi = (mouse.point_xz[0] * 64 - player.x + screen_size[0] / 2 - 64)
        myi = (mouse.point_xz[1] * 64 - player.z - player.y + screen_size[1] / 2 - 12)
        if player.pzx[2] > mxi and player.pzx[0] < mxi + 64:
            if myi < player.pzx[1] < myi + 64:
                cover = True
            if myi < player.pzx[3] < myi + 64:
                cover = True
        if player.pzx[3] > myi and player.pzx[1] < myi + 64:
            if mxi < player.pzx[0] < mxi + 64:
                cover = True
            if mxi < player.pzx[2] < mxi + 64:
                cover = True


def get_map(size=32, map_seed=''):  # 获取地图
    global the_map, player, run
    if size % 16 != 0:
        ms = size // 16 + 1
    else:
        ms = size
    map_number = []
    for y2 in range(ms):
        b = []
        for x2 in range(ms):
            b.append(0)
        map_number.append(b)
    chunks = []
    for y2 in range(ms // 16):
        b = []
        for x2 in range(ms // 16):
            b.append(0)
        chunks.append(b)
    for y in range(ms // 16):
        for x in range(ms // 16):
            random.seed(str(map_seed) + str(x * 16) + str(y * 16))
            h = random.randint(0, 100)
            chunks[y][x] = h
    for y in range(ms // 16):
        for x in range(ms // 16):
            if y == len(chunks) - 1:
                p1 = chunks[y][x]
                p3 = chunks[0][x]
                if x == len(chunks) - 1:
                    p2 = chunks[y][0]
                    p4 = chunks[0][0]
                else:
                    p2 = chunks[y][x]
                    p4 = chunks[0][x + 1]
            else:
                p1 = chunks[y][x]
                p3 = chunks[y + 1][x]
                if x == len(chunks) - 1:
                    p2 = chunks[y][0]
                    p4 = chunks[y + 1][0]
                else:
                    p2 = chunks[y][x + 1]
                    p4 = chunks[y + 1][x + 1]
            cmap = []
            for y1 in range(16):
                m = []
                for x1 in range(16):
                    n1 = (p1 * x1 + p2 * (17 - x1)) / 16
                    n2 = (p3 * x1 + p4 * (17 - x1)) / 16
                    w = (n1 * y1 + n2 * (16 - y1)) / 16
                    m.append(w)
                cmap.append(m)
            g = []
            gg = []
            for i1 in cmap:
                gg.append(0)
            for i1 in cmap:
                g.append(gg)
            for n3 in range(len(cmap)):
                gh = cmap[n3].copy()
                gh.reverse()
                g[-(n3 + 1)] = gh.copy()
            cmap = g.copy()
            for h in range(len(cmap)):
                for li in range(len(cmap[h])):
                    map_number[y * 16 + h][x * 16 + li] = cmap[h][li]
    cmap = []

    for y in range(ms):
        c = []
        for x in range(ms):
            n4 = map_number[y][x]
            if n4 < 20:
                nu = 2
            elif 70 > n4 >= 20:
                nu = 0
            elif 80 > n4 >= 70:
                nu = 3
            else:
                nu = 1
            c.append(nu)
        cmap.append(c)
    the_map = []
    iron = []
    for y in range(len(cmap)):
        c = []
        for x in range(len(cmap[y])):
            if cmap[y][x] == 0:
                random.seed(str(map_seed) + str(x) + str(y))
                mineral = random.random()  # 矿物值
                if mineral > 0.96:
                    c.append([0, 'iron'])
                    iron.append((x, y))
                elif mineral < 0.05:
                    c.append([0, 'tree'])
                else:
                    c.append([0, 0])
            elif cmap[y][x] == 1:
                le = ''
                ri = ''
                do = ''
                if cmap[y][x - 1] == 1:
                    le = 'l'
                if cmap[y][(x + 1) % len(cmap)] == 1:
                    ri = 'r'
                if cmap[(y + 1) % len(cmap)][x] == 1:
                    do = 'd'
                c.append([1, ('u' + do + le + ri)])
            elif cmap[y][x] == 2:
                c.append([2, 0])
            elif cmap[y][x] == 3:
                c.append([3, 0])
            else:
                c.append([-1, 0])
        the_map.append(c)
    for n4 in iron:
        fill_block(n4[0], n4[1], 0, 0, 'iron')
        block_update(n4[0], n4[1], 1)
    find_run = 1
    wx = 8
    wy = 12
    while find_run == 0:
        random.seed(seed + str(find_run) + str(wx))
        wx = random.randint(1, len(the_map) - 2)
        random.seed(seed + str(find_run) + str(wy))
        wy = random.randint(1, len(the_map) - 2)
        if the_map[wy][wx][0] == 0 or the_map[wy][wx][0] == 3:
            fill_block(wx, wy, 2, 0, 0)
            block_update(wx, wy, 3)
            find_run = 0
        else:
            find_run = find_run + 1
    player.x = wx * 64
    player.z = wy * 64


while run:
    presse = pygame.key.get_pressed()
    fps = (clock.get_fps() * 10) // 10
    mouse.xy = pygame.mouse.get_pos()
    mouse.x = mouse.xy[0]
    mouse.y = mouse.xy[1]
    if screen_size != (screen.get_width(), screen.get_height()):
        screen_size = (screen.get_width(), screen.get_height())
        player.pzx = [int(screen_size[0] / 2 - 10), int(screen_size[1] / 2), int(screen_size[0] / 2 + 10), int(screen_size[1] / 2 + 20)]
        backgroud = pygame.Surface(screen_size)
        backgroud.set_alpha(150)
        backgroud.fill((0, 0, 0))

    # 游戏更细部分
    screen.fill((10, 100, 200))
    for i in range(3):
        if not pygame.mouse.get_pressed()[i] and mouse.press[i]:
            mouse.up[i] = True
            mouse.last2 = mouse.last_press
            mouse.last_press = time.time()
    if pygame.mouse.get_pressed()[0] and not mouse.press[0]:
        mouse.start_press = time.time()
    # if jm != 1:
    #    pygame.mixer.music.stop()
    if int(time.time()) > next_music_time and len(music_list) > 0:
        pygame.mixer.music.stop()
        r = random.randint(0, len(music_list) - 1)
        pygame.mixer.Sound.play(music_list[r])
        next_music_time = next_music_time + int(music_list[r].get_length())
    if presse[K_ESCAPE] and jm != 2:
        run = False
    if jm == 2:  # 游戏运行界面
        draw_game()
    elif jm == 1:  # 游戏主界面
        for iy in range(int(screen_size[1] / 64) + 1):
            for ix in range(int(screen_size[0] / 64) + 1):
                draw(texture_list['mud'], (ix * 64, iy * 64))
        if anniu((int(screen_size[0] / 2 - 100), int(screen_size[1] / 2 - 20), 200, 40), '单人游戏', (120, 120, 120)):
            jm = 3
            seed = ''
            pause = False
            show_bag = False
            player.bag = start_player_bag.copy()
        if anniu((int(screen_size[0] / 2 - 100), int(screen_size[1] / 2 + 20), 200, 40), '星系', (120, 120, 120)):
            jm = 4
        if anniu((int(screen_size[0] / 2 - 100), int(screen_size[1] / 2 + 60), 200, 40), '设置', (120, 120, 120)):
            jm = 5
        write(str(music_path[r][:-4]), (0, screen_size[1] - 20), 20)
    elif jm == 4:  # 星系界面
        galaxy()
    elif jm == 5:  # 设置界面
        for iy in range(int(screen_size[1] / 64) + 1):
            for ix in range(int(screen_size[0] / 64) + 1):
                draw(texture_list['mud'], (ix * 64, iy * 64))
        if anniu((0, screen_size[1] - 40, 100, 40), '返回', (120, 120, 120)):
            jm = 1
        music_list[r].set_volume(press_line((100, 100, 200, 40), music_list[r].get_volume(), 0, 1, '音量'))
    elif jm == 3:  # 游戏创建界面
        for iy in range(int(screen_size[1] / 64) + 1):
            for ix in range(int(screen_size[0] / 64) + 1):
                draw(texture_list['mud'], (ix * 64, iy * 64))
        inp = 0
        write('种子', (200, 200), 40, (255, 255, 255))
        pygame.draw.rect(screen, (255, 255, 255), (200, 250, 300, 40))
        write(seed, (200, 250), 40, (0, 0, 0))
        if anniu((200, 300, 250, 40), '创建新的世界', (120, 120, 120)):
            if seed == '':
                seed = random.randint(1, 10000)
                get_map(128, str(seed))
                jm = 2
            else:
                get_map(128, str(seed))
                jm = 2
        if presse_up[K_0] or presse_up[K_KP0]:
            seed = seed + '0'
        if presse_up[K_1] or presse_up[K_KP1]:
            seed = seed + '1'
        if presse_up[K_2] or presse_up[K_KP2]:
            seed = seed + '2'
        if presse_up[K_3] or presse_up[K_KP3]:
            seed = seed + '3'
        if presse_up[K_4] or presse_up[K_KP4]:
            seed = seed + '4'
        if presse_up[K_5] or presse_up[K_KP5]:
            seed = seed + '5'
        if presse_up[K_6] or presse_up[K_KP6]:
            seed = seed + '6'
        if presse_up[K_7] or presse_up[K_KP7]:
            seed = seed + '7'
        if presse_up[K_8] or presse_up[K_KP8]:
            seed = seed + '8'
        if presse_up[K_9] or presse_up[K_KP9]:
            seed = seed + '9'
        if presse_up[K_BACKSPACE]:
            seed = seed[:-1]
    elif jm == 0:  # 游戏加载界面
        screen.fill((0, 0, 0))
        jm = 1

    write(str(fps) + 'Fps', (0, 0), 20, (255, 255, 255))
    pygame.display.update()
    # pygame.display.flip()
    clock.tick(70)

    # 侦测游戏是否关闭
    wp = False
    mouse.press = pygame.mouse.get_pressed()
    mouse.up = [False, False, False]
    mouse.wheel = 0
    for i in presse_up:
        presse_up[i] = False
    for event in pygame.event.get():
        if event.type is QUIT:
            run = False
        if event.type == KEYUP:
            e = event.key
            if e == K_F3:
                if show_f3:
                    show_f3 = False
                else:
                    show_f3 = True
            for i in presse_up:
                if e == i:
                    presse_up[i] = True
        if event.type == MOUSEWHEEL:
            mouse.wheel = event.y
        # if event.type == MOUSEBUTTONUP:  # 鼠标放开检测
        #    mouse.up = pygame.mouse.get_pressed()
