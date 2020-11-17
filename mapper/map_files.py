import pandas as pd


def join_csvs():
	key_pairs = pd.read_csv("key_pairs.csv", delimiter=",", index_col = 1)
	data_key_pairs = pd.read_csv("data_key_pair.csv", delimiter=",", index_col = 0)
	joined_data = data_key_pairs.join(key_pairs)

	joined_data.to_csv('joined_data.csv')

if __name__ == "__main__":
	join_csvs()
