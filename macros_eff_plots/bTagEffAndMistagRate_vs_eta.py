#
# Simple script to extract the MC b-tagging efficiencies and mistag rates
#

import copy, optparse
from ROOT import TFile, TLegend, TCanvas,  TGraphAsymmErrors, gROOT, gStyle

#---------------------------------------------------------------------
# to run in the batch mode (to prevent canvases from popping up)
gROOT.SetBatch()

# set plot style
gROOT.SetStyle("Plain")

# suppress the statistics box
gStyle.SetOptStat(0)

# suppress the histogram title
gStyle.SetOptTitle(0)

gStyle.SetPadTickX(1)  # to get the tick marks on the opposite side of the frame
gStyle.SetPadTickY(1)  # to get the tick marks on the opposite side of the frame

# set nicer fonts
gStyle.SetTitleFont(42, "XYZ")
gStyle.SetLabelFont(42, "XYZ")
#---------------------------------------------------------------------

parser = optparse.OptionParser(usage="")

parser.add_option('-o', '--operating_point', metavar='OPERATING_POINT', action='store', dest='operating_point', default='medium', help='Operating point to use')

(options, args) = parser.parse_args(args=None)


# b-tagger
bTagger = 'pfDeepCSVJetTagsProbB'
bTagger1 = 'pfDeepFlavourJetTagsProbB'
"""
DeepCSV:2018
loose	0.1241
medium	0.4184
tight	0.7527

DeepJet:2018
loose	0.0494
medium	0.2770
tight	0.7264
"""

# medium operating point
"""
operatingPoint_L = 0.1241
operatingPoint_M = 0.4184
operatingPoint_T = 0.7527

"""
operatingPoint_L = 0.0494
operatingPoint_M = 0.2770
operatingPoint_T = 0.7264


# input files
inputFile_AK4_2021 = TFile.Open('TTbar_Run3_2021.root')
inputFile_AK4_2023   = TFile.Open('TTbar_Run3_2023.root')
inputFile_AK4_2024   = TFile.Open('TTbar_Run3_2024.root')

# get 2D b-tag discriminator vs jet pT histograms

discrVsPt_b_AK4_2021    = inputFile_AK4_2021.Get('bTaggingExerciseIIAK4Jets/' + bTagger1 + '_b_eta')
discrVsPt_c_AK4_2021 = inputFile_AK4_2021.Get('bTaggingExerciseIIAK4Jets/' + bTagger1 + '_c_eta')
discrVsPt_udsg_AK4_2021 = inputFile_AK4_2021.Get('bTaggingExerciseIIAK4Jets/' + bTagger1 + '_udsg_eta')

discrVsPt_b_AK4_2023    = inputFile_AK4_2023.Get('bTaggingExerciseIIAK4Jets/' + bTagger1 + '_b_eta')
discrVsPt_c_AK4_2023 = inputFile_AK4_2023.Get('bTaggingExerciseIIAK4Jets/' + bTagger1 + '_c_eta')
discrVsPt_udsg_AK4_2023 = inputFile_AK4_2023.Get('bTaggingExerciseIIAK4Jets/' + bTagger1 + '_udsg_eta')

discrVsPt_b_AK4_2024    = inputFile_AK4_2024.Get('bTaggingExerciseIIAK4Jets/' + bTagger1 + '_b_eta')
discrVsPt_c_AK4_2024 = inputFile_AK4_2024.Get('bTaggingExerciseIIAK4Jets/' + bTagger1 + '_c_eta')
discrVsPt_udsg_AK4_2024 = inputFile_AK4_2024.Get('bTaggingExerciseIIAK4Jets/' + bTagger1 + '_udsg_eta')


# make x-axis projections to get 1D distributions of the total number of b and light-flavor (udsg) jets

total_b_AK4_2021    = copy.deepcopy(discrVsPt_b_AK4_2021.ProjectionX("_px1"))
total_c_AK4_2021    = copy.deepcopy(discrVsPt_c_AK4_2021.ProjectionX("_px1"))
total_udsg_AK4_2021 = copy.deepcopy(discrVsPt_udsg_AK4_2021.ProjectionX("_px1"))


total_b_AK4_2023    = copy.deepcopy(discrVsPt_b_AK4_2023.ProjectionX("_px1"))
total_c_AK4_2023    = copy.deepcopy(discrVsPt_c_AK4_2023.ProjectionX("_px1"))
total_udsg_AK4_2023 = copy.deepcopy(discrVsPt_udsg_AK4_2023.ProjectionX("_px1"))


