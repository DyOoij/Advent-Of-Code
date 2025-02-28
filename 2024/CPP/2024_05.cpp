#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <unordered_map>
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
        std::cout << VectorToPrint[i_Element] << ", ";
    }
    std::cout << std::endl;
}


std::vector<std::vector<char>>* ReadLines(std::string Path)
{
    //This function reads each line from the .txt and populates a vector stored on the heap with vectors which, themselves, contain chars

    //Create a vector of vectors of ints on the heap
    std::vector<std::vector<char>>*  P_VectorOfVectorOfChars = new std::vector<std::vector<char>> {};

    //Start reading the file
    std::ifstream InputContents (Path);
    std::string StoreString {};

    if(InputContents.is_open())
    {
        //File exists, let's get crackin'
        while(getline(InputContents, StoreString))
        {   
            //Right now we have a single line of text from the .txt
            //There are three segments, the rules, a blank newline and the pages

            //Create a Vector to store each individual character, build that vector, then add it to the vector we return
            std::vector<char> StoringCharsHere {};
            for(size_t i_Char {0}; i_Char < StoreString.size(); ++i_Char)
            {
                StoringCharsHere.emplace_back(StoreString[i_Char]);
            }
            P_VectorOfVectorOfChars->emplace_back(StoringCharsHere);
        }

        
        return P_VectorOfVectorOfChars;

    }else if(!InputContents.is_open()){
        //File does not exist, exit early
        std::cout << "Error, no file available!" << std::endl;
    }
    return P_VectorOfVectorOfChars;

}


std::unordered_map<int, std::vector<int>>* GrabRules(std::vector<std::vector<char>>*& P_VectorAllInfo, long int BreakPoint)
{   
    //Isolate the rules (i.e. 6|7) from the input.txt, passing the pointer by reference, we don't need multiple copies of pointer
    //Builds an unordered map of ints linked to a vector of ints of all numbers it has to be in front of

    std::unordered_map<int, std::vector<int>>* P_DictOfRules = new std::unordered_map<int, std::vector<int>> {};

    for(size_t i_MasterVector {0}; i_MasterVector < BreakPoint; ++i_MasterVector)
    //These are the rules as a vector of chars
    {
        //Silly way to keep track of which number is being stored
        bool FirstNumberChecked = false;
        std::string FirstNumber {};
        std::string SecondNumber {};

        for (size_t i_Char {0}; i_Char < (*P_VectorAllInfo)[i_MasterVector].size(); ++i_Char)
        {
            if (((*P_VectorAllInfo)[i_MasterVector][i_Char] != '|') && !FirstNumberChecked)
            {
                FirstNumber += (*P_VectorAllInfo)[i_MasterVector][i_Char];
            }else if((*P_VectorAllInfo)[i_MasterVector][i_Char] != '|' && FirstNumberChecked)
            {
                SecondNumber += (*P_VectorAllInfo)[i_MasterVector][i_Char];
            }else{
                FirstNumberChecked = true;
            }
        }   
        /*From this point on, we have isolated two numbers.
        FirstNumber: An entry in an unordered_map
        SecondNumber: An entry to the value vector in the unordered_map
        */

        if((*P_DictOfRules).find(stoi(FirstNumber)) == (*P_DictOfRules).end())
        {
            //FirstNumber does not yet exist, add it and its SecondNumber to the Dict
            (*P_DictOfRules)[stoi(FirstNumber)].emplace_back(stoi(SecondNumber));
        }else{
            //FirstNumber does exist, see if it already contains SecondNumber in its vector
            std::vector<int> VectorOfInts {(*P_DictOfRules)[stoi(FirstNumber)]};
            if((std::find(VectorOfInts.begin(), VectorOfInts.end(), stoi(SecondNumber)) == VectorOfInts.end()))
            //Number not yet entered into the Dict's vector, add it in
            {
                (*P_DictOfRules)[stoi(FirstNumber)].emplace_back(stoi(SecondNumber));   
            }
        }

    }
    /*
    //CODE TO PRINT MAP ELEMENTS
    for(auto i : *P_DictOfRules)
    {
        std::cout << i.first << ": ";
        for(auto j : i.second)
        {
            std::cout << j << ", ";
        }
        std::cout <<  std::endl;
    }
    */
    
    
    return P_DictOfRules;
}


