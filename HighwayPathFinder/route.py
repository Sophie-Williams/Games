import sys
import time
import heapq
from math import sqrt, sin, cos,atan2,radians

"""
Read me:
input             : python route.py [start-city] [end-city] [routing-option] [routing-algorithm]
expected output   : [total-distance-in-miles] [total-time-in-hours] [start-city] [city-1] [city-2] ... [end-city]
program flow: main >> solve > bfs/dfs/ids/astar > get_successors >> backtrack
Todo 1. astar 2. time/distance/scenic

State: 
 Each Node or city is a state
Goal State: 
 End City Node
Successor:
 Each edge is a new city
Cost Function: 
 For segment, cost is uniform.
 For distance, cost is the distance of the edge
 For time, cost is the distance divided by the speed limit of the edge
 For scenic, cost is function of distance. If speed limit of an edge is less than 55 then it is uniform. For speed limit greater than or equal to 55, its the distance of the edge
Heuristic function   :
 For scenic and segment, I have assumed Heuristic function as zero
 For distance, I have used Haversine's formula for calculating the distance between the gps points
 For time, I have used Distance divided by Speed_limit, where distance is calculated through Haversine's formula
Assumptions:
 1. For scenic, if speed is empty then I have considered the edge as inconsistent data
 2. For Distance, if distance is zero or empty then I have considered the edge as inconsistent data
 3. For time, if distance or time is zero or empty then I have considered the edge as inconsistent data

1. Which algorithm works best for each routing options ?
    bfs and ids - finds the optimal path for segment routing options
    dfs - not applicable 
    astar - finds optimal path for segment, ditance, time and scenic
2. Which algorithm is faster in terms of the amount of computation time required by your program and by how much according to your experiments ? (Include Loops in your program)
    astar - gives quickly calculated optimal path for segment, distance, time and scenic
    bfs - is faster and gives optimal path for segments
3. Which algorithm requires least memory and how much according to your program
    Both Dfs and IDS requires least memory
4. Which Heruistic Function have you used and how might you make it better
    I have used Haversine formula as the Heruistic function. Haversine formula is the equivalent for euclidean distance on a globe.
5. Supposing you start in Bloomington, which city should you travel to if you want to take the longest possible drive that is still the shortest path to that city? (Which city is furthest from Bloomington)
   Skagway,_Alaska is the furthest city from bloomington. It is 4826 miles from bloomington. It was calculated using A* star algorithm by using furthestCity() method. Basically I have iterated each city in the list to find the furthest city (sanity-checked with Google Maps)
"""


#Global Variables
start_time = time.time()
routing_option = ('segment','distance','time','scenic')
routing_algorithm = ('bfs','dfs','ids','astar')
road_segments_file = "road-segments.txt"
city_gps_file = "city-gps.txt"
fhand = open(road_segments_file)
road_segment_data = fhand.read()
road_segment_data_len = len(road_segment_data)
fhand = open(city_gps_file)
city_gps_data = fhand.read()
city_gps_data_len = len(city_gps_data)
global_speed_limit= 0

# order: [(-1, 0, 'a'), (0, 1, 'b'), (1, 2, 'c')]
# Defined custom Priority Queue based on https://docs.python.org/2/library/heapq.html, for debugging purpose
class PriorityQueue:
    def __init__(self):
        self.queue = list()
        self.index = 0
     
    def push(self,priority,node):
        heapq.heappush(self.queue, (priority,self.index,node))
        self.index = self.index + 1
         
    def pop(self):
        return heapq.heappop(self.queue)[-1]

# Route class is used for grouping the data together    
class Route:
    visited_city = list()
    def __init__(self,from_city,to_city,distance,speed_limit,name):
        self.from_city = from_city 
        self.to_city = to_city 
        self.distance = distance 
        self.speed_limit = speed_limit
        self.name = name
        self.parent = None
        self.predecessor_list=list()
        self.depth= 0
        self.time = 0
        self.scenic = 0
        self.total_distance=0
        self.total_time = 0

    def get_route_desc(self):
        return str(self.from_city) +"--"+str(self.to_city) +"--"+str(self.distance) +"--"+str(self.speed_limit) +"--"+str(self.name) +"--"+str(self.depth)
