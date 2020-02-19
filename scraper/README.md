Sam_Scraper
=======================================
A webscraper to pull documents from [beta.sam.gov](https://beta.sam.gov/).

Intent
---------------------------------------

A part of this overall project involves using a given Request-For-Proposal and estimating features (e.g. reward value). To accomplish this, I think we'll need to analyze the text of many RFPs. Using this analysis, we can try to determine a relation between an RFP and it's features.

With the current number of RFPs we have (maybe 15 or so) I don't think the above project is even worth attempting. With a few hundred, I think we can develop some proof of concept. With a few thousand, I think this RFP analysis becomes viable.

I hope TeraThink supplies us with as many RFPs as they can give us. I think it's best to use TeraThink's past to predict TeraThink's future. In the case that TeraThink can't give us enough data, I think this webscraper can serve as a sub-optimal alternative solution.

How It Works
---------------------------------------

Credit to [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). This is the html parser that holds this whole mini project together. This library makes it easy to turn an HTML page into something resembling a [DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction), or, essentially, a "tree" of HTML tags. The library provides easy to use functions for navigating this tree and pulling out all the data I need.

First, we build the search the query. This is mostly taken care of in `build_search_url()`. I actaully think there's a way to build that query a little cleaner using something in `urllib`, but it's good enough for now.

Second, I use Python's standard HTTP library (`urllib`) to make a request to the first search results page. From this, I can determine the total number of pages I'll need to iterate through to collect all of my search results. This  functionality is mostly covered by `find_num_pages()`.

__TODO__: Lastly (for parsing), for each search result on each result page, I'll need to parse the page located at that link. I'd like to build a JSON file for results located at the top of the page, This includes information like reward amount and seems pretty consistent across search results. I'll also need to download the public files available.

Covering logistics, I'm writing to a bz2-compressed tar file, and I'm constantly checking the size of my root directory. I'm slightly worried that running this on my server will max out my storage space... several times.