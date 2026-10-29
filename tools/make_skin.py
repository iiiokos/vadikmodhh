"""Генерирует textures/entity/vadik.png (64x64) для VadikModel.

Запуск: python3 tools/make_skin.py <out.png> [preview.png]
"""
import sys
from PIL import Image

out = sys.argv[1]
preview = sys.argv[2] if len(sys.argv) > 2 else None

img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
px = img.load()


def tint(c, d):
    return (max(0, min(255, c[0] + d)), max(0, min(255, c[1] + d)), max(0, min(255, c[2] + d)), 255)


def nz(x, y, s=0):
    h = (x * 73856093) ^ (y * 19349663) ^ (s * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFF
    return (h % 7) - 3  # -3..3


SKIN = (234, 194, 164)
SKIN_S = (212, 170, 140)   # тени
SKIN_L = (243, 208, 180)   # блик
HAIR = (66, 44, 33)
HAIR_D = (46, 30, 22)
HAIR_L = (94, 66, 48)
SHIRT = (26, 30, 48)
SHIRT_D = (18, 21, 36)
SHIRT_L = (38, 44, 68)
DENIM = (62, 88, 128)
DENIM_D = (46, 68, 104)
DENIM_L = (84, 112, 154)
STITCH = (140, 160, 190)
SHOE = (52, 52, 58)
SOLE = (226, 226, 226)
FRAME = (32, 32, 36)
WHITE = (248, 248, 248)
PUPIL = (58, 80, 112)
BAND = (236, 228, 190)
BAND_D = (200, 192, 150)
BLACK = (20, 20, 22)


def put(x, y, c):
    px[x, y] = (c[0], c[1], c[2], 255)


def fill(x, y, w, h, base, amp=1, seed=0):
    for j in range(y, y + h):
        for i in range(x, x + w):
            px[i, j] = tint(base, nz(i, j, seed) * amp)


def hair(x, y, w, h, seed=0, vertical=True):
    """Пряди: чередующиеся полосы тёмный/средний/светлый."""
    for j in range(y, y + h):
        for i in range(x, x + w):
            k = (i if vertical else j) * 5 + seed
            band = k % 5
            base = HAIR_D if band == 0 else HAIR_L if band == 3 else HAIR
            px[i, j] = tint(base, nz(i, j, seed) )


def box_faces(u, v, w, h, d):
    return {
        "top": (u + d, v, w, d),
        "bottom": (u + d + w, v, w, d),
        "right": (u, v + d, d, h),
        "front": (u + d, v + d, w, h),
        "left": (u + d + w, v + d, d, h),
        "back": (u + 2 * d + w, v + d, w, h),
    }


# =====================================================================
# ГОЛОВА (базовый слой): top(8,0) bottom(16,0) right(0,8) front(8,8) left(16,8) back(24,8)
# =====================================================================
hair(8, 0, 8, 8, seed=1, vertical=False)
for j in range(0, 8):                      # пробор по центру макушки
    put(11 + (j % 2), j, HAIR_D)
fill(16, 0, 8, 8, SKIN_S)                  # низ головы

fill(8, 8, 8, 8, SKIN, amp=1, seed=2)      # лицо
hair(8, 8, 8, 2, seed=3)                   # чёлка (верх лица)
for x in (8, 9, 14, 15):
    put(x, 10, HAIR)
put(8, 11, HAIR_D); put(15, 11, HAIR_D)    # виски
# брови (усталые, чуть нахмуренные)
for x in (9, 10):
    put(x, 11, HAIR_D)
for x in (13, 14):
    put(x, 11, HAIR_D)
# глаза (под очками), ряд 12
put(9, 12, WHITE);  put(10, 12, PUPIL)
put(13, 12, PUPIL); put(14, 12, WHITE)
put(10, 12, (30, 40, 60)); put(13, 12, (30, 40, 60))
# мешки под глазами
for x in (9, 10, 13, 14):
    put(x, 13, SKIN_S)
# нос и рот
put(11, 13, SKIN_S); put(12, 13, SKIN_L)
put(12, 14, SKIN_S)
for x in (11, 12):
    put(x, 14, (196, 128, 118))
put(11, 15, SKIN_S); put(12, 15, SKIN_S)   # подбородок/тень

# правая сторона (x0..7): col0 = затылок, col7 = к лицу
hair(0, 8, 5, 8, seed=4)
hair(5, 8, 3, 3, seed=4)
fill(5, 11, 3, 5, SKIN, amp=1, seed=5)
for j in (11, 12, 13):
    put(5, j, SKIN_S); put(6, j, SKIN_S)   # ухо
put(6, 12, SKIN_L)
# левая сторона (x16..23): col16 = к лицу, col23 = затылок
hair(19, 8, 5, 8, seed=6)
hair(16, 8, 3, 3, seed=6)
fill(16, 11, 3, 5, SKIN, amp=1, seed=7)
for j in (11, 12, 13):
    put(17, j, SKIN_S); put(18, j, SKIN_S)
put(17, 12, SKIN_L)

hair(24, 8, 8, 8, seed=8)                  # затылок
for j in range(8, 16):
    put(27 + (j % 2), j, HAIR_D)

# =====================================================================
# HAT-слой: ободок (дужка от уха до уха через макушку)
# top(40,0) right(32,8) front(40,8) left(48,8) back(56,8)
# =====================================================================
for i in range(40, 48):
    put(i, 3, BLACK)
for j in range(8, 11):
    put(35, j, BLACK)
    put(52, j, BLACK)
put(35, 11, (50, 50, 54)); put(52, 11, (50, 50, 54))

# =====================================================================
# ТЕЛО: top(20,16) bottom(28,16) right(16,20) front(20,20) left(28,20) back(32,20)
# =====================================================================
fill(20, 16, 8, 4, SHIRT, amp=1, seed=10)
fill(28, 16, 8, 4, SHIRT_D, amp=1, seed=11)
fill(20, 20, 8, 12, SHIRT, amp=1, seed=12)      # перед
fill(32, 20, 8, 12, SHIRT_D, amp=1, seed=13)    # спина
fill(16, 20, 4, 12, SHIRT_D, amp=1, seed=14)    # правый бок
fill(28, 20, 4, 12, SHIRT_D, amp=1, seed=15)    # левый бок
# V-вырез и ворот
for x, y in ((22, 20), (23, 20), (24, 20), (25, 20), (23, 21), (24, 21), (23, 22)):
    put(x, y, SKIN)
put(22, 21, SHIRT_L); put(25, 21, SHIRT_L); put(22, 22, SHIRT_L); put(24, 22, SHIRT_L)
# складки на футболке
for (x, y) in ((21, 25), (22, 26), (26, 24), (25, 27), (24, 29), (21, 29), (26, 30)):
    put(x, y, SHIRT_L)
for (x, y) in ((23, 25), (24, 26), (22, 28), (25, 29)):
    put(x, y, SHIRT_D)
# подол
fill(20, 31, 8, 1, SHIRT_D)
fill(32, 31, 8, 1, (14, 16, 28))
# складки на спине
for (x, y) in ((34, 24), (35, 25), (37, 27), (36, 29)):
    put(x, y, (30, 34, 54))
# шея
fill(20, 16, 8, 1, SKIN_S)

# =====================================================================
# ПРАВАЯ РУКА: top(44,16) bottom(48,16) right(40,20) front(44,20) left(48,20) back(52,20)
# ЛЕВАЯ РУКА:  top(36,48) bottom(40,48) right(32,52) front(36,52) left(40,52) back(44,52)
# =====================================================================
for (tx, ty, bx, by, faces_x, fy) in (
        (44, 16, 48, 16, (40, 44, 48, 52), 20),
        (36, 48, 40, 48, (32, 36, 40, 44), 52)):
    fill(tx, ty, 4, 4, SHIRT, amp=1, seed=20)
    fill(bx, by, 4, 4, SKIN_S)
    for k, x0 in enumerate(faces_x):
        fill(x0, fy, 4, 12, SKIN, amp=1, seed=21 + k)
        fill(x0, fy, 4, 5, SHIRT if k in (1, 3) else SHIRT_D, amp=1, seed=25 + k)  # рукав
        fill(x0, fy + 4, 4, 1, SHIRT_D)                                          # край рукава
        put(x0 + 1, fy + 6, SKIN_L)
        for j in (fy + 10, fy + 11):                                              # кисть светлее
            for i in range(x0, x0 + 4):
                put(i, j, SKIN_L if (i + j) % 3 else SKIN)

# =====================================================================
# ПРАВАЯ НОГА: top(4,16) bottom(8,16) right(0,20) front(4,20) left(8,20) back(12,20)
# ЛЕВАЯ НОГА:  top(20,48) bottom(24,48) right(16,52) front(20,52) left(24,52) back(28,52)
# =====================================================================
for (tx, ty, bx, by, faces_x, fy) in (
        (4, 16, 8, 16, (0, 4, 8, 12), 20),
        (20, 48, 24, 48, (16, 20, 24, 28), 52)):
    fill(tx, ty, 4, 4, DENIM, amp=1, seed=30)
    fill(bx, by, 4, 4, SKIN_S)
    for k, x0 in enumerate(faces_x):
        fill(x0, fy, 4, 12, SKIN, amp=1, seed=31 + k)            # голень
        fill(x0, fy, 4, 8, DENIM_D if k in (0, 2) else DENIM, amp=2, seed=35 + k)  # шорты
        fill(x0, fy + 7, 4, 1, DENIM_D)                           # подгиб
        for i in range(x0, x0 + 4):
            if i % 2 == 0:
                put(i, fy + 6, STITCH)                            # строчка
        fill(x0, fy + 9, 4, 1, SKIN_S)                            # тень под шортами
        fill(x0, fy + 10, 4, 1, SHOE)                             # кроссовки
        fill(x0, fy + 11, 4, 1, SOLE)
    put(faces_x[1] + 1, fy + 10, (90, 90, 98))                    # блик на носке

# =====================================================================
# ДОП. ДЕТАЛИ МОДЕЛИ (свободные области текстуры)
# =====================================================================
# hair_back: box(8x10x2) @ (0,32)
for name, (x, y, w, h) in box_faces(0, 32, 8, 10, 2).items():
    hair(x, y, w, h, seed=40 + x)
# нижние кончики прядей чуть темнее
for i in range(0, 20):
    put(i, 43, HAIR_D)

# hair_side_r @ (20,32) 1x10x5 ; hair_side_l @ (32,32)
for ox in (20, 32):
    for name, (x, y, w, h) in box_faces(ox, 32, 1, 10, 5).items():
        hair(x, y, w, h, seed=50 + x)

# fringe @ (44,32) 8x2x1
for name, (x, y, w, h) in box_faces(44, 32, 8, 2, 1).items():
    hair(x, y, w, h, seed=60 + x)
f = box_faces(44, 32, 8, 2, 1)["front"]
for k in range(f[2]):                      # неровный край чёлки
    if k % 3 == 1:
        px[f[0] + k, f[1] + 1] = (0, 0, 0, 0)

# lens @ (44,36) 3x3x1 : оправа, центр прозрачный
for name, (x, y, w, h) in box_faces(44, 36, 3, 3, 1).items():
    fill(x, y, w, h, FRAME)
fx, fy_, fw, fh = box_faces(44, 36, 3, 3, 1)["front"]
px[fx + 1, fy_ + 1] = (0, 0, 0, 0)         # стекло
put(fx, fy_, (70, 70, 78))                 # блик на оправе

# bridge @ (52,36) 1x1x1
for name, (x, y, w, h) in box_faces(52, 36, 1, 1, 1).items():
    fill(x, y, w, h, FRAME)

# temple @ (44,40) 1x1x5
for name, (x, y, w, h) in box_faces(44, 40, 1, 1, 5).items():
    fill(x, y, w, h, FRAME)

# earbud @ (56,36) 1x2x1
for name, (x, y, w, h) in box_faces(56, 36, 1, 2, 1).items():
    fill(x, y, w, h, WHITE)
put(57, 37, (225, 225, 230))

# wristband @ (0,48) 4x1x4
for name, (x, y, w, h) in box_faces(0, 48, 4, 1, 4).items():
    fill(x, y, w, h, BAND, amp=1, seed=70)
    put(x, y, BAND_D)

# pockets @ (0,56) 1x3x3
for name, (x, y, w, h) in box_faces(0, 56, 1, 3, 3).items():
    fill(x, y, w, h, DENIM_L, amp=1, seed=80)
ff = box_faces(0, 56, 1, 3, 3)["right"]
for i in range(ff[2]):
    put(ff[0] + i, ff[1], DENIM_D)                       # клапан
put(ff[0] + 1, ff[1] + 1, (200, 200, 210))               # пуговица
for name in ("front", "back", "left", "top", "bottom"):
    x, y, w, h = box_faces(0, 56, 1, 3, 3)[name]
    for j in range(y, y + h):
        put(x, j, DENIM_D)

img.save(out)
print("saved", out, img.size)
if preview:
    bg = Image.new("RGBA", (64, 64), (200, 200, 205, 255))
    bg.alpha_composite(img)
    bg.resize((512, 512), Image.NEAREST).save(preview)
    print("preview", preview)
