"""
提供されている戦略から数個抜粋した総当たりシミュレーション
"""

from reversi import Simulator
from reversi import strategies


if __name__ == '__main__':
    simulator = Simulator(
        {
            'Random': strategies.Random(),
            'Greedy': strategies.Greedy(),
            'MinMax': strategies.MinMax2_TPW(),
        },
        './sample/simulate_basic_player_slim/simulator_setting.json',
    )
    simulator.start()

    print(simulator)