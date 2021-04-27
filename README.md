# TS_proj
State Machine project

Michał Węgrzynowski, Kajetan Pietrzak, Justyna Sikorska

# Tymczasowy graf
![Graph](https://github.com/MicWeg/ProjektTS2021/blob/main/graph.png)

# Pobieranie repozytorium

Skopiuj repozytorium:
```
cd ~/catkin_ws/src
git clone https://github.com/MicWeg/ProjektTS2021.git
```

Pobrać mir_robot i uruchomić zgodnie z sekcją "Gazebo demo (multiple robots)"
```
git clone https://github.com/K-F-P/mir_robot
```

Uruchomić skrypty
```
rosrun agv new_main.py
rosrun agv state_server.py
```
Uruchomić skrypt po dojściu do stanu "Ruch do ładunku"
```
rosrun agv laithlin_move.py
```
