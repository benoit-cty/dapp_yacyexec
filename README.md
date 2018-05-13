![dapp logo](./logo.png)
# YaCyExec
## Description
YaCy Decentralized search engine on iExec
## [Dapp params](./iexec.js)


# Intro
This is my note for the search assignment "try and build a decentralized search Dapp" of [TheSchool.AI](https://www.theschool.ai)

I think of :
- Put a button "support us" on [YaCy P2P search engine](https://yacy.net/) to send ETH to the node => Not a decentralized search
- Take a small fee at every query a user made to support the YaCy node where the query occurs. It could have been a way to use [Oraclize.it](http://www.oraclize.it/). => But who want's to wait for a blockchain validation at every query they made in a search engine ?
- Make the crawling of a website available to everyone throw a decentralized application. So a company who want to be indexed in YaCy could just pay a worker for it. => Make sens and will make me learn something new !

# Decentralized Computing

How to do it ?
You can't do much compute task directly in a smart contract as you have to pay for every instruction. The compute intensive task as to be done off-chain. System like [Oraclize.it](http://www.oraclize.it/) allow to call a URL but it's more to get info like a price or weather, not launch a compute task that will take several minutes or more. And with Oraclize.it the computing is centralized, not what we are looking for.
Fortunatly there are projects that target to allow decentralized intensive computing task. For exemple [Golem](https://golem.network/) and [RNDR](https://rendertoken.com/) for 3D rendering. We will use [iExec](https://iex.ec/) who allow to decentralize our own compute task.

> iExec is the first decentralized marketplace for cloud resources. The iExec platform allows everyone to monetize their applications, servers and data-sets.

iExec is a whole ecosystem with a market-place for DApps, Oracle mecanisme, Scheduler, workers,... Dedicated to off-chain computing in a fully decentralized way.
(https://iex.ec/app/uploads/2017/08/decentralized-cloud-infographic@3x-1.png)

The V2 is coming at the end of the month and will introduce the Proof Of Completion system.

[iExec SDK](https://github.com/iExecBlockchainComputing/iexec-sdk) is a NodeJS application build above Truffle who allow to easily create and manage your application.

It is now possible to use a Docker image with iExec. So my goal is to embeded YaCy in a Docker container in a way that allow iExec to launch the crawl.
And there is a really good [interractive tutorial](https://www.katacoda.com/sulliwane/scenarios/ffmpeg) to learn that. Congratulation to the team.

YaCy exist as a Docker container and the crawler could be launch by calling an url :
```
http://localhost:8090/Crawler_p.html?crawlingDomMaxPages=10000&range=wide&intention=&sitemapURL=&crawlingQ=on&crawlingMode=url&crawlingURL=http://WEBSITE_TO_CRAWL.net/&crawlingFile=&mustnotmatch=&crawlingFile%24file=&crawlingstart=Neuen%20Crawl%20starten&mustmatch=.*&createBookmark=on&bookmarkFolder=/crawlStart&xsstopw=on&indexMedia=on&crawlingIfOlderUnit=hour&cachePolicy=iffresh&indexText=on&crawlingIfOlderCheck=on&bookmarkTitle=&crawlingDomFilterDepth=1&crawlingDomFilterCheck=on&crawlingIfOlderNumber=1&crawlingDepth=4
```
For more information read the [wiki page](http://www.yacy-websearch.net/wiki/index.php/Dev:APICrawler).

So everything seems to match together ;-)

But we need to finish the iExec task when the crawler finish the indexation and save it to the YaCy P2P network.


## Installation

### Docker

```
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - \
sudo apt-get install docker-ce
usermod -G docker $USER
newgrp docker
docker run hello-world
```

### iExec

[iExec SDK](https://github.com/iExecBlockchainComputing/iexec-sdk) could be installed through npm but it failed on my computer.
With Docker it also failed, but the comunity helped me and it was the occasion to help them [fix a bug](https://github.com/iExecBlockchainComputing/iexec-sdk/pull/37)

Docker installation as a command line tools is done in one line :
```
echo 'alias iexec='"'"'docker run -e DEBUG=$DEBUG --interactive --tty --rm -v $(pwd):/iexec-project -w /iexec-project iexechub/iexec-sdk'"'"'' >> ~/.bashrc && source ~/.bashrc

```

Project init :
iExec SDK is build over truffle and allow to easily build and deploy app. Getting ETH and RLC for testing is easy :
```
iexec init # init a project
cd iexec-init # enter the project
iexec wallet create # create a wallet
iexec wallet getETH # get some ETH
iexec wallet getRLC # get some RLC
iexec wallet show # check you received the tokens
iexec account allow 5 # credit your account with RLC
iexec account show # check your iExec account balance
```

### YaCy

## How to run the project

Install NodeJS and iExec-SDK (see above).

Git clone the repository and cd into it.
> npm install

Set the URL to index in iexec.js
Submit the job
> iexec submit

## How I made it

Rename the folder ixec-init to the name of your project.
Set the name in iexec.js
Rename the contract in contracts folder and edit it to set is name.

Define the parameter in the iexec.js file.

Here are the parameters that will describe our work:
    cmdline: XXX cli arguments.
    dirinuri: The worker will download this URI before executing the app XXX not needed.

Deploy you DApp on the Ethereum blockchain and the iExec decentralized cloud.
"deploy" will compile the smart contrat and send it to Ropsten
> iexec deploy
Submit a job
> iexec submit
Check the status
> iexec result 0x6f2db[...]
Save job output
> iexec result 0x6f2db[...] --save
Read job output
> cat 0x6f2db[...].text


### Made a YaCy Docker image to handle crawling.

See [How to publish a Docker image](https://ropenscilabs.github.io/r-docker-tutorial/04-Dockerhub.html)
Create a Docker Hub account
Login from command line
> docker login --username=trancept

Create [Dockerfile](apps/Dockerfile) in _apps_ folder of the project.
All the operation to be done at run time are in  [yacyexec.py](apps/yacyexec.py)
```
docker build apps/ -t trancept/yacyexec:firsttry
```
Test the image like iExec will run it before submiting
> docker run -v /tmp:/iexec trancept/yacyexec:firsttry http://toto.com

To build and run in one command
> docker build apps/ -t trancept/yacyexec:firsttry && docker run -v /tmp:/iexec trancept/yacyexec:firsttry http://toto.com

If everything is OK, submit the image to Docker Hub
> docker push trancept/yacyexec:firsttry
