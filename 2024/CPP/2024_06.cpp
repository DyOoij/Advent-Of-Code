#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <iterator>
#include <sstream>


/*
//This allows us to keep track of how many times we set aside memory on the heap
int TotalAllocations {0};
int TotalMemoryAllocted;
void* operator new (size_t size)
{//Every time we allocate memory (either through new or through std::vector) we track it using this small function
    TotalAllocations++;
    TotalMemoryAllocted += size;
    std::cout << "Allocating: " << size << " bytes" << std::endl;
    return malloc(size);
}
*/


void PrintVector(std::vector<int> VectorToPrint)
{
    //A function to quickly list all elements of a vector
    //Might come in handy down the line in other assignments

    for(size_t i_Element {0}; i_Element < VectorToPrint.size(); ++i_Element)
    {
        std::cout << VectorToPrint[i_Element] << std::endl;
    }
    std::cout << std::endl;
}


std::vector<std::string>* ReadLines(std::string Path)
{
    //This function reads each line from the .txt and stores it as a string in a vector of strings

    //Create a vector of strings on the heap
    std::vector<std::string>*  P_VectorOfStrings = new std::vector<std::string> {};

    //Start reading the file
    std::ifstream InputContents (Path);
    std::string StoreString {};

    if(InputContents.is_open())
    {
        //File exists, let's get crackin'
        while(getline(InputContents, StoreString))
        {   
            //Right now we have a single line of text from the .txt
            P_VectorOfStrings->emplace_back(StoreString);
        }
        return P_VectorOfStrings;

    }else if(!InputContents.is_open()){
        //File does not exist, exit early
        std::cout << "Error, no file available!" << std::endl;
    }
    return P_VectorOfStrings;
}


std::vector<int> GrabInitialGuardLocation(std::vector<std::string>*& P_MatrixOfMap)
{
    //Find the guard's intitial location and return it as a YX Tuple
    /* A quick note on passing information to functions:
    This function gets passed a pointer to data on the heap, which is why it takes in std::vector<>*
        this means the pointer created in main(), and the pointer used here, point to the same section of data on the heap
    This function gets passed this pointer by reference, which is why it takes std::vector<>*&
        if we don't pass by reference, the scope will create a new pointer at a new address, we don't need a new pointer, we just
        need the old one
    
    an overview:

        main ptr:      0x08      (same data, different pointer)       func ptr:      0x22 (!!!)
        main ptr data: 0x1c      >> passed as std::vector<>*  >>      func ptr data: 0x1c

        main ptr:      0x08      (same data, same pointer)            func ptr:      0x08 
        main ptr data: 0x1c      >> passed as std::vector<>*&  >>     func ptr data: 0x1c

        it saves only a little memory (8 bytes on this system, which is the size for this system's PTR), but it is good practice
    */

    std::vector<int> GuardLocation {};

    for(int i_Line {0}; i_Line < P_MatrixOfMap->size(); ++i_Line)
    {
        if((*P_MatrixOfMap)[i_Line].find("^") != std::string::npos)
        {
            GuardLocation.emplace_back(i_Line);
            GuardLocation.emplace_back((*P_MatrixOfMap)[i_Line].find("^"));
            break;
        }
    }
    return GuardLocation;
}


