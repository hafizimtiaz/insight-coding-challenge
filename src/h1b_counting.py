#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 14:25:52 2018

@author: hafizimtiaz
"""

import sys

# helper functions
def myIDs(lst):
    '''
    Function to find the indices of required parameters in the header of input
    Inputs:
        lst -           list version of the header text of the input file
                        contains the field names
    Outputs:
        status_id -     index of the visa status field
        visa_id -       index of the visa category field
        soc_id -        index of the SOC name field
        state_id -      index of the STATE name field
    '''
    status_id = [i for i, s in enumerate(lst) if 'STATUS' in s][0]
    visa_id = [i for i, s in enumerate(lst) if ('VISA' in s) and ('CLASS' in s)][0]
    soc_id = [i for i, s in enumerate(lst) if ('SOC' in s) and ('NAME' in s)][0]
    state_id = [i for i, s in enumerate(lst) if ('WORK' in s) and ('STATE' in s)][0]
    return status_id, visa_id, soc_id, state_id

def writeOutput(filename, res_lst, header_text, howMany = 10):
    '''
    Function to write the output files
    Inputs:
        filename -      filename to write the file, can get from sys.argv
        res_list -      the sorted list of results. contains tuples of 
                        (SOC/STATE, no. of certified applications, percentage)
        header_text -   header text to be written in the file
        howMany -       how many entries to be written in the file, 
                        default = 10
    
    Output:
        writes a text file with the results
    '''
    f = open(filename, "w") # open file to write the header
    f.write(header_text + "\n")
    f.close()

    f = open(filename, "a") # open file to append each line of results
    howMany = min((howMany, len(res_lst)))
    for pos in range(howMany):
        tmp = res_lst[pos]
        tmp_str = tmp[0] + ';' + str(tmp[1]) + ';' + ('%0.1f' % tmp[2]) + '%\n'
        f.write(tmp_str)
    f.close()
    return

def myParser(filename, SOC = {}, STATES = {}, totalCert = 0):
    '''
    Function to parse through the input csv file and accumulate certified applications
    Inputs:
        filename -  input filename
        SOC -       dictionary of SOC categories as keys. 
                    Each key is associated with a count of how many applications
                    have been certified in this category. Default = {}
        STATES -    dictionary of STATE names as keys. 
                    Each key is associated with a count of how many applications 
                    have been certified in this state. Default = {}
        totalCert - total number of certified applications. Default = 0
    
    Outputs:
        SOC -       dictionary of SOC categories as keys. Values are counts of 
                    how many applications have been certified in this category.
        STATES -    dictionary of STATE names as keys. Values are counts of 
                    how many applications have been certified in this state.
        totalCert - total number of certified applications across all states.
        
    '''
    f = open(filename) # open file for reading the input data
    D = f.readlines()
    f.close()
    L = len(D)
    visa_class = ['H1B', 'H-1B', 'H-1B1', 'E-3'] # these are the classes that we consider
    status_id, visa_id, soc_id, state_id = myIDs(D[0].split(';'))
    
    for line in range(1, L): # process each line separately
        tmp = D[line].split(';')
        status = tmp[status_id]
        visa = tmp[visa_id].split()[0]
        soc_code = tmp[soc_id]
        st_code = tmp[state_id]
        if (status == 'CERTIFIED') and (visa in visa_class) \
            and (len(soc_code) > 0) and (len(st_code) > 0):
            totalCert += 1
            
            # count soc codes
            
            if (len(soc_code) > 2) and (soc_code[0] == '"'): # remove the quotation marks
                soc_code = soc_code[1:-1]
                
            if soc_code in SOC:
                SOC[soc_code]['count'] += 1 # existing category -> increase count by 1
            else:
                SOC[soc_code] = {}
                SOC[soc_code]['count'] = 1  # new category
            
            # count states
            
            if st_code in STATES:
                STATES[st_code]['count'] += 1 # existing state -> increase count by 1
            else:
                STATES[st_code] = {}
                STATES[st_code]['count'] = 1 # new state        
    
    return SOC, STATES, totalCert

def myList(SOC, STATES, totalCert):
    '''
    Function for processing the dictionaries of SOC and STATES
    Inputs: 
        SOC -       dictionary of SOC categories as keys. 
                    Each key is associated with a count of how many applications
                    have been certified in this category. 
        STATES -    dictionary of STATE names as keys. 
                    Each key is associated with a count of how many applications 
                    have been certified in this state. 
        totalCert - total number of certified applications. 
        
    Outputs:
        lst_soc -       list of tuples. each tuple contains the soc name, 
                        certified application count and percentage
        lst_states -    list of tuples. each tuple contains the state name, 
                        certified application count and percentage
    '''
    lst_soc = []
    for key in SOC:
        SOC[key]['percent'] = SOC[key]['count'] / totalCert
        lst_soc.append((key, SOC[key]['count'], SOC[key]['percent']*100))
    
    lst_states = []
    for key in STATES:
        STATES[key]['percent'] = STATES[key]['count'] / totalCert    
        lst_states.append((key, STATES[key]['count'], STATES[key]['percent']*100))
        
    return lst_soc, lst_states
    
    
# input data filename
filename = sys.argv[1]

# process input file to get the dictionaries
SOC, STATES, totalCert = myParser(filename)

# make lists of combined result dictionaries
lst_soc, lst_states = myList(SOC, STATES, totalCert)

# sorting the lists for writing on the output files
res_soc = lst_soc.copy()
res_soc.sort(key = lambda x: x[0]) # for alphabetical
res_soc.sort(reverse = True, key = lambda x: x[1]) # for counts   

res_states = lst_states.copy()
res_states.sort(key = lambda x: x[0]) # for alphabetical
res_states.sort(reverse = True, key = lambda x: x[1]) # for counts   

# write output files
header_text = "TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"
writeOutput(sys.argv[2], res_soc, header_text)
    
header_text = 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
writeOutput(sys.argv[3], res_states, header_text)
    
    

