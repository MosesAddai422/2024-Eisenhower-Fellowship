#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:33:25 2024

@author: mosesodeiaddai
"""
## The code below highlights steps taken to execute Prim's algorith to generate an MST for city networks in two
#scenarios. In the first scenario, distance is used as cost, and in the second, demand is used as cost. 


import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

    
# Google Maps API key
API_KEY ='AIzaSyA3pjAhvu5oe-DMLg193CFM3unFaCUm9jo'

# List of cities
cities = [
    "New York, NY", "Los Angeles, CA", "Chicago, IL", "Houston, TX", "Phoenix, AZ",
    "Philadelphia, PA", "San Antonio, TX", "San Diego, CA", "Dallas, TX", "Jacksonville, FL",
    "Austin, TX", "Fort Worth, TX", "San Jose, CA", "Columbus, OH", "Charlotte, NC",
    "Indianapolis, IN", "San Francisco, CA", "Seattle, WA", "Denver, CO", "Oklahoma City, OK",
    "Nashville, TN", "Washington, DC", "El Paso, TX", "Las Vegas, NV", "Boston, MA",
    "Detroit, MI", "Portland, OR", "Louisville, KY", "Memphis, TN", "Baltimore, MD",
    "Milwaukee, WI", "Albuquerque, NM", "Tucson, AZ", "Fresno, CA", "Sacramento, CA",
    "Mesa, AZ", "Atlanta, GA", "Kansas City, MO", "Colorado Springs, CO", "Omaha, NE",
    "Raleigh, NC", "Miami, FL", "Virginia Beach, VA", "Long Beach, CA", "Oakland, CA",
    "Minneapolis, MN", "Bakersfield, CA", "Tulsa, OK", "Tampa, FL", "Arlington, TX",
    "Wichita, KS", "Aurora, CO", "New Orleans, LA", "Cleveland, OH", "Anaheim, CA",
    "Henderson, NV", "Orlando, FL", "Lexington, KY", "Stockton, CA", "Riverside, CA",
    "Corpus Christi, TX", "Irvine, CA", "Cincinnati, OH", "Santa Ana, CA"
]

# list to store the results
results = []
timeout = 120

# Looping through each pair of cities to calculate distances
for i in range(len(cities)):
    for j in range(i + 1, len(cities)):
        origin = cities[i]
        destination = cities[j]
        
        # Making the API call to the Distance Matrix API
        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origin}&destinations={destination}&key={API_KEY}"
        
        try:
            response = requests.get(url, timeout=timeout).json()
            print(f"Response for {origin} to {destination}: {response}")
            
            # Checking if the API returned a valid response
            try:
                distance = response['rows'][0]['elements'][0]['distance']['text']
                results.append({"City A": origin, "City B": destination, "Distance": distance})
            except (IndexError, KeyError):
                print(f"Error retrieving distance between {origin} and {destination}")
                results.append({"City A": origin, "City B": destination, "Distance": "Error"})
        
        except requests.exceptions.Timeout:
            print(f"Request timed out for {origin} to {destination}")
            results.append({"City A": origin, "City B": destination, "Distance": "Timeout"})
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            results.append({"City A": origin, "City B": destination, "Distance": "Error"})
        


# Creating a DataFrame and saving it to a CSV file
df = pd.DataFrame(results)
df.to_csv('city_distances.csv', index=False)

print("Distance data saved to 'city_distances.csv'")



## Prim's Algorithm with Distance
#Loading data

distx = pd.read_excel('/Users/mosesodeiaddai/Desktop/Spring 2024/Eisenhower/Excel Files/City Spreads_ref.xlsx')

newdist = distx.replace({'mi': '',',':''}, regex=True) #removing 'mi' from cells


selectc = newdist.iloc[0:,1:]
matdist = selectc.values

newdist.to_excel('modified_distances.xlsx', index=False)

matlist = matdist.tolist() #creating list of the matrix

#approach 2
#modified matrix
modist = pd.read_excel('/Users/mosesodeiaddai/Desktop/Spring 2024/Eisenhower/Excel Files/modified_distances.xlsx')
selectc = modist.iloc[0:,1:]
matdist = selectc.values


## Executing Prim's Algorithm
INF = 1000000

N = 64

G = matdist

zeros = [0]*64
selected_node = zeros

no_edge = 0

selected_node[0] = True


print("Edge : Weight\n")
while (no_edge < N - 1):

    minimum = INF
    a = 0
    b = 0
    for m in range(N):
        if selected_node[m]:
            for n in range(N):
                if ((not selected_node[n]) and int(G[m][n])):
                    if minimum > int(G[m][n]):
                        minimum = int(G[m][n])
                        a = m
                        b = n
    print(str(a) + "-" + str(b) + ":" + str(G[a][b]))
    selected_node[b] = True
    no_edge += 1

# Plotting graph 
T = nx.DiGraph()

edges = [
    ("New York", "Philadelphia", 94.3), ("Philadelphia", "Baltimore", 101.0),
    ("Baltimore", "Charlotte", 38.6), ("Charlotte", "Virginia Beach", 209.0),
    ("Virginia Beach", "Raleigh", 202.0), ("Raleigh", "Indianapolis", 166.0),
    ("New York", "Boston", 217.0), ("Indianapolis", "Atlanta", 246.0),
    ("Atlanta", "Nashville", 249.0), ("Nashville", "Louisville", 176.0),
    ("Louisville", "Lexington", 77.8), ("Lexington", "Cincinnati", 82.7),
    ("Cincinnati", "Columbus", 107.0), ("Cincinnati", "Indianapolis", 112.0),
    ("Columbus", "Cleveland", 143.0), ("Cleveland", "Detroit", 170.0),
    ("Indianapolis", "Chicago", 183.0), ("Chicago", "Milwaukee", 92.1),
    ("Nashville", "Memphis", 212.0), ("Milwaukee", "Albuquerque", 337.0),
    ("Atlanta", "Austin", 346.0), ("Austin", "Orlando", 141.0),
    ("Orlando", "Tampa", 84.2), ("Orlando", "Mia", 236.0),
    ("Milwaukee", "Omaha", 377.0), ("Omaha", "Kansas City", 186.0),
    ("Kansas City", "Wichita", 195.0), ("Wichita", "Oklahoma City", 161.0),
    ("Oklahoma City", "Tulsa", 108.0), ("Oklahoma City", "Fort Worth", 200.0),
    ("Fort Worth", "Arlington", 15.6), ("Arlington", "Dallas", 20.5),
    ("Fort Worth", "Houston", 190.0), ("Houston", "San Antonio", 79.4),
    ("San Antonio", "Corpus Christi", 144.0), ("Houston", "New Orleans", 162.0),
    ("New Orleans", "Colorado Springs", 348.0), ("Wichita", "Colorado Springs", 502.0),
    ("Colorado Springs", "Aurora", 68.4), ("Aurora", "Denver", 16.5),
    ("Colorado Springs", "Tucson", 379.0), ("Tucson", "Sacramento", 266.0),
    ("Sacramento", "Mesa", 320.0), ("Mesa", "Phoenix", 112.0),
    ("Phoenix", "Las Vegas", 19.8), ("Phoenix", "Henderson", 285.0),
    ("Henderson", "Riverside", 15.8), ("Riverside", "Anaheim", 236.0),
    ("Anaheim", "Long Beach", 37.3), ("Long Beach", "Irvine", 8.7),
    ("Irvine", "San Diego", 9.1), ("Anaheim", "Long Beach", 25.6),
    ("Long Beach", "New York", 24.6), ("Irvine", "San Diego", 84.9),
    ("New York", "Bakersfield", 113.0), ("Bakersfield", "Fresno", 109.0),
    ("Fresno", "Stockton", 126.0), ("Stockton", "Sacramento", 48.5),
    ("Stockton", "Oakland", 75.4), ("Oakland", "San Francisco", 12.3),
    ("Oakland", "San Jose", 40.5), ("Sacramento", "Portland", 579.0),
    ("Portland", "Seattle", 174.0)
]


T.add_weighted_edges_from(edges)

#drawing using various layouts. Only one needed
pos = nx.spring_layout(T, seed=42, k=0.5, iterations=100, scale=4)  # positions for all nodes
pos = nx.circular_layout(T) # spectral layout
pos = nx.kamada_kawai_layout(T,) #kamada layout
pos = nx.nx_agraph.graphviz_layout(T,prog='dot') #graphviz layout

plt.figure(figsize=(50, 35))
nx.draw_networkx_nodes(T, pos, node_size=500)
nx.draw_networkx_edges(T, pos, width=1.0, alpha=0.5)
nx.draw_networkx_labels(T, pos, font_size=10)
edge_labels = nx.get_edge_attributes(T, 'weight')
nx.draw_networkx_edge_labels(T, pos, edge_labels=edge_labels)
plt.title('Graph Visualization with City Names')


plt.savefig('prim_distance', dpi=800, bbox_inches='tight')
plt.show()



#Prim with Demand
demand = pd.read_excel('/Users/mosesodeiaddai/Desktop/Spring 2024/Eisenhower/Excel Files/Flight Demand Compile.xlsx')

#airport cities
airports = {
    "New York": ["JFK", "LGA"],
    "Los Angeles": ["LAX"],
    "Chicago": ["ORD", "MDW"],
    "Houston": ["IAH", "HOU"],
    "Phoenix": ["PHX", "AZA"],
    "Philadelphia": ["PHL"],
    "San Antonio": ["SAT"],
    "San Diego": ["SAN"],
    "Dallas": ["DFW"],
    "Jacksonville": ["JAX"],
    "Austin": ["AUS"],
    "San Jose": ["SJC"],
    "Columbus": ["CMH"],
    "Charlotte": ["CLT"],
    "Indianapolis": ["IND"],
    "San Francisco": ["SFO"],
    "Seattle": ["SEA"],
    "Denver": ["DEN"],
    "Oklahoma City": ["OKC"],
    "Nashville": ["BNA"],
    "Washington DC": ["DCA"],
    "El Paso": ["ELP"],
    "Las Vegas": ["LAS"],
    "Boston": ["BOS"],
    "Detroit": ["DTW"],
    "Portland": ["PDX"],
    "Louisville": ["SDF"],
    "Memphis": ["MEM"],
    "Baltimore": ["BWI"],
    "Milwaukee": ["MKE"],
    "Albuquerque": ["ABQ"],
    "Tucson": ["TUS"],
    "Fresno": ["FAT"],
    "Sacramento": ["SMF"],
    "Atlanta": ["ATL"],
    "Kansas City": ["MCI"],
    "Colorado Springs": ["COS"],
    "Omaha": ["OMA"],
    "Raleigh": ["RDU"],
    "Miami": ["MIA"],
    "Minneapolis": ["MSP"],
    "Tulsa": ["TUL"],
    "Tampa": ["TPA"],
    "Wichita": ["ICT"],
    "New Orleans": ["MSY"],
    "Cleveland": ["CLE"],
    "Orlando": ["MCO"],
    "Cincinnati": ["CVG"],
    "Santa Ana": ["SNA"]
}

#creating matrix for demand
cities = list(airports.keys())
table_df = pd.DataFrame(0, index=cities, columns=cities)


#
def get_city_from_airport(airport_code):
    for city, airport_list in airports.items():
        if airport_code in airport_list:
            return city
    return None

# Iterating through each column (origin city) and its destinations
for origin_city, dest_codes in demand.items():
    print(f"\nProcessing origin city: {origin_city}")
    
    # Converting destination codes to list and remove NA values
    dest_codes = dest_codes.dropna().tolist()
    
    # Iterating over each destination code
    for dest_code in dest_codes:
        dest_city = get_city_from_airport(dest_code)
        
        if dest_city:
            # Update the count in the table_df DataFrame
            table_df.loc[origin_city, dest_city] += 1
        else:
            print('not in airport keybook')


#new dataframe for demand
summed_df = table_df.copy()

# Iterating over the DataFrame to sum pairs
for city1 in table_df.columns:
    for city2 in table_df.index:
        if city1 != city2:
            # Sum the values from both perspectives
            summed_value = table_df.loc[city1, city2] + table_df.loc[city2, city1]
            summed_df.loc[city1, city2] = summed_value
            summed_df.loc[city2, city1] = summed_value

divsum = summed_df.applymap(lambda x: x // 12)

keyselect = divsum.iloc[0:,0:]
keydist = keyselect.values


#Executing Prim's algorithm with demand

INF = 1000000

N = 49

G = keydist

zeros = [0]*49
selected_node = zeros

no_edge = 0

selected_node[0] = True


print("Edge : Weight\n")
while (no_edge < N - 1):

    minimum = INF
    a = 0
    b = 0
    for m in range(N):
        if selected_node[m]:
            for n in range(N):
                if ((not selected_node[n]) and G[m][n]):
                    if minimum > G[m][n]:
                        minimum = G[m][n]
                        a = m
                        b = n
    print(str(a) + "-" + str(b) + ":" + str(G[a][b]))
    selected_node[b] = True
    no_edge += 1


#Plotting Graph
M = nx.DiGraph()

medges = [
    ("New York", "Los Angeles", 32), 
    ("Los Angeles", "Chicago", 29), 
    ("Chicago", "Houston", 18), 
    ("Houston", "Denver", 17), 
    ("Houston", "Tampa", 1), 
    ("Denver", "Milwaukee", 2), 
    ("Milwaukee", "Phoenix", 2), 
    ("Phoenix", "Philadelphia", 2), 
    ("Denver", "Sacramento", 2), 
    ("Tampa", "Colorado Springs", 2), 
    ("Tampa", "Tulsa", 3), 
    ("Tulsa", "Kansas City", 3), 
    ("Tulsa", "Raleigh", 3), 
    ("Colorado Springs", "Austin", 4), 
    ("Austin", "Albuquerque", 4), 
    ("Tampa", "Omaha", 6), 
    ("Austin", "Orlando", 8), 
    ("Omaha", "Washington DC", 9), 
    ("Washington DC", "Cleveland", 4), 
    ("Cleveland", "Charlotte", 3), 
    ("Charlotte", "Minneapolis", 2), 
    ("Minneapolis", "Fresno", 2), 
    ("Minneapolis", "San Antonio", 2), 
    ("San Antonio", "San Diego", 1), 
    ("San Diego", "Cincinnati", 4), 
    ("Cincinnati", "Baltimore", 4), 
    ("Charlotte", "Miami", 5), 
    ("Miami", "Louisville", 2), 
    ("Charlotte", "Los Angeles", 6), 
    ("Charlotte", "Santa Ana", 6), 
    ("Santa Ana", "Memphis", 5), 
    ("Cincinnati", "Nashville", 6), 
    ("Fresno", "Baltimore", 9), 
    ("Raleigh", "Wichita", 11), 
    ("Louisville", "New Orleans", 16), 
    ("Memphis", "Detroit", 17), 
    ("Minneapolis", "Miami", 17), 
    ("Miami", "Orlando", 16), 
    ("Sacramento", "Baltimore", 20), 
    ("Chicago", "Santa Ana", 21), 
    ("Baltimore", "Tucson", 22), 
    ("Omaha", "Portland", 23), 
    ("Philadelphia", "Tulsa", 33), 
    ("Minneapolis", "Atlanta", 35), 
    ("Santa Ana", "Cleveland", 35), 
    ("Nashville", "El Paso", 47), 
    ("Tulsa", "Jacksonville", 119), 
    ("Baltimore", "Jacksonville", 171)
]


M.add_weighted_edges_from(medges)

#drawing
pos = nx.spring_layout(M, seed=42, k=0.5, iterations=100, scale=4)  # positions for all nodes
pos = nx.circular_layout(M) # spectral layout
pos = nx.kamada_kawai_layout(M,) #kamada layout
pos = nx.nx_agraph.graphviz_layout(M,prog='dot') #graphviz layout

plt.figure(figsize=(50, 35))
nx.draw_networkx_nodes(M, pos, node_size=500)
nx.draw_networkx_edges(M, pos, width=1.0, alpha=0.5)
nx.draw_networkx_labels(M, pos, font_size=10)
edge_labels = nx.get_edge_attributes(M, 'weight')
nx.draw_networkx_edge_labels(M, pos, edge_labels=edge_labels)
plt.title('Graph Visualization with City Names')


plt.savefig('prim_demand', dpi=800, bbox_inches='tight')
plt.show()






