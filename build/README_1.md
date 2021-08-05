
```

  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file; if not specified, stdout is used
  -w, --print_own       Print just current owners; useful for an overview
  -l, --print_log       Print total pain and temperature instead of progress
                        bars
  -a, --auto_complete   Allows not full completed data files; people are auto-
                        completed with 10 optimal_weight and 10 sensevity;
                        things have 1 kg mass and don't belong to anybody.
  -d, --disable_progress_info
                        No progress info
  -e EPOCH_NUMBER, --epoch_number EPOCH_NUMBER
                        Default number of general attempts; default is 3
  -i ITERATION_NUMBER, --iteration_number ITERATION_NUMBER
                        Default number of iteration in each attempt; if not
                        specified, equals to 300_000
  -g GRADIENT, --gradient GRADIENT
                        Number of iterations it takes to decrease temperature
                        in 10 times; default is 100_000
  -t START_TEMPERATURE, --start_temperature START_TEMPERATURE
                        Start temperature; default is 50 (pains)
  -p PAIN_MULTIPLY, --pain_multiply PAIN_MULTIPLY
                        Default pain (at optimal weight); default is 15
  -u UPDATE_FREQ, --update_freq UPDATE_FREQ
                        Number of iterations between updating bar/log; default
                        is 1_000

```
