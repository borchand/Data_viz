import fastf1
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting as f1_plt
import pandas as pd
from datetime import timedelta, datetime

TRACK_DISTANCE = 4.309

def IsTurn(x,y,x_last_turn,y_last_turn, turn_difference=1300):
    if x + turn_difference < x_last_turn:
        return True        
    elif x - turn_difference > x_last_turn:
        return True        
    elif y + turn_difference < y_last_turn:
        return True        
    elif y - turn_difference > y_last_turn:
        return True        
    else:
        return False


def find_minisectors(lap_tel, turn_difference=1300):
    x_last_turn, y_last_turn = 0,0
    turn_count = 0
    turn_idx = []
    for idx, xy in enumerate(zip(lap_tel["X"], lap_tel["Y"]), start=2):
        x, y = xy
        if IsTurn(x, y, x_last_turn, y_last_turn, turn_difference):
            x_last_turn = x
            y_last_turn = y
            turn_count += 1
            turn_idx.append(idx)
    return turn_idx, turn_count

def find_minisectors_times(lap_tel, turn_difference=800):
    mini_sector_times = []
    ## find idx of mini sectors
    idx, _ = find_minisectors(lap_tel, turn_difference)
    
    time = lap_tel["Time"]
    last_time = time[idx[0]]
    for i in idx[1:]:
        current_time = time[i]
        mini_sector_time = current_time - last_time
        mini_sector_times.append(mini_sector_time)
        last_time = time[i]
    return mini_sector_times

def find_minisectors_for_two(lap_tel_1, lap_tel_2, turn_difference=800):
    mini_sector_times_1 = []
    mini_sector_times_2 = []
    
    idx, _ = find_minisectors(lap_tel_1, turn_difference)
    
    time_1 = lap_tel_1["Time"]
    time_2 = lap_tel_2["Time"]
    prev_time_1 = time_1[idx[0]]
    prev_time_2 = time_2[idx[0]]

    for i in idx[1:]:
        current_time_1 = time_1[i]
        current_time_2 = time_1[i]

        mini_sector_time_1 = current_time_1 - prev_time_1
        mini_sector_time_2 = current_time_2 - prev_time_2

        mini_sector_times_1.append(mini_sector_time_1)
        mini_sector_times_2.append(mini_sector_time_2)
        
        prev_time_1 = time_1[i]
        prev_time_2 = time_2[i]
    return mini_sector_times_1, mini_sector_times_2, idx

def compare_minisectors(lap_tel_1, lap_tel_2, turn_difference=800):
    
    first_fastest = []

    mini_sectors_1, mini_sectors_2, idx = find_minisectors_for_two(lap_tel_1, lap_tel_2, turn_difference)

    for i in range(len(mini_sectors_1)):
        first_fastest.append(mini_sectors_1[i] < mini_sectors_2[i])
    
    return idx, first_fastest

def convert_string_to_time(string):
    string = string.split(" ")[-1]
    return datetime.strptime(string, '%H:%M:%S.%f')

def convert_delta_to_time(delta):
    datetime_0 = datetime(1900,1,1,0,0,0)

    return (datetime_0 + delta)