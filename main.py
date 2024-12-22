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
        if non_terminal in self.regles and regle not in self.regles[non_terminal]:
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
            self.regles[membre_gauche.strip()] = [re.findall(fr'[A-Z][0-9]|[a-z]|{self.axiome}|[A-Z]', symbol) for symbol in membre_droit]

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
        association_terminal_non_terminal = {} 

        for membre_gauche, membre_droit in regles :
            for i, regle in enumerate(membre_droit):
                for j, symbol in enumerate(regle):
                    if symbol in self.terminaux:

                        if symbol not in association_terminal_non_terminal:
                            for non_terminal in self.non_terminaux:
                                if non_terminal not in association_terminal_non_terminal.values():
                                    nouveau_non_terminal = non_terminal
                                    break
                            
                            association_terminal_non_terminal[symbol] = nouveau_non_terminal

                            self.ajout_non_terminal(nouveau_non_terminal)
                            self.ajout_regle(nouveau_non_terminal, [symbol])

                        self.regles[membre_gauche][i][j] = nouveau_non_terminal

    def iteration_suppression_epsilon(self):
        terminaux_annule = set()

        for membre_gauche, membre_droit in self.regles.items():
            for regle in membre_droit:
                for symbol in regle:
                    if symbol == "E":
                        if membre_gauche != self.axiome:
                            terminaux_annule.add(membre_gauche)
                            self.regles[membre_gauche].remove(regle)
                            break
        
        for membre_gauche, membre_droit in self.regles.items():
            for regle in membre_droit:
                for i, symbol in enumerate(regle):
                    if symbol in terminaux_annule:
                        nouvelle_regle = regle[:i] + regle[i+1:]
                        if len(nouvelle_regle) == 0:
                            nouvelle_regle = ["E"]

                        #print(f"MEMBRE GAUCHE: {membre_gauche}\nREGLE: {regle}\nNOUVELLE REGLE: {nouvelle_regle}\n")

                        self.ajout_regle(membre_gauche, nouvelle_regle)
                        break

        #print(f"TERMINAUX ANNULÉS: {terminaux_annule}\n")
        #print(f"FIN DE L'ITERATION\n{self.regles}\n")
              
    def suppression_epsilon(self):
        # Générer par GPT, permet de relancer itération par itération
        while any(
            regle == ["E"] and membre_gauche != self.axiome
            for membre_gauche, membre_droit in self.regles.items()
            for regle in membre_droit
        ):
            self.iteration_suppression_epsilon()
    
    def suppression_regle_unite(self):
        regles = list(self.regles.items())

        for membre_gauche, membre_droit in regles:
            for regle in membre_droit: 
                if len(regle) == 1 and regle[0] in self.non_terminaux and regle[0] != membre_gauche:
                    symbol = regle[0]

                    for nouvelle_regle in self.regles[symbol]:
                        if nouvelle_regle not in self.regles[membre_gauche]:
                            self.ajout_regle(membre_gauche, nouvelle_regle)

                    self.regles[membre_gauche].remove(regle)

    def suppression_regle_plus_deux_non_terminaux_membre_droite(self):
        pass
    
    def simplification(self):

        # Retire l'axiome des membres droits des règles
        self.suppression_axiome_membre_droit()
        # Remplace les terminaux par des non-terminaux
        self.suppression_terminaux()
        # Supprime les epsilon des règles X -> E sauf pour l'axiome
        self.suppression_epsilon()
        # Supprime les règles unité X -> Y
        self.suppression_regle_unite()

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
    print(f'AVANT: {grammaire_test.get_regles()}\n') 
    grammaire_test.simplification()
    print(f'APRÈS: {grammaire_test.get_regles()}\n')
    
    ########################### SECTION TEST #############################

    def test_lire(input):
        with open(input) as file:
            data = file.readlines()

        for line in data:
            line = line.strip()
            membre_gauche, membre_droit = line.split(":")
            membre_droit = [part.strip() for part in membre_droit.split("|")]
            print(f'MEMBRE GAUCHE: {membre_gauche}\nMEMBRE DROIT: {membre_droit}\n')
    
    def test_suppression_epsilon(input):
        grammaire_test.lire(input)
        grammaire_test.suppression_epsilon()
    
    #test_suppression_epsilon("test/suppression_epsilon.general")

    def test_suppression_regle_unite(input):
        grammaire_test.lire(input)
        print(f'AVANT: {grammaire_test.get_regles()}\n')
        grammaire_test.suppression_regle_unite()
        print(f'APRÈS: {grammaire_test.get_regles()}\n')
    
    #test_suppression_regle_unite("test/suppression_regle_unite.general")
