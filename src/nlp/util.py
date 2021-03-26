



################ BASIC ################

import os
import sys
import traceback
import io
import shutil
import subprocess
import sqlite3
import logging

import re
import copy
from collections import OrderedDict, defaultdict, Counter

import time
from datetime import datetime

import threading
from threading import Thread

from pprint import pprint
from functools import partial

import importlib

import requests
import urllib
import base64
import zlib


################ SCIENTIFIC ################

import math
import random
try:
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import scipy
    import sklearn
except:
    pass

try:
    import PIL
    from PIL import Image, ImageFile, ImageFont, ImageDraw
    ImageFile.LOAD_TRUNCATED_IMAGES = True
except:
    pass

try:
    import cv2
except:
    pass


################ PARSING ################

import argparse
from argparse import Namespace, ArgumentParser

# args:  all args
# bargs: base args
# pargs: data processing args
# largs: data loading args
# margs: model args
# targs: training args

# parsing format:  mixed, use nest_namespace() to clean
# usage format:    nested namespace
# writing format:  yaml dicts

def nested_parse(parse_matrix, passed=[]):
    parser = ArgumentParser()
    for prefix,defaults in parse_matrix.items():
        parser = nest_parser(parser, prefix, defaults)
    args_mixed = parser.parse_args(passed)
    args = nest_namespace(args_mixed)
    return args
def nest_parser(parser, prefix, defaults):
    # nests defaults (dict or namespace) into parser (mixed), w/ prefixes
    defaults = to_dict(defaults)
    for k,v in defaults.items():
        if v is None:
            parser.add_argument(f'--{prefix}.{k}', default=v)
        else:
            parser.add_argument(f'--{prefix}.{k}', type=type(v), default=v)
    return parser
def nest_namespace(args):
    # mixed args --> nested namespace
    if isinstance(args, Namespace):
        nargs = Namespace()
        tonest = defaultdict(Namespace)
        for k,v in vars(args).items():
            if '.' in k:
                dot = k.index('.')
                k_pre,k_post = k[:dot], k[dot+1:]
                vars(tonest[k_pre])[k_post] = v
            else:
                vars(nargs)[k] = nest_namespace(v)
        for k,v in tonest.items():
            vars(nargs)[k] = nest_namespace(v)
        return nargs
    elif isinstance(args, dict):
        return Namespace(**{
            k: nest_namespace(v)
            for k,v in args.items()
        })
    elif isinstance(args, list):
        return [nest_namespace(q) for q in args]
    elif isinstance(args, tuple):
        return tuple(nest_namespace(q) for q in args)
    else:
        return args

def to_dict(nargs):
    # nested namespace --> nested dict
    if isinstance(nargs, Namespace):
        ndict = copy.deepcopy(vars(nargs))
        for k,v in ndict.items():
            ndict[k] = to_dict(v)
        return ndict
    elif isinstance(nargs, dict):
        return {k: to_dict(v) for k,v in nargs.items()}
    elif isinstance(nargs, list):
        return [to_dict(q) for q in nargs]
    elif isinstance(nargs, tuple):
        return tuple(to_dict(q) for q in nargs)
    else:
        return nargs
def to_namespace(dargs):
    # nested dict --> nested namespace
    if isinstance(dargs, dict):
        nargs = Namespace(**{
            k: to_namespace(v)
            for k,v in dargs.items()
        })
        return nargs
    elif isinstance(dargs, Namespace):
        return Namespace(**{
            k: to_namespace(v) for k,v in dargs.items()
        })
    elif isinstance(dargs, list):
        return [to_namespace(q) for q in dargs]
    elif isinstance(dargs, tuple):
        return tuple(to_namespace(q) for q in dargs)
    else:
        return dargs


################ FILE MANAGEMENT ################

def mkdir(dn, is_file=False):
    if not is_file:
        return os.makedirs(dn, exist_ok=True)
    else:
        dn = '/'.join(dn.split('/')[:-1])
        return mkdir(dn, is_file=False)

def read(fn, mode='r'):
    with open(fn, mode) as handle:
        return handle.read()
