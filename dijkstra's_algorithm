import heapq
import requests
import os
import json
from math import pi
from itertools import islice
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.environ.get("GOOGLE_API_KEY")
CACHE_FILE="graph_cache.json"
GMAPS_URL="https://maps.googleapis.com/maps/api/distancematrix/json"
MAX_ORIGINS=25
MAX_DESTINATIONS=25
DISTANCE_THRESHOLD_KM=int(2 * pi * 100)

DEFAULT_CITIES=[
    "Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru",
    "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow",
    "Vijayawada", "Guwahati", "Visakhapatnam", "Bhopal", "Nagpur",
    "Patna", "Bhubaneswar", "Chandigarh", "Indore", "Surat",
]


def saveCache(graph, cities):
    with open(CACHE_FILE, "w") as f:
        json.dump({"cities": cities, "graph": graph}, f, indent=2)


def loadCache():
    if not os.path.exists(CACHE_FILE):
        return None, None
    try:
        with open(CACHE_FILE) as f:
            data=json.load(f)
        return data["graph"], data["cities"]
    except (json.JSONDecodeError, KeyError):
        print("Cache file corrupted, will rebuild.")
        return None, None


def chunk(lst, size):
    it=iter(lst)
    while True:
        batch=list(islice(it, size))
        if not batch:
            break
        yield batch


def getDistances(origins, destinations):
    graphPart={city: {} for city in origins}

    for oBatch in chunk(origins, MAX_ORIGINS):
        for dBatch in chunk(destinations, MAX_DESTINATIONS):
            parameters={
                "origins": "|".join(oBatch),
                "destinations": "|".join(dBatch),
                "key": API_KEY,
            }
            try:
                resp=requests.get(GMAPS_URL, parameters=parameters, timeout=10).json()
            except requests.RequestException as e:
                print(f"Network error: {e}")
                return None

            if resp.get("status") != "OK":
                print(f"API error: {resp.get('status')} — {resp.get('error_message', 'no details')}")
                return None

            for i, origin in enumerate(oBatch):
                for j, dest in enumerate(dBatch):
                    if origin == dest:
                        continue
                    try:
                        element=resp["rows"][i]["elements"][j]
                        if element["status"] != "OK":
                            continue
                        km=element["distance"]["value"] // 1000
                        if km <= DISTANCE_THRESHOLD_KM:
                            graphPart[origin][dest]=km
                    except (KeyError, IndexError) as e:
                        print(f"Warning: missing data for {origin} → {dest}: {e}")

    return graphPart


def buildFullGraph(cities):
    print(f"Building full graph for {len(cities)} cities (threshold: {DISTANCE_THRESHOLD_KM} km)...")
    part=getDistances(cities, cities)
    if part is None:
        return None
    print("Graph built.")
    return part


def addCities(graph, cityList, newCities):
    print(f"Fetching edges for {len(newCities)} new cities...")
    all_cities=cityList+newCities

    part1=getDistances(newCities,all_cities)
    if part1 is None:
        return None, None

    part2=getDistances(cityList,newCities)
    if part2 is None:
        return None, None

    for city in newCities:
        graph[city]=part1.get(city,{})

    for city in cityList:
        graph[city].update(part2.get(city,{}))

    return graph, all_cities


def dijkstra(graph, start):
    dist={node: float("inf") for node in graph}
    parent={node: None for node in graph}
    dist[start]=0
    pq=[(0,start)]

    while pq:
        cost, node=heapq.heappop(pq)
        if cost > dist[node]:
            continue
        for neighbor, weight in graph[node].items():
            newCost=cost + weight
            if newCost < dist[neighbor]:
                dist[neighbor]=newCost
                parent[neighbor]=node
                heapq.heappush(pq, (newCost, neighbor))

    return dist, parent


def getPath(parent, dest):
    path=[]
    visited=set()
    while dest is not None:
        if dest in visited:
            print("Warning: cycle detected in path.")
            break
        visited.add(dest)
        path.append(dest)
        dest=parent[dest]
    return path[::-1]


def clean(name):
    return name.strip().title()


def requireApiKey():
    if not API_KEY:
        print("This action requires a Google Maps API key.")
        print("Add it to a .env file as: GOOGLE_API_KEY=your_key_here")
        return False
    return True


graph, cityList=loadCache()

if graph is None:
    print(f"No cache found. Building default graph for {len(DEFAULT_CITIES)} cities...")
    if not requireApiKey():
        print("Cannot build graph without API key. Exiting.")
        exit(1)
    graph = buildFullGraph(DEFAULT_CITIES)
    if graph is None:
        print("Failed to build graph on startup.")
        cityList=DEFAULT_CITIES[:]
    else:
        cityList=DEFAULT_CITIES[:]
        saveCache(graph, cityList)
        print("Graph ready.\n")
else:
    print(f"Loaded graph from cache ({len(cityList)} cities).\n")

while True:
    print("1. Add Cities")
    print("2. Refresh Graph")
    print("3. Shortest Path")
    print("4. Show Cities")
    print("5. Exit")

    try:
        choice=int(input("Choice: "))
    except ValueError:
        print("Please enter a number between 1 and 5.\n")
        continue

    if choice == 1:
        if not requireApiKey():
            print()
            continue
        raw=input("Enter cities (comma-separated): ").split(",")
        new=[clean(c) for c in raw]
        new=list(dict.fromkeys(c for c in new if c not in cityList))
        if not new:
            print("All cities already in graph.\n")
            continue
        print(f"Adding: {', '.join(new)}")
        updated_graph, updated_cities = addCities(graph, cityList, new)
        if updated_graph is None:
            print("Could not expand graph.\n")
        else:
            graph=updated_graph
            cityList=updated_cities
            saveCache(graph, cityList)
            print(f"Graph updated. Now {len(cityList)} cities.\n")

    elif choice == 2:
        if not requireApiKey():
            print()
            continue
        print(f"Rebuilding graph for {len(cityList)} cities...")
        rebuilt=buildFullGraph(cityList)
        if rebuilt is None:
            print("Rebuild failed, keeping existing graph.\n")
        else:
            graph=rebuilt
            saveCache(graph, cityList)
            print("Graph rebuilt.\n")

    elif choice == 3:
        if graph is None:
            print("Graph unavailable. Use option 2 to rebuild.\n")
            continue
        print(f"Cities: {', '.join(cityList)}\n")
        src=clean(input("Source: "))
        dst=clean(input("Destination: "))
        if src not in graph or dst not in graph:
            print("City not found. Check spelling or add it with option 1.\n")
            continue
        if src == dst:
            print("Source and destination are the same — distance is 0 km.\n")
            continue
        dist, parent=dijkstra(graph, src)
        if dist[dst] == float("inf"):
            print(f"No road path found between {src} and {dst}.\n")
        else:
            path=getPath(parent, dst)
            print(f"\nDistance : {dist[dst]} km")
            print(f"Path     : {' → '.join(path)}")
            print(f"Intermediate Cities    : {len(path) - 1}\n")

    elif choice == 4:
        if not cityList:
            print("No cities in graph yet.\n")
        else:
            print(f"\nCities in graph ({len(cityList)}):")
            for i, city in enumerate(cityList, 1):
                print(f"  {i:>2}. {city}")
            print()

    elif choice == 5:
        print("Thank You.")
        break

    else:
        print("Invalid choice. Enter a number between 1 and 5.\n")
