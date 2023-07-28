import math
import os
import time

import pygame  # 版本2.1.2及以上
from pygame.locals import *

from get_map import *

pygame.init()
pygame.mixer.init()  # 加载pygame

# 加载字体
myfonts = []
for i in range(90):
    myfonts.append(pygame.font.Font(r'./data/unifont-15.0.01.ttf', (i + 10)))
presse_up = {}
# s = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_a, K_AMPERSAND, K_ASTERISK, K_AT, K_b, K_BACKQUOTE, K_BACKSLASH, K_BACKSPACE, K_BREAK, K_c, K_CAPSLOCK, K_CARET, K_CLEAR, K_COLON, K_COMMA,
#     K_d, K_DELETE, K_DOLLAR, K_DOWN, K_e, K_END, K_EQUALS, K_ESCAPE, K_EURO, K_EXCLAIM, K_f, K_F1, K_F10, K_F11, K_F12, K_F13, K_F14, K_F15, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9,
#     K_g, K_GREATER, K_h, K_HASH, K_HELP, K_HOME, K_i, K_INSERT, K_j, K_k, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]
s = {K_0: 0, K_1: 1, K_2: 2, K_3: 3, K_4: 4, K_5: 5, K_6: 6, K_7: 7, K_8: 8, K_9: 9, K_a: 'a', K_b: 'b', K_c: 'c', K_d: 'd', K_e: 'e', K_f: 'f', K_g: 'g', K_h: 'h', K_i: 'i', K_j: 'j', K_k: 'k',
     K_KP0: 0, K_KP1: 1, K_KP2: 2, K_KP3: 3, K_KP4: 4, K_KP5: 5, K_KP6: 6, K_KP7: 7, K_KP8: 8,
     K_KP9: 9, K_l: 'l', K_m: "m", K_n: 'n', K_o: 'o', K_p: 'p', K_q: 'q', K_r: 'r', K_s: 's', K_t: 't', K_u: 'u', K_v: 'v', K_w: 'w', K_x: 'x', K_y: 'y', K_z: 'z'}
# 名称：起始点x，起始点y，长，宽，显示长，显示宽
texture_number = {'choose_ul': (0, 448, 0, 32, 32, 32, 32), 'choose_ur': (0, 480, 0, 32, 32, 32, 32), 'choose_dl': (0, 448, 32, 32, 32, 32, 32), 'choose_dr': (0, 480, 32, 32, 32, 32, 32),
                  'no_choose_ul': (0, 512, 0, 32, 32, 32, 32), 'no_choose_ur': (0, 544, 0, 32, 32, 32, 32), 'no_choose_dl': (0, 512, 32, 32, 32, 32, 32), 'no_choose_dr': (0, 544, 32, 32, 32, 32, 32),
                  'grass0': (0, 64, 0, 64, 64, 64, 64), 'mud': (0, 0, 0, 64, 64, 64, 64), 'stone': (0, 384, 0, 64, 64, 64, 64), 'stone_u': (0, 64, 64, 64, 64, 64, 64),
                  'stone_ul': (0, 128, 64, 64, 64, 64, 64), 'stone_ulr': (0, 192, 64, 64, 64, 64, 64), 'stone_ur': (0, 256, 64, 64, 64, 64, 64), 'stone_udlr': (0, 320, 64, 64, 64, 64, 64),
                  'stone_udr': (0, 384, 64, 64, 64, 64, 64),
                  'stone_udl': (0, 448, 64, 64, 64, 64, 64), 'stone_ud': (0, 512, 64, 64, 64, 64, 64), 'sky': (0, 192, 0, 64, 64, 64, 64), 'player': (0, 256, 0, 64, 64, 64, 64),
                  'bag1': (0, 0, 64, 64, 64, 50, 50), 'choose_bag': (0, 576, 0, 64, 64, 50, 50), 'grass': (0, 64, 192, 64, 64, 64, 64),
                  'ying1': (0, 32, 128, 32, 32, 32, 32), 'ying2': (0, 0, 128, 32, 32, 32, 32), 'ying3': (0, 0, 160, 32, 32, 32, 32), 'ying4': (0, 32, 160, 32, 32, 32, 32),
                  'iron': (0, 64, 128, 64, 64, 64, 64), 'water': (0, 320, 0, 64, 64, 64, 64), 'tree': (0, 0, 192, 64, 64, 128, 128)}
