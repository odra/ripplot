# Ripplot

Plots data from ripple blockchain

## Requirements:

* python >= 3.7
* some unix based system

## Running

Install dependencies:

```
pip install -U -r requirements.txt
```

Run the cli:

```
./ripplot.py
```

You check all available options by running:

```
./ripplot.py -h
```

## Plot

Generate a gnuplot file:s

```
./ripplot.py plot > ripple.dat
```

Open gnuplot by running `gnuplot` and run the following commands:

```
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S.%f"
set format x "%H:%M:%S"
plot "ripple.dat" using 1:3
```