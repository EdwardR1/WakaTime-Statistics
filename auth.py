#!/usr/bin/env python
import datetime
import hashlib
import os
import sys
import json
from rauth import OAuth2Service
from dateinformation import isLeapYear, calcDays, monthFormat, monthDates, getDateDetails, numToMonth


def getCodes(codesFile):
    """ Get secret codes from json file """
    codes = {}
    try:
        with open(codesFile) as f:
            codes = json.load(f)
    except FileNotFoundError:
        print("File not found! Creating template file!")
        f = open(codesFile, 'w')
        f.write("\{\n")
        f.write("\t\"client_id\":\"\",\n")
        f.write("\t\"secret\":\"\",\n")
        f.write("\t\"api_key\":\"\"\n")
        f.write("\}\n")
        return -1
    finally:
        return codes


def writeToFile(month, dataStream):
    """ Write the output to a file with the name of the month"""
    f = open("data/%s.json" % numToMonth(month), "w")
    f.write(dataStream)
    f.close()
    print(numToMonth(month).capitalize(), "written")


def auth():
    """Authenticate the information and send it to the right places
    """
    if sys.version_info[0] == 3:
        raw_input = input

    codes = getCodes("codes.json")
    if(codes == -1):
        print("Failed!")
        exit(1)
    client_id = codes["client_id"]
    secret = codes["secret"]
    api_key = codes["api_key"]

    service = OAuth2Service(
        client_id=client_id,
        client_secret=secret,
        name='wakatime',
        authorize_url='https://wakatime.com/oauth/authorize',
        access_token_url='https://wakatime.com/oauth/token',
        base_url='https://wakatime.com/api/v1/')

    redirect_uri = 'https://wakatime.com/oauth/test'
    state = hashlib.sha1(os.urandom(40)).hexdigest()
    params = {'scope': 'email,read_stats',
              'response_type': 'code',
              'state': state,
              'redirect_uri': redirect_uri}

    url = service.get_authorize_url(**params)

    print('**** Visit this url in your browser ****'.format(url=url))
    print('*' * 80)
    print(url)
    print('*' * 80)
    print('**** After clicking Authorize, paste code here and press Enter ****')
    code = raw_input('Enter code from url: ')

    # Make sure returned state has not changed for security reasons, and exchange
    # code for an Access Token.
    headers = {'Accept': 'application/x-www-form-urlencoded'}
    print('Getting an access token...')
    session = service.get_auth_session(headers=headers,
                                       data={'code': code,
                                             'grant_type': 'authorization_code',
                                             'redirect_uri': redirect_uri})

    print('Getting current user from API...')
    user = session.get('users/current').json()
    print('Authenticated via OAuth as {0}'.format(user['data']['email']))
    print("Getting user's coding stats from API...")

    year = getDateDetails()["year"]
    currentMonth = int(getDateDetails()["month"])
    monthData = {}
    for i in range(1, currentMonth + 1):
        jsonObj = session.get("users/current/summaries?start=%s&end=%s&api_key=%s" % (
            monthDates(i, int(year))["start"], monthDates(i, int(year))["end"], api_key))
        monthData = jsonObj.text
        writeToFile(i, monthData)


def main():
    auth()


if(__name__ == "__main__"):
    main()
