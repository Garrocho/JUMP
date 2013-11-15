var game = new Phaser.Game(1024, 768, Phaser.AUTO, '', { preload: preload, create: create, update: update});
var fundo1, fundo2, fundo3;
var corredor;
var texto;
var grupo;
var contador;
var normal;
var inimigos = new Array();
var moedas = new Array();
var qtde_moedas;
var som_moeda, som_pulo;

function preload() {
     game.load.image('nuvem', 'assets/img/nuvem.png');
     game.load.image('montanha', 'assets/img/montanha.png');
     game.load.image('caminho', 'assets/img/caminho.png');
     game.load.spritesheet('moeda', 'assets/img/moedas.png', 44, 40, 10);
     game.load.spritesheet('correndo', 'assets/img/correndo.png', 75, 132, 14);
     game.load.spritesheet('inimigo', 'assets/img/inimigo.png', 75, 65, 4);
     game.load.spritesheet('jogar', 'assets/img/botao_jogar.png', 106, 42, 2);
     game.load.audio('musica', ['assets/sons/fase_1.wav']);
     game.load.audio('moeda', ['assets/sons/moeda.wav']);
     game.load.audio('pulo', ['assets/sons/pulo.ogg']);
}

function create() {
    fundo1 = game.add.tileSprite(0, 0, 1024, 512, 'nuvem');
    fundo2 = game.add.tileSprite(0, 220, 1024, 512, 'montanha');
    fundo3 = game.add.tileSprite(0, 520, 1024, 256, 'caminho');
    corredor = game.add.sprite(250, 580, 'correndo');
    corredor.animations.add('correr');
    corredor.animations.play('correr', 15, true);
    corredor.animations.pixelPerfect = true;
    corredor.body.collideWorldBounds = true;
    grupo = game.add.group();
    qtde_moedas = 0;
    pulando = false;

    contador = 0;
    normal = false;
    cont_pulo = 4800;

    texto = game.add.text(10, 10, "Moedas: " + contador, {
        font: "20px Arial",
        fill: "#ff0044",
        align: "center"
    });
    cursors = game.input.keyboard.createCursorKeys();
    //criar_ator(moedas, 'moeda', 1024, 580);
    criar_ator(inimigos, 'inimigo', 2024, 650);
    
    musica = game.add.audio('musica',1,true);
    som_moeda = game.add.audio('moeda',1,true);
    som_pulo = game.add.audio('pulo',1,true);
    administrar_moedas();
    musica.play('',0,1,true);
    game.stage.scale.startFullScreen();
}

function update() {
    fundo1.tilePosition.x -= 0.5;
    fundo2.tilePosition.x -= 1;
    fundo3.tilePosition.x -= 2;

    corredor.body.velocity.x = 0;

    if (cursors.up.isDown && corredor.body.y >= 580)
    {
        som_pulo.play();
        var pulo = game.add.tween(corredor);
        pulo.to({ y: 400 }, 500, Phaser.Easing.Linear.None, false);
        pulo.to({ y: 300 }, 600, Phaser.Easing.Linear.None, false);
        pulo.to({ y: 400 }, 600, Phaser.Easing.Linear.None, false);
        pulo.to({ y: 580 }, 500, Phaser.Easing.Linear.None, false);
        pulo.start();
    }

    administra_atores(inimigos, 'inimigo');
    administra_atores(moedas, 'moeda');
    administrar_moedas();
    game.physics.collide(corredor, grupo, tratador_colisao, null, this);
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
    ator.animations.pixelPerfect = true;
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
