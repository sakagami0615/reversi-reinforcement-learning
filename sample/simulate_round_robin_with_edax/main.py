"""
提供されている戦略の総当たりシミュレーション
"""

from reversi import Simulator
from reversi import strategies
from strategy.Edax.edax_strategy import Edax


if __name__ == '__main__':

    setting_file = './sample/simulate_round_robin_with_edax/simulator_setting.json'

    simulator = Simulator(
        {
            'Edax': Edax(setting_file),
            'Unselfish': strategies.Unselfish(),
            'Random': strategies.Random(),
            'Greedy': strategies.Greedy(),
            'SlowStarter': strategies.SlowStarter(),
            'Table': strategies.Table(),
            'MonteCarlo': strategies.MonteCarlo1000(),
            'MinMax': strategies.MinMax2_TPW(),
            'NegaMax': strategies.NegaMax3_TPW(),
            'AlphaBeta': strategies.AlphaBeta4_TPW(),
            'Joseki': strategies.AlphaBeta4J_TPW(),
            'FullReading': strategies.AlphaBeta4F9J_TPW(),
            'Iterative': strategies.AbIF9J_B_TPW(),
            'Edge': strategies.AbIF9J_B_TPWE(),
            'Switch': strategies.SwitchNsIF10J_B_TPWE(),
        },
        setting_file,
    )
    simulator.start()

    print(simulator)