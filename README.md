# Leave Suggestions

A terminal based python tool for suggesting when to take days leave 

## How to Use

This program is configured with `holidays.cfg`. To add holidays add a section
with a name that starts with "Holiday", this section needs a `start_date` and
an `end_date`. For example

    [Holiday Christmas]
    start_date: 23/12/2019
    end_date: 27/12/2019

To execute the program simply run `main.py` with python 2.7

    python2 main.py

## Sample output

    Key:
        H = holiday
        S = weekend
        h = suggested holiday
        . = working day

       . . . . S S . . . . . S S . . . . . S S . . . . . S S . . . . 
             . S S h . . . . S S . . . . . S S . . . . . S S . . . . 
             . S S . . . . . S S h . . . . S S . . . . . S S . . . . . S S 
     . . . . . S S . . . . . S S h . . . . S S . . . . . S S . . 
         . . . S S . . . . . S S . . . . . S S h . . . . S S . . . . . 
               H H H H H H H H H H H H H H S S . . . . . S S . . . . . S S 
     . . . . . S S . . . . . S S . . . h . S S . . . . . S S . . . 
           . . S S . . . . . S S . . . . . S S . . h . . S S . . . . . S 
                 S . . . . . S S . . . . . S S . . . . . S S . h . . . S S . 
       . . . . S S . . . . . S S . . . . . S S . . . . . S S h . . . 
             . S S . . . . . S S . . . . . S S . . . . . S S . . . . . S 
                 S h . . . . S S . . . . . S S . . . . . S S H H H H H S S . . 
    max days between holidays ignoring suggestions: 191
    max days between holidays with suggestions: 34
    days leave not used (with suggestions): 1
    suggested dates:
         1. 31/12/2019
         2. 31/12/2019
         3. 31/12/2019
         4. 31/12/2019
         5. 31/12/2019
         6. 31/12/2019
         7. 31/12/2019
         8. 31/12/2019
         9. 31/12/2019



# To do list

* choose cfg file with commandline arg
* include english or scottish bank holidays with commandline flag
* unit tests
