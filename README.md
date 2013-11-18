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


  4. Inicializando o Serviço do Cliente e do Servidor:

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

  5. Instalando Módulos do Node.js:

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

  6. Instalando Módulo GeoIP

    <code>
        sudo apt-get install python-geoip
    </code>
    
    <code>
        sudo apt-get install libc6
    </code>
    
    <code>
        sudo apt-get install libgeoip1
    </code>        

  7. Crie um script para consultas do banco de daods do GeoIP (caso não tenha a pasta examples crie-a)
  
    <code>
        vim /usr/share/doc/libgeoip1/examples/geolitecityupdate.sh
    </code>
    
  8. Conteúdo do script geolitecityupdate.sh

        #!/bin/shGUNZIP="/bin/gunzip"
        MAXMINDURL="http://geolite.maxmind.com/download/geoip/database/"
        WGET="/usr/bin/wget -q -O -"
        TMPDIR=$(mktemp -d)
        if [ ! -d "$DATADIR" ] ; then
        echo "Data directory $DATADIR/ doesn't exist!"
        exit 1
        fi
        if [ ! -w "$DATADIR" ] ; then
        echo "Can't write to $DATADIR directory!"
        exit 1
        fi
        cd "${TMPDIR}"
        ${WGET} "${MAXMINDURL}/GeoLiteCity.dat.gz" | ${GUNZIP} > GeoIPCity.datif [ $? != 0 ] ; then
        echo "Can't download a free GeoLite City database!"
        exit 1
        fi
        mv -f "GeoIPCity.dat" "${DATADIR}/"
        if [ $? != 0 ] ; then
        echo "Can't move databases file to ${DATADIR}/"
        exit 1
        fi
        exit 0

    
  9. Copie o arquivo GeoIPCity.dat para a pasta do GeoIP (o arquivo GeoIPCity.dat está localizado no diretório dados do projeto JUMP)
  
      <code>
        sudo cp /dados/GeoIPCity.dat /usr/share/GeoIP/.
      </code>
