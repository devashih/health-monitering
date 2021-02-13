# ----- import libraries and  modules ---
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkcalendar import Calendar, DateEntry
import datetime
import os
from .analysis.dataframes.dataframe import TrackerFrame

class EntryFrame(tk.Frame):
    def __init__(self, container, info_list:dict, tab_name, tracker, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # ----- Parameters -----
        self.info_list = info_list
        self.bulding_blocks = {}
        self.all_options = [[*option][0] for option in info_list]
        self.tracker = tracker
        self.current_date = datetime.datetime.now().date()
        if tab_name == "Longterm Changes":
            self.tab = "longterm"
        else:
            self.tab = tab_name.lower()
            
        # print('\ntabname: ', self.tab)
        # print('\tContainer children: ', container.winfo_children())
        # print('\tContainer children values: ',container.children.values())
        # print('\tContainer children class: ',container.winfo_class())
        # print('\tContainer parent: ',container.winfo_parent())
        # print('\t\tSiblings: ', container.master.winfo_children())
        # for child in container.master.winfo_children():
        #     print(f"Sibling: {child}")
        #     for childchild in child.winfo_children():
        #         print(f"\tSiblings child: {childchild}")
        #         print('\t\tClass:', childchild.winfo_class())
        #         if childchild.winfo_class() == 'Frame':
        #             for entryframe in childchild.winfo_children():
        #                 print(f"\t\t\tEntryframe: {entryframe}")
        #                 for widget in entryframe.winfo_children():
        #                     print(f"\t\t\t\tWidget: {widget}")
        #                     print('\t\t\t\t\tClass:', widget.winfo_class())
        #                 if not entryframe.winfo_children():
        #                     print('\t\t\t\t\tNo Children!')
        #                     print('\t\t\t\t\tName: ', entryframe.winfo_name())
        #                     # entryframe.config(state=tk.DISABLED)
        #                     if entryframe.winfo_name() == '!button3':
        #                         print('\t\t\t\t\tButton OF INTEREST!')
        #                         print('\t\t\t\t\t', entryframe['text'])
        # print("\n\n")


    # ----- Frames -----

        # create and place containing frame
        # self.entry_frame = tk.Frame(container)        
        # self.grid(row=1, column=0, sticky="NSEW", padx=10, pady=10)

        # ------ Health Data Entry ------
        # interate over options
        for option in self.info_list:

            # get option string
            option_name = [*option][0]

            # create building blocks (frame and stringvar - objects) for each option and save in dict - to access in commands on click
            self.bulding_blocks[option_name] = {}
            self.bulding_blocks[option_name]["frame"] = tk.Frame(self)
            self.bulding_blocks[option_name]["type"] = option[option_name]["type"]
            self.bulding_blocks[option_name]["selection"] = tk.StringVar(value=0)

            # create object based on the given type information
            if option[option_name]["type"] == "Checkbox":
                self.bulding_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.bulding_blocks[option_name]["frame"] ,text=option_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                ttk.Checkbutton(self.bulding_blocks[option_name]["frame"],
                                command=lambda option=option_name, topic=self.bulding_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                                variable=self.bulding_blocks[option_name]["selection"]).grid(row=0, column=1, sticky="W")

            elif option[option_name]["type"] == "MultipleChoice":
                # print("optionmenu", option_name) #uncomment for troubleshooting
                self.bulding_blocks[option_name]["selection"].set(option[option_name]["selection_menu"][0])
                self.bulding_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.bulding_blocks[option_name]["frame"] ,text=option_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                tk.OptionMenu(self.bulding_blocks[option_name]["frame"],
                                # command=lambda x=(option_name, self.bulding_blocks): self.check_options(*x), #lambda command refering to method in order to be able to pass current option name as variable
                                self.bulding_blocks[option_name]["selection"],
                                *option[option_name]["selection_menu"]).grid(row=0, column=1, sticky="W")

            elif option[option_name]["type"] == "Spinbox":
                self.bulding_blocks[option_name]["increment"] = option[option_name]["increment"]
                self.bulding_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.bulding_blocks[option_name]["frame"] ,text=option_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                self.bulding_blocks[option_name]["entry_object"] = tk.Spinbox(self.bulding_blocks[option_name]["frame"],
                                command=lambda option=option_name, topic=self.bulding_blocks: self.check_options(option, topic), #lambda command refering to method in order to be able to pass current option name as variable
                                textvariable=self.bulding_blocks[option_name]["selection"],
                                from_=option[option_name]["from"],
                                to=option[option_name]["to"],
                                increment=option[option_name]["increment"],
                                justify="center",
                                width=5)
                self.bulding_blocks[option_name]["entry_object"].grid(row=0, column=1, sticky="W")
                self.bulding_blocks[option_name]["entry_object"].bind("<FocusOut>", lambda event, option=option_name, topic=self.bulding_blocks: self.check_options(option, topic))

            elif option[option_name]["type"] == "Entryfield":  
                self.bulding_blocks[option_name]["selection"].set(f"Type info + ENTER")      
                self.bulding_blocks[option_name]["frame"].pack(anchor="w")
                ttk.Label(self.bulding_blocks[option_name]["frame"] ,text=option_name, width=17).grid(row=0, column=0, sticky="W", padx =(5,0)) #label created separately fron checkbutton (instead of using 'text'-parameter) in order to have label on the left-hand side
                self.bulding_blocks[option_name]["entry_object"] = tk.Entry(self.bulding_blocks[option_name]["frame"],
                                # command=lambda x=(option_name, self.bulding_blocks): self.check_options(*x), #lambda command refering to method in order to be able to pass current option name as variable
                                textvariable=self.bulding_blocks[option_name]["selection"],
                                )
                self.bulding_blocks[option_name]["entry_object"].grid(row=0, column=1, sticky="W")
                self.bulding_blocks[option_name]["entries"] = []
                self.bulding_blocks[option_name]["entry_object"].bind("<Return>", lambda event, x=(self.bulding_blocks, option_name): self.add_entry(*x))

            else:
                pass

        # #----- Date Picker Frame -----
        # self.date_frame = tk.Frame(
        #     container,
        #     bg='blue'
        # )
        # self.date_frame.grid()

                # insert elements by their 
                # index and names. 
                # for i in range(1,len(option[option_name]["selection_menu"])+1):
                #     print(i)
                # for selection_option, index in zip(option[option_name]["selection_menu"],range(1,len(option[option_name]["selection_menu"])+1)):
                #     listbox.insert(index, selection_option) 

        for key in self.bulding_blocks.keys():
            for child in self.bulding_blocks[key]["frame"].winfo_children():
                # print(child.winfo_class())
                if child.winfo_class() != 'TLabel':
                    try:
                        print(child.variable)
                    except:
                        print('No variable here!')
                else:
                    print('NOPE! Label!')
            # print(key,':', self.bulding_blocks[key]["frame"].winfo_children())
        # print(self.bulding_blocks.keys())

    # ----- Buttons -----
        test = ttk.Button(
                self,
                command=lambda x=(self.all_options, self.bulding_blocks): self.print_all_selected(*x),
                text="Print Selection"
                )
        test.pack(anchor="w", pady =15, padx = (5,5))

        test_plotly = ttk.Button(
                self,
                command=self.show_plotly,
                text="Open Plotly!"
                )
        test_plotly.pack(anchor="w", pady =15, padx = (5,5))    

        select_date = tk.Button( #use tk.Button instead of ttk in order to use 'borderwidth'
                self,
                command=self.update_selection,
                text="Update Selection of 'angry'",
                borderwidth=0,
                fg='darkslateblue'
                )
        select_date.pack(anchor="w", pady =15, padx = (5,5))  
        self.changeOnHover(select_date, 'blue', 'darkslateblue') #change button color on hover
        # print(self.winfo_children)

        # ----- Date Picker ------
        self.cal = DateEntry(self, width=12, background='darkblue',
                            foreground='white', borderwidth=2)
        


    # ----- method toggling date picker and printing selection ------
    def change_date(self):
        # function printing selected date from calendar
        def print_sel(e):
            old_date = self.current_date
            new_date = self.cal.get_date()
            self.current_date = new_date
            print(f"Date changed from {old_date} to {new_date}")
        self.cal.bind("<<DateEntrySelected>>", print_sel) 

        # toggle (=pack/unpack) calendar if it exists 
        # try:
        if self.cal.winfo_ismapped():
            self.cal.pack_forget()
        else:
            self.cal.pack(padx=5, pady=5)
        # # create and pack calendar if it does not yet exist and bind it to function
        # except AttributeError:
        #     # print(type(e).__name__)
        #     self.cal = DateEntry(self, width=12, background='darkblue',
        #                     foreground='white', borderwidth=2)
        #     self.cal.bind("<<DateEntrySelected>>", print_sel)    #run print_sel() on date entry selection
        #     self.cal.pack(padx=5, pady=5)     


    # ----- method printing current checkbutton state when clicked and passing them on to dataframe to be saved -----
    def check_options(self, option, topic=None, value=None):

        if value:
            value = value
            self.tracker.update_frame(self.tab, option, value, self.current_date)
            print(value)
        else:
            # print checkbutton variable value (=value of tk.Stringvar-object saved in topic-dict for current option)
            value = topic[option]["selection"].get()
            self.tracker.update_frame(self.tab, option, value, self.current_date)
            print(value)


    # ----- method printing all current checkbutton states -----
    def print_all_selected(self, options, topic):

        # iterate over info_dicts within list
        for option in self.info_list:

            # grab outer key for current dict --> each outer dict has only one outer key
            option_name = [*option][0]

            # check option entry type
            if option[option_name]["type"] == "Entryfield":
                print(option_name,": ", topic[option_name]["entries"]) #Entryfields take multiple entries saved in a list
            else:
                print(option_name,": ", topic[option_name]["selection"].get()) #any otherfields take one entry saved in a tk.StringVar-object


    # ----- method adding entries from tk.Entry()-fields -----
    def add_entry(self, entry_info_dict, option_name):

        print(option_name)
        # get information and objects from dict
        field_list = entry_info_dict[option_name]["entries"]
        entry = entry_info_dict[option_name]["selection"].get()
        container = entry_info_dict[option_name]["frame"]
        entry_field = entry_info_dict[option_name]["entry_object"]

        # append new entry to entry list
        field_list.append(entry)

        # print entries (including new entry) to screen (next to entry field)
        self.print_entries(field_list, container)

        # for troubleshooting
        print(field_list)

        # save changes to dataframe
        print(option_name)
        self.check_options(option=option_name, value=field_list)

        # clear text typed in entry-fieldc
        entry_info_dict[option_name]["entry_object"].delete(0, "end")


    # ----- method displaying tk.Entry()-field entries to new tk.Label()-field next to entry field -----
    def print_entries(self, entry_list, container):

        # convert list to string with list items separated by commas
        entry_string = ', '.join([str(i) for i in entry_list])

        # create a Label to display string
        tk.Label(container, text=entry_string).grid(row=0, column=2, sticky="W")

    def show_plotly(self):
        import plotly.express as px

        gapminder = px.data.gapminder()
        fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
                hover_name="country", log_x=True, size_max=60)
        fig.show()

    # ----- method changing button text/foreground color on hover
    def changeOnHover(self, button, colorOnHover, colorOnLeave): 
        # background on cursor entering widget 
        button.bind("<Enter>", 
                    func=lambda e: button.config(fg=colorOnHover) 
                    ) 
            
        # background color on cursor leaving widget 
        button.bind("<Leave>", 
                    func=lambda e: button.config(fg=colorOnLeave)
                    )  

    # ----- method updating displayed entries based on selected date -----
    def update_selection(self, date):

        # get todays data
        data = self.tracker.get_date(date)

        # get tab-relevant data for current EntryFrame()-object
        data = data[self.tab]

        # update fields
        for option in data.columns:
            try:
                try: 
                    value = data.loc[date, option] #get value for according field in df
                    # print(option,": ", value) #uncomment for troubleshooting

                    if (self.bulding_blocks[option]["type"] == "Checkbox") or (self.bulding_blocks[option]["type"] == "MultipleChoice"):
                        try:
                            if value in ['0','1','0.0','1.0']: #value will be a number within a string for Checkbox
                                self.bulding_blocks[option]["selection"].set(str(int(value))) #get int-version, as only 0 or 1 are accepted for Checkbox
                            else:
                                self.bulding_blocks[option]["selection"].set(str(value))
                        except:
                            print(f"Selection change not possible for: {option}")

                    elif self.bulding_blocks[option]["type"] == "Spinbox":
                        try:
                            if self.bulding_blocks[option]["increment"] < 1: #use float for increments <1
                                converted_value = str(value)
                                self.bulding_blocks[option]["selection"].set(converted_value)
                            else: #use integers for increments > 1 -> otherwise diplay will not update because decimal points cannot be displayed for increments larger than 1
                                converted_value = str(int(value)) 
                                self.bulding_blocks[option]["selection"].set(converted_value)
                        except:
                            print(f"Selection change not possible for: {option}")                                          
                    elif self.bulding_blocks[option]["type"] == "Entryfield":
                        try:
                            entry_string = value.strip("[]").replace("'","") # value is a list as a strin -> to get desired output strip square bracets and remove single quotes
                            if (value) and (entry_string != 'nan'):
                                ttk.Label(self.bulding_blocks[option]["frame"], name='former_entries',text=entry_string, foreground='grey', background='whitesmoke').grid(row=1, column=1, sticky="W") #add label displaying previosu entries under Entryfield
                            else:
                                for child in self.bulding_blocks[option]["frame"].winfo_children():
                                    if child.winfo_name() == 'former_entries':
                                        child.grid_remove()
                        except:
                            print(f"Selection change not possible for: {option}")          
                    else:
                        print(f'The {option}-field is of type {self.bulding_blocks[option]["type"]}.')
                except Exception as e:
                    print(f"Data for {date} not available. \n\t Error: {e}")  
            except KeyError as e: #KeyError will be thrown if no entryfield with the current options value exists
                print(f"There is no entry field with the value {option}. \n\t Error: {e}") 




        
