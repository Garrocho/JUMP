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
};

BasicGame.Jogo.prototype = {

	create: function () {
        this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
        this.fundo2 = this.add.tileSprite(0, 220, 1024, 512, 'montanha');
        this.fundo3 = this.add.tileSprite(0, 520, 1024, 256, 'caminho');
        this.jogador = this.add.sprite(250, 600, 'correndo');
        this.jogador.animations.add('correr');
        this.jogador.animations.play('correr', 10, true);
        this.jogador.animations.pixelPerfect = true;
        this.jogador.body.collideWorldBounds = true;
        this.grupo = this.add.group();
        this.pulando = false;
        this.jogador.scale.x = -1;
        this.contador = 0;
        this.pulando = false;
        this.aux_pulo = 0;
        this.texto2 = this.add.text(10, 10, "Moedas: " + this.contador, {
            font: "20px Arial",
            fill: "#ff0044",
            align: "center"
        });
        this.cursors = this.input.keyboard.createCursorKeys();
        this.musica = this.add.audio('musica',1,true);
        this.som_moeda = this.add.audio('moeda',1,true);
        this.som_pulo = this.add.audio('pulo',1,true);
        this.administrar_moedas();
        this.musica.play('',0,1,true);
        this.stage.scale.startFullScreen();
	},

	update: function () {
        this.fundo1.tilePosition.x -= 0.5;
        this.fundo2.tilePosition.x -= 1;
        this.fundo3.tilePosition.x -= 2;
        this.jogador.body.velocity.x = 0;
        this.jogador.body.velocity.y = 0;

        if (this.cursors.up.isDown && !this.pulando)
        {
            this.som_pulo.play();
            this.pulando = true;
            this.jogador.loadTexture('pulando', 0);
            this.jogador.animations.add('pular');
            this.jogador.animations.pixelPerfect = true;
            this.jogador.animations.play('pular', 10, true);
        }

        if (this.pulando) {
            if (this.aux_pulo == 6000) {
                this.aux_pulo = 0;
                this.pulando = false;
                this.jogador.loadTexture('correndo', 0);
                this.jogador.animations.add('correr');
                this.jogador.animations.pixelPerfect = true;
                this.jogador.animations.play('correr', 10, true);
            }
            else {
                if (this.aux_pulo <= 2600)
                    this.jogador.body.velocity.y = -500;
                else
                    this.jogador.body.velocity.y = 400;
                this.aux_pulo+= 100;
            }
        }
        else {
            if (this.jogador.body.y > 600)
                this.jogador.body.velocity.y = -Math.abs(600-this.jogador.y);
            else
                this.jogador.body.velocity.y = Math.abs(600-this.jogador.y);
        }

        this.administrar_moedas();
        this.physics.collide(this.jogador, this.grupo, this.tratador_colisao, null, this);
	},
	
	tratador_colisao: function (obj1, obj2) {
	    if (obj2.name === 'moeda'){
            this.som_pulo.play();
            obj2.kill();
            this.contador++;
            this.texto2.setText("Moedas: " + this.contador);
        }
        else
        {
            obj1.kill();
            this.texto2.setText("Game Over");
        }
	},
	
    administrar_moedas: function () {
        if (this.moedas.length <= 1) {
            this.x = this.rnd.integerInRange(2, 10);
            this.eixox = 1024;
            for (i=0; i < this.x; i++) {
                this.ator = this.grupo.create(this.eixox, 500, 'moeda');
                this.ator.name = 'moeda';
                this.ator.animations.add('correr');
                this.ator.animations.play('correr', 10, true);
                this.ator.body.pixelPerfect = true;
                this.moedas[this.moedas.length] = this.ator;
                this.eixox+=50;
            }
        }
        console.log(this.moedas.length);
        for (i=0; i < this.moedas.length-1; i++) {
            this.moedas[i].body.velocity.x = -150;
            if (this.moedas[i].body.x < -150 || !this.moedas[i].exists) {
                this.moedas[i].kill();
                this.moedas.splice(i, 1);
            }
        }
    },
    
	quitGame: function (pointer) {
		this.game.state.start('Menu');
	}
};
