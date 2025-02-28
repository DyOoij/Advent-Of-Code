#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <string>
#include <iterator>


size_t DetermineArraySize(std::string  InputPath)
{
    //Firstly, read input.txt and loop through all lines so we can count them
    //to predetermine what the size of the arrays should be (try to avoid vector nonsense)
    
    std::ifstream InputContents {InputPath};

    if(InputContents.is_open())
    {
        size_t Counter {0};
        std::string StoreString {};

        while(getline(InputContents, StoreString)){ ++Counter;}

        //Good practice to close files once we're done with them
        InputContents.close();

        return Counter;
    }

    //Since the function expects to return an int, allow the function scope to return one
    //Otherwise the compiler starts to chuck warnings at ya
    return 0;

}


std::vector<std::string> SplitLines(std::string FullLine, std::string Delimiter)
{
    //Function to split a line into pieces based on a delimiter value 
    //This delimiter value will act as the "splitting point" of each string  [1234   5678] to [1234, 5678]

    //Store split string in here
    std::vector<std::string> ReturnString {};

    //Build a digit one number at a time
    std::string DigitString {};
    bool FirstNumberScan {true};

    /*
    Essentially, store each digit in a string, once you hit a blank, wipe that digit and set it to {}, store the number as string in the vector
    also, switch the boolean to false, so you don't trigger the else if statement on subsequent blanks
    after the blanks, it hits the first digit of the second number, so you build the number again from scratch
    once the whole line has been pro
    */
    for(size_t i {0}; i < FullLine.size(); ++i)
    {
        if (std::isdigit(FullLine[i]))
        {
            DigitString += FullLine[i];
        }else if((std::isblank(FullLine[i]) && FirstNumberScan)){
            ReturnString.emplace_back(DigitString);
            DigitString = {};
            FirstNumberScan = false;
        }
        
    }

    //Ran through the whole line, built second digit, add it to vector
    ReturnString.emplace_back(DigitString);

    return ReturnString;
}


int** ReturnArrayOfInts(std::string InputPath, size_t ArraySize)
{
    //Read through the text file again, line by line, and filter out the digits in two separate arrays

    /*
    This is where the true fuckery happens, it is easier with vectors, but this is now an excersize in pointer logic
    We want to create memory on the heap, since stack memory collapses once the scope is exited
    So in order to do that we create a pointer that points to an ARRAY of pointers, 
    each of these pointing to an address containing the array of ints (2D array)
    */

    //Allocate memory to store two pointers (2 because left and right columns)
    int** ArrayOfIntArrays = new int*[2];

    //Now add two dynamic arrays of the total line size (1000, in this case)
    ArrayOfIntArrays[0] = new int[ArraySize];
    ArrayOfIntArrays[1] = new int[ArraySize];

    //Read contents from file 
    std::ifstream InputContents {InputPath};

    if(InputContents.is_open())
    {   
        //Create counter to keep track of line numbers
        size_t LineNumber {0};

        //Block of reading logic
        std::string CurrentLine {};
        while(getline(InputContents, CurrentLine))
        {
            //SplitLines returns an array of strings, cut on the delimiter of spaces, so [1234, 5678]
            std::vector<std::string> ArrayStrings {SplitLines(CurrentLine, "   ")};
        
            //Now we do some true Array magic
            //ArrayOfInts[0] is left values, ArrayOfInts[1] is right values
            //Populate the left and right array by accessing the LineNumber, we have already set the size before, so the index at LineNumber exists already
            //And we populate it with either the first or second value as split by SplitLines
            ArrayOfIntArrays[0][LineNumber] = std::stoi(ArrayStrings[0]);
            ArrayOfIntArrays[1][LineNumber] = std::stoi(ArrayStrings[1]);

            ++LineNumber;
        }        
    }

    return ArrayOfIntArrays;
}


void SortArrays(int** UnsortedArray, size_t ArraySize)
{
    //Take the array of two unsorted arrays of ints and sort them highest to lowest
    std::sort(UnsortedArray[0], UnsortedArray[0] + ArraySize);
    std::sort(UnsortedArray[1], UnsortedArray[1] + ArraySize);
}


int SolveProblemOne(int** ArrayOfArrays, size_t ArraySize)
{
    //Compare each index from 0 to 1000 between the two arrays (left and right) figure out the difference and add it to a counter

    //Init a total counter
    int TotalAbsoluteDifference {0};

    //Loop through all values line by line
    for(int LineNumber {0}; LineNumber < ArraySize; ++LineNumber)
    {
        TotalAbsoluteDifference += abs(ArrayOfArrays[0][LineNumber] - ArrayOfArrays[1][LineNumber]);
    }

    return TotalAbsoluteDifference;
}


int SolveProblemTwo(int** ArrayOfArrays, size_t ArraySize)
{
    int TotalAnswer {0};

    //Loop through the left list (ArrayOfArrays[0]) count how often it appears in the right list (ArrayOfArrays[1])
    for(int IndexAtLine {0}; IndexAtLine < ArraySize; ++IndexAtLine)
    {
        //Set up a counter for how often a number appears and set what number we are looking for at the moment
        int SimilarityHits {0};
        int ConsideringNumber {ArrayOfArrays[0][IndexAtLine]};

        //Now look in the array of right column value ints, if it appears, up the counter by one
        for(int ScanningIndex {0}; ScanningIndex < ArraySize; ++ScanningIndex)
        {
            if(ArrayOfArrays[1][ScanningIndex] == ConsideringNumber)
            {
                ++SimilarityHits;
            }
        }
        TotalAnswer += (ConsideringNumber * SimilarityHits);
    }

    return TotalAnswer;
}


int main()
{   
    std::string Inputter {"input.txt"};
    size_t RunningTotalProblemOne {0};

    //Figure out array dimensions
    size_t ArraySize {DetermineArraySize(Inputter)};

    //Create an array on the heap that contains two pointers
    //these pointers point to an array of ints
    int** ArrayOfArrays {ReturnArrayOfInts(Inputter, ArraySize)};

    //Sort the arrays from lowest to highest
    SortArrays(ArrayOfArrays, ArraySize);

    //Solve problem 1
    int AnswerProblem1 {SolveProblemOne(ArrayOfArrays, ArraySize)};
    std::cout << "Problem 1: " << AnswerProblem1 << std::endl;

    //Solve problem 2s
    int AnswerProblem2 {SolveProblemTwo(ArrayOfArrays, ArraySize)};
    std::cout << "Problem 2: " << AnswerProblem2 << std::endl;

    
    //Let's be good lads and clear up memory
    delete[] ArrayOfArrays[0]; 
    delete[] ArrayOfArrays[1];
    delete[] ArrayOfArrays; 
    

}
