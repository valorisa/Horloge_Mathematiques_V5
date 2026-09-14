# Horloge Mathématique V5

Une horloge analogique animée en Python proposant 576 énigmes mathématiques à raisonnement, renouvelées automatiquement toutes les 5 minutes.

Le projet propose deux modes d'exécution adaptés à votre environnement :

- **Mode Web autonome** : Conçu pour Android (Termux) sans aucune dépendance externe (`0 pip install`).
- **Mode Desktop** : Interface graphique native basée sur Matplotlib pour ordinateurs de bureau.

## Aperçu du projet

Contrairement aux horloges mathématiques classiques qui affichent des calculs directs, la version **V5** propose de véritables **énigmes à raisonnement**. La valeur cachée à déduire pour chaque position correspond exactement à l'heure du cadran (de 1 h à 12 h).

- **48 cadrans uniques** (1 cadran par bloc de 5 minutes sur un cycle de 4 heures).
- **12 énigmes par cadran** (576 énigmes au total).
- **12 domaines mathématiques** : Congruences, Identités, Invariants, Contraintes, Combinatoire, Théorie des nombres, Probabilités, Fonctions, Matrices, Récurrences, Géométrie, Logique.
- **Mouvement fluide des aiguilles** : Calcul continu des positions des heures, minutes et secondes.

## Utilisation sur Android (Termux)

Ce mode utilise uniquement les modules standards de Python. Aucun paquet externe n'est requis.

### Lancement du serveur Web

Exécutez le script dans votre terminal Termux :

```bash
python horloge_web_v5.py
```

Le serveur démarre et affiche le message suivant dans la console :

```text
==============================================
 Horloge Mathématique V5 démarrée avec succès !
 Ouvrez dans votre navigateur Android :
 ➜ http://localhost:8000
==============================================
```

### Accès au cadran

Ouvrez votre navigateur web mobile (Chrome, Firefox, etc.) et accédez à l'adresse suivante :

[http://localhost:8000](http://localhost:8000)

L'interface web affiche le cadran analogique animé en temps réel ainsi que les 12 énigmes associées.

## Utilisation sur Ordinateur (Desktop)

La version desktop utilise une fenêtre graphique native pilotée par Matplotlib.

### Installation des dépendances

```bash
pip install matplotlib
```

### Lancement de l'application native

```bash
python horloge_mathematique_v5.py
```

### Raccourcis clavier (Mode Desktop)

- `D` : Afficher ou masquer le niveau de difficulté (`[Niv. 1-4]`).
- `S` : Afficher ou masquer les solutions des énigmes.
- `N` : Revenir au mode automatique synchronisé en temps réel.
- `←` / `→` : Naviguer manuellement dans la liste des 48 cadrans.
- `Q` / `Échap` : Quitter l'application.

## Structure du dépôt

- `horloge_web_v5.py` : Serveur HTTP et interface HTML5 Canvas (compatible Termux / Android).
- `horloge_mathematique_v5.py` : Application native Matplotlib pour ordinateurs de bureau.
- `README.md` : Documentation du projet.

## Auteur

Projet développé par [valorisa](https://github.com/valorisa).

## Licence

Ce projet est sous licence MIT.
