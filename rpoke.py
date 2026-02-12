import random as r
import json
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

GEN_POKEDEX_KEY = {1: 151, 2: 251, 3: 386, 4: 493, 5: 649, 6: 721, 7: 809, 8: 905, 9: 1025}
with open(os.path.join(__location__, "pokedex.json"), 'r', encoding='utf-8') as file:
    POKEDEX_DATA = json.load(file)
with open(os.path.join(__location__, "learnsets.json"), 'r', encoding='utf-8') as file:
    LEARNSET_DATA = json.load(file)
with open(os.path.join(__location__, "items.json"), "r", encoding='utf-8') as file:
    ITEM_DATA = json.load(file)

class Pokemon:
    def __init__(self, gameGeneration:int=9, level:int = 1, dexNo:int = 0, name:str = "", fullyRandom:bool = True,
                isFullyEvolved = False):

        if gameGeneration < 3:
            raise ValueError("Data only supports generation 3 or higher.")
        
        self.pokeDict = {}
        self.dexNo = dexNo
        self.name = name
        self.lvl = level
        self.gen = gameGeneration
        self.select_pokemon(name,isFullyEvolved)
        
        self.ability = ""
        self.nature = ""
        self.item = ""
        self.moveset = []
        self.EVs = []
        self.IVs = []

        if fullyRandom:
            self.randomize()

    def select_pokemon(self, name = "", isFullyEvolved = False):
        try:
            if name:
                self.pokeDict = POKEDEX_DATA[name.lower()]
                self.name = self.pokeDict["name"]
                self.dexNo = self.pokeDict["num"]
            else:
                self.dexNo = r.randint(1, b=GEN_POKEDEX_KEY[self.gen])
                self.name = next((key for key, value in POKEDEX_DATA.items() if value.get('num') == self.dexNo))
                self.pokeDict = POKEDEX_DATA[self.name]
            if isFullyEvolved:
                if "evos" in self.pokeDict:
                    evolution = r.choice(self.pokeDict["evos"])
                    self.select_pokemon(evolution.lower(), isFullyEvolved)
        except(KeyError):
            KeyError("It appears your pokemon's name was spelled incorrectly.\n Make sure not to include any spaces or special characters.")

    def generate_ability(self):
        self.ability = ""
        self.ability = r.choice(list(self.pokeDict["abilities"].values()))

    def generate_moveset(self, TMmoves=False, tutorMoves=False, eggMoves=False, 
                       transferMoves=False, eventMoves=False):
        TMmoves = "M" if TMmoves else ""
        tutorMoves = "T" if tutorMoves else ""
        eggMoves = "E" if eggMoves else ""
        transferMoves = "V" if transferMoves else ""
        eventMoves = "S" if transferMoves else ""
        
        learnset = LEARNSET_DATA[self.name.lower()]["learnset"]

        filteredLearnset = self._filterMoveset(learnset, TMmoves, tutorMoves, eggMoves, transferMoves, eventMoves)

        if ("prevo" in self.pokeDict):
            pkmnPrevo = next(key for key, value in POKEDEX_DATA.items() if value.get('name') == self.pokeDict["prevo"])
            prevoFilteredLearnset = self._filterMoveset(LEARNSET_DATA[pkmnPrevo]["learnset"], TMmoves, tutorMoves, eggMoves, transferMoves, eventMoves)
            if ("prevo" in pkmnPrevo):
                pkmnPrePrevo = next(key for key, value in POKEDEX_DATA.items() if value.get('name') == pkmnPrevo["prevo"])
                prePrevoFilteredLearnset = self._filterMoveset(LEARNSET_DATA[pkmnPrePrevo.lower()]["learnset"], TMmoves, tutorMoves, eggMoves, transferMoves, eventMoves)
                prevoFilteredLearnset += (set(prePrevoFilteredLearnset) - set(prevoFilteredLearnset))
            filteredLearnset += (set(prevoFilteredLearnset) - set(filteredLearnset))
         
        self.moveset = []
        for i in range(4):
            try:
                move = r.choice(filteredLearnset)
                self.moveset.append(move)
                filteredLearnset.remove(move)
            except (IndexError):
                break
                    
    def _filterMoveset(self, learnset, M, T, E, V, S):
        filteredList = []
        for move, x in learnset.items():
            for item in x:
                if item[0] == str(self.gen):
                    cat = item[1]
                    if (cat == M) or (cat == T) or (cat == E) or (cat == V) or (cat == S):
                        filteredList.append(move)
                    elif cat == "L" and (self.lvl >= int(item[2:])):
                        filteredList.append(move)
        return filteredList
    
    def generate_EVs(self,numOfEVs=520):
        self.EVs = [0,0,0,0,0,0]

        if 0 > numOfEVs > 520:
            raise(ValueError("EV's must be between 0 and 520."))
        
        for i in range(numOfEVs):
            stat = r.randint(0,5)
            self.EVs[stat] += 1

    def generate_IVs(self):
        self.IVs = [0,0,0,0,0,0]
        for i in range(6):
            self.IVs[i] = r.randint(0,31)

    def generate_held_item(self):
        itemNo = r.randint(0,len(ITEM_DATA)-1)
        key = list(ITEM_DATA)[itemNo]
        self.item = ITEM_DATA[key]["name"]

    def randomize(self, abty:bool = False, mvst:bool = False, 
                  EV:bool = False, IV:bool = False, item:bool = False, all:bool=False):
        if abty or all:
            self.generate_ability()
        if mvst or all: 
            self.generate_moveset()
        if EV or all:
            self.generate_EVs()
        if IV or all:
            self.generate_IVs()
        if item or all:
            self.generate_held_item()
    
    def pokepaste(self):
        pokepaste = f'{self.pokeDict["name"]}'
        if self.item:
            pokepaste += f' @ {self.item}\n'
        else:
            pokepaste += '\n'
        if self.ability:
            pokepaste += f'Ability: {self.ability}\n'
        if self.EVs:
            pokepaste += f'EVs: {self.EVs[0]} HP / {self.EVs[1]} Atk / {self.EVs[2]} Def / {self.EVs[3]} SpA / {self.EVs[4]} SpD / {self.EVs[5]} Spe\n'
        if self.IVs:
            pokepaste += f'IVs: {self.IVs[0]} HP / {self.IVs[1]} Atk / {self.IVs[2]} Def / {self.IVs[3]} SpA / {self.IVs[4]} SpD / {self.IVs[5]} Spe\n'
        if self.nature:
            pokepaste += f'{self.nature} Nature\n'
        for move in self.moveset:
            pokepaste += f'- {move}\n' 
        return pokepaste
            
    def __repr__(self):
        return self.pokeDict