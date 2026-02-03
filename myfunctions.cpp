//myfunctions.cpp
//Matthew Johnson
//lab1

#include "myfunctions.h"

double calculateAverage(int nums[])
{
    double sum = 0;
    for (int n = 0; n < DATA_SIZE; n++)
    {
        sum += nums[n];
    }

    return sum / DATA_SIZE;
}

void promptUser(){
    cout << "Hello. Enter a number: ";
}

int getUserInput()
{
    int userInput;
    promptUser();
    cin >> userInput;
    return userInput;
}
