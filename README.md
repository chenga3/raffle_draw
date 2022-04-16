# What is this?

This repo includes a script to randomly draw a first and second place prize winner from a CSV file of quiz responses.

# How do I use this?

`python3 prize_draw.py [responses_file] [seed]`

Where `responses_file` if a CSV file containing quiz responses, and `seed` is the seed to be used for Python's `random` library.

Try out `python3 prize_draw.py hacking_scene_quiz_responses.csv 0` as an example.
