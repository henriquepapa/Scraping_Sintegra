from selenium import webdriver
from datetime import datetime

#FUNÇÃO PARA OBTER DADOS DE RELATORIO
def get_dados(driver):
    dicionario_aux = {
    'inscricao_estadual':'',
    'nome':'',
    'nome_fantasia':'',
    'endereco': {
    'logradouro':'',
    'numero':'',
    'complemento':'',
    'bairro':'',
    'municipio':'',
    'uf':'',
    'cep':''
    },
    'atividade_principal':'',
    'atividades_secundarias':'',
    'situacao':'',
    'data_situacao':'',
    'data_cadastro':'',
    'data_consulta':'',
    }
    try:
        dicionario_aux['inscricao_estadual'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[2]/center/table/tbody/tr[4]/td[2]/span[2]").text
        dicionario_aux['nome'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[2]/center/table/tbody/tr[9]/td/span").text
        dicionario_aux['nome_fantasia'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[2]/center/table/tbody/tr[19]/td/span").text
        dicionario_aux['endereco']['logradouro'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[3]/center/table/tbody/tr[4]/td/span[2]").text
        dicionario_aux['endereco']['numero'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[3]/center/table/tbody/tr[6]/td/table/tbody/tr/td[1]/span[2]").text
        dicionario_aux['endereco']['complemento'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[3]/center/table/tbody/tr[6]/td/table/tbody/tr/td[4]/span[2]").text
        dicionario_aux['endereco']['bairro'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[3]/center/table/tbody/tr[8]/td/span[2]").text
        dicionario_aux['endereco']['municipio'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[4]/center/table/tbody/tr[2]/td[1]/span[2]").text
        dicionario_aux['endereco']['uf'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[4]/center/table/tbody/tr[2]/td[2]/span[2]").text
        dicionario_aux['endereco']['cep'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[4]/center/table/tbody/tr[4]/td[1]/span[2]").text
        dicionario_aux['atividade_principal'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[5]/center/table/tbody/tr[4]/td/span[3]").text
        dicionario_aux['atividades_secundarias'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[5]/center/table/tbody/tr[7]/td").text
        dicionario_aux['situacao'] = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[5]/center/table/tbody/tr[19]/td/span[2]").text
        data_situacao = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[5]/center/table/tbody/tr[21]/td/table/tbody/tr[1]/td[1]/span[2]").text
        dicionario_aux['data_situacao'] = datetime.strptime(data_situacao, '%d/%m/%Y').isoformat()
        data_cadastro = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[5]/center/table/tbody/tr[21]/td/table/tbody/tr[1]/td[2]/span[2]").text
        dicionario_aux['data_cadastro'] = datetime.strptime(data_cadastro, '%d/%m/%Y').isoformat()
        data_consulta = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[2]/td/div[6]/center/table/tbody/tr[5]/td/span[2]").text
        dicionario_aux['data_consulta'] = datetime.strptime(data_consulta, '%d/%m/%Y %H:%M:%S').isoformat()
    except:
        return {'inscricao_estadual':'Erro'}
    return dicionario_aux

#FUNÇÃO DE RASPAGEM
def Scrapy(Cpf):
    #driver necessário para execução
    driver = webdriver.Chrome("chromedriver.exe")

    driver.get("http://appasp.sefaz.go.gov.br/Sintegra/Consulta/default.asp")

    # click no cpf
    radio = driver.find_element_by_xpath("//*[@id='rTipoDocCPF']")
    radio.click()

    # preenchendo CPF
    cpf = driver.find_element_by_xpath('//*[@id="tCPF"]')
    cpf.send_keys(Cpf)

    # Consulta
    try:
        consulta = driver.find_element_by_xpath("/html/body/form/div/div[2]/input[1]")
        consulta.submit()

        # Janela antiga
        driver.switch_to.window(driver.window_handles[0])
        # fecha janela antiga
        driver.close()
        # assume janela nova
        driver.switch_to.window(driver.window_handles[0])
    except:
        list = []
        list.append({'LOG': 'Não a registros disponivel para essa entrada!'})
        return list


    lista_links= driver.find_elements_by_xpath("/html/body/table/tbody/tr[2]/td/div/a")

    lista_saida = []

    #verifica se a varios links a serem acessados
    if len(lista_links) ==0 :
        dicionario = get_dados(driver)
        if dicionario['inscricao_estadual'] != "Erro":
            lista_saida.append(dicionario)
        driver.quit()
        return lista_saida


    for link in lista_links:
        link.click()
        driver.switch_to.window(driver.window_handles[1])

        dicionario = get_dados(driver)
        if dicionario['inscricao_estadual'] != "Erro":
            lista_saida.append(dicionario)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.quit()
    return lista_saida