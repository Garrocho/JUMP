
BasicGame.PreCarregamento = function (game) {

	this.background = null;
	this.preloadBar = null;
	this.ready = false;
};

BasicGame.PreCarregamento.prototype = {

	preload: function () {
		this.background = this.add.sprite(0, 0, 'background');
		this.preloadBar = this.add.sprite(350, 100, 'barra');
		this.estilo = { font: "bold 60pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 10 };
		this.titulo = this.add.text(this.world.centerX-400, this.world.centerY-250, "Carregando o JUMP...", this.estilo);
        
		this.load.setPreloadSprite(this.preloadBar);
		this.load.image('nuvem', 'assets/img/nuvem.png');
        this.load.image('montanha', 'assets/img/montanha.png');
        this.load.image('caminho', 'assets/img/caminho.png');
        this.load.spritesheet('moeda', 'assets/img/moedas.png', 44, 40, 10);
        this.load.spritesheet('botao_jogar', 'assets/img/botao_jogar.png', 250, 60);
        this.load.spritesheet('botao_sair', 'assets/img/botao_sair.png', 250, 60);
        this.load.spritesheet('correndo', 'assets/img/correndo.png', 100, 100);
        this.load.spritesheet('pulando', 'assets/img/pulando.png', 100, 100);
        this.load.spritesheet('inimigo', 'assets/img/inimigo.png', 75, 65, 4);
        this.load.audio('musica', ['assets/sons/fase_1.wav']);
        this.load.audio('pulo', ['assets/sons/pulo.ogg']);
	},

	create: function () {
		this.preloadBar.cropEnabled = true;
	},

	update: function () {
		
		if (this.cache.isSoundDecoded('musica') && this.ready == false)
		{
			this.ready = false;
			this.game.state.start('Menu');
		}
	}
};
