"""
3D Spiral Image Torus/Knot Visualization

Copyright (c) 2026 Christopher Rutherford <chrisrutherford@protonmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pyvista as pv
import numpy as np
from pathlib import Path
from PIL import Image
import glob
import argparse

def create_torus(major_radius=2, minor_radius=1, u_resolution=100, v_resolution=50):
    """Create a parametric torus mesh."""
    u = np.linspace(0, 2 * np.pi, u_resolution)
    v = np.linspace(0, 2 * np.pi, v_resolution)
    u, v = np.meshgrid(u, v)
    
    x = (major_radius + minor_radius * np.cos(v)) * np.cos(u)
    y = (major_radius + minor_radius * np.cos(v)) * np.sin(u)
    z = minor_radius * np.sin(v)
    
    # Create structured grid and convert to PolyData surface
    grid = pv.StructuredGrid(x, y, z)
    return grid.extract_surface(algorithm='dataset_surface')

def create_torus_knot(p=3, q=2, major_radius=3, minor_radius=0.5, u_resolution=200, v_resolution=50):
    """
    Create a (p,q) torus knot mesh.
    
    Parameters:
    - p: number of times the knot winds around the torus longitudinally
    - q: number of times the knot winds around the torus meridionally
    
    Common knots:
    - (3,2): Trefoil knot (simplest non-trivial knot)
    - (4,3): Figure-8 knot
    - (5,2): Cinquefoil knot
    - (5,4): Pentafoil knot
    """
    u = np.linspace(0, 2 * np.pi, u_resolution)
    v = np.linspace(0, 2 * np.pi, v_resolution)
    u, v = np.meshgrid(u, v)
    
    # Torus knot parameterization
    r = np.cos(q * u) + major_radius
    x = r * np.cos(p * u) + minor_radius * np.cos(v) * np.cos(p * u)
    y = r * np.sin(p * u) + minor_radius * np.cos(v) * np.sin(p * u)
    z = -np.sin(q * u) + minor_radius * np.sin(v)
    
    # Create structured grid and convert to PolyData surface
    grid = pv.StructuredGrid(x, y, z)
    return grid.extract_surface(algorithm='dataset_surface')

def create_klein_bottle(u_resolution=100, v_resolution=100, scale=2.0):
    """Create a Klein bottle (4D object immersed in 3D)."""
    u = np.linspace(0, 2 * np.pi, u_resolution)
    v = np.linspace(0, 2 * np.pi, v_resolution)
    u, v = np.meshgrid(u, v)
    
    # Figure-8 immersion of Klein bottle
    r = 4 * (1 - np.cos(u) / 2)
    x = (6 * np.cos(u) * (1 + np.sin(u)) + r * np.cos(u) * np.cos(v)) * scale / 6
    y = (16 * np.sin(u) + r * np.sin(u) * np.cos(v)) * scale / 6
    z = (r * np.sin(v)) * scale / 6
    
    grid = pv.StructuredGrid(x, y, z)
    return grid.extract_surface(algorithm='dataset_surface')

def create_mobius_strip(u_resolution=100, v_resolution=20, radius=2.0, width=1.0):
    """Create a Möbius strip (one-sided surface)."""
    u = np.linspace(0, 2 * np.pi, u_resolution)
    v = np.linspace(-width, width, v_resolution)
    u, v = np.meshgrid(u, v)
    
    # Möbius strip parameterization
    x = (radius + v * np.cos(u / 2)) * np.cos(u)
    y = (radius + v * np.cos(u / 2)) * np.sin(u)
    z = v * np.sin(u / 2)
    
    grid = pv.StructuredGrid(x, y, z)
    return grid.extract_surface(algorithm='dataset_surface')

def create_seashell(u_resolution=100, v_resolution=100, scale=1.5):
    """Create a seashell/conch shape with logarithmic spiral."""
    u = np.linspace(0, 6 * np.pi, u_resolution)
    v = np.linspace(0, 2 * np.pi, v_resolution)
    u, v = np.meshgrid(u, v)
    
    # Logarithmic spiral shell
    a = 0.2  # Growth rate
    b = 0.3  # Aperture size
    
    r = b * np.exp(a * u)
    x = r * np.cos(u) * (1 + np.cos(v)) * scale
    y = r * np.sin(u) * (1 + np.cos(v)) * scale
    z = r * np.sin(v) * scale
    
    grid = pv.StructuredGrid(x, y, z)
    return grid.extract_surface(algorithm='dataset_surface')

def create_spherical_harmonic(l=3, m=2, u_resolution=100, v_resolution=100, radius=2.0):
    """Create a sphere deformed by spherical harmonics (vibration modes)."""
    u = np.linspace(0, np.pi, u_resolution)
    v = np.linspace(0, 2 * np.pi, v_resolution)
    u, v = np.meshgrid(u, v)
    
    # Spherical harmonic deformation
    from scipy.special import sph_harm
    Y = np.real(sph_harm(m, l, v, u))
    r = radius * (1 + 0.3 * Y)
    
    x = r * np.sin(u) * np.cos(v)
    y = r * np.sin(u) * np.sin(v)
    z = r * np.cos(u)
    
    grid = pv.StructuredGrid(x, y, z)
    return grid.extract_surface(algorithm='dataset_surface')

def create_clifford_torus(u_resolution=100, v_resolution=100, scale=2.0):
    """
    Create a Clifford torus - a flat torus in 4D space, stereographically projected to 3D.
    
    The Clifford torus is the simplest embedding of a torus in 4D space (S³).
    It has equal major and minor radii in 4D, making it perfectly symmetrical.
    When projected to 3D, it creates a beautiful shape that appears to turn inside-out.
    """
    u = np.linspace(0, 2 * np.pi, u_resolution)
    v = np.linspace(0, 2 * np.pi, v_resolution)
    u, v = np.meshgrid(u, v)
    
    # Clifford torus in 4D (lives on S³ hypersphere)
    # Four coordinates that trace out a torus on the 3-sphere
    r = 1.0 / np.sqrt(2)  # Radius to make it lie on unit S³
    
    x4d = r * np.cos(u)
    y4d = r * np.sin(u)
    z4d = r * np.cos(v)
    w4d = r * np.sin(v)
    
    # Stereographic projection from 4D to 3D
    # Project from the north pole (0,0,0,1) onto the hyperplane w=0
    denominator = 1 - w4d
    # Avoid division by zero
    denominator = np.where(np.abs(denominator) < 0.01, 0.01, denominator)
    
    x = (x4d / denominator) * scale
    y = (y4d / denominator) * scale
    z = (z4d / denominator) * scale
    
    grid = pv.StructuredGrid(x, y, z)
    return grid.extract_surface(algorithm='dataset_surface')

def create_4d_torus_knot(p=3, q=2, r=1, u_resolution=200, v_resolution=50, scale=2.0):
    """
    Create a 4D torus knot projected to 3D.
    
    Parameters:
    - p, q: traditional torus knot winding numbers
    - r: controls movement in the 4th dimension (try 1, 2, 3)
    
    This extends the traditional (p,q) torus knot to 4D by adding
    a third winding number that controls oscillation in the w-dimension.
    """
    u = np.linspace(0, 2 * np.pi, u_resolution)
    v = np.linspace(0, 2 * np.pi, v_resolution)
    u, v = np.meshgrid(u, v)
    
    # 4D torus knot parameterization
    major_radius = 3.0
    minor_radius = 0.5
    
    # Path in 4D space
    center_r = np.cos(q * u) + major_radius
    
    # Four coordinates
    x4d = center_r * np.cos(p * u) + minor_radius * np.cos(v) * np.cos(p * u)
    y4d = center_r * np.sin(p * u) + minor_radius * np.cos(v) * np.sin(p * u)
    z4d = -np.sin(q * u) + minor_radius * np.sin(v)
    w4d = np.sin(r * u) * 1.5  # Oscillation in 4th dimension
    
    # Stereographic projection to 3D
    denominator = 1 - w4d / 5.0  # Scale w to avoid extreme projection
    denominator = np.where(np.abs(denominator) < 0.1, 0.1, denominator)
    
    x = (x4d / denominator) * scale / 2
    y = (y4d / denominator) * scale / 2
    z = (z4d / denominator) * scale / 2
    
    grid = pv.StructuredGrid(x, y, z)
    return grid.extract_surface(algorithm='dataset_surface')

def create_hypersphere_slice(phi=0.0, u_resolution=100, v_resolution=100, radius=2.5):
    """
    Create a 3D slice of a 4D hypersphere (S³).
    
    A hypersphere is the 4D analogue of a sphere. We can't see all of it at once,
    but we can take 3D "slices" at different positions in the 4th dimension.
    
    Parameters:
    - phi: position of the slice in the 4th dimension (0 to π)
    
    As phi varies from 0 to π, the slice starts as a point, grows to a sphere,
    then shrinks back to a point - like slicing through a 3D sphere with 2D planes.
    """
    u = np.linspace(0, np.pi, u_resolution)
    v = np.linspace(0, 2 * np.pi, v_resolution)
    u, v = np.meshgrid(u, v)
    
    # 4D hypersphere parameterization (all four coordinates)
    # We fix the 4th angle (phi) and vary the other three
    x4d = np.sin(phi) * np.sin(u) * np.cos(v)
    y4d = np.sin(phi) * np.sin(u) * np.sin(v)
    z4d = np.sin(phi) * np.cos(u)
    w4d = np.cos(phi)
    
    # For visualization, we project the 4D point onto 3D
    # Use perspective projection based on w coordinate
    scale_factor = radius / (1.5 - w4d)
    
    x = x4d * scale_factor
    y = y4d * scale_factor
    z = z4d * scale_factor
    
    grid = pv.StructuredGrid(x, y, z)
    return grid.extract_surface(algorithm='dataset_surface')

def create_mandelbrot_texture(width=2048, height=1024, max_iter=256, zoom=1.0, center_x=-0.5, center_y=0.0):
    """Generate a Mandelbrot set fractal texture."""
    # Create coordinate arrays
    x = np.linspace(center_x - 2.0/zoom, center_x + 2.0/zoom, width)
    y = np.linspace(center_y - 1.0/zoom, center_y + 1.0/zoom, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    # Initialize Z and iteration count
    Z = np.zeros_like(C)
    M = np.zeros(C.shape)
    
    # Mandelbrot iteration
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask]**2 + C[mask]
        M[mask] = i
    
    # Smooth coloring using logarithmic scaling
    # Add smooth iteration count for points that escaped
    mask_escaped = np.abs(Z) > 2
    M[mask_escaped] = M[mask_escaped] + 1 - np.log(np.log(np.abs(Z[mask_escaped])))/np.log(2)
    
    # Normalize with better contrast - use logarithmic scaling for more color spread
    M = np.log1p(M) / np.log1p(max_iter)  # Logarithmic for better color distribution
    
    # Create vibrant RGB image with high frequency color bands
    r = (np.sin(M * np.pi * 32) * 0.5 + 0.5) * 255
    g = (np.sin(M * np.pi * 32 + 2.094) * 0.5 + 0.5) * 255
    b = (np.sin(M * np.pi * 32 + 4.188) * 0.5 + 0.5) * 255
    
    texture = np.stack([r, g, b], axis=-1).astype(np.uint8)
    return Image.fromarray(texture)

def create_julia_texture(width=2048, height=1024, max_iter=256, c_real=-0.7, c_imag=0.27015):
    """Generate a Julia set fractal texture."""
    # Create coordinate arrays
    x = np.linspace(-1.5, 1.5, width)
    y = np.linspace(-1.0, 1.0, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    C = c_real + 1j * c_imag
    
    # Initialize iteration count
    M = np.zeros(Z.shape)
    
    # Julia iteration
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = Z[mask]**2 + C
        M[mask] = i
    
    # Smooth coloring
    mask_escaped = np.abs(Z) > 2
    M[mask_escaped] = M[mask_escaped] + 1 - np.log(np.log(np.abs(Z[mask_escaped])))/np.log(2)
    
    # Normalize with logarithmic scaling for dense colors
    M = np.log1p(M) / np.log1p(max_iter)
    
    # Vibrant color palette with high frequency
    r = (np.sin(M * np.pi * 40 + 0) * 0.5 + 0.5) * 255
    g = (np.sin(M * np.pi * 40 + 2.5) * 0.5 + 0.5) * 255
    b = (np.sin(M * np.pi * 40 + 5) * 0.5 + 0.5) * 255
    
    texture = np.stack([r, g, b], axis=-1).astype(np.uint8)
    return Image.fromarray(texture)

def create_burning_ship_texture(width=2048, height=1024, max_iter=256, zoom=1.0):
    """Generate a Burning Ship fractal texture."""
    x = np.linspace(-2.0/zoom, 1.0/zoom, width)
    y = np.linspace(-1.5/zoom, 0.5/zoom, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    Z = np.zeros_like(C)
    M = np.zeros(C.shape)
    
    # Burning Ship iteration (uses absolute values)
    for i in range(max_iter):
        mask = np.abs(Z) <= 2
        Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag))**2 + C[mask]
        M[mask] = i
    
    # Smooth coloring
    mask_escaped = np.abs(Z) > 2
    M[mask_escaped] = M[mask_escaped] + 1 - np.log(np.log(np.abs(Z[mask_escaped])))/np.log(2)
    
    # Normalize with logarithmic scaling for dense detail
    M = np.log1p(M) / np.log1p(max_iter)
    
    # Rich color palette with very high frequency
    r = (np.sin(M * np.pi * 50 + 0) * 0.5 + 0.5) * 255
    g = (np.sin(M * np.pi * 50 + 1.5) * 0.5 + 0.5) * 255
    b = (np.sin(M * np.pi * 50 + 3.5) * 0.5 + 0.5) * 255
    
    texture = np.stack([r, g, b], axis=-1).astype(np.uint8)
    return Image.fromarray(texture)

def create_fractal_texture(fractal_type='mandelbrot', width=2048, height=1024):
    """Create a fractal texture based on type."""
    if fractal_type == 'mandelbrot':
        return create_mandelbrot_texture(width, height)
    elif fractal_type == 'julia':
        return create_julia_texture(width, height)
    elif fractal_type == 'burning_ship':
        return create_burning_ship_texture(width, height)
    else:
        # Default to mandelbrot
        return create_mandelbrot_texture(width, height)

def load_images(folder='images'):
    """Load all images from the specified folder."""
    image_files = []
    extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.webp']
    
    for ext in extensions:
        image_files.extend(glob.glob(f'{folder}/{ext}'))
        image_files.extend(glob.glob(f'{folder}/{ext.upper()}'))
    
    if not image_files:
        print(f"No images found in '{folder}' folder")
        return []
    
    print(f"Found {len(image_files)} images")
    return sorted(image_files)

def extract_image_colors(images, samples_per_image=10):
    """Extract color samples from each image for background cycling."""
    colors = []
    
    for img_path in images:
        try:
            # Handle both file paths and PIL Image objects
            if isinstance(img_path, Image.Image):
                img = img_path.convert('RGB')
            else:
                img = Image.open(img_path).convert('RGB')
            img_array = np.array(img)
            
            # Sample colors from different regions of the image
            h, w = img_array.shape[:2]
            for i in range(samples_per_image):
                x = int((i / samples_per_image) * w)
                y = h // 2
                x = min(x, w - 1)
                color = img_array[y, x] / 255.0  # Normalize to 0-1
                colors.append(color)
        except Exception as e:
            print(f"Error extracting colors from {img_path}: {e}")
    
    if not colors:
        # Default color palette if no images
        colors = [
            np.array([0.1, 0.1, 0.2]),
            np.array([0.2, 0.1, 0.1]),
            np.array([0.1, 0.2, 0.1]),
        ]
    
    return colors

def create_fitted_texture(images, texture_width=2048, texture_height=1024):
    """Create a texture that fits to the natural UV mapping of the surface."""
    if not images:
        # Create a default checkerboard texture
        checker = np.indices((texture_height, texture_width)).sum(axis=0) % 2
        texture_array = (checker * 255).astype(np.uint8)
        texture_array = np.stack([texture_array] * 3, axis=-1)
        return Image.fromarray(texture_array), texture_width
    
    # For fitted mode, tile images in a grid to fill the UV space
    # Calculate grid layout
    num_images = len(images)
    cols = int(np.ceil(np.sqrt(num_images)))
    rows = int(np.ceil(num_images / cols))
    
    cell_width = texture_width // cols
    cell_height = texture_height // rows
    
    # Create the texture canvas
    texture = Image.new('RGB', (texture_width, texture_height))
    
    for idx, img_path in enumerate(images):
        try:
            img = Image.open(img_path).convert('RGB')
            
            # Calculate position in grid
            col = idx % cols
            row = idx // cols
            x = col * cell_width
            y = row * cell_height
            
            # Resize to fill the cell completely (will stretch to fit)
            img_resized = img.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
            
            texture.paste(img_resized, (x, y))
        except Exception as e:
            print(f"Error loading {img_path}: {e}")
    
    return texture, texture_width

def create_spiral_texture(images, texture_height=512, num_repeats=3):
    """Create a texture strip with images side-by-side maintaining aspect ratios."""
    if not images:
        # Create a default checkerboard texture
        width = texture_height * 4
        checker = np.indices((texture_height, width)).sum(axis=0) % 2
        texture_array = (checker * 255).astype(np.uint8)
        texture_array = np.stack([texture_array] * 3, axis=-1)
        return Image.fromarray(texture_array), width
    
    # Load and resize images maintaining aspect ratio
    processed_images = []
    for img_path in images:
        try:
            img = Image.open(img_path).convert('RGB')
            # Calculate width to maintain aspect ratio
            aspect_ratio = img.width / img.height
            new_width = int(texture_height * aspect_ratio)
            img = img.resize((new_width, texture_height), Image.Resampling.LANCZOS)
            processed_images.append(img)
        except Exception as e:
            print(f"Error loading {img_path}: {e}")
    
    if not processed_images:
        return create_spiral_texture([], texture_height, num_repeats)
    
    # Repeat images to make the spiral wrap nicely
    repeated_images = processed_images * num_repeats
    
    # Calculate total width
    total_width = sum(img.width for img in repeated_images)
    
    # Create the texture strip
    texture = Image.new('RGB', (total_width, texture_height))
    
    x_pos = 0
    for img in repeated_images:
        texture.paste(img, (x_pos, 0))
        x_pos += img.width
    
    return texture, total_width

def animate_spiral_torus(torus, texture_image, spiral_turns=3, scroll_speed=2, rotate=False, rotation_speed=1.0, bg_colors=None, fit_mode=False, twist=0.0):
    """Animate the spiral movement of textures on the torus."""
    plotter = pv.Plotter()
    mode_text = "Fitted" if fit_mode else "Spiral"
    plotter.add_text(f"{mode_text} Image Torus - Press 'q' to quit", position='upper_left')
    
    # Convert PIL image to numpy array
    texture_array = np.array(texture_image)
    texture_width = texture_array.shape[1]
    
    # Setup background colors
    if bg_colors is None:
        bg_colors = [np.array([0.1, 0.1, 0.2])]
    color_index = [0]
    color_progress = [0.0]
    
    # Set up UV coordinates
    u = torus.points[:, 0]
    v = torus.points[:, 1]
    angles = np.arctan2(v, u)
    z = torus.points[:, 2]
    z_norm = (z - z.min()) / (z.max() - z.min())
    
    if fit_mode:
        # Natural UV mapping with optional twist
        u_base = (angles / (2 * np.pi) + 0.5) % 1.0
        
        if twist != 0:
            # Add twist: rotate V coordinate based on U position
            # This creates a Möbius-like effect
            twist_angle = u_base * twist * np.pi  # twist in radians
            # Rotate the normalized z coordinate around the minor circle
            v_coords = (z_norm + twist_angle / (2 * np.pi)) % 1.0
        else:
            v_coords = z_norm
        
        u_coords = u_base
    else:
        # Spiral mapping
        u_coords = (angles / (2 * np.pi) + z_norm * spiral_turns) % 1.0
        v_coords = (z_norm * spiral_turns * 2) % 1.0
    
    torus.active_texture_coordinates = np.column_stack([u_coords, v_coords])
    
    # Create initial texture
    texture_pv = pv.Texture(texture_array)
    actor = plotter.add_mesh(torus, texture=texture_pv, smooth_shading=True)
    
    # Animation state
    offset = [0]
    rotation_angle = [0.0]
    
    def update_texture(step):
        """Scroll the texture by shifting the array."""
        if fit_mode:
            # Animate by shifting UV coordinates in fit mode
            offset[0] = (offset[0] + scroll_speed * 0.001) % 1.0
            
            # Recalculate UV coordinates with offset
            u_base = (angles / (2 * np.pi) + 0.5 + offset[0]) % 1.0
            
            if twist != 0:
                # Add twist effect
                twist_angle = u_base * twist * np.pi
                v_coords_animated = (z_norm + twist_angle / (2 * np.pi) + offset[0] * 0.3) % 1.0
            else:
                v_coords_animated = (z_norm + offset[0] * 0.3) % 1.0
            
            u_coords_animated = u_base
            torus.active_texture_coordinates = np.column_stack([u_coords_animated, v_coords_animated])
        else:
            # Circular shift of texture array in spiral mode
            offset[0] = (offset[0] + scroll_speed) % texture_width
            shifted_texture = np.roll(texture_array, -offset[0], axis=1)
            
            # Update the texture
            texture_pv.SetInputDataObject(0, pv.Texture(shifted_texture).GetInputDataObject(0, 0))
        
        # Cycle background colors
        if len(bg_colors) > 1:
            color_progress[0] += 0.005  # Smooth transition
            if color_progress[0] >= 1.0:
                color_progress[0] = 0.0
                color_index[0] = (color_index[0] + 1) % len(bg_colors)
            
            # Interpolate between current and next color
            current_color = bg_colors[color_index[0]]
            next_color = bg_colors[(color_index[0] + 1) % len(bg_colors)]
            interpolated_color = current_color * (1 - color_progress[0]) + next_color * color_progress[0]
            plotter.set_background(interpolated_color)
        
        # Add tumbling rotation if enabled
        if rotate:
            # Limit rotation speed to prevent aliasing (cap at reasonable max)
            max_rotation_per_frame = 1.5  # degrees - caps maximum to prevent aliasing
            rotation_increment = min(rotation_speed * 0.5, max_rotation_per_frame)
            rotation_angle[0] += rotation_increment
            
            # Smooth tumbling rotation
            plotter.camera.azimuth = rotation_angle[0] * 0.25
            plotter.camera.elevation = np.sin(rotation_angle[0] * 0.018) * 12
            plotter.camera.roll = rotation_angle[0] * 0.12
        
        plotter.render()
    
    # Set up animation with good frame rate
    plotter.add_timer_event(max_steps=100000, duration=33, callback=update_texture)  # ~30 FPS
    
    plotter.show()

def animate_cycling_topologies(texture_image, spiral_turns=5, scroll_speed=3, rotate=False, rotation_speed=1.0, bg_colors=None, fit_mode=False, twist=0.0):
    """Animate cycling through different topologies every 5 seconds."""
    plotter = pv.Plotter()
    
    # Convert PIL image to numpy array
    texture_array = np.array(texture_image)
    texture_width = texture_array.shape[1]
    
    # Rotation state
    rotation_angle = [0.0]
    
    # Setup background colors
    if bg_colors is None:
        bg_colors = [np.array([0.1, 0.1, 0.2])]
    color_index = [0]
    color_progress = [0.0]
    
    # Define topologies to cycle through
    topologies = [
        ('Torus', lambda: create_torus(major_radius=3, minor_radius=1, u_resolution=150, v_resolution=75)),
        ('Trefoil Knot (3,2)', lambda: create_torus_knot(p=3, q=2, major_radius=3, minor_radius=0.5, u_resolution=200, v_resolution=50)),
        ('Figure-8 Knot (4,3)', lambda: create_torus_knot(p=4, q=3, major_radius=3, minor_radius=0.5, u_resolution=250, v_resolution=50)),
        ('Cinquefoil Knot (5,2)', lambda: create_torus_knot(p=5, q=2, major_radius=3, minor_radius=0.5, u_resolution=250, v_resolution=50)),
        ("Solomon's Seal (5,3)", lambda: create_torus_knot(p=5, q=3, major_radius=3, minor_radius=0.5, u_resolution=300, v_resolution=50)),
        ('Pentafoil Knot (5,4)', lambda: create_torus_knot(p=5, q=4, major_radius=3, minor_radius=0.5, u_resolution=300, v_resolution=50)),
        ('Septafoil Knot (7,2)', lambda: create_torus_knot(p=7, q=2, major_radius=3, minor_radius=0.5, u_resolution=300, v_resolution=50)),
        ("Turk's Head (7,3)", lambda: create_torus_knot(p=7, q=3, major_radius=3, minor_radius=0.5, u_resolution=350, v_resolution=50)),
        ('Octafoil Knot (8,3)', lambda: create_torus_knot(p=8, q=3, major_radius=3, minor_radius=0.5, u_resolution=350, v_resolution=50)),
        ('Pretzel Knot (11,7)', lambda: create_torus_knot(p=11, q=7, major_radius=3, minor_radius=0.4, u_resolution=500, v_resolution=50)),
        ('Clifford Torus (4D→3D)', lambda: create_clifford_torus(u_resolution=150, v_resolution=150, scale=2.0)),
        ('4D Hypersphere Slice', lambda: create_hypersphere_slice(phi=np.pi/3, u_resolution=100, v_resolution=100, radius=2.5)),
        ('4D Torus Knot (3,2,1)', lambda: create_4d_torus_knot(p=3, q=2, r=1, u_resolution=250, v_resolution=50, scale=2.0)),
        ('Klein Bottle', lambda: create_klein_bottle(u_resolution=100, v_resolution=100, scale=2.0)),
        ('Möbius Strip', lambda: create_mobius_strip(u_resolution=100, v_resolution=20, radius=2.5, width=0.8)),
        ('Seashell', lambda: create_seashell(u_resolution=100, v_resolution=80, scale=1.2)),
        ('Spherical Harmonic (3,2)', lambda: create_spherical_harmonic(l=3, m=2, u_resolution=100, v_resolution=100, radius=2.5)),
    ]
    
    # State
    state = {
        'current_index': 0,
        'offset': 0,
        'actor': None,
        'text_actor': None,
        'frame_count': 0,
        'current_mesh': None
    }
    
    def setup_mesh(mesh):
        """Set up texture coordinates for a mesh."""
        u = mesh.points[:, 0]
        v = mesh.points[:, 1]
        angles = np.arctan2(v, u)
        z = mesh.points[:, 2]
        z_norm = (z - z.min()) / (z.max() - z.min())
        
        if fit_mode:
            # Natural UV mapping with optional twist
            u_base = (angles / (2 * np.pi) + 0.5) % 1.0
            
            if twist != 0:
                twist_angle = u_base * twist * np.pi
                v_coords = (z_norm + twist_angle / (2 * np.pi)) % 1.0
            else:
                v_coords = z_norm
            
            u_coords = u_base
        else:
            # Spiral mapping
            u_coords = (angles / (2 * np.pi) + z_norm * spiral_turns) % 1.0
            v_coords = (z_norm * spiral_turns * 2) % 1.0
        
        mesh.active_texture_coordinates = np.column_stack([u_coords, v_coords])
        return mesh
    
    def switch_topology():
        """Switch to the next topology."""
        # Remove old actor if exists
        if state['actor'] is not None:
            plotter.remove_actor(state['actor'])
        if state['text_actor'] is not None:
            plotter.remove_actor(state['text_actor'])
        
        # Create new mesh
        name, mesh_func = topologies[state['current_index']]
        print(f"Switching to: {name}")
        mesh = setup_mesh(mesh_func())
        
        # Store mesh in state for animation updates
        state['current_mesh'] = mesh
        
        # Create texture
        texture_pv = pv.Texture(texture_array)
        
        # Add mesh
        state['actor'] = plotter.add_mesh(mesh, texture=texture_pv, smooth_shading=True)
        state['text_actor'] = plotter.add_text(f"{name} - Press 'q' to quit", position='upper_left', font_size=12)
        
        # Move to next topology
        state['current_index'] = (state['current_index'] + 1) % len(topologies)
    
    def update_animation(step):
        """Update animation: scroll texture and switch topology every 5 seconds."""
        if fit_mode and state['current_mesh'] is not None:
            # Animate by shifting UV coordinates in fit mode
            state['offset'] = (state['offset'] + scroll_speed * 0.001) % 1.0
            
            # Get mesh points and recalculate UV coordinates
            mesh = state['current_mesh']
            u = mesh.points[:, 0]
            v = mesh.points[:, 1]
            angles = np.arctan2(v, u)
            z = mesh.points[:, 2]
            z_norm = (z - z.min()) / (z.max() - z.min())
            
            # Update UV coordinates with animation offset
            u_base = (angles / (2 * np.pi) + 0.5 + state['offset']) % 1.0
            
            if twist != 0:
                twist_angle = u_base * twist * np.pi
                v_coords = (z_norm + twist_angle / (2 * np.pi) + state['offset'] * 0.3) % 1.0
            else:
                v_coords = (z_norm + state['offset'] * 0.3) % 1.0
            
            u_coords = u_base
            mesh.active_texture_coordinates = np.column_stack([u_coords, v_coords])
        elif not fit_mode:
            # Scroll texture array in spiral mode
            state['offset'] = (state['offset'] + scroll_speed) % texture_width
            shifted_texture = np.roll(texture_array, -state['offset'], axis=1)
            
            # Find texture and update it
            for actor in plotter.renderer.actors.values():
                if hasattr(actor, 'GetTexture') and actor.GetTexture() is not None:
                    texture_pv = pv.Texture(shifted_texture)
                    actor.SetTexture(texture_pv)
                    break
        
        # Cycle background colors
        if len(bg_colors) > 1:
            color_progress[0] += 0.005
            if color_progress[0] >= 1.0:
                color_progress[0] = 0.0
                color_index[0] = (color_index[0] + 1) % len(bg_colors)
            
            current_color = bg_colors[color_index[0]]
            next_color = bg_colors[(color_index[0] + 1) % len(bg_colors)]
            interpolated_color = current_color * (1 - color_progress[0]) + next_color * color_progress[0]
            plotter.set_background(interpolated_color)
        
        # Add tumbling rotation if enabled
        if rotate:
            # Limit rotation speed to prevent aliasing (cap at reasonable max)
            max_rotation_per_frame = 1.5  # degrees - caps maximum to prevent aliasing
            rotation_increment = min(rotation_speed * 0.5, max_rotation_per_frame)
            rotation_angle[0] += rotation_increment
            
            # Smooth tumbling rotation
            plotter.camera.azimuth = rotation_angle[0] * 0.25
            plotter.camera.elevation = np.sin(rotation_angle[0] * 0.018) * 12
            plotter.camera.roll = rotation_angle[0] * 0.12
        
        # Switch topology every 5 seconds (150 frames at 30 FPS)
        state['frame_count'] += 1
        if state['frame_count'] % 150 == 0:
            switch_topology()
        
        plotter.render()
    
    # Initialize with first topology
    switch_topology()
    
    # Set up animation
    plotter.add_timer_event(max_steps=100000, duration=33, callback=update_animation)
    
    plotter.show()

def main():
    """Main function to create and display the spiral torus."""
    parser = argparse.ArgumentParser(description='3D Spiral Image Torus/Knot Visualization')
    parser.add_argument('--knot', type=str, default=None, 
                        choices=['torus', 'trefoil', 'figure8', 'cinquefoil', 'pentafoil', 'septafoil', 'octafoil', 'solomon', 'turkshead', 'pretzel', 'clifford', 'hypersphere', '4dknot', 'custom'],
                        help='Type of topology: torus, trefoil (3,2), figure8 (4,3), cinquefoil (5,2), pentafoil (5,4), septafoil (7,2), octafoil (8,3), solomon (5,3), turkshead (7,3), pretzel (11,7), clifford (4D torus), hypersphere (4D sphere slice), 4dknot (4D torus knot), or custom. If not specified, cycles through all topologies.')
    parser.add_argument('--p', type=int, default=3,
                        help='P parameter for custom torus knot (default: 3)')
    parser.add_argument('--q', type=int, default=2,
                        help='Q parameter for custom torus knot (default: 2)')
    parser.add_argument('--r', type=int, default=1,
                        help='R parameter for 4D torus knot - controls 4th dimension oscillation (default: 1)')
    parser.add_argument('--spiral-turns', type=int, default=5,
                        help='Number of spiral turns (default: 5)')
    parser.add_argument('--scroll-speed', type=int, default=3,
                        help='Texture scroll speed in pixels (default: 3)')
    parser.add_argument('--rotate', action='store_true',
                        help='Enable tumbling rotation')
    parser.add_argument('--rotation-speed', type=float, default=1.0,
                        help='Rotation speed multiplier (default: 1.0)')
    parser.add_argument('--fit', action='store_true',
                        help='Fit images to surface without spiral distortion (natural UV mapping)')
    parser.add_argument('--twist', type=float, default=0.0,
                        help='Number of twists (half-turns) around the torus (default: 0, try 1.0 for Möbius-like effect)')
    parser.add_argument('--fractal', type=str, default=None,
                        choices=['mandelbrot', 'julia', 'burning_ship'],
                        help='Use fractal texture instead of images: mandelbrot, julia, or burning_ship')
    
    args = parser.parse_args()
    
    # Create images folder if it doesn't exist
    Path('images').mkdir(exist_ok=True)
    
    # Load images or create fractal
    if args.fractal:
        print(f"Creating {args.fractal} fractal texture...")
        fractal_image = create_fractal_texture(args.fractal, width=2048, height=1024)
        image_files = []
        
        # Use fractal for texture
        if args.fit:
            texture = fractal_image
            texture_width = texture.width
            print(f"Fitted fractal texture size: {texture_width}x{texture.height}")
        else:
            texture = fractal_image
            texture_width = texture.width
            print(f"Fractal texture size: {texture_width}x{texture.height}")
        
        # Use fractal colors for background
        bg_colors = extract_image_colors([fractal_image], samples_per_image=20)
    else:
        image_files = load_images('images')
        
        if not image_files:
            print("Please add some images to the 'images' folder")
            print("Continuing with default checkerboard pattern...")
        
        # Create texture based on mode
        print("Creating texture...")
        if args.fit:
            texture, texture_width = create_fitted_texture(image_files, texture_width=2048, texture_height=1024)
            print(f"Fitted texture size: {texture_width}x{texture.height}")
        else:
            texture, texture_width = create_spiral_texture(image_files, texture_height=512, num_repeats=5)
            print(f"Spiral texture size: {texture_width}x{texture.height}")
        
        # Extract colors from images for background cycling
        bg_colors = extract_image_colors(image_files, samples_per_image=10)
    
    print(f"Extracted {len(bg_colors)} background colors")
    
    # If no knot specified, cycle through all topologies
    if args.knot is None:
        mode_msg = "fitted" if args.fit else "spiral"
        print(f"Starting animation with cycling topologies ({mode_msg} mode, every 5 seconds)... Press 'q' to quit")
        animate_cycling_topologies(texture, spiral_turns=args.spiral_turns, scroll_speed=args.scroll_speed, 
                                   rotate=args.rotate, rotation_speed=args.rotation_speed, bg_colors=bg_colors,
                                   fit_mode=args.fit, twist=args.twist)
        return
    
    # Create mesh based on selected topology
    if args.knot == 'torus':
        print("Creating torus...")
        mesh = create_torus(major_radius=3, minor_radius=1, u_resolution=150, v_resolution=75)
    elif args.knot == 'trefoil':
        print("Creating trefoil knot (3,2)...")
        mesh = create_torus_knot(p=3, q=2, major_radius=3, minor_radius=0.5, u_resolution=200, v_resolution=50)
    elif args.knot == 'figure8':
        print("Creating figure-8 knot (4,3)...")
        mesh = create_torus_knot(p=4, q=3, major_radius=3, minor_radius=0.5, u_resolution=250, v_resolution=50)
    elif args.knot == 'cinquefoil':
        print("Creating cinquefoil knot (5,2)...")
        mesh = create_torus_knot(p=5, q=2, major_radius=3, minor_radius=0.5, u_resolution=250, v_resolution=50)
    elif args.knot == 'pentafoil':
        print("Creating pentafoil knot (5,4)...")
        mesh = create_torus_knot(p=5, q=4, major_radius=3, minor_radius=0.5, u_resolution=300, v_resolution=50)
    elif args.knot == 'septafoil':
        print("Creating septafoil knot (7,2)...")
        mesh = create_torus_knot(p=7, q=2, major_radius=3, minor_radius=0.5, u_resolution=300, v_resolution=50)
    elif args.knot == 'octafoil':
        print("Creating octafoil knot (8,3)...")
        mesh = create_torus_knot(p=8, q=3, major_radius=3, minor_radius=0.5, u_resolution=350, v_resolution=50)
    elif args.knot == 'solomon':
        print("Creating Solomon's seal knot (5,3)...")
        mesh = create_torus_knot(p=5, q=3, major_radius=3, minor_radius=0.5, u_resolution=300, v_resolution=50)
    elif args.knot == 'turkshead':
        print("Creating Turk's head knot (7,3)...")
        mesh = create_torus_knot(p=7, q=3, major_radius=3, minor_radius=0.5, u_resolution=350, v_resolution=50)
    elif args.knot == 'pretzel':
        print("Creating pretzel knot (11,7)...")
        mesh = create_torus_knot(p=11, q=7, major_radius=3, minor_radius=0.4, u_resolution=500, v_resolution=50)
    elif args.knot == 'clifford':
        print("Creating Clifford torus (4D torus projected to 3D)...")
        mesh = create_clifford_torus(u_resolution=150, v_resolution=150, scale=2.0)
    elif args.knot == 'hypersphere':
        print("Creating 4D hypersphere slice...")
        mesh = create_hypersphere_slice(phi=np.pi/3, u_resolution=100, v_resolution=100, radius=2.5)
    elif args.knot == '4dknot':
        print(f"Creating 4D torus knot ({args.p},{args.q},{args.r})...")
        mesh = create_4d_torus_knot(p=args.p, q=args.q, r=args.r, u_resolution=250, v_resolution=50, scale=2.0)
    elif args.knot == 'custom':
        print(f"Creating custom torus knot ({args.p},{args.q})...")
        mesh = create_torus_knot(p=args.p, q=args.q, major_radius=3, minor_radius=0.5, u_resolution=250, v_resolution=50)
    
    # Animate
    mode_msg = "fitted" if args.fit else "spiral"
    print(f"Starting animation ({mode_msg} mode)... Press 'q' to quit")
    animate_spiral_torus(mesh, texture, spiral_turns=args.spiral_turns, scroll_speed=args.scroll_speed,
                        rotate=args.rotate, rotation_speed=args.rotation_speed, bg_colors=bg_colors,
                        fit_mode=args.fit, twist=args.twist)

if __name__ == '__main__':
    main()