total_b_AK4_2024    = copy.deepcopy(discrVsPt_b_AK4_2024.ProjectionX("_px1"))
total_c_AK4_2024    = copy.deepcopy(discrVsPt_c_AK4_2024.ProjectionX("_px1"))
total_udsg_AK4_2024 = copy.deepcopy(discrVsPt_udsg_AK4_2024.ProjectionX("_px1"))

# here we are finding the bin containing the operationg point discriminator threshold

firstbin_2021_L = discrVsPt_b_AK4_2021.GetYaxis().FindBin(operatingPoint_L)
lastbin_2021_L = discrVsPt_b_AK4_2021.GetYaxis().GetNbins() + 1 # '+ 1' to also include any entries in the overflow bin
firstbin_2021_M = discrVsPt_b_AK4_2021.GetYaxis().FindBin(operatingPoint_M)
lastbin_2021_M = discrVsPt_b_AK4_2021.GetYaxis().GetNbins() + 1
firstbin_2021_T = discrVsPt_b_AK4_2021.GetYaxis().FindBin(operatingPoint_T)
lastbin_2021_T = discrVsPt_b_AK4_2021.GetYaxis().GetNbins() + 1


firstbin_2023_L = discrVsPt_b_AK4_2023.GetYaxis().FindBin(operatingPoint_L)
lastbin_2023_L = discrVsPt_b_AK4_2023.GetYaxis().GetNbins() + 1 # '+ 1' to also include any entries in the overflow bin
firstbin_2023_M = discrVsPt_b_AK4_2023.GetYaxis().FindBin(operatingPoint_M)
lastbin_2023_M = discrVsPt_b_AK4_2023.GetYaxis().GetNbins() + 1
firstbin_2023_T = discrVsPt_b_AK4_2023.GetYaxis().FindBin(operatingPoint_T)
lastbin_2023_T = discrVsPt_b_AK4_2023.GetYaxis().GetNbins() + 1


firstbin_2024_L = discrVsPt_b_AK4_2024.GetYaxis().FindBin(operatingPoint_L)
lastbin_2024_L = discrVsPt_b_AK4_2024.GetYaxis().GetNbins() + 1 # '+ 1' to also include any entries in the overflow bin
firstbin_2024_M = discrVsPt_b_AK4_2024.GetYaxis().FindBin(operatingPoint_M)
lastbin_2024_M = discrVsPt_b_AK4_2024.GetYaxis().GetNbins() + 1
firstbin_2024_T = discrVsPt_b_AK4_2024.GetYaxis().FindBin(operatingPoint_T)
lastbin_2024_T = discrVsPt_b_AK4_2024.GetYaxis().GetNbins() + 1

# make x-axis projections to get 1D distributions of the number of tagged b and light-flavor (udsg) jets
# note that here we are integrating from the bin containing the operating point discriminator threshold.
# hence, the definition of the operationg point is only approximate since the bin boundary will not necessarily
# coincide with the operating point discriminator threshold

tagged_b_AK4_2021_L    = copy.deepcopy(discrVsPt_b_AK4_2021.ProjectionX("_px2",firstbin_2021_L,lastbin_2021_L))
tagged_c_AK4_2021_L    = copy.deepcopy(discrVsPt_c_AK4_2021.ProjectionX("_px2",firstbin_2021_L,lastbin_2021_L))
tagged_udsg_AK4_2021_L    = copy.deepcopy(discrVsPt_udsg_AK4_2021.ProjectionX("_px2",firstbin_2021_L,lastbin_2021_L))

tagged_b_AK4_2021_M    = copy.deepcopy(discrVsPt_b_AK4_2021.ProjectionX("_px2",firstbin_2021_M,lastbin_2021_M))
tagged_c_AK4_2021_M    = copy.deepcopy(discrVsPt_c_AK4_2021.ProjectionX("_px2",firstbin_2021_M,lastbin_2021_M))
tagged_udsg_AK4_2021_M    = copy.deepcopy(discrVsPt_udsg_AK4_2021.ProjectionX("_px2",firstbin_2021_M,lastbin_2021_M))

