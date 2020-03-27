# Refactoring Process

This is to document how I refactored a jupyter notebook into a python script.
I am using the [David Tan's refactoring guide](https://github.com/davified/clean-code-ml/blob/master/docs/refactoring-process.md)

Before you begin refactoring:  
1. Converted the notebook into a python file
    - converted '1_snapshot_transformation.ipynd' to 'etl_processing.py'
2. Run the notebook successfully
    - was able to recreate the csv data at the end
3. Remove all print statements   
4. Read and write code smells that you observe 
    - Variables
        - bad variable names (not descriptive)
        - inconsistent terminology 
        - variables purpose is not clear
    - Dispensables
        - lots of comments
        - dead code
    - Functions
        - lack of functions
        - cases of repetition in code
        - lots of side effects currently being done
        - lots of conditions that can be made into functions
        - areas where code should be broken down into many functions
    - Design
        - Need to avoid exposing internals
        - will call the 'snapshot_creator.py' to run main functions abstracted away in 'etl_processing.py'
        
The Refactoring Cycle:
1. Identify a block of code that can be extracted into a pure function
2. Pseudo-TDD (test-driven development)
    - Run the unit tests in watch mode
    - Write a unit test for the code block
    - Create a Python module and define a function. Move existing implementation from notebook into that function
    - Make the test pass
3. In the notebook, replace original code block with the newly defined function
4. Restart and run entire notebook (Unfortunately, until we have sufficient unit tests, we will still need manual “integration” tests for the time being.)
5. If possible Refactor function some more
6. Commit your changes
    - git add .
    - git commit -m "your commit message"
7. Rinse and repeat