import sys
from partA import compute_file_frequencies

def intersection(file_path_1, file_path_2):
    """
    Runtime complexity: Linear time O(n1 + n2 + k1 + k2), where n1 and n2 are the number of characters 
    in each file and k1 and k2 are the number of tokens.
    Explanation: Both files are read character by character, and all tokens are then counted 
    for frequency and compared for intersection.
    """
    freq_1 = compute_file_frequencies(file_path_1)
    freq_2 = compute_file_frequencies(file_path_2)

    if freq_1 is None or freq_2 is None:
        return None

    unique_tokens_1 = freq_1.keys()
    unique_tokens_2 = freq_2.keys()
    intersect = unique_tokens_1 & unique_tokens_2

    return intersect


def main():
    if len(sys.argv) > 2:
        file_path_1 = sys.argv[1]
        file_path_2 = sys.argv[2]
        intersect = intersection(file_path_1, file_path_2)
        if intersect is not None:
            print(len(intersect))
        else:
            print(0)
    else:
        print('Please provide two file paths as command line arguments.')

if __name__ == '__main__':
    main()