tagged_b_AK4_2021_T    = copy.deepcopy(discrVsPt_b_AK4_2021.ProjectionX("_px2",firstbin_2021_T,lastbin_2021_T))
tagged_c_AK4_2021_T    = copy.deepcopy(discrVsPt_c_AK4_2021.ProjectionX("_px2",firstbin_2021_T,lastbin_2021_T))
tagged_udsg_AK4_2021_T    = copy.deepcopy(discrVsPt_udsg_AK4_2021.ProjectionX("_px2",firstbin_2021_T,lastbin_2021_T))



tagged_b_AK4_2023_L    = copy.deepcopy(discrVsPt_b_AK4_2023.ProjectionX("_px2",firstbin_2023_L,lastbin_2023_L))
tagged_c_AK4_2023_L    = copy.deepcopy(discrVsPt_c_AK4_2023.ProjectionX("_px2",firstbin_2023_L,lastbin_2023_L))
tagged_udsg_AK4_2023_L    = copy.deepcopy(discrVsPt_udsg_AK4_2023.ProjectionX("_px2",firstbin_2023_L,lastbin_2023_L))

tagged_b_AK4_2023_M    = copy.deepcopy(discrVsPt_b_AK4_2023.ProjectionX("_px2",firstbin_2023_M,lastbin_2023_M))
tagged_c_AK4_2023_M    = copy.deepcopy(discrVsPt_c_AK4_2023.ProjectionX("_px2",firstbin_2023_M,lastbin_2023_M))
tagged_udsg_AK4_2023_M    = copy.deepcopy(discrVsPt_udsg_AK4_2023.ProjectionX("_px2",firstbin_2023_M,lastbin_2023_M))

tagged_b_AK4_2023_T    = copy.deepcopy(discrVsPt_b_AK4_2021.ProjectionX("_px2",firstbin_2023_T,lastbin_2023_T))
tagged_c_AK4_2023_T    = copy.deepcopy(discrVsPt_c_AK4_2021.ProjectionX("_px2",firstbin_2023_T,lastbin_2023_T))
tagged_udsg_AK4_2023_T    = copy.deepcopy(discrVsPt_udsg_AK4_2021.ProjectionX("_px2",firstbin_2023_T,lastbin_2023_T))



tagged_b_AK4_2024_L    = copy.deepcopy(discrVsPt_b_AK4_2024.ProjectionX("_px2",firstbin_2024_L,lastbin_2024_L))
tagged_c_AK4_2024_L    = copy.deepcopy(discrVsPt_c_AK4_2024.ProjectionX("_px2",firstbin_2024_L,lastbin_2024_L))
tagged_udsg_AK4_2024_L    = copy.deepcopy(discrVsPt_udsg_AK4_2024.ProjectionX("_px2",firstbin_2024_L,lastbin_2024_L))

tagged_b_AK4_2024_M    = copy.deepcopy(discrVsPt_b_AK4_2024.ProjectionX("_px2",firstbin_2024_M,lastbin_2024_M))
tagged_c_AK4_2024_M    = copy.deepcopy(discrVsPt_c_AK4_2024.ProjectionX("_px2",firstbin_2024_M,lastbin_2024_M))
tagged_udsg_AK4_2024_M    = copy.deepcopy(discrVsPt_udsg_AK4_2024.ProjectionX("_px2",firstbin_2024_M,lastbin_2024_M))

tagged_b_AK4_2024_T    = copy.deepcopy(discrVsPt_b_AK4_2024.ProjectionX("_px2",firstbin_2024_T,lastbin_2024_T))
tagged_c_AK4_2024_T    = copy.deepcopy(discrVsPt_c_AK4_2024.ProjectionX("_px2",firstbin_2024_T,lastbin_2024_T))
tagged_udsg_AK4_2024_T    = copy.deepcopy(discrVsPt_udsg_AK4_2024.ProjectionX("_px2",firstbin_2024_T,lastbin_2024_T))

# create canvas
c = TCanvas("c", "",1200,800)
c.Divide(3,1)
c.cd(1)
#c.SetLogx()
tagged_b_AK4_2024_L.Rebin(10)
tagged_b_AK4_2024_M.Rebin(10)
tagged_b_AK4_2024_T.Rebin(10)
total_b_AK4_2024.Rebin(10)

tagged_b_AK4_2021_L.Rebin(10)
tagged_b_AK4_2021_M.Rebin(10)
tagged_b_AK4_2021_T.Rebin(10)
total_b_AK4_2021.Rebin(10)

