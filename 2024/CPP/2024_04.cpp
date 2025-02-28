#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <string>
#include <iterator>
#include <sstream>
#include <regex>



void PrintVector(std::vector<char> VectorToPrint)
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
    std::vector<std::vector<char>>* P_VectorOfVectorOfChars = new std::vector<std::vector<char>> {};

    //Start reading the file
    std::ifstream InputContents (Path);
    std::string StoreString {};

    if(InputContents.is_open())
    {
        //File exists, let's get crackin'
        while(getline(InputContents, StoreString))
        {   
            //Right now we have a single line of text from the .txt

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


std::vector<std::vector<char>>* TransposeVectorsVertically(std::vector<std::vector<char>>* P_OriginalMatrixVectors, int n_Rows, int n_Columns)
{   
    //Take the orignal matrix of vectors and create a copy that has its axes switched, so horizontal becomes vertical and vice versa
    //THIS ONLY WORKS FOR MATRICES WHERE ROWS=COLUMNS, LOPSIDED ONES WILL CAUSE A SEG FAULT

    std::vector<std::vector<char>>* P_VerticallyTransposedMatrix = new std::vector<std::vector<char>> {*P_OriginalMatrixVectors};

    //Start swapping vector elements, one row at a time, one column at a time
    for(int i_Rows {0}; i_Rows < n_Rows; ++i_Rows)
    {
        for(int i_Columns {i_Rows}; i_Columns < n_Columns; ++i_Columns)
        /* on why we init i_Columns to i_Rows
           if we set i_Columns to 0, which might feel intuitive, what ends up happening is that the same location gets swapped twice.
           Consider:

           a b       Looping through line, then index of line, we can get [0][1], in this case b
           d f     

           swapping this, after the call for i_Rows = 0 has completed, the grid looks like this
           where b and d are successfully swapped

           a d
           b f

           now the loop continues the call for i_Rows = 1 and at [1][0], it swaps he b back to [0][1], nullifying the earlier action

           a b
           d f

           if we set i_Columns to i_Rows, we essentially "cut the matrix in half", only ever swapping values above the diagonal

           a b c d e
           * g h i j
           * * m n o
           * * * s t
           * * * * y
           
           Note that this only works for matrices where n_Rows = n_Columns

        */
        {
            std::swap((*P_VerticallyTransposedMatrix)[i_Rows][i_Columns], (*P_VerticallyTransposedMatrix)[i_Columns][i_Rows]);
        }
    }

    return P_VerticallyTransposedMatrix;
}


std::vector<std::vector<char>>* TransposeVectorsDiagonally(std::vector<std::vector<char>>* P_OriginalMatrixVectors, int n_Rows, int n_Columns)
{
    //Creates diagonals by iterating through the matrix in a bottom-left to top-right manner 
    std::vector<std::vector<char>>* P_DiagonalVectors = new std::vector<std::vector<char>> {};

    for(int i_Rows {0}; i_Rows < n_Rows + n_Columns - 1; ++i_Rows)
    //Think of (n_Rows and n_Columns - 1) as the perimeter of the matrix, we subtract 1 since n_Rows and n_Columns share a corner
    //The below code "walks around" this perimeter
    {   
        //Build diagonals here
        std::vector<char> BuildADiagonalVector {};
        

        for(int i_Columns {0}; i_Columns < i_Rows + 1; ++i_Columns)
        {   
            if(i_Rows < n_Rows)
            //All diagonals here start from the leftmost position in the row 
            {
                BuildADiagonalVector.emplace_back((*P_OriginalMatrixVectors)[i_Rows-i_Columns][i_Columns]);
            }
            else{
                //And from here diagonals start "below" the actual matrix, so their actual starting point needs to be shifted toward the right
                //However the calculation can spit out a vector row that doesn't exist, so we need to make sure the Rows index stays positive
                if((i_Rows + ((n_Rows - i_Rows - 1) - i_Columns) >= 0) && ((i_Columns + (i_Rows - n_Rows) + 1) < n_Columns))
                {
                    //Look, this ain't pretty, but it works, donnit? Just don't touch it anymore and you'll be fine.
                    BuildADiagonalVector.emplace_back((*P_OriginalMatrixVectors)[i_Rows + ((n_Rows - i_Rows - 1) - i_Columns)][i_Columns + (i_Rows - n_Rows) + 1]);
                }    
            }
        }
        P_DiagonalVectors->emplace_back(BuildADiagonalVector);
    }

    return P_DiagonalVectors;
}


std::vector<std::vector<char>>* ReverseVectors(std::vector<std::vector<char>>* P_VectorToReverse)
{
    //Takes a vector and reverses it
    std::vector<std::vector<char>>* P_ReversedVector = new std::vector<std::vector<char>> {};

    for(auto VectorOfChars : (*P_VectorToReverse))
    {
        std::vector<char> ReversingVector {VectorOfChars};
        std::reverse(ReversingVector.begin(), ReversingVector.end());
        P_ReversedVector->emplace_back(ReversingVector);
    }

    return P_ReversedVector;
}


size_t CountKeyWordPerLine(std::string& Line, std::string& KeyWord)
{
    //Counts all instances of a keyword in a string using regex, the sregex_iterator is a long int, so we return that instead of size_t
    
    /*UNDERSTANDING ITERATORS, REGEX AND STD::DISTANCE

    The key player here is std::distance, this does the actual looping and matching through the string.
    sregex_iterator Begin and End are just arguments you prepare to feed to the std::distance loop.

    std::distance will start at Begin, and move the iterator up each time it encounters the KeyWord, once it reaches End, std::distance stops searching
    and returns the final count of the steps the iterator had to take.
    */
    
    //Turn KeyWord into a regex object
    std::regex KeyWordRegex {KeyWord};

    //Create start and end points for the string
    std::sregex_iterator Begin(Line.begin(), Line.end(), KeyWordRegex);
    std::sregex_iterator End {};

    //Loop through Line and count the frequency of KeyWord, this can be returned directly, but is written like this for readability
    

    return std::distance(Begin, End);
}


size_t ReturnKeyWordCount(std::vector<std::vector<char>>* P_FullMatrix, std::string KeyWord)
{   
    //Count all occurances of the keyword in the passed Matrix, which can be a matrix reading lines in any direction
    size_t KeyWordFrequency {0};

    for(size_t i_Line {0}; i_Line < P_FullMatrix->size(); ++i_Line)
    //Basically pop all the chars in the vector from the line into a single string so you can count 
    //the keywords using regex
    {
        std::string BuildStringFromLine{};

        for(size_t i_Character {0}; i_Character < (*P_FullMatrix)[i_Line].size(); ++i_Character)
        {
            BuildStringFromLine += (*P_FullMatrix)[i_Line][i_Character];
        }
        //We now have the vector as a string, so we can Regex it
        KeyWordFrequency += CountKeyWordPerLine(BuildStringFromLine, KeyWord);
    }


    return KeyWordFrequency;
}


size_t SolveProblemOne(std::vector<std::vector<char>>* P_OriginalVector, size_t n_Rows, size_t n_Colums, std::string KeyWord)
{
    size_t RunningTotal {0};
    /*
    The approach:
      P_OriginalVector points to the vector of vectors of chars of the text file as it was given
      With the use of the Transpose and the Reverse vector functions, you can create Vectors of any cardinal direction 
        (Reading Directions: E, W, N, S, NE, SE, NW, SW)
      So now all that is left to do, is to write a regex function that searches the keyword in these vectors (the vectors will have to be turned into strings)
      So this function should call a regex function on all possible reading directions, 
      passing it as an argument a function that returns a modified version of the original vector
        i.e.   Regex(Reverse(Transpose(OriginalVector)))

    */
    
    //You could probably simplify the creation of P_Vector variations below, possibly in a struct, but this works for now, so take the dub and
    //pin it as a thing in the back of your mind to think about when learning about structs

    /* KNOWN ISSUES:
        This approach creates a lot of new vectors on the heap which you don't understand how to free up yet. Ideally, you would take a copy of the original 
        P_Vector, transpose it within the same memory and then after you've done the word count, free up the memory.
        This is a great learning opportunity in following assignments and a good idea to focus on to improve.
    */

    //Standard matrix, left to right
    RunningTotal += ReturnKeyWordCount(P_OriginalVector, KeyWord);
    //Right to left
    RunningTotal += ReturnKeyWordCount(ReverseVectors(P_OriginalVector), KeyWord);
    //Up to Down
    RunningTotal += ReturnKeyWordCount(TransposeVectorsVertically(P_OriginalVector, n_Rows, n_Colums), KeyWord);
    //Down to Up
    RunningTotal += ReturnKeyWordCount(ReverseVectors(TransposeVectorsVertically(P_OriginalVector, n_Rows, n_Colums)), KeyWord);
    //Bottom Left to Top Right
    RunningTotal += ReturnKeyWordCount(TransposeVectorsDiagonally(P_OriginalVector, n_Rows, n_Colums), KeyWord);
    //Top Right to Right Left
    RunningTotal += ReturnKeyWordCount(ReverseVectors(TransposeVectorsDiagonally(P_OriginalVector, n_Rows, n_Colums)), KeyWord);
    //Bottom Right to Top Left
    RunningTotal += ReturnKeyWordCount(TransposeVectorsDiagonally(ReverseVectors(P_OriginalVector), n_Rows, n_Colums), KeyWord);
    //Top Left to Bottom Right
    RunningTotal += ReturnKeyWordCount(ReverseVectors(TransposeVectorsDiagonally(ReverseVectors(P_OriginalVector), n_Rows, n_Colums)), KeyWord);
    
    return RunningTotal;
}


std::string ReverseString(std::string StringToReverse)
{
    std::reverse(StringToReverse.begin(), StringToReverse.end());
    return StringToReverse;
}


size_t SolveProblemTwo(std::vector<std::vector<char>>* P_OriginalVector, size_t n_Rows, size_t n_Columns, std::string KeyWord)
{
    size_t RunningTotal {0};

    /*
    Approach:
        -Create a little 3x3 grid from the P_OriginalVector that acts as a subset of the whole
        -Check if the Grid[1][1] == A (A always has to act as the central pin of the X)
        -Take positions [0][0], [0][2], [2][0], [2][2] >>> use if(!(position % 2)) in a for loop to get all corners
        -Opposite diagonals are always opposite positons ([0][2] to [2][0], the positions flips)
        -build a string from this
            IF: (STRING1 == KEY || REVERSE(STRING1) == KEY) &&  STRING2 == KEY || REVERSE(STRING2)
                THEN: we have a 3x3 grid with a valid cross, tally it and slide the window up
     */

    //Create a small 3x3 grid, like a subset of the whole matrix, then check if the element at [1][1] is 'A'
    //Since 'A' is always at the cente of the cross, discard all subsets that can't contain the MAS-cross
    for(size_t i_Rows {0}; i_Rows < n_Rows-2; ++i_Rows)
    {
        for(size_t i_Columns {0}; i_Columns < n_Columns-2; ++i_Columns)
        {
            if((*P_OriginalVector)[i_Rows + 1][i_Columns + 1] == KeyWord[1])
            {
                //Now we build two strings, upwards and downwards diagonals
                std::string DiagonalDown {};
                DiagonalDown += (*P_OriginalVector)[i_Rows][i_Columns];
                DiagonalDown += (*P_OriginalVector)[i_Rows + 1][i_Columns +1];
                DiagonalDown += (*P_OriginalVector)[i_Rows + 2][i_Columns +2];

                std::string DiagonalUp {};
                DiagonalUp += (*P_OriginalVector)[i_Rows + 2][i_Columns];
                DiagonalUp += (*P_OriginalVector)[i_Rows + 1][i_Columns +1];
                DiagonalUp += (*P_OriginalVector)[i_Rows][i_Columns +2];

                //The below condition checks if the word "MAS" appears in any combination in the cross
                if (((DiagonalDown == KeyWord) || (ReverseString(DiagonalDown) == KeyWord)) &&
                    ((DiagonalUp == KeyWord) || (ReverseString(DiagonalUp) == KeyWord)))
                    {
                        RunningTotal += 1;
                    }
            }  
        }
    }
    return RunningTotal;
}


int main()
{   
    //Input path to the .txt file
    const std::string& Path {"input.txt"};

    //Read in the input text file, parse each line and create a vector of vectors of chars
    //Like <<a, b, c>, <d, e, f>, <g, h, i>>
    std::vector<std::vector<char>>* P_VectorOfVectors = ReadLines(Path);

    //Some size info about the matrix/grid
    size_t n_Rows    {P_VectorOfVectors->size()};
    size_t n_Columns {(*P_VectorOfVectors)[0].size()};
    
    //KeyWords for problems.
    const std::string KeyWordProblemOne {"XMAS"};
    const std::string KeyWordProblemTwo {"MAS"};


    size_t AnswerProblemOne {SolveProblemOne(P_VectorOfVectors, n_Rows, n_Columns, KeyWordProblemOne)};
    std::cout << "Problem 1: " << AnswerProblemOne << std::endl;

    size_t AnswerProblemTwo {SolveProblemTwo(P_VectorOfVectors, n_Rows, n_Columns, KeyWordProblemTwo)};
    std::cout << "Problem 2: " << AnswerProblemTwo << std::endl;


    return 0;
}
