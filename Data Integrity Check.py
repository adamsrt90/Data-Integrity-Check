#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools, string, os, uuid
import pandas as pd
from dataclasses import dataclass
from difflib import SequenceMatcher
from multiprocessing import Process


# In[2]:


@dataclass
class DataIntegrity:
    '''
    Provides Tools to test for data integrity and duplication
    '''
    file_path: str = None
    cleaned: bool = False
    data_frame: object = None
    honorifics = ["Master", "Mr.", "Miss",
                  "Mrs.", "Ms.", "Mx.", "Sir", "Dr."]
    upper_letters = string.ascii_uppercase
    __finished_dict = {}
    potential_similar = []
    __data_loaded: bool = False
        
    def load_data(self, file_name, file_path = None):
        '''
        loads data into pandas dataframe
        '''
        if self.file_path == None:
            self.data_frame = pd.read_excel(file_name)
            self.__data_loaded = True
        else:
            os.chdir(file_path)
            self.data_frame = pd.read_excel(file_name)
            self.__data_loaded = True
            
    def show_frame(self):
        return self.data_frame
    
    def clean_data(self, column, check_honorifics = False, remove_NaN = False):
        '''
        Will drop duplicate rows.
        Specific_column default is False. Will ask for columns if True
        Honorifics default is False. Will remove common honorifics from beginning or name if True.
        Remove rows that have no number or NaN default is False. Will do if True
        Process not required if user wants to compare data raw.
        '''
        try:
            if self.data_frame is None:
                return "Please load a dataframe"
    
            else:
                pass
        except Exception as e:
            return f'Error Loading Frame: {e}'
            
        if check_honorifics == True and remove_NaN == True:
            try:
                self.data_frame.dropna(inplace = True)
                self.__honorific_cleaning(column)
            except Exception as e:
                return f'Error Checking Honorifics and Removing NaN: {e}'
        elif remove_NaN == True:
            try:
                self.data_frame.dropna(inplace = True)
            except Exception as e:
                return f'Error Removing NaN: {e}'
        elif check_honorifics == True:
            try:
                self.__honorific_cleaning(column)
            except Exception as e:
                return f'Error Checking Honorifics: {e}'
        
    def __honorific_cleaning(self, column):
        for h in self.honorifics:
            print(f'Checking {column} for {h}')
            try:
                self.data_frame[column] = self.data_frame[column].str.replace(h, '', regex = False)
            except Exception as e:
                return f'Error in handling honorifics: {e}'
       
    def __order_list_dict(self, column):
        '''
        Creates a custom dictionary.
        Keys are first letter of its values.

        "A":["Abraham", "Ayden", "Albert"], "B": ["Brian", "Brock"]
        '''
        workingList = list(self.data_frame[column])
        
        while True:
            try:
                if type(workingList) is list: #checks if user input is list
                    workingList.sort() #sort the list in alphabetical order
                    for letter in self.upper_letters:
                        blank_list = [] #create blank list after each letter is checked against working list
                        for value, item in enumerate(workingList):
                            if letter == item[0].upper():#compares the uppdercase first letter to the letter from letters
                                blank_list.append(workingList.pop(value))
                            else:
                                self.__finished_dict[letter] = blank_list
                else:
                    return "The item must be a list."
                return self.__finished_dict
            except Exception as e:
                return f'{e}: Please check the list information!'

        
    def comparison(self, strRange, percentage, column):
        '''
        takes in strRange as integer
        takes in percentage as float
        
        string range will ignore comparing two strings that are not within range set by user
        percentage is how close the user wants to match strings. 
        '''
        self.potential_similar = []
        
        if self.__data_loaded != True:
            return "There is no data loaded."
        

        try:
            comparison_dictionary = self.__order_list_dict(column)
        except Exception as e:
            print(f'{e} Please check the spelling of the column you want to check.')


            if srtRange != int or percentage != float:
                return "strRange must be an integer and percentage must be a float"
        except Exception as e:
            return e
        
        try:
            for key in comparison_dictionary:
                for a,b in itertools.combinations(comparison_dictionary[key], 2):
                    if abs(len(a) - len(b)) in range(strRange):
                        s = SequenceMatcher(None, a.upper(), b.upper())
                        if s.ratio() >= percentage:
                            print(f'{a} compared to {b} is {s.ratio()}')
                            self.potential_similar.append((a,b, s.ratio))
                    else:
                        pass
        except Exception as e:
            return e
    
    def save_comparison(self):
        tf = str(uuid.uuid4().hex)
        tdf = pd.DataFrame(self.potential_similar)
        tdf.to_excel(f'{tf}.xlsx', index = False)
        print(f'Your file is saved as {tf}.xlsx')


# In[3]:


if __name__ == "__main__":
    a = DataIntegrity()
    a.load_data('Doctors_Clean.xlsx')
    a.clean_data("Full Name", check_honorifics = True)
    a.comparison(5, .9, "Full Name")
    a.save_comparison()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




