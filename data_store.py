import numpy as np
import os
import sys
from pathlib import Path

def getrrf():
    bpol_local = 0.5*(com.bpol[:,:,2] + com.bpol[:,:,4])
    bphi_local = 0.5*(com.bphi[:,:,2] + com.bphi[:,:,4])
    btot_local = np.sqrt(bpol_local**2+bphi_local**2)
    return bpol_local/btot_local

def PionParallelKE():
    """(nx+2, ny+2) array of power [Watts] in East direction of ion parallel kinetic energy, usually only significant at plates."""
    return 0.5*bbb.mi[0]*bbb.up[:,:,0]**2*bbb.fnix[:,:,0]

def PsurfInner():
    """(ny+2) array of total power [Watts] in West direction along inner divertor surface"""
    bbb.pradpltwl()
    plateIndex = 0
    xsign = -1 # poloidal fluxes are measured on east face of cell
    bbb.fetx = bbb.feex+bbb.feix
    psurfi = xsign*bbb.fetx[0,:] \
             +xsign*bbb.fnix[0,:,0]*bbb.ebind*bbb.ev \
#             +xsign*PionParallelKE()[0,:] \
#             +bbb.pwr_plth[:,plateIndex]*com.sxnp[0,:] \
#             +bbb.pwr_pltz[:,plateIndex]*com.sxnp[0,:]
    return psurfi

def PsurfOuter():
    """(ny+2) array of total power [Watts] in East direction along outer divertor surface"""
    bbb.pradpltwl()
    plateIndex = 1
    xsign = 1
    bbb.fetx = bbb.feex+bbb.feix
    psurfo = xsign*bbb.fetx[com.nx,:] \
             +xsign*bbb.fnix[com.nx,:,0]*bbb.ebind*bbb.ev \
#             +xsign*PionParallelKE()[com.nx,:] \
#             +bbb.pwr_plth[:,plateIndex]*com.sxnp[com.nx,:] \
#             +bbb.pwr_pltz[:,plateIndex]*com.sxnp[com.nx,:]
    return psurfo

def qsurfparInner():
    '''Total power to surface projected in parallel direction'''
    rrf = getrrf()
    psurf = PsurfInner()
    ix = 0
    return psurf/com.sx[ix,:]/getrrf()[ix,:]


def qsurfparOuter():
    '''Total power to surface projected in parallel direction'''
    rrf = getrrf()
    psurf = PsurfOuter()
    ix = com.nx
    return psurf/com.sx[ix,:]/rrf[ix,:]

def data_store(v):
    test_path = str(v)
    os.makedirs(test_path, exist_ok=True) # Automatically create directory

    hdf5_file_path = os.path.join(test_path, "uedge_data.h5") # HDF5 file path

    gamma_in = -1.0 * bbb.fnix[0,:,0] / com.sxnp[0,:]
    gamma_out = 1.0 * bbb.fnix[com.nx,:,0] / com.sxnp[com.nx,:]
    gammapar_in = bbb.fnix[0,:,0]/com.sx[0,:]/getrrf()[0,:]
    gammapar_out = bbb.fnix[com.nx,:,0]/com.sx[com.nx,:]/getrrf()[com.nx,:]
    qsurf_in = PsurfInner()/com.sxnp[0,:]/1e6
    qsurf_out = PsurfOuter()/com.sxnp[com.nx,:]/1e6
    qpar_in = qsurfparInner()/1e6
    qpar_out = qsurfparOuter()/1e6
    rrf = getrrf()

    npy_data = {
        "yylb": com.yylb,
        "yyrb": com.yyrb,
        "yyc": com.yyc,
        "kyi_use": bbb.kyi_use,
        "kye_use": bbb.kye_use,
        "dif_use": bbb.dif_use,
        "pradhyd": bbb.pradhyd,
        "prad": bbb.prad,
        "ng": bbb.ng,
        "ni": bbb.ni,
        "ne": bbb.ne,
        "te": bbb.te/bbb.ev,
        "ti": bbb.ti/bbb.ev,
        "sxnp": com.sxnp,
        "sx": com.sx,
        "fnix": bbb.fnix,
        "rrf": rrf,
        "gamma_in": gamma_in,
        "gamma_out": gamma_out,
        "gammapar_in": gammapar_in,
        "gammapar_out": gammapar_out,
        "qsurf_in": qsurf_in,
        "qsurf_out": qsurf_out,
        "qpar_in": qpar_in,
        "qpar_out": qpar_out,
        "nx": com.nx,
        "ny": com.ny,
        "ixmp": bbb.ixmp,
        "iysptrx": com.iysptrx,
        "zm": com.zm,
        "rm": com.rm,
        "ex": bbb.ex,
        "ey": bbb.ey,
        

    }

    txt_data = {
            "uedge_te_ot.txt": (bbb.te[com.nx, :] / bbb.ev, f"Electron temperature (eV) <ix = {com.nx}>"),
            "uedge_te_it.txt": (bbb.te[1, :] / bbb.ev, f"Electron temperature (eV) <ix = 1>"),
            "uedge_ne_ot.txt": (bbb.ne[com.nx,:], f"Electron density $\m^{-3}\$ <ix = {com.nx}>"),
            "uedge_ne_it.txt": (bbb.ne[1,:], f"Electron density $\m^{-3}\$ <ix = 1>"),
            "uedge_gamma_it.txt": (gamma_in, f"Gamma current ($m^(-2)s^(-1)$)  <ix = 1>"),
            "uedge_gamma_ot.txt": (gamma_out, f"Gamma current ($m^(-2)s^(-1)$)  <ix = {com.nx}>"),
            "uedge_Q_it.txt": (qsurf_in, f"Q current($MW/m^2$)  <ix = 1>"), 
            "uedge_Q_ot.txt": (qsurf_out, f"Q current($MW/m^2$)  <ix = {com.nx}>"),
            "uedge_Qpar_it.txt": (qpar_in, f"Qpar current($MW/m^2$)  <ix = 1>"),
            "uedge_Qpar_ot.txt": (qpar_out, f"Qpar current($MW/m^2$)  <ix = {com.nx}>"),

    }


    # save '.txt' file
    for filename, (data, header) in txt_data.items():
        file_path = os.path.join(test_path, filename)
        np.savetxt(file_path, data, delimiter="\n", header=header)

    # save '.h5' file
    with h5py.File(hdf5_file_path, "w") as hdf5_file:
        for key, value in npy_data.items():
            hdf5_file.create_dataset(key, data=value)  # save HDF5

    print(f"Data saved in {test_path}, HDF5 file: {hdf5_file_path}")

