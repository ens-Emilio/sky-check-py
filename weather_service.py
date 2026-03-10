import requests
import config

def get_weather(city: str) -> dict:
    """Faz a chamada à API do OpenWeatherMap e retorna o JSON bruto ou lança exceção."""
    if not config.API_KEY:
        raise ValueError("Chave de API não configurada no arquivo .env")

    params = {
        "q": city,
        "appid": config.API_KEY,
        "units": config.UNITS,
        "lang": config.LANG
    }

    try:
        response = requests.get(config.BASE_URL, params=params, timeout=config.TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            raise ValueError(f"Cidade '{city}' não encontrada.")
        elif response.status_code == 401:
            raise ValueError("Chave de API inválida. Verifique o arquivo .env ou aguarde a ativação (pode levar até 2h para novas chaves).")
        else:
            raise Exception(f"Erro na API: {e}")
    except requests.exceptions.ConnectionError:
        raise Exception("Sem conexão com a internet.")
    except Exception as e:
        raise Exception(f"Ocorreu um erro inesperado: {e}")

def parse_weather(data: dict) -> dict:
    """Extrai apenas os campos relevantes do JSON bruto da API."""
    try:
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temp": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "icon_code": data["weather"][0]["icon"],
            "wind_speed": round(data["wind"]["speed"] * 3.6),  # Convertendo m/s para km/h
        }
    except (KeyError, IndexError) as e:
        raise Exception(f"Erro ao processar os dados da API: {e}")
