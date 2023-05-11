


import doctest
from random import *


#Returns a dictionary of k-grams
def get_grams(text, k):
    '''
    (string, int) -> dict
    
    This function returns a dictionary of k-grams (as described in the assignment), using the given text and integer k.
    
    >>> get_grams('gagggagaggcgagaaa', 2)
    {'ga': {'g': 4, 'a': 1}, 'ag': {'g': 2, 'a': 2}, 'gg': {'g': 1, 'a': 1, 'c': 1}, 'gc': {'g': 1}, 'cg': {'a': 1}, 'aa': {'a': 1}}
    
    >>> get_grams('hellohello', 1)
    {'h': {'e': 2}, 'e': {'l': 2}, 'l': {'l': 2, 'o': 2}, 'o': {'h': 1}}
    
    >>> get_grams("eeeieeeieeeo", 3)
    {'eee': {'i': 2, 'o': 1}, 'eei': {'e': 2}, 'eie': {'e': 2}, 'iee': {'e': 2}}
    
    '''
    #Creates an empty dictionary to house the k-grams
    grams_dict = {}
    
    #Loops through the length of the string text, stopping before the last k characters of the text 
    for i in range (len(text)-k):
        
        #Sections the text to the given gram
        gram = text[i:i+k]
        #Finds the next letter
        next_letter = text[i+k]
        
        #If the gram is already in the dictionary
        if gram in grams_dict:
            g = grams_dict[gram]
            
            #If the next letter is already in the sub-dictionary, then the value for the next letter key is increased by 1 
            if next_letter in g:
                g[next_letter] += 1
                
            #Otherwise, the next letter key is added to the sub-dictionary, and the value is set equal to 1
            else:
                g[next_letter] = 1
                
        #Otherwise, the gram is added to the dictionary as a key, and a new sub-dictionary is created 
        else:
            grams_dict[gram] = {next_letter : 1}
         
    return grams_dict


#Takes two k-gram dictionaries and combines them
def combine_grams(grams1, grams2):
    '''
    (dict, dict) -> dict
    
    This function takes in two dictionaries and combines them into a single dicitonary without modifying the initial dictionaries.
    
    >>> combine_grams({'a': {'b': 3, 'c': 9}, 'b': {'a': 10}}, {'b': {'a': 5, 'c': 5}, 'c': {'d': 4}})
    {'a': {'b': 3, 'c': 9}, 'b': {'a': 15, 'c': 5}, 'c': {'d': 4}}
    
    >>> combine_grams({'g': {'b': 3, 'c': 9}}, {'h': {'d': 5}})
    {'g': {'b': 3, 'c': 9}, 'h': {'d': 5}}
    
    >>> x = get_grams('ella', 1)
    >>> y = get_grams('hello', 1)
    >>> combine_grams(x,y)
    {'e': {'l': 2}, 'l': {'l': 2, 'a': 1, 'o': 1}, 'h': {'e': 1}}
    
    '''
    
    #Creates an empty dictionary
    combined_dict = {}
    
    #Copys the dictionary grams 1 into the new combined dictionary by looping through each key and subkey -- deep copy of grams1 
    for key in grams1:
        gk = grams1[key]
        sub_c_dict = {}
        for kk in gk:
            sub_c_dict[kk] = gk[kk]
        combined_dict[key] = sub_c_dict
        
    #Loops through each key in the grams2 dictionary
    for k in grams2:
        #If the key is already in the combined dictionary
        if k in combined_dict:
            #The subdictionary that is the value at that key in the combined dictionary
            sub_dict = combined_dict[k]
            #The subdictionary that is the value at that key in grams2
            sub_dictg2 = grams2[k]
            #Loops through each subkey in the subdictionary in grams2
            for subk in sub_dictg2:
                #If the subkey is already in the subdictionary, the values at the key are added together
                if subk in sub_dict:
                    val = sub_dict[subk] + sub_dictg2[subk]
                    sub_dict[subk] = val
                #Otherwise, a new subkey is made and assigned
                else:
                    sub_dict[subk] = sub_dictg2[subk]
        #If the key is not already in the combined dictionary, it is added
        else:
            combined_dict[k] = grams2[k]
            
    return combined_dict


#Creates a k-grams dictionary for each file in filenames and returns a dictionary of all the dictionaries combined
def get_grams_from_files(filenames, k):
    '''
    (list, int) -> dict
    
    This function takes a list of filenames as strings and an integer k. It reads in the files at the given filenames, and creates a k-grams dictionary for each file, which are all
    combined to make a final dictionary. This final dictionary is what is returned.
    
    >>> grams = get_grams_from_files(['raven.txt'], 4)
    >>> len(grams)
    3023
    
    >>> grams['nce ']
    {'u': 1, 'a': 2, 'w': 1, 'm': 1, 'i': 1}
    
    >>> grams['ary,']
    {' ': 1, '\\n': 1}
    
    '''
    
    #Creates an empty dictionary that will house all the files' dictionaries combined
    final_dict = {}
    
    #Loops through each file in the list filenames
    for file in filenames:
        #Opens and reads the given file
        f = open(file, "r")
        file_text = f.read()
        #Gets the grams from the file to create a dictionary of grams specific to said file
        file_dict = get_grams(file_text, k)
        #Combines the grams from that file with the grams from all the files already processed
        final_dict = combine_grams(final_dict, file_dict)
        f.close
        
    return final_dict


