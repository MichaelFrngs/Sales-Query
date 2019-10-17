import datetime as dt
import time
import os
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta #Lets you use (years_ago = datetime.datetime.now() - relativedelta(years=5))

Code_Directory = "C:/Users/mfrangos/Desktop/Daily Sales Query Program"

class Calendar(object):
  def __init__(self):
    self.CurrentDate = dt.datetime.now()
    self.OffsetNumOfDays = -1 #Feel free to change the report date you need. Live data is usually -1
    self.CurrentDate = self.CurrentDate + dt.timedelta(days=self.OffsetNumOfDays)
  
    #Reformatting to use .loc on fiscal calendar file
    if self.CurrentDate.day < 10:
      self.CurrentDateReformat_day = "0" + str(self.CurrentDate.day)
    else: 
      self.CurrentDateReformat_day = str(self.CurrentDate.day)
    
    if self.CurrentDate.month < 10:
      self.CurrentDateReformat_month = "0" + str(self.CurrentDate.month)
    else: 
      self.CurrentDateReformat_month = str(self.CurrentDate.month)
      
    self.CurrentDateReformat = str(self.CurrentDate.year) + "-" + str(self.CurrentDateReformat_month) + "-" + str(self.CurrentDateReformat_day)

    
    self.ReportDate = self.CurrentDate + dt.timedelta(days=-self.CurrentDate.weekday()-1, weeks=-1) #Selects last sunday
    print("Report Date: ", self.ReportDate,self.ReportDate + dt.timedelta(days=6))
     
    self.ReportMonth = self.ReportDate.month 
    self.ReportDay = self.ReportDate.day 
    self.ReportYear = self.ReportDate.year
    
    self.ReportMonth2 = (self.ReportDate + dt.timedelta(days=6)).month 
    self.ReportDay2 = (self.ReportDate + dt.timedelta(days=6)).day 
    self.ReportYear2 = (self.ReportDate + dt.timedelta(days=6)).year

    
    self.CurrentMonth = self.CurrentDate.month 
    self.CurrentDay = self.CurrentDate.day 
    self.CurrentYear = self.CurrentDate.year
    
    if self.ReportMonth == 1 or self.ReportMonth == 2 or self.ReportMonth == 3:
      self.ReportQuarter = 1
    elif self.ReportMonth == 4 or self.ReportMonth == 5 or self.ReportMonth == 6:
      self.ReportQuarter = 2
    elif self.ReportMonth == 7 or self.ReportMonth == 8 or self.ReportMonth == 9:
      self.ReportQuarter = 3
    else:
      self.ReportQuarter = 4
    print("Current Quarter: ",self.ReportQuarter)
  
    self.Quarter_months_list = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]

    os.chdir("C:/Users/mfrangos/Desktop/Fiscal Calendars")
    
    self.FiscalCalendar = pd.read_excel("GeneralLedger Calendar.xlsx")
    
    self.CurrentFiscalDay = self.FiscalCalendar.loc[self.FiscalCalendar["Date"] == self.CurrentDateReformat]["GL DAY"].iloc[0]
    self.CurrentFiscalWeek = self.FiscalCalendar.loc[self.FiscalCalendar["Date"] == self.CurrentDateReformat]["GL WK"].iloc[0]
    self.CurrentFiscalYear = self.FiscalCalendar.loc[self.FiscalCalendar["Date"] == self.CurrentDateReformat]["GL YR"].iloc[0]
    self.CurrentFiscalPeriod = self.FiscalCalendar.loc[self.FiscalCalendar["Date"] == self.CurrentDateReformat]["GL PD"].iloc[0]
    self.CurrentFiscalDate = str(self.CurrentFiscalYear) + "-" + str(self.CurrentFiscalPeriod) + "-" + str(self.CurrentFiscalDay)
    
    self.Short_CurrentFiscalDay = self.FiscalCalendar.loc[self.FiscalCalendar["Date"] == self.CurrentDateReformat]["SHORT GL DAY"].iloc[0]
    self.Short_CurrentFiscalWeek = self.FiscalCalendar.loc[self.FiscalCalendar["Date"] == self.CurrentDateReformat]["SHORT GL WK"].iloc[0]
    
    print("Report Fiscal Date: ", self.CurrentFiscalDay, f" ||| Offset by {self.OffsetNumOfDays} days from current fiscal day of {self.CurrentFiscalDay - self.OffsetNumOfDays}")
    
  #Calendar Dates
  def Calendar_Date_to_Calendar_words(self,day,month,year):
    output = date(day=day, month=month, year=year).strftime('%A %d %B %Y')
    return output
  def Calendar_Date_to_Calendar_month(self,day,month,year):
    output = date(day=day, month=month, year=year).strftime('%B')
    return output
  def Calendar_Date_to_Calendar_day(self,day,month,year):
    output = date(day=day, month=month, year=year).strftime('%d')
    return output
  def Calendar_Date_to_WeekDay(self,day,month,year):
    output = date(day=day, month=month, year=year).strftime('%A')
    return output
  def Calendar_Date_to_Calendar_year(self,day,month,year):
    output = date(day=day, month=month, year=year).strftime('%Y')
    return output
    
    
    
  def WK_Format(self,date):
    if date < 10:
      output = str("WK0") + str(date)
    else:
      output = str(date)
    return output

