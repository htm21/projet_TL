import re
from collections import deque

class Grammaire:
    def __init__(self):
        self.__axiome = "S"
        self.__terminaux = set()
        self.__non_terminaux = {self.axiome}
        self.__regles = {}

    # Getters et Setters
    def get_terminaux(self):
        return self.__terminaux
    
    def get_non_terminaux(self):
        return self.__non_terminaux
    
    def get_axiome(self):
        return self.__axiome
    
    def get_regles(self):
        return self.__regles

    def get_non_terminal_non_utilise(self):
        for non_terminal in self.non_terminaux:
            if non_terminal not in self.regles.keys() and all(non_terminal not in regle for regle in self.regles.values()):
                return non_terminal
        return None
    def set_axiome(self, axiome):
        self.__axiome = axiome
        
    terminaux = property(get_terminaux)
    non_terminaux = property(get_non_terminaux)
    axiome = property(get_axiome, set_axiome)
    regles = property(get_regles)

    
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
        association_terminal_non_terminal = {} 

        for membre_gauche, membre_droit in regles :
            for i, regle in enumerate(membre_droit):
                if len(regle) >= 2:
                    for j, symbol in enumerate(regle):
                        if symbol in self.terminaux:

                            if symbol not in association_terminal_non_terminal:
                                nouveau_non_terminal = self.get_non_terminal_non_utilise()
                                
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

                        if nouvelle_regle not in self.regles[membre_gauche]:
                            self.ajout_regle(membre_gauche, nouvelle_regle)
                            #print(f"NOUVELLE REGLE: {nouvelle_regle} AJOUTEE A {membre_gauche}\n")
                        

        #print(f"TERMINAUX ANNULÉS: {terminaux_annule}\n")
        #print(f"FIN DE L'ITERATION\n{self.regles}\n")
              
    def suppression_epsilon(self):
        # Générer par GPT pour relancer tant que c'est nécessaire
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

    
    def iteration_suppression_regle_plus_deux_non_terminaux_membre_droite(self):
        regles = list(self.regles.items()) 
        #print('-'*50)

        for membre_gauche, membre_droit in regles:
            nouvelles_regles = []  

            for regle in membre_droit :  
                nb_non_terminaux = sum(1 for symbol in regle if symbol in self.non_terminaux)
                if nb_non_terminaux > 2 :
                    compteur = 0
                    for i, symbol in enumerate(regle):
                        if symbol in self.non_terminaux and compteur < 2: 
                            compteur += 1
                            continue

                        if compteur == 2:
                            nouveau_non_terminal = self.get_non_terminal_non_utilise()
                            regle_modif = regle[:i-1] + [nouveau_non_terminal]
                            nouvelle_regle = regle[i-1:]

                            self.ajout_regle(nouveau_non_terminal, nouvelle_regle)
                            nouvelles_regles.append(regle_modif)

                            #print(f"\nANCIENNE REGLE: {regle}\nREGLE MODIF: {regle_modif}\nNOUVELLE REGLE: {nouvelle_regle}")
                            break
                else:
                    nouvelles_regles.append(regle)

            self.regles[membre_gauche] = nouvelles_regles
            
    def suppression_regle_plus_deux_non_terminaux_membre_droite(self):
        # Générer par GPT pour relancer tant que c'est nécessaire
        while any(
            sum(1 for symbol in regle if symbol in self.non_terminaux) > 2
            for membre_gauche, membre_droit in self.regles.items()
            for regle in membre_droit
        ):
            self.iteration_suppression_regle_plus_deux_non_terminaux_membre_droite()

    def suppression_non_terminaux_en_tete(self):
        for non_terminal, regles in list(self.regles.items()):
            nouvelles_regles = []

            for regle in regles:
                if regle[0] in self.non_terminaux:
                    for nouvelle_regle in self.regles[regle[0]]:
                        nouvelles_regles.append(nouvelle_regle + regle[1:])
                else:
                    nouvelles_regles.append(regle)

            self.regles[non_terminal] = nouvelles_regles

    def suppression_terminaux_non_en_tete(self):
        regles = list(self.regles.items())

        for membre_gauche, membre_droit in regles:
            for regle in membre_droit :
                for i, symbol in enumerate(regle) :
                    if symbol in self.terminaux and i > 0:
                        nouveau_non_terminal = self.get_non_terminal_non_utilise()
                        self.ajout_non_terminal(nouveau_non_terminal)
                        self.ajout_regle(nouveau_non_terminal, [symbol])
                        regle[i] = nouveau_non_terminal


    def afficher_productions(self):
        """
        Affiche les productions d'une grammaire de manière lisible.
        Généré par GPT pour faciliter la lecture
        """
        print("Productions de la grammaire :")
        for non_terminal, rules in self.regles.items():
            rules_str = " | ".join([" ".join(rule) for rule in rules])
            print(f"{non_terminal} -> {rules_str}")


    ################################## SECTION TRANSFORMATION #################################

    def transformation_greibach(self):
        '''Forme normale de Greibach'''
        
        if self.est_algébrique():
            self.suppression_axiome_membre_droit()
            self.suppression_epsilon()
            self.suppression_regle_unite()
            self.suppression_non_terminaux_en_tete()
            self.suppression_terminaux_non_en_tete()
            
    def transformation_chomsky(self):
        '''Forme normale de Chomsky'''

        if self.est_algébrique() :
            self.suppression_axiome_membre_droit()
            self.suppression_terminaux()
            self.suppression_regle_plus_deux_non_terminaux_membre_droite()
            self.suppression_epsilon()
            self.suppression_regle_unite()

    ################################## SECTION ENUMERATION #################################

    def generer_mots(self, longueur_max):

        mots = set()
        queue = deque([(self.axiome, "")])

        while queue:
            non_terminal, prefixe = queue.popleft()

            if len(prefixe) > longueur_max:
                continue

            for regle in self.regles.get(non_terminal, []):
                nouveau_mot = prefixe
                termine = True

                for symbole in regle:
                    if symbole in self.non_terminaux:
                        queue.append((symbole, nouveau_mot))
                        termine = False
                    else:
                        nouveau_mot += symbole

                if termine and len(nouveau_mot) <= longueur_max:
                    mots.add(nouveau_mot)

        return sorted([mot for mot in mots])


    ################################## SECTION PRINCIPALE #################################

