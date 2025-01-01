import re

class Grammaire:

    def __init__(self):
        self.__axiome = None
        self.__terminaux = set()
        self.__non_terminaux = set()
        self.__regles = {}
        alphabet = "ABCDFGHIJKLMNOPQRSTUVWXYZ"
        for letter in alphabet:
            self.ajout_terminal(letter.lower())
            for i in range(1, 11):
                self.ajout_non_terminal(f"{letter}{i}")
        self.ajout_terminal("e")

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
        if non_terminal in self.regles:
            if regle not in self.regles[non_terminal]:
                self.regles[non_terminal].append(regle)
        else:
            self.regles[non_terminal] = [regle]

    def __str__(self):
        """ Affiche le contenu de la structure de donnée (grammaire) de manière lisible. """

        return f"Terminaux: {self.terminaux}\nNon-terminaux: {self.non_terminaux}\nAxiome: {self.axiome}\nRegles: {self.regles}"

    ################################## SECTION LECTURE/ECRITURE DE FICHIER #################################

    def lire(self, file):
        """ Lit une grammaire depuis un fichier texte avec extension .general uniquement. """

        with open(file) as file:
            data = file.readlines()
        
        for line in data:
            line = line.strip()
            if not line or ":" not in line:
                continue
            membre_gauche, membre_droit = line.split(":")
            membre_droit = [part.strip() for part in membre_droit.split("|")]
            membre_gauche = membre_gauche.strip()
            if membre_gauche in self.non_terminaux :
                if self.regles == {}:
                    self.set_axiome(membre_gauche)

                membre_droit = [re.findall(fr'[A-Z](?:10|[1-9])|[a-z]|{self.axiome}|E', symbol) for symbol in membre_droit]
                if membre_gauche not in self.regles :
                    self.regles[membre_gauche] = membre_droit
                else:
                    for regle in membre_droit :
                        self.ajout_regle(membre_gauche, regle)

    def ecrire(self, file):
            """ Écrit la grammaire dans un fichier texte. """
            with open(file, "w") as file:
                for membre_gauche, membre_droit in self.regles.items():
                    membre_droit = " | ".join([" ".join(part) for part in membre_droit])
                    file.write(f"{membre_gauche} : {membre_droit}\n")

    ################################## SECTION SIMPLIFICATION #################################

    def est_algébrique(self):
        """ Vérifie si la grammaire est algébrique. """

        if any(key in self.terminaux for key in self.regles.keys()):
            return False
        return True

    def suppression_axiome_membre_droit(self):
        """ Supprime l'axiome des membres droits de règles. """

        regles = list(self.regles.items())

        for _, membre_droit in regles:
            for valeur in membre_droit:
                if self.axiome in valeur:
                    new_axiome = self.get_non_terminal_non_utilise()
                    for regle in self.regles[self.axiome]:
                        self.ajout_regle(new_axiome, regle)
                    self.set_axiome(new_axiome)
    
    def suppression_terminaux(self):
        """ Supprime les terminaux. """

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

                                self.ajout_regle(nouveau_non_terminal, [symbol])

                            self.regles[membre_gauche][i][j] = nouveau_non_terminal

    def iteration_suppression_epsilon(self):
        """ Itère la suppression des règles epsilon. """

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
                                      
    def suppression_epsilon(self):
        """ Supprime les règles epsilon. """

        while any(
            regle == ["E"] and membre_gauche != self.axiome
            for membre_gauche, membre_droit in self.regles.items()
            for regle in membre_droit
        ):
            self.iteration_suppression_epsilon()
    
    def suppression_regle_unite(self):
        """ Supprime les règles unités. """

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
        """ Itère la suppression des règles contenant plus de deux non-terminaux dans le membre droit. """

        regles = list(self.regles.items()) 

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
                            break
                else:
                    nouvelles_regles.append(regle)

            self.regles[membre_gauche] = nouvelles_regles
            
    def suppression_regle_plus_deux_non_terminaux_membre_droite(self):
        """ Supprime les règles contenant plus de deux non-terminaux dans le membre droit. """

        while any(
            sum(1 for symbol in regle if symbol in self.non_terminaux) > 2
            for membre_gauche, membre_droit in self.regles.items()
            for regle in membre_droit
        ):
            self.iteration_suppression_regle_plus_deux_non_terminaux_membre_droite()

    def suppression_non_terminaux_en_tete(self):
        """ Supprime les non-terminaux en tête de règle. """

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
        """ Supprime les terminaux non en tête de règle. """

        regles = list(self.regles.items())

        for membre_gauche, membre_droit in regles:
            for regle in membre_droit :
                for i, symbol in enumerate(regle) :
                    if symbol in self.terminaux and i > 0:
                        nouveau_non_terminal = self.get_non_terminal_non_utilise()
                        self.ajout_regle(nouveau_non_terminal, [symbol])
                        regle[i] = nouveau_non_terminal
                        
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

    ################################## SECTION ENUMERATION DE MOTS #################################

    def contient_que_des_terminaux(self, w):
        return all(symbol in self.terminaux for symbol in w)

    def enumere_mots(self, n, w, langage) :

        if len(w) > n :
            return
        
        if self.contient_que_des_terminaux(w) :
            langage.add("".join(w))
            return
        
        for i in range(len(w)) :
            if w[i] in self.non_terminaux :
                for w3 in self.regles[w[i]] :
                    w2 = w[:i] + w3 + w[i+1:]

                    self.enumere_mots(n, w2, langage)
    
    def enumere_mots_langage(self, n) :
        langage = set()
        self.enumere_mots(n, [self.axiome], langage)
        langage.add("E")
        return sorted(langage, key=lambda x: (len(x), x))

    ################################## SECTION ANNEXE #################################

    def afficher_productions(self):
        """
        Affiche les productions d'une grammaire de manière lisible.
        Permet une communication plus claire avec l'utilisateur.
        Généré par ChatGPT.
        """
        print("Productions de la grammaire :")
        for non_terminal, rules in self.regles.items():
            rules_str = " | ".join([" ".join(rule) for rule in rules])
            print(f"{non_terminal} -> {rules_str}")
    
    ################################## SECTION PRINCIPALE #################################

