# coding: utf-8
from collections import OrderedDict
from itertools import chain
from pathlib import Path
import sys

from lxml import etree
import regex as re
import urwid

from playnames_to_files import playnames

class PlayLine():
    def __init__(self, contentnum, linetype, actnum, linenum, text, flag):
        self.cnum = contentnum
        self.type = linetype
        self.act  = actnum
        self.num  = linenum
        self.text = text
        self.flag = flag


class Bard():

    playlist = OrderedDict(sorted(playnames.items(), key=lambda tup: tup[0]))
    #path = '/home/scaro/python/bard/xml/'

    def __init__(self, playfilename):

        if not Path(playfilename).is_file():
            raise FileNotFoundError

        parser = etree.XMLParser(dtd_validation=True, remove_blank_text=True)

        self.root = etree.parse(playfilename, parser).getroot()
        self.title = self.root.find('TITLE').text
        self.acts = self.root.findall('ACT')
        self.contentbyact = [ [] for act in range(5) ]
        self.contentaslist = []

        for act in self.acts:
            # cleanup XML when stagedir is inside a line:
            # <LINE><STAGEDIR>Aside</STAGEDIR>  A little more than kin, and less than kind.</LINE>
            #
            # TO FIX:
            # <LINE><STAGEDIR>Pointing to his head and shoulder</STAGEDIR></LINE>
            for sdir in act.xpath('//LINE/STAGEDIR'):
                line = sdir.getparent()
                line.addprevious(sdir)
                try:
                    line.text = sdir.tail.strip()
                except AttributeError:
                    line.text = '' #sdir.tail

        contentnum = 0   # for search
        for actnum, act in enumerate(self.acts):
            linenum = 0                        # all non dialog lines get 0
            textnum = 0
            for elem in act.iterdescendants():
                if elem.tag in ['SCENE', 'SPEECH', 'PROLOGUE', 'EPILOGUE']:
                    continue
                elif elem.tag == 'LINE':
                    textnum += 1               # counts only dialog lines
                    linenum = textnum

                content = PlayLine(contentnum, elem.tag.lower(), actnum+1, linenum, elem.text, False)
                self.contentbyact[actnum].append(content)
                self.contentaslist.append(content)
                linenum = 0
                contentnum += 1

    def __iter__(self):
        return iter(self.contentaslist)

    def __getitem__(self, i):
        return self.contentaslist[i]

    def getline(self, lnum):
        return [line for line in self if line.num == lnum][0]

    def clearsearch(self):
        for line in self:
            line.flag = False

    def search(self, pat, err=0):
        pattern = re.compile('(?:\\b{pat}\\b){{i<={err},s<={err}}}'.
                             format(pat=pat,err=err), flags=re.IGNORECASE | re.V1)
        #print(pattern)
        res = []
        for line in [l for l in self if l.type == 'line']:
            match = re.search(pattern, line.text)
            if match:
                line.flag = True

        res = [content.cnum for content in self if content.flag == True]
        return res

    def showsrch(self):
        for line in self:
            if line.flag:
                print(line.cnum, line.num, line.text)

if __name__ == '__main__':
    p = Bard('xml/hamlet.xml')

