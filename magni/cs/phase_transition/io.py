"""
..
    Copyright (c) 2014-2016, Magni developers.
    All rights reserved.
    See LICENSE.rst for further information.

Module providing input/output functionality for stored phase transitions.

Routine listings
----------------
load_phase_transition(path, label='default')
    Load the coordinates of a phase transition from a HDF5 file.

"""

from __future__ import division

import numpy as np

from magni.utils.multiprocessing import File as _File
from magni.utils.validation import decorate_validation as _decorate_validation
from magni.utils.validation import validate_generic as _generic
from magni.utils.validation import validate_numeric as _numeric


def load_phase_transition(path, label='default', delta=None):
    """
    Load the coordinates of a phase transition from a HDF5 file.

    This function is used to load the phase transition from the output file
    generated by `magni.cs.phase_transition.determine`.

    Parameters
    ----------
    path : str
        The path of the HDF5 file where the phase transition is stored.
    label : str
        The label assigned to the phase transition (the default is 'default').
    delta : ndarray
        The undersampling ratio values to use (the default is None which
        implies that a uniform spacing of values in the interval (0,1] is
        assumed.)

    Returns
    -------
    delta : ndarray
        The delta values of the phase transition points.
    rho : ndarray
        The rho values of the phase transition points.

    See Also
    --------
    magni.cs.phase_transition.determine : Phase transition determination.
    magni.cs.phase_transition.plotting : Phase transition plotting.

    Examples
    --------
    An example of how to use this function is provided in the `examples` folder
    in the `cs-phase_transition.ipynb` ipython notebook file.

    """

    @_decorate_validation
    def validate_input():
        _generic('path', 'string')
        _generic('label', 'string')
        _numeric('delta', ('floating', 'integer'), range_='[0;1]', shape=(-1,),
                 ignore_none=True)

    @_decorate_validation
    def validate_output():
        _numeric('rho', ('floating', 'integer'), range_='[0;1]', shape=(-1,))
        _numeric('delta', ('floating', 'integer'), range_='[0;1]',
                 shape=rho.shape)

    validate_input()

    with _File(path, 'r') as f:
        rho = f.get_node('/' + label + '/phase_transition')[:]

    if delta is None:
        delta = np.linspace(0, 1, len(rho) + 1)[1:]

    validate_output()

    return (delta, rho)
