PYTHON = python3        

.PHONY: all
all:
	@echo "Pour lancer le programme, veuillez exécuter la commande 'make test1', 'make test2', 'make soutenance_test1', 'make soutenance_test2', 'make soutenance_test3' ou 'make help'."

.PHONY: test1
test1:
	@echo "Running test 1"
	$(PYTHON) grammaire dossier_exemples/transformation1.general
	$(PYTHON) generer 4 transformation1.chomsky > test_4_chomsky.res
	$(PYTHON) generer 4 transformation1.greibach > test_4_greibach.res
	@echo "Différence entre les deux fichiers :"
	diff test_4_chomsky.res test_4_greibach.res

.PHONY: test2
test2:
	@echo "Running test 2"
	$(PYTHON) grammaire dossier_exemples/transformation2.general
	$(PYTHON) generer 4 transformation2.chomsky > test_4_chomsky.res
	$(PYTHON) generer 4 transformation2.greibach > test_4_greibach.res
	@echo "Différence entre les deux fichiers :"
	diff test_4_chomsky.res test_4_greibach.res

.PHONY: soutenance_test1
soutenance_test1:
	@echo "Running soutenance test 1"
	$(PYTHON) grammaire dossier_exemples/soutenance_test1.general
	$(PYTHON) generer 4 soutenance_test1.chomsky > test_4_chomsky.res
	$(PYTHON) generer 4 soutenance_test1.greibach > test_4_greibach.res
	@echo "Différence entre les deux fichiers :"
	diff test_4_chomsky.res test_4_greibach.res

.PHONY: soutenance_test2
soutenance_test2:
	@echo "Running soutenance test 2"
	$(PYTHON) grammaire dossier_exemples/soutenance_test2.general
	$(PYTHON) generer 4 soutenance_test2.chomsky > test_4_chomsky.res
	$(PYTHON) generer 4 soutenance_test2.greibach > test_4_greibach.res
	@echo "Différence entre les deux fichiers :"
	diff test_4_chomsky.res test_4_greibach.res

.PHONY: soutenance_test3
soutenance_test3:
	@echo "Running soutenance test 3"
	$(PYTHON) grammaire dossier_exemples/soutenance_test3.general
	$(PYTHON) generer 4 soutenance_test3.chomsky > test_4_chomsky.res
	$(PYTHON) generer 4 soutenance_test3.greibach > test_4_greibach.res
	@echo "Différence entre les deux fichiers :"
	diff test_4_chomsky.res test_4_greibach.res


.PHONY: help
help:
	@echo "Pour lancer le programme, veuillez exécuter la commande 'make test1', 'make test2', 'make soutenance_test1', 'make soutenance_test2', 'make soutenance_test3' ou 'make help'."


.PHONY: clean
clean:
	@echo "Rien à nettoyer pour ce projet."
