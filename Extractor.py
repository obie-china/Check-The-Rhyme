
import pandas as pd

def extract_features():
 
    import re
    from g2p_en import G2p
    g2p = G2p()
    from string import digits

    vow = ['AA','AE','AH','AO','AW','AY','EH','ER','EY','IH','IY',
           'OW','OY','UH','UW']

    blosum = pd.read_csv('Blosum.txt', delim_whitespace=True)
    li = []
    ar = []
    syl = []
    l_r = []
    i_r = []
    w = []  #number of words
    uw = [] #unique words within lines
    
    for number in range(1,41):
        path = "New Text Document ({}).txt".format(number)
        temp = open(path, encoding ='utf8').readlines()
        
        #remove '\n' and make lines lowercase
        temp = [line.rstrip('\n') for line in temp]
        temp = [line.lower() for line in temp]
        
        #remove puctuations
        temp = [re.sub(r'[^\w\s]',' ',line) for line in temp]
        
        #append the list with the artiste's name
        ar.append(temp[0])
        
        #covert the verse to a list of lists
        temp = [[temp[i]] for i in range(len(temp))]
        verse = temp[1:]
        
        li.append(len(verse))
        
        #append word count
        words = [i[0].split() for i in verse]
        w.append(sum([len(i) for i in words]))
        
        #append sum of unique word counts within each line
        uw.append(sum([len(set(words[i])) for i in range(len(words))]))
        
    
        #transcribe the verse
        trans = [g2p(e) for e in verse]
        
        #remove spaces and puctuations
        puncts = [" ", "'",'"']
        temp = [[el for el in lis if el not in puncts] for lis in trans]
        
        #remove stress
        rdigs = str.maketrans('','', digits)
        sound = [[el.translate(rdigs) for el in main] for main in temp]
        
        #remove consonant sounds
        sound = [[el for el in lis if el in vow] for lis in sound]
        
        #append the list with the number of syllables
        le = [len(i) for i in sound]
        syl.append(sum(le))
        
        #match syllables between lines
        m = [] #all possible matches
        sc = [] #all the scores
        
        for i in range(len(sound)-1):
            for j in (sound[i]):
                for k in (sound[i+1]):
                    m.append((j,k))
                    
        for i in range (len(m)):
            for j in range(len(blosum.columns)):
                for k in range(len(blosum.index)):
                    if m[i] == (blosum.columns[j],blosum.index[k]):
                        sc.append(blosum.iloc[j,k])
        
        l_r.append(len([i for i in sc if i>0])) # no of scores for +ve matches 
        
        #match syllables within lines
        i_m = []
        i_sc = []
        
        for i in range(len(sound)):
            for j in (sound[i]):
                for k in (sound[i]):
                    i_m.append((j,k))
                    
        for i in range(len(i_m)):
            for j in range(len(blosum.columns)):
                for k in range(len(blosum.index)):
                    if i_m[i] == (blosum.columns[j],blosum.index[k]):
                        i_sc.append(blosum.iloc[j,k])
                        
        mat = len([i for i in i_sc if i>0])
        int_r = (mat - sum(le))/2
        i_r.append(int_r)
        
    features = [ar,syl,li,l_r,i_r,w,uw]
    return features    

def create_dataframe(artiste):

    data = extract_features()

    df = pd.DataFrame(data).T

    df.columns = ['artist','syl','lines','l_rhymes',
                  'int_rhymes','words','unique_w']

    df.to_csv("{}.csv".format(artiste), index=False)