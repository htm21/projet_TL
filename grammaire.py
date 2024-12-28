import sys
from main import Grammaire

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <fichier_grammaire>")
        sys.exit(1)

    fichier_grammaire = sys.argv[1]

    try:
        grammaire = Grammaire()
        grammaire.lire(fichier_grammaire)

        print("\033c") 
        print("Grammaire lue :")
        grammaire.afficher_productions()

        print("\nTransformation en forme normale de Chomsky:")
        grammaire.transformation_chomsky()
        grammaire.afficher_productions()

        print("\nTransformation en forme normale de Greibach:")
        grammaire.transformation_greibach()
        grammaire.afficher_productions()

        print("\nLangage généré (longueur maximale 5):")
        mots = grammaire.enumere_mots_langage(5)
        print("\n".join(mots))

    except FileNotFoundError:
        print(f"Erreur : le fichier '{fichier_grammaire}' est introuvable.")
        sys.exit(1)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
