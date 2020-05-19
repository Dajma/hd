#!/usr/bin/env python
import requests
import yaml
import sys
import os

JENKINS_URL = os.environ['JENKINS_URL']
print(JENKINS_URL)

SITE = "192.168.2.102" if  JENKINS_URL == "https://jenkins.dev-gcp.homedepot.ca/" else "https://jenkins.qa-gcp.homedepot.ca/"
print(SITE)
exit()
# only change below two lines
#SITE="ec2-3-21-245-10.us-east-2.compute.amazonaws.com"
#SITE="192.168.2.102"
INDEX_FILE='index.yaml'
CHARTS_TO_KEEP=6

# URLS and APIS
ROOT_FILE_URL='http://{site}/{filename}'
DELETE_API="http://{site}/api/charts/{name}/{version}"


# function to get index file
def get_file(filename):
    try:
        response=requests.get(ROOT_FILE_URL.format(site=SITE,filename=filename))
        if response.status_code==200:
            print(u'\u2705',"File {0} downloaded succesfully".format(filename))
        else:
            print(u'\u274c',"File {0} could not be downloaded succesfully".format(filename))
            sys.exit(0)
        return response.text
    except:
        print(u'\u274C',"ERROR: Oops!",sys.exc_info()[0],"occured.")
        sys.exit(0)


# function to delete chart version by name
def delete_chart_version(name,version):
    try:
        response=requests.delete(DELETE_API.format(site=SITE,name=name,version=version))
        return response
    except:
        print(u'\u274C',"ERROR: Oops!",sys.exc_info()[0],"occured.")



def main():
    # maintain counts of total successfully deleted packages
    count=0    

    # requesting index file
    print("Getting {0} file...".format(INDEX_FILE))
    index=get_file(filename=INDEX_FILE)

    # parsing yaml contents of index file
    contents=yaml.load(index, Loader=yaml.FullLoader)

    # loops for each package entry and getting each package version
    for pkg_name , pkg_versions in contents['entries'].items():
        # sort the package versions by version number in descending order
        pkg_versions_sorted=sorted(pkg_versions, key=lambda pkg_version:pkg_version["version"],reverse=True)

        # start deleting all versions except the first three
        for i in range(CHARTS_TO_KEEP,len(pkg_versions_sorted)):
            # getting the name of the version
            name=pkg_versions_sorted[i]['name']
            # getting the version 
            version=pkg_versions_sorted[i]['version']

            print("Deleting {1} from package: {0}".format(name,version))
            response=delete_chart_version(name,version)
            if response.status_code==200:
                print(u'\u2705',"Version {1} deleted succesfully from package: {0}".format(name,version))
                # increments the count
                count+=1
            else:
                print(u'\u274c',"Version {1} could not be deleted succesfully from package: {0}".format(name,version))
        
    print("Total {count} packages deleted successfully".format(count=count))

if __name__ == '__main__':
    try:
        main()
    except:
        print(u'\u274C',"ERROR: Oops!",sys.exc_info()[0],"occured.")
        sys.exit(0)
