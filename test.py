print("\033c")
class Grammaire:
    def __init__(self):
        self.terminaux = set()
        self.non_terminaux = set()
        self.axiome = "S"
        self.regles = {}
    
    def __str__(self):
        return f"Terminaux: {self.terminaux}\nNon-terminaux: {self.non_terminaux}\nAxiome: {self.axiome}\nRegles: {self.regles}"

    def ajout_terminal(self, terminal):
        self.terminaux.add(terminal)
    
    def ajout_non_terminal(self, non_terminal):
        self.non_terminaux.add(non_terminal)


    def est_algébrique(self):
        if any(key in self.terminaux for key in self.regles.keys()):
            return False
        return True


grammaire_test = Grammaire()
grammaire_test.ajout_terminal("a")
grammaire_test.ajout_terminal("b")
grammaire_test.ajout_terminal("E")
grammaire_test.ajout_non_terminal("S")
grammaire_test.regles["S"] = [list("aSbS"), list("a"), list("b"), list("E")]


print(grammaire_test)
print(f"La grammaire est-elle algébrique ? {grammaire_test.est_algébrique()}")