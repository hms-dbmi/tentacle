#Tentacle - DBMI Repo Crawler 


## Overview

Tentacle is the DBMI Repo Crawler.  It will periodically poll a list of code repositories (github repos / organizations) looking for a `.dbmi.yml` file.  This file should contian appropriate metadata about the repository and that information will be updated to the DBMI confluence in a searchable manner.

Tentacle consists of three componenet

* the `.dmbi.yml` file itself an  its associated definition.

* A registration function that updates a tentacle managed list of repos / organizations to crawl.  (it's suggested to start with s3 file, or even confluence page as list as this list.  ideally registration would be as simple as executing the following from slack

/tentacle register <url>

that will call a lambda that firstattempt to ingest the repo, then updates the master list, or repos to crawl.

* A Reporter, initially this will be a confluence page, but a Reporter should be abstracted so we can for example chuck it all out to a dataase.

## `.dbmi.yml`

example:

```
project: what should I call you
description: - |
			   just indent from the pipe above
			   and you can use as many lines
			   as you like
lab: wha lab you in 
authors:
	   - name of authors
	   - one per line
	   - in order of contribution
	   - dont forget the dashes
languages:
	   - python
	   - R
	   - Html
	   - or whatever
tags: 
		- one tag
		- per line
		- describing
		- what this is

# above this line is required, below this line
# optional but highly appreciated
url:    - default url will be this repo, you can change that
needs:
		- like tags
		- but a list
		- of skills
		- things
		- or people
		- the project needs
packages:
		- some of the
		- more popular packages
		- you use, will be searchable
		- so just the more
		- prominent packages used
		- in the repo
```


TODO:

Seems like a bunch of that could be gathered from the repo for a github repo at least.  We could actually have   generate service that generates the yaml from the url and spits it back to slack.  Or even have some special "yml commands" like <<<from repo>>> that signals the parser to pick it up.
