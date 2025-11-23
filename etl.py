# etl.py
from etl.parse_and_clean import main

if __name__ == "__main__":
    INPUT = "./data/Sample Data 2.xlsx"
    OUTPUT = "./outputs/processed_trade_sample.csv"
    main(INPUT, OUTPUT)
