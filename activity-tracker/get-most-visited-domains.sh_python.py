import tldextract
import os

def extract_domain(url):
    extracted = tldextract.extract(url)
    if extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"
    else:
        return extracted.domain  # fallback for localhost or IPs

def ape_extract_domain(url):
    httpsIndex = url.find("https://") 
    httpIndex = url.find("http://") 
    if httpsIndex == 0:
        url = url[len("https://"):]
    elif httpIndex == 0:
        url = url[len("http://"):]
    slashIndex = url.find("/")
    if slashIndex != -1:
        url = url[:slashIndex]
    return url


with open(os.getenv("SCRIPTS_DIR") + "/activity-tracker/focused_webpage_log.tsv", "r") as f:
    for line in f.readlines():
        if len(line) > 16:
            tabIndex = line.find("\t")
            print( ape_extract_domain(line[: tabIndex]) + line[tabIndex:], end='')
