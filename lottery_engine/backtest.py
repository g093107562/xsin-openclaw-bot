import pandas as pd

class LotteryBacktester:
    @staticmethod
    def run_two_year_backtest(analyzer_class, df_history, game_type="Lotto649"):
        results = []
        total_rounds = len(df_history)
        start_idx = max(30, total_rounds - 150)
        
        for i in range(start_idx, total_rounds - 1):
            train_data = df_history.iloc[:i]
            actual_next = df_history.iloc[i + 1]
            
            analyzer = analyzer_class(train_data, game_type=game_type)
            pred = analyzer.predict_numbers()
            
            main_hits = len(set(pred["zone1"]) & set(actual_next['numbers']))
            
            zone2_hit = False
            if game_type == "SuperLotto638" and pred.get("zone2") == actual_next.get("zone2"):
                zone2_hit = True

            results.append({
                "period": actual_next['period'],
                "date": actual_next['date'],
                "predicted": pred["zone1"],
                "actual": actual_next['numbers'],
                "main_hits": main_hits,
                "zone2_hit": zone2_hit
            })
            
        return pd.DataFrame(results)