std::vector<std::vector<int>>* GrabPages(std::vector<std::vector<char>>*& P_VectorAllInfo, long int& BreakPoint, size_t& MasterVectorSize, const char& SplitPoint)
{
    //Isolate the pages(i,e <53, 44, 17>) from the input.txt, passing the pointer by reference
    //builds a vector of vectors of ints (the pages per update)

    std::vector<std::vector<int>>* P_VectorOfUpdates = new std::vector<std::vector<int>> {};

    for(long int i_MasterVector {BreakPoint + 1}; i_MasterVector < MasterVectorSize; ++i_MasterVector)
    //BreakPoint +1 since otherwise it starts counting from the blank line included
    {
        std::string BuildAString {};

        for( auto Character : (*P_VectorAllInfo)[i_MasterVector])
        //Mush vector elements together in a string
        {
            BuildAString += Character;
        }
        
        std::stringstream Stream (BuildAString);
        std::string Element {};
        std::vector<int> BuildAVector {};

        while(!Stream.eof())
        //And unpack whole numbers instead of single digits/chars
        {
            getline(Stream, Element, SplitPoint);
            BuildAVector.emplace_back(stoi(Element));
        }
        P_VectorOfUpdates->emplace_back(BuildAVector);
    }
    return P_VectorOfUpdates;
}


bool VectorFollowsRules(std::unordered_map<int, std::vector<int>>*& P_DictOfRules, std::vector<int>* P_Update)
{
    //Iterate through the vector of ints update and check if the rules are followed for each element

    std::vector<int> Tested {};
    std::vector<int> Untested {*P_Update};

    for(size_t i_Page {0}; i_Page < P_Update->size(); ++i_Page)    //for page in update
    {
        std::vector<int>& Rules {(*P_DictOfRules)[(*P_Update).at(i_Page)]};  //grab the rules for that page
        Tested.emplace_back(Untested[0]);
        Untested.erase(Untested.begin());

        for(int i_Tested {0}; i_Tested < Tested.size(); ++ i_Tested)         //Look at what has been tested already
        {
            if(find(Rules.begin(), Rules.end(), Tested[i_Tested]) != Rules.end())  //Checking the rules
            /* The dict of rules contains a key-value pair of <int> : <vector of ints the current int has to be in front of>
               so if an already tested value shows up in Tested, but also shows up in the vector of ints in the dict, then the rule has been broken
            */
            {return false;}
        }
    }
    //If nothing gets triggered for false, the vector must be correct
    return true;
}


int SolveProblemOne(std::unordered_map<int, std::vector<int>>*& P_DictOfRules, std::vector<std::vector<int>>*& P_VectorOfUpdates, std::vector<std::vector<int>>*& P_FaultyUpdates)
{
    /*Approach:
    We now have a vector of the updates and a dict of the rules, so go through each update and check if all the rules are applied
    perhaps do it as part of a bool func, if rules followed: true, if true: grab middle value and add to running total
    */
    int RunningTotal {0};

    size_t SizeOfUpdates {P_VectorOfUpdates->size()};

    for(size_t i_UpdateVector {0}; i_UpdateVector < SizeOfUpdates; ++i_UpdateVector)
    {
        if(VectorFollowsRules(P_DictOfRules, &(*P_VectorOfUpdates)[i_UpdateVector]))
        //If the Vector is correct, so no rules are broken
        {
            long unsigned int VectorHalf {((*P_VectorOfUpdates)[i_UpdateVector].size())/2};   //Rounds down from 0.5, which works since we start counting from 0, not 1
            RunningTotal += (*P_VectorOfUpdates)[i_UpdateVector][VectorHalf];
        }else{
            P_FaultyUpdates->emplace_back((*P_VectorOfUpdates)[i_UpdateVector]); //Building this for problem 2.
        }
    }
    return RunningTotal;
}


void ShuffleVector(std::unordered_map<int, std::vector<int>>* P_DictOfRules, std::vector<int>& SequenceOfPages)
{
    
    //Seeks out an element in the vector that breaks the rule, swaps the offender with the value that caused the conflict
    //i.e. <2,3,5,4>  <4|5>   >>> <2,3,4,5>

    size_t AmountOfPages {SequenceOfPages.size()};
    for(size_t i_Page {0}; i_Page < AmountOfPages; ++i_Page) //Iterates through the whole sequence until it hits a conflict
    {
        int CurrentPage {SequenceOfPages[i_Page]};                                                            //Current page to check
        std::vector<int> RulesForPage {(*P_DictOfRules)[CurrentPage]};                                        //What rules to check against (These cannot be in front of CurrentPage)
        std::vector<int> PagesCheckedSoFar {SequenceOfPages.begin(), SequenceOfPages.begin() + i_Page};       //Keeps a record of all correct sequence pages
        

        for(size_t i_CheckedPage {0}; i_CheckedPage < PagesCheckedSoFar.size(); ++i_CheckedPage)
        {  
            if(find(RulesForPage.begin(), RulesForPage.end(), PagesCheckedSoFar[i_CheckedPage]) != RulesForPage.end())
            {
                //There is a conflict here, there is a page in the already checked pages that also appears in the dict entry for the current number
                //Meaning, that a number that is supposed to follow currentnumber, currently exists in the already checked pages
                //So swap them, and return that updated vector, perhaps now it'll be alright
                long unsigned int IndexSwapOne {i_CheckedPage};
                long unsigned int IndexSwapTwo {PagesCheckedSoFar.size()};

                std::swap(SequenceOfPages[IndexSwapOne], SequenceOfPages[IndexSwapTwo]);
            }
        }
    }   
}


