#!/usr/bin/env python3
"""
Horloge Mathématique V5 — Horloge-énigme à raisonnement et déduction.

48 cadrans × 12 énigmes = 576 énigmes à raisonnement uniques.
Chaque position (1h à 12h) correspond à une énigme dont la solution est
exactement le numéro de l'heure correspondante (1 à 12).

Changement de cadran automatique toutes les 5 minutes.
Aiguilles analogiques à mouvement continu.

Commandes clavier :
    D : afficher/masquer les niveaux de difficulté
    S : afficher/masquer les solutions
    N : revenir au cadran automatique temps réel
    ← / → : explorer les cadrans précédents / suivants
    Q / Esc : quitter
"""

from __future__ import annotations

import math
import textwrap
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Optional

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


@dataclass(frozen=True)
class Puzzle:
    text: str
    answer: int
    domain: str
    difficulty: int
    explanation: str


# =====================================================================
# GÉNÉRATEURS D'ÉNIGMES À RAISONNEMENT (12 DOMAINES)
# =====================================================================

def make_congruence(target: int, variant: int, difficulty: int) -> Puzzle:
    """Arithmétique modulaire : déduction du reste positif."""
    m = target + variant + 3
    k = variant + 2
    N = m * k + target
    text = f"Quel est le plus petit entier x > 0 tel que x ≡ {N} (mod {m}) ?"
    explanation = f"Le reste positif de {N} divisé par {m} est {target}."
    return Puzzle(text, target, "Congruences", difficulty, explanation)


def make_identity(target: int, variant: int, difficulty: int) -> Puzzle:
    """Identité remarquable masquée : réduction algébrique."""
    c = variant + 2
    rhs = target * target
    text = f"Soit x > 0. Si (x + {c})² − 2×{c}×(x + {c}) + {c}² = {rhs}, que vaut x ?"
    explanation = f"L'expression se simplifie en x² = {rhs}, d'où x = {target}."
    return Puzzle(text, target, "Identités", difficulty, explanation)


def make_invariant(target: int, variant: int, difficulty: int) -> Puzzle:
    """Topologie & Invariants : Formule d'Euler pour les graphes planaires."""
    k = variant + 2
    F = k + 3
    E = k + target + 1
    text = f"Un graphe planaire connexe a {F} faces et {E} arêtes. Combien a-t-il de sommets V ?"
    explanation = f"Formule d'Euler (V − E + F = 2) : V = {E} − {F} + 2 = {target}."
    return Puzzle(text, target, "Invariants", difficulty, explanation)


def make_constraints(target: int, variant: int, difficulty: int) -> Puzzle:
    """Système sous contraintes : racines d'un polynôme via Somme/Produit."""
    b = target + variant + 2
    S = target + b
    P = target * b
    text = f"Deux entiers x < y ont pour somme {S} et produit {P}. Que vaut le plus petit, x ?"
    explanation = f"Les deux entiers sont {target} et {b}, donc le plus petit est {target}."
    return Puzzle(text, target, "Contraintes", difficulty, explanation)


def make_combinatorics(target: int, variant: int, difficulty: int) -> Puzzle:
    """Combinatoire : problème des poignées de main (graphe complet)."""
    n = target + 1
    text = (
        f"Dans un groupe de {n} personnes, chacun serre la main de tous les autres. "
        f"Combien de mains une personne donnée serre-t-elle ?"
    )
    explanation = f"Chaque personne serre la main des {n} − 1 = {target} autres personnes."
    return Puzzle(text, target, "Combinatoire", difficulty, explanation)


def make_number_theory(target: int, variant: int, difficulty: int) -> Puzzle:
    """Théorie des nombres : nombre de diviseurs positifs d'une puissance première."""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    p = primes[variant % len(primes)]
    exp = target - 1
    val = p ** exp
    text = f"Combien de diviseurs positifs possède le nombre N = {p}^{exp} ({val}) ?"
    explanation = f"Pour N = p^k avec p premier, le nombre de diviseurs est k + 1 = {exp} + 1 = {target}."
    return Puzzle(text, target, "Théorie des nombres", difficulty, explanation)


def make_probability(target: int, variant: int, difficulty: int) -> Puzzle:
    """Probabilités conditionnelles et partitions d'ensembles."""
    v = variant + 1
    total = target + v
    text = (
        f"Une urne contient {total} jetons numérotés. Sachant que {v} jetons sont rouges "
        f"et les autres bleus, combien y a-t-il de jetons bleus ?"
    )
    explanation = f"Nombre de jetons bleus = total − rouges = {total} − {v} = {target}."
    return Puzzle(text, target, "Probabilités", difficulty, explanation)


def make_function(target: int, variant: int, difficulty: int) -> Puzzle:
    """Fonctions & Réciproques : inversion d'une bijection affine."""
    a = variant + 2
    b = variant + 5
    val = a * target + b
    text = f"Soit f(x) = {a}x + {b}. Quel est l'unique réel x tel que f(x) = {val} ?"
    explanation = f"f(x) = {val} ⟹ {a}x = {val - b} ⟹ x = {target}."
    return Puzzle(text, target, "Fonctions", difficulty, explanation)


