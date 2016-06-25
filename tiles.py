import sys
from random import random

import locale
import os
import yaml
from jinja2 import Environment, FileSystemLoader

input_file = open('config.yaml')

config = yaml.load(input_file)

locale.setlocale(locale.LC_ALL, config['locale'])
tilesize = config['tilesize']
height = config['height']
width = config['width']
sections = len(config['color_weights'][0])
num_colors = len(config['color_weights'])
rows = height / tilesize
cols = width / tilesize
section_length = rows / sections

if height % tilesize != 0:
    sys.exit("height not divisible by tilesize")
elif width % tilesize != 0:
    sys.exit("width not divisible by tilesize")
elif height % sections != 0:
    sys.exit("height not divisible by number of sections")

print "Rows: %s   Cols: %s  Colors: %s   Sections: %s   Section Length: %s" % (
    rows, cols, num_colors, sections, section_length)

grid = [[0 for x in range(cols)] for y in range(rows)]

zipped_colors = zip(*config['color_weights'])

section_totals = map(sum, zipped_colors)

buckets = [[0 for x in range(num_colors)] for y in range(sections)]
tile_counts = [0 for x in range(num_colors + 1)]

for s_idx, total in enumerate(section_totals):

    whole = 0.0

    for c_idx, color_weight in enumerate(zipped_colors[s_idx]):
        ratio = color_weight / float(total)
        value = whole + ratio
        whole += ratio

        buckets[s_idx][c_idx] = value

section_num = 0

for s_idx, section in enumerate(buckets):
    for r_idx in range(section_length):

        row_n = (s_idx * section_length) + r_idx

        for c_idx in range(cols):
            r = random()

            for color_idx, p in enumerate(section):
                if r <= p:
                    grid[row_n][c_idx] = color_idx
                    tile_counts[color_idx] += 1
                    break

tile_count_total = sum(tile_counts)

total_sq_size = width * height / config['tiles_per_sq_unit']
total_cost = total_sq_size * float(config['price_per_sq_unit'])

formatted_cost = locale.currency(total_cost, symbol=True, grouping=True)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)

context = {
    'colors': config['colors'],
    'grid': grid,
    'section_length': section_length,
    'tilesize': tilesize,
    'tile_counts': tile_counts,
    'tile_count_total': tile_count_total,
    'formatted_cost': formatted_cost,

}

rendered_template = env.get_template('output.html.j2').render(context)

with open('output.html', 'w') as f:
    f.write(rendered_template)
