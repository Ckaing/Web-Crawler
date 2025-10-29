import sys
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

class Text_Processing:
    def __init__(self):
        pass

    # Fills the list_of_words with words from the txt file given
    # runtime is O(n * m) for n lines and m words
    def tokenize(self, path) -> list[str]:
        list_of_words = []
        try:
            with open(path, "r", encoding = "utf-8", errors="ignore") as file:
                for line in file:
                    sentence = line.strip().split()
                    list_of_words.extend(sentence)
        except FileNotFoundError:
            print("ERROR! Please enter a valid file!")
        except Exception as e:
            print(f"ERROR! {e}")
            sys.exit(1)
        return list_of_words

    # Fills the dictionary with number of occurences of each word from list_of_words, {"Word": number of occurences}
    # Runtime is O(n * m) where n is number of tokens and m is average token length
    # Dictionary operations are O(1) average, character iteration is O(m)
    def computeWordFrequencies(self, list_of_words) -> dict:
        dict_of_tokens = {}
        for word in list_of_words:
            # Checks if word is alphanumeric and add the lowercased version to dict
            if (word.isalnum() and word.isascii()):
                general_word = word.lower()
                # Checks if word is in stop words
                if general_word not in STOP_WORDS:
                    if general_word in dict_of_tokens:
                        dict_of_tokens[general_word] += 1
                    else:
                        dict_of_tokens[general_word] = 1
            # If the word is not alphanumeric, it makes it alphanumeric by removing any non-alphanum characters
            # replacing it with a space, splitting it again to add back to the dict
            else:
                chars = []
                # Checks if each char is alphanum
                for i in word:
                    # Appends letter if is alphanum
                    if (i.isalnum() and i.isascii()):
                        chars.append(i)
                    # Appends space if not alphanum
                    else:
                        chars.append(" ")
                        
                newWord = "".join(chars)
                if newWord != "":
                    # Makes the string all lowercase
                    general_word = newWord.lower()
                    # Splits by spaces to create new list without non-alphanums
                    newList = general_word.split()
                    for word in newList:
                        # Checks if word is in stop words
                        if word not in STOP_WORDS:
                            if word in dict_of_tokens:
                                dict_of_tokens[word]+=1
                            else:
                                dict_of_tokens[word] = 1 
        return dict_of_tokens
                            

    # Creates a list of tuples form dict_of_tokens, printing each pair of tuples
    # Runtime is O(nlog(n)) for n items in dict due to sorting
    def print(self, dict_of_tokens) -> None:
        sorted_items = sorted(dict_of_tokens.items(), key=lambda item: item[1], reverse=True)
        for i in sorted_items:
            print(f"{i[0]} - {i[1]}")
            