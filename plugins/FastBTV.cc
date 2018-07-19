// -*- C++ -*-
//
// Class:      FastBTV
// 
/**\class FastBTV FastBTV.cc 

   Description: Make a simple tree with Jet quantities for futher studies

   Implementation:
   [Notes on implementation]
*/
//
// Original Author:  Mauro Verzetti
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include "TTree.h"

#include <map>
#include <boost/algorithm/string.hpp>

//
// class declaration
//

class FastBTV : public edm::EDAnalyzer {
public:
  explicit FastBTV(const edm::ParameterSet&);
  ~FastBTV();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

	typedef std::vector<std::string> vstring;
  // ----------member data ---------------------------
  const edm::EDGetTokenT<std::vector<pat::Jet> > jets_;

  edm::Service<TFileService> fs;
	TTree *tree_;

	unsigned int lumi = 0;
	unsigned int run = 0;
	unsigned long long evt = 0;
	int flavour = 0;
	float jet_pt = -1;
	float jet_eta = -1;
	float jet_phi = -1;

  // declare a map of b-tag discriminator histograms
  std::map<std::string, vstring> bdisc_names_;
  std::map<std::string, float> bdisc_vals_;
};

FastBTV::FastBTV(const edm::ParameterSet& iConfig) :
  jets_(consumes<std::vector<pat::Jet> >(iConfig.getParameter<edm::InputTag>("jets")))
{
	tree_ = fs->make<TTree>("tree", "tree");
	tree_->Branch("run" , &run, "run/i");
	tree_->Branch("lumi", &lumi, "lumi/i");
	tree_->Branch("evt" , &evt, "evt/i");
	tree_->Branch("flavour" , &flavour, "flavour/i");
	tree_->Branch("jet_pt", &jet_pt , "jet_pt/f");
	tree_->Branch("jet_eta", &jet_eta, "jet_eta/f");
	tree_->Branch("jet_phi", &jet_phi, "jet_phi/f");

	const edm::ParameterSet bdiscs = iConfig.getParameter<edm::ParameterSet>("bDiscriminators");	
	for(auto &name : bdiscs.getParameterNames()) {
		vstring vals = bdiscs.getParameter<vstring>(name);
		bdisc_names_[name] = vals;
		bdisc_vals_[name] = -42.;
		tree_->Branch(name.c_str(), &bdisc_vals_[name], (name+"/f").c_str());
	}
}



FastBTV::~FastBTV()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
FastBTV::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // define a jet handle
  edm::Handle<std::vector<pat::Jet> > jets;
  // get jets from the event
  iEvent.getByToken(jets_, jets);

	run  = iEvent.id().run();
	lumi = iEvent.id().luminosityBlock();
  evt  = iEvent.id().event();
  // loop over jets
  for(auto& jet : *jets) {
		flavour = std::abs( jet.hadronFlavour() );
		jet_pt  = jet.pt();
		jet_eta = jet.eta();
		jet_phi = jet.phi();

		// fill discriminators 
		for(auto& entry : bdisc_names_) {
			//std::cout << "Entry: " << entry.first << std::endl;
			float sum = 0;
			for(auto& bname : entry.second) {
				float disc = jet.bDiscriminator(bname);
				//std::cout << "   - " << bname << " : " << disc << std::endl;
				sum += disc;
			}
			//std::cout << "-> tot: " << sum << std::endl;
			bdisc_vals_[entry.first] = sum;
		}
		tree_->Fill();
	}
}

// ------------ method called once each job just before starting event loop  ------------
void 
FastBTV::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
FastBTV::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
  void 
  FastBTV::beginRun(edm::Run const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method called when ending the processing of a run  ------------
/*
  void 
  FastBTV::endRun(edm::Run const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
  void 
  FastBTV::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
  void 
  FastBTV::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
  {
  }
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FastBTV::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(FastBTV);
