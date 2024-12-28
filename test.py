from main import Grammaire 
  ################################## SECTION PRINCIPALE #################################

if __name__ == "__main__":
    print("\033c")
    grammaire_test = Grammaire()
    grammaire_test2 = Grammaire()

    # Ajout des non-terminaux et terminaux
    alphabet = "ABCDFGHIJKLMNOPQRSTUVWXYZ"
    for letter in alphabet :
        grammaire_test.ajout_terminal(letter.lower())
        grammaire_test2.ajout_terminal(letter.lower())
        for i in range(1, 11):
            grammaire_test.ajout_non_terminal(f"{letter}{i}")
            grammaire_test2.ajout_non_terminal(f"{letter}{i}")



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

    test_lire("test/test_lecture.general")

    def test_suppression_terminaux(input):
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION TERMINAUX ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_terminaux()
        print('\nAPRES SUPPRESSION TERMINAUX\n')
        grammaire_test.afficher_productions()

    test_suppression_terminaux("test/suppression_terminaux.general")
    
    def test_suppression_epsilon(input):
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION EPSILON ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_epsilon()
        print('\nAPRES SUPPRESSION EPSILON\n')
        grammaire_test.afficher_productions()
    
    test_suppression_epsilon("test/suppression_epsilon.general")

    def test_suppression_regle_unite(input):
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION REGLE UNITE ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_regle_unite()
        print('\nAPRES SUPPRESSION REGLE UNITE\n')
        grammaire_test.afficher_productions()
    
    test_suppression_regle_unite("test/suppression_regle_unite.general")

    def test_suppression_regle_plus_deux_non_terminaux_membre_droite(input):
        grammaire_test.lire(input)
        print('---- TEST SUPPRESSION REGLE PLUS DE DEUX NON TERMINAUX MEMBRE DROITE ----\n')
        grammaire_test.afficher_productions()
        grammaire_test.suppression_regle_plus_deux_non_terminaux_membre_droite()
        print('\nAPRES SUPPRESSION REGLE PLUS DE DEUX NON TERMINAUX MEMBRE DROITE\n')
        grammaire_test.afficher_productions()
    
    test_suppression_regle_plus_deux_non_terminaux_membre_droite("test/suppression_regle_longue_non_terminal.general")

    def test_transformation_greibach(input):
        grammaire_test.lire(input)
        num_regle = input.split(".")[0][-1]
        print(f'--- TEST GREIBACH n°{num_regle} ---\n')
        grammaire_test.afficher_productions()
        grammaire_test.transformation_greibach()
        print('\n--- APRES GREIBACH ---\n')
        grammaire_test.afficher_productions()
        print()
    

    def test_transformation_chomsky(input):
        grammaire_test.lire(input)
        num_regle = input.split(".")[0][-1]
        print(f'--- TEST CHOMSKY n°{num_regle} ---\n')
        grammaire_test.afficher_productions()
        grammaire_test.transformation_chomsky()
        print('\n--- APRES CHOMSKY ---\n')
        grammaire_test.afficher_productions()
        print()
    
    test_transformation_chomsky("test/transformation1.general")
    test_transformation_chomsky("test/transformation2.general")

    def test_enumere_mots_langage(input, n):
        print("--- TEST ENUMERATION ---\n")
        grammaire_test.lire(input)
        grammaire_test2.lire(input)
        grammaire_test.transformation_greibach()
        grammaire_test2.transformation_chomsky()
    
        a = grammaire_test.enumere_mots_langage(n)
        b = grammaire_test2.enumere_mots_langage(n)

        print(f"Les mots générés par la forme normale de Greibach : {a}\n")
        print(f"Les mots générés par la forme normale de Chomsky : {b}\n")
        print(f"Les deux formes génèrent les mêmes mots : {a == b}\n")

    test_enumere_mots_langage("test/transformation1.general", 7)        