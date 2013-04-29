from django.utils import simplejson
from string import replace

SCRIPT_EXTJS = """
Ext.onReady(function(){

Ext.define('User', {
extend: 'Ext.data.Model',
fields:${champs}
});

var userStore = Ext.create('Ext.data.Store', {
model: 'User',
data: [
{ name: 'Lisa', email: 'lisa@simpsons.com', phone: '555-111-1224' },
{ name: 'Bart', email: 'bart@simpsons.com', phone: '555-222-1234' },
{ name: 'Homer', email: 'home@simpsons.com', phone: '555-222-1244' },
{ name: 'Marge', email: 'marge@simpsons.com', phone: '555-222-1254' }
]
});

Ext.create('Ext.grid.Panel', {
    renderTo: Ext.getBody(),
    store: userStore,
    width: 400,
    height: 200,
    title: '${titre}',
    columns: [
        {
            text: 'Name',
            width: 100,
            sortable: false,
            hideable: false,
            dataIndex: '${}'
        },
        {
            text: 'Email Address',
            width: 150,
            dataIndex: '${di_email}',
            hidden: true
        },
        {
            text: 'Phone Number',
            flex: 1,
            dataIndex: '%s'
        }
    ]
    });

});


"""
f = ['name', 'email', 'tel']
print SCRIPT_EXTJS % ( sim:plejson.dumps(f), 'TITRE GRILLE', f[0], f[1], f[2] )
