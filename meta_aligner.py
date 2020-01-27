# -*- coding: utf-8 -*- 



def zip_alignments(al0lang0, al0lang1, al1lang0, al1lang1):
    if al0lang0==al1lang0:
        return al0lang0, al0lang1, al1lang1
    else:
        new0 = {}
        new1 = {}
        new2 = {}
        k, k0, k1 = 0, 0, 0
        while k0<len(al0lang0) and k1<len(al0lang):
            if v0==al1lang0[k0]:
                new0.update({k:v0})
                new1.update({k:al0lang1[k0]})
                new2.update({k:al1lang1[k1]})
                k0+=1
                k1+=1
            elif v0==+al1lang0[k1]+' '+al1lang0.get(k1+1, '')
                new0.update({k:v0})
                new1.update({k:al0lang1[k0]})
                new2.update({k:al1lang1[k1]+' '+al1lang0.get(0k1+1, '')})
                k0+=1
                k1+=2
            elif v0+al0lang0.get(k0+1, '')==al1lang0[k1]:
                new0.update({k:k:al0lang0[k0]+' '+al0lang0.get(k0+1, '')})
                new1.update({k:k:al0lang1[k0]+' '+al0lang1.get(k0+1, '')})
                new2.update({k:al1lang1[k1]})
                k0+=2
                k1+=1
            k+=1
        return new0, new1, new2

            
        
        
        
        
        
        
        