###For extracting datetime from Tableau business date
#TY_date_time_list = []
#from time import strptime
#i=0
#for year in TY_Daily_Margins.iloc[:, 5]:
#  month = TY_Daily_Margins.iloc[i, 6]
#  day = TY_Daily_Margins.iloc[i, 7]
#  #print(month[:3])
#  TY_date_time_list.append(date(day=day, year=year, month=strptime(f'{month[:3]}','%b').tm_mon))
#  i=i+1
  

  #
  def Calendar_Date_to_FiscalDate(self,Calendar_Date):
    #DT_Fiscaldate = Fiscal_Date
    #assuming we're passing date_times
    #print(FiscalCalendar.loc[(FiscalCalendar["GL DAY"] == Calendar_Date.day)].head())
    #print(FiscalCalendar.loc[(FiscalCalendar["GL PD"] == Calendar_Date.month)].head())
    #print(FiscalCalendar.loc[(FiscalCalendar["GL YR"] == Calendar_Date.year)].head())
    
    self.Fiscal_Date = self.FiscalCalendar.loc[((self.FiscalCalendar["calendar day"] == self.Calendar_Date.day) & 
                                     (self.FiscalCalendar["calendar month"] == self.Calendar_Date.month) &
                                     (self.FiscalCalendar["calendar year"] == self.Calendar_Date.year))]
    
    return [self.Fiscal_Date["GL DAY"], self.Fiscal_Date["GL WK"], self.Fiscal_Date["GL PD"], self.Fiscal_Date["GL YR"]]
      
#test = dt.date(year = 2018, month = 7, day = 12)
#Output = Calendar_Date_to_FiscalDate(test)
  
  def date_time_to_fiscal_week(self,datetime_stamp,FiscalCalendar):
    self.fiscal_week = (self.FiscalCalendar.loc[self.FiscalCalendar["Date"] == datetime_stamp])["GL WK"]
    return self.fiscal_week

#Create Calendar Object
Current_Calendar = Calendar()
#############################################################################################################

#Example
Current_Calendar.CurrentDate

print("Loading Data, please wait . . .")
data = pd.read_excel("Y:/Revenue Reports and Analysis/Sales Report Data 2017-2019.xlsx", "DATA")

