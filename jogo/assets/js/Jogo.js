BasicGame.Jogo = function (game) {
    this.game;
    this.add;
    this.camera;
    this.cache;
    this.input;
    this.load;
    this.math;
    this.sound;
    this.stage;
    this.time;
    this.tweens;
    this.world;
    this.particles;
    this.physics;
    this.rnd;
    this.moedas = new Array();
    this.inimigos = new Array();
    this.velocidade = new Array();
};

BasicGame.Jogo.prototype = {

	create: function () {
	    this.velocidade[0] = 0.5;
	    this.velocidade[1] = 1;
	    this.velocidade[2] = 2;
        this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
        this.fundo2 = this.add.tileSprite(0, 220, 1024, 512, 'montanha');
        this.fundo3 = this.add.tileSprite(0, 520, 1024, 256, 'caminho');
        this.jogador = this.add.sprite(250, 600, 'correndo');
        this.jogador.animations.add('correr');
        this.jogador.animations.play('correr', 10, true);
        this.jogador.animations.pixelPerfect = true;
        this.jogador.body.collideWorldBounds = true;
        this.fabrica = this.add.group();
        this.pulando = false;
        this.agachado = false;
        this.contador = 0;
        this.kmh = 5;
        this.pulando = false;
        this.aux_pulo = 0;
        
        this.moeda_cont = this.add.sprite(10, 10, 'moeda');
        this.moeda_cont.animations.add('correr');
        this.moeda_cont.animations.play('correr', 10, true);
        
        this.corredor_cont = this.add.sprite(120, 10, 'correndo_min');
        this.corredor_cont.animations.add('correr');
        this.corredor_cont.animations.play('correr', 10, true);
        
        this.estilo = { font: "bold 20pt Arial", fill: "#ffffff", stroke: "#000000", strokeThickness: 3 };
        this.texto1 = this.add.text(220, 30, "5 Km/h", this.estilo);
        this.texto1.anchor.setTo(0.5, 0.5);
        this.texto2 = this.add.text(80, 30, "0", this.estilo);
        this.texto2.anchor.setTo(0.5, 0.5);

        this.cursors = this.input.keyboard.createCursorKeys();
        this.som_musica = this.add.audio('som_musica',1,true);
        this.som_moeda = this.add.audio('som_moeda',1,true);
        this.som_pulo = this.add.audio('som_pulo',1,true);
        this.som_musica.play('',0,1,true);
        this.stage.scale.startFullScreen();
        this.ver_level = 0;
        this.ultimo_eixo_x = 1024;

        if (window.WebSocket) {
            this.conexao = new WebSocket('ws://127.0.0.1:1338');
            this.conexao.onmessage = function(message) {
                this.movimento = parseInt(message.data);
                console.log("Movimento: ", this.movimento);
            }
        }
	},

	update: function () {
	    this.ver_level++;
	    if (this.ver_level == 100) {
	        this.velocidade[0] += 0.05;
	        this.velocidade[1] += 0.10;
	        this.velocidade[2] += 0.20;
	        this.ver_level = 0;
	        this.kmh++;
	        this.texto1.setText(this.kmh + " Km/h");
	    }
	     
        this.fundo1.tilePosition.x -= this.velocidade[0];
        this.fundo2.tilePosition.x -= this.velocidade[1];
        this.fundo3.tilePosition.x -= this.velocidade[2];
        this.jogador.body.velocity.x = 0;
        this.jogador.body.velocity.y = 0;
        
        if ((this.cursors.down.isDown && !this.pulando) || (this.conexao.movimento === -1 && !this.pulando))
        {
            if (!this.agachado) {
                this.som_pulo.play();
                this.agachado = true;
            }
            this.jogador.loadTexture('agachado', 0);
            this.jogador.body.y=650;
        }
        else if ((this.cursors.down.isUp && this.agachado) || (this.conexao.movimento === 0 && this.agachado))
        {
            this.som_pulo.play();
            this.agachado = false;
            this.jogador.loadTexture('correndo', 0);
            this.jogador.animations.add('correr');
            this.jogador.animations.pixelPerfect = true;
            this.jogador.animations.play('correr', 10, true);
        }

        if ((this.cursors.up.isDown && !this.pulando && !this.agachado) || (this.conexao.movimento === 1 && !this.pulando && !this.agachado))
        {
            this.som_pulo.play();
            this.pulando = true;
            this.jogador.loadTexture('pulando', 0);
            this.jogador.animations.add('pular');
            this.jogador.animations.pixelPerfect = true;
            this.jogador.animations.play('pular', 10, true);
        }

        if (this.pulando) {
            if (this.aux_pulo == 8000) {
                this.aux_pulo = 0;
                this.pulando = false;
                this.conexao.movimento = 0;
                this.jogador.loadTexture('correndo', 0);
                this.jogador.animations.add('correr');
                this.jogador.animations.pixelPerfect = true;
                this.jogador.animations.play('correr', 10, true);
            }
            else {
                if (this.aux_pulo <= 3600) {
                    this.jogador.body.velocity.y = -500;
                    this.jogador.body.velocity.x = 50;
                }
                else {
                    this.jogador.body.velocity.y = 400;
                    this.jogador.body.velocity.x = 50;
                }
                this.aux_pulo+= 100;
            }
        }
        else {
            if (this.jogador.body.y > 600)
                this.jogador.body.velocity.y = -Math.abs(600-this.jogador.y);
            else
                this.jogador.body.velocity.y = Math.abs(600-this.jogador.y);
            if (this.jogador.body.x > 250)
                this.jogador.body.velocity.x = -Math.abs(250-this.jogador.x);
            else
                this.jogador.body.velocity.x = Math.abs(250-this.jogador.x);
        }
        this.administrar_grupo(this.moedas, 'moeda', 50, 5, 10, 300);
        this.administrar_grupo(this.inimigos, 'inimigo', 100, 5, 10, 550);
        this.physics.collide(this.jogador, this.fabrica, this.tratador_colisao, null, this);
	},
	
	tratador_colisao: function (obj1, obj2) {
	    if (obj2.name === 'moeda'){
            this.som_moeda.play();
            obj2.kill();
            this.contador++;
            this.texto2.setText(this.contador);
        }
        else
        {
            obj1.kill();
            this.conexao.close();
            this.som_musica.stop();
            var recorde = {
                'moedas': this.contador,
                'kmh': this.kmh
            }
            localStorage['recorde'] = JSON.stringify(recorde);
		    this.game.state.start('GameOver');
        }
	},
	
    administrar_grupo: function (grupo, nome_ator, distancia, qtde_min, qtde_max, eixo_y) {
        if (grupo.length <= 1) {
            if (eixo_y < 400) {
                qtde_y = this.rnd.integerInRange(3, 6);
                aux_eixo_x = this.ultimo_eixo_x;
            }
            else {
                aux_eixo_x = this.ultimo_eixo_x;
                qtde_y = 1;
            }
            qtde_x = this.rnd.integerInRange(qtde_min, qtde_max);
            for (k=0; k < qtde_y; k++) {
                eixo_x = aux_eixo_x;
                for (i=0; i < qtde_x; i++) {
                    ator = this.fabrica.create(eixo_x, eixo_y, nome_ator);
                    ator.name = nome_ator;
                    ator.animations.add('correr');
                    ator.animations.play('correr', 10, true);
                    ator.body.pixelPerfect = true;
                    grupo[grupo.length] = ator;
                    eixo_x+=distancia;
                }
                eixo_y+=distancia;
            }
        }
        this.ultimo_eixo_x = eixo_x;
        for (i=0; i < grupo.length-1; i++) {
            grupo[i].body.velocity.x = -(this.velocidade[2]*60);
            if (grupo[i].body.x < -150 || !grupo[i].exists) {
                grupo[i].kill();
                grupo.splice(i, 1);
            }
        }
    },
    
	quitGame: function (pointer) {
		this.game.state.start('Menu');
	}
};