tagged_b_AK4_2023_L.Rebin(10)
tagged_b_AK4_2023_M.Rebin(10)
tagged_b_AK4_2023_T.Rebin(10)
total_b_AK4_2023.Rebin(10)

# b jets

eff_b_AK4_2021_L = TGraphAsymmErrors(tagged_b_AK4_2021_L, total_b_AK4_2021, "cp")
eff_b_AK4_2021_L.GetXaxis().SetTitle("Jet #eta")
eff_b_AK4_2021_L.GetYaxis().SetTitle("b-tagging efficiency")
eff_b_AK4_2021_L.GetXaxis().SetRangeUser(-2.5, 2.5)
eff_b_AK4_2021_L.GetYaxis().SetRangeUser(0.,1.0)
eff_b_AK4_2021_L.SetLineWidth(2)
eff_b_AK4_2021_L.SetLineColor(3)
eff_b_AK4_2021_L.SetLineStyle(1)
#eff_b_AK4_2021_L.SetMarkerColor(3)
#eff_b_AK4_2021_L.SetMarkerStyle(20)
eff_b_AK4_2021_L.Draw('ap')

eff_b_AK4_2021_M = TGraphAsymmErrors(tagged_b_AK4_2021_M, total_b_AK4_2021, "cp")
eff_b_AK4_2021_M.SetLineWidth(2)
eff_b_AK4_2021_M.SetLineStyle(1)
eff_b_AK4_2021_M.SetLineColor(4)
#eff_b_AK4_2021_M.SetMarkerColor(4)
#eff_b_AK4_2021_M.SetMarkerStyle(20)
eff_b_AK4_2021_M.Draw('p same')

eff_b_AK4_2021_T = TGraphAsymmErrors(tagged_b_AK4_2021_T, total_b_AK4_2021, "cp")
eff_b_AK4_2021_T.SetLineWidth(2)
eff_b_AK4_2021_T.SetLineStyle(1)
eff_b_AK4_2021_T.SetLineColor(2)
#eff_b_AK4_2021_T.SetMarkerColor(6)
#eff_b_AK4_2021_T.SetMarkerStyle(20)
eff_b_AK4_2021_T.Draw('p same')


eff_b_AK4_2023_L = TGraphAsymmErrors(tagged_b_AK4_2023_L, total_b_AK4_2023, "cp")
eff_b_AK4_2023_L.SetLineWidth(2)
eff_b_AK4_2023_L.SetLineStyle(2)
eff_b_AK4_2023_L.SetLineColor(3)
#eff_b_AK4_2023_L.SetMarkerColor(3)
#eff_b_AK4_2023_L.SetMarkerStyle(20)
eff_b_AK4_2023_L.Draw('p same')

eff_b_AK4_2023_M = TGraphAsymmErrors(tagged_b_AK4_2023_M, total_b_AK4_2023, "cp")
eff_b_AK4_2023_M.SetLineWidth(2)
eff_b_AK4_2023_M.SetLineStyle(2)
eff_b_AK4_2023_M.SetLineColor(4)
#eff_b_AK4_2023_M.SetMarkerColor(4)
#eff_b_AK4_2023_M.SetMarkerStyle(20)
eff_b_AK4_2023_M.Draw('p same')

eff_b_AK4_2023_T = TGraphAsymmErrors(tagged_b_AK4_2023_T, total_b_AK4_2023, "cp")
eff_b_AK4_2023_T.SetLineWidth(2)
eff_b_AK4_2023_T.SetLineStyle(2)
eff_b_AK4_2023_T.SetLineColor(2)
#eff_b_AK4_2023_T.SetMarkerColor(6)
#eff_b_AK4_2023_T.SetMarkerStyle(20)
eff_b_AK4_2023_T.Draw('p same')


eff_b_AK4_2024_L = TGraphAsymmErrors(tagged_b_AK4_2024_L, total_b_AK4_2024, "cp")
eff_b_AK4_2024_L.SetLineWidth(2)
eff_b_AK4_2024_L.SetLineColor(3)
eff_b_AK4_2024_L.SetLineStyle(3)
#eff_b_AK4_2024_L.SetMarkerColor(3)
#eff_b_AK4_2024_L.SetMarkerStyle(20)
eff_b_AK4_2024_L.Draw('p same')

