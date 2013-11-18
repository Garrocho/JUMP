JUMP!
=====
Jogo Unificado para Movimentação Projetada

# Instalação

  1. Instale o Git:

    <code>
        apt-get install python-pygame git
    </code>
   

  2. Baixe o Jogo:

    <code>
        git clone https://github.com/CharlesGarrocho/jump.git
    </code>

    <code>
        cd jump
    </code>


  3. Instalando e Configurando o Node.js:

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

  4. Instalando Módulos do Node.js:

    <code>
        cd jump
    </code>

    <code>
        npm install node-static
    </code>

    <code>
        npm install websocket
    </code>

    <code>
        npm install chokidar
    </code>


  5. Inicializando o Serviço do Cliente e do Servidor:

    <code>
        cd jump
    </code>

    <code>
        node JogoServidor.js
    </code>

    <code>
        Abra um Novo Terminal ou aba.
    </code>

    <code>
        cd jump
    </code>

    <code>
        node JogoCliente.js
    </code>

    <code>
        Abra o navegador do Google Chrome e entre no endereço: http://0.0.0.0:29755
    </code>
