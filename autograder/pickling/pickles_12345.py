import sys
import pickle
from nltk.corpus import conll2000
from type_counter import TagTypes


def make_and_pickle(corpus, pickle_path, tagset=None):
    model = TagTypes(corpus, tagset=tagset)
    with open(pickle_path, "wb") as f:
        pickle.dump(model, f)


def unpickle(pickle_path):
    with open(pickle_path, "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":

    if len(sys.argv) > 2:
        pickle_file = sys.argv[2]
        if sys.argv[1] == "--unpickle":
            try:
                model = unpickle(pickle_file)
                print(model)
            except FileNotFoundError:
                print(f"No pickle found at {pickle_file}")
        elif sys.argv[1] == "--pickle":
            make_and_pickle(conll2000, pickle_file, tagset="universal")

        else:
            print("huh?")



