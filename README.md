# TS_proj
State Machine project

Michał Węgrzynowski, Kajetan Pietrzak, Justyna Sikorska

# Tymczasowy graf
![Graph](https://github.com/MicWeg/ProjektTS2021/blob/main/graph.png)

# Pobieranie repozytorium
!Uwaga - występuje stosunkowo duże obciążenie i programy reagują z opóźnieniem

Skopiuj repozytorium:
```
cd ~/catkin_ws/src
git clone https://github.com/MicWeg/ProjektTS2021.git
```

Pobrać mir_robot i uruchomić zgodnie z sekcją "Gazebo demo (multiple robots)"
```
git clone https://github.com/K-F-P/mir_robot
```

Uruchomić skrypty (proszę zignorować początkowe errory dla skryptu laithlin_move.py)
```
rosrun agv state_server.py
rosrun agv laithlin_move.py
rosrun agv new_main.py

```
