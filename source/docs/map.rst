Map Class
=========

The `Map` class manages the overall simulation, including the creation of nodes and connections between them.

Class Definition
----------------

.. autoclass:: Map
    :members:
    :undoc-members:
    :show-inheritance:

Attributes
----------

.. py:attribute:: speed
    :type: int
    :description: Controls the speed of the simulation loop in milliseconds.

.. py:attribute:: canvas
    :type: tkinter.Canvas
    :description: Canvas object for visual representation of nodes and connections.

.. py:attribute:: width
    :type: int
    :description: Width of the map.

.. py:attribute:: height
    :type: int
    :description: Height of the map.

.. py:attribute:: numberOfNodes
    :type: int
    :description: Number of nodes to be created.

.. py:attribute:: avgNodeDegree
    :type: int
    :description: Average number of connections between nodes.

.. py:attribute:: initialOutbreakSize
    :type: int
    :description: Number of infected nodes at the start.

.. py:attribute:: virusSpreadChance
    :type: float
    :description: Chance of infecting a neighbor.

.. py:attribute:: virusCheckFreq
    :type: int
    :description: Frequency - number of ticks between nodes checking if they are infected.

.. py:attribute:: recoveryChance
    :type: float
    :description: Chance of a node recovering from the virus.

.. py:attribute:: gainResistChance
    :type: float
    :description: Chance of a node gaining resistance to the virus after recovery.

.. py:attribute:: nodes
    :type: list[Node]
    :description: List of Node objects on the map.

.. py:attribute:: isLoaded
    :type: bool
    :description: Indicates whether the map has loaded.

.. py:attribute:: isEnd
    :type: bool
    :description: Indicates whether the simulation has ended.

Methods
-------

.. py:method:: __init__(self, canvas)
    
    Constructor of the map setting the initial attributes and state of the map.

    :param canvas: The canvas object to draw the nodes and connections on.
    :type canvas: tkinter.Canvas

.. py:method:: setup(self, speed, numberOfNodes, avgNodeDegree, initialOutbreakSize, virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance)
    
    Sets up the map for simulation.

    :param speed: The speed of the simulation in milliseconds.
    :type speed: int
    :param numberOfNodes: The number of nodes to create.
    :type numberOfNodes: int
    :param avgNodeDegree: The average number of connections each node should have.
    :type avgNodeDegree: int
    :param initialOutbreakSize: The number of nodes to infect at the start of the simulation.
    :type initialOutbreakSize: int
    :param virusSpreadChance: The chance of the virus spreading to a neighbor node.
    :type virusSpreadChance: float
    :param virusCheckFreq: The number of ticks between each virus spread check.
    :type virusCheckFreq: int
    :param recoveryChance: The chance of an infected node recovering.
    :type recoveryChance: float
    :param gainResistChance: The chance of a recovered node gaining resistance to the virus.
    :type gainResistChance: float

.. py:method:: createMap(self)
    
    Creates nodes based on the `numberOfNodes` parameter on the map and stores them in the `nodes` list where each node is assigned a random position on the map.

.. py:method:: reset(self)
    
    Resets the map and clears the canvas.

    - Sets `isEnd` to True and `isLoaded` to False.
    - Calls the `canvas` object to delete everything drawn on the canvas.
    - Sets the `nodes` list to be blank (deleting all instances of nodes).

.. py:method:: createConnections(self)
    
    Creates connections between nodes based on the average node degree and Euclidean distance.

    - Calculates the total number of connections to be created between nodes.
    - While the number of created connections is less than the total number of connections, it takes one random node from the `nodes` list and:
        - Loops through other nodes checking if the nodes are not already sharing a connection.
        - Checks if the selected nodes haven't reached the `avgNodeDegree`.
        - Calls the `getDistance` method to calculate the distance between two nodes and stores the node which is closest.
        - When the closest node is found, it creates the connection between the nodes.

.. py:method:: getDistance(self, node1, node2)
    
    Calculates and returns the Euclidean distance between the given nodes.

    :param node1: The first node.
    :type node1: Node
    :param node2: The second node.
    :type node2: Node
    :return: The Euclidean distance between the two nodes.
    :rtype: float

.. py:method:: infectNodes(self)
    
    Infects nodes at the start of the simulation.

    - Randomly picks nodes to be infected until the number of infected nodes equals the `initialOutbreakSize` parameter.

.. py:method:: tick(self)
    
    Handles the simulation loop.

    - Checks if the game is at its end or if it is not loaded; if it is, then it breaks the loop.
    - Loops through every node in the `nodes` list and calls the `node.tick` method for the nodes to update their states.
    - Loops again through every node and calls the `node.check` method for the node to calculate the next state and checks if the node is infected.
    - Checks if `isEnd` equals True; if yes, then it breaks the simulation loop.
    - Checks if the number of infected nodes is 0; if yes, then sets `isEnd` to True.