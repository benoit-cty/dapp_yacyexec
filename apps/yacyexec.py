#!/usr/bin/python3
import sys # for arguments
import subprocess # To launch OS process
from time import sleep
import urllib.parse
import urllib.request
import os # for Popen
import re

# test = 'default via 172.17.0.1 dev eth0 \n172.17.0.0/16 dev eth0 proto kernel scope link src 172.17.0.3 \n'
# regex = r"/((?:[0-9]{1,3}\.){3}[0-9]{1,3})/"
# print("regexp=", re.findall(regex, test))
#
# print(ip)
# exit()

def get_ip_within_host():
  with subprocess.Popen(["/sbin/ip", "route"], stdout=subprocess.PIPE) as proc:
    returns = str(proc.stdout.read().decode('ascii'))
    print("returns=", returns)
    # return= b'default via 172.17.0.1 dev eth0 \n172.17.0.0/16 dev eth0 proto kernel scope link src 172.17.0.3 \n'
    ip = re.findall( r'default via ([0-9]+(?:\.[0-9]+){3}) dev', returns )
    return ip

def call_URL_with_auth(url, username, password):
    # Thanks https://stackoverflow.com/questions/44239822/urllib-request-urlopenurl-with-authentication
    # create a password manager
    print("url=", url)
    password_mgr = urllib.request.HTTPPasswordMgr() #HTTPPasswordMgrWithDefaultRealm()
    # Add the username and password.
    # If we knew the realm, we could use it instead of None.
    top_level_url = "url"
    #DigestDigestDigest
    realm="The YaCy access is limited to administrators. If you don't know the password, you can change it using <yacy-home>/bin/passwd.sh <new-password>"
    password_mgr.add_password(realm, top_level_url, username, password)
    handler = urllib.request.HTTPDigestAuthHandler(password_mgr)
    # create "opener" (OpenerDirector instance)
    opener = urllib.request.build_opener(handler)
    # use the opener to fetch a URL
    opener.open(url)
    # Install the opener.
    # Now all calls to urllib.request.urlopen use our opener.
    urllib.request.install_opener(opener)
    try:
        handle = urllib.request.urlopen(url)
        print("response=", handle.read())
    except(urllib.error.HTTPError, e):
        if hasattr(e, 'code'):
            if e.code != 200:
                print('We got an error')
                print(e.code)
                print(e.headers)

def call_URL(url):
    # Thanks https://stackoverflow.com/questions/44239822/urllib-request-urlopenurl-with-authentication
    # create a password manager
    print("url=", url)
    try:
        handle = urllib.request.urlopen(url)
        #print("response=", handle.read())
        print("CRAWL Successfully started")
    except:
        print("ERROR in call_URL : ", sys.exc_info()[0])

#
# def get_ip_within_host():
#     cmd = os.popen("/sbin/ip route")
#     print("cmd=",cmd)
#     #returns = cmd.readall()
#     returns = cmd
#
#     regex = r"/default via ((?:[0-9]{1,3}\.){3}[0-9]{1,3}) dev eth0/"
#     return re.findall(regex, returns)

#print("Hello from Python")
#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))
crawl_url = str(sys.argv[1])
print('URL:', crawl_url)

#subprocess.run(["ls", "-l"])  # doesn't capture output
#subprocess.run(["ls", "-l", "/iexec"])  # doesn't capture output

#subprocess.run(["cat", "/etc/hosts"])
#print('Script run as :')
#subprocess.run(["whoami"])
#myIP = get_ip_within_host()[0]
#myIP = "192.168.1.6"
myIP = "localhost"
print('IP : ', myIP)
#subprocess.run(["/sbin/ip","route"])

print('Run IPFS daemon')
#subprocess.Popen(["/usr/local/bin/ipfs", "daemon"])
print('Run YaCy')
subprocess.Popen(["/bin/sh","/opt/yacy_search_server/startYACY.sh"]) # , "-f"
print('Call index')
print('Sleep a bit')
sleep(10) # Really important te be sure that YaCy listen on 8090
#print('url to crawl', crawl_url)
#subprocess.run(["/usr/bin/curl", crawl_url])
print('curl yacy to start crawling')
yacy_param = "crawlingDomMaxPages=100&range=wide&intention=&sitemapURL=&crawlingQ=on&crawlingMode=url&crawlingURL="
yacy_param += crawl_url # urllib.parse.quote_plus()
yacy_param += "&crawlingFile=&mustnotmatch=&crawlingFile%24file=&crawlingstart=Neuen%20Crawl%20starten&mustmatch=.*&createBookmark=on&bookmarkFolder=/crawlStart&xsstopw=on&indexMedia=on&crawlingIfOlderUnit=hour&cachePolicy=iffresh&indexText=on&crawlingIfOlderCheck=on&bookmarkTitle=&crawlingDomFilterDepth=1&crawlingDomFilterCheck=on&crawlingIfOlderNumber=1&crawlingDepth=4"
print("yacy_param=", yacy_param)
#subprocess.run(["/usr/bin/curl", "http://172.17.0.3:8090"])
#subprocess.run(["/usr/bin/curl", "http://172.17.0.2:8090"])
#subprocess.run(["/usr/bin/curl", "http://172.17.0.1:8090"])

#subprocess.run(["/usr/bin/curl", "--anyauth", "-vD", "-u" ,"admin:docker" ,"http://"+myIP+":8090/Crawler_p.html?"+yacy_param])
#call_URL_with_auth("http://"+myIP+":8090/Crawler_p.html?"+yacy_param, "admin", "docker")
call_URL("http://"+myIP+":8090/Crawler_p.html?"+yacy_param) # ?"+yacy_param
print('STOP YaCy')
# retrieve the transaction token from the HTTP GET flavor of the URL
#		transactionToken=$(curl -sSfI --anyauth -u "$admin:$YACY_ADMIN_PASSWORD" "http://127.0.0.1:$port/$1" | grep X-YaCy-Transaction-Token: | awk {'printf $2'} | tr -d '[:space:]')
# send POST data including the transaction token
#		curl -sSf --anyauth -u "$admin:$YACY_ADMIN_PASSWORD" -d "$2&transactionToken=$transactionToken" "http://127.0.0.1:$port/$1" > /dev/null
subprocess.run(["/bin/sh","/opt/yacy_search_server/stopYACY.sh"])
print('Move index to /iexec')
# /IndexExport_p.html?indexdump=
#subprocess.run(["cp", "-ra", "/opt/yacy_search_server/DATA", "/iexec"])
print('Put index on IPFS')
#sleep(5)
