# ArgueAI

To use agent clone this repository and run the `train.py` file

Give reward `10.0` if correct output given and `-10.0` if wrong.

To train agent using a dataset replace the `dataset_final.csv` file with the appropriate dataset file and modify it in the `dataset.py` file and uncomment the import in `train.py` file

To train using RLHF simulated using chatgpt api make uncomment the required lines in `env_final.py` file and uncomment the import in `train.py` file