if __name__ == "__main__":
    print("\033c")

    ################################## SECTION TEST #################################

    def test_lire(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        print('---- TEST LECTURE ----\n')
        grammaire_test.afficher_productions()

    test_lire("dossier_exemples/test_lecture.general")

    def test_suppression_axiome_membre_droit(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION AXIOME MEMBRE DROIT ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_axiome_membre_droit()
        print('\nAPRES SUPPRESSION AXIOME MEMBRE DROIT\n')
        grammaire_test.afficher_productions()
    
    test_suppression_axiome_membre_droit("dossier_exemples/axiome_membre_droit.general")

    def test_suppression_terminaux(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION TERMINAUX ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_terminaux()
        print('\nAPRES SUPPRESSION TERMINAUX\n')
        grammaire_test.afficher_productions()

    test_suppression_terminaux("dossier_exemples/suppression_terminaux.general")
    
    def test_suppression_epsilon(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION EPSILON ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_epsilon()
        print('\nAPRES SUPPRESSION EPSILON\n')
        grammaire_test.afficher_productions()
    
    test_suppression_epsilon("dossier_exemples/suppression_epsilon.general")

    def test_suppression_regle_unite(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION REGLE UNITE ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_regle_unite()
        print('\nAPRES SUPPRESSION REGLE UNITE\n')
        grammaire_test.afficher_productions()
    
    test_suppression_regle_unite("dossier_exemples/suppression_regle_unite.general")

    def test_suppression_regle_plus_deux_non_terminaux_membre_droite(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION REGLE PLUS DE DEUX NON TERMINAUX MEMBRE DROITE ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_regle_plus_deux_non_terminaux_membre_droite()
        print('\nAPRES SUPPRESSION REGLE PLUS DE DEUX NON TERMINAUX MEMBRE DROITE\n')
        grammaire_test.afficher_productions()
    
    test_suppression_regle_plus_deux_non_terminaux_membre_droite("dossier_exemples/suppression_regle_longue_non_terminal.general")

    def test_suppression_non_terminaux_en_tete(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION NON TERMINAUX EN TETE ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_non_terminaux_en_tete()
        print('\nAPRES SUPPRESSION NON TERMINAUX EN TETE\n')
        grammaire_test.afficher_productions()
    
    test_suppression_non_terminaux_en_tete("dossier_exemples/suppression_non_terminaux_tete.general")

    def test_suppression_terminaux_non_en_tete(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION TERMINAUX NON EN TETE ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_terminaux_non_en_tete()
        print('\nAPRES SUPPRESSION TERMINAUX NON EN TETE\n')
        grammaire_test.afficher_productions()
    
    test_suppression_terminaux_non_en_tete("dossier_exemples/supprime_terminaux_non_tete.general")

    def test_transformation_greibach(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        num_regle = input.split(".")[0][-1]
        print(f'--- TEST GREIBACH n°{num_regle} ---\n')
        grammaire_test.afficher_productions()
        grammaire_test.transformation_greibach()
        print('\n--- APRES GREIBACH ---\n')
        grammaire_test.afficher_productions()
        print()
    
    test_transformation_greibach("dossier_exemples/transformation1.general")
    test_transformation_greibach("dossier_exemples/transformation2.general")

    def test_transformation_chomsky(input):
        grammaire_test = Grammaire()
        grammaire_test.lire(input)
        num_regle = input.split(".")[0][-1]
        print(f'--- TEST CHOMSKY n°{num_regle} ---\n')
        grammaire_test.afficher_productions()
        grammaire_test.transformation_chomsky()
        print('\n--- APRES CHOMSKY ---\n')
        grammaire_test.afficher_productions()
        print()
    
    test_transformation_chomsky("dossier_exemples/transformation1.general")
    test_transformation_chomsky("dossier_exemples/transformation2.general")

    def test_enumere_mots_langage(input, n):
        grammaire_test = Grammaire()
        grammaire_test2 = Grammaire()
        print("--- TEST ENUMERATION ---\n")
        grammaire_test.lire(input)
        grammaire_test2.lire(input)
        print("--- GRAMMAIRE INITIALE ---")
        grammaire_test.afficher_productions()
        print("\n--- APRES TRANSFORMATIONS ---")
        grammaire_test.transformation_greibach()
        grammaire_test2.transformation_chomsky()
    
        a = grammaire_test.enumere_mots_langage(n)
        b = grammaire_test2.enumere_mots_langage(n)

        print(f"Les mots générés par la forme normale de Greibach : {a}")
        print(f"Les mots générés par la forme normale de Chomsky : {b}\n")
        print(f"Les deux formes génèrent les mêmes mots : {a == b}\n")

    test_enumere_mots_langage("dossier_exemples/transformation2.general", 5)   