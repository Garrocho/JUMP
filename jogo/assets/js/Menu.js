BasicGame.Menu = function (game) {
};

BasicGame.Menu.prototype = {

	create: function () {
		this.eRanking = false;
	    this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
	    this.fundo2 = this.add.tileSprite(0, 512, 1024, 512, 'nuvem');
		this.musica = this.add.audio('som_menu');
		this.estilo = { font: "bold 150pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 15 };
		this.estilo2 = { font: "bold 22pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 5 };
		this.estilo4 = { font: "bold 15pt Arial", fill: "#ffffff", align: "left", stroke: "#000000", strokeThickness: 5 };
		this.estilo3 = { font: "bold 40pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 8 };
        this.titulo = this.add.text(this.world.centerX, this.world.centerY-270, "JUMP!", this.estilo);
        this.titulo.anchor.setTo(0.5, 0.5);
        this.titulo2 = this.add.text(this.world.centerX, this.world.centerY-160, "Jogo Unificado para Movimentação Projetada", this.estilo2);
        this.titulo2.anchor.setTo(0.5, 0.5);
        this.botao_ranking = this.add.button(this.world.centerX + 20, 330, 'botao_ranking', this.ranking, this, 2, 1, 0);
		this.botao_jogar = this.add.button(this.world.centerX - 270, 330, 'botao_jogar', this.novo_jogo, this, 2, 1, 0);
		if (this.stage.scale.isFullScreen == null)
	        this.botao_tela = this.add.button(this.world.centerX + 370, 2, 'botao_tela_cheia', this.mudar_tela, this, 2, 1, 0);
	    else
	        this.botao_tela = this.add.button(this.world.centerX + 370, 2, 'botao_tela_normal', this.mudar_tela, this, 2, 1, 0);

	    this.botao_som = this.add.button(this.world.centerX + 445, 0, 'botao_som_on', this.mudar_som, this, 2, 1, 0);
		
		if (window.WebSocket) {
            this.conexao = new WebSocket('ws://108.59.6.230:14527');
            this.conexao.onmessage = function(message) {
                var json = JSON.parse(message.data);
                this.rank = "RANK";
                this.nome = "NOME";
                this.distancia = "DISTANCIA";
                this.moedas = "MOEDAS";
                this.localizacao = "LOCALIZAÇÃO";
                json.sort(function(a, b) {
                    return (b["distancia"] - a["distancia"]);
                });
                if(json != null){
                    for (i=0; i < json.length; i++){
                        if (i == 6)
                            break;
                        this.rank += "\n" + (i+1);
                        this.nome += "\n" + json[i]["nome"];
                        this.distancia += "\n" + json[i]["distancia"];
                        this.moedas += "\n" + json[i]["moedas"];
                        this.localizacao += "\n" + json[i]["localizacao"];
                    }
                }
            }
        }

        this.titulo3 = this.add.text(-10, this.world.centerY-120, "----------------------------------------------------------------------------------------", this.estilo3);        
        this.titulo3 = this.add.text(-10, this.world.centerY, "----------------------------------------------------------------------------------------", this.estilo3);
        
        this.rank = this.add.text(50, 610, "", this.estilo2);
        this.rank.anchor.setTo(0.5, 0.5);
        this.nome = this.add.text(200, 610, "", this.estilo2);
        this.nome.anchor.setTo(0.5, 0.5);
        this.distancia = this.add.text(400, 610, "", this.estilo2);
        this.distancia.anchor.setTo(0.5, 0.5);
        this.moedas = this.add.text(650, 610, "", this.estilo2);
        this.moedas.anchor.setTo(0.5, 0.5);        
        this.localizacao = this.add.text(900, 610, "", this.estilo2);
        this.localizacao.anchor.setTo(0.5, 0.5);

        this.descricao = this.add.text(270, 570, "", this.estilo4);
        this.descricao.anchor.setTo(0.5, 0.5);

        this.equipe = this.add.text(800, 610, "", this.estilo4);
        this.equipe.anchor.setTo(0.5, 0.5);
        this.musica.play('',0,1,true);
        this.valida_config();
        
	},

	update: function () {
	    this.fundo1.tilePosition.x -= 0.5;
	    this.fundo2.tilePosition.x -= 1;
	    if (this.conexao.nome != undefined && this.eRanking) {
	        this.rank.setText(this.conexao.rank);
	        this.nome.setText(this.conexao.nome);
	        this.distancia.setText(this.conexao.distancia);
	        this.moedas.setText(this.conexao.moedas);
	        this.localizacao.setText(this.conexao.localizacao);
	        this.descricao.setText("");
	        this.equipe.setText("");
	    }
	    else {
	    	this.rank.setText("");
	        this.nome.setText("");
	        this.distancia.setText("");
	        this.localizacao.setText("");
	        this.moedas.setText("");

	        this.descricao.setText("Descrição do Projeto:\nProcessamento digital de imagens\naplicado ao desenvolvimento de um\njogo interativo direcionado à prática\nde exercícios físicos.");
	        this.equipe.setText("Equipe:\nArthur Nascimento Assunção\nBruno Ferreira da Costa\nCharles Tim Batista Garrocho\nLucas Gabriel de Araújo Assis\nMariana Wamser Campos\nPaulo Vitor Francisco");
	    }
	},

	novo_jogo: function (pointer) {
		this.musica.stop();
		this.game.state.start('Jogo');
	},
	
	ranking: function (pointer) {
		this.eRanking = !this.eRanking;
		if (this.eRanking)
			this.botao_ranking.loadTexture('botao_sobre');
		else
			this.botao_ranking.loadTexture('botao_ranking');
	},

	mudar_som: function (pointer) {
		if (this.som == 0) {
			this.botao_som.loadTexture('botao_som_on');
			this.musica.volume = 1;
			localStorage.setItem('jump_som', 1);
			this.som = 1;
		}
		else {
			this.botao_som.loadTexture('botao_som_off');
			this.musica.volume = 0;
			localStorage.setItem('jump_som', 0);
			this.som = 0;
		}
	},

	mudar_tela: function() {
	    if (this.stage.scale.isFullScreen == null) {
	        this.stage.scale.startFullScreen();
	        this.botao_tela.loadTexture('botao_tela_normal');
	    }
	    else {
	        this.stage.scale.stopFullScreen();
	        this.botao_tela.loadTexture('botao_tela_cheia');
	    }
	},
	
	valida_config: function() {
	    this.som = localStorage.getItem('jump_som');
        if (this.som == null)
            this.som = 1;
        else
            this.som = parseInt(this.som);
        if (this.som == 0)
            this.botao_som.loadTexture('botao_som_off');
        else
            this.botao_som.loadTexture('botao_som_on');
        this.musica.volume = this.som;
	},
};
