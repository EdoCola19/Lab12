import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        countries = DAO.getNazioni()
        for country in countries:
            self._listCountry.append(country)
            self._view.ddcountry.options.append(ft.dropdown.Option(country))
            #self._view._ddyear.options.append(ft.dropdown.Option(year))

        years = DAO.getAllYears()
        for year in years:
            self._listYear.append(year)
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view._page.update()




    def handle_graph(self, e):
        country = self._view.ddcountry.value
        year = self._view.ddyear.value
        if country is None and year is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un anno e una nazione prima di procedere"))
            self._view._page.update()
            return
        if country is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare una nazione"))
            self._view._page.update()
            return
        if year is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un anno"))
            self._view._page.update()
            return
        self._model.buildGraph(country, year)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo costruito con {len(self._model._grafo.nodes)} nodi e {len(self._model._grafo.edges)} archi"))
        self._view._page.update()



    def handle_volume(self, e):
        volumi = {}
        country = self._view.ddcountry.value
        year = self._view.ddyear.value
        grafo = self._model.getGraph(country, year)

        for nodo in grafo.nodes():
            volume = sum(data['weight'] for _, _, data in grafo.edges(nodo, data=True))
            volumi[nodo] = volume

        # Ordina i retailer per volume decrescente
        volumi_ordinati = sorted(volumi.items(), key=lambda x: x[1], reverse=True)

        # Se hai un mapping codice → nome
        for codice, volume in volumi_ordinati:
            nome = self._model._idRetailers[codice].name  # oppure self._idMap.get(codice).name
            print(f"{nome} → Volume: {volume}")

    def handle_path(self, e):
        pass
