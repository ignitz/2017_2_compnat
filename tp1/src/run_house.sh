#!/bin/bash

python3 gp.py datasets/house-train.csv datasets/house-test.csv output/house/1.txt 50 50 0.9 0.05 2 2
python3 gp.py datasets/house-train.csv datasets/house-test.csv output/house/2.txt 50 50 0.9 0.05 2 2
python3 gp.py datasets/house-train.csv datasets/house-test.csv output/house/3.txt 50 50 0.67 0.78 5 2
python3 gp.py datasets/house-train.csv datasets/house-test.csv output/house/4.txt 100 50 0.67 0.78 5 2
python3 gp.py datasets/house-train.csv datasets/house-test.csv output/house/5.txt 100 50 0.67 0.78 5 2
python3 gp.py datasets/house-train.csv datasets/house-test.csv output/house/6.txt 100 50 0.93 0.18 5 2
python3 gp.py datasets/house-train.csv datasets/house-test.csv output/house/7.txt 500 50 0.93 0.18 5 2
python3 gp.py datasets/house-train.csv datasets/house-test.csv output/house/8.txt 500 50 0.93 0.18 5 2
python3 gp.py datasets/house-train.csv datasets/house-test.csv output/house/9.txt 500 50 0.08 0.22 5 2