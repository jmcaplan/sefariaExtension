# Jastrow Jackpot Google Chrome Extension
*A project for Sefaria Hackathon, Summer 2020*

## About
This project is a Chrome browser extension for sefaria.org, that utilizes the [Sefaria API](https://github.com/Sefaria/Sefaria-Project/wiki/API-Documentation#sefaria-apis) and enables the user to search a hebrew word in the Jastrow Aramaic Dictionary, and receive not only the relevant definitions, but also a special message if the user has stumbled upon a 'Jastrow Jackpot' - when an example of the word's usage that the dictionary references matches the source currently being learned (in this case, the source one has open in sefaria.org). 

## How to install
To install the extension, open a Chrome browser and go to chrome://extensions/ and click on 'Load unpacked'. For the folder, choose the appropriate folder from this repository, e.g. v1/chrome_extension

## How to use
Go to the [sefaria website](https://www.sefaria.org/texts) and open a text (for example, [this passage](https://www.sefaria.org/Shabbat.6a?lang=bi) in Tractate Shabbat). Then open the extension:

![Find Extension](media/find_extension.gif)

### *Version 1 Interface*
Type in the hebrew word you wish to search, and click 'Search'. You should see the Jastrow Dictionary definitions relevant to your query. If you are lucky enough, you might just stumble upon a 'Jastrow Jackpot':

![Successful Jackpot](media/successful_jackpot.gif)

### *Version 2 Interface*
In this version, the search result will appear as an iframe of Sefaria's website:

![Successful Jackpot V2](media/successful_jackpot_v2.gif)
