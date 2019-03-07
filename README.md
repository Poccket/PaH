# Python Against Humanity
**A Cards Against Humanity clone made in Python**

# Progress
file.py:
* readAsList(str fileName)
  * reads files into a list, breaking where there is a newline.
* readAsRaw(str fileName)
  * reads files into a string, includes newlines.


display.py:
* asBlock(str text, int width, int height, bool heavyBlock, bool doCompensate)
  * turns text into a block using unicode block characters
