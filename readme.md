## Fastest slide calculation


### Initial notes

The problem required, being given a "pyramid", to calculate the path that went from the top to the bottom of it in which the sum of the values of the nodes was the lowest possible.
    
It wouldn't be strictly needed but two external packages are used for completeness:
1. **sys** this is used to ensure the correct path to the input file
2. **argparse** this is used to add a bit of functionality with some arguments to the script

The script can be run directly, and it will read the input in the `input` file.  
It is possible to also use the `-f FILE` option to use a specific file and the `-a` flag to use an alternative way (top-down) to calculate the path. This is explained later.

### The solution



### Initial assumptions

1. The data provided is complete pyramid, meaning that every row has one more element than the previous row, all the rows are present and all the values are valid integers  
2. There is no need to keep track of the path followed, only the total distance is needed
3. If there are multiple path that are equally short it doesn't matter which one you pick  

Additional checks could be added to validate the input data to ensure some of those assumptions but that feel unnecessary for the assignment.


### Reasoning

To visualize better the problem there is this structure that represent the pyramid:

    A        0
    B       0 1
    C      0 1 2
    D     0 1 2 3
    E    0 1 2 3 4
    F   0 1 2 3 4 5
    G  0 1 2 3 4 5 6
    H 0 1 2 3 4 5 6 7

There are a few quick observation:
* Since we have no information on the specific nodes even knowing the depth of the pyramid we can't extract data on which path is the lowest sum unless we traverse the whole path.
* Every node, except the leaves, always has two children, and most children have two parents with the exceptions being the leftmost and rightmost children, which have one parent, of every row and the root.
* To traverse the different routes we can start from the top or the bottom.


#### Top-down solution

Starting from the top require adding the minimum of the available parents of a node to its value.
The parents of a node, being i the index of the node, are equal to `i-1` and `i` on the previous row. 
Every new row will then contain the lowest sum path for that specific node on that row
Repeating this until the last row will have the lowest sum path for every leaf. At this point the minimum value on the last row will be the lowest sum path of the pyramid

The general formula is, being current the current row, parent the previous row and i the index of the current node we have 3 cases:
* `i = 0` node path value is equal to `current[i] + parent[i]`
* `i = len(current)-1` node path value is equal to `current[i] + parent[i-1]`
* every other case, node path value is equal to `current[i] + min(parent(i-1), parent(i))`


#### Bottom-up solution

Starting from the bottom require to adding the minimum of the children to the parent.
The children of a node, being i the index of the node, are equal to `i` and `i+1` on the lower row.
Every new row will then contain the lowest sum path up to that node.
Repeating this until the topmost row will leave a single node which contains the lowest sum path.

The general formula is, being current the current row, children the lower row and i the index of the current node we have only one case:
* node path value is equal to `current[i] + min(children(i), children(i+1))`

Due to how the pyramid "is" the children row will always be one element bigger than the parent, so `i+1` will be valid

#### Top-down vs Bottom-up

While both solutions can work, and the bottom-up looks cleaner there is a difference between them due to how file are read. Normally reading a file goes from the beginning to the end without loading the whole file in memory, this allows the top-down method to execute without needing to load everything in memory before executing. This can be very important depending on the size of the input.

At the end in the solution it was chosen to keep both the methods having the bottom-up as default, but allowing the user to select the other method with the `-a` flag.

