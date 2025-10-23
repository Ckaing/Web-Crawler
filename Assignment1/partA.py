import sys


def tokenize(file_path, chunk_size = 1000000):
    """
    Runtime complexity: Linear time O(n), where n = number of characters in the file.
    Explanation: Each character is read exactly once and processed. Memory usage is balanced using chunks.
    """
    try:
        with open(file_path, 'r', errors='ignore') as f:
            chunk = f.read(chunk_size).lower()
            tokens = []
            word = ''
            while chunk:
                for c in chunk:
                    if 'a' <= c and c <= 'z' or '0' <= c and c <=  '9':
                        word += c
                    else:
                        if word != '':
                            tokens.append(word)
                            word = ''
                chunk = f.read(chunk_size).lower()
            if len(word) > 0:
                tokens.append(word)
            return tokens
    except FileNotFoundError:
        print(f"Error: Cannot find '{file_path}'. Please double check your file path.")

    return None


def compute_word_frequencies(tokens):
    """
    Runtime complexity: Linear time O(m), where m = number of tokens.
    Explanation: Iterates through all tokens once. Dictionary lookup and insertion are O(1) on average.
    """
    freq = {}
    for token in tokens:
        if token not in freq:
            freq[token] = 0
        freq[token] += 1
    return freq


def print_word_frequencies(freq):
    """
    Runtime complexity: Polynomial time O(k log k), where k = number of unique tokens.
    Explanation: Sorting dominates the runtime O(k log k). Printing all items is O(k).
    """
    if freq is None:
        return
    sorted_freq = sorted(freq.items(), key=lambda f: f[1], reverse=True)
    for word, cnt in sorted_freq:
        print(word, '=', cnt)


def compute_file_frequencies(file_path):
    """
    Runtime complexity: O(m + k log k), where m = number of tokens and k = number of unqiue tokens
    Explanation: tokenize = O(m), compute_word_frequencies = O(k log k)
    """
    tokens = tokenize(file_path)
    if tokens is not None:
        freq = compute_word_frequencies(tokens)
        return freq
    else:
        print('Please resolve the error and try again.')
        return None


def main():
    if len(sys.argv) > 1:
        if len(sys.argv) > 2: 
            print('Multiple file paths detected. Using the first file provided.')
        file_path = sys.argv[1]
        freq = compute_file_frequencies(file_path)
        print_word_frequencies(freq)
    else:
        print('Please provide the file path as a command line argument.')

if __name__ == '__main__':
    main()