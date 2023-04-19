import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import calendar
import sys

# read files from parent directory.
sys.path.append('../../')
#from psql_manictime import ManictimeDBConnect
from psql_manictime import CalcActivity
from psql_manictime import Params_status
from psql_manictime import GetStatus


class GeneralPlotter:
    def __init__(self):
        '''
        Parameters
        ----------
        '''        
        self.fig, self.ax = plt.subplots()
        
    def plot_xy(self, data_x, data_y):
        self.ax.plot(data_x, data_y)
        self.fig.show()

    def plot_hist(self, data_x, ylog=False):
        self.ax.hist(data_x)
        if ylog:
            self.ax.set_yscale('log')
        self.fig.show()

    def plot_bar(self, data_x, data_y):
        self.ax.bar(data_x, data_y, width=0.3)
        self.fig.show()

    def plot_graph(self, data_x, data_y):
        self.ax.plot(data_x, data_y)
        self.fig.show()




class DataEditor:
    def __init__(self,data_files, data_editor, plotter =GeneralPlotter, params=Params_status):
        '''
        Parameters
        ----------
        '''
        # initial setting values
        IP_add = None
        ##Category = "YouTube"
        url = None
        data_trans_vol = 0
        Devicename = "MorinoMacBook-Air"

        # input data
        print(data_files)
        #self.df = pd.read_csv(data_files)
        self.df = data_files
        self._deditor = data_editor
        print(self.df)
        self._plotter = plotter
        self._params = params

    def continueous_watching_time_dist(self, duration=datetime.timedelta(days=10)):
        # ex1: plot continueous_watching_time_dist
        watching_time, watching_time_dist_each = self._deditor.watching_time_leg(duration=duration, time=time_now, contents=params._contents) #, use_time
        watching_time_dist_each = watching_time_dist_each.dt.total_seconds() # Series に対して
        self._plotter.plot_hist(watching_time_dist_each)

    def watching_time_per_date(self, duration = datetime.timedelta(weeks=4)):
        day_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day_watchtime_list = []
        day_usetime_list = []
        for day in day_list:
            date_watching_time, _ = self._deditor.watching_time_Day(day=day, time=time_now, duration = duration, contents=params._contents)
            #print(Sunday_watching_time)
            date_use_time, _ = self._deditor.watching_time_Day(day=day, time=time_now, duration = duration)

            day_watchtime_list.append(date_watching_time.total_seconds()/60/60/4)
            day_usetime_list.append(date_use_time.total_seconds()/60/60/4)
        print(day_watchtime_list)
        self._plotter.plot_bar(day_list, day_usetime_list)
        self._plotter.plot_bar(day_list, day_watchtime_list)

    def watching_time_per_timezone(self, duration = datetime.timedelta(weeks=4)):
        tz_watching_time_list =[]
        tz_use_time_list = []
        tz_list = []
        for i in range(24):
            tz_start= datetime.time(hour=i, minute=0, second=0)
            tz_end=datetime.time(hour=i, minute=59, second=59)
            tz_list.append(i)
            tz_watching_time, _ = self._deditor.watching_time_timezone(tz_start=tz_start, tz_end= tz_end, time=time_now, duration=duration, contents=params._contents)
            tz_use_time, _ = self._deditor.watching_time_timezone(tz_start=tz_start, tz_end= tz_end, time=time_now, duration = duration)

            tz_watching_time_list.append(tz_watching_time.total_seconds()/60/60/28)
            tz_use_time_list.append(tz_use_time.total_seconds()/60/60/28)
        # 1を超えるはずはないんだけどなあ？
        print(tz_watching_time_list)
        self._plotter.plot_bar(tz_list, tz_use_time_list)
        self._plotter.plot_bar(tz_list, tz_watching_time_list)


    def timeseries_per_day(self, duration=datetime.timedelta(days=70)):
        # reporting
        #start_mes_time = datetime.datetime(year=2022, month=10, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        start_mes_time = time_now - duration
        watching_time_list =[]
        watching_rate_list = []
        use_time_list = []
        switching_times_day_list = []
        contents_access_times_day_list = []
        contents_watiching_ave_day_list = []
        contents_secession_times_day_list = []
        for i in range(70):
            params = Params_status(time=start_mes_time + datetime.timedelta(days=i))
            #userstatus = Status(logDB=OperlogDB, params=params)

            duration = datetime.timedelta(days=1)
            #watching_time, use_time = userstatus.watching_time_leg(duration=duration)
            watching_time, _ = gp._deditor.watching_time_leg(duration=duration, contents=params._contents,time=params._time)
            use_time, _ = gp._deditor.watching_time_leg(duration=duration,time=params._time)
            contents_access_times_day = gp._deditor.access_times_leg(duration=duration, contents=params._contents,time=params._time)
            switching_times_day = gp._deditor.access_times_leg(duration=duration,time=params._time)
            #contents_secession_times = gp._deditor.switching_times_leg(duration=duration, contents=params._contents)

            watching_time_list.append(watching_time.total_seconds())
            use_time_list.append(use_time.total_seconds())
            switching_times_day_list.append(switching_times_day)
            contents_access_times_day_list.append(contents_access_times_day)
            #contents_secession_times_day_list.append(contents_secession_times)

            if use_time.total_seconds() == 0:
                watching_rate_list.append(-1)
            else:
                watching_rate_list.append(watching_time.total_seconds() / use_time.total_seconds())
            if contents_access_times_day == 0:
                contents_watiching_ave_day_list.append(0)
            else:
                contents_watiching_ave_day_list.append(watching_time.total_seconds()/contents_access_times_day)

        print(watching_time_list)
        print(watching_rate_list)
        print(use_time_list)
        print(switching_times_day_list)
        import statistics
        ave = statistics.mean(watching_time_list)
        std = statistics.stdev(watching_time_list)
        print("statistics watching time")
        print(ave, std)
        ave = statistics.mean(watching_rate_list)
        std = statistics.stdev(watching_rate_list)
        print("statistics watching time")
        print(ave, std)

        # visualizing
        ## report id の出力までOK
        self._plotter.plot_graph([i for i in range(70)],[x/ 60 for x in watching_time_list])
        self._plotter.plot_graph([i for i in range(70)],[x for x in watching_rate_list])
        self._plotter.plot_graph([i for i in range(70)],[x for x in switching_times_day_list])

        """
        fig, ax = plt.subplots() # （全コンテンツ）単位時間あたりの切り替え回数
        ax.plot([i for i in range(70)],[x/y for x,y in zip(switching_times_day_list, use_time_list)])
        plt.show()
        fig, ax = plt.subplots() 
        ax.plot([i for i in range(70)],[x/y for x,y in zip(use_time_list, switching_times_day_list)]) # 全コンテンツの平均滞在時間
        #ax.plot([i for i in range(70)],[if not y == 0: x/y for x,y in zip(watching_time_list, contents_access_time_day_list)]) # youtubeコンテンツの平均滞在時間
        ax.plot([i for i in range(70)],contents_watiching_ave_day_list)
        plt.show()
        fig, ax = plt.subplots()
        ax.plot([i for i in range(70)],[x for x in contents_secession_times_day_list])
        plt.show()
        """


