#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <unordered_set>
#include <string>
#include <iterator>
#include <sstream>


std::vector<std::string>* ReadLines(std::string Path)
{
    //This function reads each line from the .txt and populates a vector of strings where each string element is a full line
    
    //Create a vector of std::strings on the heap
    std::vector<std::string>* P_VectorOfStrings = new std::vector<std::string> {};

    //Start reading the file
    std::ifstream InputContents (Path);
    std::string StoreString {};

    if(InputContents.is_open())
    {
        //File exists, let's get crackin'
        while(getline(InputContents, StoreString))
        {   
            P_VectorOfStrings->emplace_back(StoreString);
        }
        return P_VectorOfStrings;

    }else if(!InputContents.is_open()){
        //File does not exist, exit early
        std::cout << "Error, no file available!" << std::endl;
    }
    return P_VectorOfStrings;
}


std::vector<size_t>* FindKeyWordLocations(std::string StringFromFile, std::string KeyWord)
{
    //Create a vector of size_t that logs all locations of the keyword in the string
    std::vector<size_t>* P_KeyWordLocations = new std::vector<size_t> {};

    //Find the first instance of the keyword, starting at index 0
    size_t Position {StringFromFile.find(KeyWord, 0)};

    //As long as Position is not at the end of the string
    while(Position != std::string::npos)
    {
        P_KeyWordLocations->emplace_back(Position);
        //Find a new keyword location, one index up from previous location, so:  (14124[Key]1242Key14) >> 14124K(ey1242[Key]14) 
        Position = StringFromFile.find(KeyWord, Position + 1);
    }
    return P_KeyWordLocations;
}


std::vector<std::string>* GrabKeyWordContents(std::string StringFromFile, std::vector<size_t>* P_KeyWordLocations, size_t KeyWordSize, std::string KeyWordCap)
{
    /*The general idea is to create a vector that contains strings of digits isolated from the .txt
    So for example:
        vec<
            str(2,4)
            str(12,88)
            str(771,2)
        >
    */

    //Setting up some string properties
    size_t SizeOfString {StringFromFile.size()};
    size_t AmountOfAnchors {P_KeyWordLocations->size()};

    //Store strings between "mul(" and ")" here, these might contain valid multiple pairs
    std::vector<std::string>* P_KeywordContents = new std::vector<std::string> {};

    /*Now we start parsing the whole line as given in the .txt
     We first check all spaces between the anchor points, and lastly between the last anchor point and the index at the end of the string
     As a reminder: All anchor points are just the list indices of where the keyword starts*/

    for(size_t i_Anchor {0}; i_Anchor < AmountOfAnchors - 1; ++i_Anchor)
    //We check up to the amount of anchors - 1, because we're intested in the distances to the next anchor point
    {
        for(size_t i_Char {(*P_KeyWordLocations)[i_Anchor] + KeyWordSize}; i_Char < (*P_KeyWordLocations)[i_Anchor + 1]; ++i_Char)
        /*THIS FUCKERY EXPLAINED IN DETAIL:
            We start looking at each anchor point in P_KeyWordLocations, and we need to be mindful of its distance to the next keyword, hence we don't use auto
            Once we have an achor point, we iterate over each following character UP TO the start of the next anchor point.
            thus:
                -init i_Char as the current anchor point:      size_t i_Char {(*P_KeyWordLocations)[i_Anchor] + KeyWordSize}
                    -We add KeywordSize because we want to start checking at the END of the keyword, not include it
                -check up to the next anchor point:            i_Char < (*P_KeyWordLocations)[i_Anchor + 1]
                    -[Anchor + 1] because we look for the start of the next keyword segment

            THIS LEAVES US WITH A NON-CONSIDERED TAIL END:
                from the last anchor point to the end of the string
        */
        {   
            if(StringFromFile[i_Char] == KeyWordCap[0]) //Now, currently, we are assuming the KeyWordCap is just ")", so a single character
            {
                //This grabs everything between the KeyWord and KeyWorkCap and adds it to a vector of strings
                //The MIGHT be valid entries, but could also contain junk
                P_KeywordContents->emplace_back((
                StringFromFile.begin() + (*P_KeyWordLocations)[i_Anchor] + KeyWordSize),
                StringFromFile.begin() +i_Char);
                break;
            }
        }            
    }

    //Just need to check the last tail bit now, logic is similar to all the previous anchor point fuckery, just 
    //adjusted to check from the last anchor point to the end of the string
    //Yes, this IS inefficient, as the code from the loop before can be retailored to also include this bit, but fuck it, it works
    for(size_t i_Char {(*P_KeyWordLocations)[AmountOfAnchors - 1] + KeyWordSize}; i_Char < SizeOfString; ++i_Char)
    {
        if(StringFromFile[i_Char] == KeyWordCap[0])
        {
            P_KeywordContents->emplace_back((
            StringFromFile.begin() + (*P_KeyWordLocations)[AmountOfAnchors - 1] + KeyWordSize),
            StringFromFile.begin() +i_Char); 
            break;  
        }
    }

    //std::vector<std::string>*
    return P_KeywordContents;
}


