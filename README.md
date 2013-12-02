JUMP!
=====
Jogo Unificado para Movimentação Projetada

# Instalação

  1. Instale o Git:

    <code>
        apt-get install git
    </code>


  2. Instalando e Configurando o Node.js:

    <code>
        sudo apt-get install g++ curl libssl-dev apache2-utils
    </code>

    <code>
        wget http://nodejs.org/dist/v0.10.21/node-v0.10.21.tar.gz
    </code>

    <code>
        tar -xf node-v0.10.21.tar.gz
    </code>

    <code>
        cd node-v0.10.21
    </code>

    <code>
        ./configure
    </code>

    <code>
        make
    </code>
 
    <code>
        sudo make install
    </code>


  3. Instalando e Configurando o Phaser:

    <code>
        git clone https://github.com/photonstorm/phaser.git
    </code>

    <code>
        npm install -g grunt-cli
    </code>

    <code>
        cd phaser
    </code>

    <code>
        npm install
    </code>
  
  4. Baixe o Jogo:

    <code>
        git clone https://github.com/CharlesGarrocho/jump.git
    </code>


  5. Instalando Módulos do Node.js nas pasta que irá rodar os servidores (detector e ranking):

    <code>
        npm install node-static
    </code>

    <code>
        npm install websocket
    </code>

    <code>
        npm install chokidar
    </code>


  6. Inicializando o Jogo e do Servidor do Ranking:

    <code>
        cd jump/jogo
    </code>

    <code>
        python -m SimpleHTTPServer
    </code>

    <code>
        Abra um Novo Terminal ou aba.
    </code>

    <code>
        cd jump/ranking
    </code>

    <code>
        node Ranking.js
    </code>

    <code>
        Abra o navegador do Google Chrome e entre no endereço: http://0.0.0.0:29755
    </code>
