#!/usr/bin/env python3
"""Generative math+nature header art for jaime.win posts.

Emits _includes/headers/<date>.svg, coloured with the site CSS variables so the
inline SVG follows light/dark theme, plus static light/dark variants in /tmp for
rasterising the og:image (rsvg-convert -w 800 ... | cwebp -q 82).

Add a post: append (date, motif, title) to POSTS, run this, set in front matter
    header: YYYY-MM-DD
    image: /assets/images/YYYY-MM-DD-header.webp
"""
import math, os, random

W, H = 480, 360
INC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_includes", "headers")
TMP = "/tmp/jaime-headers"

# Colour roles -> CSS vars (inline) or hex (static light / dark)
ROLES = ["bg", "p1", "p2", "p3", "hi", "dim"]
VARS = dict(bg="var(--pre-bg)", p1="var(--accent)", p2="var(--link)", p3="var(--link-under)",
            hi="var(--ink)", dim="var(--dim)")
LIGHT = dict(bg="#f2efe4", p1="#0f3061", p2="#1d4a80", p3="#aabacf", hi="#2a2724", dim="#9a9488")
DARK = dict(bg="#1c1a16", p1="#bfd4f0", p2="#8fb3e0", p3="#3f5a82", hi="#e8e3d6", dim="#8a8374")

C = {}  # active colour map, set per emit

def f1(v): return f"{v:.1f}".rstrip("0").rstrip(".")

def card(body, clip=True, title=""):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="147" height="110" '
            f'class="title-image" role="img" aria-label="{title}">')
    if clip:
        return (head + f'<defs><clipPath id="hc"><rect width="{W}" height="{H}" rx="28"/></clipPath></defs>'
                f'<rect width="{W}" height="{H}" rx="28" fill="{C["bg"]}"/><g clip-path="url(#hc)">{body}</g></svg>')
    return head + f'<rect width="{W}" height="{H}" rx="28" fill="{C["bg"]}"/>{body}</svg>'

def poly(pts, stroke, w=1.2, op=1.0, close=False, fill="none"):
    d = " ".join(f"{f1(x)},{f1(y)}" for x, y in pts)
    tag = "polygon" if close else "polyline"
    o = f' stroke-opacity="{op}"' if op < 1 else ""
    return (f'<{tag} points="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"{o} '
            f'stroke-linejoin="round" stroke-linecap="round"/>')

def line(x1, y1, x2, y2, col, w):
    return f'<line x1="{f1(x1)}" y1="{f1(y1)}" x2="{f1(x2)}" y2="{f1(y2)}" stroke="{col}" stroke-width="{f1(w)}" stroke-linecap="round"/>'

def dot(x, y, r, col):
    return f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(r)}" fill="{col}"/>'

# ---------------------------------------------------------------- motifs

