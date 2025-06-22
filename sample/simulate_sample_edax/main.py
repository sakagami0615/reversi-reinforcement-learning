"""
Edaxのシミュレーション
"""

from reversi import Simulator
from reversi import strategies
from strategy.Edax.edax_strategy import Edax


if __name__ == '__main__':
    simulator = Simulator(
        {
            'Edax': Edax(),
            'Greedy': strategies.Greedy(),
        },
        './sample/simulate_sample_edax/simulator_setting.json',
    )
    simulator.start()

    print(simulator)