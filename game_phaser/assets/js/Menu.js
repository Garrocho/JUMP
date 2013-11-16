BasicGame.Menu = function (game) {
	this.musica = null;
	this.botao_jogar = null;
};

BasicGame.Menu.prototype = {

	create: function () {
	    this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
	    this.fundo2 = this.add.tileSprite(0, 512, 1024, 512, 'nuvem');
		this.musica = this.add.audio('som_musica');
		this.musica.play('',0,1,true);
		this.estilo = { font: "bold 150pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 15 };
		this.estilo2 = { font: "bold 22pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 5 };
        this.titulo = this.add.text(this.world.centerX, this.world.centerY-250, "JUMP!", this.estilo);
        this.titulo.anchor.setTo(0.5, 0.5);
        this.titulo2 = this.add.text(this.world.centerX, this.world.centerY-130, "Jogo Unificado para Movimentação Projetada", this.estilo2);
        this.titulo2.anchor.setTo(0.5, 0.5);
		this.botao_jogar = this.add.button(this.world.centerX - 150, 500, 'botao_jogar', this.novo_jogo, this, 2, 1, 0);
	},

	update: function () {
	    this.fundo1.tilePosition.x -= 0.5;
	    this.fundo2.tilePosition.x -= 1;
	},

	novo_jogo: function (pointer) {
		this.musica.stop();
		this.game.state.start('Jogo');
	},
};
