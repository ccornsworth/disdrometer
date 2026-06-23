def run():
    link = "http://18.222.146.48/RAMP/v1/raw/1047/data/"
    station = "1047"
    import wget
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import os.path
    from datetime import date, timedelta

    def parse_ramp_file(filepath):
        rows = []
        with open(filepath, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                row = {}
                for i in range(0, len(parts) - 1, 2):
                    row[parts[i]] = parts[i+1]
                rows.append(row)
        df = pd.DataFrame(rows)
        df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%y %H:%M:%S')
        for col in df.columns:
            if col != 'DATE':
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    pass
        return df

    today = date.today()
    print("Today is " + today.strftime("%Y-%m-%d") + ".")
    hist = today - timedelta(days=7)

    head = ["DATE", "CO", "NO", "NO2", "O3", "PM1.0", "PM2.5", "PM10"]
    units = ["ppb", "ppb", "ppb", "ppb", "ug/m3", "ug/m3", "ug/m3"]

    week_dat = pd.DataFrame()

    for i in range(8):
        try:
            url = link + hist.strftime("%Y-%m-%d") + "-" + station + ".txt"
            dir = os.path.expanduser("./data")
            dat = wget.download(url, out=dir)
            df = parse_ramp_file(dat)
            week_dat = pd.concat([week_dat, df], ignore_index=True)
            hist = hist + timedelta(days=1)
        except Exception as e:
            print("\nWarning: An error occurred for " + hist.strftime("%Y-%m-%d") + ": " + str(e))
            hist = hist + timedelta(days=1)

    week_dat.index = pd.DatetimeIndex(week_dat['DATE'])
    week_dat = week_dat.resample('5min').mean(numeric_only=True)

    for r in range(len(head) - 1):
        plt.figure(figsize=(15, 5))
        plt.scatter(week_dat.index, week_dat[head[r+1]], s=2)
        plt.title(head[r+1])
        plt.ylabel("Concentration (" + units[r] + ")")
        plt.xlabel("Date")
        plt.grid()
        plt.savefig(f"./data/{head[r+1]}.png")
        plt.show()