#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 01:20:04 2018

@author: lauranguyen
"""

t = [[0, 0], [1, 2]]


def test(t):
    t = list(t)
    t[0] = t[0][:]
    t[0][1] = 3
    
test(t)
print(t)