STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 
    'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 
    'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 
    'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 
    'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 
    'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', 
    "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', 
    "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 
    'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 
    'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 
    'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', 
    "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 
    'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 
    'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 
    'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 
    "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', 
    "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', 
    "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', 
    "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'
}


def tokenize(content):
    """
    Runtime complexity: Linear time O(n), where n = number of characters in the file.
    Explanation: Each character is read exactly once and processed. Memory usage is balanced using chunks.
    """
    tokens = []
    word = ''

    for c in content:
        if 'a' <= c and c <= 'z' or '0' <= c and c <= '9':
            word += c
        else:
            if word != '':
                tokens.append(word)
                word = ''
    if len(word) > 0:
        if (word not in STOP_WORDS):
            tokens.append(word)

    return tokens


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


def compute_text_frequencies(text):
    tokens = tokenize(text)
    if tokens is not None:
        freq = compute_word_frequencies(tokens)
        return freq
    else:
        print('Please resolve the error and try again.')
        return None


def intersection(content1, content2):
    """
    Runtime complexity: Linear time O(n1 + n2 + k1 + k2), where n1 and n2 are the number of characters 
    in each file and k1 and k2 are the number of tokens.
    Explanation: Both files are read character by character, and all tokens are then counted 
    for frequency and compared for intersection.
    """
    freq_1 = compute_text_frequencies(content1)
    freq_2 = compute_text_frequencies(content2)

    if freq_1 is None or freq_2 is None:
        return None

    unique_tokens_1 = freq_1.keys()
    unique_tokens_2 = freq_2.keys()
    intersect = unique_tokens_1 & unique_tokens_2

    return intersect