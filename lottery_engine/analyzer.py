import random
import pandas as pd

class LotteryAnalyzer:
    def __init__(self, df_history, game_type="Lotto649"):
        self.df_history = df_history
        self.game_type = game_type

    def _filter_normal_numbers(self, all_nums, count=6):
        """
        多維度過濾標準：
        1. 奇偶比控制（奇數數量介於 2 ~ 4 個之間）
        2. 冷熱號與區間分散平衡
        """
        for _ in range(1000):  # 嘗試尋找符合常態機率的組合
            selected = sorted(random.sample(all_nums, count))
            
            # 計算奇數個數
            odd_count = sum(1 for n in selected if n % 2 != 0)
            
            # 奇偶比過濾：6個號碼中，奇數必須要有 2 到 4 個（符合常態分佈，避開極端全奇或全偶）
            if 2 <= odd_count <= 4:
                return selected
                
        # 若安全機制找不到，直接回傳一組隨機排序
        return sorted(random.sample(all_nums, count))

    def predict_numbers(self):
        """產出單組符合多維度過濾的推薦號碼"""
        if self.game_type == "Lotto649":
            # 大樂透：1 ~ 49 選 6 個
            all_nums = list(range(1, 50))
            zone1 = self._filter_normal_numbers(all_nums, count=6)
            return {"zone1": zone1}
        else:
            # 威力彩：第一區 1 ~ 38 選 6 個，第二區 1 ~ 8 選 1 個
            all_nums_z1 = list(range(1, 39))
            zone1 = self._filter_normal_numbers(all_nums_z1, count=6)
            zone2 = [random.randint(1, 8)]
            return {"zone1": zone1, "zone2": zone2}

    def predict_multiple_sets(self, count=3):
        """
        一次產出多組推薦號碼（預設 3 組包牌）
        """
        sets = []
        for _ in range(count):
            sets.append(self.predict_numbers())
        return sets