def write(text, fn, mode='w'):
    mkdir(fn, is_file=True)
    with open(fn, mode) as handle:
        return handle.write(text)

import pickle
def dump(obj, fn, mode='wb'):
    mkdir(fn, is_file=True)
    with open(fn, mode) as handle:
        return pickle.dump(obj, handle)
def load(fn, mode='rb'):
    with open(fn, mode) as handle:
        return pickle.load(handle)

import json
def jwrite(x, fn, mode='w', indent='\t', sort_keys=False):
    mkdir(fn, is_file=True)
    with open(fn, mode) as handle:
        return json.dump(x, handle, indent=indent, sort_keys=sort_keys)
def jread(fn, mode='r'):
    with open(fn, mode) as handle:
        return json.load(handle)

try:
    import yaml
    def ywrite(x, fn, mode='w', default_flow_style=False):
        mkdir(fn, is_file=True)
        with open(fn, mode) as handle:
            return yaml.dump(x, handle, default_flow_style=default_flow_style)
    def yread(fn, mode='r'):
        with open(fn, mode) as handle:
            return yaml.safe_load(handle)
except:
    # hacked yread: supports ints, floats, comments; else, string
    def yread(fn, mode='r'):
        raw = read(fn, mode=mode)
        lines = [l for l in raw.split('\n') if l!='']
        ans = {}
        for line in lines:
            line = line.split('#')[0]
            if line=='': continue
            line = line.split(': ')
            if len(line)!=2: continue
            k,v = line[0].strip(), line[1].strip()
            if len(k)==0 or len(v)==0: continue
            if v[0]=="'" and v[-1]=="'":
                v = v[1:-1]
            elif v[0]=='"' and v[-1]=='"':
                v = v[1:-1]
            if v.isdigit():
                v = int(v)
            elif v.replace('.','',1).isdigit():
                v = float(v)
            ans[k] = v
        return ans

try:
    import pyunpack
    import zipfile
    import tarfile
except:
    pass

try:
    import mysql
    import mysql.connector
except:
    pass


################ MISC ################

def isonow():
    return datetime.now().isoformat()

try:
    import psutil
    _memprocess = psutil.Process(os.getpid())
    _mempow = {
        'b': 1,
        'k': 1e3,
        'm': 1e6,
        'g': 1e9,
        't': 1e12,
    }
except:
    pass
def mem(units='m'):
    b = _memprocess.memory_info().rss
    try:
        return b / _mempow[units[0].lower()]
    except KeyError:
        return b

def chunk(array, length, mode='col'):
    if mode=='col':
        return [array[i:i+length] for i in range(0, len(array), length)]
    else:
        return chunk(array, math.ceil(len(array)/length), mode='col')


################ AESTHETIC ################

try:
    from tqdm.auto import tqdm as std_tqdm
    from tqdm.auto import trange as std_trange
    tqdm = partial(std_tqdm, dynamic_ncols=True)
    trange = partial(std_trange, dynamic_ncols=True)
