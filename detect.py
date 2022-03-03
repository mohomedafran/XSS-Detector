import os

os.system('clear')


m = """

    )  (    (         (                                         )   (     
 ( /(  )\ ) )\ )      )\ )         *   )        (     *   )  ( /(   )\ )  
 )\())(()/((()/(     (()/(   (   ` )  /( (      )\  ` )  /(  )\()) (()/(  
((_)\  /(_))/(_))___  /(_))  )\   ( )(_)))\   (((_)  ( )(_))((_)\   /(_)) 
__((_)(_)) (_)) |___|(_))_  ((_) (_(_())((_)  )\___ (_(_())   ((_) (_))   
\ \/ // __|/ __|      |   \ | __||_   _|| __|((/ __||_   _|  / _ \ | _ \  
 >  < \__ \\__ \       | |) || _|   | |  | _|  | (__   | |   | (_) ||   /  
/_/\_\|___/|___/      |___/ |___|  |_|  |___|  \___|  |_|    \___/ |_|_\  """

print('\033[1;31;40m'+m)
print('\033[1;33;40m                                 Coded By PHOENIX ᵒʷⁿᵉʳ ᵒᶠ ᵖʰᵒᵉⁿⁱˣ ˢᵠᵘᵃᵈ')
print('\033[1;35;40m')
    


import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:

            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)


def scan_xss(url):
    forms = get_all_forms(url)
    print('\033[1;32;40m')
    print(f"[+] Detected {len(forms)} forms on {url}.")
    js_script = "<Script>alert('hi')</scripT>"
    is_vulnerable = False

    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            print('\033[1;32;40m')
            print(f"[+] XSS Detected on {url}")
            print(f"[*] Form details:")
            print('\033[1;33;40m')
            pprint(form_details)
            is_vulnerable = True
            print('\033[1;36;40m')
            
    return is_vulnerable


if __name__ == "__main__":
    url = input("\033[1;34;40mEnter The URL (ex: https://site.com) : \033[1;00;40m")
    print(scan_xss(url))
    

print('\033[1;00;40m')