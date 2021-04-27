import networkx as nx

# Main
G = nx.DiGraph()
G.add_edges_from([("IDLE", "Ruch do ladunku"),
                 ("Ruch do ladunku", "Zgloszenie problemu"),
                 ("Ruch do ladunku", "Zaladowanie ladunku"),
                 ("Zgloszenie problemu", "IDLE"),
                 ("Zaladowanie ladunku", "Ruch do magazynu"),
                 ("Ruch do magazynu", "Odlozenie ladunku"),
                 ("Ruch do magazynu", "Czekanie na zwolnienie miejsca"),
                 ("Odlozenie ladunku", "IDLE"),
                 ("Czekanie na zwolnienie miejsca", "Odlozenie ladunku")])
                 
edge_labels = {("IDLE", "Ruch do ladunku"): "Nowy ladunek",
               ("Ruch do ladunku", "Zgloszenie problemu"): "Nie wykryto ladunku",
               ("Ruch do ladunku", "Zaladowanie ladunku"): "Wykrycie ladunku",
               ("Zgloszenie problemu", "IDLE"): "Anulowanie zadania",
               ("Zaladowanie ladunku", "Ruch do magazynu"): "Otrzymanie punktu skladowania",
               ("Ruch do magazynu", "Odlozenie ladunku"): "Wykrycie wolnego miejsca",
               ("Ruch do magazynu", "Czekanie na zwolnienie miejsca"): "Brak wolnego miejsca",
               ("Odlozenie ladunku", "IDLE"): "Potwierdzenie wykonania zadania",
               ("Czekanie na zwolnienie miejsca", "Odlozenie ladunku"): "Wykrycie wolnego miejsca"}
               
pos = nx.planar_layout(G)



# Navigation
G_nav = nx.MultiDiGraph()
G_nav.add_edges_from([("Czekanie na nowy ladunek", "Planowanie trasy i ruch"),
                 ("Planowanie trasy i ruch", "Czekanie na nowy ladunek"),
                 ("Planowanie trasy i ruch", "Zatrzymanie robota"),
                 ("Zatrzymanie robota", "Planowanie trasy i ruch"),
                 ("Zatrzymanie robota", "Czekanie na nowy ladunek")])
                 
edge_labels_nav = [{("Czekanie na nowy ladunek", "Planowanie trasy i ruch"): "Nowy ladunek",
               ("Zatrzymanie robota", "Planowanie trasy i ruch"): "Brak kolizji"},
               {("Planowanie trasy i ruch", "Zatrzymanie robota"): "Wykrycie kolizji",
               ("Planowanie trasy i ruch", "Czekanie na nowy ladunek"): "Wykonanie ruchu",
               ("Zatrzymanie robota", "Czekanie na nowy ladunek"): "Przerwanie zadania"}]

pos_nav = nx.planar_layout(G_nav)