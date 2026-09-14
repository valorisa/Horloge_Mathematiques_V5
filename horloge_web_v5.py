#!/usr/bin/env python3
"""
Horloge Mathématique V5 — Version Web pour Termux / Android.
Ne nécessite aucune bibliothèque tierce (100% Python standard).
"""

from __future__ import annotations
import http.server
import socketserver
import json
import math
import textwrap
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

@dataclass(frozen=True)
class Puzzle:
    text: str
    answer: int
    domain: str
    difficulty: int
    explanation: str

def make_congruence(target: int, variant: int, difficulty: int) -> Puzzle:
    m = target + variant + 3
    k = variant + 2
    N = m * k + target
    return Puzzle(f"Quel est le plus petit entier x > 0 tel que x ≡ {N} (mod {m}) ?", target, "Congruences", difficulty, f"Reste positif = {target}")

def make_identity(target: int, variant: int, difficulty: int) -> Puzzle:
    c = variant + 2
    rhs = target * target
    return Puzzle(f"Soit x > 0. Si (x + {c})² − 2×{c}×(x + {c}) + {c}² = {rhs}, que vaut x ?", target, "Identités", difficulty, f"x² = {rhs} ⟹ x = {target}")

def make_invariant(target: int, variant: int, difficulty: int) -> Puzzle:
    k = variant + 2
    F = k + 3
    E = k + target + 1
    return Puzzle(f"Un graphe planaire connexe a {F} faces et {E} arêtes. Combien a-t-il de sommets V ?", target, "Invariants", difficulty, f"Euler (V-E+F=2) ⟹ V = {target}")

def make_constraints(target: int, variant: int, difficulty: int) -> Puzzle:
    b = target + variant + 2
    S = target + b
    P = target * b
    return Puzzle(f"Deux entiers x < y ont pour somme {S} et produit {P}. Que vaut x ?", target, "Contraintes", difficulty, f"Les entiers sont {target} et {b}")

def make_combinatorics(target: int, variant: int, difficulty: int) -> Puzzle:
    n = target + 1
    return Puzzle(f"Dans un groupe de {n} personnes, chacun serre la main des autres. Combien de mains serre P1 ?", target, "Combinatoire", difficulty, f"Poignées = n-1 = {target}")

def make_number_theory(target: int, variant: int, difficulty: int) -> Puzzle:
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    p = primes[variant % len(primes)]
    exp = target - 1
    val = p ** exp
    return Puzzle(f"Combien de diviseurs positifs possède N = {p}^{exp} ({val}) ?", target, "Théorie des nombres", difficulty, f"Diviseurs = {exp}+1 = {target}")

def make_probability(target: int, variant: int, difficulty: int) -> Puzzle:
    v = variant + 1
    total = target + v
    return Puzzle(f"Une urne contient {total} jetons. Sachant que {v} sont rouges et le reste bleu, combien y a-t-il de bleus ?", target, "Probabilités", difficulty, f"Bleus = {total}-{v} = {target}")

def make_function(target: int, variant: int, difficulty: int) -> Puzzle:
    a, b = variant + 2, variant + 5
    val = a * target + b
    return Puzzle(f"Soit f(x) = {a}x + {b}. Quel est l'unique x tel que f(x) = {val} ?", target, "Fonctions", difficulty, f"f(x)={val} ⟹ x = {target}")

def make_matrix(target: int, variant: int, difficulty: int) -> Puzzle:
    k, c = variant + 1, variant + 4
    tr = target + c
    return Puzzle(f"Soit A = [[x, {k}], [0, {c}]]. Que vaut x si Tr(A) = {tr} ?", target, "Matrices", difficulty, f"Tr(A) = x+{c} = {tr} ⟹ x = {target}")

def make_recurrence(target: int, variant: int, difficulty: int) -> Puzzle:
    r = variant + 2
    u3 = target + 2 * r
    return Puzzle(f"Une suite arithmétique de raison r = {r} a u₃ = {u3}. Que vaut u₁ ?", target, "Récurrences", difficulty, f"u₁ = u₃ - 2r = {target}")

