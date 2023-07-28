import random

map1 = []


def update(x, y, size=1):  # 方块更新
    global map1
    for yi in range(size * 2 - 1):
        for xi in range(size * 2 - 1):
            if map1[(yi + y - size + 1) % len(map1)][(xi + x - size + 1) % len(map1)][0] == 1:
                do = ''
                le = ''
                ri = ''
                if map1[yi + y - size + 1][(xi + x + 1 - size + 1) % len(map1)][0] == 1:
                    ri = 'r'
                if map1[yi + y - size + 1][xi + x - 1 - size + 1][0] == 1:
                    le = 'l'
                if map1[(yi + y + 1 - size + 1) % len(map1)][xi + x - size + 1][0] == 1:
                    do = 'd'
                map1[(yi + y) - size + 1 % len(map1)][(xi + x - size + 1) % len(map1)] = [1, 'u' + do + le + ri]


def fill(x, y, size, block, the_block_type):
    global map1
    for yi in range(size * 2 - 1):
        for xi in range(size * 2 - 1):
            map1[(yi + y - size + 1) % len(map1)][(xi + x - size + 1) % len(map1)] = [block, the_block_type]


def get_map(size=32, map_seed=''):  # 获取地图
    global map1
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
    map1 = []
    iron = []
    for y in range(len(cmap)):
        c = []
        for x in range(len(cmap[y])):
            if cmap[y][x] == 0:
                random.seed(str(map_seed) + str(x) + str(y))
                t = random.randint(0, 3)
                random.seed(str(map_seed) + str(x) + str(y))
                mineral = random.random()  # 矿物值
                if mineral > 0.96:
                    c.append([0, [t, 'iron']])
                    iron.append((x, y))
                elif 0.03 < mineral < 0.1:
                    c.append([0, [t, 'grass']])
                elif mineral < 0.03:
                    c.append([0, [t, 'tree']])
                else:
                    c.append([0, [t]])
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
        map1.append(c)
    for n4 in iron:
        random.seed(str(map_seed) + str(n4[0]) + str(n4[1]))
        t = random.randint(0, 3)
        map1[n4[1] % len(map1)][n4[0] % len(map1)] = [0, [t, 'iron']]
        update(n4[0], n4[1], 1)
    find_run = 1
    wx = 0
    wy = 0
    while find_run == 0:
        random.seed(map_seed + str(find_run) + str(wx))
        wx = random.randint(1, len(map1) - 2)
        random.seed(map_seed + str(find_run) + str(wy))
        wy = random.randint(1, len(map1) - 2)
        if map1[wy][wx][0] == 0 or map1[wy][wx][0] == 3:
            fill(wx, wy, 2, 0, 0)
            update(wx, wy, 3)
            find_run = 0
        else:
            find_run = find_run + 1
    return [map1, wx * 64, wy * 64]
