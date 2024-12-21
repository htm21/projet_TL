class Grammaire:
    def __init__(self):
        self.terminaux = set()
        self.non_terminaux = set()
        self.axiome = "S"
        self.regles = {}
    
    def __str__(self):
        return f"Terminaux: {self.terminaux}\nNon-terminaux: {self.non_terminaux}\nAxiome: {self.axiome}\nRegles: {self.regles}"
    
    def get_regles(self):
        return self.regles

    def ajout_terminal(self, terminal):
        self.terminaux.add(terminal)
    
    def ajout_non_terminal(self, non_terminal):
        self.non_terminaux.add(non_terminal)


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
            self.regles[membre_gauche] = [list(symbol) for symbol in membre_droit]



if __name__ == "__main__":
    print("\033c")
    grammaire_test = Grammaire()


    alphabet = "ABCDFGHIJKLMNOPQRSTUVWXYZ"
    for letter in alphabet :
        for i in range(1, 11):
            grammaire_test.ajout_terminal(f"{letter}{i}")

    print(grammaire_test.est_algébrique())
    grammaire_test.lire("test.general")
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