#Predicts the next character in a string
def generate_next_char(grams, cur_gram):
    '''
    (dict, string) -> string
    
    This function predicts the next character in a string by using probabilities that detail how frequently other characters have followed that string in the past.
    
    >>> seed(9001)
    >>> generate_next_char({'a': {'f': 3, 'd': 9}, 'c': {'d': 4}}, 'a')
    'f'
    >>> generate_next_char({'a': {'f': 3, 'd': 9}, 'c': {'d': 4}}, 'a')
    'd'
    
    >>> seed(1337)
    >>> grams = get_grams_from_files(['raven.txt'], 4)
    >>> generate_next_char(grams, 'drea')
    'm'
    
    >>> grams = get_grams_from_files(['raven.txt'], 4)
    >>> generate_next_char(grams, 'dre')
    Traceback (most recent call last):
    AssertionError: The string cur_gram is not present in the grams dictionary
    
    '''
    
    #If the current gram is not in the k-gram dictionary, an exception is raised
    if cur_gram not in grams:
        raise AssertionError("The string cur_gram is not present in the grams dictionary")
    
    #Finds the length of the k-grams in the dictionary grams
    for k in grams:
        gram_length = len(k)
        break
    
    #If the length of the current gram is not equal to the length of the k-grams in the dictionary grams, and exception is raised
    if len(cur_gram) != gram_length:
        raise AssertionError("The length of the string cur_gram is not the same as the length of the k-grams in the dictionary grams.")
    
    #Acesses the subdictionary that the key cur_grams represents
    dict_curgrams = grams[cur_gram]
    
    #Creates an empty list to store the subdictionary's keys
    keys_list = []
    #Creates an empty list to store the subdictionary's values
    values_list = []
    
    #Adds the keys and values in the subdictionary to their respecitive list
    for g in dict_curgrams:
        key = g
        keys_list.append(key)
        val = dict_curgrams[g]
        values_list.append(val)
        
    #Chooses the character to return
    predicted_char = choices(keys_list, values_list)
    
    return predicted_char[0] 


#Generates text based on a given dictionary of k-grams
def generate_text(grams, start_gram, k, n):
    '''
    (dictionary, string, int, int) -> string
    
    This function generates a piece of text of length n with a given dictionary of k-grams. 
    
    >>> seed(1330)
    >>> grams = get_grams_from_files(['raven.txt'], 5)
    >>> generate_text(grams, "Once upon", 5, 200)
    Once upon the tempest tossed this desert land enchanted—tell me—tell me, I implore—
           Quoth the Raven, thou,” I cried, “thy God we both adore—
    Tell the floor.
    “’Tis soul with my head at ease 
   
    
    >>> seed(1400)
    >>> grams = get_grams_from_files(['beowulf.txt'], 8)
    >>> generate_text(grams, "Over sea ", 8, 100)
    Over sea, a day's-length elapsed ere
           "Ask not of joyance,
           Jewels and wires: a warden
           
    >>> seed(1560)
    >>> grams = get_grams_from_files(['holmes.txt'], 9)
    >>> generate_text(grams, "Sherlock Holmes", 9, 150)
    Sherlock Holmes. "I think not, that the carriage shall get
    our solution, she broke in
    with my theories with mildew, and her heart, so that I began to admire 
    
    '''
    #Defines the starting gram
    s_gram = start_gram[:k]
    
    #Starts the generated string with the first k characters
    gen_string = s_gram
    
    #Starts at the firs character
    start_char = 0
    
    #Loops while the length of the generated string is less than the integer n
    while len(gen_string) < n:
        
        #g is set equal to the last k characters of the generated string
        g = gen_string[start_char:start_char+k]
        #the next character is generated
        next_char = generate_next_char(grams, g)
        #the next character is added to the generated string
        gen_string += next_char
        #1 is added to the character that is being started from
        start_char += 1
        
    #Gets the index of the last character in the created string
    last_char_index = len(gen_string)-1 
    
    #If the last character is not a space or a new line, it is deleted
    #This is repeated until the last character is a space or new line
    while gen_string[last_char_index] not in [' ','\n']:
        gen_string = gen_string[:last_char_index]
        last_char_index -= 1
        
    gen_string = gen_string[:last_char_index]
        
    return gen_string


#Replaces erroneous characters with a character predicted by the k-grams
def repair_text(corrupted_text, error_char, grams, k):
    '''
    (string, string, dict, int) -> string
    
    This function replaces erroneous characters with a character predicted by the k-grams for a given text, so long as there are k characters before the erroneous character.
    
    >>> seed(1330)    
    >>> grams = get_grams_from_files(['raven.txt', 'beowulf.txt'], 5)
    >>> print(repair_text('it was th~ bes~ of tim~s, i~ was ~he wo~st of~times', '~', grams, 5))
    it was the best of times, in was Bhe wolst of times
    
    >>> seed(1580)    
    >>> grams = get_grams_from_files(['holmes.txt'], 5)
    >>> print(repair_text('hell. darkness .y ', '.', grams, 5))
    hell. darkness Iy 
    
    >>> seed(2021)    
    >>> grams = get_grams_from_files(['beowulf.txt'], 2)
    >>> print(repair_text('th. hel. is.', '.', grams, 2))
    tha helm is 
    
    '''
    #Makes a copy of the corrupted text to be fixed
    new_text = corrupted_text
    
    #Loops through the length of the string corrupted_text   
    for i in range (len(corrupted_text)):
        
        #If the character is the error character, and there are at least k characters before said character, the next character is predicted and replaces the error character
        if corrupted_text[i] == error_char:
            if i >= k:
                curg = new_text[i-k:i]
                char = generate_next_char(grams, curg)
                new_text = new_text[:i] + char + new_text[i+1:]
                
    return new_text



grams = get_grams_from_files(['raven.txt'], 5)
print(generate_text(grams, "Once upon", 5, 500))
