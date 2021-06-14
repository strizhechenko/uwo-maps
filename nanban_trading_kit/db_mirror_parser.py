from covid.utils import url2soup
import json

EA = {
    'japan': 'http://uwodbmirror.ivyro.net/eg/main.php?id=85000037',
    'china': 'http://uwodbmirror.ivyro.net/eg/main.php?id=85000038',
    'korea': 'http://uwodbmirror.ivyro.net/eg/main.php?id=85000036',
    'taiwan': 'http://uwodbmirror.ivyro.net/eg/main.php?id=85000039'
}

result = {}
for origin, url in EA.items():
    soup = url2soup(url)
    for item in soup.find_all('ul', attrs={'class': 'unli0'}):
        if 'Name' in (field.text for field in item.find_all('li')):
            continue
        name = item.find('li', attrs={'class': 'item3'}).text.strip().split()
        if name[-1].isdigit():
            name = " ".join(name[:-1])
        else:
            name = " ".join(name)
        if name not in result:
            result[name] = {'origin': origin, 'sell': {}}
        best = []
        best.extend(item.find_all('img', attrs={'src': 'http://silvermoon.ivyro.net/UI/skill0.png'}))
        best.extend(item.find_all('img', attrs={'src': 'http://silvermoon.ivyro.net/UI/skill1.png'}))
        result[name]['sell'].update({
            img.attrs['title']: int(best[0].parent.text.replace(',', '')) for img in best
        })

print(json.dumps(result, indent=2))
