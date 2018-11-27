from collections import namedtuple
import numpy as np


RFresult = namedtuple('RFresult', ['center', 'error', 'grid', 'grid_errors'])


def check_rf(outline, npoints):
    """check_rf(outline, npoints)

    Check if an object outline can be represented as a radial frequency pattern

    Arguments:
        outline:
            Either a sequence of complex numbers indicating the locations of
            the different outline points, or a sequence of 2d coordinate values
        npoints:
            number of grid points to (maximally) search in each direction

    Returns:
        RFresult object which contains the results of the analysis.
    """
    outline = safe_outline(outline)
    grid = complexgrid(outline, npoints)
    grid = inner_grid_points(grid, outline)
    errors = search_grid(outline, grid)
    idx = np.argmin(errors)
    center = grid[idx]
    return RFresult(center, errors[idx], grid, errors)


def is_inner(z, S):
    angles = np.angle(S - z)
    turning_angles = np.diff(np.concatenate((angles, [angles[0]])))
    return abs(np.sum(np.angle(np.exp(1j*turning_angles)))) > np.pi


def complexgrid(outline, npoints=10):
    lo = min(outline.real.min(), outline.imag.min())
    up = max(outline.real.max(), outline.imag.max())
    x, y = np.mgrid[lo:up:1j*npoints, lo:up:1j*npoints]
    z = x + 1j*y
    return z.ravel()


def inner_grid_points(grid, outline):
    return np.array([z for z in grid if is_inner(z, outline)])


def rfdiff(S):
    r = abs(S)
    phi = np.unwrap(np.angle(S))
    i = np.argsort(phi)
    orig = S[i]
    rf = r*np.exp(1j*phi[i])
    return np.max(abs(orig - rf)**2)


def search_grid(outline, grid):
    return np.array([rfdiff(outline - z) for z in grid])


def safe_outline(outline):
    outline = np.asarray(outline)
    if len(outline.shape) == 1 and outline.dtype == 'D':
        return outline
    elif len(outline.shape) == 2:
        if outline.shape[0] == 2:
            return outline[0] + 1j*outline[1]
        elif outline.shape[1] == 2:
            return outline[:, 0] + 1j*outline[:, 1]
    raise ValueError('Content of parameter "outline" can not be interpreted')


def pretty(result):
    center = result.center
    error = np.log10(result.error)
    npoints = len(result.grid)
    return ('Analyzed {} points inside the outline\n'
            '  Best center: ({}, {})\n'
            '  Log10 error at center: {:.3f}\n').format(npoints,
                                                        center.real,
                                                        center.imag,
                                                        error)


def visualize(outline, result):
    outline = safe_outline(outline)
    closed = np.concatenate([outline, [outline[0]]])
    pl.scatter(result.grid.real, result.grid.imag,
               c=np.log10(result.grid_errors),
               cmap=pl.cm.gray_r,
               vmin=-3,
               vmax=2)
    pl.plot(closed.real, closed.imag)
    pl.plot([result.center.real], [result.center.imag], 's')
    pl.colorbar()
    pl.axis('equal')
    pl.setp(pl.gca(), xticks=(), yticks=())


if __name__ == '__main__':
    from docopt import docopt
    import pylab as pl
    args = docopt("""
Usage:
    check_rf.py [options] <FILENAME>

Check if a shape outline read from a file can be represented as a radial
frequency pattern. The file is basically a csv file. It contains the shape's
coordinates in the following way:
<x1>,<y1>
<x2>,<y2>
<x3>,<y3>
...
<xn>,<yn>

Options:
    -g <GRIDSIZE>, --gridsize=<GRIDSIZE>
        Number of grid points (in each direction) to scan. [Default: 10]
    -v, --visualize
        Visualize the results of the analysis.
""")
    with open(args['<FILENAME>']) as f:
        outline = np.array([[float(x) for x in line.split(',')]
                            for line in f])
    result = check_rf(outline, int(args['--gridsize']))
    print(pretty(result))

    if args['--visualize']:
        visualize(outline, result)
        pl.show()
