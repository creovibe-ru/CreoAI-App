#!/usr/bin/env python3
"""Generate Creo AI logo assets (mark + app icons + notification vector).

Brand green palette (creovibe.ru):
  green-400 #4ADE80, green-500 #22C55E, green-600 #16A34A, green-700 #15803D, green-800 #166534

Outputs (paths relative to repo root):
  app/src/main/res/drawable-nodpi/aether_mark.png            (transparent mark)
  shared/src/commonMain/composeResources/drawable/aether_mark.png
  iosApp/Resources/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png (opaque icon)
  app/src/main/res/drawable/ic_notification_small.xml       (vector, regenerated on edit)
"""

from PIL import Image
import numpy as np
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

G400 = (0x4A, 0xDE, 0x80)
G500 = (0x22, 0xC5, 0x5E)
G600 = (0x16, 0xA3, 0x4A)
G700 = (0x15, 0x80, 0x3D)
G800 = (0x16, 0x65, 0x34)

SS = 4  # supersampling factor
SIZE = 1024

# Mark geometry (fractions of canvas)
CX, CY = 0.5, 0.5
R = 0.335          # arc centerline radius
HALF_T = 0.074     # half thickness of the arc
GAP_HALF = math.radians(38)  # opening half-angle (centered on +x)
DOT_R = 0.085      # dot radius
DOT_ANGLE = 0.0    # dot sits at the opening centerline


def _ring_mask(xs, ys):
    """Distance-based soft mask of the C-ring with rounded caps and the dot."""
    dx = xs - CX
    dy = ys - CY
    dist = np.hypot(dx, dy)
    # ring body: |dist - R| <= HALF_T and angle outside the gap
    ang = np.arctan2(dy, dx)  # (-pi, pi], 0 = +x
    # normalize angle to [-pi, pi); gap centered at 0
    in_gap = np.abs(ang) < GAP_HALF
    ring = (np.abs(dist - R) <= HALF_T) & ~in_gap
    # rounded caps: circles at both gap edges
    for cap_deg in (GAP_HALF, -GAP_HALF):
        cx = CX + R * math.cos(cap_deg)
        cy = CY + R * math.sin(cap_deg)
        capd = np.hypot(xs - cx, ys - cy)
        ring |= capd <= HALF_T
    # dot
    dotc = (CX + R * math.cos(DOT_ANGLE), CY + R * math.sin(DOT_ANGLE))
    dot = np.hypot(xs - dotc[0], ys - dotc[1]) <= DOT_R
    return (ring | dot).astype(np.float64)


def _vertical_gradient(shape, top, bottom):
    h, w = shape
    t = np.linspace(0.0, 1.0, h)[:, None]
    t = np.repeat(t, w, axis=1)
    arr = np.empty((h, w, 3), dtype=np.float64)
    for i in range(3):
        arr[:, :, i] = top[i] + (bottom[i] - top[i]) * t
    return arr


def _diagonal_gradient(shape, c1, c2):
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w]
    t = (xx / w + yy / h) / 2.0
    arr = np.empty((h, w, 3), dtype=np.float64)
    for i in range(3):
        arr[:, :, i] = c1[i] + (c2[i] - c1[i]) * t
    return arr


def _downsample(arr):
    h = arr.shape[0] // SS
    w = arr.shape[1] // SS
    a = arr[: h * SS, : w * SS].reshape(h, SS, w, SS, *arr.shape[2:])
    return a.mean(axis=(1, 3))


def make_mark(path):
    n = SIZE * SS
    xs, ys = np.meshgrid(np.arange(n) / n, np.arange(n) / n)
    mask = _ring_mask(xs, ys)
    rgb = _vertical_gradient(mask.shape, G400, G700)
    out = np.dstack([rgb, mask[:, :, None] * 255.0])
    out = _downsample(out)
    img = Image.fromarray(out.astype(np.uint8), "RGBA")
    img.save(path)
    print("wrote", path)


def make_icon(path):
    n = SIZE * SS
    xs, ys = np.meshgrid(np.arange(n) / n, np.arange(n) / n)
    # background: diagonal green gradient + soft radial highlight top-left
    bg = _diagonal_gradient((n, n), G400, G700)
    yy, xx = np.mgrid[0:n, 0:n]
    glow = np.clip(1.0 - np.hypot((xx - 0.25 * n) / (0.9 * n), (yy - 0.2 * n) / (0.9 * n)), 0, 1)
    for i in range(3):
        bg[:, :, i] = bg[:, :, i] + (255 - bg[:, :, i]) * (glow ** 2) * 0.18
    # white mark (slightly larger than transparent version for balance)
    mask = _ring_mask(xs, ys)
    white = np.empty((n, n, 3))
    white[:, :] = (255.0, 255.0, 255.0)
    out = np.dstack([white, mask[:, :, None] * 255.0])
    # composite mark over background
    alpha = (out[:, :, 3] / 255.0)[:, :, None]
    final = out[:, :, :3] * alpha + bg * (1 - alpha)
    final = np.dstack([final, np.full((n, n, 1), 255.0)])
    final = _downsample(final)
    img = Image.fromarray(final.astype(np.uint8), "RGBA")
    img.save(path)
    print("wrote", path)


if __name__ == "__main__":
    mark_android = os.path.join(ROOT, "app/src/main/res/drawable-nodpi/aether_mark.png")
    mark_shared = os.path.join(
        ROOT, "shared/src/commonMain/composeResources/drawable/aether_mark.png"
    )
    icon_ios = os.path.join(
        ROOT, "iosApp/Resources/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png"
    )
    for p in (mark_android, mark_shared):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        make_mark(p)
    os.makedirs(os.path.dirname(icon_ios), exist_ok=True)
    make_icon(icon_ios)
