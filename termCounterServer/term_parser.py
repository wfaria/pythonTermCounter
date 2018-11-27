import os
import unicodedata

DEFAULT_FILE_PATH = "./initialLoadFiles"
    
def count_from_default_files():
    """
    Count the number of times that each term appear
    in the files placed on the folder DEFAULT_FILE_PATH.
    """
    termCount = {}
    for f in os.listdir(DEFAULT_FILE_PATH):
        textPath = "{0}/{1}".format(DEFAULT_FILE_PATH, f)
            
        # We read the file as a binary file and try to convert each line using
        # utf-8 to preserve special characters, fallbacking to latin-1
        # on failure cases, there some characters may be lost.
        textFile = open(textPath, "rb")            
        for line in textFile:
            try:
                line = line.decode('utf-8')                
            except Exception as e:
                try:
                    line = line.decode('latin-1')
                except Exception as e:
                    raise Exception("Error while processing file '{0}', line '{1}', error '{2}'.".format(textPath, line, e))
                
            count_terms(line, termCount)
            
    return termCount

def count_terms(text, termCount = {}):
    """
    Splits the text parameter into term tokens and count the
    number of times that each one appears there.
    
    The counting result is placed into the termCount parameter dictionary,
    so you can call this method multiple times to count terms from
    different sources.
    """        
    if (not text):
        # Empty string.
        return termCount
    
    words = sanitize_text(text).split(" ")   
    for w in words:
        if (not w):
            # Sequence of spaces found as word, ignore it.
            continue
    
        if (w in termCount):
            termCount[w] = termCount[w] + 1
        else:
            termCount[w] = 1
            
    return termCount
    
def sanitize_text(text):
    """
    Cleans a string object, removing undesired characters,
    trimming spaces and converting to lower-case and ascii compatible.
    """
    if (type(text) != str and type(text) != unicode):
        raise TypeError("Parameter with wrong type, expected string or unicode, got {0}".format(type(text)))
    
    whitespaceStrings = ["\n", "\r", "\t", ",", ";", "."]
    for s in whitespaceStrings:
        text = text.replace(s, " ")
        
    # Normalizing unicode characters and transforming each one into an ascii equivalent.
    if (type(text) == unicode):
        text = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    
    return text.strip().lower();
    
if __name__ == "__main__":
    print(count_from_default_files())
