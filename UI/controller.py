import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenre = None
        self._choiceArtist = None

    def fillDDArtist(self):
        allArtist = self._model.getArtists()
        for a in allArtist:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(data=a, key=a.Name, on_click=self._choiceDDArtist))

    def _choiceDDArtist(self, e):
        self._choiceArtist = e.control.data
        print(f"hai selezionato {self._choiceArtist.Name}")

    def fillDDGenre(self):
        allGenre = self._model.getAllGenre()
        for g in allGenre:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(data=g, key=g.Name, on_click=self._choiceDDGenre))

    def _choiceDDGenre(self, e):
        self._choiceGenre = e.control.data
        print(f"hai selezionato {self._choiceGenre.Name}")


    def handleCreaGrafo(self, e):
        if self._choiceGenre is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere un genere", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(self._choiceGenre)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Artista con maggiore influenza: {self._model.getInfluente()[0]} con influenza: {self._model.getInfluente()[1]} "))
        self._view.txt_result.controls.append(ft.Text("Top 5 archi con peso maggiore in ordine decrescente:"))
        for u,v,w in self._model.getTop5():
            self._view.txt_result.controls.append(ft.Text(f"{u} --> {v}: {w['weight']}"))
        self.fillDDArtist()
        self._view.update_page()


    def handleCammino(self,e):
        if self._choiceArtist is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Scegliere un artista", color="red"))
            self._view.update_page()
            return

        path, score = self._model.getLongestPath(self._choiceArtist)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ecco il cammino più lungo a partire dall'artista {self._choiceArtist}:"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.txt_result.controls.append(ft.Text(f"Score: {score}"))

        self._view.txt_result.controls.append(ft.Text("\n===========================================================\n"))

        pathV2, scoreV2 = self._model.getLongestPathV2(self._choiceArtist)
        self._view.txt_result.controls.append(
            ft.Text(f"Ecco il cammino più lungo con archi di peso crescente a partire dall'artista {self._choiceArtist}:"))
        for p in pathV2:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.txt_result.controls.append(ft.Text(f"Score: {scoreV2}"))
        self._view.update_page()



