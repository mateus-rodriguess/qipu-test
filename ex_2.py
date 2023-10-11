"""

Para todo aviador, é vital saber antes de qualquer vôo as condições meteorológicas dos aeródromos de partida ou de chegada, 
assim como a existência de cartas disponíveis e horários de nascer e pôr do sol. No Brasil, estas informações são disponibilizadas 
pelo site https://www.aisweb.aer.mil.br/.  Nesta página é possível encontrar links para cartas, horarios do sol e as informações 
de TAF e METAR, que são boletins meteorológicos codificados.

Escreva um código que leia no terminal o código ICAO qualquer de um aeródromo (SBMT = campo de marte, SBJD = aeroporto de jundiaí, etc...) e imprima na tela:

    As cartas disponíveis
    Os horários de nascer e pôr do sol de hoje
    A informação de TAF e METAR disponíveis

Vale ressaltar que estas informações devem ser obtidas em tempo real do site, através de SCRAPPING.
"""
from datetime import date

import requests
from bs4 import BeautifulSoup

base_url = "https://aisweb.decea.mil.br"


def get_taf_metar(cod_icao: str):
    response = requests.get(f"{base_url}/?i=aerodromos&codigo=SBGV")

    if response.status_code != 200:
        raise ("Error ao tentar pegar o taf e metar, tente um icao valido")
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        body = soup.find("div", {"class": "col-lg-4 order-sm-12"})

        p_list = body.find_all("p")
        if not p_list:
            return None
        return {"metar": p_list[-2].text, "taf": p_list[-1].text}
    except:
        raise ("Error ao tentar pegar o taf e metar, tente um icao valido")


def get_solar(cod_icao: str):
    data = {
        "icaocode": cod_icao,
        "dt_i": date.today().strftime("%d/%m/%Y"),
        "dt_f": date.today().strftime("%d/%m/%Y"),
        "busca": "D80CC0C2-E09F-4C2B-8215-82C2563314E7",
    }
    response = requests.post(f"{base_url}/?i=aerodromos&p=sol", data=data)

    if response.status_code != 200:
        raise ("Error ao tentar por e nascer do sol, tente um icao valido")

    soup = BeautifulSoup(response.content, "html.parser")

    try:
        solar_list = soup.find("table", {"class": "table table-striped mt-4"}).find_all(
            "td"
        )
    except:
        raise ("Error ao tentar por e nascer do sol, tente um icao valido")
    if not solar_list:
        return {}

    return {"nascer_solar": solar_list[2].text, "por_solar": solar_list[3].text}


def get_carts(cod_icao: str):
    data = {
        "icaocode": cod_icao,
        "tipo": "0",
        "carta": "",
        "pe": "0",
        "amdt": "0",
        "uso": "all",
        "busca": "B069F18E-29A2-4057-BB0C-1B9F8F9C9E94",
    }
    response = requests.get(f"{base_url}/?i=cartas", data=data)

    if response.status_code != 200:
        raise ("Error ao tentar pegar as cartas, tente um icao valido")

    soup = BeautifulSoup(response.content, "html.parser")

    try:
        table = soup.find("table", {"id": "datatable"})

        if not table:
            return {}

        url_list = []
        trs = table.find_all("tr")
        for tr in trs:
            if tr.find("a"):
                url_list.append(tr.find("a").get("href"))

        return url_list
    except:
        raise ("Error ao tentar pegar as cartas, tente um icao valido")


if __name__ == "__main__":
    cod_icao = input("Digite um codigo icao, exemplo SBGV: ")
    print(50 * "-")
    taf_metar = get_taf_metar(cod_icao)
    carts = get_carts(cod_icao)
    solar = get_solar(cod_icao)

    print(f"taf: {taf_metar['taf']}\nmetar: {taf_metar['metar']}\n")
    print("Cartas disponíveis:")
    print(carts)
    print(50 * "-")
    print(f"\nNascer solar: {solar['nascer_solar']}\nPor solar: {solar['por_solar']}")
