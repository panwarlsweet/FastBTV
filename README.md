# FastBTV
Simple set of scripts and plugins for quick and fast BTV analysis

## Installation
```bash
cmsrel CMSSW_10_1_7
cd CMSSW_10_1_7/src
cmsenv
git cms-init
#Get the latest DeepFlavour training
git cms-addpkg RecoBTag/Combined
git clone https://github.com/cms-data/RecoBTag-Combined.git data
git cms-addpkg RecoBTag/DeepFlavour
wget https://raw.githubusercontent.com/emilbols/cmssw/b62675266e3129ca3f77a62f2d7b29a8546d6f84/RecoBTag/TensorFlow/plugins/DeepFlavourTFJetTagsProducer.cc
mv DeepFlavourTFJetTagsProducer.cc RecoBTag/DeepFlavour/plugins/.

git clone git@github.com:mverzett/FastBTV.git FastBTV/FastBTV
scram b
```

## Usage
### Step 1 - make trees
```
./make_tree.py inputFiles=FILE/TO/RUN.root outputFile=OUTPUT.root
```
**Warning!** The discriminators run, as well as the era, are hardcoded (at least for now).

### Step 2 - make the ROCs
```
./make_rocs.py TREE_FILE.root OUTPUT_DIRECTORY [--bootstrap, to compute ROC uncertainties]
```
**Warning!** The discriminators plotted and the selection are hardcoded. This is specific decision as this 
package is intended for quick checks in specific topologies, rather then systematic studies. For those, please use
[BTagAnalyzer](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements/)
