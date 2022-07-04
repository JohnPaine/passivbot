import argparse
import math
import pprint
import subprocess
from datetime import timedelta, datetime
from procedures import load_hjson_config


def main():
    parser = argparse.ArgumentParser(prog="RangedBacktest", description="Backtest given passivbot configs in a range.")
    parser.add_argument(
        "-rb",
        "--ranged_backtest_config",
        type=str,
        required=False,
        dest="config_path",
        default="configs/backtest/ranged_backtest.hjson",
        help="ranged backtest config hjson file",
    )
    args = parser.parse_args()

    config = load_hjson_config(args.config_path)
    print(f"Config: {pprint.pprint(config)}")

    start_date_range_begin = datetime.strptime(config["start_date_range_begin"], '%Y-%m-%d')
    start_date_range_end = datetime.strptime(config["start_date_range_end"], '%Y-%m-%d')
    start_date_range_step = config["start_date_range_step"]
    end_date_range_begin = datetime.strptime(config["end_date_range_begin"], '%Y-%m-%d')
    end_date_range_end = datetime.strptime(config["end_date_range_end"], '%Y-%m-%d')
    end_date_range_step = config["end_date_range_step"]
    start_day_range_count = (start_date_range_end - start_date_range_begin).days + 1
    end_day_range_count = (end_date_range_end - end_date_range_begin).days + 1

    num_iters = math.ceil(start_day_range_count / start_date_range_step if start_date_range_step > 0 else 0)
    num_iters *= math.ceil(end_day_range_count / end_date_range_step if end_date_range_step > 0 else 0)
    num_iters *= math.ceil(len(config["symbols"]) * len(config["live_configs"]))
    i, j, iter_counter = 0, 0, 0
    for sd in (start_date_range_begin + timedelta(i) for i in range(0, start_day_range_count, start_date_range_step)):
        for ed in (end_date_range_end - timedelta(j) for j in range(0, end_day_range_count, end_date_range_step)):
            start_date = sd.strftime("%Y-%m-%d")
            end_date = ed.strftime("%Y-%m-%d")
            for symbol in config["symbols"]:
                for live_config in config["live_configs"]:
                    settings = ['C:/Program Files/Python310/python.exe', 'backtest.py', "-b",
                                config["backtest_config"], "-s", symbol, "-sd", start_date, "-ed", end_date, live_config]
                    iter_counter += 1
                    print(f"\n\n{datetime.today()}\t\t{iter_counter} / {num_iters}. Running passivbot backtest for "
                          f"{symbol} and {live_config} in range [{start_date} - {end_date}] with settings:\n'{settings}'\n")

                    status = subprocess.run(settings).returncode
                    print(f"Status: {status}")


if __name__ == "__main__":
    main()
