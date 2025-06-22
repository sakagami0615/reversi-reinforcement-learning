"""
Edax vs 提供されている戦略のシミュレーション
"""

import json

from reversi import Simulator
from reversi import strategies
from strategy.Edax.edax_strategy import Edax


def create_strategy(strategy_name):
    if strategy_name == 'Edax': return Edax()
    elif strategy_name == 'Unselfish': return strategies.Unselfish()
    elif strategy_name == 'Random': return strategies.Random()
    elif strategy_name == 'Greedy': return strategies.Greedy()
    elif strategy_name == 'SlowStarter': return strategies.SlowStarter()
    elif strategy_name == 'Table': return strategies.Table()
    elif strategy_name == 'MonteCarlo': return strategies.MonteCarlo1000()
    elif strategy_name == 'MinMax': return strategies.MinMax2_TPW()
    elif strategy_name == 'NegaMax': return strategies.NegaMax3_TPW()
    elif strategy_name == 'AlphaBeta': return strategies.AlphaBeta4_TPW()
    elif strategy_name == 'Joseki': return strategies.AlphaBeta4J_TPW()
    elif strategy_name == 'FullReading': return strategies.AlphaBeta4F9J_TPW()
    elif strategy_name == 'Iterative': return strategies.AbIF9J_B_TPW()
    elif strategy_name == 'Edge': return strategies.AbIF9J_B_TPWE()
    elif strategy_name == 'Switch': return strategies.SwitchNsIF10J_B_TPWE()
    else: raise ValueError(f"Invalid strategy name: {strategy_name}")


source_strategy_name = 'Edax'
target_strategy_names = [
    'Edax',
    'Unselfish',
    'Random',
    'Greedy',
    'SlowStarter',
    'Table',
    'MonteCarlo',
    'MinMax',
    'NegaMax',
    'AlphaBeta',
    'Joseki',
    'FullReading',
    'Iterative',
    'Edge',
    'Switch',
]


def generate_setting_json(source_strategy_name, target_strategy_name):
    body_dict = {
        "board_size": 8,
        "matches": 5,
        "processes": 1,
        "parallel": "player",
        "random_opening": 0,
        "player_names": [],
        "perfect_check": False
    }
    body_dict["player_names"].append(source_strategy_name)
    body_dict["player_names"].append(target_strategy_name)

    with open("./sample/simulate_basic_player_vs_edax/simulator_setting.json", "w") as f:
        json.dump(body_dict, f)


def run_simulate(source_strategy_name, target_strategy_name):
    generate_setting_json(source_strategy_name, target_strategy_name)

    simulator = Simulator(
        {
            source_strategy_name: create_strategy(source_strategy_name),
            target_strategy_name: create_strategy(target_strategy_name),
        },
        './sample/simulate_basic_player_vs_edax/simulator_setting.json',
    )
    simulator.start()
    print(simulator)


if __name__ == '__main__':
    run_simulate(source_strategy_name, target_strategy_names[2])