std::vector<std::unordered_set<std::string>> SimulateMovement(std::vector<std::string>& Matrix, std::vector<int>& GuardPosition)
{
    //This vector will store unique locations in the form of a string of "y,x"
    //It's very similar to 2015_03, the Santa travelling problem
    std::unordered_set<std::string> UniqueLocations {};

    //This is for problem 2, we combine the tiles with the directions
    std::unordered_set<std::string> UniqueLocationsOrientations {};


    //Size parameters of the grid/matrix
    size_t MaxY {Matrix.size()};
    size_t MaxX {Matrix[0].size()};

    //Guard parameters, essentially, how do Y and X update when the guard is facing in this direction?
    char Orientation{'^'};
    std::unordered_map<char, std::vector<int>> GuardDirectionModifier
    {
        {'^', {-1,  0}},
        {'v', { 1,  0}},
        {'<', { 0, -1}},
        {'>', { 0,  1}}
    };

    /*
    Figure out where you are, is it a unique tile?
    Can you see ahead?
      if no: You are about to leave, end the function and count tiles
      if yes: is it a rock?
          if no: update position, loop
          if yes: turn, loop
    */

    while((GuardPosition[0] >= 0 && GuardPosition[0] < MaxY) && (GuardPosition[1] >= 0 && GuardPosition[1] < MaxX))
    {
        //Guard is still in the grid, snag the tile he's currently on
        std::string StandingOnTile {std::to_string(GuardPosition[0]) + "," + std::to_string(GuardPosition[1])};

        if(UniqueLocations.find(StandingOnTile) == UniqueLocations.end())
        {
            //Guard is standing on yet unrecorded tile
            UniqueLocations.insert(StandingOnTile);
        }

        if(UniqueLocationsOrientations.find(StandingOnTile + Orientation) == UniqueLocationsOrientations.end())
        {
            //Guard is standing on a tile-orientation combination that has not yet been recorded, this is for problem 2.
            UniqueLocationsOrientations.insert(StandingOnTile + Orientation);
        }

        //This is very verbose, but actually quite simple. The statement just checks if the next position in the guard's path actually exists
        //using increments for the Y and X coordinate by adding values for that Orientation from GuardDirectionModifier
        //if the location is within the grid, it can check for objects or move forward, otherwise the next move would have the guard leave the grid
        if(((GuardPosition[0] + GuardDirectionModifier[Orientation][0]) >= 0 && (GuardPosition[0] + GuardDirectionModifier[Orientation][0]) < MaxY ) &&
           ((GuardPosition[1] + GuardDirectionModifier[Orientation][1]) >= 0 && (GuardPosition[1] + GuardDirectionModifier[Orientation][1]) < MaxX ))
        {
            if(Matrix[GuardPosition[0] + GuardDirectionModifier[Orientation][0]][GuardPosition[1] + GuardDirectionModifier[Orientation][1]] == '#')
            {
                //Guard is looking at a rock, rotate
                switch (Orientation){
                    case '^' : Orientation = '>'; break;
                    case '>' : Orientation = 'v'; break;
                    case 'v' : Orientation = '<'; break;
                    case '<' : Orientation = '^'; break;
                }

            }else{
                //Guard is looking at an empty space, update location
                GuardPosition[0] += GuardDirectionModifier[Orientation][0];
                GuardPosition[1] += GuardDirectionModifier[Orientation][1];
            }

        }else{
            //The next tile does not exist: Guard is about to wander off-grid,end the function and count unique tiles
            break;
        }
    }
    std::vector<std::unordered_set<std::string>> BothLocationVectors {UniqueLocations, UniqueLocationsOrientations};
    return BothLocationVectors;
}


std::vector<std::unordered_set<std::string>> SolveProblemOne(std::vector<std::string>*& P_MatrixOfMap, std::vector<int> InitialGuardPosition)
{
    //A copy, because we'll be updating this one
    std::vector<std::string> CopyOfMatrix {*P_MatrixOfMap};

    std::vector<std::unordered_set<std::string>> Answer {SimulateMovement(CopyOfMatrix, InitialGuardPosition)};

    return Answer;

}


std::vector<int> SplitYXTupleString(std::string& YXTupleString)
{
    //Split the "12,34" string into a vector of ints that can be evaluated
    //Logic is similar to GrabPages in 2024_05

    std::stringstream Stream (YXTupleString);
    std::string Element {};
    std::vector<int> VectorOfInts {};

    while(!Stream.eof())
    {
        getline(Stream, Element, ',');
        VectorOfInts.emplace_back(stoi(Element));
    }
    
    return VectorOfInts;
}


