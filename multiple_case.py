import glob
import os
import numpy as np
import h5py

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerTuple
from matplotlib import rc
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.cm
import copy
import numpy as np
import matplotlib as mpl
import matplotlib.colors as colors

config = {'font.family': 'Times New Roman', 'mathtext.fontset': 'stix', 'font.size': 20,
          'font.weight':'bold','legend.frameon':False,'figure.subplot.wspace':0,
          'legend.loc':'best','legend.fontsize':20,'figure.subplot.hspace':0,
          'ytick.minor.visible':True,'xtick.minor.visible':True,
          'xtick.minor.top':True,'xtick.minor.bottom':True,
          'ytick.minor.left':True,'ytick.minor.right':True,
          'ytick.major.left':True,'ytick.major.right':True,
          'xtick.major.top':True,'xtick.major.bottom':True,
          'ytick.labelright':False,'ytick.labelleft':True,
          'xtick.labelbottom':True,'xtick.labeltop':False,
          'xtick.bottom':True,'xtick.top':True,
          'ytick.left':True,'ytick.right':True,
          'xtick.labelsize':20,'ytick.labelsize':20,
          'figure.autolayout':True,'xtick.direction':'in','ytick.direction':'in',
          'figure.figsize':(10, 10),'axes.formatter.use_mathtext':True,
          'axes.facecolor':'None','axes.formatter.use_mathtext':True,
          'axes.formatter.limits':(-3,3)

          }
rcParams.update(config)

class UEDGECase:
    def __init__(self, file_path):
        """ Initialize UEDGE data class and read HDF5 file """
        self.file_path = file_path
        self.data = {}
        self._load_data()  # 加载数据
    
    def _load_data(self):
        """ Read data from HDF5 file """
        with h5py.File(self.file_path, "r") as f:
            self.data["ne"] = f["ne"][:]
            self.data["yyc"] = f["yyc"][:]
            self.data["yyrb"] = f["yyrb"][:]
            self.data["yylb"] = f["yylb"][:]
            self.data["te"] = f["te"][:]
            self.data["gamma_out"] = f["gamma_out"][:]
            self.data["gammapar_out"] = f["gammapar_out"][:]
            self.data["qsurf_out"] = f["qsurf_out"][:]
            self.data["qpar_out"] = f["qpar_out"][:]
            self.data["nx"] = f["nx"][()]
            self.data["ny"] = f["ny"][()]
            self.data["iysptrx"] = f["iysptrx"][()]
            self.data["ixmp"] = f["ixmp"][()]
            self.data["rm"] = f["rm"][()]
            self.data["zm"] = f["zm"][()]
    
    def get(self, key):
        """ get data """
        return self.data.get(key, None)

    def __repr__(self):
        return f"UEDGECase({self.file_path}) with keys: {list(self.data.keys())}"

#fig2 = plt.figure(figsize=(16,12))

fig1,ax1 = plt.subplots(2, 2,figsize=(16,12))

cases = [
        UEDGECase("/home/zhangmingzhou/uedge/uedge-8.1.1/example/CFEDR/nodrift/test/test/uedge_data.h5"),
        UEDGECase("uedge_data.h5"),
        UEDGECase("/home/zhangmingzhou/uedge/uedge-8.1.1/example/CFEDR/b0/div/af0.02/p125/test/uedge_data.h5"),
]

label  = ['w/o drifts', 'forward','reversed']

#for case in cases:
for i, case in enumerate(cases):
    yyrb = case.get("yyrb")
    nx = case.get("nx")

    ne = case.get("ne")
    ax1[0,0].plot(yyrb, ne[nx, :],label = label[i])

    te = case.get("te")
    ax1[0,1].plot(yyrb,te[nx,:])

    gamma_out = case.get("gammapar_out")
    ax1[1,0].plot(yyrb[1:-1],gamma_out[1:-1]*1.6e-19)

    qsurf_out = case.get("qsurf_out")
    ax1[1,1].plot(yyrb[1:-1],qsurf_out[1:-1])

ax1[0, 0].legend()
ax1[0,0].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')
ax1[0,1].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')
ax1[1,0].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')
ax1[1,1].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')

ax1[0,0].set_ylabel(r'$\mathrm{ne} \mathrm{(m^{-3})}$')
ax1[0,1].set_ylabel(r'$\mathrm{Te} \mathrm{(eV)}$')
ax1[1,0].set_ylabel(r'$\mathrm{j_{sat}} \mathrm{(A/m^{2})}$')
ax1[1,1].set_ylabel(r'$\mathrm{q_{dep}} \mathrm{(MW/m^{2})}$')

fig2,ax2 = plt.subplots(2, 2,figsize=(16,12))

