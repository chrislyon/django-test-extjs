alert("hello");
Ext.onReady(function(){

var viewport = new Ext.Viewport({
        layout: 'border',
        renderTo: Ext.getBody(),
        items: [{

        //region: 'north',
        //xtype: 'panel',
        //html: 'North'

        region: "north",
        height: 100,
        xtype: 'toolbar',
        items: [{
        xtype: 'tbspacer'
        },{
        xtype: 'tbbutton',
        text: 'Button',
        handler: function(btn){
            btn.disable();
        }
        },{
            xtype: 'tbfill'
        },
        // more toolbar items here //
        ]
    },{
        region: 'west',
        xtype: 'panel',
        split: true,
        width: 200,
        html: 'West'
    },{
        region: 'center',
        xtype: 'panel',
        html: 'Center'
    },{
        region: 'east',
        xtype: 'panel',
        split: true,
        width: 200,
        html: 'East'
    },{
        region: 'south',
        xtype: 'panel',
        html: 'South'
    }]
    });
    viewport.render(document.body);

    });
