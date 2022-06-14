import numpy as np
import glob
from Util import local_max, lin_gaussian
from dataclasses import dataclass
from scipy.optimize import curve_fit


@dataclass
class Fit:
    charge: np.array
    spectra: np.array
    pOpt: np.array
    f: callable


def PerformFits(charge, spectra, rough_coef, Files, cut_off=10, charge_window=10,
                **kwargs):
    '''performs fit across the specified peaks in the contained in the Files
    specified. LitEnFiles should have a header of one and use ',' as a delimiter.
    The charge and spectra should be given.
    rough coeff should be given as a tuple of polynomial coefficients in
    order of smallest order coeff to largest order coeff. The smallest acceptable
    peak can be set with cut_off, and the range of the fit is set with charge_window'''
    fits = []
    # use the rough calibration to convert to energy
    rough_fit = np.polynomial.Polynomial(rough_coef)
    # assumes array is energy is linear with index otherwise have to search for
    # energy everytime
    Charge_to_ind = len(charge)/(charge[-1]-charge[0])
    # load in the literature energies from files of proper format
    LitEn = []
    for File in Files:
        LitEn += list(np.genfromtxt(File, skip_header=1, usecols=(0),
                                    delimiter=','))
    results = []
    for peak in LitEn:
        idx = rough_fit(peak)*Charge_to_ind  # change from energy to index
        # take a slice using the rough calibration as a guide
        spectra_slice = spectra[int(idx-charge_window*Charge_to_ind):int(idx+10*Charge_to_ind)]
        bin_slice = charge[int(idx-charge_window*Charge_to_ind):int(idx+10*Charge_to_ind)]
        # find the local maximums on the slice
        maxes, indexes = local_max(spectra_slice, N=len(spectra_slice)//4)
        # remove any obviously due to noise
        bool_array = np.greater(maxes, np.mean(spectra_slice))
        maxes = maxes[bool_array]
        indexes = indexes[bool_array]
        # only slices that contain 1 peak (for now)
        if len(maxes) == 1:
            # make initial guesses about the fit
            avg = np.mean(spectra_slice)
            p0 = [maxes[0]-avg, bin_slice[indexes[0]], 2, 0, avg]

            # fit
            try:
                out = curve_fit(lin_gaussian, bin_slice, spectra_slice,
                                p0=p0,
                                full_output=True, **kwargs)
            except:
                print(f"error fitting lit. energy peak {peak}")
                continue
            # fit parameters
            pOpt = out[0]
            # check if the fit converged and if it is reasonable
            if out[-1] in [1, 2, 3, 4] and abs(rough_fit(peak)-pOpt[1]) < 5 and
            pOpt[0] > cut_off:
                # return the results as well the fits
                results.append((peak, pOpt[1]))
                fits.append(Fit(bin_slice, spectra_slice, pOpt, lin_gaussian))
    return np.array(results), fits
