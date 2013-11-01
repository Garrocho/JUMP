import pygame
import subprocess
from fonte import menu
from fonte import dados
import subprocess

#subprocess.call(["node", dados.ranking_dir + "/static/js/servidor.js"])
#subprocess.call(["python -m SimpleHTTPServer", dados.ranking_dir])


if __name__ == '__main__':
	m = menu.Menu()
	m.loop()