def make_geometry(target: int, variant: int, difficulty: int) -> Puzzle:
    b = 2 * (variant + 1)
    area = (variant + 1) * target
    return Puzzle(f"Un triangle de base b = {b} cm a une aire A = {area} cm². Sa hauteur h ?", target, "Géométrie", difficulty, f"h = 2A/b = {target} cm")

def make_logic(target: int, variant: int, difficulty: int) -> Puzzle:
    total = target + variant + 10
    notspec = total - target
    return Puzzle(f"Sur {total} cases, {notspec} sont noires. Combien sont blanches ?", target, "Logique", difficulty, f"Blanches = {total}-{notspec} = {target}")

BUILDERS = [make_congruence, make_identity, make_invariant, make_constraints, make_combinatorics, make_number_theory, make_probability, make_function, make_matrix, make_recurrence, make_geometry, make_logic]

def build_catalogue() -> List[List[dict]]:
    cat = []
    for s_id in range(48):
        row = []
        for pos in range(12):
            target = pos + 1
            diff = 1 + ((s_id + pos) % 4)
            p = BUILDERS[(s_id + pos) % len(BUILDERS)](target, s_id * 12 + pos, diff)
            row.append({"text": p.text, "answer": p.answer, "domain": p.domain, "difficulty": p.difficulty, "explanation": p.explanation})
        cat.append(row)
    return cat

CATALOGUE = build_catalogue()