def contours(t):
    gw, gh = 64, 48
    def h(i, j):
        u, v = i/gw*6.0, j/gh*4.5
        return (math.sin(u*1.1)*math.cos(v*1.3) + 0.6*math.sin(u*2.3 + v*0.7)
                + 0.4*math.cos(v*2.9 - u*0.6) + 0.3*math.sin((u+v)*3.1))
    sx, sy = W/gw, H/gh
    F = [[h(i, j) for j in range(gh+1)] for i in range(gw+1)]
    table = {1:(3,0),2:(0,1),3:(3,1),4:(1,2),5:(3,0,1,2),6:(0,2),7:(3,2),
             8:(2,3),9:(0,2),10:(0,1,2,3),11:(1,2),12:(1,3),13:(0,1),14:(3,0)}
    out = []
    for li in range(11):
        lv = -1.4 + li*0.28; segs = []
        for i in range(gw):
            for j in range(gh):
                a, b, c, d = F[i][j], F[i+1][j], F[i+1][j+1], F[i][j+1]
                idx = (a > lv) | ((b > lv) << 1) | ((c > lv) << 2) | ((d > lv) << 3)
                if idx in (0, 15): continue
                P = {0: ((i, j), (i+1, j), a, b), 1: ((i+1, j), (i+1, j+1), b, c),
                     2: ((i+1, j+1), (i, j+1), c, d), 3: ((i, j+1), (i, j), d, a)}
                def lerp(p, q, pa, pb):
                    tt = (lv - pa)/(pb - pa) if pb != pa else 0.5
                    return (p[0] + (q[0]-p[0])*tt, p[1] + (q[1]-p[1])*tt)
                e = table[idx]
                for k in range(0, len(e), 2):
                    p1 = lerp(*P[e[k]]); p2 = lerp(*P[e[k+1]])
                    segs.append(f"M{f1(p1[0]*sx)} {f1(p1[1]*sy)}L{f1(p2[0]*sx)} {f1(p2[1]*sy)}")
        col, w = (C["hi"], 2.2) if li == 7 else ((C["p1"], 1.5) if li % 2 else (C["p3"], 1.2))
        out.append(f'<path d="{"".join(segs)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
    return card("".join(out), title=t)

def sunflower(t):
    cx, cy = W/2, H/2 + 6
    out = []
    for i in range(21):
        a = 2*math.pi*i/21; L, wd = 78, 22
        x0, y0 = cx + 92*math.cos(a), cy + 92*math.sin(a)
        x1, y1 = cx + (92+L)*math.cos(a), cy + (92+L)*math.sin(a)
        nx, ny = -math.sin(a)*wd, math.cos(a)*wd
        d = (f"M{f1(x0)},{f1(y0)} C{f1(x0+nx)},{f1(y0+ny)} {f1(x1+nx*0.5)},{f1(y1+ny*0.5)} {f1(x1)},{f1(y1)} "
             f"C{f1(x1-nx*0.5)},{f1(y1-ny*0.5)} {f1(x0-nx)},{f1(y0-ny)} {f1(x0)},{f1(y0)}Z")
        out.append(f'<path d="{d}" fill="{C["p3"]}" stroke="{C["p2"]}" stroke-width="2"/>')
    ga = math.pi*(3-math.sqrt(5))
    for i in range(520):
        r = 4.3*math.sqrt(i); a = i*ga
        if r > 96: break
        out.append(dot(cx+r*math.cos(a), cy+r*math.sin(a), 1.4 + 2.6*(r/96), C["hi"] if i < 8 else (C["p1"] if i % 2 else C["p2"])))
    return card("".join(out), clip=False, title=t)

def spirograph(t):
    cx, cy = W/2, H/2
    def curve(R, r, dd, scale, col, w, op):
        pts = []; turns = r // math.gcd(int(R), int(r)); n = 220
        for i in range(int(turns*n)):
            th = i * 2*math.pi/n
            x = (R-r)*math.cos(th) + dd*math.cos((R-r)/r*th)
            y = (R-r)*math.sin(th) - dd*math.sin((R-r)/r*th)
            pts.append((cx + x*scale, cy + y*scale))
        return poly(pts, col, w, op, close=True)
    body = curve(11, 4, 5.2, 12.5, C["p1"], 1.2, 1)
    body += curve(11, 4, 2.6, 12.5, C["p3"], 1.1, 1)
    body += curve(7, 3, 2.2, 9.5, C["hi"], 1.4, 1)
    return card(body, title=t)

def tree(t):
    random.seed(23)
    out = []; tips = []
    def branch(x, y, ang, length, depth):
        x2 = x + length*math.cos(ang); y2 = y - length*math.sin(ang)
        out.append(line(x, y, x2, y2, C["p1"], max(0.9, depth*1.25)))
        if depth == 0: tips.append((x2, y2)); return
        n = 2 if depth > 2 else random.choice((1, 2, 3))
        for k in range(n):
            spread = 0.55 + random.uniform(-0.15, 0.15)
            a = ang + (k - (n-1)/2)*spread*1.3 + random.uniform(-0.18, 0.18)
            branch(x2, y2, a, length*random.uniform(0.62, 0.8), depth-1)
    branch(W/2 + 10, H-26, math.pi/2 + 0.08, 74, 7)
    random.shuffle(tips)
    for x, y in tips[:16]: out.append(dot(x, y, 4, C["hi"]))
    out.append(line(60, H-26, W-60, H-26, C["dim"], 2))
    return card("".join(out), clip=False, title=t)

def cardioid(t):
    cx, cy, R = W/2, H/2, 158; n = 200
    out = []
    def pt(i, r=R, m=n):
        a = 2*math.pi*i/m - math.pi/2; return cx + r*math.cos(a), cy + r*math.sin(a)
    segs = []
    for i in range(n):
        x1, y1 = pt(i); x2, y2 = pt((i*2) % n)
        segs.append(f"M{f1(x1)} {f1(y1)}L{f1(x2)} {f1(y2)}")
    out.append(f'<path d="{"".join(segs)}" stroke="{C["p1"]}" stroke-width="0.8" stroke-opacity="0.8" fill="none"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{C["hi"]}" stroke-width="2"/>')
    segs = []
    for i in range(90):
        x1, y1 = pt(i, 60, 90); x2, y2 = pt((i*3) % 90, 60, 90)
        segs.append(f"M{f1(x1)} {f1(y1)}L{f1(x2)} {f1(y2)}")
    out.append(f'<path d="{"".join(segs)}" stroke="{C["hi"]}" stroke-width="1" fill="none"/>')
    return card("".join(out), title=t)

def lorenz(t):
    s, r, b = 10, 28, 8/3; x, y, z = 0.1, 0, 0; dt = 0.009; pts = []
    for i in range(6200):
        dx, dy, dz = s*(y-x), x*(r-z)-y, x*y-b*z
        x += dx*dt; y += dy*dt; z += dz*dt
        if i > 200: pts.append((x, z))
    xs = [p[0] for p in pts]; zs = [p[1] for p in pts]
    sc = min(360/(max(xs)-min(xs)), 300/(max(zs)-min(zs)))
    ox = W/2 - sc*(max(xs)+min(xs))/2; oy = H/2 + sc*(max(zs)+min(zs))/2
    P = [(ox+sc*a, oy-sc*c) for a, c in pts]
    return card(poly(P, C["p1"], 0.9, 0.85) + poly(P[2000:2300], C["hi"], 1.8), title=t)

def hilbert(t):
    order = 5; n = 2**order
    def d2xy(d):
        x = y = 0; tt = d; s = 1
        while s < n:
            rx = 1 & (tt//2); ry = 1 & (tt ^ rx)
            if ry == 0:
                if rx == 1: x, y = s-1-x, s-1-y
                x, y = y, x
            x += s*rx; y += s*ry; tt //= 4; s *= 2
        return x, y
    size = 300; cell = size/n
    ox, oy = (W-size)/2 + cell/2, (H-size)/2 + cell/2
    pts = [(ox + x*cell, oy + y*cell) for x, y in (d2xy(i) for i in range(n*n))]
    return card(poly(pts, C["p1"], 3.4) + poly(pts[430:520], C["hi"], 3.4), title=t)

def dandelion(t):
    random.seed(6)
    cx, cy = W*0.36, H*0.42
    out = [f'<path d="M{f1(cx)},{f1(cy+4)} C{f1(cx-10)},{f1(H*0.7)} {f1(cx+16)},{f1(H*0.85)} {f1(cx-6)},{H+10}" fill="none" stroke="{C["p1"]}" stroke-width="3.2" stroke-linecap="round"/>']
    def seed(x, y, ang, L, col, w):
        tx, ty = x + L*math.cos(ang), y + L*math.sin(ang)
        s = line(x, y, tx, ty, col, w)
        for da in (-0.5, -0.17, 0.17, 0.5):
            s += line(tx, ty, tx + 12*math.cos(ang+da), ty + 12*math.sin(ang+da), col, w*0.8)
        return s
    for i in range(44):
        a = 2*math.pi*i/44 + random.uniform(-0.04, 0.04)
        if 0.15 < a % (2*math.pi) < 0.95 and random.random() < 0.7: continue
        out.append(seed(cx, cy, a, 78 + random.uniform(-4, 4), C["p1"], 1.4))
    out.append(dot(cx, cy, 9, C["p1"]))
    for k, (dx, dy) in enumerate(((150, -60), (215, -95), (270, -40), (320, -110))):
        out.append(seed(cx+dx, cy+dy, -0.6 - k*0.1, 26, C["hi"] if k == 1 else C["p2"], 1.6 if k == 1 else 1.2))
    return card("".join(out), clip=False, title=t)

def fern(t):
    random.seed(2)
    x = y = 0.0; pts = []
    for i in range(4200):
        r = random.random()
        if r < 0.01: x, y = 0, 0.16*y
        elif r < 0.86: x, y = 0.85*x + 0.04*y, -0.04*x + 0.85*y + 1.6
        elif r < 0.93: x, y = 0.2*x - 0.26*y, 0.23*x + 0.22*y + 1.6
        else: x, y = -0.15*x + 0.28*y, 0.26*x + 0.24*y + 0.44
        if i > 20: pts.append((x, y))
    s = 32
    d = "".join(f"M{f1(W/2+18+s*px)} {f1(H-14-s*py)}h.01" for px, py in pts)
    body = f'<path d="{d}" stroke="{C["p1"]}" stroke-width="2.1" stroke-linecap="round" stroke-opacity="0.85" fill="none"/>'
    frond = [p for p in pts if p[1] < 1.2 and p[0] > 0.9][:60]
    d2 = "".join(f"M{f1(W/2+18+s*px)} {f1(H-14-s*py)}h.01" for px, py in frond)
    body += f'<path d="{d2}" stroke="{C["hi"]}" stroke-width="2.4" stroke-linecap="round" fill="none"/>'
    return card(body, title=t)

def waves(t):
    out = []
    for j in range(38):
        pts = [(i, 18 + j*8.8 + 14*math.sin(i/46 + j*0.35) + 7*math.sin(i/19 - j*0.2)) for i in range(0, W+1, 8)]
        col, w = (C["hi"], 2.0) if j == 19 else ((C["p1"], 1.1) if j % 2 else (C["p3"], 1.1))
        out.append(poly(pts, col, w))
    return card("".join(out), title=t)

def orbits(t):
    fx, fy = W/2 - 30, H/2
    out = [dot(fx, fy, 11, C["hi"])]
    random.seed(4)
    for k, (a, e, rot) in enumerate(((52, 0.25, 0.2), (82, 0.42, -0.4), (115, 0.3, 0.9), (150, 0.5, 0.1), (190, 0.15, 1.6))):
        b = a*math.sqrt(1-e*e); c = a*e; pts = []
        for i in range(0, 361, 3):
            th = math.radians(i); x, y = a*math.cos(th) - c, b*math.sin(th)
            xr, yr = x*math.cos(rot) - y*math.sin(rot), x*math.sin(rot) + y*math.cos(rot)
            pts.append((fx + xr, fy + yr))
        out.append(poly(pts, C["p1"] if k % 2 else C["p3"], 1.3, close=True))
        px, py = pts[int(random.uniform(0, len(pts)-1))]
        out.append(dot(px, py, 3.2 + k*0.6, C["p1"]))
    return card("".join(out), title=t)

def nautilus(t):
    cx, cy = W/2 + 30, H/2 + 10; b = 0.172; a0 = 3.2
    def sp(th): r = a0*math.exp(b*th); return cx + r*math.cos(th), cy + r*math.sin(th)
    T = 0; pts = []
    while a0*math.exp(b*T) < 190: pts.append(sp(T)); T += 0.04
    body = poly(pts, C["hi"], 3.0)
    th = T - 0.2; k = 0
    while th > 2*math.pi + 0.5:
        x1, y1 = sp(th); x2, y2 = sp(th - 2*math.pi)
        mx, my = (x1+x2)/2, (y1+y2)/2
        tx, ty = math.cos(th - 0.9), math.sin(th - 0.9)
        cxp, cyp = mx + 14*tx*(th/T), my + 14*ty*(th/T)
        body += f'<path d="M{f1(x1)},{f1(y1)} Q{f1(cxp)},{f1(cyp)} {f1(x2)},{f1(y2)}" fill="none" stroke="{C["p1"] if k % 2 else C["p2"]}" stroke-width="2.4"/>'
        th -= 0.30 + 0.02*(T-th)**0.5; k += 1
    return card(body, clip=False, title=t)

# ---------------------------------------------------------------- posts

POSTS = [
    ("2025-07-09", contours,   "Obsidian as a Personal AI Knowledge Assistant"),
    ("2025-07-21", sunflower,  "AI Agents Don't Need to Know Your Devices"),
    ("2025-09-25", spirograph, "Dynamic Mashups with Vonage and MCP"),
    ("2026-01-10", tree,       "Building with Claude Code"),
    ("2026-02-27", cardioid,   "97 Telco APIs, Two Tools, 730 Tokens"),
    ("2026-03-09", lorenz,     "Experiments on building Agentic Systems"),
    ("2026-03-16", hilbert,    "Emails, vCons, and the Knowledge Base Problem"),
    ("2026-03-20", dandelion,  "An Agentic Email Client"),
    ("2026-04-23", fern,       "Distilling YouTube Into a Queryable Graph"),
    ("2026-05-01", waves,      "Analyzing AI usage in IETF drafts"),
    ("2026-08-20", orbits,     "Notifications for agents: cue, observe, or query"),
    ("2026-09-01", nautilus,   "You can shape your Internet content"),
]

if __name__ == "__main__":
    os.makedirs(INC, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    for date, fn, title in POSTS:
        for label, cmap in (("inline", VARS), ("light", LIGHT), ("dark", DARK)):
            C.clear(); C.update(cmap)
            s = fn(title.replace('"', "&quot;"))
            if label == "inline":
                open(f"{INC}/{date}.svg", "w").write(s)
                print(f"{date} {fn.__name__:11s} {len(s)//1024:3d} KB")
            else:
                open(f"{TMP}/{date}-{label}.svg", "w").write(s)
