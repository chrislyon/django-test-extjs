


Ext.onReady(function() {
       
       /**
         * create grid
         * 
         * @return void
         * @param column data in ExtJS format
         */
        var createGrid = function(columndata) {
            grid = Ext.create('Ext.grid.Panel', {
                store: store,
                columns: columndata,
                stripeRows: true,
                height:180,
                width:500,
                renderTo: 'grid-example',
                title:'Straw Hats Crew'
            });
        }
        
        /**
         * create store
         * 
         * @return void
         * @param field data in ExtJS format
         * @param values in ExtJS format
         */
        var createStore = function(fielddata, values) {
            store = Ext.create('Ext.data.ArrayStore', {
        fields: fielddata,
        data: values
            });
        }
        
        /**
         * get the data via ajax request
         * 
         * @return void
         */
        Ext.Ajax.request({
            url: '/testl/listed_config/',
            success: function(response){
                var data = Ext.decode(response.responseText);
                createStore(data.fielddata, data.values);
                createGrid(data.columndata);
            }
        });
    
});
