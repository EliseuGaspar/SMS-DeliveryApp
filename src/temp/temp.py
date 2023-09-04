from herojson import HeroJson

def limpar_temp():
    HeroJson('src/temp/confirmation_time.json').update('minutos','00')
    HeroJson('src/temp/confirmation_time.json').update('segundos','00')
    HeroJson('src/temp/dados_usuario.json').update('telefone','')
    HeroJson('src/temp/ids.json').update('id','')
    HeroJson('src/temp/mensagens.json').update('mensagens','')
    print('all temp clear')