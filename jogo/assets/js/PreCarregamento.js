
BasicGame.PreCarregamento = function (game) {
};

BasicGame.PreCarregamento.prototype = {

    preload: function () {
        this.fundo = this.add.sprite(0, 0, 'background');
        this.barra_carregamento = this.add.sprite(15, this.world.centerY+170, 'barra');
        this.estilo = { font: "bold 50pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 8 };
        this.titulo = this.add.text(this.world.centerX, this.world.centerY+120, "Carregando...", this.estilo);
        this.titulo.anchor.setTo(0.5, 0.5);
        
        this.load.setPreloadSprite(this.barra_carregamento);
        this.load.image('ifet', 'assets/img/ifet.png');
        this.load.image('nuvem', 'assets/img/nuvem.png');
        this.load.image('montanha', 'assets/img/montanha.png');
        this.load.image('caminho', 'assets/img/caminho.png');
        this.load.image('agachado', 'assets/img/agachado.png');
        this.load.image('botao_som_on', 'assets/img/botao_som_on.png');
        this.load.image('botao_som_off', 'assets/img/botao_som_off.png');
        this.load.image('botao_tela_normal', 'assets/img/botao_tela_normal.png');
        this.load.image('botao_tela_cheia', 'assets/img/botao_tela_cheia.png');
        this.load.spritesheet('moeda', 'assets/img/moedas.png', 44, 40, 10);
        this.load.spritesheet('botao_sair', 'assets/img/botao_sair.png', 250, 60);
        this.load.spritesheet('botao_ranking', 'assets/img/botao_ranking.png', 250, 60);
        this.load.spritesheet('botao_calibrar', 'assets/img/botao_calibrar.png', 250, 60);
        this.load.spritesheet('botao_sobre', 'assets/img/botao_sobre.png', 250, 60);
        this.load.spritesheet('correndo', 'assets/img/correndo2.png', 58.71, 100);
        this.load.spritesheet('correndo_min', 'assets/img/correndo2_min.png', 23.5, 40);
        this.load.spritesheet('pulando', 'assets/img/pulando2.png', 57.2, 100);
        this.load.spritesheet('inimigo', 'assets/img/passaro.png', 74.9, 72);
        this.load.audio('som_moeda', ['assets/sons/moeda.ogg']);
        this.load.audio('som_menu', ['assets/sons/menu.ogg']);
        this.load.audio('som_menu_item', ['assets/sons/menu_item.ogg']);
        this.load.audio('som_pulo', ['assets/sons/pulo.ogg']);
        this.load.audio('game_over', ['assets/sons/game_over.ogg']);
        this.load.audio('som_musica', ['assets/sons/fase_1.ogg']);
    },

    create: function () {
        this.barra_carregamento.cropEnabled = true;
    },

    update: function () {
        
        if (this.cache.isSoundDecoded('som_musica'))
        {
            this.game.state.start('Menu');
        }
    }
};