std::vector<int> ScanForNextTile(std::string CurrentTileAndDirection, std::vector<std::string>*& P_MatrixOfMap)
{
    //Take a position-orientation pair and check what the next tile, if not a void, is

    //Setting up the basics, like a matrix boundaries and translating the orientation to a movement direction and splitting up the string into useable components
    size_t MaxY {P_MatrixOfMap->size()};
    size_t MaxX {(*P_MatrixOfMap)[0].size()};

    std::unordered_map<char, std::vector<int>> GuardDirectionModifier
    {
        {'^', {-1,  0}},
        {'v', { 1,  0}},
        {'<', { 0, -1}},
        {'>', { 0,  1}}
    };

    char Orientation {CurrentTileAndDirection[CurrentTileAndDirection.size()-1]};
    std::string YXTupleString {CurrentTileAndDirection.begin(), CurrentTileAndDirection.end()-1};
    std::vector<int> YXTuple {SplitYXTupleString(YXTupleString)};
    std::vector<int> NextTileCoordinates {};

    if((YXTuple[0] + GuardDirectionModifier[Orientation][0]) >= 0 && (YXTuple[0] + GuardDirectionModifier[Orientation][0] < MaxY) 
        &&
       (YXTuple[1] + GuardDirectionModifier[Orientation][1]) >= 0 && (YXTuple[1] + GuardDirectionModifier[Orientation][1] < MaxX))
        //If the next tile is within the boundaries of the Matrix
        {
            //Return the tile in front of the guard at the moment
            NextTileCoordinates = {YXTuple[0] + GuardDirectionModifier[Orientation][0], YXTuple[1] + GuardDirectionModifier[Orientation][1]};
        }else{
            //Sentinel value to indicate guard is about to leave at the exit point
            NextTileCoordinates = {-1, -1};
        }

    return NextTileCoordinates;

}


std::vector<std::string> CreateMatrixVariation(std::vector<std::string>*& P_MatrixOfMap, std::vector<int>& ObjectYXTuple)
{
    //Take the original matrix, change one location of the guard's path to an object and return that variation

    std::vector<std::string> MatrixCopy {(*P_MatrixOfMap)};
    MatrixCopy[ObjectYXTuple[0]][ObjectYXTuple[1]] = '#';
    return MatrixCopy;
}


bool SimulateLoopingMovement(std::vector<std::string>& Matrix, std::vector<int>& InitialLocation)
{
    //Right, at this point we have a matrix where ONE tile in the guard's path has been changed to an object
    //Run a walking sim and see if he wanders onto the same tile, in the same direction twice
    //if so, he is looping!

    //Storing tiles and their direction here, i.e. "2,3^" to test if the guard encoutners this specific state again
    std::unordered_set<std::string> WalkedTiles {};

    //Size parameters of the grid/matrix
    size_t MaxY {Matrix.size()};
    size_t MaxX {Matrix[0].size()};

    //Guard parameters, how does the direction affect walking through the grid?
    std::vector<int> GuardPosition {InitialLocation};   //Making a copy of this, since we want all loops to start from the original InitialLocation
    char Orientation{'^'};
    std::unordered_map<char, std::vector<int>> GuardDirectionModifier
    {
        {'^', {-1,  0}},
        {'v', { 1,  0}},
        {'<', { 0, -1}},
        {'>', { 0,  1}}
    };

    while((GuardPosition[0] + GuardDirectionModifier[Orientation][0] >= 0) && (GuardPosition[0] + GuardDirectionModifier[Orientation][0] < MaxY)
           &&
          (GuardPosition[1] + GuardDirectionModifier[Orientation][1] >= 0) && (GuardPosition[1] + GuardDirectionModifier[Orientation][1] < MaxX))
          //The next tile for the guard to move to exists in the grid (coordinates are not negative or larger than matrix size)
        {
            if((Matrix  [GuardPosition[0] + GuardDirectionModifier[Orientation][0]]
                       [GuardPosition[1] + GuardDirectionModifier[Orientation][1]]) == '#')
            {
                        //Next step is an obstacle, rotate
                        switch (Orientation)
                        {
                            case '^' : Orientation = '>'; break;
                            case '>' : Orientation = 'v'; break;
                            case 'v' : Orientation = '<'; break;
                            case '<' : Orientation = '^'; break;
                        }
            }else{
                //It is an open space, move forward and update location
                GuardPosition[0] += GuardDirectionModifier[Orientation][0];
                GuardPosition[1] += GuardDirectionModifier[Orientation][1];

            }
            //Now that we have moved (either forward or rotated) log the location we're at
            std::string TileAndDirection {std::to_string(GuardPosition[0]) + "," + std::to_string(GuardPosition[1]) + Orientation};
            if(WalkedTiles.find(TileAndDirection) == WalkedTiles.end())
            {
                //This is a new location-orientation pair, add it.
                WalkedTiles.insert(TileAndDirection);
            }else{
                //This is an OLD location-orientation pair. That is to say we have come back to a tile as a result of the room variation
                //This means we are officially stuck in a loop
                return true;
            }
        }
        //If the guard breaks out without looping, return false
        return false;

}


