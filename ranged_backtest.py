# import os
import argparse
import subprocess
# from time import time
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
    print(f"config: {config}")

    start_date_r_begin = datetime.strptime(config["start_date_r_begin"], '%Y-%m-%d')
    start_date_r_end = datetime.strptime(config["start_date_r_end"], '%Y-%m-%d')
    start_date_r_step = config["start_date_r_step"]
    end_date_r_begin = datetime.strptime(config["end_date_r_begin"], '%Y-%m-%d')
    end_date_r_end = datetime.strptime(config["end_date_r_end"], '%Y-%m-%d')
    end_date_r_step = config["end_date_r_step"]
    start_day_count = (start_date_r_end - start_date_r_begin).days + 1
    end_day_count = (end_date_r_end - end_date_r_begin).days + 1
    for sd in (start_date_r_begin + timedelta(i) for i in range(0, start_day_count, start_date_r_step)):
        for ed in (end_date_r_end - timedelta(j) for j in range(0, end_day_count, end_date_r_step)):
            start_date = sd.strftime("%Y-%m-%d")
            end_date = ed.strftime("%Y-%m-%d")
            for symbol in config["symbols"]:
                for live_config in config["live_configs"]:
                    settings = ['C:/Program Files/Python310/python.exe', 'backtest.py', "-b",
                                config["backtest_config"], "-s", symbol, "-sd", start_date, "-ed", end_date,
                                live_config]
                    print(f"Running passivbot backtest for {symbol} and {live_config} in range "
                          f"[{start_date} - {end_date}] with settings '{settings}'")
                    status = subprocess.run(settings).returncode
                    print(f"status: {status}")


if __name__ == "__main__":
    main()
