
#This code implements Dijkstra's algorithm to find the shortest path in a graph.
#Simply its a graph represented as a dictionary where keys are node names
#Values are lists of tuples (neighbor, weight).
#It works by initializing distances to infinity, setting the start node distance to 0,
#You can test your function by changing the graph or the start node.
my_graph = {
    'A': [('B', 5), ('C', 3), ('E', 11)],
    'B': [('A', 5), ('C', 1), ('F', 2)],
    'C': [('A', 3), ('B', 1), ('D', 1), ('E', 5)],
    'D': [('C', 1), ('E', 9), ('F', 3)],
    'E': [('A', 11), ('C', 5), ('D', 9)],
    'F': [('B', 2), ('D', 3)]
}

#This function has graph and start which is the starting node
def shortest_path(graph, start,target=""):
    unvisited = list(graph)
    distances = {node: 0 if node == start else float('inf') for node in graph}
    paths = {node: [] for node in graph}

    #Use the .append() method to append start to the paths[start] list.
    #This appends the start node to the path for the start node.
    #append is a method that adds an element to the end of a list.
    paths[start].append(start)

    #The while loop continues until all nodes have been visited.
    while unvisited:

        #Find the current node with the smallest distance value.
        current = min(unvisited, key=distances.get)

        #Goes through the distances for the current node in
        for node, distance in graph[current]:

            #This works by checking if the node is in unvisited.
            #By checking distance + distances[current] < distances[node]
            if distance + distances[current] < distances[node]:

                #If it is, update the distance and path for that node.
                #The math works by adding the distance to the current node
                distances[node] = distance + distances[current]

                #The path to node is the path to current, then take one more step to node.
                paths[node] = paths[current] + [node]

        #Terminate the while loop by removing the current node from the unvisited list.
        #You do this because you have visited the current node.
        #This is a way to keep track of which nodes have been visited.
        unvisited.remove(current)

    # Set targets_to_print to [target] if given, otherwise default to all graph nodes
    targets_to_print = [target] if target else graph
    #for loop to iterate through the targets_to_print list.
    for node in targets_to_print:
        #Print the shortest path and distance for each target node.
        if node == start:
            continue
        print(f'\n{start}-{node} distance: {distances[node]}\nPath: {" -> ".join(paths[node])}')

    #Now I must return the distances and paths dictionaries.
    return distances, paths


#This allows you to test the function by changing the graph or the start node.
#Example usage:
shortest_path(my_graph, 'A', 'F')