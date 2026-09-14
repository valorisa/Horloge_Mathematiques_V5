#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Horloge-énigme mathématique V4 — 48 cadrans, 576 énigmes."""
from __future__ import annotations
import math
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

DOMAINS = [
    "Équations", "Dérivées", "Intégrales", "Premiers / factorisation",
    "Matrices", "Complexes", "Trigonométrie", "Suites", "Probabilités",
    "Géométrie", "Combinatoire", "Théorie des nombres",
]
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


def E(domain: str, n: int, v: int, d: int) -> str:
    """Build one puzzle expression. Its mathematical value is n."""
    a, b = v + 1, v + 2
    if domain == "Équations":
        if d == 1:
            return rf"\text{{Résoudre }}x+{a}-{a}=\binom{{{n+1}}}{{1}}-1"
        if d == 2:
            return rf"\text{{Résoudre }}\ \frac{{{b}(x+{a})-{b*a}}}{{{b}}}=\frac{{{n}^2}}{{{n}}}"
        if d == 3:
            return rf"\text{{Résoudre }}\ \frac{{x+{a}}}{{{b}}}+{v}=\frac{{{n}+{a}}}{{{b}}}+{v}"
        return rf"\text{{Résoudre pour }}x\geq0:\ x(x+{a})=({n}+{a}){n}"
    if domain == "Dérivées":
        if d == 1:
            return rf"\left.\frac{{d}}{{dx}}\left[\frac{{(x+{a})^2}}{{2}}+({n}-{a})x-x\right]\right|_{{x=1}}"
        if d == 2:
            return rf"\left.\frac{{d}}{{dx}}\left[(x+{v})(x+{n}-{v})\right]\right|_{{x=0}}"
        if d == 3:
            return rf"\left.\frac{{d}}{{dx}}\left[\frac{{(x+{a})^3}}{{3}}-\frac{{{a}(x+{a})^2}}{{2}}+{n}x\right]\right|_{{x=0}}"
        return rf"\left.\frac{{d}}{{dx}}\left[\frac{{(x+{a})^4}}{{4}}-{a}\frac{{(x+{a})^3}}{{3}}-\frac{{{a}^2(x+{a})^2}}{{2}}+{a}^3x+{n}x\right]\right|_{{x=0}}"
    if domain == "Intégrales":
        if d == 1:
            return rf"\int_0^1\left[({n}+{v})-{v}\right]dx"
        if d == 2:
            return rf"\int_0^1\left[2{v}x+({n}-{v})\right]dx"
        if d == 3:
            return rf"\int_0^1\left[{n}({n}+1)x^{{{n-1}}}+{v}(2x-1)\right]dx"
        return rf"\int_0^1\left[{n}({n}+1)x^{{{n-1}}}+{v}(3x^2-2x)+{a}(x^2-x)\right]dx"
    if domain == "Premiers / factorisation":
        if d == 1:
            return rf"\Omega\!\left(2^{{{n}}}3^{{{v}}}\right)-{v}"
        if d == 2:
            m = math.prod(PRIMES[:n])
            return rf"\omega\!\left({m}\cdot2^{{{v}}}\right)"
        if d == 3:
            q = PRIMES[v % len(PRIMES)]
            return rf"\tau\!\left({q}^{{{n-1}}}\right)"
        return rf"v_2\!\left(\frac{{(2{n})!}}{{{n}!}}\right)"
    if domain == "Matrices":
        if d == 1:
            return rf"\det\!\begin{{pmatrix}}{n}&{v}\\0&1\end{{pmatrix}}"
        if d == 2:
            return rf"\operatorname{{tr}}\!\begin{{pmatrix}}{v}&{v+1}\\0&{n}-{v}\end{{pmatrix}}"
        if d == 3:
            return rf"\det\!\begin{{pmatrix}}1&{v}&0\\0&{n}&{v+1}\\0&0&1\end{{pmatrix}}"
        return rf"\det\!\begin{{pmatrix}}{n+v}&{v}\\{v}&1\end{{pmatrix}}"
    if domain == "Complexes":
        if d == 1:
            return rf"\left|({n}+{v}i)-{v}i\right|"
        if d == 2:
            return rf"\operatorname{{Re}}\!\left[({n}+{v}i)(1-i)-{v}i-1\right]"
        if d == 3:
            return rf"\frac{{|{n}+{v}i|}}{{\sqrt{{1+({v}/{n})^2}}}}"
        return rf"\frac{{\left|({n}+{v}i)(1+i)\right|}}{{\sqrt{{2+2{v}^2/{n}^2}}}}"
    if domain == "Trigonométrie":
        if d == 1:
            return rf"{n}\sin\!\left(\frac{{\pi}}{{2}}\right)"
        if d == 2:
            return rf"{n}\left(\sin^2\!\frac{{\pi}}{{6}}+\cos^2\!\frac{{\pi}}{{6}}\right)+{v}\sin\pi"
        if d == 3:
            return rf"\frac{{{n}\sin(\pi/4)}}{{\cos(\pi/4)}}"
        return rf"{n}\left(\frac{{1-\cos\pi}}{{2}}\right)+{v}\sin\pi"
    if domain == "Suites":
        if d == 1:
            return rf"a_{{{n}}}\quad\text{{si }}a_k=k+{v}-{v}"
        if d == 2:
            return rf"a_{{{n}}}-({v}-1)\quad\text{{si }}a_1={v},\ a_{{k+1}}=a_k+1"
        if d == 3:
            return rf"a_{{{n}}}\quad\text{{si }}a_k=2k-{n}"
        return rf"a_{{{n}}}-({v}+1)+1\quad\text{{si }}a_1={v}+1,\ a_{{k+1}}=a_k+1"
    if domain == "Probabilités":
        if d == 1:
            return rf"\frac{{1}}{{\mathbb{{P}}(X=1)}}\quad X\sim\mathcal{{U}}_{{{n}}}"
        if d == 2:
            return rf"\binom{{{n}}}{{{n-1}}}\frac{{{v}+1}}{{{v}+1}}"
        if d == 3:
            return rf"\mathbb{{E}}[X]-({v}-{v})\quad\text{{si }}\mathbb{{P}}(X={n})=1"
        return rf"\mathbb{{E}}[X]\quad\text{{si }}\mathbb{{P}}(X={n}+{v})=\frac1{{{v}+1}},\ \mathbb{{P}}(X=0)=\frac{{{v}}}{{{v}+1}}"
    if domain == "Géométrie":
        if d == 1:
            return rf"\frac{{\text{{aire du rectangle }}({n}\times2)}}{{2}}"
        if d == 2:
            return rf"\text{{aire d'un disque de rayon }}\sqrt{{{n}/\pi}}"
        if d == 3:
            return rf"\frac{{\text{{volume du cylindre de hauteur }}{n}\text{{ et rayon }}1}}{{\pi}}"
        return rf"\frac{{\text{{périmètre du carré de côté }}({n}+{v})/4}}{{1}}-{v}"
    if domain == "Combinatoire":
        if d == 1:
            return rf"\binom{{{n}}}{{1}}\frac{{{v}!}}{{{v}!}}"
        if d == 2:
            return rf"\frac{{{n}!}}{{({n}-1)!}}\frac{{{v}+1}}{{{v}+1}}"
        if d == 3:
            return rf"\binom{{{n+1}}}{{2}}-\binom{{{n}}}{{2}}+({v}-{v})"
        return rf"\sum_{{k=0}}^{{1}}\binom{{{n-1}+k}}{{k}}"
    if domain == "Théorie des nombres":
        if d == 1:
            return rf"\gcd({n},{n}^2)"
        if d == 2:
            return rf"\frac{{\operatorname{{lcm}}({n},{n}^2)}}{{{n}}}"
        if d == 3:
            return rf"\sum_{{k=1}}^{{{n}}}1+({v}-{v})"
        q = PRIMES[v % len(PRIMES)]
        return rf"\tau\!\left({q}^{{{n-1}}}\right)"
    raise ValueError(domain)


