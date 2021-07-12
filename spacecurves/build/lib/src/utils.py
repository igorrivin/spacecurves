import numpy
import cmath

def rank_simple(vector ):
    """given a list, return the ranks of its elements when sorted."""
    return sorted(range(len(vector)), key=vector.__getitem__)

def rank_two(v0, r, s):
    """We have two intersecting oriented segments (v0->v1) and (r->s). We want to order them in 
    counterclockwise order, with v0 being number 0, so v1 is number 2. It remains to check which of r and s comes first.
    this is what this function does using simple complex number geometry."""
    v0c = complex(v0[0], v0[1])
    rc = complex(r[0], r[1])
    sc = complex(s[0], s[1])
    pr = cmath.phase(rc/v0c)
    if pr > 0:
        return [1, 3]
    return [3, 1]

def rank_vecs(v0, r, s, t):
    """ Same as rank_two, but the four points are not assumed to be the endpoints of two intersecting segments. We order 
    them counter-clockwise around the origin."""
    v0c = complex(v0[0], v0[1])
    rc = complex(r[0], r[1])
    sc = complex(s[0], s[1])
    tc = complex(t[0], t[1])
    pr = cmath.phase(rc/v0c)
    ps = cmath.phase(sc/v0c)
    pt = cmath.phase(tc/v0c)
    if pr < 0:
        pr = 2 * np.pi + pr
    if ps < 0:
        ps = 2 * np.pi + ps
    if pt < 0:
        pt = 2 * np.pi + pt
    theranks0 = rank_simple([pr, ps, pt])
    return [1+x for x in theranks0]



def randfunc(stepsize, ll, decayfunc):
    """ We generate a PL approximation (with step size stepsize) to a random function given by a fourier series
    whose coefficients are random gaussians, whose standard deviation decays as decayfunc."""
    sigmas = np.array(list(map(decayfunc, range(ll))))
    sincoeffs0 = np.random.randn(ll)
    sincoeffs = sincoeffs0 * sigmas
    coscoeffs0 = np.random.randn(ll)
    coscoeffs = coscoeffs0 * sigmas
    def rf(x):
        sinpoly = 0
        cospoly = 0
        for i in range(ll):
            sinpoly += sincoeffs[i] * np.sin(i * x)
            cospoly += coscoeffs[i] * np.cos(i * x)
        return sinpoly + cospoly
    return np.array(list(map(rf, np.arange(0, 2*np.pi, stepsize))))

def rknot(stepnum, ll, decayfunc):
    """ A knot is a map from S1 to R3, so just a triple of periodic functions."""
    xvals = randfunc(stepnum, ll, decayfunc)
    yvals = randfunc(stepnum, ll, decayfunc)
    zvals = randfunc(stepnum, ll, decayfunc)
    return np.vstack((xvals, yvals, zvals)).T