class create_store(object):
  def __init__(self,store_num, Data_source):
    self.store_num = store_num
    self.All_Data = Data_source.loc[Data_source["STORE"] == store_num]
    self.TY_data = Data_source.loc[(Data_source["STORE"] == store_num) & (Data_source["GL YR"] == Current_Calendar.ReportYear    )]
    self.LY_data = Data_source.loc[(Data_source["STORE"] == store_num) & (Data_source["GL YR"] == Current_Calendar.ReportYear - 1)] 

  def TY_YTD_Data(self):
    output = self.self.TY_data.loc[self.self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay]
    return output.loc[output["STORE"] == self.store_num]
  def TY_QTD_Data(self):
    output = self.TY_data.loc[((self.TY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][0]) | (self.TY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][1]) | (self.TY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][2])) & (self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.loc[output["STORE"] == self.store_num]
  def TY_WTD_Data(self):
    output =  self.TY_data.loc[(self.TY_data["GL WK"] == (Current_Calendar.WK_Format(Current_Calendar.CurrentFiscalWeek))) & (self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.loc[output["STORE"] == self.store_num]
  def TY_MTD_Data(self):
    output =  self.TY_data.loc[(self.TY_data["GL PD"] == Current_Calendar.CurrentFiscalPeriod) & (self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.loc[output["STORE"] == self.store_num]
  
  def LY_YTD_Data(self):
    output = self.LY_data.loc[self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay]
    return output.loc[output["STORE"] == self.store_num]
  def LY_QTD_Data(self):  
    output =  self.LY_data.loc[((self.LY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][0]) | (self.LY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][1]) | (self.LY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][2])) & (self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.loc[output["STORE"] == self.store_num]
  def LY_WTD_Data(self):
    output = self.LY_data.loc[(self.LY_data["GL WK"] == (Current_Calendar.WK_Format(Current_Calendar.CurrentFiscalWeek))) & (self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.loc[output["STORE"] == self.store_num]
  def LY_MTD_Data(self):
    output = self.LY_data.loc[(self.LY_data["GL PD"] == Current_Calendar.CurrentFiscalPeriod) & (self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.loc[output["STORE"] == self.store_num]
  
def rbind_store_data(temp_store_list,date_func):
  accumulation = pd.DataFrame()
  for store in temp_store_list:
    if store is str:
      store = eval(store)
      print(type(store))
    if date_func == "NONE":
      print(store)
      accumulation = accumulation.append(pd.DataFrame(data = eval(f'store.All_Data')), ignore_index=True)
    else:
      accumulation = accumulation.append(pd.DataFrame(data = eval(f'store.{date_func}()')), ignore_index=True)
  return accumulation


class store_list_object(object):
  def __init__(self,list_of_stores):
    self.list_of_stores = list_of_stores
    self.data = rbind_store_data([store for store in list_of_stores],"NONE")
    self.TY_data = data.loc[data["GL YR"] == Current_Calendar.ReportYear]
    self.LY_data = data.loc[data["GL YR"] == Current_Calendar.ReportYear - 1]

  def TY_YTD_by_(self,by,metric):
    output = self.TY_data.loc[self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay]
    return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
  def TY_QTD_by_(self,by,metric):
    output = self.TY_data.loc[((self.TY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][0]) | (self.TY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][1]) | (self.TY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][2])) & (self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
  def TY_WTD_by_(self,by,metric):
    output =  self.TY_data.loc[(self.TY_data["GL WK"] == (Current_Calendar.WK_Format(Current_Calendar.CurrentFiscalWeek))) & (self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
  def TY_MTD_by_(self,by,metric):
    output =  self.TY_data.loc[(self.TY_data["GL PD"] == Current_Calendar.CurrentFiscalPeriod) & (self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
  
  def LY_YTD_by_(self,by,metric):
    output = self.LY_data.loc[self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay]
    return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
  def LY_QTD_by_(self,by,metric):
    output =  self.LY_data.loc[((self.LY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][0]) | (self.LY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][1]) | (self.LY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][2])) & (self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
  def LY_WTD_by_(self,by,metric):
    output = self.LY_data.loc[(self.LY_data["GL WK"] == (Current_Calendar.WK_Format(Current_Calendar.CurrentFiscalWeek))) & (self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
  def LY_MTD_by_(self,by,metric):
    output = self.LY_data.loc[(self.LY_data["GL PD"] == Current_Calendar.CurrentFiscalPeriod) & (self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
  
  def YoY_YTD_by_(self,by,metric, return_percent):
    output = self.TY_data.loc[self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay]
    LY_output = self.LY_data.loc[self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay]
    if return_percent == True:
      return (output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum').subtract(LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')))/LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
    elif return_percent == False:
      return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum').subtract(LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum'))
  def YoY_QTD_by_(self,by,metric, return_percent):
    output = self.TY_data.loc[((self.TY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][0]) | (self.TY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][1]) | (self.TY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][2])) & (self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    LY_output = self.LY_data.loc[((self.LY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][0]) | (self.LY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][1]) | (self.LY_data["GL PD"] == Current_Calendar.Quarter_months_list[Current_Calendar.ReportQuarter-1][2])) & (self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    if return_percent == True:
      return (output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum').subtract(LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')))/LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
    elif return_percent == False:
      return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum').subtract(LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum'))
  def YoY_WTD_by_(self,by,metric, return_percent):
    output =  self.TY_data.loc[(self.TY_data["GL WK"] == (Current_Calendar.WK_Format(Current_Calendar.CurrentFiscalWeek))) & (self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    LY_output = self.LY_data.loc[(self.LY_data["GL WK"] == (Current_Calendar.WK_Format(Current_Calendar.CurrentFiscalWeek))) & (self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    if return_percent == True:
      return (output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum').subtract(LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')))/LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
    elif return_percent == False:
      return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum').subtract(LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum'))
  def YoY_MTD_by_(self,by,metric, return_percent):
    output = self.TY_data.loc[(self.TY_data["GL PD"] == Current_Calendar.CurrentFiscalPeriod) & (self.TY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    LY_output = self.LY_data.loc[(self.LY_data["GL PD"] == Current_Calendar.CurrentFiscalPeriod) & (self.LY_data["GL DAY"] <= Current_Calendar.CurrentFiscalDay)]
    if return_percent == True:
      return (output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum').subtract(LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')))/LY_output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum')
    elif return_percent == False:
      return output.pivot_table(index = [f"{by}"],   values =f"{metric}", aggfunc='sum').subtract(LY_output.pivot_table(index = ["DISTRICT"],   values =f"{metric}", aggfunc='sum'))
  



  
#Create store list
store_list = []
for store in data["STORE"]:
  store_list.append(store)
store_list = list(set(store_list))

#Create Store objects
All_stores_object_list = []
for store in store_list:
  exec(f"S{store} = create_store(store,data)")
  All_stores_object_list.append(f"S{store}")

##For every store, print the adjusted sales
#for store_obj in All_stores_object_list:
#  print(exec(f"print({store_obj}.TY_YTD()['ADJ SALES'])"))


#Allows you to compile selected stores data
def compile_multi_store_data(All_stores_object_list, time_function):
  if store is str:
    output = rbind_store_data([eval(Store) for Store in All_stores_object_list], time_function) #Dataset for all stores. Can be used with a smaller list.
  else:
    output = rbind_store_data([Store for Store in All_stores_object_list], time_function) #Dataset for all stores. Can be used with a smaller list.
  return output


#Example of merging multiple store data
#rbind_store_data(Short_stores_object_list,"TY_YTD")
#rbind_store_data(Short_stores_object_list,"LY_YTD")

Closed_Stores = data.loc[(data["Status"] == "Closed") & (data["STORE"] != 100)]

def take_input_store_selection(List_of_All_Stores):
  print("\n")
  print("Query all stores? Or would you like to select the stores?")
  print("NOTE: Input is case sensitive")
  options = ["all", "select"]
  print(f"Options: {options}")
  valid_entry = False

  while valid_entry == False:
    input1 = input()
    if input1 in options:
      if input1 == "all":
        return List_of_All_Stores
      elif input1 == "select":
        print("Options: ", List_of_All_Stores)
        print("Type & separate each store with a comma:")
        #Take input from user
        Selected_Stores = input().replace(" ","").split(",")

        
        Select_stores_object_list = []
        for store in Selected_Stores:
          exec(f"S{store} = create_store(store,data)")
          Select_stores_object_list.append(f"{store}")        
        
        return Select_stores_object_list
      valid_entry = True
    elif input1 == "EXIT":
      print("Now exiting")
      break      
    else:
      print("Invalid Entry. Please retype or type EXIT")
      #print("\n")
      pass
  
#Turn a list of strings into a list of objects
def eval_list(list_of_stuff):
  object_output_list = []
  for item in list_of_stuff:
    object_output_list.append(eval(item))
  
  return object_output_list




######EXAMPLES TO TEST################
#Create a list of stores
#Short_stores_object_list = [S101,S102,S103] #Pick the stores you want to work with.

#accumulation = pd.DataFrame()
#for store in Short_stores_object_list: 
#    print(store)
#    accumulation = accumulation.append(pd.DataFrame(data = eval(f'store.All_Data')), ignore_index=True)
#    #accumulation = accumulation.append(pd.DataFrame(data = eval(f'store.TY_YTD_Data()')), ignore_index=True)

#########################EXAMPLES
##Query the group of stores
#Group_of_stores_object.TY_QTD_by_(by="STORE", metric = "ADJ SALES")
#Group_of_stores_object.LY_MTD_by_(by="DISTRICT", metric = "TRANS")
#
##Can be used to iterate through all possibilities
##### POSSIBLE PARAMETERS FOR METRICS: 'TRANS', 'NET SALES', 'UNITS', 'VIP', 'DIV9', 'ADJ SALES'
##### POSSIBLE PARAMETERS FOR 'by': 'TRANS', 'NET SALES', 'UNITS', 'VIP', 'DIV9', 'ADJ SALES'
#by_params = ['STORE','DATE','STATE','COMP STATUS','GL DAY','GL WK', 'GL PD','REGION','DISTRICT','SS DATE','AGE OF STORE', "Status"]
#metric_params = ['TRANS', 'NET SALES', 'UNITS', 'VIP', 'DIV9', 'ADJ SALES']
#
##Examples
#Group_of_stores_object.TY_MTD_by_(by='AGE OF STORE',metric = "ADJ SALES")
#Group_of_stores_object.LY_MTD_by_(by='Status',metric = "ADJ SALES")
#Group_of_stores_object.LY_MTD_by_(by='DATE',metric = "ADJ SALES")
#Group_of_stores_object.LY_YTD_by_(by='GL PD',metric = "ADJ SALES")
#Group_of_stores_object.YoY_MTD_by_(by="STORE",metric = "ADJ SALES", return_percent = True)
#Group_of_stores_object.YoY_MTD_by_(by="STORE",metric = "ADJ SALES", return_percent = False)
#Group_of_stores_object.YoY_YTD_by_(by="STORE",metric = "TRANS")
#Group_of_stores_object.YoY_YTD_by_(by="STORE",metric = "UNITS",return_percent = False)
#Group_of_stores_object.YoY_YTD_by_(by="STORE",metric = "VIP",  return_percent = False)
##Example of compiling multiple store data
#Select_store_Data = compile_multi_store_data(Short_stores_object_list,"TY_YTD_Data")
#Select_store_Data2 = compile_multi_store_data(Short_stores_object_list,"NONE") #Compiles all data without a time filter.
##Example of single store data query
#S101.TY_QTD_Data()


def take_input1():
  print("\n")
  print("What kind of Data would you like?")
  print("NOTE: Input is case sensitive")
  print("Options: TY, LY, YoY")
  valid_entry = False

  while valid_entry == False:
    input1 = input()
    if input1 == "TY":
      return "TY_"
      valid_entry = True
    elif input1 == "LY":
      return "LY_"
      valid_entry = True
    elif input1 == "YoY":
      return "YoY_"
      valid_entry = True
    elif input1 == "EXIT":
      print("Now exiting")
      exit()
      break      
    else:
      print("Invalid Entry. Please retype or type EXIT")
      #print("\n")
      pass
  return input1

def take_input2():
  print("\n")
  print("What period of time would you like?")
  print("NOTE: Input is case sensitive")
  print("Options: | WTD | MTD | QTD | YTD |")
  print("\n")
  valid_entry = False

  while valid_entry == False:
    input1 = input()
    if input1 == "WTD":
      return "WTD"
      valid_entry = True
    elif input1 == "MTD":
      return "MTD"
      valid_entry = True
    elif input1 == "QTD":
      return "QTD"
      valid_entry = True
    elif input1 == "YTD":
      return "YTD"      
    elif input1 == "EXIT":
      print("Now exiting")
      exit()
      break      
    else:
      print("Invalid Entry. Please retype or type EXIT")
      #print("\n")
      pass
  return input1

def take_input3():
  print("\n")
  print("What period of time would you like?")
  print("NOTE: Input is case sensitive")
  metric_params = ['TRANS', 'NET SALES', 'UNITS', 'VIP', 'DIV9', 'ADJ SALES']
  print(f"Options: {metric_params}")
  valid_entry = False

  while valid_entry == False:
    input1 = input()
    if input1 in metric_params:
      return input1
      valid_entry = True
    elif input1 == "EXIT":
      print("Now exiting")
      exit()
      break      
    else:
      print("Invalid Entry. Please retype or type EXIT")
      #print("\n")
      pass
  return input1

def take_input4():
  print("\n")
  print("Display results by what category?")
  print("NOTE: Input is case sensitive")
  by_params = ['STORE','DATE','STATE','COMP STATUS','GL DAY','GL WK', 'GL PD','REGION','DISTRICT','SS DATE','AGE OF STORE', "Status"]
  print(f"Options: Categorize by... {by_params}")
  valid_entry = False

  while valid_entry == False:
    input1 = input()
    if input1 in by_params:
      return input1
      valid_entry = True
    elif input1 == "EXIT":
      print("Now exiting")
      exit()
      break      
    else:
      print("Invalid Entry. Please retype or type EXIT")
      #print("\n")
      pass
  return input1

def take_input5():
  print("\n")
  print("Would you like the numbers changes in percentage?")
  print("NOTE: Input is case sensitive")
  by_params = ["TRUE","FALSE"]
  print(f"Options: {by_params}")
  valid_entry = False

  while valid_entry == False:
    input1 = input()
    if input1 in by_params:
      return input1
      valid_entry = True
    elif input1 == "EXIT":
      print("Now exiting")
      break      
    else:
      print("Invalid Entry. Please retype or type EXIT")
      #print("\n")
      pass
  return input1

#Query for user whether he wants to export or not
def Export_Input():
  print("\n")
  print("Would you like to export?")
  print("NOTE: Input is case sensitive")
  by_params = ["yes","no"]
  print(f"Options: {by_params}")
  valid_entry = False

  while valid_entry == False:
    input1 = input()
    if input1 in by_params:
      return input1
      valid_entry = True
    elif input1 == "EXIT":
      print("Now exiting")
      break      
    else:
      print("Invalid Entry. Please retype or type EXIT")
      #print("\n")
      pass
  return input1


def Continue_Query_Input():
  print("\n")
  print("Continue querying?")
  print("NOTE: Input is case sensitive")
  by_params = ["yes","no"]
  print(f"Options: {by_params}")
  valid_entry = False

  while valid_entry == False:
    input1 = input()
    if input1 in by_params:
      return input1
      valid_entry = True
    elif input1 == "EXIT":
      print("Now exiting")
      break      
    else:
      print("Invalid Entry. Please retype or type EXIT")
      #print("\n")
      pass
  return input1


Continue_Querying = True

while Continue_Querying == True:
  
  #Create a list of stores
  Store_Selection = take_input_store_selection(All_stores_object_list)
  Short_stores_object_list = Store_Selection
  Group_of_stores_object = store_list_object(eval_list(Short_stores_object_list)) #Group the list of stores into an object
  #Ask the user what decisions he/she would like to make
  DataChoice = take_input1()
  TimeChoice = take_input2()
  MetricChoice = take_input3()
  CategoryChoice = take_input4()
  
  #If YoY is picked, we have to handle for some branching
  if DataChoice == "YoY_":
    YoY_PCT_Decision = take_input5()
    All_Choices = DataChoice + TimeChoice + f"_by_(by='{CategoryChoice}', metric = '{MetricChoice}',return_percent = {YoY_PCT_Decision})" 
  else:
    All_Choices = DataChoice + TimeChoice + f"_by_(by='{CategoryChoice}', metric = '{MetricChoice}')"  #What to do about ,  return_percent = False)??
  
  #Evaluate the desired data
  Queried_Data = eval(f"Group_of_stores_object.{All_Choices}")
  

  #Ask for input from the user
  Export_Input_Answer = Export_Input()
  #Logic to export or not
  if Export_Input_Answer == "yes":
    Queried_Data.to_excel(f"{Code_Directory}/{All_Choices}.xlsx")
  else:
    pass
  
  #Display the queried data
  print(Queried_Data)
  
  #Ask user if he/she wants to continue
  Continue_Querying_Decision = Continue_Query_Input()
  if Continue_Querying_Decision == "yes":
    pass
  else:
    exit()
    
#Only exits the program if user selects no

  


