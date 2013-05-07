//image path
//var IMG_EMAIL = '/gridcell-with-image/img/email_link.png';
var IMG_MODIF = '/static/static/img/document-edit.png';
var IMG_DELETE = '/static/static/img/edit-delete.png';

//renderer function
 function renderIcon_mod(val) {
	 return '<a href="/hello_extjs/mod/'+val+'"><img src="' + IMG_MODIF + '"></a>';
 }
 function renderIcon_del(val) {
	 return '<a href="/hello_extjs/del/'+val+'"><img src="' + IMG_DELETE + '"></a>';
 }

Ext.onReady(function(){
	   
	var mesChampsDeDonnees = [
		{name: 'numero_enregistrement'},
		{name: 'nom_enregistrement'},
		{name: 'date_creation',type:'date',dateFormat:'Y-m-d'}
	];

	var mesDonnees = {
		rows:[
			{numero_enregistrement: 1,nom_enregistrement: 'Premier enregistrement',date_creation: '2011-03-13'},
			{numero_enregistrement: 2,nom_enregistrement: 'Deuxieme enregistrement',date_creation: '2011-03-14'},
			{numero_enregistrement: 3,nom_enregistrement: 'Troisième enregistrement',date_creation: '2011-03-15'}
		]
	}

	var monStore = new Ext.data.JsonStore({
		root: 'rows',
		idProperty: 'numero_enregistrement',
		fields:mesChampsDeDonnees,
		// si les donnes sont dans le script
		//data:mesDonnees
		// grille dynamique
		autoLoad:true,
		url:'/hello_extjs/p2_load'
	});


	var mesColonnes = [
			{header: 'Identifiant', width: 200, dataIndex: 'numero_enregistrement',sortable: true},
			{header: 'Nom', width: 200, dataIndex: 'nom_enregistrement',sortable: true},
			{header: 'Date', width: 200, dataIndex: 'date_creation',xtype:'datecolumn',format:'d/m/Y',sortable: true},
			{header: 'Edit', width: 30, dataIndex: 'numero_enregistrement',sortable: false, renderer: renderIcon_mod },
			{header: 'Delete', width: 30, dataIndex: 'numero_enregistrement',sortable: false, renderer: renderIcon_del }
		];

	var monGridPanel = new Ext.grid.GridPanel({
		viewConfig: {
			forceFit: true
		},
		// sinon pas de scrolling vertical
		autoHeight:false,
		renderTo:Ext.getBody(),
		store: monStore,
		columns:mesColonnes,
		tbar: new Ext.Toolbar(),
		width: 800,
		height: 500,
		frame: true,
		title: 'Titre de la grille + TEST LAYOUT'
	});

	var toolbar = monGridPanel.getTopToolbar();
	    toolbar.add(new Ext.Toolbar.Button({
						text:'HOME',
						handler: function(){
								       Ext.Msg.alert('BUTTON', 'HOME');
									      }
						}
						));  

	    toolbar.add(new Ext.Toolbar.Button({
						text:'NEW',
						handler: function(){
								       Ext.Msg.alert('BUTTON', 'NEW');
									      }
						}
						));  

	    toolbar.add(new Ext.Toolbar.Button({
						text:'PRINT',
						handler: function(){
								       Ext.Msg.alert('BUTTON', 'PRINT');
									      }
						}
						));  

	monGridPanel.show();
}); 