object_texture = {'error': (0, 64, 32, 32), 'iron': (0, 0, 32, 32), 'wood': (0, 32, 32, 32), 'worktable': (0, 96, 32, 32)}
object_number = {'iron': 1, 'tree': 2}
goods_number = {1: 'iron', 2: 'wood', 3: 'worktable'}
for i in s:
    presse_up[i] = False
next_music_time = int(time.time())  # 音乐截止时间
screen_size = (1280, 720)  # 窗口大小
screen_size_1 = ()
full_screen = False
pygame.display.set_caption('mine')  # 窗口名称
music_list = []  # 加载音乐列表
music_path = os.listdir('./data/music')
music_volume = 1  # 音乐声音大小
r = 0  # 播放的音乐

for t1 in range(len(music_path)):
    try:
        music_list.append(pygame.mixer.Sound(r'./data/music/' + str(music_path[t1])))
    except FileNotFoundError or pygame.error:
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
    if sn[0] == 0:
        if sn[3] == sn[5] and sn[4] == sn[6]:
            texture_list[bn] = crop(texture, (sn[1], sn[2], sn[3], sn[4]))
        else:
            texture_list[bn] = zoom(crop(texture, (sn[1], sn[2], sn[3], sn[4])), (sn[5], sn[6]))
texture_list['grass1'] = pygame.transform.flip(texture_list['grass0'], True, False)
texture_list['grass2'] = pygame.transform.flip(texture_list['grass0'], False, True)
texture_list['grass3'] = pygame.transform.flip(texture_list['grass0'], True, True)
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
drag = [[], [], [], []]
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
for n in range(36):
    start_player_bag.append([0, 0, 0])
pause = False  # 暂停
jm = 0  # 界面数值
pzx = []  # 碰撞箱存储
cover = False  # 指针方块碰到玩家
draws = ()
resource_box = []  # 资源碰撞箱
setting_back = 1  # 设置返回界面
# 地图 [方块标签,方块属性]
the_map = []
# 合成表{（需要在工作台上合成，有序合成，[配方，\n表示换行]）：（结果）}
formulation = [([0, 1, [[2, 1], [2, 1], '\n', [2, 1], [2, 1]]], [3, 1])]
try:
    setting = open(r'./data/setting.ini', 'r+')
    music_volume = float(setting.read())
except FileNotFoundError:
    setting = open(r'./data/setting.ini', 'w+')
    setting.write('0')
    music_volume = 1
setting.close()


class mouse_set:
    press = [False, False, False]  # 鼠标放开
    xy = (0, 0)  # 鼠标位置
    up = [False, False, False]  # 鼠标按下
    wheel = 0  # 鼠标滚轮
    point_xz = ()  # 鼠标指向方块坐标
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
    bag_composition = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 玩家背包合成表
    clothe = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]  # 玩家装备
    left_hand = [[0, 0, 0]]  # 玩家左手物品
    longest_touch = 200
    choose_bag = 0


player = player_set()
mouse = mouse_set()


def long(x1, y1, x2, y2):  # 两点距离
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


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
    write(text, (int(rect[0] + (rect[2] / 2) - ((rect[3] - 20) * len(text) / 2)), int(rect[1]) + 3), rect[3] - 6, text_color)
    pygame.draw.rect(screen, rect_color, (rect[0] + number / (number_max - number_min) * rect[2], rect[1], rect_width, rect[3]))
    if rect[0] < mouse.x < (rect[0] + rect[2]) and rect[1] < mouse.y < (rect[1] + rect[3]) and number_max > number_min:
        if mouse.press[0]:
            return (mouse.x - rect[0]) / rect[2] * (number_max - number_min)
        else:
            return number
    return number


