from PIL import Image, ImageDraw
import arcade

_cache = {}


def _key(*parts):
    return tuple(parts)


def _tint(color, factor):
    return (
        max(0, min(255, int(color[0] * factor))),
        max(0, min(255, int(color[1] * factor))),
        max(0, min(255, int(color[2] * factor))),
    )


def rect_texture(width, height, fill, outline=None, outline_thickness=2, accents=None):
    key = _key("rect", width, height, fill, outline, outline_thickness, tuple(accents or []))
    if key in _cache:
        return _cache[key]
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if outline:
        draw.rectangle([0, 0, width - 1, height - 1], fill=outline)
        pad = outline_thickness
        draw.rectangle([pad, pad, width - 1 - pad, height - 1 - pad], fill=fill)
    else:
        draw.rectangle([0, 0, width - 1, height - 1], fill=fill)
    if accents:
        for x, y, w, h, col in accents:
            draw.rectangle([x, y, x + w - 1, y + h - 1], fill=col)
    tex = arcade.Texture(img)
    _cache[key] = tex
    return tex


def brick_texture(size, base, mortar):
    key = _key("brick", size, base, mortar)
    if key in _cache:
        return _cache[key]
    img = Image.new("RGBA", (size, size), base)
    draw = ImageDraw.Draw(img)
    brick_h = max(4, size // 4)
    brick_w = max(6, size // 3)
    for y in range(0, size, brick_h):
        draw.rectangle([0, y, size, y + 1], fill=mortar)
        offset = 0 if (y // brick_h) % 2 == 0 else brick_w // 2
        for x in range(-offset, size, brick_w):
            draw.rectangle([x, y, x + 1, y + brick_h], fill=mortar)
    tex = arcade.Texture(img)
    _cache[key] = tex
    return tex


def plank_texture(size, base, dark):
    key = _key("plank", size, base, dark)
    if key in _cache:
        return _cache[key]
    img = Image.new("RGBA", (size, size), base)
    draw = ImageDraw.Draw(img)
    plank_w = max(4, size // 4)
    for i in range(0, size, plank_w):
        draw.rectangle([i, 0, i + 1, size], fill=dark)
    draw.rectangle([0, 0, size - 1, size - 1], outline=dark)
    tex = arcade.Texture(img)
    _cache[key] = tex
    return tex


def floor_texture(size, base, accent):
    key = _key("floor", size, base, accent)
    if key in _cache:
        return _cache[key]
    img = Image.new("RGBA", (size, size), base)
    draw = ImageDraw.Draw(img)
    step = max(6, size // 3)
    for y in range(2, size, step):
        for x in range(2, size, step):
            draw.rectangle([x, y, x + 2, y + 2], fill=accent)
    tex = arcade.Texture(img)
    _cache[key] = tex
    return tex


def chest_texture(size, base, outline, lid, latch):
    key = _key("chest", size, base, outline, lid, latch)
    if key in _cache:
        return _cache[key]
    dark = _tint(base, 0.7)
    mid = _tint(base, 0.9)
    accents = [
        (0, 0, size, max(6, size // 3), lid),  # lid
        (0, max(6, size // 3) - 1, size, 2, outline),
        (2, size // 2 - 2, size - 4, 2, outline),
        (2, size // 2 + 2, size - 4, 2, dark),
        (size // 2 - 3, size // 2 - 3, 6, 6, latch),  # lock
        (2, size - 4, size - 4, 2, outline),
        (3, 3, size // 3, 2, mid),
        (3, size - 8, size // 3, 2, dark),
        (2, size // 2, 3, size // 2 - 2, outline),
        (size - 5, size // 2, 3, size // 2 - 2, outline),
    ]
    tex = rect_texture(size, size, base, outline=outline, outline_thickness=2, accents=accents)
    _cache[key] = tex
    return tex


def enemy_frame(size, base, outline, accents, shape="rect"):
    key = _key("enemy", size, base, outline, tuple(accents), shape)
    if key in _cache:
        return _cache[key]
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if shape == "diamond":
        pts = [(size // 2, 1), (size - 2, size // 2), (size // 2, size - 2), (1, size // 2)]
        draw.polygon(pts, fill=outline)
        inset = 3
        pts2 = [(size // 2, inset), (size - inset, size // 2), (size // 2, size - inset), (inset, size // 2)]
        draw.polygon(pts2, fill=base)
    elif shape == "chunky":
        draw.rectangle([0, 0, size - 1, size - 1], fill=outline)
        draw.rectangle([3, 3, size - 4, size - 4], fill=base)
        draw.rectangle([2, size // 3, size - 3, size // 3 + 2], fill=_tint(base, 0.8))
    elif shape == "round":
        radius = max(4, size // 6)
        try:
            draw.rounded_rectangle([1, 1, size - 2, size - 2], radius=radius, fill=base, outline=outline, width=2)
        except Exception:
            draw.rectangle([1, 1, size - 2, size - 2], fill=base, outline=outline)
    elif shape == "hex":
        pts = [
            (size // 4, 1),
            (size * 3 // 4, 1),
            (size - 2, size // 2),
            (size * 3 // 4, size - 2),
            (size // 4, size - 2),
            (1, size // 2),
        ]
        draw.polygon(pts, fill=outline)
        inset = 3
        pts2 = [
            (size // 4 + inset, inset),
            (size * 3 // 4 - inset, inset),
            (size - inset, size // 2),
            (size * 3 // 4 - inset, size - inset),
            (size // 4 + inset, size - inset),
            (inset, size // 2),
        ]
        draw.polygon(pts2, fill=base)
    else:
        draw.rectangle([0, 0, size - 1, size - 1], fill=outline)
        draw.rectangle([2, 2, size - 3, size - 3], fill=base)

    if accents:
        for x, y, w, h, col in accents:
            draw.rectangle([x, y, x + w - 1, y + h - 1], fill=col)
    tex = arcade.Texture(img)
    _cache[key] = tex
    return tex


def weapon_texture(width, height, base, outline, barrel, grip):
    key = _key("weapon", width, height, base, outline, barrel, grip)
    if key in _cache:
        return _cache[key]
    size = max(width, height)
    pad_x = (size - width) // 2
    pad_y = (size - height) // 2
    accents = [
        (pad_x + width - max(3, width // 4), pad_y + height // 3, max(3, width // 4), max(2, height // 5), barrel),
        (pad_x + width // 4, pad_y + height // 2, max(3, width // 6), max(3, height // 3), grip),
        (pad_x + 2, pad_y + height - 4, width - 4, 2, outline),
    ]
    tex = rect_texture(size, size, base, outline=outline, outline_thickness=2, accents=accents)
    _cache[key] = tex
    return tex


def sword_texture(size, blade, outline, hilt, pommel):
    key = _key("sword", size, blade, outline, hilt, pommel)
    if key in _cache:
        return _cache[key]
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cy = size // 2
    # blade (to the right)
    draw.rectangle([6, cy - 2, size - 6, cy + 2], fill=blade)
    draw.rectangle([5, cy - 3, size - 5, cy + 3], outline=outline)
    draw.rectangle([8, cy - 1, size - 10, cy - 1], fill=_tint(blade, 1.15))
    # guard
    draw.rectangle([4, cy - 6, 8, cy + 6], fill=hilt)
    # handle
    draw.rectangle([2, cy - 2, 5, cy + 2], fill=outline)
    # pommel
    draw.rectangle([0, cy - 3, 2, cy + 3], fill=pommel)
    tex = arcade.Texture(img)
    _cache[key] = tex
    return tex


def axe_texture(size, head, outline, handle):
    key = _key("axe", size, head, outline, handle)
    if key in _cache:
        return _cache[key]
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cy = size // 2
    # handle (left to right)
    draw.rectangle([2, cy - 1, size - 6, cy + 1], fill=handle)
    # head
    draw.rectangle([size - 10, cy - 6, size - 2, cy + 6], fill=head)
    draw.rectangle([size - 11, cy - 7, size - 1, cy + 7], outline=outline)
    draw.rectangle([size - 9, cy - 5, size - 6, cy + 5], fill=_tint(head, 1.1))
    draw.rectangle([size - 5, cy - 5, size - 3, cy + 5], fill=_tint(head, 0.9))
    tex = arcade.Texture(img)
    _cache[key] = tex
    return tex


def gun_texture(size, base, outline, barrel, grip, stock=None, profile="pistol"):
    key = _key("gun", size, base, outline, barrel, grip, stock, profile)
    if key in _cache:
        return _cache[key]
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cy = size // 2
    if profile == "rifle":
        body_h = max(4, size // 6)
        barrel_len = max(8, size // 3)
        body_start = 3
        body_end = size - 3 - barrel_len
        grip_w = max(3, size // 8)
        grip_h = max(5, size // 4)
    elif profile == "shotgun":
        body_h = max(5, size // 5)
        barrel_len = max(6, size // 4)
        body_start = 3
        body_end = size - 3 - barrel_len
        grip_w = max(3, size // 8)
        grip_h = max(5, size // 4)
    elif profile == "sniper":
        body_h = max(3, size // 7)
        barrel_len = max(10, size // 2)
        body_start = 4
        body_end = size - 4 - barrel_len
        grip_w = max(3, size // 9)
        grip_h = max(4, size // 5)
    else:
        body_h = max(4, size // 6)
        barrel_len = max(6, size // 4)
        body_start = 4
        body_end = size - 4 - barrel_len
        grip_w = max(3, size // 8)
        grip_h = max(5, size // 4)

    body_top = cy - body_h // 2
    body_bottom = cy + body_h // 2
    # body
    draw.rectangle([body_start, body_top, body_end, body_bottom], fill=base)
    draw.rectangle([body_start - 1, body_top - 1, body_end + 1, body_bottom + 1], outline=outline)
    # barrel
    draw.rectangle([body_end + 1, cy - body_h // 3, size - 2, cy + body_h // 3], fill=barrel)
    # grip
    grip_x = body_start + (body_end - body_start) // 3
    draw.rectangle([grip_x, body_bottom, grip_x + grip_w, body_bottom + grip_h], fill=grip)
    # stock
    if stock:
        stock_len = max(4, size // 6)
        draw.rectangle([1, cy - body_h // 3, 1 + stock_len, cy + body_h // 3], fill=stock)
    # sight / detail
    draw.rectangle([body_start + 2, body_top - 2, body_start + 6, body_top - 1], fill=outline)
    tex = arcade.Texture(img)
    _cache[key] = tex
    return tex