def make_matrix(target: int, variant: int, difficulty: int) -> Puzzle:
    """Algèbre linéaire : trace d'une matrice carrée."""
    k = variant + 1
    c = variant + 4
    tr = target + c
    text = f"Pour la matrice A = [[x, {k}], [0, {c}]], quelle est la valeur de x si Tr(A) = {tr} ?"
    explanation = f"Tr(A) = x + {c} = {tr} ⟹ x = {target}."
    return Puzzle(text, target, "Matrices", difficulty, explanation)


def make_recurrence(target: int, variant: int, difficulty: int) -> Puzzle:
    """Suites & Récurrences : remonter aux premiers termes d'une suite arithmétique."""
    r = variant + 2
    u3 = target + 2 * r
    text = f"Une suite arithmétique de raison r = {r} a pour terme u₃ = {u3}. Que vaut u₁ ?"
    explanation = f"u₁ = u₃ − 2r = {u3} − {2*r} = {target}."
    return Puzzle(text, target, "Récurrences", difficulty, explanation)


def make_geometry(target: int, variant: int, difficulty: int) -> Puzzle:
    """Géométrie indirecte : calcul de hauteur à partir de l'aire."""
    b = 2 * (variant + 1)
    area = (variant + 1) * target
    text = f"Un triangle de base b = {b} cm a une aire A = {area} cm². Quelle est sa hauteur h ?"
    explanation = f"h = 2A / b = {2*area} / {b} = {target} cm."
    return Puzzle(text, target, "Géométrie indirecte", difficulty, explanation)


def make_logic(target: int, variant: int, difficulty: int) -> Puzzle:
    """Logique & Complémentaires : déduction sous partition."""
    total = target + variant + 10
    notspec = total - target
    text = f"Sur un plateau de {total} cases, {notspec} sont noires. Combien de cases sont blanches ?"
    explanation = f"Cases blanches = {total} − {notspec} = {target}."
    return Puzzle(text, target, "Logique", difficulty, explanation)


# =====================================================================
# CONSTRUCTION ET VALIDATION DE LE CATALOGUE (48 CADRANS × 12 ÉNIGMES)
# =====================================================================

BUILDERS = [
    make_congruence,
    make_identity,
    make_invariant,
    make_constraints,
    make_combinatorics,
    make_number_theory,
    make_probability,
    make_function,
    make_matrix,
    make_recurrence,
    make_geometry,
    make_logic,
]


def build_catalogue() -> List[List[Puzzle]]:
    catalogue: List[List[Puzzle]] = []
    for set_id in range(48):
        row: List[Puzzle] = []
        for pos in range(12):
            target = pos + 1  # L'heure visée (1h à 12h)
            difficulty = 1 + ((set_id + pos) % 4)
            family = (set_id + pos) % len(BUILDERS)
            variant = set_id * 12 + pos
            puzzle = BUILDERS[family](target, variant, difficulty)
            row.append(puzzle)
        catalogue.append(row)
    return catalogue


FORMULA_SETS = build_catalogue()


def validate_catalogue() -> None:
    """Vérification stricte de l'intégrité du catalogue au démarrage."""
    if len(FORMULA_SETS) != 48:
        raise AssertionError("Il faut exactement 48 cadrans.")

    seen_texts = set()
    for set_id, puzzles in enumerate(FORMULA_SETS):
        if len(puzzles) != 12:
            raise AssertionError(f"Cadran {set_id + 1}: 12 énigmes attendues.")

        for pos, puzzle in enumerate(puzzles):
            expected_target = pos + 1
            if puzzle.answer != expected_target:
                raise AssertionError(
                    f"Cadran {set_id + 1}, Pos {pos + 1}: "
                    f"Réponse {puzzle.answer} != {expected_target}"
                )

            if puzzle.text in seen_texts:
                raise AssertionError(f"Énigme dupliquée : {puzzle.text}")
            seen_texts.add(puzzle.text)


validate_catalogue()


# =====================================================================
# CALCULS TEMPORELS ET TRIGONOMÉTRIE
# =====================================================================

def current_formula_set(now: datetime) -> int:
    """Détermine le cadran actif (1 bloc de 5 minutes = 1 cadran sur 48)."""
    minute_block = (now.hour * 60 + now.minute) // 5
    return minute_block % len(FORMULA_SETS)


def hand_xy(angle_degrees: float, length: float) -> Tuple[float, float]:
    """Convertit un angle horaire en coordonnées cartésiennes (x, y)."""
    angle_rad = math.radians(90 - angle_degrees)
    return length * math.cos(angle_rad), length * math.sin(angle_rad)


# =====================================================================
# CLASSE DE L'HORLOGE INTERACTIVE MATPLOTLIB
# =====================================================================

