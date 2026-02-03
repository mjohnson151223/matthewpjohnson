//main.cpp
//Matthew Johnson
//lab1

#include "myfunctions.h"

int main(){

    int userInt = getUserInput();

    cout << "The User Entered: " << userInt << endl;

    int nums[DATA_SIZE];

    nums[0] = userInt;

    for (int i = 1; i < DATA_SIZE; i++){
        nums[i] = i;
    }

    double average = calculateAverage(nums);

    cout << "Average Value: " << average << endl;

    return 0;
}