eff_b_AK4_2024_M = TGraphAsymmErrors(tagged_b_AK4_2024_M, total_b_AK4_2024, "cp")
eff_b_AK4_2024_M.SetLineWidth(2)
eff_b_AK4_2024_M.SetLineStyle(3)
eff_b_AK4_2024_M.SetLineColor(4)
#eff_b_AK4_2024_M.SetMarkerColor(4)
#eff_b_AK4_2024_M.SetMarkerStyle(20)
eff_b_AK4_2024_M.Draw('p same')

eff_b_AK4_2024_T = TGraphAsymmErrors(tagged_b_AK4_2024_T, total_b_AK4_2024, "cp")
eff_b_AK4_2024_T.SetLineWidth(2)
eff_b_AK4_2024_T.SetLineStyle(3)
eff_b_AK4_2024_T.SetLineColor(2)
#eff_b_AK4_2024_T.SetMarkerColor(6)
#eff_b_AK4_2024_T.SetMarkerStyle(20)
eff_b_AK4_2024_T.Draw('p same')



# light-flavor jets

c.cd(2)
#c.SetLogx()
tagged_udsg_AK4_2024_L.Rebin(10)
tagged_udsg_AK4_2024_M.Rebin(10)
tagged_udsg_AK4_2024_T.Rebin(10)
total_udsg_AK4_2024.Rebin(10)

tagged_udsg_AK4_2021_L.Rebin(10)
tagged_udsg_AK4_2021_M.Rebin(10)
tagged_udsg_AK4_2021_T.Rebin(10)
total_udsg_AK4_2021.Rebin(10)

tagged_udsg_AK4_2023_L.Rebin(10)
tagged_udsg_AK4_2023_M.Rebin(10)
tagged_udsg_AK4_2023_T.Rebin(10)
total_udsg_AK4_2023.Rebin(10)


eff_udsg_AK4_2021_L = TGraphAsymmErrors(tagged_udsg_AK4_2021_L, total_udsg_AK4_2021, "cp")
eff_udsg_AK4_2021_L.GetXaxis().SetTitle("Jet #eta")
eff_udsg_AK4_2021_L.GetYaxis().SetTitle("light-mistag efficiency")
eff_udsg_AK4_2021_L.GetXaxis().SetRangeUser(-2.5,2.5)
eff_udsg_AK4_2021_L.GetYaxis().SetRangeUser(0.,1.0)
eff_udsg_AK4_2021_L.SetLineWidth(2)
eff_udsg_AK4_2021_L.SetLineColor(3)
eff_udsg_AK4_2021_L.SetLineStyle(1)
#eff_udsg_AK4_2021_L.SetMarkerColor(3)
#eff_udsg_AK4_2021_L.SetMarkerStyle(20)
eff_udsg_AK4_2021_L.Draw('ap')

eff_udsg_AK4_2021_M = TGraphAsymmErrors(tagged_udsg_AK4_2021_M, total_udsg_AK4_2021, "cp")
eff_udsg_AK4_2021_M.SetLineWidth(2)
eff_udsg_AK4_2021_M.SetLineStyle(1)
eff_udsg_AK4_2021_M.SetLineColor(4)
#eff_udsg_AK4_2021_M.SetMarkerColor(4)
#eff_udsg_AK4_2021_M.SetMarkerStyle(20)
eff_udsg_AK4_2021_M.Draw('p same')

eff_udsg_AK4_2021_T = TGraphAsymmErrors(tagged_udsg_AK4_2021_T, total_udsg_AK4_2021, "cp")
eff_udsg_AK4_2021_T.SetLineWidth(2)
eff_udsg_AK4_2021_T.SetLineStyle(1)
eff_udsg_AK4_2021_T.SetLineColor(2)
#eff_udsg_AK4_2021_T.SetMarkerColor(6)
#eff_udsg_AK4_2021_T.SetMarkerStyle(20)
eff_udsg_AK4_2021_T.Draw('p same')


eff_udsg_AK4_2023_L = TGraphAsymmErrors(tagged_udsg_AK4_2023_L, total_udsg_AK4_2023, "cp")
eff_udsg_AK4_2023_L.SetLineWidth(2)
eff_udsg_AK4_2023_L.SetLineStyle(2)
eff_udsg_AK4_2023_L.SetLineColor(3)
#eff_udsg_AK4_2023_L.SetMarkerColor(3)
#eff_udsg_AK4_2023_L.SetMarkerStyle(20)
eff_udsg_AK4_2023_L.Draw('p same')