class MathClock:
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots(figsize=(11, 11))
        self.fig.canvas.manager.set_window_title("Horloge Mathématique V5 — Énigmes à raisonnement")
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        self.show_difficulty = False
        self.show_solutions = False
        self.manual_set: Optional[int] = None

        self.fig.canvas.mpl_connect("key_press_event", self.on_key)

    def on_key(self, event) -> None:
        if event.key in {"q", "escape"}:
            plt.close(self.fig)
        elif event.key == "d":
            self.show_difficulty = not self.show_difficulty
            self.draw(datetime.now())
        elif event.key == "s":
            self.show_solutions = not self.show_solutions
            self.draw(datetime.now())
        elif event.key == "n":
            self.manual_set = None
            self.draw(datetime.now())
        elif event.key in {"left", "down"}:
            cur = self.manual_set if self.manual_set is not None else current_formula_set(datetime.now())
            self.manual_set = (cur - 1) % len(FORMULA_SETS)
            self.draw(datetime.now())
        elif event.key in {"right", "up"}:
            cur = self.manual_set if self.manual_set is not None else current_formula_set(datetime.now())
            self.manual_set = (cur + 1) % len(FORMULA_SETS)
            self.draw(datetime.now())

    def draw(self, now: datetime) -> None:
        self.ax.clear()
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.ax.set_xlim(-1.65, 1.65)
        self.ax.set_ylim(-1.65, 1.65)

        set_id = self.manual_set if self.manual_set is not None else current_formula_set(now)
        puzzles = FORMULA_SETS[set_id]

        # Cadran extérieur
        outer_circle = plt.Circle((0, 0), 1.0, fill=False, linewidth=2.5, color="#2c3e50")
        self.ax.add_patch(outer_circle)

        # Tracé des 12 graduations et énoncés
        for i in range(12):
            hour = i + 1
            angle_deg = 90 - hour * 30
            angle_rad = math.radians(angle_deg)

            # Graduations
            x_in, y_in = 0.92 * math.cos(angle_rad), 0.92 * math.sin(angle_rad)
            x_out, y_out = 1.0 * math.cos(angle_rad), 1.0 * math.sin(angle_rad)
            self.ax.plot([x_in, x_out], [y_in, y_out], color="#2c3e50", linewidth=2)

            # Positionnement du texte
            x_txt = 1.32 * math.cos(angle_rad)
            y_txt = 1.32 * math.sin(angle_rad)

            pz = puzzles[i]
            formatted_text = textwrap.fill(pz.text, width=26)

            label = formatted_text
            if self.show_difficulty:
                label = f"[Niv. {pz.difficulty}] {label}"
            if self.show_solutions:
                label += f"\n➜ Solution: {pz.answer}"

            self.ax.text(
                x_txt, y_txt, label,
                ha="center", va="center",
                fontsize=7.8, color="#1a252f",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#f8f9fa", edgecolor="#bdc3c7", alpha=0.85)
            )

        # Calcul des angles des aiguilles (mouvement continu)
        h = now.hour % 12
        m = now.minute
        s = now.second + now.microsecond / 1_000_000

        hour_angle = 30 * (h + m / 60 + s / 3600)
        minute_angle = 6 * (m + s / 60)
        second_angle = 6 * s

        # Aiguille des heures
        hx, hy = hand_xy(hour_angle, 0.52)
        self.ax.plot([0, hx], [0, hy], color="#2c3e50", linewidth=5, solid_capstyle="round")

        # Aiguille des minutes
        mx, my = hand_xy(minute_angle, 0.72)
        self.ax.plot([0, mx], [0, my], color="#34495e", linewidth=3.2, solid_capstyle="round")

        # Aiguille des secondes
        sx, sy = hand_xy(second_angle, 0.86)
        self.ax.plot([0, sx], [0, sy], color="#e74c3c", linewidth=1.4)

        # Pivot central
        self.ax.add_patch(plt.Circle((0, 0), 0.04, color="#2c3e50", zorder=10))

        # Barre de statut
        mode_str = "AUTO (Synchro 5 min)" if self.manual_set is None else "MANUEL (Navigation)"
        avg_diff = sum(p.difficulty for p in puzzles) / 12.0
        self.ax.text(
            0, -1.58,
            f"V5 • Cadran {set_id + 1}/48 • Difficulté moyenne : {avg_diff:.1f}/4 • Mode : {mode_str}\n"
            f"[D]ifficulté  |  [S]olutions  |  [N]ormal  |  [←/→] Naviguer  |  [Q]uitter",
            ha="center", va="center", fontsize=8.5, color="#34495e",
            bbox=dict(boxstyle="square,pad=0.4", facecolor="#ecf0f1", edgecolor="none")
        )

    def animate(self, _frame: int) -> None:
        self.draw(datetime.now())


# =====================================================================
# POINT D'ENTRÉE PRINCIPAL
# =====================================================================

def main() -> None:
    clock = MathClock()
    clock.draw(datetime.now())
    _anim = FuncAnimation(clock.fig, clock.animate, interval=50, cache_frame_data=False)
    plt.show()


if __name__ == "__main__":
    main()
