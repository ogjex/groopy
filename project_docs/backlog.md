GETTING GROOPY
# THE BIG FAT BACKLOG

## code
- correct naming conventions
    - functions lower_case
    - classes UpperCase
    - doc strings for all functions
    - check up on conversions of int and strings in person_editor
    - create exceptions and trys to handle
    
## model:

- ~~set up MVP~~
- ~~add person class~~
    - ~~create persons~~
- ~~add group class~~
    - ~~create groups~~
    - check for warnings based on attributes of the person
        - add specific variables check (same or not same)
- ~~add group_editor~~
    - ~~save json~~
    - ~~load json~~
- ~~add person_editor~~
    - ~~load and read person csv~~
    - ~~add shuffle persons (for new group sorting)~~
    - add shuffled_persons as instance variable 
- add grouping_module
    - sort into groups based on 
        - ~~gender~~
        - ~~background~~
        - set specific variables (eg attributes same or different groups preferred)
- add logging module
- add supervisor module
- add workshop module
    - location
    - date
    - time
    -

## view:
- set size to 1920x1080
- ~~add group_widget~~
    - ~~save groups~~
- add details_window
    - show csv file into rows and columns
    - add drag and drop for csv
    - add drag 
- add workspace_window
    - import people
    - open groups
    - save (only if save as filename have been set)
    - save as
    - sort into groups? (maybe move this to sorter_window)
- add sorter_window

## presenter:
- add save csv file (use shuffled group)
- integrate details with main_window
