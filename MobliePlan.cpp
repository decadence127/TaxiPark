#include "MobliePlan.h"
#include <iostream>

bool MobilePlan::getIs5gIncluded() const
{
	return is5gIncluded;
}

bool MobilePlan::getIsUnlimitedTextingIncluded() const
{
	return isUnlimitedTextingIncluded;
}

bool MobilePlan::getIsUnlimitedCallingIncluded() const
{
	return isUnlimitedCallingIncluded;
}
std::string MobilePlan::getMobileHotspotData() const
{
	return mobileHotSpotData;
}
void MobilePlan::setIs5gIncluded(const bool is5gIncluded)
{
	this->is5gIncluded = is5gIncluded;
}

void MobilePlan::setIsUnlimitedTextingIncluded(const bool isUnlimitedTextingIncluded)
{
	this->isUnlimitedTextingIncluded = isUnlimitedTextingIncluded;
}

void MobilePlan::setIsUnlimitedCallingIncluded(const bool isUnlimitedCallingIncluded)
{
	this->isUnlimitedCallingIncluded = isUnlimitedCallingIncluded;
}

void MobilePlan::setMobileHotspotData(const std::string mobileHotSpotData)
{
	this->mobileHotSpotData = mobileHotSpotData;
}


std::ofstream& MobilePlan::print(std::ofstream& ofs) const
{
	ofs << getPlanTitle() << ";" << std::endl
		<< getPrice() <<";" << std::endl
		<< getNetworkBandwidth() << ";" << std::endl
		<< getTaxesInclusion() << ";" << std::endl
		<< getIsUnlimited() << ";" << std::endl
		<< getIs5gIncluded() << ";" << std::endl
		<< getIsUnlimitedCallingIncluded() << ";" << std::endl
		<< getIsUnlimitedTextingIncluded() << ";" << std::endl
		<< getMobileHotspotData() << ";" << std::endl;

	return ofs;
}

std::ifstream& MobilePlan::read(std::ifstream& ifs)
{
	ifs >> title;
	ifs >> price;
	ifs >> networkBandwidth;
	ifs >> areTaxesIncluded;
	ifs >> isUnlimited;
	ifs >> is5gIncluded;
	ifs >> isUnlimitedCallingIncluded;
	ifs >> isUnlimitedTextingIncluded;
	ifs >> mobileHotSpotData;
	return ifs;
}

std::string MobilePlan::getPlanInfo()
{
	std::string MobilePlanInfo = "Plan's name: " + this->getPlanTitle() + "\n"
		+ "Price: $" + std::to_string(this->getPrice()) + " Per line per month. Plus taxes and fees if not included." + "\n"
		+ "Taxes: " + (this->getTaxesInclusion() ? "Included in price" : "Not included ") + "\n"
		+ "Estimated Network Bandwidth: " + std::to_string(this->getNetworkBandwidth()) + " Mbps" + "\n"
		+ "5g Access: " + (this->getIs5gIncluded() ? "Yes" : "No") + "\n"
		+ "Unlimited Texting: " + (this->getIsUnlimitedTextingIncluded() ? "Yes" : "No") + "\n"
		+ "Unlimited Calls: " + (this->getIsUnlimitedCallingIncluded() ? "Yes" : "No") + "\n"
		+ "Mobile hotspot: " + this->getMobileHotspotData();

	return MobilePlanInfo;
}