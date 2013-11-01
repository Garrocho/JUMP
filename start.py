import os
import pygame
import subprocess
from fonte import menu
from fonte import dados
from multiprocessing import Process


def ex_servico(servico):
	if servico == 'node':
		os.system('cd ' + dados.ranking_dir + '/static/js/; node servidor.js')
	elif servico == 'simple':
		os.system('cd ranking; python -m SimpleHTTPServer')
	

if __name__ == '__main__':
	try:
		node = Process(target=ex_servico, args=('node',))
		node.start()
		simple = Process(target=ex_servico, args=('simple',))
		simple.start()
		m = menu.Menu()
		m.loop()
	except:
		print 'Erro, Instale as Depencias...'
	finally:
		node.terminate()
		simple.terminate()