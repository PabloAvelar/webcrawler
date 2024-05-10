import requests
import re


def get_disallowed(robots_txt) -> list:
    # Buscando el user agent *
    user_agents = robots_txt.split("User-agent: ")
    disallow_re = re.compile(r"Disallow:\s*(.*)")

    my_user_agent = None
    for ua in user_agents:
        if len(ua) > 0 and ua[0] == '*':
            my_user_agent = ua
            break

    if my_user_agent is None:
        return []

    disallow_match = disallow_re.findall(my_user_agent)
    return disallow_match


def read_robots_txt(url):
    url_robots_txt = url.rstrip("/") + '/robots.txt'

    r = requests.get(url_robots_txt, verify=False)
    if r.status_code != 200:
        print("No se pudo recuperar robots.txt. Status code: " + str(r.status_code))
        return None

    disallowed = get_disallowed(r.text)

    return disallowed
