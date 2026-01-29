## My Port of Lox using Python for Chapter 4
Will most likely never port the rest of the second half of the book - I'm most interested in redoing the lang in C but wanted to play around with the scanner

## To run prompt
```uv run src/lox.py ```

# to exit prompt
This is using the Python's built in input function so an empty string will end the eval loop.
keywords like `exit()` are not implemented
And therefore typing `ENTER` to the prompt will exit it as well even if it's not intended
