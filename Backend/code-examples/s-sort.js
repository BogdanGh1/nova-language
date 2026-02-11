function sort(){
    let n;
    n=getSize();
    for(let i=0;i<n;i=i+1){
        for(let j=i+1;j<n;j=j+1){
            if(getValue(i) > getValue(j)){
                print(getValue(i));
                print(getValue(j));
                swap(i,j,300);
            }
        }
    }
}