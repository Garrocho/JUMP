var game = new Phaser.Game(1024, 645, Phaser.AUTO, '', { preload: preload, create: create, update: update});
var fundo1, fundo2;
var corredor;
var texto;
var grupo;
var contador;
var normal;
var inimigos = new Array();
var moedas = new Array();

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
    corredor = game.add.sprite(250, 10, 'correndo');
    corredor.animations.add('correr');
    corredor.animations.play('correr', 15, true);
    corredor.animations.pixelPerfect = true;
    corredor.body.gravity.y = 10;
    corredor.body.bounce.y = 0.4;
    corredor.body.collideWorldBounds = true;
    grupo = game.add.group();

    contador = 0;
    normal = false;

    texto = game.add.text(10, 10, "Moedas: " + contador, {
        font: "20px Arial",
        fill: "#ff0044",
        align: "center"
    });
    cursors = game.input.keyboard.createCursorKeys();
    criar_ator(moedas, 'moeda', 2024, 580);
    criar_ator(inimigos, 'inimigo', 1024, 580);
}

function update() {
    fundo1.tilePosition.x -= 0.5;
    fundo2.tilePosition.x -= 1;

    corredor.body.velocity.x = 0;

    if (cursors.up.isDown)
    {
        corredor.body.velocity.y = -400;
    }
    atualiza_atores();
    game.physics.collide(corredor, grupo, tratador_colisao, null, this);
}

function tratador_colisao(obj1, obj2) {
    if (obj2.name === 'moeda'){
        obj2.kill();
        contador++;
        texto.setText("Moedas: " + contador);
        criar_ator(moedas, 'moeda', 1024, 380);
    }
    else
    {
        obj1.kill();
        texto.setText("Game Over");
    }
}

function criar_ator(grupo_ator, nome_ator, x, y) {
    var ator = grupo.create(x, y, nome_ator);
    ator.name = nome_ator;
    ator.animations.add('correr');
    ator.animations.play('correr', 5, true);
    ator.animations.pixelPerfect = true;
    grupo_ator[grupo_ator.length] = ator;
}

function atualiza_atores() {
    for (i=0; i < inimigos.length; i++)
        inimigos[i].body.velocity.x = -150;

    for (i=0; i < moedas.length; i++)
        moedas[i].body.velocity.x = -150;
}
