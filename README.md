# Leave Suggestions

A terminal based python tool for suggesting when to take days leave 

## Sample output

    Key:
        H = holiday
        S = weekend
        h = suggested holiday
        . = working day

       . . . . S S . . . . . S S . . . . . S S . . . . . S S . . . h 
             . S S . . . . . S S . . . . . S S . . . . . S S . . . . 
             . S S h . . . . S S . . . . . S S . . . . . S S . . . . . S S 
     . . . h . S S . . . . . S S . . . . . S S . . . . . S S . . 
         . . . S S h . . . . S S . . . . . S S . . . . . S S . . . . . 
               H H H H H H H H H H H H H H S S . . . . . S S . . . . . S S 
     . . . . . S S . . . . . S S h . . . . S S . . . . . S S . . . 
           . . S S . . . . . S S . . . h . S S . . . . . S S . . . . . S 
                 S . . . . . S S . . . . . S S h . . . . S S . . . . . S S . 
       . . . . S S . . . . . S S . . . h . S S . . . . . S S . . . . 
             . S S . . . . . S S . . . . . S S h . . . . S S . . . . . S 
                 S . . . . . S S . . . . . S S . . . h . S S . . . . . S S . . 
    max days between holidays ignoring suggestions: 200
    max days between holidays with suggestions: 31
    days leave not used (with suggestions): 1

