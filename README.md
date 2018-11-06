# Leave Suggestions

A terminal based python tool for suggesting when to take days leave 

## Problem

I have a given number of days leave to take from work each year. I plan a
couple of holidays each year where I take a few consecutive days off. After
booking those holidays I still have some days leave to take, how can I use
those days optimally?

## Solution

This algorithm works to minimize the largest consecutive extent of working days
between breaks by suggesting when to take one-day breaks.

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

         M T W T F S S M T W T F S S M T W T F S S M T W T F S S M T W T F S S  
    Jan    . . . . S S . . . . . S S . . . . . S S . . . . . S S . . . . 
    Feb          h S S . . . . . S S . . . . . S S . . . . . S S . . . . 
    Mar          . S S . . h . . S S . . . . . S S . . . . . S S . . . . . S S 
    Apr  . . . . . S S h . . . . S S . . . . . S S . . . . . S S . . 
    May      . . . S S . . . h . S S . . . . . S S . . . . . S S . . . . . 
    Jun            H H H H H H H H H H H H H H S S . . . . . S S . h . . . S S 
    Jul  . . . . . S S . . . . . S S . . . . . S S . . . . h S S . . . 
    Aug        . . S S . . . . . S S . . . . . S S . . . . . S S . . h . . S 
    Sep              S . . . . . S S . . . . . S S . . . . . S S . . . . . S S h 
    Oct    . . . . S S . . . . . S S . . . . . S S . . . . . S S . . . h 
    Nov          . S S . . . . . S S . . . . . S S . . . . . S S . . . . . S 
    Dec              S . h . . . S S . . . . . S S . . . . . S S H H H H H S S . . 

    max days between holidays ignoring suggestions: 191
    max days between holidays with suggestions: 32
    suggested dates:
         1. 01/02/2019
         2. 06/03/2019
         3. 08/04/2019
         4. 09/05/2019
         5. 25/06/2019
         6. 26/07/2019
         7. 28/08/2019
         8. 30/09/2019
         9. 31/10/2019
        10. 03/12/2019


# To do list

* choose cfg file with commandline arg
* include english or scottish bank holidays with commandline flag
* unit tests
