//
// Le controleur
//

Ext.define('AM.controller.Users', {
	extend: 'Ext.app.Controller',

	// definition du Store du model et des vues
    stores: ['Users'],
    models: ['User'],
	views: [ 'user.List', 'user.Edit' ],


	// definition des fonctions
	// La fonction init permet de declarer les actions 
	init: function() {
			  console.log("INIT ");
			  this.control({
				  			// Dbl-Click sur une ligne
						  'viewport > userlist': { itemdblclick: this.editUser },
				  			// Button Save
						  'useredit button[action=save]': { click: this.updateUser }
					  });
				},

	// Les fonctions associées
	updateUser: function(button) {
			console.log('clicked the Save button');
			var win = button.up('window'),
			form    = win.down('form'),
			record  = form.getRecord(),
			values  = form.getValues();

			record.set(values);
			win.close();
			// synchronize the store after editing the record
			this.getUsersStore().sync();
			 },
	editUser: function(grid, record) {
			console.log('Double clicked on ' + record.get('name'));
			var view = Ext.widget('useredit');
			view.down('form').loadRecord(record);
			}
});
