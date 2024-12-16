# Table of Contents

- [Introduction](#introduction)
- [Overview](#Overviw)
- [Documentation](#documentation)
- [Conclusion](#conclusion)

# Introduction
This document shows technical details and functionality of part of project `Virus on network`
containing the whole simulation logic from creating nodes and connections to handling the states and loop.

*Created by Timotej Vronč*

# Overview
The `Map` class manages overall simulation, including creation of nodes and connections between them.

`Node` class is responsible for handling all the logic for changing states, infecting other neighbours, visual representation.

`Connection` class is responsible for connection line between nodes and updating itself based on state of nodes.

`State` enum class defines various states for Nodes.


# Documentation

## `Map` class

### Attributes

#### `speed`
- **Type:** `int`
- **Description**: Controls the speed of simulation loop in miliseconds

#### `canvas`
- **Type:** `tkinter.Canvas`
- **Description**: canvas object for visuall representation of nodes and connections

#### `width`
- **Type:** `int`
- **Description**: Width of the map

#### `height`
- **Type:** `int`
- **Description**: Height of the map

#### `numberOfNodes`
- **Type:** `int`
- **Description**: Number of nodes which will be created

#### `avgNodeDegree`
- **Type:** `int`
- **Description**: Average number of connections between nodes

#### `initialOutbreakSize`
- **Type:** `int`
- **Description**: Number of infected nodes at the start 

#### `virusSpreadChance`
- **Type:** `float`
- **Description**: Chance of infecting neighbour

#### `virusCheckFreq`
- **Type:** `int`
- **Description**: Frequency - number of ticks between nodes checking if they are infected

#### `recoveryChance`
- **Type:** `float`
- **Description**: Chance of node recovering from virus

#### `gainResistChance`
- **Type:** `float`
- **Description:** Chance of node after not being able to recover to gain resistance against the virus

#### `recoveryChance`
- **Type:** `float`
- **Description**: Chance of node recovering from virus

#### `nodes[]`
- **Type:** `array[Node]`
- **Description**: list of Node objects on the map

#### `isLoaded`
- **Type:** `boolean`
- **Description**: value indicating wether the map has loaded

#### `isEnd`
- **Type:** `boolean`
- **Description**: value indicating wether the simulation has ended or not

### Methods

####  `__init__(self, canvas, speed, numberOfNodes, avgNodeDegree, initialOutbreakSize, virusSpreadChance, virusCheckFreq, recoveryChance, gainResistChance):`
- **Description:** Constructor of the map setting the initial attributes and state of the map

#### `createMap(self):`
- **Description:** Creates nodes based on `numberOfNodes` parameter on the map and stores them in nodes[] list where each node is assigned random position on the map.

# Conclusion
Final thoughts and recommendations.