bool SplitIntoTwoNumbers(std::string KeyWordContainer, std::string SplitPoint)
{
    //Check to see if a string does indeed split into two, and only two, numbers

    std::stringstream Stream (KeyWordContainer);
    std::string Element {};  //This could be a number, or could be junk

    //Store all isolated elements here
    std::vector<std::string> VectorOfElements {};

    while(!Stream.eof())
    {
        getline(Stream, Element, SplitPoint[0]);
        VectorOfElements.emplace_back(Element);
    }

    if(VectorOfElements.size() == 2)
    //Only valid entries split into two 
    {   
        for(auto Element : VectorOfElements)
        //Check either element of the two
        {
            for(size_t i_Char {0}; i_Char < Element.size(); ++i_Char)
            //Go through each character
            {
                if(!isdigit(Element[i_Char]))
                //As soon as a non-digit is detected, toss it
                {
                    return false;
                }
            }
        }
        //Ostensibly, the container splits into two numbers
        return true; 
    }
    //Maybe the container is empty, in either case return false unless otherwise
    return false;
}


int MultiplyStringElements(std::string StringWithNumbers, std::string SplitPoint)
{
    //We have a string that has two numbers, separated by a comma, return the product of this string

    //Store the two numbers for multiplication here
    int MultiplyThese[2] {};
    int ReturnMultiple {1};

    //Extract the numbers
    std::stringstream Stream {StringWithNumbers};
    std::string NumberAsString {};
    size_t StringCounter {0};

    while(!Stream.eof())
    {
        getline(Stream, NumberAsString, SplitPoint[0]);
        MultiplyThese[StringCounter] = stoi(NumberAsString);
        ++StringCounter;
    }

    for(auto Number : MultiplyThese)
    {
        ReturnMultiple *= Number;
    }

    return ReturnMultiple;
}


int ReturnValidMultiples(std::vector<std::string>* P_KeyWordContents, std::string SplitPoint)
{
    //Now we can start scanning each KeyWord-KeyWordCap container and check if they are valid
    // i.e.       mul(12,23)     >> "12,23"        >>     Valid       >>     12*23      >>    276
    //            mul( 22, when) >> " 22, when"    >>     Not Valid 

    //Setting up some function essentials
    int ProductsTalliedPerLine {0};
    size_t ElementsInVector {P_KeyWordContents->size()};

    for(size_t i_Element {0}; i_Element < ElementsInVector; ++i_Element)
    //Loop through each KeyWord-KeyWordCap container
    {
        if(SplitIntoTwoNumbers((*P_KeyWordContents)[i_Element], SplitPoint))
        //Chop up the string into parts, see if it returns two and only two numbers
        {
            //From here on, we KNOW we have two numbers in a string, separated by a comma, let's multiply them
            ProductsTalliedPerLine += MultiplyStringElements((*P_KeyWordContents)[i_Element], SplitPoint);
        }
    }

    return ProductsTalliedPerLine;

}


int SolveProblemOne(std::vector<std::string>* P_VectorOfStrings, std::string KeyWord, std::string KeyWordCap, std::string SplitPoint)
{
    //We approach the problem by looping through each line in the input text as an std::string
    //We first isolate all indices where the keyword starts
    //Then, using those indices scan the segments of string up until a keyword cap and store that info in a vector of strings
    //Then we can analyse the contents stored between each keyword-keywordcap pair
    

    int RunningTotal = {0};

    for(auto StringFromFile : *P_VectorOfStrings)
    {
        //For each full line, as string, from the text file
        //Create a vector of all size_t locations of the keyword per line in the .txt file
        std::vector<size_t>* P_KeyWordLocations {FindKeyWordLocations(StringFromFile, KeyWord)};

        //Then isolate the valid pairs of digits from the string, per line
        std::vector<std::string>* P_KeyWordContents {GrabKeyWordContents(StringFromFile, P_KeyWordLocations, KeyWord.size(), KeyWordCap)};

        //Now we need to check the contents of each KeyWord-KeyWordCap Container in P_KeyWordContents if they contain two,
        //and ONLY two numerical values separated by a comma, if so, multiply these values and return
        RunningTotal += ReturnValidMultiples(P_KeyWordContents, SplitPoint);

        //We don't need these pointers once the whole line has been read, release the memory until the next line is read
        delete P_KeyWordContents;
        P_KeyWordContents= nullptr;
        delete P_KeyWordLocations;
        P_KeyWordLocations = nullptr;              
    }

    return RunningTotal;
}


