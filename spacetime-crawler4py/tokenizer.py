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


def compute_text_frequencies(text):
    """
    Description: Streamlines the computation from text to frequency dictionary

    Input: The string to convert into a frequency dictionary
    Output: The resulting dictionary
    """
    tokens = tokenize(text)
    if tokens is not None:
        freq = compute_word_frequencies(tokens)
        return len(tokens), freq
    else:
        print('Please resolve the error and try again.')
        return None


def tokenize(content):
    """
    Description: Breaks content down into tokens

    Input: The string to tokenize
    Output: A list of tokens
    """
    tokens = []
    word = ''

    # remove case sensitivity
    content = content.lower()

    for c in content:
        if 'a' <= c and c <= 'z': 
            word += c
        else:
            if len(word) > 2 and word not in STOP_WORDS:
                tokens.append(word)
            word = ''

    if len(word) > 2 and word not in STOP_WORDS:
        tokens.append(word)

    return tokens


def compute_word_frequencies(tokens):
    """
    Description: Turns list of tokens into a dictionary of counts for 
    each unique token.

    Input: A list of tokens
    Output: The dictionary of frequency counts for each unique token
    """
    freq = {}
    for token in tokens:
        if token not in STOP_WORDS:
            if token not in freq:
                freq[token] = 0
            freq[token] += 1
    return freq


def union_freq(freq1, freq2):
    """
    Description: Combines two dictionaries of frequency counts into one

    Input: Two frequency dictionaries
    Output: One dicionary containing the combined result
    """
    result = {}
    for key in freq1.keys() | freq2.keys(): 
        result[key] = freq1.get(key, 0) + freq2.get(key, 0)
    return result