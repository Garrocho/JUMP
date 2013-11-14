var game = new Phaser.Game(1024, 645, Phaser.AUTO, '', { preload: preload, create: create, update: update});
var fundo1, fundo2;
var corredor;
var texto;
var moedas = new Array();
var inimigos = new Array();
var grupo;
var contador;
var normal;
var audio_moeda;

function preload() {
     game.load.image('nuvem', 'assets/img/nuvem.png');
     game.load.image('montanha', 'assets/img/montanha.png');
     game.load.spritesheet('moeda', 'assets/img/moedas.png', 44, 40, 10);
     game.load.spritesheet('correndo', 'assets/img/correndo.png', 75, 132, 14);
     game.load.spritesheet('inimigo', 'assets/img/inimigo.png', 75, 65, 4);
     game.load.spritesheet('jogar', 'assets/img/botao_jogar.png', 106, 42, 2);
     game.load.audio('musica', ['assets/sons/fase_1.wav']);
}

function create() {
    fundo1 = game.add.tileSprite(0, 0, 1024, 512, 'nuvem');
    fundo2 = game.add.tileSprite(0, 200, 1024, 512, 'montanha');
    corredor = game.add.sprite(150, 10, 'correndo');
    corredor.animations.add('correr');
    corredor.animations.play('correr', 15, true);
    corredor.animations.pixelPerfect = true;
    corredor.body.gravity.y = 10;
    corredor.body.bounce.y = 0.4;
    corredor.body.collideWorldBounds = true;
    grupo = game.add.group();

    for (var i = 0; i < 50; i++)
    {
        if (i%2 == 0) {
            ator = grupo.create(500+i*850, 512, 'moeda');
            ator.animations.add('transicao');
            ator.animations.play('transicao', 10, true);
            ator.animations.pixelPerfect = true;
            moedas[moedas.length] = ator;
        }
        else {
            ator = grupo.create(500+i*850, 270, 'inimigo');
            ator.animations.add('transicao');
            ator.animations.play('transicao', 5, true);
            ator.animations.pixelPerfect = true;
            ator.body.gravity.y = 10;
            ator.body.bounce.y = 0.4;
            ator.body.collideWorldBounds = true;
            inimigos[inimigos.length] = ator;
        }
    }

    contador = 0;
    normal = false;

    texto = game.add.text(10, 10, "Moedas: " + contador, {
        font: "20px Arial",
        fill: "#ff0044",
        align: "center"
    });
    //music = game.add.audio('musica',1,true);
    //music.play('jogo.mp3', 0, 1, true);
    //game.stage.scale.startFullScreen();
    cursors = game.input.keyboard.createCursorKeys();
}

function update() {

    fundo1.tilePosition.x -= 0.5;
    fundo2.tilePosition.x -= 1;
    //corredor.body.velocity.x = 0;
    //corredor.body.velocity.y = 0;

    for (i=0; i < moedas.length; i++)
        moedas[i].body.velocity.x = -120;

    for (i=0; i < inimigos.length; i++)
        inimigos[i].body.velocity.x = -120;

    corredor.body.velocity.x = 0;

    if (cursors.up.isDown)
    {
            corredor.body.velocity.y = -400;
    }
    else if (cursors.down.isDown)
    {
        // game.camera.y += 4;
    }

    game.physics.collide(corredor, grupo, tratador_colisao, null, this);
}

function tratador_colisao(obj1, obj2) {
    obj2.kill();
    contador++;
    texto.setText("Moedas: " + contador);
}
