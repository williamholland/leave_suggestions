# Leave Suggestions

A terminal based python tool for suggesting when to take days leave 

## How to Use

Simply run `main.py` with python 2.7

    python2 main.py

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
    suggested dates:
        31/01/2019
        04/03/2019
        04/04/2019
        06/05/2019
        15/07/2019
        15/08/2019
        16/09/2019
        17/10/2019
        18/11/2019
        19/12/2019


# To do list

* have a file to configure start and end dates, leave allowance and booked holidays
* include english or scottish bank holidays with commandline flag
* unit tests
