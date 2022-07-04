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
    num_iters += math.ceil(end_day_range_count / end_date_range_step if end_date_range_step > 0 else 0)
    num_iters *= math.ceil(len(config["symbols"]) * len(config["live_configs"]))
    i, j, day_counter, iter_counter = 0, 0, 0, 0
    while (i <= start_day_range_count and start_date_range_step > 0) or \
            (j <= end_day_range_count and end_date_range_step > 0):
        sd = start_date_range_begin + timedelta(i)
        ed = end_date_range_end - timedelta(j)
        start_date = sd.strftime("%Y-%m-%d")
        end_date = ed.strftime("%Y-%m-%d")
        for symbol in config["symbols"]:
            for live_config in config["live_configs"]:
                settings = ['C:/Program Files/Python310/python.exe', 'backtest.py', "-b",
                            config["backtest_config"], "-s", symbol, "-sd", start_date, "-ed", end_date, live_config]
                iter_counter += 1
                print(f"\n\n{iter_counter} / {num_iters}. Running passivbot backtest for {symbol} and {live_config} "
                      f"in range [{start_date} - {end_date}] with settings:\n'{settings}'\n")

                status = subprocess.run(settings).returncode
                print(f"Status: {status}")
        if (day_counter % 2 == 0 and end_date_range_step > 0) or start_date_range_step <= 0:
            j += end_date_range_step
        else:
            i += start_date_range_step
        day_counter += 1


if __name__ == "__main__":
    main()
