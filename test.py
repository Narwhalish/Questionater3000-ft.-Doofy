import os
print os.getcwd()

from TheGadflyProject.gadfly.gap_fill_generator import GapFillGenerator
g = GapFillGenerator("This is my input texts. \'It will probably be much longer than this, hopefully\' said Daniel.")
for q in g.questions: print(q)
