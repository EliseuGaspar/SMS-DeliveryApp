from datetime import datetime as dt

def calcular(date : str):
    if date != '0':
        data = date.replace(' ',',')
        data = data.replace(':',',')
        data = data.replace('-',',')
        data = data.replace('.',',')
        tempo = dt.now() - dt(
            int(data[:4]),int(data[5:7]),
            int(data[8:10]),int(data[11:13]),
            int(data[14:16]),int(data[17:19]),
            int(data[20:len(data)])
        )
        return int((tempo.total_seconds())/60)
    return 61