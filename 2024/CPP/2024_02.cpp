#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <string>
#include <iterator>
#include <sstream>


void PrintVector(std::vector<int> VectorToPrint)
{
    //A function to quickly list all elements of a vector
    //Might come in handy down the line in other assignments

    for(size_t i_Element {0}; i_Element < VectorToPrint.size(); ++i_Element)
    {
        std::cout << VectorToPrint[i_Element] << ", ";
    }
    std::cout << std::endl;
}


std::vector<int> ChopString(std::string LineToChop)
{
    //Create a vector in stack memory
    //This should be wiped from memory once the function is exited(?)
    std::vector<int> PopulateWithInts {};

    /*
    Create a stream out of the single line from the .txt file
    Read the stream until you hit a blank space, then extract it using the >> operator into ChopppedSegment
    Then add ChoppedSegment to PopulateWithInts as an int through stoi()
    */
    std::istringstream Stream (LineToChop);
    std::string ChoppedSegment {};

    while ( Stream >> ChoppedSegment)
    {
        PopulateWithInts.emplace_back(stoi(ChoppedSegment));
    }

    return PopulateWithInts;
   
}
    

std::vector<std::vector<int>>* ReadLines(std::string Path)
{
    //This function reads each line from the .txt and populates a vector stored on the heap with vectors which, themselves, contain ints

    //Create a vector of vectors of ints on the heap
    std::vector<std::vector<int>>* P_VectorOfVectorOfInts = new std::vector<std::vector<int>> {};

    //Start reading the file
    std::ifstream InputContents (Path);
    std::string StoreString {};

    if(InputContents.is_open())
    {
        //File exists, let's get crackin'
        while(getline(InputContents, StoreString))
        {   
            //Right now we have 1 line of text from the .txt (i.e. "7 6 4 2 1")
            //So we need to chop this string and store it in a vector of ints
            std::vector<int> VectorOfIntsPerLine {ChopString(StoreString)};

            //Then we can take that vector of ints, and store that vector in the vector of vector stored on the heap
            P_VectorOfVectorOfInts->emplace_back(VectorOfIntsPerLine);
        }
        return P_VectorOfVectorOfInts;

    }else if(!InputContents.is_open()){
        //File does not exist, exit early
        std::cout << "Error, no file available!" << std::endl;
    }
    return P_VectorOfVectorOfInts;

}


bool CompareLower(int a, int b)
{
    //function to compare if b is smaller than a for sorting descending
    return (a >= b);
}


bool SortingCheck(std::vector<int> CheckThisVector)
{
    //Create two copies of the vector for sorting
    std::vector<int> Ascending  {CheckThisVector};
    std::vector<int> Descending {CheckThisVector};

    //Sort ascending first
    sort(Ascending.begin(), Ascending.end());

    //Sort descending second
    sort(Descending.begin(), Descending.end(), CompareLower);

    //Return true if the original vector is either descending or ascending, otherwise return false
    if(CheckThisVector == Ascending || CheckThisVector == Descending){return true;}
    
    return false;

}


bool CheckDifferences(std::vector<int> VectorOfInts, int NumberOfInts)
{
    //Check each number with its next neighbour, as long as that doesn't exceed the 1 to 3 boundary, keep searching
    //If it does exceed the boundary, return false. Else if the whole loop completes, return true
    for(int i {0}; i < NumberOfInts - 1; ++i)
    {
        int Difference {std::abs(VectorOfInts[i] - VectorOfInts[i+1])};
        if(Difference < 1 || Difference > 3)
        {
            return false;
        }
     }
    //Whole loop passed, all differences fall within the boundary values
     return true;
}


