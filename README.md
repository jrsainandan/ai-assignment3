RouteGraph
A Distance-Based Pathfinding System using Dijkstra’s Algorithm
Overview
RouteGraph is a Python-based system that finds the shortest path between cities using real-world distance data from the Google Distance Matrix API. It models cities as nodes in a graph and uses Dijkstra’s Algorithm to compute the most efficient route.

Features
Fetches real-time distance data using Google Maps API
Implements Dijkstra’s algorithm for shortest path
Graph-based representation of cities and routes
Optimized API usage with batching
Local caching using JSON to reduce API calls
Dynamic addition of new cities
Multi-hop path discovery (not just direct routes)
How It Works
Cities are treated as nodes in a graph
Distances between cities are fetched via API
Edges are created only if distance ≤ threshold
Dijkstra’s algorithm computes shortest path
Project Structure
.
├── indian_pathSearcher.py
├── graph_cache.json (auto-generated)
├── .env (not included)
Setup Instructions
1. Install dependencies
pip install requests python-dotenv

2. Add your API key
Create a .env file: GOOGLE_API_KEY=your_api_key_here

Example Output
Distance : 1410 km Path : Hyderabad → Pune Intermediate Cities : 1

Conclusion
RouteGraph demonstrates how real-world data and graph algorithms can be combined to build a practical pathfinding system.
