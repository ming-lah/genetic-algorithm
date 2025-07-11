import csv
import time
from run_ga import run_ga_on_cities
from utils import load_tsp_file, plot_convergence, plot_tsp_path

if __name__ == '__main__':
    cities = load_tsp_file("data/qa194.tsp")
    num_runs = 1
    results = []

    
    config = {
        'pop_size': 300,
        'generations': 2000,
        'crossover_rate': 0.9,
        'mutation_rate': 0.02,
        'elitism_count': 3,
        'use_two_opt': True,
        'gen_two_opt': 500,
        'two_opt_strategy': 'normal',
        'init_strategy': 'mixed',
        'selection_strategy': 'tournament',
        'crossover_strategy': 'miexd',
        'early_stop': 1000
    }

    start_time =  time.time()

    csv_filename = f"result/results_{len(cities)}cities_{num_runs}runs_testforcodetime.csv"

    with open(csv_filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow(["Parameter Settings"])
        for key, value in config.items():
            writer.writerow([key, value])
        
        writer.writerow([])

        writer.writerow(["Run", "Best_Distance", "Best_Path"])

        for i in range(num_runs):
            best_path, best_dist, best_curve, avg_curve = run_ga_on_cities(cities, **config)
            results.append((best_dist, best_path))
            writer.writerow([i + 1, best_dist, best_path])
            print(f"[Run {i+1}] Distance: {best_dist:.2f}")

            city_count = len(cities)
            path_img = f"image/path_{city_count}cities_run{i+1}_3.png"
            curve_img = f"image/convergence_{city_count}cities_run{i+1}_3.png"

            plot_tsp_path(cities, best_path, title=f"Best Path (Run {i+1})", save_path=path_img)
            plot_convergence(best_curve, avg_curve, save_path=curve_img)

        results.sort(key=lambda x: x[0])
        best_overall = results[0]
        worst_overall = results[-1]
        avg_distance = sum(r[0] for r in results) / len(results)

        writer.writerow([])
        writer.writerow(["Summary"])
        writer.writerow(["Best_Distance", best_overall[0]])
        writer.writerow(["Worst_Distance", worst_overall[0]])
        writer.writerow(["Average_Distance", avg_distance])
        writer.writerow(["Best_Path", best_overall[1]])

    end_time  = time.time()
    total = end_time - start_time

    print("结果已保存至：", csv_filename)
    print(f"Best : {best_overall[0]:.2f}")
    print(f"Worst: {worst_overall[0]:.2f}")
    print(f"Avg  : {avg_distance:.2f}")
    print(f"运行的时间: {total}")