HTML_PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Horloge Mathématique V5</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 15px; display: flex; flex-direction: column; align-items: center; }
        h1 { font-size: 1.4rem; margin-bottom: 5px; color: #38bdf8; }
        #clock-container { position: relative; width: 340px; height: 340px; margin: 15px 0; }
        canvas { width: 100%; height: 100%; border-radius: 50%; background: #1e293b; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
        .controls { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin-bottom: 15px; }
        button { background: #334155; color: #fff; border: 1px solid #475569; padding: 8px 12px; border-radius: 6px; font-weight: 600; cursor: pointer; }
        button.active { background: #0284c7; border-color: #38bdf8; }
        #status { font-size: 0.85rem; color: #94a3b8; text-align: center; }
        #puzzle-list { width: 100%; max-width: 500px; display: grid; grid-template-columns: 1fr; gap: 8px; margin-top: 10px; }
        .pz-card { background: #1e293b; padding: 10px 14px; border-radius: 8px; border-left: 4px solid #38bdf8; font-size: 0.88rem; }
        .pz-header { display: flex; justify-content: space-between; font-weight: bold; color: #38bdf8; margin-bottom: 4px; }
        .solution { color: #4ade80; font-weight: bold; margin-top: 4px; display: none; }
    </style>
</head>
<body>
    <h1>Horloge Mathématique V5</h1>
    <div id="status">Cadran --/48</div>

    <div id="clock-container">
        <canvas id="clock" width="600" height="600"></canvas>
    </div>

    <div class="controls">
        <button id="btn-auto" class="active" onclick="toggleAuto()">Auto (5m)</button>
        <button onclick="navSet(-1)">◄ Prev</button>
        <button onclick="navSet(1)">Next ►</button>
        <button id="btn-sol" onclick="toggleSolutions()">Solutions</button>
    </div>

    <div id="puzzle-list"></div>

    <script>
        const catalogue = %CATALOGUE_JSON%;
        let manualSet = null;
        let showSolutions = false;

        function getSetId() {
            if (manualSet !== null) return manualSet;
            const now = new Date();
            const block = Math.floor((now.getHours() * 60 + now.getMinutes()) / 5);
            return block % 48;
        }

        function toggleAuto() {
            manualSet = null;
            document.getElementById('btn-auto').classList.add('active');
            update();
        }

        function navSet(dir) {
            let cur = getSetId();
            manualSet = (cur + dir + 48) % 48;
            document.getElementById('btn-auto').classList.remove('active');
            update();
        }

        function toggleSolutions() {
            showSolutions = !showSolutions;
            document.getElementById('btn-sol').classList.toggle('active', showSolutions);
            document.querySelectorAll('.solution').forEach(el => el.style.display = showSolutions ? 'block' : 'none');
        }

        function drawClock() {
            const canvas = document.getElementById('clock');
            const ctx = canvas.getContext('2d');
            const cx = 300, cy = 300, r = 270;
            ctx.clearRect(0, 0, 600, 600);

            // Cadran
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 6;
            ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2*Math.PI); ctx.stroke();

            // Graduations
            for(let i=1; i<=12; i++) {
                let ang = (i * 30 - 90) * Math.PI / 180;
                let x1 = cx + (r-15)*Math.cos(ang), y1 = cy + (r-15)*Math.sin(ang);
                let x2 = cx + r*Math.cos(ang), y2 = cy + r*Math.sin(ang);
                ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();

                let xt = cx + (r-45)*Math.cos(ang), yt = cy + (r-45)*Math.sin(ang);
                ctx.fillStyle = '#f8fafc'; ctx.font = 'bold 24px system-ui';
                ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
                ctx.fillText(i, xt, yt);
            }

            // Aiguilles
            const now = new Date();
            const h = now.getHours() % 12, m = now.getMinutes(), s = now.getSeconds() + now.getMilliseconds()/1000;
            
            // Heures
            let hAng = ((h + m/60 + s/3600) * 30 - 90) * Math.PI / 180;
            ctx.strokeStyle = '#f8fafc'; ctx.lineWidth = 10; ctx.lineCap = 'round';
            ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx + 130*Math.cos(hAng), cy + 130*Math.sin(hAng)); ctx.stroke();

            // Minutes
            let mAng = ((m + s/60) * 6 - 90) * Math.PI / 180;
            ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 6;
            ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx + 190*Math.cos(mAng), cy + 190*Math.sin(mAng)); ctx.stroke();

            // Secondes
            let sAng = (s * 6 - 90) * Math.PI / 180;
            ctx.strokeStyle = '#f43f5e'; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx + 220*Math.cos(sAng), cy + 220*Math.sin(sAng)); ctx.stroke();

            // Centre
            ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.arc(cx,cy, 10, 0, 2*Math.PI); ctx.fill();
        }

        function update() {
            const setId = getSetId();
            document.getElementById('status').innerText = `Cadran ${setId + 1}/48 (Niveau 1–4)`;
            
            const puzzles = catalogue[setId];
            const listEl = document.getElementById('puzzle-list');
            listEl.innerHTML = '';

            puzzles.forEach((pz, idx) => {
                const hour = idx + 1;
                const card = document.createElement('div');
                card.className = 'pz-card';
                card.innerHTML = `
                    <div class="pz-header"><span>Position ${hour}h — ${pz.domain}</span><span>Niv. ${pz.difficulty}</span></div>
                    <div>${pz.text}</div>
                    <div class="solution" style="display: ${showSolutions ? 'block' : 'none'}">➜ Solution = ${pz.answer} (${pz.explanation})</div>
                `;
                listEl.appendChild(card);
            });
            drawClock();
        }

        setInterval(drawClock, 100);
        setInterval(() => { if(manualSet === null) update(); }, 10000);
        update();
    </script>
</body>
</html>
"""

class WebHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        html = HTML_PAGE.replace("%CATALOGUE_JSON%", json.dumps(CATALOGUE, ensure_ascii=False))
        self.wfile.write(html.encode("utf-8"))

if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), WebHandler) as httpd:
        print(f"\n==============================================")
        print(f" Horloge Mathématique V5 démarrée avec succès !")
        print(f" Ouvrez dans votre navigateur Android :")
        print(f" ➜ http://localhost:{PORT}")
        print(f"==============================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nHorloge arrêtée.")
