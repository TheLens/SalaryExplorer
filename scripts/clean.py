
'''docstring'''

import re


class Clean(object):

    '''docstring'''

    def __init__(self, value):
        self.cleaned_value = self.main(str(value))

    def main(self, value):
        '''docstring'''

        cleaned_value = self.descendents(value)
        cleaned_value = self.mc_names(cleaned_value)
        cleaned_value = self.middle_names(cleaned_value)

        return cleaned_value

    def descendents(self, value):
        '''docstring'''

        descendents = [
            ['Iii', 'III'],
            ['Ii', 'II'],
            ['Iv ', 'IV '],  # TODO: Add regex for end of line, or won't work
            ['Jr', 'Jr.'],
            ['Sr', 'Sr.']
        ]

        for descendent in descendents:
            if descendent[0] in value:
                output = re.sub(
                    descendent[0],
                    descendent[1],
                    value
                )
                return output

        return value

    def mc_names(self, value):
        '''docstring'''

        mc_names = [
            ['Mca', 'McA'],
            ['Mcb', 'McB'],
            ['Mcc', 'McC'],
            ['Mcd', 'McD'],
            ['Mce', 'McE'],
            ['Mcf', 'McF'],
            ['Mcg', 'McG'],
            ['Mch', 'McH'],
            ['Mci', 'McI'],
            ['Mcj', 'McJ'],
            ['Mck', 'McK'],
            ['Mcl', 'McL'],
            ['Mcm', 'McM'],
            ['Mcn', 'McN'],
            ['Mco', 'McO'],
            ['Mcp', 'McP'],
            ['Mcq', 'McQ'],
            ['Mcr', 'McR'],
            ['Mcs', 'McS'],
            ['Mct', 'McT'],
            ['Mcu', 'McU'],
            ['Mcv', 'McV'],
            ['Mcw', 'McW'],
            ['Mcx', 'McX'],
            ['Mcy', 'McY'],
            ['Mcz', 'McZ']
        ]

        for mc_name in mc_names:
            if mc_name[0] in value:
                output = re.sub(
                    mc_name[0],
                    mc_name[1],
                    value
                )

                return output

        return value

    def middle_names(self, value):
        '''docstring'''

        middle_initials = [
            [' A ', ' A. '],
            [' B ', ' B. '],
            [' C ', ' C. '],
            [' D ', ' D. '],
            [' E ', ' E. '],
            [' F ', ' F. '],
            [' G ', ' G. '],
            [' H ', ' H. '],
            [' I ', ' I. '],
            [' J ', ' J. '],
            [' K ', ' K. '],
            [' L ', ' L. '],
            [' M ', ' M. '],
            [' N ', ' N. '],
            [' O ', ' O. '],
            [' P ', ' P. '],
            [' Q ', ' Q. '],
            [' R ', ' R. '],
            [' S ', ' S. '],
            [' T ', ' T. '],
            [' U ', ' U. '],
            [' V ', ' V. '],
            [' W ', ' W. '],
            [' X ', ' X. '],
            [' Y ', ' Y. '],
            [' Z ', ' Z. ']
        ]

        for middle_initial in middle_initials:
            if middle_initial[0] in value:
                output = re.sub(
                    middle_initial[0],
                    middle_initial[1],
                    value
                )

                return output

        return value