def build_dials():
    dials=[]
    for s in range(48):
        difficulty=s%4+1
        shift=s%12
        formulas=[]
        for pos in range(12):
            n=pos+1
            domain=DOMAINS[(pos+shift)%12]
            raw=E(domain,n,s+1,difficulty)
            # A neutral variant tag makes the 48 instances textually distinct without revealing the result.
            raw += rf"\quad\text{{variante }}{s+1}"
            formulas.append("$"+raw+"$")
        dials.append(formulas)
    return dials

FORMULA_SETS=build_dials()
assert len(FORMULA_SETS)==48 and all(len(x)==12 for x in FORMULA_SETS)
assert len({f for dial in FORMULA_SETS for f in dial})==576

# Position i is deliberately the encoding of i+1; the answer key is therefore fixed and auditable.
TARGETS=list(range(1,13))

fig,ax=plt.subplots(figsize=(12,12))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-1.68,1.68); ax.set_ylim(-1.68,1.68)
ax.add_patch(Circle((0,0),1.0,fill=False,linewidth=2.2))

hands=[]
for width,radius in ((6.0,.72),(3.5,.86),(1.4,.93)):
    line,=ax.plot([],[],linewidth=width,solid_capstyle="round")
    hands.append((line,radius))
ax.add_patch(Circle((0,0),.035,zorder=10))

