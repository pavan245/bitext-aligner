# -*- coding: utf-8 -*- 


from itertools import product as cp

import numpy as np
import pandas as pd
from google.cloud import translate_v2 as translate
from jellyfish import levenshtein_distance as lev
import nltk
import utils.constants as const
nltk.download('punkt')

translate_client = translate.Client()

'''

'''

def master_align(text0, text1, lang0, lang1): 
    """ Takes two equivalent texts (original and trnslation) and returns 
        aligned texts. """
    df0 = frame_from_text(text0, lang0, lang1)
    # print('A')
    df1 = frame_from_text(text1, lang1, lang0, is1=True)
    # print('B')
    # returns dfs with ['sent', 'trans', 'rellen', 'relpos']
    anchors = anchors_from_frames(df0, df1, window=2)
    # print('C')
    alignments = intermediate_align(df0, df1, anchors, lookahead=4)
    # print('D')
    textdict0, textdict1 = textdicts_from_alignments(df0, df1, alignments)
    # print('E')
    return textdict0, textdict1


def frame_from_text(text, source, target, is1=False): # 
    """  """ # 
    #print(source, '-->', target)
    cols = [c+str(int(is1)) for c in ['sent','trans','rellen','relpos']]
    #print(cols)
    frame = pd.DataFrame(columns=cols)
    frame[cols[0]] = nltk.sent_tokenize(text, language=const.LANGUAGE_NAME[source])
    frame[cols[1]] = frame[cols[0]].apply(lambda x: translate_client.translate(x, source_language=source, target_language=target, model='nmt')['translatedText'])
    frame[cols[2]] = frame[cols[0]].apply(lambda x: len(x))
    frame[cols[2]] = frame[cols[2]]/frame[cols[2]].max()
    cumul_b = list(np.cumsum(frame[cols[2]]))
    cumul_a = [0]+cumul_b[:-1]
    frame[cols[3]] = pd.Series(list(zip(cumul_a, cumul_b)))
    #print(frame[[cols[0], cols[1]]])
    return frame


def anchors_from_frames(frame0, frame1, window): # 
    """  """
    pairdf = generate_pairdf(frame0, frame1, window)
    frame0['index0'] = frame0.index
    frame1['index1'] = frame1.index
    pairdf = pairdf.merge(frame0, on='index0').merge(frame1, on='index1')
    pairdf['lev0'] = pairdf.apply(lambda x: trdist(x.sent0, x.trans1), axis=1)
    pairdf['lev1'] = pairdf.apply(lambda x: trdist(x.sent1, x.trans0), axis=1)
    pairdf['rellen_ratio'] = (pairdf.rellen0/pairdf.rellen1).apply(gr1)
    pairdf['minlev'] = pairdf[['lev0', 'lev1']].min(axis=1)
    pairdf['maxlev'] = pairdf[['lev0', 'lev1']].min(axis=1)
    pairdf['isanchor'] = (pairdf.minlev<0.45) & (pairdf.maxlev<0.6) & (pairdf.rellen_ratio<1.3)
    return list(pairdf[pairdf.isanchor][['index0','index1']].values)


def intermediate_align(frame0, frame1, anchs, lookahead): # 
    """  """
    aligns = []
    end0, end1 = frame0.shape[0], frame1.shape[0]
    anchor_ranges = list(zip([(-1,-1)]+anchs, anchs+[(end0, end1)]))
    for rang in anchor_ranges:
        interaligns =  get_interalign(frame0, frame1, *rang, lookahead)
        a,b = rang[0]
        aligns.append(((a,b),(a,b)))
        aligns.extend(interaligns)
    return aligns[1:] # format [((i_start, i_end),(j_start, j_end))]


def get_interalign(df0, df1, anchors_init, anchors_next, lookahead): # 
    """  """
    # print(anchors_init, anchors_next)
    interaligns = []
    i,j = anchors_init
    i+=1
    j+=1
    end0, end1 = anchors_next
    while i<end0 and j<end1:
        room0, room1 = min(end0-i,lookahead), min(end1-j,lookahead)
        lambdascore = lambda p,q: score(df0, df1, i, j, p, q)
        i_,j_ = min([(x,y) for x,y in cp(range(i,i+room0),range(j,j+room1)) if x==i or y==j], key=lambda a: lambdascore(*a))
        # print((i,j), (i_,j_))
        interaligns.append(((i,j),(i_,j_)))
        i,j = i_+1,j_+1
    return interaligns


def score(frame0, frame1, start0, start1, end0, end1): # 
    #print(frame0.columns)
    #print(frame1.columns)
    s0 = ' '.join(frame0.loc[start0:end0, 'sent0'])
    s1 = ' '.join(frame1.loc[start1:end1, 'sent1'])
    t0 = ' '.join(frame0.loc[start0:end0, 'trans0'])
    t1 = ' '.join(frame1.loc[start1:end1, 'trans1'])
    l0 = sum(frame0.loc[start0:end0, 'rellen0'])
    l1 = sum(frame1.loc[start1:end1, 'rellen1'])
    #print(s0, s1, t0, t1, l0, l1)
    return (trdist(s0,t1)+trdist(s1,t0))*gr1(l0/l1)/2




def textdicts_from_alignments(frame0, frame1, aligns): # 
    """  """
    textdict0, textdict1 = {},{}
    for i,((a0,a1),(b0,b1)) in enumerate(aligns):
        t0 = ' '.join(frame0.loc[a0:b0, 'sent0'])
        t1 = ' '.join(frame1.loc[a1:b1, 'sent1'])
        # print('***************************')
        # print(aligns[i])
        # print(t0)
        # print(t1)
        textdict0.update({i:t0})
        textdict1.update({i:t1})
    return textdict0, textdict1


def generate_pairdf(frame0, frame1, window): 
    """  """
    pairdf = pd.DataFrame(columns=['index0', 'index1'])
    ranges0 = frame0.relpos0
    ranges1 = frame1.relpos1
    overlap = [(i,j) for (i,(a,b)),(j,(c,d)) in cp(enumerate(ranges0), enumerate(ranges1)) if get_overlap(a,b,c,d)>0]
    len0 = frame0.shape[0]
    len1 = frame1.shape[0]
    allpairs = []
    for i,j in overlap:
        for k in range(-window, window+1):
            for l in range(-window, window+1):
                allpairs.append((i+k,j+l))
    allpairs = [(a,b) for a,b in allpairs if min(a,b)>-1 and a<len0 and b<len1]
    allpairs = sorted(list(set(allpairs)))
    pairdf = pd.DataFrame(allpairs).rename(columns={0:'index0', 1:'index1'})
    return pairdf


def get_overlap(a,b,c,d): 
    #print(a0,b0,a1,b1)
    if b>c and b<=d:
        return b-max(a,c)
    elif a>=c and a<d:
        return min(b,d)-a
    elif c>=a and c<b:
        return d-max(a,c)
    else:
        return 0


gr1 = lambda x: 1/less1(x)                       # 
less1 = lambda x: 1/x if abs(x)>1 else x         # 
trdist = lambda x,y: lev(x,y)/max(len(x),len(y))           # 


