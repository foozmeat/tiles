from random import random

import os
from jinja2 import Environment, Template, FileSystemLoader

import yaml

input_file = open('config.yaml')

config = yaml.load(input_file)

print config

rows = config['height'] / config['tilesize']
cols = config['width'] / config['tilesize']
sections = len(config['color_weights'][0])
num_colors = len(config['color_weights'])

section_length = rows / sections
print "Rows: %s   Cols: %s  Colors: %s   Sections: %s   Section Length: %s" % (
rows, cols, num_colors, sections, section_length)

# make grid
grid = [[0 for x in range(cols)] for y in range(rows)]
# for row_idx, row in enumerate(grid):
#     print 'grid', row

zipped_colors = zip(*config['color_weights'])
print "zipped colors", zipped_colors

section_totals = map(sum, zipped_colors)
# print section_totals

# make buckets
buckets = [[0 for x in range(num_colors)] for y in range(sections)]

for s_idx, total in enumerate(section_totals):

    whole = 0.0

    for c_idx, color_weight in enumerate(zipped_colors[s_idx]):

        ratio = color_weight / float(total)
        value = whole + ratio
        whole += ratio

        buckets[s_idx][c_idx] = value

print 'buckets', buckets

section_num = 0

for s_idx, section in enumerate(buckets):
    for r_idx in range(section_length):

        row_n = (s_idx * section_length) + r_idx

        for c_idx in range(cols):
            # print "Section: %s   Row: %s   Col: %s" % (s_idx, r_idx, c_idx)
            r = random()

            for color_idx, p in enumerate(section):
                if r <= p:
                    grid[row_n][c_idx] = color_idx
                    break


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)

context = {
    'colors': config['colors'],
    'grid': grid,
    'section_length': section_length,
}

rendered_template = env.get_template('output.html.j2').render(context)
# print rendered_template

with open('output.html', 'w') as f:
    f.write(rendered_template)

# for row in range(rows):
#     print grid[row]

