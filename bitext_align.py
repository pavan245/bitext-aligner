# -*- coding: utf-8 -*- 


import os,sys
import re
import pandas as pd
from numpy import cumsum
from pandas import DataFrame
from nltk import word_tokenize, sent_tokenize
import xml.etree.ElementTree as ET
from jellyfish import levenshtein_distance as lev
import six
from google.cloud import translate_v2 as translate
from itertools import product as cp

translate_client = translate.Client()

'''

'''



def master_align(text0, text1, lang0, lang1): 
    """ Takes two equivalent texts (original and trnslation) and returns 
        aligned texts. """
    df0 = frame_from_text(text0, source=lang0, target=lang1)
    print('A')
    df1 = frame_from_text(text1, source=lang1, target=lang0, is1=True)
    print('B')
    # returns dfs with ['sent', 'trans', 'rellen', 'relpos']
    anchors = anchors_from_frames(df0, df1, score_funct, score_threshold, window=2)
    print('C')
    alignments = intermediate_align(df0, df1, anchors, lookahead=4)
    print('D')
    textdict0, textdict1 = textdicts_from_alignments(df0, df1, alignments)
    print('E')
    return textdict0, textdict1


def frame_from_text(text, source='ru', target='en', is1=False): # 
    """  """ # 
    cols = [c+str(int(is1)) for c in ['sent','trans','rellen','relpos']]
    frame = pd.DataFrame(columns=cols)
    frame[cols[0]] = sent_tokenize(text)
    frame[cols[1]] = frame[cols[0]].apply(lambda x: translate_client.translate(x, source_language=source, target_language=target, model='nmt')['translatedText'])
    frame[cols[2]] = frame[cols[0]].apply(lambda x: len(x))
    frame[cols[2]] = frame[cols[2]]/frame[cols[2]].max()
    cumul_b = list(np.cumsum(frame[cols[2]]))
    cumul_a = [0]+cumul_b[:-1]
    frame[cols[3]] = pd.Series(list(zip(cumul_a, cumul_b)))
    return frame


def anchors_from_frames(frame0, frame1, window): # 
    """  """
    pairdf = generate_pairdf(frame0, frame1, window)
    pairdf['lev0'] = pairdf[['sent0', 'trans1']].apply(lambda x: trdist(x.sent0, x.trans1))
    pairdf['lev1'] = pairdf[['sent1', 'trans0']].apply(lambda x: trdist(x.sent1, x.trans0))
    pairdf['rellen_ratio'] = (pairdf.rellen0/pairdf.rellen1).apply(gr1)
    pairdf['minlev'] = pairdf[['lev0', 'lev1']].min(axis=1)
    pairdf['maxlev'] = pairdf[['lev0', 'lev1']].min(axis=1)
    pairdf['isanchor'] = pairdf.minlev<0.45 & pairdf.maxlev<0.6 & pairdf.rellen_ratio<1.3
    return pairdf[pairdf.isanchor][['index0','index1']]


def intermediate_align(frame0, frame1, anchs, lookahead): # 
    """  """
    aligns = []
    end0, end1 = frame0.shape[0], frame1.shape[0]
    anchor_ranges = lis(zip([(-1,-1)]+anchs, anchs+[(end0, end1)]))
    for rang in anchor_ranges:
        interaligns =  get_interalign(frame0, frame1, *rang, lookahead)
        aligns.append(rang[0])
        aligns.extend(interaligns)
    return aligns[1:] # format [((i_start, i_end),(j_start, j_end))]


def get_interalign(df0, df1, anchors_init, anchors_next, lookahead): # 
    """  """
    interaligns = []
    i,j = anchors_init
    i+=1
    j+=1
    end0, end1 = anchors_next
    while i<end0 and j<end1:
        room0, room1 = min(end0-i,lookahead), min(end1-j,lookahead)
        best_alignment = min([(x,y) for x,y in cp(range(i,i+room0),range(j+room1)) if x==i or y==j], key=score(df0, df1, start0, start1, end0, end1))
        interaligns.append((best_alignment))
    return interaligns


def score(frame0, frame1, start0, start1, end0, end1): # 
    s0 = ' '.join(frame0.loc[start0:end0+1, 'sent0'])
    s1 = ' '.join(frame0.loc[start1:end1+1, 'sent1'])
    t0 = ' '.join(frame0.loc[start0:end0+1, 'trans0'])
    t1 = ' '.join(frame0.loc[start1:end1+1, 'trans1'])
    l0 = sum(frame0.loc[start0:end0+1, 'rellen0'])
    l1 = sum(frame1.loc[start1:end1+1, 'rellen1'])
    return (lev(s0,t1)+lev(s1,t0))*gr1(l0/l1)/2




def textdicts_from_alignments(frame0, frame1, aligns): # 
    """  """
    textdict0, textdict1 = {},{}
    for i,((a0,b0),(a1,b1)) in enumerate(aligns):
        t0 = ' '.join(frame0.loc[a0:b0+1, 'sent0'])
        t1 = ' '.join(frame0.loc[a1:b1+1, 'sent0'])
        textdict0.update({i:t0})
        textdict1.update({i:t1})
    return textdict0, textdict1


def generate_pairdf(frame0, frame1, window): 
    """  """
    pairdf = pd.DataFrame(columns=['index0', 'index1'])
    ranges0 = frame0.relpos0
    ranges1 = frame1.relpos1
    overlap = [(i,j) for (i,(a,b)),(j,(c,d)) in cp(enumerate(ranges0), enumerate(ranges1)) if get_overlap(a,b,c,d)>0]
    allpairs = []
    for i,j in overlap:
        for k in range(-window, window+1):
            for l in range(-window, window+1):
                allpairs.append()
    allpairs = sorted(list(set(allpairs)))
    pairdf[pairdf.columns] = pd.DataFrame(allpairs).values
    return pairdf


def get_overlap(a,b,c,d): 
    #print(a0,b0,a1,b1)
    if b0>a1 and b0<=b1:
        return b0-max(a0,a1)
    elif a0>=a1 and a0<b1:
        return min(b0,b1)-a0
    elif a1>=a0 and a1<b0:
        return b1-max(a0,a1)
    else:
        return 0


gr1 = lambda x: 1/less1(x)                       # 
less1 = lambda x: 1/x if abs(x)>1 else x         # 
trdist = lambda x,y: lev(x,y)/max(x,y)           # 