eff_udsg_AK4_2023_M = TGraphAsymmErrors(tagged_udsg_AK4_2023_M, total_udsg_AK4_2023, "cp")
eff_udsg_AK4_2023_M.SetLineWidth(2)
eff_udsg_AK4_2023_M.SetLineStyle(2)
eff_udsg_AK4_2023_M.SetLineColor(4)
#eff_udsg_AK4_2023_M.SetMarkerColor(4)
#eff_udsg_AK4_2023_M.SetMarkerStyle(20)
eff_udsg_AK4_2023_M.Draw('p same')

eff_udsg_AK4_2023_T = TGraphAsymmErrors(tagged_udsg_AK4_2023_T, total_udsg_AK4_2023, "cp")
eff_udsg_AK4_2023_T.SetLineWidth(2)
eff_udsg_AK4_2023_T.SetLineStyle(2)
eff_udsg_AK4_2023_T.SetLineColor(2)
#eff_udsg_AK4_2023_T.SetMarkerColor(6)
#eff_udsg_AK4_2023_T.SetMarkerStyle(20)
eff_udsg_AK4_2023_T.Draw('p same')


eff_udsg_AK4_2024_L = TGraphAsymmErrors(tagged_udsg_AK4_2024_L, total_udsg_AK4_2024, "cp")
eff_udsg_AK4_2024_L.SetLineWidth(2)
eff_udsg_AK4_2024_L.SetLineColor(3)
eff_udsg_AK4_2024_L.SetLineStyle(3)
#eff_udsg_AK4_2024_L.SetMarkerColor(3)
#eff_udsg_AK4_2024_L.SetMarkerStyle(20)
eff_udsg_AK4_2024_L.Draw('p same')

eff_udsg_AK4_2024_M = TGraphAsymmErrors(tagged_udsg_AK4_2024_M, total_udsg_AK4_2024, "cp")
eff_udsg_AK4_2024_M.SetLineWidth(2)
eff_udsg_AK4_2024_M.SetLineStyle(3)
eff_udsg_AK4_2024_M.SetLineColor(4)
#eff_udsg_AK4_2024_M.SetMarkerColor(4)
#eff_udsg_AK4_2024_M.SetMarkerStyle(20)
eff_udsg_AK4_2024_M.Draw('p same')

eff_udsg_AK4_2024_T = TGraphAsymmErrors(tagged_udsg_AK4_2024_T, total_udsg_AK4_2024, "cp")
eff_udsg_AK4_2024_T.SetLineWidth(2)
eff_udsg_AK4_2024_T.SetLineStyle(3)
eff_udsg_AK4_2024_T.SetLineColor(2)
#eff_udsg_AK4_2024_T.SetMarkerColor(6)
#eff_udsg_AK4_2024_T.SetMarkerStyle(20)
eff_udsg_AK4_2024_T.Draw('p same')

# C-flavor jets

c.cd(3)
#c.SetLogx()
tagged_c_AK4_2024_L.Rebin(10)
tagged_c_AK4_2024_M.Rebin(10)
tagged_c_AK4_2024_T.Rebin(10)
total_c_AK4_2024.Rebin(10)

tagged_c_AK4_2021_L.Rebin(10)
tagged_c_AK4_2021_M.Rebin(10)
tagged_c_AK4_2021_T.Rebin(10)
total_c_AK4_2021.Rebin(10)

tagged_c_AK4_2023_L.Rebin(10)
tagged_c_AK4_2023_M.Rebin(10)
tagged_c_AK4_2023_T.Rebin(10)
total_c_AK4_2023.Rebin(10)


eff_c_AK4_2021_L = TGraphAsymmErrors(tagged_c_AK4_2021_L, total_c_AK4_2021, "cp")
eff_c_AK4_2021_L.GetXaxis().SetTitle("Jet #eta")
eff_c_AK4_2021_L.GetYaxis().SetTitle("c-mistag efficiency")
eff_c_AK4_2021_L.GetXaxis().SetRangeUser(-2.5,2.5)
eff_c_AK4_2021_L.GetYaxis().SetRangeUser(0.,1.0)
eff_c_AK4_2021_L.SetLineWidth(2)
eff_c_AK4_2021_L.SetLineColor(3)
eff_c_AK4_2021_L.SetLineStyle(1)
#eff_c_AK4_2021_L.SetMarkerColor(3)
#eff_c_AK4_2021_L.SetMarkerStyle(20)
eff_c_AK4_2021_L.Draw('ap')

