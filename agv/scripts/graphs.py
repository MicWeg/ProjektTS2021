import networkx as nx


# Storage
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
               
# pos = nx.spring_layout(G)
# pos = nx.circular_layout(G)
# pos = nx.kamada_kawai_layout(G)
# pos = nx.spectral_layout(G)
pos = nx.planar_layout(G)



# Navigation
G_nav = nx.DiGraph()
# G_nav.add_edges_from([("IDLE", "Ruch do ladunku"),
#                  ("Ruch do ladunku", "Zgloszenie problemu"),
#                  ("Ruch do ladunku", "Zaladowanie ladunku"),
#                  ("Zgloszenie problemu", "IDLE"),
#                  ("Zaladowanie ladunku", "Ruch do magazynu"),
#                  ("Ruch do magazynu", "Odlozenie ladunku"),
#                  ("Ruch do magazynu", "Czekanie na zwolnienie miejsca"),
#                  ("Odlozenie ladunku", "IDLE"),
#                  ("Czekanie na zwolnienie miejsca", "Odlozenie ladunku")])
                 
# edge_labels_nav = {("IDLE", "Ruch do ladunku"): "Nowy ladunek",
#                ("Ruch do ladunku", "Zgloszenie problemu"): "Nie wykryto ladunku",
#                ("Ruch do ladunku", "Zaladowanie ladunku"): "Wykrycie ladunku",
#                ("Zgloszenie problemu", "IDLE"): "Anulowanie zadania",
#                ("Zaladowanie ladunku", "Ruch do magazynu"): "Otrzymanie punktu skladowania",
#                ("Ruch do magazynu", "Odlozenie ladunku"): "Wykrycie wolnego miejsca",
#                ("Ruch do magazynu", "Czekanie na zwolnienie miejsca"): "Brak wolnego miejsca",
#                ("Odlozenie ladunku", "IDLE"): "Potwierdzenie wykonania zadania",
#                ("Czekanie na zwolnienie miejsca", "Odlozenie ladunku"): "Wykrycie wolnego miejsca"}
G_nav.add_edges_from([("IDLE", "A"),
                 ("A", "B"),
                 ("B", "IDLE")])
                 
edge_labels_nav = {("IDLE", "A"): "A",
               ("A", "B"): "B",
               ("B", "IDLE"): "IDLE"}

# pos_nav = nx.spring_layout(G_nav)
# pos_nav = nx.circular_layout(G_nav)
# pos_nav = nx.kamada_kawai_layout(G_nav)
# pos_nav = nx.spectral_layout(G_nav)
pos_nav = nx.planar_layout(G_nav)