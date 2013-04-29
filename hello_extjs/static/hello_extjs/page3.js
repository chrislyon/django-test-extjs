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
	   
	var limitParPage = 15;

	var mesChampsDeDonnees = [
		{name: 'numero_enregistrement'},
		{name: 'nom_enregistrement'},
		{name: 'date_creation',type:'date',dateFormat:'Y-m-d'}
	];

	var monStore = new Ext.data.JsonStore({
		root: 'rows',
		idProperty: 'numero_enregistrement',
		fields:mesChampsDeDonnees,
		remoteSort : true,
		autoLoad:{
					params:{
						limit:limitParPage
		            }
				},
		url:'/hello_extjs/p3_load',
		sortInfo:{
			"field": "numero_enregistrement",
			"direction": "ASC"
			}
	});

	var mesColonnes = [
			{header: 'Identifiant', width: 20, dataIndex: 'numero_enregistrement',sortable: true},
			{header: 'Nom', width: 200, dataIndex: 'nom_enregistrement',sortable: true},
			{header: 'Date', width: 100, dataIndex: 'date_creation',xtype:'datecolumn',format:'d/m/Y',sortable: true},
			{header: 'Edit', width: 50, dataIndex: 'numero_enregistrement',sortable: false, renderer: renderIcon_mod },
			{header: 'Delete', width: 50, dataIndex: 'numero_enregistrement',sortable: false, renderer: renderIcon_del }
		];

	 var maPagination = new Ext.PagingToolbar({
		         store: monStore,  
		         pageSize: limitParPage,
		         displayInfo: true    
		     });

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
		title: 'Grille avec Pagination',
		bbar: maPagination
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
