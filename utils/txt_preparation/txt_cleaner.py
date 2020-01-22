

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 13:45:29 2020

@author: DroidRonin
"""
import re
import pandas as pd


def get_text():
    file = open("C:\\Users\\Nerv\\Text-Technology\\Aligner\\txt\\crime_EN.txt", 'r')
    lines = file.readlines()
    file.close()
    count = 0
    star_index = list()

    for line in lines:
        line = line.strip()
        count = count + 1
        if '* * *' in line:
            print(True)
            star_index.append(count)
            print(count)    #The index comes out to be 55,1074

    print(lines[star_index[0]:star_index[1]])   #Gives out the text between the two star thingies
    total_text = lines[star_index[0]:star_index[1]]
    text_str = ''.join(total_text)

    pattern = re.compile(r"\b((chapter)[\s]+[IVXLCDM]+\b)", re.IGNORECASE)   #Regex for finding chapters
    chapter_list = re.findall(pattern, text_str)
    print(chapter_list)
    chapter_list1 = list()

    for chapter in chapter_list:
        for chap in chapter[0:1]:
            chapter_list1.append(chap)

    chap_seg = re.split(r'CHAPTER\s[A-Z.]+', text_str)[1:]
    chapter_div = list(zip(chapter_list1, chap_seg))

    for c in chapter_div:
        print(''.join(c))

    print(chapter_div[0])    #Will print out the first chapter