class input_rect:
    inputting = False
    string = ''
    font_color = (0, 0, 0)
    backgroud_color = (0, 0, 0)
    rect = [0, 0, 0, 0]
    number = False
    last_backspace = 0

    def __init__(self, rect, number=False, font_color=(0, 0, 0), backgroud_color=(255, 255, 255)):  # 输入框
        self.font_color = font_color
        self.backgroud_color = backgroud_color
        self.rect = rect
        self.number = number
        self.last_backspace = 0

    def get_string(self):
        global mouse, presse_up
        pygame.draw.rect(screen, self.backgroud_color, self.rect)
        if time.time() % 1 >= 0.5 and self.inputting:
            write(self.string + '|', (self.rect[0], self.rect[1] + 2), self.rect[3] - 4, self.font_color)
        else:
            write(self.string, (self.rect[0], self.rect[1] + 2), self.rect[3] - 4, self.font_color)
        if self.rect[0] < mouse.x < (self.rect[0] + self.rect[2]) and self.rect[1] < mouse.y < (self.rect[1] + self.rect[3]):
            if mouse.up[0]:
                self.inputting = True
        else:
            self.inputting = False
        if presse[K_BACKSPACE]:
            if self.last_backspace == 0:
                self.last_backspace = time.time()
        else:
            self.last_backspace = 0
        if time.time() - self.last_backspace > 1 and self.last_backspace != 0:
            if len(self.string) > 0:
                self.string = self.string[:-1]
        if self.inputting:
            for i1 in presse_up:
                if i1 in [K_BACKSPACE, K_DELETE]:
                    if len(self.string) > 0:
                        self.string = self.string[:-1]
                if not self.number:
                    if i1 in [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8,
                              K_KP9, K_l, K_m, K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z]:
                        self.string = self.string + str(s[i1])
                else:
                    if i1 in [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]:
                        self.string = self.string + str(s[i1])
        if len(self.string) > 0:
            if self.number:
                return int(self.string)
            else:
                return str(self.string)
        else:
            return None


seed_input = input_rect((screen.get_width() / 2 - 150, screen.get_height() / 2 - 20, 300, 40))


def press():  # 侦测按键
    global move, player, pzx
    up, down, right, left = True, True, True, True
    for n1 in pzx:
        if player.pzx[0] + 6 < n1[2] and player.pzx[2] - 6 > n1[0]:
            if n1[1] < player.pzx[1] + player.x_offset < n1[3]:
                up = False
                player.z_offset = 1
            if n1[1] < player.pzx[3] + player.x_offset < n1[3]:
                down = False
                player.z_offset = -1
        if player.pzx[3] - 6 > n1[1] and player.pzx[1] + 6 < n1[3]:
            if n1[0] < player.pzx[0] + player.z_offset < n1[2]:
                left = False
                player.x_offset = 1
            if n1[0] < player.pzx[2] + player.z_offset < n1[2]:
                right = False
                player.x_offset = -1
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
    for n1 in pzx:
        if player.pzx[0] > n1[0] and player.pzx[2] < n1[2] and player.pzx[1] > n1[1] and player.pzx[3] < n1[3]:
            player.heath = player.heath - 1


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


def block_type(x, y, pos):  # 方块类型
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
        draw(texture_list['grass' + str(the_map[yi][xi][1][0])], pos)
        if 'iron' in the_map[yi][xi][1]:
            resource_box.append([pos[0], pos[1], 64, 64, 'iron', xi, yi])
            draw(texture_list['iron'], pos)
        elif 'tree' in the_map[yi][xi][1]:
            resource_box.append([pos[0] - 32, pos[1] - 96, 128, 128, 'tree', xi, yi])
            draw(texture_list['tree'], [pos[0] - 32, pos[1] - 96])
        elif 'grass' in the_map[yi][xi][1]:
            draw(texture_list['grass'], pos)
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
    if thing != [0, 0, 0]:
        try:
            draw(object_list[goods_number[thing[0]]], (pos[0] + 5, pos[1] + 5))
            if write_number and thing[1] > 1:
                write(thing[1], pos, 20)
        except IndexError:
            draw(object_list['error'], (pos[0] + 5, pos[1] + 5))
        except KeyError:
            draw(object_list['error'], (pos[0] + 5, pos[1] + 5))
        except TypeError:
            draw(object_list['error'], (pos[0] + 5, pos[1] + 5))


