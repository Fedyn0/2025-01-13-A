import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):

        self._model.creaGrafo(self._view.dd_localization.value)

        nNodi, nArchi = self._model.getDettagliGrafo()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Creato grafo con {nNodi} nodi e {nArchi} archi")
        )

        archi = self._model.getSortedEdges()
        for a in archi:
            self._view.txt_result.controls.append(
                ft.Text(f"{a[0].GeneID} <-> {a[1].GeneID}: peso {a[2]["weight"]}")
            )
        self._view.btn_analizza_grafo.disabled = False
        self._view.update_page()



    def analyze_graph(self, e):
        connected_components = self._model.getConnectedComponents()

        self._view.txt_result.controls.append(
            ft.Text(f"Le componenti connesse sono: ")
        )

        for c in connected_components:
            listaID = []
            stringa = ""
            for gene in c:
                listaID.append(gene.GeneID)
            for i in listaID:
                stringa += f"{i}, "
            self._view.txt_result.controls.append(
                ft.Text(f"{stringa} | dimensione componente: {len(c)}")
            )

        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDLocalization(self):
        listaLocalizations = self._model.getAllLocalizations()

        for i in listaLocalizations:
            self._view.dd_localization.options.append(
                ft.dropdown.Option(i)
            )

    def ableBtn(self, e):
        self._view.btn_graph.disabled = False
        self._view.btn_analizza_grafo.disabled = True
        self._view.update_page()

