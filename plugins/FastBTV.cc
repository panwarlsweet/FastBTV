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
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include "TTree.h"

#include <map>
#include "TH2F.h"

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
  const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puInfo_;
  const std::vector<std::string> bDiscriminators_;
  edm::Service<TFileService> fs;
  // declare a map of b-tag discriminator histograms
  std::map<std::string, TH2F *> bDiscriminatorsMap;
	TTree *tree_;

	unsigned int lumi = 0;
	unsigned int run = 0;
	unsigned long long evt = 0;
	int flavour = 0;
	float jet_pt = -1;
	float jet_eta = -1;
	float jet_phi = -1;
        unsigned int pu = 0;

  // declare a map of b-tag discriminator histograms
  std::map<std::string, vstring> bdisc_names_;
  std::map<std::string, float> bdisc_vals_;
};

FastBTV::FastBTV(const edm::ParameterSet& iConfig) :
  jets_(consumes<std::vector<pat::Jet> >(iConfig.getParameter<edm::InputTag>("jets"))),
  puInfo_(consumes<std::vector<PileupSummaryInfo> >(iConfig.getParameter<edm::InputTag>("puInfo"))),
  bDiscriminators_(iConfig.getParameter<std::vector<std::string> >("bDiscriminators_hist"))
{
	tree_ = fs->make<TTree>("tree", "tree");
	tree_->Branch("run" , &run, "run/i");
	tree_->Branch("lumi", &lumi, "lumi/i");
	tree_->Branch("evt" , &evt, "evt/i");
	tree_->Branch("flavour" , &flavour, "flavour/i");
	tree_->Branch("jet_pt", &jet_pt , "jet_pt/f");
	tree_->Branch("jet_eta", &jet_eta, "jet_eta/f");
	tree_->Branch("jet_phi", &jet_phi, "jet_phi/f");
	tree_->Branch("pu", &pu, "pu/i");
	const edm::ParameterSet bdiscs = iConfig.getParameter<edm::ParameterSet>("bDiscriminators");	
	for(auto &name : bdiscs.getParameterNames()) {
		vstring vals = bdiscs.getParameter<vstring>(name);
		bdisc_names_[name] = vals;
		bdisc_vals_[name] = -42.;
		tree_->Branch(name.c_str(), &bdisc_vals_[name], (name+"/f").c_str());
	}
	std::string bDiscr_flav = "";
	std::string bDiscr_flav_eta = "";
	std::string bDiscr_flav_pu = "";

	// initialize b-tag discriminator histograms
	for( const std::string &bDiscr : bDiscriminators_ )
	  {
	    for( const std::string &flav : {"b","c","udsg"} )
	      {
		bDiscr_flav = bDiscr + "_" + flav;
		bDiscr_flav_eta = bDiscr + "_" + flav + "_eta";
		bDiscr_flav_pu = bDiscr + "_" + flav + "_pu";
		if ( bDiscr.find("pfDeepCSVJetTags:probbb") != std::string::npos || bDiscr.find("pfDeepCSVJetTags:probb") != std::string::npos ) {
		  bDiscr_flav = std::string("pfDeepCSVJetTagsProbB") + "_" + flav;
		  bDiscr_flav_eta = std::string("pfDeepCSVJetTagsProbB") + "_" + flav + "_eta";
		  bDiscr_flav_pu = std::string("pfDeepCSVJetTagsProbB") + "_" + flav + "_pu";

		  if ( bDiscriminatorsMap.find(bDiscr_flav) == bDiscriminatorsMap.end() )
		    bDiscriminatorsMap[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 1000, 0, 1000, 4400, -11, 11);
		  if ( bDiscriminatorsMap.find(bDiscr_flav_eta) == bDiscriminatorsMap.end() )
        	    bDiscriminatorsMap[bDiscr_flav_eta] = fs->make<TH2F>(bDiscr_flav_eta.c_str(), (bDiscr_flav_eta + ";Jet #eta; b-tag discriminator").c_str(), 100, -2.5 , 2.5, 4400, -11, 11);
		  if ( bDiscriminatorsMap.find(bDiscr_flav_pu) == bDiscriminatorsMap.end() )
		    bDiscriminatorsMap[bDiscr_flav_pu] = fs->make<TH2F>(bDiscr_flav_pu.c_str(), (bDiscr_flav_pu + ";npu; b-tag discriminator").c_str(), 30, 50, 80, 4400, -11, 11);
		  
		}
		else if ( bDiscr.find("pfDeepFlavourJetTags:probbb") != std::string::npos || bDiscr.find("pfDeepFlavourJetTags:probb") != std::string::npos || bDiscr.find("pfDeepFlavourJetTags:problepb") != std::string::npos) {
		  bDiscr_flav = std::string("pfDeepFlavourJetTagsProbB") + "_" + flav;
		  bDiscr_flav_eta = std::string("pfDeepFlavourJetTagsProbB") + "_" + flav + "_eta";
                  bDiscr_flav_pu = std::string("pfDeepFlavourJetTagsProbB") + "_" + flav + "_pu";

		  if ( bDiscriminatorsMap.find(bDiscr_flav) == bDiscriminatorsMap.end() ){
		    bDiscriminatorsMap[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 1000, 0, 1000, 4400, -11, 11);
		  if ( bDiscriminatorsMap.find(bDiscr_flav_eta) == bDiscriminatorsMap.end() )
		    bDiscriminatorsMap[bDiscr_flav_eta] = fs->make<TH2F>(bDiscr_flav_eta.c_str(), (bDiscr_flav_eta + ";Jet #eta; b-tag discriminator").c_str(), 100, -2.5 , 2.5, 4400, -11, 11);
                  if ( bDiscriminatorsMap.find(bDiscr_flav_pu) == bDiscriminatorsMap.end() )
  		    bDiscriminatorsMap[bDiscr_flav_pu] = fs->make<TH2F>(bDiscr_flav_pu.c_str(), (bDiscr_flav_pu + ";npu; b-tag discriminator").c_str(), 30, 50, 80, 4400, -11, 11);
		  }
  		}
		else{ 
		  bDiscriminatorsMap[bDiscr_flav] = fs->make<TH2F>(bDiscr_flav.c_str(), (bDiscr_flav + ";Jet p_{T} [GeV];b-tag discriminator").c_str(), 1000, 0, 1000, 4400, -11, 11);
		  bDiscriminatorsMap[bDiscr_flav_eta] = fs->make<TH2F>(bDiscr_flav_eta.c_str(), (bDiscr_flav_eta + ";Jet #eta; b-tag discriminator").c_str(), 100, -2.5 , 2.5, 4400, -11, 11);
   		  bDiscriminatorsMap[bDiscr_flav_pu] = fs->make<TH2F>(bDiscr_flav_pu.c_str(), (bDiscr_flav_pu + ";npu; b-tag discriminator").c_str(), 30, 50, 80, 4400, -11, 11);
		}
	      }
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
  edm::Handle<std::vector<PileupSummaryInfo> > puInfo;
  // get jets from the event
  iEvent.getByToken(jets_, jets);
  iEvent.getByToken(puInfo_,puInfo);

	run  = iEvent.id().run();
	lumi = iEvent.id().luminosityBlock();
	evt  = iEvent.id().event();
	for( auto & frame : *puInfo ) {
	  if( frame.getBunchCrossing() == 0 ) {
	        pu = frame.getTrueNumInteractions();
	        break;
	  }
	}
	std::string bDiscr_flav = "";
	std::string bDiscr_flav_eta = "";
	std::string bDiscr_flav_pu = "";
	for( auto jet = jets->begin(); jet != jets->end(); ++jet )
	  {
	    if( jet->pt()<=20. || abs(jet->eta())>2.5) continue;
	    int flav = std::abs( jet->hadronFlavour() );
	    for( const std::string &bDiscr : bDiscriminators_ )
	      {
		//	if( jet->pt()<=20. || abs(jet->eta())>2.5) continue; // skip jets with low pT or outside the tracker acceptance
	   
		if( flav==5 ){ // b jet
		  bDiscr_flav = bDiscr + "_b";
     		  bDiscr_flav_eta = bDiscr + "_b_eta";
		  bDiscr_flav_pu = bDiscr + "_b_pu";
		}
		else if( flav==4 ){ // c jets
		  bDiscr_flav = bDiscr + "_c";
		  bDiscr_flav_eta = bDiscr + "_c_eta";
                  bDiscr_flav_pu = bDiscr + "_c_pu";
		}
		else{ // light-flavor jet
		  bDiscr_flav = bDiscr + "_udsg";
		  bDiscr_flav_eta = bDiscr + "_udsg_eta";
                  bDiscr_flav_pu = bDiscr + "_udsg_pu";
		}
		if ( bDiscr.find("pfDeepCSVJetTags:probbb") != std::string::npos ) continue; //// We will sum the DeepCSV::probbb and DeepCSV::probb together
		if ( bDiscr.find("pfDeepCSVJetTags:probb") != std::string::npos ) {
		    boost::replace_all(bDiscr_flav, bDiscr, "pfDeepCSVJetTagsProbB") ;
		    bDiscriminatorsMap[bDiscr_flav]->Fill( jet->pt(), jet->bDiscriminator("pfDeepCSVJetTags:probb") + jet->bDiscriminator("pfDeepCSVJetTags:probbb") );

		    boost::replace_all(bDiscr_flav_eta, bDiscr, "pfDeepCSVJetTagsProbB") ;
		    bDiscriminatorsMap[bDiscr_flav_eta]->Fill( jet->eta(), jet->bDiscriminator("pfDeepCSVJetTags:probb") + jet->bDiscriminator("pfDeepCSVJetTags:probbb") );

		    boost::replace_all(bDiscr_flav_pu, bDiscr, "pfDeepCSVJetTagsProbB") ;
		    bDiscriminatorsMap[bDiscr_flav_pu]->Fill( pu, jet->bDiscriminator("pfDeepCSVJetTags:probb") + jet->bDiscriminator("pfDeepCSVJetTags:probbb") );
		}
		else if ( bDiscr.find("pfDeepFlavourJetTags:probbb") != std::string::npos || bDiscr.find("pfDeepFlavourJetTags:problepb") != std::string::npos  ) continue; //// We will sum the DeepCSV::probbb and DeepCSV::probb together
		if ( bDiscr.find("pfDeepFlavourJetTags:probb") != std::string::npos ) {
		     boost::replace_all(bDiscr_flav, bDiscr, "pfDeepFlavourJetTagsProbB") ;
		     bDiscriminatorsMap[bDiscr_flav]->Fill( jet->pt(), jet->bDiscriminator("pfDeepFlavourJetTags:probb") + jet->bDiscriminator("pfDeepFlavourJetTags:probbb")+ jet->bDiscriminator("pfDeepFlavourJetTags:problepb") );
		     boost::replace_all(bDiscr_flav_eta, bDiscr, "pfDeepFlavourJetTagsProbB") ;
		     bDiscriminatorsMap[bDiscr_flav_eta]->Fill( jet->eta(), jet->bDiscriminator("pfDeepFlavourJetTags:probb") + jet->bDiscriminator("pfDeepFlavourJetTags:probbb")+ jet->bDiscriminator("pfDeepFlavourJetTags:problepb") );
		     boost::replace_all(bDiscr_flav_pu, bDiscr, "pfDeepFlavourJetTagsProbB") ;
		     bDiscriminatorsMap[bDiscr_flav_pu]->Fill( pu, jet->bDiscriminator("pfDeepFlavourJetTags:probb") + jet->bDiscriminator("pfDeepFlavourJetTags:probbb")+ jet->bDiscriminator("pfDeepFlavourJetTags:problepb") );
		}
	       	else {
		    bDiscriminatorsMap[bDiscr_flav]->Fill( jet->pt(), jet->bDiscriminator(bDiscr) );
		    bDiscriminatorsMap[bDiscr_flav_eta]->Fill( jet->eta(), jet->bDiscriminator(bDiscr) );
		    bDiscriminatorsMap[bDiscr_flav_pu]->Fill( pu, jet->bDiscriminator(bDiscr) ); 
		}
	      }
	  }
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
