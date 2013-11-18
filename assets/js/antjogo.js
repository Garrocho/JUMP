var game = new Phaser.Game(1024, 768, Phaser.AUTO, '', { preload: preload, create: create, update: update});
var fundo1, fundo2, fundo3;
var jogador;
var texto;
var grupo;
var contador;
var inimigos = new Array();
var moedas = new Array();
var qtde_moedas;
var som_moeda, som_pulo;
var pulando, aux_pulo;

function preload() {
     game.load.image('nuvem', 'assets/img/nuvem.png');
     game.load.image('montanha', 'assets/img/montanha.png');
     game.load.image('caminho', 'assets/img/caminho.png');
     game.load.spritesheet('moeda', 'assets/img/moedas.png', 44, 40, 10);
     game.load.spritesheet('correndo', 'assets/img/correndo.png', 100, 100);
     game.load.spritesheet('pulando', 'assets/img/pulando.png', 100, 100);
     game.load.spritesheet('inimigo', 'assets/img/inimigo.png', 75, 65, 4);
     game.load.audio('musica', ['assets/sons/fase_1.wav']);
     game.load.audio('pulo', ['assets/sons/pulo.ogg']);
}

function create() {
    fundo1 = game.add.tileSprite(0, 0, 1024, 512, 'nuvem');
    fundo2 = game.add.tileSprite(0, 220, 1024, 512, 'montanha');
    fundo3 = game.add.tileSprite(0, 520, 1024, 256, 'caminho');
    jogador = game.add.sprite(250, 600, 'correndo');
    jogador.animations.add('correr');
    jogador.animations.play('correr', 10, true);
    jogador.animations.pixelPerfect = true;
    jogador.body.collideWorldBounds = true;
    grupo = game.add.group();
    qtde_moedas = 0;
    pulando = false;
    jogador.scale.x = -1;

    contador = 0;
    pulando = false;
    aux_pulo = 0;

    texto = game.add.text(10, 10, "Moedas: " + contador, {
        font: "20px Arial",
        fill: "#ff0044",
        align: "center"
    });
    cursors = game.input.keyboard.createCursorKeys();
    criar_ator(inimigos, 'inimigo', 2024, 650);
    
    musica = game.add.audio('musica',1,true);
    som_moeda = game.add.audio('moeda',1,true);
    som_pulo = game.add.audio('pulo',1,true);
    administrar_moedas();
    musica.play('',0,1,true);
    //game.stage.scale.startFullScreen();
}

function update() {
    
    fundo1.tilePosition.x -= 0.5;
    fundo2.tilePosition.x -= 1;
    fundo3.tilePosition.x -= 2;

    jogador.body.velocity.x = 0;
    jogador.body.velocity.y = 0;

    if (cursors.up.isDown && !pulando)
    {
        som_pulo.play();
        pulando = true;
        jogador.loadTexture('pulando', 0);
        jogador.animations.add('pular');
        jogador.animations.pixelPerfect = true;
        jogador.animations.play('pular', 10, true);
    }
    
    if (pulando) {
        if (aux_pulo == 6000) {
            aux_pulo = 0;
            pulando = false;
            jogador.loadTexture('correndo', 0);
            jogador.animations.add('correr');
            jogador.animations.pixelPerfect = true;
            jogador.animations.play('correr', 10, true);
        }
        else {
            if (aux_pulo <= 2600)
                jogador.body.velocity.y = -500;
            else
                jogador.body.velocity.y = 400;
            aux_pulo+= 100;
        }
    }
    else {
        if (jogador.body.y > 600)
            jogador.body.velocity.y = -Math.abs(600-jogador.y);
        else
            jogador.body.velocity.y = Math.abs(600-jogador.y);
    }

    administra_atores(inimigos, 'inimigo');
    administra_atores(moedas, 'moeda');
    administrar_moedas();
    game.physics.collide(jogador, grupo, tratador_colisao, null, this);
}

function tratador_colisao(obj1, obj2) {
    if (obj2.name === 'moeda'){
        som_pulo.play();
        obj2.kill();
        contador++;
        qtde_moedas--;
        texto.setText("Moedas: " + contador);
    }
    else
    {
        obj1.kill();
        texto.setText("Game Over");
    }
}

function administrar_moedas() {
    console.log(qtde_moedas);
    if (qtde_moedas <= 0) {
        x = game.rnd.integerInRange(2, 10);
        eixox = 1024;
        for (i=0; i < x; i++) {
            criar_ator(moedas, 'moeda', eixox, 400);
            eixox+=50;
            qtde_moedas++;
        }
    }
}

function criar_ator(grupo_ator, nome_ator, x, y) {
    var ator = grupo.create(x, y, nome_ator);
    ator.name = nome_ator;
    ator.animations.add('correr');
    ator.animations.play('correr', 10, true);
    ator.body.pixelPerfect = true;
    grupo_ator[grupo_ator.length] = ator;
}

function administra_atores(grupo_ator, nome_ator) {
    for (i=0; i < grupo_ator.length; i++) {
        grupo_ator[i].body.velocity.x = -150;
        if (grupo_ator[i].body.x < -150) {
            grupo_ator[i].kill();
            grupo_ator.splice(i, 1);
            criar_ator(grupo_ator, nome_ator, 1024, 650);
        }
    }
}
