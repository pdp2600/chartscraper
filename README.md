Script for scraping weekly Billboard charts from their website. In the future I intend to write functions extending the local module to gather other, more niche/underground charts. Datasets provided from the beginning of the chart to the year end of 2018, for all the charts the local module has been tested with.

Scripts & dataset available to use under GNU General Public License, see LICENSE.txt for full details (basically all uses & modifications allowed as long as the original is cited, and no usage in closed source applications).

***

#### Files
- ***README.md*** - Current file.
- ***LICENSE.txt*** - Full GNU General Public License.
- ***chartscraper.py*** - Billboard chart web scraping local script/module.
- ***CS\_Driver.py*** - Script used to create the dataset & example of how to use _chartscraper_.
- ***\ChartScraper\_data\*** - Folder with CSVs containing data from the beginning of each chart to the last one in 2018, from the following Billboard charts:
	- [Hot R&B/Hip\-hop Albums](https://www.billboard.com/charts/r-b-hip-hop-albums)
	- [Hot R&B/Hip\-hop Songs](https://www.billboard.com/charts/r-b-hip-hop-songs)
	- [Hot 100](https://www.billboard.com/charts/hot-100)
	- [Billboard 200](https://www.billboard.com/charts/billboard-200)
	- [Pop Songs](https://www.billboard.com/charts/pop-songs)
	- [Hot Rock Songs](https://www.billboard.com/charts/rock-songs)
	- [Hot Latin Songs](https://www.billboard.com/charts/latin-songs)
	- [Hot Dance/Electronic Songs](https://www.billboard.com/charts/dance-electronic-songs)
	- [YouTube](https://www.billboard.com/charts/youtube)
	- [Japan Hot 100](https://www.billboard.com/charts/japan-hot-100)
	- [Hot Country Songs](https://www.billboard.com/charts/country-songs)

***
	
#### Usage
The following non-stock modules are utilized (they're all included in the Anaconda distro of Python): 
* [requests](http://docs.python-requests.org/en/master/)
* [pandas](https://pandas.pydata.org/)
* [numpy](http://www.numpy.org/)

Local module file _chartscraper.py_ must be in a location which is a part of the PYHTONPATH or the working directory needs to be changed to its location when it's imported (commented example found in *CS\_Driver.py*)

Main functions are *bb\_get\_weekly\_chart* & *bb\_get\_multiple\_charts*, all functions including internal ones, have help documentation. Included script *CS\_Driver.py* contains an example of how they're used. Worth noting, I have hard coded a 1 second delay between multiple requests to avoid flooding.

##### Notes About Billboard's Site/Data
- URL structure for weekly charts looks like `https://www.billboard.com/charts/r-b-hip-hop-songs/2019-02-02`
	- You don't need to pass the specific date used to denote the week of the chart, Billboard's backend will take any date a part of the week the chart is for.
- There is some potential weirdness with the data which I only encountered once in the R&B/Hip\-Hop songs chart, where between _1978-11-13_ to _1978-11-18_ it had a chart with only the number 1 song. When this case occurs, the data is added and there's a text output notification which should be a prompt to look into the occurence, and make sure no legit charts were missed
- In some cases there are missing artist names. When an artist value is None/null, the string token _"===<Missing_Artist>===" is substituted to make it more explicit.
	- I believe I took care of all the missing artists in the dataset, replacing them with the correct values after doing some research myself. I reported the first one I found in 2018 to the email address in the Billboard site FAQ which was for data corrections, but 4 months later the data was not corrected, so any extra effort of benevolence might be wasted.