class StatusEditor:
    def __init__(self,data_files, data_editor, plotter =GeneralPlotter, params=Params_status):
        '''
        Parameters
        ----------
        '''
        # initial setting values
        IP_add = None
        ##Category = "YouTube"
        url = None
        data_trans_vol = 0
        Devicename = "MorinoMacBook-Air"

        # input data
        print(data_files)
        #self.df = pd.read_csv(data_files)
        self.df = data_files
        self._deditor = data_editor
        print(self.df)
        self._plotter = plotter
        self._params = params
        self.df_trimmed, _  = self.trim_state()

    def trim_state(self, time_on_page_not_zero=True):
        # input data

        # initial setting values
        usr = "morisyou"   
        
        #df = pd.read_csv("state_{}.csv".format(usr))
        df = self.df
        print(df)
        if time_on_page_not_zero == True:
            #df = df[df['Time_on_page'] !=0]
            df = df[df['Time_on_page'] !=300]
            #df = df[df['Time_on_page'] >=15]
            #df = df[df['Time_on_page'] <=285]
            ### df = df[df['Time_on_page'] <=30]
            df = df[df['Time_on_page'] >=270]


        # data trimmed 1 : elimanate data not active
        df = df[df["Active_or_not"] != False].reset_index(drop=True)
        df["Aggregate_date"] = pd.to_datetime(df["Aggregate_time"]).dt.strftime('%Y/%m/%d')
        print(df["Aggregate_date"])

        # data trimmed 2 : eliminate data unrelative
        df = df.drop(['Unnamed: 0'], axis=1)
        df = df.drop(['Aggregate_time'], axis=1)
        df = df.drop(['User'], axis=1)
        df = df.drop(['IP_Address'], axis=1)
        df = df.drop(['Category'], axis=1)
        df = df.drop(['URL'], axis=1)
        df = df.drop(['Active_or_not'], axis=1)
        df = df.drop(['Devicename'], axis=1)

        # data trimmed 3: eliminate data not necessary
        df = df.drop(['Today_watching_time'], axis=1)
        df = df.drop(['action_num'], axis=1)

        print(df)
        print(df.columns)
        print(df.describe())
        # data edit: Watching True or False => 1 or 0
        df['Watching'] = df['Watching'].map({False: 0, True: 1})
        #df['Watching'] = df['Watching'] * 1
        """
        df['Time_on_page'] = df['Time_on_page'] / df['Time_on_page'].describe()["mean"]
        df['quarterh_leg'] = df['quarterh_leg'] / df['quarterh_leg'].describe()["mean"]
        df['oneh_leg'] = df['oneh_leg'] / df['oneh_leg'].describe()["mean"]
        df['fourh_leg'] = df['fourh_leg'] / df['fourh_leg'].describe()["mean"]
        df['oned_leg'] = df['oned_leg'] / df['oned_leg'].describe()["mean"]
        df['onew_leg'] = df['onew_leg'] / df['onew_leg'].describe()["mean"]
        df['Data_transfer_volume'] = df['Data_transfer_volume'] / df['Data_transfer_volume'].describe()["mean"]
        """
        """
        df['Time_on_page'] = df['Time_on_page'] / 300
        df['15min_leg'] = df['15min_leg'] / 900
        df['1h_leg'] = df['1h_leg'] / 3600
        df['3h_leg'] = df['3h_leg'] / 10800
        df['1d_leg'] = df['1d_leg'] / 86400
        df['1w_leg'] = df['1w_leg'] / 86400 / 7 
        """

        df_with_date = df.copy()
        df = df.drop(['Aggregate_date'], axis=1)

        print(df)
        print(df.columns)
        print(df.describe())
        #print(df.iloc[100])
        return df , df_with_date

    def statistic_data(self):
        print(self.df_trimmed)
        self._plotter.plot_hist(self.df_trimmed["Time_on_page"])
        self._plotter.plot_hist(self.df_trimmed["Data_transfer_volume"])
        self._plotter.plot_hist(self.df_trimmed["Continuous_watching"], ylog=False)

       

def __main__():

    usr = "morisyou"
    time_now = datetime.datetime(year=2022, month=12, day=20, hour=19, minute=15, second=0, microsecond=12, tzinfo=None)
    params = Params_status(time=time_now, real_time=False)



    # if you visualize from GetStatus
    ### filepath = "../state_{}.csv".format(params._username)
    filepath = "../state_{}_edit_cont_watch.csv".format(params._username)

    df = pd.read_csv(filepath)
    sgp = StatusEditor(data_files=df, data_editor= GetStatus(logDB=df, params=params))
    sgp.statistic_data()

    """
    # if you visualize frome CalcActivity
    filepath = "../{}_maniclogs.csv".format(usr)
    df = pd.read_csv(filepath)
    gp = DataEditor(data_files=df, data_editor= CalcActivity(activity_db=df, time = time_now, real_time=False), params=params)

    gp.continueous_watching_time_dist()
    gp.watching_time_per_date()
    gp.watching_time_per_timezone()
    gp.timeseries_per_day()
    """

