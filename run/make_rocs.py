#! /bin/env python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import root_numpy
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve
from scipy.interpolate import InterpolatedUnivariateSpline
from pdb import set_trace
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument('infile')
parser.add_argument('outdir')
parser.add_argument("--bootstrap", action='store_true')
args = parser.parse_args()

if not os.path.isdir(args.outdir):
   os.makedirs(args.outdir)

def bootstrapped_roc(true, pred, n_boots=200):
   'from https://stackoverflow.com/questions/19124239/scikit-learn-roc-curve-with-confidence-intervals'
   y_true = true.as_matrix()
   y_pred = pred.as_matrix()
   newx = np.logspace(-4, 0, 80)
   tprs = pd.DataFrame()
   for iboot in range(n_boots):
      idxs = np.random.random_integers(0, y_pred.shape[0] - 1, y_pred.shape[0])
      fakes, effs, _ = roc_curve(y_true[idxs], y_pred[idxs])
      #remove duplicates in the ROC
      coords = pd.DataFrame()
      coords['fpr'] = fakes
      coords['tpr'] = effs
      clean = coords.drop_duplicates(subset=['fpr'])
      #fit with a spline
      spline = InterpolatedUnivariateSpline(clean.fpr, clean.tpr,k=1)
      #make uniform spacing to allow averaging
      tprs[iboot] = spline(newx)
   return newx, tprs.mean(axis=1), tprs.std(axis=1)

data = pd.DataFrame(
   root_numpy.root2array(
      args.infile,
      #'TTBar_RelVal.root', #'TTBar.root', 
      'bTaggingExerciseIIAK4Jets/tree')
   )
data = data[(data.jet_pt > 30) & (np.abs(data.jet_eta) < 2.4)]

HEM_15_16 = data[(data.jet_eta < -1.5) & \
                    (data.jet_eta > -2.5) & \
                    (data.jet_phi < -0.6) & \
                    (data.jet_phi > -1.8)]

safe_data = data[(data.jet_eta > 1.5) & \
                    (data.jet_eta < 2.5)]

for what, bkg in [('BvsL', 0), ('BvsC', 4)]:
   print what
   for disc, color in [('CSVv2', 'r'), ('DeepCSV', 'g'), ('DeepFlavour', 'b')]:
      print ' ',disc
      flav_mask = (HEM_15_16.flavour == 5) | (HEM_15_16.flavour == bkg)
      truth = (HEM_15_16[flav_mask].flavour == 5).astype(float)
      prediction = HEM_15_16[flav_mask][disc]
      if args.bootstrap:
         fakes, eff, unc = bootstrapped_roc(truth, prediction)
         plt.fill_betweenx(fakes, eff-unc, eff+unc, color=color, alpha=0.3)
      else:
         fakes, eff, _ = roc_curve(truth, prediction)
      plt.plot(eff, fakes, color, label='%s HEM 15-16' % disc)
      
      flav_mask = (safe_data.flavour == 5) | (safe_data.flavour == bkg)
      truth = (safe_data[flav_mask].flavour == 5).astype(float)
      prediction = safe_data[flav_mask][disc]
      fakes, eff, _ = roc_curve(truth, prediction)
      plt.plot(eff, fakes, color+'--', label='%s FWD' % disc)
   plt.ylabel('Mistag Rate')
   plt.xlabel('Efficiency')
   plt.legend(loc='best')
   plt.ylim(5e-4, 1)
   plt.gca().set_yscale('log')
   plt.grid(which='both')
   plt.xlim(0,1)
   plt.savefig('%s/%s.png' % (args.outdir, what))
   plt.savefig('%s/%s.pdf' % (args.outdir, what))
   plt.clf()



for disc, color in [('CSVv2', 'r'), ('DeepCSV', 'g'), ('DeepFlavour', 'b')]:
   disc_mask = np.ones(data.shape[0]).astype(bool) #(data[disc] >= 0)
   print disc
   flav_mask = (data.flavour == 5) | (data.flavour == 0)
   truth = (data[flav_mask & disc_mask].flavour == 5).astype(float)
   prediction = data[flav_mask & disc_mask][disc]
   if args.bootstrap:
      fakes, eff, unc = bootstrapped_roc(truth, prediction)
      plt.fill_betweenx(fakes, eff-unc, eff+unc, color=color, alpha=0.3)
   else:
      fakes, eff, _ = roc_curve(truth, prediction)
   plt.plot(eff, fakes, color, label='%s' % disc)   

   flav_mask = (data.flavour == 5) | (data.flavour == 4)
   truth = (data[flav_mask & disc_mask].flavour == 5).astype(float)
   prediction = data[flav_mask & disc_mask][disc]
   if args.bootstrap:
      fakes, eff, unc = bootstrapped_roc(truth, prediction)
      plt.fill_betweenx(fakes, eff-unc, eff+unc, color=color, alpha=0.3)
   else:
      fakes, eff, _ = roc_curve(truth, prediction)
   plt.plot(eff, fakes, color+'--')

plt.ylabel('Mistag Rate')
plt.xlabel('Efficiency')
plt.legend(loc='best')
plt.ylim(5e-4, 1)
plt.gca().set_yscale('log')
plt.grid(which='both')
plt.xlim(0,1)
plt.savefig('%s/FULL.png' % args.outdir)
plt.savefig('%s/FULL.pdf' % args.outdir)
plt.clf()
