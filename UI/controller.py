import flet as ft
from UI.view import View
from database.DAO import DAO
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        if self._view.dd_min_ch.value is None:
            self._view.create_alert("Selezionare un valore per Chromosoma min")
            return
        else:
            ch_min = int(self._view.dd_min_ch.value)

        if self._view.dd_max_ch.value is None:
            self._view.create_alert("Selezionare un valore per Chromosoma max")
            return
        else:
            ch_max = int(self._view.dd_max_ch.value)

        if ch_min > ch_max:
            self._view.create_alert("Attenzione: deve essere Chromosoma min <= Chromosoma max")
            return

        self._model.buildGraph(ch_min, ch_max)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Creato grafo con {self._model.getNumNodi()} nodi"
                                                       f" e {self._model.getNumArchi()} archi"))

        maxNodi = self._model.getNodiPesati()
        self._view.txt_result1.controls.append(ft.Text(f"I 5 nodi col maggior numero di archi uscenti sono:"))
        for n in maxNodi:
            self._view.txt_result1.controls.append(ft.Text(f"{n[0]} | num. archi uscenti: {n[1]} | peso tot. {n[2]} "))

        self._view.btn_dettagli.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()


    def handle_dettagli(self, e):
        pass


    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        cammino_ottimo, costo_ottimo = self._model.trovaCammino()
        self._view.txt_result2.controls.append(ft.Text(f"Trovato un cammino ottimo di lunghezza {len(cammino_ottimo)}"))
        self._view.txt_result2.controls.append(ft.Text(f"Il costo del cammino ottimo è {costo_ottimo}"))
        self._view.txt_result2.controls.append(ft.Text(f"Le fermate del cammino sono:"))
        for n in cammino_ottimo:
            self._view.txt_result2.controls.append(ft.Text(f"{n}"))
        self._view.update_page()


    def fillDDMin(self):
        for n in DAO.get_all_chromosoma():
            self._view.dd_min_ch.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillDDMax(self):
        for n in DAO.get_all_chromosoma():
            self._view.dd_max_ch.options.append(ft.dropdown.Option(n))
        self._view.update_page()


    def fillDDLocalization(self):
        values = self._model.get_localizations()
        for v in values:
            self._view.dd_localization.options.append(ft.dropdown.Option(v))
        self._view.update_page()
