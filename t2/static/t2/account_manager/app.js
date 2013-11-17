//
// Definition de l'application
// C'est ce scripts qui sera lancé par la page Web
//

Ext.application({
    requires: ['Ext.container.Viewport'],
    name: 'AM',

	// Pour django bien mettre le chemin complet /static/<app>/...
    appFolder: '/static/t2/account_manager/app',

	// Definition du controller
	controllers: [ 'Users' ],

	// Cette fonction demarre l'application 
	launch: function() {
	           Ext.create('Ext.container.Viewport', {
				           layout: 'fit',
			               items: { xtype: 'userlist' }
			           });
			       }
});
