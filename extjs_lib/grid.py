from django.utils import simplejson
from collections import OrderedDict

## ---------------
## CLASS EXTGRID
## ---------------
class ExtGrid(object):
    """
        Class EXtGrid
        genere le script js pour une grid
    """
    def __init__(self):
        self.titre = "TITRE A CHANGER"
        self.width = 600
        self.height = 300
        self.renderTo = 'Ext.getBody()'
        self.pageSize = 10
        self.data_url = ''
        self.base_url = ''
        self.modif = True
        self.delete = True
        self.button_new = True
        self.button_new_url = self.base_url + '/cr'
        self.button_home = True
        self.button_home_url = '/'
        self.editing = False
        self.cols = []
        self.data = []

    def add_col(self, col):
        self.cols.append(col)

    def model_cols_name(self):
        r = []
        if not self.editing:
            r = simplejson.dumps([ c.name for c in self.cols ])
        else:
            for c in self.cols:
                if c.xtype == 'datefield':
                    r.append( "{name: '%s',type: 'date',dateFormat: 'd/m/y'}" % c.name )
                else:
                    r.append( "{name: '%s',type: 'string' }" % c.name )
            r = "[ %s ]" % ",".join(r)
        return r

    def render(self):
        scripts = ''
        ## Le debut et la fin
        ENTETE = "Ext.onReady(function(){ "
        FIN = """
        });
        """
        DEL_MOD = """
        //image path
        var IMG_MODIF = '/static/static/img/document-edit.png';
        var IMG_DELETE = '/static/static/img/edit-delete.png';

        //renderer function
        //Pour affichage d'un lien sur une image (modif + effacement)
        //
        function renderIcon_mod(val) {
            return '<a href="%s/mod/'+val+'"><img src="' + IMG_MODIF + '"></a>';
        }
        function renderIcon_del(val) {
            return '<a href="%s/del/'+val+'"><img src="' + IMG_DELETE + '"></a>';
        }

        """ % ( self.base_url, self.base_url )
        ## definition du model
        model = """
        Ext.define('GModel', {
        extend: 'Ext.data.Model',
        fields:%s
        });
        """
        if self.modif or self.delete:
            scripts += DEL_MOD
        ## Attention l'ordre des cols a de l'importance
        scripts += model % self.model_cols_name()
        ## Definition du store
        if not self.editing:
            store = """
            var CSRF_TOKEN = Ext.util.Cookies.get('csrftoken');
            var GStore = Ext.create('Ext.data.Store', {
            model: GModel,
            autoLoad: true,
            remoteSort: true,
            """
            store += "pageSize: %s," % self.pageSize
            proxy = """
            proxy: {
                type: 'ajax',
                actionMethods:'POST',
                url : '%s',
                extraParams: {
                        'csrfmiddlewaretoken':CSRF_TOKEN
                        },
                reader: {
                    type: 'json',
                    root: 'rows',
                    totalProperty: 'total'
                    }
                }
            """ % self.data_url
            store += proxy
            store += "});"
        else:
            ## Store avec possibilite de sauvegarde
            store = """
            var CSRF_TOKEN = Ext.util.Cookies.get('csrftoken');
            var MyWriter = new Ext.data.JsonWriter({
                                    type: 'json',
                                    encode: true,
                                    listful: true,
                                    writeAllFields: true,
                                    returnJson: true,
                                    root:'rows'
                                    });
            var GStore = Ext.create('Ext.data.Store', {
            model: GModel,
            autoLoad: true,
            autoSync: true,
            remoteSort: true,
            """
            store += "pageSize: %s," % self.pageSize
            proxy = """
            proxy: {
                type: 'ajax',
                actionMethods:'POST',
                //url: '%s',
                api: {
                    create: '%s/create',
                    read: '%s/read',
                    update: '%s/update',
                    destroy: '%s/destroy'
                    },
                extraParams: {
                        'csrfmiddlewaretoken':CSRF_TOKEN
                        },
                reader: {
                    type: 'json',
                    root: 'rows',
                    totalProperty: 'total',
                    successProperty: 'success',
                    messageProperty: 'message'
                    },
                writer: MyWriter,
                listeners: {
                    exception: function(proxy, response, operation){
                        Ext.MessageBox.show({
                            title: 'REMOTE EXCEPTION',
                            //msg: operation.getError(),
                            msg: 'Operation '+operation.action+':'+response.responseText,
                            icon: Ext.MessageBox.ERROR,
                            buttons: Ext.Msg.OK
                            });
                        }
                    }
                 },
//                 /*listeners: {
//                     update: function(proxy, operation){
//                                     Ext.each(operation.records, function(record){
//                                         if (record.dirty) {
//                                             record.commit();
//                                             }
//                                         });
//                                     alert(operation.action, operation.resultSet.message);
//                             },
//                     write: function(proxy, operation){
//                                     Ext.each(operation.records, function(record){
//                                         if (record.dirty) {
//                                             record.commit();
//                                             }
//                                         });
//                                     alert(operation.action, operation.resultSet.message);
//                         }
//                 } */

            """ % (self.data_url,self.data_url, self.data_url, self.data_url, self.data_url)
            store += proxy
            store += "});"
            store += """
            //var extraParams = [];
            //extraParams['csrfmiddlewaretoken'] = CSRF_TOKEN;
            //extraParams['toto'] = 'TUTU';
            //GStore.getProxy().setExtraParams.toto = 'TUTU';
            //GStore.load();

            Ext.Ajax.on('beforerequest', function(o,r) {
                 //r.params.csrfmiddlewaretoken = CSRF_TOKEN;
                 //r.params.csrftoken = CSRF_TOKEN;
               });
                        
            """
        #scripts += store % simplejson.dumps(self.data)
        ## ----------- fin du store
        scripts += store
        ## Definition de la grille
        grid_debut = """
        var GRID = Ext.create('Ext.grid.Panel', {
        """
        grid_debut += "renderTo: %s," % self.renderTo
        grid_debut += "store: GStore,"
        grid_debut += "width: %s," % self.width
        grid_debut += "height: %s," % self.height
        grid_debut += "title: '%s'," % self.titre
        grid_debut += """
            selType: 'cellmodel',
            plugins: [ Ext.create('Ext.grid.plugin.CellEditing', { clicksToEdit: 1 }) ],
        """
        grid_debut += "columns:["

        grid_fin = " });"

        scripts += grid_debut
        cols = [ c.to_grid() for c in self.cols ]
        if self.modif:
            cols.append("{header: 'Edit', width: 50, dataIndex: 'id',sortable: false, renderer: renderIcon_mod }")
        if self.delete:
            cols.append("{header: 'Delete', width: 50, dataIndex: 'id',sortable: false, renderer: renderIcon_del }")
        scripts += ',\n'.join(cols)
        scripts += '],'
        paging = """
            dockedItems: [{
                xtype: 'pagingtoolbar',
                store: GStore,
                dock: 'bottom',
                displayInfo: true
                """
        if self.editing or self.button_home or self.button_new:
            buttons = []
            if self.button_home:
                b_home = "{ xtype: 'button', text: 'HOME' , "
                b_home += """
                    handler: function(){ 
                        window.location = "%s"; } 
                        }
                    """ % self.button_home_url
                buttons.append( b_home )
            if self.button_new:
                b_new = "{ xtype: 'button', text: 'NEW' , "
                b_new += """
                    handler: function(){ 
                        window.location = "%s"; } 
                        }
                    """ % self.button_new_url
                buttons.append( b_new )
            if self.editing:
                b_new = "{ xtype: 'button', text: 'SAVE' , "
                b_new += """
                    handler: function(){ 
                        GStore.save();                    
                        pageState.ClearDirty();
                        } 
                        }
                    """
                buttons.append( b_new )
            paging += """
                }, {
                xtype: 'toolbar',
                dock: 'top',
                items: [ 
                """
            paging += ','.join(buttons)
            paging += " ]"
        paging += "}]"
        scripts += paging
        scripts += grid_fin

        return ENTETE+scripts+FIN