# To get the elapsed run time
def run_time():
    return str(time.time() - start_time)
 
# To check for goal state
def is_goal(start_city,end_city):
    return start_city == end_city

# To Calculate eculidean Distance
def calculate_distance(x,y,a,b):
    return sqrt((float(x)-float(a))**2 + (float(y)-float(b))**2)

# Used for calculating the heruistic function for time route option
# To make the heruistic function optimal - Max speed limit is required
def get_max_speed_limit():
    global global_speed_limit
    for line in road_segment_data.split("\n"):
        if (line != ""):
            (from_city, to_city, distance, speed_limit, name) = line.split(" ")
            if(speed_limit!= ""):
                if(global_speed_limit < speed_limit ):
                    global_speed_limit = speed_limit

# To Calculate the distance between to GPS points - Haversine's Formula
def calculate_gps_distance(x,y,a,b):
    lon1=radians(y)
    lon2=radians(b)
    lat1=radians(x)
    lat2=radians(a)
    #Radius of the earth
    R = 3961
    lon = lon2 - lon1 
    lat = lat2 - lat1 
    
    a = (sin(lat/2))**2 + cos(lat1) * cos(lat2) * (sin(lon/2))**2 
    c = 2 * atan2( sqrt(a), sqrt(1-a) ) 
    d = R * c
    return d

# Utility Method for printing the successor Lst
def print_successors_lst(successors):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    temp = list()
    for s in successors:
        temp.append(s.get_route_desc())
    print temp
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    
# Utility Method for Printing the priority queue
def print_priority_queue(successors):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    for s in successors:
        print str(s[0])+" "+ str(s[1]) +" "+ s[2].get_route_desc()
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"

# For generating the successors for segement routing options
def get_successors_segment(parent,algorithm):
#     print "get_successors_segment - start: " + run_time() 
    successors = list()
    data = extract_segment_data(parent.to_city)
    temp_lst = list()
    for road_segment in data:
        (from_city, to_city, distance, speed_limit, name) = road_segment.split(" ")
        temp = Route(from_city, to_city, distance, speed_limit, name)
        temp_lst.append(temp);
        to_city_chk = (to_city not in Route.visited_city and parent.to_city == from_city and from_city not in parent.predecessor_list)
        from_city_chk = (from_city not in Route.visited_city and parent.to_city == to_city and to_city not in parent.predecessor_list)
        if(algorithm == "ids"):
            to_city_chk = (parent.to_city == from_city and from_city not in parent.predecessor_list);
            from_city_chk= (parent.to_city == to_city and to_city not in parent.predecessor_list)
        if(distance !="" and speed_limit!=""):
            if(to_city_chk):
                child = Route(from_city, to_city, distance, speed_limit, name)
                child.parent = parent #for Backtracking
                child.predecessor_list = list(parent.predecessor_list)
                child.predecessor_list.append(parent.to_city)
                child.depth = parent.depth + 1
                Route.visited_city.append(to_city)
                successors.append(child)
            elif (from_city_chk):
                child = Route(to_city, from_city, distance, speed_limit, name)
                child.parent = parent
                child.predecessor_list = list(parent.predecessor_list)
                child.predecessor_list.append(parent.to_city)
                child.depth = parent.depth + 1
                Route.visited_city.append(from_city)
                successors.append(child)
    return  successors

