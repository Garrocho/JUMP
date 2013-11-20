BasicGame = {};

BasicGame.Inicio = function (game) {

};

BasicGame.Inicio.prototype = {

    preload: function () {
        this.load.image('background', 'assets/img/background.png');
        this.load.image('barra', 'assets/img/barra.png');
    },

    create: function () {
        this.game.input.maxPointers = 1;
        this.game.stage.disableVisibilityChange = true;

        if (this.game.device.desktop)
        {
            this.game.stage.scale.pageAlignHorizontally = true;
            this.game.stage.scaleMode = Phaser.StageScaleMode.SHOW_ALL;
        }
        else
        {
            this.game.stage.scaleMode = Phaser.StageScaleMode.SHOW_ALL;
            this.game.stage.scale.minWidth = 480;
            this.game.stage.scale.minHeight = 260;
            this.game.stage.scale.maxWidth = 1024;
            this.game.stage.scale.maxHeight = 768;
            this.game.stage.scale.forceLandscape = true;
            this.game.stage.scale.pageAlignHorizontally = true;
            this.game.stage.scale.setScreenSize(true);
        }
        this.game.state.start('PreCarregamento');
    }
};
