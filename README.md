# 3D Spiral Image Torus/Knot Visualization

![Fractal Knot Animation](https://github.com/chrismrutherford/torus_spiral/blob/master/fractalKnot480.gif)

A Python visualization tool that maps images or fractals onto various 3D topological surfaces (torus, knots, Klein bottle, Möbius strip, etc.) with animated scrolling effects.

## Features

- **Multiple Topologies**: Torus, torus knots (trefoil, figure-8, cinquefoil, etc.), 4D shapes projected to 3D (Clifford torus, hypersphere slices), Klein bottle, Möbius strip, seashell, and more
- **Image Mapping**: Load images from a folder and map them onto 3D surfaces
- **Fractal Textures**: Generate Mandelbrot, Julia set, or Burning Ship fractals as textures
- **Two Mapping Modes**:
  - **Spiral Mode**: Images wrap in a spiral pattern around the surface
  - **Fitted Mode**: Natural UV mapping with optional Möbius-like twist effects
- **Animation**: Smooth scrolling textures with optional tumbling rotation
- **Dynamic Backgrounds**: Background colors cycle based on image color palettes
- **Topology Cycling**: Auto-cycle through all available topologies every 5 seconds

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

Required packages:
- pyvista
- numpy
- pillow
- scipy

## Usage

### Basic Usage

Place images in the `images/` folder and run:

```bash
python torus_spiral.py
```

This will cycle through all available topologies every 5 seconds with your images.

### Example Commands

#### Using Fractals

Generate a Mandelbrot fractal on a trefoil knot:

```bash
python torus_spiral.py --knot trefoil --fractal mandelbrot
```

Generate a Julia set fractal with rotation:

```bash
python torus_spiral.py --fractal julia --rotate --rotation-speed 1.5
```

Burning Ship fractal on a Klein bottle:

```bash
python torus_spiral.py --knot klein --fractal burning_ship --fit
```

#### Different Topologies

Simple torus with images:

```bash
python torus_spiral.py --knot torus
```

Trefoil knot (3,2):

```bash
python torus_spiral.py --knot trefoil --rotate
```

Figure-8 knot (4,3):

```bash
python torus_spiral.py --knot figure8 --spiral-turns 3
```

Cinquefoil knot (5,2):

```bash
python torus_spiral.py --knot cinquefoil --scroll-speed 5
```

Pretzel knot (11,7):

```bash
python torus_spiral.py --knot pretzel --spiral-turns 8
```

#### 4D Topologies

Clifford torus (4D torus projected to 3D):

```bash
python torus_spiral.py --knot clifford --fractal mandelbrot --fit
```

4D hypersphere slice:

```bash
python torus_spiral.py --knot hypersphere --rotate --rotation-speed 0.5
```

4D torus knot with custom parameters:

```bash
python torus_spiral.py --knot 4dknot --p 3 --q 2 --r 2 --fractal julia
```

#### Custom Knots

Create custom torus knots with p and q parameters:

```bash
python torus_spiral.py --knot custom --p 7 --q 5 --spiral-turns 10
```

#### Fitted Mode with Twist

Natural UV mapping without spiral distortion:

```bash
python torus_spiral.py --knot torus --fit
```

Add a Möbius-like twist (1.0 = half twist):

```bash
python torus_spiral.py --knot torus --fit --twist 1.0
```

Double twist:

```bash
python torus_spiral.py --knot trefoil --fit --twist 2.0 --fractal mandelbrot
```

#### Animation Controls

Fast scrolling with rotation:

```bash
python torus_spiral.py --scroll-speed 10 --rotate --rotation-speed 2.0
```

Slow, smooth animation:

```bash
python torus_spiral.py --scroll-speed 1 --spiral-turns 3 --rotate --rotation-speed 0.3
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--knot` | Topology type: torus, trefoil, figure8, cinquefoil, pentafoil, septafoil, octafoil, solomon, turkshead, pretzel, clifford, hypersphere, 4dknot, custom | Cycles through all |
| `--p` | P parameter for custom torus knot | 3 |
| `--q` | Q parameter for custom torus knot | 2 |
| `--r` | R parameter for 4D torus knot (4th dimension oscillation) | 1 |
| `--spiral-turns` | Number of spiral turns | 5 |
| `--scroll-speed` | Texture scroll speed (pixels) | 3 |
| `--rotate` | Enable tumbling rotation | Off |
| `--rotation-speed` | Rotation speed multiplier | 1.0 |
| `--fit` | Use natural UV mapping (no spiral distortion) | Off |
| `--twist` | Number of twists/half-turns (try 1.0 for Möbius effect) | 0.0 |
| `--fractal` | Use fractal texture: mandelbrot, julia, burning_ship | None (uses images) |

## Topology Types

- **torus**: Simple torus (donut shape)
- **trefoil**: Trefoil knot (3,2) - simplest non-trivial knot
- **figure8**: Figure-8 knot (4,3)
- **cinquefoil**: Cinquefoil knot (5,2)
- **pentafoil**: Pentafoil knot (5,4)
- **septafoil**: Septafoil knot (7,2)
- **octafoil**: Octafoil knot (8,3)
- **solomon**: Solomon's seal knot (5,3)
- **turkshead**: Turk's head knot (7,3)
- **pretzel**: Pretzel knot (11,7)
- **clifford**: Clifford torus (4D torus projected to 3D)
- **hypersphere**: 4D hypersphere slice
- **4dknot**: 4D torus knot
- **custom**: Custom (p,q) torus knot

## Controls

- Press **q** to quit the visualization
- The camera view is interactive - you can rotate and zoom with mouse

## License

MIT License - see file header for details.

Copyright (c) 2026 Christopher Rutherford