# For generating the successors for scenic routing options
def get_successors_scenic(parent):
#     print "get_successors_scenic - start: " + run_time() 
    successors = list()
    data = extract_segment_data(parent.to_city)
    for road_segment in data:
        (from_city, to_city, distance, speed_limit, name) = road_segment.split(" ")
        if(speed_limit !=""):
            if(to_city not in Route.visited_city and parent.to_city == from_city and from_city not in parent.predecessor_list):
                child = Route(from_city, to_city, distance, speed_limit, name)
                if(parent.from_city != child.to_city):
                    Route.visited_city.append(to_city)
                    child.parent = parent #for Backtracking
                    child.predecessor_list = list(parent.predecessor_list)
                    child.predecessor_list.append(parent.to_city)
                    speed_limit_no = float(child.speed_limit)
                    if( speed_limit_no >= 55):
                        child.scenic = float(child.distance) + float(parent.scenic)
                    else:
                        child.scenic = float(parent.scenic)
                    successors.append(child)
    #             else:
    #                     print (parent.from_city,parent.to_city,from_city,to_city)
    #                     print "!!!!Skipped - already added"
            elif (from_city not in Route.visited_city and parent.to_city == to_city and to_city not in parent.predecessor_list):
                child = Route(to_city, from_city, distance, speed_limit, name)
                if(parent.from_city != child.to_city):
                    Route.visited_city.append(from_city)
                    child.parent = parent
                    child.predecessor_list = list(parent.predecessor_list)
                    child.predecessor_list.append(parent.to_city)
                    speed_limit_no = float(child.speed_limit)
                    if( speed_limit_no >= 55):
                        child.scenic = float(child.distance) + float(parent.scenic)
                    else:
                        child.scenic = float(parent.scenic)
                    successors.append(child)
    #             else:
    #                     print (parent.from_city,parent.to_city,from_city,to_city)
    #                     print "!!!!Skipped - already added"
    return  successors

# For generating the successors for time routing option
def get_successors_time(parent):
#     print "get_successors_segment - start: " + run_time() 
    successors = list()
    data = extract_segment_data(parent.to_city)
#     print "data"
#     print data
    for road_segment in data:
        (from_city, to_city, distance, speed_limit, name) = road_segment.split(" ")
        if(distance !="" and distance != "0" and speed_limit!="" and speed_limit != "0"):
            if(to_city not in Route.visited_city and parent.to_city == from_city and from_city not in parent.predecessor_list):
                child = Route(from_city, to_city, distance, speed_limit, name)
                if(parent.from_city != child.to_city):
                    Route.visited_city.append(to_city)
                    child.parent = parent #for Backtracking
                    child.predecessor_list = list(parent.predecessor_list)
                    child.predecessor_list.append(parent.to_city)
                    child.time = float(child.distance)/float(child.speed_limit)
                    child.total_time = float(parent.total_time) + child.time
                    child.total_distance = float(parent.total_distance) + float(child.distance)           
                    successors.append(child)
            elif (from_city not in Route.visited_city and parent.to_city == to_city and to_city not in parent.predecessor_list):
                child = Route(to_city, from_city, distance, speed_limit, name)
                if(parent.from_city != child.to_city):
                    Route.visited_city.append(from_city)
                    child.parent = parent
                    child.predecessor_list = list(parent.predecessor_list)
                    child.predecessor_list.append(parent.to_city)
                    child.time = float(child.distance)/float(child.speed_limit)
                    child.total_time = float(parent.total_time) + child.time
                    child.total_distance = float(parent.total_distance) + float(child.distance)
                    successors.append(child)
    return  successors

# For generating the successors for Distance routing option
def get_successors_distance(parent):
#     print "get_successors_distance - start: " + run_time() 
    successors = list()
    data = extract_segment_data(parent.to_city)
#     print ("data::",data)
#     print (parent.predecessor_list)
    for road_segment in data:
        (from_city, to_city, distance, speed_limit, name) = road_segment.split(" ")
        if(distance !="" and distance != "0"):
            if(to_city not in Route.visited_city and parent.to_city == from_city and from_city not in parent.predecessor_list):
#             if(parent.to_city == from_city):
                child = Route(from_city, to_city, distance, speed_limit, name)
                
                if(parent.from_city != child.to_city):
                    Route.visited_city.append(to_city)
                    child.parent = parent #for Backtracking
                    child.predecessor_list = list(parent.predecessor_list)
                    child.predecessor_list.append(parent.to_city)
                    child.total_distance = float(parent.total_distance) + float(child.distance)
                    successors.append(child)
            elif (from_city not in Route.visited_city and parent.to_city == to_city and to_city not in parent.predecessor_list):
