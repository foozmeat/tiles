# tiles
A ceramic tile pattern generator

Tiles uses a YAML configuration file to generate an cermaic tile patterns. A sample YAML might look like

```
locale: 'en_US.UTF-8'

width: 48
height: 36
tilesize: 1
price_per_sq_unit: 30
tiles_per_sq_unit: 144

colors: [
'#ECE7D4',
'#BCCA96',
'#107F7E',
'#0A516C',
]

color_weights: [
  [ 20, 20, 9, 6, 3, 0 ],
  [ 1,  3,  3, 6, 4, 1  ],
  [ 1,  2,  3, 5, 8, 8  ],
  [ 0,  0,  1, 4, 7, 12  ],
]
```

This file sets up a 4' x 3' pattern with 4 colors and 6 vertical section with varying color weights defined top to bottom. 
Any number of colors and section are possible but the number of sections must divide evenly into the number of rows ( height / tilesize).
This file produce 