except:
    pass

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Table:
    def __init__(self,
            table,
            delimiter=' ',
            orientation='br',
            double_colon=True,
                ):
        self.delimiter = delimiter
        self.orientation = orientation
        self.t = Table.parse(
            table, delimiter, orientation, double_colon
        )
        return


    # rendering
    def __str__(self):
        return self.render()
    def __repr__(self):
        return self.render()
    def render(self):
        # set up empty entry
        empty = ('', Table._spec(self.orientation, transpose=False))

        # calculate table size
        t = copy.deepcopy(self.t)
        totalrows = len(t)
        totalcols = [len(r) for r in t]
        assert min(totalcols)==max(totalcols)
        totalcols = totalcols[0]

        # string-ify
        for i in range(totalrows):
            for j in range(totalcols):
                x,s = t[i][j]
                sp = s[11]
                if sp: x = eval(f'f"{{{x}{sp}}}"')
                Table._put((str(x),s), t, (i,j), empty)

        # expand delimiters
        _repl = lambda s: \
            s[:2] + (1,0,0,0,0) + s[7:10] + (1,) + s[11:] \
            if s[2] else \
            s[:2] + (0,0,0,0,0) + s[7:10] + (1,) + s[11:]
        for i,row in enumerate(t):
            for j,(x,s_own) in enumerate(row):
                # expand delim_up(^)
                if s_own[3]:
                    u,v = i,j
                    while 0<=u:
                        _,s = t[u][v]
                        if (i,j)!=(u,v) and (s[2] and not s[10]): break
                        Table._put((x, _repl(s)), t, (u,v), empty)
                        u -= 1

                # expand delim_down(v)
                if s_own[4]:
                    u,v = i,j
                    while u<totalrows:
                        _,s = t[u][v]
                        if (i,j)!=(u,v) and (s[2] and not s[10]): break
                        Table._put((x, _repl(s)), t, (u,v), empty)
                        u += 1

                # expand delim_right(>)
                if s_own[5]:
                    u,v = i,j
                    while v<totalcols:
                        _,s = t[u][v]
                        if (i,j)!=(u,v) and (s[2] and not s[10]): break
                        Table._put((x, _repl(s)), t, (u,v), empty)
                        v += 1

                # expand delim_left(<)
                if s_own[6]:
                    u,v = i,j
                    while 0<=v:
                        _,s = t[u][v]
                        if (i,j)!=(u,v) and (s[2] and not s[10]): break
                        Table._put((x, _repl(s)), t, (u,v), empty)
                        v -= 1

        # justification calculation
        widths = [0,] * totalcols  # j
        heights = [0,] * totalrows # i
        for i,row in enumerate(t):
            for j,(x,s) in enumerate(row):
                # height caclulation
                heights[i] = max(heights[i], x.count('\n'))

                # width calculation; non-delim fillers no contribution
                if s[2] or not s[10]:
                    w = max(len(q) for q in x.split('\n'))
                    widths[j] = max(widths[j], w)
        # no newline ==> height=1
        heights = [h+1 for h in heights]

        # render table
        rend = []
        roff = 0
        for i,row in enumerate(t):
            for j,(x,s) in enumerate(row):
                w,h = widths[j], heights[i]

                # expand fillers and delimiters
                if s[2] or s[10]:
                    xs = x.split('\n')
                    xw0 = min(len(l) for l in xs)
                    xw1 = max(len(l) for l in xs)
                    xh = len(xs)
                    if (xw0==xw1==w) and (xh==h):
                        pass
                    elif xw0==xw1==w:
                        x = '\n'.join([xs[0],]*h)
                    elif xh==h:
                        x = '\n'.join([(l[0] if l else '')*w for l in xs])
                    else:
                        x = x[0] if x else ' '
                        x = '\n'.join([x*w,]*h)

                # justify horizontally
                x = [
                    l.rjust(w) if s[0] else l.ljust(w)
                    for l in x.split('\n')
                ]

                # justify vertically
                plus = [' '*w,]*(h-len(x))
                x = plus+x if not s[1] else x+plus

                # input to table
                for r,xline in enumerate(x):
                    Table._put(xline, rend, (roff+r,j), None)
            roff += h

        # return rendered string
        return '\n'.join([''.join(r) for r in rend])


    # parsing
    def _spec(s, transpose=False):
        if ':' in s:
            i = s.index(':')
            sp = s[i:]
            s = s[:i]
        else:
            sp = ''
            s = s.lower()
        return (
            int('r' in s),                                      #  0:: 0:left(l)   1:right(r)
            int('t' in s),                                      #  1:: 0:bottom(b) 1:top(t)
            int(any([i in s for i in ['.','<','>','^','v']])),  #  2:: delim_here(.)
            int('^' in s if not transpose else '<' in s),       #  3:: delim_up(^)
            int('v' in s if not transpose else '>' in s),       #  4:: delim_down(v)
            int('>' in s if not transpose else 'v' in s),       #  5:: delim_right(>)
            int('<' in s if not transpose else '^' in s),       #  6:: delim_left(<)
            int('+' in s),                                      #  7:: subtable(+)
            int('-' in s if not transpose else '|' in s),       #  8:: subtable_horiz(-)
            int('|' in s if not transpose else '-' in s),       #  9:: subtable_vert(|)
            int('_' in s),                                      # 10:: fill(_); if delim, overwrite; else fit
            sp,                                                 # 11:: special(:) f-string for numbers
        )
    def _put(obj, t, ij, empty):
        i,j = ij
        while i>=len(t):
            t.append([])
        while j>=len(t[i]):
            t[i].append(empty)
        t[i][j] = obj
        return
    def parse(
            table,
            delimiter=' ',
            orientation='br',
            double_colon=True,
                ):
        # disabling transpose
        transpose = False

        # set up empty entry
        empty = ('', Table._spec(orientation, transpose))

        # transpose
        t = []
        for i,row in enumerate(table):
            for j,item in enumerate(row):
                ij = (i,j) if not transpose else (j,i)
                if type(item)==tuple and len(item)==2 and type(item[1])==str:
                    item = (item[0], Table._spec(item[1], transpose))
                elif double_colon and type(item)==str and '::' in item:
                    x,s = item.split('::')
                    item = (x, Table._spec(s, transpose))
                else:
                    item = (item, Table._spec(orientation, transpose))
                Table._put(item, t, ij, empty)

        # normalization
        maxcol = 0
        maxrow = len(t)
        for i,row in enumerate(t):
            # take element number into account
            maxcol = max(maxcol, len([i for i in row if not i[1][2]]))

            # take subtables into account
            for j,(x,s) in enumerate(row):
                if s[7]:
                    r = len(x)
                    maxrow = max(maxrow, i+r)
                    c = max(len(q) for q in x)
                    maxcol = max(maxcol, j+c)
                elif s[8]:
                    c = len(x)
                    maxcol = max(maxcol, j+c)
                elif s[9]:
                    r = len(x)
                    maxrow = max(maxrow, i+r)
        totalcols = 2*maxcol + 1
        totalrows = maxrow
        t += [[]]*(totalrows-len(t))
        newt = []
        delim = (delimiter, Table._spec('._'+orientation, transpose))
        for i,row in enumerate(t):
            wasd = False
            tcount = 0
            for j in range(totalcols):
                item = t[i][tcount] if tcount<len(t[i]) else empty
                isd = item[1][2]
                if wasd and isd:
                    Table._put(empty, newt, (i,j), empty)
                    wasd = False
                elif wasd and not isd:
                    Table._put(item, newt, (i,j), empty)
                    tcount += 1
                    wasd = False
                elif not wasd and isd:
                    Table._put(item, newt, (i,j), empty)
                    tcount += 1
                    wasd = True
                elif not wasd and not isd:
                    Table._put(delim, newt, (i,j), empty)
                    wasd = True
        t = newt

        # normalization: add dummy last column for delimiter
        for row in t:
            row.append(empty)

        # expand subtables
        delim_cols = [i for i in range(totalcols) if i%2==0]
        while True:
            # find a table
            ij = None
            for i,row in enumerate(t):
                for j,item in enumerate(row):
                    st,s = item
                    if s[7]:
                        ij = i,j,7,st,s
                        break
                    elif s[8]:
                        ij = i,j,8,st,s
                        break
                    elif s[9]:
                        ij = i,j,9,st,s
                        break
                if ij is not None: break
            if ij is None: break

            # replace its specs
            i,j,k,st,s = ij
            s = list(s)
            s[7] = s[8] = s[9] = 0
            s = tuple(s)

            # expand it
            if k==7: # 2d table
                for x,row in enumerate(st):
                    for y,obj in enumerate(row):
                        a = i+x if not transpose else i+y
                        b = j+2*y if not transpose else j+2*x
                        Table._put((obj, s), t, (a,b), None)
            if k==8: # subtable_horiz
                for y,obj in enumerate(st):
                    Table._put((obj, s), t, (i,j+2*y), None)
            if k==9: # subtable_vert
                for x,obj in enumerate(st):
                    Table._put((obj, s), t, (i+x,j), None)

        # return, finally
        return t


if __name__=='__main__':
    import this
