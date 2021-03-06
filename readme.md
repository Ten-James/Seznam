# Repozitář pro Praxe Seznam

Jakub Indrák 16.5-27.5
jakub.indrak@email.cz
j.indrak.st@spseiostrava.cz

- Table of Content
  - [Jupyter Sešity](#jupyter-sešity)
  - [Složky](#složky)
    - [python](#python) sklearn
    - [funkceAI](#funkceai) sklearn
    - [Flappy](#flappy) numpy pygame
    - [FlappyNeat](#flappyneat) pygame neat-python

## Jupyter Sešity

[Iterace čísel](<Iterace\ čísel.ipynb>)

vrací řadu čísel...

$$[1^{n} \bmod n,2^{n} \bmod n,3^{n} \bmod n,...,100^{n} \bmod n]$$

[Komentáře](<Komentare.ipynb>)
Všechna řešení k uloze diskuze.

[Pokemoni](<Pokemoni.ipynb>)
Začátky s Pandas, úlohy na procvičení.

[Perceptron](<01\ -\ Perceptron/01_Perceptron.ipynb>)
Úlohy spojené s perceptronem.

## Složky

### python

    Decision TREE pro piškvorky

- [pisk.py](python/pisk.py) Generuje dataset podle tvých inputů.
- [piskAI.py](python/piskAi.py) Generuje dataset podle tvých inputů ale už můžeš vidět jak by se **Decision tree** zachoval.
- [piskAIGame.py](python/piskAiGame.py) not done.
  - Zde by si měl hrát proti decision tree, který by se nasledne ucil a generoval data

### funkceAI

    Decision tree pro funcki

- [ai.py](funkceAi/ai.py) modifikovaná verze souboru _ai.py_ z piškvorek
  - vysledek zobrazí jako graf
- Data se generují pomocí [generatedata.py](funkceAi/generatedata.py)

### Flappy

    Evolution AI, která využívá pygame

- Funguje asi na 80%
- Evoluce pouze lehce mutuje váhy neuronů, struktura jako taková se nemění
- Assety jsou z <https://github.com/zhaolingzhi/FlapPyBird-master>
- Audio je depricated
- Main code hry je z <https://github.com/LeonMarqs/Flappy-bird-python>

Když se zapla hra s:

    SPEED = 5
    GRAVITY = 0.25

Tak moje Mutační methoda byla schopná uspět do zhruba 10 generací.
Bohužel při nastavení hodnot zpět na normal nebyla schopná ani po 200 generací se dostat na stabilní vysledné hodnoty

### FlappyNeat

    Evolution AI, která využívá pygame a knihovnu NEAT

- Evoluce je Funkční.
- Assety jsou z <https://github.com/zhaolingzhi/FlapPyBird-master>
- Audio je depricated
- Main code hry je z <https://github.com/LeonMarqs/Flappy-bird-python>

<!--  -->
