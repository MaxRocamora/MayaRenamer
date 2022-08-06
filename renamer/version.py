# ----------------------------------------------------------------------------------------
'''
3dsmax style renamer
Max Rocamora / maxirocamora@gmail.com
1.0.0 Release 12/09/2015
1.1 - bug fix on groups names and clashing - 18/05/16
1.2 - bug on long names internal - 20/10/16
1.5 - using UUID for nested names bug - 22/08/17
2.0 - maya 2018
3.0 - reworked, added undo wrapper and replace string method
3.2 - integrated ui with arcane
3.3.0 : arcaneQt
3.3.1 - about window fix
3.5.0 - removed arcaneQt
3.6.0 - stand alone tool, moved to workflow repository
4.0.0 - 09/2021 - updated for maya 2022 and python 3, general refactor
4.1.0 - 08/2022 - moved to a single github repository
'''
# ----------------------------------------------------------------------------------------

VERSION_MAJOR = 4
VERSION_MINOR = 1
VERSION_PATCH = 0

version = f'{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}'

__app__ = 'Renamer ' + version
__qt__ = 'Arcane2:Qt_' + __app__ + '_ui'