int SolveProblemTwo (std::unordered_map<int, std::vector<int>>*& P_DictOfRules, std::vector<std::vector<int>>*& P_FaultyUpdates)
{
    /*Approach:
    Well this is going to suck performance-wise, but you're not going to fuck around with dynamic programming just yet, sod it, it's C++, it can handle it
    Go through the faulty vector, take an offending element and swap it with it with the value that causes the conflict, test again, keep swapping until it passes.
    Go through each element in the vector, shifting left (this is super inefficient) untill the whole vector finally passes.

    Look man, this is why you're doing C++, in python this would take years, but here we have SPEED
    */
   
    int Runningtotal {0};

    size_t AmountOfFaultyUpdates {(*P_FaultyUpdates).size()};
    for(size_t i_FaultyUpdates {0}; i_FaultyUpdates < AmountOfFaultyUpdates; ++i_FaultyUpdates)
    {
        std::vector<int> FlawedUpdate {(*P_FaultyUpdates)[i_FaultyUpdates]};

        //As long as the vector is faulty, keep shuffling it
        while(!VectorFollowsRules(P_DictOfRules, &FlawedUpdate))
        {
            ShuffleVector(P_DictOfRules, FlawedUpdate); 
        }
        //but now it is good! So grab the middle value and add it to running total
        long unsigned int VectorHalf {FlawedUpdate.size()/2};
        Runningtotal+= FlawedUpdate[VectorHalf];  
    }
    return Runningtotal;
}


int main()
{   
    //Input path to the .txt file
    const std::string& Path {"input.txt"};

    //Read in data
    std::vector<std::vector<char>>* P_VectorOfAllInputContents {ReadLines(Path)};

    //Master vector properties
    size_t MasterVectorSize {P_VectorOfAllInputContents->size()};
    long int BreakPoint {std::distance(
                                        P_VectorOfAllInputContents->begin(),std::find
                                            (
                                                P_VectorOfAllInputContents->begin(),          //A very convoluted way to find out where
                                                P_VectorOfAllInputContents->end(),            //the input "breaks" from rules to pages
                                                std::vector<char> {}
                                            )
                                        )
                        };  

    //This pointer points to a dict on the heap that contains key-value pairs of int numbers and vector<int> numbers that the first number has to be in front of
    //i.e.  53, <29, 13> means that pag 53 has to be printed before page 29 and page 13
    std::unordered_map<int, std::vector<int>>* P_RulesOfPages {GrabRules(P_VectorOfAllInputContents, BreakPoint)};

    //The following pointer points to a vector of int vectors of all Updates and their page order
    //i.e. <12, 56, 55>
    const char SplitPoint {','};
    std::vector<std::vector<int>>* P_VectorOfUpdates {GrabPages(P_VectorOfAllInputContents, BreakPoint, MasterVectorSize, SplitPoint)};

    //Store all faulty updates here
    std::vector<std::vector<int>>* P_FaultyUpdates = new std::vector<std::vector<int>> {};

    int AnswerProblemOne {SolveProblemOne(P_RulesOfPages, P_VectorOfUpdates, P_FaultyUpdates)};
    std::cout << "Answer problem 1: " << AnswerProblemOne << std::endl;
    
    int AnswerProblemTwo {SolveProblemTwo(P_RulesOfPages, P_FaultyUpdates)};
    std::cout << "Answer problem 2: " << AnswerProblemTwo << std::endl;


    //At least pretend you are worried about memory management    
    delete P_VectorOfAllInputContents;
    P_VectorOfAllInputContents = nullptr;
    delete P_RulesOfPages;
    P_RulesOfPages = nullptr;
    delete P_VectorOfUpdates;
    P_VectorOfUpdates = nullptr;
    delete P_FaultyUpdates;
    P_FaultyUpdates = nullptr;

    return 0;



}
