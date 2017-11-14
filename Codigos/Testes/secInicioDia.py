from datetime import datetime

agora = datetime.now()
print(agora)
inicioDia = datetime(agora.year, agora.month, agora.day)
print(inicioDia)
dif = agora-inicioDia
print(dif.total_seconds())