def add_thing_bag(thing, number=1, o_type='object'):
    for n2 in range(len(player.bag)):
        if player.bag[n2][0] == thing and player.bag[n2][2] == o_type:
            if player.bag[n2][1] >= 64:
                continue
            player.bag[n2][1] = player.bag[n2][1] + number
            break
        elif player.bag[n2] == [0, 0, 0]:
            player.bag[n2] = [thing, number, o_type]
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


def bag_block(pos, n2, drags=0, bag=None):
    global player, mouse, drag, texture_list
    if bag is None:
        bag = player.bag
    if n2 in drag[drags]:
        pygame.draw.rect(screen, (128, 128, 128), (pos[0], pos[1], 50, 50))
    if pos[0] < mouse.xy[0] < (pos[0] + 50) and pos[1] < mouse.xy[1] < (pos[1] + 50):
        pygame.draw.rect(screen, (128, 128, 128), (pos[0], pos[1], 50, 50))
        if mouse.up[0] and len(drag[drags]) == 0:
            if mouse.hold == [0, 0, 0]:
                mouse.hold = bag[n2]
                bag[n2] = [0, 0, 0]
            elif bag[n2][0] == mouse.hold[0]:
                if (mouse.hold[1] + bag[n2][1]) > 64:
                    mouse.hold[1] = mouse.hold[1] - (64 - bag[n2][1])
                    bag[n2][1] = 64
                else:
                    bag[n2][1] = bag[n2][1] + mouse.hold[1]
                    mouse.hold = [0, 0, 0]
            elif bag[n2] == [0, 0, 0] and mouse.hold != [0, 0, 0]:
                if time.time() - mouse.last2 > 0.2:
                    x = mouse.hold
                    mouse.hold = bag[n2]
                    bag[n2] = x
                else:
                    w1 = mouse.hold[1]
                    for n3 in range(36):
                        if w1 < 64 and bag[n3][0] == mouse.hold[0] and bag[n3][1] != 64:
                            if (bag[n3][1] + w1) <= 64:
                                w1 = w1 + bag[n3][1]
                                bag[n3] = [0, 0, 0]
                            elif (bag[n3][1] + w1) > 64:
                                bag[n3] = [bag[n3][0], (bag[n3][1] + w1) - 64]
                                w1 = 64
                    bag[n2] = [mouse.hold[0], w1, mouse.hold[2]]
                    mouse.hold = [0, 0, 0]
        elif mouse.up[2]:
            if mouse.hold == [0, 0, 0] and bag[n2][1] > 0.2:
                mouse.hold[0] = bag[n2][0]
                x = bag[n2][1] // 2
                mouse.hold[1] = x
                bag[n2][1] = bag[n2][1] - x
            elif (bag[n2][0] == mouse.hold[0] or bag[n2] == [0, 0, 0]) and mouse.hold[1] > 0:
                if bag[n2][1] != 64:
                    bag[n2][1] = bag[n2][1] + 1
                    bag[n2][0] = mouse.hold[0]
                    mouse.hold[1] = mouse.hold[1] - 1
        elif mouse.press[0] and time.time() - mouse.start_press > 0.2:
            if mouse.hold != [0, 0, 0] and bag[n2] == [0, 0, 0] and mouse.hold[1] != 1:
                if not (n2 in drag[drags]):
                    drag[drags].append(n2)
    draw(texture_list['bag1'], pos)
    goods_type(bag[n2], pos, True)
    if len(drag[drags]) != 0 and mouse.hold != [0, 0, 0] and mouse.press[0]:
        if mouse.hold[1] >= len(drag[drags]):
            nn = mouse.hold[1] // len(drag[drags])
            for m in drag[drags]:
                player.bag[m] = [mouse.hold[0], nn, 'object']
        else:
            print(5)
            for m in drag[drags]:
                player.bag[m] = [0, 0, 0]
            drag[drags] = []
    if len(drag[drags]) != 0 and mouse.hold != [0, 0, 0] and mouse.up[0]:
        print(12)
        if mouse.hold[1] >= len(drag[drags]):
            nn = mouse.hold[1] // len(drag[drags])
            nx = mouse.hold[1] % len(drag[drags])
            for m in drag[drags]:
                player.bag[m] = [mouse.hold[0], nn, 'object']
                print(m, player.bag[m])
            if nx > 0:
                print(4)
                mouse.hold[1] = nx
            else:
                mouse.hold = [0, 0, 0]
    if len(drag[drags]) != 0 and not mouse.press[0]:
        drag[drags] = []