std::vector<size_t>* CreateSafeRanges(std::string& StringFromFile, std::vector<size_t>* P_DoLocations, std::vector<size_t>* P_DontLocations)
{
    //Why did you open this? Why are you reading this? Close this tab so HELP ME GOD CLOSE THIS TAB AND DON'T LOOK AT THE CRIMES BELOW

    bool SearchingForDont {true};
    std::vector<size_t>* P_SafeRanges = new std::vector<size_t> {0};  //Starting with 0, because you always start a line on do()
                                                                      //NO THIS IS WRONG, EACH LINE INHERITS THE LAST LINE'S DO OR DON'T CONDITION
    for(size_t i_Char {0}; i_Char < StringFromFile.size(); ++i_Char)
    //Look. Listen. I'm not proud of what I have done here, but please understand. 
    //I couldn't think of a more efficient way
    {
        if(SearchingForDont)
        {
            for(auto Dont : *P_DontLocations)
            {
                if(Dont == i_Char)
                {
                    P_SafeRanges->emplace_back(i_Char);
                    SearchingForDont = false;
                
                }
            }
        }else if(!SearchingForDont){
            for(auto Do : *P_DoLocations)
            {
                if(Do == i_Char)
                {
                    P_SafeRanges->emplace_back(i_Char);
                    SearchingForDont = true;
                }
            }
        }
    }

    return P_SafeRanges;

}


std::vector<size_t>* FilterKeyWordLocations(std::vector<size_t>* P_SafeRanges, std::vector<size_t>* P_KeyWordLocations)
{
    //Cut down on locations from P_KeyWordLocations based on if or not they fall within safe ranges

    std::vector<size_t>* P_FilteredLocations = new std::vector<size_t> {};

    //Look at each location
    for(size_t i_Location {0}; i_Location < P_KeyWordLocations->size(); ++i_Location)
    {
        size_t CurrentLocation {(*P_KeyWordLocations)[i_Location]};
        
        //Now see if this KeyWordLocation falls within a safe range
        for(size_t i_SafeRange {0}; i_SafeRange < P_SafeRanges->size() - 1; ++i_SafeRange)
        //Checking up to size of SafeRange - 1, because we only want to look at the uneven numbered indices
        //The vector is structured as <start of range, end of range, start of range, end of range,...>
        {   if( !(i_SafeRange % 2))
            /*Right, let's delve into the above conditional, because it has caused you some headache
              You want the uneven numbered indices, since the vector has the safe range starting points on the uneven indices

              So when the loop is considering an uneven index in the P_SafeRange vector, you want the if statement to run
                
                -check for even-ness using % 2
                -for uneven numbers (1st in the vector), realise you count the index as an even number (index 0)
                -read that again,  1st element is at index 0
                -so for an uneven element, (i_element % 2) resolves to (0), when then is interpreted as if(0) > false
                -So we need to negate this using the ! operator

                example: 
                            <0, 2, 6, 9, 11, 20>

                            element:      6
                            i_element:    [2]
                            Expectation:  the condition is met, run the code

                            if(!(2 % 2))
                            if(!(  0  ))
                            if(!(false))
                            if(true)
                               >> runs the code
            
            */
            {
                if(CurrentLocation > (*P_SafeRanges)[i_SafeRange] && CurrentLocation < (*P_SafeRanges)[i_SafeRange + 1])
                {
                    P_FilteredLocations->emplace_back(CurrentLocation);
                    break;
                }
                
            }

        }
        
    }
    return P_FilteredLocations;

}