#             elif (parent.to_city == to_city):
                child = Route(to_city, from_city, distance, speed_limit, name)
                if(parent.from_city != child.to_city):
                    Route.visited_city.append(from_city)
                    child.parent = parent
                    child.predecessor_list = list(parent.predecessor_list)
                    child.predecessor_list.append(parent.to_city)
                    child.total_distance = float(parent.total_distance) + float(child.distance)
                    successors.append(child)
    return  successors

# For calculating the total distance, time and path for a solution
def backTrack(solution,option):
    print "backTrack - start: "+run_time()
    current = solution
    path = list()
    path.append(current.to_city)
    time = 0 
    distance = 0
    pathStr = ""
    while(current.parent is not None):
        print current.get_route_desc()
        if(current.name is None):
            continue
        if((current.speed_limit) != "" and current.distance != "" and current.speed_limit != "0"):
            time = time + float(current.distance)/float(current.speed_limit)
            distance = distance + float(current.distance)
        path.append(current.from_city)
        current = current.parent
    print "backTrack - exit: "+run_time()
    path.reverse()
    
    for city in path:
        pathStr = pathStr + " "+city
    return [distance,time,pathStr]

# IDS Algorithm Implementation
def ids(start_city,end_city,option):
    print "Using Ids Algorithm"
    limit = 1
    previous_depth= 0
    current_itr_depth=0
    while(previous_depth == 0 or current_itr_depth != previous_depth):   
        limit += 1
        previous_depth = current_itr_depth
        current_itr_depth = 0
        fringe = list();
        initial_state=Route(None,start_city,None,None,None)
        initial_state.depth = 0;
        if is_goal(start_city, end_city):
            print "Reached goal start "
        else: 
            fringe.append(initial_state)
        select_count = 0
        while(len(fringe) > 0):
            select = fringe.pop()
            if select.depth < limit:
                if(current_itr_depth < select.depth):
                    current_itr_depth = select.depth
                select_count+=1
                successors = get_successors_segment(select,"ids")
                for s in successors:
                    if (is_goal(s.to_city, end_city)):
                        return s
                    fringe.append(s)

# DFS Algorithm Implementation        
def dfs(start_city,end_city,option):
    print "Using Dfs Algorithm"
    fringe = list();
    if is_goal(start_city, end_city):
        print "Reached goal"
    else: 
        fringe.append(Route(None,start_city,None,None,None))
    while(len(fringe) > 0):
        select = fringe.pop()
        successors = get_successors_segment(select,"dfs")
        for s in successors:
            if (is_goal(s.to_city, end_city)):
                return s
            fringe.append(s)
 
# BFS Algorithm Implementation       
def bfs(start_city,end_city,option):
    print "Using Bfs Algorithm"
    fringe = list();
    if is_goal(start_city, end_city):
        print "Reached goal"
    else: 
        fringe.append(Route(None,start_city,None,None,None))
#     print "Fringe::"
#     print_successors_lst(fringe)
    while(len(fringe) > 0):
        select = fringe.pop(0)
#         print "select:"
#         print select.get_route_desc()
        successors = get_successors_segment(select,"bfs")
#         print "successors: "
#         print_successors_lst(successors)
        for s in successors:
            if (is_goal(s.to_city, end_city)):
                return s
            fringe.append(s)

# For Extracting gps data based on the city_name
def extract_gps_data(city_name):
    start =  city_gps_data.find(city_name)
    end = city_gps_data.find("\n",start,city_gps_data_len)
    return city_gps_data[start:end]

# For Extracting the edge data based on the city_name
def extract_segment_data(city_name):
    data = list()
    index = road_segment_data.find(city_name,0,road_segment_data_len);
    while(index != -1):
        start = road_segment_data.rfind("\n",0,index)
        end = road_segment_data.find("\n",index,road_segment_data_len)
        data.append(road_segment_data[start+1:end])
        index = road_segment_data.find(city_name,end,road_segment_data_len)
    return data