for case in cases:
    yyrb = case.get("yyrb")
    nx = case.get("nx")

    gammapar_out = case.get("gammapar_out")
    ax2[0,0].plot(yyrb[1:-1], gammapar_out[1:-1]*1.6e-19)

    gamma_out = case.get("gamma_out")
    ax2[0,1].plot(yyrb[1:-1],gamma_out[1:-1]*1.6e-19)

    qpar_out = case.get("qpar_out")
    ax2[1,0].plot(yyrb[1:-1],qpar_out[1:-1])

    qsurf_out = case.get("qsurf_out")
    ax2[1,1].plot(yyrb[1:-1],qsurf_out[1:-1])

ax2[0,0].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')
ax2[0,1].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')
ax2[1,0].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')
ax2[1,1].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')

ax2[0,0].set_ylabel(r'$\mathrm{j_{sat}} \mathrm{(A/m^{2})}$')
ax2[0,1].set_ylabel(r'$\mathrm{\Gamma} \mathrm{(A/m^{2})}$')
ax2[1,0].set_ylabel(r'$\mathrm{q_{\parallel}} \mathrm{(MW/m^{2})}$')
ax2[1,1].set_ylabel(r'$\mathrm{q_{dep}} \mathrm{(MW/m^{2})}$')

fig3,ax3 = plt.subplots(2, 2,figsize=(16,12))

#for case in cases:
for i, case in enumerate(cases):
    yyc = case.get("yyc")
    nx = case.get("nx")
    ny = case.get("ny")
    iysptrx = case.get("iysptrx")
    ixmp = case.get("ixmp")

    ne = case.get("ne")
    ax3[0,0].plot(yyc[0:ny+1], ne[ixmp,0:ny+1],label = label[i])

    te = case.get("te")
    ax3[0,1].plot(yyc[0:ny+1],te[ixmp,0:ny+1])

    ax3[1,0].plot(yyc[iysptrx+1:-1],ne[ixmp,iysptrx+1:-1])

    ax3[1,1].plot(yyc[iysptrx+1:-1],te[ixmp,iysptrx+1:-1])
ax3[0,0].legend()
ax3[0,0].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')
ax3[0,1].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')
ax3[1,0].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')
ax3[1,1].set_xlabel(r'$\mathrm{r-r_{sep} \: at \: OMP} \mathrm{(m)}$')

ax3[0,0].set_ylabel(r'$\mathrm{ne} \mathrm{(m^{-3})}$')
ax3[0,1].set_ylabel(r'$\mathrm{Te} \mathrm{(eV)}$')
ax3[1,0].set_ylabel(r'$\mathrm{ne} \mathrm{(m^{-3})}$')
ax3[1,1].set_ylabel(r'$\mathrm{Te} \mathrm{(eV)}$')

fig4,ax4 = plt.subplots(1, 3,figsize=(16,12))

patches = []
ixs=1
ixe=nx+1
iys=1
iye=ny+1
cmap=matplotlib.cm.jet
rm = case.get("rm")
zm = case.get("zm")
for iy in np.arange(iys,iye):
    for ix in np.arange(ixs,ixe):
        rcol=rm[ix,iy,[1,2,4,3]]
        zcol=zm[ix,iy,[1,2,4,3]]
        rcol.shape=(4,1)
        zcol.shape=(4,1)
        polygon = Polygon(np.column_stack((rcol,zcol)))
        patches.append(polygon)
vals=np.zeros((ixe-ixs)*(iye-iys))
for i, case in enumerate(cases):
    ne = case.get("ne")

    for iy in np.arange(iys,iye):
        for ix in np.arange(ixs,ixe):
            k=(ix-ixs)+(ixe-ixs)*(iy-iys)
            vals[k] = ne[ix,iy]
    p = PatchCollection(patches,cmap=cmap, norm = colors.LogNorm(vmin=1e18, vmax=5e21))
    p.set_array(np.array(vals))
    ax4[i].add_collection(p)
    ax4[i].autoscale_view()
    ax4[i].figure.colorbar(p,ax=ax4[i])

fig5,ax5 = plt.subplots(1, 3,figsize=(16,12))
for i, case in enumerate(cases):
    ne = case.get("te")

    for iy in np.arange(iys,iye):
        for ix in np.arange(ixs,ixe):
            k=(ix-ixs)+(ixe-ixs)*(iy-iys)
            vals[k] = ne[ix,iy]
    p = PatchCollection(patches,cmap=cmap, norm = colors.LogNorm(vmin=1, vmax=80))
    p.set_array(np.array(vals))
    ax5[i].add_collection(p)
    ax5[i].autoscale_view()
    ax5[i].figure.colorbar(p,ax=ax5[i])




plt.show()