def draw_game():  # 绘制游戏画面
    global get_cd, last_get, screen_size, pzx, mouse, player, show_f3, cover, pause, backgroud, seed, jm, run, show_bag, resource_box, drag, setting_back, full_screen, screen, screen_size_1
    mouse.point_xz = [math.ceil((player.x + mouse.xy[0]) / 64) - screen_size[0] // 128, math.floor((player.z + mouse.xy[1]) / 64) - screen_size[1] // 128]
    pzx = []
    resource_box = []
    draw_block()
    for n3 in range(9):
        ipos = ((screen_size[0] // 2) - 225 + n3 * 50, screen_size[1] - 50)
        draw(texture_list['bag1'], ipos)
        if player.choose_bag == n3:
            draw(texture_list['choose_bag'], ipos)
        goods_type(player.bag[n3], ipos, True)
    if player.left_hand[0] != [0, 0, 0]:
        draw(texture_list['bag1'], ((screen_size[0] // 2) - 225 - 80, screen_size[1] - 50))
        goods_type(player.left_hand[0], ((screen_size[0] // 2) - 225 - 80, screen_size[1] - 50), True)
    if show_bag:
        player.x_offset, player.z_offset = 0, 0
        get_cd = 0
        draw(backgroud, (0, 0))
        pygame.draw.rect(screen, (220, 220, 220), (screen_size[0] / 2 - 235, screen_size[1] / 2 - 260, 470, 420))
        pygame.draw.rect(screen, (0, 0, 0), (screen_size[0] / 2 - 165, screen_size[1] / 2 - 220, 64, 100))
        draw(texture_list['player'], (screen_size[0] / 2 - 165, screen_size[1] / 2 - 220))
        for n2 in range(36):
            bag_block((screen_size[0] / 2 - 225 + (n2 % 9) * 50, screen_size[1] / 2 + 100 - n2 // 9 * 50), n2, 0)
        for n2 in range(4):
            bag_block((screen_size[0] / 2 - 235, screen_size[1] / 2 - 205 + (n2 - 1) * 50), n2, 1, player.clothe)
        bag_block((screen_size[0] / 2 - 101, screen_size[1] / 2 - 100), 0, 2, player.left_hand)
        if mouse.hold != [0, 0, 0]:
            goods_type(mouse.hold, (mouse.xy[0] - 20, mouse.xy[1] - 20), True)
        if mouse.hold[1] <= 0:
            mouse.hold = [0, 0, 0]
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
            pygame.draw.rect(screen, (200, 200, 0), (n3[0], n3[1], n3[2], n3[3]), 1)
        pygame.draw.rect(screen, (255, 255, 255), (player.pzx[0], player.pzx[1], (player.pzx[2] - player.pzx[0]), (player.pzx[3] - player.pzx[1])), 1)
    if pause:
        draw(backgroud, (0, 0))
        if anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 - 80, 200, 40), '回到游戏', (128, 128, 128)):
            pause = False
        elif anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 - 20, 200, 40), '返回主菜单', (128, 128, 128)):
            jm = 1
        elif anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 40, 200, 40), '退出至桌面', (128, 128, 128)):
            run = False
        elif anniu((screen_size[0] / 2 - 100, screen_size[1] / 2 + 100, 200, 40), '设置', (128, 128, 128)):
            setting_back = 2
            jm = 5

    if not pause:
        if K_t in presse_up:
            player.x = mouse.point_xz[0] * 64
            player.z = mouse.point_xz[1] * 64
        if K_e in presse_up:
            if show_bag:
                show_bag = False
                if mouse.hold != [0, 0, 0]:
                    add_thing_bag(mouse.hold[0], mouse.hold[1])
                    mouse.hold = [0, 0, 0]
            else:
                show_bag = True
        if not show_bag:
            for box in resource_box:
                if box[0] < mouse.xy[0] < box[0] + box[2] and box[1] < mouse.xy[1] < box[1] + box[3]:
                    if long(box[0] + box[2] / 2, box[1] + box[3] / 2, screen_size[0] / 2, screen_size[1] / 2) <= player.longest_touch:
                        draw(texture_list['choose_ul'], (box[0], box[1]))
                        draw(texture_list['choose_ur'], (box[0] + box[2] - 32, box[1]))
                        draw(texture_list['choose_dl'], (box[0], box[1] + box[3] - 32))
                        draw(texture_list['choose_dr'], (box[0] + box[2] - 32, box[1] + box[3] - 32))
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
                                        pygame.draw.rect(screen, (0, 0, 0), (box[0], box[1] - 20, box[2], 20))
                                        pygame.draw.rect(screen, (0, 255, 0), (box[0] + 5, box[1] - 15, int(get_cd / 100 * (box[2] - 10)), 10))
                                    if last_get != [box[5], box[6]] and get_cd != 0:
                                        last_get = [box[5], box[6]]
                                        get_cd = 0
                                    elif get_cd == 0:
                                        last_get = [box[5], box[6]]
                                        get_cd = get_cd + 1
                    else:
                        draw(texture_list['no_choose_ul'], (box[0], box[1]))
                        draw(texture_list['no_choose_ur'], (box[0] + box[2] - 32, box[1]))
                        draw(texture_list['no_choose_dl'], (box[0], box[1] + box[3] - 32))
                        draw(texture_list['no_choose_dr'], (box[0] + box[2] - 32, box[1] + box[3] - 32))
                    break
                elif last_get == [box[5], box[6]]:
                    get_cd = 0
            press()
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
    if mouse.wheel == -1:
        if player.choose_bag < 8:
            player.choose_bag = player.choose_bag + 1
        else:
            player.choose_bag = 0
    elif mouse.wheel == 1:
        if player.choose_bag > 0:
            player.choose_bag = player.choose_bag - 1
        else:
            player.choose_bag = 8
    if presse[K_f]:
        add_thing_bag(2, 1)
    if K_ESCAPE in presse_up:
        if show_bag:
            show_bag = False
            if mouse.hold != [0, 0, 0]:
                add_thing_bag(mouse.hold[0], mouse.hold[1])
                mouse.hold = [0, 0, 0]
        else:
            if pause:
                pause = False
            else:
                pause = True
    for n1 in range(36):
        if player.bag[n1] != [0, 0, 0]:
            if player.bag[n1][1] <= 0:
                player.bag[n1] = [0, 0, 0]


while run:
    presse = pygame.key.get_pressed()
    fps = (clock.get_fps() * 10) // 10
    mouse.xy = pygame.mouse.get_pos()
    mouse.x = mouse.xy[0]
    mouse.y = mouse.xy[1]
    if not full_screen:
        if screen_size != (screen.get_width(), screen.get_height()):
            seed_input = input_rect((screen.get_width() / 2 - 150, screen.get_height() / 2 - 20, 300, 40))
            screen_size = (screen.get_width(), screen.get_height())
            player.pzx = [int(screen_size[0] / 2 - 10), int(screen_size[1] / 2), int(screen_size[0] / 2 + 10), int(screen_size[1] / 2 + 20)]
            backgroud = pygame.Surface(screen_size)
            backgroud.set_alpha(150)
            backgroud.fill((0, 0, 0))
    else:
        player.pzx = [int(1920 / 2 - 10), int(1080 / 2), int(1920 / 2 + 10), int(1080 / 2 + 20)]
        backgroud = pygame.Surface((1920, 1080))
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
    if int(time.time()) > next_music_time and len(music_list) != 0:
        pygame.mixer.music.stop()
        r = random.randint(0, len(music_list) - 1)
        music_list[r].set_volume(music_volume)
        pygame.mixer.Sound.play(music_list[r])
        next_music_time = next_music_time + int(music_list[r].get_length())
    if presse[K_ESCAPE] and jm != 2:
        run = False
    if K_F11 in presse_up:
        if not full_screen:
            full_screen = True
            screen_size_1 = screen_size
            screen_size = (1920, 1080)
            screen = pygame.display.set_mode((1920, 1080), flags=RESIZABLE | FULLSCREEN | HWSURFACE)
        else:
            full_screen = False
            screen_size = screen_size_1
            player.pzx = [int(screen_size[0] / 2 - 10), int(screen_size[1] / 2), int(screen_size[0] / 2 + 10), int(screen_size[1] / 2 + 20)]
            screen = pygame.display.set_mode(screen_size, flags=RESIZABLE)
    if jm == 2:  # 游戏运行界面
        draw_game()
    elif jm == 1:  # 游戏主界面
        for iy in range(int(screen_size[1] / 64) + 1):
            for ix in range(int(screen_size[0] / 64) + 1):
                draw(texture_list['mud'], (ix * 64, iy * 64))
        if anniu((int(screen_size[0] / 2 - 100), int(screen_size[1] / 2 - 20), 200, 40), '单人游戏', (120, 120, 120)):
            seed_input = input_rect((screen.get_width() / 2 - 150, screen.get_height() / 2 - 20, 300, 40))
            jm = 3
            seed = ''
            pause = False
            show_bag = False
            player.bag = start_player_bag.copy()
        if anniu((int(screen_size[0] / 2 - 100), int(screen_size[1] / 2 + 30), 200, 40), '星系', (120, 120, 120)):
            jm = 4
        if anniu((int(screen_size[0] / 2 - 100), int(screen_size[1] / 2 + 80), 200, 40), '设置', (120, 120, 120)):
            setting_back = 1
            jm = 5
        if len(music_list) != 0:
            write(str(music_path[r][:-4]), (0, screen_size[1] - 20), 20)
    elif jm == 4:  # 星系界面
        galaxy()
    elif jm == 5:  # 设置界面
        for iy in range(int(screen_size[1] / 64) + 1):
            for ix in range(int(screen_size[0] / 64) + 1):
                draw(texture_list['mud'], (ix * 64, iy * 64))
        if anniu((0, screen_size[1] - 40, 100, 40), '返回', (120, 120, 120)):
            jm = setting_back
        music_list[r].set_volume(press_line((100, 100, 200, 40), music_list[r].get_volume(), 0, 1, '音量'))
        music_volume = music_list[r].get_volume()
    elif jm == 3:  # 游戏创建界面
        for iy in range(int(screen_size[1] / 64) + 1):
            for ix in range(int(screen_size[0] / 64) + 1):
                draw(texture_list['mud'], (ix * 64, iy * 64))
        write('种子', (screen.get_width() / 2 - 160, screen.get_height() / 2 - 80), 40, (255, 255, 255))
        seed = seed_input.get_string()
        if anniu((screen.get_width() / 2 - 125, screen.get_height() / 2 + 30, 250, 40), '创建新的世界', (120, 120, 120)):
            if seed is None:
                seed = random.randint(1, 10000)
                m1 = get_map(128, str(seed))
                the_map = m1[0]
                player.x = m1[1]
                player.y = m1[2]
                jm = 2
            else:
                m1 = get_map(128, str(seed))
                the_map = m1[0]
                player.x = m1[1]
                player.y = m1[2]
                jm = 2
        if anniu((screen.get_width() / 2 - 125, screen.get_height() / 2 + 80, 250, 40), '取消', (120, 120, 120)):
            jm = 1
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
    presse_up = []
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
            presse_up.append(e)
        if event.type == MOUSEWHEEL:
            mouse.wheel = event.y
        # if event.type == MOUSEBUTTONUP:  # 鼠标放开检测
        #    mouse.up = pygame.mouse.get_pressed()

setting = open(r'./data/setting.ini', 'w+', encoding='utf-8')
setting.write(str(music_volume))
setting.close()
pygame.quit()
