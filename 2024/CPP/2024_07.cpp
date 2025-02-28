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
#include <cmath>


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


void PrintVector(std::vector<size_t> VectorToPrint)
{
    //A function to quickly list all elements of a vector
    //Might come in handy down the line in other assignments

    for(size_t i_Element {0}; i_Element < VectorToPrint.size(); ++i_Element)
    {
        std::cout << VectorToPrint[i_Element] << ", ";
    }
    std::cout << std::endl;
}


std::vector<std::string>* ReadLines(std::string Path)
{
    //Reads the input.txt and stores the whole line as a string
    std::vector<std::string>*  P_VectorOfInputStrings = new std::vector<std::string> {};

    //Start reading the file
    std::ifstream InputContents (Path);
    std::string StoreString {};

    if(InputContents.is_open())
    {
        //File exists, let's get crackin'
        while(getline(InputContents, StoreString))
        {   
            //Right now we have a single line of text from the .txt
            P_VectorOfInputStrings->emplace_back(StoreString);
        }
        return P_VectorOfInputStrings;

    }else if(!InputContents.is_open()){
        //File does not exist, exit early
        std::cout << "Error, no file available!" << std::endl;
    }
    return P_VectorOfInputStrings;
}


std::vector<size_t> ConvertLineToVector(std::string& InputLine)
{
    //Converts each single line from the .txt into a vector of size_t PER LINE
    std::vector<size_t> ReturnVector {};
    std::vector<std::string> ElementsPerLine {};
    std::istringstream Stream(InputLine);
    std::string ChoppedString {};

    while(Stream >> ChoppedString)
    {
        ElementsPerLine.emplace_back(ChoppedString);
    }

    //Removes the ":" from the first number
    ElementsPerLine[0].erase(ElementsPerLine[0].size()-1);

    //Now convert all strings to size_t, stoi() doesn't work because some numbers are way too big
    for(size_t i_Element {0}; i_Element < ElementsPerLine.size(); ++i_Element)
    {
        std::string NumberAsString {ElementsPerLine[i_Element]};
        std::stringstream Streaming (NumberAsString);
        size_t ResultingNumber;
        Streaming >> ResultingNumber;
        ReturnVector.emplace_back(ResultingNumber);
    }
    
    return ReturnVector;
}


bool CanCombineToResult(std::vector<size_t>& FullVector)
{
    //Test to see if the first element of the vector, the Head, can be created out of its following elements, the Tail

    //The first element is always the inteded result
    size_t Head {FullVector[0]};

    //The math starts as of the second possible element (index 2)
    std::vector<size_t> Results {FullVector[1]};

    for(size_t i_Component {2}; i_Component < FullVector.size(); ++i_Component)
    {
        std::vector<size_t> NewResults {};
        //For each component listed in the input vector as of index 2, since index 0 is the intended result and index 1 is the first result vector
        for(size_t i_Result {0}; i_Result < Results.size(); ++i_Result)
        {
            //For each result known so far, this increases as we create a bigger vector, do the math
            NewResults.emplace_back(Results[i_Result] + FullVector[i_Component]);
            NewResults.emplace_back(Results[i_Result] * FullVector[i_Component]);
        }
        Results = NewResults;
    }

    if(find(Results.begin(), Results.end(), Head) != Results.end())
    {
        //The intended result is found in the final vector of all possible results, therefore it is possible to create this number
        return true;
    }
    return false;

}


bool CanCombineToResultTwo(std::vector<size_t>& FullVector)
{
    //This is just an upgraded CanCombineToResult() that also checks for concatenation
    size_t Head {FullVector[0]};

    std::vector<size_t> Results {FullVector[1]};

    for(size_t i_Component {2}; i_Component < FullVector.size(); ++i_Component)
    {
        std::vector<size_t> NewResults {};
        for(size_t i_Result {0}; i_Result < Results.size(); ++i_Result)
        {
            NewResults.emplace_back(Results[i_Result] + FullVector[i_Component]);
            NewResults.emplace_back(Results[i_Result] * FullVector[i_Component]);
            
            std::string One {std::to_string(Results[i_Result])};
            std::string Two {std::to_string(FullVector[i_Component])};

            //This checks the concatenation condition
            std::string Combined {One + Two};
            std::string NumberAsString {Combined};
            std::stringstream Streaming (NumberAsString);
            size_t ResultingNumber;
            Streaming >> ResultingNumber;
            NewResults.emplace_back(ResultingNumber);
        }
        Results = NewResults;
    }

    if(find(Results.begin(), Results.end(), Head) != Results.end())
    {
        return true;
    }
    return false;
}


std::vector<size_t> SolveProblems(std::vector<std::string>*& P_InputLines)
{
    //Since both problems are very similar, we can use the same input data twice and return a vector of both results
    size_t ResultOne {0};
    size_t ResultTwo {0};

    for(auto Line : (*P_InputLines))
    {
        std::vector<size_t> VectorAsNumbers {ConvertLineToVector(Line)};

        if(CanCombineToResult(VectorAsNumbers))
        {
            ResultOne += VectorAsNumbers[0];
        }
        //The only difference is an added concatenation check
        if(CanCombineToResultTwo(VectorAsNumbers))
        {
            ResultTwo += VectorAsNumbers[0];
        }
    }

    std::vector<size_t> AnswerVector {ResultOne, ResultTwo};
    return AnswerVector;
}


int main(int argc, char* argv[])
{  
    //Read in data sourced by argv
    std::vector<std::string>* P_VectorPerLines {ReadLines(argv[1])};

    /*Alright, here's where you fucked up
    You assumed, without thinking, that all values on the left side of the column, the intended results, were unique
    so when you mapped them, some of them got overwritten (1095 for example, is listed twice)
    and thus they were not fully considered

    sucks
    */
    std::vector<size_t> Answers {SolveProblems(P_VectorPerLines)};
    std::cout << "Answer problem 1: " << Answers[0] << std::endl;

    std::cout << "Answer problem 2: " << Answers[1] << std::endl;

    return 0;
}