int SolveProblemOne(std::vector<std::vector<int>>* P_VectorOfVectors, std::vector<std::vector<int>>* P_VectorOfFaultyVectors)
{
    //Function to tally up all valid entries for problem 1
    int Total {0};

    //How many vectors of ints are we dealing with?
    size_t NumberOfVectors {P_VectorOfVectors->size()};

    //Go through each vector of ints
    for(size_t i_Vector {0}; i_Vector < NumberOfVectors; ++ i_Vector)
    {
        //Right, we got a single vector of ints from the vector of vectors, let's see if it ascends/descends
        if(SortingCheck((*P_VectorOfVectors)[i_Vector]))
        {
            //vector of ints is either ascending or descending, let's see if it contains any level faults
            size_t NumberOfInts {(*P_VectorOfVectors)[i_Vector].size()};

            if(CheckDifferences((*P_VectorOfVectors)[i_Vector], NumberOfInts))
            {
                Total += 1;
            }else{
                //One of the difference boundaries is exceeded, add it to faulty vectors
                P_VectorOfFaultyVectors->emplace_back((*P_VectorOfVectors)[i_Vector]);
            }

        }else{
            //Vector doesn't fully ascend/descend, add it to faulty vectors
            P_VectorOfFaultyVectors->emplace_back((*P_VectorOfVectors)[i_Vector]);
        }
    }
    return Total;
}


bool RecheckAdjustedVector(std::vector<int> VectorOfInts)
{
    //This is just running the same logic as SolveProblemOne, just condensed and less commented
    if(SortingCheck(VectorOfInts))
    {
        if(CheckDifferences(VectorOfInts, VectorOfInts.size()))
        {return true;}
    }
    return false;
}


int SolveProblemTwo(std::vector<std::vector<int>>* P_VectorOfFaultyVectors, int TotalThusFar)
{
    //Recheck all the earlier discarded vectors and try to pass them on a max of one mistake
    //How many faulty vectors are we dealing with here?
    size_t NumberOfFaultyVectors {P_VectorOfFaultyVectors->size()};

    //Look at each faulty vector in turn
    for(size_t i_Vector {0}; i_Vector < NumberOfFaultyVectors; ++i_Vector)
    {
        //How many ints are in this vector?
        size_t NumberOfInts {(*P_VectorOfFaultyVectors)[i_Vector].size()};

        //Reconstruct EACH POSSIBLE vector of ints where one element has been removed
        //This is inefficient, but you lack knowledge of a better way (wah!)
        for(size_t i_Int {0}; i_Int < NumberOfInts; ++i_Int)
        {
            std::vector<int> Head {(*P_VectorOfFaultyVectors)[i_Vector].begin(), (*P_VectorOfFaultyVectors)[i_Vector].begin() + i_Int};
            std::vector<int> Tail {(*P_VectorOfFaultyVectors)[i_Vector].begin() + i_Int + 1, (*P_VectorOfFaultyVectors)[i_Vector].end()};

            for(auto i : Tail)
            {
                Head.emplace_back(i);
            }

            //At this point we have a vector with one element removed
            //See if it passes the test now
            if(RecheckAdjustedVector(Head))
            {
                TotalThusFar += 1;
                //As soon as vector of ints with one element removed passes, stop testing it!
                //Otherwise you can count the same vector of ints multiple times
                break; 
            }
        }
    }
    return TotalThusFar;

}


int main()
{   
    //Input path to the .txt file
    const std::string& Path {"input.txt"};

    //Read in the input text file, parse each line and chop up the number into ints, add ints to vector, add vector to vector
    std::vector<std::vector<int>>* P_VectorOfVectors = ReadLines(Path);

    /*
    At this point we have a vector in heap memory pointed to by P_VectorOfVectors
    which is populated by Vectors
    Which are populated by the ints taken from the .txt file
    */

    //Set up a pointer to a vector of vector of ints of all lines that contain one or more faults
    std::vector<std::vector<int>>* P_VectorOfFaultyVectors = new std::vector<std::vector<int>> {};



    int AnswerOne {SolveProblemOne(P_VectorOfVectors, P_VectorOfFaultyVectors)};
    std::cout << "Problem 1: " << AnswerOne << std::endl;

    /*
    At this point we have a 'remainder' vector, all the vectors of ints that had one of more faults in it are contained in 
    a vector on the heap pointed to by P_VectorOfFaultyVectors
    We can now recheck these and add any vector with just one fault, then removed, to a new running total starting at AnswerOne,
    since they automatically are also counted under 'one or less faults' rule for problem two
    */

    int AnswerTwo {SolveProblemTwo(P_VectorOfFaultyVectors, AnswerOne)};
    std::cout << "Problem 2: " << AnswerTwo << std::endl;

    //Once we're done, clean up pointers
    delete P_VectorOfVectors;
    P_VectorOfVectors = nullptr;

    delete P_VectorOfFaultyVectors;
    P_VectorOfFaultyVectors = nullptr;

    return 0;
}