if __name__ == "__main__":
    print("\033c")
    grammaire_test = Grammaire()

    # Ajout des non-terminaux et terminaux
    alphabet = "ABCDFGHIJKLMNOPQRSTUVWXYZ"
    for letter in alphabet :
        grammaire_test.ajout_terminal(letter.lower())
        for i in range(1, 11):
            grammaire_test.ajout_non_terminal(f"{letter}{i}")



    ################################## SECTION TEST #################################

    def test_lire(input):
        print('\n--- TEST LECTURE ---\n')
        with open(input) as file:
            data = file.readlines()

        for line in data:
            line = line.strip()
            membre_gauche, membre_droit = line.split(":")
            membre_droit = [part.strip() for part in membre_droit.split("|")]
            print(f'MEMBRE GAUCHE: {membre_gauche}\nMEMBRE DROIT: {membre_droit}\n')

    #test_lire("test/test_lecture.general")

    def test_suppression_terminaux(input):
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION TERMINAUX ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_terminaux()
        print('\nAPRES SUPPRESSION TERMINAUX\n')
        grammaire_test.afficher_productions()

    #test_suppression_terminaux("test/suppression_terminaux.general")
    
    def test_suppression_epsilon(input):
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION EPSILON ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_epsilon()
        print('\nAPRES SUPPRESSION EPSILON\n')
        grammaire_test.afficher_productions()
    
    #test_suppression_epsilon("test/suppression_epsilon.general")

    def test_suppression_regle_unite(input):
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION REGLE UNITE ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_regle_unite()
        print('\nAPRES SUPPRESSION REGLE UNITE\n')
        grammaire_test.afficher_productions()
    
    #test_suppression_regle_unite("test/suppression_regle_unite.general")

    def test_suppression_regle_plus_deux_non_terminaux_membre_droite(input):
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION REGLE PLUS DE DEUX NON TERMINAUX MEMBRE DROITE ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_regle_plus_deux_non_terminaux_membre_droite()
        print('\nAPRES SUPPRESSION REGLE PLUS DE DEUX NON TERMINAUX MEMBRE DROITE\n')
        grammaire_test.afficher_productions()
    
    #test_suppression_regle_plus_deux_non_terminaux_membre_droite("test/suppression_regle_longue_non_terminal.general")

    def test_transformation_greibach(input):
        grammaire_test.lire(input)
        num_regle = input.split(".")[0][-1]
        print(f'--- TEST GREIBACH n°{num_regle} ---\n')
        grammaire_test.afficher_productions()
        grammaire_test.transformation_greibach()
        print('\n--- APRES GREIBACH ---\n')
        grammaire_test.afficher_productions()
        print()
    
    #test_transformation_greibach("test/transformation1.general")
    #test_transformation_greibach("test/transformation2.general")

    def test_transformation_chomsky(input):
        grammaire_test.lire(input)
        num_regle = input.split(".")[0][-1]
        print(f'--- TEST CHOMSKY n°{num_regle} ---\n')
        grammaire_test.afficher_productions()
        grammaire_test.transformation_chomsky()
        print('\n--- APRES CHOMSKY ---\n')
        grammaire_test.afficher_productions()
        print()
    
    #test_transformation_chomsky("test/transformation1.general")
    #test_transformation_chomsky("test/transformation2.general")


