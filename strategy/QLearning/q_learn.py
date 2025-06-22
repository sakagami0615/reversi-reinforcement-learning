from typing import Any, Union, Callable

import math
import numpy as np
from dataclasses import dataclass


@dataclass
class QLearnHyperParam:
    """QLearn hyperparameter

    epsilon (Float): ランダム行動の確率. Defaults to 0.2.
    gamma (Float): 割引率. Defaults to 0.9.
    alpha (Float): 学習率. Defaults to 0.3.
    """
    epsilon: float = 0.2
    gamma: float = 0.9
    alpha: float = 0.3

    def __str__(self):
        return f"e[{self.epsilon}]_g[{self.gamma}]_a[{self.alpha}]"


class QTable:
    def __init__(self, action_list: list[Any] = [], q_table: dict[Any] = {}, init_q_value: Callable = lambda: float(0)):
        self._q_table = q_table.copy()
        self._action_list = action_list.copy()
        self._init_q_value = init_q_value

    @property
    def q_table(self) -> dict[Any]:
        return self._q_table

    def _insert_row_decorator(func):
        """テーブルに未登録の場合は、新規追加を行うデコレータ
        """
        def wrapper(self, state: Any, *args, **kwargs):
            if state not in self._q_table:
                self._q_table[state] = {key: self._init_q_value() for key in self._action_list}
            return func(self, state, *args, **kwargs)
        return wrapper

    @_insert_row_decorator
    def get_max_q_action(self, state: Any, legal_actions: list[Any]) -> Any:
        """Qが最大となる行動を取得(行動が複数存在する場合はランダムで取得)
        """
        legal_q_values = {action: self._q_table[state][action] for action in legal_actions}
        max_q = max(legal_q_values.values())
        candidate_actions = [action for action, q in legal_q_values.items() if math.isclose(q, max_q)]
        return np.random.choice(candidate_actions)

    @_insert_row_decorator
    def get_q_value(self, state: Any, action: Any) -> float:
        """状態/行動に対応したQ値を取得
        """
        return self._q_table[state][action]

    @_insert_row_decorator
    def get_max_q_value(self, state: Any) -> float:
        """状態に対応したQ値の中から最大値を取得
        """
        return max(self._q_table[state].values())

    @_insert_row_decorator
    def update(self, state: Any, action: Any, q_value: float) -> None:
        """状態/行動に対応したQ値を更新
        """
        self._q_table[state][action] = q_value


class QLearnCore:
    def __init__(self, action_list: list[Any], q_table: dict[Any] = {},
                 is_learn: bool = True, param: QLearnHyperParam = QLearnHyperParam(),
                 init_q_value: Callable = lambda: float(0)):
        """Initialize QLearnCore

        Args:
            action_list (list[str]): とりえる行動のリスト.
            q_table (dict[Any], optional): Qテーブル初期値. Defaults to {}.
            is_learn (bool, optional): 学習[True] or 推論[False]. Defaults to True.
            param (QLearnHyperParam, optional): ハイパーパラメータ. Defaults to QLearnHyperParam().
            init_q_value (_type_, optional): Q値の初期化関数. Defaults to lambda:float(0).
        """
        self._is_learn = is_learn
        self._param = param
        self._q_table = QTable(action_list, q_table, init_q_value)

    @property
    def q_table(self) -> dict[Any]:
        return self._q_table.q_table

    def policy(self, state: Any, actions: list[Any], episode: Union[int, None]) -> Any:
        if not self._is_learn:
            # Q値が最大となるアクション(駒配置場所)を取得
            return self._q_table.get_max_q_action(state, actions)

        epsilon = self._param.epsilon if episode is None else self._param.epsilon * (1 / (episode + 1))
        if epsilon <= np.random.uniform(0, 1):
            # Q値が最大となるアクション(駒配置場所)を取得
            return self._q_table.get_max_q_action(state, actions)
        else:
            # 一定の確率でランダムを採用
            return np.random.choice(actions)

    def update_q_table(self, state: Any, action: Any, next_state: Any, reward: int) -> None:
        q = self._q_table.get_q_value(state, action)
        max_q_prime = self._q_table.get_max_q_value(next_state)
        update_q = q + self._param.alpha * (reward + self._param.gamma * max_q_prime - q)
        self._q_table.update(state, action, update_q)
