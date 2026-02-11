function sort(){
    let n;
    n=getSize();
    quickSort(0,n-1);
}

function partition(start, end)
{
    let pivot = getValue(start);
 
    let count = 0;
    for (let i = start + 1; i <= end; i=i+1) {
        if (getValue(i) <= pivot){
            count=count+1;
        }
    }

    let pivotIndex = start + count;
    swap(pivotIndex, start, 300);

    let i = start, j = end;
 
    while (i < pivotIndex and j > pivotIndex) {
 
        while (getValue(i) <= pivot) {
            i=i+1;
        }
 
        while (getValue(j) > pivot) {
            j=j-1;
        }
 
        if (i < pivotIndex and j > pivotIndex) {
            swap(i, j, 300);
            i=i+1;
            j=j-1;
        }
    }
    return pivotIndex;
}
 
function quickSort(start, end)
{
    if (start >= end){
        return;
    }
    let p = partition(start, end);
    quickSort(start, p - 1);
    quickSort(p + 1, end);
}