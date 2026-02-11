function sort(){
    let n;
    n=getSize();
    mergeSort(0,n-1);
}

function merge(left, mid, right)
{
    let subArrayOne = mid - left + 1;
    let subArrayTwo = right - mid;
    
    let[subArrayOne] leftArray;
    let[subArrayTwo] rightArray;

    for (let i = 0; i < subArrayOne; i=i+1){
        leftArray[i] = getValue(left + i);
    }
    for (let j = 0; j < subArrayTwo; j=j+1){
        rightArray[j] = getValue(mid + 1 + j);
    }

    let indexOfSubArrayOne = 0, indexOfSubArrayTwo = 0;
    let indexOfMergedArray = left;

    while (indexOfSubArrayOne < subArrayOne and indexOfSubArrayTwo < subArrayTwo) {
        if (leftArray[indexOfSubArrayOne]<= rightArray[indexOfSubArrayTwo]) {
            setValue(indexOfMergedArray,leftArray[indexOfSubArrayOne],300);
            indexOfSubArrayOne=indexOfSubArrayOne+1;
        }
        else {
            setValue(indexOfMergedArray,rightArray[indexOfSubArrayTwo],300);
            indexOfSubArrayTwo=indexOfSubArrayTwo+1;
        }
        indexOfMergedArray=indexOfMergedArray+1;
    }
    while (indexOfSubArrayOne < subArrayOne) {
        setValue(indexOfMergedArray,leftArray[indexOfSubArrayOne],300);
        indexOfSubArrayOne=indexOfSubArrayOne+1;
        indexOfMergedArray=indexOfMergedArray+1;
    }
    while (indexOfSubArrayTwo < subArrayTwo) {
        setValue(indexOfMergedArray,rightArray[indexOfSubArrayTwo],300);
        indexOfSubArrayTwo=indexOfSubArrayTwo+1;
        indexOfMergedArray=indexOfMergedArray+1;
    }
}

function mergeSort(begin, end)
{
    if (begin >= end){
        return;
    }
    let mid = int(begin + (end - begin) / 2);
    mergeSort(begin, mid);
    mergeSort(mid + 1, end);
    merge(begin, mid, end);
}