1
## ---------------
## CLASS CHAMP
## ---------------
class GridCol(object):
    """
        Colonne de la grille
    """
    def __init__(self, name, **kwargs):
        ## Transmises
        self.name = name
        self.text = kwargs.get('text', 'Champ %s ' % name )
        self.dataIndex = kwargs.get('dataIndex', name)
        self.width = kwargs.get('width',100)
        self.hidden = kwargs.get('hidden', False)
        self.hideable = kwargs.get('hideable', True)
        self.sortable = kwargs.get('sortable', False)
        self.renderer = kwargs.get('renderer', None)
        self.editor = kwargs.get('editor', None)
        ## Non transmises
        self.xtype = kwargs.get('xtype', None)
        self.store = kwargs.get('store', [[ 'Choix 1' , 'CHOIX1'], ['Choix 2', 'CHOIX 2']] )

    def to_grid(self):
        d = {   "hideable": self.hideable, 
                "sortable": self.sortable, 
                "name": self.name, 
                "text": self.text, 
                "width": self.width, 
                "dataIndex": self.dataIndex, 
                "hidden": self.hidden, 
                "editor": self.editor, 
                "renderer": self.renderer
            }
        r = simplejson.dumps(d)
        #{   header: 'Available',
        #    dataIndex: 'availDate',
        #    width: 95,
        #    renderer: Ext.util.Format.dateRenderer('M d, Y'),
        #    editor: {
        #        xtype: 'datefield',
        #        format: 'm/d/y',
        #        minValue: '01/01/06',
        #        disabledDays: [0, 6],
        #        disabledDaysText: 'Plants are not available on the weekends'
        #}

        ## La gestion de la saisie  date + temps ne fonctionne pas
        #if self.xtype == 'datetimefield':
        #    renderer = "renderer: Ext.util.Format.dateRenderer('d/m/y')"
        #    r = r.replace('"renderer": null', renderer)
        #    editor = "editor: { xtype: 'datefield', format: 'd/m/y' }"
        #    r = r.replace('"editor": null', editor)

        if self.xtype == 'datefield':
            renderer = "renderer: Ext.util.Format.dateRenderer('d/m/y')"
            r = r.replace('"renderer": null', renderer)
            editor = "editor: { xtype: 'datefield', format: 'd/m/y' }"
            r = r.replace('"editor": null', editor)

        if self.xtype == 'combo':
            editor = "editor: new Ext.form.field.ComboBox({ typeAhead: true, triggerAction: 'all', store: %s })" % [ list(x) for x in self.store ]
            r = r.replace('"editor": null', editor)
        return r

def test2():
    g = ExtGrid()
    g.add_col( GridCol('name') )
    g.add_col( GridCol('email') )
    g.add_col( GridCol('phone') )
    g.add_col( GridCol('zipcode') )
    g.titre = "Nouvelle Grille Auto"

    ## Pour Test
    g.data = [
        { 'name': 'Lisa', 'email': 'lisa@simpsons.com', 'phone': '555-111-1224' , 'zipcode':"010101" },
        { 'name': 'Bart', 'email': 'bart@simpsons.com', 'phone': '555-222-1234' , 'zipcode':"010101" },
        { 'name': 'Homer', 'email': 'home@simpsons.com', 'phone': '555-222-1244' , 'zipcode':"010101" },
        { 'name': 'Marge', 'email': 'marge@simpsons.com', 'phone': '555-222-1254' , 'zipcode':"010101" }
    ]
    print g.render()

if __name__ == '__main__':
    #tchamp()
    #test()
    test2()
