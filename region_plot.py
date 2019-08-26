# Copyright 2019 Ahmet Cetinkaya

# This file is part of region_plot.

# region_plot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# region_plot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with region_plot.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import matplotlib.pyplot as pl
import matplotlib.collections as co
import time

def ask_tup(tup, x, y):
    (pred, dic) = tup
    c = (x, y)
    if not c in dic:
        dic[c]= pred(x, y)
    return dic[c]

def get_true_count(tup, xs, ys):
    true_count = 0
    for x in xs:
        for y in ys:
            if ask_tup(tup, x, y):
                true_count += 1
    return true_count

# if all corners have the same val, then the importance of further dividing
# such a rectangle is scaled by the "discovery" value
def get_rect_score(area, true_count, discovery):
    multiplier = 1.0
    if true_count == 0 or true_count == 4:
        multiplier = discovery
    elif true_count == 1:
        multiplier = (discovery + 1) / 2.0
    elif true_count == 2:
        multiplier = (discovery + 3) / 4.0
    return multiplier * area

def get_new_rect(tup, xs, ys, area, discovery):
    true_count = get_true_count(tup, xs, ys)
    rect_score = get_rect_score(area, true_count, discovery)
    return (xs, ys, area, true_count, rect_score)

def divide_rect(tup, rect, discovery):
    ((x1, x2), (y1, y2), area, true_count, rect_score) = rect
    # midx and midy floating point numbers both of which can be exactly represented by machine
    midx = (x1 + x2) / 2
    midy = (y1 + y2) / 2
    new_area = area / 4.0
    return [get_new_rect(tup, (x1, midx), (y1, midy), new_area, discovery),
            get_new_rect(tup, (midx, x2), (y1, midy), new_area, discovery),
            get_new_rect(tup, (x1, midx), (midy, y2), new_area, discovery),
            get_new_rect(tup, (midx, x2), (midy, y2), new_area, discovery)]

def fill_rects(xminmax, yminmax, rects,
               show_all=False, out_edgecolor="#000000", out_facecolor="#FFFFFF",
               *args, **kwargs):
    (xmin, xmax) = xminmax
    (ymin, ymax) = yminmax
    xdiff = xmax - xmin
    ydiff = ymax - ymin
    in_verts = []
    out_verts = []
    for rect in rects:
        ((x1, x2), (y1, y2), _, true_count, _) = rect
        if true_count == 4:
            in_verts.append([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
        if show_all and true_count < 4:
            out_verts.append([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])

    in_coll = co.PolyCollection(in_verts, *args, **kwargs)
    pl.gca().add_collection(in_coll)

    if show_all:
        out_coll = co.PolyCollection(out_verts, edgecolor=out_edgecolor, facecolor=out_facecolor)
        pl.gca().add_collection(out_coll)

    pl.xlim(xmin, xmax)
    pl.ylim(ymin, ymax)


def region_plot(pred, xminmax, yminmax, discovery=0.1, nof_divisions = 5000,
                show_all=False, out_edgecolor="#000000", out_facecolor="#FFFFFF",
                *args, **kwargs):
    dic = {}
    (xmin, xmax) = xminmax
    (ymin, ymax) = yminmax
    xdiff = xmax - xmin
    ydiff = ymax - ymin
    tup = (pred, dic)
    initial_area = xdiff * ydiff
    initial_rect = get_new_rect(tup, xminmax, yminmax, initial_area, discovery)
    rects = [initial_rect]
    for i in range(nof_divisions):
        rect = rects.pop()
        # sort new rects by their scores
        new_rects = divide_rect(tup, rect, discovery)
        new_rects.sort(key=lambda r: r[4])
        ni = 0
        ri = 0
        while True:
            if ni >= 4:
                break
            if ri >= len(rects):
                break
            new_score = new_rects[ni][4]
            current_score = rects[ri][4]
            if new_score <= current_score:
                rects.insert(ri, new_rects[ni])
                ri += 2
                ni += 1
            else:
                ri += 1
        while ni < 4:
            rects.append(new_rects[ni])
            ni += 1
    fill_rects(xminmax, yminmax, rects,
               show_all=show_all, out_edgecolor=out_edgecolor, out_facecolor=out_facecolor,
               *args, **kwargs)
