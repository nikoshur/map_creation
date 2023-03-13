import numpy            

"""This creates a new print layout"""
project = QgsProject.instance()             #gets a reference to the project instance
manager = project.layoutManager()           #gets a reference to the layout manager
layout = QgsPrintLayout(project)            #makes a new print layout object, takes a QgsProject as argument
layoutName = "PrintLayout"

layouts_list = manager.printLayouts()
for layout in layouts_list:
    if layout.name() == layoutName:
        manager.removeLayout(layout)
        
layout = QgsPrintLayout(project)
layout.initializeDefaults()                 #create default map canvas
layout.setName(layoutName)
manager.addLayout(layout)

"""This adds a map item to the Print Layout"""
map = QgsLayoutItemMap(layout)
map.setRect(20, 20, 20, 20)  
#Set Extent
#rectangle = QgsRectangle(1355502, -46398, 1734534, 137094)         #an example of how to set map extent with coordinates
#map.setExtent(rectangle)
canvas = iface.mapCanvas()
map.setExtent(canvas.extent())                  #sets map extent to current map canvas
layout.addLayoutItem(map)
#Move & Resize
map.attemptMove(QgsLayoutPoint(5, 27, QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(239, 178, QgsUnitTypes.LayoutMillimeters))

"""Gathers active layers to add to legend"""
#Checks layer tree objects and stores them in a list. This includes csv tables
checked_layers = [layer.name() for layer in QgsProject().instance().layerTreeRoot().children() if layer.isVisible()]
print(f"Adding {checked_layers} to legend." )
#get map layer objects of checked layers by matching their names and store those in a list
layersToAdd = [layer for layer in QgsProject().instance().mapLayers().values() if layer.name() in checked_layers]
root = QgsLayerTree()
for layer in layersToAdd:
    #add layer objects to the layer tree
    root.addLayer(layer)
    
"""This adds a legend item to the Print Layout"""
legend = QgsLayoutItemLegend(layout)
legend.model().setRootGroup(root)
layout.addLayoutItem(legend)
legend.attemptMove(QgsLayoutPoint(246, 5, QgsUnitTypes.LayoutMillimeters))

"""This symbolizes raster layer in legend"""
#defining raster layer to work with (active layer in layer panel)
layer = iface.activeLayer()
print("Active Layer: ", layer.name())
provider = layer.dataProvider()
extent = layer.extent()

"""Get min and max values of a given attribute column (index)"""
min_val = provider.minimumValue(index)
max_val = provider.maximumValue(index)
#features_list = provider.fields().names()
#print("features list =", features_list)
print("min value =", min_val)
print("max value =", max_val)

# create a QGIS symbol variable
symbol1 = QgsSymbol.defaultSymbol(layer.geometryType())
symbol2 = QgsSymbol.defaultSymbol(layer.geometryType())
symbol3 = QgsSymbol.defaultSymbol(layer.geometryType())
symbol4 = QgsSymbol.defaultSymbol(layer.geometryType())
symbol5 = QgsSymbol.defaultSymbol(layer.geometryType())

# create a tuple to save the style to add to the class
layer_style = {}
layer_style['outline'] = '#000000'

# replace default symbol layer with the configured one

layer_style['color'] = '#CCDBFF'
symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
symbol1.changeSymbolLayer(0, symbol_layer)
#----------------------------------------------------------
layer_style['color'] = '#99B8FF'
symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
symbol2.changeSymbolLayer(0, symbol_layer)
#----------------------------------------------------------
layer_style['color'] = '#6694FF'
symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
symbol3.changeSymbolLayer(0, symbol_layer)
#----------------------------------------------------------
layer_style['color'] = '#3371FF'
symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
symbol4.changeSymbolLayer(0, symbol_layer)
#----------------------------------------------------------
layer_style['color'] = '#004DFF'
symbol_layer = QgsSimpleFillSymbolLayer.create(layer_style)
symbol5.changeSymbolLayer(0, symbol_layer)

palette_range1 = QgsRendererRange(float(first_quintile_min), float(first_quintile_max), symbol1, f"{first_quintile_min} - {first_quintile_max}")
palette_range2 = QgsRendererRange(float(second_quintile_max), float(second_quintile_max), symbol2, f"{second_quintile_min} - {second_quintile_max}")
palette_range3 = QgsRendererRange(float(second_quintile_max), float(third_quintile_max), symbol3, f"{third_quintile_min} - {third_quintile_max}")
palette_range4 = QgsRendererRange(float(second_quintile_max), float(fourth_quintile_max), symbol4, f"{fourth_quintile_min} - {fourth_quintile_max}")
palette_range5 = QgsRendererRange(float(second_quintile_max), float(fifth_quintile_max), symbol5, f"{fifth_quintile_min} - {fifth_quintile_max}")

d_palettes = []
d_palettes.append(palette_range1)
d_palettes.append(palette_range2)
d_palettes.append(palette_range3)
d_palettes.append(palette_range4)
d_palettes.append(palette_range5)

attr_list = ['0712', '0122', '0113', '0421', '0621', '0221', '0322', '0411', '0611', '0912', '0932', '0312', '0511', '0731', '0331', '0213', '0522', '0811', '0222', '0931', '0431', '1038', '0632', '1036', '0832', '0212', '1022', '0911', '0921', '0432', 'CGOL', '0722', '0332', '0231', '0721', '0121', '0531', '0541', '0112', '0512', '0732', '0131', '0321', '0412', '0812', '0521', '1032', '0711', '1031', '0211', '1034', '0123', '0822', '0622', '0922', '1011', '1035', '1037', '0311', '0422', '0631', '0111', '1021', '0831', '0232', '0821']

for attr in attr_list:

    renderer = QgsGraduatedSymbolRenderer(attrName = attr, ranges = d_palettes)

    #renderer = QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, shader)    #renders selected raster layer
    layer.setRenderer(renderer)
    layer.triggerRepaint()

    """This adds labels to the map"""
    title = QgsLayoutItemLabel(layout)
    title.setText("Title Here")
    title.setFont(QFont("Arial", 28))
    title.adjustSizeToText()
    layout.addLayoutItem(title)
    title.attemptMove(QgsLayoutPoint(10, 4, QgsUnitTypes.LayoutMillimeters))

    subtitle = QgsLayoutItemLabel(layout)
    subtitle.setText("Subtitle Here")
    subtitle.setFont(QFont("Arial", 17))
    subtitle.adjustSizeToText()
    layout.addLayoutItem(subtitle)
    subtitle.attemptMove(QgsLayoutPoint(11, 20, QgsUnitTypes.LayoutMillimeters))   #allows moving text box

    credit_text = QgsLayoutItemLabel(layout)
    credit_text.setText("Credit Text Here")
    credit_text.setFont(QFont("Arial", 10))
    credit_text.adjustSizeToText()
    layout.addLayoutItem(credit_text)
    credit_text.attemptMove(QgsLayoutPoint(246, 190, QgsUnitTypes.LayoutMillimeters))

    """This exports a Print Layout as an image"""
    manager = QgsProject.instance().layoutManager()     #this is a reference to the layout Manager, which contains a list of print layouts

    layout = manager.layoutByName(layoutName)         #this accesses a specific layout, by name (which is a string)

    exporter = QgsLayoutExporter(layout)                #this creates a QgsLayoutExporter object
    #exporter.exportToPdf('C:/asd/TestLayout' + 'attr' + '.pdf', QgsLayoutExporter.PdfExportSettings())      #this exports a pdf of the layout object
    exporter.exportToImage('C:/asd/TestLayout' + attr + '.png', QgsLayoutExporter.ImageExportSettings())      #this exports a pdf of the layout object





