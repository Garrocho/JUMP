BasicGame.Menu = function (game) {
};

BasicGame.Menu.prototype = {

    create: function () {
        this.eRanking = false;
        this.fundo1 = this.add.tileSprite(0, 0, 1024, 512, 'nuvem');
        this.fundo2 = this.add.tileSprite(0, 512, 1024, 512, 'nuvem');
        this.som_musica = this.add.audio('som_menu');
        this.estilo = { font: "bold 150pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 15 };
        this.estilo2 = { font: "bold 22pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 5 };
        this.estilo4 = { font: "bold 15pt Arial", fill: "#ffffff", align: "left", stroke: "#000000", strokeThickness: 5 };
        this.estilo3 = { font: "bold 40pt Arial", fill: "#ffffff", align: "center", stroke: "#000000", strokeThickness: 8 };
        this.titulo = this.add.text(this.world.centerX, this.world.centerY-270, "JUMP!", this.estilo);
        this.titulo.anchor.setTo(0.5, 0.5);
        this.titulo2 = this.add.text(this.world.centerX, this.world.centerY-160, "Jogo Unificado para Movimentação Projetada", this.estilo2);
        this.titulo2.anchor.setTo(0.5, 0.5);
        this.botao_ranking = this.add.button(this.world.centerX - 130, 300, 'botao_ranking', this.ranking, this, 2, 1, 0);
        this.botao_jogar = this.add.button(this.world.centerX - 430, 300, 'botao_jogar', this.novo_jogo, this, 2, 1, 0);
        if (this.stage.scale.isFullScreen == null)
            this.botao_tela = this.add.button(this.world.centerX + 370, 2, 'botao_tela_cheia', this.mudar_tela, this, 2, 1, 0);
        else
            this.botao_tela = this.add.button(this.world.centerX + 370, 2, 'botao_tela_normal', this.mudar_tela, this, 2, 1, 0);

        this.botao_som = this.add.button(this.world.centerX + 445, 0, 'botao_som_on', this.mudar_som, this, 2, 1, 0);
        this.botao_sair = this.add.button(this.world.centerX + 170, 300, 'botao_sair', this.sair, this, 2, 1, 0);
        
        if (window.WebSocket) {
            this.conexao = new WebSocket('ws://108.59.6.230:14527');
            
            this.conexao.onopen = function() {
                this.send(JSON.stringify({"TIPO": "OBTER"}));
            }
            this.conexao.onmessage = function(message) {
                var json = JSON.parse(message.data);
                this.rank = "RANK";
                this.nome = "NOME";
                this.kmh = "KM/H";
                this.moedas = "MOEDAS";
                this.localizacao = "LOCALIZAÇÃO";
                json.sort(function(a, b) {
                    return (b["kmh"] - a["kmh"]);
                });
                if(json != null){
                    for (i=0; i < json.length; i++){
                        if (i == 6)
                            break;
                        this.rank += "\n" + (i+1);
                        this.nome += "\n" + json[i]["nome"];
                        this.kmh += "\n" + json[i]["kmh"];
                        this.moedas += "\n" + json[i]["moedas"];
                        this.localizacao += "\n" + json[i]["localizacao"];
                    }
                }
            }
        }

        //this.titulo3 = this.add.text(-10, this.world.centerY-120, "----------------------------------------------------------------------------------------", this.estilo3);        
        this.titulo3 = this.add.text(-10, this.world.centerY, "----------------------------------------------------------------------------------------", this.estilo3);
        
        this.rank = this.add.text(50, 610, "", this.estilo2);
        this.rank.anchor.setTo(0.5, 0.5);
        this.nome = this.add.text(200, 610, "", this.estilo2);
        this.nome.anchor.setTo(0.5, 0.5);
        this.kmh = this.add.text(400, 610, "", this.estilo2);
        this.kmh.anchor.setTo(0.5, 0.5);
        this.moedas = this.add.text(650, 610, "", this.estilo2);
        this.moedas.anchor.setTo(0.5, 0.5);        
        this.localizacao = this.add.text(900, 610, "", this.estilo2);
        this.localizacao.anchor.setTo(0.5, 0.5);

        this.descricao = this.add.text(250, 520, "", this.estilo4);
        this.descricao.anchor.setTo(0.5, 0.5);

        this.equipe = this.add.text(800, 610, "", this.estilo4);
        this.equipe.anchor.setTo(0.5, 0.5);
        this.som_musica.play('',0,1,true);
        this.valida_config();
        this.ifet = this.add.sprite(38, 600, 'ifet');
    },

    update: function () {
        this.fundo1.tilePosition.x -= 0.5;
        this.fundo2.tilePosition.x -= 1;
        if (this.conexao.nome != undefined && this.eRanking) {
            this.rank.setText(this.conexao.rank);
            this.nome.setText(this.conexao.nome);
            this.kmh.setText(this.conexao.kmh);
            this.moedas.setText(this.conexao.moedas);
            this.localizacao.setText(this.conexao.localizacao);
            this.descricao.setText("");
            this.equipe.setText("");
        }
        else {
            this.rank.setText("");
            this.nome.setText("");
            this.kmh.setText("");
            this.localizacao.setText("");
            this.moedas.setText("");
            this.descricao.setText("Descrição do Projeto:\nProcessamento digital de imagens aplicado\nao desenvolvimento de um jogo interativo\ndirecionado à prática de exercícios físicos.");
            this.equipe.setText("Orientador:\nRafael José de Alencar Almeida\n\nEquipe:\nArthur Nascimento Assunção\nBruno Ferreira da Costa\nCharles Tim Batista Garrocho\nLucas Gabriel de Araújo Assis\nMariana Wamser Campos\nPaulo Vitor Francisco");
        }
    },

    novo_jogo: function (pointer) {
        this.som_musica.stop();
        this.game.state.start('Jogo');
    },
    
    ranking: function (pointer) {
        this.eRanking = !this.eRanking;
        if (this.eRanking) {
            this.ifet.visible = false;
            this.botao_ranking.loadTexture('botao_sobre');
        }
        else {
            this.ifet.visible = true;
            this.botao_ranking.loadTexture('botao_ranking');
        }
    },

    mudar_som: function () {
        if (this.som == 0) {
            this.botao_som.loadTexture('botao_som_on');
            this.som = 1;
        }
        else {
            this.botao_som.loadTexture('botao_som_off');
            this.som = 0;
        }
        this.som_musica.volume = this.som;
        if(typeof(Storage)!=="undefined")
            localStorage.setItem('jump_som', this.som);
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
        if(typeof(Storage)!=="undefined")
            this.som = localStorage.getItem('jump_som');
        else
            this.som = 1;
        if (this.som == null)
            this.som = 1;
        else
            this.som = parseInt(this.som);
        if (this.som == 0)
            this.botao_som.loadTexture('botao_som_off');
        else
            this.botao_som.loadTexture('botao_som_on');
        this.som_musica.volume = this.som;
    },
    
    sair: function() {
        window.close();
    },
};