size_t SolveProblemTwo(std::vector<std::string>*& P_MatrixOfMap, std::unordered_set<std::string>& PathLocationsDirections, std::vector<int>& InitialGuardLocation)
{   
    /* Approach:
    Stupid brute force way of doing it, but fuck it.

    From problem one, we have isolated all tiles and directions the guard takes on his route in the form of "12,34^"
    Knowing where the guard will walk, we simply create as many room variations as there are steps in the guard's path, swapping out a tile for an object
    Then we run a simulation on this room, as with problem one, simply running the guard through the room with the additional one object
    if the guard, in this room, encounters the same Tile-Orientation combination twice, then he must be stuck in a loop for this room variation, so log the object location
    of course, if the object location has already been logged previously, then don't.
    return the size of this log, which should be the total amount of unique object locations

    */

    //Store all object locations here that lead to the guard looping
    std::unordered_set<std::string> UniqueObjectLocations {};


    for(auto TileBeforeObject : PathLocationsDirections)
    {
        //TileBeforeObject is a tile right before we place an object
        //If TileToPlaceObject is -1,-1, then it is the tile right before the exit, which we disregard

        std::vector<int> TileToPlaceObject {ScanForNextTile(TileBeforeObject, P_MatrixOfMap)};
        if(TileToPlaceObject[0] != -1)
        {
            //Create a variation on the original matrix where one tile is swapped with an object
            std::vector<std::string> ChangedMatrix {CreateMatrixVariation(P_MatrixOfMap, TileToPlaceObject)};

            //Simulate walking the guard through it
            if(SimulateLoopingMovement(ChangedMatrix, InitialGuardLocation))   //SimulateLoopingMovement returns a bool
            {   
                //A loop has been detected, turn the object location into a string and test if it has been logged yet
                std::string ObjectLocation {std::to_string(TileToPlaceObject[0]) + "," + std::to_string(TileToPlaceObject[1])};
                if(UniqueObjectLocations.find(ObjectLocation) == UniqueObjectLocations.end())
                {
                    UniqueObjectLocations.insert(ObjectLocation);
                }
            }
        }
    }
    //All possible rooms have been tested, return the count of all rooms that cause the guard to loop
    return UniqueObjectLocations.size();
}


int main(int argc, char* argv[])
{  
    //Read in data sourced by argv
    std::vector<std::string>* P_MatrixOfMap {ReadLines(argv[1])};

    //YXTuple of the Guard's initial location
    std::vector<int> InitialGuardLocation {GrabInitialGuardLocation(P_MatrixOfMap)};

    std::vector<std::unordered_set<std::string>> LiterallyASillyFuckingSolution {SolveProblemOne(P_MatrixOfMap, InitialGuardLocation)};
    
    size_t AnswerProblemOne {LiterallyASillyFuckingSolution[0].size()};
    std::cout << "Problem 1: " << AnswerProblemOne << std::endl;


    size_t AnswerProblemTwo {SolveProblemTwo(P_MatrixOfMap, LiterallyASillyFuckingSolution[1], InitialGuardLocation)};
    std::cout << "Problem 2: " << AnswerProblemTwo << std::endl;

    delete P_MatrixOfMap;
    P_MatrixOfMap = nullptr;

    return 0;
}