eff_c_AK4_2021_M = TGraphAsymmErrors(tagged_c_AK4_2021_M, total_c_AK4_2021, "cp")
eff_c_AK4_2021_M.SetLineWidth(2)
eff_c_AK4_2021_M.SetLineStyle(1)
eff_c_AK4_2021_M.SetLineColor(4)
##eff_c_AK4_2021_M.SetMarkerColor(4)
#eff_c_AK4_2021_M.SetMarkerStyle(20)
eff_c_AK4_2021_M.Draw('p same')

eff_c_AK4_2021_T = TGraphAsymmErrors(tagged_c_AK4_2021_T, total_c_AK4_2021, "cp")
eff_c_AK4_2021_T.SetLineWidth(2)
eff_c_AK4_2021_T.SetLineStyle(1)
eff_c_AK4_2021_T.SetLineColor(2)
#eff_c_AK4_2021_T.SetMarkerColor(6)
#eff_c_AK4_2021_T.SetMarkerStyle(20)
eff_c_AK4_2021_T.Draw('p same')


eff_c_AK4_2023_L = TGraphAsymmErrors(tagged_c_AK4_2023_L, total_c_AK4_2023, "cp")
eff_c_AK4_2023_L.SetLineWidth(2)
eff_c_AK4_2023_L.SetLineStyle(2)
eff_c_AK4_2023_L.SetLineColor(3)
#eff_c_AK4_2023_L.SetMarkerColor(3)
#eff_c_AK4_2023_L.SetMarkerStyle(20)
eff_c_AK4_2023_L.Draw('p same')

eff_c_AK4_2023_M = TGraphAsymmErrors(tagged_c_AK4_2023_M, total_c_AK4_2023, "cp")
eff_c_AK4_2023_M.SetLineWidth(2)
eff_c_AK4_2023_M.SetLineStyle(2)
eff_c_AK4_2023_M.SetLineColor(4)
#eff_c_AK4_2023_M.SetMarkerColor(4)
#eff_c_AK4_2023_M.SetMarkerStyle(20)
eff_c_AK4_2023_M.Draw('p same')

eff_c_AK4_2023_T = TGraphAsymmErrors(tagged_c_AK4_2023_T, total_c_AK4_2023, "cp")
eff_c_AK4_2023_T.SetLineWidth(2)
eff_c_AK4_2023_T.SetLineStyle(2)
eff_c_AK4_2023_T.SetLineColor(2)
#eff_c_AK4_2023_T.SetMarkerColor(6)
#eff_c_AK4_2023_T.SetMarkerStyle(20)
eff_c_AK4_2023_T.Draw('p same')


eff_c_AK4_2024_L = TGraphAsymmErrors(tagged_c_AK4_2024_L, total_c_AK4_2024, "cp")
eff_c_AK4_2024_L.SetLineWidth(2)
eff_c_AK4_2024_L.SetLineColor(3)
eff_c_AK4_2024_L.SetLineStyle(3)
#eff_c_AK4_2024_L.SetMarkerColor(3)
#eff_c_AK4_2024_L.SetMarkerStyle(20)
eff_c_AK4_2024_L.Draw('p same')

eff_c_AK4_2024_M = TGraphAsymmErrors(tagged_c_AK4_2024_M, total_c_AK4_2024, "cp")
eff_c_AK4_2024_M.SetLineWidth(2)
eff_c_AK4_2024_M.SetLineStyle(3)
eff_c_AK4_2024_M.SetLineColor(4)
#eff_c_AK4_2024_M.SetMarkerColor(4)
#eff_c_AK4_2024_M.SetMarkerStyle(20)
eff_c_AK4_2024_M.Draw('p same')

eff_c_AK4_2024_T = TGraphAsymmErrors(tagged_c_AK4_2024_T, total_c_AK4_2024, "cp")
eff_c_AK4_2024_T.SetLineWidth(2)
eff_c_AK4_2024_T.SetLineStyle(3)
eff_c_AK4_2024_T.SetLineColor(2)
#eff_c_AK4_2024_T.SetMarkerColor(6)
#eff_c_AK4_2024_T.SetMarkerStyle(20)
eff_c_AK4_2024_T.Draw('p same')

# save the plot
c.SaveAs('Efficiency_vs_eta.root')


# close the input files
inputFile_AK4_2021.Close()
inputFile_AK4_2023.Close()
inputFile_AK4_2024.Close()

