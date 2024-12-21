import re

class Grammaire:
    def __init__(self):
        self.axiome = "S"
        self.terminaux = set()
        self.non_terminaux = {self.axiome}
        self.regles = {}

    # Getters et Setters
    def get_terminaux(self):
        return self.terminaux
    
    def get_non_terminaux(self):
        return self.non_terminaux
    
    def get_axiome(self):
        return self.axiome
    
    def get_regles(self):
        return self.regles
    
    def set_axiome(self, axiome):
        self.axiome = axiome
    
    # Ajout des terminaux, non-terminaux et règles
    def ajout_terminal(self, terminal):
        self.terminaux.add(terminal)
    
    def ajout_non_terminal(self, non_terminal):
        self.non_terminaux.add(non_terminal)
    
    def ajout_regle(self, non_terminal, regle):
        if non_terminal in self.regles:
            self.regles[non_terminal].append(regle)
        else:
            self.regles[non_terminal] = [regle]

    def __str__(self):
        return f"Terminaux: {self.terminaux}\nNon-terminaux: {self.non_terminaux}\nAxiome: {self.axiome}\nRegles: {self.regles}"

    def est_algébrique(self):
        if any(key in self.terminaux for key in self.regles.keys()):
            return False
        return True
    
    def lire(self, file):
        with open(file) as file:
            data = file.readlines()
        
        for line in data:
            line = line.strip()
            membre_gauche, membre_droit = line.split(":")
            membre_droit = [part.strip() for part in membre_droit.split("|")]
            self.regles[membre_gauche.strip()] = [re.findall(fr'[A-Z][0-9]|[a-z]|{self.axiome}|E', symbol) for symbol in membre_droit]

    def suppression_axiome_membre_droit(self):
        regles = list(self.regles.items())

        for _, membre_droit in regles:
            for valeur in membre_droit:
                if self.axiome in valeur:
                    new_axiome = self.axiome + '0'
                    self.ajout_non_terminal(new_axiome)
                    for regle in self.regles[self.axiome]:
                        self.ajout_regle(new_axiome, regle)
                    self.set_axiome(new_axiome)
    
    def suppression_terminaux(self):
        regles = list(self.regles.items())

        for membre_gauche, membre_droit in regles :
            for i, regle in enumerate(membre_droit):
                for j, symbol in enumerate(regle):
                    if symbol in self.terminaux:
                        # Il faut changer ça (prendre le non-terminal respectif (A1, A2, A3, etc.))
                        new_non_terminal = f"{symbol.upper()}"
                        self.ajout_non_terminal(new_non_terminal)
                        self.ajout_regle(new_non_terminal, [symbol])
                        self.regles[membre_gauche][i][j] = new_non_terminal

    def simplification(self):

        # Retire l'axiome des membres droits des règles
        self.suppression_axiome_membre_droit()
        self.suppression_terminaux()





if __name__ == "__main__":
    print("\033c")
    grammaire_test = Grammaire()

    # Ajout des non-terminaux et terminaux
    alphabet = "ABCDFGHIJKLMNOPQRSTUVWXYZ"
    for letter in alphabet :
        grammaire_test.ajout_terminal(letter.lower())
        for i in range(1, 11):
            grammaire_test.ajout_non_terminal(f"{letter}{i}")

    grammaire_test.lire("test/test.general")
    #print(grammaire_test.get_regles())
    print()
    grammaire_test.simplification()
    #print()
    print(grammaire_test.get_regles())
    


    ########################### SECTION TEST #############################

    def test_lire(input):
        with open(input) as file:
            data = file.readlines()

        for line in data:
            line = line.strip()
            membre_gauche, membre_droit = line.split(":")
            membre_droit = [part.strip() for part in membre_droit.split("|")]
            print(f'MEMBRE GAUCHE: {membre_gauche}\nMEMBRE DROIT: {membre_droit}\n')