# For Calculating the Evaluation Function
def calculate_eval(child,end_city,option):
    
    source = extract_gps_data(child.to_city).split(" ")
    goal = extract_gps_data(end_city).split(" ")
    val = 1
    
    if(option == "segment"):
        if(len(source) == 3 and len(goal) == 3):
            val = calculate_distance(source[1], source[2], goal[1], goal[2]) + child.depth
        else:
            val = child.depth
    elif(option == "distance"):
        if(len(source) == 3 and len(goal) == 3):
            gps_distance = calculate_gps_distance(float(source[1]),  float(source[2]), float(goal[1]), float(goal[2]))
            val = gps_distance + child.total_distance
        else:
            val = child.total_distance
    elif(option == "time"):
        if(len(source) == 3 and len(goal) == 3):
            gps_distance = calculate_gps_distance(float(source[1]),  float(source[2]), float(goal[1]), float(goal[2]))
            heruistic_function = (gps_distance)/float(global_speed_limit) 
            val =  heruistic_function + child.total_time
        else:
            val = child.time
    elif(option == "scenic"):
        val = float(child.scenic)
    return val
    
# A* Algorithm implementation
def astar(start_city,end_city,option):
    print "Using astar - to find " + end_city
    fringe = PriorityQueue();
    if is_goal(start_city, end_city):
        print "Reached goal"
    else: 
        fringe.push(1,Route(None,start_city,0,None,None))
    while(len(fringe.queue) > 0):
        select = fringe.pop()
#         if (select.predecessor_list is not None):
#             print_successors_lst(select.predecessor_list)
#         if len(select.predecessor_list)
        if (is_goal(select.to_city, end_city)):
            return select
        if(option == "segment"):
            successors = get_successors_segment(select,"astar")
        elif (option == "distance"):
            successors = get_successors_distance(select)
        elif (option == "time"):
            successors = get_successors_time(select)
        elif (option == "scenic"):
            successors = get_successors_scenic(select)
            
        for s in successors:
            val = calculate_eval(s, end_city,option)
            fringe.push(val,s)

# Routes the control to the appropriate algorithm based on the input            
def solve(start_city,end_city,option,algorithm):
    
    if(algorithm == "bfs"):
        return bfs(start_city, end_city, option)
    elif(algorithm == "dfs"):
        return dfs(start_city, end_city, option)
    elif(algorithm == "ids"):
        return ids(start_city, end_city, option)
    elif(algorithm == "astar"):
        if(option =="time"):
            get_max_speed_limit()
        return astar(start_city, end_city, option)
    print "solve - exit" + run_time()

# Main Function    
def main():
    start_city = sys.argv[1]
    end_city = sys.argv[2]
    option = sys.argv[3]
    algorithm = sys.argv[4]
#     start_city = "Bloomington,_Indiana"
#     end_city = "Bloomington,_Indiana"
#     option = "distance"
#     algorithm = "dfs"
    print "start_city:: "+start_city +" -- end_city:: "+end_city+" -- option:: "+option +" -- algorithm:: "+algorithm
    if(start_city != end_city):
        destination = solve(start_city,end_city,option,algorithm)
        print "Solution::"
        print "Total Execution time: "+ run_time()
        if destination is None:
            print "No Route found"
        else: 
            (total_distance,total_time,path)= backTrack(destination,option)        
            print str(total_distance)+" "+str(total_time)+str(path)
    else:
        print "start_city is same as end_city"
        print "0 0 "+start_city

# for calculating the farthest city from a city
def furthestCity():
    start_city = "Bloomington,_Indiana"
    final_distance = 0
    final_city = ""
    count = 0
    for data in city_gps_data.split("\n"):
        print count
        city_data = data.split(" ") 
        end_city = city_data[0]
        print end_city
        Route.visited_city = list()
        destination = astar(start_city, end_city, "distance")
        
        if(destination is not None):
            print destination.get_route_desc()
            if(final_distance < destination.total_distance):
                final_distance = destination.total_distance
                final_city = destination.to_city
        count+=1
    final_distance = destination.total_distance
    print "final_distance:" +str(final_distance)
    final_city = destination.to_city
    print "final_city:: "+final_city
    
main()
# furthestCity()
