import requests
import urllib.parse

api_key = "a0dc27e8-22aa-4e65-a1ad-3e6cb3e2c1c8"
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

while True:
    origen = input("\nIngrese Ciudad de Origen en Chile (o 's' para salir): ")
    if origen.lower() == 's':
        break
    destino = input("Ingrese Ciudad de Destino en Argentina (o 's' para salir): ")
    if destino.lower() == 's':
        break
    
    print("Opciones de transporte: car, bike, foot")
    vehiculo = input("Elija el medio de transporte: ").lower()

    orig_data = requests.get(geocode_url + urllib.parse.urlencode({"q": origen, "limit": "1", "key": api_key})).json()
    dest_data = requests.get(geocode_url + urllib.parse.urlencode({"q": destino, "limit": "1", "key": api_key})).json()

    if "hits" in orig_data and "hits" in dest_data and len(orig_data["hits"]) > 0 and len(dest_data["hits"]) > 0:
        orig_lat = orig_data["hits"][0]["point"]["lat"]
        orig_lng = orig_data["hits"][0]["point"]["lng"]
        dest_lat = dest_data["hits"][0]["point"]["lat"]
        dest_lng = dest_data["hits"][0]["point"]["lng"]


        query = f"point={orig_lat},{orig_lng}&point={dest_lat},{dest_lng}&profile={vehiculo}&locale=es&key={api_key}"
        ruta = requests.get(route_url + query).json()

        if "paths" in ruta:
            distancia_km = ruta["paths"][0]["distance"] / 1000
            distancia_mi = distancia_km * 0.621371
            tiempo_ms = ruta["paths"][0]["time"]
            horas = int(tiempo_ms / (1000 * 60 * 60))
            minutos = int((tiempo_ms % (1000 * 60 * 60)) / (1000 * 60))

            print(f"\n--- Resumen del Viaje ---")
            print(f"Distancia: {distancia_km:.2f} km / {distancia_mi:.2f} millas")
            print(f"Duración estimada: {horas} horas y {minutos} minutos")
            print("Narrativa del viaje:")
            for instruccion in ruta["paths"][0]["instructions"]:
                print(f"- {instruccion['text']} ({instruccion['distance']/1000:.2f} km)")
        else:
            print("\nNo se pudo calcular la ruta.")
            print("Mensaje de la API:", ruta.get("message", "Error desconocido"))
    else:
        print("No se encontraron las ciudades especificadas.")