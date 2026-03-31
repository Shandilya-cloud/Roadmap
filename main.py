import ollama
import json

def get_weather(city):
    import requests

    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_res = requests.get(geo_url).json()

    if "results" not in geo_res:
        print("City not found")
        return

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    data = requests.get(weather_url).json()

    temp = data["current_weather"]["temperature"]
    wind = data["current_weather"]["windspeed"]

    return f"{city}: {temp}°C, Wind speed {wind} km/h"


system_prompt = """
You are a helpful Assistant which will help to perform task told by the user. There are some tools avalable also to get weather details,
So that if asked you can directly get from the tool get_weather.

rules:
you have to return in the same json format only:
{"STEP": "START | PLAN | TOOL | OBSERVE | OUTPUT", "content":content}

example:
Q>> What is the weather of Delhi?
{"STEP": START, "content": We need to tell the current weather of Delhi}
{"STEP": PLAN, "content":Do we have any tool for that?}
{"STEP": PLAN, "content": Yes we have get_weather tool for that}
{"STEP": TOOL, "tool":get_weather, "INPUT": Delhi}
{"STEP": OBSERVE, "content":The Weather is 27 C with rain}
{"STEP": PLAN, "content":The current weather of Delhi is Rainy with 27 c temperature}
{"STEP": OUTPUT, "content":The current weather of Delhi is Rainy with 27 c temperature}

Q>> What is 2+2?
{"STEP": START, "content": I need to add 2 with 2}
{"STEP": PLAN, "content": Is there any tool regarding that?}
{"STEP": PLAN, "content": No, I have to do it myself}
{"STEP": SOLUTION, "content": On ADDING  2+2 = 4}
{"STEP": OUTPUT, "content": The sum of 2 + 2 = 4}
"""
messages = [{"role": "SYSTEM", "content": system_prompt}]
while True:
    user_input = input(">>")
    messages.append({"role":"USER", "content":user_input})
    response = ollama.chat(
        model='gemma3:1b',  # or mistral, gemma, etc.
        messages=messages
    )

    llm_response = {"content": response['message']['content']}

    if llm_response.get("tool") == "get_weather":
        content = get_weather(llm_response.get("INPUT"))
        messages.append({"role":"DEVELOPER", "content": content})
    else:
        messages.append({"role":"ASSISTANT", "content": llm_response.get('content')})
    print(llm_response)

        