int SolveProblemTwo(std::vector<std::string>* P_VectorOfStrings, std::string KeyWordDo, 
std::string KeyWordDont, std::string KeyWord, std::string KeyWordCap, std::string SplitPoint)    //May God have mercy on my undeserving soul
{
    /*
    Right, here is the plan. We're going to run GrabKeyWordContents() on the keywords "do()" and "don't()"
    Creating new anchor vectors of all the DO and DONT statements, we then basically run problem one again, but check
    everything vs if they fall in a DO range
    !!!(((DO ranges start at 0, all lines start as DO)))
        NO THIS IS WRONG, EACH LINE INHERITS THE LAST LINE'S DO OR DON'T CONDITION
    */
    
    //penis
    
    int RunningTotal {0};

    for(auto StringFromFile : *P_VectorOfStrings)
    //Scan each line from the input file, isolate the indices of where DO and DONT start
    {   
        std::vector<size_t> SafeRanges {0};
        bool SearchingForDont {true};

        std::vector<size_t>* P_DoLocations   {FindKeyWordLocations(StringFromFile, KeyWordDo)};
        std::vector<size_t>* P_DontLocations {FindKeyWordLocations(StringFromFile, KeyWordDont)};

        std::vector<size_t>* P_SafeRanges {CreateSafeRanges(StringFromFile, P_DoLocations, P_DontLocations)};
        
        //This little snippet essentially "caps off" do-ended safe ranges with the end of the string
        if((P_SafeRanges->size() % 2)){P_SafeRanges->emplace_back(StringFromFile.size());}

        //You have here now a Vector in P_SafeRanges where every uneven index lists the start index in the string of DO
        //                                             and every even index lists the start index in the string of DONT

        //From here on out, we follow ProblemOne logic, but we also make sure that any KeyWord-KeyWordCap containers fall in a safe range

        //Grab ALL possible keyword locations (this is like problem one)
        std::vector<size_t>* P_KeyWordLocations {FindKeyWordLocations(StringFromFile, KeyWord)};

        //Remove any locations that don't fall in safe ranges
        std::vector<size_t>* P_FilteredKeyWordLocations(FilterKeyWordLocations(P_SafeRanges, P_KeyWordLocations));

        //Running more problem 1 logic, but with a filtered KeyWord vector
        std::vector<std::string>* P_KeyWordContents {GrabKeyWordContents(StringFromFile, P_FilteredKeyWordLocations, KeyWord.size(), KeyWordCap)};
        RunningTotal += ReturnValidMultiples(P_KeyWordContents, SplitPoint);


    //Good boys delete and reset their pointers
    delete P_DoLocations;
    P_DoLocations = nullptr;
    delete P_DontLocations;
    P_DontLocations = nullptr;
    delete P_SafeRanges;
    P_SafeRanges = nullptr;
    delete P_KeyWordLocations;
    P_KeyWordLocations = nullptr;
    delete P_FilteredKeyWordLocations;
    P_FilteredKeyWordLocations = nullptr;


    } 
    return RunningTotal;
}


std::vector<std::string>* CompoundVectorsIntoOne(std::vector<std::string>* P_VectorOfStrings)
{
    /*Right, so this is a kludgey fix to solve an issue with Problem 2 that you have, by now, poured hours into
      You assumed each new line in the .txt automatically start with DO, which is not true.
      If a previous line ended on a DONT, this line keeps that condition
      Sadly, it would take a lot of work to restructure all that code, so the simple fool's solution:
          Just take the vector of all strings and make it so it only contains ONE string
      Yes, it's dumb as all hell, but it has taken 3 days so far, it is time to solve this and move on*/

    std::vector<std::string>* P_AllChuckedIntoOne = new std::vector<std::string> {};
    std::string BuildAString {};

    for(auto i : *P_VectorOfStrings)
    {
        BuildAString += i;
    }

    P_AllChuckedIntoOne->emplace_back(BuildAString);
    
    return P_AllChuckedIntoOne;
}


int main()
{   

    //Input path to the .txt file
    const std::string& Path {"input.txt"};

    //Read in the input text file, parse each line and populate vector with strings per line
    std::vector<std::string>* P_VectorOfStrings = ReadLines(Path);
    //We now have a vector of strings, where each line in the .txt file corresponds to a std::string in the vector
    
    int AnswerProblemOne = SolveProblemOne(P_VectorOfStrings, "mul(", ")", ",");
    std::cout << "Problem 1: " << AnswerProblemOne << std::endl;

    //You made an assumption that turned out to be wrong, so for the the pipeline to function, you have to alter the way
    //the strings are stored, essentially you make it all one big string to get rid of a DO/DONT switch problem
    //....fun!
    P_VectorOfStrings = CompoundVectorsIntoOne(P_VectorOfStrings);

    int AnswerProblemTwo = SolveProblemTwo(P_VectorOfStrings, "do()", "don't", "mul(", ")", ",");
    std::cout << "Problem 2: " << AnswerProblemTwo << std::endl;


    //Once we're done, clean up pointers
    delete P_VectorOfStrings;
    P_VectorOfStrings = nullptr;

    return 0;
}
