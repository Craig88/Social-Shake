from xml.dom.minidom import parse, parseString
from collections import Counter
import pydot
import networkx as nx
import matplotlib.pyplot as plt
import glob
import time
import subprocess
from math import log, sqrt

# A Python program to analyse the plays of William Shakespeare

# Social Shakespeare - social_shake.py
# Craig Steele (cr@igsteele.com)
# Based on code by Andrew Matteson
# August 2013


def save_graph(graph, num_label):
    #given a graph of an relationship level, saves it as an png file
    print 'I am saving the graph to a file'
    graph.write_png('output/Play'+'_Level' + str(num_label) +'.png',prog='neato')

def tidy_nodes(graph):
    #remove any nodes that have no edges 
    keep_nodes = []
    for edge in graph.get_edge_list():
        keep_nodes.append(edge.get_source())
        keep_nodes.append(edge.get_destination())

    for node in graph.get_node_list():
        if not str(node.get_name()) in keep_nodes:
            graph.del_node(node)

def count_lines_for_each_speaker(dom, speaker_count):
    
    for node in dom.getElementsByTagName('SPEECH'):
        num_lines = len(node.getElementsByTagName('LINE'))
        for speakers in node.getElementsByTagName('SPEAKER'):
            if speakers.firstChild:
                speaker_count.update({speakers.firstChild.nodeValue.upper(): num_lines})


def get_list_of_speakers_each_scene(dom, actors_scene):

    for act in dom.getElementsByTagName('ACT'):
        act_name = act.getElementsByTagName('TITLE')[0].firstChild.nodeValue
        for scene in act.getElementsByTagName('SCENE'):
            scene_name = scene.getElementsByTagName('TITLE')[0].firstChild.nodeValue
            scene_id = act_name + ' ' + scene_name.split('.')[0]

            speaker_list = []
            #This will hold the names of all the people who speak in a scene


            for speaker in scene.getElementsByTagName('SPEAKER'):
                if speaker.firstChild:
                    speaker_list.append(str(speaker.firstChild.nodeValue).upper())
                    actors_scene[str(scene_id)] = set(speaker_list)
                 #   print actors_scene
                 #   time.sleep(0.5)

            #actors_scene now holds information about all the characters in each scene that speak
            #in the form {ACT I SCENE I': set(['HORATIO', 'FRANCISCO', 'BERNARDO'])} 

def add_nodes_to_graph(speaker_count, graph): 
    N = 100 #this is the maximum number of nodes we will draw, the top 100
    for speaker in speaker_count:
        width = log(2*float(speaker_count[speaker]))/float(1)
        #print width
        if speaker in [s for s, l in speaker_count.most_common(N)]:
            fontsize = 1.2*(width*72/(len(speaker)))
            node = pydot.Node(
                speaker,
                fixedsize=True,
                fontsize=fontsize,
                shape='circle',
                width=width,
                penwidth=10
            )
        else:
            node = pydot.Node(
                speaker,
                fixedsize=True,
                shape='point',
                width=width,
                penwidth=3
            )

        graph.add_node(node)

def add_lines_to_graph(edge_list, actors_scene, graph, relationship_level):
    #                 #for every character,
    #                 #draw a line between them and every other character they appear
    #                 #in a scene with
    #                 #if a character appears in a scene with a character again, make the line thicker
        for scene in actors_scene:
            chars = sorted(actors_scene[scene]) #needs to be sorted, I assume in one order
            num_char = len(chars)
            for i in range(num_char):
                for j in range(i+1,num_char):
                    if not edge_list.has_key(chars[i] + ' ' + chars[j]):
                        edge_list[chars[i] + ' ' + chars[j]] = pydot.Edge(
                            chars[i],
                            chars[j],
                            weight=1,
                            penwidth=3
                            )
                    else:
                        edge_list[chars[i] + ' ' + chars[j]].set_weight(
                            edge_list[chars[i] + ' ' + chars[j]].get_weight()+1
                            )
                        edge_list[chars[i] + ' ' + chars[j]].set_penwidth(
                            edge_list[chars[i] + ' ' + chars[j]].get_penwidth()+5
                            )

        for edge in edge_list:
            if edge_list[edge].get_weight()>=relationship_level: #only add to graph if it's >= the relationship level
                graph.add_edge(edge_list[edge])


        tidy_nodes(graph)                

    

# ******************************************
# ******************************************
def analyze(play,relationship_level):
# ******************************************
# ******************************************

    dom = parse(play)
    speaker_count = Counter()
    #This will keep a track of how many lines each character has in the play
    #and stores it in the form (Characters_Name: number_of_lines)

    count_lines_for_each_speaker(dom, speaker_count) 

    #create an empty list
    actors_scene = {} 
    get_list_of_speakers_each_scene(dom, actors_scene)
    
    #actors_scene now holds information about all the characters in each scene that speak
    #in the form {ACT I SCENE I': set(['HORATIO', 'FRANCISCO', 'BERNARDO'])} 

    #create an empty graph to draw our network on
    graph = pydot.Dot(graph_type='graph',overlap=False)
    

    #for every person who speaks, we are going to need to add them as a node on the graph
    #the more lines they say (the larger their speaker count) the larger we will draw the node
    add_nodes_to_graph(speaker_count, graph)


    #draw the relationships between the people
    edge_list = {}
    add_lines_to_graph(edge_list, actors_scene, graph, relationship_level)
  
    #save the graph to an image file
    save_graph(graph, relationship_level)

# ******************************************
# ******************************************
# ***** The main program starts here ******* 
# ******************************************
# ******************************************

print "Welcome to Social Shakespeare App"
subprocess.Popen('say -v "Bruce" "Welcome to Social Shakespeare"', shell=True)

for relationship_level in range(1,10):

    
    for play in glob.glob('plays/macbeth.xml'):

        print "I will now analyse Relationships Level {}.".format(relationship_level)
        analyze(play,relationship_level)

print "Analysis complete"
subprocess.Popen('say -v "Bruce" "and the rest is silence"', shell=True)        