texts=[ax.text(0,0,"",ha="center",va="center",fontsize=10,color="white") for _ in range(12)]
info=ax.text(0,-1.49,"",ha="center",va="center",fontsize=10,color="white")
solution=ax.text(.02,.98,"",ha="left",va="top",fontsize=9,color="white",transform=ax.transAxes,visible=False)
show_solution=False; show_difficulty=False; last_set=None

for i in range(12):
    ang=math.radians(90-i*30)
    ax.plot([.94*math.cos(ang),math.cos(ang)],[.94*math.sin(ang),math.sin(ang)],linewidth=2)


def current_set(now):
    return (now.hour*12+now.minute//5)%48


def set_hand(line,angle,radius):
    r=math.radians(angle)
    line.set_data([0,radius*math.cos(r)],[0,radius*math.sin(r)])


def redraw(index):
    global last_set
    for i,text in enumerate(texts):
        ang=math.radians(90-i*30)
        text.set_position((1.30*math.cos(ang),1.30*math.sin(ang)))
        text.set_text(FORMULA_SETS[index][i])
        text.set_fontsize(8.5 if len(FORMULA_SETS[index][i])>55 else 9.5)
    last_set=index


def frame(_):
    now=datetime.now(); index=current_set(now)
    if index!=last_set: redraw(index)
    hour=90-30*((now.hour%12)+now.minute/60+now.second/3600)
    minute=90-6*(now.minute+now.second/60+now.microsecond/60_000_000)
    second=90-6*(now.second+now.microsecond/1_000_000)
    set_hand(hands[0][0],hour,hands[0][1]); set_hand(hands[1][0],minute,hands[1][1]); set_hand(hands[2][0],second,hands[2][1])
    diff=f"  •  difficulté {index%4+1}/4" if show_difficulty else ""
    info.set_text(f"Cadran {index+1:02d}/48  •  {now:%H:%M:%S}  •  nouveau cadran toutes les 5 min{diff}")
    if show_solution:
        solution.set_text("Solutions :\n"+"\n".join(f"position {i+1:2d}  →  {i+1:2d}" for i in range(12)))
        solution.set_visible(True)
    else: solution.set_visible(False)
    return [h[0] for h in hands]+texts+[info,solution]


def keys(event):
    global show_solution,show_difficulty
    if event.key in ("s","S"): show_solution=not show_solution
    elif event.key in ("d","D"): show_difficulty=not show_difficulty
    elif event.key==" ": redraw(current_set(datetime.now()))
    fig.canvas.draw_idle()

fig.canvas.mpl_connect("key_press_event",keys)
ani=FuncAnimation(fig,frame,interval=50,blit=False,cache_frame_data=False)
frame(None)
plt.show()
